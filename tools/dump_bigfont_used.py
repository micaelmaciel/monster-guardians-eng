#!/usr/bin/env python3
"""Dump ASCII art of bigfont glyphs used by given story messages.

Usage: dump_bigfont_used.py <msg_lo> <msg_hi> [outfile]
Reads build/story_messages_raw.json, collects glyph indices (<0x1000) used in
messages msg_lo..msg_hi inclusive, prints each glyph's 16x11 art labeled with
its index and first-seen order, sorted by index.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from probe_bigfont import glyph_rows, BASE, STRIDE

HERE = os.path.dirname(__file__)
ROM = os.path.join(HERE, "..", "rom", "monster-guardians.gba")
RAW = os.path.join(HERE, "..", "build", "story_messages_raw.json")

lo, hi = int(sys.argv[1]), int(sys.argv[2])
outfile = sys.argv[3] if len(sys.argv) > 3 else None

data = open(ROM, "rb").read()
raw = json.load(open(RAW))
uniq = set()
for m in raw["messages"][lo:hi + 1]:
    for t in m["raw"]:
        v = int(t, 16)
        if v < 0x1000:
            uniq.add(v)

lines = []
for i in sorted(uniq):
    rows = glyph_rows(data, BASE + i * STRIDE)
    lines.append(f"=== idx {i:4d} 0x{i:03X} ===")
    lines.extend("".join("#" if b else "." for b in r) for r in rows)
    lines.append("")

text = "\n".join(lines)
if outfile:
    with open(outfile, "w") as f:
        f.write(text + "\n")
    print("wrote", outfile, f"({len(uniq)} glyphs)")
else:
    print(text)
