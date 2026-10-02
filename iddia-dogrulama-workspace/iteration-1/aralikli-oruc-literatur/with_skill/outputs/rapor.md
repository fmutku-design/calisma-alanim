# İddia Doğrulama Raporu — Aralıklı oruç (16:8) — kilo kaybı ve insülin direnci iddiası

**Araştırma sorusu:** "Aralıklı oruç (16:8), aynı kaloriyi alan klasik diyete göre çok daha fazla kilo verdirir ve insülin direncini tamamen düzeltir" iddiası bilimsel literatürle destekleniyor mu?  
**Tarih:** 2026-10-02 · **Şema:** v1.0 · **İddia sayısı:** 8 · **Kanıt sayısı:** 43

> **Nasıl okunur:** *S* (−1…+1) kalite-ağırlıklı kanıtların iddiayı ne yönde ve ne güçte desteklediğini gösterir. *P* önsel olasılığın kanıtların olabilirlik oranlarıyla Bayesçi güncellenmesiyle elde edilen sonsal olasılıktır. *C* (0…1) kanıtların kendi aralarındaki uyumudur. *Sağlamlık*, 27 duyarlılık senaryosunun kaçında kararın değişmediğidir.

## 1. Özet

| ID | İddia | S | Spektrum | P | Karar | C | Kalite | Sağlamlık | Uyarı |
|---|---|---|---|---|---|---|---|---|---|
| C1 | 16:8 aralıklı oruç (TRE), aynı kaloriyi alan klasik (sürekli kalori kısıtlı) diyete göre daha fazla kilo kaybı sağlar | -0.254 | Zayıf çelişki | 0.104 | Büyük olasılıkla yanlış | 0.337 | Orta | 33% | 3 |
| C2 | 16:8 TRE, eşit kalorili klasik diyete göre 'çok daha fazla' (klinik olarak anlamlı, tutarlı biçimde ≥ ~2 kg / ≥ ~2% fazladan) kilo kaybı sağlar | -0.683 | Güçlü çelişki | 0.012 | Ret | 0.514 | Orta | 78% | 1 |
| C3 | RAKİP: Eşit kaloride 16:8 TRE ile klasik diyet arasında kilo kaybı açısından (anlamlı) fark yoktur | 0.287 | Zayıf destek | 0.873 | Koşullu kabul | 0.332 | Orta | 52% | 3 |
| C4 | ZAYIF VERSİYON: 16:8 TRE, hiçbir diyet müdahalesi olmayan kontrole göre kilo kaybı sağlar (kalori kendiliğinden azaldığı için) | 0.490 | Orta destek | 0.822 | Koşullu kabul | 0.479 | Orta | 33% | 4 |
| C5 | 16:8 TRE insülin direncini azaltır (HOMA-IR düşer; müdahalesiz/serbest beslenme kontrolüne göre) | 0.188 | Zayıf destek | 0.728 | Belirsiz — ek kanıt gerekli | 0.548 | Orta | 56% | 2 |
| C6 | 16:8 TRE, eşit kalorili klasik diyete göre insülin direncini daha fazla azaltır | -0.300 | Orta çelişki | 0.154 | Büyük olasılıkla yanlış | 0.537 | Orta | 48% | 2 |
| C7 | RAKİP: Eşit kaloride 16:8 TRE ile klasik diyet arasında insülin direnci açısından fark yoktur | 0.300 | Orta destek | 0.784 | Belirsiz — ek kanıt gerekli | 0.537 | Orta | 41% | 2 |
| C8 | 16:8 TRE insülin direncini TAMAMEN düzeltir (normal aralığa getirir / ortadan kaldırır) | -0.441 | Orta çelişki | 0.010 | Ret | 0.643 | Orta | 67% | 2 |

### Spektrum görünümü

```
C1  −1 ───────●──┼────────── +1  S=-0.25  P=0.10
C2  −1 ───●──────┼────────── +1  S=-0.68  P=0.01
C3  −1 ──────────┼──●─────── +1  S=+0.29  P=0.87
C4  −1 ──────────┼────●───── +1  S=+0.49  P=0.82
C5  −1 ──────────┼─●──────── +1  S=+0.19  P=0.73
C6  −1 ───────●──┼────────── +1  S=-0.30  P=0.15
C7  −1 ──────────┼──●─────── +1  S=+0.30  P=0.78
C8  −1 ──────●───┼────────── +1  S=-0.44  P=0.01
```

## 2. İddia ayrıntıları

### C1 — 16:8 aralıklı oruç (TRE), aynı kaloriyi alan klasik (sürekli kalori kısıtlı) diyete göre daha fazla kilo kaybı sağlar

