# İddia Doğrulama Raporu — Uzaktan çalışma ve verimlilik — üç tarafın çelişkili iddiaları — DUYARLILIK: yalnızca şirket verisi + İK'nın 2 kaynağı

**Araştırma sorusu:** Bu şirkette haftalık uzaktan çalışma gün sayısı ile verimlilik puanı arasındaki ilişki nedir; Genel Müdür (düşürür), Çalışanlar (artırır) ve İK (ilişki yok) iddialarından hangisi kanıtlarla en uyumlu?  
**Tarih:** 2026-10-02 · **Şema:** v1.0 · **İddia sayısı:** 6 · **Kanıt sayısı:** 4

> **Nasıl okunur:** *S* (−1…+1) kalite-ağırlıklı kanıtların iddiayı ne yönde ve ne güçte desteklediğini gösterir. *P* önsel olasılığın kanıtların olabilirlik oranlarıyla Bayesçi güncellenmesiyle elde edilen sonsal olasılıktır. *C* (0…1) kanıtların kendi aralarındaki uyumudur. *Sağlamlık*, 27 duyarlılık senaryosunun kaçında kararın değişmediğidir.

## 1. Özet

| ID | İddia | S | Spektrum | P | Karar | C | Kalite | Sağlamlık | Uyarı |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Genel Müdür: Uzaktan çalışma verimliliği (nedensel olarak) düşürür | -0.576 | Orta çelişki | 0.093 | Ret | 0.843 | Düşük | 56% | 2 |
| C2 | Çalışanlar: Uzaktan çalışma verimliliği (nedensel olarak) artırır | -0.138 | Zayıf çelişki | 0.160 | Büyük olasılıkla yanlış | 0.214 | Düşük | 67% | 4 |
| C3 | İK: Uzaktan çalışma ile verimlilik arasında hiçbir ilişki yoktur | -1.000 | Güçlü çelişki | 0.011 | Ret | — | Yüksek | 89% | 1 |
| C4 | (GM iddiasının ilişkisel hâli) Daha çok uzaktan çalışan çalışanların verimlilik puanı daha düşüktür | -1.000 | Güçlü çelişki | 0.016 | Ret | — | Yüksek | 89% | 1 |
| C5 | (Çalışanların iddiasının ilişkisel hâli) Daha çok uzaktan çalışan çalışanların verimlilik puanı daha yüksektir | 1.000 | Güçlü destek | 0.955 | Kabul — uygulanabilir | — | Yüksek | 89% | 1 |
| C6 | (İK iddiasının 'diğer koşullar sabitken' yorumu) Kıdem ve departman sabitken uzaktan gün sayısı ile verimlilik arasında ilişki yoktur | 0.224 | Zayıf destek | 0.472 | Belirsiz — ek kanıt gerekli | 0.292 | Düşük | 67% | 4 |

### Spektrum görünümü

```
C1  −1 ────●─────┼────────── +1  S=-0.58  P=0.09
C2  −1 ─────────●┼────────── +1  S=-0.14  P=0.16
C3  −1 ●─────────┼────────── +1  S=-1.00  P=0.01
C4  −1 ●─────────┼────────── +1  S=-1.00  P=0.02
C5  −1 ──────────┼─────────● +1  S=+1.00  P=0.95
C6  −1 ──────────┼─●──────── +1  S=+0.22  P=0.47
```

## 2. İddia ayrıntıları

