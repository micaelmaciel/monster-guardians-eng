# Monster Guardians (GBA) — English translation project wiki

Single source of truth. Any agent in any session must be able to resume
from this file. Update it at the end of every work session and after each
milestone.

## Current state

- ROM supplied by user at `rom/monster-guardians.gba` (gitignored; never
  commit, never modify in place).
- **Phase: technical investigation, nearing completion. ROM not yet edited.**
- Breakthrough: text encoding is solved enough to decode strings — text is
  a stream of **16-bit glyph indices**, and the font is a **512-glyph 8×8
  tileset at ROM 0xBEDF0** (glyph index == text code). Verified visually:
  rendered ROM strings read as coherent Japanese (user-confirmed).
- Remaining before proposal: transcribe the font's glyph→character table
  (user is doing this), confirm any text categories with codes > 0x1FF.
- **Do not edit the ROM until the user approves the strategy proposal.**

## ROM identification

- File: `rom/monster-guardians.gba`, 8,388,608 bytes (8 MiB / 64 Mbit).
- Header title: `MONSTERGUARD`, game code `AMNJ`, maker `A4` (Konami),
  unit 0x96, complement 0x1B (mismatch vs computed 0x5F), checksum 0x0000.
  These anomalies are normal for launch-window carts, **not corruption**.
- Publisher Konami; developer Mobile21; GBA launch title (March 2001).
- Japanese-only release.

## Pending investigation tasks

- [x] T1 — **Text storage**: 16-bit glyph-code strings (see Findings).
- [~] T2 — **Compression**: no confirmed compression; text appears
  uncompressed. One RLE 0x30 candidate remained unverified (likely false
  positive). LZ77 hits were false positives.
- [x] T3 — **Pointers**: 32-bit little-endian direct pointers `0x08xxxxxx`.
- [x] T4 — **Free space**: one large block (see Findings).
- [~] T5 — **Font and display limits**: font located and decoded; text-box
  pixel/line limits still to be measured from a live screen.
- [x] T6 — **Prior art**: none found (see Prior art).
- [x] T7 — **Tooling**: chosen and recorded (see Tool list).

## Prior art and tools

- **No fan translation, dump, disassembly, or dedicated tool exists** for
  Monster Guardians. Only translation *requests* (romhacking.net, Reddit).
- General GBA tooling applies (mGBA, capstone/ARM disasm, tile tools).

## Findings

### Text encoding (T1) — SOLVED

- Text is stored as a stream of **16-bit little-endian glyph indices**.
- String terminator: `0x0000`. Padding/filler: `0xFFFF` (and `0x7FFF`
  appears as a separator in some tables).
- **Text code == glyph index into the font** (verified: ROM strings render
  to coherent Japanese). Example: code `0x002` renders "0".
- Codes observed mostly ≤ 0x1FF (the 512-glyph font range). Some candidate
  "strings" contain codes > 0x1FF (`0x7fff`, `0x7500`-range) — these are
  either non-text data misdetected as strings or a second escape encoding;
  still to be resolved.
- Extracted inventory: `build/strings.tsv` (~2,826 rows; addr + code list +
  pointer sources) via `tools/extract_strings.py`.
- Main text banks: `0x09DB08`, `0x0C5D9C`, `0x0A12AC`, `0x0A902A`,
  `0x0A9956`, `0x0A88A0`, `0x0B5728`, `0x0AEDE8`, `0x0CC912`, `0x0CD438`,
  `0x0CDAF8`, plus ~19 pointer-unreferenced script banks spanning
  `0x399756..0x48BD86` (~350 entries each).

### Font (T5) — SOLVED

- Font = **8×8 pixels, one glyph per tile, 4 bpp**, 32 bytes per glyph.
- **ROM base `0xBEDF0`**, 512 glyphs (indices `0x000`–`0x1FF`), 16 KiB.
- Loaded verbatim to **VRAM charBase 0** (`0x06000000`) at boot.
- Glyph `0x002` = `"0"` (user-confirmed). Glyphs `0x000`/`0x001` are blank.
- User-confirmed ordering: **digits → Latin letters → hiragana → katakana
  → symbols → kanji** (systematic order). Some slots are blank or render a
  gray box (placeholder glyph).
- Pixel value 0 = background; higher nibbles = ink.
- Renders for reference: `/tmp/opencode/fontcand/rom_BEDF0_8x8.png`
  (correct), `rom_BEDF0_8x16.png` (wrong — two chars per cell).
- **TODO:** glyph→character transcription table (user working on it).
  This becomes the project's charmap.

### Emulator harness (T7)

- `tools/mgba_dump.c` — headless libmgba 0.10.5 harvester. Dumps
  VRAM/EWRAM/IWRAM/palette/OAM/I-O and PPM screenshots at scheduled frames,
  with scheduled button input.
- Build: `gcc -O2 -o tools/mgba_dump tools/mgba_dump.c -lmgba`.
- Usage: `tools/mgba_dump <rom> <outdir> [frames_csv] [input_spec]`.
- **Critical init sequence** (a zeroed `mCoreOptions` passed to
  `mCoreConfigLoadDefaults` segfaults): `mCoreFind` → `core->init` →
  `mCoreInitConfig(core,"mgba")` →
  `mCoreConfigSetDefaultValue(...,"idleOptimization","remove")` →
  `mCoreConfigSetDefaultIntValue(...,"logToStdout",0)` →
  `mInputMapInit(&core->inputMap,&GBAInputInfo)` → `mCoreLoadFile` →
  `core->reset` → `setVideoBuffer` → **`reloadConfigOption(core,
  "hwaccelVideo", &core->config)`** (associates the software renderer;
  without it `getPixels`/screenshots are blank).
