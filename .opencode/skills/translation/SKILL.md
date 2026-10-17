---
name: translation
description: Careful, context-aware translation of long or high-stakes text (game scripts, fiction, dialogue, subtitles, manuals, UI strings, documents), especially Japanese to English. Use this skill whenever the user asks to translate more than a few lines, mentions a fan translation, localization, script, ROM text, or dialogue dump, asks for translation that sounds natural, or wants consistency across a large body of text, even if they never say "skill" or "workflow". Covers researching context before translating, using tools to extract and validate text, keeping translations natural, and preserving the author's intent.
---

# Translation Agent

Translate the way a good human localizer works: understand the source first, build a reference sheet, translate in context, then check the result against both the original meaning and natural English. Most AI translation failures come from skipping those steps and translating line by line from memory, so this workflow exists to force them.

The four drivers of this skill, in priority order:

1. **Intent preservation**: the translation must do what the original does (inform, joke, threaten, comfort, characterize), not just mean roughly the same thing.
2. **Naturality**: it must read like something a native English writer would produce in this context.
3. **Searching**: look things up instead of guessing (names, terms, references, series conventions).
4. **Tooling**: use tools to extract, chunk, track, and verify, so scale doesn't degrade quality.

When naturality and intent conflict, intent wins. A natural-sounding line that changes what the character means is a bad translation. Aditionally, you are to look up your `reference.md` file in order to maintain translation consistency.

---

## Working in milestones

Never translate a large project in one pass. Long single runs are where quality degrades, skipped lines go unnoticed, and a wrong early decision (a name, a tone, a pronoun) spreads through everything that follows. Milestones keep the user in the loop and make mistakes cheap to fix.

When this applies. Any project too large to translate, check, and proofread carefully in one sitting: a game script, a novel, a full subtitle set, a large manual. If the whole job is small (a short scene, a page of UI strings), treat it as a single milestone and deliver in one go.

### How to plan it.

1. After intake, research, and the reference sheet (Steps 0 to 2), look at the full scope and split it into milestones along natural boundaries: chapters, areas, scenes, menus vs. story vs. item text, or a fixed line count. Don't cut mid-scene or mid-conversation.
2. Size each milestone so it can go through the whole pipeline (Steps 3 to 8) with real attention. When unsure, go smaller.
3. Propose the plan to the user before starting: the milestone list, the order, and a rough size for each. Start with a milestone that is representative and low-risk, such as an opening area or a short self-contained scene, because it sets the voice and exposes problems early.
4. Wait for the user's agreement on the plan, unless they already told you how to split it.

**How to run each milestone.** Run Steps 3 to 8 on that milestone only, then stop and report (Step 9). Do not start the next milestone until the user responds. Each milestone report should say:

- what was completed (range or section, line count)
- decisions made and new glossary or character entries
- flagged lines and open questions
- what the next milestone would be, and a proposal for how to proceed

**Why stop and report.** The user may disagree with a tone, a name, or a localized joke, and it is far cheaper to change that after one milestone than after the whole project. Their feedback becomes part of the reference sheet.

**Carrying feedback forward.**

- Update the glossary, character sheet, and style guide with every correction or preference the user gives.
- If feedback changes an earlier decision, apply it to the already-translated milestones too, or tell the user which earlier lines are affected and offer to fix them.
- Re-read the updated reference sheet before starting each new milestone, and include a few lines of the end of the previous milestone as context so the join is seamless.

**Keep the work recoverable.** Save each milestone's output and the current reference sheet as files when tools allow, with clear names (for example milestone-02-forest.txt). This lets work resume after an interruption and lets the user see exactly what was delivered.

Don't stall on small things. Pause between milestones, not between lines. Within a milestone, flag uncertainties in the report instead of interrupting for each one, unless an unresolved question would invalidate the whole milestone (for instance, not knowing a main character's gender).

---

## Workflow

### Step 0: Intake

Before translating, establish:

- **Source and target language**, and target variety if it matters (US/UK English).
- **Medium and constraints**: game text box, subtitle timing, UI label, prose, etc. Note character limits, line widths, control codes, and placeholders.
- **Audience and tone**: kids' game, dark horror, comedy, formal manual.
- **Deliverable format**: plain text, original file format, side-by-side table.

Ask the user only for what you can't infer or look up. If the user gave a file, read it first; don't ask questions the file already answers.

### Step 1: Research (searching)

Search before translating, not after you hit a problem. The goal is to learn what a human translator would learn from playing, reading, or watching the source.

Look up:

- **The work itself**: genre, setting, plot summary, tone, release era, target age group. A short summary prevents tone-deaf choices.
- **Character names and readings**: kanji names can have several readings. Find the official or most established romanization. If none exists, choose one and record it.
- **Series terminology**: if the work belongs to a franchise, check how official localizations render recurring terms (spell names, item names, honorifics, titles). Match established conventions unless the user wants otherwise.
- **Existing translations**: official or fan translations of the same or related works, for terminology and for what to avoid. Use them as reference for terms, never copy their sentences.
- **Cultural references, puns, dialects, and slang**: look up anything you can't confidently explain.
- **Speech patterns**: how characters of this type are typically voiced (gruff, polite, childlike, archaic, regional dialect).

