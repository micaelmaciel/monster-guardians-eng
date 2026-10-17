#!/usr/bin/env python3
"""Render an 8x8 font glyph (ROM 0xBEDF0) as ASCII art.  Usage: small_art.py 0x5F [0x4A ...]"""
import sys

data = open("rom/monster-guardians.gba", "rb").read()
for arg in sys.argv[1:]:
    idx = int(arg, 16) if arg.lower().startswith("0x") else int(arg)
    base = 0xBEDF0 + idx * 32
    print(f"=== {idx} 0x{idx:03X} ===")
    for y in range(8):
        row = []
        for b in range(4):
            byte = data[base + y * 4 + b]
            row.append(byte & 0xF)      # low nibble = left pixel
            row.append((byte >> 4) & 0xF)  # high nibble = right pixel
        print("".join("#" if v else "." for v in row))
