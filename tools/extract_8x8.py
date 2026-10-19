#!/usr/bin/env python3
"""Build the 8x8 direct-code text corpus from the ROM.

Text lives in the window 0x099B40..0x0C6E00 as 16-bit glyph codes
(0x0000 terminator, 0x1FF line break). Three storage styles:

  term  0x0000-terminated strings (message banks)
  len   packed pool strings; length from an 8-byte {ptr,len,b} entry
  slice packed pool strings with no length entry; extent = up to the
        next known string start in the same pool (best effort)
  split known merged pool runs cut into their constituent labels
        (sub-strings are accessed by base+offset in code, so a
        translation must keep the pieces contiguous)

String acceptance:
  * referenced starts (plain pointer / {ptr,len,b} target / DB-walk name)
  * clean starts (right after 0x0000): kana >= 1 and n >= 2
  * monster-DB regions: kana >= 2 (names), plus DB-walk positions
  * mobile region (0x099B40..0x099D90): referenced + manual starts only
  * dropped: 1-code runs, box-art strings, all other junk

Output: build/8x8_corpus.tsv
  addr  region  style  n  suffix  refs  sources  text

Usage: extract_8x8.py [rom] [out.tsv]
"""
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import charmap  # noqa: E402

ROM = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "rom", "monster-guardians.gba")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "build", "8x8_corpus.tsv")
LO, HI = 0x099B40, 0x0C6E00
BASE = 0x08000000
CAP = 400

# mobile-region (tournament UI) fixed-width fields with no pointer of their
# own; starts identified by inspection (fields are space-padded, the
# surrounding labels are referenced)
MANUAL_STARTS = [
    0x099BE8,                                # クラス
    0x099C00,                                # しょうきん  0G
    0x099C34, 0x099C68, 0x099C9C, 0x099CD0,  # しょうきん 300G/600G/200G/100G
    0x099CE2,                                # さんかできないモンスターが ...
    0x099D2A, 0x099D34, 0x099D3E,            # かち / まけ / ひきわけ
    0x099D4A,                                # Lv (ranking column)
    0x099D4E, 0x099D54, 0x099D5C, 0x099D68,  # NEW / LOAD / OPTION / START
    # pool strings reached only via code-baked offsets (no pointer of their own;
    # found by the uncovered-span audit)
    0x0BD388,                                # COMPLETE
    0x0BD46E,                                # きしょう|いどう|ひこう (split below)
    0x0BDD08,                                # パーティがしゅぎょうにいっています
    0x0BE264,                                # へんせいされていません|しようできるめいれい
]

# merged pool runs: start -> constituent label lengths (codes).  The pieces
# follow each other with no terminator and are drawn via base+offset in
# code, so they must stay contiguous in any relocation.
SPLITS = {
    0x0BD3B6: [4, 4, 5],        # ステージ|けってい|キャンセル
    0x0BD3EC: [3, 4],           # EXP|けっとう
    0x0BD48A: [1, 5, 4, 7],     # G|モンスター|アイテム|ブリーフィング
    0x0BD4AC: [2, 4],           # PP|USED
    0x0BDF04: [10, 15],         # モンスターがいません|アイテムのソウビを...
    0x0BE350: [18, 11],         # パーティから⏎はずして...|はずして...
    0x0BE3DA: [8, 4, 18],       # いったい...(?)はずして|はいぞく|...
    0x0BE45A: [24, 20],         # げんざいのパーティから⏎...|...
    0x0BE4DE: [9, 14],          # ポジションへんこう|ポジションを...
    0x0BE53C: [4, 26],          # はいぶん|パラメータが⏎...
    0x0BE922: [9, 5],           # パスワードさくじょ|スピーカー
    0x0BE94A: [5, 4, 4],        # こうかおん|モノラル|ステレオ
    0x0BE9E4: [11, 17, 15, 17], # ほんとうに...|セーブは...|サウンドの...|この...
    0x0BDB52: [5, 20, 21],      # 未選択|あたらしいじょうほうは...|しゅぎょうから...
    0x0BD46E: [4, 3, 3],        # きしょう|いどう|ひこう
    0x0BE264: [11, 10],         # へんせいされていません|しようできるめいれい
}

