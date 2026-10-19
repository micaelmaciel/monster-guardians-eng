# Milestone 14 — deferred QA on battle / map / shop (8×8)

The battle/map/shop regions were drafted before the last corpus
additions and before the ≤30-glyph line rule was settled. This pass
closes both gaps: **all 8×8 regions now pass
`tools/check_8x8_en.py` with 0 errors** (1,320 rows total = the full
corpus).

## Missing rows (28 added)

All are duplicates of already-translated strings at other addresses or
Latin/numeric templates:

* **battle (7):** `EXP` / `おかね` → `Money` / `Gold` (battle-result
  HUD duplicates), `をすてて` → `: discard and `, `をはずして` →
  `: remove and ` (composition fragments: `[NAME]` + `をすてて` +
  `[NAME]` + `をアイテムにくわえました` → `[NAME]: discard and
  [NAME]: added to your items.`, matching the existing rows at
  `0x0C616C`/`0x0C60C8`), `もどる` → `Back` ×2 (menu duplicates).
* **map (4):** duplicates of `じょうない` → `Castle Interior`,
  `こじょうなか` → `Old Castle Inside`, `こじょうない＜ごうせいしつ＞`
  → `Old Castle (Combine Room)`.
* **shop (17):** the digit templates `0 0 ` / `0 ` (kept verbatim;
  they receive runtime digits), twelve `は い`/`いいえ` → Yes/No pairs,
  the sell menu `う る` → `Sell` and `えらびなおす` → `Choose again`,
  and a third copy of the Mobile Data Center connect message.

## Line re-splits (≤30 glyphs, ≤3 pages)

43 rows had EN lines over 30 glyphs. Every one is re-split so each
`⏎` segment is ≤30 glyphs (mostly ≤29), and no message exceeds 3 box
pages (2 lines each = 6 display lines):

* battle: 19 rows (mission banners, carry/trade prompts), all now
  ≤2 lines.
* shop: 24 rows. The longest, `0x0A94AE` (save-password warning), uses
  exactly 6 lines: `Save the password / to the cartridge. / If you
  lose it, / someone else could / use it without / permission. OK?`.
  Composed runs re-checked: `0x0A9242` now ends `Plus a content fee of`
  so the appended `0x0A92D8` (` yen will be charged.⏎Is that OK?`)
  still forms one sentence; `0x0A9322` ends `This session's time was`
  for the appended time fragments (` min ` / ` sec.`).

Remaining checker output is warnings only: intentional EN == JP Latin
templates (`EXP`, `Gold`, `0 ` …) and EN > JP-length rows (length is
patched at insertion, never truncated).

## Next

* Consolidated prose + run-join spacing QA across all EN files; emit
  the EN>length patch list.
* Story retranslation (63 + 33 messages, R1 strings, 753E/753F).
