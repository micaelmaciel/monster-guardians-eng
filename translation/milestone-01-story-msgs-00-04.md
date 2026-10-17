# Milestone 1 — Story messages 0–4 (opening narration)

Delivered 2026-10-17. Source: bigfont story script at `0xCFF84`, messages
0–4 (10 text boxes total). This is the first translation milestone: the
opening narration of the game, from the intro attract sequence.

**Revision 2** (2026-10-17, same day): box-seam fix after user review —
see *Revision 2* below. Text shown here is the revised version.

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
EN Said to have eternal life,   ▸ (26)
   the two giant hydra dragons      (27)

JP 大陸の権力を、掌握していた [w20]
EN held dominion                ▸ (13)
   over the continent.              (19)
   (boxes 3–4 are one sentence: box 4 continues it lowercase)
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
EN The two faced each other.    ▸ (25)
   To conquer the continent,   ▸ (25)

JP 血塗られた戦争をくり広げていた。 [w20]
EN they waged a blood-soaked war.  (30)
   (the sentence runs across boxes 1–2: box 2 continues it lowercase)
```

## Workflow followed

Translation skill pipeline: research (no prior translation exists; GBA
launch title, Konami/Mobile21 2001) → reference sheet built → translated
against it → naturality pass → intent check against the verified JP →
automated QA (`tools/story_en_export.py`) → proofread.

### Automated QA results (all pass)

- Run/box parity with source: 2 / 6 / 2 / 2 / 3 text runs — 1:1 ✓
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
5. **Box seams (rev2)** — a long JP sentence may span boxes; the seam
   must read naturally. Continuation boxes start lowercase; no box
   restarts with a pronoun for a subject named just before the seam
   ("…the two giant hydra dragons" / "They held dominion…" ✗). See
   *Revision 2*.
6. **Added line breaks** (list above) are the only structural liberty;
   defensible at insertion time and re-tunable when final glyph metrics
   are fixed.

## Revision 2 — user feedback (2026-10-17)

Review flagged box seams that read awkwardly: ending a box on a noun
phrase and restarting the next box with a pronoun for that noun
("…the two giant hydra dragons" / "They held dominion…" reads as "the
two hydra dragons, they were…"). Long sentences spanning boxes are fine;
the seam must just flow. Changes made:

- **Msg 1, boxes 3/4**: kept as one sentence in JP order — "Said to have
  eternal life, / the two giant hydra dragons" → "held dominion / over
  the continent." Box 4 continues the sentence lowercase; the subject is
  not restated. Breaks as in rev 1 (source `7530` splits box 3, one
  added `7530` splits box 4).
- **Msg 4**: "The two faced each other." takes the period (as you
  suggested). The conquest clause stays in box 1 ("To conquer the
  continent,") and box 2 continues the sentence lowercase: "they waged a
  blood-soaked war." One added `7530` (box-1 line break), as before.
- **Style guide** (`reference.md`): box-seam rule recorded — continuation
  boxes start lowercase; no pronoun restarts after a just-named subject.
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
