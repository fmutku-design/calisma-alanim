#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
talimat_duzelt.py (v1.0) - Mikroskop AI talimat dosyalarinda 15.10.2026 onariminin
ekledigi "bagimsiz isler ilerler / onay tekrar istenmez" katmanini, ozgun durma ve
onay kurallarina (kuralar/Ajan Davranis Kurallari.txt: R5, R6, Y6, Ihlal) baglar.
Kaynak kod sadece ASCII.

VARSAYILAN KURU CALISMADIR: hicbir dosyaya dokunmaz, yalniz degisecek satirlari gosterir.
Dosyalar yalniz --uygula verilirse degisir.

Kullanim (PowerShell, Downloads'tan):
  python -X utf8 talimat_duzelt.py --secenek A                # ne degisecegini goster
  python -X utf8 talimat_duzelt.py --secenek A --uygula       # uygula
  python -X utf8 talimat_duzelt.py --secenek B --atla fikrin_ozu

Secenekler:
  A  Ozgun kurallarin aynen gecerli: ihlalde ve belirsizlikte is durur, ajan sorar;
     yeni klasor/dosya/not/kayit icin her seferinde onay (Y6).
  B  A ile ayni; tek fark: onay mesajinda adi gecen is ve dosyalar icin ayni onay
     tekrar istenmez. Adi gecmeyen her yeni klasor/dosya/not/kayit icin onay gerekir.

Dosya anahtarlari (--atla icin): ajan_kurallari, agents, calisma_duzeni,
  kabul_proseduru, readme_yonlendirici, fikrin_ozu

Guvenlik:
  - Her duzenleme, dosyada TAM OLARAK bir kez gecen eski metne uygulanir. Bir eski metin
    bulunamazsa (dosya bu arada degismisse) HICBIR dosya degistirilmez (hep ya da hic).
  - Bu aracin surum notunu tasiyan dosya zaten duzeltilmis sayilir ve atlanir. Secenegi
    degistirmek icin once yedekteki dosyalari geri koy.
  - Ozgun dosyalarin kopyasi proje DISINA yazilir: ./talimat_yedek_<zaman>/
  - Kodlama (BOM) ve satir sonu (LF/CRLF) korunur.
  - Degisen dosyalarin eski ve yeni SHA-256 degerleri yazilir (manifesto guncellemesi icin).
  - Degistirilmeyenler: alt klasorlerdeki AGENTS.md (yalniz yonlendirme), gorsel toplama
    protokolu (ozgun kurallarla uyumlu), D:\ README, ANA DOGRULAMA, karar_dizini.json.
"""
import argparse
import datetime
import difflib
import hashlib
import sys
from pathlib import Path

DEFAULT_ROOT = Path.home() / "Desktop" / "mikroskop ai \u00e7al\u0131\u015fma klas\u00f6r\u00fc"
MARK = "kullan\u0131c\u0131 onay\u0131yla)"  # bu aracin yazdigi surum notunun imi

FILES = [
    {
        "anahtar": "ajan_kurallari",
        "yol": ["kuralar", "Ajan Davran\u0131\u015f Kurallar\u0131.txt"],
        "duzenlemeler": [
            ("\nTarih: 2026-10-15\n",
             "\nTarih: 2026-10-15 (v2); {tarih} (v3)\n"),
            ("S\u00fcr\u00fcm: v2 a\u00e7\u0131klama eki. A\u015fa\u011f\u0131daki \u00f6zg\u00fcn kural metni aynen korunmu\u015ftur.\n",
             {"A": "S\u00fcr\u00fcm: v3. De\u011fi\u015fiklik ({tarih}, kullan\u0131c\u0131 onay\u0131yla): a\u00e7\u0131klama ekindeki Y6 yorumu kald\u0131r\u0131ld\u0131; R5 ve ihlal a\u00e7\u0131klamalar\u0131 \u00f6zg\u00fcn metne ba\u011fland\u0131 (i\u015f durur). Bu dosyada ba\u011flay\u0131c\u0131 olan \u00f6zg\u00fcn kural metnidir; a\u00e7\u0131klamalar onunla \u00e7eli\u015firse \u00f6zg\u00fcn metin ge\u00e7erlidir. A\u015fa\u011f\u0131daki \u00f6zg\u00fcn kural metni aynen korunmu\u015ftur.\n", "B": "S\u00fcr\u00fcm: v3. De\u011fi\u015fiklik ({tarih}, kullan\u0131c\u0131 onay\u0131yla): a\u00e7\u0131klama ekindeki Y6, R5 ve ihlal a\u00e7\u0131klamalar\u0131 \u00f6zg\u00fcn metne ba\u011fland\u0131 (i\u015f durur; onay mesaj\u0131nda ad\u0131 ge\u00e7en i\u015f i\u00e7in onay tekrar istenmez). Bu dosyada ba\u011flay\u0131c\u0131 olan \u00f6zg\u00fcn kural metnidir; a\u00e7\u0131klamalar onunla \u00e7eli\u015firse \u00f6zg\u00fcn metin ge\u00e7erlidir. A\u015fa\u011f\u0131daki \u00f6zg\u00fcn kural metni aynen korunmu\u015ftur.\n"}),
            ("- Y6 yeni ve tan\u0131ms\u0131z i\u015flem i\u00e7in onay gerektirir. Kullan\u0131c\u0131n\u0131n istedi\u011fi tan\u0131ml\u0131 i\u015fin ayn\u0131 kapsamdaki gerekli uygulama/test/kay\u0131t ad\u0131mlar\u0131 i\u00e7in \u00f6nceki izin tekrar istenmez. Veri README s\u0131n\u0131rlar\u0131 korunur.\n",
             {"A": "", "B": "- Y6: Kullan\u0131c\u0131n\u0131n bir onay mesaj\u0131nda ad\u0131n\u0131 verdi\u011fi i\u015f ve dosyalar i\u00e7in ayn\u0131 onay tekrar istenmez. Onay mesaj\u0131nda ad\u0131 ge\u00e7meyen her yeni klas\u00f6r, dosya, not veya kay\u0131t i\u00e7in Y6 aynen ge\u00e7erlidir. Veri README s\u0131n\u0131rlar\u0131 korunur.\n"}),
            ("- R5 kapsam\u0131nda izinsiz de\u011fi\u015fiklik g\u00f6r\u00fcl\u00fcrse \u00f6zg\u00fcn kopya ve fark korunur, durum bildirilir; ajan kullan\u0131c\u0131 verisini veya tarihsel kayd\u0131 kendili\u011finden silerek geri alma yapmaz.\n",
             "- R5 kapsam\u0131nda izinsiz de\u011fi\u015fiklik g\u00f6r\u00fcl\u00fcrse i\u015f durur; \u00f6zg\u00fcn kopya ve fark korunur, durum kullan\u0131c\u0131ya bildirilir. Geri alma karar\u0131 kullan\u0131c\u0131n\u0131nd\u0131r; ajan kendili\u011finden silmez.\n"),
            ("- Bir \u00e7eli\u015fki veya ihlal, do\u011frudan kayna\u011f\u0131na g\u00f6re raporlan\u0131r. Yaln\u0131z etkilenen karar/ad\u0131m bekler; ba\u011f\u0131ms\u0131z yetkili i\u015fler ilerler. Fikir veya kabul ko\u015fulu tahminle doldurulmaz.\n",
             "- Bir \u00e7eli\u015fki veya ihlal, do\u011frudan kayna\u011f\u0131na g\u00f6re raporlan\u0131r ve i\u015f durur (\u00f6zg\u00fcn metin: \u201c\u0130hlal g\u00f6r\u00fcl\u00fcrse i\u015f DURUR\u201d). Fikir veya kabul ko\u015fulu tahminle doldurulmaz.\n"),
        ],
    },
    {
        "anahtar": "agents",
        "yol": ["AGENTS.md"],
        "duzenlemeler": [
            ("\nTarih: 2026-10-15\n",
             "\nTarih: 2026-10-15 (v2); {tarih} (v3)\n"),
            ("S\u00fcr\u00fcm: v2. De\u011fi\u015fiklik: kaynak yollar\u0131, karar eri\u015fimi, yetki kapsam\u0131 ve tamamlanma ayr\u0131m\u0131 onar\u0131ld\u0131. Bu s\u00fcr\u00fcm \u00fcr\u00fcn kabul\u00fc de\u011fildir.\n",
             "S\u00fcr\u00fcm: v3. De\u011fi\u015fiklik ({tarih}, kullan\u0131c\u0131 onay\u0131yla): E7, E8 ve denetleyici sat\u0131r\u0131 \u00f6zg\u00fcn durma ve onay kurallar\u0131na ba\u011fland\u0131 (kuralar/Ajan Davran\u0131\u015f Kurallar\u0131.txt: R5, R6, Y6, \u0130hlal). v2: kaynak yollar\u0131, karar eri\u015fimi, yetki kapsam\u0131 ve tamamlanma ayr\u0131m\u0131 onar\u0131ld\u0131. Bu s\u00fcr\u00fcm \u00fcr\u00fcn kabul\u00fc de\u011fildir.\n"),
            ("Denetleyiciye eri\u015filemiyorsa veya fark bildiriyorsa eksik kontrol\u00fc bildir; do\u011frulanm\u0131\u015f b\u00fct\u00fcnl\u00fck iddias\u0131 kurma. Okuma ve sorun analizi s\u00fcrd\u00fcr\u00fclebilir. Kayna\u011f\u0131 veya \u00f6l\u00e7\u00fct\u00fc fark\u0131 kapatmak i\u00e7in de\u011fi\u015ftirme.\n",
             "Denetleyiciye eri\u015filemiyorsa veya fark bildiriyorsa i\u015f durur; durumu kullan\u0131c\u0131ya bildir ve karar\u0131n\u0131 bekle. Do\u011frulanm\u0131\u015f b\u00fct\u00fcnl\u00fck iddias\u0131 kurma. Kayna\u011f\u0131 veya \u00f6l\u00e7\u00fct\u00fc fark\u0131 kapatmak i\u00e7in de\u011fi\u015ftirme.\n"),
            ("E7 \u00d6nceden verilmi\u015f onay ayn\u0131 kapsam i\u00e7in tekrar istenmez. Tan\u0131ml\u0131 i\u015fin gerekli kod/test/kay\u0131t i\u015flemleri y\u00fcr\u00fct\u00fcl\u00fcr. Fikir, kaynak anlam\u0131, kabul ko\u015fulu veya veri izinleri de\u011fi\u015fecekse somut de\u011fi\u015fiklik ve etkisi sunulur; yetki ba\u015fka dosyaya/genel kabule geni\u015fletilmez.\n",
             {"A": "E7 Onay kurallar\u0131 kuralar/Ajan Davran\u0131\u015f Kurallar\u0131.txt (Y6, R5) ve D:\\g\u00f6r\u00fcnt\u00fc veri seti\\README.txt i\u00e7indedir; bu dosya onlar\u0131 yorumlamaz. Fikir, kaynak anlam\u0131, kabul ko\u015fulu veya veri izinleri de\u011fi\u015fecekse somut de\u011fi\u015fiklik ve etkisi sunulur; yetki ba\u015fka dosyaya/genel kabule geni\u015fletilmez.\n", "B": "E7 Kullan\u0131c\u0131n\u0131n bir onay mesaj\u0131nda ad\u0131n\u0131 verdi\u011fi i\u015f ve dosyalar i\u00e7in ayn\u0131 onay tekrar istenmez; ad\u0131 ge\u00e7meyen her yeni klas\u00f6r, dosya, not veya kay\u0131t i\u00e7in onay gerekir (Ajan Davran\u0131\u015f Kurallar\u0131 Y6). Fikir, kaynak anlam\u0131, kabul ko\u015fulu veya veri izinleri de\u011fi\u015fecekse somut de\u011fi\u015fiklik ve etkisi sunulur; yetki ba\u015fka dosyaya/genel kabule geni\u015fletilmez.\n"}),
            ("E8 Belirsizlikte etkilenen karar veya a\u015fama bekler. Ba\u011f\u0131ms\u0131z tan\u0131ml\u0131 i\u015fler ilerler; ba\u015far\u0131s\u0131zl\u0131k gizlenmez, ba\u015fka \u00f6l\u00e7\u00fctle kapat\u0131lmaz.\n",
             "E8 \u201cBelirsizlikte ajan tahmin etmez, sorar; kullan\u0131c\u0131n\u0131n fikri ad\u0131na yorum yapmaz.\u201d (Ajan Davran\u0131\u015f Kurallar\u0131 R6) \u201c\u0130hlal g\u00f6r\u00fcl\u00fcrse i\u015f DURUR, durum kullan\u0131c\u0131ya raporlan\u0131r; karar kullan\u0131c\u0131ya aittir.\u201d (Ajan Davran\u0131\u015f Kurallar\u0131) Ba\u015far\u0131s\u0131zl\u0131k gizlenmez, ba\u015fka \u00f6l\u00e7\u00fctle kapat\u0131lmaz.\n"),
        ],
    },
    {
        "anahtar": "calisma_duzeni",
        "yol": ["CALISMA_DUZENI.md"],
        "duzenlemeler": [
            ("\nTarih: 2026-10-15\n",
             "\nTarih: 2026-10-15 (v1); {tarih} (v2)\n"),
            ("S\u00fcr\u00fcm: v1 \u00e7al\u0131\u015fma ortam\u0131 onar\u0131m\u0131. Bu metin fikrin yeni \u00f6zeti de\u011fildir.\n",
             "S\u00fcr\u00fcm: v2. De\u011fi\u015fiklik ({tarih}, kullan\u0131c\u0131 onay\u0131yla): Yetki ve de\u011fi\u015fiklik b\u00f6l\u00fcm\u00fc \u00f6zg\u00fcn onay ve durma kurallar\u0131na ba\u011fland\u0131. v1: \u00e7al\u0131\u015fma ortam\u0131 onar\u0131m\u0131. Bu metin fikrin yeni \u00f6zeti de\u011fildir.\n"),
            ("Tan\u0131ml\u0131 ve kullan\u0131c\u0131 taraf\u0131ndan istenmi\u015f i\u015fin gerekli uygulama/test/kay\u0131t ad\u0131mlar\u0131 ayn\u0131 kapsam i\u00e7inde yap\u0131l\u0131r. Ayn\u0131 izin tekrar istenmez. Kaynak anlam\u0131n\u0131, fikri, kabul ko\u015fulunu, s\u00fcr\u00fcm kilidini veya veri iznini de\u011fi\u015ftiren i\u015flem i\u00e7in dosya, mevcut c\u00fcmle, \u00f6nerilen c\u00fcmle ve etkisi g\u00f6sterilir. \u00d6nceki dar onay ba\u015fka de\u011fi\u015fikliklere emsal yap\u0131lmaz. Ba\u011f\u0131ms\u0131z i\u015fler s\u00fcrerken yaln\u0131z karara ba\u011fl\u0131 ad\u0131m bekler.\n",
             {"A": "Onay ve durma kurallar\u0131 kuralar/Ajan Davran\u0131\u015f Kurallar\u0131.txt (\u00f6zg\u00fcn kural metni: R5, R6, Y6, \u0130hlal) ve D:\\g\u00f6r\u00fcnt\u00fc veri seti\\README.txt i\u00e7indedir; bu dosya onlar\u0131 yorumlamaz. Kaynak anlam\u0131n\u0131, fikri, kabul ko\u015fulunu, s\u00fcr\u00fcm kilidini veya veri iznini de\u011fi\u015ftiren i\u015flem i\u00e7in dosya, mevcut c\u00fcmle, \u00f6nerilen c\u00fcmle ve etkisi g\u00f6sterilir. \u00d6nceki dar onay ba\u015fka de\u011fi\u015fikliklere emsal yap\u0131lmaz.\n", "B": "Kullan\u0131c\u0131n\u0131n bir onay mesaj\u0131nda ad\u0131n\u0131 verdi\u011fi i\u015f ve dosyalar i\u00e7in ayn\u0131 onay tekrar istenmez; ad\u0131 ge\u00e7meyen her yeni klas\u00f6r, dosya, not veya kay\u0131t i\u00e7in onay gerekir. Belirsizlikte ve ihlalde kuralar/Ajan Davran\u0131\u015f Kurallar\u0131.txt (R6, \u0130hlal) ge\u00e7erlidir: i\u015f durur, kullan\u0131c\u0131ya sorulur. Kaynak anlam\u0131n\u0131, fikri, kabul ko\u015fulunu, s\u00fcr\u00fcm kilidini veya veri iznini de\u011fi\u015ftiren i\u015flem i\u00e7in dosya, mevcut c\u00fcmle, \u00f6nerilen c\u00fcmle ve etkisi g\u00f6sterilir. \u00d6nceki dar onay ba\u015fka de\u011fi\u015fikliklere emsal yap\u0131lmaz.\n"}),
        ],
    },
    {
        "anahtar": "kabul_proseduru",
        "yol": ["do\u011frulama prosed\u00fcr\u00fc", "Kabul ve Do\u011frulama Prosed\u00fcr\u00fc.txt"],
        "duzenlemeler": [
            ("\nTarih: 2026-10-15\n",
             "\nTarih: 2026-10-15 (v2); {tarih} (v3)\n"),
            ("S\u00fcr\u00fcm: v2. De\u011fi\u015fiklik: yetki kapsam\u0131, A3/alfa kararlar\u0131, ana 5\u00d75 test kayna\u011f\u0131 ve teknik sonu\u00e7/son kabul ayr\u0131m\u0131 a\u00e7\u0131kland\u0131.\n",
             "S\u00fcr\u00fcm: v3. De\u011fi\u015fiklik ({tarih}, kullan\u0131c\u0131 onay\u0131yla): A ve C maddeleri \u00f6zg\u00fcn onay ve durma kurallar\u0131na ba\u011fland\u0131. v2: yetki kapsam\u0131, A3/alfa kararlar\u0131, ana 5\u00d75 test kayna\u011f\u0131 ve teknik sonu\u00e7/son kabul ayr\u0131m\u0131 a\u00e7\u0131kland\u0131.\n"),
            ("A) Kullan\u0131c\u0131n\u0131n istedi\u011fi tan\u0131ml\u0131 i\u015fin gerekli uygulama/test/kay\u0131t ad\u0131mlar\u0131 ayn\u0131 yetki kapsam\u0131nda yap\u0131l\u0131r. Verilmi\u015f onay tekrar istenmez. Yap\u0131lan i\u015f ve kan\u0131tlar bildirilir.\n",
             {"A": "A) Kullan\u0131c\u0131n\u0131n istedi\u011fi tan\u0131ml\u0131 i\u015fin uygulama ve test ad\u0131mlar\u0131 onaylanan kapsamda yap\u0131l\u0131r. Yeni klas\u00f6r, dosya, not veya kay\u0131t i\u00e7in Ajan Davran\u0131\u015f Kurallar\u0131 Y6 ge\u00e7erlidir. Yap\u0131lan i\u015f ve kan\u0131tlar bildirilir.\n", "B": "A) Kullan\u0131c\u0131n\u0131n istedi\u011fi tan\u0131ml\u0131 i\u015fin uygulama ve test ad\u0131mlar\u0131 onaylanan kapsamda yap\u0131l\u0131r. Onay mesaj\u0131nda ad\u0131 ge\u00e7en i\u015f i\u00e7in ayn\u0131 onay tekrar istenmez; ad\u0131 ge\u00e7meyen yeni klas\u00f6r, dosya, not veya kay\u0131t i\u00e7in Ajan Davran\u0131\u015f Kurallar\u0131 Y6 ge\u00e7erlidir. Yap\u0131lan i\u015f ve kan\u0131tlar bildirilir.\n"}),
            ("C) Tan\u0131ms\u0131z noktada yaln\u0131z ona ba\u011fl\u0131 ad\u0131m bekler; ba\u011f\u0131ms\u0131z yetkili i\u015fler ilerler. Test ba\u015far\u0131s\u0131zl\u0131\u011f\u0131 raporlan\u0131r ve neden analizi yap\u0131l\u0131r. \u0130stenen onar\u0131m kapsam\u0131ndaysa kusur d\u00fczeltilir; \u00f6l\u00e7\u00fct de\u011fi\u015ftirilmez.\n",
             "C) Tan\u0131ms\u0131z noktada i\u015f durur ve kullan\u0131c\u0131ya sorulur (Ajan Davran\u0131\u015f Kurallar\u0131 R6). Test ba\u015far\u0131s\u0131zl\u0131\u011f\u0131 raporlan\u0131r ve neden analizi yap\u0131l\u0131r. \u0130stenen onar\u0131m kapsam\u0131ndaysa kusur d\u00fczeltilir; \u00f6l\u00e7\u00fct de\u011fi\u015ftirilmez.\n"),
        ],
    },
    {
        "anahtar": "readme_yonlendirici",
        "yol": ["README_YONLENDIRICI.txt"],
        "duzenlemeler": [
            ("\nTarih: 2026-10-15\n",
             "\nTarih: 2026-10-15 (v2); {tarih} (v3)\n"),
            ("S\u00fcr\u00fcm: v2. De\u011fi\u015fiklik: mevcut kod/veri yollar\u0131 ve \u00f6nceki izinlerin kapsam\u0131 a\u00e7\u0131kland\u0131.\n",
             "S\u00fcr\u00fcm: v3. De\u011fi\u015fiklik ({tarih}, kullan\u0131c\u0131 onay\u0131yla): 5. ve 6. b\u00f6l\u00fcmler \u00f6zg\u00fcn onay ve durma kurallar\u0131na ba\u011fland\u0131. v2: mevcut kod/veri yollar\u0131 ve \u00f6nceki izinlerin kapsam\u0131 a\u00e7\u0131kland\u0131.\n"),
            ("Kapsam\u0131 belli bir i\u015flem i\u00e7in verilmi\u015f onay yeniden istenmez; yeni veri i\u015flemi veya istisna i\u00e7in ilgili karar al\u0131n\u0131r. Bkz. CALISMA_DUZENI.md.\n",
             {"A": "Onay kurallar\u0131 i\u00e7in bkz. kuralar/Ajan Davran\u0131\u015f Kurallar\u0131.txt ve D:\\g\u00f6r\u00fcnt\u00fc veri seti\\README.txt.\n", "B": "Onay mesaj\u0131nda ad\u0131 ge\u00e7en i\u015f i\u00e7in ayn\u0131 onay yeniden istenmez; ad\u0131 ge\u00e7meyen yeni veri i\u015flemi, klas\u00f6r, not veya kay\u0131t i\u00e7in onay al\u0131n\u0131r. Bkz. kuralar/Ajan Davran\u0131\u015f Kurallar\u0131.txt.\n"}),
            ("- Eri\u015fime ba\u011fl\u0131 ad\u0131m\u0131 durdur; ba\u011f\u0131ms\u0131z tan\u0131ml\u0131 i\u015fler s\u00fcrd\u00fcr\u00fclebilir.\n",
             "- \u0130\u015fi durdur.\n"),
        ],
    },
    {
        "anahtar": "fikrin_ozu",
        "yol": ["plan", "fikrin_ozu.md"],
        "duzenlemeler": [
            ("\u00c7al\u0131\u015fma a\u00e7\u0131klamas\u0131 \u2014 2026-10-15, v1 ek\nKaynak: kullan\u0131c\u0131n\u0131n ortam onar\u0131m\u0131 talimat\u0131; \u00e7al\u0131\u015fma prosed\u00fcrleri/karar_dizini.json.\nA\u015fa\u011f\u0131daki \u00f6nceki metin aynen korunmu\u015ftur. Etkin uygulamada CALISMA_DUZENI.md ve do\u011frudan kararlar K-02\u2013K-07 okunur. N/n \u00fcyelik/i\u015faretleme, A3, ara alfa ve ana A\u015fama 4 i\u00e7in eski ifadeler do\u011frudan karar\u0131n yerine kullan\u0131lamaz. Hedef 95 ve Ek/G gibi tan\u0131ms\u0131z noktalar a\u00e7\u0131k kal\u0131r. Bu ek fikir metnini yeniden yazmaz ve \u00fcr\u00fcn kabul\u00fc vermez.\n\n",
             ""),
        ],
    },
]


def load(p):
    raw = p.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = (raw[3:] if bom else raw).decode("utf-8")
    crlf = "\r\n" in text
    return raw, bom, crlf, text.replace("\r\n", "\n")


def encode(text, bom, crlf):
    if crlf:
        text = text.replace("\n", "\r\n")
    data = text.encode("utf-8")
    return b"\xef\xbb\xbf" + data if bom else data


def inside(p, root):
    try:
        Path(p).resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Talimat duzeltmesi (varsayilan: kuru calisma)")
    ap.add_argument("kok", nargs="?", default=str(DEFAULT_ROOT))
    ap.add_argument("--secenek", required=True, choices=["A", "B"])
    ap.add_argument("--atla", nargs="*", default=[], help="atlanacak dosya anahtarlari")
    ap.add_argument("--uygula", action="store_true", help="dosyalari gercekten degistir")
    a = ap.parse_args()

    root = Path(a.kok)
    if not root.is_dir():
        print("Klasor bulunamadi:", root)
        return 2
    keys = {f["anahtar"] for f in FILES}
    bad = [k for k in a.atla if k not in keys]
    if bad:
        print("Bilinmeyen anahtar:", ", ".join(bad), "| gecerli:", ", ".join(sorted(keys)))
        return 2
    today = datetime.date.today().isoformat()

    plan, problems = [], []
    for f in FILES:
        if f["anahtar"] in a.atla:
            print("ATLANDI (istegin):", f["anahtar"])
            continue
        p = root.joinpath(*f["yol"])
        if not p.is_file():
            problems.append("%s: dosya yok (%s)" % (f["anahtar"], p))
            continue
        raw, bom, crlf, text = load(p)
        if MARK in text:
            print("ATLANDI (zaten duzeltilmis; surum notunda bu aracin imi var):", f["anahtar"])
            continue
        new, missing = text, []
        for old, repl in f["duzenlemeler"]:
            r = repl[a.secenek] if isinstance(repl, dict) else repl
            n = new.count(old)
            if n == 0 and r == "":
                print("BILGI %s: silinecek metin zaten yok: %r" % (f["anahtar"], old[:60]))
                continue
            if n != 1:
                missing.append("eski metin %d kez bulundu (1 olmali): %r" % (n, old[:80]))
                continue
            new = new.replace(old, r.replace("{tarih}", today), 1)
        if missing:
            problems += ["%s: %s" % (f["anahtar"], m) for m in missing[:3]]
            if len(missing) > 3:
                problems.append("%s: ... %d sorun daha" % (f["anahtar"], len(missing) - 3))
        if new != text:
            plan.append((f, p, raw, bom, crlf, text, new))

    print("=" * 72)
    print("TALIMAT DUZELTMESI | secenek %s | %s" % (a.secenek, "UYGULAMA" if a.uygula else "KURU CALISMA (dosyalara dokunulmaz)"))
    print("Kok:", root)
    for f, p, raw, bom, crlf, text, new in plan:
        print("=" * 72)
        print("DOSYA: %s  [%s]" % (p, f["anahtar"]))
        for line in difflib.unified_diff(text.split("\n"), new.split("\n"), "simdi", "duzeltilmis", lineterm="", n=0):
            print("  " + line)
    if problems:
        print("=" * 72)
        print("SORUN VAR, HICBIR DOSYA DEGISTIRILMEDI:")
        for s in problems:
            print("  -", s)
        print("Dosya rapordaki halinden farkliysa bu duzenlemeyi elle yap ya da yeni raporu gonder.")
        return 1
    if not plan:
        print("=" * 72)
        print("Yapilacak degisiklik yok.")
        return 0
    if not a.uygula:
        print("=" * 72)
        print("Kuru calisma bitti. Uygulamak icin ayni komutu --uygula ile calistir.")
        return 0

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = Path.cwd() / ("talimat_yedek_" + stamp)
    if inside(backup, root):
        print("Yedek klasoru projenin icinde olamaz; komutu proje disindan (or. Downloads) calistir.")
        return 2
    print("=" * 72)
    print("Yedek:", backup)
    for f, p, raw, bom, crlf, text, new in plan:
        dst = backup.joinpath(*f["yol"])
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(raw)
    for f, p, raw, bom, crlf, text, new in plan:
        data = encode(new, bom, crlf)
        p.write_bytes(data)
        print("YAZILDI %-20s eski SHA-256 %s" % (f["anahtar"], hashlib.sha256(raw).hexdigest()))
        print("        %-20s yeni SHA-256 %s" % ("", hashlib.sha256(data).hexdigest()))
    print("=" * 72)
    print("Sonraki adimlar:")
    print("  1. AGENTS.md'deki ortam_denetimi.py komutunu calistir: bu dosyalar 'fark' diye gorunur (beklenen).")
    print("  2. ortam_manifestosu.json'i bu yeni SHA-256 degerleriyle, yeni surum ve onay kaydiyla guncelle.")
    print("     Guncellenmeden ajanlar duzeltilmis AGENTS.md geregi baslangicta durur.")
    print("  3. calisma_ortami_analizi.py ... --temel-kaydet ile yeni temeli kaydet.")
    print("  Geri almak icin yedekteki dosyalari ayni yerlerine kopyala.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
