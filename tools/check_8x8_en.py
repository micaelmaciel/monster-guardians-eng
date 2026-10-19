#!/usr/bin/env python3
"""QA checker for 8x8 English translation files.

Checks every translation TSV against build/8x8_corpus.tsv:

  * coverage: every corpus row of that region has an EN row
  * hard errors: EN longer than the JP code count on a `split` row
    (split pieces are read at fixed byte offsets and must keep their
    exact code count, padded with spaces at insertion time)
  * warnings: EN longer than the JP code count on len/slice/term rows
    (a display length is passed explicitly; the insertion stage must
    either pad or patch the length immediate)
  * display: any line longer than 30 glyphs (240 px / 8 px)
  * charset: characters outside ASCII plus the U+23CE line break

Usage: check_8x8_en.py translation/8x8_pool_en.tsv [...]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(ROOT, "build", "8x8_corpus.tsv")
NL = "\u23ce"


def load_corpus():
    rows = {}
    with open(CORPUS, encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            rows[p[0]] = dict(region=p[1], style=p[2], n=int(p[3]), text=p[7])
    return rows


def main(paths):
    corpus = load_corpus()
    total_err = 0
    total_warn = 0
    for path in paths:
        errors, warnings, over = [], [], []
        seen = set()
        with open(path, encoding="utf-8") as fh:
            next(fh)
            for line in fh:
                p = line.rstrip("\n").split("\t")
                if len(p) != 4:
                    errors.append(f"bad columns: {line!r}")
                    continue
                addr, n, jp, en = p[0], int(p[1]), p[2], p[3]
                seen.add(addr)
                row = corpus.get(addr)
                if row is None:
                    errors.append(f"{addr}: not in corpus")
                    continue
                if row["text"] != jp:
                    errors.append(f"{addr}: jp column does not match corpus")
                if len(en) > n:
                    if row["style"] == "split":
                        errors.append(
                            f"{addr}: split EN {len(en)} > {n}: {en}")
                    else:
                        over.append((addr, row["style"], n, len(en), en))
                for part in en.split(NL):
                    if len(part) > 30:
                        errors.append(
                            f"{addr}: line of {len(part)} glyphs: {part}")
                odd = {c for c in en if ord(c) > 126 and c != NL}
                if odd:
                    errors.append(
                        f"{addr}: non-ASCII {sorted(odd)}: {en}")
                if en == jp:
                    warnings.append(f"{addr}: untranslated (EN == JP)")
        region = None
        if seen:
            region = corpus[next(iter(seen))]["region"]
            missing = [a for a, r in corpus.items()
                       if r["region"] == region and a not in seen]
            if missing:
                errors.append(
                    f"{len(missing)} corpus rows missing, e.g. {missing[:5]}")
        total_err += len(errors)
        total_warn += len(warnings)
        print(f"== {os.path.basename(path)}")
        print(f"   rows {len(seen)}  errors {len(errors)}  "
              f"warnings {len(warnings)}  EN>n {len(over)}")
        for e in errors:
            print("   ERROR", e)
        for w in warnings:
            print("   WARN ", w)
        for o in over[:12]:
            print(f"   over  {o[0]} {o[1]} n={o[2]} en={o[3]}: {o[4]}")
        if len(over) > 12:
            print(f"   ... {len(over)-12} more over-length rows")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
