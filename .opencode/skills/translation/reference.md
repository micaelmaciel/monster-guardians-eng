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
- Three text subsystems, all extracted (2026-10-19): (1) 8×8 system/UI
  strings (1,215 corpus rows / 855 unique), (2) 16×11 "bigfont"
  story/cutscene messages (63 early + 33 late + 13 status words + R1
  support strings), (3) the field **message box** (169 strings, own 9×9
  font). Story M1–M9 cover bigfont; the message box is translated in
  `translation/msgfont_en.tsv` (M11); the 8×8 corpus and the story
  retranslation follow.
- Note: the message-box font's glyph 186 is ニ (not シ) → msg 61 is
  `イグニスを倒せ!` = **Ignis**, the story's final boss.

## Display constraints (message box, 169 strings)

- Box art 128×24 px inside two 64×32 OBJ sprites; interior exactly 20 px
  = **2 lines of 10 px pitch** (JP: wrap after **11 glyphs** on line 1,
  12 on line 2; measured in-game on msg 154).
- Planned patch (see WIKI.md): relocate font store + add ASCII glyphs,
  advance 10 → 9 px, wrap on spaces at 13 glyphs/line, optional 3rd line
  (box art redrawn ~8 px taller in the same OBJ bounds).
- **EN budget: ≤ 39 chars/string (3 lines × 13)**; keep the string's own
  header/body split (e.g. `Goal:` objectives) since the layout is
  automatic. Longest EN string in the pass is 40 (flagged); no manual
  line-break codes exist in this system — the engine wraps by count.
- Term locks: Order (命令), Goal (クリア条件 battle objectives; the
  standalone label stays "Clear Condition"), Battle Over (戦闘終了),
  Player Points, link (通信), deploy (出撃), in training (修行中),
  Eliminate (排除), Pummel (ボコれ), Item/Flee/Defend/Wait.

## Display constraints (bigfont story text)

