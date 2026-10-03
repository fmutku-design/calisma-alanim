# İddia Doğrulama Raporu — Öğrenci verisiyle danışman iddialarının doğrulanması

**Araştırma sorusu:** Danışmanın 4 iddiası (çalışma saati, sosyal medya, cinsiyet, uyku → not ortalaması) kullanıcının 240 öğrencilik verisiyle destekleniyor mu?  
**Tarih:** 2026-10-03 · **Şema:** v1.0 · **İddia sayısı:** 13 · **Kanıt sayısı:** 7

> **Nasıl okunur:** *S* (−1…+1) kalite-ağırlıklı kanıtların iddiayı ne yönde ve ne güçte desteklediğini gösterir. *P* önsel olasılığın kanıtların olabilirlik oranlarıyla Bayesçi güncellenmesiyle elde edilen sonsal olasılıktır. *C* (0…1) kanıtların kendi aralarındaki uyumudur. *Sağlamlık*, 27 duyarlılık senaryosunun kaçında kararın değişmediğidir.

## 1. Özet

| ID | İddia | S | Spektrum | P | Karar | C | Kalite | Sağlamlık | Uyarı |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Haftalık çalışma saati arttıkça not ortalaması yükselir (ilişkisel) | 1.000 | Güçlü destek | 0.987 | Kabul — uygulanabilir | — | Yüksek | 89% | 2 |
| C2 | Haftalık çalışma saati arttıkça not ortalaması düşer (rakip) | -1.000 | Güçlü çelişki | 0.002 | Ret | — | Yüksek | 89% | 2 |
| C3 | Haftalık çalışma saati ile not ortalaması arasında ilişki yoktur (rakip) | -1.000 | Güçlü çelişki | 0.010 | Ret | — | Yüksek | 89% | 2 |
| C4 | Sosyal medya kullanımı not ortalamasını düşürür (nedensel) | 0.477 | Orta destek | 0.527 | Belirsiz — ek kanıt gerekli | — | Düşük | 67% | 5 |
| C5 | Günlük sosyal medya süresi arttıkça not ortalaması düşer (ilişkisel versiyon) | 1.000 | Güçlü destek | 0.979 | Kabul — uygulanabilir | — | Yüksek | 89% | 2 |
| C6 | Günlük sosyal medya süresi arttıkça not ortalaması yükselir (rakip) | -1.000 | Güçlü çelişki | 0.003 | Ret | — | Yüksek | 89% | 2 |
| C7 | Günlük sosyal medya süresi ile not ortalaması arasında ilişki yoktur (rakip) | -1.000 | Güçlü çelişki | 0.017 | Ret | — | Yüksek | 89% | 2 |
| C8 | Kız öğrencilerin not ortalaması erkeklerden yüksektir | -1.000 | Güçlü çelişki | 0.069 | Ret | — | Yüksek | 67% | 3 |
| C9 | Erkek öğrencilerin not ortalaması kızlardan yüksektir (rakip) | -0.610 | Güçlü çelişki | 0.035 | Ret | — | Yüksek | 56% | 3 |
| C10 | Cinsiyete göre not ortalaması farkı yoktur (rakip) | 0.860 | Güçlü destek | 0.724 | Koşullu kabul | — | Yüksek | 22% | 3 |
| C11 | Uyku süresi ile not ortalaması arasında ilişki yoktur | -1.000 | Güçlü çelişki | 0.011 | Ret | — | Yüksek | 89% | 2 |
| C12 | Uyku süresi arttıkça not ortalaması yükselir (rakip) | 1.000 | Güçlü destek | 0.978 | Kabul — uygulanabilir | — | Yüksek | 89% | 2 |
| C13 | Uyku süresi arttıkça not ortalaması düşer (rakip) | -1.000 | Güçlü çelişki | 0.006 | Ret | — | Yüksek | 89% | 2 |

### Spektrum görünümü

