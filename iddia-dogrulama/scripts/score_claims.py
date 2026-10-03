#!/usr/bin/env python3
"""İddia + kanıt girdisinden ölçülebilir doğrulama meta verisi ve raporu üretir.

Kullanım:
  python score_claims.py girdi.json --out-dir sonuc/ [--lang tr|en]

Çıktılar:
  sonuc/metadata.json  – makinece okunabilir tüm skorlar, izler ve bayraklar
  sonuc/rapor.md       – insan için özet rapor (sonda "Yorum ve Uygulama" bölümü boş bırakılır)

Her sayının nasıl hesaplandığı references/scoring_rubric.md içinde açıklanır.
Girdi biçimi references/metadata_schema.md içinde tanımlıdır.
"""
import argparse
import datetime as dt
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import statlib as S  # noqa: E402

SCHEMA_VERSION = "1.0"
LN10 = math.log(10)

# ----------------------------------------------------------------- ayarlar

DEFAULTS = {
    "rho_within_cluster": 0.5,      # aynı kümedeki kanıtların varsayılan korelasyonu
    "log10_lr_cap": 2.0,            # tek kanıt en fazla LR=100 (veya 1/100) etkisi yapabilir
    "prior_default": 0.5,
    "stale_years": 15,              # bu yaştan eski kaynaklara hafif ceza
    "dominance_threshold": 0.6,     # tek kanıt toplam etkinin bu payını aşarsa bayrak
    "min_independent_clusters": 2,
    "min_total_weight": 1.0,
    "decision_thresholds": [0.90, 0.70, 0.30, 0.10],  # kabul, koşullu, belirsiz, b.o. yanlış alt sınırları
    "causal_gap_log10_cap": math.log10(3),  # gözlemsel kanıtın nedensel iddiaya verebileceği en fazla destek
    "hypothesis_gap_threshold": 0.25,       # rakip hipotez setinde |ΣP − 1| bu değeri aşarsa bayrak
}

DESIGN_BASE = {
    "meta_analysis": 0.95, "systematic_review": 0.90, "rct": 0.90,
    "quasi_experimental": 0.75, "cohort": 0.70, "longitudinal": 0.70,
    "official_statistics": 0.70, "case_control": 0.60, "textbook": 0.60,
    "cross_sectional": 0.50, "qualitative": 0.40, "case_study": 0.35,
    "expert_opinion": 0.30, "news": 0.20, "blog": 0.15, "anecdote": 0.10,
    "unknown": 0.25,
}
EMPIRICAL = {"meta_analysis", "systematic_review", "rct", "quasi_experimental", "cohort",
             "longitudinal", "case_control", "cross_sectional", "official_statistics"}
CAUSAL_CAPABLE = {"rct", "quasi_experimental"}
# Dış geçerlilik: kaynağın popülasyonu/bağlamı iddianınkine ne kadar uyuyor
APPLICABILITY = {"direct": 1.0, "partial": 0.8, "indirect": 0.5}
STRENGTH_LOG10_LR = {"strong": 1.0, "moderate": math.log10(4), "weak": math.log10(2)}

SPECTRUM_BANDS = [  # (alt sınır, tr, en)
    (0.6, "Güçlü destek", "Strong support"),
    (0.3, "Orta destek", "Moderate support"),
    (0.1, "Zayıf destek", "Weak support"),
    (-0.1, "Belirsiz / nötr", "Inconclusive / neutral"),
    (-0.3, "Zayıf çelişki", "Weak contradiction"),
    (-0.6, "Orta çelişki", "Moderate contradiction"),
    (-1.01, "Güçlü çelişki", "Strong contradiction"),
]
DECISION_BANDS = [  # (alt sınır P, kod, tr, en)
    (0.90, "accept", "Kabul — uygulanabilir", "Accept — actionable"),
    (0.70, "conditional", "Koşullu kabul", "Conditional accept"),
    (0.30, "uncertain", "Belirsiz — ek kanıt gerekli", "Uncertain — more evidence needed"),
    (0.10, "likely_false", "Büyük olasılıkla yanlış", "Likely false"),
    (0.0, "reject", "Ret", "Reject"),
]
QUALITY_BANDS = [(0.75, "Yüksek", "High"), (0.5, "Orta", "Moderate"),
                 (0.3, "Düşük", "Low"), (0.0, "Çok düşük", "Very low")]

FLAG_TEXT = {
    "insufficient_evidence": ("Kanıt yetersiz: toplam ağırlık veya bağımsız küme sayısı eşiğin altında.",
                              "Insufficient evidence: total weight or independent clusters below threshold."),
    "single_source_dominance": ("Tek bir kanıt toplam etkinin çoğunu taşıyor; sonuç ona bağımlı.",
                                "One evidence item carries most of the total effect."),
    "conflicting_evidence": ("Kanıtlar kendi aralarında çelişkili (uyum C < 0.5).",
                             "Evidence items disagree with each other (consensus C < 0.5)."),
    "method_disagreement": ("Ağırlıklı skor (S) ile Bayes olasılığı (P) farklı yönü gösteriyor.",
                            "Weighted score (S) and Bayesian probability (P) point in different directions."),
    "fragile_decision": ("Karar duyarlılık senaryolarının %70'inden azında aynı kalıyor.",
                         "Decision holds in fewer than 70% of sensitivity scenarios."),
    "unverified_sources": ("Varlığı veya içeriği doğrulanmamış kaynak(lar) var (Q cezalandırıldı).",
                           "Some sources are unverified (quality penalised)."),
    "excluded_evidence": ("Bazı kanıtlar Q=0 ile dışlandı (geri çekilmiş, bulunamayan veya yanlış aktarılmış).",
                          "Some evidence excluded with Q=0 (retracted, not found or misquoted)."),
    "causal_gap": ("Nedensel iddia, nedensellik kuramayan tasarımlarla destekleniyor.",
                   "Causal claim supported mainly by non-causal designs."),
    "stance_stats_mismatch": ("Kodlanan tutum (stance) ile raporlanan istatistiğin yönü uyuşmuyor.",
                              "Coded stance disagrees with the sign of reported statistics."),
    "relation_mismatch": ("Veri kanıtı iddiadan farklı bir ilişki türüyle test edilmiş.",
                          "Data evidence was tested with a different relation than the claim."),
    "no_counter_search": ("Karşı kanıt araması kaydedilmemiş (doğrulama yanlılığı riski).",
                          "No disconfirming search recorded (confirmation-bias risk)."),
    "prior_after_evidence": ("Önsel olasılık kanıtlar görüldükten sonra belirlenmiş.",
                             "Prior was set after seeing the evidence."),
    "causal_cap_applied": ("Gözlemsel kanıtın nedensel iddiaya desteği tavanla sınırlandı (korelasyon ≠ nedensellik).",
                           "Support from observational evidence for a causal claim was capped."),
    "hypothesis_set_incoherent": ("Bu iddianın ait olduğu rakip hipotez setinde olasılıklar toplamı 1'den belirgin sapıyor.",
                                  "Probabilities in this claim's rival-hypothesis set deviate clearly from summing to 1."),
}


