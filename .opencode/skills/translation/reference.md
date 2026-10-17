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
  auto-wraps JP mid-word; manual break = control `7530`).
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
| 魔術使い | sorcerer | Distinct from 魔獣使い (msg 5). |
| ファムファンタル火山 | Mount Famfantar | Volcano (msgs 7, 10). |
| バルロア王国 | the Kingdom of Barroa | msgs 15+. |
| 追っ手 | pursuer | msgs 14+; 追っ手１/２/３ = "Pursuer 1/2/3" (card style). |
| 衛兵 | guard | msgs 15+. |
| ベリンガム様 | Lord Beringham | 様 → "Lord". msg 16. |
| 廃墟 | ruins | Place caption (msg 14). |
| タクト | the Takt | Beast Tamer's baton (item; msg 12+). **FLAG**: keep as "Takt" unless user prefers "baton". |
| クリムト | Kurimuto | Old Beast Tamer (msgs 21+). **FLAG**: romanization TBD (Kurimt / Kurimuto). |
| ザーゴ | Zargo | Later story. |
| ヴァンダム城 | Vandam Castle | Later story. |
| ウィンスロー | Winslow | Later story. |
| 0x7540 insert | [player name] | Keep as variable `{NAME}`; never translate. |

## Character sheet (story mode)

- **Narrator** (私 = "I"): unseen sentinel who "was sent" to the world
  when it had no gods; possesses the skill to save the fallen Beast Tamer
  (msg 8). Gender and identity are unmarked in msgs 0–16 — **do not add
  gendered pronouns in EN** until confirmed later in the script.
  Voice: calm, weighty, witness-like; full sentences; no contractions.
- **Canon (カノン)**: sky hydra dragon; ruled the skies; defeated in the
  war (msg 7).
- **Ignis (イグニス)**: earth hydra dragon; ruled the land; wounded; hid
  deep beneath Mount Famfantar (msg 7).
- **The man (男)** (msgs 10–13): unnamed; has the Takt; seeks revenge on
  the Legendary Beast Tamer and the world; exclamation-heavy, blunt,
  imperative. Voice: forceful, breathless menace.
- **Pursuers 1/2/3 (追っ手１/２/３)** (msgs 14–16): guards of the Barroa
  Kingdom chasing the player character. Voice: loud, rough, bickering,
  a bit dim ("Uh... what was this one's name again?"), greedy for reward.
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
  UI/system contexts (none in story milestones so far).
- **Cries/emphasis**: keep exclamation marks as in source; do not upgrade
  single `！` to `!!`.
- **Onomatopoeia**: none encountered in story text so far.
- **Line breaks**: EN breaks are chosen for clean word wrapping; never
  hyphenate EN.

## Do-not-translate

- `MONSTER GUARDIANS` (title; rendered as graphics).
- Control codes / variables: `7530`–`7540`, `7FFF` (see WIKI.md table).

## Open questions

1. **Grandate** romanization (FLAG above).
2. **hydra dragon** vs. *Hydragon* (FLAG above).
3. Narrator identity/gender — confirmed male/female later in script?
4. **Kurimuto** romanization (flag).
5. Final English glyph metrics (8 px assumption) — wrap points may shift.
6. Should 追っ手１/２/３ be "Pursuer 1/2/3" or "Thug 1/2/3"? (chose pursuer;
   they are guards — watch for the game's later terminology.)
