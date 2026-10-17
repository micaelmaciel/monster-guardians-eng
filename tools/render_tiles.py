#!/usr/bin/env python3
"""Render 4bpp GBA tiles from a ROM region to a PNG contact sheet.

Usage: render_tiles.py <rom> <offset_hex> <count> <out.png> [tiles_per_row]
"""
import sys
from PIL import Image

rom = open(sys.argv[1], "rb").read()
start = int(sys.argv[2], 16)
count = int(sys.argv[3])
out = sys.argv[4]
tpr = int(sys.argv[5]) if len(sys.argv) > 5 else 32
SCALE = 3

rows = (count + tpr - 1) // tpr
img = Image.new("RGBA", (tpr * 8, rows * 8), (200, 200, 200, 255))
px = img.load()
pal = [(255, 255, 255, 0), (30, 30, 30, 255), (120, 120, 120, 255), (180, 180, 180, 255)]

for t in range(count):
    off = start + t * 32
    tx, ty = (t % tpr) * 8, (t // tpr) * 8
    for i in range(32):
        b = rom[off + i]
        for half, nb in ((0, b & 0xF), (1, b >> 4)):
            px_i = (i % 4) * 2 + half
            px_y = i // 4
            x, y = tx + px_i, ty + px_y
            if x < img.width and y < img.height:
                c = pal[nb] if nb < 4 else (255, 0, 0, 255)
                if c[3]:
                    px[x, y] = c

img = img.resize((img.width * SCALE, img.height * SCALE), Image.NEAREST)
img.save(out)
print(f"saved {out}: tiles {start:#x}+{count}, {tpr}/row")
