#!/usr/bin/env python3
"""Onaylanmış mimariye (mimari.json) uyumu ölçer.

Kullanım:
    python mimari.py dogrula --proje .
    python mimari.py denetle --proje . [--olcumler olcumler.json]

Metrikler (hepsi == 0 hedeflenir):
    Y1 mimari_yasak_bagimlilik   Katman kuralını çiğneyen import sayısı (izinsiz katman, özellikler arası, yasak paket)
    Y2 mimari_katmansiz_dosya    Hiçbir katmana ait olmayan lib/ dosyası sayısı
    Y3 mimari_uzun_dosya         Satır sınırını aşan dosya sayısı (Dart + Python)
    Y4 mimari_uzun_fonksiyon     Satır sınırını aşan fonksiyon/metot sayısı (Dart + Python)

Sadece Python standart kütüphanesi kullanılır.
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import json
import re
import sys
from pathlib import Path

IMPORT_RE = re.compile(r"""^\s*(?:import|export)\s+['"]([^'"]+)['"]""", re.MULTILINE)
KONTROL_KELIMELERI = {"if", "for", "while", "switch", "catch", "on", "assert", "return", "await", "else"}
URETILMIS = re.compile(r"\.(g|freezed|gr|mocks|config)\.dart$")


def json_yukle(yol: Path):
    return json.loads(yol.read_text(encoding="utf-8")) if yol.is_file() else None


# ---------------------------------------------------------------- Doğrulama

def dogrula(m: dict | None) -> list[str]:
    if m is None:
        return ["mimari.json yok — mimari onaylanmadan kod yazılmaz (references/mimari.md örneğinden önerip onay al)."]
    h = []
    if not re.match(r"^(kullanici|öneri-onaylandı|öneri-bekliyor):\S+", str(m.get("kaynak", ""))):
        h.append("kaynak 'kullanici:…' veya 'öneri-onaylandı:…' olmalı.")
    if not m.get("paket"):
        h.append("'paket' (pubspec.yaml name) eksik — package: importlarını çözmek için gerekli.")
    adlar = set()
    for k in m.get("katmanlar", []):
        if not k.get("ad") or not k.get("yollar"):
            h.append(f"katman {k}: 'ad' ve 'yollar' zorunlu.")
        adlar.add(k.get("ad"))
    for k in m.get("katmanlar", []):
        for b in k.get("izinli", []):
            if b != "*" and b not in adlar:
                h.append(f"katman {k.get('ad')}: izinli '{b}' tanımlı bir katman değil.")
    s = m.get("sinirlar", {})
    for alan in ("dosya_satir_max", "fonksiyon_satir_max"):
        if not isinstance(s.get(alan), int) or s[alan] <= 0:
            h.append(f"sinirlar.{alan} pozitif tam sayı olmalı.")
    if not m.get("katmanlar"):
        h.append("'katmanlar' boş.")
    return h


# ---------------------------------------------------------------- Yardımcılar

def katman_bul(yol: str, m: dict) -> dict | None:
    for k in m["katmanlar"]:
        if any(fnmatch.fnmatch(yol, desen) for desen in k["yollar"]):
            return k
    return None


def ozellik_bul(yol: str, m: dict) -> str | None:
    kok = m.get("ozellik_koku")
    if not kok or not yol.startswith(kok.rstrip("/") + "/"):
        return None
    return yol[len(kok.rstrip("/")) + 1:].split("/", 1)[0]


def import_coz(kaynak: Path, hedef: str, proje: Path, paket: str) -> str | None:
    """lib/ içindeki hedefin proje köküne göre yolunu verir; dış paket ise None."""
    if hedef.startswith(f"package:{paket}/"):
        return "lib/" + hedef[len(f"package:{paket}/"):]
    if hedef.startswith(("package:", "dart:")):
        return None
    return (kaynak.parent / hedef).resolve().relative_to(proje).as_posix()


def dart_temizle(metin: str) -> str:
    """Yorumları ve string içeriklerini boşlukla değiştirir; satır sayısı ve parantez dengesi korunur."""
    cikti, i, n = [], 0, len(metin)

    def bosalt(parca: str) -> str:
        return "".join("\n" if ch == "\n" else " " for ch in parca)

    while i < n:
        if metin.startswith("//", i):
            j = metin.find("\n", i)
            j = n if j < 0 else j
            cikti.append(bosalt(metin[i:j]))
            i = j
        elif metin.startswith("/*", i):
            j = metin.find("*/", i + 2)
            j = n if j < 0 else j + 2
            cikti.append(bosalt(metin[i:j]))
            i = j
        elif metin[i] in "'\"":
            ham = i > 0 and metin[i - 1] == "r"
            tirnak = metin[i:i + 3] if metin[i:i + 3] in ("'''", '"""') else metin[i]
            j, derinlik = i + len(tirnak), 0
            while j < n:
                if not ham and metin[j] == "\\":
                    j += 2
                    continue
                if not ham and metin.startswith("${", j):
                    derinlik += 1
                    j += 2
                    continue
                if derinlik and metin[j] == "}":
                    derinlik -= 1
                elif not derinlik and metin.startswith(tirnak, j):
                    j += len(tirnak)
                    break
                j += 1
            cikti.append(tirnak + bosalt(metin[i + len(tirnak):max(j - len(tirnak), i + len(tirnak))]) + tirnak)
            i = j
        else:
            cikti.append(metin[i])
            i += 1
    return "".join(cikti)


