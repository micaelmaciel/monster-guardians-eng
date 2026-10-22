# About

This an English translation of an obscure Japanese-only Konami game for the GBA, namely Monster Guardians.

That was mostly an excuse for testing some open-weight, non-frontier models on a range of complex tasks, though. Since the romhacking scene is triving right now and given the amount of work required for reverse engineering + a full translation, I thought on jumping on the bandwagon, because why not? I spent 0$ dollars on this and used 2 different Opencode free models, with **Deepseek V4.1** Flash doing the vast majority of the work here. It took 4 days from start to end (not real work time, though).

The models used during the lifetime of this project:
- Big Pickle (which is not a disclosed a model)
- Deepseek 4.1 Flash

GLM 5.3 was in use in another RE project, though I forgot to include it on this one :(

I specifically chose a game that had a decent amount of text, but could not be considered to have a heavy narrative, such that I could proofread it. I don't even care for this game (it's kinda dogshit, with all due respect), but I'm sure some people would enjoy it. Maybe Pokémon fans.

# The patch

The `.bps` patch can be downloaded in the releases page. It is not game breaking, it can be beaten, but there are still a few minor graphical issues here and there. I did some QA myself, I went over the entire storyline (which isn't that big), so hopefully you won't find anything too jarring.

# For the curious

## Usage statistics

Data extracted from the OpenCode session database (`opencode.db`). 

### Notes on how the numbers were computed

- Compaction runs (context summarization) are reported separately from regular turns.
- **Uncached input** is the fresh part of each prompt. **Cache read** is already-cached context re-read on every turn. Cache writes were always 0.
- **Active time** is the sum of assistant-turn durations. Tool execution time is already included in it.
- Models used: `deepseek-v4.1-flash-free` (`max` variant for 93% of turns, `default` for the rest) and `big-pickle` (first session only). Free-tier context cap is 200k.

### Overview

| | |
|---|---|
| Sessions | 7 |
| Model turns | 7,103 |
| Tool calls | 7,748 |
| User prompts | 119 |
| Wall-clock | 105 h |
| Agent active time | 39.3 h (37% of wall-clock) |
| Compactions | 131 (one per ~54 turns; 5 failed) |

### Tokens

| | Regular turns | Compaction | Total |
|---|---|---|---|
| Uncached input | 37.14M | 0.79M | 37.93M |
| Cache read | 780.72M | 13.65M | 794.37M |
| Output | 2.37M | 0.49M | 2.86M |
| Reasoning | 5.99M | 0.51M | 6.51M |

Cache hit rate: 95.4%. Reasoning is ~69% of all generated tokens.

### By session (millions of tokens, compaction excluded)

| Session | Turns | Active h | Prompts | Uncached in | Cache read | Output | Reasoning |
|---|---|---|---|---|---|---|---|
| ROM investigation | 288 | 2.1 | 7 | 1.1 | 26.1 | 0.11 | 0.24 |
| Narration decoding | 1,031 | 7.2 | 17 | 6.2 | 111.3 | 0.32 | 1.88 |
| Translation: M10 / late bank | 3,174 | 17.2 | 43 | 19.4 | 371.8 | 1.42 | 2.64 |
| Status labels QA | 1,566 | 8.2 | 20 | 6.4 | 168.7 | 0.29 | 0.84 |
| Truncated Yes button | 328 | 2.0 | 10 | 1.3 | 30.1 | 0.06 | 0.11 |
| Dumping JP storyline | 696 | 2.5 | 19 | 2.7 | 72.0 | 0.16 | 0.28 |
| Name selection plan | 20 | 0.1 | 3 | 0.05 | 0.7 | ~0 | ~0 |

Reverse-engineering-heavy sessions think far more than they write (narration decoding: reasoning ≈ 6x output; translation: ≈ 1.9x).

### By day (UTC-3, compaction excluded)

| Day | Turns | Active h | Uncached in | Cache read | Output | Reasoning |
|---|---|---|---|---|---|---|
| Sat 17 | 604 | 3.9 | 3.0M | 49.7M | 0.21M | 0.73M |
| Sun 18 | 839 | 7.1 | 8.5M | 97.8M | 0.62M | 1.39M |
| Mon 19 | 2,876 | 14.6 | 14.9M | 340.6M | 1.00M | 2.57M |
| Tue 20 | 1,740 | 9.0 | 6.7M | 189.8M | 0.32M | 0.91M |
| Wed 21 | 1,044 | 4.6 | 4.0M | 102.9M | 0.23M | 0.39M |

### By model

| Model (variant) | Turns | Active h | Output/turn | Reasoning/turn | Avg context | Median gen. speed |
|---|---|---|---|---|---|---|
| big-pickle | 392 | 2.6 | 335 | 650 | 80k | ~38 tok/s |
| deepseek-v4.1-flash-free (default) | 126 | 0.6 | 202 | 320 | 79k | ~33 tok/s |
| deepseek-v4.1-flash-free (max) | 6,585 | 36.1 | 336 | 866 | 118k | ~64 tok/s |

### Where the 39.3 active hours went

| | Hours |
|---|---|
| Model generation | ~32.7 |
| Tool execution | ~3.1 (shell 2.9, of which `mgba_dump` ~2.0) |
| Two stalled turns (no output; one hung 2.3 h until aborted) | ~2.95 |
| Waiting on user answers (`question` tool) | ~0.5 |

### Tool usage

| Tool | Calls | Errors |
|---|---|---|
| shell | 4,786 | 181 non-zero exits (3.8%) |
| read | 1,868 | 41 (2.2%) |
| edit | 620 | 20 (3.2%) |
| execute | 269 | 0 |
| write | 96 | 1 |
| grep / websearch / webfetch / todowrite / skill / question | 39 / 36 / 7 / 11 / 8 / 7 | 1 websearch |

Shell commands by purpose: inline Python 43%, inspect/search 18%, project pipeline scripts 16%, `mgba_dump` (custom headless emulator dumper) 14.5% of calls but ~70% of shell time (~10.6 s each), custom disassembler 4.7%. 49 distinct `tools/*.py` scripts were invoked.

Edits: 716 edits/writes across 86 files. `WIKI.md` alone took 244 edits and 134 reads (used as persistent memory across compactions). Markdown is 49% of edits, Python 37%.

79% of turns contain no visible text; the model communicates almost entirely through tool calls.

### Hypothetical API cost

Actual cost was $0 (free tier). At list prices from the OpenCode model catalog (reasoning billed as output): ~$27 on paid `deepseek-v4.1-flash`, ~$214 on `deepseek-v4-pro`, ~$300 on `glm-5.3`. Cache reads dominate the pricier tiers.


# Probably not worth it for romhacking

This game is not text heavy. Google says it can take 15 hours to beat it, but I'm guessing that's mostly grinding. The models made some mistakes here and there that later took hours to find the root cause and a fix. Mistakes in RE, mistakes in tool creation, and deepseek even misread a guide it had fetched for the game. These models are not bad, absolutely not. I did jackshit here besides playing the game (and cheating at that), and this took only 4 days!

But it so happens most games people want translated when it comes to retro stuff are quite text heavy. And the actual translation produced here was pretty fucking awful. I later reran it through a more capable model (Claude Sonnet), yet it still was pretty awkward, although better. General RE work, on the other hand; go for it.
