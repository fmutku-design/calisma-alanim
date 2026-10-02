# İddia Doğrulama Raporu — Danışman iddiaları — öğrenci verisi (n=240) ile doğrulama

**Araştırma sorusu:** Danışmanın toplantıda öne sürdüğü 4 iddia (çalışma saati, sosyal medya, cinsiyet, uyku → not ortalaması) kullanıcının 240 öğrencilik verisinde destekleniyor mu?  
**Tarih:** 2026-10-02 · **Şema:** v1.0 · **İddia sayısı:** 9 · **Kanıt sayısı:** 7

> **Nasıl okunur:** *S* (−1…+1) kalite-ağırlıklı kanıtların iddiayı ne yönde ve ne güçte desteklediğini gösterir. *P* önsel olasılığın kanıtların olabilirlik oranlarıyla Bayesçi güncellenmesiyle elde edilen sonsal olasılıktır. *C* (0…1) kanıtların kendi aralarındaki uyumudur. *Sağlamlık*, 27 duyarlılık senaryosunun kaçında kararın değişmediğidir.

## 1. Özet

| ID | İddia | S | Spektrum | P | Karar | C | Kalite | Sağlamlık | Uyarı |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Haftada daha çok çalışan öğrencinin not ortalaması daha yüksektir | 1.000 | Güçlü destek | 0.997 | Kabul — uygulanabilir | 1.000 | Yüksek | 96% | 2 |
| C1R | (Rakip) Haftalık çalışma saati ile not ortalaması arasında ilişki yoktur | -1.000 | Güçlü çelişki | 0.003 | Ret | 1.000 | Yüksek | 96% | 2 |
| C2 | Sosyal medya kullanımı notları düşürür (nedensel) | 0.827 | Güçlü destek | 0.848 | Koşullu kabul | 0.826 | Düşük | 37% | 5 |
| C2A | Daha çok sosyal medya kullanan öğrencilerin not ortalaması daha düşüktür (ilişkisel) | 0.827 | Güçlü destek | 0.974 | Kabul — uygulanabilir | 0.826 | Yüksek | 82% | 3 |
| C2R | (Rakip) Sosyal medya kullanımı ile not ortalaması arasında ilişki yoktur | -0.679 | Güçlü çelişki | 0.040 | Ret | 0.676 | Yüksek | 82% | 3 |
| C3 | Kız öğrenciler erkek öğrencilerden daha başarılıdır (daha yüksek not ortalaması) | -1.000 | Güçlü çelişki | 0.102 | Büyük olasılıkla yanlış | — | Yüksek | 44% | 3 |
| C3R | (Rakip) Kız ve erkek öğrencilerin not ortalamaları arasında fark yoktur | 0.860 | Güçlü destek | 0.724 | Koşullu kabul | — | Yüksek | 22% | 3 |
| C4 | Uyku süresinin not ortalamasıyla bir ilişkisi yoktur | -0.899 | Güçlü çelişki | 0.018 | Ret | 0.899 | Yüksek | 89% | 3 |
| C4R | (Rakip) Daha çok uyuyan öğrencilerin not ortalaması daha yüksektir | 1.000 | Güçlü destek | 0.984 | Kabul — uygulanabilir | 1.000 | Yüksek | 89% | 3 |

### Spektrum görünümü

```
C1   −1 ──────────┼─────────● +1  S=+1.00  P=1.00
C1R  −1 ●─────────┼────────── +1  S=-1.00  P=0.00
C2   −1 ──────────┼───────●── +1  S=+0.83  P=0.85
C2A  −1 ──────────┼───────●── +1  S=+0.83  P=0.97
C2R  −1 ───●──────┼────────── +1  S=-0.68  P=0.04
C3   −1 ●─────────┼────────── +1  S=-1.00  P=0.10
C3R  −1 ──────────┼────────●─ +1  S=+0.86  P=0.72
C4   −1 ─●────────┼────────── +1  S=-0.90  P=0.02
C4R  −1 ──────────┼─────────● +1  S=+1.00  P=0.98
```

## 2. İddia ayrıntıları

### C1 — Haftada daha çok çalışan öğrencinin not ortalaması daha yüksektir

