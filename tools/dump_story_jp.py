#!/usr/bin/env python3
"""Dump the complete original Japanese story script.

Reads the two extracted banks:
  build/story_messages_raw.json   63 main-story messages (msg 0-62)
  build/late_story_raw.json       33 ending messages (L0-L32)

and decodes them with data/bigfont_charmap.json into one plain-text file,
translation/story_jp.txt.  No ROM addresses, no translation.

Output conventions:
  * a blank line marks a new text box / page (7531/7532/7533)
  * a single newline marks an in-game line break (7530)
  * invisible timing/animation controls (7534, 7537-753A, 7541) are dropped
  * {{PLAYER}}        = player name insert (7540)
  * {{BEAST:n}}       = beast-name insert (753E, slot n)
  * {{WORD:n}}        = word-table insert (753F, slot n)
  * red-text spans (753B/753C) are kept as plain text

Usage: .venv/bin/python tools/dump_story_jp.py [--check]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "translation", "story_jp.txt")
CHARMAP = os.path.join(ROOT, "data", "bigfont_charmap.json")
R1 = os.path.join(ROOT, "build", "r1_text_raw.json")

BANKS = [
    ("build/story_messages_raw.json", ""),
    ("build/late_story_raw.json", "L"),
]

# Control words >= 0x1000 and their parameter counts.
PARAMS = {
    0x7530: 0, 0x7531: 0, 0x7532: 0, 0x7533: 0, 0x7534: 1,
    0x7535: 2, 0x7536: 0, 0x7537: 1, 0x7538: 2, 0x7539: 2,
    0x753A: 0, 0x753B: 1, 0x753C: 0, 0x753E: 1, 0x753F: 1,
    0x7540: 0, 0x7541: 0, 0xFFFF: 0,
}
PAGE = {0x7531, 0x7532, 0x7533}


def decode_message(raw, glyphs):
    """Decode one token stream to display text."""
    out = []
    i = 0
    while i < len(raw):
        v = int(raw[i], 16)
        if v >= 0x1000:
            n = PARAMS.get(v, 0)
            ps = raw[i + 1:i + 1 + n]
            if v == 0x7530:
                out.append("\n")
            elif v in PAGE:
                out.append("\n\n")
            elif v == 0x7540:
                out.append("{{PLAYER}}")
            elif v == 0x753E:
                out.append(f"{{{{BEAST:{int(ps[0], 16)}}}}}")
            elif v == 0x753F:
                out.append(f"{{{{WORD:{int(ps[0], 16)}}}}}")
            # everything else is invisible timing/animation/styling
            i += 1 + n
        else:
            out.append(glyphs.get(v) or f"<{v:03X}>")
            i += 1
    text = "".join(out).strip()
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text


def insert_tables():
    """Group the JP insert strings from the R1 extraction by slot."""
    doc = json.load(open(R1, encoding="utf-8"))
    tables = {}
    for key in ("name_table", "word_table"):
        slots = {}
        for e in doc[key]["entries"]:
            slots.setdefault(int(e["slot"]), {})[int(e["variant"])] = e["text"]
        tables[key] = slots
    return tables


def main():
    check_only = "--check" in sys.argv
    cm = json.load(open(CHARMAP, encoding="utf-8"))["entries"]
    glyphs = {int(k): v["char"] for k, v in cm.items() if v["char"]}

    lines = []
    missing = 0
    total = 0
    for path, tag in BANKS:
        doc = json.load(open(os.path.join(ROOT, path), encoding="utf-8"))
        for m in doc["messages"]:
            total += 1
            text = decode_message(m["raw"], glyphs)
            if "<" in text and ">" in text:
                for token in text.split():
                    if token.startswith("<") and token.endswith(">"):
                        print(f"missing glyph {token} in {tag}{m['idx']}")
                        missing += 1
            lines.append(f"## {tag}{m['idx']:02d}\n\n{text}\n")

    if missing:
        print(f"{missing} missing glyphs; not writing")
        return 1
    if check_only:
        print(f"check OK: {total} messages")
        return 0

    tables = insert_tables()
    appendix = ["# Dynamic inserts\n",
                "The game fills these in at runtime. Values are the original",
                "Japanese strings (male player / female player).\n"]
    for key, title in (("name_table", "BEAST:n"),
                       ("word_table", "WORD:n")):
        appendix.append(f"{title}")
        for slot in sorted(tables[key]):
            vals = tables[key][slot]
            if 0 in vals and 1 in vals and vals[0] != vals[1]:
                val = f"{vals[0]} / {vals[1]}"
            else:
                val = vals.get(0, vals.get(1, ""))
            appendix.append(f"  {slot:>2}  {val}")
        appendix.append("")

    text = ("Monster Guardians - original Japanese story script\n"
            "===================================================\n\n"
            "96 messages in game order: msg 00-09 (opening narration), "
            "msg 10-62 (main story), L00-L32 (ending).\n"
            "L30-L32 are alternate versions of the same final scene.\n"
            "Message numbers are only for alignment; they are not ROM "
            "addresses.\n\n"
            + "\n".join(lines) + "\n" + "\n".join(appendix))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"wrote {OUT}: {total} messages, {len(text)} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
