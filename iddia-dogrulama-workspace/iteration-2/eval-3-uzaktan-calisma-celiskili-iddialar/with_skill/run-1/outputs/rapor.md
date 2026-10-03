# İddia Doğrulama Raporu — Uzaktan çalışma ve verimlilik — üç tarafın iddiası

**Araştırma sorusu:** Haftalık uzaktan çalışma gün sayısı çalışan verimliliğini artırıyor mu, düşürüyor mu, yoksa ilişki yok mu? Genel müdür, çalışanlar ve İK iddialarından hangisi kanıtla daha uyumlu?  
**Tarih:** 2026-10-03 · **Şema:** v1.0 · **İddia sayısı:** 6 · **Kanıt sayısı:** 11

> **Nasıl okunur:** *S* (−1…+1) kalite-ağırlıklı kanıtların iddiayı ne yönde ve ne güçte desteklediğini gösterir. *P* önsel olasılığın kanıtların olabilirlik oranlarıyla Bayesçi güncellenmesiyle elde edilen sonsal olasılıktır. *C* (0…1) kanıtların kendi aralarındaki uyumudur. *Sağlamlık*, 27 duyarlılık senaryosunun kaçında kararın değişmediğidir.

## 1. Özet

| ID | İddia | S | Spektrum | P | Karar | C | Kalite | Sağlamlık | Uyarı |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Uzaktan gün sayısı fazla olan çalışanların verimlilik puanı daha yüksektir (ham ilişki — çalışanların iddiasının ilişkisel hali) | 0.141 | Zayıf destek | 0.958 | Kabul — uygulanabilir | 0.199 | Düşük | 82% | 2 |
| C2 | Uzaktan gün sayısı fazla olan çalışanların verimlilik puanı daha düşüktür (ham ilişki — genel müdürün iddiasının ilişkisel hali) | -0.452 | Orta çelişki | 0.006 | Ret | 0.325 | Düşük | 100% | 2 |
| C3 | Uzaktan çalışma ile verimlilik arasında hiçbir ilişki yoktur (İK'nın iddiası, ham ilişki) | -0.454 | Orta çelişki | 0.006 | Ret | 0.326 | Düşük | 100% | 2 |
| C4 | Uzaktan çalışma verimliliği artırır (nedensel — çalışanların iddiası) | -0.375 | Orta çelişki | 0.087 | Ret | 0.259 | Çok düşük | 59% | 5 |
| C5 | Uzaktan çalışma verimliliği düşürür (nedensel — genel müdürün iddiası) | -0.365 | Orta çelişki | 0.109 | Büyük olasılıkla yanlış | 0.333 | Çok düşük | 30% | 5 |
| C6 | Uzaktan çalışmanın verimlilik üzerinde (diğer etkenler sabitken) etkisi yoktur (nedensel 'sıfır etki' — İK iddiasının nedensel hali) | -0.104 | Zayıf çelişki | 0.356 | Belirsiz — ek kanıt gerekli | 0.259 | Çok düşük | 33% | 5 |

### Spektrum görünümü

```
C1  −1 ──────────┼●───────── +1  S=+0.14  P=0.96
C2  −1 ─────●────┼────────── +1  S=-0.45  P=0.01
C3  −1 ─────●────┼────────── +1  S=-0.45  P=0.01
C4  −1 ──────●───┼────────── +1  S=-0.38  P=0.09
C5  −1 ──────●───┼────────── +1  S=-0.36  P=0.11
C6  −1 ─────────●┼────────── +1  S=-0.10  P=0.36
```

## 2. İddia ayrıntıları

### C1 — Uzaktan gün sayısı fazla olan çalışanların verimlilik puanı daha yüksektir (ham ilişki — çalışanların iddiasının ilişkisel hali)

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`positive` · nedensel=hayır · popülasyon: Bu şirketin çalışanları
- **Önsel P₀:** 0.35 — Üç yönlü rakip set (pozitif/negatif/yok). Literatür karışık: tam/hibrit uzaktan çalışma için hem pozitif hem negatif hem sıfır bulgular var. Hafif simetrik önsel: pozitif 0.35, negatif 0.30, yok 0.35 (toplam 1).
- **Toplam Bayes faktörü:** 41.898 (log₁₀ = 1.622) → **P = 0.958** (Kabul — uygulanabilir)
- **Spektrum:** S = 0.141 (Zayıf destek) · uyum C = 0.199 · destekleyen/çelişen/nötr = 4/5/0
- **Duyarlılık:** P aralığı [0.778, 0.997] · karar sağlamlığı 82% (27 senaryo)
- **Bilginin değeri:** alt banda (P<0.9) düşmek için LR ≈ 0.399

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | source | Bloom N., Liang J., Roberts J., Ying Z.J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.284 | 10.000 | 1.921 | 1.000 | 8% | unverified |
| S2 | source | Bloom N., Han R., Liang J. (2024). Hybrid working from home improves retention without damaging performance. Nature 630:920–925. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.529 | 0.100 | 0.296 | -1.000 | 16% | unverified |
| S3 | source | Atkin D., Schoar A., Shinde S. (2023). Working from Home, Worker Sorting and Development. NBER Working Paper 31515. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.227 | 0.100 | 0.593 | -1.000 | 7% | unverified |
| S4 | source | Emanuel N., Harrington E. (2024). Working Remotely? Selection, Treatment, and the Market for Remote Work. American Economic Journal: Applied Economics 16(4):528–559. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.236 | 0.250 | 0.721 | -0.602 | 4% | unverified |
| S5 | source | Gibbs M., Mengel F., Siemroth C. (2023). Work from Home and Productivity: Evidence from Personnel and Analytics Data on Information Technology Professionals. Journal of Political Economy Microeconomics 1(1):7–41. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.257 | 0.250 | 0.700 | -0.602 | 5% | unverified |
| S6 | source | Mang C.F., Anwar A. (2026). Does Working from Home Improve Employees' Productivity? Empirical Evidence from a Meta-Analysis. ILR Review. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.479 | 4.000 | 1.942 | 0.602 | 8% | unverified |
| S7 | source | Gajendran R.S., Ponnapalli A.R., Wang C., Javalagi A.A. (2024). A dual pathway model of remote work intensity: A meta-analysis of its simultaneous positive and negative effects. Personnel Psychology. | X–Y çifti | supports | meta_orgpsikoloji | 0.559 | 2.000 | 1.473 | 0.301 | 5% | unverified |
| S8 | source | Adı belirtilmemiş iş dergisi haberi (2023): 'Yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor.' (Benzer bir rakam Owl Labs'ın 2.050 ABD'li tam zamanlı çalışanla yaptığı anketinde geçiyor: yöneticilerin %60'ı uzaktan verimlilikten endişeli, çalışanların %62'si uzaktan daha verimli hissediyor.) | X–Y çifti | contradicts | algi_anketi | 0.028 | 0.500 | 0.981 | -0.301 | 0% | unverified |
| D1 | data | pearson: haftalik_uzaktan_gun → verimlilik_puani | X–Y çifti | istatistik | veri_sirket | 0.800 | 100.000 | 39.811 | 1.000 | 47% | ok |

**Kapsam dışı bırakılan kanıtlar:** D2 (ilişkisel iddia: aynı veri kümesinde ham analiz var); D3 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C2 — Uzaktan gün sayısı fazla olan çalışanların verimlilik puanı daha düşüktür (ham ilişki — genel müdürün iddiasının ilişkisel hali)

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`negative` · nedensel=hayır · popülasyon: Bu şirketin çalışanları
- **Önsel P₀:** 0.3 — Rakip setin negatif kolu; literatürde negatif bulgular var ama çoğu tam zamanlı uzaktan / belirli iş türleri için. 0.30.
- **Toplam Bayes faktörü:** 0.014 (log₁₀ = -1.853) → **P = 0.006** (Ret)
- **Spektrum:** S = -0.452 (Orta çelişki) · uyum C = 0.325 · destekleyen/çelişen/nötr = 4/5/0
- **Duyarlılık:** P aralığı [0.001, 0.098] · karar sağlamlığı 100% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 18.501

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | source | Bloom N., Liang J., Roberts J., Ying Z.J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.284 | 0.100 | 0.521 | -1.000 | 8% | unverified |
| S2 | source | Bloom N., Han R., Liang J. (2024). Hybrid working from home improves retention without damaging performance. Nature 630:920–925. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.529 | 0.100 | 0.296 | -1.000 | 16% | unverified |
| S3 | source | Atkin D., Schoar A., Shinde S. (2023). Working from Home, Worker Sorting and Development. NBER Working Paper 31515. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.227 | 10.000 | 1.686 | 1.000 | 7% | unverified |
| S4 | source | Emanuel N., Harrington E. (2024). Working Remotely? Selection, Treatment, and the Market for Remote Work. American Economic Journal: Applied Economics 16(4):528–559. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.236 | 4.000 | 1.388 | 0.602 | 4% | unverified |
| S5 | source | Gibbs M., Mengel F., Siemroth C. (2023). Work from Home and Productivity: Evidence from Personnel and Analytics Data on Information Technology Professionals. Journal of Political Economy Microeconomics 1(1):7–41. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.257 | 4.000 | 1.428 | 0.602 | 5% | unverified |
| S6 | source | Mang C.F., Anwar A. (2026). Does Working from Home Improve Employees' Productivity? Empirical Evidence from a Meta-Analysis. ILR Review. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.479 | 0.250 | 0.515 | -0.602 | 9% | unverified |
| S7 | source | Gajendran R.S., Ponnapalli A.R., Wang C., Javalagi A.A. (2024). A dual pathway model of remote work intensity: A meta-analysis of its simultaneous positive and negative effects. Personnel Psychology. | X–Y çifti | contradicts | meta_orgpsikoloji | 0.559 | 0.500 | 0.679 | -0.301 | 5% | unverified |
| S8 | source | Adı belirtilmemiş iş dergisi haberi (2023): 'Yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor.' (Benzer bir rakam Owl Labs'ın 2.050 ABD'li tam zamanlı çalışanla yaptığı anketinde geçiyor: yöneticilerin %60'ı uzaktan verimlilikten endişeli, çalışanların %62'si uzaktan daha verimli hissediyor.) | X–Y çifti | supports | algi_anketi | 0.028 | 2.000 | 1.020 | 0.301 | 0% | unverified |
| D1 | data | pearson: haftalik_uzaktan_gun → verimlilik_puani | X–Y çifti | istatistik | veri_sirket | 0.800 | 0.012 | 0.030 | -1.000 | 46% | ok |

**Kapsam dışı bırakılan kanıtlar:** D2 (ilişkisel iddia: aynı veri kümesinde ham analiz var); D3 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C3 — Uzaktan çalışma ile verimlilik arasında hiçbir ilişki yoktur (İK'nın iddiası, ham ilişki)

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`none` · nedensel=hayır · popülasyon: Bu şirketin çalışanları
- **Önsel P₀:** 0.35 — Rakip setin 'ilişki yok' kolu; hibrit düzenlerde etkinin sıfıra yakın olduğunu gösteren çalışmalar var. 0.35.
- **Toplam Bayes faktörü:** 0.012 (log₁₀ = -1.938) → **P = 0.006** (Ret)
- **Spektrum:** S = -0.454 (Orta çelişki) · uyum C = 0.326 · destekleyen/çelişen/nötr = 1/8/0
- **Duyarlılık:** P aralığı [0.001, 0.085] · karar sağlamlığı 100% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 17.908

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | source | Bloom N., Liang J., Roberts J., Ying Z.J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.284 | 0.100 | 0.521 | -1.000 | 8% | unverified |
| S2 | source | Bloom N., Han R., Liang J. (2024). Hybrid working from home improves retention without damaging performance. Nature 630:920–925. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.529 | 10.000 | 3.382 | 1.000 | 16% | unverified |
| S3 | source | Atkin D., Schoar A., Shinde S. (2023). Working from Home, Worker Sorting and Development. NBER Working Paper 31515. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.227 | 0.100 | 0.593 | -1.000 | 7% | unverified |
| S4 | source | Emanuel N., Harrington E. (2024). Working Remotely? Selection, Treatment, and the Market for Remote Work. American Economic Journal: Applied Economics 16(4):528–559. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.236 | 0.250 | 0.721 | -0.602 | 4% | unverified |
| S5 | source | Gibbs M., Mengel F., Siemroth C. (2023). Work from Home and Productivity: Evidence from Personnel and Analytics Data on Information Technology Professionals. Journal of Political Economy Microeconomics 1(1):7–41. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.257 | 0.250 | 0.700 | -0.602 | 5% | unverified |
| S6 | source | Mang C.F., Anwar A. (2026). Does Working from Home Improve Employees' Productivity? Empirical Evidence from a Meta-Analysis. ILR Review. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.479 | 0.250 | 0.515 | -0.602 | 8% | unverified |
| S7 | source | Gajendran R.S., Ponnapalli A.R., Wang C., Javalagi A.A. (2024). A dual pathway model of remote work intensity: A meta-analysis of its simultaneous positive and negative effects. Personnel Psychology. | X–Y çifti | contradicts | meta_orgpsikoloji | 0.559 | 0.500 | 0.679 | -0.301 | 5% | unverified |
| S8 | source | Adı belirtilmemiş iş dergisi haberi (2023): 'Yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor.' (Benzer bir rakam Owl Labs'ın 2.050 ABD'li tam zamanlı çalışanla yaptığı anketinde geçiyor: yöneticilerin %60'ı uzaktan verimlilikten endişeli, çalışanların %62'si uzaktan daha verimli hissediyor.) | X–Y çifti | contradicts | algi_anketi | 0.028 | 0.500 | 0.981 | -0.301 | 0% | unverified |
| D1 | data | pearson: haftalik_uzaktan_gun → verimlilik_puani | X–Y çifti | istatistik | veri_sirket | 0.800 | 0.010 | 0.025 | -1.000 | 47% | ok |

**Kapsam dışı bırakılan kanıtlar:** D2 (ilişkisel iddia: aynı veri kümesinde ham analiz var); D3 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C4 — Uzaktan çalışma verimliliği artırır (nedensel — çalışanların iddiası)

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`positive` · nedensel=evet · popülasyon: Bu şirketin çalışanları
- **Önsel P₀:** 0.35 — Nedensel rakip set; ham set ile aynı simetrik önsel (0.35/0.30/0.35), çünkü nedensel yön hakkında önceden ayrı bilgi yok.
- **Toplam Bayes faktörü:** 0.177 (log₁₀ = -0.751) → **P = 0.087** (Ret)
- **Spektrum:** S = -0.375 (Orta çelişki) · uyum C = 0.259 · destekleyen/çelişen/nötr = 3/6/0
- **Duyarlılık:** P aralığı [0.013, 0.451] · karar sağlamlığı 59% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 1.163

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | source | Bloom N., Liang J., Roberts J., Ying Z.J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.284 | 10.000 | 1.921 | 1.000 | 13% | unverified |
| S2 | source | Bloom N., Han R., Liang J. (2024). Hybrid working from home improves retention without damaging performance. Nature 630:920–925. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.529 | 0.100 | 0.296 | -1.000 | 24% | unverified |
| S3 | source | Atkin D., Schoar A., Shinde S. (2023). Working from Home, Worker Sorting and Development. NBER Working Paper 31515. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.227 | 0.100 | 0.593 | -1.000 | 10% | unverified |
| S4 | source | Emanuel N., Harrington E. (2024). Working Remotely? Selection, Treatment, and the Market for Remote Work. American Economic Journal: Applied Economics 16(4):528–559. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.236 | 0.250 | 0.721 | -0.602 | 6% | unverified |
| S5 | source | Gibbs M., Mengel F., Siemroth C. (2023). Work from Home and Productivity: Evidence from Personnel and Analytics Data on Information Technology Professionals. Journal of Political Economy Microeconomics 1(1):7–41. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.154 | 0.250 | 0.807 | -0.602 | 4% | unverified |
| S6 | source | Mang C.F., Anwar A. (2026). Does Working from Home Improve Employees' Productivity? Empirical Evidence from a Meta-Analysis. ILR Review. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.287 | 3.000 | 1.371 | 0.477 | 6% | unverified |
| S7 | source | Gajendran R.S., Ponnapalli A.R., Wang C., Javalagi A.A. (2024). A dual pathway model of remote work intensity: A meta-analysis of its simultaneous positive and negative effects. Personnel Psychology. | X–Y çifti | supports | meta_orgpsikoloji | 0.335 | 2.000 | 1.262 | 0.301 | 5% | unverified |
| S8 | source | Adı belirtilmemiş iş dergisi haberi (2023): 'Yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor.' (Benzer bir rakam Owl Labs'ın 2.050 ABD'li tam zamanlı çalışanla yaptığı anketinde geçiyor: yöneticilerin %60'ı uzaktan verimlilikten endişeli, çalışanların %62'si uzaktan daha verimli hissediyor.) | X–Y çifti | contradicts | algi_anketi | 0.017 | 0.500 | 0.988 | -0.301 | 0% | unverified |
| D2 | data | regression: haftalik_uzaktan_gun → verimlilik_puani; kontroller: kidem_yil, departman | X–Y çifti | istatistik | veri_sirket | 0.480 | 0.038 | 0.207 | -1.000 | 31% | causal_gap |

**Kapsam dışı bırakılan kanıtlar:** D1 (nedensel iddia: aynı veri kümesinde daha kontrollü analiz var); D3 (nedensel iddia: aynı veri kümesinde daha kontrollü analiz var)

**Uyarılar:**
- `causal_cap_applied` — Gözlemsel kanıtın nedensel iddiaya desteği tavanla sınırlandı (korelasyon ≠ nedensellik).
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).
- `hypothesis_set_incoherent` — Bu iddianın ait olduğu rakip hipotez setinde olasılıklar toplamı 1'den belirgin sapıyor.

### C5 — Uzaktan çalışma verimliliği düşürür (nedensel — genel müdürün iddiası)

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`negative` · nedensel=evet · popülasyon: Bu şirketin çalışanları
- **Önsel P₀:** 0.3 — Nedensel rakip setin negatif kolu. 0.30.
- **Toplam Bayes faktörü:** 0.287 (log₁₀ = -0.542) → **P = 0.109** (Büyük olasılıkla yanlış)
- **Spektrum:** S = -0.365 (Orta çelişki) · uyum C = 0.333 · destekleyen/çelişen/nötr = 4/5/0
- **Duyarlılık:** P aralığı [0.025, 0.546] · karar sağlamlığı 30% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.3) geçmek için LR ≈ 3.487; alt banda (P<0.1) düşmek için LR ≈ 0.904

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | source | Bloom N., Liang J., Roberts J., Ying Z.J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.284 | 0.100 | 0.521 | -1.000 | 16% | unverified |
| S2 | source | Bloom N., Han R., Liang J. (2024). Hybrid working from home improves retention without damaging performance. Nature 630:920–925. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.529 | 0.100 | 0.296 | -1.000 | 29% | unverified |
| S3 | source | Atkin D., Schoar A., Shinde S. (2023). Working from Home, Worker Sorting and Development. NBER Working Paper 31515. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.227 | 10.000 | 1.686 | 1.000 | 12% | unverified |
| S4 | source | Emanuel N., Harrington E. (2024). Working Remotely? Selection, Treatment, and the Market for Remote Work. American Economic Journal: Applied Economics 16(4):528–559. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.236 | 4.000 | 1.388 | 0.602 | 8% | unverified |
| S5 | source | Gibbs M., Mengel F., Siemroth C. (2023). Work from Home and Productivity: Evidence from Personnel and Analytics Data on Information Technology Professionals. Journal of Political Economy Microeconomics 1(1):7–41. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.154 | 3.000 | 1.185 | 0.477 | 4% | unverified |
| S6 | source | Mang C.F., Anwar A. (2026). Does Working from Home Improve Employees' Productivity? Empirical Evidence from a Meta-Analysis. ILR Review. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.287 | 0.250 | 0.671 | -0.602 | 10% | unverified |
| S7 | source | Gajendran R.S., Ponnapalli A.R., Wang C., Javalagi A.A. (2024). A dual pathway model of remote work intensity: A meta-analysis of its simultaneous positive and negative effects. Personnel Psychology. | X–Y çifti | contradicts | meta_orgpsikoloji | 0.335 | 0.500 | 0.793 | -0.301 | 6% | unverified |
| S8 | source | Adı belirtilmemiş iş dergisi haberi (2023): 'Yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor.' (Benzer bir rakam Owl Labs'ın 2.050 ABD'li tam zamanlı çalışanla yaptığı anketinde geçiyor: yöneticilerin %60'ı uzaktan verimlilikten endişeli, çalışanların %62'si uzaktan daha verimli hissediyor.) | X–Y çifti | supports | algi_anketi | 0.017 | 2.000 | 1.012 | 0.301 | 0% | unverified |
| D2 | data | regression: haftalik_uzaktan_gun → verimlilik_puani; kontroller: kidem_yil, departman | X–Y çifti | istatistik | veri_sirket | 0.480 | 0.247 | 0.511 | -0.607 | 16% | causal_gap |