- **Yapı:** X=`TRE_16_8_vs_esit_kalorili_diyet` → Y=`kilo_kaybi` · ilişki=`positive` · nedensel=evet · popülasyon: Fazla kilolu/obez yetişkinler
- **Önsel P₀:** 0.35 — Enerji dengesi ilkesine göre eşit kaloride büyük fark beklenmez; sirkadiyen ritim hipotezi makul ama tartışmalı → 'makul ama tartışmalı' aralığının alt ucu. Önsel, bu oturumdaki literatür aramasından ÖNCE, iddianın yapısına ve rubric §9 rehberine göre belirlendi. Not: analistin (modelin) alana dair genel ön bilgisi vardır; bu tamamen 'kör' bir önsel değildir — duyarlılık analizi bu etkiyi ölçer.
- **Toplam Bayes faktörü:** 0.216 (log₁₀ = -0.665) → **P = 0.104** (Büyük olasılıkla yanlış)
- **Spektrum:** S = -0.254 (Zayıf çelişki) · uyum C = 0.337 · destekleyen/çelişen/nötr = 3/6/0
- **Duyarlılık:** P aralığı [0.015, 0.523] · karar sağlamlığı 33% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.3) geçmek için LR ≈ 3.678; alt banda (P<0.1) düşmek için LR ≈ 0.954

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | source | Semnani-Azad Z, Khan TA, et al. (2025). Intermittent fasting strategies and their effects on body weight and other cardiometabolic risk factors: systematic review and network meta-analysis of randomised clinical trials. BMJ 389:e082007. | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.598 | 0.100 | 0.252 | -1.000 | 16% | unverified |
| S2 | source | Garegnani LI, Oltra G, Ivaldi D, et al. (2026). Intermittent fasting for adults with overweight or obesity. Cochrane Database Syst Rev, Issue 2, CD015610.pub2. | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.662 | 0.250 | 0.400 | -0.602 | 11% | unverified |
| S3 | source | Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss. N Engl J Med 386:1495–1504. | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.630 | 0.590 | 0.717 | -0.229 | 4% | unverified |
| S4 | source | Jamshed H, Steger FL, Bryan DR, et al. (2022). Effectiveness of Early Time-Restricted Eating for Weight Loss, Fat Loss, and Cardiometabolic Health in Adults With Obesity: A Randomized Clinical Trial. JAMA Intern Med 182(9):953–962. | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.535 | 25.788 | 5.699 | 1.000 | 21% | unverified |
| S5 | source | Lin S, Cienfuegos S, Ezpeleta M, et al. (2023). Time-Restricted Eating Without Calorie Counting for Weight Loss in a Racially Diverse Population: A Randomized Controlled Trial. Ann Intern Med 176(7):885–895. | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.535 | 0.250 | 0.476 | -0.602 | 9% | unverified |
| S6 | source | Pavlou V, Cienfuegos S, Lin S, et al. (2023). Effect of Time-Restricted Eating on Weight Loss in Adults With Type 2 Diabetes: A Randomized Clinical Trial. JAMA Netw Open 6(10):e2339337. | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.535 | 2.000 | 1.449 | 0.301 | 4% | unverified |
| S7 | source | (2023). Time-restricted eating with calorie restriction on weight loss and cardiometabolic risk: a systematic review and meta-analysis. Eur J Clin Nutr (s41430-023-01311-w). | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.598 | 4.000 | 2.293 | 0.602 | 10% | unverified |
| S8 | source | Maruthur NM, et al. (2024). Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity: A Randomized Controlled Trial. Ann Intern Med 177(5). | X–Y çifti | contradicts | izokalorik_kontrollu_beslenme | 0.567 | 0.100 | 0.271 | -1.000 | 16% | unverified |
| S9 | source | (2024/2025). Is isocaloric intermittent fasting superior to calorie restriction? A systematic review and meta-analysis of RCTs. Nutr Metab Cardiovasc Dis (S0939-4753(24)00439-3). | X–Y çifti | contradicts | izokalorik_kontrollu_beslenme | 0.598 | 0.250 | 0.436 | -0.602 | 10% | unverified |

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C2 — 16:8 TRE, eşit kalorili klasik diyete göre 'çok daha fazla' (klinik olarak anlamlı, tutarlı biçimde ≥ ~2 kg / ≥ ~2% fazladan) kilo kaybı sağlar