# Kaynağın BULGUSU (finding) ile iddianın ilişki türü arasındaki ima ilişkisi:
# +1 bulgu iddiayı destekler, -1 çürütür, 0 yönsüz (karışık).
IMPLIES = {
    "positive": {"positive": 1, "nonzero": 1, "negative": -1, "none": -1},
    "negative": {"negative": 1, "nonzero": 1, "positive": -1, "none": -1},
    "none":     {"none": 1, "positive": -1, "negative": -1, "nonzero": -1},
    "nonzero":  {"nonzero": 1, "none": -1, "positive": 0, "negative": 0},
}
STANCE_OF = {1: "supports", -1: "contradicts", 0: "mixed"}


def same_pair(a, b):
    return bool(a.get("x") and a.get("y") and b.get("x") and b.get("y")) and {a["x"], a["y"]} == {b["x"], b["y"]}


def evidence_controls(e):
    """Kanıtın kontrol (düzeltme) kümesi. None = belirtilmemiş (literatür kaynaklarında olağan)."""
    if "controls" in e:
        return sorted(e["controls"] or [])
    if e.get("kind") == "data":
        return sorted((e.get("stats") or {}).get("controls") or [])
    return None


def claim_controls(c):
    return None if c.get("controls") is None else sorted(c["controls"])


def scope_key(c):
    """Aynı soruyu soran iddiaları gruplayan anahtar: değişken çifti, nedensellik, kontroller, popülasyon."""
    cc = claim_controls(c)
    return (tuple(sorted({c["x"], c["y"]})), bool(c.get("causal")),
            None if cc is None else tuple(cc), c.get("population") or "")


def scope_label(key):
    _, causal, ctrl, pop = key
    parts = ["nedensel" if causal else "ilişkisel"]
    if ctrl is not None:
        parts.append("ham" if not ctrl else "kontroller: " + ", ".join(ctrl))
    if pop:
        parts.append(pop)
    return " · ".join(parts)


def evidence_for(claim, evidence):
    """Bir iddiaya uygulanan kanıtlar ve kapsam dışı bırakılanlar.

    Doğrudan bağlı kanıtlar (claim_id) her zaman uygulanır. Değişken çifti kapsamlı kanıtlarda
    kontrol kümesi iddianın kapsamına uymalıdır:
      - iddia `controls` belirtiyorsa → yalnızca aynı kontrol kümesiyle yapılmış analizler;
      - ilişkisel iddia (controls yok) → her bağımlılık kümesinde EN AZ kontrollü analiz (ham ilişki);
      - nedensel iddia (controls yok) → her kümede EN ÇOK kontrollü analiz (karıştırıcıya en az açık).
    Kontrol kümesi belirtilmemiş kaynaklar her iddiaya uygulanır.
    """
    direct, pair = [], []
    for e in evidence:
        ids = e.get("claim_ids") or ([e["claim_id"]] if e.get("claim_id") else [])
        if claim["id"] in ids:
            direct.append((e, "claim_id"))
        elif not ids and same_pair(e, claim):
            pair.append(e)
    kept, dropped = [], []
    want = claim_controls(claim)
    if want is not None:
        for e in pair:
            ec = evidence_controls(e)
            if ec is None or ec == want:
                kept.append(e)
            else:
                dropped.append((e, f"kontroller {ec or 'yok (ham)'} ≠ iddianın {want or 'yok (ham)'}"))
    else:
        by_cluster = {}
        for e in pair:
            ec = evidence_controls(e)
            if ec is None:
                kept.append(e)
            else:
                by_cluster.setdefault(e.get("cluster") or e["id"], []).append((len(ec), e))
        for items in by_cluster.values():
            pick = max if claim.get("causal") else min
            target = pick(n for n, _ in items)
            for n, e in items:
                if n == target:
                    kept.append(e)
                else:
                    why = ("nedensel iddia: aynı veri kümesinde daha kontrollü analiz var" if claim.get("causal")
                           else "ilişkisel iddia: aynı veri kümesinde ham analiz var")
                    dropped.append((e, why))
    applied = direct + [(e, "variable_pair") for e in kept]
    return applied, [{"id": e["id"], "reason": why} for e, why in dropped]


def band(value, bands, lang, idx_tr=1):
    for b in bands:
        if value >= b[0]:
            return b[idx_tr] if lang == "tr" else b[idx_tr + 1]
    b = bands[-1]
    return b[idx_tr] if lang == "tr" else b[idx_tr + 1]


def decision(p):
    for lo, code, tr, en in DECISION_BANDS:
        if p >= lo:
            return code, tr, en
    return DECISION_BANDS[-1][1:]


def r3(x):
    return None if x is None else round(x, 3)


# ----------------------------------------------------------- kanıt puanlama

