#!/usr/bin/env python3
"""Assemble the English-patched ROM copy and emit the BPS patch.

Never touches `rom/monster-guardians.gba`: everything is applied to an
in-memory copy of the user's ROM, written to `build/patch/`, and shipped
as a BPS patch in `dist/`.

Free-space allocator: the one free block `0x76765D..0x800000` (625,059
bytes, 0x00 fill) is handed out sequentially in 16-byte aligned chunks.
Every allocation is recorded in `build/patch/allocations.json`.

Stages are cumulative; the current milestone is `--stage story`:
  font   relocate the 685-glyph story bigfont store (22 B/glyph) and
         rewrite the single descriptor pointer at 0xD6C2C.
  story  font + append 95 ASCII glyphs to the store + encode all 96 EN
         story messages, relocate the streams (keeping bank order and the
         L28/L29 chain) and retarget every message pointer, then patch the
         renderer (7 px advance, explicit-break wrapping) and localize the
         R1 insert tables (753E beast names, 753F words).

Usage:
  .venv/bin/python tools/build_patch.py [--stage story] [--no-bps]
"""
import argparse
import importlib.util
import json
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROM_PATH = ROOT / "rom" / "monster-guardians.gba"
BUILD = ROOT / "build" / "patch"
DIST = ROOT / "dist"

FREE_START = 0x767660          # first 0x10-aligned byte of the free block
FREE_END = 0x800000

# Story bigfont (large-glyph narration subsystem).
STORY_FONT_OFF = 0xD3144
STORY_FONT_GLYPHS = 685
STORY_FONT_STRIDE = 22
STORY_FONT_SIZE = STORY_FONT_GLYPHS * STORY_FONT_STRIDE   # 15,070
STORY_FONT_PTR_OFF = 0xD6C2C   # descriptor field {u16,u16,u32,ptr,...}
STORY_FONT_PTR_VALUE = 0x080D3144

ASCII_FIRST, ASCII_LAST = 0x20, 0x7E

# R1 dynamic-insert tables (bigfont strings, 0x7FFF-terminated).  The 753E
# handler at 0x8135D indexes 0xC7410 by slot*2+gender; the 753F handler at
# 0x8138D indexes 0xC73F0 the same way (its literal, not 0xC7400).
INSERT_753E_TABLE = 0xC7410       # 9 slots x 2 variants
INSERT_753F_TABLE = 0xC73F0       # 4 slots x 2 variants
INSERT_753F_WORDS = [
    ("I", "I"),
    ("son", "daughter"),
    ("the Legendary Beast Tamer", "the Legendary Beast Tamer"),
    ("he", "she"),
]
INSERT_NAMES_JSON = ROOT / "translation" / "story_insert_names.json"

# Story text layout (renderer) patch: 7 px per glyph, 31-char safety wrap.
# The per-character advance is `font->w + 1` (descriptor w at 0xD6C24, 0x0B).
# The wrap compares the column counter against 17 (line 1) / 16 (later lines);
# both are raised to 31 so the explicit EN line breaks alone control layout
# (longest translated line is 30 chars, which also fits the box interior).
FONT_W_OFF = 0xD6C24
FONT_W_ORIG = 0x0B
FONT_W_NEW = 0x06               # advance 7 px
WRAP1_OFF = 0x81094             # movs r2,#0x11  (17) on the first text line
WRAP2_OFF = 0x8109C             # movs r2,#0x10  (16) on later lines
WRAP_ORIG = (0x2211, 0x2210)
WRAP_NEW = 0x221F               # movs r2,#0x1F (31)

