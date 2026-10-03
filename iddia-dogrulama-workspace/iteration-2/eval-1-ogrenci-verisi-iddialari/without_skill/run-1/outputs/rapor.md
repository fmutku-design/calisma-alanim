# Danışman İddialarının Doğrulanması: Öğrenci Verisi (n = 240)

**Veri:** `inputs/ogrenci_verisi.csv` (240 öğrenci; değişkenler: cinsiyet, okul türü, haftalık çalışma saati, günlük sosyal medya saati, uyku saati, not ortalaması)
**Analiz kodu:** `analiz.py` · **Tüm sayısal sonuçlar:** `analiz_sonuclari.json`
**Tarih:** 3 Ekim 2026

---

## 1. Kısa sonuç

| # | İddia | Karar | Etki (95% GA) | p | Bayes: P(ilişki/fark var \| veri)* |
|---|---|---|---|---|---|
| 1 | Daha çok çalışan öğrencinin notu daha yüksek | **TUTUYOR (güçlü)** | r = 0,59 [0,50; 0,67]; çalışılan her ek saat/hafta ≈ +1,4 puan | 5×10⁻²⁴ | > %99,99 (BF₁₀ ≈ 7×10²⁰) |
| 2 | Sosyal medya notları düşürüyor | **İLİŞKİ TUTUYOR; "düşürüyor" (nedensellik) kanıtlanamaz** | r = −0,24 [−0,36; −0,12]; günlük her ek saat ≈ −2,5 puan (ham), −1,6 puan (kontrollü) | 0,00016 | ≈ %98,5 (BF₁₀ ≈ 64) |
| 3 | Kızlar erkeklerden daha başarılı | **TUTMUYOR** | Kız − Erkek = −1,9 puan [−5,0; +1,2]; yön bile ters | 0,22 (iki yönlü); 0,89 (tek yönlü, kız > erkek) | Fark var: ≈ %22; **kızların ortalamasının daha yüksek olma olasılığı ≈ %11** (bootstrap) |
| 4 | Uyku süresinin notla alakası yok | **TUTMUYOR** | r = 0,26 [0,14; 0,38]; her ek saat uyku ≈ +3,3 puan (ham), +2,2 puan (kontrollü) | 0,00006 | İlişki var: ≈ %99,4 (BF₁₀ ≈ 172) |

\* JZS Bayes faktörü ile, "ilişki var" ve "ilişki yok" hipotezlerine başta eşit (%50–%50) olasılık verilerek hesaplanmıştır. **p değeri iddianın doğru olma olasılığı değildir**; p, "gerçekte hiçbir ilişki olmasaydı bu kadar güçlü bir sonucu görme olasılığı" demektir. Bu yüzden iki ölçüt birlikte verilmiştir.

**Özetle:** 4 iddiadan 1'i açıkça doğru (çalışma), 1'i ilişki olarak doğru ama neden-sonuç olarak bu veriyle kanıtlanamaz (sosyal medya), 2'si veriyle çelişiyor (cinsiyet ve uyku).

