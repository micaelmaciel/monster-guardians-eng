# Monster Guardians (GBA) English translation

Goal: produce an English translation patch for the Japanese-only GBA game
Monster Guardians. The final deliverable is a BPS/IPS patch applied to the
user's own ROM, not a modified ROM.

## Ground rules

- The user supplies the original ROM. Never commit it, copies of it, or
  extracted copyrighted assets. Keep them in .gitignore.
- Never modify the original ROM in place. Work on copies and output patches.
- Before starting, check whether a fan translation or tools for this game
  already exist, and record what you find in the wiki.
- This is ROM hacking, not full decompilation. Focus on locating and
  extracting text, pointer tables, fonts, graphics containing text, and any
  compression, then reinserting the translation.
- If you have trouble with any capabilities you don't have, such as vision or anything else, ask me. We are working together, you do not need to decide everything for yourself.

## Project management

- Maintain WIKI.md as the single source of truth. Any agent in any session
  must be able to resume from it. Include: current state, completed work,
  next steps, tool list with versions, ROM offsets and format findings,
  decisions, and open questions. Update it at the end of every work session
  and after each milestone.
- Use git. Commit after each meaningful step with a clear message. Do not
  commit large binaries.
- Install any tools you need. If you need root, use pkexec and the user will
  enter the password. Install only what is needed, never touch files outside
  the project directory except for installing tools, and record every install
  in the wiki.
- Search thoroughly for the most current, maintained tools for dumping,
  disassembly, text extraction, pointer handling, font editing, and patch
  creation. Prefer actively maintained tools, and note versions and sources.
  If a tool offers agent-oriented skills or MCP servers, you may use them.

## Technical approach

- Do not edit the ROM until WIKI.md contains a user-approved text-handling
  strategy. If none exists yet, check WIKI.md for pending investigation tasks
  and continue them. If the tasks are missing, create them (text storage,
  compression, pointers, free space, font and display limits), then write a
  proposal and wait for the user's approval.
- The default strategy is hybrid: keep short strings such as menus and item
  names in place, within their byte and display limits, and relocate long
  text such as dialogue and descriptions to new space with updated pointers.
  Deviate only if the findings justify it, and explain why in the proposal.
- Once approved, follow the strategy recorded in WIKI.md. Track
  implementation status there: which text categories use which treatment,
  which pointer tables are done, and where relocated text lives.
- If new findings require changing the approved strategy, record the change
  and the reason in WIKI.md and tell the user before proceeding.

## Testing

- Verify changes in an emulator (for example mGBA). Check text overflow,
  glyph rendering, and crashes after each milestone.

## Translation

- Use the translation-agent skill whenever translating Japanese to English.
  Do not use it for the technical steps (extraction, hacking, tooling).
- Follow its milestone workflow: translate one chunk, run QA and proofreading,
  then stop and report to the user. Do not continue to the next milestone
  until the user responds.
- Keep the glossary, character sheet, and style guide in the repo and update
  them with user feedback.
- Text limits discovered during the technical investigation (line width, box
  size, byte budgets for in-place strings) must be passed to the translation
  step as constraints.
