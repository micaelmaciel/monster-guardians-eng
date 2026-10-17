#!/usr/bin/env python3
"""Map on-screen OBJ tiles (4bpp VRAM) back to bigfont glyph indices.

A bigfont glyph = 22 bytes: rows0-7 left (8B), rows0-7 right (8B),
rows8-10 left (3B), rows8-10 right (3B); each row byte is a 1bpp mask
(bit 7 = leftmost pixel of that 8-px half).

On screen each glyph = 16x16 OBJ sprite = 4 tiles TL,TR,BL,BR.
Previous session verified: tile 8x8 = (half rows as 1bpp bytes expanded to
4bpp nibbles) followed by zero padding.

This tool: for a given frame dump dir and frame number, read OAM + VRAM,
find the glyph sprites, and recover each ROM glyph index by matching the
reconstructed 22-byte pattern against the ROM store.

Usage: map_screen_glyphs.py <dumpdir> <frame> [--y Y] 
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))

ROM = os.path.join(os.path.dirname(__file__), "..", "rom", "monster-guardians.gba")
BIG_BASE = 0xD3144
BIG_STRIDE = 22


def expand_tile(data, off):
    """Return 8 rows of 8 palette indices (4bpp, low nibble first)."""
    rows = []
    for y in range(8):
        row = []
        for b in range(4):
            byte = data[off + y * 4 + b]
            row.append(byte & 0xF)
            row.append((byte >> 4) & 0xF)
        rows.append(row)
    return rows


def tile_to_1bpp_masks(rows):
    """Given 8x8 palette indices, return 2 bytes: for even rows (top) and
    odd rows?  Actually the known format: a half's 8 rows are packed as 1bpp
    bytes; the 4bpp tile stores... let's just return the ink pattern per row
    as an 8-bit mask using 'nonzero pixel = ink'."""
    out = []
    for r in rows:
        m = 0
        for px in r:
            m = (m << 1) | (1 if px else 0)
        out.append(m)
    return out


def main():
    dumpdir = sys.argv[1]
    frame = int(sys.argv[2])
    y_filter = None
    if "--y" in sys.argv:
        y_filter = int(sys.argv[sys.argv.index("--y") + 1])

    rom = open(ROM, "rb").read()
    # build bigfont lookup: 22-byte tuple -> index
    store = {}
    for i in range(685):
        g = rom[BIG_BASE + i * BIG_STRIDE: BIG_BASE + (i + 1) * BIG_STRIDE]
        store[bytes(g)] = i

    oam = open(os.path.join(dumpdir, f"oam_{frame:04d}.bin"), "rb").read()
    vram = open(os.path.join(dumpdir, f"vram_{frame:04d}.bin"), "rb").read()
    obj = vram[0x10000:0x18000]

    sprites = []
    for i in range(128):
        a0, a1, a2 = struct.unpack_from("<HHH", oam, i * 8)
        if a0 & 0x0200:
            continue  # OBJ disable bit set
        y = a0 & 0xFF
        x = a1 & 0x1FF
        tile = a2 & 0x3FF
        if y_filter is not None and y != y_filter:
            continue
        sprites.append((y, x, tile))

    # group into rows by y
    rows = {}
    for y, x, tile in sprites:
        rows.setdefault(y, []).append((x, tile))
    for y in sorted(rows):
        items = sorted(rows[y])
        out = []
        for x, tile in items:
            # 16x16 sprite: tiles TL=tile, TR=tile+1, BL=tile+2, BR=tile+3
            tl = tile_to_1bpp_masks(expand_tile(obj, (tile + 0) * 32))
            tr = tile_to_1bpp_masks(expand_tile(obj, (tile + 1) * 32))
            bl = tile_to_1bpp_masks(expand_tile(obj, (tile + 2) * 32))
            br = tile_to_1bpp_masks(expand_tile(obj, (tile + 3) * 32))
            # left half rows0-7 = tl, right half rows0-7 = tr
            # left rows8-10 = bl[0:3], right rows8-10 = br[0:3]
            g = bytes(tl) + bytes(tr) + bytes(bl[:3]) + bytes(br[:3])
            idx = store.get(g)
            out.append((x, tile, idx))
        print(f"y={y}: " + " ".join(
            f"x{x}:t{t}:{'?' if i is None else i}" for x, t, i in out))


if __name__ == "__main__":
    main()
