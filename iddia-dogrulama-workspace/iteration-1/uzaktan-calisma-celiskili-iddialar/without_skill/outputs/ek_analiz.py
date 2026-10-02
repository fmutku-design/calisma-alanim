"""Ek saglamlik kontrolleri: kidemin dogrusal olmamasi, gun kategorileri, kidem bantlari."""
import json, os, statistics as st
import importlib.util
spec = importlib.util.spec_from_file_location("a", os.path.join(os.path.dirname(os.path.abspath(__file__)), "analiz.py"))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
rows, deps, ols, f_test, pearson = a.rows, a.deps, a.ols, a.f_test, a.pearson
dd = [d for d in deps if d != deps[0]]
v = [r["v"] for r in rows]
def X(r, uz=1, uz2=0, k2=0, k3=0, daycat=0, kidem=1):
    x = [1.0]
    if uz: x.append(r["uz"])
    if uz2: x.append(r["uz"] ** 2)
    if kidem: x.append(r["kidem_yil"])
    if k2: x.append(r["kidem_yil"] ** 2)
    if k3: x.append(r["kidem_yil"] ** 3)
    if daycat: x += [1.0 if r["uz"] == g else 0.0 for g in range(1, 6)]
    x += [1.0 if r["departman"] == d else 0.0 for d in dd]
    return x
def N(uz=1, uz2=0, k2=0, k3=0, daycat=0, kidem=1):
    n = ["sabit"] + (["uz"] if uz else []) + (["uz2"] if uz2 else []) + (["kidem"] if kidem else []) + (["kidem2"] if k2 else []) + (["kidem3"] if k3 else [])
    n += [f"gun_{g}" for g in range(1, 6)] if daycat else []
    return n + [f"dep_{d}" for d in dd]
def fit(**kw): return ols([X(r, **kw) for r in rows], v, N(**kw))
E = {}
m_k = fit(); m_k2 = fit(k2=1); m_k2_uz2 = fit(k2=1, uz2=1); m_k3_uz2 = fit(k2=1, k3=1, uz2=1)
m0_k2 = fit(uz=0, k2=1)
E["kidem_kare_testi_(uz dogrusal)"] = f_test(m_k2, m_k)
E["kidem_kare_modelinde_uz_egimi"] = m_k2["coef"]["uz"]; E["kidem_kare_modelinde_R2"] = m_k2["r2"]
E["kidem_kare_modelinde_uz2_testi"] = f_test(m_k2_uz2, m_k2)
E["kidem_kare_modelinde_uz2_katsayilari"] = {k: m_k2_uz2["coef"][k] for k in ("uz", "uz2", "kidem", "kidem2")}
E["kidem_kup_modelinde_uz2_katsayilari"] = {k: m_k3_uz2["coef"][k] for k in ("uz", "uz2")}
E["kidem_kare_modelinde_uzaktanin_toplam_katkisi_(uz+uz2)"] = f_test(m_k2_uz2, m0_k2)
# gun kategorileri (0 gun referans), kidem + kidem^2 + departman kontrollu
m_cat = fit(uz=0, daycat=1, k2=1); m_cat_lin = fit(uz=0, daycat=1)
E["gun_kategorileri_kidem2_kontrollu"] = {k: m_cat["coef"][k] for k in m_cat["coef"] if k.startswith("gun_")}
E["gun_kategorileri_kidem_dogrusal_kontrollu"] = {k: m_cat_lin["coef"][k] for k in m_cat_lin["coef"] if k.startswith("gun_")}
E["gun_kategorileri_ortak_test_(kidem2)"] = f_test(m_cat, m0_k2)
# kidem bantlari icinde ham korelasyon
bands = [(0, 3), (3, 6), (6, 9), (9, 100)]
E["kidem_bantlari"] = {}
for lo, hi in bands:
    s = [r for r in rows if lo <= r["kidem_yil"] < hi]
    E["kidem_bantlari"][f"{lo}-{hi if hi<100 else '+'}"] = {"n": len(s), "ort_uz": st.mean(r["uz"] for r in s), "ort_v": st.mean(r["v"] for r in s),
        "pearson": pearson([r["uz"] for r in s], [r["v"] for r in s]) if len(s) > 4 else None}
# kidem ~ uzaktan gun ortalama tablosu
E["uzaktan_gune_gore_ort_kidem"] = {g: st.mean(r["kidem_yil"] for r in rows if r["uz"] == g) for g in range(6)}
# kismi korelasyon (kidem sabitken uz-v)
def resid(y, xs):
    m = ols([[1] + [x[i] for x in xs] for i in range(len(y))], y, ["c"] + [f"x{j}" for j in range(len(xs))])
    b = [m["coef"][k]["b"] for k in m["coef"]]
    return [y[i] - b[0] - sum(b[j + 1] * xs[j][i] for j in range(len(xs))) for i in range(len(y))]
kd = [r["kidem_yil"] for r in rows]; uz = [r["uz"] for r in rows]
E["kismi_korelasyon_uz_v_|kidem"] = pearson(resid(uz, [kd]), resid(v, [kd]))
json.dump(E, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ek_sonuclar.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2, default=str)
print(json.dumps(E, indent=1, ensure_ascii=False, default=lambda o: round(o, 3)))
