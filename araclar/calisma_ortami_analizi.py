#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
calisma_ortami_analizi.py (v1.0) - Calisma klasorundeki metinleri okur; talimatlari,
kurallari ve ajan notlarini ayrintili analiz eder.
Salt-okunur: taranan klasore hicbir sey yazmaz. Kaynak kod sadece ASCII.

Kullanim (PowerShell, Downloads'tan):
  python -X utf8 calisma_ortami_analizi.py
  python -X utf8 calisma_ortami_analizi.py "C:\baska\klasor"
  python -X utf8 calisma_ortami_analizi.py --temel-kaydet     # simdiki hali temel olarak sakla
  python -X utf8 calisma_ortami_analizi.py --gun 7            # son 7 gunde degisenler
  python -X utf8 calisma_ortami_analizi.py --talimat "notlar/.*\.md$"   # ek talimat deseni

Bakilanlar:
  1. Dosya turu (talimat, karar_plan, ajan_kaydi, kod, veri, ikili) ve kodlama
     (UTF-8, BOM'lu UTF-8, UTF-16, cp1254).
  2. Talimat dosyalarinda: beyan edilen yazar/hazirlayan, tarih/surum/kaynak satirlari,
     oncelik ifadeleri ("o dosya kazanir"), baska dosyalara referanslar (bulunamayanlar
     dahil) ve kural benzeri cumleler (yapma, degistirme, onay iste, -meli/-mali ...).
  3. Ayni adli talimat dosyalari (or. alt klasorlerdeki AGENTS.md) birbirinden ayrismis mi.
  4. "Sessiz otorite": ajan notlarinda gecip talimat dosyalarinda OLMAYAN kural cumleleri.
  5. Konu bazinda kurallar (onay, veri/D:, silme/degistirme ...) yan yana.
  6. Gizli icerik: gorunmez karakterler, HTML ve Markdown yorumlari.
  7. Son N gunde degisen dosyalar; --temel-kaydet ile saklanan temele gore eklenen,
     silinen, degisen dosyalar ve talimat dosyalarinda satir satir fark.

Cikti: ekranda ozet; ayrintilar Markdown raporda (varsayilan: ortam_analizi.md,
komutun calistirildigi klasorde). Temel: ortam_temel.json. Ikisi de taranan
klasorun icine yazilamaz. Rapordaki gorunmez karakterler <U+XXXX> diye yazilir.
Not: kural ve tur tespiti sezgiseldir (anahtar kelime ve ek tabanli). "Kural benzeri"
diye okunmali; emin olmak icin rapordaki satira bakilmali.
"""
import argparse
import difflib
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

VERSION = "1.0"
TEXT_EXT = {".md", ".txt", ".json", ".jsonl", ".py", ".log", ".yaml", ".yml", ".toml", ".csv",
            ".tsv", ".html", ".htm", ".css", ".js", ".ts", ".xml", ".ini", ".cfg", ".rst", ".kms",
            ".bat", ".cmd", ".ps1", ".sh"}
CODE_EXT = {".py", ".bat", ".cmd", ".ps1", ".sh", ".js", ".ts"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
MAX_BYTES = 50 * 1024 * 1024
KEEP_TEXT_MAX = 512 * 1024      # temelde tam metni saklanan dosya ust siniri
FULLTEXT_MAX = 30000            # raporda talimat dosyasi basina gosterilen metin
MAX_RULES = 3000                # dosya basina saklanan kural cumlesi
DEFAULT_ROOT = Path.home() / "Desktop" / "mikroskop ai \u00e7al\u0131\u015fma klas\u00f6r\u00fc"
DEFAULT_EXTRA = [Path("D:\\g\u00f6r\u00fcnt\u00fc veri seti\\README.txt")]

TR_FOLD = str.maketrans({
    "\u00e7": "c", "\u00c7": "c", "\u011f": "g", "\u011e": "g", "\u0131": "i", "\u0130": "i",
    "\u00f6": "o", "\u00d6": "o", "\u015f": "s", "\u015e": "s", "\u00fc": "u", "\u00dc": "u",
    "\u00e2": "a", "\u00c2": "a", "\u00ee": "i", "\u00ce": "i", "\u00fb": "u", "\u00db": "u"})

HID = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff"
                 "\ufe00-\ufe0f\U000e0000-\U000e007f\U000e0100-\U000e01ef]")
RE_HTML_COMMENT = re.compile(r"<!--[\s\S]*?-->")
RE_MD_COMMENT = re.compile(r"^[ \t]*\[//\]:[ \t]*#.*$", re.M)

# Kural benzeri cumle; katlanmis (ASCII, kucuk harf) metinde aranir.
RULE_PARTS = [
    r"yapma(?:yin|yiniz)?", r"yapilmaz", r"yapilmamali", r"yapilamaz",
    r"etme(?:yin|yiniz)?", r"edilmez", r"edilmemeli", r"edilemez",
    r"degistir(?:me|meyin|mez|ilmez|ilemez|ilmemeli|ilmesin)",
    r"sil(?:me|meyin|mez|inmez|inemez|inmemeli|inmesin)",
    r"dokunma(?:yin)?", r"dokunulmaz", r"girmez", r"konmaz",
    r"\w+(?:ilmaz|ilmez|ulmaz|ulmez|inmaz|inmez|unmaz|unmez)",
    r"\w+(?:masin|mesin)", r"\w+(?:mali|meli)(?:dir|sin|siniz|yiz)?",
    r"yasak(?:tir)?", r"zorunlu(?:dur)?", r"mecburi", r"mutlaka", r"asla", r"kesinlikle",
    r"her zaman", r"hicbir zaman", r"hic bir zaman", r"gerekir", r"gereklidir",
    r"gerekmektedir", r"sart(?:tir)?",
    r"onay(?:i|ini|in)? ?(?:iste|al|gerek|sor)\w*", r"onaysiz", r"onay olmadan",
    r"izinsiz", r"izin (?:iste|al|ver)\w*", r"kullaniciya sor\w*",
    r"must(?: not)?", r"never", r"always", r"do not", r"don't", r"shall", r"required",
    r"forbidden", r"should(?: not)?",
]
RULE_RE = re.compile(r"\b(?:" + "|".join(RULE_PARTS) + r")\b")
RULE_STOP = {"temeli", "temelidir", "normali", "emeli", "kemali", "cemali", "formali",
             "bilmez", "bilinmez", "dinmez", "sinmez", "binmez"}
# Cumle sonundaki olumsuz emir: "... ara dosya yazma." / "... uydurma."
NEG_IMP_END = re.compile(r"\b(\w{2,}(?:ma|me)(?:yin|yiniz)?)\s*[.!]\s*$")
NEG_STOP = {"calisma", "uygulama", "dogrulama", "degerlendirme", "guncelleme", "kodlama",
            "isleme", "olcme", "tamamlama", "inceleme", "kontrol etme"}

KONULAR = [
    ("onay / izin", r"\bonay|\bizin"),
    ("veri ve D: diski", r"\bd:|veri seti|veri klasor|ham gorsel|goruntu veri"),
    ("kod klasoru", r"\bkod klasor"),
    ("klasor acma / duzen", r"alt klasor|klasor ac|duzen olustur"),
    ("not / rapor birakma", r"\bnot (?:birak|yaz)|rapor\w* (?:yaz|birak|olustur)"),
    ("silme / degistirme", r"\bsil|\bdegistir"),
    ("kopya / onbellek", r"\bkopya|onbellek|\bcache"),
    ("internet / indirme", r"internet|\bindir|\bweb\b"),
    ("test / dogrulama", r"\btest|dogrula|\bkabul"),
    ("kullaniciya sorma", r"kullaniciya sor|emin degil"),
]
KONU_RE = [(ad, re.compile(d)) for ad, d in KONULAR]

AUTHOR_RE = re.compile(r"^[\s#>*\-]*\(?(hazirlayan(?:lar)?|yazar|yazan|author|written by|olusturan|onaylayan)\)?"
                       r"\s*[:=]\s*(.{1,160})")
AUTHOR_KEY = re.compile(r"(?:hazirlayan|yazar|yazan|author|olusturan|onaylayan)\w*$")
META_RE = re.compile(r"^[\s#>*\-]*(tarih|surum|versiyon|version|degisiklik|guncelleme|son guncelleme|revizyon|kaynak)"
                     r"\s*[:=]\s*(.{1,200})")
PREC_RE = re.compile(r"kazanir|gecerli(?:dir)?\b|oncelik|ustundur|baglayici|yerine gecer|gecersiz|iptal edil"
                     r"|yururluk|esas alinir|referans alinir|tek kaynak|tek yetkili|celisirse|celiski")
AGENT_RE = re.compile(r"\b(?:claude|codex|gpt\w*|chatgpt|openai|gemini|antigravity|opencode|deepseek|qwen\w*|kimi"
                      r"|llama|ollama|copilot|cursor|sonnet|opus|haiku)\b|\bajan\w*|\bagent\w*|yapay zeka")
USER_RE = re.compile(r"kullanici\w*|\butku\b|\bben\b|\binsan\b")
WINPATH = re.compile(r"[A-Za-z]:\\[^\r\n\"'<>|*?`]+")
DATED = re.compile(r"\d{4}-\d{2}-\d{2}|\d{8}|_r\d+(?=[._ -]|$)")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")

TALIMAT_ADI = re.compile(r"^(?:agents|claude|gemini|copilot-instructions)\.md$|^\.cursorrules$|^readme|talimat|kural"
                         r"|prosedur|calisma[_ ]duzeni|yonerge|yonetmelik|protokol|kilavuz|rehber|kullanim|standard")
TALIMAT_KLASOR = re.compile(r"(?:^|/)(?:kuralar|kurallar|talimatlar)/[^/]+$")
KARAR_ADI = re.compile(r"karar|plan|hedef|manifesto|fikir|fikrin|yol_haritasi|is[_ ]akisi")
KAYIT_ADI = re.compile(r"rapor|denetim|sonuc|kayit|kanit|ozet|durum|envanter|teslim|kontrol|inceleme|olcum|analiz"
                       r"|deney|taslak|onarim|kosu|test|indeks|ilerleme|girdi")
CATS = ("talimat", "karar_plan", "ajan_kaydi", "kod", "veri", "ikili")


def fold(s):
    """Turkce harfleri ASCII'ye indirip kucultur: 'De\u011fi\u015ftirme' -> 'degistirme'."""
    return unicodedata.normalize("NFC", s).translate(TR_FOLD).lower()


def norm_unit(s):
    """Karsilastirma icin: katla, madde/numara isaretlerini ve noktalamayi at, bosluklari teklestir."""
    s = re.sub(r"^[\s#>*\-\u2022\d.)(]+", "", fold(s))
    s = re.sub(r"[^\w\s:\\/]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def vis(s):
    return HID.sub(lambda m: "<U+%04X>" % ord(m.group(0)), s)


def cell(s, n=300):
    return vis(s).replace("|", "\\|").replace("\r", " ").replace("\n", " ")[:n]


def emoji_ok(s, i):
    if ord(s[i]) not in (0x200D, 0xFE0E, 0xFE0F) or i == 0:
        return False
    p = s[i - 1]
    return unicodedata.category(p).startswith("S") or p in "#*0123456789" or ord(p) in (0x200D, 0xFE0F)


def is_rule(f):
    if any(m.group(0) not in RULE_STOP for m in RULE_RE.finditer(f)):
        return True
    m = NEG_IMP_END.search(f)
    return bool(m) and m.group(1) not in NEG_STOP


def who(v):
    a, u = bool(AGENT_RE.search(v)), bool(USER_RE.search(v))
    return "karma" if a and u else "ajan" if a else "kullanici" if u else "belirsiz"


def read_text(raw):
    if raw[:3] == b"\xef\xbb\xbf":
        return raw[3:].decode("utf-8", "replace"), "utf-8-bom"
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16", "replace"), "utf-16"
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        pass
    if raw[:4096].count(b"\x00") > 64:
        try:
            return raw.decode("utf-16-le"), "utf-16-le (bomsuz)"
        except UnicodeDecodeError:
            pass
    return raw.decode("cp1254", "replace"), "cp1254"


def walk(o, path="$"):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, "%s.%s" % (path, k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, "%s[%d]" % (path, i))
    elif isinstance(o, str):
        yield path, o


def sentences(s):
    for part in SENT_SPLIT.split(s):
        part = part.strip()
        if len(part) >= 8 and re.search(r"[^\W\d_]", part):
            yield part[:500]


def units_of(ext, text):
    """(yer, metin) ciftleri: metinde satirlar, JSON'da dize degerleri (cumlelere bolunmus)."""
    if ext in (".json", ".jsonl"):
        objs = []
        if ext == ".json":
            try:
                objs = [("", json.loads(text))]
            except ValueError:
                pass
        else:
            for no, line in enumerate(text.splitlines(), 1):
                if line.strip():
                    try:
                        objs.append(("satir %d " % no, json.loads(line)))
                    except ValueError:
                        pass
        if objs:
            for pre, obj in objs:
                for path, s in walk(obj):
                    for sent in sentences(s):
                        yield pre + path, sent
            return
    for no, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if len(line) > 400:
            for sent in sentences(line):
                yield "satir %d" % no, sent
        elif len(line) >= 3:
            yield "satir %d" % no, line


def category(rel_f, ext, extra_pats):
    base = rel_f.rsplit("/", 1)[-1]
    if any(p.search(rel_f) for p in extra_pats):
        return "talimat"
    if ext not in TEXT_EXT:
        return "ikili"
    if TALIMAT_ADI.search(base) or TALIMAT_KLASOR.search(rel_f):
        return "talimat"
    if DATED.search(base) or ext in (".log", ".jsonl"):
        return "ajan_kaydi"
    if KARAR_ADI.search(base):
        return "karar_plan"
    if ext in CODE_EXT:
        return "kod"
    if KAYIT_ADI.search(base):
        return "ajan_kaydi"
    return "veri"


def resolve_path(s):
    """Metindeki 'C:\\...' yolunu, var olan en uzun on eke kadar kirpar."""
    s = re.split(r"\s{2,}|\t", s)[0].rstrip(" .,:;)]}")
    words = s.split(" ")
    for k in range(len(words), 0, -1):
        cand = " ".join(words[:k]).rstrip(" .,:;)]}")
        if os.path.exists(cand):
            return cand, True
    for k in range(1, len(words) + 1):
        cand = " ".join(words[:k]).rstrip(" .,:;)]}")
        if re.search(r"\.\w{1,5}$", cand):
            return cand, False
    return s, False


def analyze_file(p, rel, extra_pats):
    st = p.stat()
    ext = p.suffix.lower()
    info = {"rel": rel, "path": str(p), "ext": ext, "size": st.st_size, "mtime": st.st_mtime,
            "sha": None, "kind": "ikili", "enc": "-", "cat": "ikili", "rules": [], "n_rules": 0,
            "rule_counts": Counter(),
            "authors": [], "meta": [], "prec": [], "refs": [], "hidden": Counter(), "html": [],
            "mdc": [], "agent_mentions": 0, "units": 0, "text": None, "promoted": False, "error": None}
    if st.st_size > MAX_BYTES:
        info["error"] = "50 MB'tan buyuk, okunmadi"
        return info
    raw = p.read_bytes()
    info["sha"] = hashlib.sha256(raw).hexdigest()
    rel_f = fold(rel.replace("\\", "/"))
    is_text = ext in TEXT_EXT
    if not is_text and b"\x00" not in raw[:4096]:
        try:
            raw.decode("utf-8")
            is_text = True
        except UnicodeDecodeError:
            pass
    if not is_text:
        info["cat"] = category(rel_f, ext or ".bin", extra_pats)
        return info
    text, enc = read_text(raw)
    info["kind"], info["enc"] = "metin", enc
    cat = category(rel_f, ext if ext in TEXT_EXT else ".txt", extra_pats)
    for m in HID.finditer(text):
        if (m.start() == 0 and m.group(0) == "\ufeff") or emoji_ok(text, m.start()):
            continue
        info["hidden"]["U+%04X" % ord(m.group(0))] += 1
    info["html"] = [m.group(0) for m in RE_HTML_COMMENT.finditer(text)]
    info["mdc"] = [m.group(0).strip() for m in RE_MD_COMMENT.finditer(text)]
    n = 0
    for yer, u in units_of(ext, text):
        n += 1
        f = fold(u)
        if is_rule(f):
            info["n_rules"] += 1
            nu, rc = norm_unit(u), info["rule_counts"]
            if nu in rc or len(rc) < MAX_RULES:  # ayni cumle bir kez saklanir, tekrari sayilir
                if nu not in rc:
                    info["rules"].append((yer, u, nu))
                rc[nu] += 1
        if PREC_RE.search(f):
            info["prec"].append((yer, u))
        m = AUTHOR_RE.match(f)
        if m:
            info["authors"].append((yer, u.strip(), who(m.group(2))))
        elif yer.startswith(("$", "satir")) and AUTHOR_KEY.search(fold(yer).rsplit(".", 1)[-1]):
            info["authors"].append((yer, u.strip(), who(f)))
        if META_RE.match(f):
            info["meta"].append((yer, u.strip()))
    info["units"] = n
    info["agent_mentions"] = len(AGENT_RE.findall(fold(text)))
    base = rel_f.rsplit("/", 1)[-1]
    if cat == "veri" and info["n_rules"] >= 5 and info["n_rules"] >= 0.15 * n and not DATED.search(base):
        cat, info["promoted"] = "talimat", True
    info["cat"] = cat
    if cat in ("talimat", "karar_plan"):
        info["text"] = text
        seen = set()
        for m in WINPATH.finditer(text):
            ref = resolve_path(m.group(0))
            if ref[0] not in seen:
                seen.add(ref[0])
                info["refs"].append(ref)
    return info


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for f in sorted(filenames):
            yield Path(dirpath) / f


def inside(p, root):
    try:
        Path(p).resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def tstr(t):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(t))


def short_diff(a, b, la, lb, limit):
    d = list(difflib.unified_diff(a.splitlines(), b.splitlines(), la, lb, lineterm="", n=1))
    return d[:limit], max(0, len(d) - limit)


def cross_checks(files, root_names):
    """Talimatlar arasi ve talimat-not arasi karsilastirmalar."""
    tal = [f for f in files if f["cat"] == "talimat" and f["text"] is not None]
    t_set = {n for f in tal for _, _, n in f["rules"]}
    t_blob = "\n".join(" ".join(norm_unit(x) for x in f["text"].splitlines()) for f in tal)
    for f in files:
        f["new_rules"], f["quoted"] = [], 0
        if f["cat"] in ("talimat", "ikili", "kod"):  # kod yorumlari davranis anlatir, talimat degil
            continue
        for yer, u, n in f["rules"]:
            if len(n) < 15:
                continue
            if n in t_set or n in t_blob:
                f["quoted"] += f["rule_counts"][n]
            else:
                f["new_rules"].append((yer, u, f["rule_counts"][n]))
    for f in files:
        f["refs_int"] = []
        if f["text"] is not None:
            ft, own = fold(f["text"]), fold(Path(f["rel"]).name)
            f["refs_int"] = sorted(nm for nm in root_names if nm != own and nm in ft)
    topics = defaultdict(list)
    for f in files:
        for yer, u, _ in f["rules"]:
            fu = fold(u)
            for ad, rx in KONU_RE:
                if rx.search(fu):
                    topics[ad].append((f["cat"], f["rel"], yer, u))
    by_name = defaultdict(list)
    for f in tal:
        by_name[fold(Path(f["rel"].replace("\\", "/")).name)].append(f)
    diverged = []
    for nm, group in sorted(by_name.items()):
        if len(group) < 2:
            continue
        variants = defaultdict(list)
        for f in group:
            variants[f["sha"]].append(f)
        variants = sorted(variants.values(), key=len, reverse=True)
        # Ana varyanta benzerlik: yuksekse ayni dosyanin kaymis kopyasi, dusukse ayri belge
        ref = variants[0][0]["text"]
        ratios = [difflib.SequenceMatcher(None, ref, v[0]["text"]).ratio() for v in variants[1:]]
        diverged.append((nm, group, variants, ratios))
    by_sha = defaultdict(list)
    for f in files:
        if f["kind"] == "metin" and f["sha"]:
            by_sha[f["sha"]].append(f)
    copies = sorted((g for g in by_sha.values() if len(g) > 1), key=lambda g: -g[0]["size"])
    return topics, diverged, copies


def compare_baseline(base, files):
    cur = {f["rel"]: f for f in files}
    old = base.get("dosyalar", {})
    texts = base.get("metinler", {})
    added = sorted(set(cur) - set(old))
    removed = sorted(set(old) - set(cur))
    changed = sorted(r for r in set(cur) & set(old) if cur[r]["sha"] != old[r]["sha256"])
    diffs = {}
    for r in changed:
        if r in texts and cur[r]["text"] is not None:
            diffs[r] = short_diff(texts[r], cur[r]["text"], "temel", "simdi", 200)
    return added, removed, changed, diffs


def save_baseline(path, root, files):
    data = {"surum": VERSION, "kok": str(root), "olusturma": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "dosyalar": {f["rel"]: {"sha256": f["sha"], "boyut": f["size"], "mtime": f["mtime"],
                                    "tur": f["cat"]} for f in files},
            "metinler": {f["rel"]: f["text"] for f in files
                         if f["text"] is not None and f["size"] <= KEEP_TEXT_MAX}}
    Path(path).write_text(json.dumps(data, ensure_ascii=True, sort_keys=True, indent=1), encoding="utf-8")


def write_report(path, root, extras, files, topics, diverged, copies, recent, gun, cmp_res, base_info):
    L = []
    add = L.append
    tal = [f for f in files if f["cat"] == "talimat"]
    add("# Calisma ortami analizi")
    add("")
    add("- Kok: `%s`" % root)
    if extras:
        add("- Ek talimat dosyalari: " + ", ".join("`%s`" % e for e in extras))
    add("- Olusturma: %s | arac surumu %s" % (time.strftime("%Y-%m-%d %H:%M"), VERSION))
    cats = Counter(f["cat"] for f in files)
    add("- Dosya: %d | " % len(files) + " | ".join("%s=%d" % (c, cats[c]) for c in CATS))
    add("- Kodlama: " + ", ".join("%s=%d" % kv for kv in Counter(f["enc"] for f in files if f["kind"] == "metin").most_common()))
    add("")
    add("## 1. Talimat dosyalari")
    add("")
    add("| Dosya | Yazar beyani | Tarih/surum/kaynak | Kural benzeri | Degisme | Not |")
    add("|---|---|---|---|---|---|")
    for f in tal:
        au = "; ".join("%s [%s]" % (cell(v, 80), w) for _, v, w in f["authors"][:2]) or "-"
        me = "; ".join(cell(v, 60) for _, v in f["meta"][:3]) or "-"
        note = "icerikten talimat sayildi" if f["promoted"] else ""
        add("| `%s` | %s | %s | %d | %s | %s |" % (cell(f["rel"]), au, me, f["n_rules"], tstr(f["mtime"]), note))
    add("")
    for f in tal:
        add("### `%s`" % cell(f["rel"]))
        add("")
        add("- Boyut %d bayt, kodlama %s, son degisme %s, SHA-256 `%s`" % (f["size"], f["enc"], tstr(f["mtime"]), f["sha"]))
        if f["authors"]:
            add("- Yazar/hazirlayan beyani: " + "; ".join("%s: %s [%s]" % (y, cell(v, 160), w) for y, v, w in f["authors"]))
        if f["meta"]:
            add("- Tarih/surum/kaynak: " + "; ".join("%s: %s" % (y, cell(v, 160)) for y, v in f["meta"]))
        if f["prec"]:
            add("- Oncelik ifadeleri:")
            for y, u in f["prec"][:30]:
                add("  - %s: %s" % (y, cell(u)))
        if f["refs"]:
            add("- Yol referanslari: " + "; ".join("`%s` (%s)" % (cell(p, 160), "VAR" if ok else "BULUNAMADI") for p, ok in f["refs"]))
        if f["refs_int"]:
            add("- Adi gecen klasor dosyalari: " + ", ".join("`%s`" % n for n in f["refs_int"][:40]))
        if sum(f["hidden"].values()) or f["html"] or f["mdc"]:
            add("- GIZLI ICERIK: gorunmez=%s, HTML yorum=%d, Markdown yorum=%d" % (dict(f["hidden"]), len(f["html"]), len(f["mdc"])))
            for c in (f["html"] + f["mdc"])[:10]:
                add("  - `%s`" % cell(c, 400))
        add("- Kural benzeri cumleler (%d farkli, %d gecis):" % (len(f["rules"]), f["n_rules"]))
        for y, u, n in f["rules"][:300]:
            k = f["rule_counts"][n]
            add("  - %s: %s%s" % (y, cell(u), " (x%d)" % k if k > 1 else ""))
        add("")
        add("<details><summary>Tam metin</summary>")
        add("")
        add("````")
        add(vis(f["text"][:FULLTEXT_MAX]))
        if len(f["text"]) > FULLTEXT_MAX:
            add("... (%d karakter daha)" % (len(f["text"]) - FULLTEXT_MAX))
        add("````")
        add("</details>")
        add("")
    add("## 2. Ayni adli talimat dosyalari")
    add("")
    add("Ana varyanta benzerlik yuksekse (%60 ve uzeri) ayni dosyanin birbirinden kaymis kopyalaridir;"
        " dusukse ayni adli farkli belgelerdir.")
    add("")
    if not diverged:
        add("Ayni adda birden fazla talimat dosyasi yok.")
    for nm, group, variants, ratios in diverged:
        if len(variants) == 1:
            add("- `%s`: %d dosya, hepsi ayni icerik." % (nm, len(group)))
            continue
        drift = any(r >= 0.6 for r in ratios)
        add("- `%s`: %d dosya, %d farkli icerik -> %s" % (
            nm, len(group), len(variants), "**KAYMA: kopyalar birbirinden ayrismis**" if drift else "ayni adli farkli belgeler"))
        for i, v in enumerate(variants, 1):
            sim = "" if i == 1 else " (ana varyanta benzerlik %%%d)" % round(100 * ratios[i - 2])
            add("  - varyant %d%s (%d dosya): %s" % (i, sim, len(v), ", ".join(
                "`%s` (%s)" % (cell(x["rel"]), tstr(x["mtime"])) for x in v)))
        ref = variants[0][0]
        for v, r in zip(variants[1:], ratios):
            if r < 0.6:
                continue
            d, more = short_diff(ref["text"], v[0]["text"], ref["rel"], v[0]["rel"], 60)
            add("")
            add("```diff")
            add(vis("\n".join(d)))
            if more:
                add("... (%d satir daha)" % more)
            add("```")
        add("")
    add("")
    add("## 3. Sessiz otorite: talimatlarda olmayan kural cumleleri")
    add("")
    add("Talimat disi dosyalarda gecen, hicbir talimat dosyasinda (alinti olarak bile) bulunmayan kural benzeri cumleler.")
    add("Eski ajan notlari yeni ajanlara kural gibi gorunebilir; bu liste o adaylardir.")
    add("")
    holders = sorted((f for f in files if f.get("new_rules")), key=lambda f: -len(f["new_rules"]))
    add("| Dosya | Tur | Yeni kural (farkli) | Gecis | Talimattan alinti | Son degisme |")
    add("|---|---|---|---|---|---|")
    for f in holders:
        add("| `%s` | %s | %d | %d | %d | %s |" % (cell(f["rel"]), f["cat"], len(f["new_rules"]),
                                                sum(c for _, _, c in f["new_rules"]), f["quoted"], tstr(f["mtime"])))
    add("")
    for f in holders[:30]:
        add("### `%s`" % cell(f["rel"]))
        for y, u, c in f["new_rules"][:15]:
            add("- %s: %s%s" % (y, cell(u), " (x%d)" % c if c > 1 else ""))
        if len(f["new_rules"]) > 15:
            add("- ... %d cumle daha" % (len(f["new_rules"]) - 15))
        add("")
    add("## 4. Konu bazinda kurallar")
    add("")
    add("Ayni konudaki kurallar yan yana; once talimat dosyalari. Celiski olup olmadigina buradan bakilabilir.")
    add("")
    for ad, _ in KONULAR:
        items = sorted(topics.get(ad, []), key=lambda x: (x[0] != "talimat", x[1]))
        if not items:
            continue
        add("### %s (%d)" % (ad, len(items)))
        for cat, rel, y, u in items[:60]:
            add("- [%s] `%s` %s: %s" % (cat, cell(rel, 120), y, cell(u)))
        if len(items) > 60:
            add("- ... %d cumle daha" % (len(items) - 60))
        add("")
    add("## 5. Son %d gunde degisen dosyalar (%d)" % (gun, len(recent)))
    add("")
    for f in recent:
        add("- %s  [%s]  `%s`" % (tstr(f["mtime"]), f["cat"], cell(f["rel"])))
    add("")
    add("## 6. Temel karsilastirmasi")
    add("")
    if cmp_res is None:
        add(base_info)
    else:
        added, removed, changed, diffs = cmp_res
        add(base_info)
        add("")
        add("- Eklenen (%d): " % len(added) + ", ".join("`%s`" % cell(r) for r in added))
        add("- Silinen (%d): " % len(removed) + ", ".join("`%s`" % cell(r) for r in removed))
        add("- Degisen (%d): " % len(changed) + ", ".join("`%s`" % cell(r) for r in changed))
        for r, (d, more) in diffs.items():
            add("")
            add("#### `%s`" % cell(r))
            add("```diff")
            add(vis("\n".join(d)))
            if more:
                add("... (%d satir daha)" % more)
            add("```")
    add("")
    add("## 7. Birebir kopyalar (%d grup)" % len(copies))
    add("")
    for g in copies[:40]:
        add("- %d bayt: " % g[0]["size"] + ", ".join("`%s`" % cell(f["rel"]) for f in g))
    add("")
    add("## 8. Gizli icerik (tum dosyalar)")
    add("")
    hid = [f for f in files if sum(f["hidden"].values()) or f["html"] or f["mdc"]]
    if not hid:
        add("Gorunmez karakter, HTML yorumu veya Markdown yorumu iceren dosya yok.")
    for f in hid:
        add("- `%s`: gorunmez=%s, HTML yorum=%d, Markdown yorum=%d" % (cell(f["rel"]), dict(f["hidden"]), len(f["html"]), len(f["mdc"])))
    add("")
    add("## 9. Tum dosyalar")
    add("")
    add("| Dosya | Tur | Boyut | Kodlama | Son degisme | Kural benzeri (farkli/gecis) | Ajan/model adi |")
    add("|---|---|---|---|---|---|---|")
    for f in files:
        add("| `%s` | %s | %d | %s | %s | %d/%d | %d |" % (cell(f["rel"]), f["cat"], f["size"], f["enc"], tstr(f["mtime"]),
                                                       len(f["rules"]), f["n_rules"], f["agent_mentions"]))
    body = "\n".join(L) + "\n"
    Path(path).write_text(body, encoding="utf-8")
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Calisma ortami metin analizi (salt-okunur)")
    ap.add_argument("kok", nargs="?", default=str(DEFAULT_ROOT))
    ap.add_argument("--ek", nargs="*", default=None, help="kok disindaki ek talimat dosyalari")
    ap.add_argument("--talimat", nargs="*", default=[], help="talimat sayilacak ek yol desenleri (regex)")
    ap.add_argument("--gun", type=int, default=3, help="son kac gunde degisenler listelensin")
    ap.add_argument("--rapor", default="ortam_analizi.md")
    ap.add_argument("--temel", default="ortam_temel.json")
    ap.add_argument("--temel-kaydet", action="store_true", help="simdiki hali temel olarak kaydet")
    a = ap.parse_args()

    root = Path(a.kok)
    if not root.is_dir():
        print("Klasor bulunamadi:", root)
        return 2
    for out in (a.rapor, a.temel):
        if inside(out, root):
            print("Cikti dosyasi taranan klasorun icinde olamaz:", out)
            return 2
    extra_pats = [re.compile(fold(x)) for x in a.talimat]
    extras = [Path(x) for x in a.ek] if a.ek is not None else [x for x in DEFAULT_EXTRA if x.is_file()]

    files = []
    for p in iter_files(root):
        rel = str(p.relative_to(root))
        try:
            files.append(analyze_file(p, rel, extra_pats))
        except Exception as e:  # tek bir garip dosya taramayi durdurmasin
            print("ATLANDI: %s (%s: %s)" % (p, type(e).__name__, e))
    for x in extras:
        try:
            f = analyze_file(x, "[ek] " + str(x), [re.compile(".*")])
            f["cat"] = "talimat"
            f["text"] = f["text"] if f["text"] is not None else ""
            files.append(f)
        except Exception as e:
            print("EK OKUNAMADI: %s (%s)" % (x, e))

    root_names = {fold(Path(f["rel"].replace("\\", "/")).name) for f in files
                  if not f["rel"].startswith("[ek]") and len(Path(f["rel"]).name) >= 6 and "." in Path(f["rel"]).name}
    topics, diverged, copies = cross_checks(files, root_names)
    now = time.time()
    recent = sorted((f for f in files if f["mtime"] >= now - a.gun * 86400), key=lambda f: -f["mtime"])

    cmp_res, base_info = None, "Temel yok. Talimatlar istedigin haldeyken --temel-kaydet ile kaydet."
    if Path(a.temel).is_file():
        try:
            base = json.loads(Path(a.temel).read_text(encoding="utf-8"))
            cmp_res = compare_baseline(base, files)
            base_info = "Temel: `%s` (%s)" % (a.temel, base.get("olusturma"))
            if base.get("kok") != str(root):
                base_info += " -- UYARI: temel baska bir klasorden alinmis: %s" % base.get("kok")
        except (ValueError, OSError, KeyError) as e:
            base_info = "Temel okunamadi: %s" % e

    rsha = write_report(a.rapor, root, extras, files, topics, diverged, copies, recent, a.gun, cmp_res, base_info)

    # --- ekran ozeti
    cats = Counter(f["cat"] for f in files)
    tal = [f for f in files if f["cat"] == "talimat"]
    print("CALISMA ORTAMI ANALIZI v%s" % VERSION)
    print("Kok:", root)
    if extras:
        print("Ek talimat:", ", ".join(str(x) for x in extras))
    print("Dosya: %d | %s" % (len(files), " | ".join("%s=%d" % (c, cats[c]) for c in CATS)))
    print("Kodlama:", ", ".join("%s=%d" % kv for kv in Counter(f["enc"] for f in files if f["kind"] == "metin").most_common()))
    print("-" * 72)
    print("TALIMAT DOSYALARI (%d)" % len(tal))
    for f in tal:
        au = f["authors"][0][2] + ": " + vis(f["authors"][0][1])[:50] if f["authors"] else "yazar beyani yok"
        print("  %-52s kural=%-4d %s | %s" % (vis(f["rel"])[:52], len(f["rules"]), tstr(f["mtime"]), au))
    missing = [(f["rel"], p) for f in tal for p, ok in f["refs"] if not ok]
    if missing:
        print("  Bulunamayan yol referanslari:")
        for rel, p in missing[:10]:
            print("    %s -> %s" % (vis(rel)[:40], vis(p)))
    print("AYNI ADLI TALIMATLAR")
    if not diverged:
        print("  yok")
    for nm, group, variants, ratios in diverged:
        if len(variants) == 1:
            state = "hepsi ayni"
        elif any(r >= 0.6 for r in ratios):
            state = "KAYMA: %d farkli icerik (rapor bolum 2)" % len(variants)
        else:
            state = "ayni adli farkli belgeler"
        print("  %s: %d dosya, %s" % (nm, len(group), state))
    print("SESSIZ OTORITE (talimatlarda olmayan kural cumleleri)")
    holders = sorted((f for f in files if f.get("new_rules")), key=lambda f: -len(f["new_rules"]))
    print("  %d farkli cumle / %d dosya. En cok (farkli cumle, toplam gecis):" % (
        sum(len(f["new_rules"]) for f in holders), len(holders)))
    for f in holders[:8]:
        print("    %4d %7d  [%s] %s" % (len(f["new_rules"]), sum(c for _, _, c in f["new_rules"]), f["cat"], vis(f["rel"])[:62]))
    hid = [f for f in files if sum(f["hidden"].values()) or f["html"] or f["mdc"]]
    print("GIZLI ICERIK: %d dosya%s" % (len(hid), "" if not hid else " -> " + ", ".join(vis(f["rel"])[:40] for f in hid[:5])))
    print("SON %d GUNDE DEGISEN: %d dosya (%d talimat)" % (a.gun, len(recent), sum(f["cat"] == "talimat" for f in recent)))
    for f in recent[:12]:
        print("    %s  %-10s %s" % (tstr(f["mtime"]), f["cat"], vis(f["rel"])[:70]))
    if cmp_res is None:
        print("TEMEL:", base_info)
    else:
        added, removed, changed, diffs = cmp_res
        print("TEMELE GORE: eklenen=%d silinen=%d degisen=%d" % (len(added), len(removed), len(changed)))
        for r in changed[:12]:
            print("    DEGISTI: %s%s" % (vis(r)[:70], "  (satir farki raporda)" if r in diffs else ""))
        for r in added[:6]:
            print("    EKLENDI: %s" % vis(r)[:70])
        for r in removed[:6]:
            print("    SILINDI: %s" % vis(r)[:70])
    if a.temel_kaydet:
        save_baseline(a.temel, root, files)
        print("Temel kaydedildi:", Path(a.temel).resolve())
    print("-" * 72)
    print("Ayrintili rapor:", Path(a.rapor).resolve())
    print("Rapor SHA-256:", rsha)
    return 0


if __name__ == "__main__":
    sys.exit(main())
