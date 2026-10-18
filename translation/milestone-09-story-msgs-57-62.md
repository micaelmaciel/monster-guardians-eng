# Milestone 9 — Story messages 57–62 (the awakening, Canon's power, the sky's far side)

Delivered 2026-10-18. Source: bigfont story script at `0xCFF84`, messages
57–62 (6 text boxes, 30 runs). The last story range in the game: something
awakened inside the player speaks ("Heh heh!" / "It's been a while..."),
the personality visibly changes, [name] declares the centuries-old battle
will be settled on the spot, and Kurimuto sees Canon's reflected figure
behind [name]. Ignis is felled; Beringham, aghast, releases a mysterious
band of light that wraps Ignis, lifts it into the air, and both are
carried past the sky's far side. The final line trails off over [name]'s
strength.

Machine-readable output: `translation/story_en.json`. Translation input:
`translation/story_en_runs.json`. Reference sheet (glossary / characters /
style): `.opencode/skills/translation/reference.md`.

`▸` marks a manual line break (including added `7530`s);
`[scr]` marks a screen break (`7532`); `[W]…[/W]` a style span
(`7535`/`7536`); `{name}` marks the player-name insert (`7540`). JP is
the verified reading from `WIKI.md`.

**Glyph pass this milestone**: messages 57–62 transcribed and zip-verified
against their token streams on the first pass — **23 new glyphs** bound
(久ぶ 表情 明違格変貌 百年決写横 発議光帯包む宙浮強). Bigfont charmap now
**429/685**. This completes the readings for all 63 story messages.

No new in-game captures were needed (M5 OAM display model reused). All
static rows are ≤30 chars; rows combining text with the `{name}` insert
are accounted with the tool's 6-char simulation.

## Delivered text (per message)

### Message 57 — the voice through [name]

```
JP クリムト「どうした！？」 [scr] {name}「フフフッ！」 [scr] {name}▸
   「久しぶりだな[W]・・・[/W]」 [scr] {name}の表情は [scr]
   明らかにいつもと違う人格へと変貌していた。
EN Kurimuto: "What's wrong!?"          (26)
  ######: "Heh heh!"                   (18)
   ######                              (6)
   "It's been a while..."             (22)
   ######'s expression                 (19)
   had clearly transformed into       (28)
   a different personality.           (24)
   [5 screens; JP 5 screens]
```

Notes: the awakened entity speaks through [name]; the JP name row (7540
then `7530`) is kept, so the name sits alone before the quote. フフフッ →
"Heh heh!" (msg 40 laugh family). `久しぶりだな` = "It's been a while..."
(ぶ glyph shared with `やぶれる`, msg 59).

### Message 58 — the challenge

```
JP {name}▸「数百年にもわたる戦いの▸決着を今ここでつけてやる！」 [scr]
   クリムトは{name}の背後に写るカノンの姿を見た。
EN ######                              (6)
   "I'll settle this battle of        (27)
   centuries, here and now!"          (25)
   Behind ######, Kurimuto saw        (27)
   the reflected figure of Canon.     (30)
   [2 screens; JP 2 screens]
```

Notes: `数百年` = "centuries"; `決着をつける` = "settle"; `写る` =
"reflected". "Behind" is added before the `{name}` insert so the name
lands mid-clause (JP word order would strand the insert).

### Message 59 — Ignis falls

```
JP 大地のイグニスがおたけびを上げ▸地面に体を横たえた。 [scr]
   ベリンガム「なんと言うことだ！▸イグニスがやぶれるとは！！」
EN Ignis of the Earth let out         (26)
   a roar, and laid its body          (25)
   on the ground.                     (14)
   Beringham: "What on earth!         (26)
   Ignis is being defeated!!"         (26)
   [2 screens; s1 = 3 rows → 2 pages (JP s1 2 rows → 1)]
```

Notes: 大地のイグニス kept as the full term. `おたけび` = "roar";
`横たえる` = "lay down"; `やぶれる` = "be defeated". s1 cannot fit two
EN rows (67 chars) — flagged.

### Message 60 — the light band

```
JP ベリンガム▸「[W]いかん、このままでは！！[/W]」 [scr]
   ベリンガムの手から発せられた不思議な光の帯が、 [scr]
   イグニスの体を包み込むと、▸その巨体が宙に浮かんだ。
EN Beringham                           (9)
   "Not good! This won't do!!"        (27)
   A mysterious band of light         (26)
   from Beringham's hand,             (22)
   wrapped around Ignis's body,       (28)
   its giant body floated up.         (26)
   [3 screens; JP 3 screens]
```

Notes: `いかん、このままでは` = "Not good! This won't do!!" (JP comma
dropped for width). `発せられた` folded: "from Beringham's hand" (the
light's origin implies the emission). `光の帯` = "band of light";
`包み込む` = "wrapped around"; `宙に浮かんだ` = "floated up". The JP
screen break after `光の帯が、` is kept (sentence continues).

### Message 61 — carried past the sky

```
JP 光に包まれたイグニスとベリンガムは、空の彼方へ飛んでいった。
EN Wrapped in light, Ignis and        (27)
   Beringham flew beyond the sky.     (30)
   [1 screen; JP 1 screen]
```

### Message 62 — the final line

```
JP ベリンガム「[W]なんということだ！[/W]」 [scr]
   カノンと魔獣使いが合成した▸{name}は、 [scr] これほどの{強}さを[W]・・・[/W]
EN Beringham: "What's happening!"     (30)
   Canon and the Beast Tamer          (25)
   ######, made by combining,         (26)
   had such strength...               (20)
   [3 screens; JP 3 screens]
```

Notes: `合成` = "combining" (msg 46/55 terms). `これほどの強さを` trails off
in JP; EN mirrors with "had such strength..." (final message of the game's
story). The `{name}` insert keeps its position after the JP break.

## Flags for review (all non-blocking)

1. **msg 57/58** — the entity inside [name] is never named on screen;
   Kurimuto sees Canon's reflected figure behind [name]. EN keeps the
   ambiguity (no added epithets). Confirm intent if the user knows the
   full game story.
2. **msg 57** — `久しぶりだな` = "It's been a while..." — the addressee is
   unstated in the text.
3. **msg 59 s1** — EN uses 3 rows → 2 box pages where JP uses 1. Two rows
   are impossible for the full EN sentence (67 chars).
4. **msg 60** — two width-foldings recorded: `いかん、このままでは` comma
   dropped; `発せられた` folded into "from Beringham's hand".
5. **msg 58/62** — added connective words ("Behind", "made by") to place
   the `{name}` insert naturally in EN; the JP insert position is kept.

## Status after this milestone

- Readings for **all 63 story messages** are verified (429/685 glyphs).
- EN runs cover **all 63 messages**; `story_en.json` exports clean with
  zero problems.
- Page deviations across the whole story set: msgs 38, 46, 47 (earlier),
  plus msg 53, 55, 59 (this range); all others match JP page counts.

## Proposal for milestone 10

The next milestone is the **8×8 monster-names / UI pass**: read and
translate the monster names (カゼミズ ホノオ ダイチ シンセイ アンコク
ザーゴ ラミレス, レオ ティーナ カノン, 第一/第二/最終形態, 大地のイグニス)
in the 8×8 font, cross-checking story spellings (Zargo / Ramires /
Beringham / Kurimuto) against the in-game name lists. After that, the
**English glyph strategy** (new letter glyphs + bigfont store relocation +
`0xD6C2C` pointer rewrite) and the **relocation writer / BPS build**.
