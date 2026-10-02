# Danışman İddialarının Doğrulanması: Öğrenci Verisi (n = 240)

**Veri:** `inputs/ogrenci_verisi.csv` (240 öğrenci, 119 kız / 121 erkek, 120 devlet / 120 özel okul)
**Analiz:** `analiz.py` (Python 3.11, pandas, scipy, statsmodels). Tüm sayısal sonuçlar `sonuclar.json` dosyasında.
**Tarih:** 2026-10-02

---

## 1. Özet tablo

| # | Danışmanın iddiası | Sonuç | Etki büyüklüğü | p (iki yönlü) | İddia yönündeki olasılık* |
|---|---|---|---|---|---|
| 1 | Daha çok çalışanın notu yüksek | **TUTUYOR (güçlü)** | r = +0.59; haftada +1 saat ≈ +1.4 puan | < 10⁻²³ | ≈ %100 |
| 2 | Sosyal medya notları düşürüyor | **TUTUYOR (orta/zayıf, ilişki olarak)** | r = −0.24; günde +1 saat ≈ −2.5 puan (kontrollü: −1.6) | 0.0002 (kontrollü: 0.009) | ≈ %99.99 (kontrollü: ≈ %99.6) |
| 3 | Kızlar erkeklerden daha başarılı | **TUTMUYOR** | Kızlar 1.9 puan *daha düşük* (anlamlı değil), d = −0.16 | 0.22 | ≈ %11 |
| 4 | Uykunun notla alakası yok | **TUTMUYOR (yanlış)** | r = +0.26; +1 saat uyku ≈ +3.3 puan (kontrollü: +2.2) | 0.00006 (kontrollü: 0.003) | "Alakası yok" olasılığı ≈ %0.4 (kontrollü ≈ %14) |

\* "İddia yönündeki olasılık": düz (bilgisiz) önsel altında, verinin ardından etkinin iddia edilen yönde olma olasılığı (P(β>0 | veri) ya da P(β<0 | veri)). İddia 4 için, "etki var / yok" eşit önsel olasılıkla başlatıldığında BIC tabanlı Bayes faktöründen hesaplanan "etki yok" olasılığı verildi. Ayrıntılar ve yorum uyarıları Bölüm 7'de.

Holm düzeltmesinden sonra (4 iddia birlikte test edildiği için) 1, 2 ve 4 anlamlı kalıyor (düzeltilmiş p sırasıyla 2·10⁻²³, 0.0003, 0.0002), 3 anlamlı değil (0.22).

---

## 2. Veri ve hazırlık

- Ayraç `;`, ondalık işareti `,` (Türkçe biçim) olarak okundu.
- Eksik değerler: sosyal medya 6 ("NA"), uyku 9 (boş hücre). Çalışma saati, not ve cinsiyette eksik yok. Her analizde eksik olanlar sadece o analizden çıkarıldı (complete-case). Çoklu regresyon n = 226.
- Not ortalaması 100'de tavan yapıyor: 11 öğrencinin notu tam 100 (tavan etkisi). Bu öğrenciler çıkarılınca da sonuçlar değişmiyor (Bölüm 6).
- Haftada 0 saat çalışan 1 öğrenci var. Geçerli bir değer olarak tutuldu.
- Tanımlayıcı: not ort. 79.7 (ss 12.2, aralık 38.7–100); haftalık çalışma 15.0 saat (ss 5.0); günlük sosyal medya 3.1 saat (ss 1.2); uyku 6.9 saat (ss 1.0).

**Kontrollü model** (tüm iddialar için ortak):
`not ~ çalışma + sosyal_medya + uyku + kız + özel_okul`, n = 226, R² = 0.44.

| Değişken | β | %95 GA | p | Standart β |
|---|---|---|---|---|
| Haftalık çalışma (saat) | +1.40 | [1.16, 1.64] | < 10⁻²³ | +0.58 |
| Günlük sosyal medya (saat) | −1.57 | [−2.75, −0.40] | 0.009 | −0.16 |
| Uyku (saat) | +2.23 | [0.77, 3.70] | 0.003 | +0.18 |
| Kız (erkeğe göre) | −1.17 | [−3.60, 1.26] | 0.34 | — |
| Özel okul (devlete göre) | +2.11 | [−0.33, 4.54] | 0.09 | — |

Artıklar normale yakın (Jarque-Bera p = 0.72). Heteroskedastisiteye dayanıklı (HC3) standart hatalarla da sonuçlar aynı.

