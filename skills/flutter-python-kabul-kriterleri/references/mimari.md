# Örnek Mimari ve Kurulum Adımları

Bu dosya iki şey verir: (1) kullanıcıya **öneri** olarak sunulacak örnek mimari, (2) onaylanan mimarinin adım adım nasıl kurulacağı ve ölçüleceği. Çalışan, ölçülmüş tam örnek: `assets/ornek-proje/` (21/21 kriter GEÇTİ, `rapor.md`).

Mimari bir karardır: kullanıcı onaylamadan kurulmaz. Kullanıcı kendi mimarisini verirse o `mimari.json`'a yazılır ve bu örnek kullanılmaz.

## İçindekiler
1. Örnek mimari: klasör ağacı
2. Katman kuralları ve nedenleri
3. mimari.json (ölçülebilir hali)
4. Kurulum adımları (sırayla)
5. Python tarafı
6. Ölçüm: Y1–Y4

---

## 1. Örnek mimari: klasör ağacı

Özellik öncelikli (feature-first), her özellik içinde üç katman:

```
lib/
├── main.dart                         giris   — yalnızca runApp(const Uygulama())
├── uygulama.dart                     giris   — MaterialApp, tema, ilk ekran, bağımlılıkların kurulduğu tek yer
├── cekirdek/                         cekirdek — özellikler arası ortak, iş mantığı içermez
│   └── tema/
│       ├── tasarim.g.dart            ÜRETİLMİŞ (tasarim.json → scripts/tasarim.py uret)
│       └── tema.dart                 ThemeData — yalnızca Tasarim* sabitlerini kullanır
└── ozellikler/
    └── <ozellik>/                    ör. cevirici
        ├── alan/                     alan  — saf Dart: modeller, depo arayüzleri, iş kuralları
        │   ├── birim_donusumu.dart
        │   ├── donusum_deposu.dart   abstract interface class
        │   └── cevir.dart            saf fonksiyon (test edilmesi en kolay yer)
        ├── veri/                     veri  — depo arayüzünün uygulaması (asset, sqflite, dosya)
        │   └── asset_donusum_deposu.dart
        └── sunum/                    sunum — ekranlar ve widget'lar
            ├── cevirici_ekrani.dart
            └── sonuc_karti.dart
test/
├── ozellikler/                       F kriterlerinin testleri (adında kriter ID'si)
├── yerlesim/                         ÜRETİLMİŞ — ekranlar.json → T4
├── goruntu/                          ÜRETİLMİŞ — ekranlar.json → T5/T6; goldens/ = onaylı görüntüler
└── yardimci/tasarim_fontlari.dart    ÜRETİLMİŞ — testlerde gerçek font
tools/                                Python script'leri + test_*.py
tasarim/                              kullanıcının tasarım görselleri (<ekran>.png)
tasarim.json  ekranlar.json  mimari.json  kabul_kriterleri.json  kararlar.json
```

## 2. Katman kuralları ve nedenleri

| Katman | Import edebilir | Yasak | Neden |
|---|---|---|---|
| giris | hepsi | — | Uygulamanın birleştirildiği tek yer; somut sınıflar (ör. `AssetDonusumDeposu`) yalnızca burada seçilir. |
| cekirdek | — | özellik katmanları | Ortak kod özelliklere bağımlı olursa döngü oluşur. |
| alan | cekirdek | `package:flutter/`, `dart:io`, `dart:ui`, veri paketleri | İş kuralları UI ve depolamadan bağımsız olmalı; saf Dart olduğu için hızlı birim testi yazılır. |
| veri | alan, cekirdek | sunum | Veri kaynağı değişince (asset → sqflite) yalnızca bu katman değişir. |
| sunum | alan, cekirdek | **veri** | Ekran somut depoyu bilmez, arayüzü bilir; testte sahte depo verilebilir. |
| özellikler arası | — | `ozellikler/a` → `ozellikler/b` | Özellikler bağımsız kalır; ortak ihtiyaç `cekirdek`'e taşınır (önce kullanıcıya sor). |

Kod kuralları (tasarım metrikleriyle bağlantılı):
- Renk, ölçü, yazı stili yalnızca `Tasarim*` sabitlerinden gelir (T1, T2).
- `tasarim.g.dart` ve `test/yerlesim`, `test/goruntu` elle düzenlenmez; tasarım değişirse `tasarim.json` güncellenir ve `uret` çalıştırılır (T3).
- `ekranlar.json`'daki her bileşen kodda aynı `ValueKey('<ekran>.<bilesen>')` ile işaretlenir (T4).

## 3. mimari.json (ölçülebilir hali)

```json
{
  "kaynak": "öneri-onaylandı:S20",
  "paket": "birimcevirici",
  "ozellik_koku": "lib/ozellikler",
  "ozellikler_arasi_import": false,
  "katmanlar": [
    {"ad": "giris",    "yollar": ["lib/main.dart", "lib/uygulama.dart"], "izinli": ["*"]},
    {"ad": "cekirdek", "yollar": ["lib/cekirdek/*"], "izinli": []},
    {"ad": "alan",     "yollar": ["lib/ozellikler/*/alan/*"], "izinli": ["cekirdek"],
     "yasak_paketler": ["package:flutter/", "dart:io", "dart:ui", "package:sqflite"]},
    {"ad": "veri",     "yollar": ["lib/ozellikler/*/veri/*"], "izinli": ["alan", "cekirdek"]},
    {"ad": "sunum",    "yollar": ["lib/ozellikler/*/sunum/*"], "izinli": ["alan", "cekirdek"]}
  ],
  "sinirlar": {"dosya_satir_max": 200, "fonksiyon_satir_max": 40},
  "python": {"yollar": ["tools/*.py"]}
}
```

