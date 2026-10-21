#!/usr/bin/env python3
"""Insert the English 8x8 translation into the ROM copy.

Reads `build/8x8_corpus.tsv` plus `translation/8x8_*_en.tsv` and encodes
every EN row with the game's own 8x8 glyph codes (charmap, JP punctuation
glyphs, `U+23CE` line break -> 0x1FF).

Storage styles (see `tools/extract_8x8.py`):

  field  monster-DB / item record name: 16-byte field at record+0, at most
         8 codes, zero padded (full names carry no terminator)
  split  merged pool runs cut into labels that are read at fixed byte
         offsets: the exact JP code count must be kept, space padded
  slice  packed pool pieces that each own a pointer: fit in place (space
         padded) or relocate with pointer + draw-count immediates patched
  len    {u32 ptr, u16 len, u16 b} pool strings: len field patched to the
         EN code count
  term   0x0000-terminated strings: in place when the EN fits the JP code
         count, otherwise relocated with every pointer occurrence patched

Rows that cannot be handled safely (over-length fixed-width pieces with no
pointer of their own) are reported as BLOCKED; they stay in Japanese until
the translation is shortened.

Usage:
  insert_8x8.py --check            # plan + report only
  (build_patch.py --stage 8x8 applies it through its Patcher)
"""
import argparse
import json
import os
import re
import struct
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import charmap  # noqa: E402

CORPUS = os.path.join(ROOT, "build", "8x8_corpus.tsv")
TRANS = os.path.join(ROOT, "translation")
REPORT = os.path.join(ROOT, "build", "patch", "8x8_report.json")
ROM_PATH = os.path.join(ROOT, "rom", "monster-guardians.gba")

BASE = 0x08000000
NL = "\u23ce"
RAW_CODE = re.compile(r"\{([0-9A-Fa-f]{2,4})\}")
FIELD_MAX = 8

# English punctuation -> closest 8x8 glyph (the font has no ASCII
# punctuation; these are the fullwidth/CJK marks, all 8x8 fixed width).
PUNCT = {
    ".": 0x0E4,   # ．
    ",": 0x0E3,   # ，
    "!": 0x0E9,   # ！
    "?": 0x0E8,   # ？
    ":": 0x0E6,   # ：
    ";": 0x0E7,   # ；
    "'": 0x111,   # ” (apostrophe-ish mark)
    '"': 0x111,
    "(": 0x0FE,   # （
    ")": 0x0FF,   # ）
    "-": 0x0EF,   # −
    "/": 0x0EB,   # ／
    "+": 0x0EE,   # ＋
    "~": 0x0ED,   # 〜
    "%": 0x0F9,   # ％
    "&": 0x0FB,   # ＆
    "#": 0x0FA,   # ＃
    "$": 0x0F8,   # ＄
    "@": 0x0FD,   # ＠
    "[": 0x114,   # ［
    "]": 0x115,   # ］
    "{": 0x118,   # ｛
    "}": 0x119,   # ｝
    "<": 0x0F5,   # ＜
    ">": 0x0F6,   # ＞
    "=": 0x0F3,   # ＝
    "*": 0x0FC,   # ＊
    "\\": 0x0EC,  # ＼
}

SPACE = 0x001
LINEBREAK = 0x1FF

# Rows that stay in Japanese on purpose (name-entry kana row label).
KANA_ALLOW = {"0x0BCC44"}


def load_charmap():
    cm = charmap.load()
    rev = {}
    for code, ch in cm.items():
        if isinstance(ch, str) and len(ch) == 1:
            rev.setdefault(ch, code)
    return rev


class Encoder:
    def __init__(self):
        self.rev = load_charmap()

    def encode(self, text):
        out = []
        i = 0
        while i < len(text):
            m = RAW_CODE.match(text, i)
            if m:
                out.append(int(m.group(1), 16))
                i = m.end()
                continue
            ch = text[i]
            if ch == NL:
                out.append(LINEBREAK)
            elif ch in self.rev:
                out.append(self.rev[ch])
            elif ch in PUNCT:
                out.append(PUNCT[ch])
            else:
                raise SystemExit(f"unencodable 8x8 character {ch!r} in {text!r}")
            i += 1
        return out