- **Yapı:** X=`None` → Y=`None` · ilişki=`positive` · nedensel=evet · popülasyon: Fazla kilolu/obez yetişkinler
- **Önsel P₀:** 0.15 — Büyüklük vurgusu ('çok daha fazla') olağanüstü bir iddia; tek sağlık sitesinden gelen viral tarzda ifade → rubric §9 'şaşırtıcı/olağanüstü' aralığı. Önsel, bu oturumdaki literatür aramasından ÖNCE, iddianın yapısına ve rubric §9 rehberine göre belirlendi. Not: analistin (modelin) alana dair genel ön bilgisi vardır; bu tamamen 'kör' bir önsel değildir — duyarlılık analizi bu etkiyi ölçer.
- **Toplam Bayes faktörü:** 0.069 (log₁₀ = -1.158) → **P = 0.012** (Ret)
- **Spektrum:** S = -0.683 (Güçlü çelişki) · uyum C = 0.514 · destekleyen/çelişen/nötr = 1/4/0
- **Duyarlılık:** P aralığı [0.001, 0.322] · karar sağlamlığı 78% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 9.064

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S10 | source | Semnani-Azad Z, et al. (2025). BMJ 389:e082007 — 'çok daha fazla' büyüklük iddiası açısından. | doğrudan | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.598 | 0.100 | 0.252 | -1.000 | 25% | unverified |
| S11 | source | Garegnani LI, et al. (2026). Cochrane CD015610.pub2 — büyüklük iddiası açısından. | doğrudan | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.662 | 0.100 | 0.218 | -1.000 | 28% | unverified |
| S12 | source | Liu D, et al. (2022). NEJM 386:1495 — büyüklük iddiası açısından. | doğrudan | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.630 | 0.250 | 0.418 | -0.602 | 16% | unverified |
| S13 | source | Jamshed H, et al. (2022). JAMA Intern Med — büyüklük iddiası açısından. | doğrudan | supports | havuz_TRE_vs_CER_serbest_yasam | 0.535 | 2.000 | 1.449 | 0.301 | 7% | unverified |
| S14 | source | Maruthur NM, et al. (2024). Ann Intern Med 177(5) — büyüklük iddiası açısından. | doğrudan | contradicts | izokalorik_kontrollu_beslenme | 0.567 | 0.100 | 0.271 | -1.000 | 24% | unverified |

**Uyarılar:**
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C3 — RAKİP: Eşit kaloride 16:8 TRE ile klasik diyet arasında kilo kaybı açısından (anlamlı) fark yoktur

- **Yapı:** X=`TRE_16_8_vs_esit_kalorili_diyet` → Y=`kilo_kaybi` · ilişki=`none` · nedensel=evet · popülasyon: Fazla kilolu/obez yetişkinler
- **Önsel P₀:** 0.55 — Enerji dengesi ilkesinin doğrudan öngörüsü; C1'in rakibi. C1+C3 önselleri toplamı < 1 (ters yönlü fark olasılığına pay bırakıldı). Önsel, bu oturumdaki literatür aramasından ÖNCE, iddianın yapısına ve rubric §9 rehberine göre belirlendi. Not: analistin (modelin) alana dair genel ön bilgisi vardır; bu tamamen 'kör' bir önsel değildir — duyarlılık analizi bu etkiyi ölçer.
- **Toplam Bayes faktörü:** 5.605 (log₁₀ = 0.749) → **P = 0.873** (Koşullu kabul)
- **Spektrum:** S = 0.287 (Zayıf destek) · uyum C = 0.332 · destekleyen/çelişen/nötr = 6/3/0
- **Duyarlılık:** P aralığı [0.504, 0.994] · karar sağlamlığı 52% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.95) geçmek için LR ≈ 2.774; alt banda (P<0.8) düşmek için LR ≈ 0.584

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | source | Semnani-Azad Z, Khan TA, et al. (2025). Intermittent fasting strategies and their effects on body weight and other cardiometabolic risk factors: systematic review and network meta-analysis of randomised clinical trials. BMJ 389:e082007. | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.598 | 10.000 | 3.967 | 1.000 | 16% | unverified |
| S2 | source | Garegnani LI, Oltra G, Ivaldi D, et al. (2026). Intermittent fasting for adults with overweight or obesity. Cochrane Database Syst Rev, Issue 2, CD015610.pub2. | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.662 | 4.000 | 2.502 | 0.602 | 11% | unverified |
| S3 | source | Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss. N Engl J Med 386:1495–1504. | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.630 | 3.204 | 2.083 | 0.506 | 9% | unverified |
| S4 | source | Jamshed H, Steger FL, Bryan DR, et al. (2022). Effectiveness of Early Time-Restricted Eating for Weight Loss, Fat Loss, and Cardiometabolic Health in Adults With Obesity: A Randomized Clinical Trial. JAMA Intern Med 182(9):953–962. | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.535 | 0.077 | 0.254 | -1.000 | 16% | unverified |
| S5 | source | Lin S, Cienfuegos S, Ezpeleta M, et al. (2023). Time-Restricted Eating Without Calorie Counting for Weight Loss in a Racially Diverse Population: A Randomized Controlled Trial. Ann Intern Med 176(7):885–895. | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.535 | 4.000 | 2.101 | 0.602 | 9% | unverified |
| S6 | source | Pavlou V, Cienfuegos S, Lin S, et al. (2023). Effect of Time-Restricted Eating on Weight Loss in Adults With Type 2 Diabetes: A Randomized Clinical Trial. JAMA Netw Open 6(10):e2339337. | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.535 | 0.500 | 0.690 | -0.301 | 4% | unverified |
| S7 | source | (2023). Time-restricted eating with calorie restriction on weight loss and cardiometabolic risk: a systematic review and meta-analysis. Eur J Clin Nutr (s41430-023-01311-w). | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.598 | 0.250 | 0.436 | -0.602 | 10% | unverified |
| S8 | source | Maruthur NM, et al. (2024). Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity: A Randomized Controlled Trial. Ann Intern Med 177(5). | X–Y çifti | supports | izokalorik_kontrollu_beslenme | 0.567 | 10.000 | 3.690 | 1.000 | 15% | unverified |
| S9 | source | (2024/2025). Is isocaloric intermittent fasting superior to calorie restriction? A systematic review and meta-analysis of RCTs. Nutr Metab Cardiovasc Dis (S0939-4753(24)00439-3). | X–Y çifti | supports | izokalorik_kontrollu_beslenme | 0.598 | 4.000 | 2.293 | 0.602 | 10% | unverified |

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C4 — ZAYIF VERSİYON: 16:8 TRE, hiçbir diyet müdahalesi olmayan kontrole göre kilo kaybı sağlar (kalori kendiliğinden azaldığı için)

