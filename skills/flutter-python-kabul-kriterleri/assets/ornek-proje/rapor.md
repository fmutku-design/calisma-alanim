| ID | Metrik | Hedef | Ölçülen | Sonuç | Kanıt / Sebep |
|---|---|---|---|---|---|
| F1 | 5 km → m dönüşümünde 5000 gösterilir (test başarılı mı) | == 1 evet_hayir | 1 evet_hayir | **GEÇTİ** | flutter test test/ozellikler/cevirme_test.dart → çıkış kodu 0: 00:01 +3: All tests passed! |
| F3 | Sayı olmayan girdide uyarı gösterilir (test başarılı mı) | == 1 evet_hayir | 1 evet_hayir | **GEÇTİ** | flutter test test/ozellikler/cevirme_test.dart → çıkış kodu 0: 00:01 +1: All tests passed! |
| F4 | Python çıktısındaki kayıt sayısı CSV satır sayısına eşit mi | == 1 evet_hayir | 1 evet_hayir | **GEÇTİ** | pytest tools/test_birim_tablosu.py → çıkış kodu 0: 2 passed in 0.03s |
| K1 | flutter analyze bulgu sayısı | == 0 adet | 0 adet | **GEÇTİ** | flutter analyze → No issues found! |
| K4 | Başarısız Dart test sayısı | == 0 adet | 0 adet | **GEÇTİ** | flutter test → 31 geçti, 0 başarısız |
| K5 | ruff check bulgu sayısı | == 0 adet | 0 adet | **GEÇTİ** | ruff check tools → 0 bulgu |
| O2 | lib/ içinde ağ kodu referansı sayısı | == 0 adet | 0 adet | **GEÇTİ** | lib/ tarandı (9 dosya) → ağ kodu yok |
| T1 | tasarim.json dışında lib/ içinde yazılmış renk sayısı (Color(0x…), Colors.*) | == 0 adet | 0 adet | **GEÇTİ** | lib/ tarandı: bulgu yok |
| T2 | tasarim.json dışında lib/ içinde yazılmış ölçü sayısı (EdgeInsets, SizedBox, fontSize, radius… içindeki sayılar) | == 0 adet | 0 adet | **GEÇTİ** | lib/ tarandı: bulgu yok |
| T3 | tasarim.json/ekranlar.json'dan üretilen dosyalarla içeriği uyuşmayan dosya sayısı | == 0 adet | 0 adet | **GEÇTİ** | Üretilmiş dosyaların hepsi tasarım dosyalarıyla birebir aynı. |
| T4 | ekranlar.json yerleşim testlerinde başarısız kontrol sayısı (adet, sıra, ölçü, konum) | == 0 adet | 0 adet | **GEÇTİ** | flutter test test/yerlesim → 26 kontrol geçti, 0 başarısız |
| T5 | Kullanıcının tasarım görseli ile uygulama ekran görüntüsü arasındaki en büyük piksel farkı (ekran başına) | <= 2 % | 0.0 % | **GEÇTİ** | en büyük fark raporlanır \| cevirici.png ↔ cevirici.png: 0/288000 piksel farklı (%0.0, kanal eşiği 16, 360x800) \| fark görüntüleri: build/tasarim_fark/ |
| T6 | Onaylı ekran görüntüsünden (goldens/) sapan ekran sayısı | == 0 adet | 0 adet | **GEÇTİ** | flutter test test/goruntu → 1 ekran onaylı görüntüyle aynı, 0 sapma |
| Y1 | Katman kuralını çiğneyen import sayısı | == 0 adet | 0 adet | **GEÇTİ** | 9 Dart dosyasının importları katman kurallarına uyuyor. |
| Y2 | mimari.json'daki hiçbir katmana ait olmayan lib/ dosyası sayısı | == 0 adet | 0 adet | **GEÇTİ** | Her lib/ dosyası tanımlı bir katmanda. |
| Y3 | mimari.json dosya_satir_max sınırını aşan dosya sayısı | == 0 adet | 0 adet | **GEÇTİ** | Hiçbir dosya 200 satırı aşmıyor. |
| Y4 | mimari.json fonksiyon_satir_max sınırını aşan fonksiyon sayısı | == 0 adet | 0 adet | **GEÇTİ** | Hiçbir fonksiyon 40 satırı aşmıyor. |

Davranış metrikleri (Claude — zorunlu, denetim.py kontrol):

| ID | Metrik | Hedef | Ölçülen | Sonuç | Kanıt / Sebep |
|---|---|---|---|---|---|
| D1 | Kaynaksız karar (varsayım) sayısı | == 0 adet | 0 adet | **GEÇTİ** | Tüm paketler, kararlar ve kriterler kullanıcı kaynaklı. |
| D2 | Onaysız yazılmış kod dosyası sayısı | == 0 adet | 0 adet | **GEÇTİ** | Onay var: "Onaylıyorum." (2026-10-03). Kod dosyası: 18 |
| D3 | Test dosyası olmayan fonksiyonel kriter sayısı | == 0 adet | 0 adet | **GEÇTİ** | Her F kriterinin test dosyası mevcut. |
| D5 | Kriter/karar ID'si taşımayan test sayısı (kayda geçmemiş davranış) | == 0 adet | 0 adet | **GEÇTİ** | 33 testin 0 tanesinde kriter/karar ID'si yok. |

Toplam 21 kriter: 21 GEÇTİ, 0 KALDI, 0 ÖLÇÜLEMEDİ.
DURUM: TAMAM — tüm kabul kriterleri ve davranış metrikleri karşılandı.
