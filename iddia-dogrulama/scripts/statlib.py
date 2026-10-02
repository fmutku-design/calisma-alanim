"""Saf Python istatistik yardımcıları (numpy/scipy gerektirmez).

Hem data_evidence.py hem score_claims.py bu modülü kullanır; böylece
Bayes faktörü ve olasılık hesapları tek bir yerde tanımlıdır.
"""
import math

R2_MAX = 1 - 1e-12


# ---------------------------------------------------------------- dağılımlar

def _betacf(a, b, x, maxit=300, eps=3e-14, fpmin=1e-300):
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, maxit + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = fpmin if abs(d) < fpmin else d
        c = 1.0 + aa / c
        c = fpmin if abs(c) < fpmin else c
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = fpmin if abs(d) < fpmin else d
        c = 1.0 + aa / c
        c = fpmin if abs(c) < fpmin else c
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return h


def betai(a, b, x):
    """Düzenlenmiş eksik beta fonksiyonu I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                  + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1 - x) / b


def t_two_sided_p(t, df):
    if df <= 0 or math.isnan(t):
        return float("nan")
    return betai(df / 2.0, 0.5, df / (df + t * t))


# --------------------------------------------------------------- korelasyon

def mean(v):
    return sum(v) / len(v)


def pearson(xs, ys):
    mx, my = mean(xs), mean(ys)
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx == 0 or syy == 0:
        raise ValueError("Değişkenlerden biri sabit (varyans = 0); korelasyon hesaplanamaz.")
    return sxy / math.sqrt(sxx * syy)


def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(xs, ys):
    return pearson(ranks(xs), ranks(ys))


def r_to_t(r, df):
    r2 = min(r * r, R2_MAX)
    return r * math.sqrt(df / (1 - r2))


def t_to_r2(t, df):
    return t * t / (t * t + df)


def fisher_ci(r, n, z=1.959964):
    if n <= 3:
        return [float("nan"), float("nan")]
    r = max(min(r, 0.999999), -0.999999)
    zr = math.atanh(r)
    se = 1 / math.sqrt(n - 3)
    return [math.tanh(zr - z * se), math.tanh(zr + z * se)]


def d_to_r(d, n1, n2):
    a = (n1 + n2) ** 2 / (n1 * n2)
    return d / math.sqrt(d * d + a)


def effect_label_r(r):
    a = abs(r)
    if a < 0.1:
        return "önemsiz (<0.1)"
    if a < 0.3:
        return "küçük (0.1–0.3)"
    if a < 0.5:
        return "orta (0.3–0.5)"
    return "büyük (≥0.5)"


# ------------------------------------------------------------- Bayes faktörü

def log_bf10_from_r2(r2, n):
    """BIC yaklaşımıyla Bayes faktörü (Wagenmakers, 2007).

    Bir parametre eklenen iki iç içe doğrusal model için
    ΔBIC = n·ln(1 − r²) + ln(n)  ⇒  BF10 = exp(−ΔBIC / 2).
    r² burada (kısmi) belirlilik katsayısıdır. Doğal log döner.
    """
    if n < 3:
        return 0.0
    r2 = min(max(r2, 0.0), R2_MAX)
    return -(n / 2.0) * math.log(1 - r2) - 0.5 * math.log(n)


def directional_log_lr(log_bf10, sign_of_effect, relation, p_two=None):
    """Etki işareti ve iddia türüne göre iddia lehine doğal-log LR.

    relation: positive | negative | nonzero | none
    Yönlü iddialarda tek yönlü Bayes faktörü yaklaşımı kullanılır:
        BF₊₀ ≈ 2 · BF₁₀ · q,   q = P(etki iddia edilen yönde | veri) ≈ 1 − tek yönlü p
    (Morey & Wagenmakers, 2014). Etki doğru yönde ve netse BF iki katına çıkar;
    ters yönde netse q → 0 ve LR iddia aleyhine çok küçülür.
    """
    if relation == "nonzero":
        return log_bf10
    if relation == "none":
        return -log_bf10
    wanted = 1 if relation == "positive" else -1
    if p_two is None or not math.isfinite(p_two):
        p_two = 1.0 if sign_of_effect == 0 else 0.05
    if sign_of_effect == 0:
        q = 0.5
    elif sign_of_effect == wanted:
        q = 1 - p_two / 2
    else:
        q = p_two / 2
    return math.log(2) + log_bf10 + math.log(max(q, 1e-300))


# ---------------------------------------------------------------- doğrusal cebir

def mat_inv(m):
    n = len(m)
    a = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(m)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[piv][col]) < 1e-12:
            raise ValueError("Tasarım matrisi tekil (çoklu doğrusal bağlantı?).")
        a[col], a[piv] = a[piv], a[col]
        p = a[col][col]
        a[col] = [v / p for v in a[col]]
        for r in range(n):
            if r != col and a[r][col] != 0:
                f = a[r][col]
                a[r] = [vr - f * vc for vr, vc in zip(a[r], a[col])]
    return [row[n:] for row in a]


def ols(X, y):
    """X: satır listesi (sabit terim dahil). Katsayı, SE, df döner."""
    n, k = len(X), len(X[0])
    xtx = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(k)]
    inv = mat_inv(xtx)
    beta = [sum(inv[a][b] * xty[b] for b in range(k)) for a in range(k)]
    resid = [y[i] - sum(beta[a] * X[i][a] for a in range(k)) for i in range(n)]
    df = n - k
    if df <= 0:
        raise ValueError("Gözlem sayısı parametre sayısından az.")
    s2 = sum(e * e for e in resid) / df
    se = [math.sqrt(max(inv[a][a] * s2, 0.0)) for a in range(k)]
    return beta, se, df


# ---------------------------------------------------------------- olasılık

def logit(p):
    p = min(max(p, 1e-9), 1 - 1e-9)
    return math.log(p / (1 - p))


def sigmoid(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    e = math.exp(x)
    return e / (1 + e)
