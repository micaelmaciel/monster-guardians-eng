#!/usr/bin/env python3
"""Build a charmap for the large-glyph store (16x11, 22 bytes) at ROM 0xD3144.
Outputs data/bigfont_charmap.json with entries {index: {"char": "...", "notes": "..."}}
Initially empty for user transcription.
"""
import json, os

OUT = "data/bigfont_charmap.json"
data = {"base": 0xD3144, "stride": 22, "count": 685, "entries": {}}
# create empty structure by index
for i in range(685):
    data["entries"][str(i)] = {"char": "", "notes": ""}
os.makedirs("data", exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("wrote", OUT)