Dört test birlikte yapıldığı için Holm düzeltmesi uygulandı. Düzeltme sonrasında da 1, 2 ve 4 anlamlı kalıyor (düzeltilmiş p'ler sırasıyla 2×10⁻²³, 0,0003, 0,0002), 3 ise anlamsız (0,22).

---

## 2. Veri kalitesi ve varsayımlar

- **240 satır, tekrar eden kayıt yok.** Ayraç `;`, ondalık işareti `,`.
- **Eksik değerler:** sosyal medya 6 (`NA`), uyku 9 (boş hücre). Toplam 226 öğrencinin verisi tam. Her analizde ilgili değişkeni dolu olan öğrenciler kullanıldı. Çoklu regresyonda n = 226.
- **Tavan etkisi:** 11 öğrencinin notu tam 100. Bu öğrenciler çıkarılınca da sonuçlar değişmiyor (bkz. Bölüm 7).
- **Uç değerler:** 1 öğrencinin haftalık çalışması 0 saat. Çıkarılınca r = 0,58 (değişmiyor). Sosyal medyada en yüksek değer 8,2 saat/gün. En üst %1 çıkarılınca ilişki biraz güçleniyor (r = −0,27).
- **Varsayımlar:** `K` = kız, `E` = erkek. Not ortalaması 0–100 ölçeğinde (gözlenen aralık 38,7–100). Değerler muhtemelen öğrencinin kendi beyanı, bu da ölçüm hatası içerebilir.
- **Tasarım:** Veri kesitsel ve gözlemsel. Bu nedenle bütün bulgular **ilişki** gösterir, **neden-sonuç** göstermez.

---

## 3. İddia 1: "Haftada daha çok çalışan öğrencinin not ortalaması yüksek oluyor"

**Karar: TUTUYOR (çok güçlü kanıt).**

| Haftalık çalışma (çeyrek) | Aralık (saat) | n | Ortalama not |
|---|---|---|---|
| Q1 (en az) | 0 – 11,75 | 60 | 69,5 |
| Q2 | 11,75 – 15,0 | 61 | 78,3 |
| Q3 | 15,0 – 18,5 | 61 | 83,7 |
| Q4 (en çok) | 18,5 – 26,4 | 58 | 87,5 |

- Pearson r = 0,59, 95% GA [0,50; 0,67], p = 5×10⁻²⁴. Spearman ρ = 0,58. Bootstrap GA [0,51; 0,66].
- Çalışma saati, notlardaki farklılığın yaklaşık **%35'ini** tek başına açıklıyor.
- Haftada 1 saat fazla çalışma ≈ **+1,43 puan** ile ilişkili. Sosyal medya, uyku, cinsiyet ve okul türü sabit tutulduğunda da **+1,40 puan** [1,15; 1,64].
- En az çalışan çeyrek ile en çok çalışan çeyrek arasındaki fark yaklaşık **18 puan**.
- 10.000 bootstrap örneğinin hepsinde ilişki pozitif çıktı. Bayes faktörü ≈ 7×10²⁰, yani ilişkinin var olma olasılığı pratikte %100.

---

## 4. İddia 2: "Sosyal medya notları düşürüyor"

**Karar: Negatif ilişki TUTUYOR. "Düşürüyor" ifadesindeki neden-sonuç iddiası bu veriyle kanıtlanamaz.**

| Günlük sosyal medya (çeyrek) | Aralık (saat) | n | Ortalama not |
|---|---|---|---|
| Q1 (en az) | 0,1 – 2,2 | 61 | 84,3 |
| Q2 | 2,2 – 3,1 | 62 | 80,3 |
| Q3 | 3,1 – 3,8 | 57 | 78,0 |
| Q4 (en çok) | 3,8 – 8,2 | 54 | 75,3 |

- Pearson r = −0,24, 95% GA [−0,36; −0,12], p = 0,00016. Spearman ρ = −0,26. Bootstrap örneklerinin tamamında ilişki negatif.
- Günde 1 saat fazla sosyal medya ≈ **−2,5 puan** (ham). Çalışma, uyku, cinsiyet ve okul türü kontrol edilince ≈ **−1,6 puan** [−2,6; −0,6], p = 0,002.
- Bayes faktörü ≈ 64: "ilişki var" hipotezi "ilişki yok" hipotezinden yaklaşık 64 kat daha iyi destekleniyor. Eşit başlangıç olasılığıyla P(ilişki var) ≈ **%98,5**.
- **Önemli ayrıntı:** Sosyal medya süresi uykuyla güçlü biçimde ters ilişkili (r = −0,51), çalışma süresiyle ise ilişkisiz (r = 0,01). Uyku kontrol edilince etki −2,5'ten −1,6 puana düşüyor. Yani sosyal medyanın notla ilişkisinin bir kısmı **uykunun azalması üzerinden** geçiyor olabilir; çalışma süresini azaltması üzerinden geçmiyor gibi görünüyor.
- **Neden "düşürüyor" diyemiyoruz?** Ters yön de mümkün: notu düşük olan öğrenci sosyal medyaya daha çok vakit ayırıyor olabilir. Ölçülmemiş üçüncü bir etken de (motivasyon, stres vb.) ikisini birden etkiliyor olabilir. Neden-sonuç için deneysel ya da boylamsal veri gerekir.

---

## 5. İddia 3: "Kızlar erkeklerden daha başarılı"

**Karar: TUTMUYOR.** Veride kızların ortalaması daha yüksek değil; biraz daha düşük. Bu küçük fark da istatistiksel olarak anlamlı değil.

| Grup | n | Ortalama | Std. sapma | Medyan |
|---|---|---|---|---|
| Kız | 119 | 78,7 | 13,3 | 80,5 |
| Erkek | 121 | 80,6 | 11,0 | 81,3 |

- Fark (kız − erkek) = **−1,9 puan**, 95% GA [−5,0; +1,2]. Welch t = −1,23, p = 0,22. Mann-Whitney p = 0,32. Cohen d = −0,16 (çok küçük).
- İddianın yönünü test eden tek yönlü test (kız > erkek): p = 0,89.
- Bootstrap: kızların ortalamasının erkeklerden yüksek olma olasılığı ≈ **%11**.
- Bayes faktörü BF₀₁ ≈ 3,5: veri **"fark yok"** hipotezini, "fark var" hipotezinden yaklaşık 3,5 kat daha çok destekliyor (orta düzeyde kanıt). P(fark var) ≈ %22.
- **Kontrollerle de değişmiyor:**
  - Okul türü sabit tutulduğunda fark −2,1 puan, p = 0,20.
  - Tüm değişkenler sabit tutulduğunda fark −1,2 puan, p = 0,35.
  - Devlet okulunda kız 77,9, erkek 79,7. Özel okulda kız 79,4, erkek 81,7. İki okul türünde de erkekler biraz önde, fark anlamsız.
- Not: Güven aralığı +1,2 puana kadar uzandığı için kızların küçük bir üstünlüğü tamamen dışlanamaz. Ancak hocanın iddia ettiği türden belirgin bir üstünlük bu veride yok.

---

## 6. İddia 4: "Uyku süresinin notla bir alakası yok"

**Karar: TUTMUYOR.** Uyku ile not arasında anlamlı ve pozitif bir ilişki var.

| Uyku | n | Ortalama not |
|---|---|---|
| < 6 saat | 40 | 73,8 |
| 6–7 saat | 84 | 79,0 |
| 7–8 saat | 73 | 81,6 |
| ≥ 8 saat | 34 | 83,2 |

- Pearson r = 0,26, 95% GA [0,14; 0,38], p = 0,00006. Spearman ρ = 0,23. Bootstrap örneklerinin tamamında ilişki pozitif.
- 1 saat fazla uyku ≈ **+3,3 puan** (ham). Diğer değişkenler kontrol edilince ≈ **+2,2 puan** [0,8; 3,7], p = 0,002.
- 6 saatten az uyuyanlarla 8 saat ve üzeri uyuyanlar arasındaki fark yaklaşık **9 puan**.
- Bayes faktörü ≈ 172. P(ilişki var) ≈ **%99,4**.
- "Alakası yok" iddiasını doğrudan sınamak için eşdeğerlik testi (TOST) yapıldı: "ilişki ihmal edilebilir düzeyde, |r| < 0,10" hipotezi için p = 0,99. Veri "ilişki yok" iddiasını desteklemiyor.
- Ters-U biçiminde bir ilişki (çok uyumanın zararlı olması) aranmış ama bulunamamıştır (kare terim p = 0,51). Bu veride ilişki doğrusal görünüyor.
- Uyku verisi eksik olan 9 öğrencinin not ortalaması 82,8. Bu sayı sonucu değiştirecek büyüklükte değil.

---

## 7. Tüm değişkenler birlikte (çoklu regresyon) ve sağlamlık kontrolleri

Model: not ~ çalışma + sosyal medya + uyku + kız + özel okul. n = 226, R² = 0,44, standart hatalar HC3.

| Değişken | Katsayı (puan) | 95% GA | p | 1 standart sapma artışın etkisi |
|---|---|---|---|---|
| Haftalık çalışma (saat) | +1,40 | [1,15; 1,64] | < 10⁻²⁸ | +7,1 puan |
| Günlük sosyal medya (saat) | −1,57 | [−2,59; −0,56] | 0,002 | −1,9 puan |
| Uyku (saat) | +2,23 | [0,79; 3,67] | 0,002 | +2,2 puan |
| Kız (erkeğe göre) | −1,17 | [−3,62; +1,28] | 0,35 | – |
| Özel okul (devlete göre) | +2,11 | [−0,34; +4,55] | 0,09 | – |

- Notu 100 olan 11 öğrenci çıkarıldığında (n = 215) katsayılar şöyle: çalışma +1,31, sosyal medya −1,32 (p = 0,009), uyku +2,14 (p = 0,003), kız −1,37 (p = 0,27). **Hiçbir karar değişmiyor.**
- Kalıntılar normal dağılıma uygun (Jarque-Bera p = 0,72).
- Göreli önem sırası: çalışma, notla açık ara en güçlü ilişkiye sahip değişken. Uyku ve sosyal medyanın etkileri bundan küçük ve birbirine yakın.

---

## 8. Sınırlılıklar

1. **Gözlemsel veri.** Hiçbir bulgu neden-sonuç kanıtı değildir. Bu özellikle 2. iddiadaki "düşürüyor" ifadesi için önemli.
2. **Örneklem.** Veri tek bir 240 kişilik örneklemden geliyor. Başka okul ya da dönemlere genellenmesi kesin değil.
3. **Ölçüm.** Saat bilgileri büyük olasılıkla öğrencilerin kendi beyanına dayanıyor ve yuvarlama ya da hatırlama hatası içerebilir.
4. **Bayes olasılıkları varsayıma bağlı.** Burada başlangıçta "%50 ilişki var / %50 yok" varsayıldı. Farklı bir başlangıç inancıyla sayılar değişir, ama 1, 2 ve 4'teki kanıt o kadar güçlü ki makul her varsayımda karar aynı kalır.

---

## 9. Dosyalar

- `rapor.md`: bu rapor
- `analiz_sonuclari.json`: tüm istatistiklerin makinece okunabilir dökümü
- `analiz.py`: analizi baştan üreten Python betiği (pandas, scipy, statsmodels)
- `final_message.md`: kullanıcıya verilen özet yanıt
