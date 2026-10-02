# İddia Doğrulama Raporu — Uzaktan çalışma ve verimlilik — üç tarafın çelişkili iddiaları

**Araştırma sorusu:** Bu şirkette haftalık uzaktan çalışma gün sayısı ile verimlilik puanı arasındaki ilişki nedir; Genel Müdür (düşürür), Çalışanlar (artırır) ve İK (ilişki yok) iddialarından hangisi kanıtlarla en uyumlu?  
**Tarih:** 2026-10-02 · **Şema:** v1.0 · **İddia sayısı:** 6 · **Kanıt sayısı:** 9

> **Nasıl okunur:** *S* (−1…+1) kalite-ağırlıklı kanıtların iddiayı ne yönde ve ne güçte desteklediğini gösterir. *P* önsel olasılığın kanıtların olabilirlik oranlarıyla Bayesçi güncellenmesiyle elde edilen sonsal olasılıktır. *C* (0…1) kanıtların kendi aralarındaki uyumudur. *Sağlamlık*, 27 duyarlılık senaryosunun kaçında kararın değişmediğidir.

## 1. Özet

| ID | İddia | S | Spektrum | P | Karar | C | Kalite | Sağlamlık | Uyarı |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Genel Müdür: Uzaktan çalışma verimliliği (nedensel olarak) düşürür | -0.186 | Zayıf çelişki | 0.139 | Büyük olasılıkla yanlış | 0.429 | Düşük | 44% | 3 |
| C2 | Çalışanlar: Uzaktan çalışma verimliliği (nedensel olarak) artırır | -0.256 | Zayıf çelişki | 0.032 | Ret | 0.385 | Düşük | 67% | 3 |
| C3 | İK: Uzaktan çalışma ile verimlilik arasında hiçbir ilişki yoktur | -1.000 | Güçlü çelişki | 0.011 | Ret | — | Yüksek | 89% | 1 |
| C4 | (GM iddiasının ilişkisel hâli) Daha çok uzaktan çalışan çalışanların verimlilik puanı daha düşüktür | -1.000 | Güçlü çelişki | 0.016 | Ret | — | Yüksek | 89% | 1 |
| C5 | (Çalışanların iddiasının ilişkisel hâli) Daha çok uzaktan çalışan çalışanların verimlilik puanı daha yüksektir | 1.000 | Güçlü destek | 0.955 | Kabul — uygulanabilir | — | Yüksek | 89% | 1 |
| C6 | (İK iddiasının 'diğer koşullar sabitken' yorumu) Kıdem ve departman sabitken uzaktan gün sayısı ile verimlilik arasında ilişki yoktur | -0.122 | Zayıf çelişki | 0.111 | Büyük olasılıkla yanlış | 0.358 | Orta | 33% | 3 |

### Spektrum görünümü

```
C1  −1 ────────●─┼────────── +1  S=-0.19  P=0.14
C2  −1 ───────●──┼────────── +1  S=-0.26  P=0.03
C3  −1 ●─────────┼────────── +1  S=-1.00  P=0.01
C4  −1 ●─────────┼────────── +1  S=-1.00  P=0.02
C5  −1 ──────────┼─────────● +1  S=+1.00  P=0.95
C6  −1 ─────────●┼────────── +1  S=-0.12  P=0.11
```

## 2. İddia ayrıntıları