# monster DB record lists: (start, end, stride)
MDB_WALKS = [
    (0x0AEDE8, 0x0AFCDE, 0x30),
    (0x0AFCDE, 0x0B0B7C, 0x34),
    (0x0B0B7C, 0x0B271C, 0x34),
    (0x0B271C, 0x0B3900, 0x34),
    (0x0B3900, 0x0B4A00, 0x34),
    (0x0B4A00, 0x0B5728, 0x34),
]

data = open(ROM, "rb").read()
tab = charmap.load()
BOX = "┌┐└┘│─├┤┬┴┼═║╔╗╚╝"


def w(off):
    if off + 1 >= len(data):
        return None
    return data[off] | (data[off + 1] << 8)


def read_term(p, cap=CAP):
    codes = []
    for k in range(cap):
        v = w(p + 2 * k)
        if v is None or v == 0:
            return codes, v == 0
        codes.append(v)
    return codes, False


def codes_at(p, n):
    c = [w(p + 2 * k) for k in range(n)]
    if any(x is None or not (1 <= x < 0x300) for x in c):
        return None
    return c


def is_pool(a):
    return (0x0B7200 <= a < 0x0B8000) or (0x0BD000 <= a < 0x0BF000)


def region(a):
    if 0x099B40 <= a < 0x099D90:
        return "mobile"
    if 0x09D000 <= a < 0x0A1108:
        return "net"
    if 0x0A1108 <= a < 0x0A2000:
        return "report"
    if 0x0A7000 <= a < 0x0AA000:
        return "shop"
    if 0x0AA000 <= a < 0x0AED00:
        return "aa"
    if 0x0AED00 <= a < 0x0AF900:
        return "mdb1"
    if 0x0AF900 <= a < 0x0B0B7C:
        return "mdb2"
    if 0x0B0B7C <= a < 0x0B271C:
        return "mdb3"
    if 0x0B271C <= a < 0x0B3900:
        return "mdb4"
    if 0x0B3900 <= a < 0x0B4A00:
        return "mdb5"
    if 0x0B4A00 <= a < 0x0B5728:
        return "mdb6"
    if 0x0B5728 <= a < 0x0B6300:
        return "item"
    if 0x0B7200 <= a < 0x0B8000:
        return "idesc"
    if 0x0B8000 <= a < 0x0BAA00:
        return "b8xxx"
    if 0x0BAA00 <= a < 0x0BB000:
        return "tables"
    if 0x0BB000 <= a < 0x0BD000:
        return "bbxxx"
    if 0x0BD000 <= a < 0x0BF000:
        return "pool"
    if 0x0C3000 <= a < 0x0C5000:
        return "c3xxx"
    if 0x0C5000 <= a < 0x0C5D9C:
        return "mapdata"
    if 0x0C5D9C <= a < 0x0C6000:
        return "map"
    if 0x0C6000 <= a < 0x0C6E00:
        return "battle"
    return "other"


# sub-ranges that hold graphics/font/table data, not display text
EXCLUDED = (
    (0x0A1108, 0x0A12AC),   # report-bank prefix (font rows)
    (0x0A9740, 0x0A9C34),   # font chart (bitmap rows + glyph lists)
    (0x0C3000, 0x0C5D9C),   # graphics + map data tables
    (0x099D90, 0x09D000),   # mobile-region bitmask/timer tables
    (0x0C6E00, 0x0C7400),   # name-input keyboard cells (outside HI)
    (0x0B7A40, 0x0B8000),   # item-desc tail: kana composition table (data)
    (0x0BAB60, 0x0BAB8C),   # script data before beast-name pointer tables
    (0x0BAC20, 0x0BAC40),   # script data (decodes as "1 " and junk)
    (0x0BCB60, 0x0BCC28),   # input-grid glyph-code lists (data)
    (0x0A95BC, 0x0A9690),   # password-checksum blob between shop messages
    (0x0A8DE4, 0x0A902A),   # password-input ASCII/glyph tables (before CL/BS/OK)
    (0x0A9EE0, 0x0AA000),   # shop-region pointer/keyboard data block
)
CLEAN_OK = ("net", "report", "shop", "item", "map", "battle")  # + mdb*


