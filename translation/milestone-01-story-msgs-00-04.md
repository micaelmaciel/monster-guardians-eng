# Milestone 1 — Story messages 0–4 (opening narration)

Delivered 2026-10-17. Source: bigfont story script at `0xCFF84`, messages
0–4 (10 text boxes total). This is the first translation milestone: the
opening narration of the game, from the intro attract sequence.

**Revision 2** (2026-10-17, same day): box-completeness pass after user
review — see *Revision 2* below. Text shown here is the revised version.

Machine-readable output: `translation/story_en.json` (structured, ready
for the insertion tooling later). Translation input: `translation/story_en_runs.json`.
Reference sheet (glossary / characters / style): `.opencode/skills/translation/reference.md`.

## Delivered text (per box)

`▸` marks a manual line break; `[w]` etc. mark kept control codes
(invisible to players). JP is the verified reading from `WIKI.md`.

### Message 0 — the narrator's premise

```
JP 神のいない世界に、繁栄などは無い  [w60] [clear]
JP だから私が使わされた。 [w60]

EN In a world without gods,      ▸ (24)
   there is no prosperity.       ▸ (23)
   [clear]
EN That is why I was sent.          (23)
```

### Message 1 — the Age of Darkness

```
JP 暗黒の時代  [w60] [clear]
EN The Age of Darkness               (19)

JP グランデート大陸は常に ▸ 人類の危機と共に存在していた。 [w10] [scr]
EN The continent of Grandate     ▸ (25)
   always knew mankind's crises. ▸ (29)

JP 永遠の命を持つといわれた、 ▸ 巨大な２匹のハイドラゴンが [w10] [scr]
EN The two giant hydra dragons  ▸ (27)
   were said to live forever.      (26)

JP 大陸の権力を、掌握していた [w20]
EN They held dominion            ▸ (18)
   over the continent.              (19)
```

### Message 2 — Canon of the Heavens

```
JP 空を支配していた、天空の [white block] カノン [/white] [w50]
EN The one who ruled the sky, ▸ (26)
   Canon of the Heavens           (20)
```

### Message 3 — Ignis of the Earth

```
JP 地上を支配していた、大地の [white block] イグニス [/white] [w50]
EN The one who ruled the land, ▸ (27)
   Ignis of the Earth               (18)
```

### Message 4 — the war begins

```
JP ２匹は互いに対峙し、[w1] 大陸を征服しようと、[scr][w2]
EN The two faced each other.        (25)

JP 血塗られた戦争をくり広げていた。 [w20]
EN To conquer the continent,    ▸ (25)
   they waged a blood-soaked war.   (30)
```

## Workflow followed

Translation skill pipeline: research (no prior translation exists; GBA
launch title, Konami/Mobile21 2001) → reference sheet built → translated
against it → naturality pass → intent check against the verified JP →
automated QA (`tools/story_en_export.py`) → proofread.

### Automated QA results (all pass)

- Run/box parity with source: 2 / 6 / 2 / 2 / 3 text runs — 1:1 ✓
  (msg 4, run 2 is intentionally empty — see *Revision 2*)
- Control codes identical to source, **except 5 added `7530` line breaks**
  (one per message) where English would otherwise auto-wrap mid-word or
  strand a leading space.
- No CJK characters left in the English ✓
- Layout: every line ≤ 30 chars, every box ≤ 2 lines (longest box 54
  chars). Wrap simulated with the game's character-exact wrapping.

## Decisions for review (flag)

1. **Grandate** — romanization of グランデート. No official English
   exists (JP-only game). Alternatives: *Grandēto*, *Grandeato*. Chosen
   for readability; easy to change everywhere.
2. **hydra dragon** — ハイドラゴン. Kept as a descriptive creature term;
   alternative: *Hydragon* (one word, invented-name style).
3. **"always knew mankind's crises"** — 共に存在していた. *Shared* is
   the closest verb but is 1 char too long for the box safety limit;
   *knew* is neutral-literary and fits. Flagged in case you prefer
   changing the box geometry budget instead.
4. **Messages 2/3 have no sentence-end period** — mirroring the Japanese
   reveal cards (they end unpunctuated). Name placed last, as in JP.
5. **Box completeness (rev2)** — every box now ends on a complete
   sentence; no box ends mid-clause with the next box restarting on a
   bare pronoun. Done by re-allocating text between the JP runs inside a
   box (messages 1 and 4); no control code moved.
6. **Added line breaks** (list above) are the only structural liberty;
   defensible at insertion time and re-tunable when final glyph metrics
   are fixed.

## Revision 2 — user feedback (2026-10-17)

Review flagged box seams that read awkwardly: a box ending mid-sentence
and the next box restarting with a pronoun, plus the comma after "each
other". Changes made:

- **Msg 1, boxes 3/4**: was "Said to have eternal life, / the two giant
  hydra dragons" → "They held dominion…" (dangler). Now box 3 is a
  complete sentence — "The two giant hydra dragons / were said to live
  forever." — and box 4 reads as its own sentence ("They held dominion /
  over the continent."). The two JP runs exchanged English content
  (subject first); the source `7530` between them still makes the line
  break, so no break was added.
- **Msg 4**: "The two faced each other," → "The two faced each other."
  (period, as you suggested). The conquest clause now opens box 2's
  sentence instead of trailing box 1: "To conquer the continent, / they
  waged a blood-soaked war." That JP run is left empty, so no control
  code moved; box 2's added `7530` is the sentence's line break.
- **Style guide** (`reference.md`): added the box-completeness rule.
- QA re-run after revision: problems = 0, no wrap warnings, every line
  ≤ 30 chars, every box ≤ 2 lines.

## Next milestone proposal

- **M2: messages 5–9** — rest of the intro narration (the long war, the
  sorcerer, the Legendary Beast Tamer, the age of humans). Same size,
  pure narration, same voice.
- **M3: messages 10–16** — Famfantar volcano + ruins pursuit: first
  dialogue (the man, Pursuers 1/2/3), requires voice decisions.
- **M4 onward: messages 17+** — remaining story scenes (Kurimuto arc
  etc.), ~4-6 messages per milestone.
- Also pending before reinsertion: English bigfont glyphs (words/widths)
  and final wrap limits — a separate technical task.

Please review the text above; whatever you decide (names, tone, breaks)
gets recorded in the reference sheet and applied before M2.