### C1 — Genel Müdür: Uzaktan çalışma verimliliği (nedensel olarak) düşürür

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`negative` · nedensel=evet · popülasyon: Şirket çalışanları (n=180)
- **Önsel P₀:** 0.3 — Literatür bağlama göre karışık (bazı deneylerde artış, bazılarında düşüş); nedensel iddia ilişkisel versiyondan (0.35) daha güçlü olduğu için biraz daha düşük önsel.
- **Toplam Bayes faktörü:** 0.377 (log₁₀ = -0.424) → **P = 0.139** (Büyük olasılıkla yanlış)
- **Spektrum:** S = -0.186 (Zayıf çelişki) · uyum C = 0.429 · destekleyen/çelişen/nötr = 4/4/0
- **Duyarlılık:** P aralığı [0.049, 0.616] · karar sağlamlığı 44% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.3) geçmek için LR ≈ 2.652; alt banda (P<0.1) düşmek için LR ≈ 0.688

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D2 | data | regression: haftalik_uzaktan_gun → verimlilik_puani; kontroller: kidem_yil, departman | doğrudan | istatistik | sirket_verisi | 0.480 | 0.247 | 0.511 | -0.607 | 13% | causal_gap |
| S1 | source | Bloom, N., Liang, J., Roberts, J., Ying, Z. J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | doğrudan | contradicts | bloom_liang_ekibi | 0.567 | 0.250 | 0.456 | -0.602 | 16% | unverified |
| S2 | source | İş dergisi haberi (2023): yöneticilere yapılan ankete göre yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor. (Yayın adı/URL kullanıcı tarafından verilmedi.) | doğrudan | supports | yonetici_anketi_haberi | 0.034 | 2.000 | 1.024 | 0.301 | 0% | unverified |
| S3 | source | Bloom, N., Han, R., Liang, J. (2024). Hybrid working from home improves retention without damaging performance. Nature 630:920–925. | doğrudan | contradicts | bloom_liang_ekibi | 0.695 | 0.250 | 0.382 | -0.602 | 19% | unverified |
| S4 | source | Atkin, D., Schoar, A., Shinde, S. (2023). Working from Home, Worker Sorting and Development. NBER Working Paper 31515. | doğrudan | supports | atkin_schoar_shinde | 0.454 | 4.000 | 1.875 | 0.602 | 12% | unverified |
| S5 | source | Emanuel, N., Harrington, E. (2024). Working Remotely? Selection, Treatment, and the Market for Remote Work. American Economic Journal: Applied Economics 16(4):528–559. | doğrudan | supports | emanuel_harrington | 0.472 | 4.000 | 1.925 | 0.602 | 13% | unverified |
| S6 | source | Gibbs, M., Mengel, F., Siemroth, C. (2023). Work from Home and Productivity: Evidence from Personnel and Analytics Data on Information Technology Professionals. Journal of Political Economy Microeconomics 1(1):7–41. | doğrudan | supports | gibbs_mengel_siemroth | 0.309 | 4.000 | 1.534 | 0.602 | 8% | unverified |
| S7 | source | Angelici, M., Profeta, P. (2024). Smart Working: Work Flexibility Without Constraints. Management Science 70(3):1680–1705. | doğrudan | contradicts | angelici_profeta | 0.630 | 0.250 | 0.418 | -0.602 | 17% | unverified |

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C2 — Çalışanlar: Uzaktan çalışma verimliliği (nedensel olarak) artırır

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`positive` · nedensel=evet · popülasyon: Şirket çalışanları (n=180)
- **Önsel P₀:** 0.3 — C1 ile simetrik: tartışmalı alan, nedensel iddia → 0.30.
- **Toplam Bayes faktörü:** 0.078 (log₁₀ = -1.109) → **P = 0.032** (Ret)
- **Spektrum:** S = -0.256 (Zayıf çelişki) · uyum C = 0.385 · destekleyen/çelişen/nötr = 2/6/0
- **Duyarlılık:** P aralığı [0.014, 0.283] · karar sağlamlığı 67% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 3.335

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D2 | data | regression: haftalik_uzaktan_gun → verimlilik_puani; kontroller: kidem_yil, departman | doğrudan | istatistik | sirket_verisi | 0.480 | 0.038 | 0.207 | -1.000 | 26% | causal_gap |
| S1 | source | Bloom, N., Liang, J., Roberts, J., Ying, Z. J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | doğrudan | supports | bloom_liang_ekibi | 0.567 | 4.000 | 2.195 | 0.602 | 13% | unverified |
| S2 | source | İş dergisi haberi (2023): yöneticilere yapılan ankete göre yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor. (Yayın adı/URL kullanıcı tarafından verilmedi.) | doğrudan | contradicts | yonetici_anketi_haberi | 0.034 | 0.500 | 0.977 | -0.301 | 0% | unverified |
| S3 | source | Bloom, N., Han, R., Liang, J. (2024). Hybrid working from home improves retention without damaging performance. Nature 630:920–925. | doğrudan | contradicts | bloom_liang_ekibi | 0.695 | 0.250 | 0.382 | -0.602 | 16% | unverified |
| S4 | source | Atkin, D., Schoar, A., Shinde, S. (2023). Working from Home, Worker Sorting and Development. NBER Working Paper 31515. | doğrudan | contradicts | atkin_schoar_shinde | 0.454 | 0.250 | 0.533 | -0.602 | 11% | unverified |
| S5 | source | Emanuel, N., Harrington, E. (2024). Working Remotely? Selection, Treatment, and the Market for Remote Work. American Economic Journal: Applied Economics 16(4):528–559. | doğrudan | contradicts | emanuel_harrington | 0.472 | 0.250 | 0.519 | -0.602 | 11% | unverified |
| S6 | source | Gibbs, M., Mengel, F., Siemroth, C. (2023). Work from Home and Productivity: Evidence from Personnel and Analytics Data on Information Technology Professionals. Journal of Political Economy Microeconomics 1(1):7–41. | doğrudan | contradicts | gibbs_mengel_siemroth | 0.309 | 0.250 | 0.652 | -0.602 | 7% | unverified |
| S7 | source | Angelici, M., Profeta, P. (2024). Smart Working: Work Flexibility Without Constraints. Management Science 70(3):1680–1705. | doğrudan | supports | angelici_profeta | 0.630 | 4.000 | 2.395 | 0.602 | 15% | unverified |

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C3 — İK: Uzaktan çalışma ile verimlilik arasında hiçbir ilişki yoktur

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`none` · nedensel=hayır · popülasyon: Şirket çalışanları (n=180)
- **Önsel P₀:** 0.3 — Birbirini dışlayan üç ilişkisel durumdan biri (negatif 0.35 / pozitif 0.35 / yok 0.30); 'hiçbir ilişki' nokta iddiası olduğu için yönlü durumlardan biraz düşük.
- **Toplam Bayes faktörü:** 0.025 (log₁₀ = -1.600) → **P = 0.011** (Ret)
- **Spektrum:** S = -1.000 (Güçlü çelişki) · uyum C = — · destekleyen/çelişen/nötr = 0/1/0
- **Duyarlılık:** P aralığı [0.004, 0.136] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 10.321

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | data | pearson: haftalik_uzaktan_gun → verimlilik_puani | doğrudan | istatistik | sirket_verisi | 0.800 | 0.010 | 0.025 | -1.000 | 100% | ok |

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.

