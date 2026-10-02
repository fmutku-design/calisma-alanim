"""Uzaktan calisma - verimlilik analizi (yalnizca Python standart kutuphanesi)."""
import csv, json, math, random, statistics as st, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/home/user/calisma-alanim/iddia-dogrulama-workspace/inputs/calisan_verimlilik.csv"
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
for r in rows:
    r["kidem_yil"] = float(r["kidem_yil"]); r["uz"] = int(r["haftalik_uzaktan_gun"]); r["v"] = float(r["verimlilik_puani"])

# ---------- yardimci istatistik ----------
def betacf(a, b, x):
    MAXIT, EPS, FPMIN = 300, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > FPMIN else FPMIN); h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; d = FPMIN if abs(d) < FPMIN else d
        c = 1 + aa / c; c = FPMIN if abs(c) < FPMIN else c
        d = 1 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; d = FPMIN if abs(d) < FPMIN else d
        c = 1 + aa / c; c = FPMIN if abs(c) < FPMIN else c
        d = 1 / d; de = d * c; h *= de
        if abs(de - 1) < EPS: break
    return h
def betai(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    return bt * betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - bt * betacf(b, a, 1 - x) / b
def p_t(t, df):  # iki yonlu
    return betai(df / 2, 0.5, df / (df + t * t))
def t_crit(df, alpha=0.05):
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if p_t(mid, df) > alpha: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def pearson(x, y):
    mx, my = st.mean(x), st.mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x); syy = sum((b - my) ** 2 for b in y)
    r = sxy / math.sqrt(sxx * syy); n = len(x)
    t = r * math.sqrt((n - 2) / (1 - r * r)); p = p_t(t, n - 2)
    z = math.atanh(r); se = 1 / math.sqrt(n - 3)
    return {"n": n, "r": r, "p": p, "ci95": [math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se)]}

def rank(v):
    s = sorted(range(len(v)), key=lambda i: v[i]); rk = [0.0] * len(v); i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[s[j + 1]] == v[s[i]]: j += 1
        for k in range(i, j + 1): rk[s[k]] = (i + j) / 2 + 1
        i = j + 1
    return rk
def spearman(x, y):
    res = pearson(rank(x), rank(y)); return {"rho": res["r"], "p": res["p"], "n": res["n"]}

def inv(M):
    n = len(M); A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c])); A[c], A[p] = A[p], A[c]
        pv = A[c][c]; A[c] = [v / pv for v in A[c]]
        for r in range(n):
            if r != c:
                f = A[r][c]; A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [row[n:] for row in A]
def ols(X, y, names):
    n, k = len(X), len(X[0])
    XtX = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    Xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(k)]
    XtXi = inv(XtX); beta = [sum(XtXi[a][b] * Xty[b] for b in range(k)) for a in range(k)]
    res = [y[i] - sum(beta[a] * X[i][a] for a in range(k)) for i in range(n)]
    sse = sum(e * e for e in res); df = n - k; s2 = sse / df
    my = st.mean(y); sst = sum((v - my) ** 2 for v in y)
    # HC1 robust SE de hesapla
    meat = [[sum(X[i][a] * X[i][b] * res[i] ** 2 for i in range(n)) for b in range(k)] for a in range(k)]
    hc = [[sum(XtXi[a][c] * meat[c][d] * XtXi[d][b] for c in range(k) for d in range(k)) * n / df for b in range(k)] for a in range(k)]
    tc = t_crit(df); out = {}
    for a in range(k):
        se = math.sqrt(s2 * XtXi[a][a]); t = beta[a] / se; rse = math.sqrt(hc[a][a])
        out[names[a]] = {"b": beta[a], "se": se, "t": t, "p": p_t(t, df), "ci95": [beta[a] - tc * se, beta[a] + tc * se],
                         "robust_se_HC1": rse, "robust_p": p_t(beta[a] / rse, df)}
    return {"n": n, "k": k, "df": df, "r2": 1 - sse / sst, "adj_r2": 1 - (sse / df) / (sst / (n - 1)), "sse": sse, "coef": out}

def f_test(full, red):
    q = full["k"] - red["k"]; F = ((red["sse"] - full["sse"]) / q) / (full["sse"] / full["df"])
    p = betai(full["df"] / 2, q / 2, full["df"] / (full["df"] + q * F)); return {"F": F, "df1": q, "df2": full["df"], "p": p}

