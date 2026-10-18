# Milestone 7 — Story messages 41–48 (Ramires, the dragon's warning, the climb)

Delivered 2026-10-18. Source: bigfont story script at `0xCFF84`, messages
41–48 (8 text boxes, 52 runs). Beringham leaves for Mount Famfantar,
Zargo collapses, Beringham's other beast Ramires appears and tells the
player to go to the volcano, Kurimuto gives the second recipe, and the
climb begins amid endless quakes.

Machine-readable output: `translation/story_en.json`. Translation input:
`translation/story_en_runs.json`. Reference sheet (glossary / characters /
style): `.opencode/skills/translation/reference.md`.

`▸` marks a manual line break (including added `7530`s);
`[scr]` marks a screen break (`7532`); `[RED]…[/RED]` marks red-text
highlight spans (`753B`/`753C`); `[W]…[/W]` a style span (`7535`/`7536`);
`{name}` marks the player-name insert (`7540`); `[BE nn]` a beast-name
insert (`753E`). JP is the verified reading from `WIKI.md`.

**Glyph pass this milestone**: messages 41–48 transcribed and
zip-verified against their token streams — **30 new glyphs** bound
(活任ゾ古友会 / ウッ / 唸ヒ / ミレ / 告抱込飛 / 運 / 型完次 / 道至難極 /
登数切ほ揺底). Bigfont charmap now **380/685**. Notable: the second
beast's name **ラミレス** is now fully read (msg 43) and matches the 8×8
beast-name list — romanized **Ramires** (provisional, same flag class as
Zargo).

No new in-game captures were needed (M5 OAM display model reused). All
segments are ≤30 chars on static rows; rows that combine a text run with
an insert are accounted with the tool's 6-char `{name}` simulation.

## Delivered text (per message)

### Message 41 — Beringham's parting words

```
JP ベリンガム「{name}の存在に気が付いたイグニスが、 [scr] 再び復活しようとしておる！
   [scr] ザーゴ！[7534 0005]あとは任せるゾ！ [scr] わしはファムファンタル火山へ行き、
   [scr] [RED]{name}君[/RED]の古い友人に会ってくるよ。」 [scr]
   そういい残し、ベリンガムは部屋を出て行った。 [scr]
   そして、ザーゴはゆっくりと{name}に近づいてきた[W]・・・[/W]
EN Beringham: "{name}, Ignis has            (29 w/ 6-char name)
   sensed your presence.                      (21)
   He's trying to revive again!               (28)
   Zargo! I'll leave the rest                 (26)
   to you!                                    (7)
   I'm off to Mount Famfantar.                (27)
   {name}, I'll meet an old                   (24 w/ name)
   friend of yours there."                    (23)
   With those words,                          (17)
   Beringham left the room.                   (24)
   And then, Zargo slowly drew                (27)
   closer to {name}...                        (19 w/ name)
   [7 screens, all ≤2 rows; JP 7 screens]
```