### C4 — (GM iddiasının ilişkisel hâli) Daha çok uzaktan çalışan çalışanların verimlilik puanı daha düşüktür

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`negative` · nedensel=hayır · popülasyon: Şirket çalışanları (n=180)
- **Önsel P₀:** 0.35 — Tarafsız başlangıç; üç ilişkisel durumun toplamı 1 olacak şekilde.
- **Toplam Bayes faktörü:** 0.030 (log₁₀ = -1.529) → **P = 0.016** (Ret)
- **Spektrum:** S = -1.000 (Güçlü çelişki) · uyum C = — · destekleyen/çelişen/nötr = 0/1/0
- **Duyarlılık:** P aralığı [0.005, 0.152] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 6.974

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | data | pearson: haftalik_uzaktan_gun → verimlilik_puani | doğrudan | istatistik | sirket_verisi | 0.800 | 0.012 | 0.030 | -1.000 | 100% | ok |

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.

### C5 — (Çalışanların iddiasının ilişkisel hâli) Daha çok uzaktan çalışan çalışanların verimlilik puanı daha yüksektir

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`positive` · nedensel=hayır · popülasyon: Şirket çalışanları (n=180)
- **Önsel P₀:** 0.35 — C4 ile simetrik.
- **Toplam Bayes faktörü:** 39.811 (log₁₀ = 1.600) → **P = 0.955** (Kabul — uygulanabilir)
- **Spektrum:** S = 1.000 (Güçlü destek) · uyum C = — · destekleyen/çelişen/nötr = 1/0/0
- **Duyarlılık:** P aralığı [0.864, 0.996] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** alt banda (P<0.9) düşmek için LR ≈ 0.42

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | data | pearson: haftalik_uzaktan_gun → verimlilik_puani | doğrudan | istatistik | sirket_verisi | 0.800 | 100.000 | 39.811 | 1.000 | 100% | ok |

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.

