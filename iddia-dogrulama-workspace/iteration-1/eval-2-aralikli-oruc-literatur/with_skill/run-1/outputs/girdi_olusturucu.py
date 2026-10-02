#!/usr/bin/env python3
"""Aralıklı oruç (16:8) iddiası için girdi.json üretir."""
import json
import sys

OUT = sys.argv[1]

VER = {
    "exists": True,
    "claim_matches_source": None,
    "method": "WebSearch sonuç özeti (başlık/URL doğrulandı); WebFetch tüm yayıncı alan adlarında egress proxy tarafından engellendi, tam metin veya özet doğrudan okunamadı",
}
VER_UNSURE = {
    "exists": None,
    "claim_matches_source": None,
    "method": "Bulgu WebSearch özetinde geçti ama hangi yayına ait olduğu kesin eşleştirilemedi; birincil kaynak açılamadı",
}

TRE_CER = "TRE_16_8_vs_esit_kalorili_diyet"
TRE_KON = "TRE_16_8_vs_mudahalesiz_kontrol"
KILO = "kilo_kaybi"
IR = "insulin_direnci"

COUNTER_LOG_KILO = [
    "Cochrane review 2026 intermittent fasting adults overweight obesity",
    "Semnani-Azad 2025 BMJ intermittent fasting network meta-analysis time restricted eating continuous energy restriction",
    "Is isocaloric intermittent fasting superior to calorie restriction meta-analysis",
    "Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity (Maruthur 2024)",
    "Lowe 2020 TREAT randomized clinical trial 16:8 time-restricted eating (null sonuç)",
    "Liu 2022 NEJM calorie restriction with or without time-restricted eating (null sonuç)",
]
COUNTER_LOG_IR = [
    "Time-restricted eating with calorie restriction meta-analysis HOMA-IR versus calorie restriction alone",
    "Effect of Isocaloric TRE ... glucose homeostasis (Maruthur 2024)",
    "time-restricted eating meta-analysis versus ad libitum control HOMA-IR (null bulgular)",
    "Gabel 2018 16:8 time restricted feeding insulin resistance no change",
    "time-restricted eating normalizes insulin resistance reversal remission evidence HOMA-IR normal range trial",
]

PRIOR_NOTE = ("Önsel, bu oturumdaki literatür aramasından ÖNCE, iddianın yapısına ve rubric §9 rehberine göre belirlendi. "
              "Not: analistin (modelin) alana dair genel ön bilgisi vardır; bu tamamen 'kör' bir önsel değildir — duyarlılık analizi bu etkiyi ölçer.")

