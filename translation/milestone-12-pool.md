# Milestone 12 — 8×8 pool region (EN)

Scope: the `pool` region of the 8×8 direct-code corpus, ROM
`0x0BD388..0x0BEDB2`: UI labels, status labels and descriptions,
species and attribute names, new-game setup prompts, the combine-shop
old man, party/training management, item/equipment messages, options,
save/load, event-replay titles and load-screen text.

**Result:** 270 corpus rows (251 unique strings) translated in
`translation/8x8_pool_en.tsv`; `tools/check_8x8_en.py` reports
0 errors. 19 rows are intentionally identical to the JP (Latin labels
`COMPLETE`, `CLEAR`, `ON`, `OFF`, `LV`, `EXP`, `Gold`, `G`, `PP`,
`USED`, plus the 8 unread species names).

## Length model (verified in code, 2026-10-19)

Every 8×8 string is drawn with an **explicit glyph count**, not a
terminator scan. Examples checked:

| string | code | length source |
|--------|------|---------------|
| `ん？、どうするんじゃ。` `0x0BD6C6` | `0x805A1D0 ldr r0,=ptr` / `0x805A1D4 movs r0,#0xB` | code immediate (11) |
| `セーブ` `0x0BE8C0` | `0x804860C ldr r2,=ptr` / `0x8048612 movs r4,#3` | code immediate (3) |
| `はい` `0x0BD3A2` | `+0x48` object field on the sprite struct = 2 | object field |
| status labels `0x0BD402..` | `{ptr,u16 len,u16 0}` table at `0x0BAA1C` | table field |
| split pieces (e.g. `けってい`) | base pointer + fixed byte offset, length immediate at each use | mixed |

Consequences for insertion:

* `term` rows (0x0000-terminated): EN length is free (box width only).
* `len` rows: the table's u16 must be updated to the EN length (or the
  EN must be padded to the JP length).
* `slice` rows: the code immediate (or struct field) must be patched to
  the EN length, or the EN padded to the JP length.
* `split` rows: the pieces sit at **fixed byte offsets** from the run
  base and have no individual pointers. Each piece must occupy exactly
  its JP code count, padded with spaces. 35 pool pieces; all fit after
  terseness tuning.
* `tools/check_8x8_en.py` lists every EN > JP-length row for the
  insertion stage (184 in this region). Those need a length patch, not
  truncation.

The 8×8 renderer does auto-wrap in at least the net/error screens
(JP source lines up to 53 glyphs), but we keep EN lines ≤ 30 glyphs
(240 px / 8 px) to be safe.

## Unread species names (parked)

Eight of the thirteen species-table entries are 4-glyph kanji names
using codes `0x1A0–0x1BF`. The 8×8 font store at `0xBEDF0` contains
only `0x1A0` glyphs (`0x000–0x19F`); `0xC21F0` (exactly
`0xBEDF0 + 0x1A0*32`) is a separate 16×16 4bpp kana font, and codes
≥ `0x1A0` therefore render garbage with the 8×8 renderer. They are
almost certainly cut content (the table is referenced only from two
data pointers). The eight rows are left as their `{1A0}...` placeholders
and excluded from terminology decisions until the user can check a
monster-book screen.

## New-game name records

`ベッフル`, `ファーブス`, `カノン` at `0x0BD5C2`, `0x0BD5D2`,
`0x0BD5B2` are **16-byte (8-glyph) zero-padded name records** copied
into RAM by the party-setup function at `0x551EC` (three monsters,
species IDs 2/4/5). `Canon` is locked. `Beffle` and `Farbus` are
provisional romanizations (flagged for user review). All fit the
8-glyph field.

## Terminology decisions forced by tight slots

| slot | JP | EN | why |
|------|----|----|-----|
| split 4 | ステージ | Area | `Stage` is 5 glyphs |
| split 4 | けってい | OK | 4-glyph limit |
| split 5 | キャンセル | Back | 5-glyph limit |
| split 4 | けっとう | Kin | bloodline field, 4-glyph limit |
| split 4 | きしょう | Mood | temperament, 4-glyph limit |
| split 3 | いどう / ひこう | Run / Fly | 3-glyph limit |
| split 5 | モンスター | Beast | 5-glyph menu slot; consistent with 魔獣 = beast |
| split 7 | ブリーフィング | Brief | 7-glyph limit |
| split 5 | スピーカー | Spkr. | 5-glyph limit |
| split 4 | ステレオ | 2ch | 4-glyph limit |
| split 9 | パスワードさくじょ | Clear Pwd | 9-glyph limit |
| split 4 | はいぶん | Give | point assignment, 4-glyph limit |
| split 17 | セーブはおこなえません、ごめんね。 | Can't save now. | 17-glyph limit |
| split 15 | サウンドのそうさはできません。 | Sound locked. | 15-glyph limit |
| split 17 | このそうさはできません、ごめんね。 | Sorry, no can do. | 17-glyph limit |
| split 17 | モンスターリストはじゅんびちゅう。 | List coming soon. | 17-glyph limit |

Outside split slots the natural terms are used (`Monster`, `Combine`,
`Stage` where free, `Assign`, `Order`, `Element`, etc.).

## Runtime-composed sentences

Two runs are assembled from fragments in code; the EN is written so
the concatenation reads correctly:

* Combine recipe: `These two make a ` + `legendary ` + `⏎"` + NAME +
  `".⏎It costs ` + COST + `. OK?` →
  `These two make a legendary ⏎"NAME".⏎It costs N. OK?`
* Combine success: `Ho ho ho! The combine⏎worked. ` + NAME +
  ` has been born.`
* Party list: `All ` + `parties are in training.`
* Recipe screen: `the above ` + A + ` and ` + `the above ` + B +
  ` get combined.`

## Voice notes

Combine-shop old man: plain English, gruff, no dialect spelling,
`sonny` used twice; `Ho ho ho!` kept. Party/training/system text uses
neutral instructional English. `Durability/Knowledge/Obedience/...`
follow the locked status-label list.

## Next

Remaining 8×8 regions: `net` (140), `report` (45), `mobile` (42),
`item` (42), `idesc` (42), `mdb1`–`mdb6`, `bbxxx` (2). Then a
consolidated QA pass (prose, run-join spacing, ≤30-glyph lines,
EN>length patch list).
