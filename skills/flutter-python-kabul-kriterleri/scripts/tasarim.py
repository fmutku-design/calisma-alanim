#!/usr/bin/env python3
"""Kullanıcının verdiği tasarımı ölçülebilir hale getirir ve koda uyumunu ölçer.

Kullanım:
    python tasarim.py dogrula  --proje .            tasarim.json + ekranlar.json şemasını denetler
    python tasarim.py uret     --proje .            Dart tasarım sabitlerini, font yükleyiciyi, yerleşim ve
                                                    ekran görüntüsü testlerini tasarim.json/ekranlar.json'dan üretir
    python tasarim.py tablo    --proje .            Onay için tasarım değerlerini ve ekran yerleşimini tablo olarak basar
    python tasarim.py denetle  --proje . [--olcumler olcumler.json]
                                                    T1 sabit renk, T2 sabit ölçü, T3 üretilmiş dosya uyumsuzluğu

Tasarımın tek kaynağı kullanıcıdır: her tasarım değeri 'kullanici:' kaynağı taşır. Claude tasarım değeri önermez.
Sadece Python standart kütüphanesi kullanılır.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

URETILMIS_BASLIK = "// ÜRETİLMİŞ DOSYA — elle düzenleme. Kaynak: {kaynak} (scripts/tasarim.py uret)"
DART_TOKENS = "lib/cekirdek/tema/tasarim.g.dart"
FONT_YARDIMCI = "test/yardimci/tasarim_fontlari.dart"
YERLESIM_KLASORU = "test/yerlesim"
GORUNTU_KLASORU = "test/goruntu"

ZORUNLU_GRUPLAR = ("renk", "yazi", "bosluk", "kose")
SAYISAL_GRUPLAR = ("bosluk", "kose", "bilesen")
ID_RE = re.compile(r"^[a-z][A-Za-z0-9]*$")
HEX_RE = re.compile(r"^#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")
KAYNAK_RE = re.compile(r"^kullanici:\S+")


def json_yukle(yol: Path):
    if not yol.is_file():
        return None
    return json.loads(yol.read_text(encoding="utf-8"))


def sayi_mi(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _dart_sayi(x: float) -> str:
    return str(int(x)) if float(x).is_integer() else repr(float(x))


# ---------------------------------------------------------------- Doğrulama

def dogrula(tasarim: dict | None, ekranlar: dict | None) -> list[str]:
    h: list[str] = []
    if tasarim is None:
        return ["tasarim.json yok. Tasarım kullanıcıdan gelmeden kod yazılmaz — kullanıcıdan tasarımı iste."]

    def kaynak_kontrol(yer: str, d: dict) -> None:
        k = str(d.get("kaynak", ""))
        if not KAYNAK_RE.match(k):
            h.append(f"{yer}: kaynak '{k}' geçersiz. Tasarım değerleri yalnızca 'kullanici:<nerede>' kaynaklı olabilir.")

    for grup in ZORUNLU_GRUPLAR:
        if not isinstance(tasarim.get(grup), dict) or not tasarim[grup]:
            h.append(f"'{grup}' grubu eksik veya boş — kullanıcıya sor.")

    font = tasarim.get("font")
    if not isinstance(font, dict) or not font.get("aile") or not font.get("dosyalar"):
        h.append("'font' eksik: aile adı ve font dosyaları (assets yolu + ağırlık) kullanıcıdan alınmalı.")
    else:
        kaynak_kontrol("font", font)
        for i, f in enumerate(font.get("dosyalar", [])):
            if not str(f.get("yol", "")).startswith("assets/"):
                h.append(f"font.dosyalar[{i}]: yol 'assets/' ile başlamalı (offline, uygulamaya gömülü).")
            if f.get("agirlik") not in range(100, 1000, 100):
                h.append(f"font.dosyalar[{i}]: agirlik 100–900 arası 100'ün katı olmalı.")

    renkler = tasarim.get("renk", {}) or {}
    for ad, t in renkler.items():
        if not ID_RE.match(ad):
            h.append(f"renk.{ad}: ad camelCase olmalı (ör. birincilKoyu).")
        if not isinstance(t, dict) or not HEX_RE.match(str(t.get("deger", ""))):
            h.append(f"renk.{ad}: deger '#RRGGBB' veya '#AARRGGBB' olmalı.")
        else:
            kaynak_kontrol(f"renk.{ad}", t)

    for ad, t in (tasarim.get("yazi", {}) or {}).items():
        if not ID_RE.match(ad):
            h.append(f"yazi.{ad}: ad camelCase olmalı.")
        if not isinstance(t, dict):
            h.append(f"yazi.{ad}: nesne olmalı.")
            continue
        kaynak_kontrol(f"yazi.{ad}", t)
        if not sayi_mi(t.get("boyut")) or t["boyut"] <= 0:
            h.append(f"yazi.{ad}: boyut (sp) pozitif sayı olmalı.")
        if t.get("agirlik") not in range(100, 1000, 100):
            h.append(f"yazi.{ad}: agirlik 100–900 arası 100'ün katı olmalı.")
        if "satir_yuksekligi" in t and (not sayi_mi(t["satir_yuksekligi"]) or t["satir_yuksekligi"] <= 0):
            h.append(f"yazi.{ad}: satir_yuksekligi (sp) pozitif sayı olmalı.")
        if t.get("renk") not in renkler:
            h.append(f"yazi.{ad}: renk '{t.get('renk')}' renk grubunda tanımlı değil.")

    for grup in SAYISAL_GRUPLAR:
        for ad, t in (tasarim.get(grup, {}) or {}).items():
            if not ID_RE.match(ad):
                h.append(f"{grup}.{ad}: ad camelCase olmalı.")
            if not isinstance(t, dict) or not sayi_mi(t.get("deger")) or t["deger"] < 0:
                h.append(f"{grup}.{ad}: deger (dp) sıfır veya pozitif sayı olmalı.")
            else:
                kaynak_kontrol(f"{grup}.{ad}", t)

    if ekranlar is None:
        h.append("ekranlar.json yok. Her ekranın yerleşimi kullanıcının tasarımından çıkarılıp yazılmalı.")
        return h
    uyg = ekranlar.get("uygulama", {})
    for alan in ("tema_import", "tema"):
        if not uyg.get(alan):
            h.append(f"ekranlar.json: uygulama.{alan} eksik.")
    boyut = ekranlar.get("ekran_boyutu", {})
    for alan in ("genislik", "yukseklik", "piksel_orani"):
        if not sayi_mi(boyut.get(alan)) or boyut[alan] <= 0:
            h.append(f"ekranlar.json: ekran_boyutu.{alan} pozitif sayı olmalı.")
    if boyut:
        kaynak_kontrol("ekran_boyutu", boyut)
    if not sayi_mi(ekranlar.get("tolerans_dp")) or ekranlar["tolerans_dp"] < 0:
        h.append("ekranlar.json: tolerans_dp sayı olmalı (kullanıcı onaylı).")
    if not ekranlar.get("ekranlar"):
        h.append("ekranlar.json: 'ekranlar' listesi boş.")
    adlar: set[str] = set()
    for e in ekranlar.get("ekranlar", []):
        ad = e.get("ad", "?")
        if not ID_RE.match(str(ad)):
            h.append(f"ekran '{ad}': ad camelCase olmalı.")
        if ad in adlar:
            h.append(f"ekran '{ad}': ad tekrar ediyor.")
        adlar.add(ad)
        kaynak_kontrol(f"ekran {ad}", e)
        for alan in ("widget", "import"):
            if not e.get(alan):
                h.append(f"ekran {ad}: '{alan}' eksik.")
        bilesenler = e.get("bilesenler") or []
        if not bilesenler:
            h.append(f"ekran {ad}: bilesenler boş.")
        anahtarlar: set[str] = set()
        for b in bilesenler:
            a = b.get("anahtar", "")
            if not a or not str(a).startswith(f"{ad}."):
                h.append(f"ekran {ad}: bileşen anahtarı '{a}' '{ad}.' ile başlamalı.")
            if a in anahtarlar:
                h.append(f"ekran {ad}: anahtar '{a}' tekrar ediyor.")
            anahtarlar.add(a)
            if not isinstance(b.get("sira"), int):
                h.append(f"{a}: sira (yukarıdan aşağı sıra numarası) tam sayı olmalı.")
            if not isinstance(b.get("adet", 1), int) or b.get("adet", 1) < 1:
                h.append(f"{a}: adet ≥ 1 tam sayı olmalı.")
            for alan in ("yukseklik", "genislik", "ust", "sol"):
                if alan in b and (not sayi_mi(b[alan]) or b[alan] < 0):
                    h.append(f"{a}: {alan} (dp) sıfır veya pozitif sayı olmalı.")
            if not any(alan in b for alan in ("yukseklik", "genislik", "ust", "sol")):
                h.append(f"{a}: en az bir ölçü (yukseklik/genislik/ust/sol) olmalı — ölçüsüz bileşen yerleşimi tahmine bırakır.")
    return h


# ---------------------------------------------------------------- Üretim

def _sinif(ad: str, satirlar: list[str]) -> str:
    return f"abstract final class {ad} {{\n" + "\n".join(satirlar) + "\n}\n"


def dart_tokens(tasarim: dict) -> str:
    aile = tasarim["font"]["aile"]
    parcalar = [URETILMIS_BASLIK.format(kaynak="tasarim.json"), "import 'package:flutter/material.dart';", ""]
    renk = []
    for ad, t in tasarim["renk"].items():
        hx = t["deger"].lstrip("#")
        hx = ("FF" + hx) if len(hx) == 6 else hx
        renk.append(f"  static const Color {ad} = Color(0x{hx.upper()});")
    parcalar.append(_sinif("TasarimRenk", renk))
    yazi = []
    for ad, t in tasarim["yazi"].items():
        ozellik = [f"fontFamily: '{aile}'", f"fontSize: {_dart_sayi(t['boyut'])}",
                   f"fontWeight: FontWeight.w{t['agirlik']}"]
        if "satir_yuksekligi" in t:
            ozellik.append(f"height: {_dart_sayi(t['satir_yuksekligi'])} / {_dart_sayi(t['boyut'])}")
        if "harf_araligi" in t:
            ozellik.append(f"letterSpacing: {_dart_sayi(t['harf_araligi'])}")
        ozellik.append(f"color: TasarimRenk.{t['renk']}")
        yazi.append(f"  static const TextStyle {ad} = TextStyle({', '.join(ozellik)});")
    parcalar.append(_sinif("TasarimYazi", yazi))
    for grup, sinif in (("bosluk", "TasarimBosluk"), ("kose", "TasarimKose"), ("bilesen", "TasarimBilesen")):
        ogeler = [f"  static const double {ad} = {_dart_sayi(t['deger'])};" for ad, t in (tasarim.get(grup) or {}).items()]
        if ogeler:
            parcalar.append(_sinif(sinif, ogeler))
    return "\n".join(parcalar)


def font_yardimci(tasarim: dict) -> str:
    aile = tasarim["font"]["aile"]
    eklemeler = "\n".join(f"    ..addFont(rootBundle.load('{f['yol']}'))" for f in tasarim["font"]["dosyalar"])
    return f"""{URETILMIS_BASLIK.format(kaynak="tasarim.json")}
