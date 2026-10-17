#!/usr/bin/env python3
"""Render transcription-friendly font pages.

Usage: render_font_pages.py <rom> <outdir>

Produces font_page_000.png ... covering glyph indices in 128-glyph pages,
16 per row, 8 rows, at 4x scale with a grid and hex labels. Font base
ROM 0xBEDF0, 8x8 per glyph.
"""
import sys, os
from PIL import Image, ImageDraw

FONT_BASE = 0x0BEDF0
SCALE = 4
COLS = 16
ROWS = 8
PER_PAGE = COLS * ROWS  # 128


def glyph_rows(rom, g):
    off = FONT_BASE + g * 32
    out = []
    for y in range(8):
        b = rom[off + y * 4: off + y * 4 + 4]
        row = []
        for byte in b:
            row.append(byte & 0xF)
            row.append(byte >> 4)
        out.append(row)
    return out


def main():
    rom = open(sys.argv[1], "rb").read()
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    cell = 8 * SCALE
    pad = 22
    for page in range(4):
        base = page * PER_PAGE
        W = COLS * (cell + pad) + pad
        H = ROWS * (cell + pad) + pad + 14
        img = Image.new("RGB", (W, H), (245, 245, 245))
        d = ImageDraw.Draw(img)
        d.text((pad, 2), f"glyph indices 0x{base:03X} - 0x{base+PER_PAGE-1:03X}", fill=(0, 0, 160))
        for i in range(PER_PAGE):
            g = base + i
            cx = pad + (i % COLS) * (cell + pad)
            cy = pad + 14 + (i // COLS) * (cell + pad)
            # grid
            d.rectangle([cx - 1, cy - 1, cx + cell, cy + cell], outline=(200, 200, 200))
            rows = glyph_rows(rom, g)
            for y in range(8):
                for x in range(8):
                    v = rows[y][x]
                    if v:
                        c = int(255 - v * 255 / 15)
                        d.rectangle([cx + x * SCALE, cy + y * SCALE,
                                     cx + x * SCALE + SCALE - 1, cy + y * SCALE + SCALE - 1],
                                    fill=(c, c, c))
            d.text((cx, cy + cell + 3), f"{g:03X}", fill=(0, 0, 200))
        img.save(os.path.join(outdir, f"font_page_{base:03X}.png"))
        print("wrote", os.path.join(outdir, f"font_page_{base:03X}.png"), img.size)


if __name__ == "__main__":
    main()
