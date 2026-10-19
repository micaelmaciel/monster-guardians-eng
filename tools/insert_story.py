#!/usr/bin/env python3
"""Story-bank insertion logic: EN encoding, glyph store, relocation.

Used by `tools/build_patch.py --stage story`. Importable for QA in
`--check` mode (no ROM writes):

  .venv/bin/python tools/insert_story.py --check

Encoding rules
  * glyph codes: ASCII 0x20-0x7E are appended to the 685-glyph story
    store in ASCII order (codes 0x2AD..); the JP glyph for ❋ (code 670)
    is reused for the star; every EN character must be encodable.
  * the `\\n` in an EN run becomes a 0x7530 line break; all other
    control words (7530/7532/7534/7535/7536/7537/7538/7539/753E/753F/
    7540) pass through unchanged, and each message keeps its 0x7FFF
    terminator.
  * relocated messages are written to free space in index order, so
    L28/L29 (message 91/92) stay physically adjacent: message 92 is the
    staff-roll card that the engine chains into (it has no pointer).
"""
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STORY_FONT_OFF = 0xD3144
STORY_FONT_GLYPHS = 685
STORY_FONT_STRIDE = 22
STORY_FONT_SIZE = STORY_FONT_GLYPHS * STORY_FONT_STRIDE
STORY_FONT_PTR_OFF = 0xD6C2C
STORY_FONT_PTR_VALUE = 0x080D3144

ASCII_FIRST = STORY_FONT_GLYPHS            # 0x2AD
ASCII_LAST = 0x7E
REUSE_CODES = {"❋": 670, "～": 109}        # JP glyphs reused in EN

EARLY_RAW = ROOT / "build" / "story_messages_raw.json"
LATE_RAW = ROOT / "build" / "late_story_raw.json"
EARLY_EN = ROOT / "translation" / "story_en_runs.json"
LATE_EN = ROOT / "translation" / "late_story_en_runs.json"
GLYPHS_JSON = ROOT / "data" / "en_glyphs_8x8.json"

EARLY_START = 0xCFF84
BANK_END = 0xD30F4            # status word list starts here
GLYPH_TOP = 2            # vertical placement of the 8x8 ASCII glyph in the 11-row cell


def load_glyph_generate():
    """ASCII char -> 8x8 rows (strings of '0'/'1')."""
    return json.loads(GLYPHS_JSON.read_text())["glyphs"]


def ascii_code_map():
    """ASCII char -> story glyph code (appended after the JP glyphs)."""
    return {chr(c): ASCII_FIRST + (c - 0x20) for c in range(0x20, ASCII_LAST + 1)}


def build_ascii_masks(glyphs):
    """[char] -> 22-byte 1bpp mask (16x11 cell, glyph at left 8 px)."""
    masks = {}
    for ch, rows in glyphs.items():
        data = bytearray(22)

        def put(x, y, v):
            if v:
                if y < 8:
                    if x < 8:
                        data[y] |= 1 << (7 - x)
                    else:
                        data[8 + y] |= 1 << (15 - x)
                else:
                    if x < 8:
                        data[16 + (y - 8)] |= 1 << (7 - x)
                    else:
                        data[19 + (y - 8)] |= 1 << (15 - x)

        for y, row in enumerate(rows):
            for x, bit in enumerate(row):
                if bit == "1":
                    put(x, y + GLYPH_TOP, 1)
        masks[ch] = bytes(data)
    return masks