# Page glyph list.  The story box allocates a 34-entry (0x220 byte) list of
# 16-byte glyph slots -- exactly the JP layout of 17 + 16 glyphs per two-line
# page.  Two EN lines hold up to 60 glyphs, so grow the allocation to 64
# entries (0x400) and raise every walker bound from 0x21 (33) to 0x3F (63):
#   0x80D04  FUN_08080CF0  destroy-all loop
#   0x80DA4  FUN_08080D84  list reset loop (fills 1/0 marker fields)
#   0x8102C  FUN_08081010  free-slot scan before adding a glyph
#   0x817F0  FUN_08081764  scroll/advance loop (line--, destroy, rise)
#   0x80F92  printer       page glyph-count guard (count > 32 -> close box)
# obj[0x28] is the live page glyph count; FUN_08081830 decrements it when a
# glyph is destroyed, so a 30-char page (60 glyphs) stays within the new bound.
GLYPH_LIST_ALLOC_OFF = 0x80BAE
GLYPH_LIST_ALLOC_ORIG = bytes.fromhex("88208000")   # movs r0,#0x88; lsls r0,r0,#2
GLYPH_LIST_ALLOC_NEW = bytes.fromhex("8020c000")    # movs r0,#0x80; lsls r0,r0,#3
GLYPH_LIST_BOUNDS = (
    (0x80D04, 0x2C21, 0x2C3F, "destroy-all loop 33 -> 63"),
    (0x80DA4, 0x2121, 0x213F, "list reset loop 33 -> 63"),
    (0x8102C, 0x2B21, 0x2B3F, "free-slot scan 33 -> 63"),
    (0x817F0, 0x2E21, 0x2E3F, "scroll/advance loop 33 -> 63"),
    (0x80F92, 0x2820, 0x283E, "page glyph-count guard 32 -> 62"),
)

ROM_BASE = 0x08000000

CHAINED = {92}                 # staff-roll card: engine chains in, no pointer


class Patcher:
    def __init__(self, data):
        self.orig = bytes(data)
        self.data = bytearray(data)
        self.cursor = FREE_START
        self.allocations = []
        self.patches = []

    def alloc(self, size, name, align=16):
        start = (self.cursor + align - 1) & ~(align - 1)
        if start + size > FREE_END:
            raise SystemExit(f"free space exhausted allocating {name}")
        self.cursor = start + size
        # free space must be 0x00 filled before use
        if any(self.data[start:start + size]):
            raise SystemExit(f"free block not empty at {start:#x} ({name})")
        self.allocations.append({"name": name, "offset": start,
                                 "size": size, "end": start + size})
        return start

    def poke(self, off, blob, label):
        self.data[off:off + len(blob)] = blob
        self.patches.append({"label": label, "offset": off,
                             "size": len(blob)})

    def poke_u32(self, off, value, label):
        self.poke(off, struct.pack("<I", value), label)


def stage_font(p):
    """Relocate the story bigfont store and retarget its pointer."""
    if struct.unpack_from("<I", p.data, STORY_FONT_PTR_OFF)[0] != STORY_FONT_PTR_VALUE:
        raise SystemExit("story font pointer does not match the expected value")
    dst = p.alloc(STORY_FONT_SIZE, "story_bigfont_store", align=16)
    p.poke(dst, p.orig[STORY_FONT_OFF:STORY_FONT_OFF + STORY_FONT_SIZE],
           "story bigfont store copy")
    p.poke_u32(STORY_FONT_PTR_OFF, ROM_BASE | dst,
               "story bigfont descriptor pointer")
    return dst


