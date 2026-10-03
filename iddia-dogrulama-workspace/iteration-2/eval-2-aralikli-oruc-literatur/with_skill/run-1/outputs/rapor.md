# İddia Doğrulama Raporu — Aralıklı oruç (16:8) — izokalorik kilo kaybı ve insülin direnci iddiası

**Araştırma sorusu:** Sağlık sitesindeki iddia: 'Aralıklı oruç (16:8), aynı kaloriyi alan klasik diyete göre çok daha fazla kilo verdirir ve insülin direncini tamamen düzeltir.' Bilimsel literatür bu iddianın parçalarını destekliyor mu?  
**Tarih:** 2026-10-03 · **Şema:** v1.0 · **İddia sayısı:** 11 · **Kanıt sayısı:** 34

> **Nasıl okunur:** *S* (−1…+1) kalite-ağırlıklı kanıtların iddiayı ne yönde ve ne güçte desteklediğini gösterir. *P* önsel olasılığın kanıtların olabilirlik oranlarıyla Bayesçi güncellenmesiyle elde edilen sonsal olasılıktır. *C* (0…1) kanıtların kendi aralarındaki uyumudur. *Sağlamlık*, 27 duyarlılık senaryosunun kaçında kararın değişmediğidir.

## 1. Özet

| ID | İddia | S | Spektrum | P | Karar | C | Kalite | Sağlamlık | Uyarı |
|---|---|---|---|---|---|---|---|---|---|
| C1 | 16:8 TRE, aynı kaloriyi alan klasik (sürekli kalori kısıtlamalı) diyete göre DAHA FAZLA kilo kaybı sağlar | -0.122 | Zayıf çelişki | 0.124 | Büyük olasılıkla yanlış | 0.370 | Düşük | 33% | 3 |
| C2 | Aynı kaloride klasik diyet, 16:8 TRE'den daha fazla kilo kaybı sağlar (rakip) | -0.699 | Güçlü çelişki | 0.000 | Ret | 0.781 | Düşük | 100% | 1 |
| C3 | Aynı kaloride 16:8 TRE ile klasik diyet arasında kilo kaybı açısından anlamlı fark yoktur (rakip) | 0.159 | Zayıf destek | 0.851 | Koşullu kabul | 0.356 | Düşük | 56% | 3 |
| C4 | 16:8 TRE, aynı kalorili klasik diyete göre ÇOK DAHA FAZLA (klinik olarak büyük, ör. ≥%3 vücut ağırlığı / ≥3 kg ek) kilo kaybı sağlar | -0.630 | Güçlü çelişki | 0.003 | Ret | 0.530 | Düşük | 93% | 1 |
| C5 | 16:8 TRE, aynı kalorili klasik diyete göre insülin direncini DAHA FAZLA azaltır | -0.410 | Orta çelişki | 0.019 | Ret | 0.572 | Düşük | 85% | 1 |
| C6 | Aynı kaloride 16:8 TRE ile klasik diyetin insülin direncine etkisi farklı değildir (rakip) | 0.410 | Orta destek | 0.965 | Kabul — uygulanabilir | 0.572 | Düşük | 59% | 2 |
| C7 | Aynı kaloride 16:8 TRE, klasik diyete göre insülin direncini daha az azaltır / kötüleştirir (rakip) | -0.553 | Orta çelişki | 0.002 | Ret | 0.788 | Düşük | 96% | 1 |
| C8 | 16:8 TRE, normal beslenmeye (kontrol) göre insülin direncini azaltır | 0.250 | Zayıf destek | 0.749 | Belirsiz — ek kanıt gerekli | 0.591 | Orta | 63% | 2 |
| C9 | 16:8 TRE'nin normal beslenmeye göre insülin direncine etkisi yoktur (rakip) | -0.133 | Zayıf çelişki | 0.273 | Büyük olasılıkla yanlış | 0.646 | Orta | 63% | 2 |
| C10 | 16:8 TRE, normal beslenmeye göre insülin direncini artırır (rakip) | -0.652 | Güçlü çelişki | 0.002 | Ret | 0.697 | Orta | 82% | 2 |
| C11 | 16:8 TRE insülin direncini TAMAMEN düzeltir (normalleştirir / ortadan kaldırır) | -0.497 | Orta çelişki | 0.008 | Ret | 0.656 | Düşük | 70% | 1 |

### Spektrum görünümü

```
C1   −1 ─────────●┼────────── +1  S=-0.12  P=0.12
C2   −1 ───●──────┼────────── +1  S=-0.70  P=0.00
C3   −1 ──────────┼─●──────── +1  S=+0.16  P=0.85
C4   −1 ────●─────┼────────── +1  S=-0.63  P=0.00
C5   −1 ──────●───┼────────── +1  S=-0.41  P=0.02
C6   −1 ──────────┼───●────── +1  S=+0.41  P=0.96
C7   −1 ────●─────┼────────── +1  S=-0.55  P=0.00
C8   −1 ──────────┼─●──────── +1  S=+0.25  P=0.75
C9   −1 ─────────●┼────────── +1  S=-0.13  P=0.27
C10  −1 ───●──────┼────────── +1  S=-0.65  P=0.00
C11  −1 ─────●────┼────────── +1  S=-0.50  P=0.01
```

## 2. İddia ayrıntıları

### C1 — 16:8 TRE, aynı kaloriyi alan klasik (sürekli kalori kısıtlamalı) diyete göre DAHA FAZLA kilo kaybı sağlar

