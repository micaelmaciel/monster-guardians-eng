#!/usr/bin/env python3
"""Find runs of 4-aligned 32-bit pointers into GBA ROM (0x08000000..+ROM size).
Reports pointer tables: consecutive runs of >= MINRUN valid ROM pointers."""
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "rom/monster-guardians.gba"
data = open(path, "rb").read()
rom_size = len(data)
MINRUN = int(sys.argv[2]) if len(sys.argv) > 2 else 4

BASE = 0x08000000
lo, hi = BASE, BASE + rom_size

def ptr_at(off):
    v = int.from_bytes(data[off:off + 4], "little")
    return v if lo <= v < hi else None

tables = []
i = 0
n = len(data) - 4
while i <= n:
    if i % 4:
        i += 4 - (i % 4)
        continue
    if ptr_at(i) is None:
        i += 4
        continue
    j = i
    count = 0
    while j <= n:
        v = ptr_at(j)
        if v is None:
            break
        count += 1
        j += 4
    if count >= MINRUN:
        tables.append((i, count))
        i = j
    else:
        i += 4

# classify: where do pointers go (min/max targets, self-contained?)
print(f"ROM: {rom_size} bytes; pointers 0x{lo:08X}..0x{hi:08X}")
print(f"pointer tables (runs >= {MINRUN}): {len(tables)}")
for off, cnt in tables:
    vals = [int.from_bytes(data[off + 4*k:off + 4*k + 4], "little") for k in range(cnt)]
    tmin, tmax = min(vals), max(vals)
    inrom = sum(1 for v in vals if lo <= v < hi)
    print(f"0x{off:07X}  n={cnt:>4}  targets 0x{tmin:07X}..0x{tmax:07X}  (in-ROM: {inrom})")
