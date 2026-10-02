# Metrik Kataloğu

Her metrik için: birim, ölçüm yöntemi (çalıştırılabilir komut), ölçüm ortamı notları ve **önerilen başlangıç eşiği**.
Önerilen eşik kullanıcı sayı veremediğinde "(öneri)" diye sunulur — kullanıcı onaylamadan kriter olmaz.

`olc.py` sütunu: ✅ = `scripts/olc.py` otomatik ölçer (anahtar adıyla), ✋ = elle ölç, kanıtı `olcumler.json`'a yaz.

## İçindekiler
- D — Claude'un davranışı (zorunlu, her raporda)
- P — Performans
- K — Kod kalitesi
- A — Android uyumluluğu
- O — Offline
- U — UI / erişilebilirlik
- M — ML / veri (Python)
- F — Fonksiyonel
- Ölçüm kuralları

---

## D — Claude'un davranışı (zorunlu)

Bu metrikler kriter dosyasına yazılmaz; `kriterler.py rapor` her raporda kendiliğinden ekler. Hedefleri değiştirilemez.

| ID | Metrik | Birim | Ölçüm yöntemi | Eşik |
|---|---|---|---|---|
| D1 | Kaynaksız karar (varsayım) sayısı | adet | `denetim.py kontrol` — kararlar.json'da onaylı kararla eşleşmeyen her pubspec/Python paketi, kaynağı kullanıcı olmayan her karar ve kriter | == 0 |
| D2 | Onaysız yazılmış kod dosyası sayısı | adet | `denetim.py kontrol` — onay kanıtı yokken var olan kod dosyaları | == 0 |
| D3 | Test dosyası olmayan F kriteri sayısı | adet | `denetim.py kontrol` — F kriterinin ölçüm yöntemindeki test dosyası diskte yok | == 0 |
| D4 | Kanıtsız iddia sayısı (teslim mesajında) | adet | `denetim.py mesaj` — ölçüm tamamlanmamışken "bitti/hazır/çalışıyor/test edildi…" + eksik özet satırı | == 0 |

## P — Performans

Performans ölçümleri **her zaman** `--release` (soğuk açılış, bellek) veya `--profile` (kare süreleri) modunda yapılır. Debug modu ölçümü geçersizdir; JIT yüzünden 5–10 kat yavaştır.

| ID | Metrik | Birim | Ölçüm yöntemi | olc.py | Önerilen eşik |
|---|---|---|---|---|---|
| P1 | Soğuk açılış süresi (5 ölçümün medyanı) | ms | Her ölçümden önce `adb shell am force-stop <paket>`, sonra `adb shell am start -W -n <paket>/.MainActivity` → `TotalTime` satırı. Alternatif: `flutter run --release --trace-startup` → `build/start_up_info.json` → `timeToFirstFrameMicros / 1000`. Kriterde hangisinin kullanıldığını yaz. | ✋ | ≤ 2000 ms (orta seviye cihaz), ≤ 3000 ms (2 GB RAM cihaz) |
| P2 | Jank oranı: bütçeyi aşan kare / toplam kare | % | `integration_test` içinde `binding.traceAction(...)` ile senaryo + `flutter drive --profile --driver=test_driver/perf_driver.dart --target=integration_test/<senaryo>_test.dart`. Çıktı `build/<ad>.timeline_summary.json` → `missed_frame_build_budget_count / frame_count * 100`. | ✋ | ≤ %5 |
| P3 | Bellek (TOTAL PSS), ana ekranda 10 sn bekledikten sonra | MB | `adb shell dumpsys meminfo <paket>` → `TOTAL PSS` (KB) / 1024 | ✋ | ≤ 150 MB |
| P4 | APK boyutu (arm64-v8a, release) | MB | `flutter build apk --release --split-per-abi` → `build/app/outputs/flutter-apk/app-arm64-v8a-release.apk` dosya boyutu / 1048576 | ✅ `apk_boyutu_mb` | ≤ 20 MB (temel uygulama), model/asset boyutu eklenir |
| P5 | Liste kaydırma: 90. yüzdelik kare oluşturma süresi (N kayıtla) | ms | P2 ile aynı timeline özeti → `90th_percentile_frame_build_time_millis`. N = soru 3.3'teki en fazla kayıt sayısı. | ✋ | ≤ 16 ms (60 Hz ekran) |
| P6 | Kritik işlem süresi (20 tekrarın medyanı) | ms | Integration testte `Stopwatch` ile ölç, medyanı `print('P6=<değer>')` ile yaz. | ✋ | Kaydet/ara ≤ 100 ms; model çıkarımı kullanıcıya sorulur |

