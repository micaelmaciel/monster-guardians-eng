# Story terms reused outside the story

**Scope (per user, 2026-10-21).** This is not a general UI glossary. It lists
only English terms that were chosen in the 16×11 story script and then reused
in another text system: battle missions, clear conditions, event/menu labels,
or the monster database. Generic UI-only vocabulary (`Yes`/`No`, stat labels,
`Element`, `Item`, etc.) is deliberately excluded.

**Method.** For each candidate, the Japanese form in
`translation/story_jp.txt` was searched across the 8×8 banks
(`8x8_*_en.tsv`), the message-box bank (`msgfont_en.tsv`), and the late-story
bank. Only cases where the same English form is actually reused are listed.
Known divergences are called out at the end.

## 1. Names and places

| JP in story | English kept | Also used in | Notes |
|---|---|---|---|
| ベリンガム | **Beringham** | 8×8 battle mission (`Defeat Beringham!`), message-box clear condition (`Goal: Defeat Beringham!`), pool event titles (`Beringham Plot`, `Beringham's Bet`) | Story also has `Lord Beringham` and `Duke Beringham Roe`; keep the element **Beringham**. `Beringham Plot` is shortened for the 19-glyph event-replay row. |
| イグニス | **Ignis** | battle mission (`Beat revived Ignis!`), clear condition (`Goal: Defeat Ignis!`), pool event titles (`Ignis Awakens`, `Ignis Falls`), monster DB | |
| 大地のイグニス | **Ignis of the Earth** | pool legendary-monster setup | The monster DB shortens this to `Ignis` because of its 8-glyph name slot; see exceptions. |
| カノン | **Canon** | pool default-name table (`Leo`, `Tina`, `Canon`, `Beffle`, `Farbus`) | The table entry is a default name, not necessarily the sky dragon itself. |
| ザーゴ | **Zargo** | battle missions, message-box clear conditions, pool event titles, pool monster list, monster DB | Some clear-condition JP rows spell it サーゴ; the English is normalized to **Zargo**. |
| ラミレス | **Ramires** | battle missions, message-box clear conditions, pool event title (`Zargo/Ramires`), pool monster list, monster DB | The event-replay row shortens `Zargo and Ramires` to `Zargo/Ramires`. |
| ファムファンタル火山 | **Mount Famfantar** | pool event title (`Mt. Famfantar`) | The event-replay row shortens `To Mount Famfantar` to `Mt. Famfantar`. |
| 伝説の魔獣 | **Legendary Beast** | pool prompt (`Pick a legendary beast.`), pool category label `Legend` | Lowercase in the prompt, title case in story. |

## 2. Story terminology reused in UI

| JP in story | English kept | Also used in | Notes |
|---|---|---|---|
| 魔獣 | **beast** | message-box clear conditions (e.g. `Defeat the attacking beasts!`), 8×8 battle missions (e.g. `Wipe out the beasts!`), pool labels (`No Beasts 1/2/3`, `The Combined Beast`) | The story uses **beast**, never `monster`. Capitalize only in standalone labels. |
| 合成 | **combine** / **combining** | pool label `Combine`, puzzle/room names `Combine Room` and `Combine Shop`, item descriptions (`Combining keeps the attribute`, `Affects the combine result`, `Equip to combine`) | Story uses the verb (`combine`, `combining`, `combined`); UI uses the short label `Combine`. The story's 合獣機 (**beast combining machine**) is the full machine name and has no UI equivalent; see section 5. |

`Monster` is **not** on this list: the story never uses モンスター. That is a
UI-only rendering of モンスター and is kept separate from the story's
魔獣 = **beast**.

## 3. Monster names inserted into story text

These are the 9 slots of the 753E story-insert table (two variants each).
Every short English name below is also the name used in
`translation/8x8_mdb_en.tsv`.

| Slot | JP variants | English used in story | Cross-system note |
|---:|---|---|---|
| 0 | ゴーレムライト / ゴブリンフライ | `GolmLite` / `GobFly` | Both match the monster DB. |
| 1 | ホワイトドラゴン / ブラックドラゴン | `WhiteDrg` / `BlackDrg` | Both match the monster DB. |
| 2 | リトルガウ / チンビュアリー | `LilGau` / `ChinVury` | Both match the monster DB. |
| 3 | リトルガウ / チンビュアリー | `LilGau` / `ChinVury` | Same pair as slot 2. |
| 4 | こあくま / ハイエルフ | `Imp` / `HighElf` | Both match the monster DB. |
| 5 | メインガウ / リンビュアリー | `MainGau` / `LinVury` | Both match the monster DB. |
| 6 | メインガウ / リンビュアリー | `MainGau` / `LinVury` | Same pair as slot 5. |
| 7 | LV15以上のミノドラゴン / LV15以上のドラグリフォン | `Lv15+ MinoDrag` / `Lv15+ DragGrif` | The names match the DB; `Lv15+` is added only in the story insert. |
| 8 | ヘビーガウ / メインビュアリー | `HeavyGau` / `MainVury` | Both match the monster DB. |

## 4. Story-only recurring terms

These recur in the story but have no matching use in the 8×8 or message-box
banks, so changing them does not create cross-system edits (they will still
recur in the story text itself):

- クリムト — **Kurimuto**
- ウィンスロー — **Winslow** (`Winslow I`, `Winslow II`)
- バルロア — **Barroa** (`Kingdom of Barroa`)
- グランデート — **Grandate** (`continent of Grandate`)
- ヴァンダム — **Vandam** (`Vandam Castle`)
- タクト — **Takt**
- 魔獣使い — **Beast Tamer**
- 伝説の魔獣使い — **Legendary Beast Tamer**
- 魔獣騎士団 — **Beast Knight Order**
- 魔獣人間 — **beast-human**
- 合獣機 — **beast combining machine**

## 5. Exceptions and known mismatches

- **ハイドラゴン** — story uses **hydra dragon**, but the monster DB uses
  **HighDrg** for the same Japanese species name. This is the one real
  cross-system naming conflict, not just an abbreviation. Pick one
  interpretation: keep *hydra dragon* in story and use a DB short form such
  as `HydraDrg`, or change the story to *High Dragon*.
- **大地のイグニス** — story and pool use **Ignis of the Earth**; the monster
  DB uses **Ignis** to fit the 8-glyph slot. This is an intentional short
  form, not a different term.
- **カノン** — the pool default name and the story dragon share the spelling
  **Canon**, but they are not necessarily the same entity. Keep the spelling
  consistent anyway.
- **モンスター** — UI normally uses **Monster**, but one pool label
  (`0x0BD48C`) uses **Beast**. That is a UI-only outlier, not a story term.
- **`Combine` vs `beast combining machine`** — the UI has no full name for
  the machine, only `Combine Room` / `Combine Shop`. Do not rename the story
  compound to `Combine Machine` unless the UI strings are changed too.
