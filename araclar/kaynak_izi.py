#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
kaynak_izi.py (v1.0) - Yapay zeka ciktisindaki gorunmez karakterlerin KAYNAGINI arar.
Salt-okunur. Kaynak kod sadece ASCII.

Soru: model, kendi girdisinde (kullanici mesaji, arac ciktisi, okunan dosya) hic
gormedigi bir gorunmez karakteri kendisi uretiyor mu?

Kullanim (PowerShell):
  python -X utf8 kaynak_izi.py "C:\Users\UTKU\Downloads\claude-un-gizli-karakter-iddias-do-rulama.json"
  python -X utf8 kaynak_izi.py "C:\Users\UTKU\.codex\sessions"
  python -X utf8 kaynak_izi.py "C:\Users\UTKU\Documents\Codex\2026-09-30\cl\outputs\Claude-korunan"

Okudugu bicimler: OpenCode disa aktarimi (.json), Codex rollout (.jsonl),
Claude Code / Claude masaustu oturumu ve audit.jsonl (.jsonl). Digerleri icin
"type"/"role" alanina bakan genel bir tahmin kullanir.

Model ciktisi = asistan mesaji, dusunme (reasoning/thinking), arac cagrisi girdisi.
Girdi        = kullanici mesaji, arac ciktisi, sistem/oturum kayitlari.
Her model ciktisindaki gorunmez karakter, dosyadaki sirayla, ondan ONCE gelen
iceriklerle karsilastirilir ve dort siniftan birine konur:
  KOPYA       : ayni karakter, solunda ya da saginda ayni 3 karakterle daha once girdide var
  AYNI_KAR    : ayni karakter daha once girdide var, baglam farkli (or. karakterden bahsederken)
  OZ_KOPYA    : karakter sadece modelin kendi onceki ciktisinda var (zincir kaynaksiz bir cikista baslar)
  KAYNAKSIZ   : karakter oturumda daha once HIC gecmemis -> asil incelenecek durum
