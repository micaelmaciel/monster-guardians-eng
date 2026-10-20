#!/usr/bin/env python3
"""Monster status screen: English labels and one-line descriptions.

The status view draws one label from the bigfont list at 0xD30F4
(13 pointer entries at 0xC4DD0) and one description from the 9x9 message
font (13 pointer entries at 0xC4E04).  Both renderers read their strings
until 0x7FFF.

We relocate the 13 labels into free space as bigfont ASCII strings and
replace the description pointers with short single-line message-font
strings.  The long message-box translations (msgfont 125-137) stay in
place for the menu help text; the status box only has room for one line,
so status-specific short forms live here.

The label renderer advances 12 px per glyph (a JP 16x11 cell).  English
letters are 8 px wide, so its advance is patched to 8 px to keep long
labels such as "Durability" inside the label column.
"""
import csv
import importlib.util
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LABEL_TABLE = 0xC4DD0
DESC_TABLE = 0xC4E04
COUNT = 13
TERM = 0x7FFF
BIGFONT_ASCII_FIRST = 685          # insert_story appends ASCII at 685+
BIGFONT_ASCII_BASE = 0x20
LABEL_ADVANCE_OFF = 0x2F24E        # adds r0,#0xc

# Keep these in sync with translation/msgfont_en.tsv indices 125-137.
LABELS = [
    "Life",
    "Durability",
    "Attack",
    "Defense",
    "Agility",
    "Knowledge",
    "Special",
    "Counter",
    "Recon",
    "Obedience",
    "Accuracy",
    "Evasion",
    "Skill",
]
DESCRIPTIONS = [
    "Faints at zero.",
    "Smaller openings.",
    "Raises damage.",
    "Cuts damage taken.",
    "Raises move speed.",
    "Less wasted moves.",
    "Better specials.",
    "Better counters.",
    "Seeks favored foe.",
    "Obeys orders more.",
    "Better hit rate.",
    "Better evasion.",
    "Eliminate rate up.",
]

# The description row is an 18-tile strip in the EWRAM glyph buffer
# (base 0x02020000 + 0x2C0, one 32-byte tile per 8 px).  A 19th glyph is
# written past the strip and never appears on screen.
MAX_DESC = 18


def load_msgfont():
    spec = importlib.util.spec_from_file_location(
        "insert_msgfont", ROOT / "tools" / "insert_msgfont.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def encode_bigfont(text):
    if any(not (0x20 <= ord(ch) <= 0x7E) for ch in text):
        raise SystemExit(f"bigfont label not ASCII: {text!r}")
    codes = [BIGFONT_ASCII_FIRST + ord(ch) - BIGFONT_ASCII_BASE for ch in text]
    codes.append(TERM)
    return struct.pack("<%dH" % len(codes), *codes)


def encode_msgfont(text, code_map):
    missing = sorted({ch for ch in text if ch not in code_map})
    if missing:
        raise SystemExit(f"message font has no glyph for {missing!r} in {text!r}")
    codes = [code_map[ch] for ch in text]
    codes.append(TERM)
    return struct.pack("<%dH" % len(codes), *codes)


def check():
    mf = load_msgfont()
    code_map = mf.build_code_map(mf.load_lines())
    if len(mf.load_lines()) != 169:
        raise SystemExit("msgfont line table is not 169 entries")
    if len(LABELS) != COUNT or len(DESCRIPTIONS) != COUNT:
        raise SystemExit("status lists are not 13 entries")
    for i, (label, desc) in enumerate(zip(LABELS, DESCRIPTIONS)):
        if len(desc) > MAX_DESC:
            raise SystemExit(f"description {i} too long ({len(desc)}): {desc!r}")
        if len(label) * 8 > 240:
            raise SystemExit(f"label {i} too wide at 8 px: {label!r}")
        encode_bigfont(label)
        encode_msgfont(desc, code_map)
        print(f"{i:2d} {label:<11} {len(label):2d}g {len(label)*8:3d}px@8  "
              f"{desc:<22} {len(desc):2d}g {len(desc)*10:3d}px")
    print(f"labels {sum(map(len, LABELS))} chars, "
          f"descriptions {sum(map(len, DESCRIPTIONS))} chars")


def stage(p, msg_info, rom_base=0x08000000):
    """Apply the status label/description replacement.

    `msg_info["strings"]` must be the (idx, old, new_offset) list returned
    by insert_msgfont.stage().
    """
    for i, desc in enumerate(DESCRIPTIONS):
        if len(desc) > MAX_DESC:
            raise SystemExit(f"description {i} too long ({len(desc)}): {desc!r}")
    mf = load_msgfont()
    code_map = mf.build_code_map(mf.load_lines())
    placed = {idx: off for idx, old, off in msg_info["strings"]}

    # Old tables must still be the untouched JP pointers.
    for i in range(COUNT):
        old = struct.unpack_from("<I", p.orig, LABEL_TABLE + 4 * i)[0]
        if not (0x080D30F4 <= old < 0x080D3144):
            raise SystemExit(f"label pointer {i} unexpected: {old:#x}")
    for i in range(COUNT):
        old = struct.unpack_from("<I", p.orig, DESC_TABLE + 4 * i)[0]
        if not (0x080CDABE <= old < 0x080CDED4):
            raise SystemExit(f"description pointer {i} unexpected: {old:#x}")

    label_offs = []
    for i, label in enumerate(LABELS):
        blob = encode_bigfont(label)
        off = p.alloc(len(blob), f"status_label_{i}", align=2)
        p.poke(off, blob, f"status label {i}: {label}")
        p.poke_u32(LABEL_TABLE + 4 * i, rom_base | off,
                   f"status label pointer {i}")
        label_offs.append(off)

    desc_offs = []
    for i, desc in enumerate(DESCRIPTIONS):
        blob = encode_msgfont(desc, code_map)
        off = p.alloc(len(blob), f"status_desc_{i}", align=2)
        p.poke(off, blob, f"status description {i}: {desc}")
        p.poke_u32(DESC_TABLE + 4 * i, rom_base | off,
                   f"status description pointer {i}")
        desc_offs.append(off)

    # 8 px per English label glyph instead of the JP 12 px cell.
    if p.orig[LABEL_ADVANCE_OFF:LABEL_ADVANCE_OFF + 2] != b"\x0c\x30":
        raise SystemExit("status label advance instruction changed")
    p.poke(LABEL_ADVANCE_OFF, b"\x08\x30", "status label advance 8 px")

    return {"labels": label_offs, "descs": desc_offs,
            "msgfont_strings": placed}


if __name__ == "__main__":
    check()