### C6 — (İK iddiasının 'diğer koşullar sabitken' yorumu) Kıdem ve departman sabitken uzaktan gün sayısı ile verimlilik arasında ilişki yoktur

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`none` · nedensel=hayır · popülasyon: Şirket çalışanları (n=180)
- **Önsel P₀:** 0.3 — C3 ile aynı gerekçe (nokta-sıfır iddiası, üç durumdan biri).
- **Toplam Bayes faktörü:** 0.292 (log₁₀ = -0.535) → **P = 0.111** (Büyük olasılıkla yanlış)
- **Spektrum:** S = -0.122 (Zayıf çelişki) · uyum C = 0.358 · destekleyen/çelişen/nötr = 2/6/0
- **Duyarlılık:** P aralığı [0.069, 0.540] · karar sağlamlığı 33% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.3) geçmek için LR ≈ 3.426; alt banda (P<0.1) düşmek için LR ≈ 0.888

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D2 | data | regression: haftalik_uzaktan_gun → verimlilik_puani; kontroller: kidem_yil, departman | doğrudan | istatistik | sirket_verisi | 0.800 | 7.028 | 4.758 | 0.847 | 25% | ok |
| S1 | source | Bloom, N., Liang, J., Roberts, J., Ying, Z. J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | doğrudan | contradicts | bloom_liang_ekibi | 0.567 | 0.250 | 0.456 | -0.602 | 13% | unverified |
| S2 | source | İş dergisi haberi (2023): yöneticilere yapılan ankete göre yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor. (Yayın adı/URL kullanıcı tarafından verilmedi.) | doğrudan | contradicts | yonetici_anketi_haberi | 0.056 | 0.500 | 0.962 | -0.301 | 1% | unverified |
| S3 | source | Bloom, N., Han, R., Liang, J. (2024). Hybrid working from home improves retention without damaging performance. Nature 630:920–925. | doğrudan | supports | bloom_liang_ekibi | 0.695 | 4.000 | 2.619 | 0.602 | 16% | unverified |
| S4 | source | Atkin, D., Schoar, A., Shinde, S. (2023). Working from Home, Worker Sorting and Development. NBER Working Paper 31515. | doğrudan | contradicts | atkin_schoar_shinde | 0.454 | 0.250 | 0.533 | -0.602 | 10% | unverified |
| S5 | source | Emanuel, N., Harrington, E. (2024). Working Remotely? Selection, Treatment, and the Market for Remote Work. American Economic Journal: Applied Economics 16(4):528–559. | doğrudan | contradicts | emanuel_harrington | 0.472 | 0.250 | 0.519 | -0.602 | 10% | unverified |
| S6 | source | Gibbs, M., Mengel, F., Siemroth, C. (2023). Work from Home and Productivity: Evidence from Personnel and Analytics Data on Information Technology Professionals. Journal of Political Economy Microeconomics 1(1):7–41. | doğrudan | contradicts | gibbs_mengel_siemroth | 0.514 | 0.250 | 0.490 | -0.602 | 12% | unverified |
| S7 | source | Angelici, M., Profeta, P. (2024). Smart Working: Work Flexibility Without Constraints. Management Science 70(3):1680–1705. | doğrudan | contradicts | angelici_profeta | 0.630 | 0.250 | 0.418 | -0.602 | 14% | unverified |

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

## 3. İddialar arası uyum

| İddialar | İlişkiler | Mantıksal uyum | P değerleri | Tutarsızlık | Not |
|---|---|---|---|---|---|
| C1 ↔ C2 | negative / positive | −1 çelişik | 0.139 / 0.032 | 0.000 |  |
| C1 ↔ C3 | negative / none | −1 çelişik | 0.139 / 0.011 | 0.000 |  |
| C1 ↔ C4 | negative / negative | +1 uyumlu | 0.139 / 0.016 | — |  |
| C1 ↔ C5 | negative / positive | −1 çelişik | 0.139 / 0.955 | 0.094 |  |
| C1 ↔ C6 | negative / none | −1 çelişik | 0.139 / 0.111 | 0.000 |  |
| C2 ↔ C3 | positive / none | −1 çelişik | 0.032 / 0.011 | 0.000 |  |
| C2 ↔ C4 | positive / negative | −1 çelişik | 0.032 / 0.016 | 0.000 |  |
| C2 ↔ C5 | positive / positive | +1 uyumlu | 0.032 / 0.955 | — |  |
| C2 ↔ C6 | positive / none | −1 çelişik | 0.032 / 0.111 | 0.000 |  |
| C3 ↔ C4 | none / negative | −1 çelişik | 0.011 / 0.016 | 0.000 |  |
| C3 ↔ C5 | none / positive | −1 çelişik | 0.011 / 0.955 | 0.000 |  |
| C3 ↔ C6 | none / none | +1 uyumlu | 0.011 / 0.111 | — |  |
| C4 ↔ C5 | negative / positive | −1 çelişik | 0.016 / 0.955 | 0.000 |  |
| C4 ↔ C6 | negative / none | −1 çelişik | 0.016 / 0.111 | 0.000 |  |
| C5 ↔ C6 | positive / none | −1 çelişik | 0.955 / 0.111 | 0.066 |  |

