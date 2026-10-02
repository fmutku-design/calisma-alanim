"""Tanımlayıcı kontrol: uzaktan gün başına ortalama verimlilik ve kıdem; kıdem üçte-birlik dilimlerinde korelasyon.
Puanlamaya girmez (aynı veri kümesi; çift sayım olur) — yalnızca karıştırıcılığı göstermek için."""
import csv, math, statistics as st, json, os, sys
CSV = sys.argv[1] if len(sys.argv) > 1 else "/home/user/calisma-alanim/iddia-dogrulama-workspace/inputs/calisan_verimlilik.csv"
R = list(csv.DictReader(open(CSV)))
f = lambda r, k: float(r[k])
def corr(a, b):
    ma, mb = st.mean(a), st.mean(b)
    return sum((x-ma)*(y-mb) for x, y in zip(a, b)) / math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))
u = [f(r, "haftalik_uzaktan_gun") for r in R]; k = [f(r, "kidem_yil") for r in R]; v = [f(r, "verimlilik_puani") for r in R]
out = {"r_uzaktan_verim": round(corr(u, v), 3), "r_kidem_uzaktan": round(corr(k, u), 3), "r_kidem_verim": round(corr(k, v), 3),
       "uzaktan_gune_gore": [], "kidem_dilimleri": []}
for d in range(6):
    s = [r for r in R if int(r["haftalik_uzaktan_gun"]) == d]
    out["uzaktan_gune_gore"].append({"gun": d, "n": len(s), "ort_verim": round(st.mean(f(r, "verimlilik_puani") for r in s), 1),
                                     "ort_kidem": round(st.mean(f(r, "kidem_yil") for r in s), 1)})
srt = sorted(R, key=lambda r: f(r, "kidem_yil")); m = len(srt) // 3
for i in range(3):
    s = srt[i*m:(i+1)*m] if i < 2 else srt[2*m:]
    out["kidem_dilimleri"].append({"kidem": f"{s[0]['kidem_yil']}–{s[-1]['kidem_yil']}", "n": len(s),
        "r_uzaktan_verim": round(corr([f(r, "haftalik_uzaktan_gun") for r in s], [f(r, "verimlilik_puani") for r in s]), 3)})
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kidem_tabakali.json"), "w"), ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=1))
