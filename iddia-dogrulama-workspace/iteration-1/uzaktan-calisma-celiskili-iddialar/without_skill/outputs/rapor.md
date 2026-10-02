# Uzaktan Çalışma ve Verimlilik: Üç İddianın Doğrulanması

*Yönetim kurulu için hazırlanmıştır. Tarih: 2 Ekim 2026. Veri: 180 çalışan (`calisan_verimlilik.csv`).*

## 1. Kısa cevap

**Üç taraftan hiçbiri tam olarak haklı değil. En çok da çalışanların iddiası verinin yanıltıcı bir okumasına dayanıyor.**

| İddia | Sahibi | Hüküm | Gerekçe |
|---|---|---|---|
| "Uzaktan çalışma verimliliği **artırıyor**" | Çalışanlar | **Desteklenmiyor** (yanıltıcı) | Ham verideki güçlü pozitif ilişki (r = 0,44) tamamen **kıdemden** kaynaklanıyor. Kıdemli çalışanlar hem daha çok uzaktan çalışıyor hem daha verimli. Kıdem sabit tutulunca ilişki kayboluyor. |
| "Uzaktan çalışma verimliliği **düşürüyor**" | Genel müdür | **Desteklenmiyor** (genel hâliyle) | Kıdem ve departman kontrol edildiğinde gün başına etki −0,66 puan, 95% GA [−1,8; +0,5], p = 0,26. Anlamlı değil. Yalnız haftada **5 gün** uzaktan çalışan küçük grupta (n = 12) zayıf ve kırılgan bir düşüş işareti var. |
| "Uzaktan çalışma ile verimlilik arasında **hiçbir ilişki yok**" | İK | **Kısmen doğru, ama fazla kesin** | Ham veride açık bir ilişki *var* (korelasyon). Ancak bu ilişki nedensel görünmüyor: kıdem sabitken etki sıfırdan ayırt edilemiyor. Yine de veri "etki tam olarak sıfır" demeye yetmiyor: güven aralığı haftada 5 gün için −9 ile +2,5 puan arasındaki etkileri dışlamıyor. |

**Bu üç taraf içinde verinin en yakın durduğu yer İK'nın tutumu**, şu düzeltmeyle: *"Uzaktan gün sayısı ile verimlilik birlikte artıyor. Ama bunun sebebi kıdem. Uzaktan çalışmanın kendisinin verimliliği belirgin şekilde artırdığına ya da düşürdüğüne dair kanıt yok. Tamamen uzaktan çalışmanın etkisi ise belirsiz."*

## 2. İddialar birbiriyle uyuşuyor mu?

- **Genel müdür ve çalışanlar** doğrudan çelişiyor: biri etkinin negatif, diğeri pozitif olduğunu söylüyor. İkisi aynı anda doğru olamaz.
- **İK** ikisiyle de çelişiyor, çünkü etkinin sıfır olduğunu söylüyor.
- **Ancak üçü farklı soruları yanıtladığı için kısmen uzlaştırılabilir:**
  - Çalışanlar **ham ilişkiye** bakıyor: "Daha çok uzaktan çalışanlarımız daha verimli." Bu gözlem doğru ama nedensel değil.
  - İK **kontrollü ilişkiye** bakıyor: "Kıdem eşitken fark yok." Veri buna en yakın.
  - Genel müdürün kaygısı yalnızca **tamamen uzaktan (5 gün)** uç noktası için zayıf bir işaret buluyor. Genelleştirilmiş hâli desteklenmiyor.
- **İK'nın gönderdiği iki kaynak da birbiriyle çelişmiyor**, çünkü farklı şeyleri ölçüyorlar. Bloom ve ark. **ölçülen performansı** ölçüyor, dergi anketi ise **yöneticilerin algısını**. "Yöneticilerin %60'ı daha az verimli olduğunu düşünüyor" bilgisi verimlilik hakkında değil, yönetici kanaati hakkında bir bulgu.

## 3. Veri analizi

### 3.1 Veri
- 180 satır, eksik değer yok, tekrarlanan ID yok.
- Departmanlar: destek 48, satış 48, finans 45, yazılım 39.
- Haftalık uzaktan gün sayıları: 0 gün 40 kişi, 1 gün 35, 2 gün 35, 3 gün 39, 4 gün 19, 5 gün 12.
- Verimlilik puanı 36,5 ile 98,6 arasında. Ortalaması 67,5, standart sapması 11,4.

