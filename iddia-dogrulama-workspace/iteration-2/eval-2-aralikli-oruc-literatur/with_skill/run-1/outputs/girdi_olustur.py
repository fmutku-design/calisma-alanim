import json, sys
OUT = "/home/user/calisma-alanim/iddia-dogrulama-workspace/iteration-2/eval-2-aralikli-oruc-literatur/with_skill/run-1/outputs/girdi.json"

XA = "TRE_16_8_vs_izokalorik_KKK"   # 16:8 zaman kısıtlı beslenme vs aynı kalorili sürekli kalori kısıtlaması
YW = "kilo_kaybi"
YI = "insulin_direnci"
XC = "TRE_16_8_vs_kontrol"           # 16:8 vs normal/serbest beslenme (kalori eşitlenmemiş)
POP = "Aşırı kilolu/obez yetişkinler (prediyabet/T2D dahil)"

VER = {"exists": True, "claim_matches_source": None,
       "method": "WebSearch sonuç özetleriyle başlık/yazar/dergi/yıl doğrulandı; WebFetch egress proxy tarafından engellendi, tam metin/özet doğrudan okunamadı (bulgu ikincil özetten)"}

counter_w = [
  "time-restricted eating superior to calorie restriction greater weight loss randomized trial matched calories",
  "Liu 2022 NEJM calorie restriction with or without time-restricted eating (null sonuç)",
  "Maruthur 2024 isocaloric time-restricted eating body weight (null sonuç)",
  "Is isocaloric intermittent fasting superior to calorie restriction meta-analysis",
  "Lin 2023 Annals time-restricted eating vs calorie restriction",
  "Lowe 2020 TREAT 16:8 weight loss (null sonuç)",
  "Semnani-Azad 2025 BMJ network meta-analysis TRE vs continuous energy restriction"]
counter_i = [
  "ChronoFast isocaloric time-restricted eating insulin sensitivity (null sonuç)",
  "meta-analysis TRE vs continuous energy restriction isocaloric HOMA-IR",
  "Sutton 2018 eTRF insulin sensitivity without weight loss (destekleyici)",
  "Jamshed 2022 eTRE insulin resistance no difference",
  "intermittent fasting reverse insulin resistance normalize HOMA-IR remission"]

def claim(id, text, x, y, rel, prior, rat, log, causal=True, src=None):
    c = {"id": id, "text": text, "relation": rel, "causal": causal, "population": POP,
         "prior": prior, "prior_rationale": rat, "prior_set_before_evidence": True,
         "counter_evidence_searched": True, "counter_search_log": log}
    if x: c["x"], c["y"] = x, y
    if src: c["source_of_claim"] = src
    return c