## 4. Değişken özeti

| Değişken | İddialar | Ort. S | Ort. P |
|---|---|---|---|
| `haftalik_uzaktan_gun` | C1, C2, C3, C4, C5, C6 | -0.261 | 0.211 |
| `verimlilik_puani` | C1, C2, C3, C4, C5, C6 | -0.261 | 0.211 |

## 5. Yöntem

- Kanıt kalitesi **Q** ∈ [0,1]: tasarım taban puanı × düzelticiler (n, hakem, çıkar çatışması, replikasyon, yaş, doğrulama, nedensellik açığı). Her çarpan `metadata.json` içindeki `quality_trace`'te.
- Ham olabilirlik oranı: veri/raporlanan istatistik için BIC yaklaşımlı Bayes faktörü BF₁₀ = (1−r²)^(−n/2)/√n, yönlü iddiada işarete göre çevrilir; kaynak tutumu için güçlü=10, orta=4, zayıf=2. Tek kanıt |log₁₀ LR| ≤ 2.0 ile sınırlanır.
- Etkin LR = LR_ham^Q. Aynı kümedeki k kanıt ortalanıp k_eff = k/(1+(k−1)ρ) ile ölçeklenir (ρ = 0.5).
- P = σ(logit P₀ + Σ ln LR_küme). S = Σ Q·d / Σ Q, d = kırpılmış log₁₀ LR_ham ∈ [−1,1]. C = 1 − ağırlıklı standart sapma(d).
- Karar bantları: P≥0.9 kabul · 0.7–0.9 koşullu · 0.3–0.7 belirsiz · 0.1–0.3 büyük olasılıkla yanlış · <0.1 ret.

## 6. Yorum ve Uygulama

### Yönetim kurulu için tek paragraf

**Hiçbir taraf tam olarak haklı değil; her biri sorunun farklı bir parçasında haklı ya da haksız.** Şirket verisinde daha çok uzaktan çalışanların puanı gerçekten daha yüksek (C5, P=0.955, r=+0.44). Yani çalışanların *gözlemi* doğru, Genel Müdür'ün *gözlemi* yanlış (C4, P=0.016). Ancak bu fark neredeyse tamamen **kıdemden** geliyor. Kıdemli çalışanlar hem daha çok uzaktan çalışıyor (r=0.70) hem de daha yüksek puan alıyor (r=0.69). Kıdem ve departman sabit tutulunca uzaktan gün başına etki −0.66 puan (SE 0.59, p=0.26, kısmi r −0.08, %95 GA −0.23…+0.06), yani pratikte sıfır. Bu yüzden İK'nın "hiçbir ilişki yok" sözü ham veride yanlış (C3, P=0.011). "Kıdem sabitken etki yok" anlamında ise şirket verisi tek başına bu yorumu destekliyor (D2: C6 lehine LR≈7). Nedensel soru ("uzaktan çalışma verimliliği artırır mı / düşürür mü") **çözülmüş değil**. Uzaktan çalışmanın verimliliği **artırdığı** iddiası, analiz edilen tüm senaryolarda en zayıf hipotez (C2, P=0.032, 27 senaryonun hepsinde P<0.30).

