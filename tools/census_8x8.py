#!/usr/bin/env python3
"""Pointer census for the 8x8-text window 0x099B40..0x0C6E00.

Collects every halfword-aligned 32-bit value in the ROM that points into the
window (text/code pointers are halfword-aligned; odd hits are byte-value
coincidences) and lists the source offsets.  Matches the reference collection
in tools/extract_8x8.py so the census and the corpus stay consistent.
"""
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LO, HI, BASE = 0x099B40, 0x0C6E00, 0x08000000

ROM = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "rom", "monster-guardians.gba")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "build", "8x8_ptrs.tsv")

data = open(ROM, "rb").read()
refs = defaultdict(list)
for off in range(0, len(data) - 8, 2):
    p = int.from_bytes(data[off:off + 4], "little") - BASE
    if LO <= p < HI and p % 2 == 0:
        refs[p].append(off)

with open(OUT, "w") as f:
    f.write("target\tnrefs\tsources\n")
    for p in sorted(refs):
        f.write(f"0x{p:06X}\t{len(refs[p])}\t" + ",".join(f"0x{o:06X}" for o in refs[p]) + "\n")

print(f"{len(refs)} targets -> {os.path.relpath(OUT, ROOT)}")
