# Milestone 6 — Story messages 33–40 (the tremor, Zargo, the altar room)

Delivered 2026-10-18. Source: bigfont story script at `0xCFF84`, messages
33–40 (8 text boxes, 39 runs). Kurimuto leaves to research the next
beasts, the castle starts to quake, the player heads for the altar room,
Beringham appears with his beast Zargo, and Kurimuto saves the player.

Machine-readable output: `translation/story_en.json`. Translation input:
`translation/story_en_runs.json`. Reference sheet (glossary / characters /
style): `.opencode/skills/translation/reference.md`.

`▸` marks a manual line break (including added `7530`s);
`[RED]…[/RED]` marks red-text highlight spans (`753B`/`753C`);
`{name}` marks the player-name insert (`7540`). JP is the verified reading
from `WIKI.md`.

**Glyph pass this milestone**: messages 33–40 transcribed and
zip-verified against their token streams — **22 new glyphs** bound
(方処旅知壇震ゆ近づ気暴振ざザ狙裏付遅面激 and the `7534`/`7537`/
`7538`/`7539` params around them). Bigfont charmap now **350/685**.
Notable: `0x7F` read as **ザ** (not サ) and confirmed against the 8×8
text: the beast's name appears in game scripts as ザーゴ
(`あらわれたザーゴを、たおせ！！`), matching `[RED]ザーゴ[/RED]` here.

No new in-game captures were needed: the M5 OAM display model (17-glyph
rows, 2 rows/page) was reused for page accounting. All segments are ≤30
chars on static rows; rows that combine a text run with a `7540` name
insert are accounted at 29 chars with the tool's 6-char name simulation.

## Delivered text (per message)

### Message 33 — Kurimuto departs

```
JP クリムト「わしは再びその後の魔獣の作り方を調べる！」▸クリムト「後はまかせたぞ！」▸
EN Kurimuto: "I'll research how                        (28)
   the next beasts are made!"                           (26)
   Kurimuto: "I leave the rest                          (27)
   to you!"                                            (8)
   [4 rows -> 2 pages; JP 3 rows -> 2 pages]
```

### Message 34 — he walks away

```
JP そう言い残してクリムトは▸何処かへ旅立って行った。 [scr]
EN And with that, Kurimuto                              (23)
   set off for parts unknown.                           (26)

JP その後ろ姿を見て▸{name}は思った。 [scr]
EN Watching him walk away,                              (23)
   {name} thought.                                      (15 w/ 6-char name)
```

### Message 35 — the aftermath

```
JP [7538 000E 000F]クリムト老人は、こうなる事を知っていたのではないだろうかと・・・▸
EN Perhaps old Kurimuto had                             (24)
   known this would happen...                           (26)
   [2 rows -> 1 page; JP 32 glyphs -> 2 rows -> 1 page]
```

### Message 36 — the tremor

```
JP ゴゴゴゴゴ！ [scr]
EN RUMBLE! RUMBLE! RUMBLE!                              (23)

JP {name}が祭壇のある部屋に入った時、▸大きく城がゆれはじめた。 [scr]
EN {name} entered the altar room                        (29 w/ 6-char name)
   the castle began to shake.                           (26)

JP {name}「地震？」          (7540 before the quote)
EN {name}: "An earthquake?"                             (24 w/ 6-char name)
```

### Message 37 — the giant

```
JP 地震に気をとられていた{name}の目前に、 [scr]
EN Distracted by the                                     (17)
   quake, {name} looked up:                             (24 w/ 6-char name)

JP 見たことも無い大男が立っていた。 [scr]
EN A giant of a man unlike any                          (27)
   ever seen stood there.                               (22)

JP 彼は{name}をにらみつけながら近づいてきた。
EN He glared at                                         (12)
   {name} and drew closer.                              (23 w/ 6-char name)
```

### Message 38 — Beringham explains

