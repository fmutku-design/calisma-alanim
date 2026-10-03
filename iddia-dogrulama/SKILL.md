---
name: iddia-dogrulama
description: Araştırma ve veri analizinde iddiaları adım adım, ölçülebilir biçimde doğrular; iddiayı X→Y yapısına ayırır, kaynak ve veri kanıtlarını kalite puanıyla (Q) değerlendirir, uyuşma/çelişmeyi −1…+1 spektrumunda (S) puanlar, Bayesçi sonsal olasılık (P) ve duyarlılık analizi hesaplar, JSON meta veri + Markdown rapor üretir. Kullanıcı bir iddianın, hipotezin, bulgunun veya haberin doğruluğunu sorduğunda; "kaynaklar ne diyor", "verim bunu destekliyor mu", "X ile Y arasında ilişki var mı", fact-check, kanıt sentezi, çelişkili bulgular, hipotez testi dendiğinde; bir CSV/veri setiyle değişken iddiaları test edilmek istendiğinde veya araştırma sonuçlarının güvenilirliği sayısal ölçülmek istendiğinde kullan — "doğrulama" kelimesi geçmese bile. Use for claim verification, evidence grading and Bayesian evidence synthesis.
---

# İddia Doğrulama (ölçülebilir kanıt sentezi)

Bu skill'in amacı "bu iddia doğru mu?" sorusunu **tekrarlanabilir sayılara** çevirmektir.
Her sonuç, bir başkasının aynı girdiyle aynı sayıyı üretebileceği şekilde izlenebilir olmalı:
hangi kanıt, hangi kalite puanıyla, hangi olabilirlik oranıyla sonuca ne kadar katkı yaptı.

Üç ölçü birlikte raporlanır, çünkü her biri farklı bir soruyu yanıtlar:

| Ölçü | Aralık | Soru |
|---|---|---|
| **S** — spektrum skoru | −1 … +1 | Kanıtlar *ortalamada* iddiayı ne yönde, ne güçte destekliyor? |
| **P** — sonsal olasılık | 0 … 1 | Önsel inanç + tüm kanıtlar birikince iddia ne kadar olası? |
| **C** — uyum | 0 … 1 | Kanıtlar *kendi aralarında* ne kadar hemfikir? |

Hesaplamaların hepsini `scripts/` içindeki betikler yapar (yalnızca Python standart kütüphanesi;
kurulum gerekmez). Sen kanıtı bulur, doğrular ve kodlarsın; sayıları elle hesaplama — elle hesap
hem hata üretir hem de "istenen sonuca göre ayar" riskini açar.

## Dosyalar

- `scripts/data_evidence.py` — CSV'de X→Y iddiasını test eder (pearson, spearman, regresyon, iki grup farkı), kanıt kaydı üretir
- `scripts/score_claims.py` — girdi JSON'undan `metadata.json` + `rapor.md` üretir
- `references/scoring_rubric.md` — Q tabloları, LR kuralları, eşikler, bayraklar ve **gerekçeleri**. Kanıtları kodlamadan önce §1–§2'yi, yorumlamadan önce §5–§8'i oku
- `references/metadata_schema.md` — girdi alanları ve çıktı şeması
- `assets/ornek_girdi.json` — eksiksiz örnek girdi

## İş akışı

### Adım 0 — Kapsam

Şunları belirle ve `project` alanına yaz: araştırma sorusu, elde veri var mı (CSV yolu, sütunlar),
kaynak araması yapılacak mı (web erişimi var mı), kullanıcının verdiği kaynaklar. Kullanıcı Excel
verdiyse ve okuyamıyorsan CSV'ye çevirmesini iste.

Veri varsa önce sütunlara bak (`head -5 veri.csv`) ki iddiadaki değişken adlarını gerçek sütunlara
eşleyebilesin.

### Adım 1 — İddiaları atomik hale getir

Doğrulanabilir bir iddia tek bir X→Y ilişkisi içerir. Bileşik veya belirsiz iddiaları böl:

> "Sosyal medya gençlerde depresyonu ve kaygıyı artırıyor, özellikle kızlarda"
> → C1: sosyal_medya → depresyon, positive, causal · C2: sosyal_medya → kaygı, positive, causal ·
> C3: (kızlarda) sosyal_medya → depresyon, positive, causal, population="kız ergenler"