- **Yapı:** X=`TRE_16_8_vs_izokalorik_KKK` → Y=`kilo_kaybi` · ilişki=`positive` · nedensel=evet · popülasyon: Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)
- **Önsel P₀:** 0.35 — İzokalorik koşulda enerji dengesi kilo farkını sınırlar; sirkadiyen/metabolik avantaj hipotezi makul ama tartışmalı → nötrün biraz altı
- **Toplam Bayes faktörü:** 0.262 (log₁₀ = -0.582) → **P = 0.124** (Büyük olasılıkla yanlış)
- **Spektrum:** S = -0.122 (Zayıf çelişki) · uyum C = 0.370 · destekleyen/çelişen/nötr = 4/6/0
- **Duyarlılık:** P aralığı [0.063, 0.507] · karar sağlamlığı 33% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.3) geçmek için LR ≈ 3.037; alt banda (P<0.1) düşmek için LR ≈ 0.787

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1w | source | Semnani-Azad Z, Khan TA, et al. (2025). Intermittent fasting strategies and their effects on body weight and other cardiometabolic risk factors: systematic review and network meta-analysis of randomised clinical trials. BMJ. | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.250 | 0.515 | -0.602 | 10% | unverified |
| S2w | source | Hamsho M, et al. (2025). Is isocaloric intermittent fasting superior to calorie restriction? A systematic review and meta-analysis of RCTs. Nutr Metab Cardiovasc Dis. | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.250 | 0.515 | -0.602 | 10% | unverified |
| S3w | source | Črešnovar T, Habe B, Jenko Pražnikar Z, Petelin A. (2023). Effectiveness of Time-Restricted Eating with Caloric Restriction vs. Caloric Restriction for Weight Loss and Health: Meta-Analysis. Nutrients. | X–Y çifti | supports | MA_havuzu | 0.479 | 4.000 | 1.942 | 0.602 | 10% | unverified |
| S4w | source | (2023). Time-restricted eating with calorie restriction on weight loss and cardiometabolic risk: a systematic review and meta-analysis. Eur J Clin Nutr (yazarlar doğrulanamadı). | X–Y çifti | supports | MA_havuzu | 0.479 | 4.000 | 1.942 | 0.602 | 10% | unverified |
| S5w | source | Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss (TREATY). N Engl J Med. | X–Y çifti | contradicts | Liu2022 | 0.630 | 0.580 | 0.709 | -0.237 | 5% | unverified |
| S6w | source | Jamshed H, Steger FL, Bryan DR, et al. (2022). Effectiveness of Early Time-Restricted Eating for Weight Loss, Fat Loss, and Cardiometabolic Health in Adults With Obesity: A Randomized Clinical Trial. JAMA Intern Med. | X–Y çifti | supports | Jamshed2022 | 0.428 | 10.000 | 2.682 | 1.000 | 15% | unverified |
| S7w | source | Maruthur NM, et al. (2024). Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity: A Randomized Controlled Trial. Ann Intern Med 177(5):549-558. | X–Y çifti | contradicts | Maruthur2024 | 0.428 | 0.100 | 0.373 | -1.000 | 15% | unverified |
| S8w | source | Lin S, Cienfuegos S, Ezpeleta M, et al. (2023). Time-Restricted Eating Without Calorie Counting for Weight Loss in a Racially Diverse Population: A Randomized Controlled Trial. Ann Intern Med 176(7). | X–Y çifti | contradicts | Lin2023 | 0.428 | 0.250 | 0.552 | -0.602 | 9% | unverified |
| S9w | source | Lowe DA, Wu N, Rohdin-Bibby L, et al. (2020). Effects of Time-Restricted Eating on Weight Loss and Other Metabolic Parameters in Women and Men With Overweight and Obesity: The TREAT Randomized Clinical Trial. JAMA Intern Med 180(11):1491-1499. | X–Y çifti | contradicts | MA_16_8 | 0.504 | 0.250 | 0.497 | -0.602 | 11% | unverified |
| S10w | source | Pavlou V, Cienfuegos S, Lin S, et al. (2023). Effect of Time-Restricted Eating on Weight Loss in Adults With Type 2 Diabetes: A Randomized Clinical Trial. JAMA Netw Open 6(10). | X–Y çifti | supports | Pavlou2023 | 0.428 | 2.000 | 1.346 | 0.301 | 4% | unverified |

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C2 — Aynı kaloride klasik diyet, 16:8 TRE'den daha fazla kilo kaybı sağlar (rakip)

- **Yapı:** X=`TRE_16_8_vs_izokalorik_KKK` → Y=`kilo_kaybi` · ilişki=`negative` · nedensel=evet · popülasyon: Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)
- **Önsel P₀:** 0.15 — Rakip hipotez; TRE'nin kilo kaybını azaltacağına dair güçlü mekanizma yok
- **Toplam Bayes faktörü:** 0.001 (log₁₀ = -2.931) → **P = 0.000** (Ret)
- **Spektrum:** S = -0.699 (Güçlü çelişki) · uyum C = 0.781 · destekleyen/çelişen/nötr = 0/10/0
- **Duyarlılık:** P aralığı [0.000, 0.017] · karar sağlamlığı 100% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 536.619

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1w | source | Semnani-Azad Z, Khan TA, et al. (2025). Intermittent fasting strategies and their effects on body weight and other cardiometabolic risk factors: systematic review and network meta-analysis of randomised clinical trials. BMJ. | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.250 | 0.515 | -0.602 | 8% | unverified |
| S2w | source | Hamsho M, et al. (2025). Is isocaloric intermittent fasting superior to calorie restriction? A systematic review and meta-analysis of RCTs. Nutr Metab Cardiovasc Dis. | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.250 | 0.515 | -0.602 | 8% | unverified |
| S3w | source | Črešnovar T, Habe B, Jenko Pražnikar Z, Petelin A. (2023). Effectiveness of Time-Restricted Eating with Caloric Restriction vs. Caloric Restriction for Weight Loss and Health: Meta-Analysis. Nutrients. | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.250 | 0.515 | -0.602 | 8% | unverified |
| S4w | source | (2023). Time-restricted eating with calorie restriction on weight loss and cardiometabolic risk: a systematic review and meta-analysis. Eur J Clin Nutr (yazarlar doğrulanamadı). | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.250 | 0.515 | -0.602 | 8% | unverified |
| S5w | source | Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss (TREATY). N Engl J Med. | X–Y çifti | contradicts | Liu2022 | 0.630 | 0.034 | 0.120 | -1.000 | 26% | unverified |
| S6w | source | Jamshed H, Steger FL, Bryan DR, et al. (2022). Effectiveness of Early Time-Restricted Eating for Weight Loss, Fat Loss, and Cardiometabolic Health in Adults With Obesity: A Randomized Clinical Trial. JAMA Intern Med. | X–Y çifti | contradicts | Jamshed2022 | 0.428 | 0.100 | 0.373 | -1.000 | 12% | unverified |
| S7w | source | Maruthur NM, et al. (2024). Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity: A Randomized Controlled Trial. Ann Intern Med 177(5):549-558. | X–Y çifti | contradicts | Maruthur2024 | 0.428 | 0.100 | 0.373 | -1.000 | 12% | unverified |
| S8w | source | Lin S, Cienfuegos S, Ezpeleta M, et al. (2023). Time-Restricted Eating Without Calorie Counting for Weight Loss in a Racially Diverse Population: A Randomized Controlled Trial. Ann Intern Med 176(7). | X–Y çifti | contradicts | Lin2023 | 0.428 | 0.250 | 0.552 | -0.602 | 7% | unverified |
| S9w | source | Lowe DA, Wu N, Rohdin-Bibby L, et al. (2020). Effects of Time-Restricted Eating on Weight Loss and Other Metabolic Parameters in Women and Men With Overweight and Obesity: The TREAT Randomized Clinical Trial. JAMA Intern Med 180(11):1491-1499. | X–Y çifti | contradicts | MA_16_8 | 0.504 | 0.250 | 0.497 | -0.602 | 8% | unverified |
| S10w | source | Pavlou V, Cienfuegos S, Lin S, et al. (2023). Effect of Time-Restricted Eating on Weight Loss in Adults With Type 2 Diabetes: A Randomized Clinical Trial. JAMA Netw Open 6(10). | X–Y çifti | contradicts | Pavlou2023 | 0.428 | 0.500 | 0.743 | -0.301 | 4% | unverified |

**Uyarılar:**
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C3 — Aynı kaloride 16:8 TRE ile klasik diyet arasında kilo kaybı açısından anlamlı fark yoktur (rakip)

