#!/usr/bin/env python3
"""Decode every string in build/strings.tsv using the game charmap.

Usage: decode_strings.py [in.tsv] [out.tsv]

Output columns: addr, n_codes, unknown_count, flag, text
flag = TEXT (looks like prose) or DATA (control/esc codes, e.g. 0x7FFF).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import charmap


def main():
    here = os.path.dirname(__file__)
    inp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "build", "strings.tsv")
    outp = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "..", "build", "strings_decoded.tsv")
    table = charmap.load()
    n_text = n_data = 0
    with open(inp) as f, open(outp, "w") as o:
        o.write("addr\tn\tunknown\tflag\ttext\n")
        f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 5:
                continue
            addr = int(p[2], 16)
            codes = [int(c, 16) for c in p[4].split()]
            # strip trailing terminator/padding
            body = [c for c in codes if c != 0x0000 and c != 0xFFFF]
            unknown = [c for c in body if c not in table]
            text = charmap.decode(codes, table)
            flag = "DATA" if any(c >= 0x200 for c in body) else "TEXT"
            if flag == "TEXT":
                n_text += 1
            else:
                n_data += 1
            o.write(f"0x{addr:06X}\t{len(body)}\t{len(unknown)}\t{flag}\t{text}\n")
    print(f"wrote {outp}: {n_text} TEXT, {n_data} DATA")


if __name__ == "__main__":
    main()