- **Yapı:** X=`TRE_16_8_vs_mudahalesiz_kontrol` → Y=`kilo_kaybi` · ilişki=`positive` · nedensel=evet · popülasyon: Fazla kilolu/obez yetişkinler
- **Önsel P₀:** 0.6 — Yeme penceresini daraltmak çoğu kişide toplam alımı azaltır → makul; büyüklüğü belirsiz. Nedensel iddianın 'ilişkisel versiyonu' yerine konan daha zayıf/gerçekçi versiyon. Önsel, bu oturumdaki literatür aramasından ÖNCE, iddianın yapısına ve rubric §9 rehberine göre belirlendi. Not: analistin (modelin) alana dair genel ön bilgisi vardır; bu tamamen 'kör' bir önsel değildir — duyarlılık analizi bu etkiyi ölçer.
- **Toplam Bayes faktörü:** 3.088 (log₁₀ = 0.490) → **P = 0.822** (Koşullu kabul)
- **Spektrum:** S = 0.490 (Orta destek) · uyum C = 0.479 · destekleyen/çelişen/nötr = 6/1/0
- **Duyarlılık:** P aralığı [0.383, 0.999] · karar sağlamlığı 33% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.95) geçmek için LR ≈ 4.101; alt banda (P<0.8) düşmek için LR ≈ 0.863

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S15 | source | (2023). Is time-restricted eating (8/16) beneficial for body weight and metabolism of obese and overweight adults? A systematic review and meta-analysis of randomized controlled trials. (PMC10002957). | X–Y çifti | supports | havuz_TRE_vs_kontrol | 0.598 | 10.000 | 3.967 | 1.000 | 22% | unverified |
| S16 | source | Garegnani LI, et al. (2026). Cochrane CD015610.pub2 — müdahalesiz kontrol karşılaştırması. | X–Y çifti | supports | havuz_TRE_vs_kontrol | 0.662 | 4.000 | 2.502 | 0.602 | 15% | unverified |
| S17 | source | Lin S, et al. (2023). Ann Intern Med 176(7):885–895 — kontrol karşılaştırması. | X–Y çifti | supports | havuz_TRE_vs_kontrol | 0.535 | 10.000 | 3.432 | 1.000 | 20% | unverified |
| S18 | source | Pavlou V, et al. (2023). JAMA Netw Open 6(10):e2339337 — kontrol karşılaştırması. | X–Y çifti | supports | havuz_TRE_vs_kontrol | 0.535 | 4.000 | 2.101 | 0.602 | 12% | unverified |
| S19 | source | Cienfuegos S, Gabel K, Kalam F, et al. (2020). Effects of 4- and 6-h Time-Restricted Feeding on Weight and Cardiometabolic Health: A Randomized Controlled Trial in Adults with Obesity. Cell Metab 32(3):366–378. | X–Y çifti | supports | havuz_TRE_vs_kontrol | 0.567 | 4.000 | 2.195 | 0.602 | 13% | unverified |
| S20 | source | Gabel K, Hoddy KK, Haggerty N, et al. (2018). Effects of 8-hour time restricted feeding on body weight and metabolic disease risk factors in obese adults: A pilot study. Nutr Healthy Aging 4:345–353. | X–Y çifti | supports | havuz_TRE_vs_kontrol | 0.472 | 2.000 | 1.388 | 0.301 | 5% | unverified |
| S21 | source | Lowe DA, Wu N, Rohdin-Bibby L, et al. (2020). Effects of Time-Restricted Eating on Weight Loss and Other Metabolic Parameters in Women and Men With Overweight and Obesity: The TREAT Randomized Clinical Trial. JAMA Intern Med 180(11):1491–1499. | X–Y çifti | contradicts | havuz_TRE_vs_kontrol | 0.630 | 0.250 | 0.418 | -0.602 | 14% | unverified |

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C5 — 16:8 TRE insülin direncini azaltır (HOMA-IR düşer; müdahalesiz/serbest beslenme kontrolüne göre)