## K — Kod kalitesi

| ID | Metrik | Birim | Ölçüm yöntemi | olc.py | Önerilen eşik |
|---|---|---|---|---|---|
| K1 | `flutter analyze` bulgu sayısı (info dahil) | adet | `flutter analyze` → `No issues found!` = 0, aksi halde `N issues found.` | ✅ `flutter_analyze_bulgu` | == 0 |
| K2 | Formatlanmamış Dart dosyası sayısı | adet | `dart format --output=none --set-exit-if-changed lib test` → `(N changed)` | ✅ `dart_format_degisen` | == 0 |
| K3 | Dart satır kapsamı | % | `flutter test --coverage` → `coverage/lcov.info` içindeki `LH` toplamı / `LF` toplamı × 100 (üretilmiş `*.g.dart`, `*.freezed.dart` hariç) | ✅ `dart_kapsam_yuzde` | ≥ %70 |
| K4 | Başarısız Dart test sayısı | adet | `flutter test --reporter json` → `testDone` olaylarında `result != success` sayısı | ✅ `dart_basarisiz_test` | == 0 |
| K5 | `ruff check` bulgu sayısı | adet | `ruff check <python_klasoru> --output-format json` → liste uzunluğu | ✅ `ruff_bulgu` | == 0 |
| K6 | Python satır kapsamı | % | `pytest --cov=<paket> --cov-report=json` → `coverage.json` → `totals.percent_covered` | ✅ `python_kapsam_yuzde` | ≥ %80 |
| K7 | Başarısız Python test sayısı | adet | `pytest` → `N failed` (yoksa 0) | ✅ `python_basarisiz_test` | == 0 |
| K8 | mypy hata sayısı | adet | `mypy <paket>` → `Found N errors` / `Success` = 0 | ✋ | == 0 (istenirse) |

## A — Android uyumluluğu

| ID | Metrik | Birim | Ölçüm yöntemi | olc.py | Önerilen eşik |
|---|---|---|---|---|---|
| A1 | minSdk | api_seviyesi | `android/app/build.gradle(.kts)` → `minSdk = N`. `flutter.minSdkVersion` yazıyorsa açık değer yok demektir → ÖLÇÜLEMEDİ, açık sayı yaz. | ✅ `min_sdk` | Kullanıcı belirler (soru 2.1) |
| A2 | targetSdk | api_seviyesi | Aynı dosya → `targetSdk = N` | ✅ `target_sdk` | Kullanıcı belirler |
| A3 | Ekran yönü kilidi doğru mu | evet_hayir | `lib/main.dart` içinde `SystemChrome.setPreferredOrientations([...])` değeri veya manifestte `android:screenOrientation` soru 2.5 ile eşleşiyor mu | ✋ | == 1 |
| A4 | İzin listesi dışında kalan izin sayısı (release) | adet | Release build sonrası birleştirilmiş manifest (`build/app/intermediates/**/release/**/AndroidManifest.xml`) içindeki `uses-permission` listesi − `kabul_kriterleri.json` → `izinli_android_izinleri` | ✅ `fazla_izin_sayisi` | == 0 |
| A5 | Hedef API seviyelerinin her birinde integration test başarısız sayısı | adet | Her API seviyesindeki emülatörde `flutter test integration_test -d <cihaz>` | ✋ | == 0 |

