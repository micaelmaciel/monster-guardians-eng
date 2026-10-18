# Milestone 8 — Story messages 49–56 (the beasts' taunt, the ruined altar, the revival)

Delivered 2026-10-18. Source: bigfont story script at `0xCFF84`, messages
49–56 (8 text boxes, 52 runs). Zargo and Ramires reappear; the player
feels a violent power surge from within. At the crater the ruined altar
of Ignis waits; Beringham celebrates, Kurimuto arrives too late, and
after the beasts are beaten the ground crumbles — a magma-red dragon
rises from the depths: Ignis, fully revived. Beringham orders his men
to the old castle ruins and reveals the player's origin; as Kurimuto
urges retreat, something awakens inside the player.

Machine-readable output: `translation/story_en.json`. Translation input:
`translation/story_en_runs.json`. Reference sheet (glossary / characters /
style): `.opencode/skills/translation/reference.md`.

`▸` marks a manual line break (including added `7530`s);
`[scr]` marks a screen break (`7532`); `[RED]…[/RED]` marks red-text
highlight spans (`753B`/`753C`); `[W]…[/W]` a style span (`7535`/`7536`);
`{name}` marks the player-name insert (`7540`). JP is the verified
reading from `WIKI.md`.

**Glyph pass this milestone**: messages 49–56 transcribed and
zip-verified against their token streams on the first pass — **26 new
glyphs** bound (怒狂ぎ / 着朽果殿跡待祝コ届 / 崩 / マ赤チ嵐 / 瞬間 /
例準備 / 我能 / ひ). Bigfont charmap now **406/685**.

No new in-game captures were needed (M5 OAM display model reused). All
segments are ≤30 chars; rows combining text with the `{name}` insert are
accounted with the tool's 6-char simulation.

## Delivered text (per message)

### Message 49 — the beasts appear

```
JP と突然、ベリンガムの魔獣▸[RED]ザーゴ[/RED][7537 001A]と[RED]ラミレス[/RED][7537 0019]が現れた。
   [scr] ザーゴ「もっと・・・戦え！」 [scr]
   ラミレス「たくさん・・・戦えば、▸イグニス・・・怒る！」 [scr]
   {name}は体の中から[RED]狂暴な力[/RED]がみなぎるのを感じていた[W]・・・[/W]
EN Suddenly, Beringham's beasts       (28)
   Zargo and Ramires appeared!        (27)
   Zargo: "Fight... more!"            (23)
   Ramires: "Fight... a lot,          (25)
   and Ignis... gets angry!"          (25)
   {name} felt, from deep within,     (30 w/ name)
   a violent power surging up...      (30)
   [4 screens; JP 4 screens]
```

Notes: JP `と突然` continues msg 48's unclosed sentence ("…地底で暴れ
ている" + "と突然" = "as it raged, suddenly…"); EN bridges the pair with
"Suddenly," in msg 49 (flag 1). The `7537` pauses pass through around the
red name spans. P4: the red span holds `狂暴な力` = "a violent power"
(leading space inside the span; an added break after "within," keeps the
wrap at the clause edge).

### Message 50 — the ruined altar

```
JP ファムファンタル火山の火口に着くと、 [scr] そこには朽ち果てた神殿跡があった。 [scr]
   [7537 001B]ベリンガム「ここは大地のイグニスを祭った祭壇だよ。 [scr]
   待っていたよ。 [scr] もっともワシ以上にイグニスは▸君を待っていたはず・・・ [scr]
   さあ！[7534 0001]復活を盛大に▸祝おうではないか！！」 [scr]
   するとベリンガムの背後から魔獣達が現れた。▸[7537 001C]クリムト「ムッ！遅かったか。 [scr]
   いかんココで戦っては！」 [scr] しかし、遅れてきたクリムトの声は届かなかった・・・
EN At Mount Famfantar's crater,        (28)
   there stood a crumbling temple     (30)
   Beringham: "This altar              (22)
   enshrines Ignis of the Earth."     (30)
   I've been waiting.                 (18)
   Though Ignis must have awaited     (30)
   you even more than I...            (23)
   Now! Let us celebrate the          (25)
   revival in grand style!!"          (25)
   Then, from behind Beringham,       (28)
   the beasts appeared.               (20)
   Kurimuto: "Mmph! Too late, hm.     (30)
   This is no place to fight!"        (27)
   But Kurimuto's voice, arriving     (30)
   too late, did not reach...         (26)
   [9 screens; s7 = 3 lines → 2 pages (JP s7 = 3 rows → 2 pages)]
```