def n_modifier(n):
    if n is None:
        return None
    if n < 30:
        return 0.70
    if n < 100:
        return 0.85
    if n >= 1000:
        return 1.05
    return 1.0


def quality_source(ev, claim, cfg, year_now):
    design = ev.get("design", "unknown")
    if design not in DESIGN_BASE:
        design = "unknown"
    q = DESIGN_BASE[design]
    trace = [f"tasarım={design} → {q}"]

    def mul(f, why):
        nonlocal q
        q *= f
        trace.append(f"×{f} ({why})")

    ver = ev.get("verification", {}) or {}
    if ev.get("retracted"):
        return 0.0, trace + ["geri çekilmiş → Q=0"], "excluded"
    if ver.get("exists") is False:
        return 0.0, trace + ["kaynak bulunamadı → Q=0"], "excluded"
    if ver.get("claim_matches_source") is False:
        return 0.0, trace + ["kaynak aktarılan şeyi söylemiyor → Q=0"], "excluded"

    status = None
    if ver.get("exists") is None:
        mul(0.5, "varlığı doğrulanmadı")
        status = "unverified"
    if ver.get("claim_matches_source") is None:
        mul(0.7, "içerik doğrulanmadı")
        status = "unverified"

    nm = n_modifier(ev.get("n"))
    if nm is not None and nm != 1.0:
        mul(nm, f"n={ev.get('n')}")
    elif nm is None and design in EMPIRICAL:
        mul(0.9, "n bilinmiyor")

    pr = ev.get("peer_reviewed")
    if pr is False:
        mul(0.8, "hakemsiz")
    elif pr is None and design in EMPIRICAL:
        mul(0.9, "hakem durumu bilinmiyor")
    if ev.get("conflict_of_interest"):
        mul(0.8, "çıkar çatışması")
    if ev.get("preregistered"):
        mul(1.05, "ön kayıtlı")
    if ev.get("replicated"):
        mul(1.1, "bağımsız replikasyon")
    yr = ev.get("year")
    if isinstance(yr, int) and year_now - yr > cfg["stale_years"]:
        mul(0.9, f"{year_now - yr} yıllık")

    app = ev.get("applicability")
    if app in APPLICABILITY and APPLICABILITY[app] != 1.0:
        mul(APPLICABILITY[app], f"uygulanabilirlik: {app} — {ev.get('applicability_note', 'farklı popülasyon/bağlam')}")

    causal_design = ev.get("causal_design", design in CAUSAL_CAPABLE)
    if claim.get("causal") and not causal_design:
        mul(0.6, "nedensel iddia / nedensel olmayan tasarım")
        status = status or "causal_gap"
    return min(max(q, 0.0), 1.0), trace, status


def quality_data(ev, claim):
    q = 0.9 if ev.get("experimental") else 0.8
    trace = [f"veri analizi ({'deneysel' if ev.get('experimental') else 'gözlemsel'}) → {q}"]
    mf = ev.get("missing_frac", 0) or 0
    if mf > 0:
        f = round(1 - 0.5 * mf, 3)
        q *= f
        trace.append(f"×{f} (eksik veri oranı {mf:.0%})")
    nm = n_modifier(ev.get("n"))
    if nm and nm != 1.0:
        q *= nm
        trace.append(f"×{nm} (n={ev.get('n')})")
    if ev.get("quality_multiplier"):
        q *= ev["quality_multiplier"]
        trace.append(f"×{ev['quality_multiplier']} (kullanıcı notu: {ev.get('data_quality_notes', '')})")
    status = None
    if claim.get("causal") and not ev.get("experimental"):
        q *= 0.6
        trace.append("×0.6 (nedensel iddia / gözlemsel veri)")
        status = "causal_gap"
    return min(max(q, 0.0), 1.0), trace, status


def log_lr_from_reported(rep, claim):
    """Kaynakta raporlanan istatistikten doğal-log LR. None → kullanılamaz."""
    n = rep.get("n")
    if "r" in rep and n:
        r, nn = rep["r"], n
    elif "t" in rep and "df" in rep:
        r = math.copysign(math.sqrt(S.t_to_r2(rep["t"], rep["df"])), rep["t"])
        nn = n or rep["df"] + 2
    elif "d" in rep and rep.get("n1") and rep.get("n2"):
        r = S.d_to_r(rep["d"], rep["n1"], rep["n2"])
        nn = rep["n1"] + rep["n2"]
    else:
        return None, None
    lbf = S.log_bf10_from_r2(r * r, nn)
    sign = 0 if r == 0 else (1 if r > 0 else -1)
    p_two = S.t_two_sided_p(S.r_to_t(r, nn - 2), nn - 2) if nn > 2 else None
    return S.directional_log_lr(lbf, sign, claim["relation"], p_two), sign


