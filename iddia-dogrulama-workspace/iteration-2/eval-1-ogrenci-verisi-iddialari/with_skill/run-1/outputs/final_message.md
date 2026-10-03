Hocanızın 4 iddiasını 240 öğrencilik verinizle test ettim. İkisi tutuyor (biri yalnızca kısmen), ikisi tutmuyor.

| # | İddia | Sonuç | Olasılık (P) | Verideki karşılığı |
|---|---|---|---|---|
| 1 | Çok çalışanın notu yüksek | **Tutuyor** | **%98.7** | r = 0.59, yani güçlü bir ilişki. Haftada 1 saat fazla çalışma yaklaşık +1.4 not puanı demek. Diğer değişkenler sabit tutulunca da değişmiyor. |
| 2 | Sosyal medya notu düşürüyor | **Kısmen tutuyor** | İlişki: **%97.9** · "Düşürüyor": **%52.7** | Sosyal medyada daha çok vakit geçirenlerin notu daha düşük (r = −0.24). "Düşürüyor" ise neden-sonuç iddiası; bunu kesitsel veri kanıtlayamaz, bu yüzden belirsiz kaldı. |
| 3 | Kızlar erkeklerden daha başarılı | **Tutmuyor** | **%6.9** | Kızların ortalaması 78.7, erkeklerin 80.6. Kızlar aslında 1.9 puan geride ama bu fark anlamsız (p = 0.22). En olası açıklama "cinsiyet farkı yok" (%72). |
| 4 | Uykunun notla alakası yok | **Tutmuyor** | **%1.1** | Tersine, uyku ile not arasında pozitif ilişki var (r = +0.26; "uyku arttıkça not artar" için P = %97.8). 6 saatten az uyuyanların ortalaması 73.8, 8 saat ve üzeri uyuyanlarınki 83.2. |

**Dikkat edilmesi gereken iki nokta:**
- **Sosyal medyanın etkisinin bir kısmı uykuyla ilişkili olabilir.** Sosyal medya ile uyku arasında r = −0.51 var. Uyku hesaba katılınca sosyal medyanın nota etkisi saat başına −2.6 puandan −1.6 puana iniyor. Yani sosyal medya uykuyu kısaltarak notu dolaylı yoldan etkiliyor olabilir. Bunu netleştirmek için öğrencileri dönemler boyunca izleyen bir veri ya da bir deney gerekir.
- **Sonuçlar bu 240 öğrenciye özgü.** Tek bir veri setine dayandığı için rapor bunları "ön bulgu" olarak işaretliyor. Siz yalnızca kendi verinizle doğrulama istediğiniz için literatür taraması yapmadım. Cinsiyet sonucu varsayımlara en duyarlı olanı: farklı senaryolarda "fark yok" olasılığı %54 ile %95 arasında değişiyor. Yine de "kızlar daha başarılı" iddiası hiçbir senaryoda %25'in üstüne çıkmıyor.

**Varsayımlarım:** "Daha başarılı" sözünü daha yüksek not ortalaması olarak aldım. Boş ve NA değerleri eksik veri saydım; sosyal medyada 6, uykuda 9 eksik değer vardı. Notu tam 100 olan 11 öğrenci var; onları çıkarınca da sonuçlar değişmedi. Her olasılık, veriye bakmadan önce belirlediğim bir başlangıç değerinin verideki kanıtla güncellenmesiyle hesaplandı.

Dosyalar `iteration-2/eval-1-ogrenci-verisi-iddialari/with_skill/run-1/outputs/` klasöründe:
- `rapor.md`: tam rapor, yorum ve öneriler burada
- `metadata.json`: tüm sayılar
- `girdi.json`: iddialar, başlangıç olasılıkları ve analizler
- `ek_analizler.json`: ek sağlamlık kontrolleri
