#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
atif_coz.py (v1.0) - Codex oturumlarindaki U+E200 / U+E202 / U+E201 "alfabesini" cozer.
Salt-okunur. Kaynak kod sadece ASCII.

Kullanim (PowerShell):
  python -X utf8 atif_coz.py                      # varsayilan: %USERPROFILE%\.codex\sessions
  python -X utf8 atif_coz.py "C:\baska\klasor" --ornek 10

Bicim (OpenAI atif isaretlemesi):
  U+E200 = ac   U+E202 = alan ayirici   U+E201 = kapat
  U+E200 cite U+E202 turn1view3 U+E201   ->   [[cite | turn1view3]]
  turn1 = oturumdaki 2. web cagrisi (0'dan sayar), view3 = o cagrida acilan 4. sayfa,
  search0 = o cagridaki 1. arama sonucu.

Her dosya icin: isaret sayisi, aileler (cite ...), kimlik kaliplari (turnNsearchN ...),
isaretin gectigi kayit turu (arac ciktisi / asistan mesaji), web aracinin kac kez
cagrildigi ve bu kaliba UYMAYAN ozel-kullanim (PUA, U+E000-U+F8FF) karakterleri.
Uymayan varsa "!! KALIP DISI" satiriyla baglamiyla basilir.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

PUA = re.compile("[\uE000-\uF8FF]")
ESC = re.compile(r"\\u(?:e[0-9a-f]{3}|f[0-8][0-9a-f]{2})", re.I)
MARK = re.compile("\uE200([^\uE000-\uF8FF]{1,40})((?:\uE202[^\uE000-\uF8FF]{0,400})+)\uE201")
WEB_HINTS = ("web__run", "web_search", "web.run")
MAX_ODD = 200


def walk(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)
    elif isinstance(o, str):
        yield o


def payload(o):
    return o.get("payload") if isinstance(o, dict) and isinstance(o.get("payload"), dict) else {}


def label(o):
    if not isinstance(o, dict):
        return "(json degil)"
    pl = payload(o)
    parts = [o.get("type"), pl.get("type"), pl.get("role") or o.get("role")]
    return "/".join(str(x) for x in parts if x) or "(?)"


def is_web_call(o):
    pl = payload(o)
    t = str(pl.get("type", ""))
    if t == "web_search_call":
        return True
    if not t.endswith("_call"):
        return False
    blob = "%s %s %s" % (pl.get("name", ""), pl.get("input", ""), pl.get("arguments", ""))
    return any(h in blob for h in WEB_HINTS)


def visible(s):
    s = s.replace("\uE200", "[[").replace("\uE202", " | ").replace("\uE201", "]]")
    return PUA.sub(lambda m: "<U+%04X>" % ord(m.group(0)), s)


def scan(fp):
    text = fp.read_bytes().decode("utf-8", "replace")
    st = {"marks": 0, "fam": Counter(), "shape": Counter(), "where": Counter(),
          "examples": [], "odd": [], "odd_n": 0, "web": 0}
    for no, line in enumerate(text.split("\n"), 1):
        has_web = any(h in line for h in WEB_HINTS)
        has_pua = bool(PUA.search(line) or ESC.search(line))
        if not (has_web or has_pua):
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            obj = None
        if has_web and obj is not None and is_web_call(obj):
            st["web"] += 1
        if not has_pua:
            continue
        for s in (walk(obj) if obj is not None else [line]):
            if not PUA.search(s):
                continue
            covered = set()
            for m in MARK.finditer(s):
                st["marks"] += 1
                st["fam"][m.group(1)] += 1
                st["where"][label(obj)] += 1
                for f in m.group(2).split("\uE202")[1:]:
                    st["shape"][re.sub(r"\d+", "N", f)[:40]] += 1
                if len(st["examples"]) < 50:
                    st["examples"].append(visible(m.group(0)))
                covered.update(range(m.start(), m.end()))
            for m in PUA.finditer(s):
                if m.start() in covered:
                    continue
                st["odd_n"] += 1
                if len(st["odd"]) < MAX_ODD:
                    ctx = visible(s[max(0, m.start() - 60):m.start() + 60])
                    st["odd"].append((no, label(obj), ctx))
    return st


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Codex atif isaretlerini cozer (salt-okunur)")
    ap.add_argument("hedef", nargs="?", default=str(Path.home() / ".codex" / "sessions"))
    ap.add_argument("--ornek", type=int, default=5, help="dosya basina gosterilecek ornek isaret")
    a = ap.parse_args()
    root = Path(a.hedef)
    if not root.exists():
        print("Bulunamadi:", root)
        return 2
    files = [root] if root.is_file() else sorted(root.rglob("*.jsonl"))

    tot, fam, shape, where = Counter(), Counter(), Counter(), Counter()
    for fp in files:
        try:
            st = scan(fp)
        except OSError as e:
            print("OKUNAMADI:", fp, e)
            continue
        tot[("isaretli" if st["marks"] else "isaretsiz") + ("+web" if st["web"] else "+webyok")] += 1
        tot["odd"] += st["odd_n"]
        if not st["marks"] and not st["odd_n"]:
            continue
        fam.update(st["fam"])
        shape.update(st["shape"])
        where.update(st["where"])
        print("=" * 72)
        print("DOSYA:", fp)
        print("  isaret: %d | web cagrisi: %d | kalip disi PUA: %d" % (st["marks"], st["web"], st["odd_n"]))
        print("  aileler          :", dict(st["fam"]))
        print("  kimlik kaliplari :", dict(st["shape"].most_common(8)))
        print("  gectigi kayitlar :", dict(st["where"].most_common(6)))
        for e in st["examples"][:a.ornek]:
            print("     ", e)
        for no, lab, ctx in st["odd"][:10]:
            print("  !! KALIP DISI satir %d (%s): %s" % (no, lab, ctx))

    print("=" * 72)
    print("Taranan .jsonl                  :", len(files))
    print("  isaretli  + web cagrisi var   :", tot["isaretli+web"])
    print("  isaretli  + web cagrisi YOK   :", tot["isaretli+webyok"])
    print("  isaretsiz + web cagrisi var   :", tot["isaretsiz+web"])
    print("  isaretsiz + web cagrisi YOK   :", tot["isaretsiz+webyok"])
    print("Toplam isaret:", sum(fam.values()), "| aileler:", dict(fam))
    print("Kimlik kaliplari:", dict(shape.most_common(10)))
    print("Gectigi kayit turleri:", dict(where.most_common(8)))
    print("KALIP DISI PUA toplam:", tot["odd"], "(0 degilse yukaridaki !! satirlarina bak)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