Notes: the red span wraps `{name}`+君 — 君 ("-kun") has no natural EN
counterpart, so EN puts the name alone in red with the vocative comma
(flag 1). `{name}の存在に気が付いたイグニスが、` (Ignis noticed the
player's presence) is recast as a direct address: "…, Ignis has sensed
your presence." The trailing `[W]・・・[/W]` becomes `...` in its own run
(same pattern as msg 28).

### Message 42 — Zargo falls

```
JP ザーゴ「グウウウウッ！」 [scr] ザーゴが唸り声を上げ、▸ヒザをついて倒れこんだ！
EN Zargo: "Guuuuuh!"                          (17)
   Zargo let out a growl and                  (25)
   crumpled to its knees!                     (22)
   [2 screens; JP 2 screens]
```

### Message 43 — Ramires appears

```
JP その時、上空からベリンガムのもう一人の魔獣[RED]ラミレス[/RED]が現れた！
EN Just then, from the sky came               (28)
   his other beast: Ramires!                  (25)
   [1 screen; JP 1 screen]
```

Notes: added break keeps the red name starting row 2. もう一人の魔獣 =
"his other beast" (Beringham last named in msg 41). **ラミレス =
Ramires** — glyphs finally read (ミ = `0x82`, レ = `0x83`); matches the
8×8 beast-name list.

### Message 44 — Ramires' warning

```
JP ラミレスはザーゴの前に立ち、▸{name}に告げた！▸[7537 0014]
   ラミレス「自分・・・事・・・しりたいか・・・？」 [scr]
   [7538 0012 0013]ならば・・・ファムファンタル火山に行け・・・」 [scr]
   そう言い残してザーゴを抱え込み▸飛び立っていった
EN Ramires stood before Zargo,                (27)
   {name} was told:                           (16 w/ name)
   Ramires: "You wish... to know              (29)
   of yourself...?"                           (16)
   Then... go to                              (13)
   Mount Famfantar...!"                       (20)
   With that, it wrapped its arms             (30)
   around Zargo and flew away.                (27)
   [3 screens; s1 = 4 lines → 2 pages, JP s1 = 4 rows → 2 pages]
```

Notes: `{name}に告げた！` is object-first; the name renders first in the
row, so EN uses the passive "###### was told:" (flag 2). Ramires' halting
three-group ellipsis rhythm is kept. `抱え込み` = "wrapped its arms
around"; JP omits the final 。 — EN adds the period (flag 4).

### Message 45 — Kurimuto: to the volcano

```
JP クリムト「これも運命かの・・・▸こうなったら行くしかないぞ。 [scr]
   ファムファンタル火山へ・・・！ [scr] そこでおぬしの全てが解るはずじゃ！」 [scr]
EN Kurimuto: "Fate again, hm..."              (29)
   we've no choice but to go.                 (26)
   To Mount Famfantar...!                     (22)
   There, you'll learn everything             (30)
   about yourself!"                           (16)
   [4 screens; JP 4 screens]
```

### Message 46 — the second recipe

```
JP [7539 0015 0016][7539 0017 0018]クリムト「よいか、それまでに [scr]
   伝説の魔獣[RED][BE 08][/RED]の中型体を▸完成させるのじゃ！ [scr]
   次は[RED][BE 03][/RED]と [scr] [RED][BE 04][/RED]を合成する。 [scr]
   さすれば、[RED][BE 08][/RED]の [scr] 中型体[RED][BE 05][/RED]が▸完成するはずじゃ！」
EN Kurimuto: "Listen: by then,                (27)
   the Legendary Beast's medium               (28)
   form,                                      (5)
   you must complete it!                      (21)
   Next, combine and                          (17)
   .
   Then,'s                                    (7)
   medium form should be                      (21)
   complete!"                                 (10)
   [6 screens; s2 = 3 lines → 2 pages (JP s2 = 2 rows → 1 page)]
```

Notes: the row text above is the insert-blind simulation — in-game the
`[BE nn]` beast names appear at the `and`/`.`/`'s` slots (e.g. "Next,
combine [BE 03] and / [BE 04]." and "Then, [BE 08]'s / medium form
[BE 05] should be / complete!"). Rows are worded so each name slot reads
naturally; e2 holds a manual break because the base text ("the Legendary
Beast's medium form") would otherwise mid-wrap. 中型体 = "medium form"
(glossary term confirmed here; the msg-32 flag is resolved).

### Message 47 — Kurimuto departs (again)

```
JP クリムト「ワシはまた、伝説の魔獣の事をしらべに旅に出る。▸火山までの道のりは▸
   至難を極めるぞ！！」 [scr] そういい残し、▸クリムトは去って行った。
EN Kurimuto: "I set off again to              (29)
   study the Legendary Beasts."               (28)
   the road to the volcano                    (23)
   will be the hardest yet!!"                 (26)
   With those words,                          (17)
   Kurimuto departed.                         (18)
   [2 screens; JP 2 screens, s1 JP 5 rows → 3 pages, EN 4 lines → 2]
```

### Message 48 — the climb

```
JP {name}がファムファンタル火山を登り始めてから [scr]
   数え切れないほどの地震が起きていた。 [scr] {name}は感じた。 [scr]
   この揺れは[RED]イグニス[/RED]が▸地底で暴れている
EN {name} began the climb up                  (25 w/ name)
   Mount Famfantar,                           (16)
   since then, countless quakes               (28)
   had struck.                                (11)
   {name} felt it.                            (15 w/ name)
   This quake is Ignis,                       (20)
   raging underground.                        (19)
   [4 screens; JP 4 screens]
```

Notes: 登り始めてから = "began the climb up … / since then"; JP ends the
message without 。 — EN adds the period (flag 4). S4 keeps the JP row
split ("This quake is Ignis," / "raging underground.").

## Flags for review (all non-blocking)

1. **msg 41** — the red span is `{name}`+君; EN highlights the name alone
   and carries 君 as the vocative comma ("{name}, …"). If the user wants
   "-kun" kept literally, this is the one place it appears in-story.
2. **msg 44** — "{name}に告げた！" (object-first) rendered passively as
   "###### was told:"; alternative wording "###### heard it speak:"
   available if the passive reads flat.
3. **Ramires** romanization (msg 43) — provisional, same class as Zargo
   (ラミレス → Ramires). Confirm before the monster-names milestone.
4. **Terminal punctuation** — JP omits 。 at msg 44 r5 and msg 48 r6; EN
   adds "." per EN convention (recorded per message).
5. **msg 45** — これも運命かの → "Fate again, hm..." (old-man か → "hm",
   consistent with Kurimuto's voice).
6. **msg 46** — "よいか、それまでに" → "Listen: by then,"; "by then"
   reads as "by the time you reach the volcano" — revisit if msg 49+
   clarifies the timeline.
7. **msg 47** — 至難を極める → "will be the hardest yet!!" (set phrase,
   "will be extremely difficult").
8. **Insert rows** — all `[BE nn]` rows are sim-blind (insert width
   unknown); wording keeps base rows short so any 4–8 char EN beast name
   still fits. Final check at the monster-names milestone.

## Proposal for milestone 8

Story messages **49–56** (8 more boxes, same pipeline: render → read →
readings with zip-check → EN runs → exporter QA → milestone doc).
After M8 the remaining range is 57–62 (M9), then: the 8×8 string
inventory/monster-names milestone, the relocation writer, and the BPS
patch build.
