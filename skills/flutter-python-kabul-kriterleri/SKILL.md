---
name: flutter-python-kabul-kriterleri
description: İnternetsiz (offline) çalışan Flutter Android uygulamaları ve onlara eşlik eden Python script/otomasyon/ML işleri için varsayım yapmadan, ölçülebilir kabul kriterleriyle çalışma yöntemi. Önce eksik bilgileri soru olarak sorar, sonra her isteği sayısal eşikli metriklere (ms, MB, %, adet, dp, API seviyesi) çevirir, kullanıcı onaylamadan kod yazmaz ve iş bitti demeden önce her metriği komutla ölçüp GEÇTİ/KALDI raporu verir. Kullanıcı Flutter, Dart, Android, APK/AAB, offline/internetsiz uygulama, TFLite/ML modeli, Python ile veri hazırlama veya build scripti, yeni ekran/özellik ekleme, "uygulama yap", "app geliştir", kabul kriteri, metrik, test kriteri dediğinde mutlaka bu skill'i kullan — kullanıcı "kabul kriteri" kelimesini söylemese bile, Flutter/Android işi istendiği anda kullan.
---

# Flutter + Python (Offline Android) — Ölçülebilir Kabul Kriterleri

## Bu skill neden var

Kullanıcının yaşadığı sorun şu: Claude belirsiz bir istek alınca boşlukları kendi tahminleriyle dolduruyor (state management seçiyor, minSdk uyduruyor, "hızlı" diyip ölçmüyor) ve sonuç kullanıcının istediği şey olmuyor. Bu skill bunu iki kuralla engeller:

1. **Varsayım yapma, sor.** Bilinmeyen her karar kullanıcıya soru olarak gider. Sessizce seçilmiş bir varsayılan, yanlış tahminle aynı zararı verir.
2. **Her şey ölçülebilir metriğe iner.** "Hızlı", "akıcı", "kullanıcı dostu", "iyi çalışsın" kabul kriteri değildir. Kriter = metrik + operatör + sayı + birim + ölçüm komutu. Ölçülemeyen bir şeye "bitti" denemez.

Bu yüzden süreç dört aşamalıdır ve aşamalar atlanmaz. Kullanıcı açıkça "onaylıyorum" demeden 3. aşamaya geçilmez.

```
1. SORU TURU  →  2. KABUL KRİTERLERİ (onay)  →  3. UYGULAMA  →  4. ÖLÇÜM RAPORU
```

## Aşama 1 — Soru turu

`references/soru-bankasi.md` dosyasını oku. Oradaki zorunlu soruların hangilerinin kullanıcının mesajında **açıkça** cevaplandığını işaretle; cevaplanmamış olanları sor.

"Açıkça cevaplanmış" ne demek: kullanıcı değeri kendisi yazmış olmalı. "Not uygulaması" demesi, verinin SQLite'ta tutulacağı anlamına gelmez; "eski telefonlarda da çalışsın" demesi minSdk = 21 anlamına gelmez. Bunlar çıkarımdır ve çıkarımlar sorulur.

Soruları sorarken:
- Kategoriye göre grupla ve numarala (S1, S2, …) ki kullanıcı "S3: 24" diye kısa cevap verebilsin.
- Mümkün olan her soruda seçenek sun (ör. `a) Riverpod b) Bloc c) Provider d) setState`). Seçenek sunmak, varsayım yapmadan kullanıcının işini kolaylaştırır.
- Bir öneri yapmak istersen yap ama **"(öneri)"** diye işaretle ve yine de cevabını bekle. Öneri ≠ karar.
- Her soruya, cevabın hangi metriğe dönüşeceğini kısaca yaz (ör. "→ P1 soğuk açılış eşiği"). Kullanıcı sorunun neden sorulduğunu görür.
- Tek seferde en fazla ~15 soru sor; daha fazlası varsa en kritik olanları (mimari ve kapsamı belirleyenleri) önce sor, kalanları ikinci tura bırak.

Bu aşamada **kod, dosya iskeleti veya `flutter create` çalıştırma**. Kod yazmak, cevabı bilinmeyen sorulara örtük cevap vermek demektir.

