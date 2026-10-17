#!/usr/bin/env python3
"""Dump GBA ROM header fields."""
import struct
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "rom/monster-guardians.gba"
data = open(path, "rb").read()

def s(off, n):
    return data[off:off + n].split(b"\x00")[0].decode("ascii", "replace")

print(f"file size: {len(data)} bytes ({len(data)/1024/1024:.2f} MiB / {len(data)*8/1024/1024:.0f} Mbit)")
print(f"entry point: {data[0:4].hex()} (b {data[3]:02x})")
print(f"title:      {s(0xA0, 12)!r}")
print(f"game code:  {s(0xAC, 4)!r}")
print(f"maker code: {s(0xB0, 2)!r}")
print(f"unit code:  0x{data[0xB2]:02x}")
print(f"device:     0x{data[0xB3]:02x}")
print(f"reserved:   {data[0xB4:0xBC].hex()}")
print(f"version:    {data[0xBC]}")
print(f"complement: 0x{data[0xBD]:02x}")
print(f"checksum:   0x{data[0xBE]:02x}{data[0xBF]:02x}")

# verify header complement check
chk = 0
for b in data[0xA0:0xBD]:
    chk = (chk - b - 0x19) & 0xFF
print(f"complement check: {'OK' if chk == data[0xBD] else 'MISMATCH (computed 0x%02x)' % chk}")
