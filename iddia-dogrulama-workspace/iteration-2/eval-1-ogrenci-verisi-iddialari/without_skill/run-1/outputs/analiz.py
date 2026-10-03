"""Danisman iddialarinin ogrenci verisiyle dogrulanmasi.

Calistirma: python3 analiz.py  (pandas, numpy, scipy, statsmodels gerekir)
Cikti: analiz_sonuclari.json (ayni klasore)
"""
import json
import math
import os

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import integrate, stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/home/user/calisma-alanim/iddia-dogrulama-workspace/inputs/ogrenci_verisi.csv"
RNG = np.random.default_rng(20261003)
N_BOOT = 10000

# ---------------------------------------------------------------- veri
df = pd.read_csv(DATA, sep=";", decimal=",", na_values=["NA", ""], keep_default_na=True)
df = df.rename(columns={
    "haftalik_calisma_saati": "calisma",
    "gunluk_sosyal_medya_saat": "sosyal",
    "uyku_saat": "uyku",
    "not_ortalamasi": "gpa",
})
df["kiz"] = (df["cinsiyet"] == "K").astype(int)
df["ozel"] = (df["okul_turu"] == "ozel").astype(int)

veri_kalitesi = {
    "satir": int(len(df)),
    "eksik": {c: int(df[c].isna().sum()) for c in df.columns if df[c].isna().any()},
    "tam_satir": int(df.dropna().shape[0]),
    "tekrar_id": int(df["ogrenci_id"].duplicated().sum()),
    "not_100_olan": int((df["gpa"] >= 100).sum()),
    "calisma_0_olan": int((df["calisma"] == 0).sum()),
    "araliklar": {c: [float(df[c].min()), float(df[c].max())] for c in ["calisma", "sosyal", "uyku", "gpa"]},
    "cinsiyet_n": df["cinsiyet"].value_counts().to_dict(),
    "okul_n": df["okul_turu"].value_counts().to_dict(),
}


# ------------------------------------------------------------- yardimci
def fisher_ci(r, n, alpha=0.05):
    z = math.atanh(r)
    se = 1 / math.sqrt(n - 3)
    q = stats.norm.ppf(1 - alpha / 2)
    return math.tanh(z - q * se), math.tanh(z + q * se)


def jzs_bf_corr(r, n):
    """Wetzels & Wagenmakers (2012) JZS Bayes faktoru, korelasyon icin (BF10).

    Tasmayi onlemek icin log-olcekte, g = exp(u) donusumuyle hesaplanir.
    """
    def logf(u):  # log[f(g) * dg/du], g = e^u
        g = math.exp(u)
        return (((n - 2) / 2) * math.log1p(g)
                - ((n - 1) / 2) * math.log1p((1 - r ** 2) * g)
                - 1.5 * u - n / (2 * g) + u)
    grid = np.linspace(-10, 40, 5001)
    vals = np.array([logf(u) for u in grid])
    m = vals.max()
    u0 = grid[vals.argmax()]
    val = integrate.quad(lambda u: math.exp(logf(u) - m), -10, 60, points=[u0], limit=500)[0]
    log_bf = math.log(math.sqrt(n / 2) / math.gamma(0.5)) + m + math.log(val)
    return math.exp(min(log_bf, 700))


def jzs_bf_ttest(t, n1, n2, rscale=math.sqrt(2) / 2):
    """Rouder vd. (2009) JZS Bayes faktoru, iki bagimsiz orneklem (BF10), Cauchy olcegi 0.707."""
    nu = n1 + n2 - 2
    neff = n1 * n2 / (n1 + n2)

    def f(g):
        return ((1 + neff * g * rscale ** 2) ** -0.5
                * (1 + t ** 2 / ((1 + neff * g * rscale ** 2) * nu)) ** (-(nu + 1) / 2)
                * (2 * math.pi) ** -0.5 * g ** -1.5 * math.exp(-1 / (2 * g)))
    num = integrate.quad(f, 0, np.inf, limit=200)[0]
    den = (1 + t ** 2 / nu) ** (-(nu + 1) / 2)
    return num / den


