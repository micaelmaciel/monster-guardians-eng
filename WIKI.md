# Monster Guardians (GBA) — English translation project wiki

Single source of truth. Any agent in any session must be able to resume
from this file. Update it at the end of every work session and after each
milestone.

## Current state

- ROM supplied by user at `rom/monster-guardians.gba` (gitignored; never
  commit, never modify in place).
- **Phase: strategy APPROVED (2026-10-17); no ROM edits yet.** Both text
  subsystems are now structurally understood: (1) 8×8 direct-code text
  (2,223 strings, ready for translation), (2) 16×11 large-glyph story
  script at `0xCFF84` with a 685-glyph store at `0xD3144`.
- **Story script is READABLE.** The 63 messages are fully decodeable;
  `tools/render_story.py` renders any message as a PNG (game-like layout,
  optional hex labels) and `tools/zoom_tokens.py` zooms token ranges.
  Charmap for the bigfont now has **260 glyphs verified** (messages 0–24
  fully transcribed, each zipped token-by-token against its stream with
  zero mismatches/conflicts) via `tools/build_charmap_story.py`; see
  `data/bigfont_charmap.json`. Control parsing corrected 2026-10-18:
  `7538` takes **2 params** (was 1 — msg 22 desync fix), `753F` added as
  a 1-param insert (ご子息, msg 21).
- Confirmed by reading the actual game: 63 messages are the **whole game's
  story/event text** (intro attract = messages 0–9, then in-game event
  scenes). See "Story script readings" below.
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
- [ ] T8 — **Story/narration charmap**: build a character map for the
  685-glyph store at `0xD3144`, then decode all 63 script messages at
  `0xCFF84..0xD1F96`. **In progress**: 222 glyphs verified (msgs 0–16
  fully readable; remaining glyphs read via vision renders — no OCR);

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
- Dictionary at `0xD30F4..0xD3143`: 32 entries of
  `{c1, c2, 0x7FFF}` (two glyph codes + terminator), codes up to
  `0x2AC`. Likely a kanji-compound ↔ kana reading pair table used by the
  story renderer; trailer word `0x7D10` after `0xD3143` may be a
  checksum or count (unresolved).
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
| `0x753E` | 1 | param command (10×, msgs 31/32/46; params 0–5,8 — beast-name inserts inside red spans; EN plan: drop + spell the word) |
| `0x753F` | 1 | word insert (1×, msg 21): prints the canned word ご子息 "son" mid-line — verified in-game, frame 19200. EN drops the control and carries the word as plain text. |
| `0x7540` | 0 | player-name variable insert (30×). Occurs inside red blocks (msg 16: `「[753B][7540][753C]だった！」`) and mid-sentence (`追っ手達が[7540]に手をかけようとした`). Keep verbatim in translation. |
| `0x7FFF` | 0 | end of message |
| `0xFFFE`/`0xFFFF` | 0/1 | in-block sentinels/params (msg 2/3 use `7535 0001 FFFF`; 60/62 use `FFFE` + glyphs) |

Display limits (measured in-game): glyph advance 12 px, line height
13 px; the box fits **~17 glyphs per line, 2 lines**; text auto-wraps
mid-word (msg 4 line 1 = 17 glyphs exactly, "…征服しよ" then "うと、").
`0x7530` starts a new line. Verified in a live playthrough 2026-10-18
(`/tmp/opencode/story_run`, frames cited):

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

### Story script readings (verified against renders + live frames)

Messages 0–24 **fully verified** (2026-10-17/18): every glyph zips
against its token stream in `tools/build_charmap_story.py` `READINGS` —
260 glyphs mapped, zero length mismatches, zero char conflicts.
Notation: `／` = box line break, `[wN]` = 0x7534 wait, `[SCR]` = 0x7532
screen break, `[CLR]` = 0x7531 clear, `[W]…[/W]` = 7535/7536 white block,
`[RED]…[/RED]` = 753B/753C red block, `[名]` = 0x7540 name insert,
`[753F n]` = word insert (prints a canned word).

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