- **Yapı:** X=`haftalik_calisma_saati` → Y=`not_ortalamasi` · ilişki=`positive` · nedensel=hayır · popülasyon: veri setindeki 240 öğrenci
- **Önsel P₀:** 0.7 — Çalışma süresi–başarı arasında pozitif ilişki yaygın olarak beklenir; ancak literatürde ilişkinin beklenenden zayıf olduğu (çalışmanın niteliği önemli) bilinir → yerleşik ama tartışmasız değil: 0.70
- **Toplam Bayes faktörü:** 126.590 (log₁₀ = 2.102) → **P = 0.997** (Kabul — uygulanabilir)
- **Spektrum:** S = 1.000 (Güçlü destek) · uyum C = 1.000 · destekleyen/çelişen/nötr = 2/0/0
- **Duyarlılık:** P aralığı [0.894, 1.000] · karar sağlamlığı 96% (27 senaryo)
- **Bilginin değeri:** alt banda (P<0.9) düşmek için LR ≈ 0.03

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | data | pearson: haftalik_calisma_saati → not_ortalamasi | X–Y çifti | istatistik | ogrenci_veri | 0.800 | 100.000 | 39.811 | 1.000 | 51% | ok |
| D2 | data | regression: haftalik_calisma_saati → not_ortalamasi; kontroller: gunluk_sosyal_medya_saat, uyku_saat, cinsiyet, okul_turu | X–Y çifti | istatistik | ogrenci_veri | 0.777 | 100.000 | 35.777 | 1.000 | 49% | ok |

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C1R — (Rakip) Haftalık çalışma saati ile not ortalaması arasında ilişki yoktur

- **Yapı:** X=`haftalik_calisma_saati` → Y=`not_ortalamasi` · ilişki=`none` · nedensel=hayır · popülasyon: veri setindeki 240 öğrenci
- **Önsel P₀:** 0.3 — C1'in tümleyenine yakın rakip
- **Toplam Bayes faktörü:** 0.008 (log₁₀ = -2.102) → **P = 0.003** (Ret)
- **Spektrum:** S = -1.000 (Güçlü çelişki) · uyum C = 1.000 · destekleyen/çelişen/nötr = 0/2/0
- **Duyarlılık:** P aralığı [0.000, 0.106] · karar sağlamlığı 96% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 32.82

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | data | pearson: haftalik_calisma_saati → not_ortalamasi | X–Y çifti | istatistik | ogrenci_veri | 0.800 | 0.010 | 0.025 | -1.000 | 51% | ok |
| D2 | data | regression: haftalik_calisma_saati → not_ortalamasi; kontroller: gunluk_sosyal_medya_saat, uyku_saat, cinsiyet, okul_turu | X–Y çifti | istatistik | ogrenci_veri | 0.777 | 0.010 | 0.028 | -1.000 | 49% | ok |

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C2 — Sosyal medya kullanımı notları düşürür (nedensel)

- **Yapı:** X=`gunluk_sosyal_medya_saat` → Y=`not_ortalamasi` · ilişki=`negative` · nedensel=evet · popülasyon: veri setindeki 240 öğrenci
- **Önsel P₀:** 0.45 — Nedensel iddia ilişkisel olandan daha güçlüdür; literatürde sosyal medya–akademik başarı ilişkisi küçük ve tartışmalı, nedensellik zayıf kanıtlı → 0.45
- **Toplam Bayes faktörü:** 6.834 (log₁₀ = 0.835) → **P = 0.848** (Koşullu kabul)
- **Spektrum:** S = 0.827 (Güçlü destek) · uyum C = 0.826 · destekleyen/çelişen/nötr = 2/0/0
- **Duyarlılık:** P aralığı [0.546, 0.990] · karar sağlamlığı 37% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.9) geçmek için LR ≈ 1.61; alt banda (P<0.7) düşmek için LR ≈ 0.417

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D3 | data | pearson: gunluk_sosyal_medya_saat → not_ortalamasi | X–Y çifti | istatistik | ogrenci_veri | 0.474 | 100.000 | 8.881 | 1.000 | 76% | causal_gap |
| D4 | data | regression: gunluk_sosyal_medya_saat → not_ortalamasi; kontroller: haftalik_calisma_saati, uyku_saat, cinsiyet, okul_turu | X–Y çifti | istatistik | ogrenci_veri | 0.466 | 4.480 | 2.012 | 0.651 | 24% | causal_gap |

