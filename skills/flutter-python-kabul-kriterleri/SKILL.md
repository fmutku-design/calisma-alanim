---
name: flutter-python-kabul-kriterleri
description: İnternetsiz (offline) çalışan Flutter Android uygulamaları ve onlara eşlik eden Python script/otomasyon/ML işleri için varsayımsız, ölçülebilir ve dürüst çalışma yöntemi. Hem uygulamayı hem Claude'un kendi davranışını sayısal metriklerle ölçer — varsayım sayısı, onaysız kod, testsiz özellik ve kanıtsız "bitti/çalışıyor" iddiası script ile sayılır ve 0 olmak zorundadır. Önce eksik bilgileri sorar, cevapları eşikli kabul kriterlerine ve kaynağı kayıtlı kararlara çevirir, onay alınca işi sonuna kadar yapar, her kriteri komutla ölçer ve script'in ürettiği GEÇTİ/KALDI/ÖLÇÜLEMEDİ raporuyla teslim eder. Kullanıcı Flutter, Dart, Android, APK/AAB, offline/internetsiz uygulama, TFLite/ML modeli, Python ile veri hazırlama veya build scripti, yeni ekran/özellik ekleme, "uygulama yap", "app geliştir", kabul kriteri, metrik veya test kriteri dediğinde mutlaka bu skill'i kullan — "kabul kriteri" kelimesi geçmese bile, Flutter/Android işi istendiği anda kullan.
---

# Flutter + Python (Offline Android) — Ölçülebilir ve Dürüst Çalışma

## Bu skill neden var

Kullanıcının sorunu: Claude belirsiz bir istek alınca boşlukları kendi tahminiyle dolduruyor ("kafasına göre iş yapıyor") ve test etmediği şeye "çalışıyor" diyor. Kural koymak bunu çözmedi, çünkü kurala uyulup uyulmadığını kullanıcı göremiyor. Bu yüzden bu skill'de **Claude'un davranışı da bir metriktir** ve script ile sayılır:

| ID | Metrik | Hedef | Nasıl sayılır |
|---|---|---|---|
| D1 | Kaynaksız karar (varsayım) sayısı | == 0 | `denetim.py kontrol`: `pubspec.yaml` ve Python bağımlılıklarındaki her paket, `kararlar.json`'daki her karar ve her kriter `kullanici:` veya `öneri-onaylandı:` kaynağına bağlı olmalı. Bağlı olmayan her biri = 1 varsayım. |
| D2 | Onaysız yazılmış kod dosyası sayısı | == 0 | `denetim.py kontrol`: `kabul_kriterleri.json` onaylanmamışken (veya onay kanıtı yokken) var olan her `.dart`/`.py`/`.kt` dosyası. |
| D3 | Test dosyası olmayan fonksiyonel kriter | == 0 | `denetim.py kontrol`: her F kriterinin ölçüm yöntemindeki test dosyası diskte var mı. |
| D4 | Kanıtsız iddia sayısı | == 0 | `denetim.py mesaj`: tüm kriterler GEÇMEDEN kullanıcıya giden mesajdaki "bitti, hazır, çalışıyor, test edildi, başarıyla…" sayısı + mesajda güncel ölçüm özeti yoksa 1. |

D1–D3 her ölçüm raporunda otomatik yer alır ve çıkarılamaz. D4 mesaj gönderilmeden önceki son kapıdır. Bunlar kullanıcının "kafana göre yapma, yalan söyleme" isteğinin ölçülebilir hâlidir.

## Akış

```
1. SORU TURU → 2. KRİTER + KARAR KAYDI → (kullanıcı "onaylıyorum") → 3. UYGULAMA → 4. ÖLÇÜM → 5. TESLİM
                                                                         ↑______ KALDI varsa düzelt ___|
```

Aşama atlanmaz. Kullanıcı onay vermeden 3. aşamaya geçilmez (D2).

## Aşama 1 — Soru turu

`references/soru-bankasi.md`'yi oku. Kullanıcının mesajında **açıkça yazılmış** olanları işaretle, kalanları sor. Kullanıcı bir değeri kendisi yazmadıysa o değer bilinmiyordur; "not uygulaması" demek SQLite demek değildir, "eski telefonlar" minSdk 21 demek değildir. Çıkarım = varsayım = D1.

