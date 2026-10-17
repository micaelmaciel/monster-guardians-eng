# Monster Guardians (GBA) — English translation project wiki

Single source of truth. Any agent in any session must be able to resume
from this file. Update it at the end of every work session and after each
milestone.

## Current state

- Project started. ROM supplied by user at `rom/monster-guardians.gba`
  (gitignored; never commit, never modify in place).
- **Phase: technical investigation → strategy proposal. ROM not yet edited.**
- Awaiting user approval of the text-handling strategy (see
  "Strategy proposal") before any ROM work begins.

## ROM identification

- File: `rom/monster-guardians.gba`, 8,388,608 bytes (8 MiB).
- GBA header title: `MONSTERGUARD`, game code: `AMNJA4`, maker: `01` (Nintendo),
  revision: Rev.00.
- Japanese-only release. (More header details: see "Findings".)

## Pending investigation tasks

- [ ] T1 — **Text storage**: locate all text in the ROM; determine encoding
  (custom charmap vs. plain ASCII/halfwidth), where strings live (flat
  blobs, per-message structs, script format), and which text categories
  exist (menus, item names, dialogue, descriptions, credits).
- [ ] T2 — **Compression**: determine whether text/script/graphics data is
  compressed (GBA conventions: LZ77 0x10 header, Huffman 0x11, RLE 0x30,
  or custom). Identify which assets use which scheme.
- [ ] T3 — **Pointers**: find pointer tables (arrays of 0x08xxxxxx pointers)
  pointing at text; determine pointer width, table locations, and whether
  pointers are direct ROM offsets, indirect, or relative.
- [ ] T4 — **Free space**: map unused regions (0xFF/0x00 padding) in the
  8 MiB ROM for relocated text and any inserted code.
- [ ] T5 — **Font and display limits**: locate the font/character map
  (glyph count, widths, halfwidth vs. fullwidth), text box dimensions
  (pixels, line count, line width), and any variable-width font (VWF)
  support. Derive per-string byte budgets.
- [ ] T6 — **Prior art**: check for existing fan translations, dumps,
  disassemblies, or tools for this game. (See "Prior art and tools".)
- [ ] T7 — **Tooling**: pick and record tools with versions (extraction,
  disassembly, pointer handling, patch creation).

## Prior art and tools

- (To be filled by T6/T7.)

## Findings

- (To be filled by T1–T5.)

## Strategy proposal

- (Draft to be written after T1–T7; needs user approval before ROM edits.)

## Decisions

- (None yet.)

## Open questions

- (To be filled.)

## Tool list (with versions)

- (To be filled.)

## Install log

- (None yet.)