- **Yapı:** X=`TRE_16_8_vs_izokalorik_KKK` → Y=`kilo_kaybi` · ilişki=`none` · nedensel=evet · popülasyon: Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)
- **Önsel P₀:** 0.5 — Enerji dengesi ilkesine göre izokalorik iki diyetin benzer sonuç vermesi beklenir → C1–C3 setinde en yüksek önsel; set toplamı 1.0
- **Toplam Bayes faktörü:** 5.694 (log₁₀ = 0.755) → **P = 0.851** (Koşullu kabul)
- **Spektrum:** S = 0.159 (Zayıf destek) · uyum C = 0.356 · destekleyen/çelişen/nötr = 6/4/0
- **Duyarlılık:** P aralığı [0.573, 0.960] · karar sağlamlığı 56% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.95) geçmek için LR ≈ 3.337; alt banda (P<0.8) düşmek için LR ≈ 0.703

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1w | source | Semnani-Azad Z, Khan TA, et al. (2025). Intermittent fasting strategies and their effects on body weight and other cardiometabolic risk factors: systematic review and network meta-analysis of randomised clinical trials. BMJ. | X–Y çifti | supports | MA_havuzu | 0.479 | 4.000 | 1.942 | 0.602 | 10% | unverified |
| S2w | source | Hamsho M, et al. (2025). Is isocaloric intermittent fasting superior to calorie restriction? A systematic review and meta-analysis of RCTs. Nutr Metab Cardiovasc Dis. | X–Y çifti | supports | MA_havuzu | 0.479 | 4.000 | 1.942 | 0.602 | 10% | unverified |
| S3w | source | Črešnovar T, Habe B, Jenko Pražnikar Z, Petelin A. (2023). Effectiveness of Time-Restricted Eating with Caloric Restriction vs. Caloric Restriction for Weight Loss and Health: Meta-Analysis. Nutrients. | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.250 | 0.515 | -0.602 | 10% | unverified |
| S4w | source | (2023). Time-restricted eating with calorie restriction on weight loss and cardiometabolic risk: a systematic review and meta-analysis. Eur J Clin Nutr (yazarlar doğrulanamadı). | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.250 | 0.515 | -0.602 | 10% | unverified |
| S5w | source | Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss (TREATY). N Engl J Med. | X–Y çifti | supports | Liu2022 | 0.630 | 3.256 | 2.104 | 0.513 | 11% | unverified |
| S6w | source | Jamshed H, Steger FL, Bryan DR, et al. (2022). Effectiveness of Early Time-Restricted Eating for Weight Loss, Fat Loss, and Cardiometabolic Health in Adults With Obesity: A Randomized Clinical Trial. JAMA Intern Med. | X–Y çifti | contradicts | Jamshed2022 | 0.428 | 0.100 | 0.373 | -1.000 | 14% | unverified |
| S7w | source | Maruthur NM, et al. (2024). Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity: A Randomized Controlled Trial. Ann Intern Med 177(5):549-558. | X–Y çifti | supports | Maruthur2024 | 0.428 | 10.000 | 2.682 | 1.000 | 14% | unverified |
| S8w | source | Lin S, Cienfuegos S, Ezpeleta M, et al. (2023). Time-Restricted Eating Without Calorie Counting for Weight Loss in a Racially Diverse Population: A Randomized Controlled Trial. Ann Intern Med 176(7). | X–Y çifti | supports | Lin2023 | 0.428 | 4.000 | 1.811 | 0.602 | 8% | unverified |
| S9w | source | Lowe DA, Wu N, Rohdin-Bibby L, et al. (2020). Effects of Time-Restricted Eating on Weight Loss and Other Metabolic Parameters in Women and Men With Overweight and Obesity: The TREAT Randomized Clinical Trial. JAMA Intern Med 180(11):1491-1499. | X–Y çifti | supports | MA_16_8 | 0.504 | 4.000 | 2.011 | 0.602 | 10% | unverified |
| S10w | source | Pavlou V, Cienfuegos S, Lin S, et al. (2023). Effect of Time-Restricted Eating on Weight Loss in Adults With Type 2 Diabetes: A Randomized Clinical Trial. JAMA Netw Open 6(10). | X–Y çifti | contradicts | Pavlou2023 | 0.428 | 0.500 | 0.743 | -0.301 | 4% | unverified |

**Uyarılar:**
- `conflicting_evidence` — Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C4 — 16:8 TRE, aynı kalorili klasik diyete göre ÇOK DAHA FAZLA (klinik olarak büyük, ör. ≥%3 vücut ağırlığı / ≥3 kg ek) kilo kaybı sağlar

- **Yapı:** X=`None` → Y=`None` · ilişki=`positive` · nedensel=evet · popülasyon: Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)
- **Önsel P₀:** 0.12 — 'Çok daha fazla' büyüklük iddiası; izokalorik koşulda büyük fark termodinamik açıdan beklenmez → olağanüstü iddia bandı (0.10–0.25) alt ucu
- **Toplam Bayes faktörü:** 0.025 (log₁₀ = -1.603) → **P = 0.003** (Ret)
- **Spektrum:** S = -0.630 (Güçlü çelişki) · uyum C = 0.530 · destekleyen/çelişen/nötr = 1/5/0
- **Duyarlılık:** P aralığı [0.001, 0.151] · karar sağlamlığı 93% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 32.637

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1m | source | Semnani-Azad Z, Khan TA, et al. (2025). Intermittent fasting strategies and their effects on body weight and other cardiometabolic risk factors: systematic review and network meta-analysis of randomised clinical trials. BMJ. | doğrudan | contradicts | MA_havuzu | 0.479 | 0.100 | 0.332 | -1.000 | 23% | unverified |
| S3m | source | Črešnovar T, Habe B, Jenko Pražnikar Z, Petelin A. (2023). Effectiveness of Time-Restricted Eating with Caloric Restriction vs. Caloric Restriction for Weight Loss and Health: Meta-Analysis. Nutrients. | doğrudan | contradicts | MA_havuzu | 0.479 | 0.500 | 0.718 | -0.301 | 7% | unverified |
| S5m | source | Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss (TREATY). N Engl J Med. | doğrudan | contradicts | Liu2022 | 0.630 | 0.100 | 0.234 | -1.000 | 30% | unverified |
| S6m | source | Jamshed H, Steger FL, Bryan DR, et al. (2022). Effectiveness of Early Time-Restricted Eating for Weight Loss, Fat Loss, and Cardiometabolic Health in Adults With Obesity: A Randomized Clinical Trial. JAMA Intern Med. | doğrudan | supports | Jamshed2022 | 0.428 | 2.000 | 1.346 | 0.301 | 6% | unverified |
| S7m | source | Maruthur NM, et al. (2024). Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity: A Randomized Controlled Trial. Ann Intern Med 177(5):549-558. | doğrudan | contradicts | Maruthur2024 | 0.428 | 0.100 | 0.373 | -1.000 | 21% | unverified |
| S8m | source | Lin S, Cienfuegos S, Ezpeleta M, et al. (2023). Time-Restricted Eating Without Calorie Counting for Weight Loss in a Racially Diverse Population: A Randomized Controlled Trial. Ann Intern Med 176(7). | doğrudan | contradicts | Lin2023 | 0.428 | 0.250 | 0.552 | -0.602 | 12% | unverified |