def post_prob(bf10):
    """Esit (1:1) on olasilikla P(H1 | veri)."""
    return bf10 / (1 + bf10)


def boot_corr(x, y, method="pearson"):
    n = len(x)
    out = np.empty(N_BOOT)
    for i in range(N_BOOT):
        idx = RNG.integers(0, n, n)
        if method == "pearson":
            out[i] = np.corrcoef(x[idx], y[idx])[0, 1]
        else:
            out[i] = stats.spearmanr(x[idx], y[idx])[0]
    return out


def corr_block(col):
    d = df[[col, "gpa"]].dropna()
    x, y = d[col].to_numpy(), d["gpa"].to_numpy()
    n = len(d)
    r, p = stats.pearsonr(x, y)
    rho, p_s = stats.spearmanr(x, y)
    lo, hi = fisher_ci(r, n)
    b = boot_corr(x, y)
    bf = jzs_bf_corr(r, n)
    slope = stats.linregress(x, y)
    return {
        "n": int(n),
        "pearson_r": float(r), "pearson_p": float(p), "pearson_ci95": [lo, hi],
        "spearman_rho": float(rho), "spearman_p": float(p_s),
        "bootstrap_ci95": [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))],
        "bootstrap_P_r_pozitif": float((b > 0).mean()),
        "bootstrap_P_r_negatif": float((b < 0).mean()),
        "egim_puan_per_saat": float(slope.slope), "egim_se": float(slope.stderr),
        "r2": float(r ** 2),
        "BF10_JZS": float(bf), "P_H1_given_data_1to1_prior": post_prob(bf),
    }


# --------------------------------------------------- coklu regresyon
cc = df.dropna(subset=["calisma", "sosyal", "uyku", "gpa"]).copy()
model = smf.ols("gpa ~ calisma + sosyal + uyku + kiz + ozel", data=cc).fit(cov_type="HC3")
model_q = smf.ols("gpa ~ calisma + sosyal + uyku + I(uyku**2) + kiz + ozel", data=cc).fit(cov_type="HC3")
# 100 tavanini dislayan duyarlilik
model_nc = smf.ols("gpa ~ calisma + sosyal + uyku + kiz + ozel", data=cc[cc.gpa < 100]).fit(cov_type="HC3")
# etkilesim: calisma x cinsiyet (cinsiyet farki calismaya bagli mi?)
model_std = smf.ols("gpa ~ calisma + sosyal + uyku + kiz + ozel",
                    data=cc.assign(**{c: (cc[c] - cc[c].mean()) / cc[c].std() for c in ["calisma", "sosyal", "uyku"]})
                    ).fit(cov_type="HC3")


def coef(m, name):
    ci = m.conf_int().loc[name]
    return {"b": float(m.params[name]), "se": float(m.bse[name]), "p": float(m.pvalues[name]),
            "ci95": [float(ci[0]), float(ci[1])]}


regresyon = {
    "n": int(model.nobs), "r2": float(model.rsquared), "r2_adj": float(model.rsquared_adj),
    "se_turu": "HC3 (heteroskedastisiteye dayanikli)",
    "katsayilar": {k: coef(model, k) for k in ["calisma", "sosyal", "uyku", "kiz", "ozel"]},
    "standart_katsayilar_(1SS_artisin_puan_etkisi)": {k: coef(model_std, k) for k in ["calisma", "sosyal", "uyku"]},
    "uyku_kare_terimi": coef(model_q, "I(uyku ** 2)"),
    "tavan_disi_(gpa<100)": {"n": int(model_nc.nobs),
                             "katsayilar": {k: coef(model_nc, k) for k in ["calisma", "sosyal", "uyku", "kiz"]}},
}

