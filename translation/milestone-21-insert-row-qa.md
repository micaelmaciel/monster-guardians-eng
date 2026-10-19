# Milestone 21 — insert-row QA and early-bank deferred fixes

Date: 2026-10-19. Status: delivered. Closes the deferred "insert rows are
sim-blind" item from milestone 07 and the msg 9 pronoun defect.

## Findings

- The `753E` beast-name table (`0xC7410` → strings at `0xCFA1E`) is
  **9 slots × 2 variants**, not two name forms of one beast. The variant
  is selected by the player's gender and is a **different species**
  (variant 0 = male set, variant 1 = female set), e.g. slot 0 =
  `GolmLite`/`GobFly`, slot 8 = `HeavyGau`/`MainVury` (full table in
  `translation/story_insert_names.json`). Slot 7 is a
  leveled recipe ingredient: JP `LV１５以上のミノドラゴン` /
  `LV１５以上のドラグリフォン` → EN `Lv15+ MinoDrag` / `Lv15+ DragGrif`
  (14 chars; appears alone on its line in L9, so fine).
- All other EN insert names are 3–8 chars, well inside the exporter's
  12-char reserve. The two `WARN: … auto-wraps mid-word` lines the
  exporter prints for msg 32/46 are placeholder artifacts only; with the
  real names every line fits.
- `7540` player name stays at a 6-char reserve; `753F` real widths are
  `I` (1), `son`/`daughter` (3/8), `the Legendary Beast Tamer` (25),
  `he`/`she` (2/3).

## Fixes applied

- **msg 9** (gender consistency): `his two beasts` → `the two beasts`
  (matches JP 二匹の魔獣), `calling him` → `calling them` (singular
  "they" for the player / the Tamer's reincarnation).
- **msg 46** (insert spacing, exposed by the real-name pass):
  - `the Legendary Beast` now ends its line, so `<BE8>` starts the next
    line and `'s medium form,` follows it (line was 37 chars with a real
    name and would have hard-wrapped mid-word);
  - `Next, combine` → trailing space before `<BE3>`;
  - `Then,` → trailing space before `<BE8>`;
  - `medium form` → trailing space before `<BE5>`.
- **L9** wording: `Combine the medium forms` → `Combine the medium form`
  (only `<BE6>` is a medium form; `<BE7>` is the Lv15+ ingredient).

## New files

- `translation/story_insert_names.json` — 18 `753E` entries with JP,
  EN, ROM target and pointer slot; source of truth for the insertion
  pass.
- `tools/check_insert_rows.py` — replays both story banks with the real
  insert strings, for both player-gender variants; reports lines >30,
  screens >6 lines, and insert-boundary spacing defects. Exit 1 on any
  problem.

## Verification

- `tools/check_insert_rows.py`: story 63 messages, max line 30, max
  screen 6 lines; late 33 messages, max line 29, max screen 5 lines —
  **no problems** (both gender variants).
- `tools/story_en_export.py --bank story` → 63 messages `problems=0`;
  `--bank late` → 33 messages `problems=0`.
- Emulator check: still deferred to the insertion pass (no ROM edits).

## Next

1. Consolidated prose / run-join QA workbook (all regions).
2. Insertion pass: English glyph strategy (bigfont relocation + ASCII),
   message pointers, length patches; then mGBA verification and BPS.
