# Monster Guardians — translation reference sheet

Canonical glossary / character sheet / style guide for the English
translation. Read this before translating any milestone; update it with
every decided term and every piece of user feedback. Companion docs:
`translation/milestone-*.md` (delivered text), `translation/story_en.json`
(machine-readable output), `WIKI.md` (technical state).

## Project brief

- Source: Japanese (JP) → Target: US English.
- Game: *Monster Guardians* (モンスターガーディアンズ), GBA, 2001,
  Konami / Mobile21, Japan-only. Tactical RPG; real-time monster battles;
  boy-or-girl player character. A Japanese launch title for the GBA.
- Tone: earnest 2001-era kids'/teens' fantasy adventure. The story mode
  narration is epic and solemn (war, gods, legendary beasts); in-game
  dialogue is lighter (comedy sidekicks, thugs). Preserve the contrast.
- Two text subsystems: (1) 8×8 system/dialogue strings (2,223), (2) 16×11
  "bigfont" story/cutscene messages (63). Milestones so far cover the
  bigfont story text only.

## Display constraints (bigfont story text)

- One story screen = one text box; max 2 lines per box; box ≈ 240 px.
- Japanese glyph advance ≈ 14 px → 17 JP glyphs/line (the game
  auto-wraps JP mid-word; manual break = control `7530`). Widths vary
  (small kana and 、 are narrower): a 17-glyph line can still overflow
  and clear the box — msg 24, frames 19900–20100.
- English will use new **halfwidth Latin glyphs** added to the relocated
  bigfont store (planned 8 px advance) → up to 30 chars per line, 60 per
  screen. **Working limits: ≤ 29 chars/line, ≤ 58 chars/screen** (flag
  overflows in QA). Final wrap tuning happens at insertion time once the
  glyph metrics are fixed.
- Preserve every control code exactly; `7530` line breaks may move or be
  added where English grammar/wrapping demands it (recorded per message).
- No em dashes or curly quotes in EN text (no planned glyphs); use
  commas, periods, `...` (three ASCII dots), straight `"` quotes.

## Glossary — story text (bigfont)

| JP | EN | notes |
|----|----|-------|
| グランデート大陸 | the continent of Grandate | No official romanization exists. **FLAG**: alternatives Grandēto / Grandeato. Chosen for readability. |
| ハイドラゴン | hydra dragon | Race name, lowercase as description. Possibly intended "Hydragon". **FLAG** for user. |
| カノン | Canon | Sky hydra dragon. |
| イグニス | Ignis | Earth hydra dragon. |
| 暗黒の時代 | the Age of Darkness | Title card (msg 1). Title case. |
| 魔獣 | magical beast / beast | Context-dependent; "beast" in prose. |
| 魔獣使い | Beast Tamer | Role/class term; "beast tamer" in plain prose, capitalized as a title. |
| 伝説の魔獣使い | the Legendary Beast Tamer | Red-highlighted title phrase (msgs 9, 12). |
| 魔術使い | sorcerer | Distinct from 魔獣使い (msg 5). Red-highlighted reveal (753B). |
| 生命 | life | 全ての生命 = all life (msg 5). |
| 繁栄 | prosperity | msgs 0 and 5. |
| 戦い / 戦争 | battle / war | Keep distinct: 戦争 = war (msg 4), 戦い = battle (msgs 6+). |
| 人類 | mankind | msg 9–. |
| 支配者 | ruler | 人類が支配者となった → "came under mankind's rule" (msg 9). |
| ファムファンタル火山 | Mount Famfantar | Volcano (msgs 7, 10). |
| バルロア王国 | the Kingdom of Barroa | msgs 15+. |
| 追っ手 | pursuer | msgs 14+; 追っ手１/２/３ = "Pursuer 1/2/3" (card style). |
| 衛兵 | guard | msgs 15+. |
| ベリンガム様 | Lord Beringham | 様 → "Lord". msg 16. |
| ベリンガム | Beringham | Invader of Vandam Castle; Beast Knight Order (msgs 25+). Full name ベリンガム・ロー□□ — surname glyphs pending (M5). |
| 廃墟 | ruins | Place caption (msg 14). |
| タクト | the Takt | Beast Tamer's baton (item; msg 12+). **FLAG**: keep as "Takt" unless user prefers "baton". |
| クリムト | Kurimuto | Old Beast Tamer (msgs 21+); gives the player his Takt (msg 29). **FLAG**: romanization TBD — クリムト is also the JP katakana for painter *Klimt*; alternatives Kurimuto / Klimt. |
| 老人 | Old man | Speaker card (msg 20) until the self-introduction caption (msg 21) switches to "Kurimuto:". |
| 事件 | the incident | msg 22 (red span). The Vandam Castle attack, retold msgs 25+. |
| 城主 | lord of the castle | msg 24. |
| 魔獣騎士団 | the Beast Knight Order | Pope's order that seized Vandam Castle (msg 25; red span verified in-game). |
| 法王 | the Pope | 法王直属 = "directly under the Pope" (msg 25). |
| ザーゴ | Zargo | Beringham's beast; later story. |
| ヴァンダム城 | Vandam Castle | msg 23 caption, msgs 24+. |
| ウィンスロー | Winslow | ウィンスローのご子息 = "son of Winslow" (msg 21 via 753F); ウィンスロー二世 = "Winslow II" (msg 24). |
| 0x753F insert | [canned word] | One occurrence: ご子息 "son" (msg 21). **Drop the control; carry the word as plain EN text.** Same default planned for 753E (beast-name inserts, msgs 31+). |
| 0x7540 insert | [player name] | Keep as variable `{NAME}`; never translate. QA sim width = 6 chars. |