import 'dart:io';

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

/// Testlerde gerçek fontları yükler. Yüklenmezse Flutter testleri yazıları kutu (Ahem) olarak çizer
/// ve yerleşim/ekran görüntüsü ölçümleri tasarımla karşılaştırılamaz.
Future<void> tasarimFontlariniYukle() async {{
  TestWidgetsFlutterBinding.ensureInitialized();
  await (FontLoader('{aile}')
{eklemeler})
      .load();
  final ikon = _materialIkonFontu();
  if (ikon != null) {{
    final veri = ikon.readAsBytesSync();
    await (FontLoader('MaterialIcons')
          ..addFont(Future.value(ByteData.sublistView(veri))))
        .load();
  }}
}}

/// Flutter SDK içindeki Material ikon fontunu bulur (flutter_tester'ın konumundan).
File? _materialIkonFontu() {{
  var dizin = File(Platform.resolvedExecutable).parent;
  for (var i = 0; i < 6; i++) {{
    final aday = File('${{dizin.path}}/material_fonts/MaterialIcons-Regular.otf');
    if (aday.existsSync()) return aday;
    dizin = dizin.parent;
  }}
  return null;
}}
"""


def _ortak_ac(ekranlar: dict, ekran: dict) -> str:
    b = ekranlar["ekran_boyutu"]
    oran = b["piksel_orani"]
    return f"""  Future<void> ac(WidgetTester tester) async {{
    tester.view.physicalSize = const Size({_dart_sayi(b['genislik'] * oran)}, {_dart_sayi(b['yukseklik'] * oran)});
    tester.view.devicePixelRatio = {_dart_sayi(oran)};
    addTearDown(tester.view.reset);
    await tester.pumpWidget(
      MaterialApp(
        debugShowCheckedModeBanner: false,
        theme: {ekranlar['uygulama']['tema']},
        home: {ekran['widget']},
      ),
    );
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 500));
  }}
