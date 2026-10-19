#!/usr/bin/env python3
"""Extract the R1 story-system support region (0xCF52C..0xCFB82) from the ROM.

R1 sits between the scenario/sequence tables and the story message banks and
holds the story system's support text:

  0xCF52C  stale copy of the opening message (no pointers into it found;
           the leading words look damaged)
  0xCF58C  test scene ("テスト..." prefix); referenced from the event table
           (0xC8D08) with a second entry point 0xCF6F4 from 0x6EB2F4
  0xCF7A6  debug digit strip (０１２３...」」」) + research scene variant
  0xCF8C0  scene variant using "「ティーナ」" where messages insert the
           player name
  0xCF9A0  message-renderer fragments (▼, 、。, bracket variants, ～)
  0xCF9C4  debug prompts (BG/フェイスチェック用)
  0xCFA18  "AB"
  0xCFA1E  753E beast-name strings (18 = 9 slots x 2 variants)
  0xCFB40  753F word-table strings (8 = 4 slots x 2 variants)
  0xCFB82  name-input charset table (512 x u16), referenced from 0x8140C

Strings are 0x7FFF-terminated token streams exactly like the story banks.
0x0000 is the glyph 神 in the message banks; here it only appears in the
stale opening copy.

The tool verifies:
  * exactly EXPECTED_COUNT 0x7FFF-terminated segments between START and END
  * every 753E/753F table entry points at a segment start in this region
  * the name-input charset has CHARSET_COUNT entries
and records every ROM pointer (2-byte-aligned, u32) into the region, so the
referenced (displayed) and unreferenced (stale/debug) parts stay separated.

Usage: python tools/extract_r1.py [--check]
    --check   only verify, do not write build/r1_text_raw.json
"""
import array
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ROM = os.path.join(ROOT, "rom", "monster-guardians.gba")
OUT = os.path.join(ROOT, "build", "r1_text_raw.json")
CHARMAP = os.path.join(ROOT, "data", "bigfont_charmap.json")

START = 0xCF52C
END = 0xCFB82
EXPECTED_COUNT = 37
CTL_END = 0x7FFF

NAME_TABLE = 0xC7410      # 753E: 18 ptrs = 9 slots x 2 (0=male, 1=female)
NAME_COUNT = 18
WORD_TABLE = 0xC73F0      # 753F: 8 ptrs = 4 slots x 2 (0=male, 1=female)
WORD_COUNT = 8
CHARSET = 0xCFB82
CHARSET_COUNT = 512

BASE = 0x08000000

# Control-code parameter counts (verified in-game / by extraction).
PARAMS = {
    0x7530: 0, 0x7531: 0, 0x7532: 0, 0x7533: 0, 0x7534: 1,
    0x7535: 2, 0x7536: 0, 0x7537: 1, 0x7538: 2, 0x7539: 2,
    0x753A: 0, 0x753B: 1, 0x753C: 0, 0x753E: 1, 0x753F: 1,
    0x7540: 0, 0x7541: 0, 0xFFFF: 0,
}


def load_rom():
    with open(ROM, "rb") as f:
        return f.read()


def segments(data, start, end):
    """Split [start, end) into (offset, tokens) segments at 0x7FFF."""
    out = []
    o = start
    begin = None
    while o < end:
        v = struct.unpack_from("<H", data, o)[0]
        if v == CTL_END:
            if begin is not None:
                out.append((begin, [struct.unpack_from("<H", data, x)[0]
                                    for x in range(begin, o, 2)]))
                begin = None
        elif begin is None:
            begin = o
        o += 2
    if begin is not None:
        raise SystemExit(f"unterminated segment from 0x{begin:06X}")
    return out


def decode(toks, bc):
    """Best-effort decode with insert markers (for readability only)."""
    parts = []
    i = 0
    while i < len(toks):
        t = toks[i]
        if t >= 0x1000:
            n = PARAMS.get(t, 0)
            ps = toks[i + 1:i + 1 + n]
            if t == 0x7540:
                parts.append("«P»")
            elif t == 0x753F:
                parts.append(f"«W{ps[0] if ps else '?'}»")
            elif t == 0x753E:
                parts.append(f"«BE{ps[0] if ps else '?'}»")
            else:
                arg = ",".join(str(p) for p in ps)
                parts.append(f"[{t:04X}{':' + arg if arg else ''}]")
            i += 1 + n
        else:
            e = bc.get(str(t))
            parts.append((e or {}).get("char") or f"<{t:03X}>")
            i += 1
    return "".join(parts)


