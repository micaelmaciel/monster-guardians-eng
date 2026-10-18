# Milestone 5 — Story messages 25–32 (the coup, Winslow's death, the training arc)

Delivered 2026-10-18. Source: bigfont story script at `0xCFF84`, messages
25–32 (8 text boxes, 49 runs). Beringham's Beast Knight Order storms
Vandam Castle, Winslow is killed, the player finds Beringham with the
Takt, and Kurimuto hands over his beasts and starts the training arc.

Machine-readable output: `translation/story_en.json`. Translation input:
`translation/story_en_runs.json`. Reference sheet (glossary / characters /
style): `.opencode/skills/translation/reference.md`.

`▸` marks a manual line break (including added `7530`s);
`[RED]…[/RED]` marks the red-text highlight spans (`753B`/`753C`);
`[beast]` marks a beast-name insert (`753E <id>`, name from the beast
table — still Japanese until the monster-names milestone); `{name}` marks
the player-name insert (`7540`). JP is the verified reading from `WIKI.md`.

**Display model verified in-game this milestone** (OAM analysis of
`/tmp/opencode/story_run/` frames 20300–21300): the story box is drawn
with 16×16 OBJ sprites at 12 px advance, **2 rows per page** (row pitch
13 px), and the JP renderer wraps at **17 glyphs per row** — msg 25's
31-glyph culprit line types as 17+14 (frames 20600→20700), and msg 25
shows as 5 display pages in JP: screen 1 = [16-glyph row + 7-glyph
row] then [17+14 wrap], screen 2 = [8+12] then [17+10], screen 3 = [17+2].
This is the first milestone where the JP page structure was measured
directly instead of inferred from run lengths.

EN rows hold ~30 chars against JP's 17 glyphs, so information-dense
narration runs one box page longer than JP (msgs 25 s1/s2, 31 s3). The
exporter QA limit is now "≤6 rows (3 pages) per screen"; beyond that is
still a restructure flag. Dialogue-heavy screens (26–30, 28) still match
JP page counts.

## Delivered text (per message)

### Message 25 — the Beast Knight Order takes the castle

```
JP 法王直属の[RED]魔獣騎士団[/RED]が城に乱入！▸城を占拠した。▸首謀者は、
   法王の軍事顧問として仕えてきた[RED]ベリンガム・ロー公爵[/RED]。 [scr]
EN The Pope's [RED]Beast Knight Order[/RED]            (29)
   stormed the castle! It fell.                       (28)
   The mastermind: the Pope's                         (26)
   military advisor,                                  (17)
   [RED]Duke Beringham Roe[/RED].                     (19)
   [5 rows -> 3 pages; JP 3 lines -> 2 pages]

JP 彼は[RED]魔獣騎士団[/RED]の▸最高司令官でもある男だ。▸彼は城占拠の理由を、
   王国に対立する組織へ協力した疑い！ [scr]
EN He is also the                                     (14)
   [RED]Beast Knight Order[/RED]'s                    (20)
   supreme commander.                                 (18)
   He gave his reason for the                         (26)
   seizure: aiding a faction                          (25)
   hostile to the kingdom!                            (23)
   [6 rows -> 3 pages; JP 3 lines -> 2 pages]

JP と、示したがまったくの濡れ衣であった。
EN That was his claim, but it                         (26)
   was a complete frame-up.                           (24)
   [2 rows -> 1 page; JP 17+2 wrap -> 1 page]
```

### Message 26 — Winslow's death

```
JP 捜索の邪魔をするものは、容赦なく捕らえられ、 [scr]
EN Those who hindered the search                      (29)
   were captured without mercy.                       (28)

JP その混乱の中{name}が見たものは、 [scr]
EN Amid the chaos, {name} saw:                         (27 w/ 6-char name)

JP 自分の目前ですでに息絶えている、▸父ウィンスローの姿であった。
EN their father Winslow, already                      (29)
   dead before their own eyes.                        (27)
```

### Message 27 — the unfamiliar Takt

```
JP そこには、見覚えの無い魔獣使いのタクトを手にしている [scr]
EN There he was, an unfamiliar                        (27)
   Beast Tamer's Takt in hand.                        (27)

JP ベリンガムの姿があった。
EN It was Beringham.                                  (17)
```

### Message 28 — Kurimuto has questions

```
JP クリムト「[W]・・・[/W]」 [scr]
EN Kurimuto: "..."                                     (15)

JP クリムト「伝説の魔獣使いのタクトが目的か？▸いや・・・なんでもない。 [scr]
EN Kurimuto: "So your aim is the                      (29)
   Legendary Beast Tamer's Takt?                      (29)
   No... never mind.                                  (17)
   [3 rows -> 2 pages]

JP それよりおぬし・・・▸父や家族の仇をとるつもりか？ [scr]
EN More to the point, will you                        (27)
   avenge your father and kin?                        (27)

JP 何も言わんでも▸その目が語っとるわい！」
EN You needn't say a word.                            (23)
   Those eyes say it all!"                            (23)
```

