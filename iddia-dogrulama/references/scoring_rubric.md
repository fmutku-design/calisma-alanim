# Puanlama Kuralları (Rubric)

Bu belge `score_claims.py`'nin her sayıyı nasıl ürettiğini ve **neden** öyle ürettiğini açıklar.
Kanıtları kodlarken (stance, strength, design…) bu tablolara bakın; sonuçları yorumlarken
de buradaki gerekçelere dayanın.

## İçindekiler
1. Kanıt kalitesi Q
2. Olabilirlik oranı (LR)
3. Bağımlı kanıtlar (kümeler) ve kapsam (ham / kontrollü / nedensel)
4. Sonsal olasılık P ve rakip hipotez setleri
5. Spektrum skoru S ve uyum C
6. Karar bantları
7. Duyarlılık ve bilginin değeri
8. Bayraklar
9. Önsel olasılık seçimi

---

## 1. Kanıt kalitesi Q ∈ [0, 1]

Q = tasarım taban puanı × düzelticiler, sonra [0,1]'e kırpılır. Her çarpım `quality_trace`'e
yazılır; böylece "bu kaynak neden 0.43 aldı?" sorusu her zaman yanıtlanabilir.

### Tasarım taban puanları (`design`)

| design | Taban | Ne zaman |
|---|---|---|
| `meta_analysis` | 0.95 | Birden çok çalışmanın nicel birleşimi |
| `systematic_review` | 0.90 | Protokollü sistematik derleme |
| `rct` | 0.90 | Rastgele kontrollü deney |
| `quasi_experimental` | 0.75 | Doğal deney, fark-farkı, RDD, araç değişken |
| `cohort` / `longitudinal` | 0.70 | Zaman içinde izlenen örneklem |
| `official_statistics` | 0.70 | TÜİK, Eurostat, OECD vb. resmî veri |
| `case_control` | 0.60 | Vaka-kontrol |
| `textbook` | 0.60 | Yerleşik ders kitabı / el kitabı |
| `cross_sectional` | 0.50 | Tek zamanlı anket/gözlem |
| `qualitative` | 0.40 | Görüşme, odak grup |
| `case_study` | 0.35 | Tek vaka |
| `expert_opinion` | 0.30 | Uzman görüşü, pozisyon yazısı |
| `news` | 0.20 | Haber |
| `blog` | 0.15 | Blog, sosyal medya |
| `anecdote` | 0.10 | Kişisel deneyim |
| `unknown` | 0.25 | Tasarım belirlenemedi |

Veri analizi kanıtı (`kind: "data"`): gözlemsel 0.80, deneysel (`experimental: true`) 0.90.
Taban yüksek çünkü veriyi doğrudan görüyoruz; ama nedensel iddialarda aşağıdaki ceza uygulanır.

### Düzelticiler

| Koşul | Çarpan | Gerekçe |
|---|---|---|
| `retracted: true` | Q = 0 | Geri çekilmiş kanıt kanıt değildir |
| `verification.exists: false` | Q = 0 | Bulunamayan kaynak (olası uydurma) |
| `verification.claim_matches_source: false` | Q = 0 | Kaynak aktarılanı söylemiyor |
| `verification.exists: null` | ×0.5 | Varlığı kontrol edilemedi |
| `verification.claim_matches_source: null` | ×0.7 | Metin okunamadı, sadece özet/ikincil aktarım |
| n < 30 | ×0.70 | Küçük örneklem, kararsız tahmin |
| 30 ≤ n < 100 | ×0.85 | |
| n ≥ 1000 | ×1.05 | |
| n bilinmiyor (ampirik tasarım) | ×0.90 | |
| `peer_reviewed: false` | ×0.80 | |
| hakem durumu bilinmiyor (ampirik) | ×0.90 | |
| `conflict_of_interest: true` | ×0.80 | Fon/sponsor sonucu yönlendirebilir |
| `preregistered: true` | ×1.05 | p-hacking riski düşük |
| `replicated: true` | ×1.10 | Bağımsız olarak tekrarlanmış |
| yaş > 15 yıl | ×0.90 | Hızlı değişen alanlarda bağlam eskiyebilir (`settings.stale_years`) |
| eksik veri oranı m (veri) | ×(1 − 0.5m) | Liste bazlı silme yanlılık doğurabilir |
| `applicability: partial` | ×0.80 | Popülasyon/bağlam kısmen farklı (başka ülke, yakın sektör) |
| `applicability: indirect` | ×0.50 | Belirgin farklı bağlam (başka iş türü, laboratuvar → saha, hayvan → insan) |
| **nedensel iddia + nedensel olmayan tasarım** | ×0.60 | Korelasyon nedensellik değildir; kanıt yine sayılır ama zayıflatılır (ayrıca §2c tavanı) |

