"""C1, C2, C6 birbirini dışlayan ve birlikte tüketen üç hipotezdir (kıdem+departman sabitken
etki negatif / pozitif / sıfır). score_claims.py her iddiayı ayrı güncellediği için P'lerin toplamı
1 olmak zorunda değildir. Bu betik göreli payları (P_i / ΣP) hesaplar — sezgisel bir özet, resmi P değil."""
import json, sys, os
here = os.path.dirname(os.path.abspath(__file__))
out = {}
for name, path in [("ana_analiz", os.path.join(here, "..", "metadata.json")),
                   ("yalnizca_kullanici_kaynaklari", os.path.join(here, "yalnizca_kullanici_kaynaklari", "metadata.json"))]:
    m = json.load(open(path))
    P = {c["id"]: c["scores"]["posterior_P"] for c in m["claims"]}
    rng = {c["id"]: [c["sensitivity"]["P_min"], c["sensitivity"]["P_max"]] for c in m["claims"]}
    for grp, ids in (("nedensel_kontrollu", ["C1", "C2", "C6"]), ("iliskisel_ham", ["C4", "C5", "C3"])):
        tot = sum(P[i] for i in ids)
        out.setdefault(name, {})[grp] = {"P": {i: P[i] for i in ids}, "toplam_P": round(tot, 3),
            "goreli_pay": {i: round(P[i] / tot, 3) for i in ids}, "P_araligi": {i: rng[i] for i in ids}}
json.dump(out, open(os.path.join(here, "tutarlilik_normalizasyonu.json"), "w"), ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=1))
