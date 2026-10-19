# Milestone 17 — late-bank story retranslation, chunk 3 (L11–L16)

Date: 2026-10-19. Status: delivered, QA `problems=0`.
Continues M15 (L0–L5) and M16 (L6–L10). Fresh translation from the JP
corpus.

## Scope and sources

- JP runs: `tools/show_runs.py --bank late 11..16`.
- EN runs: `translation/late_story_en_runs.json` (L0–L16 now).
- Export/QA: `tools/story_en_export.py --bank late` → 17 messages,
  `problems=0`. Run counts 1:1: L11 4, L12 5, L13 9, L14 4, L15 6,
  L16 1.

## Content covered

- L11: the courtyard ambush (Zargo / Ramires return).
- L12: Beringham's "pathetic lot" line (7537 0x27–0x29 pass through).
- L13: Beringham's last stand and decision to enter the machine
  (7537 0x2A/0x2B + 7534 wait; red span on 力 = `power` kept on that
  run only).
- L14: dying stutter, quote deliberately left open (JP `」` is in L15).
- L15: Ignis already inside the machine; Beringham drags himself in.
- L16: the machine erupts and engulfs the castle.

## Quality notes

- All working lines ≤29; screens run 1–3 lines, max 3 pages.
- Sim review caught two missing join spaces (both plain red spans, not
  inserts) and one exactly-30 line; all fixed before delivery:
  `to grant even greater power, I` → `, / I myself...` (29+12).
- Added breaks per message: L11 3, L12 2, L13 3, L14 0, L15 3, L16 2.
- Zargo / Ramires / Beringham spelled per glossary; player narration
  still singular "they" (`appeared before them`).
- L15 keeps the JP repetition of 合獣機 (both r4 and r5 say "beast
  combining machine").

## Terminology locked this chunk

- ザコ同士 = "small fry"; その先には = "Inside,"; 体を引きずりながら =
  "Dragging his body"; 火を噴き = "burst into flames"; またたくまに =
  "in an instant".

## Verification

- Exporter: controls intact, run counts 1:1, `problems=0`; sim lines
  reviewed (joins across red spans, page counts).
- Emulator check: deferred to the insertion pass (data-only stage).

## Next

- Chunk 4: L17+ (16 messages left; L22 carries the 753F:0 = "I"
  insert; L29 staff roll, L30–L32 ending variants are the tail).