# ---------- references ----------
refs = defaultdict(list)
lenmap = defaultdict(list)
for off in range(0, len(data) - 8, 2):
    p = int.from_bytes(data[off:off + 4], "little") - BASE
    if LO <= p < HI and p % 2 == 0:  # text/code pointers are halfword-aligned;
        refs[p].append(off)          # odd hits are byte-value coincidences
        a = w(off + 4)
        b = w(off + 6)
        if b <= 0xFF and 1 <= a <= 300:
            lenmap[p].append((a, off))

# ---------- terminated runs at every 2-aligned offset ----------
runs = {}
p = LO
while p + 2 < min(HI, len(data)):
    codes, ok = read_term(p, CAP)
    if ok and codes and all(1 <= c < 0x300 for c in codes):
        runs[p] = codes
    p += 2

by_term = defaultdict(list)
for p, c in runs.items():
    by_term[p + 2 * len(c)].append(p)
suffix = set()
for t, ps in by_term.items():
    if len(ps) > 1:
        ps.sort()
        suffix.update(ps[:-1])


def kana_count(codes):
    n = 0
    for c in codes:
        ch = tab.get(c)
        if ch:
            o = ord(ch[0])
            if 0x3040 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF:
                n += 1
    return n


def punct_count(text):
    n = 0
    for ch in text:
        o = ord(ch)
        if 0x3000 <= o <= 0x303F or 0xFF01 <= o <= 0xFF60:
            n += 1
    return n


def unmapped_count(codes):
    n = 0
    for c in codes:
        if c not in tab:
            n += 1
    return n


# ---------- monster DB walks ----------
def kana_in_text(s):
    return any(0x3040 <= ord(ch) <= 0x30FF or 0x4E00 <= ord(ch) <= 0x9FFF for ch in s)


walk_names = {}  # addr -> codes
for mlo, mhi, stride in MDB_WALKS:
    rec = mlo
    while rec < mhi:
        for off in range(rec, rec + min(stride - 2, 0x18), 2):
            codes = []
            q = off
            while q < rec + stride and len(codes) < 16:
                v = w(q)
                if v is None or v == 0:
                    break
                codes.append(v)
                q += 2
            if codes and w(q) == 0 and 1 <= len(codes) <= 14 and all(1 <= c < 0x300 for c in codes):
                if kana_in_text(charmap.decode(codes, tab)):
                    walk_names[off] = codes
                    break
        rec += stride

starts = sorted({r for r in runs if not is_pool(r)} | set(refs) | set(lenmap) | set(walk_names) | set(MANUAL_STARTS))
declared = set(refs) | set(lenmap) | set(walk_names) | set(MANUAL_STARTS)


