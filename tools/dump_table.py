#!/usr/bin/env python3
"""Dump a pointer table and the data it points to, in a 16-bit-code friendly view.

Usage: dump_table.py <rom> <table_offset_hex> [count] [target_bytes]
"""
import sys

rom = open(sys.argv[1], "rb").read()
tbl = int(sys.argv[2], 16)
count = int(sys.argv[3]) if len(sys.argv) > 3 else 16
tbytes = int(sys.argv[4]) if len(sys.argv) > 4 else 48

def word(off):
    return int.from_bytes(rom[off:off + 2], "little")

def view16(off, n):
    """n = number of 16-bit codes"""
    out = []
    for i in range(n):
        v = word(off + 2 * i)
        out.append(f"{v:04X}")
    return " ".join(out)

print(f"== table at 0x{tbl:X} ({count} entries) ==")
for i in range(count):
    p = int.from_bytes(rom[tbl + 4 * i:tbl + 4 * i + 4], "little")
    off = p - 0x08000000
    if not (0 <= off < len(rom)):
        print(f"[{i:3}] 0x{p:08X} (outside ROM)")
        continue
    codes = tbytes // 2
    v = view16(off, codes)
    print(f"[{i:3}] ptr 0x{p:08X} (rom 0x{off:06X}): {v}")
