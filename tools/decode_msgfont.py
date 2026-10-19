#!/usr/bin/env python3
"""Decode the third text system (field message box, "message font").

Inputs:
  build/msgfont_strings_raw.json  -- 169 x {start, codes} extracted by the
                                     whole-ROM 0x7FFF scan (see WIKI.md).
  data/msgfont_charmap.json       -- 317-glyph code -> char map.

Output:
  build/msgfont_strings.tsv       -- addr / idx / codes / text

Usage:
  tools/decode_msgfont.py                 # write the TSV
  tools/decode_msgfont.py --list          # print all decoded strings
  tools/decode_msgfont.py --render 47 out.png   # render one string
"""
import json
import sys

RAW = "build/msgfont_strings_raw.json"
CHARMAP = "data/msgfont_charmap.json"
TSV = "build/msgfont_strings.tsv"


def load():
    segs = json.load(open(RAW))
    cm = json.load(open(CHARMAP))
    cmap = {int(k): v for k, v in cm["entries"].items()}
    return segs, cm, cmap


def addr_of(seg):
    st = seg["start"]
    return int(st, 16) if isinstance(st, str) else st


def decode(seg, cmap):
    return "".join(cmap.get(c, f"<{c}>") for c in seg["codes"])


def write_tsv(segs, cmap):
    rows = ["addr\tidx\tcodes\ttext"]
    for i, s in enumerate(segs):
        rows.append(
            "0x%06X\t%d\t%s\t%s"
            % (addr_of(s), i, " ".join(map(str, s["codes"])), decode(s, cmap))
        )
    open(TSV, "w").write("\n".join(rows) + "\n")
    print("wrote", TSV, "(%d strings)" % len(segs))


def render(segs, idx, out):
    from PIL import Image, ImageDraw

    rom = open("rom/monster-guardians.gba", "rb").read()
    cm = json.load(open(CHARMAP))
    base, stride = cm["base"], cm["stride"]

    def glyph(g):
        b = rom[base + g * stride: base + (g + 1) * stride]
        rows = []
        for r in range(8):
            rows.append([(b[r] >> (7 - x)) & 1 for x in range(8)] + [(b[8 + r] >> 7) & 1])
        rows.append([(b[16] >> (7 - x)) & 1 for x in range(8)] + [(b[17] >> 7) & 1])
        return rows

    s = segs[idx]
    per = 11  # renderer wrap width
    lines = [s["codes"][i:i + per] for i in range(0, len(s["codes"]), per)]
    S = 6
    W = 2 + per * 10 * S
    H = 2 + len(lines) * (9 * S + 4) + 14
    img = Image.new("RGB", (W, H), (15, 15, 15))
    d = ImageDraw.Draw(img)
    cmap = {int(k): v for k, v in cm["entries"].items()}
    d.text((2, 1), "#%d 0x%06X %s" % (idx, addr_of(s), decode(s, cmap)), fill=(110, 200, 110))
    y = 14
    for line in lines:
        for k, g in enumerate(line):
            rows = glyph(g)
            for yy in range(9):
                for xx in range(9):
                    if rows[yy][xx]:
                        d.rectangle(
                            [4 + (k * 10 + xx) * S, y + yy * S,
                             4 + (k * 10 + xx) * S + S - 1, y + yy * S + S - 1],
                            fill=(235, 235, 225),
                        )
        y += 9 * S + 4
    img.save(out)
    print("wrote", out)


def main(argv):
    segs, cm, cmap = load()
    if "--list" in argv:
        for i, s in enumerate(segs):
            print("%3d 0x%06X %s" % (i, addr_of(s), decode(s, cmap)))
        return
    if "--render" in argv:
        i = argv.index("--render")
        render(segs, int(argv[i + 1]), argv[i + 2])
        return
    write_tsv(segs, cmap)


if __name__ == "__main__":
    main(sys.argv[1:])