### C1 — Genel Müdür: Uzaktan çalışma verimliliği (nedensel olarak) düşürür

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`negative` · nedensel=evet · popülasyon: Şirket çalışanları (n=180)
- **Önsel P₀:** 0.3 — Literatür bağlama göre karışık (bazı deneylerde artış, bazılarında düşüş); nedensel iddia ilişkisel versiyondan (0.35) daha güçlü olduğu için biraz daha düşük önsel.
- **Toplam Bayes faktörü:** 0.238 (log₁₀ = -0.623) → **P = 0.093** (Ret)
- **Spektrum:** S = -0.576 (Orta çelişki) · uyum C = 0.843 · destekleyen/çelişen/nötr = 1/2/0
- **Duyarlılık:** P aralığı [0.056, 0.488] · karar sağlamlığı 56% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 1.088

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D2 | data | regression: haftalik_uzaktan_gun → verimlilik_puani; kontroller: kidem_yil, departman | doğrudan | istatistik | sirket_verisi | 0.480 | 0.247 | 0.511 | -0.607 | 45% | causal_gap |
| S1 | source | Bloom, N., Liang, J., Roberts, J., Ying, Z. J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | doğrudan | contradicts | bloom_liang_ekibi | 0.567 | 0.250 | 0.456 | -0.602 | 53% | unverified |
| S2 | source | İş dergisi haberi (2023): yöneticilere yapılan ankete göre yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor. (Yayın adı/URL kullanıcı tarafından verilmedi.) | doğrudan | supports | yonetici_anketi_haberi | 0.034 | 2.000 | 1.024 | 0.301 | 2% | unverified |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C2 — Çalışanlar: Uzaktan çalışma verimliliği (nedensel olarak) artırır

- **Yapı:** X=`haftalik_uzaktan_gun` → Y=`verimlilik_puani` · ilişki=`positive` · nedensel=evet · popülasyon: Şirket çalışanları (n=180)
- **Önsel P₀:** 0.3 — C1 ile simetrik: tartışmalı alan, nedensel iddia → 0.30.
- **Toplam Bayes faktörü:** 0.444 (log₁₀ = -0.353) → **P = 0.160** (Büyük olasılıkla yanlış)
- **Spektrum:** S = -0.138 (Zayıf çelişki) · uyum C = 0.214 · destekleyen/çelişen/nötr = 1/2/0
- **Duyarlılık:** P aralığı [0.112, 0.610] · karar sağlamlığı 67% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.3) geçmek için LR ≈ 2.253; alt banda (P<0.1) düşmek için LR ≈ 0.584

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D2 | data | regression: haftalik_uzaktan_gun → verimlilik_puani; kontroller: kidem_yil, departman | doğrudan | istatistik | sirket_verisi | 0.480 | 0.038 | 0.207 | -1.000 | 66% | causal_gap |
| S1 | source | Bloom, N., Liang, J., Roberts, J., Ying, Z. J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | doğrudan | supports | bloom_liang_ekibi | 0.567 | 4.000 | 2.195 | 0.602 | 33% | unverified |
| S2 | source | İş dergisi haberi (2023): yöneticilere yapılan ankete göre yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor. (Yayın adı/URL kullanıcı tarafından verilmedi.) | doğrudan | contradicts | yonetici_anketi_haberi | 0.034 | 0.500 | 0.977 | -0.301 | 1% | unverified |

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `single_source_dominance` — Tek bir kanıt toplam etkinin çoğunu taşıyor; sonuç ona bağımlı.
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
- **Toplam Bayes faktörü:** 2.086 (log₁₀ = 0.319) → **P = 0.472** (Belirsiz — ek kanıt gerekli)
- **Spektrum:** S = 0.224 (Zayıf destek) · uyum C = 0.292 · destekleyen/çelişen/nötr = 1/2/0
- **Duyarlılık:** P aralığı [0.375, 0.879] · karar sağlamlığı 67% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.7) geçmek için LR ≈ 2.61; alt banda (P<0.3) düşmek için LR ≈ 0.479

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D2 | data | regression: haftalik_uzaktan_gun → verimlilik_puani; kontroller: kidem_yil, departman | doğrudan | istatistik | sirket_verisi | 0.800 | 7.028 | 4.758 | 0.847 | 65% | ok |
| S1 | source | Bloom, N., Liang, J., Roberts, J., Ying, Z. J. (2015). Does Working from Home Work? Evidence from a Chinese Experiment. Quarterly Journal of Economics 130(1):165–218. | doğrudan | contradicts | bloom_liang_ekibi | 0.567 | 0.250 | 0.456 | -0.602 | 33% | unverified |
| S2 | source | İş dergisi haberi (2023): yöneticilere yapılan ankete göre yöneticilerin %60'ı uzaktan çalışanların daha az verimli olduğunu düşünüyor. (Yayın adı/URL kullanıcı tarafından verilmedi.) | doğrudan | contradicts | yonetici_anketi_haberi | 0.056 | 0.500 | 0.962 | -0.301 | 2% | unverified |

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `single_source_dominance` — Tek bir kanıt toplam etkinin çoğunu taşıyor; sonuç ona bağımlı.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

