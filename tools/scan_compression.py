#!/usr/bin/env python3
"""Scan a GBA ROM for Nintendo compression formats (LZ77 0x10, Huffman 0x11,
LZ77-2 0x12?, RLE 0x30) at 4-aligned offsets, with strict validation."""
import struct
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "rom/monster-guardians.gba"
data = open(path, "rb").read()

def try_lz77(off):
    """Validate and size an LZ77 block at off. Returns decompressed length or None."""
    if off + 8 > len(data):
        return None
    hdr = data[off:off + 4]
    if hdr[0] != 0x10:
        return None
    dsize = int.from_bytes(hdr[1:4], "little")
    if not (8 <= dsize <= 0x200000):  # sanity range
        return None
    p = off + 4
    out = 0
    try:
        while out < dsize:
            flags = data[p]; p += 1
            for bit in range(7, -1, -1):
                if out >= dsize:
                    break
                if flags & (1 << bit):
                    b1 = data[p]; b2 = data[p + 1]; p += 2
                    n = (b1 >> 4) + 3
                    disp = (((b1 & 0xF) << 8) | b2) + 1
                    if disp > out - (off + 4 - off):  # disp must reference produced output
                        if disp > out:
                            return None
                    out += n
                else:
                    p += 1
                    out += 1
    except IndexError:
        return None
    if out < dsize:
        return None
    return dsize, p - off

def try_rle(off):
    if off + 4 > len(data) or data[off] != 0x30:
        return None
    dsize = int.from_bytes(data[off + 1:off + 4], "little")
    if not (8 <= dsize <= 0x200000):
        return None
    p = off + 4
    out = 0
    try:
        while out < dsize:
            v = data[p]; p += 1
            if v & 0x80:
                n = (v & 0x7F) + 3
                p += 1
            else:
                n = v + 1
            out += n
    except IndexError:
        return None
    if out != dsize:
        return None
    return dsize, p - off

hits = {"lz77": [], "rle": []}
for off in range(0, len(data) - 8, 4):
    if data[off] == 0x10:
        r = try_lz77(off)
        if r:
            hits["lz77"].append((off, r[0], r[1]))
    if data[off] == 0x30:
        r = try_rle(off)
        if r:
            hits["rle"].append((off, r[0], r[1]))

for kind, lst in hits.items():
    print(f"== {kind}: {len(lst)} validated blocks ==")
    total = sum(sz for _, sz, _ in lst)
    print(f"   total decompressed bytes: {total} ({total/1024:.0f} KiB)")
    for off, sz, clen in lst[:40]:
        print(f"   0x{off:07X}  comp={clen:>8}  decomp={sz:>8}")
    if len(lst) > 40:
        print(f"   ... and {len(lst) - 40} more")