claims = [
 claim("C1", "16:8 TRE, aynı kaloriyi alan klasik (sürekli kalori kısıtlamalı) diyete göre DAHA FAZLA kilo kaybı sağlar", XA, YW, "positive", 0.35,
       "İzokalorik koşulda enerji dengesi kilo farkını sınırlar; sirkadiyen/metabolik avantaj hipotezi makul ama tartışmalı → nötrün biraz altı", counter_w, src="sağlık sitesi (kullanıcı)"),
 claim("C2", "Aynı kaloride klasik diyet, 16:8 TRE'den daha fazla kilo kaybı sağlar (rakip)", XA, YW, "negative", 0.15,
       "Rakip hipotez; TRE'nin kilo kaybını azaltacağına dair güçlü mekanizma yok", counter_w),
 claim("C3", "Aynı kaloride 16:8 TRE ile klasik diyet arasında kilo kaybı açısından anlamlı fark yoktur (rakip)", XA, YW, "none", 0.50,
       "Enerji dengesi ilkesine göre izokalorik iki diyetin benzer sonuç vermesi beklenir → C1–C3 setinde en yüksek önsel; set toplamı 1.0", counter_w),
 claim("C4", "16:8 TRE, aynı kalorili klasik diyete göre ÇOK DAHA FAZLA (klinik olarak büyük, ör. ≥%3 vücut ağırlığı / ≥3 kg ek) kilo kaybı sağlar", None, None, "positive", 0.12,
       "'Çok daha fazla' büyüklük iddiası; izokalorik koşulda büyük fark termodinamik açıdan beklenmez → olağanüstü iddia bandı (0.10–0.25) alt ucu", counter_w, src="sağlık sitesi (kullanıcı)"),
 claim("C5", "16:8 TRE, aynı kalorili klasik diyete göre insülin direncini DAHA FAZLA azaltır", XA, YI, "negative", 0.35,
       "Sirkadiyen hizalama hipotezi (erken TRE) makul ama izokalorik koşulda tartışmalı", counter_i, src="sağlık sitesi (kullanıcı) — ima edilen karşılaştırma"),
 claim("C6", "Aynı kaloride 16:8 TRE ile klasik diyetin insülin direncine etkisi farklı değildir (rakip)", XA, YI, "none", 0.50,
       "İnsülin duyarlılığındaki iyileşmenin büyük kısmının kilo kaybından gelmesi beklenir → izokalorik koşulda fark yok en olası", counter_i),
 claim("C7", "Aynı kaloride 16:8 TRE, klasik diyete göre insülin direncini daha az azaltır / kötüleştirir (rakip)", XA, YI, "positive", 0.15,
       "Rakip hipotez; geç yeme penceresinin olumsuz etkisi teorik olarak mümkün ama zayıf", counter_i),
 claim("C8", "16:8 TRE, normal beslenmeye (kontrol) göre insülin direncini azaltır", XC, YI, "negative", 0.55,
       "Serbest TRE genelde kalori alımını ve kiloyu azaltır; bu da insülin direncini düşürmeli → makul, hafif olumlu önsel", counter_i),
 claim("C9", "16:8 TRE'nin normal beslenmeye göre insülin direncine etkisi yoktur (rakip)", XC, YI, "none", 0.40,
       "Kilo kaybı küçük kalırsa etki ölçülemeyebilir", counter_i),
 claim("C10", "16:8 TRE, normal beslenmeye göre insülin direncini artırır (rakip)", XC, YI, "positive", 0.05,
       "Mekanizma yok; dışlayıcı tamamlayıcı hipotez", counter_i),
 claim("C11", "16:8 TRE insülin direncini TAMAMEN düzeltir (normalleştirir / ortadan kaldırır)", None, None, "positive", 0.08,
       "Mutlak/olağanüstü iddia: insülin direnci çok etkenli (adipozite, genetik, aktivite); tek bir öğün zamanlaması müdahalesinin onu tamamen ortadan kaldırması biyolojik olarak beklenmez → 0.05–0.10", counter_i, src="sağlık sitesi (kullanıcı)"),
]

def src(id, citation, design, year, cluster, url=None, doi=None, n=None, peer=True, x=None, y=None, finding=None,
        strength="moderate", applic="direct", note=None, quote=None, claim_id=None, stance=None, stats=None, causal_design=None, notes=None, ver=VER, prereg=None):
    e = {"id": id, "kind": "source", "citation": citation, "design": design, "year": year, "n": n,
         "peer_reviewed": peer, "strength": strength, "applicability": applic, "verification": ver, "cluster": cluster}
    if url: e["url"] = url
    if doi: e["doi"] = doi
    if x: e["x"], e["y"] = x, y
    if finding: e["finding"] = finding
    if claim_id: e["claim_id"] = claim_id
    if stance: e["stance"] = stance
    if stats: e["reported_stats"] = stats
    if note: e["applicability_note"] = note
    if quote: e["quote"] = quote
    if causal_design is not None: e["causal_design"] = causal_design
    if notes: e["notes"] = notes
    if prereg is not None: e["preregistered"] = prereg
    return e

BMJ = dict(citation="Semnani-Azad Z, Khan TA, et al. (2025). Intermittent fasting strategies and their effects on body weight and other cardiometabolic risk factors: systematic review and network meta-analysis of randomised clinical trials. BMJ.",
           design="meta_analysis", year=2025, url="https://www.researchgate.net/publication/392802015", causal_design=True)
HAM = dict(citation="Hamsho M, et al. (2025). Is isocaloric intermittent fasting superior to calorie restriction? A systematic review and meta-analysis of RCTs. Nutr Metab Cardiovasc Dis.",
           design="meta_analysis", year=2025, url="https://www.nmcd-journal.com/article/S0939-4753(24)00439-3/fulltext", causal_design=True)
