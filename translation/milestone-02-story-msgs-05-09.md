# Milestone 2 — Story messages 5–9 (intro narration, part 2)

Delivered 2026-10-17. Source: bigfont story script at `0xCFF84`, messages
5–9 (10 text boxes). Second half of the intro attract narration: the
sorcerer's challenge, the long battle, the dragons' fate, and the birth
of the Legendary Beast Tamer legend.

**Revision 2** (2026-10-17, same day): msg 8 boxes 3/4 and msg 9 boxes
1/2 reworked after user review — see *Revision 2* below. Text shown here
is the revised version.

Machine-readable output: `translation/story_en.json`. Translation input:
`translation/story_en_runs.json`. Reference sheet (glossary / characters /
style): `.opencode/skills/translation/reference.md`.

`▸` marks a manual line break (including the few added `7530`s);
`[RED]…[/RED]` marks the game's red-text highlight span (`753B`/`753C`).
JP is the verified reading from `WIKI.md`.

## Delivered text (per box)

### Message 5 — the sorcerer appears

```
JP 長き戦いの末、 ▸ この大陸全ての生命と、 [scr]
EN At the end of a long war,        ▸ (25)
   when all life and prosperity       (28)

JP 繁栄が消え去ろうとしたとき [styled] ・・・ [/styled] [scr]
EN of this continent was about     ▸ (27)
   to vanish...                       (12)

JP 見たことも無い二匹の魔獣を ▸ 引き連れた、一人の [RED]魔術使い[/RED] が現れ、 [w] [scr]
EN leading two unseen beasts,       ▸ (26)
   a lone [RED]sorcerer[/RED] appeared, and       (29)

JP ２匹に戦いを挑んだ！ [w]
EN challenged the two to battle!      (29)
```

### Message 6 — the long battle

```
JP 長く壮絶な戦いが繰り広げられ [styled] ・・・ [/styled] [w]
EN The fierce battle raged on...       (29)
```

### Message 7 — the dragons' fate

```
JP 天空のカノンは敗れ、 ▸ 傷を負った大地のイグニスは、 [w] [scr]
EN Canon of the Heavens fell,       ▸ (26)
   Ignis of the Earth, wounded,       (28)

JP ファムファンタル火山の地下深く、 ▸ 姿を隠したのであった。 [w] [scr]
EN deep beneath Mount Famfantar,   ▸ (29)
   went into hiding.                  (17)
```

### Message 8 — the price of victory

```
JP その勝利は、二匹の魔獣の命と、 ▸ 引き換えに勝ち取った。 [w] [scr]
EN That victory was bought         ▸ (23)
   with the two beasts' lives.        (27)

JP そして魔獣使い自身もまた、 ▸ 力尽きようとしていた。 [w] [scr]
EN And the Beast Tamer himself     ▸ (27)
   was on the verge of collapse.      (29)

JP その時、この魔獣使いを救える技術を持つ者は [RED]私[/RED] 以外、 [w] [scr]
EN At that moment, other than      ▸ (26)
   [RED]me[/RED],                           (3)

JP この世界には [w] 居なかった。 [w]
EN there was no one in this world  ▸ (30)
   who could save him.                (19)
```

### Message 9 — the legend is born

```
JP その後この魔獣使いと、二匹の魔獣は [scr]
EN In time, this Beast Tamer and   ▸ (29)
   his two beasts became legend.      (29)

JP [RED]伝説の魔獣使い[/RED] ▸ として人々に伝えられた。 [w] [scr]
EN [RED]The Legendary Beast Tamer,[/RED]  (26)
   the name the people gave him.      (29)

JP そしてグランデート大陸は、 ▸ 人類が支配者となった。 [w]
EN And the continent of Grandate    ▸ (29)
   came under mankind's rule.         (26)
```

## Workflow followed

Same pipeline as milestone 1: verified JP readings → drafted against the
reference sheet (narrator voice: solemn, no contractions, sentence
continuations across boxes start lowercase per the rev-2 seam rule) →
naturality pass → intent check → automated QA (`tools/story_en_export.py`)
→ proofread.