# ------------------------------------------------ Iddia 1: calisma
i1 = corr_block("calisma")
# ucuc deger hassasiyeti: calisma=0 olan ogrenciyi cikar
d = df[df.calisma > 0]
i1["calisma0_haric_r"] = float(stats.pearsonr(d.calisma, d.gpa)[0])
i1["ceyreklere_gore_ortalama_not"] = (
    df.groupby(pd.qcut(df.calisma, 4, labels=["Q1 (en az)", "Q2", "Q3", "Q4 (en cok)"]), observed=True)
    .gpa.agg(["count", "mean"]).round(1).reset_index().astype({"calisma": str}).to_dict("records"))
i1["ceyrek_aralik_sinirlari"] = [float(v) for v in df.calisma.quantile([0, .25, .5, .75, 1])]
i1["regresyon_kontrollu"] = regresyon["katsayilar"]["calisma"]

# ------------------------------------------- Iddia 2: sosyal medya
i2 = corr_block("sosyal")
d = df.dropna(subset=["sosyal"])
d2 = d[d.sosyal < d.sosyal.quantile(0.99)]
i2["en_ust_%1_haric_r"] = float(stats.pearsonr(d2.sosyal, d2.gpa)[0])
i2["sosyal_ile_calisma_r"] = float(stats.pearsonr(d.sosyal, d.calisma)[0])
d3 = df.dropna(subset=["sosyal", "uyku"])
i2["sosyal_ile_uyku_r"] = float(stats.pearsonr(d3.sosyal, d3.uyku)[0])
i2["ceyreklere_gore_ortalama_not"] = (
    d.groupby(pd.qcut(d.sosyal, 4, labels=["Q1 (en az)", "Q2", "Q3", "Q4 (en cok)"]), observed=True)
    .gpa.agg(["count", "mean"]).round(1).reset_index().astype({"sosyal": str}).to_dict("records"))
i2["ceyrek_aralik_sinirlari"] = [float(v) for v in d.sosyal.quantile([0, .25, .5, .75, 1])]
i2["regresyon_kontrollu"] = regresyon["katsayilar"]["sosyal"]

# ------------------------------------------------ Iddia 3: cinsiyet
k = df.loc[df.kiz == 1, "gpa"].to_numpy()
e = df.loc[df.kiz == 0, "gpa"].to_numpy()
t, p_two = stats.ttest_ind(k, e, equal_var=False)
p_one_k_gt_e = float(stats.ttest_ind(k, e, equal_var=False, alternative="greater").pvalue)
u = stats.mannwhitneyu(k, e, alternative="two-sided")
sp = math.sqrt(((len(k) - 1) * k.var(ddof=1) + (len(e) - 1) * e.var(ddof=1)) / (len(k) + len(e) - 2))
dcoh = (k.mean() - e.mean()) / sp
se_diff = math.sqrt(k.var(ddof=1) / len(k) + e.var(ddof=1) / len(e))
dfw = se_diff ** 4 / ((k.var(ddof=1) / len(k)) ** 2 / (len(k) - 1) + (e.var(ddof=1) / len(e)) ** 2 / (len(e) - 1))
q = stats.t.ppf(0.975, dfw)
diff = k.mean() - e.mean()
bdiff = np.array([RNG.choice(k, len(k)).mean() - RNG.choice(e, len(e)).mean() for _ in range(N_BOOT)])
t_student = stats.ttest_ind(k, e, equal_var=True).statistic
bf_g = jzs_bf_ttest(float(t_student), len(k), len(e))
adj = smf.ols("gpa ~ kiz + ozel", data=df).fit(cov_type="HC3")
i3 = {
    "n_kiz": int(len(k)), "n_erkek": int(len(e)),
    "ort_kiz": float(k.mean()), "ort_erkek": float(e.mean()),
    "ss_kiz": float(k.std(ddof=1)), "ss_erkek": float(e.std(ddof=1)),
    "medyan_kiz": float(np.median(k)), "medyan_erkek": float(np.median(e)),
    "fark_kiz_eksi_erkek": float(diff), "fark_ci95_welch": [diff - q * se_diff, diff + q * se_diff],
    "welch_t": float(t), "welch_p_iki_yonlu": float(p_two),
    "tek_yonlu_p_(kiz>erkek)": p_one_k_gt_e,
    "mann_whitney_p": float(u.pvalue),
    "cohens_d": float(dcoh),
    "bootstrap_P_kiz_ort_buyuk": float((bdiff > 0).mean()),
    "BF10_JZS_(iki_yonlu,_r=0.707)": float(bf_g), "BF01_(fark_yok_lehine)": float(1 / bf_g),
    "P_H1_given_data_1to1_prior": post_prob(bf_g),
    "okul_turu_kontrollu": coef(adj, "kiz"),
    "tum_degiskenler_kontrollu": regresyon["katsayilar"]["kiz"],
    "okul_turune_gore": df.groupby(["okul_turu", "cinsiyet"]).gpa.agg(["count", "mean"]).round(2)
    .reset_index().to_dict("records"),
}

