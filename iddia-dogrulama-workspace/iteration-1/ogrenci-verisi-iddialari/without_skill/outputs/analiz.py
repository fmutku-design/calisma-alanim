"""Danisman iddialarinin ogrenci_verisi.csv ile dogrulanmasi.
Calistirma: python3 analiz.py  (numpy, pandas, scipy, statsmodels gerekir)"""
import json, sys
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

IN = '/home/user/calisma-alanim/iddia-dogrulama-workspace/inputs/ogrenci_verisi.csv'
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
rng = np.random.default_rng(2026)

df = pd.read_csv(IN, sep=';', decimal=',', na_values=['NA', ''])
df = df.rename(columns={'haftalik_calisma_saati': 'calisma', 'gunluk_sosyal_medya_saat': 'sosyal',
                        'uyku_saat': 'uyku', 'not_ortalamasi': 'gpa'})
df['kiz'] = (df.cinsiyet == 'K').astype(int)
df['ozel'] = (df.okul_turu == 'ozel').astype(int)

R = {'veri': {
    'n_toplam': int(len(df)),
    'eksik': {c: int(df[c].isna().sum()) for c in ['calisma', 'sosyal', 'uyku', 'gpa']},
    'not_100_tavan_sayisi': int((df.gpa == 100).sum()),
    'calisma_0_saat': int((df.calisma == 0).sum()),
    'cinsiyet': df.cinsiyet.value_counts().to_dict(),
    'okul_turu': df.okul_turu.value_counts().to_dict(),
    'tanimlayici': df[['calisma', 'sosyal', 'uyku', 'gpa']].describe().round(2).to_dict(),
    'pearson_korelasyon_matrisi': df[['calisma', 'sosyal', 'uyku', 'gpa', 'kiz', 'ozel']].corr().round(3).to_dict(),
}}

def corr_block(x, y):
    d = df[[x, y]].dropna()
    n = len(d)
    r, p = stats.pearsonr(d[x], d[y])
    z, se = np.arctanh(r), 1 / np.sqrt(n - 3)
    lo, hi = np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se)
    rho, prho = stats.spearmanr(d[x], d[y])
    # bootstrap r
    idx = rng.integers(0, n, (5000, n))
    xs, ys = d[x].values[idx], d[y].values[idx]
    xc, yc = xs - xs.mean(1, keepdims=True), ys - ys.mean(1, keepdims=True)
    rb = (xc * yc).sum(1) / np.sqrt((xc**2).sum(1) * (yc**2).sum(1))
    return {'n': n, 'pearson_r': r, 'r_95GA': [lo, hi], 'p': p, 'spearman_rho': rho, 'spearman_p': prho,
            'bootstrap_P(r>0)': float((rb > 0).mean()), 'bootstrap_r_95GA': list(np.percentile(rb, [2.5, 97.5]))}

def bic_bf(full, reduced_formula, data):
    """BIC yaklasimli Bayes faktoru BF10 ve 50/50 onsel ile P(etki var | veri)."""
    red = smf.ols(reduced_formula, data=data).fit()
    bf10 = float(np.exp((red.bic - full.bic) / 2))
    return bf10, bf10 / (1 + bf10)

def coef_block(model, term, reduced_formula, data):
    b, se, p = model.params[term], model.bse[term], model.pvalues[term]
    lo, hi = model.conf_int().loc[term]
    t = b / se
    p_pos = float(stats.t.cdf(t, model.df_resid))  # duz onsel altinda P(beta>0 | veri)
    bf10, p_h1 = bic_bf(model, reduced_formula, data)
    return {'beta': b, 'se': se, '95GA': [lo, hi], 'p_iki_yonlu': p,
            'P(beta>0|veri)_duz_onsel': p_pos, 'P(beta<0|veri)_duz_onsel': 1 - p_pos,
            'BF10_BIC': bf10, 'P(etki_var|veri)_50_50_onsel': p_h1, 'n': int(model.nobs)}

