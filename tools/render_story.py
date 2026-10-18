#!/usr/bin/env python3
"""Render bigfont story text to PNG images for direct reading (vision).

The bigfont is the 16x11 px glyph store at ROM 0xD3144 (685 glyphs, 22 bytes
each). Story message token lists live in build/story_messages_raw.json.

Subcommands:
  msg <out.png> <idx> [<idx> ...]
      Render messages in a game-like layout: one panel per "screen"
      (7531 clears the screen), glyphs at the game's 12 px advance and
      13 px line spacing, then a [wait]/[ctl ...] marker inline.
  sheet <outdir> [start] [count] [cols] [rows]
      Labeled glyph sheets (index printed under each glyph) for building
      data/bigfont_charmap.json. Defaults: start 0, count 685, 12 cols,
      8 rows per page.
  glyph <idx> [scale]
      Render a single glyph large, for disambiguating hard readings.

Coordinates: bit row-major, MSB first, left half rows 0-7 at bytes 0-7,
right half rows 0-7 at bytes 8-15, bottom 3 rows left at 16-18, right at
19-21 (see tools/probe_bigfont.py glyph_rows).
"""
import json
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ROM = os.path.join(ROOT, "rom", "monster-guardians.gba")
RAW = os.path.join(ROOT, "build", "story_messages_raw.json")
BASE = 0xD3144
STRIDE = 22
GW, GH = 16, 11

CTL_NEWLINE = 0x7530
CTL_CLEAR = 0x7531
CTL_SCREEN = 0x7532
CTL_WAIT = 0x7534
CTL_OPEN = 0x7535
CTL_CLOSE = 0x7536
CTL_END = 0x7FFF
CTL_OPEN2 = 0x753B
CTL_CLOSE2 = 0x753C


def load_rom():
    with open(ROM, "rb") as f:
        return f.read()


def glyph_rows(data, idx):
    g = data[BASE + idx * STRIDE:BASE + (idx + 1) * STRIDE]
    rows = []
    for r in range(8):
        left, right = g[r], g[8 + r]
        rows.append([(left >> (7 - p)) & 1 for p in range(8)] +
                    [(right >> (7 - p)) & 1 for p in range(8)])
    for r in range(3):
        left, right = g[16 + r], g[19 + r]
        rows.append([(left >> (7 - p)) & 1 for p in range(8)] +
                    [(right >> (7 - p)) & 1 for p in range(8)])
    return rows


def tokens(msg):
    return [int(t, 16) for t in msg["raw"]]


def split_screens(toks):
    """Split a message token list into screens.

    Returns list of screens; each screen is a list of items:
      ("g", idx)       glyph
      ("nl",)          line break (7530)
      ("ctl", tok, param_or_None)  other control
    """
    screens = [[]]
    i = 0
    while i < len(toks):
        t = toks[i]
        if t == CTL_NEWLINE:
            screens[-1].append(("nl",))
        elif t in (CTL_CLEAR, CTL_SCREEN):
            screens.append([])
            screens[-1].append(("ctl", t, None))
        elif t == CTL_END:
            break
        elif t in (CTL_WAIT, 0x7537, CTL_OPEN2, 0x753E, 0x753F):
            # 753F <word id>: word insert. Verified in-game (frame 19200):
            # 753F 0001 renders as ご子息 (msg 21).
            param = toks[i + 1] if i + 1 < len(toks) else None
            screens[-1].append(("ctl", t, param))
            i += 1
        elif t in (0x7538, 0x7539):
            # Two params, no visible text.
            # 7538 verified against in-game msg 22 (frame 19400):
            # "7538 0031 0030 [name]は昨..." displays from the name, so both
            # 0031 and 0030 are consumed and neither shows as text.
            # 7539 same shape (msg 32: 7539 000B 000C / 7539 000D 000D feel
            # like screen-side events; the params must not render as glyphs).
            p1 = toks[i + 1] if i + 1 < len(toks) else None
            p2 = toks[i + 2] if i + 2 < len(toks) else None
            screens[-1].append(("ctl", t, p1))
            i += 2
        elif t == CTL_OPEN:
            # 7535 <style> <delay> <content...> 7536 -- two params.
            # In-game the delay param is not displayed (e.g. msg6:
            # 7535 0001 0004 0065 0065 0065 7536 shows only ・・・).
            p1 = toks[i + 1] if i + 1 < len(toks) else None
            p2 = toks[i + 2] if i + 2 < len(toks) else None
            screens[-1].append(("ctl", t, p1))
            i += 2
        elif t == CTL_CLOSE:
            screens[-1].append(("ctl", t, None))
        elif t == CTL_CLOSE2:
            screens[-1].append(("ctl", t, None))
        elif t == 0xFFFF:
            screens[-1].append(("ctl", t, None))
        elif t >= 0x1000:
            screens[-1].append(("ctl", t, None))
        else:
            screens[-1].append(("g", t))
        i += 1
    return [s for s in screens if s]