- **Yapı:** X=`TRE_16_8_vs_mudahalesiz_kontrol` → Y=`insulin_direnci` · ilişki=`negative` · nedensel=evet · popülasyon: Fazla kilolu/obez yetişkinler, prediyabet/metabolik sendrom dahil
- **Önsel P₀:** 0.55 — Kilo kaybı insülin duyarlılığını genelde iyileştirir; TRE'nin kilo kaybı küçük olabilir → makul ama tartışmalı. Önsel, bu oturumdaki literatür aramasından ÖNCE, iddianın yapısına ve rubric §9 rehberine göre belirlendi. Not: analistin (modelin) alana dair genel ön bilgisi vardır; bu tamamen 'kör' bir önsel değildir — duyarlılık analizi bu etkiyi ölçer.
- **Toplam Bayes faktörü:** 2.193 (log₁₀ = 0.341) → **P = 0.728** (Belirsiz — ek kanıt gerekli)
- **Spektrum:** S = 0.188 (Zayıf destek) · uyum C = 0.548 · destekleyen/çelişen/nötr = 4/3/0
- **Duyarlılık:** P aralığı [0.365, 0.956] · karar sağlamlığı 56% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.8) geçmek için LR ≈ 1.492; alt banda (P<0.3) düşmek için LR ≈ 0.16

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S22 | source | (2023). Is time-restricted eating (8/16) beneficial ... meta-analysis (PMC10002957) — HOMA-IR. | X–Y çifti | supports | havuz_TRE_IR_vs_kontrol | 0.598 | 4.000 | 2.293 | 0.602 | 20% | unverified |
| S23 | source | (2025). Effect of 8-Hour Time-Restricted Eating (16/8 TRE) on Glucose Metabolism and Lipid Profile in Adults: A Systematic Review and Meta-Analysis. Nutr Rev (nuaf206). | X–Y çifti | supports | havuz_TRE_IR_vs_kontrol | 0.598 | 4.000 | 2.293 | 0.602 | 20% | unverified |
| S24 | source | Kaynağı kesin eşlenemeyen TRE meta-analizi (13 RCT, n=612; WebSearch özetinde Frontiers Nutr 2025 sonuçlarıyla birlikte geçti). | X–Y çifti | contradicts | havuz_TRE_IR_vs_kontrol | 0.332 | 0.250 | 0.631 | -0.602 | 11% | unverified |
| S25 | source | Cienfuegos S, et al. (2020). Cell Metab 32(3) — insülin direnci. | X–Y çifti | supports | havuz_TRE_IR_vs_kontrol | 0.567 | 4.000 | 2.195 | 0.602 | 19% | unverified |
| S26 | source | Gabel K, et al. (2018). Nutr Healthy Aging 4:345 — insülin direnci. | X–Y çifti | contradicts | havuz_TRE_IR_vs_kontrol | 0.472 | 0.500 | 0.721 | -0.301 | 8% | unverified |
| S27 | source | Lowe DA, et al. (2020). TREAT, JAMA Intern Med — kardiyometabolik sonuçlar. | X–Y çifti | contradicts | havuz_TRE_IR_vs_kontrol | 0.630 | 0.500 | 0.646 | -0.301 | 11% | unverified |
| S28 | source | Manoogian ENC, et al. (2024). Time-Restricted Eating in Adults With Metabolic Syndrome: A Randomized Controlled Trial. Ann Intern Med 177(11). | X–Y çifti | supports | manoogian_TIMET | 0.630 | 2.000 | 1.548 | 0.301 | 11% | unverified |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C6 — 16:8 TRE, eşit kalorili klasik diyete göre insülin direncini daha fazla azaltır