def score_evidence(ev, claim, cfg, year_now, flags):
    kind = ev.get("kind", "source")
    cap = cfg["log10_lr_cap"]
    stance = None
    if kind == "data":
        q, trace, status = quality_data(ev, claim)
        st = ev.get("stats", {})
        # yalnızca doğrudan bağlı kanıtta anlamlı; çift kapsamlı kanıt rakip iddialara da uygulanır
        if (ev.get("_applied_via") == "claim_id" and ev.get("relation_tested")
                and ev["relation_tested"] != claim["relation"]):
            flags.add("relation_mismatch")
        lbf = st.get("log10_bf10", 0.0) * LN10
        log_lr_raw = S.directional_log_lr(lbf, st.get("effect_sign", 0), claim["relation"], st.get("p_two_sided"))
        basis = f"BIC-BF10={st.get('bf10', float('nan')):.3g}, r={st.get('r_equivalent')}, n={ev.get('n')}"
    else:
        q, trace, status = quality_source(ev, claim, cfg, year_now)
        if ev.get("finding") in IMPLIES:
            stance = STANCE_OF[IMPLIES[ev["finding"]][claim["relation"]]]
        else:
            stance = ev.get("stance", "mixed")
        strength = ev.get("strength", "moderate")
        rep = ev.get("reported_stats")
        lr_rep, sign = (log_lr_from_reported(rep, claim) if rep else (None, None))
        if lr_rep is not None:
            log_lr_raw = lr_rep
            basis = f"raporlanan istatistik {rep}"
            implied = "supports" if lr_rep > 0 else "contradicts"
            if stance in ("supports", "contradicts") and stance != implied and abs(lr_rep) > math.log(3):
                flags.add("stance_stats_mismatch")
            stance = implied if abs(lr_rep) > math.log(1.5) else "mixed"
        elif stance in ("supports", "contradicts"):
            mag = STRENGTH_LOG10_LR.get(strength, STRENGTH_LOG10_LR["moderate"]) * LN10
            log_lr_raw = mag if stance == "supports" else -mag
            basis = f"tutum={stance}, güç={strength}"
        else:
            log_lr_raw = 0.0
            basis = f"tutum={stance} (yönsüz)"

    if status == "excluded":
        flags.add("excluded_evidence")
    elif status == "unverified":
        flags.add("unverified_sources")

    l10_raw = max(min(log_lr_raw / LN10, cap), -cap)
    if kind == "data":
        noncausal = not ev.get("experimental")
    else:
        noncausal = not ev.get("causal_design", ev.get("design", "unknown") in CAUSAL_CAPABLE)
    ccap = cfg["causal_gap_log10_cap"]
    if claim.get("causal") and noncausal and l10_raw > ccap and q > 0:
        trace = trace + [f"LR_ham {10 ** l10_raw:.3g} → {10 ** ccap:.3g} tavanı (gözlemsel kanıt nedenselliği tek başına kanıtlayamaz)"]
        l10_raw = ccap
        flags.add("causal_cap_applied")
    l10_eff = l10_raw * q                      # LR_eff = LR_raw ^ Q
    d = max(min(l10_raw, 1.0), -1.0)           # yön + güç, [-1, +1]
    return {
        "id": ev["id"], "kind": kind, "cluster": ev.get("cluster") or ev["id"],
        "label": ev.get("citation") or ev.get("description") or ev["id"],
        "applied_via": ev.get("_applied_via", "claim_id"),
        "stance_used": stance,
        "quality_Q": r3(q), "quality_trace": trace, "status": status or "ok",
        "lr_basis": basis,
        "log10_lr_raw": r3(l10_raw), "lr_raw": r3(10 ** l10_raw),
        "log10_lr_effective": r3(l10_eff), "lr_effective": r3(10 ** l10_eff),
        "direction_d": r3(d),
        "_q": q, "_l10": l10_eff, "_d": d, "_l10raw": l10_raw,
    }


# ------------------------------------------------------------ iddia puanlama

def combine(scored, prior, rho, q_scale=1.0):
    """Kümelenmiş Bayes birleşimi; doğal-log sonsal odds ve P döner."""
    clusters = {}
    for e in scored:
        if e["_q"] <= 0:
            continue
        q = min(e["_q"] * q_scale, 1.0)
        clusters.setdefault(e["cluster"], []).append(e["_l10raw"] * q)
    total_l10 = 0.0
    contrib = {}
    for c, vals in clusters.items():
        k = len(vals)
        k_eff = k / (1 + (k - 1) * rho)
        cl = sum(vals) / k * k_eff
        contrib[c] = {"k": k, "k_effective": k_eff, "log10_lr": cl}
        total_l10 += cl
    post = S.logit(prior) + total_l10 * LN10
    return S.sigmoid(post), total_l10, contrib


