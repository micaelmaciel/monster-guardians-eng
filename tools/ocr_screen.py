#!/usr/bin/env python3
"""OCR a GBA screenshot by template-matching 8x8 cells against the game font.

The game draws text as 8x8 glyphs from the font at ROM 0xBEDF0. Text boxes are
dark with light text, so "ink" is the brighter pixels. Each cell is matched
against all 512 glyphs by Hamming distance on a 64-bit ink mask.

Usage: ocr_screen.py <shot.ppm> [--thresh T] [--good S] [--min-len N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import charmap

FONT_BASE = 0xBEDF0
ROM = os.path.join(os.path.dirname(__file__), "..", "rom", "monster-guardians.gba")


def load_ppm(path):
    with open(path, "rb") as f:
        data = f.read()
    parts = data.split(None, 4)
    w, h = int(parts[1]), int(parts[2])
    px = parts[4]
    return w, h, px


def load_glyphs(text_only=True):
    with open(ROM, "rb") as f:
        rom = f.read()
    masks = {}
    for g in range(512):
        m = 0
        for y in range(8):
            b = rom[FONT_BASE + g * 32 + y * 4:FONT_BASE + g * 32 + y * 4 + 4]
            for byte in b:
                m = (m << 1) | (1 if (byte & 0xF) else 0)
                m = (m << 1) | (1 if (byte >> 4) else 0)
        pc = m.bit_count()
        # Skip blank and solid/box-fill tiles: real text glyphs have moderate
        # ink density.
        if text_only and not (5 <= pc <= 45):
            continue
        masks[g] = m
    return masks


def cell_mask(lum, w, x0, y0, thresh):
    m = 0
    for y in range(8):
        base = (y0 + y) * w
        for x in range(8):
            m = (m << 1) | (1 if lum[base + x0 + x] >= thresh else 0)
    return m


def best_glyph(m, masks, cache):
    if m in cache:
        return cache[m]
    best, bd = -1, 65
    for g, gm in masks.items():
        d = (m ^ gm).bit_count()
        if d < bd:
            bd, best = d, g
    cache[m] = (best, bd)
    return best, bd


def main():
    path = sys.argv[1]
    thresh = 48
    good = 56          # min score (out of 64) to accept a cell
    minlen = 2
    if "--thresh" in sys.argv:
        thresh = int(sys.argv[sys.argv.index("--thresh") + 1])
    if "--good" in sys.argv:
        good = int(sys.argv[sys.argv.index("--good") + 1])
    if "--min-len" in sys.argv:
        minlen = int(sys.argv[sys.argv.index("--min-len") + 1])

    w, h, px = load_ppm(path)
    lum = [0] * (w * h)
    for i in range(w * h):
        lum[i] = (px[i * 3] + px[i * 3 + 1] + px[i * 3 + 2]) // 3
    masks = load_glyphs()
    table = charmap.load()
    cache = {}

    results = []
    for y0 in range(0, h - 8):
        x = 0
        while x <= w - 8:
            m = cell_mask(lum, w, x, y0, thresh)
            if not (5 <= m.bit_count() <= 45):
                x += 1
                continue
            g, d = best_glyph(m, masks, cache)
            if 64 - d >= good:
                codes, scores = [], []
                x2 = x
                while x2 <= w - 8:
                    m2 = cell_mask(lum, w, x2, y0, thresh)
                    if not (5 <= m2.bit_count() <= 45):
                        break
                    g2, d2 = best_glyph(m2, masks, cache)
                    if 64 - d2 < good:
                        break
                    codes.append(g2)
                    scores.append(64 - d2)
                    x2 += 8
                distinct = len(set(codes))
                if len(codes) >= minlen and distinct >= 2:
                    results.append((len(codes), sum(scores) / len(scores), x, y0, codes))
                x = x2 + 8
            else:
                x += 1
    results.sort(key=lambda r: (-r[0], -r[1]))
    seen = set()
    for n, avg, x0, y0, codes in results[:8]:
        if any(abs(y0 - y) < 4 and abs(x0 - xx) < 40 for y, xx in seen):
            continue
        seen.add((y0, x0))
        print(f"y0={y0} x0={x0} n={n} avg={avg:.1f}")
        print("  codes:", " ".join(f"{c:03x}" for c in codes))
        print("  text :", charmap.decode(codes, table))


if __name__ == "__main__":
    main()