- Soruları kategoriye göre grupla, numarala (S1, S2…) ki kullanıcı "S3: b" diye cevaplayabilsin.
- Her soruya seçenek ve cevabın dönüşeceği metriği yaz (ör. "→ P1 soğuk açılış").
- Öneri yapabilirsin ama "(öneri)" diye işaretle. Öneri, kullanıcı kabul edene kadar karar değildir.
- Bir turda en fazla ~15 soru; mimariyi belirleyenler önce.
- Kullanıcının verdiği bilgileri bir tabloda geri yansıt ("bunları tekrar sormuyorum") ki yanlış anlama varsa hemen görülsün.
- Bu aşamada kod, iskelet, `flutter create` yok.

Kullanıcı "sen seç" derse somut değer öner ve onu da onaya sun; kabul ederse kaynak `öneri-onaylandı:Sx` olur.

## Aşama 2 — Kabul kriterleri ve karar kaydı

Cevaplardan proje köküne iki dosya yaz:

**`kabul_kriterleri.json`** — ölçülecek hedefler. Şablon: `assets/kabul_kriterleri.ornek.json`. Metrikler ve ölçüm komutları: `references/metrik-katalogu.md`. Her kriter: `id, kategori, metrik, operator, esik (sayı), birim, olcum_yontemi (komut), olcum_ortami, kaynak`. Fonksiyonel her gereksinim, test dosyası yolu yazılmış bir F kriteridir (`integration_test/not_sil_test.dart: ekle → sola kaydır → onayla → listede yok`).

**`kararlar.json`** — ölçülmeyen ama verilmesi gereken her karar: paketler, mimari, davranış (boş liste ne gösterir, silme onay sorar mı…). Şablon: `assets/kararlar.ornek.json`. Her karar `kaynak` taşır; paket gerektiren kararlar `paketler` listesi taşır. `flutter create` şablonunun getirdiği paketler (`cupertino_icons`, `flutter_lints`) de birer karardır — kullanıcıya sor.

Henüz cevaplanmamış önerilerin kaynağı `öneri-bekliyor:Sx` olur; dosya bu durumdayken onaylanamaz.

Doğrula ve göster:

```bash
python <skill>/scripts/kriterler.py dogrula kabul_kriterleri.json
python <skill>/scripts/kriterler.py tablo   kabul_kriterleri.json
```

`dogrula` ölçüsüz kelimeleri ("hızlı", "akıcı", "kullanıcı dostu"…), sayı olmayan eşikleri, ölçüm yöntemi olmayan ve kaynağı geçersiz kriterleri reddeder. Geçmeden kullanıcıya sunma.

Tabloyu ve karar listesini göster, şunu sor ve bekle:

> Bu kriterleri ve kararları onaylıyor musun? "Onaylıyorum" yazarsan uygulamaya geçerim. Değiştirmek istediğin satırı ID ile yaz.

Onay gelince `onay.durum = "onaylandi"`, `onay.tarih`, `onay.kanit = <kullanıcının cümlesi aynen>` yaz. Kanıtsız onay geçersizdir (D2 sayar).

## Aşama 3 — Uygulama (işi sonuna kadar yap)

Onaydan sonra kriterlerdeki **her şeyi** yap: kod, testler (her F kriteri için test dosyası — D3), Python script'leri, gerekli konfigürasyon. Yarım bırakıp "gerisini sen yaparsın" deme; yapamadığın bir parça varsa nedenini Aşama 5'te açıkça yaz.