**Uyarılar:**
- `causal_gap` — Nedensel iddia, nedensellik kuramayan tasarımlarla destekleniyor.
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).
- `single_source_dominance` — Tek bir kanıt toplam etkinin çoğunu taşıyor; sonuç ona bağımlı.

### C2A — Daha çok sosyal medya kullanan öğrencilerin not ortalaması daha düşüktür (ilişkisel)

- **Yapı:** X=`gunluk_sosyal_medya_saat` → Y=`not_ortalamasi` · ilişki=`negative` · nedensel=hayır · popülasyon: veri setindeki 240 öğrenci
- **Önsel P₀:** 0.6 — Küçük negatif ilişki makul ve sık raporlanır ama tartışmalı → 0.60
- **Toplam Bayes faktörü:** 24.613 (log₁₀ = 1.391) → **P = 0.974** (Kabul — uygulanabilir)
- **Spektrum:** S = 0.827 (Güçlü destek) · uyum C = 0.826 · destekleyen/çelişen/nötr = 2/0/0
- **Duyarlılık:** P aralığı [0.738, 0.999] · karar sağlamlığı 82% (27 senaryo)
- **Bilginin değeri:** alt banda (P<0.9) düşmek için LR ≈ 0.244

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D3 | data | pearson: gunluk_sosyal_medya_saat → not_ortalamasi | X–Y çifti | istatistik | ogrenci_veri | 0.790 | 100.000 | 38.089 | 1.000 | 76% | ok |
| D4 | data | regression: gunluk_sosyal_medya_saat → not_ortalamasi; kontroller: haftalik_calisma_saati, uyku_saat, cinsiyet, okul_turu | X–Y çifti | istatistik | ogrenci_veri | 0.777 | 4.480 | 3.206 | 0.651 | 24% | ok |

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).
- `single_source_dominance` — Tek bir kanıt toplam etkinin çoğunu taşıyor; sonuç ona bağımlı.

### C2R — (Rakip) Sosyal medya kullanımı ile not ortalaması arasında ilişki yoktur

- **Yapı:** X=`gunluk_sosyal_medya_saat` → Y=`not_ortalamasi` · ilişki=`none` · nedensel=hayır · popülasyon: veri setindeki 240 öğrenci
- **Önsel P₀:** 0.4 — C2A'nın rakibi; büyük çalışmalarda ihmal edilebilir etkiler de raporlanır
- **Toplam Bayes faktörü:** 0.062 (log₁₀ = -1.206) → **P = 0.040** (Ret)
- **Spektrum:** S = -0.679 (Güçlü çelişki) · uyum C = 0.676 · destekleyen/çelişen/nötr = 0/2/0
- **Duyarlılık:** P aralığı [0.002, 0.320] · karar sağlamlığı 82% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 2.679

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D3 | data | pearson: gunluk_sosyal_medya_saat → not_ortalamasi | X–Y çifti | istatistik | ogrenci_veri | 0.790 | 0.011 | 0.029 | -1.000 | 85% | ok |
| D4 | data | regression: gunluk_sosyal_medya_saat → not_ortalamasi; kontroller: haftalik_calisma_saati, uyku_saat, cinsiyet, okul_turu | X–Y çifti | istatistik | ogrenci_veri | 0.777 | 0.444 | 0.533 | -0.352 | 15% | ok |

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).
- `single_source_dominance` — Tek bir kanıt toplam etkinin çoğunu taşıyor; sonuç ona bağımlı.

### C3 — Kız öğrenciler erkek öğrencilerden daha başarılıdır (daha yüksek not ortalaması)

- **Yapı:** X=`cinsiyet` → Y=`not_ortalamasi` · ilişki=`positive` · nedensel=hayır · popülasyon: veri setindeki 240 öğrenci
- **Önsel P₀:** 0.65 — Okul notlarında kızların küçük bir farkla önde olduğu yaygın bir bulgudur, ancak fark küçüktür ve örnekleme göre değişir → 0.65
- **Toplam Bayes faktörü:** 0.061 (log₁₀ = -1.214) → **P = 0.102** (Büyük olasılıkla yanlış)
- **Spektrum:** S = -1.000 (Güçlü çelişki) · uyum C = — · destekleyen/çelişen/nötr = 0/1/0
- **Duyarlılık:** P aralığı [0.012, 0.243] · karar sağlamlığı 44% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.3) geçmek için LR ≈ 3.777; alt banda (P<0.1) düşmek için LR ≈ 0.979

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D5 | data | group_diff: cinsiyet → not_ortalamasi | X–Y çifti | istatistik | ogrenci_veri | 0.800 | 0.030 | 0.061 | -1.000 | 100% | ok |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C3R — (Rakip) Kız ve erkek öğrencilerin not ortalamaları arasında fark yoktur