- **Yapı:** X=`TRE_16_8_vs_esit_kalorili_diyet` → Y=`insulin_direnci` · ilişki=`negative` · nedensel=evet · popülasyon: Fazla kilolu/obez yetişkinler, prediyabet dahil
- **Önsel P₀:** 0.35 — Kilodan bağımsız sirkadiyen etki hipotezi var (erken TRE), ancak tartışmalı → C1 ile aynı mantık. Önsel, bu oturumdaki literatür aramasından ÖNCE, iddianın yapısına ve rubric §9 rehberine göre belirlendi. Not: analistin (modelin) alana dair genel ön bilgisi vardır; bu tamamen 'kör' bir önsel değildir — duyarlılık analizi bu etkiyi ölçer.
- **Toplam Bayes faktörü:** 0.337 (log₁₀ = -0.472) → **P = 0.154** (Büyük olasılıkla yanlış)
- **Spektrum:** S = -0.300 (Orta çelişki) · uyum C = 0.537 · destekleyen/çelişen/nötr = 3/6/0
- **Duyarlılık:** P aralığı [0.007, 0.618] · karar sağlamlığı 48% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.3) geçmek için LR ≈ 2.361; alt banda (P<0.1) düşmek için LR ≈ 0.612

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S29 | source | Liu D, et al. (2022). NEJM 386:1495 — HOMA-IR. | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.630 | 0.250 | 0.418 | -0.602 | 16% | unverified |
| S30 | source | (2023). Eur J Clin Nutr TRE+CR meta-analizi — HOMA-IR. | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.665 | 0.250 | 0.398 | -0.602 | 17% | unverified |
| S31 | source | Jamshed H, et al. (2022). JAMA Intern Med — kardiyometabolik sonuçlar. | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.535 | 0.500 | 0.690 | -0.301 | 7% | unverified |
| S32 | source | Semnani-Azad Z, et al. (2025). BMJ 389:e082007 — kardiyometabolik risk faktörleri. | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.598 | 0.500 | 0.660 | -0.301 | 8% | unverified |
| S33 | source | Pavlou V, et al. (2023). JAMA Netw Open — HbA1c (TRE vs CR). | X–Y çifti | contradicts | havuz_TRE_vs_CER_serbest_yasam | 0.535 | 0.500 | 0.690 | -0.301 | 7% | unverified |
| S34 | source | Maruthur NM, et al. (2024). Ann Intern Med 177(5) — glukoz homeostazı / HOMA-IR. | X–Y çifti | contradicts | izokalorik_kontrollu_beslenme | 0.567 | 0.100 | 0.271 | -1.000 | 24% | unverified |
| S35 | source | Sutton EF, Beyl R, Early KS, et al. (2018). Early Time-Restricted Feeding Improves Insulin Sensitivity, Blood Pressure, and Oxidative Stress Even without Weight Loss in Men with Prediabetes. Cell Metab 27(6):1212–1221. | X–Y çifti | supports | izokalorik_kontrollu_beslenme | 0.441 | 4.000 | 1.843 | 0.602 | 12% | unverified |
| S36 | source | (2024/2025). NMCD izokalorik IF vs CR meta-analizi — HOMA-IR. | X–Y çifti | supports | izokalorik_kontrollu_beslenme | 0.598 | 2.000 | 1.514 | 0.301 | 8% | unverified |
| S37 | source | Effects of Time-Restricted Eating on Insulin Sensitivity, Glycemic Control, and Metabolic Outcomes in Low- and Middle-Income Countries: A Systematic Review (PMC13498806) — aktarılan 'Lucknow' hipokalorik TRE kohortu. | X–Y çifti | supports | lmic_lucknow | 0.052 | 2.000 | 1.037 | 0.301 | 1% | unverified |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C7 — RAKİP: Eşit kaloride 16:8 TRE ile klasik diyet arasında insülin direnci açısından fark yoktur

