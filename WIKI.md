# Monster Guardians (GBA) — English translation project wiki

Single source of truth. Any agent in any session must be able to resume
from this file. Update it at the end of every work session and after each
milestone.

## Current state

- ROM supplied by user at `rom/monster-guardians.gba` (gitignored; never
  commit, never modify in place).
- **Phase: strategy APPROVED (2026-10-17); no ROM edits yet.** *Three*
  text subsystems are now structurally understood and **all three are
  fully extracted**: (1) 8×8 direct-code text — region-aware extraction
  gives **1,215 rows** (see "8×8 direct-code text corpus" in Findings);
  the 32 four-glyph kanji names (`0x1A0–0x1BF`) still await the user's
  reading from a rendered contact sheet; (2) 16×11 large-glyph story
  script at `0xCFF84` with a 685-glyph store at `0xD3144` — **fully
  enumerated**: 63 story messages + 33 late messages + 13 status words +
  the R1 support strings — see "Complete text inventory & completeness
  audit" in Findings; (3) the **field message box** system (9×9 message
  font at `0xCDED4`, 317 glyphs, descriptor `0xCF520`, renderer
  `0x0EC38`) — **169 strings fully extracted and decoded** into
  `build/msgfont_strings.tsv` + `data/msgfont_charmap.json` (317/317
  glyphs mapped) — see "Field message box — third text system" below.
  Remaining extraction work: graphics containing text (title screen,
  logos, name-input UI cells).
- **Workflow change (user, 2026-10-19): extract first, translate later.**
  All remaining Japanese text is to be fully extracted and inventoried
  before any further translation; the translation itself is then done in
  a dedicated pass with the translation skill (no RE/translation
  interleaving). The late-bank EN drafts (L0–L5, in
  `translation/late_story_en_runs.json`) are provisional and are to be
  retranslated from the complete corpus in that pass.
- **Story script is READABLE.** The 63 messages are fully decodeable;
  `tools/render_story.py` renders any message as a PNG (game-like layout,
  optional hex labels) and `tools/zoom_tokens.py` zooms token ranges.
  Charmap for the bigfont now has **649 glyphs verified** (all 63 story
  messages AND all 33 late messages zipped token-by-token against their
  streams with zero mismatches/conflicts, plus hand-verified name-input
  charset / status-word glyphs) via `tools/build_charmap_story.py`; see
  `data/bigfont_charmap.json`. Control parsing corrected 2026-10-18:
  `7538` takes **2 params** (was 1 — msg 22 desync fix), `753F` added as
  a 1-param insert (ご子息, msg 21), `7539` consumes **2 params** (was 1 —
  msgs 32/46 desync fix, confirmed pass-through).
- Confirmed by reading the actual game **and corrected by the M10 audit**:
  the large-glyph story text is 63 messages (intro attract = 0–9, then
  in-game event scenes) **plus 33 late messages** (the game's ending,
  `0xD1F96..0xD30F4`). The earlier assumption that the story bank ended
  at `0xD1F96` was the root cause of the miss; see "Complete text
  inventory & completeness audit" below. Same for R1 (insert tables,
  render fragments, scene variants) and the status word list.
- **Translation milestone 1 approved** (2026-10-17, rev 2 after user
  feedback — box-seam fix): story msgs 0–4 translated and QA'd — see
  `translation/milestone-01-story-msgs-00-04.md`; machine-readable output
  `translation/story_en.json`. Reference sheet (glossary/characters/style):
  `.opencode/skills/translation/reference.md`. QA/re-export done by
  `tools/story_en_export.py`.