Search rules:

- Prefer primary and well-maintained sources (official sites, wikis, community translation notes) over aggregators.
- Do not mention or rely on a patch's existence without verifying it.
- If a search doesn't resolve something, say so and flag it in the output. Do not fill the gap with a confident guess.
- Paraphrase what you find. Don't paste long passages from sources into the translation or notes.

### Step 2: Build the reference sheet

Create (and keep updating) a reference sheet before the first translated line. Save it as a file when tools allow, so it survives long sessions.

Include:

- **Glossary**: source term, chosen translation, notes, and where it first appeared.
- **Character sheet**: name (source + target), gender and pronouns, age/role, speech style, how they address others (by name, title, nickname), and relationships.
- **Style guide**: register, contractions, profanity level, how to handle honorifics, onomatopoeia, sound effects, and units.
- **Do-not-translate list**: names, brand terms, or catchphrases that stay as-is.
- **Open questions**: ambiguities to flag to the user.

Every later chunk is translated against this sheet. Consistency across thousands of lines depends on it, because you will not reliably remember how you rendered a term 500 lines earlier.

### Step 3: Prepare and chunk the text (tooling)

Use tools instead of doing everything by eye.

- **Extract text programmatically** if the source is a file (script dumps, subtitle files, spreadsheets, game text exports). Preserve IDs, line numbers, and structure so output maps back to the source one-to-one.
- **Protect non-text elements.** Control codes, tags, variables, placeholders, and escape sequences must be identified up front and passed through untouched. Examples: `<br>`, `{name}`, `%s`, `\n`, color codes, byte-like markers. Move them only where English grammar demands it, and never delete or alter them.
- **Chunk by meaning, not by size.** Break at scene or dialogue boundaries, not mid-conversation. Include the preceding 10 to 20 lines as read-only context so speakers, pronouns, and running jokes carry across.
- **Track progress.** Maintain a count of source lines vs. translated lines per chunk so skipped or merged lines are caught mechanically.
- **Run automated checks** after each chunk (see Step 7).

If no code or file tools are available, apply the same discipline manually: number the lines, keep the reference sheet in view, and verify counts at the end.

### Step 4: Translate with context

For each chunk:

1. **Read the whole chunk first**, plus the context lines, before writing anything.
2. **Identify the speaker and listener of every line.** Japanese often omits subjects, so infer them from surrounding lines, honorific levels, and the character sheet. If a line's speaker is genuinely ambiguous, mark it instead of guessing silently.
3. **Decide what each line is doing**: joke, threat, hesitation, politeness, sarcasm, exposition. Translate that function.
4. **Draft the translation using the glossary and style guide.**
5. **Keep a one-to-one line mapping** unless the user allows restructuring. Don't merge, split, summarize, or drop lines.

### Step 5: Naturality pass

After drafting, reread the English on its own, without looking at the source, and ask whether a native speaker would say or write this.

Fix:

- **Translationese**: literal word order, stiff phrasing, unnecessary pronouns (English needs subjects, but not repeated "he/she" every sentence), over-long sentences copied from the source structure.
- **Calques**: phrases that are grammatical but nobody says. Replace with the idiom an English speaker would actually use in that situation.
- **Register mismatches**: a child character using formal vocabulary, a soldier using flowery language.
- **Over-polishing**: smoothing rough, quirky, or distinctive speech into bland neutral English. Distinct voices should stay distinct.
- **Rhythm**: dialogue should be speakable. Read it aloud mentally.

Preserve flavor deliberately:

- Show formality and personality through word choice and sentence shape instead of leaving untranslated honorifics, unless the style guide says to keep them.
- Dialects and verbal tics (a character who ends sentences with a catchphrase) need an English equivalent that is applied consistently, not dropped.

### Step 6: Intent preservation check

Compare each translated line back against the source with a skeptical eye.

For every line, confirm:

- **Meaning**: nothing added, nothing dropped, no softened or hardened force. Don't change a character's level of anger, doubt, affection, or certainty.
- **Function**: jokes still land (or are replaced with an equivalent joke, flagged in notes), threats still threaten, hints still hint without spoiling.
- **Information**: facts, numbers, names, and plot-relevant details are identical.
- **Ambiguity**: if the original is deliberately vague, the English is deliberately vague. Don't resolve ambiguity the author left open.
- **Cultural references**: choose deliberately between keeping the reference (with a brief note if the format allows), adapting it, or replacing it. Never silently delete it, and avoid adaptations that change what is actually being said.

Wordplay and puns: translate the effect when the literal meaning can't carry it. If you substitute a different joke, flag it in the notes so the user can review. Don't pretend a literal rendering preserved a pun that is gone.