"""


def _importlar(ekranlar: dict, ekran: dict, ekstra: list[str]) -> str:
    satirlar = {"package:flutter/material.dart", "package:flutter_test/flutter_test.dart",
                ekranlar["uygulama"]["tema_import"], ekran["import"], *ekran.get("ek_importlar", [])}
    paket = sorted(s for s in satirlar)
    return "\n".join([*(f"import '{s}';" for s in ekstra), *(f"import '{s}';" for s in paket),
                      "", "import '../yardimci/tasarim_fontlari.dart';"])


def yerlesim_testi(ekranlar: dict, ekran: dict) -> str:
    ad, tol = ekran["ad"], _dart_sayi(ekranlar["tolerans_dp"])
    testler = []
    bilesenler = sorted(ekran["bilesenler"], key=lambda b: b["sira"])
    for b in bilesenler:
        a, adet = b["anahtar"], b.get("adet", 1)
        bul = f"find.byKey(const ValueKey('{a}'))"
        testler.append(f"""  testWidgets('T4 {ad}: {a} adet {adet}', (tester) async {{
    await ac(tester);
    expect({bul}, findsNWidgets({adet}));
  }});""")
        for alan, ifade in (("yukseklik", "r.height"), ("genislik", "r.width"), ("ust", "r.top"), ("sol", "r.left")):
            if alan in b:
                testler.append(f"""  testWidgets('T4 {ad}: {a} {alan} {_dart_sayi(b[alan])}±{tol} dp', (tester) async {{
    await ac(tester);
    final r = tester.getRect({bul}.first);
    expect({ifade}, closeTo({_dart_sayi(b[alan])}, {tol}));
  }});""")
    for once, sonra in zip(bilesenler, bilesenler[1:]):
        if once["sira"] == sonra["sira"]:
            continue
        testler.append(f"""  testWidgets('T4 {ad}: sıra {once['anahtar']} → {sonra['anahtar']}', (tester) async {{
    await ac(tester);
    final ust = tester.getRect(find.byKey(const ValueKey('{once['anahtar']}')).first);
    final alt = tester.getRect(find.byKey(const ValueKey('{sonra['anahtar']}')).first);
    expect(ust.top, lessThanOrEqualTo(alt.top));
  }});""")
    return f"""{URETILMIS_BASLIK.format(kaynak="ekranlar.json")}
{_importlar(ekranlar, ekran, [])}

