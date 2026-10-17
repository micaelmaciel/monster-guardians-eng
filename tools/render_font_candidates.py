#!/usr/bin/env python3
"""Render candidate font layouts from a ROM region into labelled PNG sheets.

Usage: render_font_candidates.py <rom> <outdir>
Produces:
  font_A_8x8.png   : 8x8 glyphs, 32 per row
  font_B_8x16.png  : 8x16 glyphs (2 stacked 8x8 tiles), 16 per row
"""
import sys, os
from PIL import Image, ImageDraw

SCALE = 3
ROMBASE = 0x0BEE00
NPIX = 8


def tile_pixels(data, off):
    """Return 8x8 list of palette indices (4bpp)."""
    rows = []
    for y in range(8):
        b = data[off + y * 4: off + y * 4 + 4]
        row = []
        for byte in b:
            row.append(byte & 0xF)
            row.append(byte >> 4)
        rows.append(row)
    return rows


def render_sheet(data, out, gw, gh, per_row, count, label_prefix, start=0):
    cw = gw * SCALE
    ch = gh * SCALE
    pad = 2
    lh = 10
    cols = per_row
    rows = (count + cols - 1) // cols
    W = cols * (cw + pad) + 2
    H = rows * (ch + pad + lh) + 2
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for i in range(count):
        idx = start + i
        gx = 1 + (i % cols) * (cw + pad)
        gy = 1 + (i // cols) * (ch + pad + lh)
        # glyph = gh/8 stacked tiles starting at idx* (gw*gh/2) bytes
        tiles_high = gh // 8
        tiles_wide = gw // 8
        n_tiles = tiles_high * tiles_wide
        base = idx * n_tiles * 32
        for th in range(tiles_high):
            for tw in range(tiles_wide):
                off = base + (th * tiles_wide + tw) * 32
                if off + 32 > len(data):
                    continue
                pix = tile_pixels(data, off)
                for y in range(8):
                    for x in range(8):
                        v = pix[y][x]
                        c = 255 - int(v * 255 / 15)
                        px = gx + (tw * 8 + x) * SCALE
                        py = gy + (th * 8 + y) * SCALE
                        d.rectangle([px, py, px + SCALE - 1, py + SCALE - 1], fill=(c, c, c))
        d.text((gx, gy + ch + 0), f"{idx:03X}", fill=(0, 0, 200))
    img.save(out)
    print("wrote", out, img.size)


def main():
    rom = sys.argv[1]
    outdir = sys.argv[2]
    data = open(rom, "rb").read()
    seg = data[ROMBASE:ROMBASE + 0x2000]  # 16 KiB copied to VRAM per CpuSet log
    os.makedirs(outdir, exist_ok=True)
    # A: 8x8 glyphs, 512 of them (16 KiB / 32)
    render_sheet(seg, os.path.join(outdir, "font_A_8x8.png"), 8, 8, 32, 512, "A")
    # B: 8x16 glyphs, 256 of them (16 KiB / 64)
    render_sheet(seg, os.path.join(outdir, "font_B_8x16.png"), 8, 16, 16, 256, "B")


if __name__ == "__main__":
    main()