claims = [
    {
        "id": "C1", "text": "16:8 aralıklı oruç (TRE), aynı kaloriyi alan klasik (sürekli kalori kısıtlı) diyete göre daha fazla kilo kaybı sağlar",
        "x": TRE_CER, "y": KILO, "relation": "positive", "causal": True,
        "population": "Fazla kilolu/obez yetişkinler", "timeframe": "≥ 8 hafta",
        "conditions": "Enerji alımı iki kolda eşit (izokalorik) veya aynı kalori hedefi",
        "prior": 0.35,
        "prior_rationale": "Enerji dengesi ilkesine göre eşit kaloride büyük fark beklenmez; sirkadiyen ritim hipotezi makul ama tartışmalı → 'makul ama tartışmalı' aralığının alt ucu. " + PRIOR_NOTE,
        "prior_set_before_evidence": True, "counter_evidence_searched": True, "counter_search_log": COUNTER_LOG_KILO,
        "source_of_claim": "Kullanıcının aktardığı sağlık sitesi metni",
    },
    {
        "id": "C2", "text": "16:8 TRE, eşit kalorili klasik diyete göre 'çok daha fazla' (klinik olarak anlamlı, tutarlı biçimde ≥ ~2 kg / ≥ ~2% fazladan) kilo kaybı sağlar",
        "relation": "positive", "causal": True,
        "population": "Fazla kilolu/obez yetişkinler", "timeframe": "≥ 3 ay",
        "conditions": "'Çok daha fazla' ifadesi, analist varsayımıyla klinik anlamlı ve tekrarlanabilir üstünlük olarak işlemselleştirildi",
        "prior": 0.15,
        "prior_rationale": "Büyüklük vurgusu ('çok daha fazla') olağanüstü bir iddia; tek sağlık sitesinden gelen viral tarzda ifade → rubric §9 'şaşırtıcı/olağanüstü' aralığı. " + PRIOR_NOTE,
        "prior_set_before_evidence": True, "counter_evidence_searched": True, "counter_search_log": COUNTER_LOG_KILO,
        "source_of_claim": "Kullanıcının aktardığı sağlık sitesi metni",
    },
    {
        "id": "C3", "text": "RAKİP: Eşit kaloride 16:8 TRE ile klasik diyet arasında kilo kaybı açısından (anlamlı) fark yoktur",
        "x": TRE_CER, "y": KILO, "relation": "none", "causal": True,
        "population": "Fazla kilolu/obez yetişkinler", "timeframe": "≥ 8 hafta",
        "prior": 0.55,
        "prior_rationale": "Enerji dengesi ilkesinin doğrudan öngörüsü; C1'in rakibi. C1+C3 önselleri toplamı < 1 (ters yönlü fark olasılığına pay bırakıldı). " + PRIOR_NOTE,
        "prior_set_before_evidence": True, "counter_evidence_searched": True, "counter_search_log": COUNTER_LOG_KILO,
        "source_of_claim": "Analist (rakip iddia)",
    },
    {
        "id": "C4", "text": "ZAYIF VERSİYON: 16:8 TRE, hiçbir diyet müdahalesi olmayan kontrole göre kilo kaybı sağlar (kalori kendiliğinden azaldığı için)",
        "x": TRE_KON, "y": KILO, "relation": "positive", "causal": True,
        "population": "Fazla kilolu/obez yetişkinler", "timeframe": "≥ 8 hafta",
        "prior": 0.6,
        "prior_rationale": "Yeme penceresini daraltmak çoğu kişide toplam alımı azaltır → makul; büyüklüğü belirsiz. Nedensel iddianın 'ilişkisel versiyonu' yerine konan daha zayıf/gerçekçi versiyon. " + PRIOR_NOTE,
        "prior_set_before_evidence": True, "counter_evidence_searched": True, "counter_search_log": COUNTER_LOG_KILO,
        "source_of_claim": "Analist (iddianın zayıf versiyonu)",
    },
    {
        "id": "C5", "text": "16:8 TRE insülin direncini azaltır (HOMA-IR düşer; müdahalesiz/serbest beslenme kontrolüne göre)",
        "x": TRE_KON, "y": IR, "relation": "negative", "causal": True,
        "population": "Fazla kilolu/obez yetişkinler, prediyabet/metabolik sendrom dahil", "timeframe": "≥ 8 hafta",
        "prior": 0.55,
        "prior_rationale": "Kilo kaybı insülin duyarlılığını genelde iyileştirir; TRE'nin kilo kaybı küçük olabilir → makul ama tartışmalı. " + PRIOR_NOTE,
        "prior_set_before_evidence": True, "counter_evidence_searched": True, "counter_search_log": COUNTER_LOG_IR,
        "source_of_claim": "Kullanıcı iddiasının 'insülin direnci' kısmının zayıf versiyonu",
    },
    {
        "id": "C6", "text": "16:8 TRE, eşit kalorili klasik diyete göre insülin direncini daha fazla azaltır",
        "x": TRE_CER, "y": IR, "relation": "negative", "causal": True,
        "population": "Fazla kilolu/obez yetişkinler, prediyabet dahil", "timeframe": "≥ 5 hafta",
        "prior": 0.35,
        "prior_rationale": "Kilodan bağımsız sirkadiyen etki hipotezi var (erken TRE), ancak tartışmalı → C1 ile aynı mantık. " + PRIOR_NOTE,
        "prior_set_before_evidence": True, "counter_evidence_searched": True, "counter_search_log": COUNTER_LOG_IR,
        "source_of_claim": "Kullanıcı iddiasının kalori-karşılaştırmalı okuması",
    },
    {
        "id": "C7", "text": "RAKİP: Eşit kaloride 16:8 TRE ile klasik diyet arasında insülin direnci açısından fark yoktur",
        "x": TRE_CER, "y": IR, "relation": "none", "causal": True,
        "population": "Fazla kilolu/obez yetişkinler", "timeframe": "≥ 5 hafta",
        "prior": 0.55,
        "prior_rationale": "Metabolik iyileşmenin büyük ölçüde kilo/enerji açığından geldiği hipotezi; C6'nın rakibi. " + PRIOR_NOTE,
        "prior_set_before_evidence": True, "counter_evidence_searched": True, "counter_search_log": COUNTER_LOG_IR,
        "source_of_claim": "Analist (rakip iddia)",
    },
    {
        "id": "C8", "text": "16:8 TRE insülin direncini TAMAMEN düzeltir (normal aralığa getirir / ortadan kaldırır)",
        "relation": "positive", "causal": True,
        "population": "İnsülin direnci olan yetişkinler",
        "prior": 0.05,
        "prior_rationale": "'Tamamen düzeltir' mutlak ve çok faktörlü bir durum (genetik, yağ dağılımı, aktivite, uyku) için olağanüstü bir iddia; hiçbir diyet müdahalesi için tipik değildir → rubric §9 olağanüstü iddia aralığının altı. " + PRIOR_NOTE,
        "prior_set_before_evidence": True, "counter_evidence_searched": True, "counter_search_log": COUNTER_LOG_IR,
        "source_of_claim": "Kullanıcının aktardığı sağlık sitesi metni",
    },
]

def src(id_, citation, url, design, year, n, cluster, **kw):
    d = {"id": id_, "kind": "source", "citation": citation, "url": url, "design": design,
         "year": year, "n": n, "peer_reviewed": True, "cluster": cluster,
         "verification": kw.pop("verification", VER)}
    d.update(kw)
    return d