def dart_fonksiyonlari(metin: str) -> list[tuple[str, int, int]]:
    """(ad, başlangıç satırı, satır sayısı) listesi. Gövdeli '{…}' ve '=> …;' fonksiyonları sayar."""
    t = dart_temizle(metin)
    eslesme, yigin = {}, []
    for i, ch in enumerate(t):
        if ch in "({[":
            yigin.append(i)
        elif ch in ")}]" and yigin:
            eslesme[yigin.pop()] = i
    acan = {v: k for k, v in eslesme.items()}
    sonuc = []

    def satir(i: int) -> int:
        return t.count("\n", 0, i) + 1

    for i, ch in enumerate(t):
        if ch == "{" or t.startswith("=>", i):
            j = i - 1
            while j >= 0 and t[j].isspace():
                j -= 1
            onek = t[max(0, j - 6):j + 1]
            for kelime in ("async*", "sync*", "async"):
                if onek.endswith(kelime):
                    j -= len(kelime)
                    while j >= 0 and t[j].isspace():
                        j -= 1
                    break
            if j < 0 or t[j] != ")" or j not in acan:
                continue
            ac = acan[j]
            k = ac - 1
            while k >= 0 and t[k].isspace():
                k -= 1
            bas = k
            while k >= 0 and (t[k].isalnum() or t[k] in "_$."):
                k -= 1
            ad = t[k + 1:bas + 1]
            if ad.split(".")[-1] in KONTROL_KELIMELERI:
                continue
            if ch == "{":
                if i not in eslesme:
                    continue
                bitis = eslesme[i]
            else:
                derinlik, bitis = 0, None
                for q in range(i + 2, len(t)):
                    if t[q] in "({[":
                        derinlik += 1
                    elif t[q] in ")}]":
                        if derinlik == 0:
                            bitis = q
                            break
                        derinlik -= 1
                    elif t[q] in ";," and derinlik == 0:
                        bitis = q
                        break
                if bitis is None:
                    continue
            sonuc.append((ad or "(anonim)", satir(ac), satir(bitis) - satir(ac) + 1))
    return sonuc


# ---------------------------------------------------------------- Denetim

