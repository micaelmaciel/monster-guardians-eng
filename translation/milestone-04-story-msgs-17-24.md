# Milestone 4 — Story messages 17–24 (the rescue, Kurimuto, the incident)

Delivered 2026-10-18. Source: bigfont story script at `0xCFF84`, messages
17–24 (13 text boxes, 25 runs). The rescue in the ruins, the introduction
of Kurimuto, the player retelling *the incident*, and the location card
for Vandam Castle with lord Winslow II.

Machine-readable output: `translation/story_en.json`. Translation input:
`translation/story_en_runs.json`. Reference sheet (glossary / characters /
style): `.opencode/skills/translation/reference.md`.

`▸` marks a manual line break (including the few added `7530`s);
`[RED]…[/RED]` marks the game's red-text highlight span (`753B`/`753C`);
`{name}` marks the player-name insert (`7540`). JP is the verified reading
from `WIKI.md`.

**Box behavior verified in-game this milestone** (frames in
`/tmp/opencode/story_run/`, log in `WIKI.md`): the `7538` control with
`0031 0030` renders the player-name at the start of msg 22 (frame 19400);
the `753F 0001` word insert renders ご子息 mid-line in msg 21 screen 2
(frame 19200); the msg 23 caption types in the box with the ▼ advance
marker (frame 19700); and in msg 24 the box **clears between the two
lines** (frames 19900 → 20000/20100), i.e. that message is 2 display
pages in JP, not one 2-line box. Details under *Layout*.

## Delivered text (per box)

### Message 17 — the ambush

```
JP 背後から魔獣達が／突然、追っ手達におそいかかった！
EN From behind, the beasts                          (23)
   suddenly attacked the guards!                    (29)
```

### Message 18 — the pursuers are routed

```
JP 追っ手達「うわあ！！」 [scr]
EN Pursuers: "Uwaaah!!"                             (20)

JP {name}は唖然として、／事の成り行きを見ていた。
EN {name} stood there, in shock,                    (29 w/ 6-char name)
   watching how it all unfolded.                    (29)
```

### Message 19 — an old man appears

```
JP 追っ手達はあっというまに倒された [scr]
EN The pursuers fell in no time!                    (29)

JP [W]すると、となりの部屋から／一人の老人が現れた。[/W]
EN Then, from the next room,                        (25)
   an old man appeared.                             (20)
```

### Message 20 — "noisy!"

```
JP [7537 0002]老人「やかましいのう！[7534 0006]わしゃ／寝起きは機嫌がわるいんじゃ！」
EN Old man: "Noisy!" I'm in a                       (26)
   bad mood when I wake up!"                        (25)
```

### Message 21 — Kurimuto (box pages)

```
JP その老人はクリムトと名乗った。 [7533] (caption)
EN The old man said his name:                       (26)

JP クリムト「いや、助けたのはベリンガムと言う名を聞いてな。／
   やつとは少々ワケありでの[W]・・・[/W] [scr]
EN Kurimuto: "No. I heard the                      ▸ (26)
   name Beringham. I stepped in.                    (29)
   That one and I have a past...                    (29)   ▸ (page)

JP うーん、そなたはヴァンダム城の／ウィンスローの[753F 0001]とみたが・・ [scr]
EN Hmm. I peg you for the son of                    (29)
   Winslow of Vandam Castle...                      (27)

JP 城でなにかあったかの？」
EN What happened at the castle?                     (28)
```

### Message 22 — the retelling setup

```
JP [7538 0031 0030]{name}は昨日に起こった／[RED]事件[/RED]をクリムトに語り始めた。
EN {name} began telling him of                      (27 w/ 6-char name)
   [RED]yesterday's incident[/RED].                 (21)
```

### Message 23 — location card

```
JP ～バルロア王国、ヴァンダム城～ [7531] (caption)
EN ~Barroa's Vandam Castle~                         (24)
```

### Message 24 — the castle lord

```
JP [7537 0032]城主は、貴族の一人ウィンスロー二世／
   事件は小雨の降る朝に、突然起こった。
EN The lord: noble Winslow II.                      (27)
   The incident struck one                          (23)   ▸ (page)
   drizzly morning.                                 (16)
```

## Layout — verified in-game, not just simulated

- **`753F` word insert** (msg 21 screen 2) — frame 19200 shows
  `ウィンスローのご子息とみたが`: the `753F 0001` control prints the
  canned word ご子息 ("son") *after* ウィンスローの. There is **no**
  glyph data for it in the message. Policy for now: at insertion time
  the control is **dropped** and the word is carried as plain EN text
  (here "son" lives right at the corresponding spot in the EN runs).
  Same default planned for `753E` (beast-name inserts, msgs 31+).
- **`7538` with 2 params** (msg 22) — frame 19400 shows the display
  starting with the player name (`レオは昨日に起こった`); both params
  are consumed and print nothing. EN keeps them as pass-through.
- **`7537` / `7534` controls** (msgs 20, 24) — invisible in-game
  (frames 18000, 19900+); EN keeps them as pass-through.
- **Caption with ▼** — msg 23's `～バルロア王国、ヴァンダム城～`
  types inside the normal box and waits for input (▼ visible, frame
  19700), then `7531` clears it. EN mirrors: one caption line, cleared.