- **Yapı:** X=`cinsiyet` → Y=`not_ortalamasi` · ilişki=`none` · nedensel=hayır · popülasyon: veri setindeki 240 öğrenci
- **Önsel P₀:** 0.35 — C3'ün rakibi
- **Toplam Bayes faktörü:** 4.879 (log₁₀ = 0.688) → **P = 0.724** (Koşullu kabul)
- **Spektrum:** S = 0.860 (Güçlü destek) · uyum C = — · destekleyen/çelişen/nötr = 1/0/0
- **Duyarlılık:** P aralığı [0.542, 0.953] · karar sağlamlığı 22% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.9) geçmek için LR ≈ 3.425; alt banda (P<0.7) düşmek için LR ≈ 0.888

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D5 | data | group_diff: cinsiyet → not_ortalamasi | X–Y çifti | istatistik | ogrenci_veri | 0.800 | 7.252 | 4.879 | 0.860 | 100% | ok |

**Uyarılar:**
- `fragile_decision` — Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).

### C4 — Uyku süresinin not ortalamasıyla bir ilişkisi yoktur

- **Yapı:** X=`uyku_saat` → Y=`not_ortalamasi` · ilişki=`none` · nedensel=hayır · popülasyon: veri setindeki 240 öğrenci
- **Önsel P₀:** 0.35 — Literatürde uyku süresi/kalitesi ile akademik başarı arasında genellikle küçük pozitif ilişki raporlanır; 'hiç ilişki yok' iddiası bu beklentiye aykırı → 0.35
- **Toplam Bayes faktörü:** 0.035 (log₁₀ = -1.459) → **P = 0.018** (Ret)
- **Spektrum:** S = -0.899 (Güçlü çelişki) · uyum C = 0.899 · destekleyen/çelişen/nötr = 0/2/0
- **Duyarlılık:** P aralığı [0.001, 0.242] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** üst banda (P≥0.1) geçmek için LR ≈ 5.943

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D6 | data | pearson: uyku_saat → not_ortalamasi | X–Y çifti | istatistik | ogrenci_veri | 0.785 | 0.010 | 0.027 | -1.000 | 72% | ok |
| D7 | data | regression: uyku_saat → not_ortalamasi; kontroller: haftalik_calisma_saati, gunluk_sosyal_medya_saat, cinsiyet, okul_turu | X–Y çifti | istatistik | ogrenci_veri | 0.777 | 0.159 | 0.240 | -0.797 | 28% | ok |

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).
- `single_source_dominance` — Tek bir kanıt toplam etkinin çoğunu taşıyor; sonuç ona bağımlı.

### C4R — (Rakip) Daha çok uyuyan öğrencilerin not ortalaması daha yüksektir

- **Yapı:** X=`uyku_saat` → Y=`not_ortalamasi` · ilişki=`positive` · nedensel=hayır · popülasyon: veri setindeki 240 öğrenci
- **Önsel P₀:** 0.6 — Literatürdeki küçük pozitif ilişki beklentisi
- **Toplam Bayes faktörü:** 41.205 (log₁₀ = 1.615) → **P = 0.984** (Kabul — uygulanabilir)
- **Spektrum:** S = 1.000 (Güçlü destek) · uyum C = 1.000 · destekleyen/çelişen/nötr = 2/0/0
- **Duyarlılık:** P aralığı [0.799, 1.000] · karar sağlamlığı 89% (27 senaryo)
- **Bilginin değeri:** alt banda (P<0.9) düşmek için LR ≈ 0.146

| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D6 | data | pearson: uyku_saat → not_ortalamasi | X–Y çifti | istatistik | ogrenci_veri | 0.785 | 100.000 | 37.119 | 1.000 | 65% | ok |
| D7 | data | regression: uyku_saat → not_ortalamasi; kontroller: haftalik_calisma_saati, gunluk_sosyal_medya_saat, cinsiyet, okul_turu | X–Y çifti | istatistik | ogrenci_veri | 0.777 | 12.528 | 7.126 | 1.000 | 35% | ok |

