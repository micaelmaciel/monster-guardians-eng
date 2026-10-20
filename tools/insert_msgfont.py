#!/usr/bin/env python3
"""Message-font (9x9) English insertion data.

The field message box uses a 317-glyph 9x9 1bpp font at 0xCDED4 and a
string table at 0xCC92C..0xCDED4.  Its renderer (0xEC38) draws at 10 px
advance and wraps after 11 glyphs, and only a small fullwidth Latin
subset exists in the font.

This module builds:
  * an extended 9x9 store: the 317 JP glyphs plus the ASCII glyphs used
    by the English strings (letters/digits from the 8x8 font, simple
    hand-drawn punctuation);
  * the 169 English strings, encoded for a 9 px advance and a 13-glyph
    first line (the translation supplies an explicit "|" break; the
    first line is padded so the second line starts at glyph 13);
  * a sorted old-pointer -> new-pointer lookup table.  55 of the 169
    JP strings have no direct pointer (they are reached by base+offset
    arithmetic), so instead of retargeting every caller the box
    renderer is hooked and looks up the final pointer at runtime;
  * a small Thumb lookup routine and an 8-byte near stub placed in the
    dead old story-font store at 0xD3144 (the story insertion moved
    that store to free space).

All addresses are file offsets; pointers are 0x08000000 | offset.
"""

import csv
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROM_PATH = ROOT / "rom" / "monster-guardians.gba"
GLYPHS_PATH = ROOT / "data" / "en_glyphs_8x8.json"
RAW_PATH = ROOT / "build" / "msgfont_strings_raw.json"
LINES_PATH = ROOT / "translation" / "msgfont_lines.tsv"

FONT_STORE = 0xCDED4
FONT_GLYPHS = 317
FONT_STRIDE = 18
FONT_DESC_STORE_PTR = 0xCF528
SPACE_CODE = 49
TERM = 0x7FFF
EN_FIRST = 317
LINE1_GLYPHS = 13

# Renderer patch sites (Thumb, file offsets).
RENDERER_HOOK = 0xEC3A          # mov r7,sl ; mov r6,sb  (4 bytes)
RENDERER_WRAP = 0xECB8          # cmp r7,#0xA
RENDERER_LINE2_INIT = 0xECE0    # literal FF9A0000
RENDERER_ADVANCE = 0xECF0       # movs r0,#0xA0 (0xA0000 after lsl 12)
NEAR_STUB = 0xD3144             # dead old story-font store


def load_lines():
    """idx -> "line1|line2" (line2 optional)."""
    out = {}
    with LINES_PATH.open() as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[int(row["idx"])] = row["lines"]
    if sorted(out) != list(range(169)):
        raise SystemExit("msgfont_lines.tsv must cover idx 0..168")
    return out


def load_raw():
    raw = json.loads(RAW_PATH.read_text())
    if len(raw) != 169:
        raise SystemExit("raw msgfont string table is not 169 rows")
    return raw


def load_ascii_glyphs():
    """char -> 8 rows of '0'/'1' (same table the story bigfont uses)."""
    data = json.loads(GLYPHS_PATH.read_text())
    glyphs = data["glyphs"]
    missing = [chr(c) for c in range(0x21, 0x7F) if chr(c) not in glyphs]
    if missing:
        raise SystemExit(f"ASCII glyph table missing: {missing!r}")
    return glyphs


def glyph9(ch, glyphs):
    """Place the 8x8 ASCII glyph in a 9x9 cell (one-pixel top/bottom margin)."""
    if ch not in glyphs:
        raise SystemExit(f"no 9x9 glyph for {ch!r}")
    m = [[0] * 9 for _ in range(9)]
    rows = glyphs[ch]
    for y, row in enumerate(rows):
        for x, bit in enumerate(row):
            if bit == "1":
                m[y + 1][x] = 1
    return m


def pack9(m):
    """Pack a 9x9 mask into the message font's 18-byte format."""
    out = bytearray(18)
    for y in range(8):
        for x in range(8):
            if m[y][x]:
                out[y] |= 1 << (7 - x)
        if m[y][8]:
            out[8 + y] |= 0x80
    for x in range(8):
        if m[8][x]:
            out[16] |= 1 << (7 - x)
    if m[8][8]:
        out[17] |= 0x80
    return bytes(out)