def load_messages():
    """[(index, items, en_runs)] for all 96 messages; items from parse."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "story_en_export", ROOT / "tools" / "story_en_export.py")
    sx = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sx)
    early = json.loads(EARLY_RAW.read_text())["messages"]
    late = json.loads(LATE_RAW.read_text())["messages"]
    early_en = json.loads(EARLY_EN.read_text())
    late_en = json.loads(LATE_EN.read_text())
    en = [early_en[str(i)] for i in range(len(early))]
    en += [late_en[str(i)] for i in range(len(late))]
    out = []
    raw = [(m["raw"]) for m in early] + [(m["raw"]) for m in late]
    for i, tokens in enumerate(raw):
        runs = en[i]
        items = sx.parse_message(tokens)
        n_runs = sum(1 for it in items if it[0] == "text")
        if n_runs != len(runs):
            raise SystemExit(f"msg {i}: run count {len(runs)} != {n_runs}")
        out.append((i, items, runs))
    return out


def encode_message(items, runs, code_map):
    """items + EN runs -> list of u16 words (with 0x7FFF terminator)."""
    words = []
    ri = 0
    unknown = set()
    for it in items:
        if it[0] == "text":
            text = runs[ri]
            ri += 1
            parts = text.split("\n")
            for k, part in enumerate(parts):
                if k:
                    words.append(0x7530)
                for ch in part:
                    if ch in REUSE_CODES:
                        words.append(REUSE_CODES[ch])
                    elif ch in code_map:
                        words.append(code_map[ch])
                    else:
                        unknown.add(ch)
        else:
            words.append(it[1])
            for p in it[2]:
                words.append(int(p, 16))
    words.append(0x7FFF)
    if unknown:
        raise SystemExit(f"unencodable characters: {sorted(unknown)}")
    if ri != len(runs):
        raise SystemExit(f"used {ri} of {len(runs)} EN runs")
    return words


def charsets(messages):
    per = {}
    for i, items, runs in messages:
        chars = set("".join(runs)) - {"\n"}
        per[i] = chars
    return per


def message_starts():
    """Original start offsets for all 96 messages (computed, verified).

    The JP bank is one contiguous run of 0x7FFF-terminated streams; the
    walk must land exactly on the status word list at 0xD30F4.
    """
    early = json.loads(EARLY_RAW.read_text())["messages"]
    late = json.loads(LATE_RAW.read_text())["messages"]
    raw_lens = [len(m["raw"]) for m in early] + [len(m["raw"]) for m in late]
    starts = []
    off = EARLY_START
    for n in raw_lens:
        starts.append(off)
        off += n * 2 + 2
    if off != BANK_END:
        raise SystemExit(f"message walk ends at {off:#x}, expected {BANK_END:#x}")
    return starts


def encoded_streams():
    """[(index, old_start, blob)] for all 96 EN streams, in bank order."""
    code_map = ascii_code_map()
    starts = message_starts()
    out = []
    for (i, items, runs), old in zip(load_messages(), starts):
        words = encode_message(items, runs, code_map)
        blob = struct.pack(f"<{len(words)}H", *words)
        out.append((i, old, blob))
    return out


def pointer_hits(rom, old_start):
    """Every u32 in the ROM that points at `old_start`."""
    pat = struct.pack("<I", 0x08000000 | old_start)
    hits = []
    j = 0
    while True:
        k = rom.find(pat, j)
        if k < 0:
            return hits
        hits.append(k)
        j = k + 1


def check():
    glyphs = load_glyph_generate()
    code_map = ascii_code_map()
    masks = build_ascii_masks(glyphs)
    messages = load_messages()

    starts = message_starts()
    rom = (ROOT / "rom" / "monster-guardians.gba").read_bytes()

    total_words = 0
    total_chars = set()
    no_ptr = []
    for (i, items, runs), start in zip(messages, starts):
        words = encode_message(items, runs, code_map)
        total_words += len(words)
        total_chars.update("".join(runs))
        if not pointer_hits(rom, start):
            no_ptr.append(i)
    print(f"messages: {len(messages)}")
    print(f"total EN words: {total_words} ({total_words*2} bytes)")
    print(f"EN charset: {len(total_chars - {chr(10)})} chars")
    missing = sorted(c for c in total_chars - {"\n", "❋", "～"}
                     if c not in code_map)
    print(f"not encodable: {missing}")
    print(f"ASCII glyphs: {len(masks)}")
    print(f"new store: {STORY_FONT_SIZE + len(masks)*STORY_FONT_STRIDE} bytes "
          f"({STORY_FONT_GLYPHS + len(masks)} glyphs)")
    print(f"messages without a pointer (chained): {no_ptr}")
    print(f"stream bytes: {sum(len(b) for _, _, b in encoded_streams())}")
    print("starts ok; check passes")
    return 0


if __name__ == "__main__":
    import sys
    if "--check" in sys.argv:
        sys.exit(check())
    print(__doc__)