### 3.2 Ham ilişki: çalışanların gördüğü tablo
| Haftalık uzaktan gün | n | Ort. verimlilik | Ort. kıdem (yıl) |
|---|---|---|---|
| 0 | 40 | 58,6 | 2,4 |
| 1 | 35 | 66,9 | 4,8 |
| 2 | 35 | 68,8 | 4,9 |
| 3 | 39 | 70,3 | 6,9 |
| 4 | 19 | 74,0 | 8,5 |
| 5 | 12 | 75,5 | 11,4 |

- Pearson r = 0,44 (95% GA 0,31–0,55), p < 0,001. Basit regresyonda gün başına +3,3 puan.
- İlişki **her departmanda** ayrı ayrı da görülüyor: r = 0,42–0,51 ve hepsinde p < 0,01.
- **Ancak tablonun son sütununa bakın:** uzaktan gün arttıkça ortalama kıdem 2,4 yıldan 11,4 yıla çıkıyor.

### 3.3 Karıştırıcı değişken: kıdem
- Kıdem ile uzaktan gün arasındaki korelasyon r = 0,70. Kıdem ile verimlilik arasında r = 0,69. İkisi de p < 0,001.
- Yani kıdemli çalışanlar hem daha çok uzaktan çalışıyor (muhtemelen bu hak kıdemle veriliyor) hem de daha verimli.

### 3.4 Kıdem kontrol edildiğinde
| Model | Uzaktan gün katsayısı (puan/gün) | 95% GA | p | R² |
|---|---|---|---|---|
| Yalnız uzaktan gün | +3,30 | [+2,30; +4,29] | < 0,001 | 0,19 |
| + departman | +3,40 | [+2,39; +4,41] | < 0,001 | 0,20 |
| + kıdem | −0,64 | [−1,77; +0,49] | 0,26 | 0,48 |
| **+ kıdem + departman (ana model)** | **−0,66** | **[−1,82; +0,50]** | **0,26** | **0,48** |
| + kıdem² + departman | −0,60 | [−1,74; +0,55] | 0,31 | 0,50 |

- **Kısmi korelasyon** (kıdem sabitken): r = −0,08, p = 0,26.
- **Kıdem bantları içinde** ham korelasyon her bantta sıfıra yakın:

| Kıdem bandı | n | r | p |
|---|---|---|---|
| 0–3 yıl | 45 | 0,02 | 0,92 |
| 3–6 yıl | 53 | −0,04 | 0,77 |
| 6–9 yıl | 55 | 0,07 | 0,63 |
| 9+ yıl | 27 | −0,05 | 0,82 |

- Departmanlar arasında farklı bir etki yok. Etkileşim testi F = 0,004, p ≈ 1,00. Kıdem kontrol edildiğinde dört departmanın hiçbirinde anlamlı bir eğim çıkmıyor.
- Sonuç değişmiyor: robust (HC1) standart hatalarla da aynı.

### 3.5 Doğrusal olmayan etki: "5 gün" işareti (temkinli)
- Ana modele uzaktan gün² eklendiğinde ters U-şekli çıkıyor (p = 0,001). Kıdem² de eklendiğinde p = 0,015.
- Gün kategorilerini (referans 0 gün) kıdem, kıdem² ve departmanla birlikte modele koyunca:
  - 1 gün: +2,0 puan (p = 0,35)
  - 2 gün: +3,4 puan (p = 0,11)
  - 3 gün: −0,7 puan (p = 0,74)
  - 4 gün: −0,4 puan (p = 0,89)
  - 5 gün: −6,8 puan (p = 0,07; robust p = 0,04)
- Altı kategorinin ortak testi ise anlamlı değil: F = 1,99, p = 0,08.
- **Yorum:** Hibrit (1–2 gün) düzeyinde hafif bir artış ve tamamen uzaktan çalışmada (5 gün) bir düşüş *işareti* var. Ancak:
  - 5 gün grubu yalnızca 12 kişiden oluşuyor ve bu kişilerin kıdemi çok yüksek (ort. 11,4 yıl). Bu yüzden kıdem düzeltmesi bu uçta bir ekstrapolasyona dayanıyor.
  - Birden fazla karşılaştırma yapıldı.
  - Bu bulgu **ancak hipotez** olarak kullanılabilir. Genel müdürün genel iddiasını doğrulamaz.