- **Yapı:** X=`TRE_16_8_vs_esit_kalorili_diyet` → Y=`insulin_direnci` · ilişki=`none` · nedensel=evet · popülasyon: Fazla kilolu/obez yetişkinler
- **Önsel P₀:** 0.55 — Metabolik iyileşmenin büyük ölçüde kilo/enerji açığından geldiği hipotezi; C6'nın rakibi. Önsel, bu oturumdaki literatür aramasından ÖNCE, iddianın yapısına ve rubric §9 rehberine göre belirlendi. Not: analistin (modelin) alana dair genel ön bilgisi vardır; bu tamamen 'kör' bir önsel değildir — duyarlılık analizi bu etkiyi ölçer.
- **Toplam Bayes faktörü:** 2.967 (log₁₀ = 0.472) → **P = 0.784** (Belirsiz — ek kanıt gerekli)
- **Spektrum:** S = 0.300 (Orta destek) · uyum C = 0.537 · destekleyen/çelişen/nötr = 6/3/0
- **Duyarlılık:** P aralığı [0.382, 0.993] · karar sağlamlığı 41% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.8) geçmek için LR ≈ 1.103; alt banda (P<0.3) düşmek için LR ≈ 0.118

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S29 | source | Liu D, et al. (2022). NEJM 386:1495 — HOMA-IR. | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.630 | 4.000 | 2.395 | 0.602 | 16% | unverified |
| S30 | source | (2023). Eur J Clin Nutr TRE+CR meta-analizi — HOMA-IR. | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.665 | 4.000 | 2.514 | 0.602 | 17% | unverified |
| S31 | source | Jamshed H, et al. (2022). JAMA Intern Med — kardiyometabolik sonuçlar. | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.535 | 2.000 | 1.449 | 0.301 | 7% | unverified |
| S32 | source | Semnani-Azad Z, et al. (2025). BMJ 389:e082007 — kardiyometabolik risk faktörleri. | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.598 | 2.000 | 1.514 | 0.301 | 8% | unverified |
| S33 | source | Pavlou V, et al. (2023). JAMA Netw Open — HbA1c (TRE vs CR). | X–Y çifti | supports | havuz_TRE_vs_CER_serbest_yasam | 0.535 | 2.000 | 1.449 | 0.301 | 7% | unverified |
| S34 | source | Maruthur NM, et al. (2024). Ann Intern Med 177(5) — glukoz homeostazı / HOMA-IR. | X–Y çifti | supports | izokalorik_kontrollu_beslenme | 0.567 | 10.000 | 3.690 | 1.000 | 24% | unverified |
| S35 | source | Sutton EF, Beyl R, Early KS, et al. (2018). Early Time-Restricted Feeding Improves Insulin Sensitivity, Blood Pressure, and Oxidative Stress Even without Weight Loss in Men with Prediabetes. Cell Metab 27(6):1212–1221. | X–Y çifti | contradicts | izokalorik_kontrollu_beslenme | 0.441 | 0.250 | 0.543 | -0.602 | 12% | unverified |
| S36 | source | (2024/2025). NMCD izokalorik IF vs CR meta-analizi — HOMA-IR. | X–Y çifti | contradicts | izokalorik_kontrollu_beslenme | 0.598 | 0.500 | 0.660 | -0.301 | 8% | unverified |
| S37 | source | Effects of Time-Restricted Eating on Insulin Sensitivity, Glycemic Control, and Metabolic Outcomes in Low- and Middle-Income Countries: A Systematic Review (PMC13498806) — aktarılan 'Lucknow' hipokalorik TRE kohortu. | X–Y çifti | contradicts | lmic_lucknow | 0.052 | 0.500 | 0.964 | -0.301 | 1% | unverified |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C8 — 16:8 TRE insülin direncini TAMAMEN düzeltir (normal aralığa getirir / ortadan kaldırır)