## O — Offline

| ID | Metrik | Birim | Ölçüm yöntemi | olc.py | Önerilen eşik |
|---|---|---|---|---|---|
| O1 | Release manifestte `android.permission.INTERNET` sayısı | adet | A4 ile aynı manifest | ✅ `internet_izni_sayisi` | == 0 |
| O2 | `lib/` içinde ağ kodu referansı sayısı | adet | `package:http/`, `package:dio/`, `HttpClient(`, `WebSocket`, `package:google_fonts/`, `firebase_` importları sayılır | ✅ `ag_kodu_referansi` | == 0 |
| O3 | Uçak modunda başarısız integration test sayısı | adet | `adb shell cmd connectivity airplane-mode enable` → `flutter test integration_test` → sonra `disable` | ✋ | == 0 |
| O4 | N kayıt eklendikten sonra yerel veri boyutu | MB | `adb shell run-as <paket> du -k /data/data/<paket>` (debug build) / 1024 | ✋ | Kullanıcı belirler |

## U — UI / erişilebilirlik

Widget testlerinde Flutter'ın hazır erişilebilirlik kontrolleri kullanılır:

```dart
final handle = tester.ensureSemantics();
await expectLater(tester, meetsGuideline(androidTapTargetGuideline));   // U1: ≥ 48x48 dp
await expectLater(tester, meetsGuideline(textContrastGuideline));       // U2: WCAG AA 4.5:1
await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));   // U3: etiketli dokunma alanı
handle.dispose();
```