def extent(p):
    if region(p) == "mobile":
        # one big unterminated block of fixed-width fields; boundaries
        # come from referenced/manual starts
        nxt = [s for s in declared if p < s <= p + 0x100]
        if nxt:
            c = codes_at(p, (min(nxt) - p) // 2)
            if c:
                return c, "slice"
        if p in runs:
            return runs[p], "term"
        return None
    pool = is_pool(p)
    if pool:
        if p in lenmap:
            a = max(l for l, _ in lenmap[p])
            c = codes_at(p, a)
            if c:
                return c, "len"
        if p in runs:
            end = p + 2 * len(runs[p])
            if not any(p < s < end for s in starts):
                return runs[p], "term"
        nxt = [s for s in starts if p < s <= p + 0x100]
        if nxt:
            c = codes_at(p, (min(nxt) - p) // 2)
            if c:
                return c, "slice"
        if p in runs:
            return runs[p], "term"
        return None
    if p in runs:
        return runs[p], "term"
    if p in lenmap:
        a = max(l for l, _ in lenmap[p])
        c = codes_at(p, a)
        if c:
            return c, "len"
    nxt = [s for s in starts if p < s <= p + 0x100]
    if nxt:
        c = codes_at(p, (min(nxt) - p) // 2)
        if c:
            return c, "slice"
    return None


def at_name_pos(p):
    """True when p sits on a monster-DB record start (name field position)."""
    for mlo, mhi, stride in MDB_WALKS:
        if mlo <= p < mhi and (p - mlo) % stride == 0:
            return True
    return False


def accept(p, codes, text):
    refd = p in refs or p in lenmap or p in walk_names
    reg = region(p)
    clean = p >= 2 and w(p - 2) == 0
    kana = kana_count(codes)
    pauld = kana + punct_count(text)
    if len(codes) < 2:
        return refd and pauld >= 1
    if p in MANUAL_STARTS:
        return True
    if reg == "mobile":
        return refd or p in MANUAL_STARTS
    if reg == "other":
        return False
    if reg == "item" and (p - 0x0B5728) % 0x40:
        return False  # item names live at 0x40-stride record starts only
    if reg.startswith("mdb") and len(codes) == 2 and not refd \
            and w(p - 2) == 0 and w(p + 4) == 0 and not at_name_pos(p):
        return False  # per-record parameter field between two terminators
    if refd:
        if unmapped_count(codes) >= 2 and pauld == 0 and not is_pool(p):
            return False
        return True
    if reg.startswith("mdb"):
        return (clean and kana >= 2) or p in walk_names
    if reg in CLEAN_OK and clean:
        return kana >= 1
    return False


rows = []
for p in starts:
    res = extent(p)
    if not res:
        continue
    codes, style = res
    if not codes:
        continue
    if any(lo <= p < hi for lo, hi in EXCLUDED):
        continue
    text = charmap.decode(codes, tab).replace("\t", " ").replace("\n", "⏎")
    if any(ch in BOX for ch in text):
        continue
    reg = region(p)
    if reg.startswith("mdb") or reg == "item":
        if reg == "item":
            codes = codes[:8]  # name field is 8 codes; later record fields follow
        # strip trailing item-index / field digits merged into the name run
        while codes and 0x0002 <= codes[-1] <= 0x000B:
            codes = codes[:-1]
        if reg.startswith("mdb"):
            if codes == [0x00E0, 0x0080]:
                continue  # constant per-record parameter field (decodes as ヴめ)
            if len(codes) == 2 and codes[0] in (0x00E0, 0x0180, 0x01C0) \
                    and codes[1] in (0x0040, 0x0080, 0x00A0):
                continue  # same field family in the other DBs (百ケ / ヴぁ / {1C0}ケ)
            # fusion/monster records: name starts at the first name-like code
            for i, c in enumerate(codes):
                ch = tab.get(c)
                if (ch and (0x3040 <= ord(ch[0]) <= 0x30FF or 0x4E00 <= ord(ch[0]) <= 0x9FFF)) \
                        or 0x1A0 <= c <= 0x1C0:
                    codes = codes[i:]
                    p += 2 * i
                    break
        if len(codes) < 2:
            continue
        text = charmap.decode(codes, tab).replace("\t", " ").replace("\n", "⏎")
    if p in SPLITS:
        off = p
        total = sum(SPLITS[p])
        if total > len(codes):
            print(f"WARN: split mismatch at 0x{p:06X}: have {len(codes)}, want {total}")
            continue
        for ln in SPLITS[p]:
            c2 = codes_at(off, ln)
            if c2:
                t2 = charmap.decode(c2, tab).replace("\t", " ").replace("\n", "⏎")
                if not any(ch in BOX for ch in t2):
                    rows.append((off, "split", len(c2), 1 if off in suffix else 0,
                                 refs.get(off, []) if off == p else [], t2))
            off += 2 * ln
        rem = len(codes) - total
        if rem > 0:
            c2 = codes_at(off, rem)
            if c2:
                t2 = charmap.decode(c2, tab).replace("\t", " ").replace("\n", "⏎")
                if not any(ch in BOX for ch in t2):
                    rows.append((off, "split", len(c2), 1 if off in suffix else 0, [], t2))
        continue
    if not accept(p, codes, text):
        continue
    srcs = refs.get(p, [])
    rows.append((p, style, len(codes), 1 if p in suffix else 0, srcs, text))

# collapse rows that converged on the same address+text (mdb field-prefix strip
# can map several record offsets onto one name); keep the best-referenced copy
merged = {}
order = []
for r in rows:
    key = (r[0], r[5])
    if key in merged:
        if len(r[4]) > len(merged[key][4]):
            merged[key] = r
    else:
        merged[key] = r
        order.append(key)
rows = [merged[k] for k in order]

# mdb walks record a suffix when a record boundary falls inside a name; drop
# unreferenced rows that are strict sub-spans of a longer mdb row
spans = [(r[0], r[0] + 2 * r[2]) for r in rows if region(r[0]).startswith("mdb")]
drop = set()
for i, r in enumerate(rows):
    if not region(r[0]).startswith("mdb") or r[4]:
        continue
    a0, a1 = r[0], r[0] + 2 * r[2]
    if any(b0 <= a0 and a1 <= b1 and (b1 - b0) > (a1 - a0) for b0, b1 in spans):
        drop.add(i)
rows = [r for i, r in enumerate(rows) if i not in drop]

with open(OUT, "w") as f:
    f.write("addr\tregion\tstyle\tn\tsuffix\trefs\tsources\ttext\n")
    for p, style, n, suf, srcs, text in rows:
        src = ",".join(f"0x{s:06X}" for s in srcs[:4])
        f.write(f"0x{p:06X}\t{region(p)}\t{style}\t{n}\t{suf}\t{len(srcs)}\t{src}\t{text}\n")

# ---------- stats ----------
byreg = defaultdict(Counter)
for p, style, n, suf, srcs, text in rows:
    byreg[region(p)][style] += 1
print(f"corpus rows: {len(rows)}  (wrote {os.path.relpath(OUT, ROOT)})")
for reg in sorted(byreg):
    c = byreg[reg]
    print(f"  {reg:7s} {sum(c.values()):4d}  term={c.get('term',0):4d} len={c.get('len',0):3d} slice={c.get('slice',0):3d}")

nref = sum(1 for r in rows if r[4])
print(f"referenced rows: {nref};  walk names: {len(walk_names)}")
unmapped = Counter()
for p, style, n, suf, srcs, text in rows:
    for m in re.finditer(r"\{([0-9A-F]+)\}", text):
        c = int(m.group(1), 16)
        if c < 0x200:
            unmapped[c] += 1
print(f"unmapped low glyph codes in use: {len(unmapped)}")
for c, n in unmapped.most_common(48):
    print(f"   0x{c:03X} x{n}")

# ---------- coverage audit: kana clean runs outside the window ----------
kana_codes = set()
for c, s in tab.items():
    o = ord(s[0])
    if 0x3040 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF:
        kana_codes.add(c)
hits = Counter()
d = data
p = 2
while p + 2 < len(d):
    if (d[p] | (d[p + 1] << 8)) in kana_codes and not (LO <= p < HI) \
            and d[p - 2] == 0 and d[p - 1] == 0:
        codes2, ok = read_term(p, 64)
        if ok and len(codes2) >= 2 and all(1 <= c < 0x300 for c in codes2) and kana_count(codes2) >= 1:
            hits[p >> 12] += 1
    p += 2
print("kana clean runs outside window (by 0x1000 page):")
for page in sorted(hits):
    print(f"  0x{page * 0x1000:06X}: {hits[page]}")