Nedensellik kurabilen tasarımlar: `rct`, `quasi_experimental`. Bir meta-analiz yalnızca RCT'leri
birleştiriyorsa kanıta `"causal_design": true` ekleyin.

## 2. Olabilirlik oranı (LR)

LR = P(kanıt | iddia doğru) / P(kanıt | iddia yanlış). LR > 1 iddiayı destekler, < 1 çürütür.

### a) Sayısal kanıt (veri analizi veya kaynakta raporlanan istatistik)
BIC yaklaşımıyla Bayes faktörü (Wagenmakers 2007):

    BF₁₀ = (1 − r²)^(−n/2) / √n

r² korelasyon karesi, kısmi r² (regresyon) veya t'den türetilir: r² = t²/(t²+df).
Cohen d → r: r = d / √(d² + (n₁+n₂)²/(n₁n₂)).

İddia türüne göre çevirme:
- `nonzero` → LR = BF₁₀
- `none` → LR = 1/BF₁₀
- `positive`/`negative` (yönlü) → tek yönlü yaklaşım (Morey & Wagenmakers 2014):
  **LR ≈ 2 · BF₁₀ · q**, q = 1 − (iddia yönündeki tek yönlü p). Etki doğru yönde ve netse
  q ≈ 1 ve LR iki katına çıkar; ters yönde netse q ≈ 0 ve LR iddia aleyhine çok küçülür.

BIC-BF bilinçli olarak tutucudur: küçük etkiler orta n'de (ör. d=0.35, n=120, p≈0.06) LR≈1
verir — "bu çalışma tek başına pek bir şey söylemiyor". Bu bir hata değil; p<0.05 eşiğinin
kanıtı abarttığını hatırlatır.

Neden BIC-BF? p-değeri "sıfır hipotezi yanlış mı" sorusuna yanıt verir ama kanıt miktarını ölçmez
ve büyük n'de anlamsız küçük etkileri "anlamlı" yapar. BF hem büyüklüğü hem n'yi hesaba katar
ve sıfır lehine de kanıt üretebilir (p-değeri bunu yapamaz).

### b) Kaynak tutumu (sayı yoksa)
| stance | strength | LR_ham |
|---|---|---|
| supports | strong | 10 |
| supports | moderate | 4 |
| supports | weak | 2 |
| mixed / irrelevant | — | 1 |
| contradicts | weak / moderate / strong | 1/2, 1/4, 1/10 |

**strength nasıl seçilir:**
- `strong`: kaynak iddiayı doğrudan, açık bir bulgu olarak (etki büyüklüğü + belirsizlik) raporluyor
- `moderate`: doğrudan bulgu ama belirsizlik geniş, ya da iddiaya yakın ama birebir olmayan sonuç
- `weak`: dolaylı, yan bulgu, tartışma bölümünde geçen yorum

İki kodlama yolu vardır:

1. **`finding` (tercih edilen):** kaynağın X–Y ilişkisi hakkında ne *bulduğunu* yazın
   (`positive` · `negative` · `none` · `nonzero`). Tutum her iddia için otomatik türetilir:

   | finding \ iddia | positive | negative | nonzero | none |
   |---|---|---|---|---|
   | positive | destekler | çürütür | destekler | çürütür |
   | negative | çürütür | destekler | destekler | çürütür |
   | none | çürütür | çürütür | çürütür | destekler |
   | nonzero | karışık | karışık | destekler | çürütür |

2. **`stance`:** iddiaya göre (`supports`/`contradicts`/`mixed`/`irrelevant`). "X'in Y'ye etkisi
   yoktur" iddiası için "etki bulunamadı" diyen kaynak `supports`'tur. Yalnızca iddiaya özgü
   (değişken çiftine indirgenemeyen) kanıtlarda kullanın.