def stage_renderer(p):
    """Story text layout: 7 px advance + explicit-break-only wrapping."""
    for off, want, what in ((FONT_W_OFF, FONT_W_ORIG, "font w"),
                            (WRAP1_OFF, WRAP_ORIG[0], "wrap line 1"),
                            (WRAP2_OFF, WRAP_ORIG[1], "wrap later lines")):
        got = struct.unpack_from("<H", p.data, off)[0]
        if got != want:
            raise SystemExit(f"{what} at {off:#x}: expected {want:#06x}, got {got:#06x}")
    p.poke(FONT_W_OFF, struct.pack("<H", FONT_W_NEW), "story font w -> 6 (7 px advance)")
    p.poke(WRAP1_OFF, struct.pack("<H", WRAP_NEW), "story wrap line 1 -> 31")
    p.poke(WRAP2_OFF, struct.pack("<H", WRAP_NEW), "story wrap later lines -> 31")

    if p.orig[GLYPH_LIST_ALLOC_OFF:GLYPH_LIST_ALLOC_OFF + 4] != GLYPH_LIST_ALLOC_ORIG:
        raise SystemExit(f"glyph list alloc at {GLYPH_LIST_ALLOC_OFF:#x} does not match")
    p.poke(GLYPH_LIST_ALLOC_OFF, GLYPH_LIST_ALLOC_NEW,
           "glyph list alloc 0x220 -> 0x400 (34 -> 64 slots)")
    for off, want, new, label in GLYPH_LIST_BOUNDS:
        got = struct.unpack_from("<H", p.data, off)[0]
        if got != want:
            raise SystemExit(f"glyph list bound at {off:#x}: expected {want:#06x}, got {got:#06x}")
        p.poke(off, struct.pack("<H", new), f"glyph list bound {off:#x}: {label}")
    print(f"renderer: font w {FONT_W_ORIG:#x} -> {FONT_W_NEW:#x} at {FONT_W_OFF:#x}; "
          f"wrap {WRAP_ORIG[0]:#06x}/{WRAP_ORIG[1]:#06x} -> {WRAP_NEW:#06x}; "
          f"glyph list 34 -> 64 slots")


def en_bigfont_words(text, code_map):
    """EN string -> bigfont u16 words + 0x7FFF terminator."""
    words = []
    for ch in text:
        if ch not in code_map:
            raise SystemExit(f"unencodable insert character {ch!r}")
        words.append(code_map[ch])
    words.append(0x7FFF)
    return struct.pack(f"<{len(words)}H", *words)


def stage_inserts(p):
    """Localize the 753E beast-name and 753F word insert tables."""
    ins = load_insert_story()
    code_map = ins.ascii_code_map()
    entries = json.loads(INSERT_NAMES_JSON.read_text())["entries"]
    if len(entries) != 18:
        raise SystemExit(f"753E table has {len(entries)} entries, expected 18")

    # --- 753E: 9 slots x 2 gender variants, strings + pointer table
    seen = set()
    for e in entries:
        slot, variant = int(e["slot"]), int(e["variant"])
        ptr_off = int(e["ptr_src"], 16)
        want = ROM_BASE | int(e["rom_target"], 16)
        got = struct.unpack_from("<I", p.data, ptr_off)[0]
        if got != want:
            raise SystemExit(
                f"753E pointer {ptr_off:#x}: expected {want:#010x}, got {got:#010x}")
        if (slot, variant) in seen:
            raise SystemExit(f"753E duplicate slot {slot} variant {variant}")
        seen.add((slot, variant))
        blob = en_bigfont_words(e["en"], code_map)
        dst = p.alloc(len(blob), f"insert_753E_{slot}_{variant}", align=2)
        p.poke(dst, blob, f"753E slot {slot} v{variant} = {e['en']!r}")
        p.poke_u32(ptr_off, ROM_BASE | dst, f"753E table[{slot}x2+{variant}]")
    if seen != {(s, v) for s in range(9) for v in range(2)}:
        raise SystemExit("753E table is missing (slot, variant) entries")

    # --- 753F: 4 slots x 2 gender variants ("I", son/daughter, ...)
    for slot, pair in enumerate(INSERT_753F_WORDS):
        for variant, text in enumerate(pair):
            ptr_off = INSERT_753F_TABLE + slot * 8 + variant * 4
            old = struct.unpack_from("<I", p.data, ptr_off)[0]
            if not (ROM_BASE + 0xC0000 < old < ROM_BASE + 0xD30F4):
                raise SystemExit(
                    f"753F pointer {ptr_off:#x} does not look like an R1 string: {old:#010x}")
            blob = en_bigfont_words(text, code_map)
            dst = p.alloc(len(blob), f"insert_753F_{slot}_{variant}", align=2)
            p.poke(dst, blob, f"753F slot {slot} v{variant} = {text!r}")
            p.poke_u32(ptr_off, ROM_BASE | dst, f"753F table[{slot}x2+{variant}]")
    print(f"inserts: 18 beast-name strings + 8 word strings relocated")