def render_msg(data, msg, scale=4, labels=False, wrap=24):
    screens = split_screens(tokens(msg))
    adv = 12 * scale
    lh = (13 + (10 if labels else 0)) * scale
    margin = 8 * scale

    # first pass: measure (wrap long lines)
    panels = []
    for s in screens:
        lines = [[]]
        for it in s:
            if it[0] == "nl":
                lines.append([])
            else:
                if len(lines[-1]) >= wrap:
                    lines.append([])
                lines[-1].append(it)
        panels.append(lines)
    max_len = max((len(l) for p in panels for l in p), default=1)
    box_w = max(15, min(wrap, max_len)) * adv + 2 * margin
    total_h = 0
    panel_h = []
    for lines in panels:
        h = max(1, len(lines)) * lh + 2 * margin
        panel_h.append(h)
        total_h += h + margin

    img = Image.new("RGB", (box_w + 2 * margin, total_h), (40, 40, 40))
    d = ImageDraw.Draw(img)
    y = 0
    for lines, ph in zip(panels, panel_h):
        d.rectangle([margin // 2, y, box_w + margin * 3 // 2 - 1,
                     y + ph - 1], fill=(250, 250, 250), outline=(120, 120, 120))
        ty = y + margin
        for line in lines:
            tx = margin
            for it in line:
                if it[0] == "g":
                    rows = glyph_rows(data, it[1])
                    for ry in range(GH):
                        for rx in range(GW):
                            if rows[ry][rx]:
                                d.rectangle([tx + rx * scale, ty + ry * scale,
                                             tx + (rx + 1) * scale - 1,
                                             ty + (ry + 1) * scale - 1],
                                            fill=(10, 10, 10))
                    if labels:
                        d.text((tx + 2, ty + (GH + 1) * scale), f"{it[1]:03X}",
                               fill=(200, 0, 0))
                else:
                    # control marker: small gray box with hex label
                    tok = it[1]
                    lbl = f"{tok:04X}"
                    d.rectangle([tx, ty + 2 * scale, tx + 4 * len(lbl) + 4,
                                 ty + 9 * scale],
                                outline=(180, 60, 60))
                    d.text((tx + 2, ty + 3 * scale), lbl, fill=(180, 60, 60))
                tx += adv
            ty += lh
        y += ph + margin
    return img


def render_sheet(data, start, count, cols, rows, scale=5):
    cell_w = GW * scale
    cell_h = GH * scale + 18
    pages = []
    per_page = cols * rows
    n_pages = (count + per_page - 1) // per_page
    for p in range(n_pages):
        img = Image.new("RGB", (cols * cell_w + 20, rows * cell_h + 20),
                        (255, 255, 255))
        d = ImageDraw.Draw(img)
        for k in range(per_page):
            idx = start + p * per_page + k
            if idx >= start + count:
                break
            cx = 10 + (k % cols) * cell_w
            cy = 10 + (k // cols) * cell_h
            gr = glyph_rows(data, idx)
            for ry in range(GH):
                for rx in range(GW):
                    if gr[ry][rx]:
                        d.rectangle([cx + rx * scale, cy + ry * scale,
                                     cx + (rx + 1) * scale - 1,
                                     cy + (ry + 1) * scale - 1],
                                    fill=(0, 0, 0))
            d.rectangle([cx - 1, cy - 1, cx + cell_w, cy + GH * scale],
                        outline=(220, 220, 220))
            d.text((cx + 2, cy + GH * scale + 3), f"{idx:03X}", fill=(150, 0, 0))
        pages.append(img)
    return pages


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    data = load_rom()
    cmd = sys.argv[1]
    if cmd == "msg":
        out = sys.argv[2]
        args = sys.argv[3:]
        labels = "--labels" in args
        idxs = [int(a) for a in args if not a.startswith("--")]
        msgs = json.load(open(RAW))["messages"]
        for i in idxs:
            img = render_msg(data, msgs[i], labels=labels)
            name = out.replace(".png", f"_{i:02d}.png")
            img.save(name)
            print(name, img.size)
    elif cmd == "sheet":
        outdir = sys.argv[2]
        start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        count = int(sys.argv[4]) if len(sys.argv) > 4 else 685
        cols = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        rows = int(sys.argv[6]) if len(sys.argv) > 6 else 8
        os.makedirs(outdir, exist_ok=True)
        pages = render_sheet(data, start, count, cols, rows)
        for p, img in enumerate(pages):
            name = os.path.join(outdir, f"glyphs_{start:03X}_p{p}.png")
            img.save(name)
            print(name, img.size)
    elif cmd == "glyph":
        idx = int(sys.argv[2])
        scale = int(sys.argv[3]) if len(sys.argv) > 3 else 16
        img = Image.new("RGB", (GW * scale, GH * scale), (255, 255, 255))
        d = ImageDraw.Draw(img)
        gr = glyph_rows(data, idx)
        for ry in range(GH):
            for rx in range(GW):
                if gr[ry][rx]:
                    d.rectangle([rx * scale, ry * scale,
                                 (rx + 1) * scale - 1, (ry + 1) * scale - 1],
                                fill=(0, 0, 0))
        img.save(f"/tmp/opencode/glyph_{idx:03X}.png")
        print(f"/tmp/opencode/glyph_{idx:03X}.png", img.size)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