Names/terms found so far: グランデート大陸 (Grandeート continent),
カノン (Canon — sky dragon), イグニス (Ignis — earth dragon),
ハイドラゴン (hydra dragon), クリムト (Kurimuto — old beast tamer),
ベリンガム (Beringham — lord), バルロア王国 (Kingdom of Barroa),
ファムファンタル火山 (Famfantar volcano), ザーゴ (Zargo — man-made
beast), タクト (tact/baton — beast-tamer tool), 魔獣使い (beast tamer),
追っ手 (pursuers), 廃墟 (ruins), ウィンスロー (Winslow — lord of
Vandam Castle; 二世 = "II"), ヴァンダム城 (Vandam Castle — msg 23
caption), 事件 (the incident — msg 22, red span). The player character's
name is inserted via `0x7540`. Partial decode pass over msgs 25–62
(glyphs pending) adds: 魔獣騎士団 (the Pope's Beast Knight Order),
法王 (the Pope), Beringham's second beast ラ□□ス, and Beringham's full
name ベリンガム・ロー□□ — **2 surname glyphs still unread (M5)**.

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
  control codes, and readings for msgs 0–24 (see Findings). 260/685
  glyphs mapped. Next: read/translate remaining messages (M5 = msgs
  25+); then English glyph strategy (new glyphs; store relocation to
  free space + pointer rewrite at `0xD6C2C`).
- [x] Text-box line width: **17 glyphs/line, 2 lines/box**, then the box
  **pages** (clears and continues) if more lines arrive; `7533` caption
  clears the box (frame-verified 2026-10-18; auto-wrap mid-word; box
  ~240 px).
- [ ] Text inventory: categorize strings (dialogue / menu / item / skill /
  UI) and locate the pointer(s) for each.
- [ ] Relocation writer: assemble new ROM copy, retarget pointers, emit BPS.
- [~] Translation (translation skill, milestone workflow). **M1 (story
  msgs 0–4) approved 2026-10-17** (rev 2). **M2 (story msgs 5–9)
  delivered 2026-10-17, revs 2–3 after user feedback**. **M3 (story
  msgs 10–16) delivered 2026-10-18** — first dialogue, captions, name
  inserts; outputs in `translation/`. **M4 (story msgs 17–24) delivered
  2026-10-18** — Kurimuto intro, 753F insert handling, incident setup.
  Per user decision 2026-10-18: continue without per-milestone review.
  Next: M5 = story msgs 25+.

Open items to resolve: OCR'd kanji review (8×8 charmap); the
`0x1A0–0x1BF` tiles; indexing of the `0x39D000..0x48C000` banks;
semantics of 7537/7539/753E params (7538 = 2 params and 753F = word
insert **resolved** 2026-10-18). M4 translation flags awaiting user:
msg 21 line-1 story reading; Kurimuto vs Klimt romanization;
Beringham's surname glyphs (2 unread) — see
`translation/milestone-04-story-msgs-17-24.md`.

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

## Open questions

- Which specific kanji OCR readings are wrong.
- Meaning/purpose of the `0x1A0–0x1BF` "squeezed kana" tiles.
- Indexing scheme for the pointer-unreferenced `0x39D000..0x48C000` banks.
- Story/narration control codes: classified (see Findings table). Remaining
  unknowns: exact semantics of 7537/7539/753E params (7538 = 2 params,
  753F = canned-word insert — resolved 2026-10-18).
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
  streams and writes `data/bigfont_charmap.json` (`READINGS` dict is the
  verified-translation source).
- `tools/story_en_export.py` — builds/QA-checks `translation/story_en.json`
  from `translation/story_en_runs.json`: run parity, control-code diff,
  char-exact wrap simulation, width/CJK checks.
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
