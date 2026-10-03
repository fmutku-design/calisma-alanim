# Soru Bankası

Aşama 1'de kullanılır. Her soru için: neden sorulduğu ve cevabın hangi kritere dönüştüğü yazılı.
Kullanıcının mesajında **açıkça** cevabı olan soruları atla; çıkarım yapabildiğin ama kullanıcının yazmadığı her şeyi sor.

İşaretler: **[Z]** = zorunlu (cevapsız kod yazılmaz), **[D]** = duruma göre (ilgili özellik varsa sor).

## İçindekiler
1. Kapsam ve fonksiyonlar
2. Android ve cihaz
3. Offline ve veri
4. Mimari ve paketler
5. Performans
6. Kod kalitesi ve test
7. UI ve erişilebilirlik
8. Python: script / otomasyon
9. Python: ML / veri işleme
10. Teslim
11. Tasarım (kullanıcı verir — öneri yok)
12. Yazılım mimarisi

---

## 1. Kapsam ve fonksiyonlar

| # | Soru | İşaret | Neden / Hangi kriter |
|---|---|---|---|
| 1.1 | Uygulamadaki ekranların tam listesi nedir? | Z | Her ekran en az bir F kriteri alır. Ekran sayısı tahmin edilirse kapsam şişer veya eksik kalır. |
| 1.2 | Her ekranda kullanıcı hangi işlemleri yapabilmeli? (ekle, sil, düzenle, ara, filtrele, sırala, paylaş…) | Z | Her işlem bir F kriteri + integration testi olur. |
| 1.3 | Veri modelindeki alanlar ve tipleri nelerdir? Zorunlu olanlar hangileri? | Z | Doğrulama kuralları ve test verisi buradan çıkar. |
| 1.4 | Hata ve kenar durumlarda ne olmalı? (boş liste, çok uzun metin, aynı isimli kayıt, silme onayı) | Z | F kriterleri; sorulmazsa Claude kendi davranışını uydurur. |
| 1.5 | Kapsam dışı olan, kesinlikle istemediğin bir şey var mı? | D | Kapsam sınırı. |

## 2. Android ve cihaz

| # | Soru | İşaret | Neden / Hangi kriter |
|---|---|---|---|
| 2.1 | minSdk kaç? a) 21 (5.0) b) 23 (6.0) c) 24 (7.0) d) 26 (8.0) | Z | A1. Paket uyumluluğunu ve kullanılabilir API'leri belirler. |
| 2.2 | targetSdk kaç? (Play Store'a yüklenecekse güncel zorunlu seviye) | Z | A2. |
| 2.3 | En zayıf hedef cihaz: RAM (GB), Android sürümü, örnek model? | Z | Performans kriterlerinin ölçüm ortamı. "Eski cihazlar" ≠ ölçüm ortamı. |
| 2.4 | Ölçüm hangi cihaz/emülatörde yapılacak? Fiziksel cihaz var mı? | Z | Tüm P kriterlerinin `olcum_ortami` alanı. |
| 2.5 | Ekran yönü: a) sadece dikey b) dikey + yatay | Z | A3, U kriterleri. |
| 2.6 | Tablet desteği gerekli mi? Hangi genişlikler test edilecek? (ör. 360dp, 411dp, 600dp, 840dp) | Z | U5. |
| 2.7 | Hangi Android izinleri gerekli? (kamera, depolama, bildirim, konum…) Tam liste. | Z | A4 — izin listesi birebir eşleşmeli; fazlası KALDI. |

## 3. Offline ve veri

| # | Soru | İşaret | Neden / Hangi kriter |
|---|---|---|---|
| 3.1 | Uygulama hiç internete çıkmayacak mı, yoksa isteğe bağlı senkron var mı? | Z | O1 (INTERNET izni == 0) veya farklı kriter seti. |
| 3.2 | Veriler nerede saklanacak? a) sqflite b) drift c) hive d) isar e) shared_preferences f) dosya | Z | Mimari. Sorulmadan seçilmez. |
| 3.3 | Beklenen en fazla kayıt sayısı? (ör. 1.000 / 10.000 / 100.000) | Z | P5 liste performansı ve O3 depolama testi bu sayıyla yapılır. |
| 3.4 | Uygulamayla gelen hazır veri (asset/DB) var mı? Boyutu (MB)? | D | P4 APK boyutu bütçesi. |
| 3.5 | Yedekleme / dışa aktarma (export/import) gerekli mi? Format? (JSON, CSV) | D | F kriteri. |
| 3.6 | Uygulama kaldırılıp kurulunca veri kalmalı mı? (Android Auto Backup açık/kapalı) | D | A kriteri — `allowBackup` değeri. |