---

## 3. İddia 1: "Haftada daha çok çalışan öğrencinin not ortalaması yüksek oluyor" → TUTUYOR

- Pearson r = **0.59** (%95 GA 0.50–0.67), Spearman ρ = 0.58. Verideki en güçlü ilişki bu.
- Haftalık çalışma 1 saat arttıkça not ortalaması ortalama **+1.43 puan** artıyor (diğer değişkenler sabitken +1.40).
- Çeyreklere göre ortalama not:

| Haftalık çalışma | n | Ortalama not |
|---|---|---|
| 0–11.8 saat (en az çalışan %25) | 60 | 69.5 |
| 11.8–15.0 saat | 61 | 78.3 |
| 15.0–18.5 saat | 61 | 83.7 |
| 18.5–26.4 saat (en çok çalışan %25) | 58 | 87.5 |

- Artış tekdüze. Karesel terim anlamsız (p = 0.17), yani verideki aralıkta belirgin bir "doyma" yok.
- **Olasılık:** İlişkinin pozitif olma olasılığı pratikte %100 (bootstrap'te 5000 örneğin hepsinde r > 0).
- **Uyarı:** Bu bir gözlemsel veri. "Çalışmak notu artırır" nedensel yorumu makul ama bu veriyle kanıtlanmış olmaz. Motivasyon gibi ölçülmemiş etkenler hem çalışmayı hem notu artırıyor olabilir.

---

## 4. İddia 2: "Sosyal medya notları düşürüyor" → TUTUYOR (ilişki olarak), nedensellik kanıtlanamaz

- Pearson r = **−0.24** (%95 GA −0.36 ile −0.12), Spearman ρ = −0.26, p = 0.0002.
- Günlük sosyal medya 1 saat arttıkça not ortalama **−2.5 puan** düşük.
- **Önemli ayrıntı:** Sosyal medya ile uyku arasında güçlü negatif ilişki var (r = −0.51). Çok sosyal medya kullanan daha az uyuyor. Uyku modele eklenince sosyal medyanın etkisi −2.5'ten **−1.6 puana** iniyor (p = 0.009). Yani sosyal medyanın nota "etkisinin" yaklaşık üçte biri uyku üzerinden ya da uykuyla ortak gidiyor. Kalan kısım bağımsız olarak da anlamlı.
- Sosyal medya ile çalışma saati arasında ilişki yok (r = 0.01). "Sosyal medya çalışma zamanını yiyor" açıklaması bu veride desteklenmiyor.
- **Olasılık:** İlişkinin negatif olma olasılığı ≈ %99.99 (kontrollü modelde ≈ %99.6). Bayes faktörüyle "bir etki var" olasılığı kontrolsüz modelde ≈ %99, kontrollü modelde ≈ %69 (BIC muhafazakâr bir yaklaşımdır).
- **Uyarı:** "Düşürüyor" nedensel bir ifade. Veri yalnızca "daha çok sosyal medya kullananların notu ortalamada daha düşük" diyor. Etki büyüklüğü de orta-zayıf: çalışma saatinin etkisinin yaklaşık dörtte biri (standart β −0.16'ya karşı +0.58).

---

## 5. İddia 3: "Kızlar erkeklerden daha başarılı" → TUTMUYOR

| | n | Ortalama | SS | Medyan |
|---|---|---|---|---|
| Kız | 119 | 78.7 | 13.3 | 80.5 |
| Erkek | 121 | 80.6 | 11.0 | 81.3 |

- Fark (kız − erkek) = **−1.9 puan** (%95 GA −5.0 ile +1.2). Welch t-testi p = 0.22, Mann-Whitney p = 0.32, Cohen d = −0.16 (çok küçük).
- Yani veride kızlar daha başarılı **değil**. Ortalamaları azıcık daha düşük, ama bu fark da istatistiksel olarak anlamlı değil. En doğru okuma: **cinsiyetler arasında anlamlı bir fark yok.**
- Okul türüne göre de durum aynı: devlette kız 77.9 / erkek 79.7, özelde kız 79.4 / erkek 81.7.
- Çalışma, sosyal medya, uyku ve okul türü kontrol edildiğinde de fark yok (β = −1.2, p = 0.34).
- Rastgele seçilen bir kızın rastgele seçilen bir erkekten yüksek not alma olasılığı %46 (yazı-tura düzeyinde).
- **Olasılık:** Kızların ortalamasının erkeklerinkinden yüksek olma olasılığı ≈ **%11** (bootstrap: %10.5). Bayes faktörü "fark yok" hipotezini yaklaşık 7'ye 1 destekliyor (kontrollü modelde yaklaşık 9.5'e 1). "Bir fark var" olasılığı ≈ %12 (kontrollüde ≈ %10).

---

## 6. İddia 4: "Uyku süresinin notla bir alakası yok" → TUTMUYOR (iddia yanlış)

- Pearson r = **+0.26** (%95 GA 0.14–0.38), Spearman ρ = 0.23, p = 0.00006.
- 1 saat fazla uyku ≈ **+3.3 puan** (diğer değişkenler sabitken +2.2, p = 0.003).

| Uyku | n | Ortalama not |
|---|---|---|
| ≤ 6 saat | 45 | 74.4 |
| 6–7 saat | 89 | 79.8 |
| 7–8 saat | 67 | 81.3 |
| > 8 saat | 30 | 82.9 |

- Eşdeğerlik testi (TOST, |r| < 0.1 "pratikte alakasız" sınırı) p = 0.99. Yani "alakası yok" iddiasını destekleyen hiçbir kanıt yok. Tersine, ilişkinin varlığı açık.
- Karesel terim anlamsız (p = 0.92), yani verideki aralıkta (4.2–9.5 saat) "fazla uyku zararlı" gibi ters-U bir desen görünmüyor.
- **Olasılık:** "Uyku ile not arasında ilişki yok" olasılığı (eşit önsel, BIC Bayes faktörü) ≈ **%0.4**. Sosyal medya, çalışma, cinsiyet ve okul kontrol edilince ≈ %14. İlişkinin pozitif olma olasılığı %99.9'un üzerinde.
- Not: Uykunun etkisinin bir kısmı sosyal medyayla örtüşüyor (r = −0.51). Ama sosyal medya sabit tutulduğunda da uyku anlamlı kalıyor.

---

## 7. Duyarlılık analizleri ve yöntem notları

- **Tavan etkisi:** Notu 100 olan 11 öğrenci çıkarıldığında (n = 215) sonuçlar aynı kalıyor: çalışma +1.31 (p < 10⁻²⁰), sosyal medya −1.32 (p = 0.03), uyku +2.14 (p = 0.004), kız −1.37 (p = 0.27).
- **Parametrik olmayan testler** (Spearman, Mann-Whitney) ve **bootstrap** (5000 / 10000 tekrar) parametrik sonuçlarla birebir uyumlu.
- **Olasılıkların anlamı:**
  - *p-değeri*, "iddianın doğru olma olasılığı" değildir. "Gerçekte hiç etki olmasaydı, bu kadar güçlü bir sonucu görme olasılığı" demektir.
  - Tabloda "iddia yönündeki olasılık" olarak verilen değerler, bilgisiz (düz) bir önsel altında hesaplanan Bayesçi sonsal olasılıklardır: P(etki iddia edilen yönde | veri).
  - "Etki var / yok" olasılıkları, iki hipoteze %50–%50 önsel verilerek BIC yaklaşımlı Bayes faktöründen hesaplandı. BIC küçük etkilere karşı muhafazakârdır, bu yüzden bu olasılıklar temkinli (alt sınıra yakın) okunmalıdır.
- **Nedensellik:** Bu veri kesitsel ve gözlemsel. Hiçbir sonuç tek başına "X, Y'yi artırır/düşürür" demeye yetmez. "X ile Y birlikte değişiyor" demek doğru olur. Özellikle İddia 2'deki "düşürüyor" ifadesi bu veriyle kanıtlanamaz, yalnızca ilişki gösterilebilir.
- **Genellenebilirlik:** Sonuçlar bu 240 öğrencilik örnekleme aittir. Örneklemin nasıl seçildiği bilinmiyor.
- **Varsayımlar:** "Not ortalaması" 0–100 ölçeğinde kabul edildi. "Kız = K, Erkek = E" olarak okundu. "Başarılı" not ortalamasının yüksekliği olarak tanımlandı.

## 8. Dosyalar

- `rapor.md`: bu rapor
- `sonuclar.json`: tüm test istatistikleri, güven aralıkları ve olasılıklar
- `analiz.py`: analizi yeniden üreten betik (`python3 analiz.py <çıktı_klasörü>`)