- **Translation milestone 2 delivered** (2026-10-17; rev 2–3 after user
  feedback): story msgs 5–9 (intro narration part 2: the sorcerer, the
  long battle, the dragons' fate, the legend's birth) — see
  `translation/milestone-02-story-msgs-05-09.md`. Red-text spans
  (`753B`/`753C`) mapped to the same reveal concepts. Rev 2–3 reworked
  msg 8 boxes 3/4 ("…no one in this world who could save him.") and
  msg 9 boxes 1/2 (user wording: "In time, the Beast Tamer and his two
  beasts became legend. / The Legendary Beast Tamer, people took to
  calling him.").
- **Translation milestone 3 delivered** (2026-10-18): story msgs 10–16
  (the man with the Takt; the ruins pursuit — first dialogue cards,
  captions, three `7540` name inserts) — see
  `translation/milestone-03-story-msgs-10-16.md`. Box behavior verified
  in a live headless playthrough (see "Display limits"): the `7533`
  caption clears the box for the narration; a full 2-line box **pages**
  (clears and continues) when more lines arrive. The player-name entry
  UI sits between msgs 15 and 16 (8×8-font screens; separate later
  milestone).
- **Translation milestone 4 delivered** (2026-10-18): story msgs 17–24
  (the rescue in the ruins; Kurimuto's introduction; the incident
  retelling setup; the Vandam Castle location card and lord Winslow II)
  — see `translation/milestone-04-story-msgs-17-24.md`. 25 runs,
  QA `problems=0`, msgs 0–16 output byte-identical. New in-game facts:
  `7538` consumed as 2 params (msg 22 frame 19400), `753F 0001` prints
  canned ご子息 mid-line (msg 21 frame 19200; EN drops the control and
  carries the word), and msg 24's JP box **clears between its two lines**
  (2 display pages, frames 19900–20100). One story-reading flag raised
  for the user (msg 21 line 1, milestone-04 flag 1).
- **Translation milestone 5 delivered** (2026-10-18): story msgs 25–32
  (the coup, Winslow's death, the training arc; 49 runs, QA
  `problems=0`, msgs 0–24 output byte-identical) — see
  `translation/milestone-05-story-msgs-25-32.md`. New in-game facts: the
  JP story box was measured directly from OAM this milestone —
  **17-glyph rows, 2 rows per page (row pitch 13 px), 12 px advance**;
  msg 25 shows as 5 JP display pages (S1 2, S2 2, S3 1; the 31-glyph
  segment wraps 17+14 mid-word — frames 20300–21300). EN rows hold
  ~30 chars vs JP's 17 glyphs, so information-dense narration runs one
  box page longer than JP; the exporter QA budget was relaxed to
  **≤6 rows (3 pages) per screen** (was 4). 7 review flags recorded in
  the milestone doc (width-driven compressions; dynamic beast names).
- **Translation milestone 6 delivered** (2026-10-18): story msgs 33–40
  (Kurimuto departs, the tremor, Zargo at the altar; 39 runs, QA
  `problems=0`, msgs 0–32 output byte-identical) — see
  `translation/milestone-06-story-msgs-33-40.md`. Glyph pass added 22 new
  bigfont glyphs (方処旅知壇震ゆ近づ気暴振ざザ狙裏付遅面激) — charmap now
  **350/685**. `0x7F` read as ザ (not サ): the beast name ザーゴ =
  "Zargo" in msg 39's red span matches the 8×8 scripts
  (`ザーゴをたおせ！`), a useful cross-subsystem check. No new in-game
  captures were needed (M5's OAM display model reused for page
  accounting); every static row is ≤30 chars and the biggest EN/JP page
  deviation is msg 38 s1 (EN 1 page vs JP 2).
- **Translation milestone 7 delivered** (2026-10-18): story msgs 41–48
  (Beringham's exit, Zargo falls, Ramires appears, the second recipe, the
  climb; 52 runs, QA `problems=0`, full-range export 49 messages clean) —
  see `translation/milestone-07-story-msgs-41-48.md`. Glyph pass added 30
  new bigfont glyphs (活任ゾ古友会 ウッ 唸ヒ ミレ 告抱込飛 運 型完次
  道至難極 登数切ほ揺底) — charmap now **380/685**. **ラミレス = Ramires
  confirmed** (msg 43; glyphs fully read, matches the 8×8 beast list).
  No new captures needed; all static rows ≤30 chars (msg 41 s5 was
  rebalanced by one char). Page deviations: only msg 46 s2 (EN 3 rows vs
  JP 2) and msg 47 s1 (EN 4 rows vs JP 5; EN shorter).
- **Translation milestone 8 delivered** (2026-10-18): story msgs 49–56
  (the beasts' taunt, the ruined altar, Ignis's full revival; 52 runs,
  QA `problems=0`, full-range export 57 messages clean) — see
  `translation/milestone-08-story-msgs-49-56.md`. Glyph pass added 26
  new bigfont glyphs (怒狂ぎ 着朽果殿跡待祝コ届 崩 マ赤チ嵐 瞬間 例準備 我能
  ひ) — charmap now **406/685**. First read pass zip-verified clean.
  No new captures needed; all static rows ≤30 chars. Page deviations:
  msg 53 and msg 55 s1/s4 use 1 extra page (EN rows vs JP); rest match.
- **Translation milestone 9 delivered** (2026-10-18): story msgs 57–62
  (the awakening, Canon's power, the sky's far side — the final story
  range; 30 runs, QA `problems=0`, full-range export 63 messages clean)
  — see `translation/milestone-09-story-msgs-57-62.md`. Glyph pass added
  23 new bigfont glyphs (久ぶ 表情 明違格変貌 百年決写横 発議光帯包む宙浮強)
  — charmap now **429/685**, completing all 63 story messages. No new
  captures needed; all rows ≤30 chars (two width-foldings recorded,
  msg 60). Page deviation: msg 59 s1 (2 pages vs JP 1); rest match.
- **Text encoding is cracked.** Text = stream of 16-bit glyph indices;
  font = 512-glyph 8×8 tileset at ROM `0xBEDF0`; glyph index == text code.
  Verified: `tools/decode_strings.py` decodes the whole ROM to coherent
  Japanese (2,223 TEXT strings, 603 DATA/table strings).
- Charmap lives in `data/charmap.json` (built by `tools/charmap.py`).
- **Do not edit the ROM until the user approves the strategy proposal.**

## ROM identification

- File: `rom/monster-guardians.gba`, 8,388,608 bytes (8 MiB / 64 Mbit).
- Header title: `MONSTERGUARD`, game code `AMNJ`, maker `A4` (Konami),
  unit 0x96, complement 0x1B (mismatch vs computed 0x5F), checksum 0x0000.
  Normal for launch-window carts, **not corruption**.
- Publisher Konami; developer Mobile21; GBA launch title (March 2001).
- Japanese-only release.

## Pending investigation tasks

- [x] T1 — **Text storage**: 16-bit glyph-index strings (see Findings).
- [x] T2 — **Compression**: text is uncompressed. No verified compressed
  assets; LZ77/RLE hits were false positives.
- [x] T3 — **Pointers**: 32-bit little-endian direct pointers `0x08xxxxxx`.
- [x] T4 — **Free space**: one block of 625,059 bytes (see Findings).
- [x] T5 — **Font and display limits**: font decoded; display limits partly
  known (8×8 fixed glyphs; `0x1FF` = line break). Text-box line width still
  to be measured from a live screen.
- [x] T6 — **Prior art**: none found.
- [x] T7 — **Tooling**: chosen and recorded.
- [x] T8 — **Story/narration charmap**: character map for the 685-glyph
  store at `0xD3144`; all large-glyph text decoded — 63 story messages at
  `0xCFF84..0xD1F96`, 33 late messages at `0xD1F96..0xD30F4`, the status
  word list at `0xD30F4..0xD3144` and the R1 support strings at
  `0xCF52C..0xCFB82`. **649/685 glyphs verified** (readings via vision
  renders — no OCR); the 36 unfilled entries are unread symbols/fragments
  (see Open questions).
- [x] T9 — **Third text system (field message box)**: 9×9 "message font"
  317 glyphs at `0x0CDED4`, descriptor `0xCF520`, renderer `0x0EC38`,
  string table `0x0CC92C..0x0CDED4` = **169 strings**, all extracted and
  decoded (`build/msgfont_strings.tsv`, `data/msgfont_charmap.json`,
  317/317 glyphs). Found 2026-10-19; see "Field message box — third text
  system" in Findings.

## Prior art and tools

- **No fan translation, dump, disassembly, or dedicated tool exists** for
  Monster Guardians. Only translation *requests* (romhacking.net, Reddit).
- General GBA tooling applies (mGBA, capstone/ARM disasm, tile tools).

## Findings

### Text encoding (T1) — SOLVED

- Text is a stream of **16-bit little-endian glyph indices**.
- **Text code == glyph index into the font.** Verified end to end.
- Control codes:
  - `0x0000` — string terminator.
  - `0xFFFF` — padding / filler.
  - `0x1FF` — **line break** (renders as the enter-arrow glyph).
  - `0x001` — space / blank lead (roomaji space).
  - `0x7FFF` (and `0x75xx`-range values) — appear in non-text **data
    tables**, not prose; classed as `DATA`.
- Extracted inventory: `build/strings.tsv` (~2,826 rows) via
  `tools/extract_strings.py`; decoded dump `build/strings_decoded.tsv`
  via `tools/decode_strings.py` (2,223 TEXT + 603 DATA).
- Main text banks: `0x09DB08`, `0x0C5D9C`, `0x0A12AC`, `0x0A902A`,
  `0x0A9956`, `0x0A88A0`, `0x0B5728`, `0x0AEDE8`, `0x0CC912`, `0x0CD438`,
  `0x0CDAF8`, plus ~19 pointer-unreferenced script banks spanning
  `0x399756..0x48BD86` (~350 entries each).
- Sample decoded strings (coherent Japanese):
  - `0x09DBCA` — `CODE：11−000 ⏎ でんわがうまくかけられないか、かいせんが
    こんでいるためつうしんできません。…`
  - `0x0BD42A` — `ちしき ひっさつわざ はんげき さくてき じゅうじゅん
    めいちゅう かいひ ぎのう きしょう いどう ひこう Gold G …`
  - `0x0B7740` — item descriptions (`これをつけてゴウセイすると…`).

### Charmap (T5) — SOLVED (kanji via OCR, may need review)

`data/charmap.json` (334 entries), from user transcription of the font:

- `0x000`,`0x001` blank/space; `0x002–0x00B` `0–9`;
  `0x00C–0x025` `A–Z`; `0x026–0x03F` `a–z`.
- `0x040–0x08F` hiragana (80, includes small + dakuten/handakuten);
  `0x090–0x0DF` katakana (80, identical order).
- `0x0E0` ヴ; `0x0E1–0x0FF` CJK punctuation/symbols (`、。，．・：；？！ー／＼〜
  ＋−±×÷＝≠＜＞¥$％#&＊@（）`).
- `0x100–0x132` arrows / UI & box-drawing symbols; `0x133–0x13C` small
  digits; `0x13D` `lv`, `0x13E–0x13F` filled arrows; `0x140–0x16E`
  placeholder/gray-box glyphs; `0x16F` blank.
- `0x170–0x193` kanji (36): 世界無私恒共巨太匹空天地上血戦応百年文化消去一人
  脱火山下助持以外間支配常 — **OCR-derived; verify individual kanji during
  translation.**
- `0x194–0x19F` blank; `0x1A0–0x1BF` appear to be *cut/odd* tiles (possibly
  two squeezed kana) — likely unused; `0x1C0–0x1FE` blank;
  `0x1FF` enter arrow (line break).

### Font (T5) — SOLVED

- Font = **8×8 pixels, one glyph per tile, 4 bpp**, 32 bytes/glyph,
  512 glyphs (`0x000–0x1FF`), 16 KiB.
- **ROM base `0xBEDF0`**; loaded verbatim to **VRAM charBase 0**
  (`0x06000000`) at boot. BG2/BG3 draw text windows from it.
- Fixed-width: every glyph is 8 px wide (no VWF). Implication: English
  text needs roughly the same glyph count as Japanese, so it must be
  relocated (free space is ample).
- Reference render: `/tmp/opencode/fontcand/rom_BEDF0_8x8.png`.

### Emulator harness (T7)

- `tools/mgba_dump.c` — headless libmgba 0.10.5 harvester. Dumps
  VRAM/EWRAM/IWRAM/palette/OAM/I-O and PPM screenshots at scheduled frames,
  with scheduled button input.
- Build: `gcc -O2 -o tools/mgba_dump tools/mgba_dump.c -lmgba`.
- Usage: `tools/mgba_dump <rom> <outdir> [frames_csv] [input_spec]`.
- **Critical init sequence**: `mCoreFind` → `core->init` →
  `mCoreInitConfig(core,"mgba")` →
  `mCoreConfigSetDefaultValue(...,"idleOptimization","remove")` →
  `mCoreConfigSetDefaultIntValue(...,"logToStdout",0)` →
  `mInputMapInit(&core->inputMap,&GBAInputInfo)` → `mCoreLoadFile` →
  `core->reset` → `setVideoBuffer` → **`reloadConfigOption(core,
  "hwaccelVideo", &core->config)`** (associates the software renderer;
  without it screenshots are blank). Do NOT pass a zeroed `mCoreOptions`.
- `color_t` is `uint32_t` (not COLOR_16_BIT) — framebuffer is BGR8.
- Buttons set via `core->setKeys(core, 1<<GBA_KEY_*)`.
- Scheduled input windows: `"start-end:KEY+KEY,..."`, up to 256 windows;
  dump-frame list up to 1024 entries.
- **Input bug fixed 2026-10-18**: the original parser used `strtok` for
  both the window list and the key list — shared tokenizer state meant
  only the FIRST window was ever applied (the long "title menu is
  unresponsive" mystery). Now uses `strtok_r` for both. Verified: a
  scheduled A press shows in `io_*.bin` at `0x130` (KEYINPUT,
  active-low) as `0x03FE`, and the full menu → NEW GAME → story
  playthrough works under this harness.
- Save loading: set `MGBA_SAV=<path>` to load a `.sav` via
  `mCoreLoadSaveFile(core, sav, false)` after `mCoreLoadFile` (optional).

### Graphics / screen structure

- `DISPCNT` mode 0. BG0 is often a 64×64 **image** layer (tilemap of
  distinct sequential tile indices, e.g. map `0xD000`, charBase 1).
- BG2/BG3 use **charBase 0 = the font** and draw text windows (border tiles
  e.g. `0x120`–`0x145`).
- A large sequential glyph-ID table at ROM ~`0x399700` is copied to EWRAM
  `0x02004530`; it is a full-screen BG tilemap (image), not text.
- `0x0C5AF8` holds a kanji/glyph index list (data table), confirming the
  kanji range.

### Pointers (T3)

- 32-bit little-endian **direct** pointers `0x08xxxxxx`.
- 530 pointer tables found (e.g. `0x228C4`, `0x24634` → `0xA8864`,
  `0xB5728`, `0xB61F0`; array `0x0C370C` → `0x0CD3DC..0x0CD4AE`).
- Dense target hot-spots: `0x090000`, `0x0C0000`, `0x0B0000`,
  `0x540000–0x55FFFF`, `0x760000`.

### Free space (T4)

- One large free block: **`0x76765D..0x800000` = 625,059 bytes**, fill
  `0x00`. Ample for relocated dialogue.

### Large-glyph narration subsystem (story text) — format SOLVED

A **second, independent text subsystem** renders story/narration text as
individual 16×16 OBJ sprites, one sprite per character:

- **Glyph store: ROM `0xD3144`, 16×11 px glyphs, 22 bytes each**
  (stride 0x16). Layout per glyph:
  `[rows0-7 left half (8B)][rows0-7 right half (8B)][rows8-10 left
  (3B)][rows8-10 right (3B)]`.
- On screen each glyph is a 16×16 OBJ; its 4 tiles (TL,TR,BL,BR) = ROM
  left/right half-data + 5 zero pad bytes. **Verified byte-exact** against
  live VRAM dumps and the frame-0900 screenshot.
- Advance is 12 px; sprites at frame 0900: 6 glyphs at y=124, x=17..77,
  tiles 0,4,8,12,16,20. Frame 1800: 11 glyphs at y=124 + 15 at y=137,
  tiles 0..100 stride 4. All sz=1 (16×16), shape=0, pal=0.
- Confirmed glyph indices at 0xD3144: index14=だ `0xD3278`, 15=か
  `0xD328E`, 16=ら `0xD32A4`, 17=私 `0xD32BA`, 18=が `0xD32D0`, 19=使
  `0xD32E6`, 23=た `0xD333E`.
- The narration line `だから私が使` does **not** exist in ROM as 8×8
  direct codes (byte-search confirmed; `だから` hits at `0x0A86F6`,
  `0x0A8A64`, `0x0A9D7C` are ordinary dialogue).
- All on-screen text (dialogue included) is OBJ sprites, never BG text:
  BG2/BG3 tilemaps contain only box-frame tiles (1, 288–296, 320–328)
  across a 24,000-frame capture.
- Candidate structures in the narration region:
  - `0xD30F4..0xD3143`: entries of 2×16-bit codes terminated by `0x7FFF`
    (6 bytes each); 32-bit pointer table at `0xC4DD0` → each entry.
  - `0xD3000..0xD3143`: 16-bit blocks terminated by `0x7532`/`0x7540`
    (values do not decode with the 8×8 charmap → data).
  - `0xD6C24`: struct `{0x000B,0x000B,0x40000000,ptr=0x080D3144,
    count=4,stride=0x16,0x7530,0x7541}`; similar struct `0xD6C40` with
    self-pointer, count=4, stride=0x1E.
  - 32-bit pointers into `0xD2000..0xD2F32` from `0xCA7AC..0xCBA30`;
    `0xC79A8→0xD2F32`, `0xC7A34→0xD2FAC`, `0xC7AC0→0xD3050`.
- Glyph source is ROM-direct (no glyph bytes in IWRAM; EWRAM `0x11A0` is
  a per-frame render buffer, absent from ROM).
- **RESOLVED — code-indexed glyph store, not a strip.** Each of the 685
  glyphs (indices 0x000–0x2AC) appears exactly once in ROM (verified by
  byte-search for several glyphs). The store at `0xD3144` is
  **685 glyphs × 22 bytes = 15,070 bytes, ending at `0xD6C22`**, exactly
  where the descriptor struct begins. Glyph order is roughly
  first-use order of the story text (index 14–19 = だか私らが, matching
  the frame-0900 line), so it is not a standard kana ordering.
- **Narration text stream: ROM `0xCFF84`..`0xD1F96`, 63 messages**,
  delimited by `0x7FFF`. Each message is a stream of 16-bit glyph
  indices interleaved with control words:
  - `0x7534 <param>` — parameterized command (e.g. `0x7534 0x003C` =
    60 = delay/speed; `0x7534 0x000A` also seen).
  - `0x7530`, `0x7531`, `0x7532` — one-word commands (probably
    position/clear/pause).
  - `0x7FFF` — end of message.
  - Live EWRAM buffer (frame 1800 @ `0xA568`) shows a runtime control
    word `0x412` inside a glyph run — the interpreter may transform
    commands; not fully classified yet.
- Referenced from event-table field at ROM `0xC8E48` → `0x0CFF84`.
- Confirmed glyph indices in the story script reference the store
  directly (index == position in the store), e.g. first run
  `0E 0F 10 11 12 13 14 15 16 17 18` = だか私らが使うた(い)… — matches
  the frame-0900 line and its continuation (text types on progressively;
  frame 0900 shows only first 6 of 11 glyphs).
- `0xD30F4..0xD3143` is **not** a dictionary: it is the **monster status
  word list** — 13 entries of `{c1[,c2,c3], 0x7FFF}` (生命, 耐久, 攻撃,
  防御, 行動, 知識, 必殺技, 反撃, 索敵, 従順, 命中, 回避, 技能; codes
  0x2A1–0x2AC identified from renders). See the M10 audit section.
  (Superseded 2026-10-19.)
- **No Latin letters or digits exist in the 685-glyph store** (spot-check
  of indices 0–21, 480–495, 664–684 shows only kana/kanji/punctuation).
  English story text will need **new glyphs**: the store is full (ends
  exactly at the descriptor struct), so it must be relocated to free
  space and the single pointer at `0xD6C2C` (+ count/stride fields in
  the same struct) rewritten. Stride is fixed at 22 bytes (16×11 px);
  an English letter must fit that box.

### Story script control codes — CLASSIFIED (2026-10-17)

Control words are `>= 0x1000` in the 16-bit token stream. Confirmed
against in-game frames where noted:

| code | params | meaning |
|------|--------|---------|
| `0x7530` | 0 | line break inside the current box (2 lines max visible) |
| `0x7531` | 0 | clear box / start next screen |
| `0x7532` | 0 | screen break (new page; box cleared) |
| `0x7533` | 0 | scene-caption separator (used after `～場所～` banners) |
| `0x7534` | 1 | wait/pause; param = frames-ish (1,2,3,4,5,6,8,10,20,26,30,50,60 seen; 31×) |
| `0x7535` | 2 | styled block open: `<style> <delay>`, closed by `0x7536`. Style 001 = white/default (19×; style is always 001 so far). Content between params and `0x7536` is displayed (e.g. カノン, イグニス, `・・・`). Delay param values: 1,2,4,5,8,10,`0xFFFE`,`0xFFFF`; never displays (verified in-game, msg 6). |
| `0x753B` | 1 | styled block open, closed by `0x753C` (38×, paired 1:1). Param is **always `0x2`** = **red text** (verified in-game: 伝説の魔獣使い red in frame 8700). Highlights key nouns: 魔術使い(5) 私(8) 伝説の魔獣使い(9,12) 男(10) 火口(10) イグニス(11) 復讐(12) ベリンガム様(16) … |
| `0x7537` | 1 | param command (12×; params 0,1,2,4,0x10,0x11,0x14,0x19–0x1C,0x1F,0x32 — semantics TBD; never displays) |
| `0x7538` | **2** | param command (5×). **Fixed 2026-10-18**: 2 params, not 1 — msg 22 desync fix, display-verified in-game (both consumed, prints nothing, frame 19400). Params are consecutive ID pairs: `0031 0030`, `0007 0008`, `000E 000F`, `0012 0013`, `001D 001E` (msgs 22, 28, 35, 44, 55) — likely two related page/event IDs. |
| `0x7539` | 2 | rare (4×, msgs 32/46; params are consecutive pairs 0xB–0xE, 0x15–0x18 — semantics TBD, pass-through) |
| `0x753E` | 1 | param command (10×, msgs 31/32/46; params 0–5,8 — **beast-name inserts** inside red spans; the name comes from the beast table. EN **keeps the control** (names stay dynamic); sentences are worded so the slot reads naturally.) |
| `0x753F` | 1 | word insert (1×, msg 21): prints the canned word ご子息 "son" mid-line — verified in-game, frame 19200. EN drops the control and carries the word as plain text. |
| `0x7540` | 0 | player-name variable insert (30×). Occurs inside red blocks (msg 16: `「[753B][7540][753C]だった！」`) and mid-sentence (`追っ手達が[7540]に手をかけようとした`). Keep verbatim in translation. |
| `0x7FFF` | 0 | end of message |
| `0xFFFE`/`0xFFFF` | 0/1 | in-block sentinels/params (msg 2/3 use `7535 0001 FFFF`; 60/62 use `FFFE` + glyphs) |

Display limits (measured in-game): glyph advance 12 px, line height
13 px; the box fits **17 glyphs per line, 2 lines**; text auto-wraps
mid-word (msg 4 line 1 = 17 glyphs exactly, "…征服しよ" then "うと、").
`0x7530` starts a new line. **M5 OAM measurement (frames 20300–21300)**:
rows are 16×16 OBJ sprites at 12 px advance, y=124/137 (row pitch 13 px),
one page = 2 rows, and a ▼ cursor sprite sits at x=209 on the last row;
msg 25 JP = 5 display pages (S1 16+7 then 31→17+14; S2 8+12 then
27→17+10; S3 19→17+2) — the 17-glyph wrap holds in the box itself.
Verified in a live playthrough 2026-10-18 (`/tmp/opencode/story_run`,
frames cited):

- A third line does **not** fit; when a further line arrives after a
  full box, the box **clears and continues** (pages), each page ≤2 lines
  (msg 15 screen 1 = 2+1 lines; frames 13800–14000). "A third line is
  impossible" was wrong — it pages instead.
- `0x7533` caption (`～…～`) shows alone in the box, then the box clears
  for the narration (msg 10; frames 10400–10700).
- `0x7540` renders the player name **inside** the red span in msg 16
  screen 2 (frames 15600–16100).
- **msg 24 clears between its two lines** (frames 19900–20100): the
  17-glyph first line (`城主は、貴族の一人ウィンスロー二世`) overflowed
  the box (JP glyph widths vary), the box cleared, and line 2
  (`事件は…`) typed from the top row — that message is **2 JP display
  pages**, not one 2-line box. Do not assume a 7530 pair always fits.
- The player's name is entered in a naming UI **between msgs 15 and 16**
  (8×8-font screens: なまえ / monster-select list / はい・いいえ;
  default captured: レオ). Those UI strings are a separate milestone.
- Auto-wrap: msg 13 screen 3's single 33-glyph segment wraps at 17 in
  game (そのとき男は足元の地中深くから、何／かがうごめく…).
- **EN box budget (M5)**: EN rows are limited to 30 chars (29 working
  limit); the exporter's page budget is **≤6 rows (3 pages) per screen**
  (was 4) — EN at 30 chars/row carries ~1.75× a JP row (17 glyphs), so
  information-dense narration legitimately takes one page more than JP
  (msgs 25 s1/s2, 31 s3). More than 3 pages is still flagged for
  restructuring.

### Story script readings (verified against renders + live frames)

Messages 0–62 **fully verified** (2026-10-17/18): every glyph zips
against its token stream in `tools/build_charmap_story.py` `READINGS` —
429 glyphs mapped, zero length mismatches, zero char conflicts.
Notation: `／` = box line break, `[wN]` = 0x7534 wait, `[SCR]` = 0x7532
screen break, `[CLR]` = 0x7531 clear, `[W]…[/W]` = 7535/7536 white block,
`[RED]…[/RED]` = 753B/753C red block, `[名]` = 0x7540 name insert,
`[753F n]` = word insert (prints a canned word), `[BE nn]` = 0x753E
beast-name insert (name from the beast table).

- **0** — 神のいない世界に、繁栄などは無い [w60][CLR] だから私が使わされた。 [w60]
- **1** — 暗黒の時代 [w60][CLR] グランデート大陸は常に／人類の危機と共に存在していた。 [w10][SCR] 永遠の命を持つといわれた、／巨大な２匹のハイドラゴンが [w10][SCR] 大陸の権力を、掌握していた [w20]
- **2** — 空を支配していた、天空の[W]カノン[/W] [w50]
- **3** — 地上を支配していた、大地の[W]イグニス[/W] [w50]
- **4** — ２匹は互いに対峙し、[w1] 大陸を征服しようと、[SCR][w2] 血塗られた戦争をくり広げていた。 [w20]
- **5** — 長き戦いの末、／この大陸全ての生命と、[SCR] 繁栄が消え去ろうとしたとき[W]・・・[/W][SCR] 見たことも無い二匹の魔獣を／引き連れた、一人の[RED]魔術使い[/RED]が現れ、[w20][SCR] ２匹に戦いを挑んだ！ [w30]
- **6** — 長く壮絶な戦いが繰り広げられ[W]・・・[/W] [w30]
- **7** — 天空のカノンは敗れ、／傷を負った大地のイグニスは、[w10][SCR] ファムファンタル火山の地下深く、／姿を隠したのであった。 [w20][SCR]
- **8** — その勝利は、二匹の魔獣の命と、／引き換えに勝ち取った。 [w20][SCR] そして魔獣使い自身もまた、／力尽きようとしていた。 [w20][SCR] その時、この魔獣使いを救える技術を持つ者は[RED]私[/RED]以外、[w4][SCR] この世界には [w1] 居なかった。 [w30]
- **9** — その後この魔獣使いと、二匹の魔獣は[SCR][RED]伝説の魔獣使い[/RED]／[w1]として人々に伝えられた。 [w20][SCR] そしてグランデート大陸は、／人類が支配者となった。 [w30]
- **10** — ～ファムファンタル火山～[7533] その[RED]男[/RED]は、いまだ盛んに噴煙を上げる、[RED]火口[/RED]にいた。
- **11** — 火口には[RED]イグニス[/RED]を祭ったと思われる、廃墟が残っていた。[SCR] 男「どうした！大地のイグニスよ！」
- **12** — 男「このタクトを見て思い出さないのか？」[SCR] 男「おまえを世界から追いやった／[RED]伝説の魔獣使い[/RED]のタクトだ！」[SCR] 男「今再びよみがえりヤツに、／いやこの世界に[SCR] 共に、[RED]復讐[/RED]しようではないか！！」
- **13** — 男「[W]・・・[/W]」[SCR] 男「これだけではまだ弱いか！[w8]／やはりヤツを[W]・・・[/W]」[SCR] そのとき男は足元の地中深くから、何かがうごめく／のを感じとっていた。
- **14** — ～廃墟～[7533] 朝もやの中、人里離れた廃墟から、／男達の声が聞こえた！[SCR] 追っ手１「見つけ出すぞ！」[SCR] 追っ手２「逃がすな！！」
- **15** — それは、バルロア王国配下の／衛兵達であった。／追っ手３「もう逃がさんぞ！」[SCR] 追っ手２／「えーと[W]・・・[/W][w26] こいつの名前は？」
- **16** — 追っ手３「あ、そうだ！」[SCR] 追っ手１／「[RED][名][/RED]だった！」[SCR] 追っ手２「かくごしろ！／[名]！」[SCR] おまえを捕まえて[RED]ベリンガム様[/RED]に／渡せば謝礼がたんまりと[W]・・・[/W]」[SCR] そういって追っ手達が[名]に手をかけようとしたその時！
- **17** — 背後から魔獣達が／突然、追っ手達におそいかかった！
- **18** — 追っ手達「うわあ！！」[SCR] [名]は唖然として、／事の成り行きを見ていた。
- **19** — 追っ手達はあっというまに倒された [SCR] [W]すると、となりの部屋から／一人の老人が現れた。[/W]
- **20** — 老人「やかましいのう！[w6]わしゃ／寝起きは機嫌がわるいんじゃ！」 (7537 0002 before the card; 7534 0006 = [w6])
- **21** — その老人はクリムトと名乗った。[7533] クリムト「いや、助けたのはベリンガムと言う名を聞いてな。／やつとは少々ワケありでの[W]・・・[/W][SCR] うーん、そなたはヴァンダム城の／ウィンスローの[753F 0001]とみたが・・[SCR] 城でなにかあったかの？」
- **22** — [7538 0031 0030][名]は昨日に起こった／[RED]事件[/RED]をクリムトに語り始めた。
- **23** — ～バルロア王国、ヴァンダム城～[7531]
- **24** — [7537 0032]城主は、貴族の一人ウィンスロー二世／事件は小雨の降る朝に、突然起こった。
- **25** — 法王直属の[RED]魔獣騎士団[/RED]が城に乱入！／城を占拠した。／首謀者は、法王の軍事顧問として仕えてきた[7537 0004][RED]ベリンガム・ロー公爵[/RED]。[SCR] 彼は[RED]魔獣騎士団[/RED]の／最高司令官でもある男だ。／彼は城占拠の理由を、王国に対立する組織へ協力した疑い！[SCR] と、示したがまったくの濡れ衣であった。
- **26** — 捜索の邪魔をするものは、容赦なく捕らえられ、[SCR] その混乱の中[名]が見たものは、[SCR] 自分の目前ですでに息絶えている、／父ウィンスローの姿であった。
- **27** — そこには、見覚えの無い魔獣使いのタクトを手にしている[SCR] ベリンガムの姿があった。
- **28** — [7538 0007 0008]クリムト「[W]・・・[/W]」[SCR] クリムト「伝説の魔獣使いのタクトが目的か？／いや・・・なんでもない。[SCR] それよりおぬし・・・／父や家族の仇をとるつもりか？[SCR] 何も言わんでも／その目が語っとるわい！」
- **29** — そう言うと、クリムトは自分のタクトを[名]に手渡した。
- **30** — クリムト「わしの魔獣達をおぬしにあずけよう。[SCR] しばらくこの廃墟をねぐらにして／訓練するがよいぞ！」
- **31** — クリムト「よいか、ベリンガム達と戦うには、[SCR] この魔獣達では力不足じゃ！[SCR] そこで[RED]伝説の魔獣使い[/RED]がつれていた[RED]伝説の魔獣[/RED][SCR] [RED][BE 08][/RED]を作るんじゃ！」
- **32** — クリムト「ワシはその研究しておった。[SCR] まだ一部しか／解っておらんがの・・・」[SCR] [7539 000B 000C][7539 000D 000D]クリムト「ワシの調べでは、最初は[SCR] [RED][BE 00][/RED]と／[RED][BE 01][/RED]を合成すると、[SCR] [RED][BE 08][/RED]の幼体[RED][BE 02][/RED]が出来るはずじゃ！」
- **33** — クリムト「わしは再びその後の魔獣の作り方を調べる！」／クリムト「後はまかせたぞ！」／
- **34** — そう言い残してクリムトは／何処かへ旅立って行った。[SCR] その後ろ姿を見て／[名]は思った。[SCR]
- **35** — [7538 000E 000F]クリムト老人は、こうなる事を知っていたのではないだろうかと・・・／
- **36** — ゴゴゴゴゴ！[SCR] [名]が祭壇のある部屋に入った時、／大きく城がゆれはじめた。[SCR] [名]「地震？」
- **37** — 地震に気をとられていた[名]の目前に、[SCR] 見たことも無い大男が立っていた。[SCR] 彼は[名]をにらみつけながら近づいてきた。
- **38** — ベリンガム「わかるかね！この地震はイグニスが[RED]君[/RED]に気づきはじめて、／地下で暴れているのだよ！」[SCR] 声のする方向には／ベリンガムの姿があった。
- **39** — [名]は[7537 0011]ベリンガムに向けて、[SCR] タクトを振りかざそうとしたその時[SCR] クリムト「気をつけろ！ヤツの作った魔獣[RED]ザーゴ[/RED]に狙われておるぞ！」[SCR] [7537 0010]いつのまにか／背後にクリムトの姿があった。[SCR] クリムト／「よくここまで来れたのう。」
- **40** — ベリンガム「[W]フフフ・・・[/W]やはり[7534 0003]クリムトが裏に付いていたか！／だがすでに遅いな！」[SCR] その時、再び地面が／激しくゆれ始めた！
- **41** — ベリンガム「[名]の存在に気が付いたイグニスが、[SCR] 再び復活しようとしておる！[SCR] ザーゴ！[7534 0005] あとは任せるゾ！[SCR] わしはファムファンタル火山へ行き、[SCR] [RED][名]君[/RED]の古い友人に会ってくるよ。」[SCR] そういい残し、ベリンガムは部屋を出て行った。[SCR] そして、ザーゴはゆっくりと[名]に近づいてきた[W]・・・[/W]
- **42** — ザーゴ「グウウウウッ！」[SCR] ザーゴが唸り声を上げ、／ヒザをついて倒れこんだ！
- **43** — その時、上空からベリンガムのもう一人の魔獣[RED]ラミレス[/RED]が現れた！
- **44** — ラミレスはザーゴの前に立ち、／[名]に告げた！／[7537 0014] ラミレス「自分・・・事・・・しりたいか・・・？」[SCR] [7538 0012 0013] ならば・・・ファムファンタル火山に行け・・・」[SCR] そう言い残してザーゴを抱え込み／飛び立っていった
- **45** — クリムト「これも運命かの・・・／こうなったら行くしかないぞ。[SCR] ファムファンタル火山へ・・・！[SCR] そこでおぬしの全てが解るはずじゃ！」[SCR]
- **46** — [7539 0015 0016][7539 0017 0018]クリムト「よいか、それまでに[SCR] 伝説の魔獣[RED][BE 08][/RED]の中型体を／完成させるのじゃ！[SCR] 次は[RED][BE 03][/RED]と[SCR] [RED][BE 04][/RED]を合成する。[SCR] さすれば、[RED][BE 08][/RED]の[SCR] 中型体[RED][BE 05][/RED]が／完成するはずじゃ！」
- **47** — クリムト「ワシはまた、伝説の魔獣の事をしらべに旅に出る。／火山までの道のりは／至難を極めるぞ！！」[SCR] そういい残し、／クリムトは去って行った。
- **48** — [名]がファムファンタル火山を登り始めてから[SCR] 数え切れないほどの地震が起きていた。[SCR] [名]は感じた。[SCR] この揺れは[RED]イグニス[/RED]が／地底で暴れている
- **49** — と突然、ベリンガムの魔獣／[RED]ザーゴ[/RED][7537 001A]と[RED]ラミレス[/RED][7537 0019]が現れた。[SCR] ザーゴ「もっと・・・戦え！」[SCR] ラミレス「たくさん・・・戦えば、／イグニス・・・怒る！」[SCR] [名]は体の中から[RED]狂暴な力[/RED]がみなぎるのを感じていた[W]・・・[/W]
- **50** — ファムファンタル火山の火口に着くと、[SCR] そこには朽ち果てた神殿跡があった。[SCR] [7537 001B] ベリンガム「ここは大地のイグニスを祭った祭壇だよ。[SCR] 待っていたよ。[SCR] もっともワシ以上にイグニスは／君を待っていたはず・・・[SCR] さあ！[w1] 復活を盛大に／祝おうではないか！！」[SCR] するとベリンガムの背後から魔獣達が現れた。／[7537 001C] クリムト「ムッ！遅かったか。[SCR] いかんココで戦っては！」[SCR] しかし、遅れてきたクリムトの声は届かなかった・・・
- **51** — ベリンガムの魔獣を倒したその時、大きく大地がゆれ[SCR] [名]達の足元が崩れ出した。
- **52** — そして地中深くより／巨大なドラゴンが現れた。
- **53** — そのドラゴンは、まるでマグマのように赤い体をし、／巨大なクチからは、嵐のような息使いが聞こえていた。
- **54** — ベリンガム「ハハッ！！[w8]／待っていたぞ、この瞬間を。[SCR] [RED]大地のイグニス[/RED]の完全復活だ！」
- **55** — [7538 001D 001E] ベリンガム「おまえ達は例の古城跡で合獣機の準備をしろ！[SCR] ワシは二人の再会を見てから行く。[SCR] イグニスと[RED]天空のカノン[/RED]と[RED]伝説の魔獣使い[/RED]が[SCR] 合成して出来た[RED][名][/RED]君とのな・・・」／[名]は息をのんだ。
- **56** — クリムト「今の我々の力では／イグニスを倒す事は不可能じゃ！[SCR] ここはひとまず逃げるぞ！！」[SCR] しかしその時、／[名]の中で[SCR] 何かが目覚めていた[W]・・・[/W]
- **57** — クリムト「どうした！？」[SCR] [名]「フフフッ！」[SCR] [名]／「久しぶりだな[W]・・・[/W]」[SCR] [名]の表情は[SCR] 明らかにいつもと違う人格へと変貌していた。
- **58** — [名]／「数百年にもわたる戦いの／決着を今ここでつけてやる！」[SCR] クリムトは[名]の背後に写るカノンの姿を見た。
- **59** — 大地のイグニスがおたけびを上げ／地面に体を横たえた。[SCR] ベリンガム「なんと言うことだ！／イグニスがやぶれるとは！！」
- **60** — ベリンガム／「[W]いかん、このままでは！！[/W]」[SCR] ベリンガムの手から発せられた不思議な光の帯が、[SCR] イグニスの体を包み込むと、／その巨体が宙に浮かんだ。
- **61** — 光に包まれたイグニスとベリンガムは、空の彼方へ飛んでいった。
- **62** — ベリンガム「[W]なんということだ！[/W]」[SCR] カノンと魔獣使いが合成した／[名]は、[SCR] これほどの強さを[W]・・・[/W]

#### Late story bank L0–L32 (0xD1F96..0xD30F4) — the game's ending

Found by the M10 completeness audit (see "Complete text inventory &
completeness audit" below). Readings are glyph-only; insert positions
(«P» player name, «Wn» word-table, «BEn» beast-name) are visible in
the decoded text of `build/late_story_raw.json`. Zip-verified against
`READINGS_LATE` in `tools/build_charmap_story.py`, zero mismatches.

- **L0** — 「ハアハア！」イグニスが去った後、我に返ったはその場に倒れこんだ。クリムト「おぬし・・・そうか！何かをきっかけとして、カノンの魂が目覚めるのか！」クリムト「もう話さねばなるまい。全ての事を・・・」クリムト「ベリンガムが言っていた事は事実じゃ！ワシがカノンと魔獣使いを合成し、おぬしが生まれた。」
- **L1** — クリムト「そもそもワシがこの世界に合獣機というものを作り出したんじゃ。」クリムト「二匹のドラゴンが支配し狂暴な魔獣達が、支配していたこの世界に、人間的な秩序を持った魔獣人間を作ろうとしたんじゃ」
- **L2** — クリムト「ワシが初めて作った魔獣人間、それがベリンガムじゃ。」クリムト「合成した魔獣は、強い遺伝に影響される。複数の魔獣達と合成を繰り返したが、ヤツは暗黒系の遺伝子をより強く受け継いでしまった。姿は人間だが心は狂暴な魔獣達と変わらないヤツだ。」
- **L3** — クリムト「結局、ワシの理想はムズカシイと感じ始めた時、が現れた。」クリムト「は２匹のドラゴンと壮絶な戦いをし、が勝利したが、もまた全身に瀕死の重傷をおい、もはや命を助けるには合獣機を使う方法しか残されていなかった。」
- **L4** — クリムト「わしは生命力の強いカノンと、を合成したんじゃ！」
- **L5** — クリムト「そして、の遺伝子を強く受け継いだ、魔獣人間のおぬしが産まれた。」しかし、いっさいの記憶を失ってな。その後、おぬしはバルロア国の貴族、ウィンスロー一世の子供だと判った。つまり死んだおぬしの父、ウィンスロー二世はそなたの弟だ！彼は事実を知り、記憶の無いおぬしを本当の子のように育ててくれたんじゃよ。」父では無く自分の弟だったウィンスロー二世・・・は動揺する自分を抑えることで精一杯であった。
- **L6** — クリムト「ベリンガムはこの事実を知ってイグニスをおびき出すために、おぬしを利用したんじゃ」
- **L7** — クリムト「ヤツは古城跡に向かっているはずじゃ。あそこには昔、おぬしを合成した合獣機がある。ヤツはおぬしになろうとしておる。」
- **L8** — クリムト「おぬしとイグニスの因果関係は永遠。逃れることは出来ん！伝説の魔獣を復活し、ヤツらを倒すのじゃ！」
- **L9** — クリムト「いいか！これで伝説の魔獣が完成する。中型体のとを合成するんじゃ！
- **L10** — クリムト「さすれば伝説の魔獣の完成じゃ！この魔獣を使えるのは、そなただけだ。古城跡へ向かい、ベリンガムの野望を阻止するんじゃ！」
- **L11** — が中庭まで来ると、突然目の前にザーゴとラミレスが現れた。ザーゴ「今度は・・・本気！」ラミレス「もう容赦・・・しない！」
- **L12** — ベリンガムの所へザーゴとラミレスが、逃げ帰って来た。ベリンガム「情けないやつらだ。おまえ達、この中へ入れ！」
- **L13** — ベリンガム「おのれ、所詮ザコ同士の合成では、この程度の強さかっ！」ベリンガム「ならばさらなる力をあたえるために、ワシ自身と・・・」そう言うと、ベリンガムみずから合獣機の中に入った。
- **L14** — ベリンガム「お・・・おのれこれ・・・で、ワシが・・・
- **L15** — 最強・・・」その先には、すでにイグニスが合獣機の中に入れられていた。ベリンガムは体を引きずりながら、合獣機の中に入った。
- **L16** — 合獣機が火を噴き、その炎はまたたくまに古城全体を包んだ！
- **L17** — 部屋中が炎に包まれてもは逃げ出さず、死んだベリンガムの姿をみつめていた。
- **L18** — は思い出していた。ベリンガムが城に攻めて来た時の事を。
- **L19** — ウィンスロー「これが目的だったのか！」ウィンスロー王が伝説の魔獣使いのタクトをベリンガムの前に差し出した時！タクトを見たの心がカノンの魂に支配され
- **L20** — 伝説の魔獣使いに恨みを持つカノンが、弟であるウィンスロー王に何をしたのか・・・
- **L21** — の手から魔獣使いのタクトが落ちた。
- **L22** — 「が殺した・・・」炎が部屋中に広がり、の姿も炎に包まれた。
- **L23** — 古城全体が煙に包まれ、外壁が崩れた。
- **L24** — クリムト「古い合獣機をムリに動かした結果じゃ！」クリムト「は・・・？」
- **L25** — その時、炎に包まれていた城が崩れ落ちた。
- **L26** — クリムトはその崩れた残骸の中、を探し歩いた。そして、火に焼かれ黒くなったタクトを見つけ出した。クリムトはそのタクトを見て確信した。
- **L27** — クリムト「そうか・・・全て知った上での、決断か・・・」クリムト「何処かで生き延びているじゃろ！」
- **L28** — そう自分に言い聞かせるよう、黒くなったタクトを見つめていた。
- **L29** — ～スタッフロール～❋The End❋
- **L30** — は立ち止まり、考えた。クリムト老人が言った、伝説の魔獣無しで、戦えるだろうかと？そう考え、はその場を立ち去った。
- **L31** — は立ち止まり、考えた。この先にはベリンガム達が、待ち構えている。伝説の魔獣の完成無しで、はたして勝てるのだろうか？魔獣を完成させるためはその場を離れた。
- **L32** — は立ち止まり、考えた。この先にはベリンガム達が、待ち構えている。伝説の魔獣の完成無しではたして勝てるのだろうか？魔獣を完成させるため、はその場を離れた。

Scene map: L0–L12 = the opening/back-story and fusion-tutorial scenes
(incl. the God-less opening, the war back-story and the fusion recipes),
L13–L32 = the finale (Vandam Castle attack, the volcano, the awakening,
the ending and the staff roll).

Names/terms found so far: グランデート大陸 (Grandeート continent),
カノン (Canon — sky dragon), イグニス (Ignis — earth dragon),
ハイドラゴン (hydra dragon), クリムト (Kurimuto — old beast tamer),
ベリンガム (Beringham — lord), バルロア王国 (Kingdom of Barroa),
ファムファンタル火山 (Famfantar volcano), ザーゴ (Zargo — man-made
beast), タクト (tact/baton — beast-tamer tool), 魔獣使い (beast tamer),
追っ手 (pursuers), 廃墟 (ruins), ウィンスロー (Winslow — lord of
Vandam Castle; 二世 = "II"), ヴァンダム城 (Vandam Castle — msg 23
caption), 事件 (the incident — msg 22, red span). The player character's
name is inserted via `0x7540`. Partial decode pass over msgs 25–62 adds:
魔獣騎士団 (the Pope's Beast Knight Order), 法王 (the Pope), and
Beringham's full name ベリンガム・ロー公爵 = "Duke Beringham Roe"
(msgs 25+; ロー = Roe provisional — **FLAG**). Also 軍事顧問 (military
advisor), 最高司令官 (supreme commander), 首謀者 (mastermind), 濡れ衣
(frame-up), 幼体 (young form — see msg 32), 合成 (combine). Beringham's
second beast ラミレス = **Ramires** (msgs 43–44; glyphs fully read — ミ/レ
bound in M7 — and matching the 8×8 name list; **FLAG** provisional like
Zargo). M6 addenda: ザーゴ = "Zargo"
(msg 39 red span; same name in the 8×8 scripts — one spelling across
subsystems; **FLAG** provisional), 祭壇 (altar — msg 36), 地震
(earthquake — msgs 36–38), 大男 (giant — msg 37), 裏に付く (side with —
msg 40), plus SFX ゴゴゴゴゴ (rumble) / フフフ (laugh). M7 addenda:
復活 (revive — msg 41), 存在 (presence — msg 41), 告げる (tell —
msg 44), 唸り声 (growl — msg 42), 道のり / 至難を極める (the road / be
the hardest yet — msg 47), 登る / 数え切れない / 地底 (climb / countless /
underground — msg 48). M8 addenda: 合獣機 (beast combining machine —
msg 55), 例の古城跡 (the old castle ruins — msg 55), 我々 (we — msg 56),
瞬間 (moment — msg 54), 祝う (celebrate — msg 50), 届く (reach, of a
voice — msg 50), 崩れる (crumble — msg 51), マグマ (magma — msg 53),
息をのむ (hold one's breath — msg 55), 狂暴な力 / みなぎる (violent power /
surge — msg 49), 大地のイグニス (Ignis of the Earth — msg 54). M9
addenda: 久しぶり (long time no see — msg 57), 表情 / 人格 / 変貌
(expression / personality / transform — msg 57), 数百年 (centuries —
msg 58), 決着 (settle — msg 58), 写る (be reflected — msg 58), おたけび
(roar — msg 59), 横たえる (lay down — msg 59), やぶれる (be defeated —
msg 59), 発する (emit — msg 60), 光の帯 (band of light — msg 60), 包む
(wrap — msg 60), 宙に浮かぶ (float in the air — msg 60), 彼方 (far
beyond — msg 61), 強さ (strength — msg 62).

### Complete text inventory & completeness audit (M10, 2026-10-18/19)

The user asked how the 32 late messages were missed and whether any other
game text was missed. Findings:

**The large-glyph text region is now fully enumerated.**

| region | what | status |
|--------|------|--------|
| `0xCFF84..0xD1F96` | 63 story messages | read + translated (M1-M9) |
| `0xD1F96..0xD30F4` | 33 late messages (the ending) | read; translation = M11 |
| `0xD30F4..0xD3144` | monster status word list (13 entries) | read; translation = M11 |
| `0xCF52C..0xCFB82` | R1 support region (37 segments) | extracted; see below |

**Root causes of the missed messages**

1. The first extraction stopped at `0xD1F96` — the 63-message bank read
   exactly to there — but the token stream continues for another 4,446
   bytes (`0xD1F96..0xD30F4`, exactly 33 messages, 33 `0x7FFF`
   terminators).
2. The ad-hoc re-extraction that found the continuation kept only 32 of 33
   messages because it had no count/offset verification and silently
   dropped `0xD2CCA` (44 tokens). That message IS referenced from the
   scene table at `0xCB6FC`, so it displays in game.
3. R1 was never inventoried: earlier work examined only
   event-table-referenced message streams, not the story-system support
   region.

**Verification now built in** (all committed):

- `tools/extract_late_bank.py` — segments `0xD1F96..0xD30F4`; asserts the
  count (33), the expected-start list, and the region end.
- `tools/build_charmap_story.py` — zips **both** banks glyph-by-glyph
  against `READINGS` / `READINGS_LATE` plus the hand-verified `EXTRAS`;
  649/685 glyphs mapped, zero mismatches/conflicts.
- `tools/extract_r1.py` — R1 segments, the `753E`/`753F` tables, the
  name-input charset, and a whole-ROM pointer census for the region.

**Pointer census (whole ROM, 2-aligned u32)**

- All 63 story-bank starts are referenced from scene/event tables
  (`0xC8xxx`/`0xCAxxx`).
- Late bank: all 33 starts are referenced (scene tables
  `0xCA6F8..0xCBA30`, plus `0xC79A8`/`0xC7A34`/`0xC7AC0` for the last
  three) except `0xD2F08`, which is a chained continuation the engine
  advances into.
- No real mid-message pointers exist in either bank: odd-offset hits are
  byte-overlap artifacts, and the handful of even-offset hits inside the
  bank window match chance for that window size.

**R1 support region (`0xCF52C..0xCFB82`) — display status**

DISPLAYED content (referenced):

- the two insert tables (below), used inside story messages via `753E` /
  `753F`;
- renderer fragments `0xCF9A0` (`▼「」`), `0xCF9A8` (`、。`), `0xCF9AE`
  (`、。」{089}！～`), `0xCF9BC` (`「{08A}～`) — referenced from data tables
  at `0x80FD4`/`0x80FF0`/`0x8100C`/`0x8175C` (message renderer);
- debug prompts `0xCF9C4` / `0xCF9EC` (「BGチェック用／フェイスチェック用
  Aボタンで次へ進みます」) — referenced mid-string from `0x724324`,
  `0x7465C4`, `0x757AA0` (debug screens only);
- test scene `0xCF58C` (268 tokens, starts `テスト…`) — referenced from
  the event table at `0xC8D08`; contains real fusion dialogue (variants of
  msg 46 and the L9/L10 recipes) plus test lines
  (`彼は１２３４５をにらみつけながら…`).

NOT referenced (stale/leftover, not displayed):

- `0xCF52C` — a copy of the opening message with damaged leading tokens;
- `0xCF7A6` — digit strip + research-scene variant;
- `0xCF8C0` — ヴァンダム城 scene variant using 「ティーナ」 as the
  name placeholder;
- `0xCFA18` — `AB` fragment.

Correction: an earlier note listed `0x6EB2F4 -> 0xCF6F4` as a reference
into the test scene. The pointer scan shows the bytes around
`0x6EB2B2`/`0x6EB2F4` sit in a data region dense with pointer-shaped byte
patterns (one candidate is the invalid odd address `0xCF8F5`), so both are
coincidental artifacts, not references.

**Insert tables**

- `753E` beast-name table `0xC7410`: 18 strings = 9 slots x 2 genders
  (index = slot*2 + variant; 0 = male, 1 = female): ゴーレムライト /
  ゴブリンフライ, ホワイトドラゴン / ブラックドラゴン, リトルガウ /
  チンビュアリー, リトルガウ / チンビュアリー (dup), こあくま / ハイエルフ,
  メインガウ / リンビュアリー, メインガウ / リンビュアリー (dup),
  LV１５以上のミノドラゴン / LV１５以上のドラグリフォン,
  ヘビーガウ / **メインビュアリー** (earlier "ツインビュアリー" was a
  misread of メイン).
- `753F` word table `0xC73F0`: 8 strings = 4 slots x 2 (same indexing):
  僕 / 私, ご子息 / ご息女, 伝説の魔獣使い x2, 彼 / 彼女.

**Monster status word list (`0xD30F4..0xD3144`)** — 13 entries terminated
by `0x7FFF`: 生命 (HP), 耐久 (durability), 攻撃 (attack), 防御 (defense),
行動 (agility), 知識 (knowledge), 必殺技 (special technique), 反撃
(counter), 索敵 (recon), 従順 (obedience), 命中 (accuracy), 回避
(evasion), 技能 (skills). Codes `0x2A1-0x2AC` identified from renders.
This is the monster status screen's bigfont label list; translation = M11.

**Other regions re-checked and closed (no text)**

- `0xCC000..0xCC92C` mixed scenario/sequence id data (not text).
  **Correction (2026-10-19):** `0xCC92C..0xCDED4` is *not* id data — it
  is the **field-message string table** (the third text system, decoded
  below), and `0xCDED4..0xCF51E` is that system's 317-glyph font store.
  The font descriptor sits at `0xCF520` and its store pointer
  `0x080CDED4` is the u32 at `0xCF528`.
- All 8 single-term runs (`0x09C0BA`, `0x0A9C24`, `0x0A9F22`, `0x0F8FA2`,
  `0x21B266`, `0x2C9D78`, `0x2CA376`, `0x56F5BA`) = graphics/palette/tile
  data, not text.
- `0xCFF82` holds the `0x7FFF` after the 512-entry name-input charset
  (`0xCFB82..0xCFF82`); the story bank starts exactly at `0xCFF84`.

**Still outside the story pipeline** (not missed, but not yet mined):
graphics containing text (title screen, logos, name-input UI key cells
`0x0C6E00+`) — next extraction milestone. The 8×8 direct-code text is now
fully extracted — see "8×8 direct-code text corpus" below.

### 8×8 direct-code text corpus (M11, 2026-10-19) — EXTRACTED

The 8×8 subsystem (menus, battles, shops, monster/item databases, network
messages) is fully extracted. Window `0x099B40..0x0C6E00`; **1,215 rows**
in `build/8x8_corpus.tsv` (columns: `addr region style n suffix refs
sources text`; styles `term`/`len`/`slice`/`split`).

Tooling (both committed):

- `tools/extract_8x8.py` — pointer-driven extraction. Reference sources:
  - `refs` = every halfword-aligned u32 in the ROM pointing into the
    window (odd hits are byte-value coincidences and are dropped);
  - `lenmap` = `{ptr, u16 len, u16 b}` entries (`1 <= len <= 300`,
    `b <= 0xFF`) giving the **exact code length**;
  - `runs` = every `0x0000`-terminated 16-bit code run at 2-aligned
    offsets;
  - `walk_names` = first name-like run in the first 0x18 bytes of each
    monster-DB record (6 walks, 374 names);
  - plus the `MANUAL_STARTS`, `SPLITS`, `EXCLUDED` tables below.
- `tools/census_8x8.py` — pointer census → `build/8x8_ptrs.tsv`
  (**1,502 targets** with source offsets).
- `tools/render_glyph_sheet.py` — contact sheets for unresolved glyphs.

**Entry layouts.** Pool tables are `{u32 ptr, u16 f1, u16 f2}` with
`f1` = exact code length and `f2` = `b` (0 or small). The network message
table at `0x09D8C0` (77 entries) uses `f1` = **code number** (e.g. 10-000),
not a length. Item descriptions use `{ptr, len}` into the idesc pool.

**Regions (row counts).**

| region | rows | contents / notes |
|--------|-----:|------------------|
| `mobile` | 42 | tournament / Mobile Adapter GB UI at `0x099B64..0x099D72`: one *unterminated* run, split by declared fixed-width fields (`EXP`, `LV`, `しょうきん  0G`, `Lv51いじょうクラス      `) — slices from `MANUAL_STARTS`; fields are space-padded to fixed widths |
| `net` | 140 | network/system message bank `0x09D000..0x0A1108`: `CODE：10−000 …とりあつかいせつめいしょをごらんください。` errors, connection screens |
| `report` | 45 | post-battle / party-report messages from `0x0A12AC`: `がしゅぎょうからかえってきたよ。`, level-up / capture / release prompts (some are sentence fragments composed at runtime) |
| `shop` | 110 | shop + password + save messages `0x0A7000..0x0AA000` (`いらっしゃいませ！`, `CL BS OK` input labels); two data blocks excluded |
| `item` | 42 | item names: first 8 codes of each `0x40`-stride record at `0x0B5728` (letter/number fields follow inside the record) — **names are limited to 8 codes** |
| `idesc` | 42 | item descriptions via `{ptr,len}` at record `+0x38` into pool `0x0B720C..0x0B7A40` |
| `mdb1`–`mdb6` | 56/35/107/52/69/29 | monster database name fields (walks below); mdb1 stores each name at two consecutive records (56 rows = 28 unique × 2); mdb2 fragments (`メインガウ`, `ヘビーガウ`…) are legitimate fusion-name parts |
| `map` | 35 | map / start-location names from `0x0C5DAE`: `すたーとちてん`, `へいげん`, `へいげん2`, `おか`… (digit table at `0x0C5D9C` is data) |
| `battle` | 139 | battle message bank `0x0C6000..0x0C6E00` (incl. `タマゴ`, `レオ`, `ティーナ`) |
| `bbxxx` | 2 | name-input row keys: `SPC` (`0x0BCC2C`), `あ` (`0x0BCC44`) |
| `pool` | 270 | main label/message pool `0x0BD000..0x0BF000`: chapter labels, menu labels, the eight four-glyph monster names, name suggestions, system boxes, `COMPLETE`/`CLEAR`/`はい`/`いいえ`/`ON`/`OFF`… |

**Monster-DB walks** (start, end, stride): `(0x0AEDE8,0x0AFCDE,0x30)`,
`(0x0AFCDE,0x0B0B7C,0x34)`, `(0x0B0B7C,0x0B271C,0x34)`,
`(0x0B271C,0x0B3900,0x34)`, `(0x0B3900,0x0B4A00,0x34)`,
`(0x0B4A00,0x0B5728,0x34)`. Per-record constant field pairs
(`0x00E0/0x0180/0x01C0` + `0x0040/0x0080/0x00A0`, which decode as kana
like `ヴめ`/`百ケ`) are filtered out; unreferenced 2-code runs between
terminators are dropped unless they sit on a record start.

**Key tables.** `0x0BCA74` = 33 chapter/demo-select labels (13 entries are
`？` placeholders); `0x0BAA1C` = 13 status names + 13 descriptions;
`0x0BAB8C`/`0x0BABC4`/`0x0BABDC` = 18 four-code entries into `0x0BD4CC..`
(beast/type names, incl. the eight kanji names); `0x0BAE3C` = 6×12-byte
name-insert records `{ptr,len,id,handler}` ids `0x20–0x25` (what the story
`753E` command inserts); `0x0C7410` = bigfont-side beast pointer table.

**Split pool labels** (merged runs the game reads at fixed offsets — must
stay contiguous when relocated): `0x0BD3B6 [4,4,5]`, `0x0BD3EC [3,4]`,
`0x0BD46E [4,3,3]` (きしょう/いどう/ひこう), `0x0BD48A [1,5,4,7]`,
`0x0BD4AC [2,4]`, `0x0BDB52 [5,20,21]`, `0x0BDF04 [10,15]`,
`0x0BE264 [11,10]`, `0x0BE350 [18,11]`, `0x0BE3DA [8,4,18]`,
`0x0BE45A [24,20]`, `0x0BE4DE [9,14]`, `0x0BE53C [4,26]`,
`0x0BE922 [9,5]`, `0x0BE94A [5,4,4]`, `0x0BE9E4 [11,17,15,17]` (+ auto
remainder `モンスターリストはじゅんびちゅう。`).

**Excluded data zones** (inside the window, not text): `0x0A1108–0x0A12AC`
(font rows), `0x0A9740–0x0A9C34` (font chart), `0x0A95BC–0x0A9690`
(password-checksum blob), `0x0A8DE4–0x0A902A` (password-input ASCII/glyph
tables; contains debug strings `testl1`), `0x0A9EE0–0x0AA000` (shop
pointer/keyboard block), `0x0B7A40–0x0B8000` (kana composition table),
`0x0BAB60–0x0BAB8C` + `0x0BAC20–0x0BAC40` (script data),
`0x0BCB60–0x0BCC28` (glyph-code lists), `0x0C3000–0x0C5D9C`
(graphics/map data), `0x099D90–0x09D000` (Mobile tables),
`0x0C6E00–0x0C7400` (name-input keyboard cells).

**Code-baked strings (`MANUAL_STARTS`)**: mobile fixed-width fields
(`0x099BE8` クラス, `0x099C00`, `0x099C34/68/9C/D0`, `0x099CE2`,
`0x099D2A/34/3E`, `0x099D4A`, `0x099D4E/54/5C/68` NEW/LOAD/OPTION/START)
and the pool strings reached only via code-baked offsets: `0x0BD388`
`COMPLETE`; `0x0BD46E` split labels; `0x0BDD08`
`パーティがしゅぎょうにいっています` (composed with the preceding
`すべての` row at runtime); `0x0BE264` split labels.

**Audits.** Full-ROM kana coverage and a whole-window uncovered-span audit
(maximal code spans minus corpus coverage) were run; every remaining
uncovered text-like span is data (glyph-order table `0x0A1BCA..`, kana
input grid `0x0AB004..`, DB field values, `TET` font bitmap at
`0x0BEFB8`, small markers). The eight four-glyph monster names at
`0x0BD4E4..0x0BD52A` use codes `0x1A0–0x1BF`, the only unmapped glyphs
(32); contact sheets: `build/glyph_sheet_1A0_1BF.png` (grid) and
`build/glyph_names_1A0_1BF.png` (the eight names as words) — **user
reading pending**.

**Open items.** `0x0BE2A8` `しゅぎょうちゅうパーティせんたくにもどる`
kept as one slice (split `[8,12]` vs `[12,8]` undecidable); `0x0BECE6`
`？？AB` rejected (two `？` + index letters, not text); `みへんせい` =
未編成; a few mdb2 stray suffixes (`リン` etc.) are kept as fragments.

### Field message box — third text system ("message font") — SOLVED & EXTRACTED (2026-10-19)

The field message box ("ワールドマップへ切替えます") is **not** the 8×8
system and **not** the 16×11 story bigfont. It is a third, self-contained
text system with its own 9×9 font, its own code space (0–316), and its own
renderer.

**Font.** 317 glyphs × 18 bytes at `0x0CDED4` (`0xCDED4..0xCF51E`).
Glyph format: 8 B = rows 0–7, left 8 columns (MSB = leftmost); 8 B = the
9th column, bit 7 of each row byte; 1 B = row 8 left 8 columns; 1 B = row 8
column 8. That is a 9×9 1bpp mask laid out as three stacked blocks.
Descriptor at `0xCF520`:
`{u16 w=9, u16 h=9, u32 flags=0x40000000, u32 store=0x080CDED4, u32 4,
u32 stride=0x12, u32 0x7530, u32 0x7541, ...}`. The store pointer at file
offset `0xCF528` is the single handle for relocating/extending the font.

**Renderer** at `0x0EC38`: takes a u16 string pointer, draws into
`0x0203E800` (64 OBJ-sized tiles = the box's two 64×32 halves), glyph
advance 10 px, line 1 y=6, line 2 y=16, **auto-wraps after 11 glyphs**,
terminates on `0x7FFF`. The box itself is 4 OBJ 64×32 sprites (tiles
`0x000/0x020/0x040`, palette 14) at (76,16) and (140,16); EWRAM
`0x3E000` = border-only box, `0x3E800` = box with text. The 8×8 font
cannot draw text into this box; the message font's descriptor/renderer is
the only path.

**String table** `0x0CC92C..0x0CDED4`: 169 strings, each `0x7FFF`-
terminated, pure glyph codes 0–316 (no control codes), 2,603 glyphs total.
The table is referenced from code literal pools all over the ROM (e.g.
`0x3114 -> 0x080CCE48`, `0x38BC -> 0x080CCE74`); a whole-ROM scan found no
other message-font strings (the remaining `0x7FFF`-terminated runs are
story bigfont / R1 / data).

**Extraction (complete).**

- `build/msgfont_strings_raw.json` — 169 × `{start, codes}`.
- `data/msgfont_charmap.json` — **317/317 code→char mapped** (built by
  reading all 169 strings from rendered PNGs at S=4–8 and aligning
  code-by-code; every code appears in a readable context).
- `build/msgfont_strings.tsv` — `addr idx codes text`, all 169 decoded.

**Contents** (all UI/system text, translatable):

- battle orders and clear conditions: `命令を決めてください`,
  `指示の対象を決めてください`, `【クリア条件】…` (26 mission objectives,
  0xCCE88–0xCD3DA), `【命令：戦え／待機／排除／アイテム／逃げる／守れ／
  ボコれ】…`;
- network/battle states: `通信準備ができたらＡボタンを押してください`,
  `通信中です。Ｂボタンでキャンセルできます`, `通信エラーです。ケーブルを
  確認してください`, class/fee table `ＬＶ５１以上クラス　料金３００Ｇ`,
  `対戦成績　勝　負　引き分け`, `プレイヤーポイントが足りません`;
- field menu descriptions: `ワールドマップ／ブリーフィング／モンスター管理／
  パーティ編成／アイテム管理／システム処理へ切替えます`, `修行中の為、…`,
  `位置変更／パーティから外せます`, item/parameter help lines;
- save/load + sound/event config: `データをセーブしますか　はい　いいえ`,
  `音楽のＯＮ／ＯＦＦを設定します`, `効果音の…`;
- the 13 monster status labels (identical to the bigfont status list at
  `0xD30F4`): 生命 耐久 攻撃 防御 行動 知識 必殺技 反撃 索敵 従順 命中
  回避 技能.

**Reading notes / quirks.** The font is first-use ordered, so it contains
duplicate glyphs: 4/48 = ー, 49 = blank (space), 1/141 = ン, 59/76 = る,
82 = ボ / 88 = ポ (msg 15/79 renders ポコれ; likely ボコれ), 158/302 = 魔,
159/178/303 = 獣, 185 = グ, 186/221 = シ, 214/291 = へ, 68/206 = 除,
58/292 = 撃, 267 = 技 / 316 = 能. Two strings contain **source typos**:
msg 11/75 `排まえる` (should be 排除する) and msg 26/85 `あ加できない`
(should be あつかえない/扱えない). One reading is still uncertain:
code 166 (`砦` by shape; the word `砦備` in msg 47 is otherwise
unexplained — probably a source typo for 配備/砦塞) and code 168
(`塞`, word `城塞` in msgs 48/49).

**Translation implication (recorded now, decision later).** The message
font contains only a *subset* of Latin: A, B, F, G, L, V, N, O, digits
0–9, `【】！：／～` — no lowercase, no most uppercase, no `.`/`,`/`?`.
Translating the 169 strings in place would immediately run out of glyphs.
Options: (a) relocate the 317-glyph store to free space (`0x76765D`),
append Latin glyphs at 18 B each, update the descriptor's store pointer
(one u32 at `0xCF528`); (b) keep the store and draw message text with the
8×8 system instead (needs a different renderer path — the box uses OBJ
tiles, so probably not); (c) shorten/avoid. The 11-glyph wrap and 2-line
box also constrain English line length (11 chars/line × 2 lines per page;
the renderer does not page automatically beyond the 2 lines — the string
must be split manually). Decided in the translation pass, recorded here.

### Compression (T2)

- Text is plain 16-bit codes, uncompressed. No verified compressed asset.

## Strategy — APPROVED (2026-10-17)

User approved the hybrid strategy as proposed. Implementation has begun on a
copy; output will be a BPS patch. **Never edit `rom/monster-guardians.gba`.**

Round-trip validation (decode → re-encode → byte-compare, all 2,223 TEXT
strings):

- Prose (kana/latin/punctuation) round-trips exactly.
- 309 strings reference glyph codes not yet in the charmap — all UI/graphics
  (button icons `0x104–0x10F`, box-drawing `0x120–0x131`, placeholders
  `0x140+`, "squeezed" tiles `0x1A0+`). Handled case by case.
- 8 strings hit **duplicate glyphs** (the font draws some characters more
  than once: small vs. normal digits, two dakuten marks, filled vs. hollow
  arrows). `data/charmap.json` keeps the canonical code; the alias codes are
  recorded in `data/glyph_aliases.json` and preserved when re-inserting
  untouched strings.

Default **hybrid** strategy, adapted to findings:

1. **Short strings in place** (menus, item/skill names, short labels) where
   the English fits the existing 2-byte-per-glyph budget. Same code count
   or fewer → overwrite in place, pad with `0x0000`.
2. **Long text relocated** (dialogue, descriptions, network-error text) to
   the free block at `0x76765D`, rewriting the 32-bit pointer(s) that
   reference each string. Because the 8×8 font is fixed-width and English
   is longer in glyph count than Japanese, most prose will be relocated.
3. **Charmap**: `data/charmap.json`; keep the game's own 8×8 font. Latin
   lowercase/uppercase/digits already exist (`0x002–0x03F`), so English
   needs no new glyphs for v1. Punctuation exists at `0x0E1+` (plus a
   halfwidth-ish set); map English `.,!?'"()-` to the closest glyphs.
4. **Line breaks**: encoded as `0x1FF`. Translation tooling must wrap
   English lines at the measured text-box width and emit `0x1FF`.
5. **No font expansion** for v1; revisit only if needed.
6. Output a **BPS patch** against the user's ROM (never ship the ROM).

Rationale: matches the default hybrid policy; low risk; no code changes
needed beyond pointer retargeting.

## Implementation status

- [x] Charmap (`data/charmap.json`) + encode/decode tools
  (`tools/charmap.py`, `tools/encode_text.py`, `tools/decode_strings.py`).
- [x] Round-trip validation of all TEXT strings.
- [x] Large-glyph story subsystem: format, glyph store, script stream,
  control codes, readings for msgs 0–62 **and the 33 late messages**, the
  R1 support strings and the status word list (see Findings). 649/685
  glyphs mapped. Next: English glyph strategy (new
  glyphs; store relocation to free space + pointer rewrite at `0xD6C2C`).
- [x] Text-box line width: **17 glyphs/line, 2 lines/box**, then the box
  **pages** (clears and continues) if more lines arrive; `7533` caption
  clears the box (frame-verified 2026-10-18; auto-wrap mid-word; box
  ~240 px). EN budget: 30 chars/row, ≤3 pages/screen (M5).
- [ ] **Text inventory (next; M11 per user direction 2026-10-19)**:
  complete extraction of the remaining Japanese text — categorize 8×8
  direct-code strings (dialogue / menu / item / skill / UI) and locate
  the pointer(s) for each; mine graphics containing text; finish the
  four-kanji name tiles (blocked on a user read of the 8×8 sheet).
- [ ] Relocation writer: assemble new ROM copy, retarget pointers, emit BPS.
- [~] Translation (translation skill, milestone workflow). **M1 (story
  msgs 0–4) approved 2026-10-17** (rev 2). **M2 (story msgs 5–9)
  delivered 2026-10-17, revs 2–3 after user feedback**. **M3 (story
  msgs 10–16) delivered 2026-10-18** — first dialogue, captions, name
  inserts; outputs in `translation/`. **M4 (story msgs 17–24) delivered
  2026-10-18** — Kurimuto intro, 753F insert handling, incident setup.
  **M5 (story msgs 25–32) delivered 2026-10-18** — the coup, Winslow's
  death, the training arc; OAM-verified page model; exporter budget
  ≤3 pages. **M6 (story msgs 33–40) delivered 2026-10-18** — the tremor,
  Zargo, the altar room; 22 new glyphs; Zargo cross-checked against the
  8×8 scripts. **M7 (story msgs 41–48) delivered 2026-10-18** — Ramires
  appears, the second recipe, the climb; 30 new glyphs; ラミレス =
  Ramires confirmed against the 8×8 list. **M8 (story msgs 49–56)
  delivered 2026-10-18** — the beasts' taunt, the ruined altar, Ignis's
  full revival; 26 new glyphs; first-pass clean zip. **M9 (story msgs
  57–62) delivered 2026-10-18** — the awakening, Canon's power, the
  sky's far side; 23 new glyphs; all 63 story messages now read and
  translated. Per user decision 2026-10-18: continue without
  per-milestone review. **M10 (completeness audit + late-bank/R1
  integration) delivered 2026-10-19** — 33 late messages extracted and
  verified, charmap 649/685, R1 + status word list extracted. **M11
  (late-bank translation) paused 2026-10-19 by user direction**: the
  L0–L5 EN drafts were judged unacceptable and everything after msg 63
  is to be retranslated in a dedicated translation pass *after* the
  text extraction is complete (see the Text inventory item above and
  the workflow Decision). Then: English glyph strategy (bigfont
  relocation), relocation writer / BPS build.

Open items to resolve: OCR'd kanji review (8×8 charmap); the
`0x1A0–0x1BF` tiles; indexing of the `0x39D000..0x48C000` banks;
semantics of **7537** params only (7538 = 2 params, 7539 = 2-param
pass-through pair, 753E = beast-name insert, 753F = word insert — **all
resolved** 2026-10-18). M4–M9 translation flags awaiting user: msg 21
line-1 story reading; Kurimuto vs Klimt romanization; ロー = Roe/Rowe;
Zargo/Ramires spellings; M5 width-driven compressions and dynamic beast
names; M6 flags (その後 wording, の目前に compression); M7 flags (msg 41
red span drops 君, msg 44 passive "was told", terminal punctuation adds,
by-then wording); M8 flags (msg 49 "と突然" bridge, msg 55 君とのな
trailing, 例の folding, 完全復活 rephrase, 合獣機 term); M9 flags (entity
identity kept ambiguous, 久しぶり addressee unstated, msg 59 s1 page,
msg 60 width-foldings) — see
`translation/milestone-04-story-msgs-17-24.md`,
`translation/milestone-05-story-msgs-25-32.md`,
`translation/milestone-06-story-msgs-33-40.md`,
`translation/milestone-07-story-msgs-41-48.md`,
`translation/milestone-08-story-msgs-49-56.md` and
`translation/milestone-09-story-msgs-57-62.md`.

## Decisions

- WIKI.md is the single source of truth; checklist T1–T7 tracked here.
- Encoding standard: glyph index == text code; charmap in
  `data/charmap.json`.
- Use a custom headless libmgba harvester (`tools/mgba_dump.c`).
- Font identification combined runtime VRAM dumps with the user eyeballing
  rendered sheets and transcribing the charmap (OCR used for kanji).
- Automated shape-matching against Noto CJK abandoned (unreliable).
- Translation workflow (user, 2026-10-18): no per-milestone review pause;
  continue through milestones, contacting the user only for truly
  ambiguous or genuinely unsure cases. Recorded in `AGENTS.md` and the
  translation skill.
- Story EN page budget (2026-10-18, M5): accept up to 3 box pages per
  dense narration screen instead of compressing content (exporter flags
  >6 rows). EN rows hold 30 chars vs JP's 17 glyphs, so JP-aligned page
  counts are not always achievable; compressions are kept to a minimum
  and recorded per message.
- Workflow (user, 2026-10-19): **complete all Japanese-text extraction
  before translating.** Translation is a separate, dedicated pass using
  the translation skill, working from the complete corpus (full context,
  no RE interleaving). The late-bank EN drafts (L0–L5) are superseded
  and will be retranslated. Translation QA must include a composed-prose
  review (cohesion, punctuation, repetition) and a run-join spacing check
  — runs concatenate raw in engine order, and the current exporter does
  not detect a missing space between runs.

## Open questions

- Which specific kanji OCR readings are wrong.
- Unread bigfont entries (36 of 685): symbol block 0x12D–0x157 partially
  read; fragments 0x089/0x08A unknown; 0x0000-decoding quirk in the stale
  `0xCF52C` copy.
- M11 scope decision: the unreferenced R1 leftovers (`0xCF52C`, `0xCF7A6`,
  `0xCF8C0`, `0xCFA18`) are not displayed; plan is to skip translating
  them and note it in the milestone doc.
- Meaning/purpose of the `0x1A0–0x1BF` "squeezed kana" tiles.
- Indexing scheme for the pointer-unreferenced `0x39D000..0x48C000` banks.
- Story/narration control codes: classified (see Findings table). Remaining
  unknowns: exact semantics of 7537 params (7538 = 2 params, 7539 = 2-param
  pass-through pair, 753E = beast-name insert, 753F = canned-word insert —
  resolved 2026-10-18).
- Story/narration glyph space: `0x7D10` trailer; possible second table
  referencing glyphs; and the English font requirement (need to add
  letters/digits to a relocated 22-byte store, or squeeze — 16×11 box
  may be tight for small capitals; will need user input).

## Tool list (with versions)

- mGBA 0.10.5 (`mgba-qt`, `mgba-sdl`, `libmgba-dev`) — emulator + libmgba.
- capstone (Python) — ARM/Thumb disassembly.
- Pillow (Python) — image/tile rendering.
- `tools/mgba_dump.c` — headless harvester.
- `tools/extract_strings.py` → `build/strings.tsv` — string inventory.
- `tools/charmap.py` → `data/charmap.json` — glyph↔character table.
- `tools/decode_strings.py` → `build/strings_decoded.tsv` — decoder.
- `tools/render_font_candidates.py`, `tools/render_font_pages.py`,
  `tools/render_strings.py` — font/string renderers.
- `tools/ocr_screen.py` — OCR of dumped screens (kanji reading aid).
- `tools/probe_bigfont.py` — 16×11 glyph store prober: `count <off>`
  (ROM-wide occurrence count), `art <off> [n]` (ASCII-art render).
- `tools/render_story.py` — render story messages as PNGs (subcommands:
  `msg`, `sheet`, `glyph N`; `glyph` takes decimal index) — main
  vision-reading tool; `tools/zoom_tokens.py` — boxed, labeled zooms of a
  message's token range.
- `tools/build_charmap_story.py` — verifies transcriptions against token
  streams and writes `data/bigfont_charmap.json` (`READINGS` + `READINGS_LATE`
  dicts are the verified-translation source; `EXTRAS` adds hand-verified
  non-message glyphs).
- `tools/extract_late_bank.py` — extracts the 33 late messages
  (`0xD1F96..0xD30F4`) with count/start/end verification → `build/late_story_raw.json`.
- `tools/extract_r1.py` — extracts the R1 support region (`0xCF52C..0xCFB82`):
  37 segments, the 753E/753F tables, the name-input charset, and a
  pointer census → `build/r1_text_raw.json`.
- `tools/extract_8x8.py` — the 8×8 direct-code corpus extractor (window
  `0x099B40..0x0C6E00`): pointer-driven with `term`/`len`/`slice`/`split`
  styles, DB walks, `MANUAL_STARTS`/`SPLITS`/`EXCLUDED` tables →
  `build/8x8_corpus.tsv` (1,215 rows).
- `tools/census_8x8.py` — halfword-aligned pointer census of the same
  window → `build/8x8_ptrs.tsv` (1,502 targets + sources).
- `tools/render_glyph_sheet.py` → `build/glyph_sheet_1A0_1BF.png` +
  `build/glyph_names_1A0_1BF.png` — contact sheets for the unresolved
  glyphs `0x1A0–0x1BF`.
- `tools/story_en_export.py` — builds/QA-checks `translation/story_en.json`
  from `translation/story_en_runs.json`: run parity, control-code diff,
  char-exact wrap simulation, width/CJK checks, and a per-screen page
  budget (≤6 rows = 3 pages; more = restructure flag).
- `tools/story_render.py` (ASCII-art message render), `tools/small_art.py`
  (ASCII-art 8×8 glyph), `tools/dump_bigfont_used.py`,
  `tools/bigfont_groups.py`, `tools/bigfont_match.py`,
  `tools/map_screen_glyphs.py` (frame VRAM→glyph mapping) — exploration.
- `tools/scan_ptrs.py`, `tools/scan_compression.py`, `tools/scan_free.py`,
  `tools/scan_tiles.py`, `tools/render_tiles.py`, `tools/dump_table.py`,
  `tools/header.py` — analysis utilities.

## Install log

- `mgba-qt`, `mgba-sdl`, `libmgba-dev` (Debian) — via user, system pkgs.
- Python venv `.venv/` with `pillow`, `capstone` (pip).
- mGBA 0.10.5 source at `/tmp/opencode/mgba-0.10.5/` (API reference).
- Noto Sans CJK JP reference font `fonts/NotoSansCJKjp-Regular.otf`
  (matching abandoned; may drop).