`sinirlar` değerleri kullanıcıya sorulur (soru bankası 11.x). Örnekteki 200/40 yalnızca öneri olarak sunulur.

## 4. Kurulum adımları (sırayla)

Her adımın sonunda belirtilen komut temiz geçmeden sonraki adıma geçme. Böylece hata, oluştuğu adımda yakalanır.

1. **İskelet.** `flutter create --platforms android --org <org> --project-name <paket> -e .` → `lib/main.dart`'ı sil. Şablonun eklediği `cupertino_icons` karar kaydında yoksa `pubspec.yaml`'dan çıkar (D1).
2. **Spesifikasyon dosyaları.** `tasarim.json`, `ekranlar.json`, `mimari.json`, `kabul_kriterleri.json`, `kararlar.json` proje kökünde, onaylı.
   `python scripts/tasarim.py dogrula --proje .` · `python scripts/mimari.py dogrula --proje .` · `python scripts/kriterler.py dogrula kabul_kriterleri.json`
3. **Fontlar.** Kullanıcının verdiği font dosyalarını `assets/fonts/`'a koy, `pubspec.yaml` → `flutter: fonts:` altına `tasarim.json`'daki aile/ağırlıklarla ekle.
4. **Üret.** `python scripts/tasarim.py uret --proje .` → `tasarim.g.dart`, font yükleyici, yerleşim ve görüntü testleri.
5. **Çekirdek.** `lib/cekirdek/tema/tema.dart`: `ThemeData`'yı yalnızca `Tasarim*` sabitleriyle kur (örnek: `assets/ornek-proje/lib/cekirdek/tema/tema.dart`).
6. **Alan.** Modeller, depo arayüzleri, iş kuralları — saf Dart. Her kural için adında F/K ID'si olan birim testi (`test('F1 cevir: 5 km → 5000 m', …)`).
   `python scripts/mimari.py denetle --proje .` → Y1 = 0.
7. **Veri.** Depo arayüzünün uygulaması. Asset okurken `rootBundle.loadString(yol, cache: false)` — önbellekli Future bir sonraki widget testinde tamamlanmaz.
8. **Sunum.** Ekranları `ekranlar.json`'daki sırayla kur; her bileşene `ValueKey('<ekran>.<bilesen>')`. Ölçü/renk/yazı yalnızca `Tasarim*`. `build` uzarsa (Y4) parçaları özel metotlara/widget'lara böl.
   `flutter test test/yerlesim` → T4 = 0. Kalan her kontrol için ölçülen değeri tasarım değeriyle karşılaştır: fark bir tasarım sabitiyle kapanmıyorsa (ör. 32 dp boşluk var ama `bosluk` grubunda yok) **kullanıcıya sor**, sayı uydurma.
9. **Giriş.** `uygulama.dart`: `MaterialApp(theme: uygulamaTemasi(), home: …)`, somut depoyu burada ver; `main.dart` yalnızca `runApp`.
10. **Python.** `tools/<script>.py` + `tools/test_<script>.py` (test adlarında ID: `test_f4_…`). `ruff check tools` = 0.
11. **Ekran görüntüleri.** `flutter test --update-goldens --dart-define=GORUNTU_KLASORU=olcum test/goruntu` → `test/goruntu/olcum/<ekran>.png`. Bu görüntüleri ve `build/tasarim_fark/` fark görüntülerini kullanıcıya göster. Kullanıcı onaylarsa `flutter test --update-goldens test/goruntu` → `goldens/` (T6 artık regresyonu korur). Onaysız golden üretme.
12. **Ölçüm ve rapor.** SKILL.md Aşama 4–5.

## 5. Python tarafı

- `tools/` altında, her script tek sorumluluk: girdi dosyası → çıktı dosyası; `main(argv) -> int` çıkış kodu döndürür (test edilebilir).
- Fonksiyon/dosya uzunluk sınırı Dart ile aynı `sinirlar` değerleridir (Y3, Y4; `ast` ile kesin ölçülür).
- Script'in ürettiği dosya (ör. `assets/birimler.json`) uygulamanın tek veri kaynağıdır; elle düzenlenmez.

## 6. Ölçüm: Y1–Y4

`python scripts/mimari.py denetle --proje .` (olc.py bunu kendiliğinden çağırır):

| ID | olc_anahtari | Ne sayar |
|---|---|---|
| Y1 | mimari_yasak_bagimlilik | İzinsiz katman importu + özellikler arası import + katmanın yasak paketi |
| Y2 | mimari_katmansiz_dosya | Hiçbir katman yoluna uymayan `lib/` dosyası |
| Y3 | mimari_uzun_dosya | `dosya_satir_max`'ı aşan Dart/Python dosyası |
| Y4 | mimari_uzun_fonksiyon | `fonksiyon_satir_max`'ı aşan fonksiyon/metot (Dart: gövdeli ve `=>` fonksiyonlar, closure'lar dahil; Python: `ast`) |

Sınır: Dart fonksiyon uzunluğu ayrıştırıcı değil sezgisel tarayıcıyla ölçülür (string/yorum temizlenip parantez eşlenir). Olağan dışı sözdiziminde yanlış sayabilir; şüpheli bir bulguyu kullanıcıya kanıt satırıyla göster.