CRE = dict(citation="Črešnovar T, Habe B, Jenko Pražnikar Z, Petelin A. (2023). Effectiveness of Time-Restricted Eating with Caloric Restriction vs. Caloric Restriction for Weight Loss and Health: Meta-Analysis. Nutrients.",
           design="meta_analysis", year=2023, url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10708501/", causal_design=True)
EJC = dict(citation="(2023). Time-restricted eating with calorie restriction on weight loss and cardiometabolic risk: a systematic review and meta-analysis. Eur J Clin Nutr (yazarlar doğrulanamadı).",
           design="meta_analysis", year=2023, doi="10.1038/s41430-023-01311-w", url="https://www.nature.com/articles/s41430-023-01311-w", causal_design=True)
LIU = dict(citation="Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss (TREATY). N Engl J Med.",
           design="rct", year=2022, n=139, doi="10.1056/NEJMoa2114833", url="https://www.nejm.org/doi/full/10.1056/NEJMoa2114833")
JAM = dict(citation="Jamshed H, Steger FL, Bryan DR, et al. (2022). Effectiveness of Early Time-Restricted Eating for Weight Loss, Fat Loss, and Cardiometabolic Health in Adults With Obesity: A Randomized Clinical Trial. JAMA Intern Med.",
           design="rct", year=2022, n=90, url="https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2794819")
MAR = dict(citation="Maruthur NM, et al. (2024). Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity: A Randomized Controlled Trial. Ann Intern Med 177(5):549-558.",
           design="rct", year=2024, n=41, doi="10.7326/M23-3132", url="https://www.acpjournals.org/doi/10.7326/M23-3132")
LIN = dict(citation="Lin S, Cienfuegos S, Ezpeleta M, et al. (2023). Time-Restricted Eating Without Calorie Counting for Weight Loss in a Racially Diverse Population: A Randomized Controlled Trial. Ann Intern Med 176(7).",
           design="rct", year=2023, n=90, doi="10.7326/M23-0052", url="https://www.acpjournals.org/doi/10.7326/M23-0052")
LOW = dict(citation="Lowe DA, Wu N, Rohdin-Bibby L, et al. (2020). Effects of Time-Restricted Eating on Weight Loss and Other Metabolic Parameters in Women and Men With Overweight and Obesity: The TREAT Randomized Clinical Trial. JAMA Intern Med 180(11):1491-1499.",
           design="rct", year=2020, n=116, url="https://jamanetwork.com/journals/intemed/articlepdf/2771095/jamainternal_lowe_2020_oi_200064_1613679348.50724.pdf")
PAV = dict(citation="Pavlou V, Cienfuegos S, Lin S, et al. (2023). Effect of Time-Restricted Eating on Weight Loss in Adults With Type 2 Diabetes: A Randomized Clinical Trial. JAMA Netw Open 6(10).",
           design="rct", year=2023, n=75, doi="10.1001/jamanetworkopen.2023.39337", url="https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2811116")
CHR = dict(citation="Peters B, Schwarz J, et al. (2025). Intended isocaloric time-restricted eating shifts circadian clocks but does not improve cardiometabolic health in women with overweight (ChronoFast). Sci Transl Med 17:eadv6787.",
           design="rct", year=2025, doi="10.1126/scitranslmed.adv6787", url="https://www.science.org/doi/10.1126/scitranslmed.adv6787")
SUT = dict(citation="Sutton EF, Beyl R, Early KS, et al. (2018). Early Time-Restricted Feeding Improves Insulin Sensitivity, Blood Pressure, and Oxidative Stress Even without Weight Loss in Men with Prediabetes. Cell Metab 27(6):1212-1221.",
           design="rct", year=2018, n=8, url="https://www.cell.com/cell-metabolism/fulltext/S1550-4131(18)30253-5")
NR = dict(citation="(2025). Effect of 8-Hour Time-Restricted Eating (16/8 TRE) on Glucose Metabolism and Lipid Profile in Adults: A Systematic Review and Meta-Analysis. Nutrition Reviews (23 RCT, n=1280).",
          design="meta_analysis", year=2025, n=1280, doi="10.1093/nutrit/nuaf206", url="https://academic.oup.com/nutritionreviews/article/84/8/1600/8373435", causal_design=True)
CIE = dict(citation="Cienfuegos S, Gabel K, Kalam F, et al. (2020). Effects of 4- and 6-h Time-Restricted Feeding on Weight and Cardiometabolic Health: A Randomized Controlled Trial in Adults with Obesity. Cell Metab.",
           design="rct", year=2020, url="https://www.cell.com/cell-metabolism/fulltext/S1550-4131(20)30319-3")
HEP = dict(citation="(t.y.) Hepatic-Metabolite-Based Intermittent Fasting Enables a ... (Thieme Connect, doi 10.1055/a-1510-8896) — insülin direnci normalleşmesi/remisyonu >%76 bildiriliyor (arama özetinden).",
           design="unknown", year=2021, peer=None, url="https://www.thieme-connect.com/products/ejournals/pdf/10.1055/a-1510-8896.pdf")

ev = []
# ---- Çift A: kilo (C1–C3)
ev += [
 src("S1w", **BMJ, cluster="MA_havuzu", x=XA, y=YW, finding="none", strength="moderate", applic="partial",
     note="99 RCT; TRE tüm pencereler (yalnız 16:8 değil); sürekli enerji kısıtlaması her zaman birebir izokalorik değil",
     quote="(özet aktarımı) intermittent fasting diets have similar benefits to continuous energy restriction for weight loss... minor differences... some benefit of weight loss with alternate day fasting"),
 src("S2w", **HAM, cluster="MA_havuzu", x=XA, y=YW, finding="none", strength="moderate", applic="partial",
     note="İzokalorik IF vs CR; 20 RCT; IF türleri karışık (yalnız 16:8 değil)",
     quote="(özet aktarımı) IF may be an effective alternative to CR but is not superior to CR"),
 src("S3w", **CRE, cluster="MA_havuzu", x=XA, y=YW, finding="positive", strength="moderate", applic="partial",
     note="TRE+CR vs yalnız CR (kalori hedefleri benzer); 7 RCT, n=458; TRE pencereleri karışık",
     quote="(özet aktarımı) TRE with CR compared to CR alone resulted in significantly greater reductions in body weight (MD: −2.11 kg)"),
 src("S4w", **EJC, cluster="MA_havuzu", x=XA, y=YW, finding="positive", strength="moderate", applic="partial",
     note="TRE+CR vs CR; erken TRE alt grubunda etki",
     quote="(özet aktarımı) WMD −1.40 kg (95% CI −1.81 to −1.00)"),
 src("S5w", **LIU, cluster="Liu2022", x=XA, y=YW, applic="direct", strength="strong",
     note="8 saatlik pencere (08–16) = 16:8; iki kolda aynı kalori reçetesi; 12 ay; Çin, obez yetişkinler",
     stats={"t": 1.6, "df": 137, "n": 139},
     quote="(özet aktarımı) weight loss 8.0 kg vs 6.3 kg... not superior... net difference −1.8 kg; P = .11",
     notes="t, P=.11'den türetildi (iki yönlü p=0.11 → |t|≈1.6, df≈137); işaret TRE lehine daha çok kilo kaybı yönünde +"),
 src("S6w", **JAM, cluster="Jamshed2022", x=XA, y=YW, finding="positive", strength="strong", applic="partial",
     note="Erken TRE (07–15) + enerji kısıtlaması vs ≥12 saat pencere + aynı enerji kısıtlaması; 14 hafta. Pencere erken (klasik 16:8'den farklı zamanlama)",
     quote="(özet aktarımı) eTRE group had lost an additional 2.3 kg compared to CON... estimated to equate to a 214 kcal/day reduction in energy intake",
     notes="Yazarlar farkın ölçülmemiş ~214 kcal/gün alım farkından gelebileceğini tahmin ediyor → 'aynı kalori' varsayımı zayıf"),
 src("S7w", **MAR, cluster="Maruthur2024", x=XA, y=YW, finding="none", strength="strong", applic="partial",
     note="Kontrollü beslenme ile gerçekten izokalorik; ama 10 saatlik pencere (16:8 değil) ve karşılaştırma 'olağan yeme düzeni' (klasik diyet değil); %93 kadın",
     quote="(özet aktarımı) In the setting of isocaloric eating, TRE did not decrease weight or improve glucose homeostasis relative to UEP"),
 src("S8w", **LIN, cluster="Lin2023", x=XA, y=YW, finding="none", strength="moderate", applic="partial",
     note="12:00–20:00 TRE (16:8) kalori saymadan vs %25 CR; gerçekleşen alım azalması benzer (−425 vs −405 kcal) → fiilen yaklaşık izokalorik; 12 ay",
     quote="(özet aktarımı) TRE lost 4.61 kg, CR 5.42 kg vs control... difference not statistically significant"),
 src("S9w", **LOW, cluster="MA_16_8", x=XA, y=YW, finding="none", strength="moderate", applic="partial",
     note="16:8 (12–20) vs 3 öğün; kalori hedefi yok ama gruplar arası enerji alımı farklı değil → fiilen benzer kalori",
     quote="(özet aktarımı) Time-restricted eating, in the absence of other interventions, is not more effective in weight loss than eating throughout the day"),
 src("S10w", **PAV, cluster="Pavlou2023", x=XA, y=YW, finding="positive", strength="weak", applic="partial",
     note="T2D'li obez yetişkinler; TRE (12–20) kalori saymadan vs %25 CR — izokalorik değil; TRE vs CR doğrudan farkının anlamlılığı doğrulanamadı",
     quote="(özet aktarımı) TRE was more effective for weight loss (−3.6%) than CR (−1.8%) compared with controls"),
]
# ---- Çift B: insülin direnci, izokalorik karşılaştırma (C5–C7)
ev += [
 src("S2i", **HAM, cluster="MA_havuzu", x=XA, y=YI, finding="negative", strength="weak", applic="partial",
     note="İzokalorik IF (türler karışık) vs CR; uzun dönemde HOMA-IR P=0.04 IF lehine ama genel sonuç 'üstün değil'",
     quote="(özet aktarımı) IF groups had significant reductions in ... fasting blood insulin (P < 0.00001) and HOMA-IR (P = 0.04) in the long term"),
 src("S3i", **CRE, cluster="MA_havuzu", x=XA, y=YI, finding="none", strength="weak", applic="partial",
     quote="(özet aktarımı) no additional impact of TRE in combination with CR in comparison to CR on serum biochemical measures"),
 src("S4i", **EJC, cluster="MA_havuzu", x=XA, y=YI, finding="none", strength="moderate", applic="partial",
     quote="(özet aktarımı) compared with CR alone, TRE plus CR exhibited no significant benefit on blood pressure, glucose profile, and lipid profile"),
 src("S5i", **LIU, cluster="Liu2022", x=XA, y=YI, finding="none", strength="moderate", applic="direct",
     quote="(özet aktarımı) not more beneficial than daily calorie restriction with regard to reduction in body weight, body fat, or metabolic risk factors"),
 src("S6i", **JAM, cluster="Jamshed2022", x=XA, y=YI, finding="none", strength="moderate", applic="partial",
     quote="(özet aktarımı) primary analysis showed no difference between groups [insulin resistance, glucose]; adherent-completer secondary analysis HOMA-IR −2.80 (p=0.047)",
     notes="Birincil (ITT) analiz esas alındı; uyumlu-tamamlayan ikincil analiz post hoc olduğu için kodlanmadı"),
 src("S7i", **MAR, cluster="Maruthur2024", x=XA, y=YI, finding="none", strength="moderate", applic="partial",
     note="10 saatlik izokalorik TRE vs olağan yeme; glisemik ölçütler (insülin direnci ölçütünün ayrıntısı doğrulanamadı)",
     quote="(özet aktarımı) Change in glycemic measures did not differ between groups"),
 src("S11i", **CHR, cluster="ChronoFast2025", x=XA, y=YI, finding="none", strength="strong", applic="partial",
     note="İzokalorik 8 saatlik erken ve geç TRE (16:8), çapraz RCT, 2'şer hafta, aşırı kilolu kadınlar; birincil sonuç insülin duyarlılığı; karşılaştırma TRE pencereleri ve başlangıç (klasik diyet kolu yok)",
     quote="(özet aktarımı) In an intended isocaloric setting, neither eTRE nor lTRE improves insulin sensitivity or other cardiometabolic traits"),
 src("S12i", **SUT, cluster="Sutton2018", x=XA, y=YI, finding="negative", strength="moderate", applic="indirect",
     note="6 saatlik erken TRF (18:6, akşam yemeği 15:00 öncesi), kilo sabit tutulmuş kontrollü beslenme, prediyabetik 8 erkek, çapraz; 16:8'e uzak",
     quote="(özet aktarımı) eTRF improved insulin sensitivity, β cell responsiveness, blood pressure, oxidative stress... even without weight loss"),
 src("S10i", **PAV, cluster="Pavlou2023", x=XA, y=YI, finding="none", strength="weak", applic="indirect",
     note="T2D; ölçüt HbA1c (insülin direnci değil); izokalorik değil",
     quote="(özet aktarımı) changes in HbA1c levels did not differ between the TRE (−0.91%) and CR (−0.94%) groups"),
]
# ---- Çift C: 16:8 vs kontrol, insülin direnci (C8–C10)
ev += [
 src("S13c", **NR, cluster="MA_16_8", x=XC, y=YI, applic="direct", strength="moderate",
     stats={"d": -0.16, "n1": 640, "n2": 640},
     quote="(özet aktarımı) slight reduction in HOMA-IR levels (SMD, −0.16; 95% CI, −0.29 to −0.02; P = .03)... high heterogeneity",
     notes="n1/n2 toplam 1280 katılımcının eşit bölündüğü varsayımıyla; negatif d = TRE'de daha düşük HOMA-IR"),
 src("S9c", **LOW, cluster="MA_16_8", x=XC, y=YI, finding="none", strength="weak", applic="direct",
     quote="(özet aktarımı) there were no significant changes in any of the other secondary outcomes",
     notes="İkincil sonuçların insülin/HOMA-IR içerdiği özetten çıkarıldı; ayrıntı doğrulanamadı → weak"),
 src("S14c", **CIE, cluster="Cienfuegos2020", x=XC, y=YI, finding="negative", strength="moderate", applic="partial",
     note="4 ve 6 saatlik TRF (16:8'den daha kısıtlayıcı), 8 hafta, obez yetişkinler; ~550 kcal/gün alım azalması",
     quote="(özet aktarımı) both 4- and 6-h TRF produced comparable reductions in body weight (3%), insulin resistance, and oxidative stress, versus controls"),
]
# ---- C4: 'çok daha fazla' büyüklük iddiası (iddiaya özgü tutum)
ev += [
 src("S1m", **BMJ, cluster="MA_havuzu", claim_id="C4", stance="contradicts", strength="strong", applic="partial",
     quote="(özet aktarımı) similar benefits to continuous energy restriction... minor differences"),
 src("S3m", **CRE, cluster="MA_havuzu", claim_id="C4", stance="contradicts", strength="weak", applic="partial",
     notes="TRE lehine en olumlu meta-analiz bile ~2 kg ek kayıp → 'daha fazla' ile uyumlu ama 'çok daha fazla' değil",
     quote="(özet aktarımı) MD: −2.11 kg"),
 src("S5m", **LIU, cluster="Liu2022", claim_id="C4", stance="contradicts", strength="strong", applic="direct",
     quote="(özet aktarımı) net difference −1.8 kg; P = .11 (12 ay, aynı kalori reçetesi)"),
 src("S6m", **JAM, cluster="Jamshed2022", claim_id="C4", stance="supports", strength="weak", applic="partial",
     quote="(özet aktarımı) additional 2.3 kg ... estimated 214 kcal/day reduction in energy intake",
     notes="En büyük TRE lehine fark; ancak yazarlar farkı ek kalori açığına bağlıyor"),
 src("S7m", **MAR, cluster="Maruthur2024", claim_id="C4", stance="contradicts", strength="strong", applic="partial",
     quote="(özet aktarımı) weight decreased by 2.3 kg in TRE and 2.6 kg in UEP (isocaloric)"),
 src("S8m", **LIN, cluster="Lin2023", claim_id="C4", stance="contradicts", strength="moderate", applic="partial",
     quote="(özet aktarımı) TRE −4.61 kg vs CR −5.42 kg (vs control), not significant"),
]
# ---- C11: 'tamamen düzeltir'
ev += [
 src("S13t", **NR, cluster="MA_16_8", claim_id="C11", stance="contradicts", strength="strong", applic="direct",
     quote="(özet aktarımı) slight reduction in HOMA-IR (SMD −0.16)"),
 src("S9t", **LOW, cluster="MA_16_8", claim_id="C11", stance="contradicts", strength="weak", applic="direct",
     quote="(özet aktarımı) no significant changes in any of the other secondary outcomes"),
 src("S11t", **CHR, cluster="ChronoFast2025", claim_id="C11", stance="contradicts", strength="moderate", applic="partial",
     quote="(özet aktarımı) neither eTRE nor lTRE improves insulin sensitivity"),
 src("S5t", **LIU, cluster="Liu2022", claim_id="C11", stance="contradicts", strength="weak", applic="direct",
     quote="(özet aktarımı) not more beneficial than daily calorie restriction ... metabolic risk factors"),
 src("S12t", **SUT, cluster="Sutton2018", claim_id="C11", stance="mixed", strength="weak", applic="indirect",
     notes="İyileşme gösteriyor ama normalleşme/tam düzelme bildirmiyor"),
 src("S15t", **HEP, cluster="Thieme_HMIF", claim_id="C11", stance="supports", strength="weak", applic="indirect",
     ver={"exists": True, "claim_matches_source": None, "method": "Yalnızca arama özeti; tasarım, n, hakem durumu ve yazarlar doğrulanamadı"},
     note="16:8 değil, 'karaciğer metaboliti temelli' özel bir IF protokolü; tasarım bilinmiyor",
     quote="(arama özeti) greater than 76% efficiency for insulin resistance normalization and remission"),
]

data = {
 "project": {
   "title": "Aralıklı oruç (16:8) — izokalorik kilo kaybı ve insülin direnci iddiası",
   "question": "Sağlık sitesindeki iddia: 'Aralıklı oruç (16:8), aynı kaloriyi alan klasik diyete göre çok daha fazla kilo verdirir ve insülin direncini tamamen düzeltir.' Bilimsel literatür bu iddianın parçalarını destekliyor mu?",
   "analyst": "Claude (iddia-dogrulama skill)",
   "scope_notes": ("Veri seti yok; yalnızca literatür kanıtı. Kaynaklar WebSearch ile bulundu; WebFetch ve doğrudan HTTP erişimi egress proxy tarafından engellendiği için hiçbir kaynağın tam metni/özeti doğrudan okunamadı — bulgular arama motoru özetlerinden alındı, bu yüzden tüm kaynaklarda claim_matches_source=null (×0.7). "
                   "Varsayımlar: (1) 'klasik diyet' = sürekli günlük kalori kısıtlaması (CER/CR); (2) 'çok daha fazla' = klinik olarak büyük ek kayıp (≥%3 vücut ağırlığı / ≥3 kg); (3) 'tamamen düzeltir' = insülin direncinin normalleşmesi/ortadan kalkması; (4) popülasyon = aşırı kilolu/obez yetişkinler. "
                   "Bağımlılık: meta-analizler (S1–S4) birbirleriyle ve bazı bireysel RCT'lerle (Liu, Jamshed, Lin, Lowe, Pavlou) örtüşüyor. Meta-analizler tek kümede (MA_havuzu) toplandı; bireysel RCT'ler ayrı kümelerde. Bu bir miktar çift sayım içerir; etkisi 'varyant_tek_kume' alt klasöründeki duyarlılık çalıştırmasıyla (tüm kilo/insülin karşılaştırma kanıtı tek kümede) gösterildi. "
                   "Sağlık iddiası olduğu için karar eşikleri sıkılaştırıldı: [0.95, 0.80, 0.30, 0.10]."),
   "revisions": []
 },
 "settings": {"decision_thresholds": [0.95, 0.80, 0.30, 0.10]},
 "claims": claims,
 "evidence": ev,
}
if len(sys.argv) > 1 and sys.argv[1] == "tek":
    for e in data["evidence"]:
        if e["cluster"] not in ("Thieme_HMIF", "Cienfuegos2020"):
            e["cluster"] = "TRE_literatur_tek_kume"
    data["project"]["title"] += " — VARYANT: tüm örtüşen RCT/MA kanıtı tek kümede"
    OUT = OUT.replace("outputs/girdi.json", "outputs/varyant_tek_kume/girdi.json")
import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(data, open(OUT, "w"), ensure_ascii=False, indent=2)
print("yazıldı", OUT, len(claims), len(ev))