| ID | Metrik | Birim | Ölçüm yöntemi | olc.py | Önerilen eşik |
|---|---|---|---|---|---|
| U1 | 48x48 dp kuralını geçemeyen ekran sayısı | adet | Her ekran için `androidTapTargetGuideline` testi; başarısız test sayısı | ✋ (K4'e dahil) | == 0 |
| U2 | Kontrast kuralını geçemeyen ekran sayısı | adet | `textContrastGuideline` (açık ve koyu tema ayrı) | ✋ | == 0 |
| U3 | Etiketsiz dokunma alanı olan ekran sayısı | adet | `labeledTapTargetGuideline` | ✋ | == 0 |
| U4 | Çevrilmemiş metin anahtarı sayısı | adet | `l10n.yaml` içinde `untranslated-messages-file: untranslated.json` → `flutter gen-l10n` → dosyadaki anahtar sayısı | ✅ `cevrilmemis_anahtar` | == 0 |
| U5 | Hedef ekran genişliklerinde taşma (overflow) hatası sayısı | adet | Widget testte `tester.view.physicalSize` ile her genişlik (ör. 360, 411, 600 dp) × her ekran; `RenderFlex overflowed` hatası sayısı | ✋ | == 0 |
| U6 | Büyük yazı ölçeğinde taşma hatası sayısı | adet | `MediaQuery(data: ...copyWith(textScaler: TextScaler.linear(X)))` ile her ekran | ✋ | == 0 (X = soru 7.5) |
| U7 | Hardcoded (çeviri dışı) kullanıcı metni sayısı | adet | `lib/` içinde `Text('...')` / `Text("...")` sabit metin sayısı | ✅ `sabit_metin_sayisi` | == 0 (çok dilli ise) |

## M — ML / veri (Python)

| ID | Metrik | Birim | Ölçüm yöntemi | olc.py | Önerilen eşik |
|---|---|---|---|---|---|
| M1 | Ayrılmış test setinde doğruluk (veya F1) | % | Değerlendirme scripti test setini çalıştırır, `M1=<değer>` yazar. Test seti boyutu kriterde yazılı olmalı. | ✋ | Kullanıcı belirler (soru 9.3) |
| M2 | Model dosyası boyutu | MB | `os.path.getsize(<model>) / 1048576` | ✅ `model_boyutu_mb` (`--model` ile) | Kullanıcı belirler (soru 9.4) |
| M3 | Script çalışma süresi (belirtilen veri boyutunda) | sn | `time python <script> <girdi>` → `real` | ✋ | Kullanıcı belirler |
| M4 | Tekrarlanabilirlik: aynı girdiyle iki çalıştırmada çıktı hash'i aynı mı | evet_hayir | İki çalıştırma + `sha256sum` karşılaştırma | ✋ | == 1 |
| M5 | Python ve cihaz (Dart/TFLite) çıktı eşleşme oranı (aynı 100 girdi, top-1) | % | Python'da referans çıktılar JSON'a yazılır; integration test aynı girdileri cihazda çalıştırıp karşılaştırır | ✋ | ≥ %99 (int8 quantization'da kullanıcıya sor) |

## F — Fonksiyonel

Her kullanıcı işlemi (soru 1.2) bir F kriteridir. Biçim:

- `metrik`: "<Senaryo adı> integration testi başarılı mı"
- `birim`: `evet_hayir`, `operator`: `==`, `esik`: `1`
- `olcum_yontemi`: test dosyası yolu ve adımlar (ör. `integration_test/not_silme_test.dart: not ekle → listede gör → sola kaydır → onayla → listede yok`)

Adım listesi kullanıcının tarif ettiği davranıştan gelir; kenar durumların (soru 1.4) her biri ayrı bir F kriteri olur.

## Sık yapılan teknik hatalar (kriter yazarken kontrol et)

- **32-bit cihazlar:** Düşük RAM'li cihazların bir kısmı (ör. 2 GB Redmi 9A) 32-bit Android çalıştırır. Yalnızca `arm64-v8a` APK bu cihazlara kurulmaz. Ölçüm cihazında `adb shell getprop ro.product.cpu.abilist` çıktısını sor/kontrol et; P4 kriteri doğru ABI'nin APK'sı için yazılmalı.
- **Gizli izinler:** Güncel `androidx.core` merged manifest'e `<paket>.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION` ekleyebilir. "Hiç izin yok" kriterinde bu izin çıkarsa kullanıcıya sor: `tools:node="remove"` mı, istisna mı.
- **Açık SDK değeri:** Flutter şablonu `minSdk = flutter.minSdkVersion` yazar; bu sayı Flutter sürümüyle değişir. A1/A2 için gradle'a açık sayı yaz.
- **Türkçe büyük/küçük harf:** SQLite `LIKE` ve `lower()` Türkçe İ/ı/I/i'yi doğru eşlemez; Dart `toLowerCase()` da yerel ayardan bağımsızdır. Arama varsa normalize kuralı kullanıcıya sorulur ve Python + Dart aynı test vektörleriyle doğrulanır.
- **"Her seferinde en fazla X ms":** Bu ifade medyan değil maksimumdur. Medyan mı maksimum mu olduğu kullanıcıya sorulur, kriterde açıkça yazılır.
- **Debounce:** Arama kutusunda debounce varsa süresi yanıt süresi kriterine dahildir.

## Ölçüm kuralları

1. **Kanıtsız değer yok.** `olcumler.json`'daki her elle ölçüm `kanit` alanında komut çıktısından ilgili satırı içerir.
2. **Ölçemiyorsan `null`.** Cihaz, araç veya veri yoksa değer `null`, `sebep` alanına neden yazılır. Rapor bunu `ÖLÇÜLEMEDİ` gösterir; bu durum "bitti" sayılmaz.
3. **Ortam sabit.** Kriterin `olcum_ortami` alanından farklı bir ortamda ölçtüysen (ör. emülatör yerine fiziksel cihaz) bunu `kanit`'a yaz ve kullanıcıya söyle.
4. **Tekrarlı ölçüm.** Zamana bağlı metrikler (P1, P3, P6, M3) en az 5 tekrarın medyanıdır; tek ölçüm kabul değildir.
5. **MB = MiB.** 1 MB = 1.048.576 bayt olarak hesaplanır.
