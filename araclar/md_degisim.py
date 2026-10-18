#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
md_degisim.py (v1.0) - Proje belgelerinin (.md ve .txt) degisip degismedigini gosterir.
Salt-okunur: hicbir dosyaya yazmaz. Kaynak kod sadece ASCII.

Her belgeyi uc ya da dort ana gore SHA-256 ile karsilastirir:
  ONCE    : 15.10 ortam onarimindan onceki kopya   (ortam_onarimi_2026-10-15\once)
  ONARIM  : onarimin projeye kurdugu kopya          (ortam_onarimi_2026-10-15\aday)
  TARAMA  : gizli karakter taramandaki SHA-256      (tarama_raporu.json, varsa)
  SIMDI   : projedeki dosya
Ayrica onarimin ozgun_kaynaklar klasorundeki kopyalari Downloads'taki ayni adli dosyalarla karsilastirir.

Kullanim (PowerShell, Downloads'tan):
  python -X utf8 md_degisim.py
  python -X utf8 md_degisim.py --fark "plan\fikrin_ozu.md"     # bir belgenin satir farki
  python -X utf8 md_degisim.py --hepsi                          # onarimdan sonra eklenen .txt'ler de

Varsayilanlar: proje ~\Desktop\mikroskop ai ... klasoru, onarim klasoru
~\Documents\Codex\2026-10-15\ana-mikroskop-ai-projesi-nin-i\ortam_onarimi_2026-10-15,
tarama ~\Downloads\tarama_raporu.json. Hepsi --kok, --onarim, --tarama ile degistirilebilir.
"""
import argparse
import difflib
import hashlib
import json
import os
import sys
from pathlib import Path

HOME = Path.home()
ROOT = HOME / "Desktop" / "mikroskop ai \u00e7al\u0131\u015fma klas\u00f6r\u00fc"
REPAIR = HOME / "Documents" / "Codex" / "2026-10-15" / "ana-mikroskop-ai-projesi-nin-i" / "ortam_onarimi_2026-10-15"
SCAN = HOME / "Downloads" / "tarama_raporu.json"
EXTS = (".md", ".txt")
MARK = "kullan\u0131c\u0131 onay\u0131yla)"      # talimat_duzelt.py'nin surum notu
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def tree(base):
    """{goreli yol (kucuk harf, \\ ile): (gorunen yol, SHA-256, tam yol)}"""
    out = {}
    if not base.is_dir():
        return out
    for dirpath, dirnames, files in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in files:
            if name.lower().endswith(EXTS):
                p = Path(dirpath) / name
                rel = str(p.relative_to(base)).replace("/", "\\")
                try:
                    out[rel.lower()] = (rel, sha(p), p)
                except OSError:
                    pass
    return out


def scan_hashes(path, root):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    fs = data.get("file_sha256") if isinstance(data, dict) else None
    if not isinstance(fs, dict):
        return None
    pre = str(root).replace("/", "\\").rstrip("\\").lower() + "\\"
    out = {}
    for k, v in fs.items():
        kk = str(k).replace("/", "\\")
        if kk.lower().startswith(pre) and kk.lower().endswith(EXTS):
            rel = kk[len(pre):]
            out[rel.lower()] = (rel, str(v).lower(), None)
    return out


def short(h):
    return h[:8] if h else "-"


def verdict(o, a, t, s, marked):
    """o: onarim oncesi, a: onarim, t: tarama, s: simdi (SHA-256 ya da None)."""
    if s is None:
        return "SILINMIS / TASINMIS (projede yok)"
    parts = []
    if o is None and a is not None:
        parts.append("onarimda eklendi")
    elif o is not None and a is not None and o != a:
        parts.append("onarimda degisti")
    if a is not None and s == a and o == a:
        return "hic degismedi"
    if a is not None and s == a:
        parts.append("sonra degismedi")
    elif o is not None and s == o:
        parts.append("simdi onarim oncesi haline dondu")
    elif a is not None:
        parts.append("onarimdan sonra degisti")
        if t is not None:
            parts.append("taramadan once" if t != a else "taramadan sonra")
        if marked:
            parts.append("talimat_duzelt surum notu var")
    if not parts:
        parts.append("degismedi")
    return "; ".join(parts)


def show_diff(rel, sources):
    print("=" * 78)
    print("FARK: " + rel)
    cur = sources.get("SIMDI")
    for name in ("ONCE", "ONARIM"):
        old = sources.get(name)
        print("-" * 78)
        if old is None or cur is None:
            print("%s -> SIMDI: karsilastirilamaz (%s yok)" % (name, name if old is None else "SIMDI"))
            continue
        a = old.read_bytes().decode("utf-8-sig", "replace").replace("\r\n", "\n").split("\n")
        b = cur.read_bytes().decode("utf-8-sig", "replace").replace("\r\n", "\n").split("\n")
        print("%s -> SIMDI (%s -> %s)" % (name, short(sha(old)), short(sha(cur))))
        lines = list(difflib.unified_diff(a, b, name, "SIMDI", lineterm="", n=0))
        if not lines:
            print("  metin ayni" + ("" if old.read_bytes() == cur.read_bytes() else " (fark yalniz BOM/satir sonunda)"))
        for x in lines:
            print("  " + x)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Belge degisim tablosu (salt-okunur)")
    ap.add_argument("--kok", default=str(ROOT))
    ap.add_argument("--onarim", default=str(REPAIR))
    ap.add_argument("--tarama", default=str(SCAN))
    ap.add_argument("--fark", metavar="GORELI_YOL")
    ap.add_argument("--hepsi", action="store_true")
    a = ap.parse_args()
    root, rep = Path(a.kok), Path(a.onarim)
    if not root.is_dir():
        print("Proje klasoru yok:", root)
        return 2
    once, aday, now = tree(rep / "once"), tree(rep / "aday"), tree(root)
    scan = scan_hashes(a.tarama, root)
    print("Proje   :", root)
    print("Onarim  :", rep, "" if (rep / "aday").is_dir() else "(YOK: ONCE/ONARIM sutunlari bos kalir)")
    print("Tarama  :", a.tarama if scan is not None else "(yok ya da okunamadi; TARAMA sutunu bos)")
    if a.fark:
        key = a.fark.replace("/", "\\").lower()
        show_diff(a.fark, {"ONCE": once.get(key, (0, 0, None))[2], "ONARIM": aday.get(key, (0, 0, None))[2],
                           "SIMDI": now.get(key, (0, 0, None))[2]})
        return 0
    scan = scan or {}
    keys = sorted(set(once) | set(aday))
    print("=" * 78)
    print("1) ONARIMDA VAR OLAN BELGELER  (SHA-256 ilk 8 hane: ONCE > ONARIM > TARAMA > SIMDI)")
    groups = {}
    for k in keys:
        rel = (now.get(k) or aday.get(k) or once.get(k))[0]
        o, d = (once.get(k) or (0, None))[1], (aday.get(k) or (0, None))[1]
        t, s = (scan.get(k) or (0, None))[1], (now.get(k) or (0, None))[1]
        marked = False
        if s is not None:
            try:
                marked = MARK in now[k][2].read_text(encoding="utf-8-sig", errors="replace")
            except OSError:
                pass
        groups.setdefault(verdict(o, d, t, s, marked), []).append(
            (rel, " > ".join(short(x) for x in (o, d, t, s))))

    def rank(v):
        return next((i for i, w in enumerate(("SILINMIS", "onarimdan sonra", "oncesi haline", "onarimda degisti",
                                                "onarimda eklendi")) if w in v), 9)
    for v in sorted(groups, key=rank):
        rows = groups[v]
        if v == "hic degismedi" and not a.hepsi:
            shown = [r for r in rows if not r[0].lower().startswith("ai ar\u015fivi")]
            print("  [%s] %d belge (ai arsivi'ndekiler sayildi; adlari --hepsi ile)" % (v, len(rows)))
            rows = shown
        else:
            print("  [%s]" % v)
        for rel, chain in rows:
            print("     %-58s %s" % (rel, chain))
    later = sorted(k for k in set(now) | set(scan) if k not in once and k not in aday)
    print("=" * 78)
    print("2) ONARIMDAN SONRA EKLENEN BELGELER  (TARAMA / SIMDI)")
    hidden = 0
    for k in later:
        rel = (now.get(k) or scan.get(k))[0]
        t, s = (scan.get(k) or (0, None))[1], (now.get(k) or (0, None))[1]
        if s is None:
            note = "TARAMADAN SONRA SILINMIS / TASINMIS"
        elif not scan:
            note = ""
        elif t is None:
            note = "taramadan sonra eklendi"
        elif t != s:
            note = "taramadan sonra degisti"
        else:
            note = "taramadan sonra degismedi"
        if not (a.hepsi or rel.lower().endswith(".md") or s is None
                or note in ("taramadan sonra degisti", "taramadan sonra eklendi")):
            hidden += 1
            continue
        print("  %-8s %-8s  %s  %s" % (short(t), short(s), rel, ("-> " + note) if note else ""))
    if hidden:
        print("  (taramadan beri degismeyen %d .txt gosterilmedi; --hepsi)" % hidden)
    src = rep / "ozgun_kaynaklar"
    if src.is_dir():
        print("=" * 78)
        print("3) OZGUN KAYNAKLAR: onarimin 15.10'da aldigi kopya / Downloads'taki dosya")
        for p in sorted(x for x in src.iterdir() if x.is_file()):
            d = HOME / "Downloads" / p.name
            o, s = sha(p), (sha(d) if d.is_file() else None)
            note = "Downloads'ta yok" if s is None else ("15.10'dan beri degismedi" if s == o else "15.10'DAN SONRA DEGISMIS")
            print("  %-8s %-8s  %s  -> %s" % (short(o), short(s), p.name, note))
    print("=" * 78)
    print("Bir belgenin satir farki icin: python -X utf8 md_degisim.py --fark \"GORELI\\YOL\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