def used_chars(lines):
    chars = set()
    for text in lines.values():
        for part in text.split("|"):
            chars.update(ch for ch in part if ch != " ")
    return sorted(chars)


def build_code_map(lines):
    """char -> glyph code.  Space reuses the existing blank (49)."""
    code = {" ": SPACE_CODE}
    for i, ch in enumerate(used_chars(lines)):
        code[ch] = EN_FIRST + i
    return code


def build_font_blob(rom, lines):
    """317 original glyphs + one glyph per used ASCII character."""
    code = build_code_map(lines)
    glyphs = load_ascii_glyphs()
    used = [ch for ch in used_chars(lines)]
    orig = rom[FONT_STORE:FONT_STORE + FONT_GLYPHS * FONT_STRIDE]
    extra = b"".join(pack9(glyph9(ch, glyphs)) for ch in used)
    blob = orig + extra
    if len(blob) != (FONT_GLYPHS + len(used)) * FONT_STRIDE:
        raise SystemExit("font blob size mismatch")
    return blob, code


def encode_string(text, code):
    parts = text.split("|")
    if len(parts) > 2:
        raise SystemExit(f"too many line breaks: {text!r}")
    first = parts[0]
    second = parts[1] if len(parts) == 2 else ""
    if len(first) > LINE1_GLYPHS or len(second) > LINE1_GLYPHS:
        raise SystemExit(f"line too long: {text!r}")
    codes = [code[ch] for ch in first]
    if second:
        codes += [SPACE_CODE] * (LINE1_GLYPHS - len(codes))
        codes += [code[ch] for ch in second]
    codes.append(TERM)
    return struct.pack("<%dH" % len(codes), *codes)


def build_strings(rom, lines, code):
    """[(idx, old_pointer, encoded_bytes)] in table order."""
    raw = load_raw()
    out = []
    for idx in range(169):
        old = 0x08000000 | int(raw[idx]["start"], 16)
        out.append((idx, old, encode_string(lines[idx], code)))
    return out


def build_lookup_table(pairs):
    """pairs = [(old_ptr, new_ptr)] -> sorted 8-byte entries."""
    pairs = sorted(pairs)
    blob = b"".join(struct.pack("<II", old, new) for old, new in pairs)
    if len(blob) != 8 * 169:
        raise SystemExit("lookup table size mismatch")
    return blob


def build_far_routine(table_off):
    """Thumb routine: map r2 (old string pointer) via the lookup table.

    Entered with lr = 0xEC40 (after the 4-byte hook).  r0/r1 (x,y) are
    preserved; r2 is replaced when a match is found; the two original
    instructions (mov r7,sl / mov r6,sb) are replayed before returning.
    """
    orig = (ROOT / "rom" / "monster-guardians.gba").read_bytes()
    mov1, mov2 = struct.unpack_from("<HH", orig, 0xEC3A)
    code = bytearray()
    code += struct.pack("<H", 0xB403)      # push {r0,r1}
    ldr_pos = len(code)
    code += b"\x00\x00"                    # ldr r3,[pc,#lit]
    code += struct.pack("<H", 0x20A9)      # movs r0,#169
    loop = len(code)
    code += struct.pack("<H", 0x6819)      # ldr r1,[r3]
    code += struct.pack("<H", 0x4291)      # cmp r1,r2
    beq_pos = len(code)
    code += b"\x00\x00"                    # beq found
    code += struct.pack("<H", 0x3308)      # adds r3,#8
    code += struct.pack("<H", 0x3801)      # subs r0,#1
    bne_pos = len(code)
    code += b"\x00\x00"                    # bne loop
    # not found: keep the original pointer
    code += struct.pack("<H", 0xBC03)      # pop {r0,r1}
    code += struct.pack("<H", mov1)
    code += struct.pack("<H", mov2)
    code += struct.pack("<H", 0x4770)      # bx lr
    found = len(code)
    code += struct.pack("<H", 0x685A)      # ldr r2,[r3,#4]
    code += struct.pack("<H", 0xBC03)      # pop {r0,r1}
    code += struct.pack("<H", mov1)
    code += struct.pack("<H", mov2)
    code += struct.pack("<H", 0x4770)      # bx lr
    while len(code) % 4:
        code += b"\x00"
    lit = len(code)
    code += struct.pack("<I", 0x08000000 | table_off)
    base = (ldr_pos + 4) & ~3
    n = lit - base
    if not (0 <= n <= 1020 and n % 4 == 0):
        raise SystemExit(f"far routine literal out of range: {n}")
    code[ldr_pos:ldr_pos + 2] = struct.pack("<H", 0x4B00 | (n >> 2))
    beq_off = (found - (beq_pos + 4)) // 2
    if not -128 <= beq_off <= 127:
        raise SystemExit("beq out of range")
    code[beq_pos:beq_pos + 2] = struct.pack("<H", 0xD000 | (beq_off & 0xFF))
    bne_off = (loop - (bne_pos + 4)) // 2
    if not -128 <= bne_off <= 127:
        raise SystemExit("bne out of range")
    code[bne_pos:bne_pos + 2] = struct.pack("<H", 0xD100 | (bne_off & 0xFF))
    return bytes(code)