### Ana bulgular
- **C5 güçlü desteklendi (S=+1.00, P=0.955, kabul, sağlamlık %89):** Ham ilişki pozitif ve belirgin (r=0.44, %95 GA 0.31–0.55, n=180, BF₁₀≈1.9×10⁷). Uzaktan gün 0→5 arttıkça ortalama puan 58.5→75.5. Aynı gruplarda ortalama kıdem de 2.4→11.4 yıl (`ek_analiz/kidem_tabakali.json`).
- **C3 (İK, kelimesi kelimesine) ve C4 (GM'nin ilişkisel hâli) reddedildi (P=0.011 ve 0.016, sağlamlık %89):** Verideki ham ilişki ne sıfır ne de negatif.
- **C2 (çalışanlar, nedensel) reddedildi (S=−0.26, P=0.032, ret).** Kontrollü regresyon, iddianın yönünün tersini gösteriyor (D2, LR_ham=0.038). Dış deneyler bölünmüş: 2 pozitif (Bloom 2015, Angelici & Profeta 2024), 1 sıfır (Bloom ve ark. 2024), 3 negatif (Atkin ve ark. 2023, Emanuel & Harrington 2024, Gibbs ve ark. 2023). Duyarlılık aralığı [0.014, 0.283]. Karar bandı "ret" ile "büyük olasılıkla yanlış" arasında değişiyor (sağlamlık %67), ama hiçbir senaryoda "belirsiz" banda çıkmıyor. Yalnızca İK'nın kaynaklarıyla yapılan duyarlılık çalışmasında da C2'nin P'si 0.160.
- **C1 (Genel Müdür, nedensel) büyük olasılıkla yanlış ama kırılgan (S=−0.19, P=0.139, sağlamlık %44, aralık [0.049, 0.616]).** Şirket verisi negatif bir nedensel etkiyi desteklemiyor (D2, LR_ham=0.247). Destek yalnızca başka ülkelerde, çoğunlukla tam zamanlı uzaktan çalışmayla yapılan çalışmalardan geliyor (Hindistan'da veri girişi, ABD'de çağrı merkezi, pandemide zorunlu evden çalışan BT çalışanları).
- **C6 (İK'nın "kıdem sabitken" yorumu) belirsiz ile büyük olasılıkla yanlış arasında (S=−0.12, P=0.111, sağlamlık %33, aralık [0.069, 0.540]).** Şirket verisi C6'yı destekliyor (LR=7.0). Literatürdeki sıfırdan farklı bulgular (6 çalışmadan 5'i) bu desteği dengeliyor.

### İddialar arası tutarlılık
- **Çalışanlar ile GM aynı gerçeğin iki farklı yorumunu tartışıyor.** Ham ilişki (C5) ile kontrollü/nedensel ilişki (C1, C2, C6) farklı nicelikler. Uyum matrisinde C1↔C5 (tutarsızlık=0.094) ve C5↔C6 (0.066) çiftleri "çelişik" görünüyor, çünkü betik aynı X–Y çiftindeki her iddiayı karşılaştırıyor. Bu çiftler gerçek bir mantıksal çelişki değil, klasik bir **karıştırıcı değişken (kıdem) durumu**. "Uzaktan çalışanların puanı daha yüksek" ile "uzaktan çalışma puanı artırmıyor" aynı anda doğru olabilir. Kurula iletilecek ana mesaj bu: Ham tablo, uzaktan çalışma iznini zaten kıdemlilerin aldığını gösteriyor.
- **Birbirini dışlayan üç nedensel hipotezin olasılık toplamı 1'in altında (C1+C2+C6 = 0.139+0.032+0.111 = 0.282).** Betik her iddiayı ayrı güncelliyor. Dış çalışmaların çoğu her hipotezden birini destekleyip diğer ikisiyle çeliştiği için hepsi birlikte aşağı itiliyor. Bu bir hata değil; kanıtın üç seçenek arasında **ayrım yapamadığını** gösteriyor. Göreli paylar (sezgisel, `ek_analiz/tutarlilik_normalizasyonu.json`): GM %49 · İK-kontrollü %39 · Çalışanlar %11.
- **Sonuç, hangi literatürün eklendiğine bağlı.** Yalnızca şirket verisi ve İK'nın iki kaynağıyla (`ek_analiz/yalnizca_kullanici_kaynaklari/`) önde giden hipotez C6 (P=0.472, pay %65) olur, C1'in P'si ise 0.093'e düşer. Karşı aramada bulunan üç negatif çalışma dengeyi GM'ye doğru kaydırıyor. Bu kayma, bu çalışmaların popülasyonları (tam zamanlı uzaktan çalışma, rutin işler, gelişmekte olan ülkeler, pandemi) şirketinkinden farklı olduğu hâlde oluyor.
- **Literatürdeki çelişkinin olası moderatörleri:** (1) Tam zamanlı uzaktan çalışmada negatif sonuçlar çıkıyor (S4, S5, S6). Hibrit/esnek düzende sonuç sıfır ya da pozitif (S3, S7), ve şirketteki düzen 0–5 gün hibrit. (2) Seçilim: Emanuel & Harrington'da ham farkın 2/3'ü seçilimden geliyor. Bu, şirket verisindeki kıdem karıştırıcılığının aynısı. (3) Gönüllülük: Bloom 2015'te katılımcılar gönüllüydü. (4) Zorunlu pandemi koşulları (S6).
- **İK'nın gönderdiği iki kaynak birbiriyle ve verilerle çelişiyor, ama ağırlıkları çok farklı.** Bloom 2015 RCT'si Q=0.567 ile C2 lehine LR_etkin=2.2 katkı yapıyor. Yönetici anketi haberinin katkısı ise Q=0.034 ve LR_etkin≈1.02, yani pratikte sıfır. Bunun iki nedeni var: anket verimliliği değil yöneticilerin *algısını* ölçüyor, ve haber tanımlanamadı. Aynı türdeki anketlerde çalışanların ~%62'si kendini uzaktan daha verimli hissettiğini söylüyor. İki taraf da öz-algıya dayanıyor ve bu tartışmanın aynası niteliğinde. Bloom ve ark. (2024) deneyinde yöneticilerin beklentisi deney sonunda −%2.6'dan +%1.0'a dönmüş.

### Sınırlılıklar
- `causal_gap` (C1, C2'de D2): Şirket verisi kesitsel ve gözlemsel, bu yüzden Q 0.8'den 0.48'e indirildi. Kıdem ve departman kontrol edildi, ama ölçülmeyen karıştırıcılar (iş tipi, yönetici, performans geçmişi) ve ters nedensellik dışlanamıyor. Ters nedenselliğe örnek: yüksek performanslı/kıdemli çalışana uzaktan çalışma izni verilmesi. Kıdem dilimlerinde ham korelasyonun işareti bile tutarsız (+0.20 / −0.21 / +0.20).
- `conflicting_evidence` (C1, C2, C6; C=0.36–0.43): Literatür gerçekten bölünmüş. Bu bir kodlama hatası değil, bağlama bağlı bir etkinin işareti (yukarıdaki moderatörler).
- `fragile_decision` (C1 %44, C2 %67, C6 %33): Önsel, küme içi korelasyon ve kalite ölçeği makul aralıkta değiştiğinde C1 ve C6'nın kararı değişiyor. Nedensel sonuçlar kesin dille sunulmamalı. C2 için yalnızca "ret" ile "büyük olasılıkla yanlış" arasında gidip geliyor.
- `insufficient_evidence` (C3, C4, C5): Ham ilişki iddiaları tek bir veri setine dayanıyor (tek küme). Yine de BF₁₀≈1.9×10⁷ ile sonuç istatistiksel olarak açık. Bayrak, "bu yalnızca bu şirketin bu kesiti için geçerli" anlamında okunmalı.
- `unverified_sources`: Web sayfası okuma ağ proxy'si tarafından engellendi. Tüm makaleler arama motoru özetleri ve birden çok indeks üzerinden doğrulandı (varlık: evet). Tam metin okunamadığı için hepsine ×0.7 uygulandı. 2023 haberi tanımlanamadı (varlık: bilinmiyor, ×0.5). Bloom 2015'in n'si (~250) doğrulanamadığı için boş bırakıldı.
- **Ölçüm:** `verimlilik_puani`'nın nasıl üretildiği (nesnel çıktı mı, yönetici değerlendirmesi mi) bilinmiyor. Yönetici değerlendirmesiyse, yöneticilerin uzaktan çalışana karşı algı yanlılığı (S2'deki %60) puanı doğrudan etkileyebilir.
- **Kapsam dışı bırakılanlar:** Mang & Anwar (2026, ILR Review) meta-analizi (82 çalışma, "küçük pozitif, bağlama bağlı etki") puanlanmadı. Büyük olasılıkla S1 ve S3–S7'yi içeriyor (çift sayım riski) ve etki büyüklüğü okunamadı. Choudhury ve ark. (2021) WFA–WFH karşılaştırması olduğu için konu dışı sayıldı. Meta-analizin yönü C2 lehine, büyüklüğü ise "küçük".
- Karar eşikleri varsayılan bırakıldı (0.90/0.70/0.30/0.10). Uzaktan çalışma politikası geri alınabilir bir karar olduğu için yüksek riskli sınıfına alınmadı.

### Uygulama önerileri
| İddia | Karar | Önerilen eylem | Koşul / izlenecek gösterge |
|---|---|---|---|
| C5 — Ham ilişki pozitif | Kabul (P=0.955) | Kurula "uzaktan çalışanların puanı daha yüksek" bilgisini **yalnızca betimsel** olarak sunun ve hemen kıdem açıklamasını ekleyin | Kıdem dağılımı değişirse (ör. yeni işe alım dalgası) ilişki de değişir |
| C4 / C3 — Ham ilişki negatif / sıfır | Ret (P=0.016 / 0.011) | "Evden çalışanlar verimsiz" veya "hiçbir ilişki yok" ifadeleri, şirket verisiyle sunulmamalı | — |
| C2 — Uzaktan çalışma verimliliği artırır | Ret (P=0.032; aralık 0.014–0.283) | Uzaktan günleri **verimlilik artışı gerekçesiyle** genişletmeyin. Gerekçe başkaysa (elde tutma, memnuniyet, maliyet) o ayrıca değerlendirilmeli | Kontrollü etki pozitif ve anlamlı çıkarsa yeniden değerlendirin |
| C1 — Uzaktan çalışma verimliliği düşürür | Büyük olasılıkla yanlış, kırılgan (P=0.139; aralık 0.049–0.616) | Uzaktan çalışmayı **verimlilik gerekçesiyle kısıtlamayın**. Şirket verisi bunu desteklemiyor, dış destek ise farklı bağlamlardan (tam zamanlı uzaktan çalışma) geliyor | Özellikle tam zamanlı (4–5 gün) uzaktan ve kıdemsiz çalışanlarda kontrollü etkiyi izleyin (literatürdeki negatif etkiler bu grupta) |
| C6 — Kıdem sabitken etki yok | Büyük olasılıkla yanlış / belirsiz sınırında, kırılgan (P=0.111; aralık 0.069–0.540) | Mevcut hibrit düzeni koruyun ve aşağıdaki pilotla test edin | Pilotta iki grup arasındaki fark ve güven aralığı |

### Sonraki en değerli kanıt
- Belirsiz ve kırılgan nedensel iddiaları bir üst banda taşımak için gereken olabilirlik oranları (`value_of_information`): **C1 → LR≈2.65** (P≥0.30), **C2 → LR≈3.34** (P≥0.10), **C6 → LR≈3.43** (P≥0.30). Üçü de "tek bir iyi çalışma uzaklıkta".
- **En değerli tek adım: şirket içi rastgele hibrit pilotu.** Önerilen tasarım şöyle: Uzaktan çalışmaya uygun ve gönüllü çalışanlar arasında kurayla, ör. haftada 2 gün uzaktan / 0–1 gün uzaktan. Süre 6–9 ay, kıdem ve departmana göre tabakalanmış atama. Sonuç ölçüsü yönetici puanı değil, nesnel çıktı (satış, kapatılan talep, teslim edilen iş). Analiz planı önceden yazılmalı. Bu, `experimental: true` ile Q≈0.9 alacak ve doğrudan şirket popülasyonunu ölçen bir kanıt olur. Örnekte ~150+ çalışan ve şirket verisindeki dağılıma benzer bir etki olursa, betiğin tutucu BIC-BF ölçüsüyle bile C1, C2 ve C6'dan birini ötekilerden ayırabilecek (LR≥3–7) güçte olur.
- **Daha ucuz ara adım:** Elde varsa aynı çalışanların **zaman içindeki** uzaktan gün değişimleri ve puanlarıyla kişi-içi (sabit etkili) bir analiz. Kıdem gibi kişiye özgü karıştırıcıları otomatik olarak dışlar.
- `verimlilik_puani`'nın nasıl üretildiğini netleştirin. Yönetici değerlendirmesiyse, nesnel bir çıktı ölçüsüyle karşılaştırın.

