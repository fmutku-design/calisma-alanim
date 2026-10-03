# Tasarım: Kullanıcının Tasarımını Ölçülebilir Hale Getirme

Kural: **Tasarımı kullanıcı verir. Claude tasarım değeri seçmez, önermez, görselden göz kararı çıkarmaz.** Tasarım gelmeden kod yazılmaz. Her tasarım değeri `tasarim.json`/`ekranlar.json`'da `kullanici:<nerede>` kaynağıyla durur; script başka kaynağı reddeder.

Çalışan tam örnek: `assets/ornek-proje/` (`tasarim.json`, `ekranlar.json`, `tasarim/cevirici.png`, üretilmiş testler, onaylı golden).

## İçindekiler
1. Kullanıcıdan istenecekler (kontrol listesi)
2. Tasarımı dosyalara dökme
3. Eksik değer — ne yapılır
4. Onay
5. Kod: tasarım değerlerini kullanma
6. Ölçüm: T1–T6
7. Sık hatalar

---

## 1. Kullanıcıdan istenecekler (kontrol listesi)

Kullanıcıya bu listeyi ver; eksik kalan her madde bir sorudur.

| # | İstenen | Nereye yazılır |
|---|---|---|
| 1 | Tasarım kaynağı: Figma dosyası/sayfası, ya da her ekranın PNG'si + değer listesi | `ekranlar[].kaynak`, `tasarim/<ekran>.png` |
| 2 | Her ekranın PNG dışa aktarımı — **aynı çerçeve boyutunda** (ör. 360×800 dp, @1x) | `tasarim/<ekran>.png`, `ekran_boyutu` |
| 3 | Durum ekranları ayrı ayrı: boş liste, hata, yükleniyor, uzun metin | Ayrı ekran girdileri (ör. `listeBos`) |
| 4 | Renkler (hex) ve adları | `renk` |
| 5 | Font ailesi, font dosyaları (TTF/OTF, offline gömülecek), kullanılan ağırlıklar | `font` |
| 6 | Yazı stilleri: boyut (sp), ağırlık, satır yüksekliği, harf aralığı, renk | `yazi` |
| 7 | Boşluk ölçeği (ör. 4/8/16/24/32 dp) | `bosluk` |
| 8 | Köşe yarıçapları | `kose` |
| 9 | Bileşen ölçüleri: AppBar, buton, girdi, kart yükseklikleri vb. | `bilesen` |
| 10 | Her ekranda her bileşenin üst/sol konumu ve genişlik/yüksekliği (Figma "Inspect" değerleri) | `ekranlar[].bilesenler` |
| 11 | Yerleşim toleransı (± kaç dp kabul) | `tolerans_dp` |
| 12 | Tasarım görseliyle ekran görüntüsü arasında kabul edilen en büyük piksel farkı (%) | T5 eşiği |
| 13 | Kullanılan her Material bileşeninin (girdi kenarlığı, açılır liste metni, buton, liste satırı, ayırıcı) renk ve yazı stili. Tasarımda yoksa: Material varsayılanının kullanılacağını kullanıcı açıkça onaylamalı → `kararlar.json` | `renk`/`yazi` veya karar |

## 2. Tasarımı dosyalara dökme

1. **`tasarim.json`** — şablon: `assets/ornek-proje/tasarim.json`. Adlar camelCase (Dart sabiti olur). Her değerin `kaynak`'ı nereden okunduğunu söyler: `kullanici:figma/Stiller/Renk/Birincil`, `kullanici:mesaj-3`.
2. **`ekranlar.json`** — şablon: `assets/ornek-proje/ekranlar.json`. Her ekran: `ad`, test için `widget` ifadesi ve `import`'u, `referans_goruntu`, `bilesenler`. Her bileşen: `anahtar` (`<ekran>.<bilesen>`, kodda `ValueKey` olur), `sira` (yukarıdan aşağı; yan yana olanlar aynı sıra), en az bir ölçü (`ust`, `sol`, `genislik`, `yukseklik`), gerekirse `adet` (liste satırı sayısı gibi).
3. Doğrula: `python scripts/tasarim.py dogrula --proje .`

Değerleri yalnızca kullanıcının verdiği yerden oku (Figma Inspect, kullanıcının yazdığı liste). PNG'ye bakıp "yaklaşık 16 dp" demek tahmindir — yapma; o değer eksiktir, sor.

## 3. Eksik değer — ne yapılır