**Uyarılar:**
- `insufficient_evidence` — Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.
- `no_counter_search` — Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).
- `single_source_dominance` — Tek bir kanıt toplam etkinin çoğunu taşıyor; sonuç ona bağımlı.

## 3. İddialar arası uyum

| İddialar | İlişkiler | Mantıksal uyum | P değerleri | Tutarsızlık | Not |
|---|---|---|---|---|---|
| C1 ↔ C1R | positive / none | −1 çelişik | 0.997 / 0.003 | 0.000 |  |
| C2 ↔ C2A | negative / negative | +1 uyumlu | 0.848 / 0.974 | — |  |
| C2 ↔ C2R | negative / none | −1 çelişik | 0.848 / 0.040 | 0.000 |  |
| C2A ↔ C2R | negative / none | −1 çelişik | 0.974 / 0.040 | 0.014 |  |
| C3 ↔ C3R | positive / none | −1 çelişik | 0.102 / 0.724 | 0.000 |  |
| C4 ↔ C4R | none / positive | −1 çelişik | 0.018 / 0.984 | 0.002 |  |

## 4. Değişken özeti

| Değişken | İddialar | Ort. S | Ort. P |
|---|---|---|---|
| `haftalik_calisma_saati` | C1, C1R | 0.000 | 0.500 |
| `not_ortalamasi` | C1, C1R, C2, C2A, C2R, C3, C3R, C4, C4R | 0.104 | 0.521 |
| `gunluk_sosyal_medya_saat` | C2, C2A, C2R | 0.325 | 0.621 |
| `cinsiyet` | C3, C3R | -0.070 | 0.413 |
| `uyku_saat` | C4, C4R | 0.050 | 0.501 |

## 5. Yöntem

- Kanıt kalitesi **Q** ∈ [0,1]: tasarım taban puanı × düzelticiler (n, hakem, çıkar çatışması, replikasyon, yaş, doğrulama, nedensellik açığı). Her çarpan `metadata.json` içindeki `quality_trace`'te.
- Ham olabilirlik oranı: veri/raporlanan istatistik için BIC yaklaşımlı Bayes faktörü BF₁₀ = (1−r²)^(−n/2)/√n, yönlü iddiada işarete göre çevrilir; kaynak tutumu için güçlü=10, orta=4, zayıf=2. Tek kanıt |log₁₀ LR| ≤ 2.0 ile sınırlanır.
- Etkin LR = LR_ham^Q. Aynı kümedeki k kanıt ortalanıp k_eff = k/(1+(k−1)ρ) ile ölçeklenir (ρ = 0.5).
- P = σ(logit P₀ + Σ ln LR_küme). S = Σ Q·d / Σ Q, d = kırpılmış log₁₀ LR_ham ∈ [−1,1]. C = 1 − ağırlıklı standart sapma(d).
- Karar bantları: P≥0.9 kabul · 0.7–0.9 koşullu · 0.3–0.7 belirsiz · 0.1–0.3 büyük olasılıkla yanlış · <0.1 ret.

## 6. Yorum ve Uygulama