**Uyarılar:**
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C5 — 16:8 TRE, aynı kalorili klasik diyete göre insülin direncini DAHA FAZLA azaltır

- **Yapı:** X=`TRE_16_8_vs_izokalorik_KKK` → Y=`insulin_direnci` · ilişki=`negative` · nedensel=evet · popülasyon: Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)
- **Önsel P₀:** 0.35 — Sirkadiyen hizalama hipotezi (erken TRE) makul ama izokalorik koşulda tartışmalı
- **Toplam Bayes faktörü:** 0.036 (log₁₀ = -1.441) → **P = 0.019** (Ret)
- **Spektrum:** S = -0.410 (Orta çelişki) · uyum C = 0.572 · destekleyen/çelişen/nötr = 2/7/0
- **Duyarlılık:** P aralığı [0.004, 0.183] · karar sağlamlığı 85% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 5.693

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S2i | source | Hamsho M, et al. (2025). Is isocaloric intermittent fasting superior to calorie restriction? A systematic review and meta-analysis of RCTs. Nutr Metab Cardiovasc Dis. | X–Y çifti | supports | MA_havuzu | 0.479 | 2.000 | 1.394 | 0.301 | 7% | unverified |
| S3i | source | Črešnovar T, Habe B, Jenko Pražnikar Z, Petelin A. (2023). Effectiveness of Time-Restricted Eating with Caloric Restriction vs. Caloric Restriction for Weight Loss and Health: Meta-Analysis. Nutrients. | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.500 | 0.718 | -0.301 | 7% | unverified |
| S4i | source | (2023). Time-restricted eating with calorie restriction on weight loss and cardiometabolic risk: a systematic review and meta-analysis. Eur J Clin Nutr (yazarlar doğrulanamadı). | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.250 | 0.515 | -0.602 | 14% | unverified |
| S5i | source | Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss (TREATY). N Engl J Med. | X–Y çifti | contradicts | Liu2022 | 0.630 | 0.250 | 0.418 | -0.602 | 18% | unverified |
| S6i | source | Jamshed H, Steger FL, Bryan DR, et al. (2022). Effectiveness of Early Time-Restricted Eating for Weight Loss, Fat Loss, and Cardiometabolic Health in Adults With Obesity: A Randomized Clinical Trial. JAMA Intern Med. | X–Y çifti | contradicts | Jamshed2022 | 0.428 | 0.250 | 0.552 | -0.602 | 12% | unverified |
| S7i | source | Maruthur NM, et al. (2024). Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity: A Randomized Controlled Trial. Ann Intern Med 177(5):549-558. | X–Y çifti | contradicts | Maruthur2024 | 0.428 | 0.250 | 0.552 | -0.602 | 12% | unverified |
| S11i | source | Peters B, Schwarz J, et al. (2025). Intended isocaloric time-restricted eating shifts circadian clocks but does not improve cardiometabolic health in women with overweight (ChronoFast). Sci Transl Med 17:eadv6787. | X–Y çifti | contradicts | ChronoFast2025 | 0.454 | 0.100 | 0.352 | -1.000 | 21% | unverified |
| S12i | source | Sutton EF, Beyl R, Early KS, et al. (2018). Early Time-Restricted Feeding Improves Insulin Sensitivity, Blood Pressure, and Oxidative Stress Even without Weight Loss in Men with Prediabetes. Cell Metab 27(6):1212-1221. | X–Y çifti | supports | Sutton2018 | 0.220 | 4.000 | 1.358 | 0.602 | 6% | unverified |
| S10i | source | Pavlou V, Cienfuegos S, Lin S, et al. (2023). Effect of Time-Restricted Eating on Weight Loss in Adults With Type 2 Diabetes: A Randomized Clinical Trial. JAMA Netw Open 6(10). | X–Y çifti | contradicts | Pavlou2023 | 0.268 | 0.500 | 0.831 | -0.301 | 4% | unverified |

**Uyarılar:**
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C6 — Aynı kaloride 16:8 TRE ile klasik diyetin insülin direncine etkisi farklı değildir (rakip)

- **Yapı:** X=`TRE_16_8_vs_izokalorik_KKK` → Y=`insulin_direnci` · ilişki=`none` · nedensel=evet · popülasyon: Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)
- **Önsel P₀:** 0.5 — İnsülin duyarlılığındaki iyileşmenin büyük kısmının kilo kaybından gelmesi beklenir → izokalorik koşulda fark yok en olası
- **Toplam Bayes faktörü:** 27.588 (log₁₀ = 1.441) → **P = 0.965** (Kabul — uygulanabilir)
- **Spektrum:** S = 0.410 (Orta destek) · uyum C = 0.572 · destekleyen/çelişen/nötr = 7/2/0
- **Duyarlılık:** P aralığı [0.817, 0.996] · karar sağlamlığı 59% (27 senaryo)
- **Bilginin değeri:** alt banda (P<0.95) düşmek için LR ≈ 0.689

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S2i | source | Hamsho M, et al. (2025). Is isocaloric intermittent fasting superior to calorie restriction? A systematic review and meta-analysis of RCTs. Nutr Metab Cardiovasc Dis. | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.500 | 0.718 | -0.301 | 7% | unverified |
| S3i | source | Črešnovar T, Habe B, Jenko Pražnikar Z, Petelin A. (2023). Effectiveness of Time-Restricted Eating with Caloric Restriction vs. Caloric Restriction for Weight Loss and Health: Meta-Analysis. Nutrients. | X–Y çifti | supports | MA_havuzu | 0.479 | 2.000 | 1.394 | 0.301 | 7% | unverified |
| S4i | source | (2023). Time-restricted eating with calorie restriction on weight loss and cardiometabolic risk: a systematic review and meta-analysis. Eur J Clin Nutr (yazarlar doğrulanamadı). | X–Y çifti | supports | MA_havuzu | 0.479 | 4.000 | 1.942 | 0.602 | 14% | unverified |
| S5i | source | Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss (TREATY). N Engl J Med. | X–Y çifti | supports | Liu2022 | 0.630 | 4.000 | 2.395 | 0.602 | 18% | unverified |
| S6i | source | Jamshed H, Steger FL, Bryan DR, et al. (2022). Effectiveness of Early Time-Restricted Eating for Weight Loss, Fat Loss, and Cardiometabolic Health in Adults With Obesity: A Randomized Clinical Trial. JAMA Intern Med. | X–Y çifti | supports | Jamshed2022 | 0.428 | 4.000 | 1.811 | 0.602 | 12% | unverified |
| S7i | source | Maruthur NM, et al. (2024). Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity: A Randomized Controlled Trial. Ann Intern Med 177(5):549-558. | X–Y çifti | supports | Maruthur2024 | 0.428 | 4.000 | 1.811 | 0.602 | 12% | unverified |
| S11i | source | Peters B, Schwarz J, et al. (2025). Intended isocaloric time-restricted eating shifts circadian clocks but does not improve cardiometabolic health in women with overweight (ChronoFast). Sci Transl Med 17:eadv6787. | X–Y çifti | supports | ChronoFast2025 | 0.454 | 10.000 | 2.842 | 1.000 | 21% | unverified |
| S12i | source | Sutton EF, Beyl R, Early KS, et al. (2018). Early Time-Restricted Feeding Improves Insulin Sensitivity, Blood Pressure, and Oxidative Stress Even without Weight Loss in Men with Prediabetes. Cell Metab 27(6):1212-1221. | X–Y çifti | contradicts | Sutton2018 | 0.220 | 0.250 | 0.737 | -0.602 | 6% | unverified |
| S10i | source | Pavlou V, Cienfuegos S, Lin S, et al. (2023). Effect of Time-Restricted Eating on Weight Loss in Adults With Type 2 Diabetes: A Randomized Clinical Trial. JAMA Netw Open 6(10). | X–Y çifti | supports | Pavlou2023 | 0.268 | 2.000 | 1.204 | 0.301 | 4% | unverified |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C7 — Aynı kaloride 16:8 TRE, klasik diyete göre insülin direncini daha az azaltır / kötüleştirir (rakip)