cc = df.dropna(subset=['calisma', 'sosyal', 'uyku', 'gpa']).copy()
FULL = 'gpa ~ calisma + sosyal + uyku + kiz + ozel'
mfull = smf.ols(FULL, data=cc).fit()
mfull_hc = smf.ols(FULL, data=cc).fit(cov_type='HC3')
R['coklu_regresyon'] = {'formul': FULL, 'n': int(mfull.nobs), 'R2': mfull.rsquared, 'R2_duz': mfull.rsquared_adj,
                        'katsayilar': {k: {'beta': mfull.params[k], 'se': mfull.bse[k], 'p': mfull.pvalues[k],
                                           'se_HC3': mfull_hc.bse[k], 'p_HC3': mfull_hc.pvalues[k],
                                           '95GA': list(mfull.conf_int().loc[k])} for k in mfull.params.index}}
std = cc.copy()
for c in ['calisma', 'sosyal', 'uyku', 'gpa']:
    std[c] = (std[c] - std[c].mean()) / std[c].std()
R['coklu_regresyon']['standart_beta'] = smf.ols(FULL, data=std).fit().params.drop('Intercept').to_dict()

# --- Tavan etkisi duyarlilik: not=100 olanlar cikarilinca
m_noceil = smf.ols(FULL, data=cc[cc.gpa < 100]).fit()
R['duyarlilik_not100_haric'] = {k: {'beta': m_noceil.params[k], 'p': m_noceil.pvalues[k]} for k in m_noceil.params.index}
R['duyarlilik_not100_haric']['n'] = int(m_noceil.nobs)

# ---------- IDDIA 1: calisma saati
d1 = df.dropna(subset=['calisma', 'gpa'])
m1 = smf.ols('gpa ~ calisma', data=d1).fit()
q = pd.qcut(d1.calisma, 4, labels=['Q1 (en az)', 'Q2', 'Q3', 'Q4 (en cok)'])
m1q = smf.ols('gpa ~ calisma + I(calisma**2)', data=d1).fit()
R['iddia1_calisma'] = {
    'korelasyon': corr_block('calisma', 'gpa'),
    'basit_regresyon': coef_block(m1, 'calisma', 'gpa ~ 1', d1),
    'kontrollu_regresyon': coef_block(mfull, 'calisma', 'gpa ~ sosyal + uyku + kiz + ozel', cc),
    'ceyreklik_ortalamalar': d1.groupby(q, observed=True).gpa.agg(['count', 'mean']).round(2).reset_index().astype({'calisma': str}).to_dict('records'),
    'ceyrek_sinirlari_saat': list(np.round(d1.calisma.quantile([0, .25, .5, .75, 1]).values, 1)),
    'karesel_terim_p': m1q.pvalues['I(calisma ** 2)'], 'karesel_terim_beta': m1q.params['I(calisma ** 2)'],
}

# ---------- IDDIA 2: sosyal medya
d2 = df.dropna(subset=['sosyal', 'gpa'])
m2 = smf.ols('gpa ~ sosyal', data=d2).fit()
m2b = smf.ols('gpa ~ sosyal + calisma + kiz + ozel', data=df.dropna(subset=['sosyal', 'gpa', 'calisma'])).fit()
R['iddia2_sosyal_medya'] = {
    'korelasyon': corr_block('sosyal', 'gpa'),
    'basit_regresyon': coef_block(m2, 'sosyal', 'gpa ~ 1', d2),
    'kontrollu_regresyon': coef_block(mfull, 'sosyal', 'gpa ~ calisma + uyku + kiz + ozel', cc),
    'uyku_haric_kontrollu': coef_block(m2b, 'sosyal', 'gpa ~ calisma + kiz + ozel', df.dropna(subset=['sosyal', 'gpa', 'calisma'])),
    'sosyal_uyku_korelasyonu': corr_block('sosyal', 'uyku'),
    'sosyal_calisma_korelasyonu': corr_block('sosyal', 'calisma'),
}

