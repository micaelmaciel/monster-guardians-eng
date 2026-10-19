# Milestone 16 — late-bank story retranslation, chunk 2 (L6–L10)

Date: 2026-10-19. Status: delivered, QA `problems=0`.
Continues M15 (L0–L5). Fresh translation from the JP corpus; no
placeholder text.

## Scope and sources

- JP runs: `tools/show_runs.py --bank late 6..10`.
- EN runs: `translation/late_story_en_runs.json` (L0–L10 now).
- Export/QA: `tools/story_en_export.py --bank late` → 11 messages,
  `problems=0`. Run counts 1:1: L6 4, L7 4, L8 5, L9 6, L10 5.

## Quality notes

- All working lines ≤29; every screen ≤2 box pages except L10 s1
  (5 lines = 3 pages, within the allowed cap; JP has 4 lines = 2 —
  recorded, not compressed).
- Box-seam and insert joins re-read as composed prose; no em dashes,
  `...` only, straight quotes.
- 7537 single-param controls (L6 0x21, L8 0x22) and 7539 pairs (L9)
  pass through unchanged.

## Insert handling (753E beast names)

- L9 has inserts 0x8, 0x6, 0x7 and L10 0x8, each red-wrapped in JP and
  kept so in EN. Conventions reused from the approved early msgs 32/46
  ("the Legendary Beast / [NAME] / 's medium form" pattern):
  - title "the Legendary Beast" on its own line, insert line starts
    with the name; following run supplies the space (" is complete.").
  - `Combine the medium forms / [X] and / [Y]!` mirrors msg 46's
    "Next, combine / [X] and / [Y]." cadence; verb carried early,
    final run closes with punctuation (msg 46 precedent).
- Beast-name reserve 12 respected; no segment exceeds 30 even with the
  reserve (max 28).
- L9's JP lacks a closing 」; EN closes the quote at r5 for
  readability (noted as a deliberate small fix).
- L10 s1 needs both added breaks: the JP 7530 before the insert forces
  a break; "Kurimuto: "Then, the Legendary Beast " (35) cannot fit one
  line, so 20/16/26/24/18 = 5 lines / 3 pages.

## Terminology

- 伝説の魔獣 plural = "Legendary Beasts" (matches msgs 31, 47).
- 中型体 = "medium form"; 合獣機 = "beast combining machine";
  因果関係 = "bound by fate"; 野望を阻止 = "foil his plan".

## Verification

- Exporter: controls intact, run counts 1:1, `problems=0`; sim lines
  reviewed (spacing across every insert, page counts).
- Emulator check: deferred to the insertion pass (data-only stage).

## Next

- Chunk 3: L11+ (the ending sequence continues); no further 753E/753F
  inserts until L22 (753F:0 = "I").