## 4. Mimari ve paketler

| # | Soru | İşaret | Neden / Hangi kriter |
|---|---|---|---|
| 4.1 | State management: a) Riverpod b) Bloc/Cubit c) Provider d) setState e) GetX f) sen öner | Z | Mimari. En sık yapılan varsayım budur — mutlaka sor. |
| 4.2 | Flutter sürümü / kanal? (ör. 3.24 stable) — `flutter --version` çıktısı | Z | Paket uyumluluğu. |
| 4.3 | Kullanılması yasak veya zorunlu paket var mı? | D | Kapsam. |
| 4.4 | Klasör yapısı tercihi: a) feature-first b) layer-first c) mevcut proje yapısı | D | Kod düzeni. Mevcut proje varsa ona uy ve bunu söyle. |
| 4.6 | `flutter create` şablonunun getirdiği paketler (`cupertino_icons`, `flutter_lints`) kalsın mı? | Z | Her paket bir karardır (D1). |
| 4.5 | Navigasyon: a) Navigator 2 / go_router b) Navigator.push c) auto_route | D | Mimari. |

## 5. Performans

Kullanıcı sayı veremezse `metrik-katalogu.md`'deki önerilen başlangıç eşiğini "(öneri)" olarak sun.

| # | Soru | İşaret | Kriter |
|---|---|---|---|
| 5.1 | Soğuk açılış en fazla kaç ms? | Z | P1 |
| 5.2 | Kabul edilebilir jank (atlanan kare) oranı en fazla yüzde kaç? | Z | P2 |
| 5.3 | Bellek kullanımı (PSS) en fazla kaç MB? | D | P3 |
| 5.4 | APK boyutu (arm64, release) en fazla kaç MB? | Z | P4 |
| 5.5 | En kalabalık listede kaydırma: 90. yüzdelik kare süresi en fazla kaç ms? | D | P5 |
| 5.6 | Kritik işlemlerin (kaydet, ara, model çıkarımı) süresi en fazla kaç ms? | D | P6 |

## 6. Kod kalitesi ve test

| # | Soru | İşaret | Kriter |
|---|---|---|---|
| 6.1 | Dart test kapsamı (line coverage) en az yüzde kaç? | Z | K3 |
| 6.2 | `flutter analyze` uyarı sayısı 0 mı olmalı? Hangi lint seti? (flutter_lints / very_good_analysis) | Z | K1 |
| 6.3 | Integration test (gerçek cihaz/emülatörde) gerekli mi? Hangi akışlar? | Z | F kriterlerinin ölçüm yöntemi. |
| 6.4 | Python kodu için: test kapsamı en az yüzde kaç? `ruff` uyarısı 0 mı? Tip kontrolü (mypy) gerekli mi? | D | K5, K6, K7 |

## 7. UI ve erişilebilirlik

| # | Soru | İşaret | Kriter |
|---|---|---|---|
| 7.1 | Desteklenen diller? (ör. tr, en) Varsayılan dil? | Z | U4 — eksik çeviri anahtarı == 0. |
| 7.2 | Tema: a) sadece açık b) açık + koyu c) sistemi takip et (koyu tema varsa onun tasarım değerleri de §11'den istenir) | Z | U kriteri. |
| 7.3 | Tasarım → §11. Tasarım kullanıcıdan gelmeden kod yazılmaz; Material 3 varsayılanı da bir tasarım değildir. | Z | T1–T6 |
| 7.4 | Erişilebilirlik: dokunma alanı ≥ 48dp, kontrast, ekran okuyucu etiketi kriterlerini dahil edelim mi? | Z | U1–U3 |
| 7.5 | En büyük yazı ölçeği (textScaleFactor) kaç olmalı ve taşma olmamalı? (ör. 1.3 / 2.0) | D | U6 |

## 8. Python: script / otomasyon

| # | Soru | İşaret | Neden / Kriter |
|---|---|---|---|
| 8.1 | Python script nerede çalışacak? a) geliştirici makinesinde, build öncesi b) CI'da c) telefonda (Chaquopy / serious_python) | Z | Mimari ve P4. Cihazda Python APK'ya onlarca MB ekler. |
| 8.2 | Script ne yapacak? Girdi dosyası/formatı ve çıktı dosyası/formatı tam olarak nedir? | Z | F kriteri: belirli girdi → beklenen çıktı (hash veya satır sayısı). |
| 8.3 | Python sürümü? (ör. 3.11) İzin verilen bağımlılıklar? | Z | Ortam. |
| 8.4 | Script en fazla kaç saniyede bitmeli, hangi veri boyutunda? | D | M3 |
| 8.5 | Hata durumunda davranış: dur ve çık kodu ≠ 0 mı, yoksa atla ve logla mı? | D | F kriteri. |

