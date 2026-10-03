# Girdi ve Çıktı Şeması

## İçindekiler
1. Girdi dosyası (`girdi.json`)
2. İddia alanları
3. Kanıt alanları — kaynak
4. Kanıt alanları — veri
5. Ayarlar
6. Çıktı: `metadata.json`

Tam bir örnek için `assets/ornek_girdi.json` dosyasına bakın.

---

## 1. Girdi dosyası

```json
{
  "project":  { "title": "...", "question": "...", "analyst": "...", "scope_notes": "..." },
  "settings": { },
  "claims":   [ { ... } ],
  "evidence": [ { ... } ]
}
```

## 2. İddia (`claims[]`)

| Alan | Zorunlu | Tür | Açıklama |
|---|---|---|---|
| `id` | ✓ | str | `C1`, `C2`… |
| `text` | ✓ | str | İddianın atomik, tek cümlelik hâli |
| `x` | ✓* | str | Açıklayıcı değişken (veri sütun adıyla aynı yazın) |
| `y` | ✓* | str | Sonuç değişkeni |
| `relation` | ✓ | enum | `positive` · `negative` · `nonzero` (yön belirtilmemiş ilişki) · `none` (ilişki yok) |
| `causal` | | bool | İddia "neden olur/etkiler/artırır" diyorsa `true` |
| `population` | | str | Kimin için geçerli (ülke, yaş grubu…) |
| `timeframe` | | str | Hangi dönem |
| `conditions` | | str | Koşullar, serbest metin |
| `controls` | | list[str] | Kontrollü iddia için sabit tutulan değişkenler (`[]` = yalnızca ham ilişki). Kapsam seçimini belirler; bkz. rubric §3 |
| `prior` | | float (0,1) | Önsel olasılık; varsayılan 0.5 |
| `prior_rationale` | | str | Önselin gerekçesi |
| `prior_set_before_evidence` | | bool | Önsel kanıtlardan önce mi belirlendi |
| `counter_evidence_searched` | | bool | Karşı kanıt araması yapıldı mı |
| `counter_search_log` | | list[str] | Yapılan karşı kanıt aramaları (sorgu metinleri) |
| `source_of_claim` | | str | İddia nereden geldi (kullanıcı, makale, haber) |

\* Değişkenler arası uyum matrisi ve değişken özeti için gerekli; yoksa iddia yalnızca tek başına puanlanır.

## 3. Kaynak kanıtı (`evidence[]`, `kind: "source"`)

| Alan | Tür | Açıklama |
|---|---|---|
| `id` | str | `S1`, `S2`… |
| `claim_id` / `claim_ids` | str / list | Hangi iddia(lar)a ait. **Boş bırakılırsa** `x`+`y` gerekir ve kanıt o çifti içeren tüm iddialara uygulanır |
| `x`, `y` | str | Kanıtın hakkında olduğu değişken çifti (çift kapsamı için) |
| `controls` | list[str] | Kaynağın raporladığı sonuç hangi değişkenler kontrol edilerek elde edildi (belirtilmezse her kapsama uygulanır) |
| `applicability` | enum | `direct` · `partial` · `indirect`: popülasyon/bağlam uyumu (×1.0/0.8/0.5) |
| `applicability_note` | str | Uyum gerekçesi (ör. "Çin çağrı merkezi; farklı iş türü") |
| `kind` | `"source"` | |
| `citation` | str | Yazar (yıl). Başlık. Yayın. |
| `url` / `doi` | str | |
| `design` | enum | rubric §1 tablosu |
| `n` | int\|null | Örneklem büyüklüğü |
| `year` | int | |
| `peer_reviewed` | bool\|null | |
| `conflict_of_interest` | bool | |
| `preregistered` | bool | |
| `replicated` | bool | |
| `retracted` | bool | |
| `causal_design` | bool | Varsayılanı tasarımdan gelir; RCT meta-analizi için `true` |
| `finding` | enum | Kaynağın bulgusu: `positive` · `negative` · `none` · `nonzero` (tercih edilen; çift kapsamında zorunlu, reported_stats yoksa) |
| `stance` | enum | `supports` · `contradicts` · `mixed` · `irrelevant` — iddiaya göre; yalnızca `claim_id`'li kanıtta |
| `strength` | enum | `strong` · `moderate` · `weak` |
| `reported_stats` | obj | `{"r":..,"n":..}` veya `{"t":..,"df":..,"n":..}` veya `{"d":..,"n1":..,"n2":..}` — yön iddianın X→Y yönüne göre |
| `quote` | str | Kaynaktan iddiayla ilgili birebir alıntı (doğrulama izi) |
| `verification` | obj | `{"exists": bool\|null, "claim_matches_source": bool\|null, "method": "DOI çözüldü / tam metin okundu / yalnızca özet"}` |
| `cluster` | str | Bağımlılık kümesi |
| `notes` | str | |

