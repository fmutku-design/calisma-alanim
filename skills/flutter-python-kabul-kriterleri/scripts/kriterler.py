#!/usr/bin/env python3
"""Kabul kriterleri dosyasını doğrular, tablo olarak basar ve ölçümlerle karşılaştırır.

Kullanım:
    python kriterler.py dogrula kabul_kriterleri.json
    python kriterler.py tablo   kabul_kriterleri.json
    python kriterler.py rapor   kabul_kriterleri.json olcumler.json

Sadece Python standart kütüphanesi kullanılır.
Çıkış kodu: 0 = her şey yolunda / tüm kriterler GEÇTİ, 1 = hata veya en az bir kriter GEÇMEDİ.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KATEGORILER = {
    "performans",
    "kod_kalitesi",
    "android",
    "offline",
    "ui_erisilebilirlik",
    "ml_veri",
    "fonksiyonel",
}
OPERATORLER = {"<=", ">=", "==", "<", ">"}
BIRIMLER = {"ms", "sn", "MB", "KB", "%", "adet", "dp", "fps", "api_seviyesi", "oran", "evet_hayir"}
ZORUNLU_ALANLAR = ("id", "kategori", "metrik", "operator", "esik", "birim", "olcum_yontemi", "olcum_ortami", "kaynak")

# Ölçüsüz, yoruma açık kelimeler. Kriter metninde geçerlerse kriter ölçülebilir değildir.
BELIRSIZ_DESENLER = [
    r"hızlı\w*", r"yavaş\w*", r"akıcı\w*", r"iyi", r"kötü", r"uygun\w*", r"makul\w*",
    r"kullanıcı dostu", r"modern\w*", r"düzgün\w*", r"güzel\w*", r"sorunsuz\w*", r"stabil\w*",
    r"kararlı\w*", r"performanslı\w*", r"verimli\w*", r"optimize\w*", r"yeterli\w*",
    r"kabul edilebilir\w*", r"mümkün olduğunca", r"gerektiği kadar", r"şık\w*", r"temiz\w*",
    r"fast", r"slow", r"smooth\w*", r"good", r"reasonable", r"user[- ]friendly", r"nice",
    r"clean", r"efficient\w*", r"acceptable", r"responsive", r"intuitive",
]
BELIRSIZ_RE = re.compile(r"(?<!\w)(" + "|".join(BELIRSIZ_DESENLER) + r")(?!\w)", re.IGNORECASE)


def yukle(yol: str) -> dict:
    try:
        return json.loads(Path(yol).read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"HATA: dosya bulunamadı: {yol}")
    except json.JSONDecodeError as e:
        sys.exit(f"HATA: {yol} geçerli JSON değil: {e}")


def sayi_mi(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def dogrula(veri: dict) -> list[str]:
    hatalar: list[str] = []
    if not isinstance(veri.get("surum"), int):
        hatalar.append("Üst seviye: 'surum' tam sayı olmalı (kriter değiştikçe artırılır).")
    onay = veri.get("onay")
    if not isinstance(onay, dict) or onay.get("durum") not in {"bekliyor", "onaylandi"}:
        hatalar.append("Üst seviye: 'onay.durum' 'bekliyor' veya 'onaylandi' olmalı.")
    izinler = veri.get("izinli_android_izinleri")
    if izinler is not None and not (isinstance(izinler, list) and all(isinstance(i, str) for i in izinler)):
        hatalar.append("Üst seviye: 'izinli_android_izinleri' metin listesi olmalı.")

    kriterler = veri.get("kriterler")
    if not isinstance(kriterler, list) or not kriterler:
        hatalar.append("Üst seviye: 'kriterler' boş olmayan bir liste olmalı.")
        return hatalar

    gorulen: set[str] = set()
    for i, k in enumerate(kriterler):
        etiket = k.get("id") or f"#{i + 1}"
        for alan in ZORUNLU_ALANLAR:
            if alan not in k or k[alan] in (None, ""):
                hatalar.append(f"{etiket}: '{alan}' alanı eksik veya boş.")
        if k.get("id") in gorulen:
            hatalar.append(f"{etiket}: id tekrar ediyor.")
        gorulen.add(k.get("id"))

        if k.get("kategori") and k["kategori"] not in KATEGORILER:
            hatalar.append(f"{etiket}: kategori '{k['kategori']}' geçersiz. Geçerli: {sorted(KATEGORILER)}")
        if k.get("operator") and k["operator"] not in OPERATORLER:
            hatalar.append(f"{etiket}: operator '{k['operator']}' geçersiz. Geçerli: {sorted(OPERATORLER)}")
        if k.get("birim") and k["birim"] not in BIRIMLER:
            hatalar.append(f"{etiket}: birim '{k['birim']}' geçersiz. Geçerli: {sorted(BIRIMLER)}")

        esik = k.get("esik")
        if "esik" in k and not sayi_mi(esik):
            hatalar.append(f"{etiket}: esik sayı olmalı, '{esik!r}' verilmiş. Metin eşik ölçülemez.")
        elif sayi_mi(esik):
            if k.get("birim") == "evet_hayir" and esik not in (0, 1):
                hatalar.append(f"{etiket}: evet_hayir biriminde esik 0 veya 1 olmalı.")
            if k.get("birim") == "%" and not 0 <= esik <= 100:
                hatalar.append(f"{etiket}: yüzde eşiği 0–100 arasında olmalı.")
            if esik < 0:
                hatalar.append(f"{etiket}: esik negatif olamaz.")

        yontem = k.get("olcum_yontemi") or ""
        if yontem and len(yontem.strip()) < 10:
            hatalar.append(f"{etiket}: olcum_yontemi çok kısa; çalıştırılabilir komut veya adım adım prosedür yaz.")

        for alan in ("metrik", "olcum_yontemi"):
            metin = k.get(alan) or ""
            bulunan = sorted({m.group(0).lower() for m in BELIRSIZ_RE.finditer(metin)})
            if bulunan:
                hatalar.append(
                    f"{etiket}: '{alan}' içinde ölçüsüz kelime var: {', '.join(bulunan)}. "
                    "Bunu sayısal bir ölçüye çevir."
                )
    return hatalar


def tablo(veri: dict) -> str:
    satirlar = [
        f"**{veri.get('proje', 'Proje')}** — kriter sürümü {veri.get('surum')} — onay: {veri.get('onay', {}).get('durum')}",
        "",
        "| ID | Kategori | Metrik | Hedef | Ölçüm yöntemi | Ortam | Kaynak |",
        "|---|---|---|---|---|---|---|",
    ]
    for k in veri.get("kriterler", []):
        hedef = f"{k.get('operator')} {k.get('esik')} {k.get('birim')}"
        satirlar.append(
            "| {id} | {kat} | {met} | {hedef} | {yon} | {ort} | {kay} |".format(
                id=k.get("id"),
                kat=k.get("kategori"),
                met=_hucre(k.get("metrik")),
                hedef=hedef,
                yon=_hucre(k.get("olcum_yontemi")),
                ort=_hucre(k.get("olcum_ortami")),
                kay=k.get("kaynak"),
            )
        )
    izinler = veri.get("izinli_android_izinleri")
    if izinler is not None:
        satirlar += ["", f"İzinli Android izinleri: {', '.join(izinler) if izinler else '(hiçbiri)'}"]
    return "\n".join(satirlar)


def _hucre(x) -> str:
    return str(x or "").replace("|", "\\|").replace("\n", " ")


def karsilastir(deger: float, op: str, esik: float) -> bool:
    return {
        "<=": deger <= esik,
        ">=": deger >= esik,
        "==": deger == esik,
        "<": deger < esik,
        ">": deger > esik,
    }[op]


def rapor(veri: dict, olcumler: dict) -> tuple[str, bool]:
    # olcumler.json biçimi: {"<anahtar>": {"deger": <sayı|null>, "kanit": "...", "sebep": "..."}}
    # Anahtar önce kriter id'si (ör. "P1"), yoksa kriterin olc_anahtari (ör. "apk_boyutu_mb") olarak aranır.
    if "olcumler" in olcumler and isinstance(olcumler["olcumler"], dict):
        olcumler = olcumler["olcumler"]

    satirlar = [
        "| ID | Metrik | Hedef | Ölçülen | Sonuç | Kanıt / Sebep |",
        "|---|---|---|---|---|---|",
    ]
    sayac = {"GEÇTİ": 0, "KALDI": 0, "ÖLÇÜLEMEDİ": 0}
    for k in veri.get("kriterler", []):
        kayit = olcumler.get(k["id"])
        if kayit is None and k.get("olc_anahtari"):
            kayit = olcumler.get(k["olc_anahtari"])
        hedef = f"{k['operator']} {k['esik']} {k['birim']}"

        if not isinstance(kayit, dict) or not sayi_mi(kayit.get("deger")):
            sonuc = "ÖLÇÜLEMEDİ"
            olculen = "—"
            aciklama = (kayit or {}).get("sebep") if isinstance(kayit, dict) else None
            aciklama = aciklama or "Ölçüm kaydı yok."
        elif not (kayit.get("kanit") or "").strip():
            sonuc = "ÖLÇÜLEMEDİ"
            olculen = str(kayit["deger"])
            aciklama = "Değer var ama kanıt (komut çıktısı) yok; kanıtsız değer kabul edilmez."
        else:
            deger = kayit["deger"]
            sonuc = "GEÇTİ" if karsilastir(deger, k["operator"], k["esik"]) else "KALDI"
            olculen = f"{deger} {k['birim']}"
            aciklama = kayit["kanit"]
        sayac[sonuc] += 1
        satirlar.append(
            f"| {k['id']} | {_hucre(k['metrik'])} | {hedef} | {olculen} | **{sonuc}** | {_hucre(aciklama)} |"
        )

    toplam = sum(sayac.values())
    hepsi_gecti = sayac["GEÇTİ"] == toplam and toplam > 0
    ozet = (
        f"\nToplam {toplam} kriter: {sayac['GEÇTİ']} GEÇTİ, {sayac['KALDI']} KALDI, "
        f"{sayac['ÖLÇÜLEMEDİ']} ÖLÇÜLEMEDİ.\n"
        + ("SONUÇ: Tüm kabul kriterleri karşılandı." if hepsi_gecti
           else "SONUÇ: İş tamamlanmadı — KALDI ve ÖLÇÜLEMEDİ satırları kapanmadan 'bitti' denemez.")
    )
    return "\n".join(satirlar) + "\n" + ozet, hepsi_gecti


def main(argv: list[str]) -> int:
    if len(argv) < 3 or argv[1] not in {"dogrula", "tablo", "rapor"}:
        print(__doc__)
        return 1
    komut, kriter_yolu = argv[1], argv[2]
    veri = yukle(kriter_yolu)

    hatalar = dogrula(veri)
    if komut == "dogrula":
        if hatalar:
            print(f"GEÇERSİZ — {len(hatalar)} hata:")
            for h in hatalar:
                print(f"  - {h}")
            return 1
        print(f"GEÇERLİ — {len(veri['kriterler'])} kriter, hepsi ölçülebilir biçimde tanımlı.")
        return 0

    if hatalar:
        print("Önce kriter dosyasını düzelt (python kriterler.py dogrula ...):")
        for h in hatalar:
            print(f"  - {h}")
        return 1

    if komut == "tablo":
        print(tablo(veri))
        return 0

    if len(argv) < 4:
        print("rapor için olcumler.json yolu gerekli.")
        return 1
    metin, hepsi_gecti = rapor(veri, yukle(argv[3]))
    print(metin)
    return 0 if hepsi_gecti else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