### Ana bulgular
- **İddia 1 — çalışma saati → not (C1): TUTUYOR.** S=+1.00, P=0.997, Kabul; sağlamlık %96 (P aralığı 0.894–1.000). Pearson r=0.59 (%95 GA 0.50–0.67, n=240); diğer değişkenler sabitken kısmi r=0.61, haftada +1 saat çalışma ≈ +1.40 puan not ortalaması (D2). Rakip "ilişki yok" iddiası (C1R) P=0.003 ile reddedildi. Dört iddia içinde açık ara en güçlü ilişki budur.
- **İddia 2 — sosyal medya notları düşürüyor: İLİŞKİ TUTUYOR, NEDENSELLİK KANITLANMADI.** İlişkisel versiyon C2A: S=+0.83, P=0.974, Kabul (r=−0.24, %95 GA −0.36…−0.12, n=234; diğer değişkenler sabitken kısmi r=−0.18, günde +1 saat ≈ −1.57 puan). Danışmanın söylediği nedensel hâli C2 ise P=0.848 "Koşullu kabul" ama sağlamlığı yalnızca %37 (P aralığı 0.546–0.990) ve `causal_gap` bayrağı var: kesitsel veriyle "düşürüyor" denemez, "daha düşük notla birlikte görülüyor" denebilir.
- **İddia 3 — kızlar daha başarılı (C3): TUTMUYOR.** S=−1.00, P=0.102, "Büyük olasılıkla yanlış" (P<0.10 ret sınırının hemen üstünde). Bu veride kızların ortalaması 78.71, erkeklerin 80.64 — yön iddianın tersi, ama fark küçük ve istatistiksel olarak belirgin değil (d=−0.16, Welch p=0.22). Doğru okuma "erkekler daha başarılı" değil, "anlamlı bir fark yok"tur: rakip C3R ("fark yok") P=0.724, Koşullu kabul. Her iki kararın sağlamlığı düşük (%44 ve %22), çünkü tek ve küçük-etkili bir testten geliyor.
- **İddia 4 — uykunun notla alakası yok (C4): TUTMUYOR.** S=−0.90, P=0.018, Ret; sağlamlık %89. Uyku ile not arasında pozitif ilişki var: r=0.26 (%95 GA 0.14–0.38, n=231), diğer değişkenler sabitken kısmi r=0.20 (gecelik +1 saat ≈ +2.23 puan). Rakip C4R ("daha çok uyuyanın notu daha yüksek") P=0.984, Kabul.

### İddialar arası tutarlılık
- Tüm çelişik çiftlerde (C1↔C1R, C2A↔C2R, C3↔C3R, C4↔C4R) tutarsızlık ≤ 0.014 → olasılıklar mantıksal olarak tutarlı; eşik (0.1) aşılmıyor.
- C2 (nedensel) ile C2A (ilişkisel) uyumlu ama P farkı 0.974 → 0.848: aynı veri, nedensel iddia için kalite cezası (×0.6) aldığı için daha az kanıt değeri taşıyor. Fark tamamen "korelasyon ≠ nedensellik" kaynaklı.
- **Sosyal medya ve uyku birbirine bağlı:** günlük sosyal medya ile uyku süresi arasında r=−0.51 (sağlamlık kontrolü, kanıt olarak girilmedi). Sosyal medyanın nota ilişkisi uyku ve diğer değişkenler kontrol edilince r=−0.24'ten kısmi r=−0.18'e iniyor. Yani sosyal medyanın nota "etkisi"nin bir kısmı uyku üzerinden geçiyor olabilir (aracı değişken) veya ikisi ortak bir nedene bağlı olabilir; bu veriyle ayırt edilemez. Danışmanın 2. ve 4. iddiaları bu açıdan birbiriyle çelişiyor: sosyal medya notu düşürüyorsa ve bunu kısmen uykuyu azaltarak yapıyorsa, uykunun notla "alakasız" olması beklenmez — veride de alakasız değil.
- Çalışma saati sosyal medyadan bağımsız (r=0.01) ve okul türü/cinsiyet gruplarında benzer (p=0.93, p=0.28); bu yüzden C1'in kontrollü ve kontrolsüz sonuçları neredeyse aynı (r=0.59 → kısmi r=0.61).

### Sağlamlık kontrolleri (kanıt olarak sayılmadı, yalnızca teyit için)
- Spearman (sıra) korelasyonları Pearson ile aynı yönde ve büyüklükte: çalışma 0.58, sosyal medya −0.26, uyku 0.23 → sonuçlar aykırı değerlere veya 100 puan tavanına (11 öğrenci) bağlı değil.
- Uyku–not ilişkisinde doğrusal olmama yok (karesel terim t=−0.10); gruplar: <6 saat 73.8, 6–7 saat ≈79, 7–7.5 saat 80.6, ≥7.5 saat 83.2. Çalışma saatinde azalan getiri işareti zayıf ve anlamsız (karesel terim t=−1.38).
- Okul türü notu anlamlı biçimde değiştirmiyor (devlet 78.9, özel 80.5; p=0.32).
- Eksik veri az (sosyal medya 6, uyku 9 satır; en fazla %6 regresyonlarda); eksik satırların not ortalaması biraz daha yüksek (≈82–83) ama bu sayı sonuçları değiştirecek büyüklükte değil.