def ptr_refs(data, start, end):
    """All 2-byte-aligned u32 pointer values into [start, end).

    Returns {target: [src, ...]}.  Both even and odd-2 alignments are
    scanned so packed 16-bit tables cannot hide a reference.
    """
    refs = {}
    for shift in (0, 2):
        n = (len(data) - shift) // 4 * 4
        arr = array.array("I")
        arr.frombytes(data[shift:shift + n])
        for i, v in enumerate(arr):
            if BASE <= v < BASE + len(data):
                t = v - BASE
                if start <= t < end:
                    refs.setdefault(t, []).append(i * 4 + shift)
    return refs


def table_entries(data, table_off, count, seg_text, problems):
    """Resolve a u32 pointer table into this region."""
    entries = []
    for idx in range(count):
        src = table_off + idx * 4
        v = struct.unpack_from("<I", data, src)[0]
        t = v - BASE if v >= BASE else None
        text = seg_text.get(t)
        if text is None:
            print(f"FAIL: table 0x{table_off:06X}[{idx}] -> 0x{v:08X} "
                  f"is not a segment start")
            problems += 1
            text = "?"
        entries.append({
            "idx": idx, "slot": idx // 2, "variant": idx % 2,
            "ptr_src": f"0x{src:06X}",
            "target": f"0x{t:06X}" if t is not None else None,
            "text": text,
        })
    return entries


def main():
    check_only = "--check" in sys.argv
    data = load_rom()
    bc = json.load(open(CHARMAP))["entries"]

    segs = segments(data, START, END)
    problems = 0
    if len(segs) != EXPECTED_COUNT:
        print(f"FAIL: found {len(segs)} segments, expected {EXPECTED_COUNT}")
        problems += 1
    if struct.unpack_from("<H", data, END - 2)[0] != CTL_END:
        print("FAIL: byte pair before region end is not a 0x7FFF terminator")
        problems += 1

    seg_text = {off: decode(toks, bc) for off, toks in segs}

    name_table = table_entries(data, NAME_TABLE, NAME_COUNT, seg_text,
                               problems)
    word_table = table_entries(data, WORD_TABLE, WORD_COUNT, seg_text,
                               problems)

    charset = [struct.unpack_from("<H", data, CHARSET + i * 2)[0]
               for i in range(CHARSET_COUNT)]
    odd = sorted({v for v in charset if v >= 0x1000})
    if odd:
        print(f"note: charset values >= 0x1000: {[hex(v) for v in odd]}")

    refs = ptr_refs(data, START, END)
    unresolved = sorted(t for t in refs if t not in seg_text)
    if unresolved:
        print(f"note: pointers into mid-segment/meta offsets: "
              f"{[hex(t) for t in unresolved]}")

    print(f"segments: {len(segs)}; name table: {len(name_table)}; "
          f"word table: {len(word_table)}; pointer targets: {len(refs)}")
    for off, toks in segs:
        hit = sorted({t for t in refs if off <= t < off + len(toks) * 2})
        if hit:
            srcs = sorted(s for t in hit for s in refs[t])
            print(f"  0x{off:06X} len={len(toks):3d} refs from "
                  f"{[hex(s) for s in srcs]}")

    if problems:
        print("problems found; not writing")
        return 1
    if check_only:
        print("check OK")
        return 0

    segs_doc = []
    for off, toks in segs:
        hit = sorted({t for t in refs if off <= t < off + len(toks) * 2})
        segs_doc.append({
            "off": f"0x{off:06X}",
            "len": len(toks),
            "raw": [f"0x{t:X}" for t in toks],
            "text": seg_text[off],
            "refs": [{"src": f"0x{s:06X}", "target": f"0x{t:06X}"}
                     for t in hit for s in refs[t]],
        })

    doc = {
        "region": {"start": f"0x{START:06X}", "end": f"0x{END:06X}"},
        "count": len(segs_doc),
        "segments": segs_doc,
        "name_table": {"off": f"0x{NAME_TABLE:06X}", "entries": name_table},
        "word_table": {"off": f"0x{WORD_TABLE:06X}", "entries": word_table},
        "charset": {"off": f"0x{CHARSET:06X}", "count": CHARSET_COUNT,
                    "values": charset},
    }
    with open(OUT, "w") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"wrote {OUT} ({len(segs_doc)} segments)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