- **Yapı:** X=`TRE_16_8_vs_izokalorik_KKK` → Y=`insulin_direnci` · ilişki=`positive` · nedensel=evet · popülasyon: Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)
- **Önsel P₀:** 0.15 — Rakip hipotez; geç yeme penceresinin olumsuz etkisi teorik olarak mümkün ama zayıf
- **Toplam Bayes faktörü:** 0.014 (log₁₀ = -1.850) → **P = 0.002** (Ret)
- **Spektrum:** S = -0.553 (Orta çelişki) · uyum C = 0.788 · destekleyen/çelişen/nötr = 0/9/0
- **Duyarlılık:** P aralığı [0.000, 0.101] · karar sağlamlığı 96% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 44.612

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S2i | source | Hamsho M, et al. (2025). Is isocaloric intermittent fasting superior to calorie restriction? A systematic review and meta-analysis of RCTs. Nutr Metab Cardiovasc Dis. | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.500 | 0.718 | -0.301 | 7% | unverified |
| S3i | source | Črešnovar T, Habe B, Jenko Pražnikar Z, Petelin A. (2023). Effectiveness of Time-Restricted Eating with Caloric Restriction vs. Caloric Restriction for Weight Loss and Health: Meta-Analysis. Nutrients. | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.500 | 0.718 | -0.301 | 7% | unverified |
| S4i | source | (2023). Time-restricted eating with calorie restriction on weight loss and cardiometabolic risk: a systematic review and meta-analysis. Eur J Clin Nutr (yazarlar doğrulanamadı). | X–Y çifti | contradicts | MA_havuzu | 0.479 | 0.250 | 0.515 | -0.602 | 14% | unverified |
| S5i | source | Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss (TREATY). N Engl J Med. | X–Y çifti | contradicts | Liu2022 | 0.630 | 0.250 | 0.418 | -0.602 | 18% | unverified |
| S6i | source | Jamshed H, Steger FL, Bryan DR, et al. (2022). Effectiveness of Early Time-Restricted Eating for Weight Loss, Fat Loss, and Cardiometabolic Health in Adults With Obesity: A Randomized Clinical Trial. JAMA Intern Med. | X–Y çifti | contradicts | Jamshed2022 | 0.428 | 0.250 | 0.552 | -0.602 | 12% | unverified |
| S7i | source | Maruthur NM, et al. (2024). Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity: A Randomized Controlled Trial. Ann Intern Med 177(5):549-558. | X–Y çifti | contradicts | Maruthur2024 | 0.428 | 0.250 | 0.552 | -0.602 | 12% | unverified |
| S11i | source | Peters B, Schwarz J, et al. (2025). Intended isocaloric time-restricted eating shifts circadian clocks but does not improve cardiometabolic health in women with overweight (ChronoFast). Sci Transl Med 17:eadv6787. | X–Y çifti | contradicts | ChronoFast2025 | 0.454 | 0.100 | 0.352 | -1.000 | 21% | unverified |
| S12i | source | Sutton EF, Beyl R, Early KS, et al. (2018). Early Time-Restricted Feeding Improves Insulin Sensitivity, Blood Pressure, and Oxidative Stress Even without Weight Loss in Men with Prediabetes. Cell Metab 27(6):1212-1221. | X–Y çifti | contradicts | Sutton2018 | 0.220 | 0.250 | 0.737 | -0.602 | 6% | unverified |
| S10i | source | Pavlou V, Cienfuegos S, Lin S, et al. (2023). Effect of Time-Restricted Eating on Weight Loss in Adults With Type 2 Diabetes: A Randomized Clinical Trial. JAMA Netw Open 6(10). | X–Y çifti | contradicts | Pavlou2023 | 0.268 | 0.500 | 0.831 | -0.301 | 4% | unverified |

**Uyarılar:**
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C8 — 16:8 TRE, normal beslenmeye (kontrol) göre insülin direncini azaltır

- **Yapı:** X=`TRE_16_8_vs_kontrol` → Y=`insulin_direnci` · ilişki=`negative` · nedensel=evet · popülasyon: Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)
- **Önsel P₀:** 0.55 — Serbest TRE genelde kalori alımını ve kiloyu azaltır; bu da insülin direncini düşürmeli → makul, hafif olumlu önsel
- **Toplam Bayes faktörü:** 2.447 (log₁₀ = 0.389) → **P = 0.749** (Belirsiz — ek kanıt gerekli)
- **Spektrum:** S = 0.250 (Zayıf destek) · uyum C = 0.591 · destekleyen/çelişen/nötr = 2/1/0
- **Duyarlılık:** P aralığı [0.397, 0.911] · karar sağlamlığı 63% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.8) geçmek için LR ≈ 1.338; alt banda (P<0.3) düşmek için LR ≈ 0.143

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S13c | source | (2025). Effect of 8-Hour Time-Restricted Eating (16/8 TRE) on Glucose Metabolism and Lipid Profile in Adults: A Systematic Review and Meta-Analysis. Nutrition Reviews (23 RCT, n=1280). | X–Y çifti | supports | MA_16_8 | 0.698 | 3.309 | 2.306 | 0.520 | 44% | unverified |
| S9c | source | Lowe DA, Wu N, Rohdin-Bibby L, et al. (2020). Effects of Time-Restricted Eating on Weight Loss and Other Metabolic Parameters in Women and Men With Overweight and Obesity: The TREAT Randomized Clinical Trial. JAMA Intern Med 180(11):1491-1499. | X–Y çifti | contradicts | MA_16_8 | 0.630 | 0.500 | 0.646 | -0.301 | 23% | unverified |
| S14c | source | Cienfuegos S, Gabel K, Kalam F, et al. (2020). Effects of 4- and 6-h Time-Restricted Feeding on Weight and Cardiometabolic Health: A Randomized Controlled Trial in Adults with Obesity. Cell Metab. | X–Y çifti | supports | Cienfuegos2020 | 0.454 | 4.000 | 1.875 | 0.602 | 33% | unverified |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C9 — 16:8 TRE'nin normal beslenmeye göre insülin direncine etkisi yoktur (rakip)

