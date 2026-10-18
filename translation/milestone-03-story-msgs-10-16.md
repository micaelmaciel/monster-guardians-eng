# Milestone 3 — Story messages 10–16 (Famfantar + the ruins pursuit)

Delivered 2026-10-18. Source: bigfont story script at `0xCFF84`, messages
10–16 (22 text boxes). The scene shift from narration to the game's first
*dialogue*: the man with the Takt taunting Ignis, then Pursuers 1/2/3
chasing the player character for Lord Beringham's reward.

Machine-readable output: `translation/story_en.json`. Translation input:
`translation/story_en_runs.json`. Reference sheet (glossary / characters /
style): `.opencode/skills/translation/reference.md`.

`▸` marks a manual line break (including the few added `7530`s);
`[RED]…[/RED]` marks the game's red-text highlight span (`753B`/`753C`);
`{name}` marks the player-name insert (`7540`). JP is the verified reading
from `WIKI.md`.

**Box behavior verified in-game this milestone** (headless mGBA
playthrough, frames logged in `WIKI.md`): the `7533` caption shows alone
in the box and the box then clears for the narration; the 2-line box
clears and continues (pages) when a further line arrives; the `7540`
name renders in red inside the first insert. Details under *Layout*.

## Delivered text (per box)

### Message 10 — Mount Famfantar

```
JP ～ファムファンタル火山～ [7533] (caption)
EN ~Mount Famfantar~                            (17)

JP その[RED]男[/RED]は、いまだ盛んに噴煙を上げる、[RED]火口[/RED]にいた。
EN That [RED]man[/RED] stood at the [RED]crater[/RED],   ▸ (29)
   which still belched smoke.                       (26)
```

### Message 11 — the crater ruins

```
JP 火口には[RED]イグニス[/RED]を祭ったと思われる、廃墟が残っていた。 [scr]
EN At the crater, ruins that                    ▸ (25)
   enshrine [RED]Ignis[/RED] still remain.          (28)

JP 男「どうした！大地のイグニスよ！」
EN Man: "What's wrong,                          ▸ (19)
   Ignis of the Earth!"                             (20)
```

### Message 12 — the Takt of the Legendary Beast Tamer

```
JP 男「このタクトを見て思い出さないのか？」 [scr]
EN Man: "Remember this Takt?"                       (26)

JP 男「おまえを世界から追いやった／[RED]伝説の魔獣使い[/RED]のタクトだ！」 [scr]
EN Man: "It's the Takt of the                       (26)
   [RED]Legendary Beast Tamer[/RED]                     (21)
   who cast you from the world!"                    (29)   ▸ (page)

JP 男「今再びよみがえりヤツに、／いやこの世界に [scr]
EN Man: "Rise again now and take                ▸ (29)
   on him... no, on this world.                     (28)

JP 共に、[RED]復讐[/RED]しようではないか！！
EN Together, let's take [RED]revenge[/RED]!!            (30)
```

### Message 13 — "still too weak"

```
JP 男「[W]・・・[/W]」 [scr]
EN Man: "..."                                       (10)

JP 男「これだけではまだ弱いか！[w8]／やはりヤツを[W]・・・[/W]」 [scr]
EN Man: "Is that all you've got!"               ▸ (30)
   As I thought, it's him..."                       (26)

JP そのとき男は足元の地中深くから、何かがうごめく／のを感じとっていた。
EN Just then, the man sensed                    ▸ (25)
   something moving deep below.                     (28)
```

### Message 14 — the ruins at dawn

```
JP ～廃墟～ [7533] (caption)
EN ~Ruins~                                          (7)

JP 朝もやの中、人里離れた廃墟から、／男達の声が聞こえた！ [scr]
EN Through morning mist, from the               ▸ (30)
   remote ruins, shouts rang out!                   (30)

JP 追っ手１「見つけ出すぞ！」 [scr]
EN Pursuer 1: "We'll find you!"                     (28)

JP 追っ手２「逃がすな！！」
EN Pursuer 2: "Don't lose him!!"                    (29)
```

### Message 15 — the Barroa guards (box pages)

```
JP それは、バルロア王国配下の／衛兵達であった。／追っ手３「もう逃がさんぞ！」 [scr]
EN They were royal guards of the                ▸ (29)
   Kingdom of Barroa.                                (18)
   Pursuer 3: "No more escapes!"                    (29)   ▸ (page)

JP 追っ手２／「えーと[W]・・・[/W][w26] こいつの名前は？」
EN Pursuer 2:                                        (9)
   "Uh... what was the name?"                       (26)
```

### Message 16 — the name reveal

```
JP 追っ手３「あ、そうだ！」 [scr]
EN Pursuer 3: "Oh, that's right!"                   (30)

JP 追っ手１／「[RED][名][/RED]だった！」 [scr]
EN Pursuer 1                                    ▸ (9)
   "It was [RED]{name}[/RED]!"                      (16 w/ 6-char name)

JP 追っ手２「かくごしろ！／[名]！」 [scr]
EN Pursuer 2: "Prepare yourself!                 ▸ (29)
   {name}!                                          (~7)

JP おまえを捕まえて[RED]ベリンガム様[/RED]に／渡せば謝礼がたんまりと[W]・・・[/W]」 [scr]
EN Catch you for [RED]Lord Beringham[/RED],           ▸ (29)
   and get a fat reward..."                         (24)

JP そういって追っ手達が[名]に手をかけようとしたその時！
EN With that the pursuers moved                  ▸ (28)
   to grab {name}... just then!                     (28 w/ 6-char name)
```