```
C1   −1 ──────────┼─────────● +1  S=+1.00  P=0.99
C2   −1 ●─────────┼────────── +1  S=-1.00  P=0.00
C3   −1 ●─────────┼────────── +1  S=-1.00  P=0.01
C4   −1 ──────────┼────●───── +1  S=+0.48  P=0.53
C5   −1 ──────────┼─────────● +1  S=+1.00  P=0.98
C6   −1 ●─────────┼────────── +1  S=-1.00  P=0.00
C7   −1 ●─────────┼────────── +1  S=-1.00  P=0.02
C8   −1 ●─────────┼────────── +1  S=-1.00  P=0.07
C9   −1 ────●─────┼────────── +1  S=-0.61  P=0.04
C10  −1 ──────────┼────────●─ +1  S=+0.86  P=0.72
C11  −1 ●─────────┼────────── +1  S=-1.00  P=0.01
C12  −1 ──────────┼─────────● +1  S=+1.00  P=0.98
C13  −1 ●─────────┼────────── +1  S=-1.00  P=0.01
```

## 2. İddia ayrıntıları

### C1 — Haftalık çalışma saati arttıkça not ortalaması yükselir (ilişkisel)

- **Yapı:** X=`haftalik_calisma_saati` → Y=`not_ortalamasi` · ilişki=`positive` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.65 — Literatürde çalışma süresi–not ilişkisi genelde pozitif ama zayıf (r≈0.1–0.3); makul, yaygın kabul gören → 0.65
- **Toplam Bayes faktörü:** 39.811 (log₁₀ = 1.600) → **P = 0.987** (Kabul — uygulanabilir)
- **Spektrum:** S = 1.000 (Güçlü destek) · uyum C = — · destekleyen/çelişen/nötr = 1/0/0
- **Duyarlılık:** P aralığı [0.864, 0.996] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** alt banda (P<0.9) düşmek için LR ≈ 0.122

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | data | pearson: haftalik_calisma_saati → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.800 | 100.000 | 39.811 | 1.000 | 100% | ok |

**Kapsam dışı bırakılan kanıtlar:** D2 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C2 — Haftalık çalışma saati arttıkça not ortalaması düşer (rakip)

- **Yapı:** X=`haftalik_calisma_saati` → Y=`not_ortalamasi` · ilişki=`negative` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.07 — Mekanizma zayıf (yalnızca zorlanan öğrencinin daha çok çalışması gibi ters nedensellik) → düşük
- **Toplam Bayes faktörü:** 0.025 (log₁₀ = -1.600) → **P = 0.002** (Ret)
- **Spektrum:** S = -1.000 (Güçlü çelişki) · uyum C = — · destekleyen/çelişen/nötr = 0/1/0
- **Duyarlılık:** P aralığı [0.001, 0.136] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 58.768

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | data | pearson: haftalik_calisma_saati → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.800 | 0.010 | 0.025 | -1.000 | 100% | ok |

**Kapsam dışı bırakılan kanıtlar:** D2 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C3 — Haftalık çalışma saati ile not ortalaması arasında ilişki yoktur (rakip)

- **Yapı:** X=`haftalik_calisma_saati` → Y=`not_ortalamasi` · ilişki=`none` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.28 — Bazı çalışmalar ihmal edilebilir ilişki raporluyor → kalan olasılık
- **Toplam Bayes faktörü:** 0.025 (log₁₀ = -1.600) → **P = 0.010** (Ret)
- **Spektrum:** S = -1.000 (Güçlü çelişki) · uyum C = — · destekleyen/çelişen/nötr = 0/1/0
- **Duyarlılık:** P aralığı [0.004, 0.136] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 11.374

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | data | pearson: haftalik_calisma_saati → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.800 | 0.010 | 0.025 | -1.000 | 100% | ok |

**Kapsam dışı bırakılan kanıtlar:** D2 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C4 — Sosyal medya kullanımı not ortalamasını düşürür (nedensel)

- **Yapı:** X=`gunluk_sosyal_medya_saat` → Y=`not_ortalamasi` · ilişki=`negative` · nedensel=evet · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.4 — Nedensel iddia ilişkiselden daha güçlü; literatürde etki küçük ve tartışmalı → 0.40
- **Toplam Bayes faktörü:** 1.669 (log₁₀ = 0.222) → **P = 0.527** (Belirsiz — ek kanıt gerekli)
- **Spektrum:** S = 0.477 (Orta destek) · uyum C = — · destekleyen/çelişen/nötr = 1/0/0
- **Duyarlılık:** P aralığı [0.334, 0.847] · karar sağlamlığı 67% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.7) geçmek için LR ≈ 2.097; alt banda (P<0.3) düşmek için LR ≈ 0.385

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D4 | data | regression: gunluk_sosyal_medya_saat → not_ortalamasi; kontroller: haftalik_calisma_saati, uyku_saat, okul_turu, cinsiyet | X–Y çifti | istatistik | ogrenci_verisi | 0.466 | 3.000 | 1.669 | 0.477 | 100% | causal_gap |