### Automated QA results (all pass)

- Run/box parity with source: 9 / 2 / 4 / 9 / 5 text runs — 1:1 ✓
- Control codes identical to source; **4 added `7530` line breaks** —
  msg 5 ×1 (box 2), msg 8 ×2 (boxes 3 and 4), msg 9 ×1 (box 1) — every
  one verified against the engine's mid-word auto-wrap (details in
  `story_en_runs.json` `_notes`).
- Red-text spans (`753B`/`753C`) kept on the same emphasized concepts:
  魔術使い → "sorcerer", 私 → "me", 伝説の魔獣使い → "the Legendary
  Beast Tamer".
- No CJK characters left in the English ✓
- Layout: every line ≤ 30 chars, every box ≤ 2 lines (longest box 58
  chars — msg 9 box 1).

## Decisions for review (flag)

1. **"unseen"** for 見たことも無い (lit. "that have never been seen").
   Shortened to fit box 3 line 1; alternatives: *unknown*, *never-before-
   seen* (needs another re-split of box 3).
2. **"fell"** for 敗れ (msg 7). *Was defeated* does not fit the line;
   *fell* carries the same meaning in this register.
3. **"went into hiding."** for 姿を隠したのであった — deliberately
   gender-neutral (no pronouns for the dragons yet). Alternative:
   *hid himself away* if you want the dragons gendered from here on.
4. **"was on the verge of collapse."** for 力尽きようとしていた (msg 8).
   Alternatives: *was about to give out*, *had nearly run out of
   strength*.
5. **"That victory was bought / with the two beasts' lives."** for
   その勝利は、二匹の魔獣の命と、引き換えに勝ち取った — "bought with
   lives" idiom for the exchange construction.
6. **Message 9 title sentence** — rewritten in rev 2 (your call): the
   trio *became legend*, and the title explicitly names the tamer —
   *The Legendary Beast Tamer, / the name the people gave him.* The JP
   does literally group them ("this Beast Tamer and the two beasts …
   as the Legendary Beast Tamer"), but title-on-the-tamer is the
   natural reading. See *Revision 2*.
7. **"The fierce battle raged on..."** (msg 6) — "long" is folded into
   *raged on* to stay one line (the JP is 長く壮絶な = long and fierce).
8. **Red spans**: msg 8's 私 → "me" is the narrator's first-person
   self-reveal; kept RED, as in the JP.

## Revision 2 — user feedback (2026-10-17)

Two review points, both adopted:

- **Msg 8, boxes 3/4** — "this Beast Tamer" read childishly and the
  sentence was chopped mid-clause. Now: "At that moment, other than /
  me," → "there was no one in this world / who could save him." The
  noun appears once (box 2); the closing clause flows in one piece
  with your phrasing. Gender: "him" — the man refers to the tamer as
  ヤツ in msg 13, so masculine is safe.
- **Msg 9, boxes 1/2** — the JP literally hands down "this Beast Tamer
  and the two beasts … as the Legendary Beast Tamer" (として covers
  the group), which reads as if the beasts share the title. EN now
  gives the trio *became legend* and the title explicitly to him:
  "became legend. / *The Legendary Beast Tamer,* / the name the people
  gave him." Red span still on the title.
- Breaks: msg 8 keeps 2 added `7530`s (box-3 line break in run 4,
  box-4 line break in run 7); msg 9 keeps 1 (inside run 0).
- QA re-run after revision: problems = 0, no wrap warnings, every line
  ≤ 30 chars, every box ≤ 2 lines.

## Next milestone proposal

- **M3: messages 10–16** — Famfantar volcano and the ruins pursuit:
  the first *dialogue* (the man, the Takt, Pursuers 1/2/3, Lord
  Beringham) plus three boxes with the player-name insert (`7540`).
  This needs voice decisions (blunt menace vs. loud bumbling guards)
  and a rendering for the name variable — I will propose both.
- **M4 onward: messages 17+** — the Kurimuto arc and later story scenes.

Please review the text above; decisions feed the reference sheet before
M3 starts.