def denetle(proje: Path) -> dict[str, dict]:
    m = json_yukle(proje / "mimari.json")
    anahtarlar = ("mimari_yasak_bagimlilik", "mimari_katmansiz_dosya", "mimari_uzun_dosya", "mimari_uzun_fonksiyon")
    hatalar = dogrula(m)
    if hatalar:
        return {k: {"deger": None, "kanit": "", "sebep": "; ".join(hatalar)} for k in anahtarlar}

    paket, s = m["paket"], m["sinirlar"]
    yasak, katmansiz, uzun_dosya, uzun_fonk = [], [], [], []
    dart = [p for p in sorted((proje / "lib").rglob("*.dart")) if not URETILMIS.search(p.name)] if (proje / "lib").is_dir() else []

    for d in dart:
        yol = d.relative_to(proje).as_posix()
        metin = d.read_text(encoding="utf-8", errors="replace")
        satir_sayisi = metin.count("\n") + 1
        if satir_sayisi > s["dosya_satir_max"]:
            uzun_dosya.append(f"{yol} ({satir_sayisi} satır)")
        for ad, bas, uz in dart_fonksiyonlari(metin):
            if uz > s["fonksiyon_satir_max"]:
                uzun_fonk.append(f"{yol}:{bas} {ad} ({uz} satır)")

        k = katman_bul(yol, m)
        if k is None:
            katmansiz.append(yol)
            continue
        oz = ozellik_bul(yol, m)
        for hedef in IMPORT_RE.findall(metin):
            for yp in k.get("yasak_paketler", []):
                if hedef.startswith(yp):
                    yasak.append(f"{yol}: '{hedef}' ({k['ad']} katmanında yasak)")
            hedef_yol = import_coz(d, hedef, proje, paket)
            if hedef_yol is None:
                continue
            hk = katman_bul(hedef_yol, m)
            if hk is None:
                continue
            if hk["ad"] != k["ad"] and "*" not in k.get("izinli", []) and hk["ad"] not in k.get("izinli", []):
                yasak.append(f"{yol} → {hedef_yol} ({k['ad']} → {hk['ad']} izinli değil)")
            hoz = ozellik_bul(hedef_yol, m)
            if oz and hoz and oz != hoz and not m.get("ozellikler_arasi_import", False):
                yasak.append(f"{yol} → {hedef_yol} (özellik '{oz}' → '{hoz}' import edemez)")

    py = m.get("python")
    if py:
        for desen in py.get("yollar", []):
            for p in sorted(proje.glob(desen)):
                if p.suffix != ".py" or not p.is_file():
                    continue
                yol = p.relative_to(proje).as_posix()
                metin = p.read_text(encoding="utf-8", errors="replace")
                if metin.count("\n") + 1 > s["dosya_satir_max"]:
                    uzun_dosya.append(f"{yol} ({metin.count(chr(10)) + 1} satır)")
                try:
                    agac = ast.parse(metin)
                except SyntaxError as e:
                    uzun_fonk.append(f"{yol}: ayrıştırılamadı ({e})")
                    continue
                for dugum in ast.walk(agac):
                    if isinstance(dugum, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        uz = dugum.end_lineno - dugum.lineno + 1
                        if uz > s["fonksiyon_satir_max"]:
                            uzun_fonk.append(f"{yol}:{dugum.lineno} {dugum.name} ({uz} satır)")

    def kayit(liste: list[str], bos: str) -> dict:
        return {"deger": len(liste), "kanit": "; ".join(liste[:15]) if liste else bos}

    return {
        "mimari_yasak_bagimlilik": kayit(yasak, f"{len(dart)} Dart dosyasının importları katman kurallarına uyuyor."),
        "mimari_katmansiz_dosya": kayit(katmansiz, "Her lib/ dosyası tanımlı bir katmanda."),
        "mimari_uzun_dosya": kayit(uzun_dosya, f"Hiçbir dosya {s['dosya_satir_max']} satırı aşmıyor."),
        "mimari_uzun_fonksiyon": kayit(uzun_fonk, f"Hiçbir fonksiyon {s['fonksiyon_satir_max']} satırı aşmıyor."),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("komut", choices=["dogrula", "denetle"])
    ap.add_argument("--proje", default=".")
    ap.add_argument("--olcumler", default=None)
    a = ap.parse_args()
    proje = Path(a.proje).resolve()
    if a.komut == "dogrula":
        h = dogrula(json_yukle(proje / "mimari.json"))
        print("GEÇERLİ — mimari.json" if not h else "GEÇERSİZ:\n  - " + "\n  - ".join(h))
        return 0 if not h else 1
    sonuc = denetle(proje)
    yol = Path(a.olcumler) if a.olcumler else proje / "olcumler.json"
    mevcut = json_yukle(yol) or {}
    mevcut.update(sonuc)
    yol.write_text(json.dumps(mevcut, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in sonuc.items():
        print(f"{k} = {v['deger']}  ({(v.get('sebep') or v['kanit'])[:300]})")
    return 0 if all(v["deger"] == 0 for v in sonuc.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
