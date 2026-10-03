#!/usr/bin/env python3
"""Bir veri setinde (CSV/TSV) değişken iddiasını test eder ve kanıt kaydı üretir.

Örnekler:
  # X ile Y arasında pozitif ilişki iddiası (Pearson)
  python data_evidence.py --csv veri.csv --x egitim_yili --y gelir \
      --relation positive --test pearson --claim C1 --id E1 --cluster D1

  # Kontrollü regresyon (yaş ve cinsiyet sabitken)
  python data_evidence.py --csv veri.csv --x egitim_yili --y gelir \
      --controls yas,cinsiyet --test regression --relation positive \
      --claim C1 --id E2 --cluster D1 --append-to girdi.json

  # İki grup farkı: "kadin" grubunda Y daha yüksek (ikinci grup = 'yüksek' taraf)
  python data_evidence.py --csv veri.csv --x cinsiyet --y maas \
      --test group_diff --groups erkek,kadin --relation positive --claim C2 --id E3

Yön kuralı: positive = x arttıkça (veya --groups'taki İKİNCİ grupta) y daha yüksek.
Çıktı: stdout'a JSON kanıt kaydı; --append-to ile girdi JSON'unun "evidence" listesine eklenir.
"""
import argparse
import csv
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import statlib as S  # noqa: E402

MISSING = {"", "na", "n/a", "nan", "null", "none", ".", "-", "?"}


def sniff_delimiter(sample):
    counts = {d: sample.count(d) for d in [",", ";", "\t", "|"]}
    return max(counts, key=counts.get)


def parse_num(v, decimal_comma):
    v = v.strip()
    if v.lower() in MISSING:
        return None
    try:
        return float(v.replace(",", ".") if decimal_comma else v)
    except ValueError:
        return v  # metin (kategorik) değer