# ---------- IDDIA 3: kizlar > erkekler
k = df.loc[df.cinsiyet == 'K', 'gpa']; e = df.loc[df.cinsiyet == 'E', 'gpa']
t, p_welch = stats.ttest_ind(k, e, equal_var=False)
diff = k.mean() - e.mean()
se_d = np.sqrt(k.var() / len(k) + e.var() / len(e))
dfw = (k.var()/len(k) + e.var()/len(e))**2 / ((k.var()/len(k))**2/(len(k)-1) + (e.var()/len(e))**2/(len(e)-1))
sp = np.sqrt(((len(k)-1)*k.var() + (len(e)-1)*e.var()) / (len(k)+len(e)-2))
u, p_mw = stats.mannwhitneyu(k, e, alternative='two-sided')
lev = stats.levene(k, e)
bk = rng.choice(k.values, (10000, len(k))).mean(1); be = rng.choice(e.values, (10000, len(e))).mean(1)
m3 = smf.ols('gpa ~ kiz', data=df).fit()
R['iddia3_cinsiyet'] = {
    'kiz': {'n': int(len(k)), 'ort': k.mean(), 'ss': k.std(), 'medyan': k.median()},
    'erkek': {'n': int(len(e)), 'ort': e.mean(), 'ss': e.std(), 'medyan': e.median()},
    'fark_kiz_eksi_erkek': diff, 'fark_95GA': [diff - stats.t.ppf(.975, dfw)*se_d, diff + stats.t.ppf(.975, dfw)*se_d],
    'welch_t': t, 'welch_p_iki_yonlu': p_welch, 'welch_p_tek_yonlu_kiz>erkek': float(stats.t.sf(t, dfw)),
    'cohen_d': diff / sp, 'mann_whitney_p': p_mw, 'P(kiz>erkek rastgele cift)': u / (len(k)*len(e)),
    'levene_varyans_esitligi_p': lev.pvalue,
    'bootstrap_P(kiz_ort>erkek_ort)': float((bk > be).mean()),
    'P(kiz_ort>erkek_ort|veri)_duz_onsel': float(stats.t.cdf(diff/se_d, dfw)),
    'BF10_BIC_ve_P(fark_var)': bic_bf(m3, 'gpa ~ 1', df),
    'kontrollu_regresyon': coef_block(mfull, 'kiz', 'gpa ~ calisma + sosyal + uyku + ozel', cc),
    'okul_turune_gore_ort': df.groupby(['okul_turu', 'cinsiyet']).gpa.mean().round(2).unstack().to_dict(),
    'calisma_saati_cinsiyete_gore': df.groupby('cinsiyet').calisma.mean().round(2).to_dict(),
}

# ---------- IDDIA 4: uyku alakasiz
d4 = df.dropna(subset=['uyku', 'gpa'])
m4 = smf.ols('gpa ~ uyku', data=d4).fit()
m4q = smf.ols('gpa ~ uyku + I(uyku**2)', data=d4).fit()
# esdegerlik (TOST): etki |r| < 0.1 araliginda mi?
r4 = stats.pearsonr(d4.uyku, d4.gpa)[0]; z = np.arctanh(r4); se = 1/np.sqrt(len(d4)-3)
tost_p = max(stats.norm.sf((z - np.arctanh(-0.1))/se), stats.norm.cdf((z - np.arctanh(0.1))/se))
ub = pd.cut(d4.uyku, [0, 6, 7, 8, 24], labels=['<=6', '6-7', '7-8', '>8'])
R['iddia4_uyku'] = {
    'korelasyon': corr_block('uyku', 'gpa'),
    'basit_regresyon': coef_block(m4, 'uyku', 'gpa ~ 1', d4),
    'kontrollu_regresyon': coef_block(mfull, 'uyku', 'gpa ~ calisma + sosyal + kiz + ozel', cc),
    'karesel_terim_p': m4q.pvalues['I(uyku ** 2)'],
    'TOST_esdegerlik_|r|<0.1_p': float(tost_p),
    'uyku_grubu_ortalamalari': d4.groupby(ub, observed=True).gpa.agg(['count', 'mean']).round(2).reset_index().astype({'uyku': str}).to_dict('records'),
}

# Holm duzeltmesi (bivariate p'ler, 4 iddia)
ps = {'iddia1': R['iddia1_calisma']['korelasyon']['p'], 'iddia2': R['iddia2_sosyal_medya']['korelasyon']['p'],
      'iddia3': p_welch, 'iddia4': R['iddia4_uyku']['korelasyon']['p']}
order = sorted(ps, key=ps.get); adj = {}; prev = 0
for i, kk in enumerate(order):
    prev = max(prev, min(1, ps[kk] * (len(ps) - i))); adj[kk] = prev
R['holm_duzeltilmis_p'] = adj

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    return o
json.dump(clean(R), open(f'{OUT}/sonuclar.json', 'w'), ensure_ascii=False, indent=2)
print(mfull.summary())
print(json.dumps(clean(R), ensure_ascii=False, indent=1))