## Character sheet (story mode)

- **Narrator** (私 = "I"): unseen sentinel who "was sent" to the world
  when it had no gods; possesses the skill to save the fallen Beast Tamer
  (msg 8). Gender and identity are unmarked in msgs 0–16 — **do not add
  gendered pronouns in EN** until confirmed later in the script.
  Voice: calm, weighty, witness-like; full sentences; no contractions.
- **Canon (カノン)**: sky hydra dragon; ruled the skies; fell in the war
  (msg 7). No gendered pronouns used in EN yet.
- **Ignis (イグニス)**: earth hydra dragon; ruled the land; wounded; went
  into hiding deep beneath Mount Famfantar (msg 7). No gendered pronouns
  used in EN yet.
- **The man (男)** (msgs 10–13): unnamed; has the Takt; seeks revenge on
  the Legendary Beast Tamer and the world; exclamation-heavy, blunt,
  imperative. Voice: forceful, breathless menace. Identity unresolved —
  do not imply a link to later characters in EN yet.
- **Kurimuto (クリムト)** (msgs 20+): old Beast Tamer asleep in the
  ruins; saves the player, name-drops Beringham ("some history" with
  him), recognizes the player as Winslow's son, and later hands over
  his own Takt (msg 29) and beasts (msg 30). Grumpy-soft old-man voice:
  casual contractions, gruff asides, no modern slang.
- **Beringham (ベリンガム)** (msg 16 mention; msgs 25+ seen): leader
  figure of the Pope's Beast Knight Order, invader of Vandam Castle.
  Grandiose, mocking (フフフ / ハハハ laughers); EN keeps the theatrical
  menace and the laugh beats ("Heh...", "Hahah!").
- **Pursuers 1/2/3 (追っ手１/２/３)** (msgs 14–16): guards of the Barroa
  Kingdom chasing the player character. Voice: loud, rough, bickering,
  a bit dim ("Uh... what was the name?"), greedy for reward. Routed by
  the beasts in msgs 17–19.
- **Player character**: name is variable (0x7540). Boy or girl (chosen at
  game start); do not assume gender in text that refers to the player.
- **Legendary Beast Tamer**: the hero of the old war (msgs 5–13); the man
  (msgs 10–13) seeks revenge related to this figure.

## Style guide

- US English; standard punctuation; straight quotes; `...` for ellipses.
- **Narration**: literary epic register, but tight — short sentences,
  strong verbs, no filler. No contractions. No modern slang. Keep the
  weight of だったのであった style endings without over-arching English
  ("And so it was that..." — use sparingly, if at all).
- **Dialogue**: natural modern speech; contractions fine; each speaker
  keeps a distinct voice per the character sheet.
- **Names**: per glossary; no Japanese honorifics (-san/-chan); 様 → Lord.
- **Numbers**: spell out small numbers in prose ("two"); digits only in
  UI/system contexts (none in story milestones so far); regnal suffixes
  use capital Roman numerals — ウィンスロー二世 = "Winslow II" (msg 24).
