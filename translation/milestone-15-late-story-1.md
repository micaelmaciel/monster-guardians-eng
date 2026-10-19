# Milestone 15 — late-bank story retranslation, chunk 1 (L0–L5)

Date: 2026-10-19. Status: delivered, QA `problems=0`.
Supersedes the rejected M11 drafts for these messages (all 61 runs
rewritten from the JP corpus; none of the old draft text survived).

## Scope and sources

- JP runs: `tools/show_runs.py --bank late N` (decoded from
  `build/late_story_raw.json` with `data/bigfont_charmap.json`).
- EN runs: `translation/late_story_en_runs.json` (L0–L5 only; L6–L32
  still have no EN).
- Export/QA: `tools/story_en_export.py --bank late` →
  `translation/late_story_en.json`, result `6 messages; problems=0`.
- Run counts 1:1 with the JP: 17 / 8 / 10 / 8 / 4 / 14.

## Quality rules applied

- Prose-first: the composed text (runs joined across every insert and
  box seam) was read end-to-end; the exporter's line simulation was
  used as the run-join spacing check (it is what caught a missing space
  before the `he/she` insert and in L5's "so that you").
- ≤29 chars per working line; no mid-word auto-wrap anywhere (no WARN
  lines in the sim); screens that need it use 3 lines = 2 pages
  (L0 s2/s7, L3 s3, L5 s1/s4/s5); nothing exceeds 3 pages.
- No em dashes; `...` (three dots); straight quotes; no "this" before
  a person; box seams land on clause edges; singular "they" for the
  player.
- Added breaks (7530 via `\n` in a run) are used where English
  wrapping demands; totals per message: L0 ×5, L1 ×2, L2 ×3, L3 ×5,
  L4 ×1, L5 ×10 (counted by the exporter; all reported).

## Insert conventions (753F word table: kept + localized)

- Slot 2 (伝説の魔獣使い) = `the Legendary Beast Tamer` (25 wide;
  exporter reserves 24). It gets its own box line in L3/L4/L5 because
  25 + following text cannot fit ≤29.
- Slot 3 (彼/彼女) = `he`/`she` **lowercase** so both player-gender
  variants read correctly in any position. EN wording guarantees no
  sentence-initial use: L3 r2 supplies `Then ` before the first insert.
- L5's おぬし is a plain red span (not an insert); the necessary space
  is supplied by run text (`so that ` + [red]you[/red] + ` were born…`).
- L3 r7 has no 753F control and must not hardcode a gender: reworded to
  "machine could save a life." ("his/her" would be wrong for one of the
  two variants).

## Per-message notes (deviations and choices)

- **L0** — speaker card `######: "Haa haa!"` kept (msg 57 precedent).
  Collapse screen: 3 lines / 2 pages (JP 3 lines). "What Beringham /
  said was true!" (1 added break). Reveal: 2 added breaks →
  `I combined Canon and the / Beast Tamer, and so you / were born.`
  (3 lines / 2 pages vs 2 JP lines, recorded not compressed).
- **L1** — no added breaks; screens map 1:1 onto the JP 7532s.
- **L2** — 1 added break in r0 (`The first / beast-human I made,`);
  final screen reworded to `is a savage beast's."` to stay ≤29.
- **L3** — screen 1 = 4 lines / 2 pages (the insert gets its own line);
  screen 3 = 3 lines / 2 pages; screens 4/5 match JP line counts.
- **L4** — 1 added break; the slot-2 insert sits inside its red span
  (as in JP). EN distributes "combined" into r0, so r3 = `!"`.
  7537:0x20 passes through, position unchanged.
- **L5** — insert gets its own line both sides; narrator screens 8/9
  stay at JP line counts; [7540] name width 6 accounted for in r13.

## Verification

- Exporter: run counts 1:1, control sequence intact (7530/7532/7535-36/
  7537/753F/7540), `problems=0`.
- Sim output reviewed line by line (spacing across inserts, seam
  wording, page counts).
- Emulator check (mGBA): deferred to the insertion pass — this
  milestone is data-only, no ROM edits.

## Parked items found during this chunk

- Early-bank consistency: msg 9 EN has "his two beasts" for the
  Legendary Beast Tamer, whose gender is player-variant in JP (753F
  slot 3). Fix in the early-bank consistency sweep (together with the
  queued msg 32/46 fixes).
- Remaining late-bank inserts for later chunks: 753E beast names
  (L9 ×3, L10 ×1) need the localized beast-name table; 753F:0 = "I"
  (L22 ×1) is trivial; no other inserts in L6–L32.