- **Yapı:** X=`TRE_16_8_vs_kontrol` → Y=`insulin_direnci` · ilişki=`none` · nedensel=evet · popülasyon: Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)
- **Önsel P₀:** 0.4 — Kilo kaybı küçük kalırsa etki ölçülemeyebilir
- **Toplam Bayes faktörü:** 0.564 (log₁₀ = -0.249) → **P = 0.273** (Büyük olasılıkla yanlış)
- **Spektrum:** S = -0.133 (Zayıf çelişki) · uyum C = 0.646 · destekleyen/çelişen/nötr = 1/2/0
- **Duyarlılık:** P aralığı [0.142, 0.660] · karar sağlamlığı 63% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.3) geçmek için LR ≈ 1.14; alt banda (P<0.1) düşmek için LR ≈ 0.296

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S13c | source | (2025). Effect of 8-Hour Time-Restricted Eating (16/8 TRE) on Glucose Metabolism and Lipid Profile in Adults: A Systematic Review and Meta-Analysis. Nutrition Reviews (23 RCT, n=1280). | X–Y çifti | contradicts | MA_16_8 | 0.698 | 0.603 | 0.703 | -0.220 | 25% | unverified |
| S9c | source | Lowe DA, Wu N, Rohdin-Bibby L, et al. (2020). Effects of Time-Restricted Eating on Weight Loss and Other Metabolic Parameters in Women and Men With Overweight and Obesity: The TREAT Randomized Clinical Trial. JAMA Intern Med 180(11):1491-1499. | X–Y çifti | supports | MA_16_8 | 0.630 | 2.000 | 1.548 | 0.301 | 31% | unverified |
| S14c | source | Cienfuegos S, Gabel K, Kalam F, et al. (2020). Effects of 4- and 6-h Time-Restricted Feeding on Weight and Cardiometabolic Health: A Randomized Controlled Trial in Adults with Obesity. Cell Metab. | X–Y çifti | contradicts | Cienfuegos2020 | 0.454 | 0.250 | 0.533 | -0.602 | 44% | unverified |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C10 — 16:8 TRE, normal beslenmeye göre insülin direncini artırır (rakip)

- **Yapı:** X=`TRE_16_8_vs_kontrol` → Y=`insulin_direnci` · ilişki=`positive` · nedensel=evet · popülasyon: Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)
- **Önsel P₀:** 0.05 — Mekanizma yok; dışlayıcı tamamlayıcı hipotez
- **Toplam Bayes faktörü:** 0.047 (log₁₀ = -1.331) → **P = 0.002** (Ret)
- **Spektrum:** S = -0.652 (Güçlü çelişki) · uyum C = 0.697 · destekleyen/çelişen/nötr = 0/3/0
- **Duyarlılık:** P aralığı [0.000, 0.264] · karar sağlamlığı 82% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 45.19

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S13c | source | (2025). Effect of 8-Hour Time-Restricted Eating (16/8 TRE) on Glucose Metabolism and Lipid Profile in Adults: A Systematic Review and Meta-Analysis. Nutrition Reviews (23 RCT, n=1280). | X–Y çifti | contradicts | MA_16_8 | 0.698 | 0.010 | 0.040 | -1.000 | 75% | unverified |
| S9c | source | Lowe DA, Wu N, Rohdin-Bibby L, et al. (2020). Effects of Time-Restricted Eating on Weight Loss and Other Metabolic Parameters in Women and Men With Overweight and Obesity: The TREAT Randomized Clinical Trial. JAMA Intern Med 180(11):1491-1499. | X–Y çifti | contradicts | MA_16_8 | 0.630 | 0.500 | 0.646 | -0.301 | 10% | unverified |
| S14c | source | Cienfuegos S, Gabel K, Kalam F, et al. (2020). Effects of 4- and 6-h Time-Restricted Feeding on Weight and Cardiometabolic Health: A Randomized Controlled Trial in Adults with Obesity. Cell Metab. | X–Y çifti | contradicts | Cienfuegos2020 | 0.454 | 0.250 | 0.533 | -0.602 | 15% | unverified |

**Uyarılar:**
- `single_source_dominance` — Tek bir kanıt toplam etkinin çoğunu taşıyor; sonuç ona bağımlı.
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

### C11 — 16:8 TRE insülin direncini TAMAMEN düzeltir (normalleştirir / ortadan kaldırır)

- **Yapı:** X=`None` → Y=`None` · ilişki=`positive` · nedensel=evet · popülasyon: Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)
- **Önsel P₀:** 0.08 — Mutlak/olağanüstü iddia: insülin direnci çok etkenli (adipozite, genetik, aktivite); tek bir öğün zamanlaması müdahalesinin onu tamamen ortadan kaldırması biyolojik olarak beklenmez → 0.05–0.10
- **Toplam Bayes faktörü:** 0.091 (log₁₀ = -1.039) → **P = 0.008** (Ret)
- **Spektrum:** S = -0.497 (Orta çelişki) · uyum C = 0.656 · destekleyen/çelişen/nötr = 1/4/1
- **Duyarlılık:** P aralığı [0.002, 0.347] · karar sağlamlığı 70% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 13.974

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S13t | source | (2025). Effect of 8-Hour Time-Restricted Eating (16/8 TRE) on Glucose Metabolism and Lipid Profile in Adults: A Systematic Review and Meta-Analysis. Nutrition Reviews (23 RCT, n=1280). | doğrudan | contradicts | MA_16_8 | 0.698 | 0.100 | 0.200 | -1.000 | 51% | unverified |
| S9t | source | Lowe DA, Wu N, Rohdin-Bibby L, et al. (2020). Effects of Time-Restricted Eating on Weight Loss and Other Metabolic Parameters in Women and Men With Overweight and Obesity: The TREAT Randomized Clinical Trial. JAMA Intern Med 180(11):1491-1499. | doğrudan | contradicts | MA_16_8 | 0.630 | 0.500 | 0.646 | -0.301 | 14% | unverified |
| S11t | source | Peters B, Schwarz J, et al. (2025). Intended isocaloric time-restricted eating shifts circadian clocks but does not improve cardiometabolic health in women with overweight (ChronoFast). Sci Transl Med 17:eadv6787. | doğrudan | contradicts | ChronoFast2025 | 0.454 | 0.250 | 0.533 | -0.602 | 20% | unverified |
| S5t | source | Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss (TREATY). N Engl J Med. | doğrudan | contradicts | Liu2022 | 0.630 | 0.500 | 0.646 | -0.301 | 14% | unverified |
| S12t | source | Sutton EF, Beyl R, Early KS, et al. (2018). Early Time-Restricted Feeding Improves Insulin Sensitivity, Blood Pressure, and Oxidative Stress Even without Weight Loss in Men with Prediabetes. Cell Metab 27(6):1212-1221. | doğrudan | mixed | Sutton2018 | 0.220 | 1.000 | 1.000 | 0.000 | 0% | unverified |
| S15t | source | (t.y.) Hepatic-Metabolite-Based Intermittent Fasting Enables a ... (Thieme Connect, doi 10.1055/a-1510-8896) — insülin direnci normalleşmesi/remisyonu >%76 bildiriliyor (arama özetinden). | doğrudan | supports | Thieme_HMIF | 0.052 | 2.000 | 1.037 | 0.301 | 1% | unverified |