void main() {{
  setUpAll(tasarimFontlariniYukle);

{_ortak_ac(ekranlar, ekran)}
{chr(10).join(testler)}
}}
"""


def goruntu_testi(ekranlar: dict, ekran: dict) -> str:
    ad = ekran["ad"]
    return f"""{URETILMIS_BASLIK.format(kaynak="ekranlar.json")}
{_importlar(ekranlar, ekran, ["dart:io"])}

/// Varsayılan: onaylı ekran görüntüsüyle (goldens/) birebir karşılaştırma (T6).
/// Ölçüm: --update-goldens --dart-define=GORUNTU_KLASORU=olcum ile güncel görüntü olcum/ altına yazılır,
/// sonra goruntu_karsilastir.py kullanıcının tasarım görseliyle karşılaştırır (T5).
const _klasor = String.fromEnvironment('GORUNTU_KLASORU', defaultValue: 'goldens');

void main() {{
  setUpAll(tasarimFontlariniYukle);

{_ortak_ac(ekranlar, ekran)}
  final onayli = File('{GORUNTU_KLASORU}/goldens/{ad}.png');
  testWidgets(
    'T6 {ad}: ekran görüntüsü',
    (tester) async {{
      await ac(tester);
      await expectLater(find.byType(MaterialApp), matchesGoldenFile('$_klasor/{ad}.png'));
    }},
    skip: _klasor == 'goldens' && !onayli.existsSync() && !autoUpdateGoldenFiles,
  );
}}
"""


def uretilecekler(tasarim: dict, ekranlar: dict) -> dict[str, str]:
    dosyalar = {DART_TOKENS: dart_tokens(tasarim), FONT_YARDIMCI: font_yardimci(tasarim)}
    for e in ekranlar.get("ekranlar", []):
        dosyalar[f"{YERLESIM_KLASORU}/{_dosya_adi(e['ad'])}_yerlesim_test.dart"] = yerlesim_testi(ekranlar, e)
        dosyalar[f"{GORUNTU_KLASORU}/{_dosya_adi(e['ad'])}_goruntu_test.dart"] = goruntu_testi(ekranlar, e)
    return dosyalar


def _dosya_adi(ad: str) -> str:
    return re.sub(r"(?<!^)([A-Z])", r"_\1", ad).lower()


# ---------------------------------------------------------------- Denetim (T1–T3)

RENK_RE = re.compile(r"Color\(\s*0x[0-9A-Fa-f]+\s*\)|Color\.from(?:ARGB|RGBO)\(|\bColors\.(?!transparent\b)\w+")
OLCU_ARG_RE = re.compile(
    r"\b(width|height|fontSize|elevation|radius|letterSpacing|iconSize|size|spacing|runSpacing|"
    r"toolbarHeight|thickness|indent|endIndent|borderRadius|minHeight|maxHeight|minWidth|maxWidth)"
    r"\s*:\s*(\d+(?:\.\d+)?)\b"
)
OLCU_KONUM_RE = re.compile(
    r"\b(EdgeInsets\.(?:all|symmetric|only|fromLTRB)|EdgeInsetsDirectional\.(?:all|symmetric|only|fromSTEB)|"
    r"BorderRadius\.circular|Radius\.circular|SizedBox\.square|Size)\(([^()]*)\)"
)
SAYI_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])")


def _kod_satirlari(dosya: Path):
    for no, satir in enumerate(dosya.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        yalin = satir.split("//", 1)[0]
        if yalin.strip():
            yield no, yalin


def _lib_dosyalari(proje: Path) -> list[Path]:
    lib = proje / "lib"
    if not lib.is_dir():
        return []
    return [p for p in sorted(lib.rglob("*.dart")) if not p.name.endswith(".g.dart")]


def t1_sabit_renk(proje: Path) -> tuple[int, list[str]]:
    bulgular = []
    for d in _lib_dosyalari(proje):
        for no, s in _kod_satirlari(d):
            for m in RENK_RE.finditer(s):
                bulgular.append(f"{d.relative_to(proje)}:{no} {m.group(0)}")
    return len(bulgular), bulgular


def t2_sabit_olcu(proje: Path) -> tuple[int, list[str]]:
    bulgular = []
    for d in _lib_dosyalari(proje):
        for no, s in _kod_satirlari(d):
            for m in OLCU_ARG_RE.finditer(s):
                if float(m.group(2)) != 0:
                    bulgular.append(f"{d.relative_to(proje)}:{no} {m.group(1)}: {m.group(2)}")
            for m in OLCU_KONUM_RE.finditer(s):
                sayilar = [x for x in SAYI_RE.findall(m.group(2)) if float(x) != 0]
                if sayilar:
                    bulgular.append(f"{d.relative_to(proje)}:{no} {m.group(1)}({', '.join(sayilar)})")
    return len(bulgular), bulgular


def _icerik(metin: str) -> str:
    """Biçimden bağımsız içerik: dart format'ın değiştirdiği boşluk ve sondaki virgüller yok sayılır."""
    return re.sub(r"\s+", "", re.sub(r",(\s*[)\]}])", r"\1", metin))