- **Yapı:** X=`None` → Y=`None` · ilişki=`positive` · nedensel=evet · popülasyon: İnsülin direnci olan yetişkinler
- **Önsel P₀:** 0.05 — 'Tamamen düzeltir' mutlak ve çok faktörlü bir durum (genetik, yağ dağılımı, aktivite, uyku) için olağanüstü bir iddia; hiçbir diyet müdahalesi için tipik değildir → rubric §9 olağanüstü iddia aralığının altı. Önsel, bu oturumdaki literatür aramasından ÖNCE, iddianın yapısına ve rubric §9 rehberine göre belirlendi. Not: analistin (modelin) alana dair genel ön bilgisi vardır; bu tamamen 'kör' bir önsel değildir — duyarlılık analizi bu etkiyi ölçer.
- **Toplam Bayes faktörü:** 0.189 (log₁₀ = -0.723) → **P = 0.010** (Ret)
- **Spektrum:** S = -0.441 (Orta çelişki) · uyum C = 0.643 · destekleyen/çelişen/nötr = 0/4/2
- **Duyarlılık:** P aralığı [0.001, 0.513] · karar sağlamlığı 67% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 11.16

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S38 | source | Maruthur NM, et al. (2024). Ann Intern Med — 'tamamen düzeltir' açısından. | doğrudan | contradicts | izokalorik_kontrollu_beslenme | 0.567 | 0.100 | 0.271 | -1.000 | 40% | unverified |
| S39 | source | (2025). Nutr Rev 16/8 TRE meta-analizi — etki büyüklüğü açısından. | doğrudan | contradicts | havuz_TRE_IR_vs_kontrol | 0.598 | 0.250 | 0.436 | -0.602 | 25% | unverified |
| S40 | source | (2023). PMC10002957 16:8 meta-analizi — etki büyüklüğü açısından. | doğrudan | contradicts | havuz_TRE_IR_vs_kontrol | 0.598 | 0.250 | 0.436 | -0.602 | 25% | unverified |
| S41 | source | Gabel K, et al. (2018). Nutr Healthy Aging — 16:8 ile HOMA-IR. | doğrudan | contradicts | havuz_TRE_IR_vs_kontrol | 0.472 | 0.500 | 0.721 | -0.301 | 10% | unverified |
| S42 | source | Sutton EF, et al. (2018). Cell Metab — 'tamamen düzeltir' açısından. | doğrudan | mixed | izokalorik_kontrollu_beslenme | 0.441 | 1.000 | 1.000 | 0.000 | 0% | unverified |
| S43 | source | Cienfuegos S, et al. (2020). Cell Metab — 'tamamen düzeltir' açısından. | doğrudan | mixed | havuz_TRE_IR_vs_kontrol | 0.567 | 1.000 | 1.000 | 0.000 | 0% | unverified |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

## 3. İddialar arası uyum

| İddialar | İlişkiler | Mantıksal uyum | P değerleri | Tutarsızlık | Not |
|---|---|---|---|---|---|
| C1 ↔ C3 | positive / none | −1 çelişik | 0.104 / 0.873 | 0.000 |  |
| C6 ↔ C7 | negative / none | −1 çelişik | 0.154 / 0.784 | 0.000 | Popülasyonlar farklı; çelişki bağlama bağlı olabilir. |

## 4. Değişken özeti

| Değişken | İddialar | Ort. S | Ort. P |
|---|---|---|---|
| `TRE_16_8_vs_esit_kalorili_diyet` | C1, C3, C6, C7 | 0.008 | 0.479 |
| `kilo_kaybi` | C1, C3, C4 | 0.174 | 0.600 |
| `TRE_16_8_vs_mudahalesiz_kontrol` | C4, C5 | 0.339 | 0.775 |
| `insulin_direnci` | C5, C6, C7 | 0.063 | 0.555 |

## 5. Yöntem

- Kanıt kalitesi **Q** ∈ [0,1]: tasarım taban puanı × düzelticiler (n, hakem, çıkar çatışması, replikasyon, yaş, doğrulama, nedensellik açığı). Her çarpan `metadata.json` içindeki `quality_trace`'te.
- Ham olabilirlik oranı: veri/raporlanan istatistik için BIC yaklaşımlı Bayes faktörü BF₁₀ = (1−r²)^(−n/2)/√n, yönlü iddiada işarete göre çevrilir; kaynak tutumu için güçlü=10, orta=4, zayıf=2. Tek kanıt |log₁₀ LR| ≤ 2.0 ile sınırlanır.
- Etkin LR = LR_ham^Q. Aynı kümedeki k kanıt ortalanıp k_eff = k/(1+(k−1)ρ) ile ölçeklenir (ρ = 0.5).
- P = σ(logit P₀ + Σ ln LR_küme). S = Σ Q·d / Σ Q, d = kırpılmış log₁₀ LR_ham ∈ [−1,1]. C = 1 − ağırlıklı standart sapma(d).
- Karar bantları: P≥0.95 kabul · 0.8–0.95 koşullu · 0.3–0.8 belirsiz · 0.1–0.3 büyük olasılıkla yanlış · <0.1 ret.

## 6. Yorum ve Uygulama

<!-- YORUM_UYGULAMA: Bu bölüm SKILL.md Adım 7'ye göre doldurulur. -->
