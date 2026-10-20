#!/usr/bin/env python3
"""Build a QA-only ROM with every story message reduced to its terminator.

The intro is ~500,000 emulated frames of typewriter text.  For reaching
the field and status screens during QA we do not need the intro, so this
tool copies build/patch/patched.gba and overwrites the *start* of each
relocated story stream with 0x7FFF.  Stream pointers are untouched and
the rest of each allocation is left in place, so the engine simply sees
empty messages.

The shipped patched.gba and BPS are never modified.
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "build" / "patch" / "patched.gba"
DST = ROOT / "build" / "qa" / "patched_faststory.gba"
REPORT = ROOT / "build" / "patch" / "story_report.json"


def main():
    rom = bytearray(SRC.read_bytes())
    report = json.loads(REPORT.read_text())
    for m in report["mapping"]:
        off, size = m["new"], m["size"]
        if size < 2:
            raise SystemExit(f"message {m['msg']} too small: {size}")
        rom[off:off + 2] = b"\xff\x7f"
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_bytes(rom)
    print(f"wrote {DST} ({len(rom)} bytes, "
          f"{len(report['mapping'])} messages emptied)")


if __name__ == "__main__":
    main()