Her iddia için doldur: `x`, `y`, `relation` (`positive`/`negative`/`nonzero`/`none`), `causal`
("artırır, neden olur, etkiler" → true; "ilişkili, birlikte görülür" → false), `population`,
`timeframe`. "Etkiler" gibi yönsüz fiiller için yönü kullanıcıya sor veya `nonzero` kullan.

**Kapsamı belirle: ham, kontrollü, nedensel.** Aynı X–Y çifti hakkında üç farklı soru sorulabilir
ve cevapları farklı olabilir:

| Kapsam | Örnek ifade | Alanlar | Hangi veri kanıtını kullanır |
|---|---|---|---|
| Ham ilişki | "daha çok X'li olanlarda Y daha yüksek" | `causal: false` | aynı veri kümesindeki ham analiz |
| Kontrollü ilişki | "kıdem sabitken X ile Y ilişkisiz" | `controls: ["kidem"]` | yalnızca aynı kontrollerle yapılmış analiz |
| Nedensel | "X, Y'yi artırır/düşürür" | `causal: true` | aynı veri kümesindeki en kontrollü analiz |

Betik değişken çifti kanıtını bu kapsama göre otomatik seçer; dışarıda bıraktığını gerekçesiyle
raporlar. Bu ayrım önemlidir çünkü karıştırıcı bir değişken (ör. kıdem) ham ilişkiyi güçlü
gösterirken kontrollü ilişkiyi sıfırlayabilir; iki iddiaya aynı kanıtı uygulamak yanlış sonuç verir.

**Rakip iddiaları da ekle.** Kullanıcının iddiasının karşıtlarını aynı kapsamda ayrı iddialar olarak
gir. Örneğin "X Y'yi artırır" için "X Y'yi azaltır" ve "X'in Y'ye etkisi yoktur" iddialarını ekle.
Aynı kapsamdaki positive, negative ve none iddiaları birlikte bir **rakip hipotez seti** oluşturur.
Betik bu sette ΣP'yi ve normalize olasılıkları hesaplar; böylece "hangi taraf haklı?" sorusu tek bir
tutarlı dağılımla yanıtlanır. Nedensel bir iddia varsa ilişkisel versiyonunu da ekle. Çoğu zaman
ilişkisel iddia desteklenir, nedensel olan desteklenmez ve bu fark kullanıcı için en değerli bulgudur.

### Adım 2 — Önsel olasılığı kanıta bakmadan belirle

`prior` ve `prior_rationale` yaz, `prior_set_before_evidence: true` işaretle. Rehber değerler
rubric §9'da. Önseli kanıttan sonra değiştirirsen bunu `false` yap — betik bayrak kaldırır. Bu
kuralın nedeni: önsel kanıttan sonra seçilirse sonuç istenen yere çekilebilir ve sayıların
anlamı kalmaz. Duyarlılık analizi önsel seçiminin etkisini zaten ölçer.

### Adım 3 — Kanıt topla

**3a. Veri kanıtı** (CSV varsa). Her X–Y çifti için uygun testi çalıştır:

```bash
python scripts/data_evidence.py --csv veri.csv --x X --y Y --test pearson --id D1 --cluster veri1 --append-to girdi.json
```

| Durum | `--test` |
|---|---|
| İki sayısal değişken, doğrusal | `pearson` |
| Sıralı veri, aykırı değer, doğrusal olmayan monoton | `spearman` |
| Karıştırıcılar var ("diğer değişkenler sabitken") | `regression --controls a,b` |
| X iki gruplu kategorik | `group_diff --groups A,B` (B = pozitif yön) |

`--claim` vermezsen kanıt o X–Y çiftini içeren **tüm** iddialara (kapsamı uyan) uygulanır;
genelde istediğin budur. Aynı veri setinden yapılan tüm analizlere aynı `--cluster` ver, çünkü
bağımsız değiller ve kapsam seçimi bu küme içinde yapılır.

