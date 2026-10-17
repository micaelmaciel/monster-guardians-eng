#!/usr/bin/env python3
"""Encode English/Japanese text to the game's 16-bit glyph codes.

Uses data/charmap.json (reversed for encoding).

Usage: encode_text.py "some text"
       (newline -> 0x1FF line break)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import charmap

TERMINATOR = 0x0000
LINEBREAK = 0x01FF
SPACE = 0x0001


def build_reverse(table=None):
    table = table or charmap.load()
    rev = {}
    for code, ch in table.items():
        if ch in rev:
            continue
        rev[ch] = code
    return rev


def encode(text, rev=None):
    rev = rev or build_reverse()
    out = []
    for ch in text:
        if ch == "\n":
            out.append(LINEBREAK)
        elif ch == " ":
            out.append(SPACE)
        elif ch in rev:
            out.append(rev[ch])
        else:
            raise ValueError(f"no glyph for {ch!r} (U+{ord(ch):04X})")
    return out


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    codes = encode(text)
    print(" ".join(f"{c:03x}" for c in codes))
    print("; + terminator:", " ".join(f"{c:03x}" for c in codes + [TERMINATOR]))


if __name__ == "__main__":
    main()
