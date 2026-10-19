#!/usr/bin/env python3
"""Render contact sheets for the unresolved 8x8 glyphs 0x1A0..0x1BF.

Outputs (default build/):
  glyph_sheet_1A0_1BF.png  - grid of all 32 glyphs at 12x with code labels
  glyph_names_1A0_1BF.png  - the eight four-glyph names (0x0BD4E4..0x0BD52A)
                             rendered word-by-word at 12x with code labels

Ink = palette values 0xE/0xF (verified: best-match layer against the 1-bit
bigfont for 265 shared characters); value 1 is an outline/shadow layer and is
rendered light gray; 0 is white.
"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ROM = os.path.join(ROOT, "rom", "monster-guardians.gba")
OUTDIR = os.path.join(ROOT, "build")
FONT_BASE = 0x0BEDF0
SCALE = 12

# eight four-glyph names stored at 0x0BD4E4..0x0BD52A
NAME_ADDRS = [0x0BD4E4, 0x0BD4EC, 0x0BD4FA, 0x0BD50A,
              0x0BD512, 0x0BD51A, 0x0BD522, 0x0BD52A]


def glyph_rows(rom, g):
    off = FONT_BASE + g * 32
    out = []
    for y in range(8):
        row = []
        for b in range(4):
            byte = rom[off + y * 4 + b]
            row.append(byte & 0xF)
            row.append(byte >> 4)
        out.append(row)
    return out


def draw_glyph(img, px, g, rows, x0, y0):
    d = ImageDraw.Draw(img)
    for y in range(8):
        for x in range(8):
            v = rows[y][x]
            if v == 0:
                continue
            color = (0, 0, 0) if v in (0xE, 0xF) else (185, 185, 185)
            d.rectangle([x0 + x * SCALE, y0 + y * SCALE,
                         x0 + (x + 1) * SCALE - 1, y0 + (y + 1) * SCALE - 1],
                        fill=color)


def main():
    rom = open(ROM, "rb").read()
    glyphs = {g: glyph_rows(rom, g) for g in range(0x1A0, 0x1C0)}

    # ---- sheet ----
    cols, rows = 8, 4
    cell = 8 * SCALE
    pad = 26
    lab = 20
    W = cols * (cell + pad) + pad
    H = rows * (cell + pad + lab) + pad
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    for i, g in enumerate(range(0x1A0, 0x1C0)):
        cx = pad + (i % cols) * (cell + pad)
        cy = pad + (i // cols) * (cell + pad + lab)
        draw_glyph(img, img.load(), g, glyphs[g], cx, cy)
        d.rectangle([cx - 1, cy - 1, cx + cell, cy + cell], outline=(200, 200, 200))
        d.line([cx, cy + cell // 2, cx + cell, cy + cell // 2], fill=(235, 235, 235))
        d.line([cx + cell // 2, cy, cx + cell // 2, cy + cell], fill=(235, 235, 235))
        d.text((cx + cell // 2 - 18, cy + cell + 3), f"0x{g:03X}", fill=(0, 0, 0))
    img.save(os.path.join(OUTDIR, "glyph_sheet_1A0_1BF.png"))

    # ---- names ----
    ncell = 8 * SCALE
    npad = 18
    W2 = 6 + 4 * (ncell + npad) + npad + 120
    H2 = len(NAME_ADDRS) * (ncell + npad + 16) + npad
    img2 = Image.new("RGB", (W2, H2), "white")
    d2 = ImageDraw.Draw(img2)
    for i, addr in enumerate(NAME_ADDRS):
        codes = [int.from_bytes(rom[addr + 2 * k:addr + 2 * k + 2], "little")
                 for k in range(4)]
        y0 = npad + i * (ncell + npad + 16)
        d2.text((6, y0 + ncell // 2 - 6), f"{i + 1}", fill=(0, 0, 0))
        for k, g in enumerate(codes):
            x0 = 30 + k * (ncell + npad)
            draw_glyph(img2, img2.load(), g, glyphs[g], x0, y0)
            d2.rectangle([x0 - 1, y0 - 1, x0 + ncell, y0 + ncell],
                         outline=(200, 200, 200))
            d2.text((x0 + ncell // 2 - 18, y0 + ncell + 3),
                    f"0x{g:03X}", fill=(0, 0, 0))
        d2.text((30 + 4 * (ncell + npad) + 6, y0 + ncell // 2 - 6),
                f"0x{addr:06X}", fill=(120, 120, 120))
    img2.save(os.path.join(OUTDIR, "glyph_names_1A0_1BF.png"))

    print("wrote build/glyph_sheet_1A0_1BF.png and build/glyph_names_1A0_1BF.png")


if __name__ == "__main__":
    main()