- **msg 24 is 2 JP display pages** — frame 19900 shows line 1
  (`城主は、貴族の一人ウィンス…`); by frame 20000 the box has **cleared**
  and line 2 (`事件は…`) types from the *top* row. The 17-glyph first
  line overflowed the box (JP glyphs vary in width), so this message
  clears once even without a 3rd line. EN also produces 2 box pages,
  but pages at the sentence boundary differently — see flag 4.
- **Quote paging** (msg 21 screen 1) — the quote wraps to a second JP
  line and the trailing `やつとは…での・・・` arrives as a third line,
  which pages the box (frames 18600–18800). EN: quote = 2 lines, the
  tail lands on the fresh page ✓ same 2-page rhythm.
- **msg 21 added break** — the JP quote's 28-glyph run auto-wraps
  mid-word; the EN replaces it with a clean word-boundary break
  (added `7530`, reported by QA).

## Workflow followed

Same pipeline as milestones 1–3: verified JP readings (all 38 new glyph
codes read and committed to the charmap, `problems=0`, milestone M4
prep commit `9dadb5e`) → drafted against the reference sheet → naturality
pass → intent check → automated QA (`tools/story_en_export.py`) →
proofread. All runs drafted together, QA before commit.

### Automated QA results (all pass, `problems=0`)

- Run parity per message: 2 / 3 / 3 / 3 / 8 / 3 / 1 / 2 — 1:1 with
  source ✓
- Control codes identical to source; **2 added `7530`s** — msg 21 ×1
  (quote line split), msg 24 ×1 (incident sentence split) — both at
  word boundaries ✓
- Red span kept on the same concept: 事件 → "yesterday's incident"
  (see flag 5) ✓
- No CJK left in EN ✓
- Every segment ≤ 30 chars (no mid-word wraps); pages only where the
  source itself pages (msgs 21, 24) ✓
- Regression: msgs 0–16 output byte-identical to the committed M3
  output ✓

## Decisions for review (flag)

1. **msg 21 line 1 — interpretation chosen.** JP:
   `いや、助けたのはベリンガムと言う名を聞いてな。`
   Two readings exist: (a) "the one I saved/helped — I hear he goes by
   Beringham" (Kurimuto once saved Beringham), or (b) "[the reason] I
   saved you: I heard the name 'Beringham', y'see" (the name made him
   step in). Chosen: **(b)** — the te-form + な reason pattern (「～てな」
   as "because…", common in old-man speech) reads naturally here, and it
   pairs with the next clause 「やつとは少々ワケありでの」 ("that guy and
   I have a bit of history") to explain *why* he intervened. EN: `No. I
   heard the name Beringham. I stepped in.` If the intended story beat
   is (a), this is a one-run edit — please confirm when convenient.
2. **Kurimuto romanization** — クリムト is also the standard JP katakana
   for the painter *Klimt*; in a fantasy cast (Beringham, Winslow,
   Zargo…) the intended name may be "Klimt". Kept **Kurimuto** (direct
   transliteration) in EN for now — glad to switch globally if you
   prefer.
3. **msg 23 caption** — JP `バルロア王国、ヴァンダム城`. The direct
   `~Barroa Kingdom, Vandam Castle~` is 31 chars (one over the 30-char
   line cap), so EN uses `~Barroa's Vandam Castle~` (24). Alternatives:
   `~Barroa Kingdom: Vandam Castle~` (31, wraps) or two caption lines.
4. **msg 24 = 3 EN lines → 2 pages** — JP also shows 2 display pages
   here (verified), so the page count matches; the split point differs
   (JP pages at the sentence edge — lord / incident — EN pages mid
   incident sentence, keeping 小雨の降る朝 as "one drizzly morning").
   Alternative keeps JP's split with "The incident struck in rain."
   (loses the morning). Kept content whole.
5. **Red span width** — JP red = 事件 only; EN red = "yesterday's
   incident". With "began telling" kept, fitting just "incident" inside
   the span at this width forces dropping 語り始めた ("began"). Span
   still highlights the same reveal noun; flagging the compromise.
6. **Speaker sequence** — msg 20 card is "Old man:" (name unknown in
   story until msg 21); from the msg 21 self-introduction caption
   onward, cards read "Kurimuto:". Keeps the card convention while
   matching the JP's 老人 → クリムト shift.
7. **"peg you for"** (msg 21, とみた) — "took you for" is 2 chars
   longer and exactly hits the 30-char cap; "peg" keeps ≤29 and suits
   the old man's gruff register.

## Next milestone proposal

- **M5: messages 25–32** — the incident retelling (Beringham's
  invasion), Winslow's death, and Kurimuto's training arc. Requires:
  reading the new glyph codes used in 25+ (charmap currently verified
  through msg 24), and 2 glyphs of Beringham's surname
  (`ベリンガム・ロー□□`, msg 25) pending — first decode pass drafted.
- The naming + monster-select UI strings (8×8 font) remain a separate,
  later milestone.

Please review the flagged decisions at your convenience; the 2026-10-18
workflow decision stands (no per-milestone pause — M5 drafting may
proceed unless something here needs a change). Flag 1 is the one worth
a look if you have a minute — it's a story fact, not just wording.
