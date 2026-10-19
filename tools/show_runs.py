#!/usr/bin/env python3
"""Print per-run JA text for a message bank (translation working view).

Runs = maximal glyph sequences between control codes; they are the units
that `translation/*_en_runs.json` holds English text for, indexed from 0.

Usage: .venv/bin/python tools/show_runs.py [--bank story|late] msg [msg ...]
    --bank  story (default) | late
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BANKS = {
    "story": ("build/story_messages_raw.json", "msg"),
    "late": ("build/late_story_raw.json", "L"),
}

PARAMS = {0x7534: 1, 0x7535: 2, 0x7537: 1, 0x7538: 2,
          0x753B: 1, 0x753E: 1, 0x753F: 1, 0x7539: 2}


def main():
    args = sys.argv[1:]
    bank = "story"
    if args and args[0] == "--bank":
        bank = args[1]
        args = args[2:]
    raw_rel, tag = BANKS[bank]
    msgs = json.load(open(os.path.join(ROOT, raw_rel)))["messages"]
    cm = json.load(open(os.path.join(ROOT, "data",
                                     "bigfont_charmap.json")))["entries"]

    def glyph(v):
        e = cm.get(str(v))
        return (e or {}).get("char") or f"<{v:03X}>"

    for a in args:
        idx = int(a)
        m = msgs[idx]
        raw = m["raw"]
        print(f"==== {tag} {idx} "
              f"({m.get('off', '-')}, {len(raw)} tokens) ====")
        j = 0
        run = 0
        while j < len(raw):
            v = int(raw[j], 16)
            if v >= 0x1000:
                n = PARAMS.get(v, 0)
                ps = raw[j + 1:j + 1 + n]
                j += 1 + n
                if v == 0x7530:
                    print("[7530 break]")
                elif v == 0x7531:
                    print("[7531 clear]")
                elif v == 0x7532:
                    print("[7532 screen]")
                elif v == 0x7533:
                    print("[7533 caption]")
                elif v == 0x7540:
                    print("[7540 name]")
                elif v == 0x753E:
                    print(f"[753E beast {ps[0] if ps else '?'}]")
                elif v == 0x753F:
                    print(f"[753F word {ps[0] if ps else '?'}]")
                elif v == 0x7535:
                    print(f"[7535 style {','.join(ps)}]")
                elif v == 0x7536:
                    print("[7536 /style]")
                elif v == 0x753B:
                    print(f"[753B red {','.join(ps)}]")
                elif v == 0x753C:
                    print("[753C /red]")
                else:
                    print(f"[{v:04X}"
                          f"{':' + ','.join(ps) if ps else ''}]")
            else:
                text = []
                while j < len(raw) and int(raw[j], 16) < 0x1000:
                    text.append(glyph(int(raw[j], 16)))
                    j += 1
                print(f"r{run:<3d} {''.join(text)}")
                run += 1
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