**Değişken çifti kapsamı:** `claim_id` vermeyip `x` ve `y` verdiğiniz kanıt (finding veya
reported_stats ile), aynı X–Y çiftini içeren **tüm** iddialara uygulanır. Bu sayede "X Y'yi artırır",
"X Y'yi nedensel olarak artırır" ve "X ile Y ilişkisizdir" iddiaları aynı kanıt havuzuyla
değerlendirilir ve aralarındaki uyum/çelişki ölçülebilir hale gelir.

Kaynakta r, t/df veya d/n₁/n₂ varsa `reported_stats` alanına girin; tutum tablosu yerine (a)
kullanılır. Kodlanan tutum ile istatistiğin yönü uyuşmazsa `stance_stats_mismatch` bayrağı kalkar.

### c) Sınır ve kalite ağırlığı
- |log₁₀ LR_ham| ≤ 2 (`log10_lr_cap`): tek kanıt en fazla 100 kat etki yapar. Aksi halde büyük
  bir veri seti tüm literatürü tek başına ezer; ölçüm hatası, yanlış model vb. model dışı
  belirsizliklere yer bırakmak için sınır gerekir.
- **Nedensellik tavanı:** nedensel bir iddiayı *destekleyen* gözlemsel kanıtın (deneysel olmayan veri,
  RCT/yarı-deneysel olmayan kaynak) LR_ham değeri en fazla 3 olur (`causal_gap_log10_cap`). Gerekçe:
  korelasyon nedenselliğin gerekli ama yeterli olmayan koşuludur. Ne kadar güçlü olursa olsun tek bir
  korelasyon, karıştırıcı ve ters nedensellik olasılığını ortadan kaldırmaz. Birçok bağımsız gözlemsel
  çalışmanın aynı yönü göstermesi ise P'yi yine yükseltebilir. Tavan uygulanınca `causal_cap_applied`
  bayrağı kalkar ve `quality_trace`'e yazılır.
- **LR_etkin = LR_ham^Q**: Q=1 ise kanıt tam sayılır, Q=0 ise hiç sayılmaz (LR=1).

## 3. Bağımlı kanıtlar (kümeler)

Aynı veri seti, aynı yazar grubu veya birbirini aktaran haberler bağımsız kanıt değildir;
çarpmak kanıtı şişirir. Aynı `cluster` değerini alan k kanıt için:

    küme log LR = ortalama(log LR_etkin) × k_eff,   k_eff = k / (1 + (k−1)ρ)

ρ = 0.5 varsayılan (`settings.rho_within_cluster`). ρ=0 → tam bağımsız, ρ=1 → tek kanıt.
Cluster boş bırakılırsa her kanıt kendi kümesidir.

**Kümeleme kuralları:** aynı veri setinden yapılan tüm analizler → tek küme; aynı birincil
çalışmayı aktaran ikincil kaynaklar → birincil çalışmanın kümesi; aynı yazar ekibinin çalışmaları
→ tek küme; bir meta-analiz ile içerdiği çalışmalar → ikisini birden girmeyin, meta-analizi tercih edin.

### Kapsam: ham, kontrollü, nedensel

Aynı X–Y çifti için farklı analizler farklı soruları yanıtlar. Değişken çifti kapsamlı kanıt
(`claim_id` olmayan) her iddiaya şu kuralla uygulanır:

| İddia | Uygulanan veri kanıtı (her küme içinde) |
|---|---|
| `controls: [a, b]` belirtilmiş | yalnızca kontrol kümesi tam olarak {a, b} olan analiz |
| `controls: []` belirtilmiş | yalnızca ham analiz |
| ilişkisel (`causal: false`), controls yok | en az kontrollü analiz (genelde ham) |
| nedensel (`causal: true`), controls yok | en çok kontrollü analiz (karıştırıcıya en az açık) |

Kontrol kümesi belirtilmemiş kaynaklar her kapsama uygulanır. Bir kaynak kontrollü bir sonuç
raporluyorsa `controls` alanıyla bunu belirtin. Kapsam dışı kalan kanıtlar `evidence_scoped_out`
alanında gerekçesiyle listelenir.

Neden? Karıştırıcı bir değişken (ör. kıdem hem uzaktan çalışmayı hem verimliliği artırıyorsa) ham
ilişkiyi güçlü, kontrollü ilişkiyi sıfır gösterir. Ham kanıtı "kıdem sabitken ilişki yok" iddiasına
uygulamak, doğru bir iddiayı yanlış diye reddettirir.