## 3. İddialar arası uyum

| İddialar | İlişkiler | Mantıksal uyum | P değerleri | Tutarsızlık | Not |
|---|---|---|---|---|---|
| C1 ↔ C2 | negative / positive | −1 çelişik | 0.093 / 0.160 | 0.000 |  |
| C1 ↔ C3 | negative / none | −1 çelişik | 0.093 / 0.011 | 0.000 |  |
| C1 ↔ C4 | negative / negative | +1 uyumlu | 0.093 / 0.016 | — |  |
| C1 ↔ C5 | negative / positive | −1 çelişik | 0.093 / 0.955 | 0.048 |  |
| C1 ↔ C6 | negative / none | −1 çelişik | 0.093 / 0.472 | 0.000 |  |
| C2 ↔ C3 | positive / none | −1 çelişik | 0.160 / 0.011 | 0.000 |  |
| C2 ↔ C4 | positive / negative | −1 çelişik | 0.160 / 0.016 | 0.000 |  |
| C2 ↔ C5 | positive / positive | +1 uyumlu | 0.160 / 0.955 | — |  |
| C2 ↔ C6 | positive / none | −1 çelişik | 0.160 / 0.472 | 0.000 |  |
| C3 ↔ C4 | none / negative | −1 çelişik | 0.011 / 0.016 | 0.000 |  |
| C3 ↔ C5 | none / positive | −1 çelişik | 0.011 / 0.955 | 0.000 |  |
| C3 ↔ C6 | none / none | +1 uyumlu | 0.011 / 0.472 | — |  |
| C4 ↔ C5 | negative / positive | −1 çelişik | 0.016 / 0.955 | 0.000 |  |
| C4 ↔ C6 | negative / none | −1 çelişik | 0.016 / 0.472 | 0.000 |  |
| C5 ↔ C6 | positive / none | −1 çelişik | 0.955 / 0.472 | 0.427 |  |

## 4. Değişken özeti

| Değişken | İddialar | Ort. S | Ort. P |
|---|---|---|---|
| `haftalik_uzaktan_gun` | C1, C2, C3, C4, C5, C6 | -0.248 | 0.284 |
| `verimlilik_puani` | C1, C2, C3, C4, C5, C6 | -0.248 | 0.284 |

## 5. Yöntem

- Kanıt kalitesi **Q** ∈ [0,1]: tasarım taban puanı × düzelticiler (n, hakem, çıkar çatışması, replikasyon, yaş, doğrulama, nedensellik açığı). Her çarpan `metadata.json` içindeki `quality_trace`'te.
- Ham olabilirlik oranı: veri/raporlanan istatistik için BIC yaklaşımlı Bayes faktörü BF₁₀ = (1−r²)^(−n/2)/√n, yönlü iddiada işarete göre çevrilir; kaynak tutumu için güçlü=10, orta=4, zayıf=2. Tek kanıt |log₁₀ LR| ≤ 2.0 ile sınırlanır.
- Etkin LR = LR_ham^Q. Aynı kümedeki k kanıt ortalanıp k_eff = k/(1+(k−1)ρ) ile ölçeklenir (ρ = 0.5).
- P = σ(logit P₀ + Σ ln LR_küme). S = Σ Q·d / Σ Q, d = kırpılmış log₁₀ LR_ham ∈ [−1,1]. C = 1 − ağırlıklı standart sapma(d).
- Karar bantları: P≥0.9 kabul · 0.7–0.9 koşullu · 0.3–0.7 belirsiz · 0.1–0.3 büyük olasılıkla yanlış · <0.1 ret.

## 6. Yorum ve Uygulama

Bu bir duyarlılık çalışmasıdır. Yorum ve öneriler ana raporda (`../../rapor.md`, bölüm 6 → 'İddialar arası tutarlılık') yer alır. Bu çalışmada, analistin eklediği S3–S7 çıkarıldığında nedensel sorudaki dengenin C6'ya (kıdem sabitken etki yok) kaydığı görülür.