def score_claim(claim, evs, cfg, lang, year_now, scoped_out=()):
    flags = set()
    prior = claim.get("prior", cfg["prior_default"])
    rho = cfg["rho_within_cluster"]
    scored = [score_evidence(dict(e, _applied_via=via), claim, cfg, year_now, flags) for e, via in evs]
    active = [e for e in scored if e["_q"] > 0]

    # Ağırlıklı kanıt skoru (spektrum) ve uyum
    W = sum(e["_q"] for e in active)
    if W > 0:
        S_score = sum(e["_q"] * e["_d"] for e in active) / W
        var = sum(e["_q"] * (e["_d"] - S_score) ** 2 for e in active) / W
        consensus = 1 - math.sqrt(var) if len(active) > 1 else None  # tek kanıtta uyum tanımsız
        mean_q = W / len(active)
    else:
        S_score, consensus, mean_q = 0.0, None, 0.0

    # Bayes
    P, total_l10, contrib = combine(scored, prior, rho)

    # bayraklar
    n_clusters = len(contrib)
    if W < cfg["min_total_weight"] or n_clusters < cfg["min_independent_clusters"]:
        flags.add("insufficient_evidence")
    abs_sum = sum(abs(e["_l10"]) for e in active)
    if len(active) > 1 and abs_sum > 0:
        top = max(active, key=lambda e: abs(e["_l10"]))
        if abs(top["_l10"]) / abs_sum > cfg["dominance_threshold"]:
            flags.add("single_source_dominance")
            dominant = top["id"]
        else:
            dominant = None
    else:
        dominant = None
    if consensus is not None and consensus < 0.5 and len(active) > 1:
        flags.add("conflicting_evidence")
    if abs(S_score) > 0.1 and abs(2 * P - 1) > 0.2 and (S_score > 0) != (P > 0.5):
        flags.add("method_disagreement")
    if claim.get("causal"):
        gap = [e for e in active if any("nedensel" in t for t in e["quality_trace"])]
        if active and len(gap) == len(active):
            flags.add("causal_gap")
    ces = claim.get("counter_evidence_searched", False)
    if ces is not True and ces != "not_applicable":
        flags.add("no_counter_search")
    if claim.get("prior_set_before_evidence") is False:
        flags.add("prior_after_evidence")

    # Duyarlılık analizi: 3 önsel × 3 rho × 3 kalite ölçeği = 27 senaryo
    base_dec = decision(P)[0]
    priors = sorted({0.25, prior, 0.75})
    rhos = sorted({0.0, rho, 0.8})
    scen = []
    for pr in priors:
        for rh in rhos:
            for qs in (0.8, 1.0, 1.2):
                p_s, _, _ = combine(scored, pr, rh, qs)
                scen.append(p_s)
    robust = sum(1 for p_s in scen if decision(p_s)[0] == base_dec) / len(scen)
    if robust < 0.7:
        flags.add("fragile_decision")

    # Bilginin değeri: bir üst / alt karar bandına geçmek için gereken LR
    bounds = sorted(b[0] for b in DECISION_BANDS if b[0] > 0)
    up = next((b for b in bounds if b > P + 1e-9), None)
    down = next((b for b in reversed(bounds) if b < P - 1e-9), None)
    lp = S.logit(P)
    voi = {
        "lr_needed_to_move_up": r3(math.exp(S.logit(up) - lp)) if up else None,
        "next_band_up_at_P": up,
        "lr_needed_to_move_down": r3(math.exp(S.logit(down) - lp)) if down else None,
        "next_band_down_at_P": down,
    }

    code, dec_tr, dec_en = decision(P)
    out_ev = [{k: v for k, v in e.items() if not k.startswith("_")} for e in scored]
    for e in out_ev:
        e["share_of_total_effect"] = r3(abs(next(s["_l10"] for s in scored if s["id"] == e["id"])) / abs_sum) if abs_sum else 0
    return {
        "id": claim["id"],
        "text": claim.get("text", ""),
        "structure": {k: claim.get(k) for k in
                      ("x", "y", "relation", "causal", "controls", "population", "timeframe", "conditions")},
        "prior": prior,
        "prior_rationale": claim.get("prior_rationale", ""),
        "scores": {
            "spectrum_S": r3(S_score),
            "spectrum_label": band(S_score, SPECTRUM_BANDS, lang),
            "posterior_P": r3(P),
            "posterior_odds": r3(P / (1 - P)) if P < 1 else None,
            "log10_bayes_factor_total": r3(total_l10),
            "bayes_factor_total": r3(10 ** total_l10),
            "decision_code": code,
            "decision": dec_tr if lang == "tr" else dec_en,
            "consensus_C": r3(consensus),
            "mean_quality_Q": r3(mean_q),
            "evidence_quality_grade": band(mean_q, QUALITY_BANDS, lang),
            "total_weight_W": r3(W),
            "n_evidence": len(scored), "n_active_evidence": len(active),
            "n_independent_clusters": n_clusters,
            "n_supporting": sum(1 for e in active if e["_d"] > 0.05),
            "n_contradicting": sum(1 for e in active if e["_d"] < -0.05),
            "n_neutral": sum(1 for e in active if abs(e["_d"]) <= 0.05),
            "spectrum_vs_probability_gap": r3(S_score - (2 * P - 1)),
        },
        "sensitivity": {
            "scenarios": len(scen), "P_min": r3(min(scen)), "P_max": r3(max(scen)),
            "decision_robustness": r3(robust),
            "grid": {"priors": priors, "rho": rhos, "quality_scale": [0.8, 1.0, 1.2]},
        },
        "value_of_information": voi,
        "dominant_evidence": dominant,
        "clusters": {c: {"k": v["k"], "k_effective": r3(v["k_effective"]), "log10_lr": r3(v["log10_lr"])}
                     for c, v in contrib.items()},
        "flags": [{"code": f, "message": FLAG_TEXT[f][0 if lang == "tr" else 1]} for f in sorted(flags)],
        "evidence": out_ev,
        "evidence_scoped_out": list(scoped_out),
    }


# ----------------------------------------------------- iddialar arası uyum

COMPAT = {  # aynı X–Y çifti için mantıksal uyum: +1 uyumlu, -1 çelişik, 0 bağımsız/kısmi
    ("positive", "positive"): 1, ("negative", "negative"): 1, ("none", "none"): 1,
    ("nonzero", "nonzero"): 1, ("positive", "negative"): -1, ("positive", "none"): -1,
    ("negative", "none"): -1, ("nonzero", "none"): -1, ("positive", "nonzero"): 1,
    ("negative", "nonzero"): 1,
}


def claim_relations(claims, scored):
    by_id = {c["id"]: c for c in claims}
    out = []
    ids = [c["id"] for c in claims]
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = by_id[ids[i]], by_id[ids[j]]
            if not same_pair(a, b):
                continue
            ra, rb = a["relation"], b["relation"]
            pa, pb = scored[a["id"]]["scores"]["posterior_P"], scored[b["id"]]["scores"]["posterior_P"]
            ka, kb = scope_key(a), scope_key(b)
            same_scope = ka == kb
            comp = COMPAT.get((ra, rb), COMPAT.get((rb, ra), 0)) if same_scope else 0
            rec = {"claims": [a["id"], b["id"]], "relations": [ra, rb], "same_scope": same_scope,
                   "logical_compatibility": comp, "P": [pa, pb]}
            if not same_scope:
                rec["note"] = (f"Farklı kapsam ({scope_label(ka)} / {scope_label(kb)}): "
                               "ikisi aynı anda doğru olabilir, mantıksal çelişki sayılmaz.")
            if comp == -1:
                rec["incoherence"] = r3(max(0.0, pa + pb - 1))  # >0 ise olasılıklar tutarsız
            out.append(rec)
    return out