Kullanıcı "sen seç" / "fark etmez" derse: somut bir değer öner, gerekçesini bir cümleyle yaz ve o değeri de onaya sun. Kriter tablosunda `kaynak` alanına `"öneri-onaylandı"` yazılır; böylece hangi değerin kimden geldiği izlenebilir kalır.

## Aşama 2 — Kabul kriterleri

Cevaplar toplanınca proje köküne `kabul_kriterleri.json` yaz. Şablon: `assets/kabul_kriterleri.ornek.json`. Metrik tanımları ve ölçüm komutları: `references/metrik-katalogu.md` (gerekli olan kategorinin bölümünü oku).

Her kriterin alanları:

| Alan | Açıklama | Örnek |
|---|---|---|
| `id` | Kategori harfi + sıra | `P1`, `K3`, `O2` |
| `kategori` | performans / kod_kalitesi / android / offline / ui_erisilebilirlik / ml_veri / fonksiyonel | `performans` |
| `metrik` | Ne ölçülüyor, tek cümle | `Soğuk açılış süresi (5 ölçümün medyanı)` |
| `operator` | `<=`, `>=`, `==`, `<`, `>` | `<=` |
| `esik` | Sayı (metin değil) | `1500` |
| `birim` | ms, MB, %, adet, dp, fps, sn, api_seviyesi, oran | `ms` |
| `olcum_yontemi` | Çalıştırılabilir komut veya adım adım test prosedürü | `adb shell am start -W -n <paket>/.MainActivity → TotalTime` |
| `olcum_ortami` | Cihaz/emülatör, build modu | `Pixel 4a emülatör, API 30, --release` |
| `kaynak` | Değer nereden geldi | `kullanici:S7` veya `öneri-onaylandı:S12` |

Fonksiyonel gereksinimler de metriğe iner: "not silinebilsin" → `F3: not silme senaryosu integration testi geçen adım sayısı == 4/4` gibi; ya da `== 1` (test geçti = 1). Bir özellik için test yazılamıyorsa, kullanıcıya nasıl doğrulanacağını sor.

Dosyayı yazdıktan sonra doğrula:

```bash
python <skill-yolu>/scripts/kriterler.py dogrula kabul_kriterleri.json
```

Script şunları reddeder: eksik alan, sayısal olmayan eşik, bilinmeyen birim veya operatör, ölçüm yöntemi olmayan kriter, kriter metninde ölçüsüz belirsiz kelimeler ("hızlı", "akıcı", "iyi", "uygun", "makul", "kullanıcı dostu", "modern", "düzgün" …). Hata varsa düzelt ve tekrar çalıştır; geçmeden kullanıcıya sunma.

Sonra kullanıcıya tabloyu göster:

```bash
python <skill-yolu>/scripts/kriterler.py tablo kabul_kriterleri.json
```

Tablonun altına şunu yaz ve cevabı bekle:

> Bu kriterleri onaylıyor musun? "Onaylıyorum" yazarsan uygulamaya geçerim. Değiştirmek istediğin satırı ID ile belirt (ör. "P1 eşiği 2000 olsun").

## Aşama 3 — Uygulama

Yalnızca onaylanmış kriterleri karşılayacak kodu yaz. Uygulama sırasında yeni bir karar noktası çıkarsa (ör. boş liste ekranında ne gösterilecek, iki kayıt aynı isimdeyse ne olacak) dur ve sor; cevabı yeni bir kriter olarak dosyaya ekle. Bu, "kendi kafana göre yapma" kuralının uygulama aşamasındaki karşılığıdır.

Kapsam dışı iş yapma: kriterlerde olmayan bir özellik, paket veya ekran eklemek istiyorsan önce öner, onay al.

Offline uygulamalarda dikkat: Flutter `debug`/`profile` manifestlerine `INTERNET` izni otomatik ekler; `release` manifestinde olmamalı ve hiçbir paket ağ çağrısı yapmamalı (analitik, crash reporting, font indirme — ör. `google_fonts` çalışma anında indirir, font dosyaları asset olarak paketlenmeli). Kullanılacak her paketin offline çalıştığını kontrol et; emin değilsen kullanıcıya söyle.

