#!/usr/bin/env python3
"""Generate the EN 8x8 glyph bitmaps used by the story bigfont.

Source: the system VGA 8x8 PSF console font (crisp, public-domain style
bitmaps). The result is committed as `data/en_glyphs_8x8.json` so the
build never depends on the system font being installed.

Usage:
  .venv/bin/python tools/gen_en_glyphs.py [psf_path]
"""
import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PSF = "/usr/share/consolefonts/Arabic-VGA8.psf.gz"
OUT = ROOT / "data" / "en_glyphs_8x8.json"

FIRST, LAST = 0x20, 0x7E


def read_psf(path):
    raw = gzip.open(path, "rb").read()
    if raw[:2] != b"\x36\x04":
        raise SystemExit(f"{path}: not a PSF1 font")
    mode, size = raw[2], raw[3]
    data = raw[4:]
    count = len(data) // size
    return [data[i * size:(i + 1) * size] for i in range(count)], size


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PSF
    glyphs, size = read_psf(path)
    if size != 8:
        raise SystemExit(f"{path}: glyph size {size}, expected 8")
    out = {}
    for code in range(FIRST, LAST + 1):
        g = glyphs[code]
        out[chr(code)] = ["".join("1" if (row >> (7 - x)) & 1 else "0"
                                  for x in range(8)) for row in g]
    payload = {
        "_notes": f"8x8 bitmap glyphs for ASCII 0x20-0x7E, generated from "
                  f"a VGA 8x8 PSF console font by tools/gen_en_glyphs.py. "
                  f"Rows are MSB-left. Embedded into the story bigfont "
                  f"(16x11 1bpp cells) by tools/insert_story.py.",
        "source": path,
        "glyphs": out,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(f"wrote {OUT}: {len(out)} glyphs")


if __name__ == "__main__":
    sys.exit(main())