## 4. Sonsal olasılık P

    logit P = logit P₀ + Σ_küme ln LR_küme
    P = 1 / (1 + e^(−logit P))

Olasılık yorumu: "Önsel inancımız ve bu kanıtlar verildiğinde iddianın doğru olma olasılığı."

### Rakip hipotez setleri

Aynı kapsamda (aynı değişken çifti, nedensellik, kontroller ve popülasyon) olan `positive`, `negative`
ve `none` iddiaları birbirini dışlar ve birlikte tüm olasılıkları kapsar. `nonzero` + `none` ikilisi
için de aynısı geçerlidir. Bu yüzden ΣP ≈ 1 olmalıdır. Her iddia kendi önseliyle ayrı puanlandığı için
toplam 1'den sapabilir:

- **ΣP < 1:** kanıtlar hipotezleri iyi ayırt edemiyor. Hepsi düşük kalıyor.
- **ΣP > 1:** çelişik iddialar aynı anda yüksek olasılık almış; kodlama veya önseller hatalı olabilir.

Betik `normalized_P = P / ΣP` ile tutarlı bir dağılım ve `coherence_gap = |ΣP − 1|` verir. Açık 0.25'i
aşarsa (`hypothesis_gap_threshold`) setteki iddialara `hypothesis_set_incoherent` bayrağı eklenir.
"Hangi taraf haklı?" sorusunun yanıtı normalize P'dir. Farklı kapsamdaki iddialar (ham ve nedensel
gibi) mantıksal olarak çelişmez; uyum matrisinde 0 olarak gösterilir.

## 5. Spektrum skoru S ve uyum C

Her kanıtın yön-güç değeri: **d = kırp(log₁₀ LR_ham, −1, +1)**. Yani LR=10 → d=+1, LR=0.1 → d=−1,
LR=2 → d=+0.30.

    S = Σ Qᵢ dᵢ / Σ Qᵢ                     ∈ [−1, +1]
    C = 1 − √( Σ Qᵢ (dᵢ − S)² / Σ Qᵢ )       ∈ [0, 1]   (tek kanıtta tanımsız)

| S aralığı | Etiket |
|---|---|
| ≥ 0.6 | Güçlü destek |
| 0.3 – 0.6 | Orta destek |
| 0.1 – 0.3 | Zayıf destek |
| −0.1 – 0.1 | Belirsiz / nötr |
| −0.3 – −0.1 | Zayıf çelişki |
| −0.6 – −0.3 | Orta çelişki |
| < −0.6 | Güçlü çelişki |

**S ile P neden ikisi birden?** S "kanıtların ortalama ne dediği"dir — kanıt sayısından bağımsızdır,
5 zayıf destekleyici çalışma ile 50 tanesi aynı S'yi verir. P ise birikimlidir — çok kanıt P'yi uçlara
iter ve önsel olasılığı hesaba katar. İkisi farklı yönü gösterirse (`method_disagreement`) genelde
şu durumlardan biri vardır: tek bir güçlü kanıt çok sayıda zayıf kanıta karşı duruyor, ya da önsel
olasılık kanıtlardan baskın. Bu bir hata değil, raporlanması gereken bir bulgudur.

**Kalite derecesi** (ortalama Q, GRADE benzeri): ≥0.75 Yüksek · 0.5–0.75 Orta · 0.3–0.5 Düşük · <0.3 Çok düşük.

## 6. Karar bantları (P)

| P | Kod | Karar | Uygulama anlamı |
|---|---|---|---|
| ≥ 0.90 | accept | Kabul — uygulanabilir | Karar/politikaya temel alınabilir; izlemeye devam |
| 0.70 – 0.90 | conditional | Koşullu kabul | Geri dönüşü kolay, düşük maliyetli adımlarda kullan; pilot uygula |
| 0.30 – 0.70 | uncertain | Belirsiz | Uygulama yok; VoI'ye göre en değerli ek kanıtı topla |
| 0.10 – 0.30 | likely_false | Büyük olasılıkla yanlış | Buna dayanan kararları gözden geçir |
| < 0.10 | reject | Ret | İddiayı kullanma; yaygınsa düzeltme notu hazırla |

