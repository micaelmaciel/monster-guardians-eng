#!/usr/bin/env python3
"""Catalog all 16-bit-code strings in the ROM.

A string: 4+ consecutive 16-bit words, >=80% of which are in 1..MAXCODE,
terminated by 0x0000. Groups strings into banks. Also builds a reverse pointer
index (which 32-bit ROM pointers reference which offsets) and reports, per
bank, how many strings are referenced by pointers.

Usage: extract_strings.py [rom] [out_tsv]
"""
import sys
from collections import defaultdict

rom_path = sys.argv[1] if len(sys.argv) > 1 else "rom/monster-guardians.gba"
out_path = sys.argv[2] if len(sys.argv) > 2 else "build/strings.tsv"
MAXCODE = 0x3FF

data = open(rom_path, "rb").read()
n = len(data)
BASE = 0x08000000

def word(off):
    return data[off] | (data[off + 1] << 8)

# --- reverse pointer index ---
ptr_at = defaultdict(list)  # target rom offset -> [source offsets]
for off in range(0, n - 4, 4):
    v = int.from_bytes(data[off:off + 4], "little")
    if BASE <= v < BASE + n:
        ptr_at[v - BASE].append(off)

# --- string extraction (scan 2-aligned) ---
strings = []  # (start, end_excl, codes)
off = 0
while off + 4 <= n:
    codes = []
    p = off
    ok = False
    while p + 2 <= n and len(codes) < 200:
        v = word(p)
        codes.append(v)
        p += 2
        if v == 0:
            ok = len(codes) >= 5 and sum(1 for c in codes if 1 <= c <= MAXCODE) >= len(codes) * 0.8
            break
    if ok:
        strings.append((off, p, codes))
        off = p  # skip past string (strings are contiguous in banks)
    else:
        off += 2

print(f"extracted {len(strings)} candidate strings")

# --- group into banks (gap <= 64 bytes => same bank) ---
banks = []
for s, e, codes in strings:
    if banks and s - banks[-1][1] <= 64:
        banks[-1][1] = e
        banks[-1][2].append((s, e, codes))
    else:
        banks.append([s, e, [(s, e, codes)]])

print(f"grouped into {len(banks)} banks")
print(f"{'bank start':>10} {'bank end':>10} {'#strings':>8} {'ptrd':>5}  maxcode")
import os
os.makedirs("build", exist_ok=True)
with open(out_path, "w") as f:
    f.write("bank_start\tbank_end\tstr_start\tstr_end\tcodes\tptr_sources\n")
    for bs, be, strs in banks:
        ptrd = sum(1 for s, e, c in strs if s in ptr_at)
        maxcode = max((v for s, e, c in strs for v in c), default=0)
        print(f"0x{bs:08X} 0x{be:08X} {len(strs):>8} {ptrd:>5}  0x{maxcode:03X}")
        for s, e, c in strs:
            srcs = ",".join(f"0x{x:06X}" for x in ptr_at.get(s, [])[:5])
            f.write(f"0x{bs:06X}\t0x{be:06X}\t0x{s:06X}\t0x{e:06X}\t" +
                    " ".join(f"{v:03x}" for v in c) + f"\t{srcs}\n")
print(f"wrote {out_path}")
