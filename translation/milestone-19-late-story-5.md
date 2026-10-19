# Milestone 19 — late-bank story retranslation, chunk 5 (L21–L26)

Date: 2026-10-19. Status: delivered, QA `problems=0`.
Continues M15–M18 (L0–L20).

## Scope and sources

- JP runs: `tools/show_runs.py --bank late 21..26`.
- EN runs: `translation/late_story_en_runs.json` (L0–L26 now).
- Export/QA: `tools/story_en_export.py --bank late` → 27 messages,
  `problems=0`. Run counts 1:1: L21 2, L22 5, L23 2, L24 4, L25 2,
  L26 5.

## Content covered

- L21: the Takt falls from the player's hand.
- L22: the memory quote ("I killed him..."), flames engulf the player.
- L23–L25: the castle collapses.
- L26: Kurimuto searches the rubble, finds the burned Takt.

## Quality notes

- All lines ≤29; screens 1–3 lines, max 2 pages.
- L22 keeps the 753F:0 insert (`I`; WORD_W slot = 1) inside the 7535
  style span; the following space is supplied by r1. "killed him" =
  King Winslow (male, established L19–L20).
- L24 reuses the name-card pattern (`Kurimuto` + break + quote), with
  the [7540] between r2/r3 kept in place; the quote renders as
  `"[NAME]...?"`.
- Added breaks: L21 0, L22 2, L23 0, L24 2, L25 0, L26 2.

## Terminology used

- 合獣機 = "beast combining machine" (kept), タクト = "the Takt",
  残骸 = "ruins/rubble", 確信した = "was certain".

## Verification

- Exporter: controls intact (7535/7537/753F pass-through), run counts
  1:1, `problems=0`; sim lines reviewed.
- Emulator check: deferred to the insertion pass (data-only stage).

## Next

- Chunk 6: L27–L32 — 6 messages left: the last Kurimuto scenes, the
  staff roll (L29), and the three ending variants (L30–L32).
