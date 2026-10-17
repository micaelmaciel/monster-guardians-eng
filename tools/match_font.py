#!/usr/bin/env python3
"""Identify 8x16 font glyphs (2 consecutive 4bpp tiles, ink = nibble 15).

Matches against a reference CJK font rendered 16x16 -> pooled 8x8.
Tile side: 16 rows x 8 cols, ink=nibble15 -> pooled 16->8 rows -> 8x8.

Usage: match_font.py <rom> <fontfile> <start_hex> <glyph_count> [out_tsv]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

rom = open(sys.argv[1], "rb").read()
fontfile = sys.argv[2]
start = int(sys.argv[3], 16)
gcount = int(sys.argv[4])
out = sys.argv[5] if len(sys.argv) > 5 else None

def glyph_grid(off):
    """16 rows x 8 cols, value = nibble"""
    g = []
    for half in (0, 0x20):
        for r in range(8):
            row = rom[off + half + r*4: off + half + r*4 + 4]
            vals = []
            for b in row:
                vals.append(b & 0xF); vals.append(b >> 4)
            g.append(vals)
    return g

def tile_vec(off):
    """pool 16x8 -> 8x8 continuous 0..1, ink = nibble 15 (gray 1 ignored)"""
    g = glyph_grid(off)
    vec = []
    for y in range(8):
        for x in range(8):
            a = g[2*y][x]; b = g[2*y+1][x]
            vec.append(max((a == 15) + 0.5 * (a == 1), (b == 15) + 0.5 * (b == 1)))
    return vec

chars = []
chars += [chr(c) for c in range(0x3041, 0x3097)]
chars += [chr(c) for c in range(0x30A1, 0x30FB)]
chars += ["ー", "、", "。", "「", "」", "・", "！", "？", "（", "）", "…", "～"]
chars += list("0123456789")
chars += list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
chars += list("abcdefghijklmnopqrstuvwxyz")
chars += [chr(c) for c in range(0x4E00, 0x4E01)]  # placeholder, extended below via JIS list
# common kanji: JIS level 1 core set (frequent ~500)
KANJI = ("一二三四五六七八九十百千万円年月日時分秒週火水木金土人口目手足耳頭心体力走話読書学年生先山川田村林森海空雨雪風雲鳥魚馬犬虫花草原野室家屋門街道橋駅市町県都国世界東西南北中上下左右前后内外新古今明暗長短大小多少早遅強弱速明暗男女父母兄弟子供友達先生学生名前言思想見聞知覚考感情喜怒哀楽愛憎夢希望夢"
         "敵味方攻守撃防魔法剣槍盾鎧兜靴薬袋箱鑰金銀銅鉄石鉱木材布絹皮毛肉飯料理味塩糖油醋茶酒杯皿碗箸厨洗掃壊建設造作業使役召喚契約結界封印解除効果能力技能経験熟練修練鍛錬勝利敗北戦闘戦場軍隊団体組合同盟敵対友好善悪正邪神霊魔竜龍獅虎豹狼狐猫鷹翼爪牙角尾鬣鱗甲"
         "赤橙黄緑青藍紫黒白灰茶金色銀色銅色鉄色肌髪瞳頬唇歯顔顎鼻眉髭鬢")
chars += list(dict.fromkeys(KANJI))

CACHE = {}
def ref_vec(ch):
    if ch in CACHE:
        return CACHE[ch]
    img = Image.new("L", (16, 16), 0)
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(fontfile, 13)
    d.text((1, 1), ch, font=f, fill=255)
    vec = []
    for y in range(8):
        for x in range(8):
            a = img.getpixel((2*x, 2*y)); b = img.getpixel((2*x+1, 2*y))
            c = img.getpixel((2*x, 2*y+1)); e = img.getpixel((2*x+1, 2*y+1))
            vec.append((a + b + c + e) / (4 * 255))
    CACHE[ch] = vec
    return vec

def soft_iou(a, b):
    inter = union = 0.0
    for x, y in zip(a, b):
        inter += min(x, y); union += max(x, y)
    return inter / union if union else 0.0

refs = [(ch, ref_vec(ch)) for ch in chars]
print(f"{len(refs)} reference glyphs")

res = []
for t in range(gcount):
    off = start + t*0x40
    tv = tile_vec(off)
    if sum(tv) < 0.5:
        res.append((off, []))
        print(f"0x{off:06X} [{t:4}]: (blank)")
        continue
    scores = sorted(((soft_iou(tv, g), ch) for ch, g in refs), reverse=True)[:3]
    res.append((off, scores))
    print(f"0x{off:06X} [{t:4}]: " + " ".join(f"{c}({s:.2f})" for s, c in scores))

if out:
    with open(out, "w") as f:
        for off, scores in res:
            f.write(f"0x{off:06X}\t" + "\t".join(f"{c}:{s:.3f}" for s, c in scores) + "\n")
    print("wrote", out)