def hypothesis_sets(claims, scored, cfg):
    """Aynı kapsamda birbirini dışlayan iddiaları (artırır / azaltır / yok) bir arada değerlendirir.

    positive, negative ve none aynı kapsamda hem birbirini dışlar hem de tüm olasılıkları kapsar;
    bu yüzden P'lerinin toplamı ≈ 1 olmalıdır (nonzero + none için de aynısı). Her iddia ayrı
    önselle puanlandığı için toplam 1'den sapabilir; sapma, kanıtların hipotezleri ne kadar
    ayırt edebildiğini gösterir. Normalize P tutarlı bir dağılım verir.
    """
    groups = {}
    for c in claims:
        if c.get("x") and c.get("y"):
            groups.setdefault(scope_key(c), []).append(c)
    out = []
    for key, cs in groups.items():
        rels = {}
        for c in cs:
            rels.setdefault(c["relation"], []).append(c["id"])
        if {"positive", "negative", "none"} <= rels.keys():
            members, exhaustive = ["positive", "negative", "none"], True
        elif {"nonzero", "none"} <= rels.keys():
            members, exhaustive = ["nonzero", "none"], True
        else:
            members = [r for r in ("positive", "negative", "none") if r in rels]
            exhaustive = False
            if len(members) < 2:
                continue
        ids = [rels[r][0] for r in members]
        Ps = [scored[i]["scores"]["posterior_P"] for i in ids]
        tot = sum(Ps)
        gap = abs(tot - 1) if exhaustive else max(0.0, tot - 1)
        rec = {
            "variables": list(key[0]), "scope": scope_label(key), "claims": ids, "relations": members,
            "P": Ps, "sum_P": r3(tot), "exhaustive": exhaustive,
            "normalized_P": [r3(p / tot) for p in Ps] if tot > 0 else None,
            "most_probable": ids[Ps.index(max(Ps))], "coherence_gap": r3(gap),
            "incoherent": gap > cfg["hypothesis_gap_threshold"],
        }
        if exhaustive and tot < 1 - cfg["hypothesis_gap_threshold"]:
            rec["interpretation"] = "ΣP < 1: kanıtlar rakip hipotezleri iyi ayırt edemiyor; normalize paylara bakın."
        elif tot > 1 + cfg["hypothesis_gap_threshold"]:
            rec["interpretation"] = "ΣP > 1: birbirini dışlayan iddialar aynı anda yüksek olasılık almış; kodlamayı/önselleri kontrol edin."
        out.append(rec)
    return out


def variable_summary(claims, scored):
    vs = {}
    for c in claims:
        for v in (c.get("x"), c.get("y")):
            if not v:
                continue
            d = vs.setdefault(v, {"claims": [], "S": [], "P": []})
            d["claims"].append(c["id"])
            d["S"].append(scored[c["id"]]["scores"]["spectrum_S"])
            d["P"].append(scored[c["id"]]["scores"]["posterior_P"])
    return {v: {"claims": d["claims"], "mean_S": r3(sum(d["S"]) / len(d["S"])),
                "mean_P": r3(sum(d["P"]) / len(d["P"]))} for v, d in vs.items()}


# --------------------------------------------------------------- rapor

def spectrum_bar(s, width=20):
    pos = round((s + 1) / 2 * width)
    cells = ["─"] * (width + 1)
    cells[width // 2] = "┼"
    cells[pos] = "●"
    return "−1 " + "".join(cells) + " +1"


def cell(v):
    return str(v).replace("|", "\\|").replace("\n", " ")


def fmt(v):
    return "—" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))