def build_near_stub(far_off):
    """8-byte stub at NEAR_STUB: load the far address and bx to it.

    The low bit must be set: bx selects Thumb state from it, and the far
    routine is Thumb code.
    """
    return struct.pack("<HHI", 0x4B00, 0x4718, 0x08000000 | far_off | 1)


def stage(p, encode_bl, rom_base=0x08000000):
    """Apply the message-font insertion to a Patcher-like object.

    `p` must provide: orig, alloc(size, name, align), poke(off, blob, label),
    and allocations.  `encode_bl(addr, target)` returns 4 Thumb BL bytes.
    """
    rom = p.orig
    lines = load_lines()
    blob, code = build_font_blob(rom, lines)

    # 1. extended 9x9 font store
    store_off = p.alloc(len(blob), "msgfont_store", align=4)
    p.poke(store_off, blob, "msgfont extended 9x9 store")
    p.poke(FONT_DESC_STORE_PTR, struct.pack("<I", rom_base | store_off),
           "msgfont descriptor store pointer")

    # 2. English strings
    strings = build_strings(rom, lines, code)
    pairs = []
    for idx, old, data in strings:
        off = p.alloc(len(data), f"msgfont_str_{idx}", align=2)
        p.poke(off, data, f"msgfont EN string {idx}")
        pairs.append((old, rom_base | off))

    # 3. lookup table + far routine
    table_off = p.alloc(8 * 169, "msgfont_lookup", align=4)
    p.poke(table_off, build_lookup_table(pairs), "msgfont lookup table")
    far = build_far_routine(table_off)
    far_off = p.alloc(len(far), "msgfont_lookup_code", align=4)
    p.poke(far_off, far, "msgfont lookup routine")

    # 4. near stub in the dead old story-font store, then hook the renderer
    p.poke(NEAR_STUB, build_near_stub(far_off), "msgfont near stub")
    p.poke(RENDERER_HOOK, encode_bl(RENDERER_HOOK, NEAR_STUB),
           "msgfont renderer hook")
    p.poke(RENDERER_WRAP, b"\x0c\x2f", "msgfont wrap after 13 glyphs")
    p.poke(RENDERER_LINE2_INIT, struct.pack("<I", 0xFF930000),
           "msgfont line-2 x origin (-109)")
    p.poke(RENDERER_ADVANCE, b"\x90\x20", "msgfont advance 9 px")
    return {"store": store_off, "table": table_off,
            "far": far_off, "glyphs": len(used_chars(lines))}


if __name__ == "__main__":
    rom = ROM_PATH.read_bytes()
    lines = load_lines()
    blob, code = build_font_blob(rom, lines)
    strings = build_strings(rom, lines, code)
    print(f"used chars: {len(used_chars(lines))}")
    print(f"font blob: {len(blob)} bytes")
    print(f"strings: {sum(len(x[2]) for x in strings)} bytes")
    print(f"lookup: {8 * 169} bytes")
    far = build_far_routine(0x770000)
    print(f"far routine: {len(far)} bytes")
