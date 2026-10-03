"""Uzaktan calisma - verimlilik iddialarinin dogrulanmasi.
Girdi: inputs/calisan_verimlilik.csv (180 calisan)
Cikti: sonuclar.json + 3 grafik (PNG), bu klasore.
"""
import json, os
import numpy as np, pandas as pd, scipy.stats as st
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
SRC = "/home/user/calisma-alanim/iddia-dogrulama-workspace/inputs/calisan_verimlilik.csv"
d = pd.read_csv(SRC)
Y, X, K = "verimlilik_puani", "haftalik_uzaktan_gun", "kidem_yil"
rng = np.random.default_rng(20261003)
R = {}

# --- veri kalitesi
R["veri"] = {
    "n": int(len(d)), "eksik_deger": int(d.isna().sum().sum()),
    "tekrarlanan_id": int(d.duplicated("calisan_id").sum()),
    "departman_n": d.departman.value_counts().to_dict(),
    "uzaktan_gun_aralik": [int(d[X].min()), int(d[X].max())],
    "kidem_aralik": [float(d[K].min()), float(d[K].max())],
    "verimlilik_aralik": [float(d[Y].min()), float(d[Y].max())],
    "verimlilik_ort": round(float(d[Y].mean()), 2),
}

# --- 1) ham iliski
pr = st.pearsonr(d[X], d[Y]); sr = st.spearmanr(d[X], d[Y])
ci = pr.confidence_interval(0.95)
grp = d.groupby(X)[Y].agg(["count", "mean", "std"])
grp["se"] = grp["std"] / np.sqrt(grp["count"])
m0 = smf.ols(f"{Y} ~ {X}", d).fit(cov_type="HC3")
R["ham_iliski"] = {
    "pearson_r": round(pr.statistic, 3), "pearson_r_95GA": [round(ci.low, 3), round(ci.high, 3)],
    "pearson_p": float(pr.pvalue), "spearman_rho": round(sr.statistic, 3), "spearman_p": float(sr.pvalue),
    "egim_puan_per_gun": round(m0.params[X], 2),
    "egim_95GA": [round(v, 2) for v in m0.conf_int().loc[X]],
    "gun_gruplari": {int(k): {"n": int(r["count"]), "ort": round(r["mean"], 1), "ss": round(r["std"], 1)} for k, r in grp.iterrows()},
    "fark_5gun_vs_0gun": round(grp.loc[5, "mean"] - grp.loc[0, "mean"], 1),
}

# --- 2) karistirici: kidem
R["kidem_karistirici"] = {
    "r_kidem_uzaktan": round(st.pearsonr(d[K], d[X]).statistic, 3),
    "r_kidem_verimlilik": round(st.pearsonr(d[K], d[Y]).statistic, 3),
    "gun_gruplarina_gore_ort_kidem": {int(k): round(v, 1) for k, v in d.groupby(X)[K].mean().items()},
    "R2_sadece_uzaktan": round(smf.ols(f"{Y} ~ {X}", d).fit().rsquared, 3),
    "R2_sadece_kidem": round(smf.ols(f"{Y} ~ {K}", d).fit().rsquared, 3),
}
r1 = smf.ols(f"{Y} ~ {K} + C(departman)", d).fit().resid
r2 = smf.ols(f"{X} ~ {K} + C(departman)", d).fit().resid
pc = st.pearsonr(r1, r2)
R["kidem_karistirici"]["kismi_r_uzaktan_verimlilik_kidem_dept_sabit"] = round(pc.statistic, 3)
R["kidem_karistirici"]["kismi_r_p"] = round(pc.pvalue, 3)

# --- 3) duzeltilmis modeller (HC3 saglam SH)
models = {
    "M1_ham": f"{Y} ~ {X}",
    "M2_kidem": f"{Y} ~ {X} + {K}",
    "M3_kidem_dept": f"{Y} ~ {X} + {K} + C(departman)",
    "M4_kidem2_dept": f"{Y} ~ {X} + {K} + I({K}**2) + C(departman)",
    "M5_kidem_ceyrek_dept": f"{Y} ~ {X} + C(kq) + C(departman)",
}
d["kq"] = pd.qcut(d[K], 4, labels=["Q1", "Q2", "Q3", "Q4"])
R["modeller"] = {}
for name, f in models.items():
    m = smf.ols(f, d).fit(cov_type="HC3")
    R["modeller"][name] = {"formul": f, "egim_puan_per_gun": round(m.params[X], 2),
                           "95GA": [round(v, 2) for v in m.conf_int().loc[X]],
                           "p": round(m.pvalues[X], 3), "R2": round(m.rsquared, 3)}
main = smf.ols(models["M3_kidem_dept"], d).fit(cov_type="HC3")
b, (lo, hi) = main.params[X], main.conf_int().loc[X]
# bootstrap
bs = []
for _ in range(2000):
    s = d.sample(len(d), replace=True, random_state=int(rng.integers(1e9)))
    bs.append(smf.ols(models["M3_kidem_dept"], s).fit().params[X])