**Nedensel veya kontrollü iddia varsa hem ham hem kontrollü analiz çalıştır.** Kontrol değişkenlerini
veride olası karıştırıcılardan seç: hem X'i hem Y'yi etkileyebilecek değişkenler (yaş, kıdem, gelir,
grup). Ham ve kontrollü sonucun farkı başlı başına bir bulgudur; ham etkinin ne kadarının
karıştırıcıdan geldiğini raporla.
Rastgele atamalı deney verisiyse `--experimental` ekle. Pearson ve Spearman'ı aynı çift için
ikisini birden girme; aynı bilgiyi iki kez saymış olursun.

**3b. Kaynak kanıtı.** Arama yapabiliyorsan her iddia için hem destekleyen hem **karşı** kanıt ara
(ör. "X Y no effect", "X Y null result", "X Y replication failed"). Karşı arama yapılmazsa
doğrulama yanlılığı oluşur; yaptığın sorguları `counter_search_log`'a yaz ve
`counter_evidence_searched: true` işaretle. Kullanıcı yalnızca kendi verisiyle doğrulama istediyse
literatür araması kapsam dışıdır: `counter_evidence_searched: "not_applicable"` yaz ve gerekçeyi
`project.scope_notes`'a ekle. Bu durumda karşı kanıt rolünü rakip iddialar üstlenir; onları
mutlaka ekle.

Her kaynak için doğrulama kontrol listesi:
1. **Var mı?** DOI/URL açılıyor, başlık-yazar-yıl tutuyor mu → `verification.exists`
2. **Söylüyor mu?** İddia edilen bulgu kaynağın kendi metninde var mı; birebir alıntıyı `quote`'a koy → `claim_matches_source`
3. **Geri çekilmiş mi?** → `retracted`
4. **Tasarım, n, hakem, yıl, çıkar çatışması, ön kayıt, replikasyon** → ilgili alanlar
5. **Bulgu:** kaynak X–Y hakkında ne buldu → `finding`; sayı raporluyorsa (r, t/df, d/n₁/n₂) → `reported_stats`
6. **Bağımlılık:** aynı birincil çalışmayı aktaran haber/derleme → aynı `cluster`
7. **Uygulanabilirlik:** kaynağın popülasyonu/bağlamı iddianınkine uyuyor mu → `applicability`
   (`direct` ×1.0 · `partial` ×0.8 · `indirect` ×0.5) ve `applicability_note`. Örneğin başka ülkede ve
   başka iş türünde yapılmış bir deney, bu şirkete özgü iddia için `indirect` olur. Yüksek kaliteli
   ama uzak bir çalışma, yakın ama zayıf bir çalışmadan daha az bilgi taşıyabilir.

Kontrol edemediğin şeyi `null` bırak, tahmin etme — betik belirsizliği cezalandırır, yanlış
`true` ise cezayı atlatır. Kaynak uydurma: bulamadığın bir çalışmayı asla girme. Kullanıcının
verdiği bir kaynak bulunamıyorsa `exists: false` ile gir; betik onu dışlar ve raporda görünür.

Kanıtı mümkünse `finding` + `x`/`y` ile (çift kapsamlı) kodla; `stance` yalnızca bir iddiaya özgü,
X–Y ilişkisine indirgenemeyen kanıt içindir. Kodlama ayrıntıları ve `strength` seçimi rubric §2'de.

### Adım 4 — Girdi dosyasını yaz

`girdi.json` biçimi `references/metadata_schema.md`'de, tam örnek `assets/ornek_girdi.json`'da.
Çıktı klasörünü kullanıcının çalışma dizininde oluştur (ör. `dogrulama/`).

### Adım 5 — Puanla

```bash
python scripts/score_claims.py dogrulama/girdi.json --out-dir dogrulama/
```

Girdi hatası varsa betik nedenini söyler; düzelt ve tekrar çalıştır.

### Adım 6 — Bayrakları işle

Her bayrak bir sonraki eylemi söyler (rubric §8). Ayrım önemli:

- **Kodlama hataları** (`stance_stats_mismatch`, `relation_mismatch`): girdiyi düzelt, yeniden çalıştır.
- **Kanıt durumu** (`insufficient_evidence`, `conflicting_evidence`, `single_source_dominance`, `fragile_decision`, `causal_gap`, `causal_cap_applied`, `method_disagreement`, `hypothesis_set_incoherent`): bunlar *bulgudur*, düzeltilmez; raporda açıklanır. Mümkünse ek kanıt ara (Adım 3) ve tekrar puanla.
- **Süreç** (`no_counter_search`, `unverified_sources`, `prior_after_evidence`): mümkünse eksik adımı tamamla; değilse sınırlılık olarak yaz.