### Message 29 — the Takt is handed over

```
JP そう言うと、クリムトは自分のタクトを{name}に手渡した。
EN So saying, Kurimuto held                           (24)
   out his own Takt to {name}.                        (27 w/ 6-char name)
```

### Message 30 — the beasts are entrusted

```
JP クリムト「わしの魔獣達をおぬしにあずけよう。 [scr]
EN Kurimuto: "I leave my beasts                       (28)
   in your care.                                      (13)

JP しばらくこの廃墟をねぐらにして▸訓練するがよいぞ！」
EN Roost in these ruins a while,                      (29)
   and train all you like!"                           (24)
```

### Message 31 — the legend plan

```
JP クリムト「よいか、ベリンガム達と戦うには、 [scr]
EN Kurimuto: "Listen: to fight                        (27)
   Beringham and his men,                             (22)

JP この魔獣達では力不足じゃ！ [scr]
EN these beasts are too weak!                         (26)

JP そこで[RED]伝説の魔獣使い[/RED]がつれていた[RED]伝説の魔獣[/RED] [scr]
EN So, you'll make the                                (19)
   [RED]Legendary Beast Tamer[/RED]'s                 (23)
   [RED]Legendary Beasts[/RED]                        (16)
   [3 rows -> 2 pages; JP 21 glyphs -> 1 page]

JP [RED][beast][/RED]を作るんじゃ！」
EN [RED][beast][/RED]!                                (1 + name)
```

### Message 32 — the combination recipe

```
JP クリムト「ワシはその研究しておった。 [scr]
EN Kurimuto: "I've studied that.                      (29)

JP まだ一部しか▸解っておらんがの・・・」 [scr]
EN But only part of it, you                           (24)
   see..."                                            (7)

JP [T][T]クリムト「ワシの調べでは、最初は [scr]
EN Kurimuto: "First, combining                         (27)
   ([T] = 7539 pair, pass-through)

JP [RED][beast0][/RED]と▸[RED][beast1][/RED]を合成すると、 [scr]
EN [RED][beast0][/RED] and                             (4 + name)
   [RED][beast1][/RED],                                (1 + name)

JP [RED][beast8][/RED]の幼体[RED][beast2][/RED]が出来るはずじゃ！」
EN [RED][beast8][/RED]'s young form,                   (14 + name)
   [RED][beast2][/RED], should be created!"            (21 + name)
   [2 rows -> 1 page; JP ~22 glyphs -> 2 rows -> 1 page]
```

## Flags for review

1. **Beast names are dynamic** (msgs 31/32) — the `753E` inserts render
   name values from the beast table, which is still Japanese. The EN
   sentences are built so the name slots read naturally once the table
   is translated (separate monster-names milestone). Nothing to fix now;
   listed so the dependency is visible.
2. **msg 25 "直属" compression** — 法王直属の ("directly under the
   Pope") becomes "The Pope's" because the red span (18 chars) plus any
   longer qualifier exceeds the 29-char row. Also "It fell." carries
   城を占拠した ("the castle was occupied" would not fit the row).
3. **msg 25 red-span title order** — JP highlights ベリンガム・ロー公爵
   (name then 公爵); EN highlights "Duke Beringham Roe" (title first,
   matching the "Lord Beringham" convention). Same person, same span.
   The Roe/Rowe romanization remains open (carried from milestone 04).
4. **msg 25 paging** — screens 1 and 2 need 3 box pages in EN where JP
   used 2, purely from the 17-glyph vs 30-char row width. Content is
   complete; nothing was cut for the extra page except flag 2.
5. **msg 31 paging + verb position** — screen 3 (そこで…) needs 2 pages
   in EN vs JP 1; and the 作る verb ("you'll make") sits in the first row
   of that screen (the JP puts it in the next screen, after the beast
   insert). A verb in the last run would break the red-span row.
6. **msg 32 "I've studied that."** — ワシはその研究しておった compressed
   (the continuous "have been studying" does not fit the row); noted.
   "young form" for 幼体 is provisional until the 中型体 (medium form)
   terminology lands with the later script (msg 46).
7. **msg 28 "kin"** — 家族 renders as "family" everywhere else, but
   "avenge your father and family?" is exactly 30 chars, over the
   working 29 limit with the closing "?"; "kin" keeps the row safe.

## Next milestone proposal

- **M6: messages 33–40** — continuation of Kurimuto's training arc and
  the first synthesis results. Needs new in-game captures beyond frame
  24000 (the current run stops at msg ~25; captures must be extended
  with the existing `tools/mgba_dump` input schedule).
- Beast-name table + monster-names milestone (8×8 font side) remains
  queued; the story text is ready to accept those names dynamically.
