#!/usr/bin/env python3
"""Extract the late story message bank (0xD1F96..0xD30F4) from the ROM.

The story message text lives in one contiguous region:

    0xCFF84 .. 0xD1F96   63 messages ("story bank", see story_messages_raw.json)
    0xD1F96 .. 0xD30F4   33 messages ("late bank", this tool)
    0xD30F4 .. 0xD3144   small dictionary (40 words)

Messages are token streams terminated by 0x7FFF.  Every message start in the
late bank is referenced by a scene/event table, except 0xD2F08 which is a
chained continuation (the engine advances into it).

Earlier extractions used an ad-hoc script that silently dropped the message
at 0xD2CCA (it is referenced at 0xCB6FC), leaving 32 of 33 messages.
This tool re-extracts all segments between 0x7FFF terminators and verifies:

  * the segment count is exactly EXPECTED_COUNT
  * the region ends exactly at END
  * each referenced segment start is in the known scene-table pointer set

Usage: python tools/extract_late_bank.py [--check]
    --check   only verify, do not write build/late_story_raw.json
"""
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ROM = os.path.join(ROOT, "rom", "monster-guardians.gba")
OUT = os.path.join(ROOT, "build", "late_story_raw.json")
CHARMAP = os.path.join(ROOT, "data", "bigfont_charmap.json")

START = 0xD1F96
END = 0xD30F4
EXPECTED_COUNT = 33
CTL_END = 0x7FFF

# Scenic pointer-table references found by the 4-byte-aligned ROM scan
# (scene tables 0xC79A8..0xC7AC0 and 0xCA6F8..0xCBA30).  0xD2F08 has no
# reference: it is a continuation of the previous message.
EXPECTED_STARTS = [
    0xD1F96, 0xD20EA, 0xD21BE, 0xD22C8, 0xD23C2, 0xD2414, 0xD25CA,
    0xD2634, 0xD26B8, 0xD2730, 0xD27AE, 0xD2842, 0xD28C2, 0xD2940,
    0xD2A12, 0xD2A52, 0xD2ADA, 0xD2B14, 0xD2B64, 0xD2BA8, 0xD2C4C,
    0xD2CA2, 0xD2CCA, 0xD2D24, 0xD2D4C, 0xD2DA0, 0xD2DCC, 0xD2E5C,
    0xD2EC8, 0xD2F08, 0xD2F32, 0xD2FAC, 0xD3050,
]

# Control-code parameter counts (verified in-game / by extraction).
PARAMS = {
    0x7530: 0, 0x7531: 0, 0x7532: 0, 0x7533: 0, 0x7534: 1,
    0x7535: 2, 0x7536: 0, 0x7537: 1, 0x7538: 2, 0x7539: 2,
    0x753A: 0, 0x753B: 1, 0x753C: 0, 0x753E: 1, 0x753F: 1,
    0x7540: 0, 0x7541: 0, 0xFFFF: 0,
}


def load_rom():
    with open(ROM, "rb") as f:
        return f.read()


def segments(data, start, end):
    """Split [start, end) into (offset, tokens) message segments."""
    out = []
    o = start
    begin = None
    while o < end:
        v = struct.unpack_from("<H", data, o)[0]
        if v == CTL_END:
            if begin is not None:
                out.append((begin, [struct.unpack_from("<H", data, x)[0]
                                    for x in range(begin, o, 2)]))
                begin = None
        elif begin is None:
            begin = o
        o += 2
    return out


def decode(toks, bc):
    """Best-effort decode with insert markers (for readability only)."""
    parts = []
    i = 0
    while i < len(toks):
        t = toks[i]
        if t >= 0x1000:
            n = PARAMS.get(t, 0)
            ps = toks[i + 1:i + 1 + n]
            if t == 0x7540:
                parts.append("«P»")
            elif t == 0x753F:
                parts.append(f"«W{ps[0] if ps else '?'}»")
            elif t == 0x753E:
                parts.append(f"«BE{ps[0] if ps else '?'}»")
            else:
                arg = ",".join(str(p) for p in ps)
                parts.append(f"[{t:04X}{':' + arg if arg else ''}]")
            i += 1 + n
        else:
            e = bc.get(str(t))
            parts.append((e or {}).get("char") or f"<{t:03X}>")
            i += 1
    return "".join(parts)


def main():
    check_only = "--check" in sys.argv
    data = load_rom()
    bc = json.load(open(CHARMAP))["entries"]

    segs = segments(data, START, END)
    problems = 0
    if len(segs) != EXPECTED_COUNT:
        print(f"FAIL: found {len(segs)} segments, expected {EXPECTED_COUNT}")
        problems += 1
    starts = [s for s, _ in segs]
    for want in EXPECTED_STARTS:
        if want not in starts:
            print(f"FAIL: expected start 0x{want:06X} missing")
            problems += 1
    last_off, last_toks = segs[-1]
    end_pos = last_off + len(last_toks) * 2
    if end_pos + 2 != END:
        # last segment is followed by its terminator
        print(f"WARN: region end mismatch: last segment ends at 0x{end_pos:06X}"
              f" (terminator would be at 0x{end_pos:06X}), expected 0x{END:06X}")
        problems += 1
    # the terminator after the final segment must be the region end
    if struct.unpack_from("<H", data, END - 2)[0] != CTL_END:
        print("FAIL: byte pair before region end is not a 0x7FFF terminator")
        problems += 1

    print(f"segments: {len(segs)}")
    total = sum(len(t) for _, t in segs)
    print(f"total tokens: {total} (= {(END - START) // 2} incl. terminators;"
          f" delta {total + len(segs) - (END - START) // 2})")

    if problems:
        print("problems found; not writing")
        return 1
    if check_only:
        print("check OK")
        return 0

    msgs = []
    for idx, (off, toks) in enumerate(segs):
        msgs.append({
            "idx": idx,
            "off": f"0x{off:06X}",
            "len": len(toks),
            "raw": [f"0x{t:X}" for t in toks],
            "text": decode(toks, bc),
        })
    doc = {"count": len(msgs), "start": f"0x{START:06X}",
           "end": f"0x{END:06X}", "messages": msgs}
    with open(OUT, "w") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"wrote {OUT} ({len(msgs)} messages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