KAYNAKSIZ her zaman gizli mesaj demek degildir (or. model Farsca yazarken U+200C,
Arapca yazarken U+200F kullanir); baglam satiri bunu ayirt etmek icin basilir.
Not: sistem istemi ve arac tanimlari kayitlarda yoksa onlar kaynak olarak gorulmez.
"""
import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

HID = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff"
                 "\ufe00-\ufe0f\U000e0000-\U000e007f\U000e0100-\U000e01ef]")
ESC = re.compile(r"\\u(?:200[b-f]|202[a-e]|206[0-4]|206[6-9]|feff|fe0[0-9a-f]|db40)", re.I)
STRIP = re.compile(r"[\\\"'`]")
WS = re.compile(r"\s+")
W = 3
CLASSES = ("KOPYA", "AYNI_KAR", "OZ_KOPYA", "KAYNAKSIZ")


def norm(s):
    return WS.sub(" ", STRIP.sub("", s))


def u(c):
    return "U+%04X" % ord(c)


def sides(n, m):
    """Karakterin sol ve sag yakin baglami (W karakter); biri tutarsa birebir kopya sayilir."""
    return ("L" + n[max(0, m.start() - W):m.end()], "R" + n[m.start():m.end() + W])


def visible(s):
    return HID.sub(lambda m: "<%s>" % u(m.group(0)), s).replace("\r", "\\r").replace("\n", "\\n")


def emoji_ok(s, i):
    """ZWJ/VS15/VS16 bir sembolden sonra geliyorsa emoji parcasidir, sayilmaz."""
    if ord(s[i]) not in (0x200D, 0xFE0E, 0xFE0F) or i == 0:
        return False
    p = s[i - 1]
    return unicodedata.category(p).startswith("S") or p in "#*0123456789" or ord(p) in (0x200D, 0xFE0F)


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


# --- bicim cozuculer: (yon, etiket, nesne) uretir; yon = "cikti" | "girdi" | None
def is_opencode(d):
    return isinstance(d, dict) and isinstance(d.get("info"), dict) and isinstance(d.get("messages"), list)


def events_opencode(d):
    for i, m in enumerate(d["messages"]):
        if not isinstance(m, dict):
            continue
        role = m["info"].get("role") if isinstance(m.get("info"), dict) else None
        for p in m.get("parts") or []:
            if not isinstance(p, dict):
                continue
            t = p.get("type")
            lab = "msg%d/%s/%s" % (i, role, t)
            if role != "assistant":
                yield "girdi", lab, p
            elif t in ("text", "reasoning"):
                yield "cikti", lab, p.get("text", "")
            elif t == "tool":
                st = p.get("state") or {}
                yield "cikti", lab + "/cagri", st.get("input")
                yield "girdi", lab + "/sonuc", {k: v for k, v in st.items() if k != "input"}


def events_line(o, no):
    if not isinstance(o, dict):
        return
    if "payload" in o and o.get("type") in ("response_item", "event_msg", "session_meta",
                                            "turn_context", "compacted"):
        pl = o.get("payload") or {}
        pt = str(pl.get("type", ""))
        lab = "satir%d/%s/%s" % (no, o.get("type"), pt)
        if o["type"] == "response_item":
            if pt == "message":
                yield ("cikti" if pl.get("role") == "assistant" else "girdi"), lab + "/" + str(pl.get("role")), pl
            elif pt == "reasoning" or pt.endswith("_call"):
                yield "cikti", lab, pl
            else:
                yield "girdi", lab, pl
        elif o["type"] == "event_msg":
            it = pl.get("item") if isinstance(pl.get("item"), dict) else {}
            tag = (pt + " " + str(it.get("type", ""))).lower()
            if "agent" in tag or "reasoning" in tag or "assistant" in tag:
                return  # asistan ciktisinin arayuz kopyasi; kaynak sayilmasin
            yield "girdi", lab, pl
        else:
            yield "girdi", lab, pl
        return
    msg = o.get("message")
    if o.get("type") in ("assistant", "user") and isinstance(msg, dict):
        lab = "satir%d/%s" % (no, o["type"])
        content = msg.get("content")
        if o["type"] == "user":
            yield "girdi", lab, o
        elif isinstance(content, list):
            for b in content:
                if isinstance(b, dict) and b.get("type") in ("text", "thinking", "tool_use"):
                    yield "cikti", lab + "/" + b["type"], b.get("text") or b.get("thinking") or b.get("input")
        else:
            yield "cikti", lab, content
        return
    kind = str(o.get("role") or o.get("type") or "")
    out = re.search(r"assistant|planner|response|model", kind, re.I)
    yield ("cikti" if out else "girdi"), "satir%d/%s" % (no, kind or "?"), o


def iter_events(fp):
    raw = fp.read_bytes().decode("utf-8-sig", "replace")
    if fp.suffix.lower() == ".json":
        try:
            d = json.loads(raw)
        except ValueError:
            return
        if is_opencode(d):
            yield from events_opencode(d)
        else:
            yield "girdi", "json", d
        return
    for no, line in enumerate(raw.split("\n"), 1):
        if not (HID.search(line) or ESC.search(line)):
            continue  # gizli karakter yok: kaynak ya da cikti olarak bir sey eklemez
        try:
            o = json.loads(line)
        except ValueError:
            yield "girdi", "satir%d/(json degil)" % no, line
            continue
        yield from events_line(o, no)


def check(fp):
    seen_in, seen_out, ctx_in = set(), set(), set()
    res = Counter()
    first_in, flagged = None, []
    for way, lab, obj in iter_events(fp):
        if way is None:
            continue
        for s in strings(obj):
            if not HID.search(s):
                continue
            n = norm(s)
            # norm() gorunmez karakterlere dokunmaz: n'deki i. eslesme s'deki i. eslesmedir
            hits = [(a, b) for a, b in zip(HID.finditer(n), HID.finditer(s)) if not emoji_ok(n, a.start())]
            if way == "girdi":
                for a, _ in hits:
                    seen_in.add(a.group(0))
                    ctx_in.update(sides(n, a))
                if hits and first_in is None:
                    b = hits[0][1]
                    first_in = (lab, visible(s[max(0, b.start() - 50):b.end() + 50]))
                continue
            for a, b in hits:
                c = a.group(0)
                if any(x in ctx_in for x in sides(n, a)):
                    k = "KOPYA"
                elif c in seen_in:
                    k = "AYNI_KAR"
                elif c in seen_out:
                    k = "OZ_KOPYA"
                else:
                    k = "KAYNAKSIZ"
                res[k] += 1
                res[u(c)] += 1
                if k in ("KAYNAKSIZ", "OZ_KOPYA") and len(flagged) < 20:
                    flagged.append((k, lab, visible(s[max(0, b.start() - 60):b.end() + 60])))
            seen_out.update(a.group(0) for a, _ in hits)
    return res, first_in, flagged


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Gorunmez karakter kaynak izi (salt-okunur)")
    ap.add_argument("hedef", nargs="+")
    a = ap.parse_args()
    files = []
    for h in a.hedef:
        p = Path(h)
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files += sorted(x for x in p.rglob("*") if x.suffix.lower() in (".jsonl", ".json"))
        else:
            print("Bulunamadi:", p)
    tot = Counter()
    for fp in files:
        try:
            res, first_in, flagged = check(fp)
        except Exception as e:  # tek bir garip dosya taramayi durdurmasin
            print("ATLANDI: %s (%s: %s)" % (fp, type(e).__name__, e))
            tot["atlanan"] += 1
            continue
        n_out = sum(res[k] for k in CLASSES)
        tot.update(res)
        tot["dosya"] += 1
        if not n_out:
            continue
        tot["ciktisinda_gizli_olan_dosya"] += 1
        print("=" * 72)
        print("DOSYA:", fp)
        print("  model ciktisindaki gorunmez karakter: %d | %s" % (
            n_out, " | ".join("%s=%d" % (k, res[k]) for k in CLASSES)))
        print("  kod noktalari:", {k: v for k, v in res.items() if k.startswith("U+")})
        if first_in:
            print("  girdiye ilk giris: %s ...%s..." % first_in)
        else:
            print("  girdiye ilk giris: YOK (bu kayittaki hicbir girdide gorunmez karakter yok)")
        for k, lab, ctx in flagged:
            print("  !! %s %s: ...%s..." % (k, lab, ctx))
    print("=" * 72)
    print("Taranan dosya:", tot["dosya"], "| model ciktisinda gorunmez karakter olan:",
          tot["ciktisinda_gizli_olan_dosya"], "| atlanan:", tot["atlanan"])
    print("Toplam:", " | ".join("%s=%d" % (k, tot[k]) for k in CLASSES))
    print("KAYNAKSIZ 0 ise: modellerin yazdigi her gorunmez karakter, o oturumda once girdide vardi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
