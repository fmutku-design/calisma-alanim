#!/usr/bin/env python3
"""Claude'un kendi davranışını ölçer: varsayım, onaysız kod, testsiz özellik, kanıtsız iddia.

Kullanım:
    python denetim.py kontrol --proje . [--olcumler olcumler.json]
        D1, D2, D3 metriklerini hesaplar ve olcumler.json'a yazar.
    python denetim.py mesaj yanit.md --kriterler kabul_kriterleri.json --olcumler olcumler.json
        Kullanıcıya gidecek mesajı denetler (D4). 0 dışındaki her sonuç = mesaj gönderilemez.

Metrikler (hepsinin hedefi 0):
    D1 kaynaksiz_karar        Kullanıcıdan gelmeyen karar sayısı = varsayım sayısı.
    D2 onaysiz_kod            Kriterler onaylanmadan var olan kod dosyası sayısı.
    D3 testsiz_ozellik        Test dosyası olmayan fonksiyonel (F) kriter sayısı.
    D4 kanitsiz_iddia         Ölçüm tamamlanmamışken mesajdaki "bitti/çalışıyor/hazır…" iddiası sayısı
                              + mesajda ölçüm raporu özeti yoksa 1.

Sadece Python standart kütüphanesi kullanılır.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

GECERLI_KAYNAK = re.compile(r"^(kullanici|öneri-onaylandı):\S+")
# Flutter SDK'nın parçası olan, ayrı bir seçim olmayan bağımlılıklar.
SDK_PAKETLERI = {"flutter", "flutter_test", "flutter_localizations", "integration_test", "flutter_driver", "flutter_web_plugins"}
TEST_YOLU_RE = re.compile(r"((?:integration_test|test)/[\w/.-]+_test\.dart|[\w/.-]*test_[\w.-]+\.py|[\w/.-]+_test\.py)")

# Ölçüm tamamlanmamışken kullanılamayan iddialar. Olumsuz halleri (bitmedi, çalışmıyor…) ayrı kelimelerdir.
IDDIA_DESENLERI = [
    r"bitti", r"bitirdim", r"tamamlandı", r"tamamladım", r"tamamdır", r"hazır(?!\s+değil)",
    r"çalışıyor", r"sorunsuz", r"test edildi", r"test ettim", r"doğrulandı", r"doğruladım",
    r"başarıyla", r"eksiksiz", r"kusursuz",
    r"done", r"finished", r"completed", r"works", r"working", r"ready", r"tested", r"verified",
]
IDDIA_RE = re.compile(r"(?<![\w'\"“‘«`])(" + "|".join(IDDIA_DESENLERI) + r")(?!\w)", re.IGNORECASE)
OZET_RE = re.compile(r"Toplam \d+ kriter: \d+ GEÇTİ, \d+ KALDI, \d+ ÖLÇÜLEMEDİ")


def json_yukle(yol: Path, varsayilan=None):
    if not yol.is_file():
        return varsayilan
    return json.loads(yol.read_text(encoding="utf-8"))


def olcum(deger, kanit: str) -> dict:
    return {"deger": deger, "kanit": kanit}


# ---------------------------------------------------------------- Bağımlılık okuma

def pubspec_paketleri(proje: Path) -> list[str]:
    dosya = proje / "pubspec.yaml"
    if not dosya.is_file():
        return []
    paketler, bolumde = [], False
    for satir in dosya.read_text(encoding="utf-8").splitlines():
        if not satir.strip() or satir.lstrip().startswith("#"):
            continue
        girinti = len(satir) - len(satir.lstrip())
        if girinti == 0:
            bolumde = satir.rstrip().rstrip(":") in {"dependencies", "dev_dependencies"}
            continue
        if bolumde and girinti == 2:
            ad = satir.strip().split(":", 1)[0]
            if ad not in SDK_PAKETLERI:
                paketler.append(ad)
    return paketler


def python_paketleri(proje: Path) -> list[str]:
    adlar: list[str] = []
    yok = {".git", "build", ".dart_tool", "node_modules", ".venv", "venv"}
    for req in proje.rglob("requirements*.txt"):
        if yok & set(req.relative_to(proje).parts):
            continue
        for satir in req.read_text(encoding="utf-8").splitlines():
            satir = satir.split("#", 1)[0].strip()
            if satir and not satir.startswith("-"):
                adlar.append(re.split(r"[<>=~!;\[\s]", satir, maxsplit=1)[0])
    pyproject = proje / "pyproject.toml"
    if pyproject.is_file():
        veri = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        proj = veri.get("project", {})
        bagimliliklar = list(proj.get("dependencies", []))
        for grup in proj.get("optional-dependencies", {}).values():
            bagimliliklar += grup
        for grup in veri.get("dependency-groups", {}).values():
            bagimliliklar += [b for b in grup if isinstance(b, str)]
        adlar += [re.split(r"[<>=~!;\[\s]", b, maxsplit=1)[0] for b in bagimliliklar]
    return sorted({a.lower().replace("_", "-") for a in adlar if a})


def kod_dosyalari(proje: Path) -> list[Path]:
    yok = {".git", "build", ".dart_tool", "node_modules", ".venv", "venv", "__pycache__"}
    sonuc = []
    for uzanti in ("*.dart", "*.py", "*.kt", "*.java"):
        for p in proje.rglob(uzanti):
            if not (yok & set(p.relative_to(proje).parts)):
                sonuc.append(p)
    return sorted(sonuc)


# ---------------------------------------------------------------- D1–D3

def d1_kaynaksiz_karar(proje: Path, kriterler: dict, kararlar: dict) -> dict:
    bulgular: list[str] = []

    karar_listesi = kararlar.get("kararlar", []) if kararlar else []
    onayli_paketler: set[str] = set()
    for k in karar_listesi:
        kaynak = str(k.get("kaynak", ""))
        if not GECERLI_KAYNAK.match(kaynak):
            bulgular.append(f"karar {k.get('id', '?')} ({k.get('konu', '?')}): kaynak '{kaynak}' kullanıcıdan değil")
            continue
        for paket in k.get("paketler", []):
            onayli_paketler.add(paket.lower().replace("_", "-"))

    for paket in pubspec_paketleri(proje):
        if paket.lower().replace("_", "-") not in onayli_paketler:
            bulgular.append(f"pubspec.yaml: '{paket}' kararlar.json'da onaylı bir kararla eşleşmiyor")
    for paket in python_paketleri(proje):
        if paket not in onayli_paketler:
            bulgular.append(f"Python bağımlılığı: '{paket}' kararlar.json'da onaylı bir kararla eşleşmiyor")

    if kriterler:
        for k in kriterler.get("kriterler", []):
            if not GECERLI_KAYNAK.match(str(k.get("kaynak", ""))):
                bulgular.append(f"kriter {k.get('id')}: kaynak '{k.get('kaynak')}' kullanıcı onaylı değil")

    if not kararlar and kod_dosyalari(proje):
        bulgular.append("kararlar.json yok ama kod var — verilen hiçbir kararın kaynağı kayıtlı değil")

    return olcum(len(bulgular), "; ".join(bulgular) if bulgular else "Tüm paketler, kararlar ve kriterler kullanıcı kaynaklı.")


def d2_onaysiz_kod(proje: Path, kriterler: dict) -> dict:
    dosyalar = kod_dosyalari(proje)
    onay = (kriterler or {}).get("onay", {})
    onayli = onay.get("durum") == "onaylandi" and str(onay.get("kanit", "")).strip()
    if onayli:
        return olcum(0, f"Onay var: \"{onay.get('kanit')}\" ({onay.get('tarih')}). Kod dosyası: {len(dosyalar)}")
    ornek = ", ".join(str(p.relative_to(proje)) for p in dosyalar[:5])
    return olcum(len(dosyalar), f"Onay durumu '{onay.get('durum')}', onay kanıtı yok. Kod dosyaları: {ornek or '(yok)'}")


def d3_testsiz_ozellik(proje: Path, kriterler: dict) -> dict:
    bulgular = []
    for k in (kriterler or {}).get("kriterler", []):
        if k.get("kategori") != "fonksiyonel":
            continue
        yollar = TEST_YOLU_RE.findall(k.get("olcum_yontemi", ""))
        if not yollar:
            bulgular.append(f"{k['id']}: ölçüm yönteminde test dosyası yolu yok")
        for y in yollar:
            if not (proje / y).is_file():
                bulgular.append(f"{k['id']}: {y} yok")
    return olcum(len(bulgular), "; ".join(bulgular) if bulgular else "Her F kriterinin test dosyası mevcut.")


# ---------------------------------------------------------------- D4

def tum_kriterler_gecti(kriterler: dict, olcumler: dict) -> tuple[bool, str]:
    sys.path.insert(0, str(Path(__file__).parent))
    from kriterler import rapor  # noqa: PLC0415

    metin, gecti = rapor(kriterler, olcumler)
    ozet = OZET_RE.search(metin)
    return gecti, ozet.group(0) if ozet else ""


def d4_mesaj(mesaj_yolu: Path, kriterler: dict, olcumler: dict) -> tuple[int, list[str]]:
    metin = mesaj_yolu.read_text(encoding="utf-8")
    bulgular: list[str] = []

    gecti, ozet = tum_kriterler_gecti(kriterler, olcumler)
    if ozet and ozet not in metin:
        bulgular.append(f"Mesajda güncel ölçüm özeti yok. Rapordan aynen eklenmeli: \"{ozet}\"")
    if not gecti:
        # Kod blokları ve tablo satırları (script çıktısı) iddia sayılmaz.
        duz = re.sub(r"```.*?```", "", metin, flags=re.DOTALL)
        for no, satir in enumerate(duz.splitlines(), 1):
            if satir.lstrip().startswith("|"):
                continue
            for m in IDDIA_RE.finditer(satir):
                bulgular.append(f"satır {no}: '{m.group(0)}' — ölçüm tamamlanmamışken iddia ({satir.strip()[:80]})")
    return len(bulgular), bulgular


# ---------------------------------------------------------------- Ana akış

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut", required=True)
    k = alt.add_parser("kontrol")
    k.add_argument("--proje", default=".")
    k.add_argument("--olcumler", default=None)
    m = alt.add_parser("mesaj")
    m.add_argument("mesaj")
    m.add_argument("--kriterler", required=True)
    m.add_argument("--olcumler", required=True)
    a = ap.parse_args()

    if a.komut == "kontrol":
        proje = Path(a.proje).resolve()
        kriterler = json_yukle(proje / "kabul_kriterleri.json", {})
        kararlar = json_yukle(proje / "kararlar.json", {})
        sonuc = {
            "D1": d1_kaynaksiz_karar(proje, kriterler, kararlar),
            "D2": d2_onaysiz_kod(proje, kriterler),
            "D3": d3_testsiz_ozellik(proje, kriterler),
        }
        yol = Path(a.olcumler) if a.olcumler else proje / "olcumler.json"
        mevcut = json_yukle(yol, {}) or {}
        mevcut.update(sonuc)
        yol.write_text(json.dumps(mevcut, ensure_ascii=False, indent=2), encoding="utf-8")
        for anahtar, v in sonuc.items():
            print(f"{anahtar} = {v['deger']}  ({v['kanit']})")
        print(f"\n{yol} güncellendi.")
        return 0 if all(v["deger"] == 0 for v in sonuc.values()) else 1

    kriterler = json_yukle(Path(a.kriterler), {})
    olcumler = json_yukle(Path(a.olcumler), {})
    sayi, bulgular = d4_mesaj(Path(a.mesaj), kriterler, olcumler)
    print(f"D4 kanitsiz_iddia = {sayi}")
    for b in bulgular:
        print(f"  - {b}")
    print("Mesaj gönderilebilir." if sayi == 0 else "Mesaj GÖNDERİLEMEZ — iddiaları kaldır veya önce ölçümü tamamla.")
    return 0 if sayi == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
