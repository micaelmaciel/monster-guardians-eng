#!/usr/bin/env python3
"""Print bigfont glyphs side by side in groups for reading.

Usage: bigfont_groups.py <idx> [<idx> ...]  |  --range lo hi
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from probe_bigfont import glyph_rows, BASE, STRIDE

data = open(os.path.join(os.path.dirname(__file__), "..", "rom",
                         "monster-guardians.gba"), "rb").read()

if sys.argv[1] == "--range":
    idxs = list(range(int(sys.argv[2]), int(sys.argv[3]) + 1))
else:
    idxs = [int(a, 16) if a.lower().startswith("0x") else int(a) for a in sys.argv[1:]]

for i in range(0, len(idxs), 4):
    grp = idxs[i:i + 4]
    arts = []
    for k in grp:
        rows = glyph_rows(data, BASE + k * STRIDE)
        arts.append(["".join("#" if b else "." for b in r) for r in rows])
    print("idx " + " ".join(f"{k:16d}" for k in grp))
    for r in range(11):
        print("    " + " ".join(a[r] for a in arts))
    print()