**Kapsam dışı bırakılan kanıtlar:** D3 (nedensel iddia: aynı veri kümesinde daha kontrollü analiz var)

**Uyarılar:**
- `causal_cap_applied` — Gözlemsel kanıtın nedensel iddiaya desteği tavanla sınırlandı (korelasyon ≠ nedensellik).
- `causal_gap` — Nedensel iddia, nedensellik kuramayan tasarımlarla destekleniyor.
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C5 — Günlük sosyal medya süresi arttıkça not ortalaması düşer (ilişkisel versiyon)

- **Yapı:** X=`gunluk_sosyal_medya_saat` → Y=`not_ortalamasi` · ilişki=`negative` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.55 — Küçük negatif ilişki bulgusu yaygın ama tutarsız → hafif olumlu önsel
- **Toplam Bayes faktörü:** 38.089 (log₁₀ = 1.581) → **P = 0.979** (Kabul — uygulanabilir)
- **Spektrum:** S = 1.000 (Güçlü destek) · uyum C = — · destekleyen/çelişen/nötr = 1/0/0
- **Duyarlılık:** P aralığı [0.860, 0.996] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** alt banda (P<0.9) düşmek için LR ≈ 0.193

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D3 | data | pearson: gunluk_sosyal_medya_saat → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.790 | 100.000 | 38.089 | 1.000 | 100% | ok |

**Kapsam dışı bırakılan kanıtlar:** D4 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C6 — Günlük sosyal medya süresi arttıkça not ortalaması yükselir (rakip)

- **Yapı:** X=`gunluk_sosyal_medya_saat` → Y=`not_ortalamasi` · ilişki=`positive` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.08 — Makul mekanizma yok → düşük
- **Toplam Bayes faktörü:** 0.034 (log₁₀ = -1.464) → **P = 0.003** (Ret)
- **Spektrum:** S = -1.000 (Güçlü çelişki) · uyum C = — · destekleyen/çelişen/nötr = 0/1/0
- **Duyarlılık:** P aralığı [0.002, 0.168] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 37.216

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D3 | data | pearson: gunluk_sosyal_medya_saat → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.790 | 0.014 | 0.034 | -1.000 | 100% | ok |

**Kapsam dışı bırakılan kanıtlar:** D4 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C7 — Günlük sosyal medya süresi ile not ortalaması arasında ilişki yoktur (rakip)

- **Yapı:** X=`gunluk_sosyal_medya_saat` → Y=`not_ortalamasi` · ilişki=`none` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.37 — Büyük çalışmalarda ihmal edilebilir etki raporlanıyor → kalan olasılık
- **Toplam Bayes faktörü:** 0.029 (log₁₀ = -1.535) → **P = 0.017** (Ret)
- **Spektrum:** S = -1.000 (Güçlü çelişki) · uyum C = — · destekleyen/çelişen/nötr = 0/1/0
- **Duyarlılık:** P aralığı [0.005, 0.151] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 6.492

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D3 | data | pearson: gunluk_sosyal_medya_saat → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.790 | 0.011 | 0.029 | -1.000 | 100% | ok |

**Kapsam dışı bırakılan kanıtlar:** D4 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C8 — Kız öğrencilerin not ortalaması erkeklerden yüksektir

- **Yapı:** X=`cinsiyet` → Y=`not_ortalamasi` · ilişki=`positive` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.55 — Okul notlarında kızlar lehine küçük fark literatürde yaygın (d≈0.2) ama örneklemden örnekleme değişir → 0.55
- **Toplam Bayes faktörü:** 0.061 (log₁₀ = -1.214) → **P = 0.069** (Ret)
- **Spektrum:** S = -1.000 (Güçlü çelişki) · uyum C = — · destekleyen/çelişen/nötr = 0/1/0
- **Duyarlılık:** P aralığı [0.012, 0.243] · karar sağlamlığı 67% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 1.488

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D5 | data | group_diff: cinsiyet → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.800 | 0.030 | 0.061 | -1.000 | 100% | ok |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C9 — Erkek öğrencilerin not ortalaması kızlardan yüksektir (rakip)