## 4. Veri kanıtı (`kind: "data"`)

`scripts/data_evidence.py` tarafından üretilir; elle yazmayın. `--claim` verilmezse kanıt çift
kapsamlıdır (önerilen). Alanlar: `id, [claim_id], kind,
cluster, description, dataset, test, x, y, controls, relation_tested, n, n_total_rows, missing_frac,
experimental, data_quality_notes, stats{...}`. `stats` içinde `t, df, p_two_sided, r_equivalent,
r_ci95, effect_size_label, effect_sign, log10_bf10, bf10` ve teste özgü alanlar (`r`, `coef`, `se`,
`partial_r`, `cohens_d`, `mean_A/B`, `welch_t/p`…) bulunur.

İsteğe bağlı elle eklenebilir: `quality_multiplier` (0–1, örn. ölçüm güvenilirliği düşükse 0.8)
ve gerekçesi `data_quality_notes`.

## 5. Ayarlar (`settings`, hepsi isteğe bağlı)

| Alan | Varsayılan | |
|---|---|---|
| `rho_within_cluster` | 0.5 | Küme içi korelasyon |
| `log10_lr_cap` | 2.0 | Tek kanıt LR sınırı (log₁₀) |
| `prior_default` | 0.5 | |
| `stale_years` | 15 | |
| `dominance_threshold` | 0.6 | |
| `min_independent_clusters` | 2 | |
| `min_total_weight` | 1.0 | |
| `causal_gap_log10_cap` | log₁₀3 ≈ 0.477 | Gözlemsel kanıtın nedensel iddiayı destekleme tavanı |
| `hypothesis_gap_threshold` | 0.25 | Rakip setinde \|ΣP−1\| bayrak eşiği |
| `decision_thresholds` | [0.90, 0.70, 0.30, 0.10] | Kabul / koşullu / belirsiz / b.o. yanlış alt sınırları (azalan) |

## 6. Çıktı: `metadata.json`

```text
schema_version, generated_at, project, settings
totals: { n_claims, n_evidence, decisions: {accept, conditional, uncertain, likely_false, reject} }
claims[]:
  id, text, structure{x,y,relation,causal,controls,population,timeframe,conditions}, prior, prior_rationale
  scores:
    spectrum_S            [-1,1]   kalite-ağırlıklı yön
    spectrum_label        7 kademeli etiket
    posterior_P           [0,1]    Bayes sonsal olasılık
    posterior_odds
    log10_bayes_factor_total, bayes_factor_total
    decision_code, decision
    consensus_C           [0,1]    kanıtlar arası uyum (tek kanıtta null)
    mean_quality_Q, evidence_quality_grade
    total_weight_W        ΣQ
    n_evidence, n_active_evidence, n_independent_clusters
    n_supporting, n_contradicting, n_neutral
    spectrum_vs_probability_gap   S − (2P−1)
  sensitivity: { scenarios, P_min, P_max, decision_robustness, grid }
  value_of_information: { lr_needed_to_move_up, next_band_up_at_P, lr_needed_to_move_down, next_band_down_at_P }
  dominant_evidence
  clusters: { <küme>: { k, k_effective, log10_lr } }
  flags[]: { code, message }
  evidence[]: { id, kind, cluster, label, applied_via (claim_id|variable_pair), stance_used, quality_Q, quality_trace[], status, lr_basis,
                log10_lr_raw, lr_raw, log10_lr_effective, lr_effective, direction_d, share_of_total_effect }
  evidence_scoped_out[]: { id, reason }   kapsam nedeniyle bu iddiaya uygulanmayan çift kanıtları
claim_relations[]: { claims[2], relations[2], same_scope, logical_compatibility (+1/0/−1), P[2], incoherence?, note? }
hypothesis_sets[]: { variables[2], scope, claims[], relations[], P[], sum_P, exhaustive, normalized_P[],
                     most_probable, coherence_gap, incoherent, interpretation? }
variables: { <değişken>: { claims[], mean_S, mean_P } }
```

`incoherence` = max(0, P_a + P_b − 1), yalnızca mantıksal olarak çelişik iddia çiftleri için.
Birbirini dışlayan iki iddianın olasılıkları toplamı 1'i aşamaz; aşıyorsa kanıt kodlamasında
veya iddiaların kapsamında (farklı popülasyon?) bir sorun vardır.
