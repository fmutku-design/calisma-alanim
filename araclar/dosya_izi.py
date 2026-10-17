#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
dosya_izi.py (v1.0) - Bir dosyayi hangi yapay zeka oturumunun, ne zaman ve hangi cagriyla
degistirdigini oturum kayitlarindan bulur. Salt-okunur: hicbir dosyaya yazmaz.
Kaynak kod sadece ASCII.

Kullanim (PowerShell; yollari Turkce harfleriyle yaz):
  python -X utf8 dosya_izi.py "C:\Users\UTKU\Desktop\mikroskop ai ...\AGENTS.md"
  python -X utf8 dosya_izi.py "...\AGENTS.md" --baslangic "2026-10-17 18:00" --bitis "2026-10-17 18:45" --komutlar
  python -X utf8 dosya_izi.py "...\AGENTS.md" --fark "ESKI_SURUM" "YENI_SURUM"

Secenekler:
  --baslangic/--bitis  yerel saat araligi ("YYYY-AA-GG SS:DD")
  --komutlar           aralikta calisan TUM arac cagrilarini da listeler; dosya adini anmayan bir
                       betikle yapilan yazmayi yakalamak icin (aralik gerekir, dar tut)
  --hepsi              yazma gorunmeyen bahisleri de gosterir
  --tam                kisaltmadan yazar
  --kayit KLASOR ...   ek kayit klasorleri
  --fark ESKI YENI     iki surum arasindaki satir farkini BOM, satir sonu ve SHA-256 ile gosterir

Bakilan kayitlar (varsa): ~\.codex\sessions, ~\.codex\archived_sessions, ~\.claude\projects,
~\.local\share\opencode, %APPDATA%\Claude, ~\.gemini.
Okudugu bicimler: Codex rollout ve Claude Code oturumu (.jsonl), OpenCode depo parcasi ve disa
aktarimi, Gemini CLI sohbeti (.json). Bilinmeyen json'da ve json olmayan dosyalarda (or. Antigravity)
adi ham olarak arar.

Siniflar:
  YAZMA        hedef dosyayi acikca degistiren cagri (apply_patch, Edit/Write, edit/write ...)
  YAZMA_ADAYI  dosya adini ve bir yazma komutunu birlikte iceren kabuk komutu; elle bakilmali
  BAHIS        dosya adi geciyor, yazma gorunmuyor (yalniz --hepsi ile)
  HAM          json olarak cozulemeyen dosyada ad ve klasor geciyor; zaman = dosyanin degisme zamani
  KOMUT        --komutlar ile: aralikta calisan herhangi bir arac cagrisi
