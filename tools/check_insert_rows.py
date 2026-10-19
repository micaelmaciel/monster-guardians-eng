#!/usr/bin/env python3
"""Check story EN rows against the REAL dynamic-insert widths.

The exporter sim (`tools/story_en_export.py`) reserves fixed placeholder
widths for the 753E beast names (12), the 753F word table (WORD_W) and
the 7540 player name (6). This tool substitutes the actual EN strings and
replays the same screen simulation for both player-gender variants:

  * 753E: `translation/story_insert_names.json` (9 slots x 2 variants)
  * 753F: I / son|daughter / the Legendary Beast Tamer / he|she
  * 7540: 6-char player name (unchanged reserve)

Reports, per bank:
  * lines over 30 chars (the engine hard-wraps and would split a word)
  * screens over 6 lines (page overflow)
  * insert boundary spacing defects (missing space before/after an insert)

Exit code 1 on any problem.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRAP = 30
MAX_SCREEN = 6
NAME_W = 6

# 753F word table EN (variant 0 = male player, 1 = female player).
WORD_EN = [
    ["I"],
    ["son", "daughter"],
    ["the Legendary Beast Tamer"],
    ["he", "she"],
]

BANKS = [
    ("build/story_messages_raw.json", "translation/story_en_runs.json", "story"),
    ("build/late_story_raw.json", "translation/late_story_en_runs.json", "late"),
]

spec = importlib.util.spec_from_file_location(
    "story_en_export", ROOT / "tools" / "story_en_export.py")
sx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sx)


def load_names():
    data = json.load(open(ROOT / "translation" / "story_insert_names.json"))
    names = {}
    for e in data["entries"]:
        names[(int(e["slot"]), int(e["variant"]))] = e["en"]
    return names


def word_name(slot, variant):
    vals = WORD_EN[slot]
    return vals[min(variant, len(vals) - 1)]


def compose(items, runs, variant, names, placeholders):
    """Build the EN text (or placeholder text) for one message."""
    out = []
    ri = 0
    for it in items:
        if it[0] == "text":
            out.append(runs[ri])
            ri += 1
            continue
        code = it[1]
        if code == 0x7530:
            out.append("\n")
        elif code in (0x7531, 0x7532, 0x7533):
            out.append("\x01")
        elif code == 0x7540:
            out.append("\x00N\x00" if placeholders else "#" * NAME_W)
        elif code == 0x753E:
            slot = int(it[2][0], 16)
            if (slot, variant) not in names:
                raise SystemExit(f"missing 753E name for slot {slot} variant {variant}")
            out.append(f"\x00B{slot}\x00" if placeholders else names[(slot, variant)])
        elif code == 0x753F:
            slot = int(it[2][0], 16)
            out.append(f"\x00W{slot}\x00" if placeholders else word_name(slot, variant))
    return "".join(out)


def check_bank(raw_path, runs_path, bank, names, problems):
    msgs = json.load(open(ROOT / raw_path))["messages"]
    runs = json.load(open(ROOT / runs_path))
    checked = 0
    max_line = 0
    max_screen = 0
    for mi, m in enumerate(msgs):
        key = str(mi)
        if key not in runs:
            continue
        items = sx.parse_message(m["raw"])
        n_runs = sum(1 for it in items if it[0] == "text")
        if n_runs != len(runs[key]):
            problems.append((bank, mi, "run count", len(runs[key]), n_runs))
            continue
        checked += 1
        # 1) boundary spacing (placeholder pass)
        s = compose(items, runs[key], 0, names, placeholders=True)
        for mm in re.finditer("\x00([NBW][0-9A-F]?)\x00", s):
            a, b = mm.start(), mm.end()
            prev = s[a - 1] if a else None
            nxt = s[b] if b < len(s) else None
            if prev not in (None, " ", "\n", "\x01", '"'):
                problems.append((bank, mi, "space-before", mm.group(1),
                                 repr(s[max(0, a - 14):b + 14])))
            if nxt not in (None, " ", "\n", "\x01", "'", ",", ".", "!", "?",
                           ":", '"', ")", ";"):
                problems.append((bank, mi, "space-after", mm.group(1),
                                 repr(s[max(0, a - 14):min(len(s), b + 14)])))
        # 2) real-width screen simulation, both gender variants
        for variant in (0, 1):
            text = compose(items, runs[key], variant, names, placeholders=False)
            screens = text.split("\x01")
            for si, scr in enumerate(screens):
                lines = []
                for part in scr.split("\n"):
                    if not part:
                        continue
                    while len(part) > WRAP:
                        lines.append(part[:WRAP])
                        part = part[WRAP:]
                    lines.append(part)
                max_screen = max(max_screen, len(lines))
                if len(lines) > MAX_SCREEN:
                    problems.append((bank, mi, "screen overflow", variant,
                                     f"s{si + 1}: {len(lines)} lines"))
                for line in lines:
                    max_line = max(max_line, len(line))
                    if len(line) > WRAP:
                        problems.append((bank, mi, "line over 30", variant,
                                         repr(line)))
    return checked, max_line, max_screen


def main():
    names = load_names()
    problems = []
    for raw_path, runs_path, bank in BANKS:
        checked, max_line, max_screen = check_bank(
            raw_path, runs_path, bank, names, problems)
        print(f"{bank}: {checked} messages checked, "
              f"max line {max_line}, max screen {max_screen} lines")
    if problems:
        print(f"\nPROBLEMS: {len(problems)}")
        for p in problems:
            print(" ", p)
        return 1
    print("\nno problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