- **Yapı:** X=`cinsiyet` → Y=`not_ortalamasi` · ilişki=`negative` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.1 — Literatürle uyumsuz → düşük
- **Toplam Bayes faktörü:** 0.325 (log₁₀ = -0.488) → **P = 0.035** (Ret)
- **Spektrum:** S = -0.610 (Güçlü çelişki) · uyum C = — · destekleyen/çelişen/nötr = 0/1/0
- **Duyarlılık:** P aralığı [0.028, 0.550] · karar sağlamlığı 56% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 3.077

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D5 | data | group_diff: cinsiyet → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.800 | 0.245 | 0.325 | -0.610 | 100% | ok |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C10 — Cinsiyete göre not ortalaması farkı yoktur (rakip)

- **Yapı:** X=`cinsiyet` → Y=`not_ortalamasi` · ilişki=`none` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.35 — Fark küçük olduğu için tek okulda/örneklemde sıfıra yakın çıkabilir → kalan olasılık
- **Toplam Bayes faktörü:** 4.879 (log₁₀ = 0.688) → **P = 0.724** (Koşullu kabul)
- **Spektrum:** S = 0.860 (Güçlü destek) · uyum C = — · destekleyen/çelişen/nötr = 1/0/0
- **Duyarlılık:** P aralığı [0.542, 0.953] · karar sağlamlığı 22% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.9) geçmek için LR ≈ 3.425; alt banda (P<0.7) düşmek için LR ≈ 0.888

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D5 | data | group_diff: cinsiyet → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.800 | 7.252 | 4.879 | 0.860 | 100% | ok |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C11 — Uyku süresi ile not ortalaması arasında ilişki yoktur

- **Yapı:** X=`uyku_saat` → Y=`not_ortalamasi` · ilişki=`none` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.3 — Uyku–akademik başarı ilişkisi literatürde küçük-orta pozitif; 'ilişki yok' iddiası azınlık görüş → 0.30
- **Toplam Bayes faktörü:** 0.027 (log₁₀ = -1.570) → **P = 0.011** (Ret)
- **Spektrum:** S = -1.000 (Güçlü çelişki) · uyum C = — · destekleyen/çelişen/nötr = 0/1/0
- **Duyarlılık:** P aralığı [0.004, 0.143] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 9.624

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D6 | data | pearson: uyku_saat → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.785 | 0.010 | 0.027 | -1.000 | 100% | ok |

**Kapsam dışı bırakılan kanıtlar:** D7 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C12 — Uyku süresi arttıkça not ortalaması yükselir (rakip)

- **Yapı:** X=`uyku_saat` → Y=`not_ortalamasi` · ilişki=`positive` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.55 — Yeterli uyku–öğrenme mekanizması makul → 0.55
- **Toplam Bayes faktörü:** 37.119 (log₁₀ = 1.570) → **P = 0.978** (Kabul — uygulanabilir)
- **Spektrum:** S = 1.000 (Güçlü destek) · uyum C = — · destekleyen/çelişen/nötr = 1/0/0
- **Duyarlılık:** P aralığı [0.857, 0.996] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** alt banda (P<0.9) düşmek için LR ≈ 0.198

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D6 | data | pearson: uyku_saat → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.785 | 100.000 | 37.119 | 1.000 | 100% | ok |

**Kapsam dışı bırakılan kanıtlar:** D7 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C13 — Uyku süresi arttıkça not ortalaması düşer (rakip)

- **Yapı:** X=`uyku_saat` → Y=`not_ortalamasi` · ilişki=`negative` · nedensel=hayır · popülasyon: bu veri setindeki 240 öğrenci
- **Önsel P₀:** 0.15 — Az uyuyup çok çalışma ödünleşimi olası ama zayıf → 0.15
- **Toplam Bayes faktörü:** 0.034 (log₁₀ = -1.468) → **P = 0.006** (Ret)
- **Spektrum:** S = -1.000 (Güçlü çelişki) · uyum C = — · destekleyen/çelişen/nötr = 0/1/0
- **Duyarlılık:** P aralığı [0.003, 0.167] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 18.48

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D6 | data | pearson: uyku_saat → not_ortalamasi | X–Y çifti | istatistik | ogrenci_verisi | 0.785 | 0.013 | 0.034 | -1.000 | 100% | ok |

**Kapsam dışı bırakılan kanıtlar:** D7 (ilişkisel iddia: aynı veri kümesinde ham analiz var)

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

