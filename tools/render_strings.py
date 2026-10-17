#!/usr/bin/env python3
"""Render ROM text-code strings as images using the game's 8x8 font.

Usage: render_strings.py <rom> <strings.tsv> <out.png> <addr> [<addr> ...]

Font: 8x8 tiles at ROM 0xBEDF0, glyph index == code value (hypothesis).
Codes >= 0x200 render as a red box.
"""
import sys
from PIL import Image, ImageDraw

FONT_BASE = 0x0BEDF0
FONT_GLYPHS = 0x200
SCALE = 2
WRAP = 26
LINE_H = 10
LABEL_H = 12


def load_font(rom):
    glyphs = []
    for g in range(FONT_GLYPHS):
        off = FONT_BASE + g * 32
        rows = []
        for y in range(8):
            b = rom[off + y * 4: off + y * 4 + 4]
            row = []
            for byte in b:
                row.append(byte & 0xF)
                row.append(byte >> 4)
            rows.append(row)
        glyphs.append(rows)
    return glyphs


def draw_glyph(img, d, glyphs, code, x, y, scale, fg=(0, 0, 0), bg=(255, 255, 255)):
    if code >= FONT_GLYPHS:
        d.rectangle([x, y, x + 8 * scale - 1, y + 8 * scale - 1], outline=(255, 0, 0))
        return
    g = glyphs[code]
    for yy in range(8):
        for xx in range(8):
            v = g[yy][xx]
            if v:
                c = int(255 - v * 255 / 15)
                d.rectangle([x + xx * scale, y + yy * scale,
                             x + xx * scale + scale - 1, y + yy * scale + scale - 1],
                            fill=(c, c, c))


def main():
    rom = open(sys.argv[1], "rb").read()
    tsv = sys.argv[2]
    out = sys.argv[3]
    addrs = [int(a, 16) for a in sys.argv[4:]]
    strings = {}
    with open(tsv) as f:
        f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 5:
                continue
            strings[int(p[2], 16)] = [int(c, 16) for c in p[4].split()]
    glyphs = load_font(rom)
    blocks = []
    for a in addrs:
        codes = strings.get(a)
        if codes is None:
            continue
        lines = [codes[i:i + WRAP] for i in range(0, len(codes), WRAP)]
        blocks.append((a, lines))
    width = WRAP * 8 * SCALE + 8
    height = sum(LABEL_H + len(l) * LINE_H * SCALE + 6 for _, l in blocks) + 8
    img = Image.new("RGB", (width, height), (250, 250, 250))
    d = ImageDraw.Draw(img)
    y = 4
    for a, lines in blocks:
        d.text((4, y), f"ROM 0x{a:06X}", fill=(0, 0, 200))
        y += LABEL_H
        for line in lines:
            x = 4
            for c in line:
                draw_glyph(img, d, glyphs, c, x, y, SCALE)
                x += 8 * SCALE
            y += LINE_H * SCALE
        y += 6
    img.save(out)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