**Kapsam dışı bırakılan kanıtlar:** D1 (nedensel iddia: aynı veri kümesinde daha kontrollü analiz var); D3 (nedensel iddia: aynı veri kümesinde daha kontrollü analiz var)

**Uyarılar:**
- `causal_cap_applied` — Gözlemsel kanıtın nedensel iddiaya desteği tavanla sınırlandı (korelasyon ≠ nedensellik).
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).
- `hypothesis_set_incoherent` — Bu iddianın ait olduğu rakip hipotez setinde olasılıklar toplamı 1'den belirgin sapıyor.

### C6 — Uzaktan çalışmanın verimlilik üzerinde (diğer etkenler sabitken) etkisi yoktur (nedensel 'sıfır etki' — İK iddiasının nedensel hali)

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`none` · nedensel=evet · popülasyon: Bu şirketin çalışanları
- **Önsel P₀:** 0.35 — Nedensel rakip setin 'etki yok' kolu. 0.35.
- **Toplam Bayes faktörü:** 1.028 (log₁₀ = 0.012) → **P = 0.356** (Belirsiz — ek kanıt gerekli)
- **Spektrum:** S = -0.104 (Zayıf çelişki) · uyum C = 0.259 · destekleyen/çelişen/nötr = 2/7/0
- **Duyarlılık:** P aralığı [0.138, 0.773] · karar sağlamlığı 33% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.7) geçmek için LR ≈ 4.217; alt banda (P<0.3) düşmek için LR ≈ 0.774

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | source | Bloom N., Liang J., Roberts J., Ying Z.J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.284 | 0.100 | 0.521 | -1.000 | 16% | unverified |
| S2 | source | Bloom N., Han R., Liang J. (2024). Hybrid working from home improves retention without damaging performance. Nature 630:920–925. | X–Y çifti | supports | ekonomi_literaturu_wfh | 0.529 | 10.000 | 3.382 | 1.000 | 30% | unverified |
| S3 | source | Atkin D., Schoar A., Shinde S. (2023). Working from Home, Worker Sorting and Development. NBER Working Paper 31515. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.227 | 0.100 | 0.593 | -1.000 | 13% | unverified |
| S4 | source | Emanuel N., Harrington E. (2024). Working Remotely? Selection, Treatment, and the Market for Remote Work. American Economic Journal: Applied Economics 16(4):528–559. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.236 | 0.250 | 0.721 | -0.602 | 8% | unverified |
| S5 | source | Gibbs M., Mengel F., Siemroth C. (2023). Work from Home and Productivity: Evidence from Personnel and Analytics Data on Information Technology Professionals. Journal of Political Economy Microeconomics 1(1):7–41. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.154 | 0.250 | 0.807 | -0.602 | 5% | unverified |
| S6 | source | Mang C.F., Anwar A. (2026). Does Working from Home Improve Employees' Productivity? Empirical Evidence from a Meta-Analysis. ILR Review. | X–Y çifti | contradicts | ekonomi_literaturu_wfh | 0.287 | 0.250 | 0.671 | -0.602 | 10% | unverified |
| S7 | source | Gajendran R.S., Ponnapalli A.R., Wang C., Javalagi A.A. (2024). A dual pathway model of remote work intensity: A meta-analysis of its simultaneous positive and negative effects. Personnel Psychology. | X–Y çifti | contradicts | meta_orgpsikoloji | 0.335 | 0.500 | 0.793 | -0.301 | 6% | unverified |
| S8 | source | Adı belirtilmemiş iş dergisi haberi (2023): 'Yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor.' (Benzer bir rakam Owl Labs'ın 2.050 ABD'li tam zamanlı çalışanla yaptığı anketinde geçiyor: yöneticilerin %60'ı uzaktan verimlilikten endişeli, çalışanların %62'si uzaktan daha verimli hissediyor.) | X–Y çifti | contradicts | algi_anketi | 0.017 | 0.500 | 0.988 | -0.301 | 0% | unverified |
| D2 | data | regression: haftalik_uzaktan_gun → verimlilik_puani; kontroller: kidem_yil, departman | X–Y çifti | istatistik | veri_sirket | 0.480 | 3.000 | 1.694 | 0.477 | 13% | causal_gap |