- Kontrol listesindeki bir değer yoksa: sor. Soruya hangi ekran/bileşen için gerektiğini ve hangi kriteri etkilediğini yaz (ör. "S7: Sonuç kartı ile birim seçiciler arası boşluk kaç dp? → T4 sonucKarti.ust").
- Uygulama sırasında yerleşim testi (T4) bir farkı gösterir ve fark mevcut bir tasarım sabitiyle kapanmıyorsa (ör. 32 dp gerekiyor, `bosluk`'ta 32 yok): sabit ekleme, `SizedBox(height: 32)` yazma — **sor**. Cevap gelince `tasarim.json`'a kullanıcı kaynağıyla ekle, `uret` çalıştır.
- Bir Material bileşeni tasarımda tanımlı olmayan bir renk/yazı stili kullanıyorsa (kenarlık rengi, açılır liste metni…), varsayılanı sessizce bırakmak da bir tasarım kararıdır: sor; kullanıcı "varsayılan kalsın" derse `kararlar.json`'a kaydet. T1/T2 tema varsayılanlarını göremez, bu yüzden bu kontrol sende.
- Kullanıcı "sen karar ver" derse: bu skill'de tasarım değeri önerilmez. Kullanıcıya hangi değerin eksik olduğunu ve tasarım aracında nereye bakacağını söyle.

## 4. Onay

`python scripts/tasarim.py tablo --proje .` çıktısını (tüm değerler + her ekranın bileşen tablosu) kullanıcıya göster; mimari tablosu ve kabul kriterleriyle birlikte "Onaylıyorum" bekle.

## 5. Kod: tasarım değerlerini kullanma

1. `python scripts/tasarim.py uret --proje .` üretir:
   - `lib/cekirdek/tema/tasarim.g.dart` → `TasarimRenk`, `TasarimYazi`, `TasarimBosluk`, `TasarimKose`, `TasarimBilesen`
   - `test/yardimci/tasarim_fontlari.dart` → testlerde gerçek fontu ve Material ikonlarını yükler
   - `test/yerlesim/<ekran>_yerlesim_test.dart` → T4 kontrolleri
   - `test/goruntu/<ekran>_goruntu_test.dart` → T5/T6 ekran görüntüsü
2. `tema.dart` `ThemeData`'yı yalnızca bu sabitlerle kurar. Widget'larda renk/ölçü/yazı stili yalnızca `Tasarim*` sabitlerinden gelir: `EdgeInsets.all(TasarimBosluk.s16)`, `BorderRadius.circular(TasarimKose.kart)`, `style: TasarimYazi.govde`. Sayı veya `Color(0x…)`/`Colors.*` yazmak T1/T2'yi artırır.
3. Her bileşene `ekranlar.json`'daki anahtar: `key: const ValueKey('cevirici.sonucKarti')`.
4. Üretilmiş dosyaları elle düzenleme (T3). `dart format` serbesttir; T3 biçim farkını saymaz.

## 6. Ölçüm: T1–T6

`olc.py` hepsini kendiliğinden ölçer (`tasarim.json` varsa).

| ID | olc_anahtari | Ne ölçer | Hedef |
|---|---|---|---|
| T1 | tasarim_sabit_renk | `lib/` içinde (üretilmiş dosya hariç) `Color(0x…)`, `Color.fromARGB/RGBO`, `Colors.*` (transparent hariç) | == 0 |
| T2 | tasarim_sabit_olcu | `EdgeInsets.*(…)`, `BorderRadius/Radius.circular(…)`, `Size(…)` ve `width/height/fontSize/elevation/radius/…:` içindeki sıfır olmayan sayılar | == 0 |
| T3 | tasarim_uretim_uyumsuz | Üretilmiş dosyaların tasarım dosyalarından yeniden üretilenle içerik farkı | == 0 |
| T4 | tasarim_yerlesim_hata | `flutter test test/yerlesim` başarısız kontrol: bileşen adedi, sırası, üst/sol/genişlik/yükseklik (± tolerans) | == 0 |
| T5 | tasarim_goruntu_fark_yuzde | Ekran görüntüsü ↔ kullanıcının PNG'si, en büyük farklı piksel yüzdesi (kanal eşiği 16/255). Fark görüntüleri `build/tasarim_fark/` | ≤ kullanıcının eşiği |
| T6 | tasarim_onayli_goruntu_sapma | Kullanıcının onayladığı ekran görüntülerinden (`test/goruntu/goldens/`) sapan ekran | == 0 |

**T5 nasıl okunur:** Tasarım aracı ile Flutter aynı fontu biraz farklı çizebilir (kenar yumuşatma), bu yüzden %0 genelde gerçekçi değildir — eşik kullanıcının kararıdır. Fark görüntüsünde kırmızı alanlar farklı pikselleri gösterir; büyük kırmızı bloklar yerleşim/renk hatasıdır, ince kırmızı çizgiler çoğunlukla yazı kenarıdır. Fark görüntüsünü kullanıcıya göster.

**T6 akışı:** İlk ekran görüntüleri kullanıcıya gösterilir (`test/goruntu/olcum/` + fark görüntüleri). Kullanıcı onaylayınca `flutter test --update-goldens test/goruntu` ile `goldens/` oluşturulur. Bundan sonra tasarımda istenmemiş her görsel değişiklik T6'yı artırır. Golden'ı kullanıcı onayı olmadan güncellemek, ölçümü silmek demektir — yapma.

## 7. Sık hatalar

- **Ahem fontu:** Flutter testleri font yüklenmezse yazıları kutu olarak çizer; boyutlar ve görüntüler tasarımla tutmaz. Üretilmiş testler `tasarimFontlariniYukle()` çağırır; font dosyaları `pubspec.yaml`'da asset olarak tanımlı olmalı.
- **Çerçeve boyutu:** `ekran_boyutu × piksel_orani` tasarım PNG'sinin piksel boyutuyla aynı olmalı; değilse T5 ÖLÇÜLEMEDİ olur (ölçekleme yapılmaz — o da tahmin olurdu).
- **Async veri:** Ekran veriyi asenkron yüklüyorsa üretilmiş testler 500 ms bekler. Asset okurken `cache: false` kullan; önbellekli Future sonraki widget testinde tamamlanmaz ve ekran boş ölçülür.
- **Debug şeridi:** Testler `debugShowCheckedModeBanner: false` ile çizer; uygulamada da kapalı olmalı.