Python tarafında: script'in nerede çalıştığı (geliştirici makinesinde build öncesi mi, cihazda mı) Aşama 1'de sorulmuş olmalı. Cihazda Python (Chaquopy, serious_python) APK boyutunu ciddi büyütür; bu kararın etkisi P4 (APK boyutu) kriterine yansır.

## Aşama 4 — Ölçüm raporu

"Bitti" demeden önce her kriteri ölç. Otomatik ölçülebilenler için:

```bash
python <skill-yolu>/scripts/olc.py --proje . --cikti olcumler.json
```

Bu script `flutter analyze`, `dart format`, `flutter test --coverage`, APK boyutu, manifest izinleri, minSdk/targetSdk, `ruff`, `pytest --cov` gibi ölçümleri yapar. Bir araç yoksa veya komut başarısız olursa değeri `null` ve sebebini yazar — **asla tahmini değer yazmaz**.

Otomatik ölçülemeyenleri (cihazda soğuk açılış, bellek, jank, model doğruluğu) `metrik-katalogu.md`'deki komutlarla ölç ve sonucu `olcumler.json`'a `{"deger": ..., "kanit": "<komut çıktısından ilgili satır>"}` olarak ekle. Ölçemiyorsan (ör. cihaz yok) değeri `null` bırak ve sebebini yaz.

Sonra raporu üret:

```bash
python <skill-yolu>/scripts/kriterler.py rapor kabul_kriterleri.json olcumler.json
```

Rapordaki her satır `GEÇTİ`, `KALDI` veya `ÖLÇÜLEMEDİ` olur. Kullanıcıya bu tabloyu olduğu gibi göster:

- Tüm satırlar `GEÇTİ` ise iş bitti diyebilirsin.
- `KALDI` varsa düzelt ve yeniden ölç; düzeltemiyorsan nedenini ve seçenekleri yaz, eşiği kendi başına değiştirme.
- `ÖLÇÜLEMEDİ` varsa iş bitmedi demektir; neyin eksik olduğunu (cihaz, araç, veri seti) ve kullanıcının nasıl ölçebileceğini yaz.

Bir kriterin eşiğini değiştirmek yalnızca kullanıcının kararıdır. Kriter değişirse dosyadaki `surum` alanını artır.

## Kısa örnek

**Kullanıcı:** "İnternetsiz çalışan bir yapılacaklar listesi uygulaması yap."

**Yanlış (varsayım):** Hemen `flutter create todo` çalıştırıp Provider + Hive ile 3 ekran yazmak.

**Doğru:** Soru turu —
> **Kapsam**
> S1. Hangi ekranlar olacak? (ör. liste, ekleme/düzenleme, ayarlar) → F kriterleri
> S2. Bir görevde hangi alanlar var? (başlık, açıklama, tarih, öncelik, kategori…) → F kriterleri
> **Android**
> S3. minSdk kaç? a) 21 (Android 5) b) 24 (Android 7) c) 26 (Android 8) → A1
> S4. En düşük hedef cihaz RAM'i? a) 2 GB b) 3 GB c) 4 GB → P1, P3 ölçüm ortamı
> **Veri**
> S5. Yerel veritabanı: a) sqflite b) drift c) hive d) isar e) sen öner → mimari
> S6. Beklenen en fazla kayıt sayısı? → P5 liste kaydırma eşiği
> **Performans**
> S7. Soğuk açılış en fazla kaç ms olsun? (öneri: orta seviye cihazda ≤ 2000 ms) → P1
> …

## Referans dosyaları

- `references/soru-bankasi.md` — Kategori bazında zorunlu sorular ve her sorunun hangi metriğe dönüştüğü. Aşama 1'de oku.
- `references/metrik-katalogu.md` — Her metrik için birim, ölçüm komutu, ölçüm ortamı, önerilen başlangıç eşiği. Aşama 2 ve 4'te ilgili bölümü oku.
- `assets/kabul_kriterleri.ornek.json` — Doldurulmuş örnek kriter dosyası.
- `scripts/kriterler.py` — `dogrula`, `tablo`, `rapor` alt komutları. Sadece Python standart kütüphanesi.
- `scripts/olc.py` — Otomatik ölçülebilen metrikleri toplar, `olcumler.json` yazar.
