#!/usr/bin/env python3
"""Render bigfont story messages from build/story_messages_raw.json as ASCII art.

Usage:
  story_render.py [msg_index ...]        render listed messages (default 0-4)
  story_render.py --ids [msg ...]        print glyph index lines only
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from probe_bigfont import glyph_rows, BASE, STRIDE

ROM = os.path.join(os.path.dirname(__file__), "..", "rom", "monster-guardians.gba")
RAW = os.path.join(os.path.dirname(__file__), "..", "build", "story_messages_raw.json")

CONTROL = {0x7530: "Cmd30", 0x7531: "Cmd31", 0x7532: "Cmd32", 0x7533: "Cmd33",
           0x7534: "Cmd34", 0x7535: "Cmd35", 0x7536: "Cmd36", 0x7FFF: "End"}


def load():
    with open(ROM, "rb") as f:
        return f.read()


def glyph_art(data, idx):
    rows = glyph_rows(data, BASE + idx * STRIDE)
    return ["".join("#" if b else "." for b in r) for r in rows]


def main():
    data = load()
    with open(RAW) as f:
        raw = json.load(f)
    msgs = raw["messages"]
    if "--ids" in sys.argv:
        for i in [int(x) for x in sys.argv[sys.argv.index("--ids") + 1:]] or range(5):
            toks = [int(t, 16) for t in msgs[i]["raw"]]
            print(f"--- msg {i} ({len(toks)} words)")
            print(" ".join(f"{t:04X}" for t in toks))
        return
    which = [int(x) for x in sys.argv[1:]] or list(range(5))
    for i in which:
        toks = [int(t, 16) for t in msgs[i]["raw"]]
        print(f"===== message {i} =====")
        # split into runs of glyphs (<=0x6ff) vs controls
        run = []
        for t in toks:
            if t >= 0x1000:
                if run:
                    print("idx: " + " ".join(f"{g:4d}" for g in run))
                    arts = [glyph_art(data, g) for g in run]
                    for r in range(11):
                        print("     " + " ".join(a[r] for a in arts))
                    run = []
                name = CONTROL.get(t, f"Cmd{t:04X}")
                if t == 0x7534 or t == 0x7532 or t == 0x7530:
                    print(f"[{name}]")
                else:
                    print(f"[{name}]")
            else:
                run.append(t)
        if run:
            print("idx: " + " ".join(f"{g:4d}" for g in run))
            arts = [glyph_art(data, g) for g in run]
            for r in range(11):
                print("     " + " ".join(a[r] for a in arts))
        print()


if __name__ == "__main__":
    main()