Yüksek riskli kararlarda (sağlık, büyük yatırım) bu eşikleri `settings` içinde yükseltin ve
raporda belirtin.

## 7. Duyarlılık ve bilginin değeri

**Duyarlılık:** P, 27 senaryoda yeniden hesaplanır — önsel ∈ {0.25, P₀, 0.75} × ρ ∈ {0, ρ, 0.8} ×
kalite ölçeği ∈ {0.8, 1.0, 1.2}. `decision_robustness` = kararın değişmediği senaryo oranı.
< %70 ise `fragile_decision`. P_min–P_max aralığı bir belirsizlik bandı olarak raporlanır.

**Bilginin değeri (VoI):** P'yi bir üst/alt karar bandına taşımak için gereken toplam LR.
Örn. "LR ≈ 3.2 gerekiyor" → tek bir orta güçte (LR=4), Q≈0.85 bağımsız çalışma yeter. Bu, hangi
iddia için ek araştırma yapmanın en çok işe yarayacağını sıralamak için kullanılır: küçük LR
gereken iddialar "bir çalışma uzaklıkta"dır.

## 8. Bayraklar

| Kod | Tetikleyici | Ne yapılmalı |
|---|---|---|
| `insufficient_evidence` | ΣQ < 1.0 veya bağımsız küme < 2 | Karar bandı ne olursa olsun "ön bulgu" olarak raporla |
| `single_source_dominance` | Bir kanıt toplam etkinin > %60'ı | O kanıtı ayrıca doğrula; onsuz sonucu belirt |
| `conflicting_evidence` | C < 0.5 | Çelişkiyi açıklayan moderatör ara (popülasyon, dönem, ölçüm) |
| `method_disagreement` | S ve P zıt yönde | Bölüm 5'teki açıklamayı rapora yaz |
| `fragile_decision` | sağlamlık < %70 | Kararı kesin dille sunma |
| `unverified_sources` | doğrulanmamış kaynak | Doğrulamayı tamamla veya sınırlılık olarak yaz |
| `excluded_evidence` | Q=0 kanıt var | Hangi kaynağın neden dışlandığını raporla |
| `causal_gap` | Nedensel iddiada tüm kanıt nedensel olmayan | İddiayı ilişkisel olarak yeniden ifade etmeyi öner |
| `stance_stats_mismatch` | Tutum ≠ istatistik yönü | Kodlamayı yeniden kontrol et |
| `relation_mismatch` | Veri farklı ilişki türüyle test edilmiş | Testi iddianın ilişki türüyle tekrar çalıştır |
| `no_counter_search` | `counter_evidence_searched` true değil | Karşı kanıt araması yap ve kaydet |
| `prior_after_evidence` | `prior_set_before_evidence: false` | Önseli gerekçelendir; duyarlılık aralığını vurgula |
| `causal_cap_applied` | Gözlemsel kanıt nedensel iddiada tavana takıldı | "İlişki var, nedensellik kanıtlanmadı" diye raporla; deneysel kanıt öner |
| `hypothesis_set_incoherent` | Rakip setinde \|ΣP − 1\| > 0.25 | Normalize P'yi raporla; ΣP<1 ise ayırt edici kanıt ara |

## 9. Önsel olasılık (P₀) seçimi

Önseli **kanıtlara bakmadan önce** belirleyin ve gerekçesini yazın; aksi halde istenen sonuca
göre ayar yapılır. Yol gösterici değerler:

| Durum | P₀ |
|---|---|
| Bilgi yok / tarafsız başlangıç | 0.50 |
| Yerleşik bilimsel uzlaşı ile uyumlu | 0.75 – 0.85 |
| Makul ama tartışmalı | 0.40 – 0.60 |
| Şaşırtıcı, olağanüstü veya tek kaynaklı viral iddia | 0.10 – 0.25 |
| Bilinen fizik/biyoloji yasalarıyla çelişen | 0.01 – 0.05 |
| Alanın taban oranı biliniyorsa (örn. bir alanda bulguların ~%40'ı replike oluyor) | o oran |

Duyarlılık analizi önsel seçiminin etkisini zaten gösterir; önseli "doğru" bulmak için uğraşmak
yerine makul ve gerekçeli seçmek yeterlidir.