def t3_uyumsuz(proje: Path, tasarim: dict, ekranlar: dict) -> tuple[int, list[str]]:
    bulgular = []
    for yol, icerik in uretilecekler(tasarim, ekranlar).items():
        p = proje / yol
        if not p.is_file():
            bulgular.append(f"{yol} yok (python tasarim.py uret çalıştırılmadı)")
        elif _icerik(p.read_text(encoding="utf-8")) != _icerik(icerik):
            bulgular.append(f"{yol} tasarım dosyasından üretilenle aynı değil (elle değiştirilmiş veya tasarım güncellenip yeniden üretilmemiş)")
    return len(bulgular), bulgular


def denetle(proje: Path) -> dict[str, dict]:
    tasarim = json_yukle(proje / "tasarim.json")
    ekranlar = json_yukle(proje / "ekranlar.json")
    sonuc: dict[str, dict] = {}
    if tasarim is None:
        neden = "tasarim.json yok — kullanıcı tasarım vermedi."
        return {k: {"deger": None, "kanit": "", "sebep": neden}
                for k in ("tasarim_sabit_renk", "tasarim_sabit_olcu", "tasarim_uretim_uyumsuz")}
    for anahtar, fn in (("tasarim_sabit_renk", t1_sabit_renk), ("tasarim_sabit_olcu", t2_sabit_olcu)):
        n, b = fn(proje)
        sonuc[anahtar] = {"deger": n, "kanit": f"lib/ tarandı: {'; '.join(b[:15]) if b else 'bulgu yok'}"}
    hatalar = dogrula(tasarim, ekranlar)
    if hatalar:
        sonuc["tasarim_uretim_uyumsuz"] = {"deger": None, "kanit": "", "sebep": "Tasarım dosyaları geçersiz: " + "; ".join(hatalar[:5])}
    else:
        n, b = t3_uyumsuz(proje, tasarim, ekranlar)
        sonuc["tasarim_uretim_uyumsuz"] = {"deger": n, "kanit": "; ".join(b) if b else "Üretilmiş dosyaların hepsi tasarım dosyalarıyla birebir aynı."}
    return sonuc