- `color_t` is `uint32_t` (not COLOR_16_BIT) — framebuffer is BGR8.
- Buttons set via `core->setKeys(core, 1<<GBA_KEY_*)`.

### Graphics / screen structure

- `DISPCNT` mode 0. BG0 is commonly a 64×64 **image** layer (tilemap of
  distinct sequential tile indices, e.g. map `0xD000`, charBase 1).
- BG2/BG3 use **charBase 0 = the font** and draw text windows (border tiles
  e.g. `0x120`–`0x145`).
- A large sequential glyph-ID table lives at ROM ~`0x399700` and is copied
  to EWRAM `0x02004530`; it matches a full-screen BG tilemap (image), not
  text.

### Pointers (T3)

- 32-bit little-endian **direct** pointers `0x08xxxxxx`.
- 530 pointer tables found (e.g. `0x228C4`, `0x24634` → `0xA8864`,
  `0xB5728`, `0xB61F0`; array `0x0C370C` → `0x0CD3DC..0x0CD4AE`).
- Dense target hot-spots: `0x090000`, `0x0C0000`, `0x0B0000`,
  `0x540000–0x55FFFF`, `0x760000`.

### Free space (T4)

- One large free block: **`0x76765D..0x800000` = 625,059 bytes**, fill
  `0x00`. Ample for relocated dialogue.
- Total free space > 4 KiB: 625,059 bytes.

### Compression (T2)

- No confirmed compression. Text is plain 16-bit codes. LZ77/RLE hits were
  false positives; one RLE `0x30` candidate implausible and unverified.

## Strategy proposal (DRAFT — needs user approval)

Default **hybrid** strategy, adapted to findings:

1. **Short strings in place** (menus, item/skill names, short labels) where
   the English fits the existing 2-byte-per-glyph budget. Same byte length
   or shorter → overwrite in place, pad with `0x0000`/`0xFFFF`.
2. **Long text relocated** (dialogue, descriptions, endings) to the free
   block at `0x76765D`, rewriting the 32-bit pointer(s) that reference each
   string. Because English is longer than Japanese in glyph count, almost
   all dialogue will be relocated.
3. **Charmap**: build the glyph→character table from the user's
   transcription of the font sheet; preserve the game's own 8×8 font for
   all new English text (Latin glyphs already exist at low indices).
4. **No font expansion** for v1 (English fits the existing Latin glyphs).
   Revisit only if the font lacks needed punctuation.
5. Output a **BPS patch** against the user's ROM (never ship the ROM).

Rationale: matches the default hybrid policy; low risk; no code changes
needed beyond pointer retargeting.

Pending before approval: full charmap transcription, text-box line-width
measurement, resolution of >0x1FF code strings.

## Decisions

- WIKI.md is the single source of truth; checklist T1–T7 tracked here.
- Use a custom headless libmgba harvester (`tools/mgba_dump.c`) for dumps
  and screenshots (mGBA SDL frontend has no scripting; Qt scripting
  avoided).
- Font identification combined runtime VRAM dumps (ground truth) with the
  user eyeballing rendered PNG sheets; automated shape-matching against
  Noto CJK was unreliable and is abandoned.
- Glyph rendering uses ROM `0xBEDF0` / VRAM charBase 0 as the canonical
  font source.

## Open questions

- Full glyph→character table (in progress with user).
- Size and identity of the kanji block; how many glyphs are actually used.
- Meaning of candidate strings whose codes exceed `0x1FF`.
- Indexing scheme for the pointer-unreferenced `0x39D000..0x48C000` banks.
- Exact text-box line width and line count (from a live text screen).
- Whether any assets (script tables) use RLE.

## Tool list (with versions)

- mGBA 0.10.5 (`mgba-qt`, `mgba-sdl`, `libmgba-dev`) — emulator + libmgba.
- capstone (Python) — ARM/Thumb disassembly.
- Pillow (Python) — image/tile rendering.
- `tools/mgba_dump.c` — headless harvester (in repo).
- `tools/extract_strings.py` → `build/strings.tsv` — string/bank inventory.
- `tools/render_font_candidates.py` — labelled font-sheet renderer.
- `tools/render_strings.py` — render ROM code strings with the game font.
- `tools/scan_ptrs.py`, `tools/scan_compression.py`, `tools/scan_free.py`,
  `tools/scan_tiles.py`, `tools/render_tiles.py`, `tools/dump_table.py`,
  `tools/header.py`, `tools/match_font.py` (deprecated) — analysis utils.

## Install log

- `mgba-qt`, `mgba-sdl`, `libmgba-dev` (Debian) — via user, system pkgs.
- Python venv `.venv/` with `pillow`, `capstone` (pip).
- mGBA 0.10.5 source at `/tmp/opencode/mgba-0.10.5/` (for API reference).
- Noto Sans CJK JP reference font `fonts/NotoSansCJKjp-Regular.otf`
  (matching abandoned; may drop).
