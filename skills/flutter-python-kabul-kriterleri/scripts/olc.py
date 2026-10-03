#!/usr/bin/env python3
"""Flutter + Python projesinde otomatik ölçülebilen metrikleri toplar ve olcumler.json'a yazar.

Kullanım:
    python olc.py --proje . --cikti olcumler.json [--kriterler kabul_kriterleri.json]
                  [--python-klasoru ml] [--model assets/model.tflite] [--build-apk] [--atla anahtar1,anahtar2]

Kural: Bir araç yoksa veya komut başarısız olursa değer null olur ve 'sebep' yazılır.
Tahmini değer asla yazılmaz. Mevcut olcumler.json içindeki elle girilmiş kayıtlar (ör. "P1") korunur.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

MB = 1048576
URETILMIS_DOSYA = re.compile(r"\.(g|freezed|gr|mocks|config)\.dart$")
AG_DESENLERI = [
    r"package:http/", r"package:dio/", r"HttpClient\(", r"WebSocket", r"package:google_fonts/",
    r"package:firebase_", r"package:web_socket_channel/", r"package:connectivity", r"package:url_launcher/",
]
AG_RE = re.compile("|".join(AG_DESENLERI))
SABIT_METIN_RE = re.compile(r"""\bText\(\s*(['"])(?!\1)""")


def olcum(deger=None, kanit: str = "", sebep: str = "") -> dict:
    kayit = {"deger": deger, "kanit": kanit.strip()}
    if deger is None:
        kayit["sebep"] = sebep or "Ölçülemedi."
    return kayit


def calistir(komut: list[str], cwd: Path, zaman_asimi: int = 900) -> tuple[int | None, str]:
    if shutil.which(komut[0]) is None:
        return None, f"'{komut[0]}' bulunamadı (PATH'te yok)."
    try:
        p = subprocess.run(komut, cwd=cwd, capture_output=True, text=True, timeout=zaman_asimi)
    except subprocess.TimeoutExpired:
        return None, f"'{' '.join(komut)}' {zaman_asimi} sn içinde bitmedi."
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def dart_dosyalari(proje: Path) -> list[Path]:
    lib = proje / "lib"
    if not lib.is_dir():
        return []
    return [p for p in lib.rglob("*.dart") if not URETILMIS_DOSYA.search(p.name) and "l10n" not in p.parts]


# ---------------------------------------------------------------- Dart / Flutter

def flutter_analyze(proje: Path) -> dict:
    kod, cikti = calistir(["flutter", "analyze"], proje)
    if kod is None:
        return olcum(sebep=cikti)
    if "No issues found" in cikti:
        return olcum(0, "flutter analyze → No issues found!")
    m = re.search(r"(\d+) issues? found", cikti)
    if m:
        return olcum(int(m.group(1)), f"flutter analyze → {m.group(0)}")
    return olcum(sebep=f"flutter analyze çıktısı çözümlenemedi (çıkış kodu {kod}): {cikti[-300:]}")


def dart_format(proje: Path) -> dict:
    hedefler = [d for d in ("lib", "test", "integration_test") if (proje / d).is_dir()]
    if not hedefler:
        return olcum(sebep="lib/test klasörü yok.")
    kod, cikti = calistir(["dart", "format", "--output=none", "--set-exit-if-changed", *hedefler], proje)
    if kod is None:
        return olcum(sebep=cikti)
    m = re.search(r"Formatted \d+ files? \((\d+) changed\)", cikti)
    if m:
        return olcum(int(m.group(1)), f"dart format → {m.group(0)}")
    return olcum(sebep=f"dart format çıktısı çözümlenemedi: {cikti[-300:]}")


def flutter_test(proje: Path) -> tuple[dict, dict]:
    if not (proje / "test").is_dir():
        sebep = "test/ klasörü yok — test yoksa kapsam ve test sonucu ölçülemez."
        return olcum(sebep=sebep), olcum(sebep=sebep)
    kod, cikti = calistir(["flutter", "test", "--coverage", "--reporter", "json"], proje, zaman_asimi=1800)
    if kod is None:
        return olcum(sebep=cikti), olcum(sebep=cikti)

    gecen = basarisiz = 0
    for satir in cikti.splitlines():
        try:
            olay = json.loads(satir)
        except json.JSONDecodeError:
            continue
        if isinstance(olay, dict) and olay.get("type") == "testDone" and not olay.get("hidden"):
            if olay.get("skipped"):
                continue
            if olay.get("result") == "success":
                gecen += 1
            else:
                basarisiz += 1
    if gecen + basarisiz == 0:
        test_kaydi = olcum(sebep=f"Hiç test sonucu okunamadı (çıkış kodu {kod}).")
    else:
        test_kaydi = olcum(basarisiz, f"flutter test → {gecen} geçti, {basarisiz} başarısız")

    lcov = proje / "coverage" / "lcov.info"
    if not lcov.is_file():
        return test_kaydi, olcum(sebep="coverage/lcov.info oluşmadı.")
    lf = lh = 0
    atla = False
    for satir in lcov.read_text(encoding="utf-8", errors="replace").splitlines():
        if satir.startswith("SF:"):
            atla = bool(URETILMIS_DOSYA.search(satir))
        elif satir.startswith("LF:") and not atla:
            lf += int(satir[3:])
        elif satir.startswith("LH:") and not atla:
            lh += int(satir[3:])
    if lf == 0:
        return test_kaydi, olcum(sebep="lcov.info içinde satır bilgisi yok.")
    yuzde = round(lh / lf * 100, 2)
    return test_kaydi, olcum(yuzde, f"coverage/lcov.info → LH {lh} / LF {lf} (üretilmiş dosyalar hariç)")


def apk_boyutu(proje: Path, build: bool) -> dict:
    yol = proje / "build/app/outputs/flutter-apk/app-arm64-v8a-release.apk"
    if build:
        kod, cikti = calistir(["flutter", "build", "apk", "--release", "--split-per-abi"], proje, zaman_asimi=1800)
        if kod is None:
            return olcum(sebep=cikti)
        if kod != 0:
            return olcum(sebep=f"flutter build apk başarısız: {cikti[-400:]}")
    if not yol.is_file():
        return olcum(sebep=f"{yol.relative_to(proje)} yok. --build-apk ile ya da elle 'flutter build apk --release --split-per-abi' çalıştır.")
    boyut = yol.stat().st_size
    return olcum(round(boyut / MB, 2), f"{yol.relative_to(proje)} → {boyut} bayt")


# ---------------------------------------------------------------- Android

def gradle_sdk(proje: Path) -> tuple[dict, dict]:
    adaylar = [proje / "android/app/build.gradle.kts", proje / "android/app/build.gradle"]
    dosya = next((d for d in adaylar if d.is_file()), None)
    if dosya is None:
        s = "android/app/build.gradle(.kts) bulunamadı."
        return olcum(sebep=s), olcum(sebep=s)
    metin = dosya.read_text(encoding="utf-8", errors="replace")
    sonuc = []
    for ad in ("minSdk", "targetSdk"):
        m = re.search(rf"\b{ad}(?:Version)?\s*=?\s*([^\s\n]+)", metin)
        if not m:
            sonuc.append(olcum(sebep=f"{dosya.name} içinde {ad} bulunamadı."))
        elif m.group(1).isdigit():
            sonuc.append(olcum(int(m.group(1)), f"{dosya.relative_to(proje)} → {m.group(0).strip()}"))
        else:
            sonuc.append(olcum(sebep=f"{ad} açık sayı değil ('{m.group(1)}'). Kriterle karşılaştırmak için sayı yaz."))
    return sonuc[0], sonuc[1]


def release_manifest_izinleri(proje: Path) -> tuple[list[str] | None, str]:
    kok = proje / "build/app/intermediates"
    if not kok.is_dir():
        return None, "build/app/intermediates yok — önce release build al."
    adaylar = [p for p in kok.rglob("AndroidManifest.xml") if "release" in p.as_posix().lower() and "merged" in p.as_posix().lower()]
    if not adaylar:
        return None, "Release birleştirilmiş manifest bulunamadı — 'flutter build apk --release' çalıştır."
    dosya = max(adaylar, key=lambda p: p.stat().st_mtime)
    metin = dosya.read_text(encoding="utf-8", errors="replace")
    izinler = re.findall(r'<uses-permission(?:-sdk-23)?\s[^>]*android:name="([^"]+)"', metin)
    return sorted(set(izinler)), str(dosya.relative_to(proje))


def izin_olcumleri(proje: Path, izinli: list[str] | None) -> tuple[dict, dict]:
    izinler, kaynak = release_manifest_izinleri(proje)
    if izinler is None:
        return olcum(sebep=kaynak), olcum(sebep=kaynak)
    internet = sum(1 for i in izinler if i == "android.permission.INTERNET")
    internet_kaydi = olcum(internet, f"{kaynak} → izinler: {', '.join(izinler) or '(yok)'}")
    if izinli is None:
        return internet_kaydi, olcum(sebep="kabul_kriterleri.json içinde 'izinli_android_izinleri' yok (--kriterler ver).")
    fazla = [i for i in izinler if i not in set(izinli)]
    return internet_kaydi, olcum(len(fazla), f"{kaynak} → izinli liste dışı: {', '.join(fazla) or '(yok)'}")


# ---------------------------------------------------------------- Statik kod taraması

def ag_kodu(proje: Path) -> dict:
    dosyalar = dart_dosyalari(proje)
    if not dosyalar:
        return olcum(sebep="lib/ altında Dart dosyası yok.")
    bulunan = []
    for d in dosyalar:
        for no, satir in enumerate(d.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if AG_RE.search(satir):
                bulunan.append(f"{d.relative_to(proje)}:{no}")
    return olcum(len(bulunan), f"lib/ tarandı ({len(dosyalar)} dosya) → {', '.join(bulunan[:10]) or 'ağ kodu yok'}")


def sabit_metin(proje: Path) -> dict:
    dosyalar = dart_dosyalari(proje)
    if not dosyalar:
        return olcum(sebep="lib/ altında Dart dosyası yok.")
    bulunan = []
    for d in dosyalar:
        for no, satir in enumerate(d.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if SABIT_METIN_RE.search(satir):
                bulunan.append(f"{d.relative_to(proje)}:{no}")
    return olcum(len(bulunan), f"lib/ içinde Text('...') sabit metin → {', '.join(bulunan[:10]) or 'yok'}")


def cevrilmemis(proje: Path) -> dict:
    l10n = proje / "l10n.yaml"
    if not l10n.is_file():
        return olcum(sebep="l10n.yaml yok — çok dilli değilse bu kriteri kullanma.")
    m = re.search(r"untranslated-messages-file:\s*(\S+)", l10n.read_text(encoding="utf-8"))
    if not m:
        return olcum(sebep="l10n.yaml içinde 'untranslated-messages-file' tanımlı değil.")
    kod, cikti = calistir(["flutter", "gen-l10n"], proje)
    if kod is None:
        return olcum(sebep=cikti)
    dosya = proje / m.group(1)
    if not dosya.is_file():
        return olcum(0, f"flutter gen-l10n → {m.group(1)} oluşmadı (çevrilmemiş anahtar yok)")
    veri = json.loads(dosya.read_text(encoding="utf-8") or "{}")
    toplam = sum(len(v) for v in veri.values()) if isinstance(veri, dict) else 0
    return olcum(toplam, f"{m.group(1)} → {json.dumps(veri, ensure_ascii=False)[:200]}")


# ---------------------------------------------------------------- Python

def python_klasoru_bul(proje: Path, verilen: str | None) -> Path | None:
    if verilen:
        return proje / verilen
    for ad in ("python", "ml", "scripts", "tools", "araclar"):
        d = proje / ad
        if d.is_dir() and any(d.rglob("*.py")):
            return d
    return None


def ruff(klasor: Path | None, proje: Path) -> dict:
    if klasor is None:
        return olcum(sebep="Python klasörü bulunamadı (--python-klasoru ver).")
    kod, cikti = calistir(["ruff", "check", str(klasor), "--output-format", "json"], proje)
    if kod is None:
        return olcum(sebep=cikti)
    try:
        bulgular = json.loads(cikti[cikti.index("["): cikti.rindex("]") + 1])
    except ValueError:
        return olcum(sebep=f"ruff çıktısı çözümlenemedi: {cikti[-300:]}")
    return olcum(len(bulgular), f"ruff check {klasor.relative_to(proje)} → {len(bulgular)} bulgu")


def pytest_olc(klasor: Path | None, proje: Path) -> tuple[dict, dict]:
    if klasor is None:
        s = "Python klasörü bulunamadı (--python-klasoru ver)."
        return olcum(sebep=s), olcum(sebep=s)
    rapor = proje / ".olc_coverage.json"
    pytest = [sys.executable, "-m", "pytest"]
    kod, cikti = calistir([*pytest, "--version"], proje)
    if kod != 0:
        if shutil.which("pytest") is None:
            s = "pytest kurulu değil (pip install pytest pytest-cov)."
            return olcum(sebep=s), olcum(sebep=s)
        pytest = ["pytest"]
    kod, cikti = calistir(
        [*pytest, "-q", f"--cov={klasor}", f"--cov-report=json:{rapor}", str(klasor)],
        proje, zaman_asimi=1800,
    )
    if kod is None:
        return olcum(sebep=cikti), olcum(sebep=cikti)
    if "unrecognized arguments: --cov" in cikti:
        kod, cikti = calistir([*pytest, "-q", str(klasor)], proje, zaman_asimi=1800)
        kapsam = olcum(sebep="pytest-cov kurulu değil (pip install pytest-cov).")
    else:
        kapsam = None

    if kod == 5 or "no tests ran" in cikti:
        s = "Hiç Python testi bulunamadı."
        return olcum(sebep=s), kapsam or olcum(sebep=s)
    ozet = next((s for s in reversed(cikti.splitlines()) if re.search(r"\d+ (passed|failed|error)", s)), "")
    if not ozet:
        return olcum(sebep=f"pytest özeti okunamadı: {cikti[-300:]}"), kapsam or olcum(sebep="pytest çalışmadı.")
    m_fail = re.search(r"(\d+) failed", ozet)
    m_err = re.search(r"(\d+) errors?", ozet)
    basarisiz = (int(m_fail.group(1)) if m_fail else 0) + (int(m_err.group(1)) if m_err else 0)
    test_kaydi = olcum(basarisiz, f"pytest → {ozet.strip('= ')}")

    if kapsam is None:
        if rapor.is_file():
            yuzde = json.loads(rapor.read_text())["totals"]["percent_covered"]
            rapor.unlink()
            kapsam = olcum(round(yuzde, 2), f"pytest --cov={klasor.relative_to(proje)} → totals.percent_covered")
        else:
            kapsam = olcum(sebep="Kapsam raporu oluşmadı.")
    return test_kaydi, kapsam


def model_boyutu(proje: Path, model: str | None) -> dict:
    if not model:
        return olcum(sebep="--model verilmedi.")
    yol = proje / model
    if not yol.is_file():
        return olcum(sebep=f"{model} bulunamadı.")
    b = yol.stat().st_size
    return olcum(round(b / MB, 2), f"{model} → {b} bayt")


# ---------------------------------------------------------------- Fonksiyonel (F) kriterler

TEST_YOLU_RE = re.compile(r"((?:integration_test|test)/[\w/.-]+_test\.dart|[\w/.-]*test_[\w.-]+\.py|[\w/.-]+_test\.py)")


def fonksiyonel_testler(proje: Path, kriterler: list[dict]) -> dict[str, dict]:
    """Her F kriterinin ölçüm yöntemindeki test dosyasını çalıştırır: geçti = 1, kaldı = 0, çalıştırılamadı = null."""
    sonuc: dict[str, dict] = {}
    for k in kriterler:
        if k.get("kategori") != "fonksiyonel":
            continue
        yollar = TEST_YOLU_RE.findall(k.get("olcum_yontemi", ""))
        if not yollar:
            sonuc[k["id"]] = olcum(sebep="Ölçüm yönteminde test dosyası yolu yok.")
            continue
        kanitlar, deger = [], 1
        for y in yollar:
            if not (proje / y).is_file():
                sonuc[k["id"]] = olcum(sebep=f"{y} yok.")
                break
            if y.startswith("integration_test/"):
                sonuc[k["id"]] = olcum(sebep=f"{y} cihaz/emülatör gerektirir: flutter test {y} -d <cihaz>")
                break
            # Yalnızca bu kriterin ID'sini adında taşıyan testler çalıştırılır (aynı dosyadaki başka kriter etkilemez).
            idk = re.escape(k["id"]).replace("\\-", "-?")
            if y.endswith(".dart"):
                komut = ["flutter", "test", y, "--name", rf"(^|[^0-9A-Za-z]){idk}([^0-9]|$)"]
            else:
                komut = [sys.executable, "-m", "pytest", "-q", y, "-k", k["id"].lower().replace("-", "")]
            kod, cikti = calistir(komut, proje, zaman_asimi=900)
            if kod is None:
                sonuc[k["id"]] = olcum(sebep=cikti)
                break
            ozet_re = re.compile(r"All tests passed|Some tests failed|\d+ (passed|failed)|[+-]\d+")
            son = next((s.strip() for s in reversed(cikti.splitlines()) if ozet_re.search(s)), "")
            gosterim = f"flutter test {y}" if y.endswith(".dart") else f"pytest {y}"
            kanitlar.append(f"{gosterim} → çıkış kodu {kod}: {son[-120:]}")
            if "No tests ran" in cikti or "no tests ran" in cikti or re.search(r"\b0 selected|deselected", son) and "passed" not in son:
                sonuc[k["id"]] = olcum(sebep=f"{y} içinde adı {k['id']} taşıyan test yok.")
                break
            if kod != 0:
                deger = 0
        else:
            sonuc[k["id"]] = olcum(deger, " | ".join(kanitlar))
    return sonuc


# ---------------------------------------------------------------- Tasarım (T) ve mimari (Y)

def _test_sayimi(proje: Path, argumanlar: list[str]) -> tuple[int | None, int, int, str]:
    """flutter test --reporter json → (çıkış kodu, geçen, başarısız, çıktı). Atlanan testler sayılmaz."""
    kod, cikti = calistir(["flutter", "test", *argumanlar, "--reporter", "json"], proje, zaman_asimi=1800)
    gecen = basarisiz = 0
    for satir in cikti.splitlines() if kod is not None else []:
        try:
            olay = json.loads(satir)
        except json.JSONDecodeError:
            continue
        if isinstance(olay, dict) and olay.get("type") == "testDone" and not olay.get("hidden") and not olay.get("skipped"):
            if olay.get("result") == "success":
                gecen += 1
            else:
                basarisiz += 1
    return kod, gecen, basarisiz, cikti


def tasarim_olcumleri(proje: Path) -> dict[str, dict]:
    """T1–T3 (statik), T4 yerleşim testleri, T5 tasarım görseliyle piksel farkı, T6 onaylı görüntü sapması."""
    sys.path.insert(0, str(Path(__file__).parent))
    import goruntu_karsilastir  # noqa: PLC0415
    import tasarim  # noqa: PLC0415

    sonuc = tasarim.denetle(proje)
    ekranlar = tasarim.json_yukle(proje / "ekranlar.json")
    if ekranlar is None or sonuc["tasarim_uretim_uyumsuz"]["deger"] is None:
        neden = "ekranlar.json yok veya tasarım dosyaları geçersiz (tasarim.py dogrula)."
        for k in ("tasarim_yerlesim_hata", "tasarim_goruntu_fark_yuzde", "tasarim_onayli_goruntu_sapma"):
            sonuc[k] = olcum(sebep=neden)
        return sonuc

    if not (proje / tasarim.YERLESIM_KLASORU).is_dir():
        sonuc["tasarim_yerlesim_hata"] = olcum(sebep="test/yerlesim yok — python tasarim.py uret çalıştır.")
    else:
        kod, gecen, kalan, cikti = _test_sayimi(proje, [tasarim.YERLESIM_KLASORU])
        sonuc["tasarim_yerlesim_hata"] = (
            olcum(sebep=cikti) if kod is None else
            olcum(sebep=f"Yerleşim testleri çalışmadı (çıkış kodu {kod}): {cikti[-300:]}") if gecen + kalan == 0 else
            olcum(kalan, f"flutter test {tasarim.YERLESIM_KLASORU} → {gecen} kontrol geçti, {kalan} başarısız")
        )

    kod, cikti = calistir(["flutter", "test", "--update-goldens", "--dart-define=GORUNTU_KLASORU=olcum",
                           tasarim.GORUNTU_KLASORU], proje, zaman_asimi=1800)
    farklar, eksik = [], []
    fark_klasoru = proje / "build" / "tasarim_fark"
    fark_klasoru.mkdir(parents=True, exist_ok=True)
    for e in ekranlar["ekranlar"]:
        ref = e.get("referans_goruntu")
        uyg = proje / tasarim.GORUNTU_KLASORU / "olcum" / f"{e['ad']}.png"
        if not ref or not (proje / ref).is_file():
            eksik.append(f"{e['ad']}: kullanıcının tasarım görseli yok ({ref or 'referans_goruntu tanımsız'})")
        elif not uyg.is_file():
            eksik.append(f"{e['ad']}: ekran görüntüsü üretilemedi ({(cikti or '')[-200:]})")
        else:
            try:
                yuzde, kanit = goruntu_karsilastir.karsilastir(proje / ref, uyg, 16, fark_klasoru / f"{e['ad']}.png")
                farklar.append((yuzde, kanit))
            except (ValueError, OSError) as hata:
                eksik.append(f"{e['ad']}: {hata}")
    if eksik:
        sonuc["tasarim_goruntu_fark_yuzde"] = olcum(sebep="; ".join(eksik))
    else:
        sonuc["tasarim_goruntu_fark_yuzde"] = olcum(
            max(f[0] for f in farklar),
            "en büyük fark raporlanır | " + " | ".join(f[1] for f in farklar) + " | fark görüntüleri: build/tasarim_fark/",
        )

    onayli = list((proje / tasarim.GORUNTU_KLASORU / "goldens").glob("*.png"))
    if not onayli:
        sonuc["tasarim_onayli_goruntu_sapma"] = olcum(
            sebep="Onaylı ekran görüntüsü yok: kullanıcı ekran görüntülerini onaylayınca "
                  "'flutter test --update-goldens test/goruntu' ile goldens/ oluşturulur.")
    else:
        kod, gecen, kalan, cikti = _test_sayimi(proje, [tasarim.GORUNTU_KLASORU])
        sonuc["tasarim_onayli_goruntu_sapma"] = (
            olcum(sebep=cikti) if kod is None else
            olcum(kalan, f"flutter test {tasarim.GORUNTU_KLASORU} → {gecen} ekran onaylı görüntüyle aynı, {kalan} sapma")
        )
    return sonuc


def mimari_olcumleri(proje: Path) -> dict[str, dict]:
    sys.path.insert(0, str(Path(__file__).parent))
    import mimari  # noqa: PLC0415

    return mimari.denetle(proje)


# ---------------------------------------------------------------- Ana akış

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--proje", default=".")
    ap.add_argument("--cikti", default="olcumler.json")
    ap.add_argument("--kriterler", default=None, help="kabul_kriterleri.json (izinli izin listesi için)")
    ap.add_argument("--python-klasoru", default=None)
    ap.add_argument("--model", default=None)
    ap.add_argument("--build-apk", action="store_true", help="Ölçmeden önce release APK üret")
    ap.add_argument("--atla", default="", help="Virgülle ayrılmış, atlanacak ölçüm anahtarları")
    a = ap.parse_args()

    proje = Path(a.proje).resolve()
    atla = {x.strip() for x in a.atla.split(",") if x.strip()}
    izinli = None
    kriter_listesi: list[dict] = []
    kriter_yolu = Path(a.kriterler) if a.kriterler else proje / "kabul_kriterleri.json"
    if kriter_yolu.is_file():
        kriter_verisi = json.loads(kriter_yolu.read_text(encoding="utf-8"))
        izinli = kriter_verisi.get("izinli_android_izinleri")
        kriter_listesi = kriter_verisi.get("kriterler", [])

    sonuc: dict[str, dict] = {}

    def ekle(anahtar: str, fn):
        if anahtar in atla:
            return
        sonuc[anahtar] = fn()
        print(f"  {anahtar}: {sonuc[anahtar].get('deger')}  {sonuc[anahtar].get('sebep', '')}")

    print(f"Ölçülüyor: {proje}")
    flutter_proje = (proje / "pubspec.yaml").is_file()
    if flutter_proje:
        ekle("flutter_analyze_bulgu", lambda: flutter_analyze(proje))
        ekle("dart_format_degisen", lambda: dart_format(proje))
        if not {"dart_basarisiz_test", "dart_kapsam_yuzde"} <= atla:
            t, k = flutter_test(proje)
            sonuc["dart_basarisiz_test"], sonuc["dart_kapsam_yuzde"] = t, k
            print(f"  dart_basarisiz_test: {t.get('deger')}  {t.get('sebep', '')}")
            print(f"  dart_kapsam_yuzde: {k.get('deger')}  {k.get('sebep', '')}")
        ekle("apk_boyutu_mb", lambda: apk_boyutu(proje, a.build_apk))
        sonuc["min_sdk"], sonuc["target_sdk"] = gradle_sdk(proje)
        sonuc["internet_izni_sayisi"], sonuc["fazla_izin_sayisi"] = izin_olcumleri(proje, izinli)
        for k in ("min_sdk", "target_sdk", "internet_izni_sayisi", "fazla_izin_sayisi"):
            print(f"  {k}: {sonuc[k].get('deger')}  {sonuc[k].get('sebep', '')}")
        ekle("ag_kodu_referansi", lambda: ag_kodu(proje))
        ekle("sabit_metin_sayisi", lambda: sabit_metin(proje))
        ekle("cevrilmemis_anahtar", lambda: cevrilmemis(proje))
        for kaynak in (tasarim_olcumleri, mimari_olcumleri):
            for anahtar, kayit in kaynak(proje).items():
                if anahtar not in atla:
                    sonuc[anahtar] = kayit
                    print(f"  {anahtar}: {kayit.get('deger')}  {kayit.get('sebep', '')[:160]}")
    else:
        print("  pubspec.yaml yok — Flutter ölçümleri atlandı.")

    py = python_klasoru_bul(proje, a.python_klasoru)
    ekle("ruff_bulgu", lambda: ruff(py, proje))
    if not {"python_basarisiz_test", "python_kapsam_yuzde"} <= atla:
        t, k = pytest_olc(py, proje)
        sonuc["python_basarisiz_test"], sonuc["python_kapsam_yuzde"] = t, k
        print(f"  python_basarisiz_test: {t.get('deger')}  {t.get('sebep', '')}")
        print(f"  python_kapsam_yuzde: {k.get('deger')}  {k.get('sebep', '')}")
    for anahtar, kayit in fonksiyonel_testler(proje, kriter_listesi).items():
        if anahtar not in atla:
            sonuc[anahtar] = kayit
            print(f"  {anahtar}: {kayit.get('deger')}  {kayit.get('sebep', '')}")
    if a.model:
        ekle("model_boyutu_mb", lambda: model_boyutu(proje, a.model))

    cikti = Path(a.cikti)
    mevcut = {}
    if cikti.is_file():
        try:
            mevcut = json.loads(cikti.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            mevcut = {}
    mevcut.update(sonuc)  # elle girilmiş kriter-id kayıtları (P1, M1…) korunur
    cikti.write_text(json.dumps(mevcut, ensure_ascii=False, indent=2), encoding="utf-8")
    olculemeyen = [k for k, v in sonuc.items() if v.get("deger") is None]
    print(f"\n{cikti} yazıldı. {len(sonuc)} otomatik ölçüm, {len(olculemeyen)} tanesi ölçülemedi: {', '.join(olculemeyen) or '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