Sonuç beğenilmediği için önsel, Q veya kodlama değiştirme. İlk çalıştırmadan sonra yaptığın her
değişikliği gerekçesiyle `project.revisions` listesine ekle.

### Adım 7 — Yorum ve uygulama bölümünü yaz

`rapor.md`'nin sonundaki `<!-- YORUM_UYGULAMA ... -->` satırını aşağıdaki yapıyla değiştir.
Her cümleyi `metadata.json`'daki bir sayıya dayandır; sayı vermeden "güçlü kanıt" deme.

```markdown
### Ana bulgular
- (3–5 madde; her biri iddia ID'si + S, P, karar. Örn: "C1 güçlü desteklendi (S=+0.72, P=0.96), ancak
  nedensel versiyonu C2 belirsiz kaldı (P=0.58): ilişki var, nedensellik kanıtlanmadı.")

### İddialar arası tutarlılık
- (Rakip hipotez setlerinden: her set için en olası hipotez ve normalize P'si. ΣP < 1 ise
  "kanıtlar hipotezleri ayırt edemiyor", ΣP > 1 ise "çelişik iddialar aynı anda yüksek puan almış"
  diye yorumla.)
- (Kapsamlar arası: ham ilişki ile kontrollü/nedensel sonuç farklıysa nedenini — karıştırıcı,
  ters nedensellik — açıkla. Farklı kapsamdaki iddialar mantıksal olarak çelişmez; ikisi birden doğru
  olabilir: "ham ilişki var ama kıdem sabitken yok".)

### Sınırlılıklar
- (Her bayrak için bir cümle: ne anlama geliyor, sonucu nasıl etkiliyor)

### Uygulama önerileri
| İddia | Karar | Önerilen eylem | Koşul / izlenecek gösterge |
|---|---|---|---|
(Karar bandına göre: kabul → uygula ve izle; koşullu → geri alınabilir/pilot uygulama;
belirsiz → uygulama yok, ek kanıt; büyük olasılıkla yanlış/ret → buna dayanan kararları gözden geçir.
Bkz. rubric §6.)

### Sonraki en değerli kanıt
- (Belirsiz bantlardaki iddiaları `value_of_information` LR değerine göre sırala: en küçük LR
  gerektiren iddia "bir çalışma uzaklıkta"dır. Ne tür bir çalışmanın — tasarım, n, popülasyon —
  o LR'yi sağlayacağını somut olarak öner.)
```

### Adım 8 — Teslim

Kullanıcıya kısa bir özet ver: her iddia için tek satır (ID · S · etiket · P · karar · sağlamlık),
en önemli 1–2 bayrak ve dosya yolları (`metadata.json`, `rapor.md`, `girdi.json`). Ayrıntıyı rapora
bırak. Kullanıcı İngilizce yazıyorsa `--lang en` ile çalıştır (etiket, karar ve bayrak metinleri İngilizce
olur; rapor iskeleti Türkçe kalır) ve özeti İngilizce yaz.

## Sınır durumlar

- **Kanıt hiç bulunamadı:** yine de puanla. P = önsel, S = 0, `insufficient_evidence` çıkar. "Doğrulanamadı" demek de ölçülebilir bir sonuçtur.
- **Sadece veri var, kaynak yok** (veya tersi): akış aynı; olmayan adımı atla ve rapora yaz.
- **Değişkene indirgenemeyen iddia** ("X şirketi 2023'te iflas etti"): `x`/`y` boş bırak, kanıtı `claim_id` + `stance` ile gir. Uyum matrisi bu iddiayı içermez; diğer her şey çalışır.
- **Çok sayıda iddia (>15):** önce kullanıcıyla öncelik sırası belirle; en önemli 5–10 iddiayı derinlemesine doğrula.
- **Yüksek riskli karar** (sağlık, hukuk, büyük yatırım): `settings.decision_thresholds` değerini sıkılaştır (ör. `[0.95, 0.8, 0.3, 0.1]`), bunu raporda belirt ve sonuçların uzman görüşünün yerini tutmadığını yaz.
