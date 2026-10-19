# Milestone 18 — late-bank story retranslation, chunk 4 (L17–L20)

Date: 2026-10-19. Status: delivered, QA `problems=0`.
Continues M15–M17 (L0–L16).

## Scope and sources

- JP runs: `tools/show_runs.py --bank late 17..20`.
- EN runs: `translation/late_story_en_runs.json` (L0–L20 now).
- Export/QA: `tools/story_en_export.py --bank late` → 21 messages,
  `problems=0`. Run counts 1:1: L17 3, L18 3, L19 8, L20 4.

## Content covered (the flashback sequence)

- L17: the player does not flee the burning room; gazes at Beringham.
- L18: the memory begins (Beringham's attack on the castle).
- L19: King Winslow hands over the Legendary Beast Tamer's Takt;
  Canon seizes the player's heart.
- L20: Canon's grudge; what Canon did to the player's younger brother,
  King Winslow.

## Quality notes

- All lines ≤29; screens 1–4 lines, max 2 pages.
- Story consistency: L20 uses "their younger brother, King Winslow",
  matching L5's approved phrasing for the Winslow II revelation
  (singular "they" for the player throughout the narration).
- L19 uses a name card ("Winslow" alone, then the quote) per the L9
  precedent; the flashback quote is a single line.
- Added breaks: L17 1, L18 0 (JP 7530 maps 1:1), L19 1, L20 2.
- L19 reorders the term into two lines ("held out the Legendary /
  Beast Tamer's Takt", 23+18) so the glossary term never exceeds 29.

## Terminology used

- 伝説の魔獣使いのタクト = "the Legendary Beast Tamer's Takt"
  (matches msg 28's approved EN).
- 差し出す = "held out"; 心が…に支配され = "heart was seized by".

## Verification

- Exporter: controls intact (7538 0x2C/0x2D pass through), run counts
  1:1, `problems=0`; sim lines reviewed (joins across [7540] name and
  red spans, page counts).
- Emulator check: deferred to the insertion pass (data-only stage).

## Next

- Chunk 5: L21+ — 13 messages left; L22 carries the 753F:0 = "I"
  insert inside a quote. L29 staff roll, L30–L32 ending variants are
  the tail.