Notes: `朽ち果てた神殿跡` = "a crumbling temple" (朽ち果てた rendered
"crumbling", 神殿 = "temple" per msg 11's enshrine note). `祭った` →
"enshrines" (msg 11 consistency). S7 rows land so the Kurimuto card
starts its own row. `届かなかった` = "did not reach".

### Message 51 — the ground gives way

```
JP ベリンガムの魔獣を倒したその時、大きく大地がゆれ [scr]
   {name}達の足元が崩れ出した。
EN When Beringham's beasts fell,      (29)
   the ground shook violently         (26)
   {name} and the others' footing     (30 w/ name)
   began to crumble.                  (17)
   [2 screens; JP 2 screens]
```

Notes: `達` = "and the others" (no equivalent suffix; the group with the
player). e1 starts with a space because the `{name}` insert precedes it.

### Message 52 — the dragon rises

```
JP そして地中深くより▸巨大なドラゴンが現れた。
EN And from deep underground,          (26)
   a giant dragon appeared.            (24)
   [1 screen; JP 1 screen]
```

### Message 53 — the dragon described

```
JP そのドラゴンは、まるでマグマのように赤い体をし、▸
   巨大なクチからは、嵐のような息使いが聞こえていた。
EN The dragon's body was red as        (28)
   magma, and from its giant           (25)
   maw came breath like a storm.       (29)
   [1 screen, 3 lines → 2 pages (JP 4 rows → 2 pages)]
```

Notes: `クチ` (katakana 口) → "maw"; `息使い` = "breath"; `嵐のような`
= "like a storm". The word "giant" ends a row and "maw" starts the next
(break at a space, no hyphen).

### Message 54 — the revival announced

```
JP ベリンガム「ハハッ！！[7534 0008]▸待っていたぞ、この瞬間を。 [scr]
   [RED]大地のイグニス[/RED]の完全復活だ！」
EN Beringham: "Hahah!!                 (19)
   I've waited for this moment.       (28)
   Ignis of the Earth                 (18)
   has fully revived!"                (19)
   [2 screens; JP 2 screens]
```

Notes: `ハハッ` follows the msg-40 laugh style ("Hahah!!"). `完全復活だ`
rephrased as "has fully revived!" so the red span ("Ignis of the Earth",
the msg 3/7 term) gets its own row via an added break (flag 4).

### Message 55 — Beringham's orders and the revelation

```
JP [7538 001D 001E]ベリンガム「おまえ達は例の古城跡で合獣機の準備をしろ！ [scr]
   ワシは二人の再会を見てから行く。 [scr]
   イグニスと[RED]天空のカノン[/RED]と[RED]伝説の魔獣使い[/RED]が [scr]
   合成して出来た[RED]{name}[/RED]君とのな・・・」▸{name}は息をのんだ。
EN Beringham: "You lot, prepare        (28)
   the beast combining machine        (27)
   at the old castle ruins!           (24)
   I'll leave once I've seen the      (29)
   two of them reunited.              (21)
   Ignis, Canon of the Heavens,       (28)
   and the Legendary Beast Tamer      (29)
   combined to create                 (18)
   {name}. You and I, well..."        (27 w/ name)
   {name} held their breath.          (25 w/ name)
   [4 screens; s1 = 3 lines → 2 pages (JP s1 2 rows → 1); s4 = 3 lines → 2 pages (JP 2 rows → 1)]
```

Notes: `7538(001D,001E)` passes through. `例の` (the aforementioned) is
folded as "the old" (flag 3). `合獣機` = "beast combining machine"
(flag 5 — new glossary term; 合成 = "combine" per msg 46). The three-item
list reuses the established red terms; the list is split `", / and`
to keep every row ≤30. `君とのな…」` trails off in JP; EN mirrors with
". You and I, well..." (flag 2). `息をのんだ` = "held their breath".

### Message 56 — something awakens

```
JP クリムト「今の我々の力では▸イグニスを倒す事は不可能じゃ！ [scr]
   ここはひとまず逃げるぞ！！」 [scr] しかしその時、▸{name}の中で [scr]
   何かが目覚めていた[7535 0001 0004]・・・[7536]
EN Kurimuto: "We cannot beat          (25)
   Ignis as we are now!"              (21)
   For now, we must flee!!"           (24)
   But just then,                     (14)
   {name}, deep inside,               (20 w/ name)
   something was awakening           (23)
   ...                                (3)
   [4 screens; JP 4 screens]
```

Notes: `我々` = "we"; `不可能` = "impossible" (rephrased across the row
split); `ひとまず` = "for now"; `ここは` = "For now" in s2. The trailing
styled dots (`7535`/`7536` span) become "..." in their own run.

## Flags for review (all non-blocking)

1. **msg 49** — "と突然" welds onto msg 48's unclosed sentence; EN opens
   with "Suddenly," so the pair reads as one beat. If the in-game text
   box clears between 48 and 49 (it should — separate boxes), the effect
   is: "…raging underground." / "Suddenly, Beringham's beasts…".
2. **msg 55** — "[{name}]君とのな…」" trails off mid-thought in JP. EN:
   ". You and I, well..." — the least-invasive rendering of the broken
   sentence; alternative readings ("you and I, you see…") available.
3. **msg 55** — `例の古城跡`: "例の" (the aforementioned / the agreed one)
   folded as "the old castle ruins". If a specific castle name is
   preferred later, this is the line to revisit.
4. **msg 54** — `完全復活` → "has fully revived!" (rephrase from the JP
   noun phrase for row layout).
5. **msg 55** — `合獣機` = "beast combining machine" (new term, added to
   the glossary; 合成 = "combine" established at msg 46).
6. **Page counts** — msg 53 and msg 55 s1/s4 use 2 box pages where JP
   uses 1–2; within the ≤3-page budget, kept as-is for clean EN rows.
   (msg 50 s7 and all others match JP: 3 lines → 2 pages.)

## Proposal for milestone 9

Story messages **57–62** (the last 6 boxes) — same pipeline: render →
read → readings zip-check → EN runs → exporter QA → milestone doc.
After M9: the 8×8 monster-names milestone (names: カゼミズ ホノオ ダイチ
シンセイ アンコク ザーゴ ラミレス; characters レオ ティーナ カノン; forms
第一/第二/最終形態; 太地のイグニス), then the relocation writer and the
BPS patch build.