## Layout — verified in-game, not just simulated

The headless playthrough (menu → NEW GAME → story start) was captured
frame-by-frame and compared against these boxes:

- **Caption clearing** — msg 10 caption `～ファムファンタル火山～` shows
  alone in the bordered box, then the box clears and その男は… types
  (story_run frames 10400–10700). The `7533` simulation now splits
  screens there.
- **Box paging** — msg 15 screen 1's three segments show as two lines,
  then the box clears and the third segment types from the top
  (frames 13800–14000). A further line after a full box pages
  automatically; each page holds ≤2 lines. So 3-segment source screens
  are safe, and our EN mirrors the same page split (2 + 1 lines).
- **Name insert** — `7540` renders in red inside msg 16 screen 2; the
  naming UI (8×8-font screens: なまえ / モンスター選択 + はい/いいえ)
  appears *between* msgs 15 and 16 and sets the value (default レオ in
  the capture). The UI strings are a separate later milestone.
- **Auto-wrap** — msg 13 screen 3's single 33-glyph segment wraps at 17
  glyphs in-game (そのとき男は足元の地中深くから、何／かがうごめく…),
  the case our added `7530` replaces with a clean EN break.

## Workflow followed

Same pipeline as milestones 1–2: verified JP readings → drafted against
the reference sheet (new voice sheets for the man and the pursuers) →
naturality pass → intent check → automated QA (`tools/story_en_export.py`,
sim extended this milestone for `7533` captions, `7540` width, and box
paging) → proofread. All runs drafted together, QA before commit.

### Automated QA results (all pass)

- Run parity per message: 6 / 4 / 9 / 8 / 5 / 7 / 14 — 1:1 with source ✓
- Control codes identical to source; **6 added `7530`s** — msg 10 ×1,
  msg 11 ×2, msg 12 ×1, msg 13 ×1, msg 16 ×1 — each replaces a JP
  mid-segment auto-wrap or splits an over-30 EN line at a word boundary ✓
- Red spans kept on the same concepts: 男 → "man", 火口 → "crater",
  イグニス → "Ignis", 伝説の魔獣使い → "Legendary Beast Tamer",
  復讐 → "revenge", ベリンガム様 → "Lord Beringham", plus the `7540`
  name (first insert) ✓
- No CJK left in EN ✓
- Every segment ≤ 30 chars (no mid-word wraps); pages only where the
  source itself has >2 lines, or msg 12 screen 2 (3 lines → 2 pages,
  see flag 3) ✓

## Decisions for review (flag)

1. **"Takt"** kept for タクト (staff-flag in the glossary). "Baton" is
   the literal reading; "Takt" (German *Taktstock*) is the game's item
   name and probably its English title too — will confirm later in the
   script.
2. **"Catch you for Lord Beringham,"** (msg 16) keeps 捕まえて "catch"
   on line 1; line 2 lands the reward clause. Alternative: *Hand you to
   Lord Beringham,* (drops "catch", keeps に-attachment literal).
3. **msg 12 screen 2 is 3 EN lines (2 pages)** — JP is 2 lines. The
   full relative clause ("…who cast you from the world!") does not fit
   the 30-char lines around the red title without a mid-word break. EN
   pages once more than JP. Alternative: drop the clause (keeps 2 lines,
   loses the taunt's key fact).
4. **"on him... no, on this world."** (msg 12 screen 3) mirrors the JP's
   ヤツに、いやこの世界に pivot; the verb lands in screen 4 ("Together,
   let's take revenge!!"). Read the two screens as one sentence.
5. **Gender-neutral pursue lines**: msg 15 asks "what was the name?"
   (こいつの名前); the player enters the name right after and the
   character's gender is not established — no "his/her" until confirmed.
6. **"Pursuer 1/2/3"** card style confirmed (was open question #6 in
   the reference sheet — now delivered).
7. **msg 12's quote never closes** (JP has no 」 in the message) — EN
   mirrors; msg 16's quote closes only in screen 4's last line.
8. **"shouts rang out!"** (msg 14) — 男達の声 "the men's voices" does
   not fit line 2 (=30); the pursuers are on screen next, so the
   referent is immediate.

## Next milestone proposal

- **M4: messages 17+** — the girl/character continues; the playthrough
  already captured frames past msg 16 (up to ~frame 24000) to verify
  layouts as we go; the naming + monster-select UI strings (8×8 font)
  are proposed as a separate, later milestone.
- Remaining open items from WIKI carry over (3-line screen behavior now
  resolved — paging verified).

Please review the flagged decisions at your convenience; workflow
decision of 2026-10-18 stands (no per-milestone pause — M4 drafting may
proceed unless something here needs a change).
