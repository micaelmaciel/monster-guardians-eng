#!/usr/bin/env python3
"""Render a token range of a story message as a boxed, labeled PNG at
large scale -- for zooming into ambiguous glyphs.

Usage: zoom_tokens.py <msg_idx> <start_token> <end_token> <out.png> [scale]

Tokens are shown in their own box with the hex index underneath; controls
show as their hex code. end_token is exclusive.
"""
import json
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ROM = os.path.join(ROOT, "rom", "monster-guardians.gba")
RAW = os.path.join(ROOT, "build", "story_messages_raw.json")

sys.path.insert(0, HERE)
from render_story import load_rom, glyph_rows, GW, GH  # noqa: E402


def main():
    msg_idx = int(sys.argv[1])
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    out = sys.argv[4]
    scale = int(sys.argv[5]) if len(sys.argv) > 5 else 8

    data = load_rom()
    msgs = json.load(open(RAW))["messages"]
    toks = [int(t, 16) for t in msgs[msg_idx]["raw"]]
    sel = toks[start:end]

    cell_w = (GW + 2) * scale
    img = Image.new("RGB", (len(sel) * cell_w + 40, GH * scale + 70),
                    (255, 255, 255))
    d = ImageDraw.Draw(img)
    x = 20
    for t in sel:
        if t < 0x1000:
            rows = glyph_rows(data, t)
            d.rectangle([x, 0, x + GW * scale - 1, GH * scale - 1],
                        outline=(200, 200, 255))
            for ry in range(GH):
                for rx in range(GW):
                    if rows[ry][rx]:
                        d.rectangle([x + rx * scale, ry * scale,
                                     x + (rx + 1) * scale - 1,
                                     (ry + 1) * scale - 1], fill=(0, 0, 0))
            d.text((x + 4, GH * scale + 8), f"{t:03X}", fill=(200, 0, 0))
        else:
            d.rectangle([x, 0, x + GW * scale - 1, GH * scale - 1],
                        outline=(255, 150, 150))
            d.text((x + 4, GH * scale // 2), f"{t:04X}", fill=(200, 0, 0))
            d.text((x + 4, GH * scale + 8), "ctl", fill=(150, 0, 0))
        x += cell_w
    img.save(out)
    print(out, img.size)


if __name__ == "__main__":
    main()