**Uyarılar:**
- `unverified_sources` — Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).

## 3. İddialar arası uyum

| İddialar | İlişkiler | Mantıksal uyum | P değerleri | Tutarsızlık | Not |
|---|---|---|---|---|---|
| C1 ↔ C2 | positive / negative | −1 çelişik | 0.124 / 0.000 | 0.000 |  |
| C1 ↔ C3 | positive / none | −1 çelişik | 0.124 / 0.851 | 0.000 |  |
| C2 ↔ C3 | negative / none | −1 çelişik | 0.000 / 0.851 | 0.000 |  |
| C5 ↔ C6 | negative / none | −1 çelişik | 0.019 / 0.965 | 0.000 |  |
| C5 ↔ C7 | negative / positive | −1 çelişik | 0.019 / 0.002 | 0.000 |  |
| C6 ↔ C7 | none / positive | −1 çelişik | 0.965 / 0.002 | 0.000 |  |
| C8 ↔ C9 | negative / none | −1 çelişik | 0.749 / 0.273 | 0.022 |  |
| C8 ↔ C10 | negative / positive | −1 çelişik | 0.749 / 0.002 | 0.000 |  |
| C9 ↔ C10 | none / positive | −1 çelişik | 0.273 / 0.002 | 0.000 |  |

### Rakip hipotez setleri

Aynı kapsamda birbirini dışlayan iddialar. Kapsayıcı setlerde ΣP ≈ 1 olmalıdır; *normalize P* tutarlı olasılık dağılımıdır.

| Değişkenler | Kapsam | Hipotezler | P | ΣP | Normalize P | En olası | Açık |
|---|---|---|---|---|---|---|---|
| TRE_16_8_vs_izokalorik_KKK – kilo_kaybi | nedensel · Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil) | C1:positive, C2:negative, C3:none | 0.124 / 0.000 / 0.851 | 0.975 | 0.127 / 0.000 / 0.873 | C3 | 0.025 |
| TRE_16_8_vs_izokalorik_KKK – insulin_direnci | nedensel · Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil) | C7:positive, C5:negative, C6:none | 0.002 / 0.019 / 0.965 | 0.986 | 0.002 / 0.019 / 0.979 | C6 | 0.014 |
| TRE_16_8_vs_kontrol – insulin_direnci | nedensel · Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil) | C10:positive, C8:negative, C9:none | 0.002 / 0.749 / 0.273 | 1.024 | 0.002 / 0.731 / 0.267 | C8 | 0.024 |

## 4. Değişken özeti

| Değişken | İddialar | Ort. S | Ort. P |
|---|---|---|---|
| `TRE_16_8_vs_izokalorik_KKK` | C1, C2, C3, C5, C6, C7 | -0.202 | 0.327 |
| `kilo_kaybi` | C1, C2, C3 | -0.221 | 0.325 |
| `insulin_direnci` | C5, C6, C7, C8, C9, C10 | -0.181 | 0.335 |
| `TRE_16_8_vs_kontrol` | C8, C9, C10 | -0.178 | 0.341 |

## 5. Yöntem

- Kanıt kalitesi **Q** ∈ [0,1]: tasarım taban puanı × düzelticiler (n, hakem, çıkar çatışması, replikasyon, yaş, doğrulama, nedensellik açığı). Her çarpan `metadata.json` içindeki `quality_trace`'te.
- Ham olabilirlik oranı: veri/raporlanan istatistik için BIC yaklaşımlı Bayes faktörü BF₁₀ = (1−r²)^(−n/2)/√n, yönlü iddiada işarete göre çevrilir; kaynak tutumu için güçlü=10, orta=4, zayıf=2. Tek kanıt |log₁₀ LR| ≤ 2.0 ile sınırlanır.
- Etkin LR = LR_ham^Q. Aynı kümedeki k kanıt ortalanıp k_eff = k/(1+(k−1)ρ) ile ölçeklenir (ρ = 0.5).
- P = σ(logit P₀ + Σ ln LR_küme). S = Σ Q·d / Σ Q, d = kırpılmış log₁₀ LR_ham ∈ [−1,1]. C = 1 − ağırlıklı standart sapma(d).
- Kapsam: değişken çifti kanıtı iddianın kapsamına göre seçilir — `controls` belirten iddia yalnızca aynı kontrollerle yapılmış analizi; ilişkisel iddia aynı veri kümesindeki ham analizi; nedensel iddia en kontrollü analizi kullanır. Gözlemsel kanıtın nedensel iddiaya desteği LR ≤ 3 ile sınırlanır.
- Karar bantları: P≥0.95 kabul · 0.8–0.95 koşullu · 0.3–0.8 belirsiz · 0.1–0.3 büyük olasılıkla yanlış · <0.1 ret.

## 6. Yorum ve Uygulama

### Ana bulgular
- **"Aynı kaloride daha fazla kilo verdirir" (C1) büyük olasılıkla yanlış:** S=−0.12, P=0.124 (duyarlılık aralığı 0.06–0.51, sağlamlık %33, kırılgan). Rakip set içinde en olası hipotez C3 "anlamlı fark yok" (P=0.851, normalize 0.873; koşullu kabul). Kalori gerçekten eşitlendiğinde (Maruthur 2024: TRE −2.3 kg / olağan düzen −2.6 kg; TREATY/Liu 2022: 12 ayda net fark −1.8 kg, P=.11) TRE'nin üstünlüğü görülmüyor. TRE lehine çıkan meta-analizler (Črešnovar 2023: −2.11 kg; EJCN 2023: −1.40 kg) ve Jamshed 2022 (+2.3 kg, yazarların tahminine göre ~214 kcal/gün daha düşük alımla açıklanıyor) farkın küçük olduğunu gösteriyor ve büyük olasılıkla kalori eşitliğinin tam sağlanamamasından kaynaklanıyor.
- **"ÇOK daha fazla kilo verdirir" (C4) reddedildi:** S=−0.63, P=0.003, sağlamlık %93. TRE lehine en olumlu tahminler bile ~1.4–2.3 kg. Bu fark "çok daha fazla" ifadesini karşılamıyor.
- **"İnsülin direncini tamamen düzeltir" (C11) reddedildi:** S=−0.50, P=0.008 (aralık 0.002–0.35, sağlamlık %70). 16:8'e özgü en geniş meta-analiz (23 RCT, n=1280) HOMA-IR'de yalnızca "hafif" bir düşüş buluyor (SMD −0.16; %95 GA −0.29 ile −0.02). Hiçbir RCT normalleşme veya ortadan kalkma bildirmiyor. İddiayı destekleyen tek kaynak (Thieme, özel bir IF protokolü) doğrulanamadı ve Q=0.05 aldı.
- **Doğru olan kısmı (C8):** 16:8, serbest beslenmeye göre insülin direncini *biraz* azaltıyor olabilir: P=0.749, S=+0.25. Sıkılaştırılmış eşiklerde bu sonuç "belirsiz" bandında kalıyor. Bu etki büyük olasılıkla kalori azalması ve kilo kaybı üzerinden işliyor. Kalori sabitken insülin direncinde TRE'ye özgü ek fayda görülmüyor: C5 P=0.019 (ret), C6 "fark yok" P=0.965 (sağlamlık %59, kırılgan). Kalori sabit tutulan ChronoFast 2025 çalışmasında insülin duyarlılığı değişmedi.