def load_corpus(path=CORPUS):
    rows = {}
    with open(path, encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            rows[p[0]] = {
                "addr": p[0],
                "region": p[1],
                "style": p[2],
                "n": int(p[3]),
                "suffix": int(p[4]),
                "refs": int(p[5]),
                "sources": [s for s in p[6].split(",") if s],
                "text": p[7],
            }
    return rows


def load_rows(corpus=None, trans_dir=TRANS):
    corpus = corpus or load_corpus()
    enc = Encoder()
    rows = []
    for name in sorted(os.listdir(trans_dir)):
        if not (name.startswith("8x8_") and name.endswith("_en.tsv")):
            continue
        with open(os.path.join(trans_dir, name), encoding="utf-8") as fh:
            next(fh)
            for line in fh:
                p = line.rstrip("\n").split("\t")
                if len(p) != 4:
                    raise SystemExit(f"{name}: bad TSV row {line!r}")
                addr, n, jp, en = p
                c = corpus.get(addr)
                if c is None:
                    raise SystemExit(f"{name}: {addr} not in corpus")
                if c["text"] != jp:
                    raise SystemExit(f"{name}: {addr} JP column mismatch")
                codes = enc.encode(en)
                row = dict(c)
                row.update(kind=classify(c), n_jp=int(n), jp=jp, en=en,
                           codes=codes, en_len=len(codes))
                rows.append(row)
    rows.sort(key=lambda r: int(r["addr"], 16))
    return rows


def classify(c):
    region, style = c["region"], c["style"]
    if region.startswith("mdb") or region == "item":
        return "field"
    if style == "split":
        return "split"
    if region == "mobile":
        return "mobile"
    if style == "slice":
        return "slice"
    if style == "len":
        return "len"
    if style == "term":
        return "term"
    raise SystemExit(f"unknown style {style!r} at {c['addr']}")


# ---------------------------------------------------------------- pointers
def pointer_hits(rom, addr):
    """Every 2-aligned u32 equal to BASE+addr (pointer slots and literals)."""
    want = struct.pack("<I", BASE + addr)
    hits = []
    pos = rom.find(want)
    while pos >= 0:
        if pos % 2 == 0:
            hits.append(pos)
        pos = rom.find(want, pos + 1)
    return hits


def _h(rom, off):
    return rom[off] | (rom[off + 1] << 8)


def find_loads(rom, site, back=0x600, fwd=0x200):
    """Thumb `ldr rX,[pc,#imm]` instructions whose literal is at `site`."""
    out = []
    for a in range(max(0, site - back), min(len(rom) - 2, site + fwd), 2):
        h = _h(rom, a)
        if (h & 0xF800) == 0x4800:
            target = ((a + 4) & ~3) + (h & 0xFF) * 4
            if target == site:
                out.append(a)
    return out


def thumb_len(h):
    """Instruction length in bytes for a Thumb halfword."""
    return 4 if (h & 0xF800) in (0xE800, 0xF000, 0xF800) else 2


def encode_movs(rom, off, value):
    """Re-encode a Thumb `movs Rd,#imm8` with a new immediate, keeping Rd.

    Count patches must stay instructions: writing the bare value over the
    halfword turns `movs r1,#9` (09 21) into `lsls r2,r1,#0` (0a 00) and the
    draw call then runs off into code.  Only the low immediate byte changes.
    """
    if not 0 <= value <= 0xFF:
        raise ValueError(f"count {value} does not fit an imm8 at {off:#x}")
    h = _h(rom, off)
    if (h & 0xF800) != 0x2000:
        raise ValueError(
            f"count site {off:#x} is not `movs Rd,#imm` (halfword {h:#06x})")
    return struct.pack("<H", (h & 0xFF00) | value)


DRAW_FN = 0x3D114
WRAP_SPAN = 0x40

# Draw-count immediates the dataflow scan cannot reach: the count sits behind a
# conditional branch / DMA wait loop before the draw call, or is fed to a
# custom buffer writer instead of DRAW_FN.  They are still real `movs` counts
# and must be widened when the row relocates to a longer EN string.
# addr -> (count-site offsets, ...) holding the JP glyph count
EXTRA_COUNT_SITES = {
    # はい Yes.  Besides the direct draw counts, four question-box builders
    # copy the JP length into a text-slot field (movs #2; strh ...), so the
    # scanner cannot see them next to a draw call.  Left unpatched they clip
    # the English "Yes" to "Ye".
    "0x0BD3A2": (0x41A12, 0x41E04, 0x42DA4, 0x4893A, 0x4D5C0, 0x4DB74,
                 0x5FAB2),
    # へんせいをつづける Edit again.  Third option of the "End editing and
    # apply it?" party box; the builder writes the JP length into the slot
    # field (movs #9; strh ...) and the draw itself is a tail call, so the
    # scanner bails out.  Left unpatched, "Edit again" clips to "Edit agai".
    "0x0BE2D0": (0x41A8C,),
    "0x0BD3D0": (0x5EBFE,),                    # なまえ Name (combine result)
    "0x0BE298": (0x2971E,),                    # たいき Idle (training row)
    "0x0BE29E": (0x29748,),                    # しゅつげき Deploy (training row)
}


def add_extra_counts(r, rom):
    """Merge manual count sites into a row, guarded by the JP immediate."""
    extra = EXTRA_COUNT_SITES.get(r["addr"])
    if not extra:
        return
    for off in extra:
        h = _h(rom, off)
        if (h & 0xF800) != 0x2000 or (h & 0xFF) != r["n_jp"]:
            raise SystemExit(
                f"extra count site {off:#x} for {r['addr']}: expected "
                f"movs #{r['n_jp']}, got {h:#06x}")
    r["count_sites"] = sorted(set(r.get("count_sites", [])) | set(extra))


def _is_bl(h):
    return (h & 0xF800) == 0xF000


def _is_b(h):
    return (h & 0xF800) == 0xE000


def _is_bcond(h):
    return (h & 0xF000) == 0xD000 and (h & 0x0F00) != 0x0F00


def _is_branch(h):
    return _is_bl(h) or _is_b(h) or _is_bcond(h) or (h & 0xFF00) == 0xDF00


def _b_target(rom, a):
    s = _h(rom, a) & 0x7FF
    if s & 0x400:
        s -= 0x800
    return (a + 4 + s * 2) & 0xFFFFFF


def _bl_target(rom, a):
    h1, h2 = _h(rom, a), _h(rom, a + 2)
    s = (h1 >> 10) & 1
    imm10 = h1 & 0x3FF
    imm11 = h2 & 0x7FF
    j1 = (h2 >> 13) & 1
    j2 = (h2 >> 11) & 1
    i1 = 1 - (j1 ^ s)
    i2 = 1 - (j2 ^ s)
    imm = (s << 24) | (i1 << 23) | (i2 << 22) | (imm10 << 12) | (imm11 << 1)
    if imm & (1 << 24):
        imm -= 1 << 25
    return (a + 4 + imm) & 0xFFFFFF


def decode(rom, start, end):
    """(addr, halfword, size) for the instruction stream at a synced start."""
    out = []
    a = start
    while a + 2 <= min(end, len(rom)):
        h = _h(rom, a)
        size = thumb_len(h)
        if a + size > end:
            break
        out.append((a, h, size))
        a += size
    return out


def sync_back(rom, start, span=0x180):
    """Earliest offset that decodes exactly onto `start` (instruction sync)."""
    best = start
    for cand in range(start - 2, max(0, start - span) - 1, -2):
        a = cand
        while a < start:
            a += thumb_len(_h(rom, a))
        if a == start:
            best = cand
    return best


def _writes_reg(h, reg):
    """True when the halfword may write `reg`; used to bound back-tracing."""
    if (h & 0xE000) == 0x0000:                       # shifts/add/sub imm
        if (h & 0x1800) == 0x1800:                    # add/sub immediate
            return reg == (h & 7)
        op = (h >> 11) & 3
        if op == 1:                                   # cmp: no write
            return False
        return reg == (h & 7)
    if (h & 0xE000) == 0x2000:                       # movs/cmp/adds/subs imm8
        op = (h >> 11) & 3
        if op == 1:
            return False
        return reg == ((h >> 8) & 7)
    if (h & 0xFC00) == 0x4000:                       # ALU register ops
        op = (h >> 6) & 0xF
        if op in (8, 10, 11):                         # tst/cmp/cmn
            return False
        return reg == (h & 7)
    if (h & 0xFC00) == 0x4400:                       # hi-reg add/cmp/mov/bx
        op = (h >> 8) & 3
        if op in (1, 3):
            return False
        return reg == ((h & 7) | (((h >> 7) & 1) << 3))
    if (h & 0xF800) == 0x4800:                       # ldr Rd,[pc]
        return reg == ((h >> 8) & 7)
    if (h & 0xF000) == 0x5000:                       # load/store reg offset
        return bool(h & 0x800) and reg == (h & 7)
    if (h & 0xF000) in (0x6000, 0x7000, 0x8000):     # ldr/ldrb/ldrh imm
        return bool(h & 0x800) and reg == (h & 7)
    if (h & 0xF000) == 0x9000:                       # ldr/str [sp]
        return bool(h & 0x800) and reg == ((h >> 8) & 7)
    if (h & 0xF000) == 0xA000:                       # add Rd,pc/sp
        return reg == ((h >> 8) & 7)
    if (h & 0xF600) == 0xB400:                       # push
        return False
    if (h & 0xF600) == 0xBC00:                       # pop
        return bool((h >> reg) & 1) if reg < 8 else False
    if (h & 0xF000) == 0xC000:                       # ldmia
        return bool(h & 0x800) and bool((h >> reg) & 1) if reg < 8 else False
    if (h & 0xF000) == 0xB000 or (h & 0xF000) == 0xF000:
        return False
    return False


def find_count_site(inss, use_idx, reg):
    """Locate the `movs` that defines the count register before it is stored."""
    j = use_idx - 1
    while j >= 0:
        a, h, _size = inss[j]
        if _is_bl(h):
            # AAPCS: r0-r3/lr are clobbered, r4-r11 survive across calls.
            if reg < 4:
                return None
            j -= 1
            continue
        if _is_branch(h):
            return None
        if (h & 0xFC00) == 0x4400 and ((h >> 8) & 3) == 2:   # mov Rd,Rs
            d = (h & 7) | (((h >> 7) & 1) << 3)
            s = (h >> 3) & 0xF
            if d == reg:
                reg = s
                j -= 1
                continue
        if _writes_reg(h, reg):
            if (h & 0xF800) == 0x2000 and ((h >> 8) & 7) == reg:
                return a
            return None
        j -= 1
    return None


def _wrapper_count(rom, target):
    """`str rY,[sp]; bl 0x3D114` tail-call wrapper -> rY."""
    inss = decode(rom, target, target + 12)
    if len(inss) >= 2:
        h0 = inss[0][1]
        h1 = inss[1][1]
        if ((h0 & 0xF000) == 0x9000 and not (h0 & 0x800)
                and _is_bl(h1) and _bl_target(rom, inss[1][0]) == DRAW_FN):
            return (h0 >> 8) & 7
    return None


def _struct_count(inss, idx, n_jp):
    """Message setup: pointer stored at [base+8], glyph count byte at [base+3].

    Setup blocks write the text pointer into a message object and load the
    glyph count as an immediate right after it:
        ldr r0,=text
        str r0,[r1,#8]
        movs r0,#21
        strb r0,[r1,#3]
    The later draw reads both fields back from the object.
    """
    if n_jp is None:
        return None
    h = inss[idx][1]
    if (h & 0xF800) != 0x4800:
        return None
    ptr = (h >> 8) & 7
    base = None
    j = idx
    for j in range(idx + 1, min(len(inss), idx + 12)):
        hj = inss[j][1]
        if (hj & 0xF800) == 0x6000 and not (hj & 0x800):
            rt, rn = hj & 7, (hj >> 3) & 7
            off = ((hj >> 6) & 0x1F) * 4
            if rt == ptr and off == 8:
                base = rn
                break
    if base is None:
        return None
    for k in range(j + 1, min(len(inss), j + 12)):
        hk = inss[k][1]
        if (hk & 0xF800) == 0x2000 and (hk & 0xFF) == n_jp:
            rz = (hk >> 8) & 7
            for m in range(k + 1, min(len(inss), k + 4)):
                hm = inss[m][1]
                if ((hm & 0xF800) == 0x7000 and not (hm & 0x800)
                        and (hm & 7) == rz
                        and ((hm >> 3) & 7) == base
                        and ((hm >> 6) & 0x1F) == 3):
                    return inss[k][0]
            for m in range(k + 1, min(len(inss), k + 3)):
                if _is_branch(inss[m][1]):
                    return inss[k][0]
    return None


def analyze_draw(rom, load_off, n_jp=None, span=WRAP_SPAN):
    """Find the draw/setup fed by a string-pointer literal load.

    Returns (call_addr, count_site, note).  `count_site` is the `movs` that
    supplies the glyph count when it is a plain immediate; None means the
    count could not be tied to an immediate (free length or dynamic).
    """
    start = sync_back(rom, max(0, load_off - 0x120))
    inss = decode(rom, start, load_off + span)
    first = next((i for i, (a, _h2, _s) in enumerate(inss) if a == load_off), None)
    if first is None:
        return (None, None, "load not decoded")
    h0 = inss[first][1]
    dreg = (h0 >> 8) & 7

    block, branch = [], None
    for i in range(first + 1, min(len(inss), first + 16)):
        a, h, _size = inss[i]
        block.append((i, a, h))
        if _is_bl(h) or _is_b(h) or _is_bcond(h):
            branch = (i, a, h)
            break

    for i, a, h in block:
        if _is_bl(h):
            target = _bl_target(rom, a)
            if target == DRAW_FN:
                site, _note = _count_of_call(inss, i, None)
                if site is not None:
                    return (a, site, "draw arg")
            wr = _wrapper_count(rom, target)
            if wr is not None:
                site, _note = _count_of_call(inss, i, wr)
                if site is not None:
                    return (a, site, "draw arg")
        elif _is_b(h):
            wr = _wrapper_count(rom, _b_target(rom, a))
            if wr is not None:
                site, _note = _count_of_call(inss, i, wr)
                if site is not None:
                    return (a, site, "draw arg")

    site = _struct_count(inss, first, n_jp)
    if site is not None:
        return (inss[first][0], site, "struct count")

    if n_jp is not None:
        for _i, a, h in block:
            if (h & 0xF800) == 0x2000 and (h & 0xFF) == n_jp:
                z = (h >> 8) & 7
                if z != dreg and dreg == 1 and z == 2:
                    return (a, a, "call arg")

    if branch is None:
        return (None, None, "no draw call in window")
    _i, a, h = branch
    if _is_bcond(h):
        return (a, None, "conditional branch")
    return (a, None, "tail-call")


def _count_of_call(inss, i, reg):
    """Resolve the 5th argument at call index i (or the register in `reg`)."""
    if reg is None:
        j = i - 1
        while j >= 0:
            h = inss[j][1]
            if (h & 0xF000) == 0x9000 and not (h & 0x800):
                reg = (h >> 8) & 7
                break
            j -= 1
        if reg is None:
            return (None, "no [sp] count store")
    else:
        j = i
    site = find_count_site(inss, j, reg)
    if site is None:
        return (None, "dynamic count")
    return (site, "ok")


def find_count_imms(rom, site, n_jp, span=28):
    """Count immediates for a string address (draw-call dataflow based).

    Returns (sites, notes): `sites` are `movs` offsets whose immediate equals
    `n_jp`; `notes` describe pointer loads whose draw could not be resolved.
    """
    sites, notes = [], []
    for load in find_loads(rom, site):
        call, csite, note = analyze_draw(rom, load, n_jp)
        if csite is None:
            if note not in ("no draw call in window",):
                notes.append((load, call, note))
            continue
        imm = _h(rom, csite) & 0xFF
        if imm == n_jp:
            sites.append(csite)
        else:
            notes.append((load, call, f"immediate {imm} != {n_jp}"))
    return sites, notes


# ---------------------------------------------------------------- planning
def plan(rows, rom):
    """Decide the treatment for every row (no ROM writes)."""
    for r in rows:
        addrs = r["addr"]
        a = int(addrs, 16)
        hits = pointer_hits(rom, a) if r["en_len"] > r["n_jp"] or r["kind"] in (
            "term", "len", "slice") else []
        r["ptr_hits"] = hits
        n, L, kind = r["n_jp"], r["en_len"], r["kind"]

        orig = [struct.unpack_from("<H", rom, a + 2 * i)[0] for i in range(L)]
        if orig == r["codes"]:
            r["action"] = "identical"
            continue

        if kind == "field":
            if L <= FIELD_MAX:
                r["action"] = "field"
                r["write_len"] = min(L + 1, FIELD_MAX)
            else:
                r["action"] = "blocked"
                r["why"] = f"field EN {L} > {FIELD_MAX}"
            continue

        if kind in ("split", "mobile"):
            if L <= n:
                r["action"] = "inplace"
                r["write_len"] = n
            else:
                r["action"] = "blocked"
                r["why"] = f"{kind} EN {L} > {n} (fixed width, no relocation)"
            continue

        if kind == "slice":
            if L <= n:
                r["action"] = "inplace"
                r["write_len"] = n
            elif hits:
                r["action"] = "reloc"
                sites, notes = [], []
                for h in hits:
                    s, nt = find_count_imms(rom, h, n)
                    sites += s
                    notes += nt
                r["count_sites"] = sorted(set(sites))
                r["count_notes"] = notes
                add_extra_counts(r, rom)
            else:
                r["action"] = "blocked"
                r["why"] = f"slice EN {L} > {n} and no pointer"
            continue

        if kind == "len":
            r["count_sites"] = [int(s, 16) + 4 for s in r["sources"]]
            if L <= n:
                r["action"] = "inplace"
                r["write_len"] = n
            elif hits:
                r["action"] = "reloc"
            else:
                r["action"] = "blocked"
                r["why"] = f"len EN {L} > {n} and no pointer"
            continue

        if kind == "term":
            if L <= n:
                r["action"] = "inplace"
                r["write_len"] = L + 1
            elif hits:
                r["action"] = "reloc"
                sites, notes = [], []
                for h in hits:
                    s, nt = find_count_imms(rom, h, n)
                    sites += s
                    notes += nt
                r["count_sites"] = sorted(set(sites))
                r["count_notes"] = notes
                add_extra_counts(r, rom)
            else:
                r["action"] = "blocked"
                r["why"] = f"term EN {L} > {n} and no pointer"
            continue
    return rows


def overlaps(rows):
    """In-place write ranges that collide (start, end, row)."""
    spans = []
    for r in rows:
        if r["action"] != "inplace":
            continue
        a = int(r["addr"], 16)
        spans.append((a, a + 2 * r["write_len"], r["addr"], r["kind"]))
    spans.sort()
    out = []
    for i in range(1, len(spans)):
        if spans[i][0] < spans[i - 1][1]:
            out.append((spans[i - 1], spans[i]))
    return out


# ---------------------------------------------------------------- apply
def blob_for(r, relocate):
    codes = list(r["codes"])
    if r["kind"] == "field":
        n = min(len(codes) + 1, FIELD_MAX)
        codes = codes[:FIELD_MAX]
        if len(codes) < FIELD_MAX:
            codes = codes + [0]
        return struct.pack(f"<{len(codes)}H", *codes)
    if r["kind"] == "len" and not relocate:
        codes = codes + [SPACE] * (r["n_jp"] - len(codes))
        return struct.pack(f"<{len(codes)}H", *codes)
    if r["kind"] in ("split", "mobile"):
        codes = codes + [SPACE] * (r["n_jp"] - len(codes))
        return struct.pack(f"<{len(codes)}H", *codes)
    if r["kind"] == "slice" and not relocate:
        codes = codes + [SPACE] * (r["n_jp"] - len(codes))
        return struct.pack(f"<{len(codes)}H", *codes)
    codes = codes + [0]
    return struct.pack(f"<{len(codes)}H", *codes)


def apply(p, rows, report_only=False):
    """Write the plan through a Patcher-like object."""
    rom = p.orig
    enc_rows = plan(rows, rom)
    bad = [r for r in enc_rows if r["action"] == "blocked"]
    for r in enc_rows:
        if r["action"] == "field":
            blob = blob_for(r, False)
            p.poke(int(r["addr"], 16), blob, f"8x8 field {r['addr']} {r['en']!r}")
        elif r["action"] == "inplace":
            blob = blob_for(r, False)
            p.poke(int(r["addr"], 16), blob,
                   f"8x8 in place {r['addr']} {r['en']!r}")
            if r["kind"] == "len":
                for off in r["count_sites"]:
                    p.poke(off, struct.pack("<H", r["en_len"]),
                           f"8x8 len {r['addr']} -> {r['en_len']}")
        elif r["action"] == "reloc":
            blob = blob_for(r, True)
            dst = p.alloc(len(blob), f"8x8 {r['kind']} {r['addr']}", align=2)
            p.poke(dst, blob, f"8x8 reloc {r['addr']} {r['en']!r}")
            for h in r["ptr_hits"]:
                p.poke_u32(h, BASE | dst, f"8x8 ptr {r['addr']} @ {h:#x}")
            if r["kind"] == "len":
                for off in r["count_sites"]:
                    p.poke(off, struct.pack("<H", r["en_len"]),
                           f"8x8 len {r['addr']} -> {r['en_len']}")
            else:
                for off in r.get("count_sites", []):
                    p.poke(off, encode_movs(rom, off, r["en_len"]),
                           f"8x8 count {r['addr']} -> {r['en_len']}")
            r["new_addr"] = dst
    return enc_rows, bad


def summarize(rows):
    by = Counter()
    for r in rows:
        by[(r["kind"], r["action"])] += 1
    return by


def report(rows, extra=None):
    by = summarize(rows)
    print("8x8 insertion plan")
    for (kind, action), c in sorted(by.items()):
        print(f"  {kind:7s} {action:8s} {c:4d}")
    blocked = [r for r in rows if r["action"] == "blocked"]
    if blocked:
        print(f"  blocked: {len(blocked)}")
        for r in blocked:
            print(f"    {r['addr']} {r['kind']:6s} n={r['n_jp']:2d} "
                  f"en={r['en_len']:2d} {r['why']}")
    ov = overlaps(rows)
    if ov:
        print(f"  inline overlaps: {len(ov)}")
        for a, b in ov:
            print(f"    0x{a[0]:06X}-0x{a[1]:06X} {a[3]} {a[2]}  /  "
                  f"0x{b[0]:06X}-0x{b[1]:06X} {b[3]} {b[2]}")
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    doc = {
        "summary": {f"{k[0]}/{k[1]}": v for k, v in by.items()},
        "rows": [
            {k: r[k] for k in ("addr", "region", "kind", "n_jp", "en_len",
                               "action", "en")
             if k in r}
            | ({"why": r["why"]} if "why" in r else {})
            | ({"new_addr": r["new_addr"]} if "new_addr" in r else {})
            | ({"ptr_hits": len(r.get("ptr_hits", []))})
            | ({"count_sites": [f"0x{x:06X}" for x in r["count_sites"]]}
               if r.get("count_sites") else {})
            for r in rows
        ],
        "blocked": [r["addr"] for r in blocked],
        "overlaps": [{"a": a[2], "b": b[2]} for a, b in ov],
    }
    if extra:
        doc.update(extra)
    with open(REPORT, "w") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")
    print(f"  report -> {os.path.relpath(REPORT, ROOT)}")
    return by, blocked, ov


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--rom", default=ROM_PATH)
    args = ap.parse_args()
    rom = open(args.rom, "rb").read()
    rows = load_rows()
    plan(rows, rom)
    report(rows)
    blocked = [r for r in rows if r["action"] == "blocked"]
    # sanity: blocked rows must at least encode
    for r in blocked:
        if any(c is None for c in r["codes"]):
            raise SystemExit(f"blocked row {r['addr']} has unencodable codes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