- One story screen = one text box; max 2 lines per box; box ≈ 240 px.
- Japanese glyph advance = 12 px, row pitch 13 px, 2 rows per box page
  (OAM-measured M5) → 17 JP glyphs/line (the game auto-wraps JP mid-word;
  manual break = control `7530`). Widths vary (small kana and 、 are
  narrower): a 17-glyph line can still overflow and clear the box —
  msg 24, frames 19900–20100.
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
| ベリンガム | Beringham | Invader of Vandam Castle; Beast Knight Order (msgs 25+). Full name ベリンガム・ロー公爵 = "Duke Beringham Roe" (msgs 25+; 公爵 = Duke). **FLAG**: ロー → Roe/Rowe pending. |
| 廃墟 | ruins | Place caption (msg 14). |
| タクト | the Takt | Beast Tamer's baton (item; msg 12+). **FLAG**: keep as "Takt" unless user prefers "baton". |
| クリムト | Kurimuto | Old Beast Tamer (msgs 21+); gives the player his Takt (msg 29). **FLAG**: romanization TBD — クリムト is also the JP katakana for painter *Klimt*; alternatives Kurimuto / Klimt. |
| 老人 | Old man | Speaker card (msg 20) until the self-introduction caption (msg 21) switches to "Kurimuto:". |
| 事件 | the incident | msg 22 (red span). The Vandam Castle attack, retold msgs 25+. |
| 城主 | lord of the castle | msg 24. |
| 魔獣騎士団 | the Beast Knight Order | Pope's order that seized Vandam Castle (msg 25; red span verified in-game). |
| 法王 | the Pope | 法王直属 = "directly under the Pope" (msg 25); EN compresses to "The Pope's" for row width (M5 flag 2). |
| 公爵 | Duke | Title, placed before the name in EN ("Duke Beringham Roe"), inside the same red span (msg 25). |
| 首謀者 | mastermind | msg 25. EN "The mastermind: …". |
| 軍事顧問 | military advisor | msg 25; として仕えてきた = "who had served as". |
| 最高司令官 | supreme commander | msg 25; でもある = "is also". |
| 占拠 | seizure / occupation | 城を占拠した (msg 25) → "It fell." / "the seizure" (row width). |
| 濡れ衣 | frame-up | msg 25: まったくの濡れ衣 = "a complete frame-up". |
| 容赦なく捕らえられ | captured without mercy | msg 26. |
| 幼体 / 中型体 | young form / medium form | msgs 32 and 46 — "medium form" confirmed at msg 46; terminology no longer provisional. |
| 合成 | combine | msg 32: 合成すると = "combining …". |
| ザーゴ | Zargo | Beringham's man-made beast. Red span in msg 39; also in the 8×8 scripts (`ザーゴをたおせ！`) — keep one spelling across subsystems. **FLAG**: Zargo / Zaago provisional. |
| ラミレス | Ramires | Beringham's other beast (msgs 43–44); glyphs fully read (ミ/レ), matches the 8×8 beast list. Speaks in halting fragments. **FLAG**: Ramires provisional (Zargo class). |
| 復活 | revive | msg 41: 再び復活しようとしておる = "trying to revive again". |
| 告げる | to tell | msg 44: {name}に告げた！ → object-first clause; EN passive "###### was told:". |
| 抱え込む | wrap one's arms around | msg 44: ザーゴを抱え込み = "wrapped its arms around Zargo". |
| 唸り声 / ヒザ | growl / knees | msg 42 (ヒザ is katakana in JP): 唸り声を上げ = "let out a growl"; ヒザをついて倒れこんだ = "crumpled to its knees". |
| 道のり / 至難を極める | the road / be the hardest yet | msg 47: 火山までの道のり "the road to the volcano"; 至難を極める set phrase, "will be the hardest yet". |
| 登る / 数え切れない / 地底 | climb / countless / underground | msg 48: 登り始めてから "began the climb ... since then"; 数え切れないほどの地震 "countless quakes"; 地底で暴れている "raging underground". |
| 怒る | to get angry | msg 49: イグニス・・・怒る！ = "Ignis... gets angry!" (Ramires' taunt: the more you fight, the more Ignis stirs). |
| 狂暴な力 / みなぎる | violent power / surge up | msg 49 P4: [name]の体の中から狂暴な力がみなぎる = "felt a violent power surging up from deep within". |
| 朽ち果てた / 神殿跡 | crumbling / temple remains | msg 50: 朽ち果てた神殿跡 = "a crumbling temple" (msg 11 "enshrine" reused). |
| 着く | to reach / arrive at | msg 50: 火口に着くと = "At ... crater," (arrival implied in EN). |
| 待つ | to wait | msgs 50/54: 待っていたよ "I've been waiting."; 待っていたぞ、この瞬間を "I've waited for this moment." |
| 祝う / 盛大に | celebrate / in grand style | msg 50: 復活を盛大に祝おうではないか = "Let us celebrate the revival in grand style!!" |
| 届く | to reach (of a voice) | msg 50: 声は届かなかった = "voice did not reach". |
| 崩れ出した | began to crumble | msg 51. |
| クチ / 息使い / 嵐のような | maw / breath / like a storm | msg 53: クチ is katakana 口 → "maw"; 息使い = "breath". |
| 瞬間 | moment | msg 54: この瞬間を = "this moment". |
| 完全復活 | fully revived | msg 54: rephrased "has fully revived!" for row layout. |
| 例の古城跡 | the old castle ruins | msg 55: 例の (aforementioned) folded as "the old". **FLAG** (see open questions 13). |
| 合獣機 | beast combining machine | msg 55: new term; 合成 = "combine" (msg 46). Under review for the glossary. |
| 準備 | preparation | msg 55: 合獣機の準備をしろ = "prepare the beast combining machine". |
| 我々 / 不可能 | we / impossible | msg 56: 今の我々の力では…不可能じゃ = "We cannot beat Ignis as we are now!". |
| ひとまず | for now | msg 56: ここはひとまず逃げるぞ = "For now, we must flee!!". |
| 息をのむ | to hold one's breath | msg 55: {name}は息をのんだ = "{name} held their breath". |
| 久しぶり | long time no see | msg 57: 久しぶりだな = "It's been a while..." (the entity through [name]). |
| 表情 / 人格 / 変貌 | expression / personality / transform | msg 57: 表情 = "expression"; 人格 = "personality"; 〜へと変貌していた = "had transformed into". |
| 数百年 | centuries | msg 58: 数百年にもわたる戦い = "battle spanning centuries". |
| 決着をつける | to settle | msg 58: 決着を今ここでつけてやる = "I'll settle this ... here and now!". |
| 写る | to be reflected | msg 58: 背後に写るカノンの姿 = "Canon's reflected figure". |
| おたけび / 横たえる | roar / to lay down | msg 59: おたけびを上げ = "let out a roar"; 地面に体を横たえた = "laid its body on the ground". |
| やぶれる | to be defeated | msg 59: イグニスがやぶれるとは = "Ignis is being defeated!". |
| 発する / 光の帯 | emit / band of light | msg 60: 発せられた folded as "from ... hand"; 光の帯 = "band of light". |
| 包む / 宙に浮かぶ | wrap / float in the air | msg 60: 包み込む = "wrapped around"; 宙に浮かんだ = "floated up". |
| 彼方 | far beyond | msg 61: 空の彼方へ = "beyond the sky". |
| 強さ | strength | msg 62 final line: これほどの強さを = "had such strength..." (trails off). |
| 祭壇 | altar | msg 36: 祭壇のある部屋 = "the altar room". |
| 地震 | earthquake | msgs 36–38; 地震に気をとられる = "distracted by the quake" (msg 37). |
| 大男 | giant of a man | msg 37: 見たことも無い大男 = "a giant of a man unlike any ever seen". |
| 旅立つ / 何処かへ | set off / for parts unknown | msg 34: 何処かへ旅立って行った = "set off for parts unknown". |
| 裏に付く | to side with | msg 40: クリムトが裏に付いていた = "Kurimuto has sided with you". |
| 狙う | to target / be after | msg 39: 狙われておる = "is after you" (passive). |
| 振りかざす | to brandish | msg 39: タクトを振りかざそうとした = "just as the Takt swung up" (compressed for row width). |
| ゴゴゴゴゴ | RUMBLE! RUMBLE! RUMBLE! | msg 36 SFX line. |
| フフフ | "Heh heh heh..." | Beringham's laugh; inside a `7535`/`7536` white-style span (msg 40). |
| ヴァンダム城 | Vandam Castle | msg 23 caption, msgs 24+. |
| ウィンスロー | Winslow | ウィンスローのご子息 = "son of Winslow" (msg 21 via 753F); ウィンスロー二世 = "Winslow II" (msg 24). |
| 0x753F insert | [canned word] | Word-insert table `0xC73F0`: 4 slots × 2 gender variants (僕/私, ご子息/ご息女, 伝説の魔獣使い ×2, 彼/彼女); the engine picks `slot*2 + gender`. **Keep the control in the stream; localize the table** (supersedes the earlier "drop the control" note — hardcoding would lose the gender variant). |
| 0x753E insert | [beast name] | Beast-name inserts (msgs 31/32): **keep the control in the stream** — the name is dynamic (beast table, still JP until the monster-names milestone). EN is worded so the name slot reads naturally. |
| 0x7540 insert | [player name] | Keep as variable `{NAME}`; never translate. QA sim width = 6 chars. |

## Character sheet (story mode)

- **Narrator** (私 = "I"): unseen sentinel who "was sent" to the world
  when it had no gods; possesses the skill to save the fallen Beast Tamer
  (msg 8). Gender and identity are unmarked in msgs 0–16 — **do not add
  gendered pronouns in EN** until confirmed later in the script.
  Voice: calm, weighty, witness-like; full sentences; no contractions.
- **Canon (カノン)**: sky hydra dragon; ruled the skies; fell in the war
  (msg 7). No gendered pronouns used in EN yet. Its reflected figure
  appears behind [name] when the entity awakens (msg 58); Beringham ties
  [name]'s creation to Canon and the Legendary Beast Tamer (msgs 55/62).
- **Ignis (イグニス)**: earth hydra dragon; ruled the land; wounded; went
  into hiding deep beneath Mount Famfantar (msg 7). No gendered pronouns
  used in EN yet. Revives fully at the crater as a giant, magma-red
  dragon (msgs 52–54); Beringham's line ties the player's creation to it
  (msg 55). Felled by the awoken [name] (msg 59): roars, lies down;
  Beringham's light band lifts it away past the sky (msgs 60–61).
- **The man (男)** (msgs 10–13): unnamed; has the Takt; seeks revenge on
  the Legendary Beast Tamer and the world; exclamation-heavy, blunt,
  imperative. Voice: forceful, breathless menace. Identity unresolved —
  do not imply a link to later characters in EN yet.
- **Kurimuto (クリムト)** (msgs 20+): old Beast Tamer asleep in the
  ruins; saves the player, name-drops Beringham ("some history" with
  him), recognizes the player as Winslow's son, hands over his own Takt
  (msg 29) and beasts (msg 30), and departs to research the next beasts
  (msg 33). Returns to save the player from Zargo at the altar (msg 39)
  — old-man particle のう → "hm?". Voice: grumpy-soft, casual
  contractions, no modern slang. Witnesses the awakening (msg 57) and
  sees Canon's reflected figure behind [name] (msg 58).
- **Beringham (ベリンガム)** (msg 16 mention; msgs 25+ seen): leader
  figure of the Pope's Beast Knight Order, invader of Vandam Castle,
  mastermind of the coup (msg 25). Commands the man-made beast Zargo
  (msg 39) and his other beast Ramires, and mocks the player over the
  altar (msg 40). Grandiose, mocking (フフフ / ハハハ laughers); EN keeps
  the theatrical menace and the laugh beats ("Heh heh heh...", "Hahah!").
  At the crater he speaks of the altar enshrining Ignis (msg 50), hails
  the "fully revived" magma dragon as Ignis of the Earth (msg 54), orders
  his men to prepare the 合獣機 at the old castle ruins (msg 55), and
  reveals the player's origin: created by combining Ignis, Canon of the
  Heavens, and the Legendary Beast Tamer (msg 55). Aghast at Ignis's
  defeat (msg 59); his hand releases the light band that carries him and
  Ignis past the sky (msgs 60–62).
- **Ramires (ラミレス)** (msgs 43–44): Beringham's other beast; appears
  when Zargo falls and tells the player to go to Mount Famfantar ("You
  wish... to know of yourself...?"). Speaks in halting fragments
  ("..." between phrases); carries Zargo away. No gendered pronouns in
  EN — use "it". Returns with Zargo at the crater (msg 49), taunting:
  "Fight... a lot, and Ignis... gets angry!".
- **Pursuers 1/2/3 (追っ手１/２/３)** (msgs 14–16): guards of the Barroa
  Kingdom chasing the player character. Voice: loud, rough, bickering,
  a bit dim ("Uh... what was the name?"), greedy for reward. Routed by
  the beasts in msgs 17–19.
- **Player character**: name is variable (0x7540). Boy or girl (chosen at
  game start); do not assume gender in text that refers to the player.
  Msg 55 reveals the player was created by combining Ignis, Canon of the
  Heavens, and the Legendary Beast Tamer — keep EN pronouns neutral
  ("their" for the player in narration).
- **The entity inside [name] (msgs 56–62)**: awakens within the player
  ("something was awakening"), speaks in first person through [name]
  ("It's been a while...", "I'll settle this battle of centuries"), and
  Canon's reflected figure appears behind [name]. Never named or
  gendered on screen — keep EN ambiguous; add no epithets.
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
- **Onomatopoeia** (M6): the katakana rumble ゴゴゴゴゴ (msg 36) →
  "RUMBLE! RUMBLE! RUMBLE!"; laughs フフフ → "Heh heh heh...". Keep SFX
  loud but readable; do not invent extra SFX the JP lacks.
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
  a source screen may hold up to 3+ segs. M5+: up to 3 box pages per
  screen accepted for information-dense EN (exporter flags >6 lines) —
  e.g. msg 25 s1/s2, msg 31 s3, msg 40 s1.

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
8. **Beringham's surname** — RESOLVED M5: ベリンガム・ロー公爵 =
   "Duke Beringham Roe"; ロー romanization (Roe / Rowe) still a **FLAG**.
9. **7540 length** — QA sim reserves 6 chars for the player name
   (={`######`}); names longer than 6 could push msg 21/22 rows past
   30 — the naming UI milestone should cap EN name length.
10. **msg 33 その後** — その後の魔獣の作り方を調べる rendered "research
   how the next beasts are made" (the later-stage beasts; cf. 最初は in
   msg 32 and 中型体 later). M8 read (msgs 49–56): msg 55 names the
   合獣機 (beast combining machine) as the device behind beast creation,
   but その後 itself stays unconfirmed — revisit at M9.
11. **Zargo** romanization (see glossary FLAG) — fix the spelling before
   the monster-names milestone so story and 8×8 text match.
12. **Ramires** romanization (msg 43) — provisional, same class as Zargo;
   settle both together at the monster-names milestone.
13. **msg 55 君とのな…」** — JP trails off mid-thought; EN ". You and I,
   well..." (M8 flag 2). Alternative settled wording welcome.
14. **msg 55 合獣機** — EN "beast combining machine" (glossary row added).
   Confirm term before the monster-names milestone.
15. **msg 55 例の古城跡** — 例の (aforementioned) folded as "the old" in
   "at the old castle ruins". Revisit if a specific castle name is
   preferred once later text clarifies the location.
16. **msgs 56–62 entity** — the awakened voice speaks through [name]
   (`久しぶりだな`, msg 57); Canon's reflected figure appears behind
   [name] (msg 58). The text never names the entity — EN keeps the
   ambiguity (no added epithets). Confirm intent if the user knows the
   full game story.
17. **msg 59 s1 box page** — EN 3 rows → 2 box pages vs JP 2 rows → 1;
   the 67-char sentence cannot fit two 30-char rows. Recorded, not a
   defect.