### Step 7: Automated and manual QA

Run these checks on the full output:

- **Line count matches** the source, with IDs aligned.
- **Placeholders and control codes** are identical in source and target (diff them).
- **Glossary consistency**: search the output for each glossary term and verify uniform rendering. Check for variant spellings of names.
- **Length limits**: flag any line that exceeds the character or width limit. Shorten by rephrasing, not by dropping meaning.
- **Pronoun and speaker spot-check**: sample dialogue exchanges and verify who is speaking to whom.
- **Untranslated leftovers**: scan for source-language characters that shouldn't remain.
- **Skipped or summarized content**: spot-check long chunks against the source for silently condensed lines.

Fix problems at the root and update the reference sheet when a decision changes. If a term changes, apply it everywhere.

### Step 8: Proofread

Proofreading is the last pass over the text before delivery. It fixes errors only. It must not change meaning, voice, or decisions already recorded in the style guide, because rewriting at this stage reintroduces the problems the earlier steps removed. If something needs more than a correction, flag it instead of changing it.

Check:

- **Spelling and typos**, including character names, invented terms, and glossary entries.
- **Grammar**: subject-verb agreement, tense consistency within a scene, articles, plurals, and doubled or missing words.
- **Punctuation and capitalization**: ellipses, dashes, quotation marks (matched and of one style), apostrophes, sentence-initial capitals, and title case in menus and labels.
- **Formatting consistency**: spacing, line breaks, how sound effects, emphasis, and thoughts are styled, and number and unit formats.
- **Presentation in context**: read the text as the end user will see it (in a text box, subtitle, or UI) when possible. Many errors only show up there, such as overflow, orphaned words, or a break in the wrong place.
- **A fresh read**: go through the output once more start to finish as if you had never seen it, looking only for things that read as mistakes.

After any proofreading fix, rerun the Step 7 checks that could be affected (line counts, placeholders, length limits), since a correction can break them.

### Step 9: Deliver with a short report

Deliver the translation in the requested format, plus a brief note containing:

- Decisions the user may want to review (names, localized jokes, adapted references).
- **Flagged lines**: ambiguous, uncertain, or unresolvable items, with the reading you chose and the alternative.
- Assumptions made where research was inconclusive.
- The final glossary and character sheet if the user will continue the project.

Be plain about uncertainty. A flagged line is far more useful than a confident wrong one.

---

## Common mistakes to avoid

These are the specific failure modes of AI translation on large texts. Treat them as a checklist.

| Mistake | How to avoid it |
|---|---|
| **Inconsistent terms and names** across a long text | Keep and consult the glossary every chunk; run a consistency search at the end |
| **Wrong speaker or pronouns** because Japanese drops subjects | Identify speaker and listener per line; use the character sheet; mark true ambiguity |
| **Flattened voice** where every character sounds the same | Define each character's speech style up front and reread against it |
| **Skipped, merged, or summarized lines** in long outputs | One-to-one line mapping; count lines per chunk |
| **Invented or dropped content** | Compare back to the source; never add explanation inside the translation itself |
| **Confident guesses on ambiguity** | Flag the line and give alternatives instead of silently choosing |
| **Lost puns and wordplay** | Translate the effect, replace deliberately, and note the substitution |
| **Wrong name readings or inconsistent romanization** | Research readings; record the decision in the glossary |
| **Broken tags, variables, and control codes** | Protect them in preprocessing; diff source vs. target codes |
| **Lines too long for the container** | Check length limits; rephrase rather than cut meaning |
| **Cultural references mishandled** (left opaque or over-localized) | Decide deliberately per reference; keep decisions consistent |
| **Drifting quality late in a long job** | Chunk the work, re-read the style guide at each chunk, and do a final QA pass |
| **Translationese** | Do a separate naturality pass reading only the English |
| **Over-smoothing quirky source text** | Preserve intentional roughness, dialect, and verbal tics |
| **Typos, grammar slips, and inconsistent punctuation** | Run a dedicated proofreading pass at the end that fixes errors only |
| **Late "fixes" that change meaning or voice** | Keep proofreading limited to corrections; flag anything bigger |

---

## Principles to keep in mind

- **Never guess silently.** Research it, ask, or flag it.
- **The user is a human.** The user knows best what sounds natural and what doesn't, so take their input on anything ambiguous or that is not easily answerable with a web search.
- **Translate meaning and function, not words.** But never change meaning in the name of fluency.
- **Context first.** A line alone is rarely enough. Read what comes before and after.
- **One decision, applied everywhere.** Record it, then follow it.
- **Don't summarize.** Unless the user asks for a summary, every source line gets a translated line.
- **Respect the author.** Keep their tone, pacing, and level of explicitness. Don't censor, sanitize, or embellish unless asked.
- **Be honest about limits.** If the source text is corrupted, partial, or uses an unknown encoding, say so instead of producing plausible-looking output.