def perm_slope_within(rows, B=5000, seed=42):
    """Departman ici permutasyon: uzaktan gunleri yalniz departman icinde karistirip, departman-ici egimi test eder."""
    rnd = random.Random(seed)
    def within_slope(uz):
        num = den = 0.0
        for d in deps:
            idx = [i for i, r in enumerate(rows) if r["departman"] == d]
            mx = st.mean(uz[i] for i in idx); my = st.mean(rows[i]["v"] for i in idx)
            num += sum((uz[i] - mx) * (rows[i]["v"] - my) for i in idx); den += sum((uz[i] - mx) ** 2 for i in idx)
        return num / den
    uz0 = [r["uz"] for r in rows]; obs = within_slope(uz0); cnt = 0
    groups = {d: [i for i, r in enumerate(rows) if r["departman"] == d] for d in deps}
    for _ in range(B):
        uz = uz0[:]
        for d, idx in groups.items():
            vals = [uz0[i] for i in idx]; rnd.shuffle(vals)
            for i, v in zip(idx, vals): uz[i] = v
        if abs(within_slope(uz)) >= abs(obs) - 1e-12: cnt += 1
    return {"observed_within_slope": obs, "B": B, "p_two_sided": (cnt + 1) / (B + 1)}

deps = sorted({r["departman"] for r in rows})
R = {"veri": {"n": len(rows), "departmanlar": {d: sum(r["departman"] == d for r in rows) for d in deps},
              "eksik_deger": 0}}
uz = [r["uz"] for r in rows]; v = [r["v"] for r in rows]; kd = [r["kidem_yil"] for r in rows]

# 1) Ham (havuzlanmis) iliski
R["ham_iliski"] = {"pearson": pearson(uz, v), "spearman": spearman(uz, v),
                   "basit_regresyon": ols([[1, x] for x in uz], v, ["sabit", "uzaktan_gun"])}
R["uzaktan_gun_bazinda_ortalama"] = {str(g): {"n": sum(1 for x in uz if x == g),
    "ort_verimlilik": st.mean([r["v"] for r in rows if r["uz"] == g])} for g in sorted(set(uz))}

# 2) Departman bazinda
R["departman_bazinda"] = {}
for d in deps:
    s = [r for r in rows if r["departman"] == d]
    R["departman_bazinda"][d] = {"n": len(s), "ort_uzaktan_gun": st.mean(r["uz"] for r in s),
        "ort_verimlilik": st.mean(r["v"] for r in s), "ort_kidem": st.mean(r["kidem_yil"] for r in s),
        "pearson_uz_v": pearson([r["uz"] for r in s], [r["v"] for r in s]),
        "egim_uz": ols([[1, r["uz"]] for r in s], [r["v"] for r in s], ["sabit", "uzaktan_gun"])["coef"]["uzaktan_gun"],
        "egim_uz_kidem_kontrollu": ols([[1, r["uz"], r["kidem_yil"]] for r in s], [r["v"] for r in s], ["sabit", "uzaktan_gun", "kidem"])["coef"]["uzaktan_gun"]}

# 3) Karistirici degiskenler: departman ve kidem ile uzaktan gun / verimlilik iliskisi
R["karistirici_kontrol"] = {"kidem_vs_uzaktan": pearson(kd, uz), "kidem_vs_verimlilik": pearson(kd, v)}

# 4) Coklu regresyon modelleri
base = deps[0]; dd = [d for d in deps if d != base]
def X_of(r, uzaktan=True, kidem=True, dep=True, quad=False, inter=False):
    x = [1.0]
    if uzaktan: x.append(r["uz"])
    if quad: x.append(r["uz"] ** 2)
    if kidem: x.append(r["kidem_yil"])
    if dep: x += [1.0 if r["departman"] == d else 0.0 for d in dd]
    if inter: x += [r["uz"] * (1.0 if r["departman"] == d else 0.0) for d in dd]
    return x
def nm(uzaktan=True, kidem=True, dep=True, quad=False, inter=False):
    n = ["sabit"]
    if uzaktan: n.append("uzaktan_gun")
    if quad: n.append("uzaktan_gun_kare")
    if kidem: n.append("kidem_yil")
    if dep: n += [f"dep_{d}" for d in dd]
    if inter: n += [f"uzaktan_x_{d}" for d in dd]
    return n