## 3. İddialar arası uyum

| İddialar | İlişkiler | Mantıksal uyum | P değerleri | Tutarsızlık | Not |
|---|---|---|---|---|---|
| C1 ↔ C2 | positive / negative | −1 çelişik | 0.987 / 0.002 | 0.000 |  |
| C1 ↔ C3 | positive / none | −1 çelişik | 0.987 / 0.010 | 0.000 |  |
| C2 ↔ C3 | negative / none | −1 çelişik | 0.002 / 0.010 | 0.000 |  |
| C4 ↔ C5 | negative / negative | 0 kısmi | 0.527 / 0.979 | — | Farklı kapsam (nedensel · bu veri setindeki 240 öğrenci / ilişkisel · bu veri setindeki 240 öğrenci): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C4 ↔ C6 | negative / positive | 0 kısmi | 0.527 / 0.003 | — | Farklı kapsam (nedensel · bu veri setindeki 240 öğrenci / ilişkisel · bu veri setindeki 240 öğrenci): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C4 ↔ C7 | negative / none | 0 kısmi | 0.527 / 0.017 | — | Farklı kapsam (nedensel · bu veri setindeki 240 öğrenci / ilişkisel · bu veri setindeki 240 öğrenci): ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz. |
| C5 ↔ C6 | negative / positive | −1 çelişik | 0.979 / 0.003 | 0.000 |  |
| C5 ↔ C7 | negative / none | −1 çelişik | 0.979 / 0.017 | 0.000 |  |
| C6 ↔ C7 | positive / none | −1 çelişik | 0.003 / 0.017 | 0.000 |  |
| C8 ↔ C9 | positive / negative | −1 çelişik | 0.069 / 0.035 | 0.000 |  |
| C8 ↔ C10 | positive / none | −1 çelişik | 0.069 / 0.724 | 0.000 |  |
| C9 ↔ C10 | negative / none | −1 çelişik | 0.035 / 0.724 | 0.000 |  |
| C11 ↔ C12 | none / positive | −1 çelişik | 0.011 / 0.978 | 0.000 |  |
| C11 ↔ C13 | none / negative | −1 çelişik | 0.011 / 0.006 | 0.000 |  |
| C12 ↔ C13 | positive / negative | −1 çelişik | 0.978 / 0.006 | 0.000 |  |

### Rakip hipotez setleri

Aynı kapsamda birbirini dışlayan iddialar. Kapsayıcı setlerde ΣP ≈ 1 olmalıdır; *normalize P* tutarlı olasılık dağılımıdır.

| Değişkenler | Kapsam | Hipotezler | P | ΣP | Normalize P | En olası | Açık |
|---|---|---|---|---|---|---|---|
| haftalik_calisma_saati – not_ortalamasi | ilişkisel · bu veri setindeki 240 öğrenci | C1:positive, C2:negative, C3:none | 0.987 / 0.002 / 0.010 | 0.999 | 0.988 / 0.002 / 0.010 | C1 | 0.001 |
| gunluk_sosyal_medya_saat – not_ortalamasi | ilişkisel · bu veri setindeki 240 öğrenci | C6:positive, C5:negative, C7:none | 0.003 / 0.979 / 0.017 | 0.999 | 0.003 / 0.980 / 0.017 | C5 | 0.001 |
| cinsiyet – not_ortalamasi | ilişkisel · bu veri setindeki 240 öğrenci | C8:positive, C9:negative, C10:none | 0.069 / 0.035 / 0.724 | 0.828 | 0.083 / 0.042 / 0.874 | C10 | 0.172 |
| not_ortalamasi – uyku_saat | ilişkisel · bu veri setindeki 240 öğrenci | C12:positive, C13:negative, C11:none | 0.978 / 0.006 / 0.011 | 0.995 | 0.983 / 0.006 / 0.011 | C12 | 0.005 |

## 4. Değişken özeti

| Değişken | İddialar | Ort. S | Ort. P |
|---|---|---|---|
| `haftalik_calisma_saati` | C1, C2, C3 | -0.333 | 0.333 |
| `not_ortalamasi` | C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13 | -0.252 | 0.334 |
| `gunluk_sosyal_medya_saat` | C4, C5, C6, C7 | -0.131 | 0.381 |
| `cinsiyet` | C8, C9, C10 | -0.250 | 0.276 |
| `uyku_saat` | C11, C12, C13 | -0.333 | 0.332 |