### 3.6 Etki büyüklüğü
Ana modeldeki nokta tahmini −0,66 puan/gün. Bu, standart sapmanın 0,06'sı ve ortalama verimliliğin yaklaşık %1'i, yani pratikte küçük. Güven aralığı yine de 5 günlük farkta −9 ile +2,5 puan arasındaki etkileri dışlamıyor. Bu yüzden "etki kesinlikle sıfır" (İK'nın ifadesi) da kanıtlanmış değil.

## 4. Dış kaynakların değerlendirmesi

### (a) Bloom, Liang, Roberts ve Ying (2015), *Quarterly Journal of Economics* 130(1): 165–218
- **Doğrulandı:** Ctrip'in Şanghay çağrı merkezinde yapılmış rastgele kontrollü bir deney. Gönüllü 249 çalışan kura ile seçilmiş ve haftada 4 gün evden çalışmış. Performans %13 artmış: yaklaşık %9'u daha fazla çalışılan dakikadan (daha az mola ve hastalık izni), yaklaşık %4'ü dakika başına daha fazla çağrıdan geliyor. Ayrıca işten ayrılma yaklaşık %50 düşmüş. Öte yandan performans sabitken terfi oranı da düşmüş.
- **Güçlü yanı:** Rastgele deney olduğu için nedensellik iddiası sağlam. Bizim gözlemsel verimizden çok daha güçlü bir tasarım.
- **Sınırları (bizim şirkete genellenebilirlik):**
  - Tek bir şirket ve tek bir iş tipi: kolay ölçülen, bireysel, rutin çağrı merkezi işi.
  - Katılımcılar gönüllü.
  - Çin, 2010–2011, pandemi öncesi.
  - Yazılım, satış ve finans gibi iş birliği gerektiren işlere doğrudan taşınamaz.
  - Kısmen çalışanların iddiasını destekliyor ama **"bizim şirkette de artırır"** anlamına gelmez.
- **Literatür karışık:**
  - Aynı ekibin daha yeni çalışması (Bloom, Han ve Liang, 2024, *Nature*) 1.612 çalışanlı bir rastgele deney. Haftada 2 gün hibrit çalışmanın **performansı etkilemediğini** ama ayrılmaları üçte bir azalttığını buluyor. Bu sonuç bizim kontrollü bulgumuzla (anlamlı etki yok) uyumlu.
  - Hindistan'da bir BT firmasında yapılan gözlemsel bir çalışma (Gibbs, Mengel ve Siemroth, 2023, *JPE Micro*), pandemi döneminde evden çalışmada saat başına verimliliğin yaklaşık %8–19 düştüğünü raporluyor.
  - Etkinin yönü işe, düzene (tam uzaktan mı, hibrit mi) ve bağlama göre değişiyor.

### (b) 2023 iş dergisi haberi: "Yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor"
- **Ne ölçüyor:** Verimliliği değil, **yöneticilerin kanaatini**. Yalnızca yöneticilere sorulmuş ve çalışanlar örneklemde yok.
- **Kanıt değeri:** Verimlilik iddiası için düşük. Bu tür anketler bir "algı açığını" gösteriyor. Örneğin Bloom ve ark. 2024 deneyinde yöneticilerin beklentisi deneyden önce −%2,6 iken deneyden sonra +%1,0'a dönmüş.
- **Kaynak bilgisi:** Haberin adı ve yayın organı belirtilmemiş, bu yüzden doğrudan doğrulanamadı. Benzer bir rakam Owl Labs'ın 2023 "State of Remote Work" raporunda geçiyor: "Yöneticilerin %60'ı uzaktan çalışanların daha az verimli olmasından endişeli." Haberin kaynağı muhtemelen bu rapor, ama bu bir varsayım.
- Genel müdürün iddiasını **ölçüm olarak değil, yaygın bir kanaat olarak** destekliyor.

### Kanıt hiyerarşisi (en güçlüden zayıfa)
1. Rastgele deneyler (Bloom 2015, Bloom 2024). Nedensel kanıt, ama başka şirketler ve işler için.
2. Bizim şirket verisi, kıdem ve departman kontrollü. Bizim bağlamımızda ama gözlemsel.
3. Bizim şirket verisi, ham. Kıdemle karışmış olduğu için yanıltıcı.
4. Yönetici kanaat anketi. Verimliliği ölçmüyor.

## 5. Sınırlar ve varsayımlar
- **Gözlemsel veri:** Uzaktan gün sayısı rastgele atanmamış. Kıdem ve departman kontrol edildi, ama ölçülmeyen başka faktörler (rol, yönetici, ev koşulları, performansa göre uzaktan çalışma izni verilmesi gibi ters nedensellik) sonucu etkileyebilir.
- **Verimlilik puanının nasıl ölçüldüğü bilinmiyor.** Yönetici değerlendirmesiyse algı yanlılığı içerebilir. Analizde bunun nesnel bir ölçü olduğu varsayıldı.
- **Kesit veri:** Tek bir zaman noktası. Aynı kişinin uzaktan gün sayısı değiştiğinde ne olduğunu göremiyoruz.
- **Örneklem:** 180 kişi küçük. Özellikle 4–5 gün grupları az kişiden oluşuyor (19 ve 12), bu yüzden bu uçtaki tahminler belirsiz.
- **"Hiç ilişki yok" iddiası için eşik:** Pratikte önemsiz kabul edilecek etki eşiği önceden tanımlanmadığı için eşdeğerlik iddiası kurulamadı. Güven aralığı sunuldu.

## 6. Yönetim kurulu için öneriler
1. **Ham karşılaştırmalarla karar vermeyin.** "Uzaktan çalışanlar daha verimli" ya da "daha verimsiz" türünden çıkarımlar kıdem farkıyla karışıyor.
2. **Mevcut veriyle hibrit düzenin (1–3 gün) verimliliğe zarar verdiğine dair bir kanıt yok.** Dış literatür de (Bloom 2024) aynı yönde.
3. **Tamamen uzaktan (5 gün) düzen için temkinli olun** ve bunu ölçün. Burada zayıf bir negatif işaret var, ama 12 kişilik grup kesin hüküm için yetersiz.
4. **Kesin cevap için küçük bir pilot yapın.** Bir veya iki departmanda uzaktan gün sayısını kura ile atayın (örneğin 0, 2 ve 4 gün) ve 3–6 ay boyunca nesnel çıktı metriklerini izleyin. Aynı çalışanları zaman içinde izleyen panel veri de toplanabilir.
5. **Verimlilik ölçümünü netleştirin.** Yönetici puanı yerine ya da yanında nesnel çıktı ölçütleri kullanın.

## 7. Dosyalar
- `analiz.py`: Ana analiz (yalnızca Python standart kütüphanesi). Çalıştırınca `sonuclar.json` dosyasını üretir.
- `ek_analiz.py`: Sağlamlık kontrolleri (kıdem², gün kategorileri, kıdem bantları, kısmi korelasyon). Çalıştırınca `ek_sonuclar.json` dosyasını üretir.
- `sonuclar.json` ve `ek_sonuclar.json`: Tüm sayısal sonuçlar.
- `iddia_degerlendirme.json`: İddia bazında yapılandırılmış hüküm özeti.

## Kaynaklar
- Bloom, N., Liang, J., Roberts, J., Ying, Z. J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. *QJE* 130(1), 165–218. https://www.nber.org/papers/w18871 · https://ideas.repec.org/a/oup/qjecon/v130y2015i1p165-218.html
- Bloom, N., Han, R., Liang, J. (2024). Hybrid working from home improves retention without damaging performance. *Nature* 630, 920–925. https://www.nature.com/articles/s41586-024-07500-2
- Gibbs, M., Mengel, F., Siemroth, C. (2023). Work from Home and Productivity: Evidence from Personnel and Analytics Data on IT Professionals. *JPE Microeconomics* 1(1). https://docs.iza.org/dp14336.pdf
- Yönetici algısı (%60) için olası kaynak: Owl Labs 2023 *State of Remote Work* (ikincil özetlerden; birincil kaynak doğrudan doğrulanmadı). https://hbr.org/2023/01/research-where-managers-and-employees-disagree-about-remote-work (yönetici ve çalışan algı farkına dair ilgili bir HBR yazısı)