def read_table(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(20000)
        f.seek(0)
        delim = sniff_delimiter(sample)
        rows = list(csv.reader(f, delimiter=delim))
    header = [h.strip() for h in rows[0]]
    # ';' ayraçlı Türkçe/Avrupa CSV'lerinde ondalık ayırıcı genelde virgüldür
    decimal_comma = delim == ";"
    data = []
    for r in rows[1:]:
        if not any(c.strip() for c in r):
            continue
        r = r + [""] * (len(header) - len(r))
        data.append({h: parse_num(c, decimal_comma) for h, c in zip(header, r)})
    return header, data


def need(header, col):
    if col not in header:
        sys.exit(f"HATA: '{col}' sütunu yok. Mevcut sütunlar: {', '.join(header)}")


def is_num(v):
    return isinstance(v, float)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--x", required=True, help="bağımsız / açıklayıcı değişken")
    ap.add_argument("--y", required=True, help="bağımlı / sonuç değişkeni")
    ap.add_argument("--relation", default=None, choices=["positive", "negative", "nonzero", "none"],
                    help="(isteğe bağlı) test edilen iddianın ilişki türü; yalnızca tutarlılık kontrolü için")
    ap.add_argument("--test", default="pearson", choices=["pearson", "spearman", "regression", "group_diff"])
    ap.add_argument("--controls", default="", help="regresyon için virgülle ayrılmış kontrol değişkenleri")
    ap.add_argument("--groups", default="", help="group_diff için 'A,B' (B = pozitif yön)")
    ap.add_argument("--claim", default=None,
                    help="iddia kimliği (örn. C1). Verilmezse kanıt aynı X–Y çiftini içeren TÜM iddialara uygulanır")
    ap.add_argument("--id", required=True, help="kanıt kimliği, örn. E1")
    ap.add_argument("--cluster", default=None, help="bağımlılık kümesi (aynı veri seti = aynı küme)")
    ap.add_argument("--experimental", action="store_true", help="veri rastgele atamalı deneyden geliyorsa")
    ap.add_argument("--note", default="", help="veri kalitesi notu")
    ap.add_argument("--append-to", default=None, help="kaydı bu girdi JSON'unun evidence listesine ekle")
    a = ap.parse_args()

    header, data = read_table(a.csv)
    controls = [c.strip() for c in a.controls.split(",") if c.strip()]
    for c in [a.x, a.y] + controls:
        need(header, c)

    cols = [a.x, a.y] + controls
    total = len(data)
    rows = [r for r in data if all(r[c] is not None for c in cols)]
    n = len(rows)
    missing_frac = 1 - n / total if total else 1.0
    if n < 5:
        sys.exit(f"HATA: eksik değerler atıldıktan sonra yalnızca {n} gözlem kaldı.")

    ys = [r[a.y] for r in rows]
    if not all(is_num(v) for v in ys):
        sys.exit(f"HATA: '{a.y}' sayısal değil; bağımlı değişken sayısal olmalı.")

    stats = {}
    if a.test == "group_diff":
        levels = sorted({str(r[a.x]) for r in rows})
        if a.groups:
            g = [s.strip() for s in a.groups.split(",")]
        elif len(levels) == 2:
            g = levels
        else:
            sys.exit(f"HATA: '{a.x}' içinde {len(levels)} düzey var ({levels[:10]}); --groups A,B verin.")
        rows = [r for r in rows if str(r[a.x]) in g]
        n = len(rows)
        ys = [r[a.y] for r in rows]
        dummy = [1.0 if str(r[a.x]) == g[1] else 0.0 for r in rows]
        g0 = [y for y, d in zip(ys, dummy) if d == 0]
        g1 = [y for y, d in zip(ys, dummy) if d == 1]
        if len(g0) < 2 or len(g1) < 2:
            sys.exit("HATA: her grupta en az 2 gözlem gerekli.")
        m0, m1 = S.mean(g0), S.mean(g1)
        v0 = sum((v - m0) ** 2 for v in g0) / (len(g0) - 1)
        v1 = sum((v - m1) ** 2 for v in g1) / (len(g1) - 1)
        sp = math.sqrt(((len(g0) - 1) * v0 + (len(g1) - 1) * v1) / (n - 2))
        r = S.pearson(dummy, ys)  # nokta-çift serili korelasyon
        df = n - 2
        t = S.r_to_t(r, df)
        r2 = r * r
        welch_se = math.sqrt(v0 / len(g0) + v1 / len(g1))
        welch_t = (m1 - m0) / welch_se if welch_se else float("nan")
        welch_df = (v0 / len(g0) + v1 / len(g1)) ** 2 / (
            (v0 / len(g0)) ** 2 / (len(g0) - 1) + (v1 / len(g1)) ** 2 / (len(g1) - 1))
        stats.update({
            "groups": {"A": g[0], "B": g[1]}, "n_A": len(g0), "n_B": len(g1),
            "mean_A": m0, "mean_B": m1, "mean_diff_B_minus_A": m1 - m0,
            "cohens_d": (m1 - m0) / sp if sp else float("nan"),
            "welch_t": welch_t, "welch_df": welch_df, "welch_p": S.t_two_sided_p(welch_t, welch_df),
            "r_point_biserial": r,
        })
        effect = m1 - m0
    else:
        xs = [r[a.x] for r in rows]
        if not all(is_num(v) for v in xs):
            sys.exit(f"HATA: '{a.x}' sayısal değil. Kategorik ise --test group_diff kullanın.")
        if a.test == "regression":
            # kategorik kontrolleri kukla değişkene çevir
            design_cols, X = [], []
            cat_levels = {}
            for c in controls:
                vals = [r[c] for r in rows]
                if not all(is_num(v) for v in vals):
                    lv = sorted({str(v) for v in vals})
                    cat_levels[c] = lv[1:]
            for r in rows:
                row = [1.0, r[a.x]]
                for c in controls:
                    if c in cat_levels:
                        row += [1.0 if str(r[c]) == lv else 0.0 for lv in cat_levels[c]]
                    else:
                        row.append(r[c])
                X.append(row)
            beta, se, df = S.ols(X, ys)
            t = beta[1] / se[1] if se[1] else float("nan")
            r2 = S.t_to_r2(t, df)
            r = math.copysign(math.sqrt(r2), t)  # kısmi korelasyon
            stats.update({"coef": beta[1], "se": se[1], "partial_r": r,
                          "controls": controls, "dummy_coded": {k: v for k, v in cat_levels.items()}})
            effect = beta[1]
        else:
            r = S.pearson(xs, ys) if a.test == "pearson" else S.spearman(xs, ys)
            df = n - 2
            t = S.r_to_t(r, df)
            r2 = r * r
            stats.update({"r": r})
            effect = r

    p = S.t_two_sided_p(t, df)
    log_bf = S.log_bf10_from_r2(r2, n)
    sign = 0 if effect == 0 else (1 if effect > 0 else -1)
    stats.update({
        "t": t, "df": df, "p_two_sided": p,
        "r_equivalent": r, "r_ci95": S.fisher_ci(r, n),
        "effect_size_label": S.effect_label_r(r),
        "effect_sign": sign,
        "log10_bf10": log_bf / math.log(10),
        "bf10": math.exp(min(log_bf, 700)),
    })
    stats = {k: (float(f"{v:.6g}") if isinstance(v, float) and math.isfinite(v) else v) for k, v in stats.items()}
    stats["r_ci95"] = [round(v, 4) for v in stats["r_ci95"]]

    rec = {
        "id": a.id,
        "kind": "data",
        "cluster": a.cluster or f"data:{os.path.basename(a.csv)}",
        "description": f"{a.test}: {a.x} → {a.y}" + (f"; kontroller: {', '.join(controls)}" if controls else ""),
        "dataset": os.path.basename(a.csv),
        "test": a.test, "x": a.x, "y": a.y, "controls": controls,
        **({"relation_tested": a.relation} if a.relation else {}),
        "n": n, "n_total_rows": total, "missing_frac": round(missing_frac, 4),
        "experimental": a.experimental,
        "data_quality_notes": a.note,
        "stats": stats,
    }

    if a.claim:
        rec["claim_id"] = a.claim
    if a.append_to:
        with open(a.append_to, encoding="utf-8") as f:
            doc = json.load(f)
        ev = [e for e in doc.get("evidence", []) if e.get("id") != a.id]
        ev.append(rec)
        doc["evidence"] = ev
        with open(a.append_to, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        print(f"'{a.id}' kaydı {a.append_to} dosyasına eklendi.", file=sys.stderr)
    print(json.dumps(rec, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