- Kriterlerde ve `kararlar.json`'da olmayan bir paket, dosya türü veya davranış gerekirse **dur ve sor**. Cevabı `kararlar.json`'a ekle, sonra devam et. Sessizce eklenen paket D1'de yakalanır.
- Kapsam dışı "iyileştirme" ekleme; önce öner.
- Offline: release manifestinde `INTERNET` olmamalı; Flutter bunu debug/profile manifestlerine kendisi ekler. Ağ kullanan paket (`google_fonts` çalışma anında indirir, analitik, crash raporlama) kullanma; fontlar asset olarak paketlenir.
- Python cihazda mı (Chaquopy, serious_python — APK'ya onlarca MB ekler) yoksa geliştirici makinesinde mi çalışıyor, Aşama 1'de sorulmuş olmalı.

## Aşama 4 — Ölçüm

```bash
python <skill>/scripts/olc.py --proje . --cikti olcumler.json [--python-klasoru tools] [--model assets/x.tflite] [--build-apk]
python <skill>/scripts/denetim.py kontrol --proje .
```

`olc.py` araçla ölçülebilenleri (analyze, format, testler, kapsam, APK boyutu, izinler, minSdk, ağ kodu, ruff, pytest) ölçer ve her F kriterinin test dosyasını kendisi çalıştırır (geçti = 1, kaldı = 0). F sonuçlarını elle yazma; script'in sonucu geçerlidir. Araç yoksa değeri `null` yapar ve sebebini yazar; **tahmini değer yazmaz**. Cihaz gerektirenleri (soğuk açılış, bellek, jank, çıkarım süresi) katalogdaki komutlarla ölç ve `olcumler.json`'a `{"deger": x, "kanit": "<komut çıktısından satır>"}` ekle. Ölçemiyorsan `{"deger": null, "sebep": "..."}` yaz — `null` dürüsttür, uydurma değer yalandır.

```bash
python <skill>/scripts/kriterler.py rapor kabul_kriterleri.json olcumler.json > rapor.md
```

`KALDI` varsa düzelt ve yeniden ölç. Döngü, her satır `GEÇTİ` olana veya kalan satırlar kullanıcının cihazı/verisi olmadan ölçülemeyecek (`ÖLÇÜLEMEDİ`) hâle gelene kadar sürer. Eşiği kendi başına değiştirmek yasak; eşik değişikliği kullanıcı kararıdır ve `surum` artar.

## Aşama 5 — Teslim

Teslim mesajını `yanit.md` olarak yaz, **şu yapıyla**:

```markdown
## Teslim raporu
**DURUM:** <rapor.md'nin son satırı, aynen>

### Ölçüm tablosu
<rapor.md içeriği, aynen — elle düzenleme yok>

### Yapılanlar
<oluşturulan/değiştirilen dosyalar, her biri hangi kriter için>

### Ölçülemeyenler
<her ÖLÇÜLEMEDİ satırı için: neden ölçülemedi + kullanıcının çalıştıracağı komut>

### Açık sorular / sapmalar
<varsa; yoksa "Yok">
```

Sonra mesajı denetle:

```bash
python <skill>/scripts/denetim.py mesaj yanit.md --kriterler kabul_kriterleri.json --olcumler olcumler.json
```

D4 > 0 ise mesaj gönderilmez: iddia cümlelerini olgu cümleleriyle değiştir ("çalışıyor" → "K4: 12 testin 12'si geçti"), özet satırını ekle, tekrar denetle. Tüm kriterler GEÇTİ ise "bitti" demek serbesttir — çünkü artık kanıtı vardır.

## Kısa örnek

**Kullanıcı:** "İnternetsiz çalışan bir yapılacaklar listesi uygulaması yap."

**Yanlış:** `flutter create` + Provider + Hive ile 3 ekran yazıp "Uygulama hazır, çalışıyor" demek. Sonuç: D1 = 3 (Provider, Hive, ekran sayısı tahmin), D2 = 12 dosya, D4 = 2 iddia.

**Doğru:** S1–S15 soruları → cevaplar → `kabul_kriterleri.json` + `kararlar.json` → onay → kod + testler → ölçüm → `DURUM: TAMAM DEĞİL — 2 ÖLÇÜLEMEDİ (P1, P3: fiziksel cihaz gerekiyor; komutlar aşağıda)`.

## Dosyalar

- `references/soru-bankasi.md` — Zorunlu sorular ve hangi metriğe dönüştükleri. Aşama 1.
- `references/metrik-katalogu.md` — Her metriğin birimi, ölçüm komutu, önerilen başlangıç eşiği, sık yapılan teknik hatalar. Aşama 2 ve 4.
- `assets/kabul_kriterleri.ornek.json`, `assets/kararlar.ornek.json` — Şablonlar.
- `scripts/kriterler.py` — `dogrula`, `tablo`, `rapor` (D1–D3 dahil).
- `scripts/olc.py` — Otomatik ölçümler → `olcumler.json`.
- `scripts/denetim.py` — `kontrol` (D1–D3), `mesaj` (D4).