### Sınırlılıklar
- `insufficient_evidence` (tüm iddialar): tüm kanıtlar tek bir veri setinden (tek bağımsız küme) geliyor. Sonuçlar "bu 240 öğrencide" geçerlidir; başka okul/sınıflara genellemek için ikinci bir veri seti gerekir.
- `no_counter_search` (tüm iddialar): kullanıcı "benim verimle doğrula" dediği için literatür taraması yapılmadı; önseller genel alan bilgisine dayanıyor. Duyarlılık analizi önsel 0.25–0.75 arasında değişince kararların çoğunun korunduğunu gösteriyor (C1 %96, C4/C4R %89, C2A %82).
- `single_source_dominance` (C2A, C2R, C2, C4, C4R): kontrolsüz Pearson testi etkinin %65–85'ini taşıyor; kontrollü regresyon aynı yönde ama daha zayıf (ör. C2A için LR 100 → 4.5). Kontrollü sonuç tek başına da aynı yöndedir.
- `causal_gap` (C2): veri gözlemsel ve kesitsel; ters nedensellik (notu düşük olan öğrencinin sosyal medyaya kaçması) ve ölçülmemiş karıştırıcılar dışlanamaz.
- `fragile_decision` (C2, C3, C3R): bu kararlar önsel/ρ/kalite varsayımlarına duyarlı; kesin dille sunulmamalı. C3'te sağlam olan kısım "kızlar daha başarılı" bulgusunun **bu veride görülmemesi**dir (P aralığı 0.012–0.243, hiçbir senaryoda 0.30'u geçmiyor).
- Varsayım: "başarı" = `not_ortalamasi`; öz-bildirim değişkenleri (çalışma, sosyal medya, uyku saati) ölçüm hatası içerebilir — bu, ilişkileri genelde olduğundan zayıf gösterir.

### Uygulama önerileri
| İddia | Karar | Önerilen eylem | Koşul / izlenecek gösterge |
|---|---|---|---|
| C1 çalışma → not | Kabul (P=0.997) | Danışmanın 1. iddiası verinle destekleniyor; tezde/raporda ilişkisel dille kullanılabilir ("r=0.59") | İlişki nedensel değil; çalışma niteliği ölçülmedi |
| C2A / C2 sosyal medya → not | İlişkisel: Kabul (0.974); nedensel: Koşullu (0.848, kırılgan) | "Sosyal medya kullanımı daha düşük notlarla ilişkili" de; "düşürüyor" deme | Uyku aracı rolü; boylamsal veya müdahale verisi olmadan nedensel dil kullanma |
| C3 kızlar daha başarılı | Büyük olasılıkla yanlış (0.102) | Danışmana bu veride farkın olmadığını (yön tersine bile, d=−0.16, p=0.22) bildir | Grup büyüklükleri 119/121; küçük farkları yakalamak için daha büyük örneklem gerekir |
| C4 uyku alakasız | Ret (0.018) | İddia bu veriyle çürütülüyor; uyku süresi notla pozitif ilişkili (r=0.26), modellerde kontrol değişkeni olarak tutulmalı | Sosyal medya ile uyku arasındaki r=−0.51 ilişkiyi analizlerde dikkate al |

### Sonraki en değerli kanıt
- **C2 (nedensel sosyal medya, P=0.848):** kabul bandına (P≥0.9) çıkması için yalnızca LR≈1.61 gerekiyor, ama bu LR'nin nedensel tasarımdan gelmesi anlamlı olur: aynı öğrencileri dönem başı/sonu izleyen boylamsal veri (sosyal medya değişimi → not değişimi) ya da sosyal medya kısıtlama müdahalesi (randomize, n≥100). Bu, aynı zamanda uykunun aracı rolünü test etmeyi sağlar.
- **C3 / C3R (cinsiyet, P=0.102 / 0.724):** C3R'nin kabul bandına çıkması için LR≈3.43, C3'ün belirsiz banda dönmesi için LR≈3.78 gerekiyor — "bir çalışma uzaklıkta". Küçük farkları (d≈0.2) ayırt etmek için grup başına ≈400 öğrenci gereken bağımsız bir örneklem veya ilgili okul/bölümün resmî not istatistikleri en değerli ek kanıt olur.
- C1, C1R, C4, C4R ve C2A kendi uç bantlarında; karar bandını değiştirmek için çok güçlü karşı kanıt gerekir (ör. C4 için LR≈5.9, C1 için LR≈0.03), bu yüzden öncelikli değil.