# ---------------------------------------------------------------- Onay tablosu

def tablo(tasarim: dict, ekranlar: dict) -> str:
    s = ["### Tasarım değerleri", "", "| Grup | Ad | Değer | Kaynak |", "|---|---|---|---|"]
    f = tasarim["font"]
    s.append(f"| font | {f['aile']} | " + ", ".join(f"{d['agirlik']}: {d['yol']}" for d in f["dosyalar"]) + f" | {f['kaynak']} |")
    for ad, t in tasarim["renk"].items():
        s.append(f"| renk | {ad} | {t['deger']} | {t['kaynak']} |")
    for ad, t in tasarim["yazi"].items():
        deger = f"{_dart_sayi(t['boyut'])} sp, {t['agirlik']}"
        if "satir_yuksekligi" in t:
            deger += f", satır {_dart_sayi(t['satir_yuksekligi'])} sp"
        s.append(f"| yazi | {ad} | {deger}, renk {t['renk']} | {t['kaynak']} |")
    for grup in SAYISAL_GRUPLAR:
        for ad, t in (tasarim.get(grup) or {}).items():
            s.append(f"| {grup} | {ad} | {_dart_sayi(t['deger'])} dp | {t['kaynak']} |")
    b = ekranlar["ekran_boyutu"]
    s += ["", f"### Ekranlar ({_dart_sayi(b['genislik'])}×{_dart_sayi(b['yukseklik'])} dp, piksel oranı "
              f"{_dart_sayi(b['piksel_orani'])}, tolerans ±{_dart_sayi(ekranlar['tolerans_dp'])} dp)"]
    for e in ekranlar["ekranlar"]:
        s += ["", f"**{e['ad']}** — görsel: `{e.get('referans_goruntu', 'YOK')}` — kaynak: {e['kaynak']}", "",
              "| Sıra | Anahtar | Adet | Üst | Sol | Genişlik | Yükseklik |", "|---|---|---|---|---|---|---|"]
        for c in sorted(e["bilesenler"], key=lambda c: c["sira"]):
            hucre = [_dart_sayi(c[a]) if a in c else "—" for a in ("ust", "sol", "genislik", "yukseklik")]
            s.append(f"| {c['sira']} | {c['anahtar']} | {c.get('adet', 1)} | " + " | ".join(hucre) + " |")
    return "\n".join(s)