Her olayda o oturumda ondan once gelen son kullanici mesaji yazilir: degisikligi kullanici mi
istedi, ajan mi kendiliginden yapti, oradan gorulur. Zamanlar bu bilgisayarin yerel saatidir.
Sinir: dosya adini hic anmayan bir betikle yapilan yazma YAZMA olarak gorunmez; --komutlar kullan.
"""
import argparse
import datetime
import difflib
import hashlib
import json
import os
import posixpath
import re
import sys
from collections import Counter
from pathlib import Path

HOME = Path.home()
LOG_DIRS = [HOME / ".codex" / "sessions", HOME / ".codex" / "archived_sessions",
            HOME / ".claude" / "projects", HOME / ".local" / "share" / "opencode",
            Path(os.environ.get("APPDATA") or HOME) / "Claude", HOME / ".gemini"]
SKIP_DIRS = {"cache", "code cache", "gpucache", "dawncache", "dawngraphitecache", "dawnwebgpucache",
             "blob_storage", "service worker", "indexeddb", "local storage", "session storage",
             "crashpad", "shared_proto_db", "network", "node_modules", "vm_bundles", ".git"}
MAX_HAM = 300 * 1024 * 1024
PATCH_HDR = re.compile(r"^\*\*\* (Update File|Add File|Delete File|Move to): *(.+?) *$")
WRITE_CMD = re.compile(
    r"Set-Content|Add-Content|Out-File|WriteAll(?:Text|Bytes|Lines)|New-Item|Copy-Item|Move-Item|"
    r"Rename-Item|Remove-Item|\b(?:cp|mv|rm|copy|move|del|ren|tee)\b|sed\s+-i|write_text|write_bytes|"
    r"\.write\(|open\([^)]*['\"][wax]|shutil\.|os\.replace|os\.rename", re.I)
REDIRECT = re.compile(r"(?<![0-9&])>>?\s*['\"]?([^'\"|&;<>\r\n]+)")
WRITE_TOOL = re.compile(r"edit|write|patch|replace|create|insert|notebook|move|rename|delete", re.I)
HID = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff]")
USER_SKIP = ("<environment_context", "# agents.md", "<user_instructions", "<permissions", "<turn_aborted")
MARKERS = ('"session_meta"', '"turn_context"', '"user_message"', '"type":"user"', '"type": "user"',
           '"role":"user"', '"role": "user"', '_output"')
PATH_KEYS = ("file_path", "filePath", "notebook_path", "path", "absolute_path", "target_file", "file")


def norm(p):
    p = str(p).strip().strip("\"'`").replace("\\", "/")
    return p[4:] if p.startswith("//?/") else p


def resolve(p, cwd):
    p = norm(p)
    if cwd and not re.match(r"^[a-z]:/|^/", p, re.I):
        p = norm(cwd).rstrip("/") + "/" + p
    return posixpath.normpath(p).lower()


class Hedef:
    def __init__(self, s):
        p = norm(s)
        self.full = bool(re.match(r"^[a-z]:/|^/", p, re.I))
        self.raw = p.rsplit("/", 1)[-1]
        self.base = self.raw.lower()
        self.esc = json.dumps(self.raw)[1:-1].lower()
        self.path = posixpath.normpath(p).lower() if self.full else None
        self.dir = self.path.rsplit("/", 1)[0] if self.full else None
        self.dirname = p.rsplit("/", 2)[-2] if self.full and p.count("/") >= 2 else None

    def same(self, p, cwd):
        r = resolve(p, cwd)
        return r == self.path if self.full else r.rsplit("/", 1)[-1] == self.base

    def in_scope(self, txt, cwd):
        if not self.full:
            return True
        if self.dir in norm(txt).lower():
            return True
        return bool(cwd) and resolve(cwd, None).startswith(self.dir)


def visible(s):
    return HID.sub(lambda m: "<U+%04X>" % ord(m.group(0)), s)


def short(s, n):
    return s if len(s) <= n else s[:n] + " ...(+%d karakter)" % (len(s) - n)


def to_local(v):
    """ISO metni ya da ms/s epoch -> yerel saatli datetime; cozulemezse None."""
    try:
        if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
            return datetime.datetime.fromtimestamp(v / 1000.0 if v > 1e11 else v).astimezone()
        if isinstance(v, str) and len(v) >= 10 and v[:4].isdigit() and v[4] == "-":
            v = re.sub(r"(\.\d{6})\d+", r"\1", v.strip().replace("Z", "+00:00"))
            return datetime.datetime.fromisoformat(v).astimezone()
    except (ValueError, OverflowError, OSError):
        pass
    return None


def ts_of(o):
    if isinstance(o, dict):
        for k in ("timestamp", "created_at", "createdAt", "time", "ts", "date"):
            v = o.get(k)
            if isinstance(v, dict):
                v = v.get("start") or v.get("created")
            t = to_local(v)
            if t:
                return t
    return None


def text_of(v):
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        return " ".join(text_of(x) for x in v)
    if isinstance(v, dict):
        return "\n".join(text_of(x) for x in v.values())
    return "" if v is None else str(v)


def user_text(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(b.get("text", "") for b in c
                         if isinstance(b, dict) and b.get("type") in ("text", "input_text"))
    return ""


def set_user(ctx, ts, txt):
    s = (txt or "").strip()
    if s and not s.lower().startswith(USER_SKIP):
        ctx["user"] = (ts, s)


def items(o, ctx):
    """Kayit nesnesinden ("cagri", ts, arac, girdi, klasor, id) ve ("sonuc", id, metin, hata) uretir.
    ctx: oturum klasoru, son kullanici mesaji ve nesnenin bilinen bir bicim olup olmadigi."""
    if not isinstance(o, dict):
        return
    ts, t = ts_of(o), o.get("type")
    if "payload" in o and t in ("session_meta", "turn_context", "response_item", "event_msg", "compacted"):
        ctx["bilinen"] = True                                   # Codex rollout
        p = o["payload"] if isinstance(o.get("payload"), dict) else {}
        pt = str(p.get("type"))
        if t in ("session_meta", "turn_context"):
            ctx["cwd"] = p.get("cwd") or ctx["cwd"]
        elif t == "event_msg" and pt == "user_message":
            set_user(ctx, ts, p.get("message"))
        elif t == "response_item" and pt == "message" and p.get("role") == "user":
            set_user(ctx, ts, user_text(p.get("content")))
        elif t == "response_item" and pt in ("function_call", "custom_tool_call", "local_shell_call"):
            a = p.get("arguments", p.get("input", p.get("action")))
            if isinstance(a, str):
                try:
                    a = json.loads(a)
                except ValueError:
                    pass
            wd = (a.get("workdir") or a.get("working_directory") or a.get("cwd")) if isinstance(a, dict) else None
            yield "cagri", ts, "codex/" + str(p.get("name") or pt), a, wd, p.get("call_id")
        elif t == "response_item" and pt.endswith("_output"):
            out = p.get("output")
            if isinstance(out, str):
                try:
                    j = json.loads(out)
                    out = j.get("output", out) if isinstance(j, dict) else out
                except ValueError:
                    pass
            yield "sonuc", p.get("call_id"), text_of(out), False
        return
    msg = o.get("message")
    if "sessionId" in o and "uuid" in o:                        # Claude Code satir zarfi (ek, ozet ...)
        ctx["bilinen"] = True
        ctx["cwd"] = o.get("cwd") or ctx["cwd"]
    if t in ("user", "assistant") and isinstance(msg, dict):    # Claude Code mesaji
        ctx["bilinen"] = True
        ctx["cwd"] = o.get("cwd") or ctx["cwd"]
        c = msg.get("content")
        if t == "user":
            if isinstance(c, list):
                for b in c:
                    if isinstance(b, dict) and b.get("type") == "tool_result":
                        yield "sonuc", b.get("tool_use_id"), text_of(b.get("content")), bool(b.get("is_error"))
            set_user(ctx, ts, user_text(c))
        elif isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    yield "cagri", ts, "claude/" + str(b.get("name")), b.get("input"), None, b.get("id")
        return
    if ctx["bilinen"]:
        return
    if t == "tool" and isinstance(o.get("state"), dict):         # OpenCode depo parcasi
        ctx["bilinen"] = True
        st = o["state"]
        cid = o.get("callID") or o.get("id")
        yield "cagri", ts_of(st) or ts, "opencode/" + str(o.get("tool")), st.get("input"), None, cid
        yield "sonuc", cid, "%s %s" % (st.get("status", ""), text_of(st.get("output") or st.get("error"))), \
            st.get("status") == "error"
        return
    if isinstance(o.get("info"), dict) and isinstance(o.get("messages"), list):   # OpenCode disa aktarimi
        ctx["bilinen"] = True
        ctx["cwd"] = o["info"].get("directory") or ctx["cwd"]
        for m in o["messages"]:
            if not isinstance(m, dict):
                continue
            info = m.get("info") if isinstance(m.get("info"), dict) else {}
            for part in m.get("parts") or []:
                if not isinstance(part, dict):
                    continue
                if info.get("role") == "user" and part.get("type") == "text":
                    set_user(ctx, ts_of(info), part.get("text"))
                elif part.get("type") == "tool":
                    for it in items(part, ctx):
                        yield it
        return
    if isinstance(o.get("messages"), list):                     # Gemini CLI sohbeti
        ctx["bilinen"] = True
        for m in o["messages"]:
            if not isinstance(m, dict):
                continue
            if m.get("type") == "user":
                set_user(ctx, ts_of(m), text_of(m.get("content")))
            for c in m.get("toolCalls") or []:
                if isinstance(c, dict):
                    cid = c.get("id")
                    yield "cagri", ts_of(c) or ts_of(m), "gemini/" + str(c.get("name")), c.get("args"), None, cid
                    yield "sonuc", cid, str(c.get("status", "")), c.get("status") == "error"


def classify(h, tool, inp, cwd):
    txt = text_of(inp)
    for ln in txt.splitlines():
        m = PATCH_HDR.match(ln.strip())
        if m and h.same(m.group(2), cwd):
            return "YAZMA"
    if h.base not in txt.lower() or not h.in_scope(txt, cwd):
        return None
    if isinstance(inp, dict):
        paths = [inp[k] for k in PATH_KEYS if isinstance(inp.get(k), str)]
        if any(h.same(v, cwd) for v in paths):
            return "YAZMA" if WRITE_TOOL.search(tool) else "BAHIS"
        if paths and "command" not in inp and "cmd" not in inp:
            return "BAHIS"              # baska bir dosyaya ait cagri; hedefin adi yalniz icerikte geciyor
    if any(h.base in r.lower() for r in REDIRECT.findall(txt)) or WRITE_CMD.search(txt):
        return "YAZMA_ADAYI"
    return "BAHIS"


def body(h, inp, cwd, full):
    txt = text_of(inp)
    lines = []
    if any(PATCH_HDR.match(x.strip()) for x in txt.splitlines()):
        on = False
        for x in txt.splitlines():
            m = PATCH_HDR.match(x.strip())
            if m and m.group(1) != "Move to":
                on = h.same(m.group(2), cwd)
            elif x.strip().startswith("*** End Patch"):
                on = False
            if on:
                lines.append(x)
    elif isinstance(inp, dict) and any(k in inp for k in ("old_string", "oldString", "new_string",
                                                         "newString", "content", "edits")):
        for e in inp["edits"] if isinstance(inp.get("edits"), list) else [inp]:
            if not isinstance(e, dict):
                continue
            for k, sign in (("old_string", "- "), ("oldString", "- "), ("new_string", "+ "),
                            ("newString", "+ "), ("content", "+ ")):
                if isinstance(e.get(k), str):
                    lines += [sign + x for x in e[k].splitlines()]
    else:
        cmd = inp.get("command", inp.get("cmd")) if isinstance(inp, dict) else None
        lines = text_of(cmd if cmd is not None else inp).splitlines()
    if not lines:
        lines = txt.splitlines()
    if not full and len(lines) > 40:
        lines = lines[:40] + ["... (%d satir daha; tamami icin --tam)" % (len(lines) - 40)]
    return [visible(x if full else short(x, 400)) for x in lines]


def one_line(inp):
    txt = text_of(inp)
    hdr = [m.group(0) for m in (PATCH_HDR.match(x.strip()) for x in txt.splitlines()) if m]
    if hdr:
        return visible(short(" ; ".join(hdr), 300))
    cmd = inp.get("command", inp.get("cmd")) if isinstance(inp, dict) else None
    return visible(short(" ".join(text_of(cmd if cmd is not None else inp).split()), 300))


def objects(fp, h, want_all):
    with open(fp, encoding="utf-8", errors="replace") as f:
        if fp.suffix.lower() == ".json":
            raw = f.read()
            low = raw.lower()
            hit = h.base in low or h.esc in low
            if not (hit or want_all):
                return
            try:
                yield 1, json.loads(raw), hit
                return
            except ValueError:
                lines = raw.split("\n")
        else:
            lines = f
        for no, line in enumerate(lines, 1):
            low = line.lower()
            hit = h.base in low or h.esc in low
            if hit or want_all or any(m in line for m in MARKERS):
                try:
                    yield no, json.loads(line), hit
                except ValueError:
                    continue


def in_window(a, ts):
    if ts is None:
        return not (a.start or a.end)
    return not ((a.start and ts < a.start) or (a.end and ts > a.end))


def scan(fp, h, a, events, stats):
    try:
        st = fp.stat()
    except OSError:
        return
    mt = datetime.datetime.fromtimestamp(st.st_mtime).astimezone()
    if a.start and mt < a.start:
        return                      # aralik baslamadan once kapanmis kayit
    if fp.suffix.lower() not in (".jsonl", ".json"):
        ham(fp, h, a, events, mt, st.st_size)
        return
    stats["kayit"] += 1
    ctx, pending = {"cwd": None, "user": None}, {}
    for no, o, hit in objects(fp, h, bool(a.komutlar)):
        ctx["bilinen"] = False
        for it in items(o, ctx):
            if it[0] == "sonuc":
                ev = pending.pop(it[1], None) if it[1] else None
                if ev is not None:
                    ev["sonuc"] = ("HATA: " if it[3] else "") + short(" ".join(it[2].split()), 200)
                continue
            _, ts, tool, inp, wd, cid = it
            if not in_window(a, ts):
                continue
            cwd = wd or ctx["cwd"]
            k = classify(h, tool, inp, cwd) if hit else None
            if k is None and not a.komutlar:
                continue
            ev = {"ts": ts, "sinif": k or "KOMUT", "arac": tool, "dosya": fp, "satir": no, "klasor": cwd,
                  "kullanici": ctx["user"],
                  "govde": body(h, inp, cwd, a.tam) if k else [one_line(inp)]}
            events.append(ev)
            if cid:
                pending[cid] = ev
        if hit and not ctx["bilinen"]:
            ts = ts_of(o)
            txt = text_of(o)
            if not in_window(a, ts) or not h.in_scope(txt, None):
                continue
            k = "YAZMA_ADAYI" if WRITE_CMD.search(txt) or any(
                PATCH_HDR.match(x.strip()) for x in txt.splitlines()) else "BAHIS"
            i = txt.lower().find(h.base)
            events.append({"ts": ts, "sinif": k, "arac": "bilinmeyen-bicim", "dosya": fp, "satir": no,
                           "govde": [visible(" ".join(txt[max(0, i - 200):i + 200].split()))]})


def ham(fp, h, a, events, mt, size):
    if not a.start or not size or size > MAX_HAM:
        return                      # ham arama yalniz aralikla ve makul boyutta
    try:
        data = fp.read_bytes()
    except OSError:
        return
    n = sum(data.count(h.raw.encode(e)) for e in ("utf-8", "utf-16-le"))
    if not n:
        return
    if h.dirname and not any(h.dirname.encode(e) in data for e in ("utf-8", "utf-16-le")):
        return
    events.append({"ts": mt, "sinif": "HAM", "arac": fp.suffix or "-", "dosya": fp, "satir": None,
                   "govde": ["adi %d kez geciyor; zaman = bu dosyanin son degisme zamani" % n]})


def stamp(p):
    return datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")


def fark(pa, pb):
    print("=" * 72)
    print("FARK (eski -> yeni)")
    data = []
    for p in (pa, pb):
        if not p.is_file():
            print("  dosya yok:", p)
            return
        raw = p.read_bytes()
        print("  %s\n    %d bayt | SHA-256 %s | BOM %s | satir sonu %s | son degisme %s" % (
            p, len(raw), hashlib.sha256(raw).hexdigest(), "var" if raw.startswith(b"\xef\xbb\xbf") else "yok",
            "CRLF" if b"\r\n" in raw else "LF", stamp(p)))
        data.append(raw)
    A, B = [r.decode("utf-8-sig", "replace").replace("\r\n", "\n").split("\n") for r in data]
    ops = [op for op in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes() if op[0] != "equal"]
    if not ops:
        print("  Metin ayni;", "fark yalniz BOM/satir sonu/kodlamada." if data[0] != data[1] else "dosyalar birebir ayni.")

    def rng(x, y):
        return "%d-%d" % (x + 1, y) if y > x else "yok (%d. satirdan sonra)" % x
    for tag, i1, i2, j1, j2 in ops:
        print("  @@ eski satir %s | yeni satir %s | %s" % (
            rng(i1, i2), rng(j1, j2), {"replace": "degisti", "delete": "silindi", "insert": "eklendi"}[tag]))
        for line in difflib.ndiff(A[i1:i2], B[j1:j2]):
            if line[:1] in "-+?":
                print("    " + visible(line.rstrip("\n")))


def parse_time(s, end):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            t = datetime.datetime.strptime(s.strip(), fmt)
        except ValueError:
            continue
        if fmt == "%Y-%m-%d" and end:
            t += datetime.timedelta(days=1)
        return t.astimezone()
    raise SystemExit('Zaman bicimi "YYYY-AA-GG SS:DD" olmali (or. "2026-10-17 18:00"): %s' % s)


def show(e, full):
    t = e["ts"].strftime("%Y-%m-%d %H:%M:%S") if e["ts"] else "????-??-?? ??:??:??"
    where = "%s%s" % (e["dosya"], "  satir %d" % e["satir"] if e["satir"] else "")
    if e["sinif"] == "KOMUT":
        print("%s  KOMUT        %-24s %s" % (t, e["arac"], e["govde"][0]))
        print("%21s%s" % ("", where))
        return
    print("-" * 72)
    print("%s  %-12s %s" % (t, e["sinif"], e["arac"]))
    print("  kayit : " + where)
    if e.get("klasor"):
        print("  klasor: %s" % e["klasor"])
    if e.get("sonuc"):
        print("  sonuc : %s" % visible(e["sonuc"]))
    u = e.get("kullanici")
    if u:
        txt = " ".join(u[1].split())
        print("  ondan onceki son kullanici mesaji (%s): %s" % (
            u[0].strftime("%Y-%m-%d %H:%M:%S") if u[0] else "?", visible(txt if full else short(txt, 400))))
    for x in e["govde"]:
        print("    " + x)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Dosya izi: bu dosyayi hangi ajan oturumu degistirdi (salt-okunur)")
    ap.add_argument("hedef", help="izi surulecek dosyanin tam yolu (yalniz adi da olur)")
    ap.add_argument("--baslangic")
    ap.add_argument("--bitis")
    ap.add_argument("--komutlar", action="store_true")
    ap.add_argument("--hepsi", action="store_true")
    ap.add_argument("--tam", action="store_true")
    ap.add_argument("--kayit", nargs="*", default=[])
    ap.add_argument("--fark", nargs=2, metavar=("ESKI", "YENI"))
    a = ap.parse_args()
    a.start = parse_time(a.baslangic, False) if a.baslangic else None
    a.end = parse_time(a.bitis, True) if a.bitis else None
    if a.komutlar and not a.start:
        print("--komutlar icin --baslangic gerekir; araligi dar tut (or. 30 dakika).")
        return 2
    h = Hedef(a.hedef)
    if a.fark:
        fark(Path(a.fark[0]), Path(a.fark[1]))
    print("=" * 72)
    tp = Path(a.hedef)
    if tp.is_file():
        raw = tp.read_bytes()
        print("HEDEF: %s\n  simdi %d bayt | SHA-256 %s | son degisme %s" % (
            tp, len(raw), hashlib.sha256(raw).hexdigest(), stamp(tp)))
    else:
        print("HEDEF: %s (bu adla dosya yok; yalniz kayitlarda aranir)" % a.hedef)
    print("Aralik: %s -> %s" % (a.baslangic or "en bastan", a.bitis or "simdiye kadar"))
    dirs = LOG_DIRS + [Path(x) for x in a.kayit]
    for d in dirs:
        print("  kayit klasoru %-5s %s" % ("var" if d.is_dir() else "yok", d))
    events, stats = [], Counter()
    for d in dirs:
        if not d.is_dir():
            continue
        for root, subdirs, files in os.walk(d):
            subdirs[:] = [s for s in subdirs if s.lower() not in SKIP_DIRS]
            for name in files:
                fp = Path(root) / name
                try:
                    scan(fp, h, a, events, stats)
                except Exception as ex:      # tek bir garip kayit taramayi durdurmasin
                    stats["atlanan"] += 1
                    print("ATLANDI: %s (%s: %s)" % (fp, type(ex).__name__, ex))
    events.sort(key=lambda e: e["ts"].timestamp() if e["ts"] else 0)
    for e in events:
        if e["sinif"] != "BAHIS" or a.hepsi:
            show(e, a.tam)
    c = Counter(e["sinif"] for e in events)
    print("=" * 72)
    print("OZET: %s | taranan json kaydi: %d | atlanan: %d" % (
        " | ".join("%s=%d" % (k, c[k]) for k in ("YAZMA", "YAZMA_ADAYI", "BAHIS", "HAM", "KOMUT")),
        stats["kayit"], stats["atlanan"]))
    if c["BAHIS"] and not a.hepsi:
        print("  BAHIS satirlari gosterilmedi (--hepsi ile gorunur).")
    yazan = Counter(str(e["dosya"]) for e in events if e["sinif"] in ("YAZMA", "YAZMA_ADAYI"))
    if yazan:
        print("Yazma gorulen kayitlar:")
        for s, n in yazan.most_common():
            print("  %3d  %s" % (n, s))
    else:
        print("Bu aralikta taranan kayitlarin hicbirinde bu dosyaya yazma gorulmedi. Olasiliklar:")
        print("  elle (bir duzenleyiciyle) degistirildi; dosya adini anmayan bir betikle yazildi")
        print("  (--komutlar ile araliktaki tum cagrilara bak); ya da kaydi burada taranmayan bir arac yazdi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