- **Word inserts**: `753F`/`753E` print a canned JP word (ご子息 "son",
  msg 21; beast names, msgs 31+). The EN patch **drops the control** and
  spells the word as plain text in the surrounding runs.
- **Cries/emphasis**: keep exclamation marks as in source; do not upgrade
  single `！` to `!!`.
- **Onomatopoeia**: none encountered in story text so far.
- **Line breaks**: EN breaks are chosen for clean word wrapping; never
  hyphenate EN.
- **Box seams** (user feedback, 2026-10-17): a long sentence may span
  boxes (text too big for one box) — continue it in the next box with a
  lowercase start. Do not end a box on a noun phrase and restart the
  next box with a pronoun for it ("…the two giant hydra dragons" /
  "They held dominion…" ✗ — reads as "the dragons, they…"). Land seams
  on clause boundaries where possible.
- **"this" + person** (user feedback, 2026-10-18): この + person → "the",
  never "this" ("this Beast Tamer" reads like casual "this guy"). "this"
  stays for places/ideas in narration ("this world", "this continent").
- **Red text** (`753B`/`753C`): wraps a reveal word or phrase. Keep the
  same emphasized concept inside the span (msg5 魔術使い → "sorcerer",
  msg8 私 → "me", msg9 伝説の魔獣使い → "the Legendary Beast Tamer")
  and keep the span on one line.
- **Speaker cards**: `Man: "…"` / `Pursuer 1: "…"` / `Old man: "…"` — JP
  男/追っ手/老人「…」 gets a colon + straight quotes in EN. When the JP
  card stands alone on its line, so does the EN (`Pursuer 2:` /
  `"Uh... what was the name?"`). After the self-introduction caption
  (msg 21) the old man's card reads `Kurimuto: "…"` — matching the JP's
  老人 → クリムト shift. A quote that spans boxes stays open until the
  JP closes it (msg 12's invitation never closes — EN mirrors; msg 16's
  quote closes in screen 4).
- **Captions** (`7533`): `~Mount Famfantar~`, `~Ruins~` — ASCII `~`
  pair. Verified in-game: the caption shows alone in the box and the
  box then clears for the narration (sim splits there).
- **Box paging** (verified in-game, msg 15): the box shows 2 lines and
  clears automatically when a further line arrives (2 lines + 1 page
  for the JP's 3-segment screen). msg 21: quote + tail = 2 pages ✓.
  msg 24: **JP itself clears between line 1 and line 2** (2 display
  pages — frames 19900–20100); EN mirrors the page count, but the split
  point may differ when width demands (flag in the milestone doc).
  Keep every segment ≤30 chars so page breaks fall where the JP's do;
  a source screen may hold up to 3+ segs.

## Do-not-translate

- `MONSTER GUARDIANS` (title; rendered as graphics).
- Control codes / variables: `7530`–`7540`, `7FFF` (see WIKI.md table).

## Open questions

1. **Grandate** romanization (FLAG above).
2. **hydra dragon** vs. *Hydragon* (FLAG above).
3. Narrator identity/gender — confirmed male/female later in script?
4. **Kurimuto** romanization — Kurimuto / Klimt (クリムト = JP
   katakana for the painter Klimt; fantasy-cast name) / Kurimt.
5. Final English glyph metrics (8 px assumption) — wrap points may shift.
6. Player-character gender: the naming screen (between msgs 15 and 16)
   lets the player name the character (default name observed: レオ).
   Keep pursuit lines gender-neutral until the story confirms.
   The naming/monster-select UI screens are 8×8-font text — later
   milestone.
7. **msg 21 story line** — 「いや、助けたのはベリンガムと言う名を聞いてな。」
   taken as "the reason I stepped in: I heard the name Beringham"
   (te-form reason). Alternative: "the one I saved is named Beringham."
   User confirmation welcome (one-run edit).
8. **Beringham's surname** — ベリンガム・ロー□□ (msg 25): 2 glyph codes
   pending M5 reads.
9. **7540 length** — QA sim reserves 6 chars for the player name
   (={`######`}); names longer than 6 could push msg 21/22 rows past
   30 — the naming UI milestone should cap EN name length.
