#!/usr/bin/env python3
"""Map free space (runs of 0xFF / 0x00) in a GBA ROM."""
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "rom/monster-guardians.gba"
data = open(path, "rb").read()
MIN = 256  # only report runs >= this

runs = []
i = 0
n = len(data)
while i < n:
    b = data[i]
    if b in (0x00, 0xFF):
        j = i
        while j < n and data[j] == b:
            j += 1
        if j - i >= MIN:
            runs.append((i, j - i, b))
        i = j
    else:
        i += 1

# merge runs separated by tiny non-free gaps (< 16 bytes) -- approximate usage
merged = []
for start, length, b in runs:
    if merged and start - (merged[-1][0] + merged[-1][1]) < 16 and merged[-1][2] == b:
        merged[-1][1] = start + length - merged[-1][0]
    else:
        merged.append([start, length, b])

total = sum(l for _, l, _ in runs)
print(f"ROM size: {n} bytes ({n/1024/1024:.2f} MiB)")
print(f"free runs (>={MIN}B): {len(runs)}, total {total} bytes ({total/n*100:.1f}% of ROM)")
print(f"merged (gaps<16B): {len(merged)} runs, total {sum(l for _,l,_ in merged)} bytes")
print(f"{'start':>10} {'end':>10} {'size':>10} {'KiB':>8} byte")
for start, length, b in merged:
    print(f"0x{start:08X} 0x{start+length:08X} {length:>10} {length/1024:>8.1f} 0x{b:02X}")
