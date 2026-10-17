# Monster Guardians (GBA) — English translation project wiki

Single source of truth. Any agent in any session must be able to resume
from this file. Update it at the end of every work session and after each
milestone.

## Current state

- ROM supplied by user at `rom/monster-guardians.gba` (gitignored; never
  commit, never modify in place).
- **Phase: technical investigation COMPLETE. Awaiting user approval of the
  strategy proposal before any ROM edits.**
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
- [ ] Text-box line width (awaiting user transcription of screens).
- [ ] Text inventory: categorize strings (dialogue / menu / item / skill /
  UI) and locate the pointer(s) for each.
- [ ] Relocation writer: assemble new ROM copy, retarget pointers, emit BPS.
- [ ] Translation (translation-agent skill, milestone workflow).

Open items to resolve: text-box line width; OCR'd kanji review; the
`0x1A0–0x1BF` tiles; indexing of the `0x39D000..0x48C000` banks.

## Decisions

- WIKI.md is the single source of truth; checklist T1–T7 tracked here.
- Encoding standard: glyph index == text code; charmap in
  `data/charmap.json`.
- Use a custom headless libmgba harvester (`tools/mgba_dump.c`).
- Font identification combined runtime VRAM dumps with the user eyeballing
  rendered sheets and transcribing the charmap (OCR used for kanji).
- Automated shape-matching against Noto CJK abandoned (unreliable).

## Open questions

- Exact text-box line width / line count (from a live text screen).
- Which specific kanji OCR readings are wrong.
- Meaning/purpose of the `0x1A0–0x1BF` "squeezed kana" tiles.
- Indexing scheme for the pointer-unreferenced `0x39D000..0x48C000` banks.

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
- `tools/scan_ptrs.py`, `tools/scan_compression.py`, `tools/scan_free.py`,
  `tools/scan_tiles.py`, `tools/render_tiles.py`, `tools/dump_table.py`,
  `tools/header.py` — analysis utilities.

## Install log

- `mgba-qt`, `mgba-sdl`, `libmgba-dev` (Debian) — via user, system pkgs.
- Python venv `.venv/` with `pillow`, `capstone` (pip).
- mGBA 0.10.5 source at `/tmp/opencode/mgba-0.10.5/` (API reference).
- Noto Sans CJK JP reference font `fonts/NotoSansCJKjp-Regular.otf`
  (matching abandoned; may drop).