**Kapsam dışı bırakılan kanıtlar:** D1 (nedensel iddia: aynı veri kümesinde daha kontrollü analiz var); D3 (nedensel iddia: aynı veri kümesinde daha kontrollü analiz var)

**Uyarılar:**
- `causal_cap_applied` — Gözlemsel kanıtın nedensel iddiaya desteği tavanla sınırlandı (korelasyon ≠ nedensellik).
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).
- `hypothesis_set_incoherent` — Bu iddianın ait olduğu rakip hipotez setinde olasılıklar toplamı 1'den belirgin sapıyor.

## 3. İddialar arası uyum

| İddialar | İlişkiler | Mantıksal uyum | P değerleri | Tutarsızlık | Not |
|---|---|---|---|---|---|
| C1 ↔ C2 | positive / negative | −1 çelişik | 0.958 / 0.006 | 0.000 |  |
| C1 ↔ C3 | positive / none | −1 çelişik | 0.958 / 0.006 | 0.000 |  |
| C1 ↔ C4 | positive / positive | 0 kısmi | 0.958 / 0.087 | — | Farklı kapsam (ilişkisel · Bu şirketin çalışanları / nedensel · Bu şirketin çalışanları): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C1 ↔ C5 | positive / negative | 0 kısmi | 0.958 / 0.109 | — | Farklı kapsam (ilişkisel · Bu şirketin çalışanları / nedensel · Bu şirketin çalışanları): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C1 ↔ C6 | positive / none | 0 kısmi | 0.958 / 0.356 | — | Farklı kapsam (ilişkisel · Bu şirketin çalışanları / nedensel · Bu şirketin çalışanları): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C2 ↔ C3 | negative / none | −1 çelişik | 0.006 / 0.006 | 0.000 |  |
| C2 ↔ C4 | negative / positive | 0 kısmi | 0.006 / 0.087 | — | Farklı kapsam (ilişkisel · Bu şirketin çalışanları / nedensel · Bu şirketin çalışanları): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C2 ↔ C5 | negative / negative | 0 kısmi | 0.006 / 0.109 | — | Farklı kapsam (ilişkisel · Bu şirketin çalışanları / nedensel · Bu şirketin çalışanları): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C2 ↔ C6 | negative / none | 0 kısmi | 0.006 / 0.356 | — | Farklı kapsam (ilişkisel · Bu şirketin çalışanları / nedensel · Bu şirketin çalışanları): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C3 ↔ C4 | none / positive | 0 kısmi | 0.006 / 0.087 | — | Farklı kapsam (ilişkisel · Bu şirketin çalışanları / nedensel · Bu şirketin çalışanları): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C3 ↔ C5 | none / negative | 0 kısmi | 0.006 / 0.109 | — | Farklı kapsam (ilişkisel · Bu şirketin çalışanları / nedensel · Bu şirketin çalışanları): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C3 ↔ C6 | none / none | 0 kısmi | 0.006 / 0.356 | — | Farklı kapsam (ilişkisel · Bu şirketin çalışanları / nedensel · Bu şirketin çalışanları): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C4 ↔ C5 | positive / negative | −1 çelişik | 0.087 / 0.109 | 0.000 |  |
| C4 ↔ C6 | positive / none | −1 çelişik | 0.087 / 0.356 | 0.000 |  |
| C5 ↔ C6 | negative / none | −1 çelişik | 0.109 / 0.356 | 0.000 |  |