## 5. Yöntem

- Kanıt kalitesi **Q** ∈ [0,1]: tasarım taban puanı × düzelticiler (n, hakem, çıkar çatışması, replikasyon, yaş, doğrulama, nedensellik açığı). Her çarpan `metadata.json` içindeki `quality_trace`'te.
- Ham olabilirlik oranı: veri/raporlanan istatistik için BIC yaklaşımlı Bayes faktörü BF₁₀ = (1−r²)^(−n/2)/√n, yönlü iddiada işarete göre çevrilir; kaynak tutumu için güçlü=10, orta=4, zayıf=2. Tek kanıt |log₁₀ LR| ≤ 2.0 ile sınırlanır.
- Etkin LR = LR_ham^Q. Aynı kümedeki k kanıt ortalanıp k_eff = k/(1+(k−1)ρ) ile ölçeklenir (ρ = 0.5).
- P = σ(logit P₀ + Σ ln LR_küme). S = Σ Q·d / Σ Q, d = kırpılmış log₁₀ LR_ham ∈ [−1,1]. C = 1 − ağırlıklı standart sapma(d).
- Kapsam: değişken çifti kanıtı iddianın kapsamına göre seçilir — `controls` belirten iddia yalnızca aynı kontrollerle yapılmış analizi; ilişkisel iddia aynı veri kümesindeki ham analizi; nedensel iddia en kontrollü analizi kullanır. Gözlemsel kanıtın nedensel iddiaya desteği LR ≤ 3 ile sınırlanır.
- Karar bantları: P≥0.9 kabul · 0.7–0.9 koşullu · 0.3–0.7 belirsiz · 0.1–0.3 büyük olasılıkla yanlış · <0.1 ret.

## 6. Yorum ve Uygulama

### Danışmanın 4 iddiası — kısa karar

| # | Danışmanın iddiası | Test edilen iddia | S | P | Karar | Sonuç |
|---|---|---|---|---|---|---|
| 1 | Çok çalışanın notu yüksek | C1 | +1.00 | 0.987 | Kabul (sağlamlık %89) | **Tutuyor** |
| 2 | Sosyal medya notu düşürüyor | C5 (ilişki) / C4 (nedensel) | +1.00 / +0.48 | 0.979 / 0.527 | Kabul / Belirsiz | **Kısmen tutuyor:** ilişki var, "düşürüyor" (nedensellik) bu veriyle kanıtlanamaz |
| 3 | Kızlar erkeklerden başarılı | C8 | −1.00 | 0.069 | Ret (sağlamlık %67, P aralığı 0.012–0.243) | **Tutmuyor** |
| 4 | Uykunun notla alakası yok | C11 | −1.00 | 0.011 | Ret (sağlamlık %89) | **Tutmuyor:** tersine, uyku ile not arasında pozitif ilişki var (C12, P=0.978) |

### Ana bulgular
- **C1 güçlü desteklendi (S=+1.00, P=0.987, Kabul).** Haftalık çalışma saati ile not ortalaması arasında r=0.59 (%95 GA 0.50–0.67, n=240) var; bu "büyük" bir etki. Sosyal medya, uyku, okul türü ve cinsiyet sabitken de neredeyse aynı (kısmi r=0.61, haftada +1 saat çalışma ≈ +1.40 not puanı; D2). Yani ilişki bu değişkenlerden kaynaklanmıyor. Spearman (0.58) ve 100 alan 11 öğrenci çıkarılınca hesaplanan Pearson (0.58) da aynı sonucu veriyor.
- **Sosyal medya: ilişki kesin, nedensellik belirsiz.** C5 (ilişkisel) S=+1.00, P=0.979, Kabul. Ham r=−0.24 (%95 GA −0.36 ile −0.12, n=234). Ancak danışmanın "düşürüyor" ifadesi nedensel bir iddia: C4 için P=0.527 (Belirsiz, P aralığı 0.334–0.847, sağlamlık %67). Bunun iki nedeni var: (a) veri gözlemsel olduğu için destek LR≤3 tavanına takıldı (`causal_cap_applied`); (b) çalışma, uyku, okul ve cinsiyet kontrol edilince etki küçülüyor (kısmi r=−0.18, saat başına −1.57 puan, D4).
- **C8 desteklenmedi (S=−1.00, P=0.069, Ret).** Verinizde kızların ortalaması erkeklerden **düşük**: kızlar 78.7, erkekler 80.6, fark −1.9 puan, d=−0.16, p=0.22. Ama bu fark da anlamlı değil, o yüzden "erkekler daha başarılı" (C9) da desteklenmiyor (P=0.035). En olası hipotez "fark yok" (C10, P=0.724, normalize P=0.874). Ancak bu karar kırılgan (sağlamlık %22, P aralığı 0.542–0.953).
- **C11 reddedildi (S=−1.00, P=0.011, Ret).** Uyku ile not arasında r=+0.26 (%95 GA 0.14–0.38, n=231). Diğer değişkenler sabitken de sürüyor (kısmi r=+0.20, saat başına +2.23 puan, D7). Gruplara göre ortalama not: <6 saat uyuyan 73.8 (n=40) · 6–7 saat 79.0 · 7–8 saat 81.6 · ≥8 saat 83.2 (n=34). Karesel terim anlamsız (t=−0.1); yani "çok uyuyunca düşüyor" gibi ters U biçimli bir ilişki de görünmüyor.

