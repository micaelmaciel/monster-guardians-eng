# Milestone 20 — late-bank story retranslation completed (L27–L32)

Date: 2026-10-19. Status: delivered, QA `problems=0`.
Final chunk of the late-bank retranslation (M15–M20). **All 33 late
messages now have EN**, and both story banks export clean.

## Scope and sources

- JP runs: `tools/show_runs.py --bank late 27..32`.
- EN runs: `translation/late_story_en_runs.json` (L0–L32).
- Export/QA: `tools/story_en_export.py --bank late` → **33 messages,
  `problems=0`**. Early bank re-checked: `--bank story` → 63 messages,
  `problems=0`.

## Content covered

- L27: Kurimuto accepts the player's decision ("I see...").
- L28: telling himself the player survived, staring at the black Takt.
- L29: staff-roll card + `❋The End❋` (already English in JP; kept).
- L30–L32: the three ending-choice variants (leave without the beasts /
  return to complete them; L31 and L32 differ only by a JP comma, so
  their EN is identical).

## Quality notes

- All lines ≤29; screens 1–3 lines, max 2 pages.
- Consistency: "old Kurimuto" matches the approved early-bank phrasing
  (not "old man Kurimuto").
- Ending variants keep identical EN where the JP is identical (L31/L32)
  so the branch reads consistently.
- Added breaks: L27 2, L28 0, L29 0, L30 3, L31 4, L32 4.

## Late-bank completion summary (M15–M20)

- 33 messages, 174 runs, all 1:1 with the JP run counts.
- Word-table inserts localized (753F: slot0 "I", slot1 son/daughter
  per msg 21, slot2 "the Legendary Beast Tamer", slot3 lowercase
  "he"/"she" with wording that never puts it at sentence start).
- Beast-name inserts (753E 0x6/0x7/0x8) handled with the 12-wide
  reserve; spelling matches the approved early msgs 32/46.
- All 7530/7532/7534/7535/7536/7537/7538/7539/7540 controls kept in
  place; added line breaks only via `\n` in EN runs (counted per
  message in `_notes`).
- Story consistency carried across banks: Baron/Barroa, Winslow I/II,
  Canon, Ignis, Beringham, Zargo, Ramires, Kurimuto, "the Takt",
  "beast combining machine", "the Legendary Beasts", singular "they"
  for the player.

## Verification

- Exporter: run counts 1:1, control sequences intact, `problems=0` for
  both banks; sim lines reviewed for joins/page counts in every chunk.
- Emulator check: still deferred to the insertion pass (text is
  data-only at this stage; no ROM edits yet).

## Next

1. Early-bank deferred fixes: msg 32/46 insert-length corrections and
   msg 9's "his two beasts" pronoun (player-gender dependent slot).
2. Consolidated QA: merge all regions into one workbook; prose +
   run-join spacing; width overflow list; EN>JP length-patch list.
3. Insertion pass: English glyph strategy (bigfont relocation + ASCII),
   length patches, pointers; then mGBA verification and the BPS patch.
