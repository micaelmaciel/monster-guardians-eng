#!/usr/bin/env python3
"""Probe the 16x11 (22-byte) large-glyph store at ROM 0xD3144.

Subcommands:
  count <hexoffset>   -- count ROM-wide occurrences of the 22 bytes at offset
  art <hexoffset> [n] -- render n (default 40) consecutive glyphs as ASCII art
"""
import sys

ROM = "rom/monster-guardians.gba"
BASE = 0xD3144
STRIDE = 22


def glyph_rows(data, off):
    """Return 11 rows of 16 booleans for the glyph at off."""
    g = data[off:off + STRIDE]
    if len(g) < STRIDE:
        return None
    rows = []
    for r in range(8):
        left, right = g[r], g[8 + r]
        row = []
        for px in range(8):
            row.append((left >> (7 - px)) & 1)
        for px in range(8):
            row.append((right >> (7 - px)) & 1)
        rows.append(row)
    for r in range(3):
        left, right = g[16 + r], g[19 + r]
        row = []
        for px in range(8):
            row.append((left >> (7 - px)) & 1)
        for px in range(8):
            row.append((right >> (7 - px)) & 1)
        rows.append(row)
    return rows


def render(rows):
    return "\n".join("".join("#" if p else "." for p in row) for row in rows)


def main():
    data = open(ROM, "rb").read()
    cmd = sys.argv[1]
    if cmd == "count":
        off = int(sys.argv[2], 16)
        needle = data[off:off + STRIDE]
        hits = []
        start = 0
        while True:
            i = data.find(needle, start)
            if i < 0:
                break
            hits.append(i)
            start = i + 1
        print(f"22 bytes at 0x{off:X} found {len(hits)}x: " +
              ", ".join(f"0x{h:X}" for h in hits[:40]))
    elif cmd == "art":
        off = int(sys.argv[2], 16)
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 40
        for k in range(n):
            o = off + k * STRIDE
            rows = glyph_rows(data, o)
            if rows is None:
                break
            print(f"--- offset 0x{o:X} (index from base: {(o - BASE) // STRIDE}) ---")
            print(render(rows))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
