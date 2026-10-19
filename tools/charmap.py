#!/usr/bin/env python3
"""Build data/charmap.json (glyph index -> character) from the user's
transcription of the game font, and provide decoding helpers.

Glyph index == text code (16-bit). Font glyphs are 8x8, ROM base 0xBEDF0.
"""
import json
import os
import sys

# --- digit / latin ---
M = {}
for i, ch in enumerate("0123456789"):
    M[0x002 + i] = ch
for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    M[0x00C + i] = ch
for i, ch in enumerate("abcdefghijklmnopqrstuvwxyz"):
    M[0x026 + i] = ch

# --- hiragana 0x040-0x08F (80) ---
HIRA = (
    "ぁあぃいぅうぇえぉお"
    "かがきぎくぐけげこご"
    "さざしじすずせぜそぞ"
    "ただちぢっつづてでと"
    "どなにぬねのはばぱひ"
    "びぴふぶぷへべぺほぼ"
    "ぽまみむめもゃやゅゆ"
    "ょよらりるれろわをん"
)
assert len(HIRA) == 80, len(HIRA)
for i, ch in enumerate(HIRA):
    M[0x040 + i] = ch

# --- katakana 0x090-0x0DF (80) ---
KATA = (
    "ァアィイゥウェエォオ"
    "カガキギクグケゲコゴ"
    "サザシジスズセゼソゾ"
    "タダチヂッツヅテデト"
    "ドナニヌネノハバパヒ"
    "ビピフブプヘベペホボ"
    "ポマミムメモャヤュユ"
    "ョヨラリルレロワヲン"
)
assert len(KATA) == 80, len(KATA)
for i, ch in enumerate(KATA):
    M[0x090 + i] = ch

# --- symbols 0x0E0-0x0FF ---
SYM_E0 = "ヴ、。，．・：；？！ー／＼〜＋−±×÷＝≠＜＞¥$％#&＊@（）"
assert len(SYM_E0) == 32, len(SYM_E0)
for i, ch in enumerate(SYM_E0):
    M[0x0E0 + i] = ch

# --- symbols / UI 0x100+ (partial, from user description) ---
M[0x100] = "→"
M[0x101] = "←"
M[0x102] = "↑"
M[0x103] = "↓"
M[0x110] = "“"
M[0x111] = "”"
M[0x112] = "〈"
M[0x113] = "〉"
M[0x114] = "["
M[0x115] = "]"
M[0x116] = "゛"
M[0x117] = "＿"
M[0x118] = "{"
M[0x119] = "}"
M[0x11A] = "｜"
M[0x11B] = "「"
M[0x11C] = "」"
M[0x11D] = "゛"
M[0x11E] = "゜"
M[0x11F] = "～"
M[0x120] = "┌"
M[0x121] = "─"
M[0x122] = "┐"
M[0x123] = "│"
M[0x125] = "│"
M[0x126] = "└"
M[0x127] = "─"
M[0x128] = "┘"
M[0x132] = "№"
for i in range(10):
    M[0x133 + i] = "0123456789"[i]  # small digits (shown in upper-left)
M[0x13D] = "lv"
M[0x13E] = "→"  # filled right arrow
M[0x13F] = "↓"  # filled down arrow
M[0x1FF] = "\u23ce"  # enter arrow

# --- kanji 0x170-0x193 ---
KANJI = (
    "世界無私恒共巨大匹空"
    "天地上血戦応百年文化"
    "消去一人脱火山下助持"
    "以外間支配常"
)
assert len(KANJI) == 36, len(KANJI)
for i, ch in enumerate(KANJI):
    M[0x170 + i] = ch

# 0x001 is a blank/space filler
M[0x001] = " "


def load(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "data", "charmap.json")
    with open(path) as f:
        d = json.load(f)
    return {int(k, 16): v for k, v in d.items()}


def dump(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({f"0x{k:03X}": v for k, v in sorted(M.items())}, f,
                  ensure_ascii=False, indent=1)
    print("wrote", path, len(M), "entries")


def decode(codes, table=None):
    table = table or M
    out = []
    for c in codes:
        if c == 0x0000:
            break
        if c == 0xFFFF:
            continue
        if c in table:
            out.append(table[c])
        else:
            out.append(f"{{{c:03X}}}")
    return "".join(out)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "data", "charmap.json")
    dump(out)
