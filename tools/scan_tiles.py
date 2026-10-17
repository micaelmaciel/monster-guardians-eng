#!/usr/bin/env python3
"""Scan a GBA ROM for runs of 4bpp tile-like data (candidate font/graphics banks).

A tile = 32 bytes (8x8 px, 4bpp). Heuristic per tile: some ink, few distinct
nibbles. Reports maximal runs of >= MINRUN consecutive tile-like tiles."""
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "rom/monster-guardians.gba"
data = open(path, "rb").read()
MINRUN = int(sys.argv[2]) if len(sys.argv) > 2 else 512  # tiles

def tile_stats(off):
    ink = 0
    nibs = set()
    for i in range(32):
        b = data[off + i]
        for nb in (b & 0xF, b >> 4):
            if nb:
                ink += 1
            nibs.add(nb)
    return ink / 64.0, len(nibs)

n_tiles = len(data) // 32
flags = bytearray(n_tiles)
for t in range(n_tiles):
    d, nc = tile_stats(t * 32)
    # nonempty, mostly low-index colors (font/16-color graphics), not raw code
    if 0.03 <= d <= 0.95 and nc <= 8:
        flags[t] = 1

runs = []
t = 0
while t < n_tiles:
    if flags[t]:
        j = t
        while j < n_tiles and flags[j]:
            j += 1
        if j - t >= MINRUN:
            runs.append((t * 32, (j - t) * 32, j - t))
        t = j
    else:
        t += 1

print(f"tile-like runs >= {MINRUN} tiles ({MINRUN*32//1024} KiB): {len(runs)}")
for start, size, cnt in runs:
    # ink stats over the run for a feel
    print(f"  0x{start:06X}..0x{start+size:06X}  {size//1024:>5} KiB  {cnt:>6} tiles")
