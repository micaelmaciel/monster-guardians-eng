#!/usr/bin/env python3
"""Redraw the pre-rendered 32x16 battle command/target labels in English.

The radial order menu is not drawn with a text routine.  Every label is a
32x16 OBJ sprite with the box and Japanese text baked into 8 tiles (256
bytes, 4bpp).  The ROM copies those tiles verbatim to OBJ VRAM (verified
byte-for-byte against the order-menu VRAM), so the graphics are patched at
their ROM source offsets.

The contiguous label family has three visual styles:
  brown  five commands (Fight/Guard/Flee/Item/Pummel), selected and
         unselected variants;
  teal   six commands (Fight/Guard/Flee/Item/Capture/Leave), selected and
         unselected variants;
  cream  seven commands (Fight/Guard/Flee/Item/Pummel/Capture/Leave) plus
         the "All" target box, one variant each.  Cream uses text index 1
         (black) on fill index 15, so the text colour is also the border
         colour: old text may only be blanked inside the rounded interior.

Only the text pixels are replaced.  The box border, shadow and fill are
left untouched; the label's own text colour (and optional 1 px shadow) is
reused.  English text uses the project's 8x8 ASCII glyphs, trimmed to the
ink box and packed with a 1 px gap where it fits in the rounded 20/22 px
interior.  The labels are abbreviated because the boxes are only 32x16.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLYPHS_PATH = ROOT / "data" / "en_glyphs_8x8.json"
LABELS_PATH = ROOT / "translation" / "battle_labels_en.tsv"

INTERIOR_X0, INTERIOR_X1 = 5, 26
INTERIOR_Y0, INTERIOR_Y1 = 4, 11
INTERIOR_W = INTERIOR_X1 - INTERIOR_X0 + 1


def load_glyphs():
    return json.loads(GLYPHS_PATH.read_text())["glyphs"]


def load_labels():
    rows = []
    lines = LABELS_PATH.read_text().splitlines()
    if not lines:
        raise SystemExit(f"empty label table: {LABELS_PATH}")
    header = lines[0].split("\t")
    for line in lines[1:]:
        if not line.strip():
            continue
        fields = line.split("\t")
        if len(fields) != len(header):
            raise SystemExit(f"bad row in {LABELS_PATH}: {line!r}")
        row = dict(zip(header, fields))
        rows.append({
            "tile": int(row["tile"], 16),
            "offset": int(row["offset"], 16),
            "style": row["style"],
            "variant": row["variant"],
            "jp": row["jp"],
            "en": row["en"],
            "text_idx": int(row["text"]),
            "shadow_idx": int(row["shadow"]) if row["shadow"] else None,
            "fill_idx": int(row["fill"]),
        })
    if len(rows) < 6:
        raise SystemExit(f"expected at least 6 battle labels, got {len(rows)}")
    return rows


def decode(data):
    """256-byte 4bpp 32x16 tile block -> 16 rows of 32 palette indices."""
    if len(data) != 256:
        raise ValueError("label block must be 256 bytes")
    grid = [[0] * 32 for _ in range(16)]
    for ty in range(2):
        for tx in range(4):
            off = (ty * 4 + tx) * 32
            for y in range(8):
                for x in range(8):
                    b = data[off + y * 4 + x // 2]
                    grid[ty * 8 + y][tx * 8 + x] = (
                        (b & 0xF) if x % 2 == 0 else (b >> 4))
    return grid


def encode(grid):
    """16 rows of 32 palette indices -> 256-byte 4bpp 32x16 tile block."""
    out = bytearray(256)
    for ty in range(2):
        for tx in range(4):
            off = (ty * 4 + tx) * 32
            for y in range(8):
                for x in range(0, 8, 2):
                    lo = grid[ty * 8 + y][tx * 8 + x] & 0xF
                    hi = grid[ty * 8 + y][tx * 8 + x + 1] & 0xF
                    out[off + y * 4 + x // 2] = lo | (hi << 4)
    return bytes(out)


def ink_bbox(glyphs, ch):
    xs, ys = [], []
    for y, row in enumerate(glyphs[ch]):
        for x, c in enumerate(row):
            if c == "1":
                xs.append(x)
                ys.append(y)
    if not xs:
        raise SystemExit(f"glyph {ch!r} has no ink")
    return min(xs), min(ys), max(xs), max(ys)


def text_width(glyphs, text, gap):
    width = 0
    for i, ch in enumerate(text):
        b = ink_bbox(glyphs, ch)
        width += b[2] - b[0] + 1
        if i:
            width += gap
    return width


def safe_mask():
    """Rounded 22 px box interior: 20 px on the top/bottom rows, 22 between."""
    mask = [[False] * 32 for _ in range(16)]
    for y in range(INTERIOR_Y0, INTERIOR_Y1 + 1):
        x0, x1 = (6, 25) if y in (INTERIOR_Y0, INTERIOR_Y1) else (5, 26)
        for x in range(x0, x1 + 1):
            mask[y][x] = True
    return mask


def pixel_positions(glyphs, text, x0, y0, shadow):
    """Text pixels and (optionally) shadow pixels for a candidate placement."""
    text_px, shadow_px = [], []
    x = x0
    for ch in text:
        minx, miny, maxx, maxy = ink_bbox(glyphs, ch)
        for yy in range(miny, maxy + 1):
            row = glyphs[ch][yy]
            for xx in range(minx, maxx + 1):
                if row[xx] != "1":
                    continue
                px, py = x + (xx - minx), y0 + yy
                text_px.append((px, py))
                if shadow is not None:
                    shadow_px.append((px + 1, py + 1))
        x += maxx - minx + 1
    return text_px, shadow_px


def find_placement(glyphs, text, shadow, mask):
    """Pick the best 1 px-gap placement, falling back to 0 px if needed.

    The text must stay on the rounded box interior.  The 1 px drop shadow may
    be clipped by the interior edge; the original selected labels also clip
    their shadow at the border.
    """
    for gap in (1, 0):
        width = text_width(glyphs, text, gap) + (1 if shadow is not None else 0)
        if width > INTERIOR_W:
            continue
        candidates = []
        for y0 in (INTERIOR_Y0, INTERIOR_Y0 + 1):
            for x0 in range(INTERIOR_X0, 32 - width + 1):
                text_px, _shadow_px = pixel_positions(
                    glyphs, text, x0, y0, shadow)
                if all(0 <= x < 32 and 0 <= y < 16 and mask[y][x]
                       for x, y in text_px):
                    score = abs((x0 + width / 2) - 15.5) + abs((y0 + 3.5) - 7.5)
                    candidates.append((score, x0, y0, gap, width))
        if candidates:
            return min(candidates)
    raise SystemExit(f"label {text!r} does not fit the box interior")


def draw_text(grid, glyphs, text, x0, y0, color, shadow=None, mask=None):
    x = x0
    for ch in text:
        minx, miny, maxx, maxy = ink_bbox(glyphs, ch)
        for yy in range(miny, maxy + 1):
            row = glyphs[ch][yy]
            for xx in range(minx, maxx + 1):
                if row[xx] != "1":
                    continue
                px, py = x + (xx - minx), y0 + yy
                if shadow is not None:
                    sx, sy = px + 1, py + 1
                    if mask is None or (0 <= sx < 32 and 0 <= sy < 16
                                        and mask[sy][sx]):
                        grid[sy][sx] = shadow
                grid[py][px] = color
        x += maxx - minx + 1


def build_block(original, glyphs, text, text_idx, shadow_idx, fill_idx):
    """Return a redrawn 256-byte label block and its placement details."""
    grid = decode(original)
    if encode(grid) != original:
        raise SystemExit("label block does not round-trip through 4bpp decode")

    if not any(grid[y][x] == text_idx
               for y in range(16) for x in range(32)):
        raise SystemExit(f"expected text index {text_idx:#x} not found in label")

    mask = safe_mask()
    # Blank the old text to the box fill inside the rounded interior.  The
    # cream 'All' style uses index 1 for both its text and its dark border,
    # so this must not be a global colour replacement.
    for y in range(16):
        for x in range(32):
            if mask[y][x] and (grid[y][x] == text_idx
                               or (shadow_idx is not None
                                   and grid[y][x] == shadow_idx)):
                grid[y][x] = fill_idx

    # Place the text only on the rounded interior, preferring a 1 px gap.
    score, x0, y0, gap, width = find_placement(
        glyphs, text, shadow_idx, mask)
    draw_text(grid, glyphs, text, x0, y0, text_idx, shadow_idx, mask)
    out = encode(grid)

    # Everything outside the rounded interior is structural: transparent 0
    # and border 1/2 must not change.  Inside the interior, old fill and old
    # text pixels may be replaced.
    before = decode(original)
    after = decode(out)
    for y in range(16):
        for x in range(32):
            if (not mask[y][x] and before[y][x] in (0, 1, 2)
                    and after[y][x] != before[y][x]):
                raise SystemExit(
                    f"label box pixel changed at ({x},{y}): "
                    f"{before[y][x]} -> {after[y][x]}")

    return out, {"x0": x0, "y0": y0, "gap": gap, "width": width}


def stage(p):
    glyphs = load_glyphs()
    labels = load_labels()
    changed = 0
    for row in labels:
        off = row["offset"]
        if p.data[off:off + 256] != p.orig[off:off + 256]:
            raise SystemExit(f"battle label at {off:#x} was already modified")
        block, info = build_block(
            bytes(p.orig[off:off + 256]), glyphs, row["en"],
            row["text_idx"], row["shadow_idx"], row["fill_idx"])
        if block == p.orig[off:off + 256]:
            raise SystemExit(f"battle label at {off:#x} did not change")
        p.poke(off, block,
              f"battle label {row['style']}/{row['variant']} "
              f"{row['tile']:#05x}: {row['jp']} -> {row['en']}")
        changed += 1
        print(f"battle label {row['style']:5s} {row['variant']:5s} "
              f"{row['tile']:#05x} {off:#08x}: "
              f"{row['jp']} -> {row['en']!r} "
              f"(x={info['x0']}, y={info['y0']}, gap={info['gap']}, "
              f"w={info['width']})")
    return changed