```
JP ベリンガム「わかるかね！この地震はイグニスが[RED]君[/RED]に気づきはじめて、
   地下で暴れているのだよ！」 [scr]
EN Beringham: "Ignis senses [RED]you[/RED],                 (29)
   and he's raging underground!"                        (29)
   [2 rows -> 1 page; JP S1 = 3 rows -> 2 pages]

JP 声のする方向には▸ベリンガムの姿があった。
EN Where the voice came from,                           (26)
   there stood Beringham.                               (22)
```

### Message 39 — Zargo attacks

```
JP {name}は[7537 0011]ベリンガムに向けて、 [scr]
EN {name} faced Beringham, and                          (27 w/ 6-char name)

JP タクトを振りかざそうとしたその時 [scr]
EN just as the Takt swung up,                           (26)

JP クリムト「気をつけろ！ヤツの作った魔獣[RED]ザーゴ[/RED]に狙われておるぞ！」 [scr]
EN Kurimuto: "Look out! A beast                         (28)
   [RED]Zargo[/RED] he built is after you!"             (29)
   [2 rows -> 1 page; JP 2 rows -> 1 page]

JP [7537 0010]いつのまにか▸背後にクリムトの姿があった。 [scr]
EN Before they knew it,                                 (20)
   Kurimuto stood at their back.                        (29)

JP クリムト▸「よくここまで来れたのう。」
EN Kurimuto:                                            (9)
   "You made it this far, hm?"                          (27)
```

### Message 40 — Beringham mocks

```
JP ベリンガム「[W]フフフ・・・[/W]やはり[7534 0003]クリムトが裏に付いていたか！
   だがすでに遅いな！」 [scr]
EN Beringham: "Heh heh heh...                           (26)
   As expected, Kurimuto has                            (25)
   sided with you!                                      (15)
   But it's already too late!"                          (27)
   [4 rows -> 2 pages; JP 3 rows -> 2 pages]

JP その時、再び地面が▸激しくゆれ始めた！
EN Just then, the ground again                          (27)
   began to shake violently!                            (25)
```

## Flags for review

1. **msg 33 “その後”** — その後の魔獣の作り方を調べる rendered as
   "research how the next beasts are made" (interpreting その後 as the
   later-stage beasts, cf. msg 32 最初は and the later 中型体; msg 46
   will confirm). 再び ("once more") folded away for space.
2. **msg 37 “の目前に”** — the JP puts the name before 目前に
   ("before {name}'s eyes"); run order forces a subject-first EN, so it
   is rendered "…{name} looked up:" with the next screen supplying the
   sight. Nothing lost but the literal "before their eyes".
3. **msg 38 word order** — 気づきはじめて ("begun to notice") is
   rendered "senses" *before* the red span because English needs
   verb-object order ([you] must stay inside the span for the tooling).
   Also わかるかね ("you see?") was dropped to fit the row — the milder
   "Ignis senses you, and he's raging underground!" still reads as a
   boast. This screen is 1 EN page vs JP's 2.
4. **msg 39 Zargo romanization** — ザーゴ → "Zargo" (provisional;
   long-vowel ザー could also give "Zaago/Zago"). The same beast name is
   in the 8×8 text (`ザーゴをたおせ！`), so the monster-names milestone
   must use the same spelling.
5. **name-width rows** — msgs 34/36/37/39 combine text with the `7540`
   name insert; rows are sized for the tool's 6-char name simulation
   (≤29 with the sim). A much longer player name will push those rows
   over 30 and auto-wrap mid-word; nothing to fix in the script, noted
   for the ROM-writer milestone (name entry length can also be capped
   there).
6. **msg 36 altar room** — " entered the altar room" has no trailing
   comma (comma would make the row exactly 30 with the 6-char sim); the
   clause break carries the "when" of 入った時.

## Next milestone proposal

- **M7: messages 41–48** — the altar-room confrontation continues
  (msg 46 carries the second recipe with `7539` pairs and 中型体).
  The current captures end at frame 24000 (~msg 32); later milestones
  can proceed from renders + the verified display model, with fresh
  captures needed only when display behavior of a new control is in
  question.
- Item/monster name table translation and the 8×8 naming UI remain on
  the parallel track; story text keeps beast names dynamic.