# --------------------------------------------------- Iddia 4: uyku
i4 = corr_block("uyku")
# esdegerlik testi (TOST): |r| < 0.10 ("alakasi yok" = pratikte ihmal edilebilir)
n4 = i4["n"]
z = math.atanh(i4["pearson_r"])
se = 1 / math.sqrt(n4 - 3)
bound = 0.10
p_low = 1 - stats.norm.cdf((z - math.atanh(-bound)) / se)
p_up = stats.norm.cdf((z - math.atanh(bound)) / se)
i4["TOST_|r|<0.10_p"] = float(max(p_low, p_up))
i4["uyku_kare_terimi"] = regresyon["uyku_kare_terimi"]
i4["regresyon_kontrollu"] = regresyon["katsayilar"]["uyku"]
d = df.dropna(subset=["uyku"])
i4["gruplara_gore_ortalama_not"] = (
    d.groupby(pd.cut(d.uyku, [0, 6, 7, 8, 24], right=False,
                     labels=["<6 saat", "6-7 saat", "7-8 saat", ">=8 saat"]), observed=True)
    .gpa.agg(["count", "mean"]).round(1).reset_index().astype({"uyku": str}).to_dict("records"))
d4 = df.dropna(subset=["uyku", "sosyal"])
i4["uyku_eksik_olanlarin_ort_notu"] = float(df[df.uyku.isna()].gpa.mean())
i4["uyku_var_olanlarin_ort_notu"] = float(d.gpa.mean())

# ------------------------------------------------ coklu karsilastirma
raw_p = {"iddia1": i1["pearson_p"], "iddia2": i2["pearson_p"], "iddia3": i3["welch_p_iki_yonlu"],
         "iddia4": i4["pearson_p"]}
order = sorted(raw_p, key=raw_p.get)
holm, running = {}, 0.0
for rank, kk in enumerate(order):
    running = max(running, min(1.0, (len(order) - rank) * raw_p[kk]))
    holm[kk] = running

sonuc = {
    "veri_kalitesi": veri_kalitesi,
    "iddia1_calisma_not": i1,
    "iddia2_sosyal_medya_not": i2,
    "iddia3_kiz_erkek": i3,
    "iddia4_uyku_not": i4,
    "coklu_regresyon": regresyon,
    "holm_duzeltilmis_p": holm,
    "notlar": {
        "bootstrap_tekrar": N_BOOT,
        "bayes": "JZS Bayes faktoru; P(H1|veri) esit on olasilik (0.5/0.5) varsayimiyla.",
        "eksik_veri": "Her analizde mevcut durum (pairwise/complete-case) analizi.",
    },
}
with open(os.path.join(HERE, "analiz_sonuclari.json"), "w", encoding="utf-8") as fh:
    json.dump(sonuc, fh, ensure_ascii=False, indent=2, default=float)
print(model.summary())
print(json.dumps(sonuc, ensure_ascii=False, indent=1, default=float))