def load_insert_story():
    spec = importlib.util.spec_from_file_location(
        "insert_story", ROOT / "tools" / "insert_story.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_insert_8x8():
    spec = importlib.util.spec_from_file_location(
        "insert_8x8", ROOT / "tools" / "insert_8x8.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def stage_8x8(p):
    """Insert the English 8x8 menu / UI / item / monster text."""
    mod = load_insert_8x8()
    rows = mod.load_rows()
    rows, blocked = mod.apply(p, rows)
    mod.report(rows)
    print(f"8x8: {sum(1 for r in rows if r['action'] == 'reloc')} relocated, "
          f"{sum(1 for r in rows if r['action'] == 'inplace')} in place, "
          f"{sum(1 for r in rows if r['action'] == 'field')} name fields, "
          f"{len(blocked)} blocked")
    return rows


def encode_bl(addr, target):
    """Encode a Thumb-2 BL from `addr` to `target`."""
    off = target - (addr + 4)
    if not -(1 << 24) <= off < (1 << 24):
        raise SystemExit(f"BL out of range {addr:#x} -> {target:#x}")
    s = (off >> 24) & 1
    i1 = (off >> 23) & 1
    i2 = (off >> 22) & 1
    imm10 = (off >> 12) & 0x3FF
    imm11 = (off >> 1) & 0x7FF
    # Thumb-2 encodes J1/J2 inverted relative to I1/I2 when S is clear,
    # and straight when S is set.
    j1 = 1 - (i1 ^ s)
    j2 = 1 - (i2 ^ s)
    h1 = 0xF000 | (s << 10) | imm10
    # second halfword: 11 J1 1 J2 imm11
    h2 = 0xD000 | (j1 << 13) | (j2 << 11) | imm11
    return struct.pack("<HH", h1, h2)


def stage_engine_fixes(p):
    """Engine fixes independent of which text stages are applied."""
    # 7531 (page clear): the "A held / still revealing" fast path reset the
    # glyph list without destroying the glyph records, so the next page drew
    # on top of the old one.  Use the normal destroy-and-reopen path.
    p.poke(0x8116E, encode_bl(0x8116E, 0x81674),
           "7531 busy page clear destroys glyphs")
    # 7533: same fast/slow split; make the deferred close destroy too.
    p.poke(0x811C4, b"\x00\x21", "7533 busy page clear close_mode 0")


def stage_8x8_fixes(p):
    """Fixes required by the longer English 8x8 strings."""
    # 0x58BF8 draws the 7-glyph "Element" label, but r8 is also the next
    # menu id and must stay 4.
    p.poke(0x58C48, b"\x04\x22", "setup next menu id = 4 (decouple Element count)")
    # The default male name "Leo" is 3 glyphs; the copy length was the JP
    # 2-glyph length.
    p.poke(0x57E1A, b"\x06\x22", "default male name copy 3 glyphs")

    # Status screen: one r4 count is shared by the "Assign"/"Order" labels
    # and two 4-digit number fields.  English needs 6 and 5 glyphs; keep
    # the numbers at 4 with tiny trampolines.
    p.poke(0x36D0E, b"\x06\x24", "Assign label count 6")
    num_tramp = p.alloc(12, "tramp_number_width4", align=2)
    p.poke(num_tramp,
           b"\x10\xb5" + b"\x04\x24" + b"\x00\x94"
           + encode_bl(num_tramp + 6, 0x3D634) + b"\x10\xbd",
           "trampoline: number width 4")
    order_tramp = p.alloc(12, "tramp_order_count5", align=2)
    p.poke(order_tramp,
           b"\x10\xb5" + b"\x05\x24" + b"\x00\x94"
           + encode_bl(order_tramp + 6, 0x3D114) + b"\x10\xbd",
           "trampoline: Order label count 5")
    for addr, target in ((0x36D2E, num_tramp), (0x36D60, num_tramp),
                         (0x36D3E, order_tramp)):
        p.poke(addr, encode_bl(addr, target), f"call trampoline {target:#x}")


def stage_story(p):
    """Extended glyph store + all 96 EN message streams and pointers."""
    ins = load_insert_story()

    # --- glyph store: 685 JP glyphs + 95 ASCII glyphs appended
    if struct.unpack_from("<I", p.data, STORY_FONT_PTR_OFF)[0] != STORY_FONT_PTR_VALUE:
        raise SystemExit("story font pointer does not match the expected value")
    masks = ins.build_ascii_masks(ins.load_glyph_generate())
    ascii_blob = b"".join(masks[chr(c)] for c in range(ASCII_FIRST, ASCII_LAST + 1))
    jp_blob = p.orig[STORY_FONT_OFF:STORY_FONT_OFF + STORY_FONT_SIZE]
    store = jp_blob + ascii_blob
    store_off = p.alloc(len(store), "story_bigfont_store", align=16)
    p.poke(store_off, store, "story bigfont store (JP + ASCII glyphs)")
    p.poke_u32(STORY_FONT_PTR_OFF, ROM_BASE | store_off,
               "story bigfont descriptor pointer")

    # --- message streams: one contiguous block, bank order preserved so
    # message 92 (staff-roll card) stays right after message 91's stream
    streams = ins.encoded_streams()
    total = sum(len(blob) for _, _, blob in streams)
    base = p.alloc(total, "story_streams", align=2)
    mapping = []
    off = base
    for idx, old, blob in streams:
        p.poke(off, blob, f"story stream {idx}")
        mapping.append({"msg": idx, "old": old, "new": off, "size": len(blob)})
        off += len(blob)

    # --- pointers: every u32 that pointed at an original start
    pointer_patches = 0
    missing = []
    for m in mapping:
        if m["msg"] in CHAINED:
            continue
        hits = ins.pointer_hits(p.orig, m["old"])
        if not hits:
            missing.append(m["msg"])
            continue
        for h in hits:
            p.poke_u32(h, ROM_BASE | m["new"],
                       f"story pointer msg {m['msg']} @ {h:#x}")
            pointer_patches += 1
    if missing:
        raise SystemExit(f"messages with no pointer: {missing}")

    report = {
        "store": {"offset": store_off, "size": len(store),
                  "glyph_count": STORY_FONT_GLYPHS + len(masks)},
        "streams": {"offset": base, "size": total},
        "pointers_patched": pointer_patches,
        "mapping": mapping,
    }
    (BUILD / "story_report.json").write_text(json.dumps(report, indent=1) + "\n")
    print(f"story store -> {store_off:#08x} ({len(store)} bytes, "
          f"{report['store']['glyph_count']} glyphs)")
    print(f"story streams -> {base:#08x} ({total} bytes)")
    print(f"story pointers patched: {pointer_patches}")
    return store_off


# ---------------------------------------------------------------- BPS
def _varint(n):
    out = bytearray()
    while n >= 0x80:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    out.append(n)
    return bytes(out)


def bps_encode(source, target):
    """Minimal valid BPS1: SourceRead for unchanged runs, TargetRead for
    changed runs (no SourceCopy/TargetCopy)."""
    assert len(source) == len(target) or True
    out = bytearray(b"BPS1")
    out += _varint(len(source))
    out += _varint(len(target))
    i = 0
    n = len(target)
    while i < n:
        # unchanged run
        j = i
        while j < n and j < len(source) and source[j] == target[j]:
            j += 1
        if j > i:
            out += _varint(((j - i - 1) << 2) | 0)
            i = j
            continue
        # changed run
        j = i
        while j < n and (j >= len(source) or source[j] != target[j]):
            j += 1
        chunk = target[i:j]
        out += _varint(((len(chunk) - 1) << 2) | 1)
        out += chunk
        i = j
    out += struct.pack("<I", zlib.crc32(source) & 0xFFFFFFFF)
    out += struct.pack("<I", zlib.crc32(target) & 0xFFFFFFFF)
    return bytes(out)


def bps_apply(patch, source):
    """Reference applier used to verify the patch we just wrote."""
    if patch[:4] != b"BPS1":
        raise SystemExit("not a BPS1 patch")
    pos = 4

    def varint():
        nonlocal pos
        shift = 0
        value = 0
        while True:
            b = patch[pos]
            pos += 1
            value |= (b & 0x7F) << shift
            if not (b & 0x80):
                return value
            shift += 7

    src_size = varint()
    tgt_size = varint()
    if src_size != len(source):
        raise SystemExit("BPS source size mismatch")
    out = bytearray()
    src_rel = 0
    tgt_rel = 0
    while len(out) < tgt_size:
        cmd = varint()
        action = cmd & 3
        length = (cmd >> 2) + 1
        if action == 0:                      # SourceRead
            out += source[len(out):len(out) + length]
        elif action == 1:                    # TargetRead
            out += patch[pos:pos + length]
            pos += length
        elif action == 2:                    # SourceCopy
            off = varint()
            src_rel = (src_rel - (off >> 1)) if (off & 1) else (src_rel + (off >> 1))
            out += source[src_rel:src_rel + length]
            src_rel += length
        else:                                # TargetCopy
            off = varint()
            tgt_rel = (tgt_rel - (off >> 1)) if (off & 1) else (tgt_rel + (off >> 1))
            for _ in range(length):
                out.append(out[tgt_rel])
                tgt_rel += 1
    src_crc, tgt_crc = struct.unpack("<II", patch[-8:])
    if zlib.crc32(source) & 0xFFFFFFFF != src_crc:
        raise SystemExit("source CRC mismatch")
    if zlib.crc32(bytes(out)) & 0xFFFFFFFF != tgt_crc:
        raise SystemExit("target CRC mismatch")
    return bytes(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="font")
    ap.add_argument("--no-bps", action="store_true")
    args = ap.parse_args()

    if not ROM_PATH.exists():
        raise SystemExit(f"user ROM missing: {ROM_PATH}")
    rom = ROM_PATH.read_bytes()
    if len(rom) != 0x800000:
        raise SystemExit(f"unexpected ROM size {len(rom):#x}")

    p = Patcher(rom)
    if args.stage == "font":
        dst = stage_font(p)
        print(f"story font store -> {dst:#08x} ({STORY_FONT_SIZE} bytes)")
    elif args.stage == "story":
        stage_story(p)
        stage_renderer(p)
        stage_inserts(p)
    elif args.stage in ("8x8", "all"):
        stage_story(p)
        stage_renderer(p)
        stage_inserts(p)
        stage_8x8(p)
        stage_8x8_fixes(p)
    else:
        raise SystemExit(f"unknown stage {args.stage!r}")

    if args.stage in ("story", "8x8", "all"):
        stage_engine_fixes(p)

    BUILD.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)
    patched = bytes(p.data)
    rom_out = BUILD / "patched.gba"
    rom_out.write_bytes(patched)
    (BUILD / "allocations.json").write_text(
        json.dumps(p.allocations, indent=1) + "\n")
    (BUILD / "patches.json").write_text(
        json.dumps(p.patches, indent=1) + "\n")
    print(f"wrote {rom_out} ({len(patched)} bytes, {len(p.patches)} patches)")

    if not args.no_bps:
        patch = bps_encode(rom, patched)
        bps_path = DIST / "monster-guardians-en.bps"
        bps_path.write_bytes(patch)
        # verify round-trip
        if bps_apply(patch, rom) != patched:
            raise SystemExit("BPS round-trip verification FAILED")
        print(f"wrote {bps_path} ({len(patch)} bytes, round-trip OK)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
