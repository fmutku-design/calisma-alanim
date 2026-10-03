Üç taraftan hiçbiri tam haklı değil. Verilere en yakın olan İK, ama "hiçbir ilişki yok" demesi fazla kesin. Asıl mesele şu: uzaktan çalışanlar daha kıdemli, kıdemliler de daha verimli.

## Verideki tablo (180 çalışan)

- **İlk bakışta çalışanlar haklı görünüyor.** Uzaktan gün sayısı arttıkça verimlilik de artıyor (r = 0,44). 5 gün uzaktan çalışanların ortalaması 75,5, hiç uzaktan çalışmayanlarınki 58,6. Bu desen dört departmanın hepsinde var.
- **Bunun sebebi kıdem.** Uzaktan gün sayısı kıdemle birlikte artıyor (r = 0,70). Hiç uzaktan çalışmayanlar ortalama 2,4 yıllık, 5 gün uzaktan çalışanlar 11,4 yıllık. Kıdem de verimlilikle güçlü biçimde ilişkili (r = 0,69).
- **Kıdem ve departman sabit tutulunca etki kayboluyor.** Her ek uzaktan gün yaklaşık −0,66 puan fark ediyor. %95 güven aralığı −1,9 ile +0,6 arasında ve sıfırı içeriyor (p = 0,31), yani istatistiksel olarak anlamlı değil. Sonuç dört farklı model kurulumunda, bootstrap'ta ve kıdem dilimlerinde ayrı ayrı bakıldığında da değişmiyor. Departmanlar arasında da fark yok.

## Kim ne kadar haklı?

| İddia | Hüküm |
|---|---|
| **Genel müdür:** uzaktan çalışma verimliliği düşürüyor | **Desteklenmiyor.** Ham veri bunun tersini gösteriyor. Kıdem düzeltmesinden sonra kalan küçük negatif eğim istatistiksel olarak anlamlı değil. |
| **Çalışanlar:** uzaktan çalışma verimliliğimizi artırıyor | **Desteklenmiyor.** Gözlem doğru ama sebebi uzaktan çalışma değil, kıdem. Düzeltilmiş tahminin üst sınırı gün başına +0,6 puan. Bloom çalışmasındaki büyüklükte bir artış (gün başına yaklaşık 2,2 puan) bu veriyle uyumlu değil. |
| **İK:** hiçbir ilişki yok | **Kısmen doğru.** Ham veride güçlü bir ilişki var. Kıdem sabit tutulunca anlamlı bir etki kalmıyor, ama sıfır olduğu da kanıtlanmış değil. 0 günden 5 güne geçişin etkisi −9,6 ile +3,1 puan arasında olabilir. Orta büyüklükte bir düşüş dışlanamıyor. |

## İddialar birbiriyle uyuşuyor mu?

Söylendikleri haliyle hayır. Biri düşüş, biri artış, biri sıfır diyor, üçü aynı anda doğru olamaz. Ancak her taraf farklı bir soruya cevap veriyor:

- **Çalışanlar** ham tabloya bakıyor: uzaktan çalışanlar gerçekten daha verimli.
- **İK** kıdem gibi farkları hesaba katan karşılaştırmaya yakın: aynı kıdemdeki kişiler arasında anlamlı fark yok.
- **Genel müdürün** iddiası ise bir algı. Verilerde karşılığı yok.

İK'nın iki kaynağı da birbirini çürütmüyor, çünkü farklı şeyler ölçüyorlar:

- **(a) Bloom ve ark. 2015:** Atıf doğru (QJE, Ctrip çağrı merkezi, rastgele deney, %13 artış). Ama katılımcılar gönüllüydü, haftada 4 gün evden çalıştılar ve iş kolay ölçülen bireysel bir işti. Evden çalışanların terfi oranı da düştü. Aynı ekibin 2024 tarihli hibrit deneyinde (Nature) performansa etki bulunmadı. Başka bir çalışmada ise (Emanuel ve Harrington 2024) uzaktan çalışanlar daha az verimli çıktı. Kısacası literatür karışık. Ayrıca bu kaynak İK'nın "ilişki yok" iddiasını değil, çalışanların iddiasını destekliyor.
- **(b) "Yöneticilerin %60'ı" haberi:** Bu bir algı anketi, verimlilik ölçümü değil. Büyük ihtimalle Owl Labs'ın 2023 anketi. Birincil kaynağı açamadım, eşleşme arama sonuçlarına dayanıyor. Aynı ankette çalışanların %62'si kendini uzaktan daha verimli hissettiğini söylüyor. Yani şirketteki tartışmanın aynısını ölçüyor, kimin haklı olduğunu değil. Genel müdürün iddiasına kanıt sayılmaz.

## Kurula sunarken dikkat edilecekler

- **Veri gözlemsel.** Uzaktan çalışma hakkı performansa göre veriliyorsa sonuç çarpılmış olabilir.
- **Verimlilik puanının nasıl ölçüldüğünü bilmiyorum.** Yönetici değerlendirmesiyse, (b)'deki yönetici önyargısını taşıyor olabilir.
- **İki zayıf sinyal var, aşırı yorumlamayın:**
  - Yazılım departmanında departman içi eğim −2,15/gün (p = 0,027), ama dört departman ayrı ayrı test edildiği için bu sonuç anlamlılık eşiğini geçmiyor.
  - Tam uzaktan (5 gün) çalışanlarda −6,8 puan (p = 0,06), ama bu grupta yalnızca 12 kişi var.
- **Öneri:** Ham korelasyona dayanarak ne uzaktan çalışmayı genişletin ne de kısıtlayın. Kesin cevap için kıdeme göre tabakalı, rastgele atamalı bir pilot yapın, örneğin 6 ay hibrit (2 gün) ile ofis karşılaştırması. Verimliliği nesnel çıktıyla ölçün ve işten ayrılmayı da izleyin.

Her şeyi kaydettim. Rapor ve grafikler kurula sunulabilir durumda. İsterseniz raporu paylaşılabilir bir web sayfası olarak da yayımlayabilirim.

Dosyalar `.../without_skill/run-1/outputs/` klasöründe:
- `rapor.md`: kurul raporu
- `grafik_1_ham_iliski.png`, `grafik_2_kidem_karistirici.png`, `grafik_3_ham_vs_duzeltilmis.png`: grafikler
- `sonuclar.json`: tüm sayılar
- `analiz.py`: tekrar üretilebilir analiz kodu