### Rakip hipotez setleri

Aynı kapsamda birbirini dışlayan iddialar. Kapsayıcı setlerde ΣP ≈ 1 olmalıdır; *normalize P* tutarlı olasılık dağılımıdır.

| Değişkenler | Kapsam | Hipotezler | P | ΣP | Normalize P | En olası | Açık |
|---|---|---|---|---|---|---|---|
| haftalik_uzaktan_gun – verimlilik_puani | ilişkisel · Bu şirketin çalışanları | C1:positive, C2:negative, C3:none | 0.958 / 0.006 / 0.006 | 0.970 | 0.988 / 0.006 / 0.006 | C1 | 0.030 |
| haftalik_uzaktan_gun – verimlilik_puani | nedensel · Bu şirketin çalışanları | C4:positive, C5:negative, C6:none | 0.087 / 0.109 / 0.356 | 0.552 | 0.158 / 0.197 / 0.645 | C6 | 0.448 ⚠ |
- C4 / C5 / C6: ΣP < 1: kanıtlar rakip hipotezleri iyi ayırt edemiyor; normalize paylara bakın.

## 4. Değişken özeti

| Değişken | İddialar | Ort. S | Ort. P |
|---|---|---|---|
| `haftalik_uzaktan_gun` | C1, C2, C3, C4, C5, C6 | -0.268 | 0.254 |
| `verimlilik_puani` | C1, C2, C3, C4, C5, C6 | -0.268 | 0.254 |