M = {}
M["m1_sadece_uzaktan"] = ols([X_of(r, kidem=False, dep=False) for r in rows], v, nm(kidem=False, dep=False))
M["m2_uzaktan+departman"] = ols([X_of(r, kidem=False) for r in rows], v, nm(kidem=False))
M["m3_uzaktan+kidem"] = ols([X_of(r, dep=False) for r in rows], v, nm(dep=False))
M["m4_uzaktan+kidem+departman"] = ols([X_of(r) for r in rows], v, nm())
M["m0_kidem+departman_(uzaktansiz)"] = ols([X_of(r, uzaktan=False) for r in rows], v, nm(uzaktan=False))
M["m5_kare_terimli"] = ols([X_of(r, quad=True) for r in rows], v, nm(quad=True))
M["m6_departman_etkilesimli"] = ols([X_of(r, inter=True) for r in rows], v, nm(inter=True))
R["modeller"] = {k: {"r2": m["r2"], "adj_r2": m["adj_r2"], "n": m["n"], "coef": m["coef"]} for k, m in M.items()}
R["model_testleri"] = {
    "uzaktan_katkisi_F_(m4_vs_m0)": f_test(M["m4_uzaktan+kidem+departman"], M["m0_kidem+departman_(uzaktansiz)"]),
    "dogrusal_olmama_F_(m5_vs_m4)": f_test(M["m5_kare_terimli"], M["m4_uzaktan+kidem+departman"]),
    "departmana_gore_farkli_etki_F_(m6_vs_m4)": f_test(M["m6_departman_etkilesimli"], M["m4_uzaktan+kidem+departman"])}
R["departman_ici_permutasyon"] = perm_slope_within(rows)

# 5) Esdegerlik (TOST) - "hic iliski yok" iddiasi icin: anlamli etki esigi +/- 1 puan/gun (varsayim)
c = M["m4_uzaktan+kidem+departman"]["coef"]["uzaktan_gun"]; df = M["m4_uzaktan+kidem+departman"]["df"]
sd_v = st.stdev(v)
R["etki_buyuklugu"] = {"verimlilik_sd": sd_v, "kontrollu_egim_puan_per_gun": c["b"],
    "kontrollu_egim_sd_cinsinden": c["b"] / sd_v,
    "0_vs_5_gun_fark_puan": 5 * c["b"], "0_vs_5_gun_fark_sd": 5 * c["b"] / sd_v,
    "ortalama_verimlilige_gore_yuzde_per_gun": 100 * c["b"] / st.mean(v)}

json.dump(R, open(os.path.join(HERE, "sonuclar.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# kisa konsol ozeti
f = lambda x: round(x, 3)
print("HAM:", {k: f(x) if isinstance(x, float) else x for k, x in R["ham_iliski"]["pearson"].items() if k != "ci95"}, [f(x) for x in R["ham_iliski"]["pearson"]["ci95"]])
print("HAM egim:", f(M["m1_sadece_uzaktan"]["coef"]["uzaktan_gun"]["b"]), "p", R["ham_iliski"]["basit_regresyon"]["coef"]["uzaktan_gun"]["p"])
print("Gun ortalamalari:", {k: (x["n"], f(x["ort_verimlilik"])) for k, x in R["uzaktan_gun_bazinda_ortalama"].items()})
for d, x in R["departman_bazinda"].items():
    print(d, x["n"], "uz", f(x["ort_uzaktan_gun"]), "v", f(x["ort_verimlilik"]), "kidem", f(x["ort_kidem"]), "r", f(x["pearson_uz_v"]["r"]), "p", f(x["pearson_uz_v"]["p"]),
          "egim", f(x["egim_uz"]["b"]), [f(t) for t in x["egim_uz"]["ci95"]], "kidemk egim", f(x["egim_uz_kidem_kontrollu"]["b"]), f(x["egim_uz_kidem_kontrollu"]["p"]))
print("Karistirici:", {k: (f(x["r"]), x["p"]) for k, x in R["karistirici_kontrol"].items()})
for k, m in M.items():
    print(k, "R2", f(m["r2"]), {n: (f(c["b"]), f(c["se"]), "%.2g" % c["p"], [f(t) for t in c["ci95"]], "rob_p %.2g" % c["robust_p"]) for n, c in m["coef"].items()})
print(json.dumps(R["model_testleri"], indent=1)); print(R["departman_ici_permutasyon"]); print(R["etki_buyuklugu"])