bs = np.array(bs)
R["ana_sonuc"] = {
    "model": "M3: verimlilik ~ uzaktan_gun + kidem + departman (HC3)",
    "egim": round(b, 2), "95GA": [round(lo, 2), round(hi, 2)], "p": round(main.pvalues[X], 3),
    "bootstrap_95GA": [round(np.percentile(bs, 2.5), 2), round(np.percentile(bs, 97.5), 2)],
    "bootstrap_pay_egim_negatif": round(float((bs < 0).mean()), 3),
    "0dan_5gune_ima_edilen_etki_95GA": [round(5 * lo, 1), round(5 * hi, 1)],
    "kidem_katsayisi_puan_per_yil": round(main.params[K], 2),
}
# esdegerlik (TOST, 90% GA) farkli marjlar
lo90, hi90 = main.conf_int(alpha=0.10).loc[X]
R["esdegerlik_TOST"] = {"90GA": [round(lo90, 2), round(hi90, 2)],
                        **{f"marj_+-{mj}_puan_per_gun": bool(lo90 > -mj and hi90 < mj) for mj in [0.5, 1, 1.5, 2]}}

# --- 4) departmanlar
dep = {}
for g, s in d.groupby("departman"):
    raw = st.pearsonr(s[X], s[Y])
    ma = smf.ols(f"{Y} ~ {X} + {K}", s).fit(cov_type="HC3")
    dep[g] = {"n": int(len(s)), "ham_r": round(raw.statistic, 3), "ham_p": round(raw.pvalue, 4),
              "duzeltilmis_egim": round(ma.params[X], 2), "95GA": [round(v, 2) for v in ma.conf_int().loc[X]],
              "p": round(ma.pvalues[X], 3)}
full = smf.ols(f"{Y} ~ {X} * C(departman) + {K}", d).fit()
red = smf.ols(f"{Y} ~ {X} + C(departman) + {K}", d).fit()
ft = full.compare_f_test(red)
R["departmanlar"] = {"departman_bazinda": dep, "etkilesim_F": round(ft[0], 3), "etkilesim_p": round(ft[1], 3)}

# --- 5) kidem ceyreklerinde (tabakalandirma)
strata = {}
for q, s in d.groupby("kq", observed=True):
    r = st.pearsonr(s[X], s[Y]); sl = smf.ols(f"{Y} ~ {X}", s).fit(cov_type="HC3")
    strata[str(q)] = {"kidem_aralik": [float(s[K].min()), float(s[K].max())], "n": int(len(s)),
                      "r": round(r.statistic, 3), "p": round(r.pvalue, 3),
                      "egim": round(sl.params[X], 2), "95GA": [round(v, 2) for v in sl.conf_int().loc[X]]}
R["kidem_ceyreklerinde"] = strata

# --- 6) dogrusal olmayanlik: gun kategorik
mc = smf.ols(f"{Y} ~ C({X}) + {K} + I({K}**2) + C(departman)", d).fit(cov_type="HC3")
R["gun_kategorik_0_gune_gore"] = {k.split("[T.")[1].rstrip("]"): {"fark": round(v, 2), "95GA": [round(x, 2) for x in mc.conf_int().loc[k]], "p": round(mc.pvalues[k], 3)}
                                  for k, v in mc.params.items() if k.startswith(f"C({X})")}
R["gun_kategorik_not"] = ("5 gun grubu n=12 ve ortalama kidemi 11.4 yil (kidem dagiliminin ucu); 5 karsilastirmadan "
                          "biri, coklu karsilastirma duzeltmesi (Bonferroni esik 0.01) sonrasi anlamli degil. Ust kidemde (>9 yil) "
                          "3/4/5 gun gruplarinin ham ortalamalari ~78 ile esit.")
R["kidem_9_ustu_gun_ort"] = {int(k): round(v, 1) for k, v in d[d[K] > 9].groupby(X)[Y].mean().items()}

# --- Bloom karsilastirmasi (olcek donusumu kaba varsayim)
bloom_pts_4gun = 0.13 * d[Y].mean()
R["bloom_kiyas"] = {"varsayim": "Bloom'daki %13 artis (haftada 4 gun evden) bu sirketin ortalama puanina oransal tasinirsa",
                    "beklenen_puan_4gun": round(bloom_pts_4gun, 1), "beklenen_puan_per_gun": round(bloom_pts_4gun / 4, 2),
                    "bu_veride_ust_GA_per_gun": round(hi, 2),
                    "yorum": "Bloom buyuklugunde pozitif etki bu sirketin (duzeltilmis) verisiyle uyumsuz"}