## 9. Python: ML / veri işleme

| # | Soru | İşaret | Neden / Kriter |
|---|---|---|---|
| 9.1 | Model ne yapıyor? Girdi (boyut, tip) ve çıktı (sınıf listesi, sayı)? | Z | Arayüz sözleşmesi. |
| 9.2 | Model formatı: a) TFLite b) ONNX c) başka — cihazda hangi paketle çalışacak? | Z | Mimari. |
| 9.3 | Ayrılmış test setinde hedef doğruluk / F1 en az yüzde kaç? Test seti nerede, kaç örnek? | Z | M1 — test seti yoksa M1 ölçülemez, bunu söyle. |
| 9.4 | Model dosyası en fazla kaç MB? Quantization (int8/float16) kabul mü? | Z | M2, P4 |
| 9.5 | Hedef cihazda tek çıkarım en fazla kaç ms? | Z | P6 |
| 9.6 | Tekrarlanabilirlik: sabit seed ve aynı girdiyle aynı çıktı şart mı? | D | M4 |

## 10. Teslim

| # | Soru | İşaret | Neden |
|---|---|---|---|
| 10.1 | Çıktı: a) APK b) AAB c) ikisi — split-per-abi? | Z | P4 ölçüm yöntemi. |
| 10.2 | Paket adı (applicationId)? Uygulama adı? | Z | Uydurulmaz. |
| 10.4 | Ölçüm cihazının CPU mimarisi? (`adb shell getprop ro.product.cpu.abilist`) | Z | 32-bit cihaza arm64 APK kurulmaz; P4 doğru ABI için yazılır. |
| 10.3 | İmzalama: debug imza yeterli mi, yoksa keystore var mı? | D | Release build. |

## 11. Tasarım (kullanıcı verir — öneri yok)

Ayrıntı ve kontrol listesi: `references/tasarim.md` §1. Bu sorularda Claude **değer önermez**; kullanıcı vermezse değer eksik kalır ve kod yazılmaz.

| # | Soru | İşaret | Kriter |
|---|---|---|---|
| 11.1 | Tasarım kaynağı nedir? (Figma dosyası/sayfası, ekran PNG'leri + değer listesi) | Z | Tüm T |
| 11.2 | Her ekranın PNG dışa aktarımı, aynı çerçeve boyutunda: kaç × kaç dp, hangi ölçekte (@1x/@2x)? | Z | T5, `ekran_boyutu` |
| 11.3 | Durum ekranları (boş liste, hata, yükleniyor, uzun metin) tasarımda var mı? Yoksa her biri için görsel iste. | Z | T4, T5 |
| 11.4 | Renkler: ad + hex listesi | Z | T1 |
| 11.5 | Font ailesi, font dosyaları (TTF/OTF), kullanılan ağırlıklar | Z | T4, T5 |
| 11.6 | Yazı stilleri: her biri için boyut (sp), ağırlık, satır yüksekliği, renk | Z | T2 |
| 11.7 | Boşluk ölçeği (dp listesi) ve köşe yarıçapları | Z | T2 |
| 11.8 | Bileşen ölçüleri: AppBar, buton, girdi, kart, liste satırı yükseklikleri | Z | T2, T4 |
| 11.9 | Her ekranda her bileşenin üst/sol konumu ve genişlik/yüksekliği (Figma Inspect) | Z | T4 |
| 11.10 | Yerleşim toleransı: ± kaç dp? | Z | T4 |
| 11.11 | Tasarım görseli ile ekran görüntüsü arasında kabul edilen en büyük piksel farkı (%)? | Z | T5 |

## 12. Yazılım mimarisi

Ayrıntı: `references/mimari.md`. Kullanıcının mimarisi yoksa örnek mimari "(öneri)" olarak gösterilir.

| # | Soru | İşaret | Kriter |
|---|---|---|---|
| 12.1 | Kendi mimarin / klasör yapın var mı? Yoksa örnek mimari (giris / cekirdek / ozellikler/<ad>/{alan, veri, sunum}) uygun mu? | Z | Y1, Y2 |
| 12.2 | Katman kuralları: sunum veriyi doğrudan import edemez, alan katmanı Flutter'a bağımlı olamaz, özellikler birbirini import edemez — onay? | Z | Y1 |
| 12.3 | Bir dosya en fazla kaç satır olsun? (öneri: 200) | Z | Y3 |
| 12.4 | Bir fonksiyon/metot en fazla kaç satır olsun? (öneri: 40) | Z | Y4 |
| 12.5 | Python script'leri hangi klasörde (`tools/`) ve aynı sınırlar mı geçerli? | D | Y3, Y4 |