def render_report(meta, lang):
    p = meta["project"]
    L = []
    L.append(f"# İddia Doğrulama Raporu — {p.get('title', '')}")
    L.append("")
    if p.get("question"):
        L.append(f"**Araştırma sorusu:** {p['question']}  ")
    L.append(f"**Tarih:** {meta['generated_at'][:10]} · **Şema:** v{meta['schema_version']} · "
             f"**İddia sayısı:** {len(meta['claims'])} · **Kanıt sayısı:** {meta['totals']['n_evidence']}")
    L.append("")
    L.append("> **Nasıl okunur:** *S* (−1…+1) kalite-ağırlıklı kanıtların iddiayı ne yönde ve ne güçte "
             "desteklediğini gösterir. *P* önsel olasılığın kanıtların olabilirlik oranlarıyla Bayesçi "
             "güncellenmesiyle elde edilen sonsal olasılıktır. *C* (0…1) kanıtların kendi aralarındaki uyumudur. "
             "*Sağlamlık*, 27 duyarlılık senaryosunun kaçında kararın değişmediğidir.")
    L.append("")
    L.append("## 1. Özet")
    L.append("")
    L.append("| ID | İddia | S | Spektrum | P | Karar | C | Kalite | Sağlamlık | Uyarı |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for c in meta["claims"]:
        s = c["scores"]
        L.append(f"| {c['id']} | {cell(c['text'])} | {fmt(s['spectrum_S'])} | {s['spectrum_label']} | "
                 f"{fmt(s['posterior_P'])} | {s['decision']} | {fmt(s['consensus_C'])} | "
                 f"{s['evidence_quality_grade']} | {c['sensitivity']['decision_robustness']:.0%} | "
                 f"{len(c['flags'])} |")
    L.append("")
    L.append("### Spektrum görünümü")
    L.append("")
    L.append("```")
    w = max(len(c["id"]) for c in meta["claims"])
    for c in meta["claims"]:
        L.append(f"{c['id']:<{w}}  {spectrum_bar(c['scores']['spectrum_S'])}  S={c['scores']['spectrum_S']:+.2f}  "
                 f"P={c['scores']['posterior_P']:.2f}")
    L.append("```")
    L.append("")
    L.append("## 2. İddia ayrıntıları")
    for c in meta["claims"]:
        s, st = c["scores"], c["structure"]
        L.append("")
        L.append(f"### {c['id']} — {c['text']}")
        L.append("")
        L.append(f"- **Yapı:** X=`{st.get('x')}` → Y=`{st.get('y')}` · ilişki=`{st.get('relation')}` · "
                 f"nedensel={'evet' if st.get('causal') else 'hayır'}"
                 + (f" · popülasyon: {st['population']}" if st.get("population") else ""))
        L.append(f"- **Önsel P₀:** {c['prior']} — {c['prior_rationale'] or 'gerekçe belirtilmedi'}")
        L.append(f"- **Toplam Bayes faktörü:** {fmt(s['bayes_factor_total'])} (log₁₀ = {fmt(s['log10_bayes_factor_total'])}) "
                 f"→ **P = {fmt(s['posterior_P'])}** ({s['decision']})")
        L.append(f"- **Spektrum:** S = {fmt(s['spectrum_S'])} ({s['spectrum_label']}) · uyum C = {fmt(s['consensus_C'])} · "
                 f"destekleyen/çelişen/nötr = {s['n_supporting']}/{s['n_contradicting']}/{s['n_neutral']}")
        sen = c["sensitivity"]
        L.append(f"- **Duyarlılık:** P aralığı [{fmt(sen['P_min'])}, {fmt(sen['P_max'])}] · "
                 f"karar sağlamlığı {sen['decision_robustness']:.0%} ({sen['scenarios']} senaryo)")
        v = c["value_of_information"]
        parts = []
        if v["lr_needed_to_move_up"]:
            parts.append(f"üst banda (P≥{v['next_band_up_at_P']}) geçmek için LR ≈ {v['lr_needed_to_move_up']}")
        if v["lr_needed_to_move_down"]:
            parts.append(f"alt banda (P<{v['next_band_down_at_P']}) düşmek için LR ≈ {v['lr_needed_to_move_down']}")
        if parts:
            L.append(f"- **Bilginin değeri:** " + "; ".join(parts))
        L.append("")
        L.append("| Kanıt | Tür | Kaynak / açıklama | Bağ | Tutum | Küme | Q | LR (ham) | LR (etkin) | d | Pay | Durum |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
        via = {"claim_id": "doğrudan", "variable_pair": "X–Y çifti"}
        for e in c["evidence"]:
            L.append(f"| {e['id']} | {e['kind']} | {cell(e['label'])} | {via[e['applied_via']]} | "
                     f"{e['stance_used'] or 'istatistik'} | {cell(e['cluster'])} | {fmt(e['quality_Q'])} | "
                     f"{fmt(e['lr_raw'])} | {fmt(e['lr_effective'])} | {fmt(e['direction_d'])} | "
                     f"{e['share_of_total_effect']:.0%} | {e['status']} |")
        if c.get("evidence_scoped_out"):
            L.append("")
            L.append("**Kapsam dışı bırakılan kanıtlar:** " + "; ".join(
                f"{d['id']} ({d['reason']})" for d in c["evidence_scoped_out"]))
        if c["flags"]:
            L.append("")
            L.append("**Uyarılar:**")
            for f in c["flags"]:
                L.append(f"- `{f['code']}` — {f['message']}")
    rels = meta["claim_relations"]
    if rels:
        L.append("")
        L.append("## 3. İddialar arası uyum")
        L.append("")
        L.append("| İddialar | İlişkiler | Mantıksal uyum | P değerleri | Tutarsızlık | Not |")
        L.append("|---|---|---|---|---|---|")
        lab = {1: "+1 uyumlu", -1: "−1 çelişik", 0: "0 kısmi"}
        for r in rels:
            L.append(f"| {' ↔ '.join(r['claims'])} | {' / '.join(r['relations'])} | {lab[r['logical_compatibility']]} | "
                     f"{' / '.join(fmt(x) for x in r['P'])} | {fmt(r.get('incoherence'))} | {r.get('note', '')} |")
    hs = meta.get("hypothesis_sets") or []
    if hs:
        L.append("")
        L.append("### Rakip hipotez setleri")
        L.append("")
        L.append("Aynı kapsamda birbirini dışlayan iddialar. Kapsayıcı setlerde ΣP ≈ 1 olmalıdır; "
                 "*normalize P* tutarlı olasılık dağılımıdır.")
        L.append("")
        L.append("| Değişkenler | Kapsam | Hipotezler | P | ΣP | Normalize P | En olası | Açık |")
        L.append("|---|---|---|---|---|---|---|---|")
        for h in hs:
            hyp = ", ".join(f"{i}:{r}" for i, r in zip(h["claims"], h["relations"]))
            warn = " ⚠" if h["incoherent"] else ""
            L.append(f"| {' – '.join(h['variables'])} | {cell(h['scope'])} | {hyp} | "
                     f"{' / '.join(fmt(p) for p in h['P'])} | {fmt(h['sum_P'])} | "
                     f"{' / '.join(fmt(p) for p in (h['normalized_P'] or []))} | {h['most_probable']} | "
                     f"{fmt(h['coherence_gap'])}{warn} |")
        for h in hs:
            if h.get("interpretation"):
                L.append(f"- {' / '.join(h['claims'])}: {h['interpretation']}")
    if meta["variables"]:
        L.append("")
        L.append("## 4. Değişken özeti")
        L.append("")
        L.append("| Değişken | İddialar | Ort. S | Ort. P |")
        L.append("|---|---|---|---|")
        for v, d in meta["variables"].items():
            L.append(f"| `{v}` | {', '.join(d['claims'])} | {fmt(d['mean_S'])} | {fmt(d['mean_P'])} |")
    L.append("")
    L.append("## 5. Yöntem")
    L.append("")
    L.append("- Kanıt kalitesi **Q** ∈ [0,1]: tasarım taban puanı × düzelticiler (n, hakem, çıkar çatışması, "
             "replikasyon, yaş, doğrulama, nedensellik açığı). Her çarpan `metadata.json` içindeki `quality_trace`'te.")
    L.append("- Ham olabilirlik oranı: veri/raporlanan istatistik için BIC yaklaşımlı Bayes faktörü "
             "BF₁₀ = (1−r²)^(−n/2)/√n, yönlü iddiada işarete göre çevrilir; kaynak tutumu için güçlü=10, orta=4, zayıf=2. "
             f"Tek kanıt |log₁₀ LR| ≤ {meta['settings']['log10_lr_cap']} ile sınırlanır.")
    L.append("- Etkin LR = LR_ham^Q. Aynı kümedeki k kanıt ortalanıp k_eff = k/(1+(k−1)ρ) ile ölçeklenir "
             f"(ρ = {meta['settings']['rho_within_cluster']}).")
    L.append("- P = σ(logit P₀ + Σ ln LR_küme). S = Σ Q·d / Σ Q, d = kırpılmış log₁₀ LR_ham ∈ [−1,1]. "
             "C = 1 − ağırlıklı standart sapma(d).")
    t = meta["settings"]["decision_thresholds"]
    L.append("- Kapsam: değişken çifti kanıtı iddianın kapsamına göre seçilir — `controls` belirten iddia yalnızca aynı "
             "kontrollerle yapılmış analizi; ilişkisel iddia aynı veri kümesindeki ham analizi; nedensel iddia en kontrollü analizi kullanır. "
             f"Gözlemsel kanıtın nedensel iddiaya desteği LR ≤ {10 ** meta['settings']['causal_gap_log10_cap']:.2g} ile sınırlanır.")
    L.append(f"- Karar bantları: P≥{t[0]} kabul · {t[1]}–{t[0]} koşullu · {t[2]}–{t[1]} belirsiz · "
             f"{t[3]}–{t[2]} büyük olasılıkla yanlış · <{t[3]} ret.")
    L.append("")
    L.append("## 6. Yorum ve Uygulama")
    L.append("")
    L.append("<!-- YORUM_UYGULAMA: Bu bölüm SKILL.md Adım 7'ye göre doldurulur. -->")
    L.append("")
    return "\n".join(L)


# ----------------------------------------------------------------- ana

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--lang", default="tr", choices=["tr", "en"])
    a = ap.parse_args()

    with open(a.input, encoding="utf-8") as f:
        doc = json.load(f)
    cfg = dict(DEFAULTS)
    cfg.update(doc.get("settings", {}))
    t = cfg["decision_thresholds"]
    if not (len(t) == 4 and 1 > t[0] > t[1] > t[2] > t[3] > 0):
        sys.exit("HATA: decision_thresholds azalan 4 değer olmalı, örn. [0.95, 0.8, 0.3, 0.1]")
    global DECISION_BANDS
    DECISION_BANDS = [(lo,) + b[1:] for lo, b in zip(list(t) + [0.0], DECISION_BANDS)]
    claims = doc.get("claims", [])
    evidence = doc.get("evidence", [])
    if not claims:
        sys.exit("HATA: 'claims' listesi boş.")
    ids = {c["id"] for c in claims}
    errs = []
    for c in claims:
        if c.get("relation") not in ("positive", "negative", "nonzero", "none"):
            errs.append(f"{c['id']}: relation positive|negative|nonzero|none olmalı")
        p = c.get("prior", cfg["prior_default"])
        if not (0 < p < 1):
            errs.append(f"{c['id']}: prior (0,1) aralığında olmalı")
    for e in evidence:
        cids = e.get("claim_ids") or ([e["claim_id"]] if e.get("claim_id") else [])
        for cid in cids:
            if cid not in ids:
                errs.append(f"{e.get('id')}: claim_id '{cid}' bilinmiyor")
        if not cids:
            if not (e.get("x") and e.get("y")):
                errs.append(f"{e.get('id')}: claim_id yok; değişken çifti kapsamı için x ve y gerekli")
            elif not any(same_pair(e, c) for c in claims):
                errs.append(f"{e.get('id')}: {e['x']}–{e['y']} çiftini içeren iddia yok")
            if e.get("kind", "source") == "source" and not (e.get("finding") or e.get("reported_stats")):
                errs.append(f"{e.get('id')}: çift kapsamlı kaynak kanıtı 'finding' veya 'reported_stats' içermeli "
                            "(stance iddiaya göredir, iddialar arasında aktarılamaz)")
    if errs:
        sys.exit("GİRDİ HATALARI:\n  " + "\n  ".join(errs))

    year_now = dt.date.today().year
    scored = {}
    for c in claims:
        evs, scoped_out = evidence_for(c, evidence)
        scored[c["id"]] = score_claim(c, evs, cfg, a.lang, year_now, scoped_out)

    hsets = hypothesis_sets(claims, scored, cfg)
    for h in hsets:
        if h["incoherent"]:
            for cid in h["claims"]:
                fl = scored[cid]["flags"]
                if not any(f["code"] == "hypothesis_set_incoherent" for f in fl):
                    fl.append({"code": "hypothesis_set_incoherent",
                               "message": FLAG_TEXT["hypothesis_set_incoherent"][0 if a.lang == "tr" else 1]})

    meta = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "project": doc.get("project", {}),
        "settings": cfg,
        "totals": {
            "n_claims": len(claims), "n_evidence": len(evidence),
            "decisions": {code: sum(1 for c in scored.values() if c["scores"]["decision_code"] == code)
                          for _, code, _, _ in DECISION_BANDS},
        },
        "claims": [scored[c["id"]] for c in claims],
        "claim_relations": claim_relations(claims, scored),
        "hypothesis_sets": hsets,
        "variables": variable_summary(claims, scored),
    }
    os.makedirs(a.out_dir, exist_ok=True)
    mp = os.path.join(a.out_dir, "metadata.json")
    rp = os.path.join(a.out_dir, "rapor.md" if a.lang == "tr" else "report.md")
    with open(mp, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    with open(rp, "w", encoding="utf-8") as f:
        f.write(render_report(meta, a.lang))

    for c in meta["claims"]:
        s = c["scores"]
        print(f"{c['id']:<5} S={s['spectrum_S']:+.2f} [{s['spectrum_label']}]  P={s['posterior_P']:.3f} "
              f"[{s['decision']}]  C={fmt(s['consensus_C'])}  sağlamlık={c['sensitivity']['decision_robustness']:.0%}  "
              f"uyarı={[f['code'] for f in c['flags']]}")
    print(f"\nYazıldı: {mp}\nYazıldı: {rp}")


if __name__ == "__main__":
    main()