with open(os.path.join(OUT, "sonuclar.json"), "w", encoding="utf-8") as fh:
    json.dump(R, fh, ensure_ascii=False, indent=2, default=float)

# ---------------- grafikler
BLUE, ORANGE, INK, INK2, GRID = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb"})

# G1: ham iliski - gun basina ortalama verimlilik
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
ax.bar(grp.index, grp["mean"], width=0.6, color=BLUE, edgecolor="#fcfcfb", linewidth=2)
ax.errorbar(grp.index, grp["mean"], yerr=1.96 * grp["se"], fmt="none", ecolor=INK2, capsize=4, lw=1.2)
for k, r in grp.iterrows():
    ax.text(k, 40.8, f"n={int(r['count'])}", ha="center", color="white", fontsize=8.5)
    ax.text(k, r["mean"] + 1.96 * r["se"] + 1, f"{r['mean']:.1f}", ha="center", color=INK, fontsize=9)
ax.set_ylim(40, 90); ax.set_xlabel("Haftalık uzaktan çalışma günü"); ax.set_ylabel("Ortalama verimlilik puanı")
ax.set_title("Ham tablo: uzaktan gün arttıkça verimlilik yükseliyor gibi görünüyor\n(r = %.2f; çubuklar %%95 güven aralığı)" % pr.statistic,
             loc="left", fontsize=11, color=INK)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "grafik_1_ham_iliski.png"), dpi=160); plt.close(fig)

# G2: kidem karistiricisi - iki panel
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
kg = d.groupby(X)[K].agg(["mean", "std", "count"])
axs[0].grid(axis="y", color=GRID, lw=0.8); axs[0].set_axisbelow(True)
axs[0].bar(kg.index, kg["mean"], width=0.6, color=ORANGE, edgecolor="#fcfcfb", linewidth=2)
for k, r in kg.iterrows():
    axs[0].text(k, r["mean"] + 0.3, f"{r['mean']:.1f}", ha="center", fontsize=9, color=INK)
axs[0].set_xlabel("Haftalık uzaktan çalışma günü"); axs[0].set_ylabel("Ortalama kıdem (yıl)")
axs[0].set_title("Uzaktan günü çok olanlar daha kıdemli\n(r = %.2f)" % R["kidem_karistirici"]["r_kidem_uzaktan"], loc="left", fontsize=11)
axs[1].grid(color=GRID, lw=0.8); axs[1].set_axisbelow(True)
axs[1].scatter(d[K], d[Y], s=22, color=ORANGE, edgecolor="#fcfcfb", linewidth=0.8, alpha=0.9)
z = np.polyfit(d[K], d[Y], 1); xs = np.linspace(0, d[K].max(), 50)
axs[1].plot(xs, np.polyval(z, xs), color=INK2, lw=2)
axs[1].set_xlabel("Kıdem (yıl)"); axs[1].set_ylabel("Verimlilik puanı")
axs[1].set_title("Kıdemliler daha verimli\n(r = %.2f)" % R["kidem_karistirici"]["r_kidem_verimlilik"], loc="left", fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "grafik_2_kidem_karistirici.png"), dpi=160); plt.close(fig)

# G3: ham vs duzeltilmis egim (katsayi grafigi)
rows = [("Ham (düzeltmesiz)", R["modeller"]["M1_ham"]),
        ("+ kıdem", R["modeller"]["M2_kidem"]),
        ("+ kıdem + departman (ana model)", R["modeller"]["M3_kidem_dept"]),
        ("+ kıdem² + departman", R["modeller"]["M4_kidem2_dept"]),
        ("kıdem çeyrekleri + departman", R["modeller"]["M5_kidem_ceyrek_dept"])]
fig, ax = plt.subplots(figsize=(8, 4.1))
ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
for i, (lab, r) in enumerate(rows[::-1]):
    c = BLUE if lab.startswith("Ham") else ORANGE
    ax.plot(r["95GA"], [i, i], color=c, lw=2.2); ax.plot(r["egim_puan_per_gun"], i, "o", ms=8, color=c, mec="#fcfcfb", mew=2)
    ax.text(r["95GA"][1] + 0.15, i, f"{r['egim_puan_per_gun']:+.2f}  [{r['95GA'][0]:+.2f}, {r['95GA'][1]:+.2f}]", va="center", fontsize=8.5, color=INK)
ax.axvline(0, color=INK2, lw=1, ls="--")
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]])
ax.set_xlim(-3, 8); ax.set_xlabel("Her ek uzaktan gün başına verimlilik puanı farkı (%95 GA)")
ax.set_title("Kıdem hesaba katılınca \"etki\" sıfır civarına iniyor\n(mavi: ham, turuncu: düzeltilmiş)", loc="left", fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "grafik_3_ham_vs_duzeltilmis.png"), dpi=160); plt.close(fig)
print(json.dumps(R, ensure_ascii=False, indent=1, default=float))