### İddialar arası tutarlılık
- Kilo seti (C1/C2/C3): ΣP=0.975, normalize P = 0.127 / 0.000 / 0.873 → en olası hipotez "fark yok" (C3). Set tutarlı (açık 0.025).
- İzokalorik insülin seti (C5/C6/C7): ΣP=0.986, normalize P = 0.019 / 0.979 / 0.002 → en olası hipotez "fark yok" (C6).
- 16:8 ve kontrol insülin seti (C8/C9/C10): ΣP=1.024, normalize P = 0.731 / 0.267 / 0.002 → en olası hipotez "azaltır" (C8), ama net bir ayrım yok.
- Kapsamlar arası: C8 (kontrole göre azaltır, P=0.75) ile C6 (aynı kaloride fark yok, P=0.97) çelişmiyor, ikisi aynı anda doğru olabilir. TRE insanların daha az yemesini sağladığı için insülin direncini düşürebiliyor, ama aynı kalori alınırsa ek bir avantajı görünmüyor. Sitedeki iddia bu iki durumu birbirine karıştırıyor.

### Sınırlılıklar
- `unverified_sources` (tüm iddialarda): Ortamda WebFetch ve doğrudan HTTP erişimi engelliydi. Kaynakların varlığı arama sonuçlarıyla doğrulandı, ama bulgular tam metinden değil, arama özetlerinden alındı. Bu nedenle tüm kaynaklarda `claim_matches_source=null` (×0.7) ve ortalama Q yalnızca 0.43–0.59. Tam metin okunduğunda Q değerleri yükselir ve sonuçlar uçlara doğru kayar. Jamshed 2022 GA'sı ve Maruthur 2024 HOMA-IR ayrıntısı gibi bazı rakamlar doğrulanamadı.
- `fragile_decision` (C1, C3, C6, C8, C9): Bu iddialarda karar önsele, ρ'ya ve Q ölçeğine duyarlı. Ayrıca meta-analizler ile içerdikleri RCT'ler kısmen örtüşüyor (çift sayım riski). Tüm örtüşen kanıtın tek kümede toplandığı en tutucu varyantta (`varyant_tek_kume/`) sonuçlar şöyle: C1 P=0.297 (yine "büyük olasılıkla yanlış"), C3 P=0.578 (belirsiz), C6 P=0.675 (belirsiz), C5 P=0.206. C4 P=0.040 ve C11 P=0.031 bu varyantta da **ret** bandında kalıyor. Yani iddianın abartılı iki parçasının ("çok daha fazla" ve "tamamen düzeltir") reddi sağlam. "Fark yok" sonucunun kesinlik derecesi ise bağımlılık varsayımına bağlı.
- `conflicting_evidence` (C1, C3; C=0.37 / 0.36): Kilo karşılaştırmasında kaynaklar bölünmüş durumda (4 destek / 6 çelişki). Akla yatkın moderatörler: kalori eşitliğinin ne kadar sıkı sağlandığı (kontrollü beslenme mi, reçete mi), pencerenin erken mi geç mi olduğu ve süre.
- `single_source_dominance` (C10): Sonuç büyük ölçüde 16/8 meta-analizine (S13c, %75 pay) dayanıyor. Ancak bu iddia zaten rakip bir hipotez ve ana sonucu etkilemiyor.
- Varsayımlar: "klasik diyet" sürekli kalori kısıtlaması, "çok daha fazla" ≥%3 vücut ağırlığı veya ≥3 kg ek kayıp, "tamamen düzeltir" insülin direncinin normalleşmesi olarak yorumlandı. Popülasyon aşırı kilolu veya obez yetişkinler. Birçok RCT farklı pencereler kullanıyor (6, 8 ve 10 saat; erken veya geç); bu fark `applicability` ile cezalandırıldı.
- Sağlık iddiası olduğu için karar eşikleri sıkılaştırıldı: kabul ≥0.95, koşullu ≥0.80, belirsiz ≥0.30, b.o. yanlış ≥0.10. Bu analiz tıbbi tavsiye değildir ve hekim veya diyetisyen görüşünün yerini tutmaz.

### Uygulama önerileri
| İddia | Karar | Önerilen eylem | Koşul / izlenecek gösterge |
|---|---|---|---|
| C1 aynı kaloride daha fazla kilo | B.o. yanlış (P=0.12) | Sitedeki ifade "aynı kaloride benzer kilo kaybı" olarak düzeltilmeli | Sıkı kalori eşitlemeli yeni RCT'ler |
| C4 "çok daha fazla" kilo | Ret (P=0.003) | Bu ifade kaldırılmalı; yanıltıcı | — |
| C3 / C6 aynı kaloride fark yok | Koşullu kabul / kabul (kırılgan) | 16:8, kalori açığı oluşturmayı kolaylaştıran bir *araç* olarak sunulabilir; sihirli bir avantaj olarak değil | Kişinin uyumu, gerçek kalori alımı |
| C8 insülin direncini azaltabilir | Belirsiz (P=0.75) | "Kilo kaybıyla birlikte insülin direnci biraz iyileşebilir" denebilir | HOMA-IR ve açlık insülini; kilo değişimi |
| C11 tamamen düzeltir | Ret (P=0.008) | Bu ifade kaldırılmalı. İnsülin direnci veya diyabeti olanlar ilaç ya da tedaviyi hekim onayı olmadan bırakmamalı; öğün atlama hipoglisemi riski taşıyabilir | Hekim takibi, HbA1c |

### Sonraki en değerli kanıt
- **C9 / C8 (LR ≈ 1.14 / 1.34):** Bu iki iddia bir çalışma uzaklıkta. Klasik 16:8 (12:00–20:00) ile serbest beslenmeyi karşılaştıran, n≥150, ≥6 ay süren, HOMA-IR'i veya tercihen clamp ile ölçülen insülin duyarlılığını birincil sonuç alan, ön kayıtlı bir RCT bu iki iddiayı belirgin biçimde ayırır.
- **C1 / C3 (LR ≈ 3.0 / 3.3):** Kalori alımını kontrollü beslenmeyle *gerçekten* eşitleyen, klasik 16:8 penceresi kullanan, n≥100 ve ≥6 aylık bir RCT. Böyle bir çalışmada fark yine bulunmazsa C3 kabul bandına geçer.
- **Mevcut kanıtın doğrulanması:** Liu 2022, Maruthur 2024, ChronoFast 2025 ve 16/8 meta-analizinin tam metinlerinin okunması (`claim_matches_source=true`) Q değerlerini ~%40 artırır. Bu, yeni bir çalışmaya gerek kalmadan sonuçları netleştirmenin en ucuz yoludur.