E = []
# ---------------- Kilo: TRE vs eşit kalorili diyet (C1, C3) -- serbest yaşam RCT havuzu
CL_HAVUZ_CER = "havuz_TRE_vs_CER_serbest_yasam"
E += [
    src("S1", "Semnani-Azad Z, Khan TA, et al. (2025). Intermittent fasting strategies and their effects on body weight and other cardiometabolic risk factors: systematic review and network meta-analysis of randomised clinical trials. BMJ 389:e082007.",
        "https://doi.org/10.1136/bmj-2024-082007", "meta_analysis", 2025, None, CL_HAVUZ_CER,
        x=TRE_CER, y=KILO, finding="none", strength="strong", causal_design=True,
        quote="Compared with continuous energy restriction, alternate day fasting was the only form of intermittent fasting diet strategy to show benefit in body weight reduction (MD −1.29 kg) ... intermittent fasting diets have similar benefits to continuous energy restriction for weight loss and cardiometabolic risk factors.",
        notes="99 RCT. TRE, sürekli enerji kısıtlamasına (CER) göre ek kilo kaybı göstermedi. Katılımcı sayısı doğrulanamadı → n=null. Birincil RCT'lerin (S3–S6) çoğunu içerdiği için aynı kümede."),
    src("S2", "Garegnani LI, Oltra G, Ivaldi D, et al. (2026). Intermittent fasting for adults with overweight or obesity. Cochrane Database Syst Rev, Issue 2, CD015610.pub2.",
        "https://doi.org/10.1002/14651858.CD015610.pub2", "systematic_review", 2026, 1995, CL_HAVUZ_CER,
        x=TRE_CER, y=KILO, finding="none", strength="moderate", causal_design=True,
        quote="Compared to regular dietary advice, intermittent fasting may result in little to no difference in percentage from baseline weight loss (MD −0.33, 95% CI −0.92 to 0.26; 21 studies, 1430 participants; low-certainty evidence).",
        notes="22 RCT, 1995 yetişkin. Karşılaştırma 'olağan diyet önerisi' (her zaman izokalorik değil) ve aralıklı orucun tüm türleri (yalnızca 16:8 değil) → strength moderate."),
    src("S3", "Liu D, Huang Y, Huang C, et al. (2022). Calorie Restriction with or without Time-Restricted Eating in Weight Loss. N Engl J Med 386:1495–1504.",
        "https://doi.org/10.1056/NEJMoa2114833", "rct", 2022, 139, CL_HAVUZ_CER,
        x=TRE_CER, y=KILO, strength="moderate",
        reported_stats={"t": 1.61, "df": 137, "n": 139},
        quote="Weight loss at 12 months: −8.0 kg (TRE) vs −6.3 kg (daily calorie restriction); net difference −1.8 kg (95% CI −4.0 to 0.4; P=0.11).",
        notes="İki kola aynı kalori kısıtlaması (8:00–16:00 penceresi = 16:8). t, iki yönlü P=0.11 ve df≈137'den türetildi (TRE lehine pozitif yön)."),
    src("S4", "Jamshed H, Steger FL, Bryan DR, et al. (2022). Effectiveness of Early Time-Restricted Eating for Weight Loss, Fat Loss, and Cardiometabolic Health in Adults With Obesity: A Randomized Clinical Trial. JAMA Intern Med 182(9):953–962.",
        "https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2794819", "rct", 2022, 90, CL_HAVUZ_CER,
        x=TRE_CER, y=KILO, strength="moderate",
        reported_stats={"t": 3.15, "df": 88, "n": 90},
        quote="The early time-restricted eating plus energy restriction intervention was more effective for losing weight (−2.3 kg; P = .002) but did not affect body fat (−1.4 kg; P = .09).",
        notes="14 hafta; eTRE (07:00–15:00, 8 saat pencere) + enerji kısıtlaması vs ≥12 saat pencere + aynı enerji kısıtlaması hedefi. t, P=0.002 ve df≈88'den türetildi. İddiayı destekleyen en güçlü birincil çalışma."),
    src("S5", "Lin S, Cienfuegos S, Ezpeleta M, et al. (2023). Time-Restricted Eating Without Calorie Counting for Weight Loss in a Racially Diverse Population: A Randomized Controlled Trial. Ann Intern Med 176(7):885–895.",
        "https://www.acpjournals.org/doi/10.7326/M23-0052", "rct", 2023, 90, CL_HAVUZ_CER,
        x=TRE_CER, y=KILO, finding="none", strength="moderate",
        quote="TRE and CR led to similar, significant reductions in weight compared to control.",
        notes="12 ay; 8 saat TRE (12:00–20:00, kalori saymadan) vs %25 kalori kısıtlaması vs kontrol. Tasarım gereği izokalorik değil ama iki kolda benzer enerji açığı → moderate."),
    src("S6", "Pavlou V, Cienfuegos S, Lin S, et al. (2023). Effect of Time-Restricted Eating on Weight Loss in Adults With Type 2 Diabetes: A Randomized Clinical Trial. JAMA Netw Open 6(10):e2339337.",
        "https://doi.org/10.1001/jamanetworkopen.2023.39337", "rct", 2023, 75, CL_HAVUZ_CER,
        x=TRE_CER, y=KILO, finding="positive", strength="weak",
        quote="TRE was more effective for weight loss (−3.6%) than CR (−1.8%) compared with controls.",
        notes="Tip 2 diyabetli obez yetişkinler, 6 ay. Kalori eşit değil (TRE serbest, CR %25 kısıtlı); TRE–CR doğrudan farkının anlamlılığı özetten doğrulanamadı → weak."),
    src("S7", "(2023). Time-restricted eating with calorie restriction on weight loss and cardiometabolic risk: a systematic review and meta-analysis. Eur J Clin Nutr (s41430-023-01311-w).",
        "https://www.nature.com/articles/s41430-023-01311-w", "meta_analysis", 2023, None, CL_HAVUZ_CER,
        x=TRE_CER, y=KILO, finding="positive", strength="moderate", causal_design=True,
        quote="The pooled results showed that time-restricted eating (TRE) with calorie restriction (CR) reduced body weight, fat mass, and waist circumference significantly.",
        notes="TRE+CR vs yalnız CR. Yazar listesi özetten doğrulanamadı. Küçük ama anlamlı ek kilo kaybı bildiriyor (büyüklük doğrulanamadı)."),
]
# ---------------- Kilo: izokalorik kontrollü / izokalorik meta-analiz kümesi
CL_IZO = "izokalorik_kontrollu_beslenme"
E += [
    src("S8", "Maruthur NM, et al. (2024). Effect of Isocaloric, Time-Restricted Eating on Body Weight in Adults With Obesity: A Randomized Controlled Trial. Ann Intern Med 177(5).",
        "https://www.acpjournals.org/doi/10.7326/M23-3132", "rct", 2024, None, CL_IZO,
        x=TRE_CER, y=KILO, finding="none", strength="strong",
        quote="At 12 weeks, weight decreased by 2.3 kg in the TRE group and by 2.6 kg in the UEP group ... in the setting of isocaloric eating, TRE did not decrease weight or improve glucose homeostasis relative to a UEP.",
        notes="Tüm yemeklerin sağlandığı kontrollü izokalorik besleme — iddianın 'aynı kalori' koşulunu en doğrudan test eden tasarım. Pencere 10 saat (16:8 değil) ve kalorilerin %80'i 13:00'ten önce. n doğrulanamadı."),
    src("S9", "(2024/2025). Is isocaloric intermittent fasting superior to calorie restriction? A systematic review and meta-analysis of RCTs. Nutr Metab Cardiovasc Dis (S0939-4753(24)00439-3).",
        "https://www.nmcd-journal.com/article/S0939-4753(24)00439-3/fulltext", "meta_analysis", 2024, None, CL_IZO,
        x=TRE_CER, y=KILO, finding="none", strength="moderate", causal_design=True,
        quote="Isocaloric intermittent fasting (IF) is not superior to calorie restriction (CR) in enhancing health outcomes in adults and the elderly. The health benefits induced by intermittent fasting are calorie restriction dependent.",
        notes="Tüm IF türleri; kısa dönemde yağ kütlesi lehine küçük fark bildirildi. Yazarlar doğrulanamadı."),
]
# ---------------- C2: 'çok daha fazla' (iddiaya özgü, stance)
E += [
    src("S10", "Semnani-Azad Z, et al. (2025). BMJ 389:e082007 — 'çok daha fazla' büyüklük iddiası açısından.",
        "https://doi.org/10.1136/bmj-2024-082007", "meta_analysis", 2025, None, CL_HAVUZ_CER,
        claim_id="C2", stance="contradicts", strength="strong", causal_design=True,
        quote="Compared with continuous energy restriction, alternate day fasting was the only form of intermittent fasting diet strategy to show benefit in body weight reduction.",
        notes="TRE için CER'e karşı anlamlı fark yok; 'çok daha fazla' ile doğrudan çelişir."),
    src("S11", "Garegnani LI, et al. (2026). Cochrane CD015610.pub2 — büyüklük iddiası açısından.",
        "https://doi.org/10.1002/14651858.CD015610.pub2", "systematic_review", 2026, 1995, CL_HAVUZ_CER,
        claim_id="C2", stance="contradicts", strength="strong", causal_design=True,
        quote="Although participants who used intermittent fasting lost more weight than those who received no treatment, the amount of weight lost was smaller than what is considered clinically meaningful.",
        notes="Müdahalesiz kontrole karşı bile klinik anlamlı eşiğin altında; olağan diyete karşı fark ~0.3 puan."),
    src("S12", "Liu D, et al. (2022). NEJM 386:1495 — büyüklük iddiası açısından.",
        "https://doi.org/10.1056/NEJMoa2114833", "rct", 2022, 139, CL_HAVUZ_CER,
        claim_id="C2", stance="contradicts", strength="moderate",
        quote="Net difference −1.8 kg (95% CI −4.0 to 0.4; P=0.11).",
        notes="Fark istatistiksel olarak anlamlı değil; GA geniş."),
    src("S13", "Jamshed H, et al. (2022). JAMA Intern Med — büyüklük iddiası açısından.",
        "https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2794819", "rct", 2022, 90, CL_HAVUZ_CER,
        claim_id="C2", stance="supports", strength="weak",
        quote="More effective for losing weight (−2.3 kg; P = .002) but did not affect body fat.",
        notes="14 haftada 2.3 kg ek kayıp — eşiğe yakın; ama yağ kaybı farkı yok ve tek çalışma → weak destek."),
    src("S14", "Maruthur NM, et al. (2024). Ann Intern Med 177(5) — büyüklük iddiası açısından.",
        "https://www.acpjournals.org/doi/10.7326/M23-3132", "rct", 2024, None, CL_IZO,
        claim_id="C2", stance="contradicts", strength="strong",
        quote="Weight decreased by 2.3 kg in the TRE group and by 2.6 kg in the UEP group.",
        notes="Kontrollü izokalorik beslemede TRE kolu biraz DAHA AZ kilo verdi."),
]
# ---------------- Kilo: TRE vs müdahalesiz kontrol (C4)
CL_HAVUZ_KON = "havuz_TRE_vs_kontrol"
E += [
    src("S15", "(2023). Is time-restricted eating (8/16) beneficial for body weight and metabolism of obese and overweight adults? A systematic review and meta-analysis of randomized controlled trials. (PMC10002957).",
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10002957/", "meta_analysis", 2023, None, CL_HAVUZ_KON,
        x=TRE_KON, y=KILO, finding="positive", strength="strong", causal_design=True,
        quote="Participants following TRE (8/16) showed significant body weight reduction (mean difference: −1.48 kg) and fat mass reduction (−1.09 kg).",
        notes="Özellikle 16:8'e odaklı meta-analiz. Dergi/yazarlar özetten doğrulanamadı."),
    src("S16", "Garegnani LI, et al. (2026). Cochrane CD015610.pub2 — müdahalesiz kontrol karşılaştırması.",
        "https://doi.org/10.1002/14651858.CD015610.pub2", "systematic_review", 2026, 1995, CL_HAVUZ_KON,
        x=TRE_KON, y=KILO, finding="positive", strength="moderate", causal_design=True,
        quote="Participants who used intermittent fasting lost more weight than those who received no treatment, [but] the amount ... was smaller than what is considered clinically meaningful.",
        notes="Tüm IF türleri; yön pozitif, büyüklük küçük."),
    src("S17", "Lin S, et al. (2023). Ann Intern Med 176(7):885–895 — kontrol karşılaştırması.",
        "https://www.acpjournals.org/doi/10.7326/M23-0052", "rct", 2023, 90, CL_HAVUZ_KON,
        x=TRE_KON, y=KILO, finding="positive", strength="strong",
        quote="Compared with the control group, the time-restricted eating group reduced on average 425 more kilocalories per day and lost 4.61 kg more weight at 12 months.",
        notes="Mekanizmayı da gösteriyor: TRE kolu günde ~425 kcal daha az yedi."),
    src("S18", "Pavlou V, et al. (2023). JAMA Netw Open 6(10):e2339337 — kontrol karşılaştırması.",
        "https://doi.org/10.1001/jamanetworkopen.2023.39337", "rct", 2023, 75, CL_HAVUZ_KON,
        x=TRE_KON, y=KILO, finding="positive", strength="moderate",
        quote="TRE was more effective for weight loss (−3.6%) than CR (−1.8%) compared with controls."),
    src("S19", "Cienfuegos S, Gabel K, Kalam F, et al. (2020). Effects of 4- and 6-h Time-Restricted Feeding on Weight and Cardiometabolic Health: A Randomized Controlled Trial in Adults with Obesity. Cell Metab 32(3):366–378.",
        "https://www.cell.com/cell-metabolism/fulltext/S1550-4131(20)30319-3", "rct", 2020, None, CL_HAVUZ_KON,
        x=TRE_KON, y=KILO, finding="positive", strength="moderate",
        quote="After 8 weeks, 4- and 6-h TRF produced comparable reductions in body weight (∼3%), insulin resistance, and oxidative stress, versus controls ... reduced energy intake by ∼550 kcal per day.",
        notes="16:8 değil (20:4 ve 18:6). Etki enerji alımındaki ~550 kcal düşüşle birlikte."),
    src("S20", "Gabel K, Hoddy KK, Haggerty N, et al. (2018). Effects of 8-hour time restricted feeding on body weight and metabolic disease risk factors in obese adults: A pilot study. Nutr Healthy Aging 4:345–353.",
        "https://journals.sagepub.com/doi/pdf/10.3233/NHA-170036", "quasi_experimental", 2018, None, CL_HAVUZ_KON,
        x=TRE_KON, y=KILO, finding="positive", strength="weak",
        quote="In this trial of 8-h TRF, body weight was reduced by 2.6% after 12 weeks ... 8-h time restricted feeding produces mild caloric restriction and weight loss, without calorie counting.",
        notes="Pilot; tarihsel (eşleştirilmiş) kontrol grubu → quasi_experimental."),
    src("S21", "Lowe DA, Wu N, Rohdin-Bibby L, et al. (2020). Effects of Time-Restricted Eating on Weight Loss and Other Metabolic Parameters in Women and Men With Overweight and Obesity: The TREAT Randomized Clinical Trial. JAMA Intern Med 180(11):1491–1499.",
        "https://doi.org/10.1001/jamainternmed.2020.4153", "rct", 2020, 116, CL_HAVUZ_KON,
        x=TRE_KON, y=KILO, finding="none", strength="moderate",
        quote="Time-restricted eating, in the absence of other interventions, is not more effective in weight loss than eating throughout the day.",
        notes="Doğrudan 16:8 (12:00–20:00) vs 3 öğün; enerji alımında gruplar arası fark yok. WebSearch özetlerinde kilo değişimi sayıları tutarsız olduğundan istatistik girilmedi."),
]
# ---------------- İnsülin direnci: TRE vs kontrol (C5)
CL_IR_KON = "havuz_TRE_IR_vs_kontrol"
E += [
    src("S22", "(2023). Is time-restricted eating (8/16) beneficial ... meta-analysis (PMC10002957) — HOMA-IR.",
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10002957/", "meta_analysis", 2023, None, CL_IR_KON,
        x=TRE_KON, y=IR, finding="negative", strength="moderate", causal_design=True,
        quote="The available evidence indicated that TRE could decrease body weight, fat mass, fasting blood glucose, and HOMA-IR, especially in overweight participants ... HOMA-IR was significantly improved in overweight but not in normal-weight or obese participants.",
        notes="Etki alt gruba bağlı (obezlerde anlamlı değil)."),
    src("S23", "(2025). Effect of 8-Hour Time-Restricted Eating (16/8 TRE) on Glucose Metabolism and Lipid Profile in Adults: A Systematic Review and Meta-Analysis. Nutr Rev (nuaf206).",
        "https://academic.oup.com/nutritionreviews/advance-article/doi/10.1093/nutrit/nuaf206/8373435", "meta_analysis", 2025, None, CL_IR_KON,
        x=TRE_KON, y=IR, finding="negative", strength="moderate", causal_design=True,
        quote="The 16/8 TRE significantly improved levels of fasting glucose, HOMA-IR, fasting insulin, and HDL-C compared to the control diet, though significant improvements in HOMA-IR were only found in studies with intervention durations of 6 months or longer.",
        notes="Doğrudan 16:8. Atıf eşleşmesi WebSearch özetine dayanıyor."),
    src("S24", "Kaynağı kesin eşlenemeyen TRE meta-analizi (13 RCT, n=612; WebSearch özetinde Frontiers Nutr 2025 sonuçlarıyla birlikte geçti).",
        "https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2025.1664412/full", "meta_analysis", 2025, 612, CL_IR_KON,
        x=TRE_KON, y=IR, finding="none", strength="moderate", causal_design=True, verification=VER_UNSURE,
        quote="A meta-analysis of 13 RCTs involving 612 participants found that TRE significantly reduced body weight by 1.927 kg ... TRE showed no significant effects on HOMA-IR.",
        notes="Karşı kanıt; varlık/eşleşme doğrulanamadığı için Q cezalı."),
    src("S25", "Cienfuegos S, et al. (2020). Cell Metab 32(3) — insülin direnci.",
        "https://www.cell.com/cell-metabolism/fulltext/S1550-4131(20)30319-3", "rct", 2020, None, CL_IR_KON,
        x=TRE_KON, y=IR, finding="negative", strength="moderate",
        quote="Both diets produced comparable reductions in body weight, energy intake, insulin resistance, and oxidative stress [versus controls].",
        notes="20:4 / 18:6, 8 hafta; ~%3 kilo kaybıyla birlikte."),
    src("S26", "Gabel K, et al. (2018). Nutr Healthy Aging 4:345 — insülin direnci.",
        "https://journals.sagepub.com/doi/pdf/10.3233/NHA-170036", "quasi_experimental", 2018, None, CL_IR_KON,
        x=TRE_KON, y=IR, finding="none", strength="weak",
        quote="Fasting glucose, fasting insulin, HOMA-IR ... were not significantly different from controls after 12 weeks.",
        notes="Doğrudan 16:8."),
    src("S27", "Lowe DA, et al. (2020). TREAT, JAMA Intern Med — kardiyometabolik sonuçlar.",
        "https://doi.org/10.1001/jamainternmed.2020.4153", "rct", 2020, 116, CL_IR_KON,
        x=TRE_KON, y=IR, finding="none", strength="weak",
        quote="Time-restricted eating did not confer weight loss or cardiometabolic benefits in this study.",
        notes="HOMA-IR'e özgü sayı özetten doğrulanamadı → weak."),
    src("S28", "Manoogian ENC, et al. (2024). Time-Restricted Eating in Adults With Metabolic Syndrome: A Randomized Controlled Trial. Ann Intern Med 177(11).",
        "https://www.acpjournals.org/doi/abs/10.7326/M24-0859", "rct", 2024, 108, "manoogian_TIMET",
        x=TRE_KON, y=IR, finding="negative", strength="weak",
        quote="Compared with SOC, TRE improved HbA1c by −0.10% (95% CI, −0.19% to −0.003%).",
        notes="Kontrol = standart beslenme danışmanlığı. Ölçüt HbA1c (glisemi), doğrudan insülin direnci değil; etki küçük → weak."),
]
# ---------------- İnsülin direnci: TRE vs eşit kalorili diyet (C6, C7)
E += [
    src("S29", "Liu D, et al. (2022). NEJM 386:1495 — HOMA-IR.",
        "https://doi.org/10.1056/NEJMoa2114833", "rct", 2022, 139, CL_HAVUZ_CER,
        x=TRE_CER, y=IR, finding="none", strength="moderate",
        quote="Fasting glucose levels, 2-hour postprandial glucose levels, scores on the insulin disposition index and HOMA–IR, and lipid levels were similar in the two groups."),
    src("S30", "(2023). Eur J Clin Nutr TRE+CR meta-analizi — HOMA-IR.",
        "https://www.nature.com/articles/s41430-023-01311-w", "meta_analysis", 2023, 329, CL_HAVUZ_CER,
        x=TRE_CER, y=IR, finding="none", strength="moderate", causal_design=True,
        quote="HOMA-IR and HOMA-β were investigated in four studies (329 participants) and two articles (127 participants) respectively, but no statistically significant differences were found.",
        notes="n = HOMA-IR analizine giren katılımcı sayısı."),
    src("S31", "Jamshed H, et al. (2022). JAMA Intern Med — kardiyometabolik sonuçlar.",
        "https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2794819", "rct", 2022, 90, CL_HAVUZ_CER,
        x=TRE_CER, y=IR, finding="none", strength="weak",
        quote="The lack of effects on cardiometabolic outcomes differed from other studies of time-restricted eating, which have shown improvements in levels of glucose and fasting insulin, as well as insulin sensitivity.",
        notes="Tartışma bölümünden aktarım → weak."),
    src("S32", "Semnani-Azad Z, et al. (2025). BMJ 389:e082007 — kardiyometabolik risk faktörleri.",
        "https://doi.org/10.1136/bmj-2024-082007", "meta_analysis", 2025, None, CL_HAVUZ_CER,
        x=TRE_CER, y=IR, finding="none", strength="weak", causal_design=True,
        quote="Intermittent fasting diets have similar benefits to continuous energy restriction for weight loss and cardiometabolic risk factors.",
        notes="Genel ifade; TRE'ye özgü HOMA-IR sayısı doğrulanamadı → weak. (Bir WebSearch özeti IF'nin HOMA-IR'ü CER'den fazla düşürdüğünü yazdı ama bunun BMJ makalesine ait olduğu doğrulanamadığı için kullanılmadı.)"),
    src("S33", "Pavlou V, et al. (2023). JAMA Netw Open — HbA1c (TRE vs CR).",
        "https://doi.org/10.1001/jamanetworkopen.2023.39337", "rct", 2023, 75, CL_HAVUZ_CER,
        x=TRE_CER, y=IR, finding="none", strength="weak",
        quote="Changes in HbA1c levels did not differ between the TRE (−0.91%) and CR (−0.94%) groups compared with controls.",
        notes="HbA1c, insülin direncinin dolaylı göstergesi; kalori eşit değil → weak."),
    src("S34", "Maruthur NM, et al. (2024). Ann Intern Med 177(5) — glukoz homeostazı / HOMA-IR.",
        "https://www.acpjournals.org/doi/10.7326/M23-3132", "rct", 2024, None, CL_IZO,
        x=TRE_CER, y=IR, finding="none", strength="strong",
        quote="Change in glycemic measures did not differ between groups. Secondary outcomes ... fasting glucose, HOMA-IR, glucose AUC by OGTT, and glycated albumin ... TRE did not ... improve glucose homeostasis relative to a UEP.",
        notes="Prediyabet / diyetle kontrollü diyabet; kontrollü izokalorik besleme."),
    src("S35", "Sutton EF, Beyl R, Early KS, et al. (2018). Early Time-Restricted Feeding Improves Insulin Sensitivity, Blood Pressure, and Oxidative Stress Even without Weight Loss in Men with Prediabetes. Cell Metab 27(6):1212–1221.",
        "https://www.cell.com/cell-metabolism/fulltext/S1550-4131(18)30253-5", "rct", 2018, 8, CL_IZO,
        x=TRE_CER, y=IR, finding="negative", strength="moderate", preregistered=None,
        quote="eTRF reduced mean and peak insulin values by 26 ± 9 mU/L and 35 ± 13 mU/L ... investigators maintaining oversight and matching caloric intake across study arms.",
        notes="Randomize çapraz, kontrollü izokalorik besleme; 6 saat ERKEN pencere (18:6, son öğün 15:00), 16:8 değil; n=8 erkek. İddia lehine en güçlü mekanistik kanıt."),
    src("S36", "(2024/2025). NMCD izokalorik IF vs CR meta-analizi — HOMA-IR.",
        "https://www.nmcd-journal.com/article/S0939-4753(24)00439-3/fulltext", "meta_analysis", 2024, None, CL_IZO,
        x=TRE_CER, y=IR, finding="negative", strength="weak", causal_design=True,
        quote="IF groups showed significant reduction in HOMA-IR in the long term (P = 0.04).",
        notes="Genel sonuç 'IF üstün değil' olmasına rağmen uzun dönem HOMA-IR alt analizi IF lehine; P sınırda, tüm IF türleri → weak."),
    src("S37", "Effects of Time-Restricted Eating on Insulin Sensitivity, Glycemic Control, and Metabolic Outcomes in Low- and Middle-Income Countries: A Systematic Review (PMC13498806) — aktarılan 'Lucknow' hipokalorik TRE kohortu.",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC13498806/", "unknown", None, None, "lmic_lucknow",
        x=TRE_CER, y=IR, finding="negative", strength="weak", verification=VER_UNSURE,
        quote="The Lucknow hypocaloric TRE cohort achieved a HOMA-IR reduction of 2.6 ± 1.9, significantly outperforming standard caloric restriction at 1.55 ± 1.2 (p = 0.024).",
        notes="Birincil çalışma tanımlanamadı; tasarım bilinmiyor → design=unknown; ikincil aktarım → exists=null."),
]
# ---------------- C8: 'tamamen düzeltir' (iddiaya özgü)
E += [
    src("S38", "Maruthur NM, et al. (2024). Ann Intern Med — 'tamamen düzeltir' açısından.",
        "https://www.acpjournals.org/doi/10.7326/M23-3132", "rct", 2024, None, CL_IZO,
        claim_id="C8", stance="contradicts", strength="strong",
        quote="TRE did not decrease weight or improve glucose homeostasis relative to a UEP.",
        notes="Prediyabetik obezlerde izokalorik TRE ile iyileşme yok; tam düzelme hiç yok."),
    src("S39", "(2025). Nutr Rev 16/8 TRE meta-analizi — etki büyüklüğü açısından.",
        "https://academic.oup.com/nutritionreviews/advance-article/doi/10.1093/nutrit/nuaf206/8373435", "meta_analysis", 2025, None, CL_IR_KON,
        claim_id="C8", stance="contradicts", strength="moderate", causal_design=True,
        quote="Significant improvements in HOMA-IR were only found in studies with intervention durations of 6 months or longer.",
        notes="İyileşme kısmi ve koşullu; normalizasyon (tam düzelme) bildirilmiyor."),
    src("S40", "(2023). PMC10002957 16:8 meta-analizi — etki büyüklüğü açısından.",
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10002957/", "meta_analysis", 2023, None, CL_IR_KON,
        claim_id="C8", stance="contradicts", strength="moderate", causal_design=True,
        quote="HOMA-IR was significantly improved in overweight but not in normal-weight or obese participants.",
        notes="Obezlerde anlamlı değil → 'tamamen düzeltir' ile çelişir."),
    src("S41", "Gabel K, et al. (2018). Nutr Healthy Aging — 16:8 ile HOMA-IR.",
        "https://journals.sagepub.com/doi/pdf/10.3233/NHA-170036", "quasi_experimental", 2018, None, CL_IR_KON,
        claim_id="C8", stance="contradicts", strength="weak",
        quote="HOMA-IR ... not significantly different from controls after 12 weeks."),
    src("S42", "Sutton EF, et al. (2018). Cell Metab — 'tamamen düzeltir' açısından.",
        "https://www.cell.com/cell-metabolism/fulltext/S1550-4131(18)30253-5", "rct", 2018, 8, CL_IZO,
        claim_id="C8", stance="mixed", strength="weak",
        quote="Prediabetic men following early time-restricted feeding improved their insulin sensitivity ... without losing weight.",
        notes="Anlamlı iyileşme var ama normalizasyon bildirilmiyor; 18:6 erken pencere → mixed."),
    src("S43", "Cienfuegos S, et al. (2020). Cell Metab — 'tamamen düzeltir' açısından.",
        "https://www.cell.com/cell-metabolism/fulltext/S1550-4131(20)30319-3", "rct", 2020, None, CL_IR_KON,
        claim_id="C8", stance="mixed", strength="weak",
        quote="Comparable reductions in ... insulin resistance ... versus controls.",
        notes="Azalma var, tam düzelme bildirilmiyor → mixed."),
]