## 5. Yöntem

- Kanıt kalitesi **Q** ∈ [0,1]: tasarım taban puanı × düzelticiler (n, hakem, çıkar çatışması, replikasyon, yaş, doğrulama, nedensellik açığı). Her çarpan `metadata.json` içindeki `quality_trace`'te.
- Ham olabilirlik oranı: veri/raporlanan istatistik için BIC yaklaşımlı Bayes faktörü BF₁₀ = (1−r²)^(−n/2)/√n, yönlü iddiada işarete göre çevrilir; kaynak tutumu için güçlü=10, orta=4, zayıf=2. Tek kanıt |log₁₀ LR| ≤ 2.0 ile sınırlanır.
- Etkin LR = LR_ham^Q. Aynı kümedeki k kanıt ortalanıp k_eff = k/(1+(k−1)ρ) ile ölçeklenir (ρ = 0.5).
- P = σ(logit P₀ + Σ ln LR_küme). S = Σ Q·d / Σ Q, d = kırpılmış log₁₀ LR_ham ∈ [−1,1]. C = 1 − ağırlıklı standart sapma(d).
- Kapsam: değişken çifti kanıtı iddianın kapsamına göre seçilir — `controls` belirten iddia yalnızca aynı kontrollerle yapılmış analizi; ilişkisel iddia aynı veri kümesindeki ham analizi; nedensel iddia en kontrollü analizi kullanır. Gözlemsel kanıtın nedensel iddiaya desteği LR ≤ 3 ile sınırlanır.
- Karar bantları: P≥0.9 kabul · 0.7–0.9 koşullu · 0.3–0.7 belirsiz · 0.1–0.3 büyük olasılıkla yanlış · <0.1 ret.

## 6. Yorum ve Uygulama

<!-- YORUM_UYGULAMA: Bu bölüm SKILL.md Adım 7'ye göre doldurulur. -->
