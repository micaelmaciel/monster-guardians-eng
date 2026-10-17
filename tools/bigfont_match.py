#!/usr/bin/env python3
"""Match 16x11 bigfont glyphs (ROM 0xD3144, 22 bytes/glyph) against the
known 8x8 font (ROM 0xBEDF0, 32 bytes/glyph) to bootstrap a charmap.

The bigfont is a larger rendering of the same character set. We downsample
each bigfont glyph to 8x8 (2x2 block majority) and search the 8x8 font for
the best match by ink-mask Hamming distance. Also report top-N candidates.

Usage:
  bigfont_match.py <bigfont_index> [...]        show matches for indices
  bigfont_match.py --all-used <msg_a> <msg_b>   all glyphs used in a message range
  bigfont_match.py --table                      full table of 685 glyphs
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

ROM = os.path.join(os.path.dirname(__file__), "..", "rom", "monster-guardians.gba")
BIG_BASE = 0xD3144
BIG_STRIDE = 22
SMALL_BASE = 0xBEDF0
SMALL_STRIDE = 32
RAW = os.path.join(os.path.dirname(__file__), "..", "build", "story_messages_raw.json")


def load_rom():
    with open(ROM, "rb") as f:
        return f.read()


def big_rows(data, idx):
    """16 columns x 11 rows of 0/1."""
    g = data[BIG_BASE + idx * BIG_STRIDE: BIG_BASE + (idx + 1) * BIG_STRIDE]
    if len(g) < BIG_STRIDE:
        return None
    rows = []
    for r in range(8):
        left, right = g[r], g[8 + r]
        rows.append([(left >> (7 - p)) & 1 for p in range(8)] +
                    [(right >> (7 - p)) & 1 for p in range(8)])
    for r in range(3):
        left, right = g[16 + r], g[19 + r]
        rows.append([(left >> (7 - p)) & 1 for p in range(8)] +
                    [(right >> (7 - p)) & 1 for p in range(8)])
    return rows


def big_mask_8x8(data, idx):
    """Downsample bigfont glyph to 8x8 ink mask (64-bit)."""
    rows = big_rows(data, idx)
    if rows is None:
        return None
    m = 0
    for by in range(8):
        for bx in range(8):
            # map output cell (bx,by) to a 2x~1.4 block of the 16x11 source
            x0 = int(bx * 2)
            y0 = int(round(by * 11 / 8))
            y1 = max(y0 + 1, int(round((by + 1) * 11 / 8)))
            ink = 0
            n = 0
            for y in range(y0, min(y1 + 1, 11)):
                for x in range(x0, min(x0 + 2, 16)):
                    ink += rows[y][x]
                    n += 1
            m = (m << 1) | (1 if ink * 2 >= n else 0)
    return m


def small_mask(data, idx):
    m = 0
    for y in range(8):
        base = SMALL_BASE + idx * SMALL_STRIDE + y * 4
        for b in range(4):
            byte = data[base + b]
            m = (m << 1) | (1 if (byte & 0xF) else 0)
            m = (m << 1) | (1 if (byte >> 4) else 0)
    return m


def load_small_all(data):
    return {i: small_mask(data, i) for i in range(512)}


def load_charmap():
    with open(os.path.join(os.path.dirname(__file__), "..", "data", "charmap.json")) as f:
        return json.load(f)


def best(data, masks, big_idx, n=5):
    bm = big_mask_8x8(data, big_idx)
    if bm is None:
        return []
    scored = sorted(masks.items(), key=lambda kv: (bm ^ kv[1]).bit_count())
    return [(i, (bm ^ m).bit_count()) for i, m in scored[:n]]


def main():
    data = load_rom()
    masks = load_small_all(data)
    cm = load_charmap()

    def char_of(code):
        v = cm.get(f"0x{code:03X}")
        if v is None:
            return "?"
        return v if isinstance(v, str) else v[0]

    if "--table" in sys.argv:
        for i in range(685):
            cands = best(data, masks, i, 3)
            top = " ".join(f"{char_of(c)}({d})" for c, d in cands)
            print(f"{i:4d} 0x{i:03X}: {top}")
        return

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--all-used" in sys.argv:
        # collect glyph indices used in message range
        with open(RAW) as f:
            raw = json.load(f)
        lo, hi = int(args[0]), int(args[1])
        uniq = set()
        for m in raw["messages"][lo:hi + 1]:
            for t in m["raw"]:
                v = int(t, 16)
                if v < 0x1000:
                    uniq.add(v)
        idxs = sorted(uniq)
    else:
        idxs = [int(a, 16) if a.startswith("0x") else int(a) for a in args]

    for i in idxs:
        cands = best(data, masks, i, 6)
        top = " ".join(f"{char_of(c)}[{c:02X}]({d})" for c, d in cands)
        print(f"{i:4d} 0x{i:03X}: {top}")


if __name__ == "__main__":
    main()