for e in E:
    if e.get("preregistered", "x") is None:
        e.pop("preregistered")
    if e.get("year") is None:
        e.pop("year")

doc = {
    "project": {
        "title": "Aralıklı oruç (16:8) — kilo kaybı ve insülin direnci iddiası",
        "question": "\"Aralıklı oruç (16:8), aynı kaloriyi alan klasik diyete göre çok daha fazla kilo verdirir ve insülin direncini tamamen düzeltir\" iddiası bilimsel literatürle destekleniyor mu?",
        "analyst": "Claude (iddia-dogrulama skill'i)",
        "scope_notes": (
            "Veri seti yok; yalnızca kaynak kanıtı. Web araması (WebSearch) çalıştı, ancak WebFetch tüm yayıncı/indeks alan adlarında "
            "(pubmed, pmc, nejm, jamanetwork, bmj, cochrane, researchgate, europepmc, crossref, openalex) egress proxy tarafından engellendi. "
            "Bu nedenle tüm kaynaklarda claim_matches_source=null (yalnızca arama özeti) — Q puanları ×0.7 cezalı. "
            "Kümeleme: bir meta-analiz ile içerdiği birincil RCT'ler bağımsız sayılmadı; aynı soruyu yanıtlayan, örtüşen meta-analizler ve bunların içerdiği "
            "RCT'ler tek kümeye konuldu (rubric §3). Kontrollü izokalorik besleme çalışmaları (Maruthur 2024, Sutton 2018) ve izokalorik IF meta-analizi ayrı bir küme. "
            "16:8 = 8 saatlik yeme penceresi; 6 saat/10 saat pencereli çalışmalar notlarda belirtildi. "
            "Nedensel iddianın 'ilişkisel versiyonu' yerine (müdahale iddiası RCT'lerle test edildiğinden anlamsız olurdu) 'zayıf versiyon' C4/C5 eklendi: TRE vs hiçbir müdahale. "
            "Sağlık konusu olduğundan karar eşikleri sıkılaştırıldı: [0.95, 0.80, 0.30, 0.10]."
        ),
        "revisions": ["İlk çalıştırmadan sonra: S37'nin tasarımı 'rct' olarak tahmin edilmişti; SKILL.md 'kontrol edemediğin şeyi tahmin etme' kuralı gereği 'unknown' yapıldı (kodlama düzeltmesi; sonuçtan bağımsız, iddia lehine olan bir kanıtın ağırlığını AZALTIR)."],
    },
    "settings": {"decision_thresholds": [0.95, 0.80, 0.30, 0.10]},
    "claims": claims,
    "evidence": E,
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
print("ok", len(claims), "claims", len(E), "evidence")