### İddialar arası tutarlılık
- Dört rakip hipotez setinin üçünde ΣP≈1 (0.999 / 0.999 / 0.995). Bu üç sette kanıt hipotezleri net ayırıyor: çalışmada C1 (normalize 0.988), sosyal medyada C5 (0.980), uykuda C12 (0.983) öne çıkıyor.
- Cinsiyet setinde ΣP=0.828 (açık 0.172, bayrak eşiği 0.25'in altında). Bu, kanıtın hipotezleri tam ayırt edemediğini gösteriyor. n=240 ile "fark yok" en olası sonuç, ama küçük bir farkı dışlamak için örneklem sınırlı. Öte yandan literatürde kızlar lehine bildirilen d≈+0.2 düzeyindeki farkı veri büyük ölçüde dışlıyor: r'nin %95 GA üst sınırı 0.048, bu d≈+0.10'a karşılık geliyor.
- **Kapsamlar arası (C4 ↔ C5):** İki iddia çelişmiyor, ikisi aynı anda doğru olabilir. "İlişki var" (P=0.979) ama "neden olduğu kanıtlanmadı" (P=0.527). Sosyal medya ile uyku arasında r=−0.51 bulunuyor. Uyku kontrol edilmeden (yalnızca çalışma, okul ve cinsiyet sabitken) sosyal medya katsayısı −2.57 puan/saat (kısmi r=−0.31); uyku eklenince −1.57'ye düşüyor. Yani ilişkinin yaklaşık %40'ı uykuyla örtüşüyor. Bunun iki açıklaması olabilir: sosyal medya uykuyu kısaltıp notu dolaylı olarak etkiliyor olabilir (aracı değişken) ya da az uyuyan öğrenci daha çok sosyal medyada kalıyor olabilir (karıştırıcı). Kesitsel veri bu ikisini ayıramaz. Puanlamaya önceden belirlenen ve daha tutucu olan D4 modeli girdi. Uyku hariç model girilse de LR tavanı (3) yine bağlayıcı olurdu, dolayısıyla P değişmezdi.
- Çalışma saati sosyal medyayla (r=0.01) ve uykuyla (r=−0.01) ilişkisiz. Bu yüzden "çok çalışan az uyuyor, o yüzden uyku notu düşürüyor" türünden bir karışma bu veride yok.

### Sınırlılıklar
- `insufficient_evidence` (tüm iddialar): Tüm kanıt tek bir veri kümesinden (ogrenci_verisi) geliyor. Bağımsız küme sayısı 1 olduğu için betik bunu otomatik "ön bulgu" sayıyor. Sonuçlar **bu 240 öğrenci için** geçerli; başka okullara ve dönemlere genellemek için bağımsız veri gerekir.
- `no_counter_search` (tüm iddialar): Siz "benim verimle doğrula" dediğiniz için literatür ve kaynak araması yapılmadı. Önseller genel literatür bilgisiyle ve veriye bakılmadan belirlendi. Doğrulama yanlılığı riskini azaltmak için her iddiaya rakip hipotezler (pozitif / negatif / ilişki yok) eklendi ve tüm testler iki yönlü yapıldı.
- `causal_cap_applied`, `causal_gap` (C4): Gözlemsel veri nedenselliği tek başına kanıtlayamaz. C4'ün desteği LR=4.48'den 3'e indirildi ve kalite puanı ×0.6 ile çarpıldı (Q=0.466).
- `fragile_decision` (C4, C8, C9, C10): Bu iddiaların kararı önsel ve kalite varsayımlarına duyarlı. C8 tüm senaryolarda P≤0.243 kalıyor; yani "kızlar daha başarılı" iddiası hiçbir senaryoda desteklenmiyor, değişen yalnızca "ret" ile "büyük olasılıkla yanlış" arasındaki ayrım. C10 ("fark yok") ise 0.542–0.953 arasında oynuyor; kesin dille sunulmamalı.
- Veri kalitesi: 11 öğrencinin notu tam 100. Bu bir tavan etkisi ve ilişkileri hafifçe zayıflatabilir; ancak bu öğrenciler çıkarılınca sonuçlar değişmiyor (çalışma 0.58, sosyal medya −0.20, uyku 0.23). Sosyal medya verisinde %2.5 (6), uyku verisinde %3.75 (9) eksik değer var; liste bazlı silme uygulandı ve kalite puanına yansıtıldı. Süreler büyük olasılıkla öz-bildirim; ölçüm hatası ilişkileri zayıflatma yönünde etki eder.
- Revizyon: İlk çalıştırmadan sonra veri kanıtları `--relation` parametresi olmadan yeniden üretildi. Bu yalnızca yapay `relation_mismatch` bayraklarını kaldırdı, sayılar değişmedi (bkz. `project.revisions`).

### Uygulama önerileri
| İddia | Karar | Önerilen eylem | Koşul / izlenecek gösterge |
|---|---|---|---|
| C1 çalışma → not | Kabul (P=0.987) | Danışmanla paylaşılabilir. "Bu örneklemde haftada +1 saat çalışma ≈ +1.4 puan" diye raporlayın | Nedensel yorum için dikkatli olun (ör. motivasyon her ikisini de etkileyebilir); yeni dönem verisiyle tekrar edin |
| C5 / C4 sosyal medya | Kabul (ilişki) / Belirsiz (nedensellik) | "Sosyal medya süresi yüksek olanların notu daha düşük" demek uygun. "Düşürüyor" demek bu veriyle **erken** | Uyku aracılığını raporlayın; nedensellik için boylamsal ya da deneysel veri gerekir |
| C8 kızlar daha başarılı | Ret (P=0.069) | Bu veriye dayanarak bu iddia kullanılmamalı. Danışmana verinin kızlar lehine bir fark göstermediğini (sayısal olarak erkekler +1.9 puan önde, anlamsız) iletin | Daha büyük örneklemde ya da ders bazında yeniden bakılabilir |
| C11 uykunun alakası yok | Ret (P=0.011) | İddia veriyle çelişiyor. Raporda "uyku süresi notla pozitif ilişkili (r=0.26); <6 saat uyuyanların ortalaması ≥8 saat uyuyanlardan 9.4 puan düşük" diye düzeltin | Diğer değişkenler sabitken de (kısmi r=0.20) sürüyor |

### Sonraki en değerli kanıt
- **C4 (sosyal medya nedenselliği), LR≈2.1 ile bir üst banda geçiyor:** "bir çalışma uzaklıkta." En değerli kanıt, aynı öğrencilerin dönemler arası sosyal medya değişimiyle not değişimini karşılaştıran boylamsal (sabit etkili) bir veri olur. Daha da güçlüsü, sosyal medya kısıtlama müdahalesini rastgele atayan küçük bir deney olur (rct, Q≈0.9). Tek bir orta güçte bağımsız deneysel kanıt (LR≈4) yeterli. Ters yönde LR≈0.39'luk bir sıfır sonuç da iddiayı "büyük olasılıkla yanlış" bandına indirir.
- **C10 ("cinsiyet farkı yok"), kabul bandı için LR≈3.4 gerekiyor:** Kurumsal not kayıtlarından n≥1000'lik bağımsız bir örneklem cinsiyet sorusunu netleştirir.
- C1, C5, C11 ve C12 için karar bandı ancak çok güçlü karşı kanıtla değişir (C11'in üst banda geçmesi için LR≈9.6 gerekir). Bu iddialar için ek veri toplamanın getirisi düşük.
