#!/usr/bin/env python3
"""Disassemble a ROM range (Thumb) with literal and branch annotations."""
import struct
import sys

import capstone

ROM = "rom/monster-guardians.gba"
BASE = 0x08000000


def main():
    rom = open(ROM, "rb").read()
    start = int(sys.argv[1], 0)
    end = int(sys.argv[2], 0) if len(sys.argv) > 2 else start + 0x100
    if start < BASE:
        start += BASE
        end += BASE
    md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_THUMB)
    md.detail = True
    md.skipdata = True
    code = rom[start - BASE:end - BASE]
    for ins in md.disasm(code, start):
        text = f"{ins.address:07X}: {ins.bytes.hex():<8} {ins.mnemonic:<7} {ins.op_str}"
        # annotate pc-relative loads
        if ins.mnemonic.startswith("ldr") and "pc" in ins.op_str:
            try:
                imm = int(ins.op_str.split("#")[1].rstrip("]"), 0)
                lit_addr = ((ins.address + 4) & ~3) + imm
                lit = struct.unpack("<I", rom[lit_addr - BASE:lit_addr - BASE + 4])[0]
                text += f"   ; [{lit_addr:07X}] = {lit:08X}"
            except Exception:
                pass
        # annotate internal branch targets
        if ins.mnemonic.startswith(("b", "bl")) and ins.op_str.startswith("#"):
            try:
                tgt = int(ins.op_str[1:], 0)
                text += f"   ; -> {tgt:07X}"
            except Exception:
                pass
        print(text)


if __name__ == "__main__":
    main()