# ---------------------------------------------------------------- Ana akış

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("komut", choices=["dogrula", "uret", "tablo", "denetle"])
    ap.add_argument("--proje", default=".")
    ap.add_argument("--olcumler", default=None)
    a = ap.parse_args()
    proje = Path(a.proje).resolve()
    tasarim = json_yukle(proje / "tasarim.json")
    ekranlar = json_yukle(proje / "ekranlar.json")

    if a.komut in ("dogrula", "uret", "tablo"):
        hatalar = dogrula(tasarim, ekranlar)
        if hatalar:
            print(f"GEÇERSİZ — {len(hatalar)} hata:")
            for x in hatalar:
                print(f"  - {x}")
            return 1
        if a.komut == "tablo":
            print(tablo(tasarim, ekranlar))
            return 0
        if a.komut == "dogrula":
            n = sum(len(tasarim.get(g) or {}) for g in ("renk", "yazi", *SAYISAL_GRUPLAR))
            b = sum(len(e["bilesenler"]) for e in ekranlar["ekranlar"])
            print(f"GEÇERLİ — {n} tasarım değeri, {len(ekranlar['ekranlar'])} ekran, {b} bileşen; hepsi kullanıcı kaynaklı.")
            return 0
        for yol, icerik in uretilecekler(tasarim, ekranlar).items():
            p = proje / yol
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(icerik, encoding="utf-8")
            print(f"yazıldı: {yol}")
        return 0

    sonuc = denetle(proje)
    yol = Path(a.olcumler) if a.olcumler else proje / "olcumler.json"
    mevcut = json_yukle(yol) or {}
    mevcut.update(sonuc)
    yol.write_text(json.dumps(mevcut, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in sonuc.items():
        print(f"{k} = {v['deger']}  ({v.get('sebep') or v['kanit'][:200]})")
    return 0 if all(v["deger"] == 0 for v in sonuc.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
