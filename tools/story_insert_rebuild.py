#!/usr/bin/env python3
"""Rebuild EN story item streams and 1:1 text runs from the constrained text.

The new text in translation/story_en_constrained.txt is the authoritative
screen layout.  We keep the visible non-text controls (timing, colour
spans, pauses) from the pre-constrained translation runs, regenerate
inserts and line breaks from the new text, and write:

  translation/story_en_items.json      insertion control stream
  translation/story_en_runs.json       one EN string per text item
  translation/late_story_en_items.json
  translation/late_story_en_runs.json

The *_runs_preconstrained.json files are the control-span templates and
must not be overwritten by this tool.
"""
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import story_en_export as sx

TEXT_RE = re.compile(r'\{\{(PLAYER|BEAST:(\d+)|WORD:(\d+))\}\}|\n')
TOK_RE = re.compile(r"\x00|[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*|[^\s]")
SCREEN_SEPS = {0x7531, 0x7532, 0x7533}
INSERTS = {0x753E, 0x753F, 0x7540}
SPAN_REMAP = {
    'Canon of the Heavens': 'Canon of the Sky',
    'sorcerer': 'Beast Tamer',
    'The Legendary Beast Tamer,': 'the Legendary Beast Tamer',
    'Then, from the next room,an old man appeared.':
        'Then an old man came out of the next room.',
    "yesterday's incident": 'the incident',
    'Legendary Beasts': 'legendary beast',
    'a violent power': 'a savage power',
    "Not good! This won't do!!": 'No, at this rate--!!',
    "What's happening!": 'How is this possible!',
}
SPAN_OPEN = {0x753B, 0x7535}
SPAN_CLOSE = {0x753C, 0x7536}


def parse_candidate(path):
    text = Path(path).read_text()
    main = text.split('\n# Dynamic inserts')[0]
    parts = re.split(r'(?m)^## (L?\d+)\s*$', main)
    out = {}
    for i in range(1, len(parts), 2):
        body = parts[i + 1].strip('\n')
        screens = [p.strip('\n') for p in re.split(r'\n\s*\n', body) if p.strip()]
        out[parts[i]] = screens
    return out


def split_screens(items):
    screens = []
    cur = []
    for it in items:
        if it[0] == 'ctl' and it[1] in SCREEN_SEPS:
            screens.append((cur, it))
            cur = []
        else:
            cur.append(it)
    screens.append((cur, None))
    return screens


def old_sequence(cur, old_runs, run_start):
    """-> list of ('t', text) / ('c', ctl), next run index."""
    seq = []
    ri = run_start
    for it in cur:
        if it[0] == 'text':
            seq.append(('t', old_runs[ri]))
            ri += 1
        else:
            seq.append(('c', it))
    return seq, ri


def old_plain_and_controls(seq):
    parts = []
    controls = []
    for kind, val in seq:
        if kind == 't':
            parts.append(val.replace('\n', ' '))
        else:
            off = sum(len(x) for x in parts)
            if val[1] in INSERTS:
                parts.append(' \x00 ')
            elif val[1] == 0x7530:
                parts.append(' ')
            else:
                controls.append((off, val))
                parts.append(' ')
    return ''.join(parts), controls


def old_spans(seq):
    """Collect 753B/753C colour spans and 7535/7536 pause spans."""
    spans = []
    stack = []
    for idx, (kind, val) in enumerate(seq):
        if kind == 'c' and val[1] in SPAN_OPEN:
            stack.append({'open_idx': idx, 'open': val, 'text': []})
        elif kind == 'c' and val[1] in SPAN_CLOSE and stack:
            sp = stack.pop()
            txt = []
            for k, v in seq[sp['open_idx'] + 1:idx]:
                if k == 't':
                    txt.append(v)
                elif v[1] in INSERTS:
                    txt.append('\x00')
            sp['close_idx'] = idx
            sp['close'] = val
            sp['old_text'] = ' '.join(''.join(txt).replace('\n', ' ').split())
            spans.append(sp)
    return spans


def tokenize_old(s):
    return list(TOK_RE.finditer(s))


def tokenize_candidate(raw):
    """[(text, start, end)] with each placeholder as a single \x00 token."""
    toks = []
    last = 0
    for m in TEXT_RE.finditer(raw):
        if m.start() > last:
            toks += [(t.group(), t.start(), t.end())
                     for t in TOK_RE.finditer(raw, last, m.start())]
        if m.group(0) != '\n':
            toks.append(('\x00', m.start(), m.end()))
        last = m.end()
    if last < len(raw):
        toks += [(t.group(), t.start(), t.end())
                 for t in TOK_RE.finditer(raw, last, len(raw))]
    return toks


def map_control_positions(old_plain, controls, new_raw):
    """Map old control boundaries to new raw offsets using token alignment."""
    if not controls:
        return []
    old_toks = tokenize_old(old_plain)
    new_toks = tokenize_candidate(new_raw)
    old_txt = [m.group() for m in old_toks]
    new_txt = [t[0] for t in new_toks]
    sm = difflib.SequenceMatcher(None, old_txt, new_txt, autojunk=False)
    match = {}
    for b in sm.get_matching_blocks():
        for k in range(b.size):
            match[b.a + k] = b.b + k

    def tok_index_for_off(off):
        lo, hi = 0, len(old_toks)
        while lo < hi:
            mid = (lo + hi) // 2
            if old_toks[mid].start() < off:
                lo = mid + 1
            else:
                hi = mid
        return lo

    out = []
    for off, it in controls:
        i = tok_index_for_off(off)
        if i in match:
            j = match[i]
        else:
            j = round(i / max(1, len(old_toks)) * len(new_toks))
            for d in range(1, len(old_toks) + 1):
                if i - d in match:
                    j = match[i - d]
                    break
                if i + d in match:
                    j = match[i + d]
                    break
        pos = new_toks[j][1] if j < len(new_toks) else len(new_raw)
        out.append((pos, it))
    return out


def norm_map(raw):
    """Normalize candidate text for phrase search.

    Newlines/whitespace collapse to one space; placeholders become \x01.
    Returns (normalized text, start map, end map) where the maps point back
    to raw offsets.
    """
    out = []
    starts = []
    ends = []
    prev_space = True

    def add(ch, a, b):
        nonlocal prev_space
        if ch.isspace():
            if not prev_space:
                out.append(' ')
                starts.append(a)
                ends.append(b)
                prev_space = True
        else:
            out.append(ch.lower())
            starts.append(a)
            ends.append(b)
            prev_space = False

    i = 0
    for m in TEXT_RE.finditer(raw):
        if m.start() > i:
            for k in range(i, m.start()):
                add(raw[k], k, k + 1)
        if m.group(0) != '\n':
            out.append('\x01')
            starts.append(m.start())
            ends.append(m.end())
            prev_space = False
        else:
            add(' ', m.start(), m.end())
        i = m.end()
    for k in range(i, len(raw)):
        add(raw[k], k, k + 1)
    return ''.join(out), starts, ends


def find_span(norm, nmap, old_text, search_from=0):
    """Find an old span phrase in normalized candidate text."""
    s = ' '.join(old_text.replace('\x00', '\x01').split()).lower()
    if not s:
        return None
    k = norm.find(s, search_from)
    if k < 0:
        return None
    starts, ends = nmap
    return k, k + len(s), starts[k], ends[k + len(s) - 1]


def build_screen(cur, old_runs, run_start, cand_screen):
    raw = cand_screen
    events = []  # (pos, priority, seq, kind, payload)
    seq = 0

    # Candidate inserts and manual line breaks.
    for m in TEXT_RE.finditer(raw):
        g = m.group(0)
        if g == '\n':
            events.append((m.start(), 2.0, seq, 'line', None))
        else:
            if m.group(1) == 'PLAYER':
                code, params = 0x7540, []
            elif m.group(1).startswith('BEAST'):
                code, params = 0x753E, [f'0x{int(m.group(2), 16):X}']
            else:
                code, params = 0x753F, [f'0x{int(m.group(3), 16):X}']
            events.append((m.start(), 1.0, seq, 'ctl', (code, params)))
        seq += 1

    seq_old, next_run = old_sequence(cur, old_runs, run_start)
    old_plain, all_controls = old_plain_and_controls(seq_old)

    # Generic controls: everything except line breaks, inserts, and spans.
    controls = [(off, it) for off, it in all_controls
                if it[1] != 0x7530 and it[1] not in INSERTS
                and it[1] not in SPAN_OPEN and it[1] not in SPAN_CLOSE]
    for pos, it in map_control_positions(old_plain, controls, raw):
        events.append((pos, 1.5, seq, 'ctl', (it[1], it[2])))
        seq += 1

    # Colour and pause spans: match the old span text in the new screen.
    norm, starts, ends = norm_map(raw)
    search_from = {}
    for sp in old_spans(seq_old):
        key = sp['old_text']
        found = find_span(norm, (starts, ends), key, search_from.get(key, 0))
        if not found and key in SPAN_REMAP:
            key2 = SPAN_REMAP[key]
            found = find_span(norm, (starts, ends), key2, search_from.get(key2, 0))
            if found:
                search_from[key2] = found[0] + 1
        if found:
            _, _, a, b = found
            search_from[key] = found[0] + 1
        else:
            continue
        open_pri = 3.0 if a < len(raw) and raw[a] == '\n' else 0.5
        close_pri = 0.0 if b < len(raw) and raw[b] == '\n' else 2.5
        events.append((a, open_pri, seq, 'ctl', (sp['open'][1], sp['open'][2])))
        seq += 1
        events.append((b, close_pri, seq, 'ctl', (sp['close'][1], sp['close'][2])))
        seq += 1

    # Walk the candidate text, emitting events and accumulating text runs.
    events.sort(key=lambda e: (e[0], e[1], e[2]))
    items = []
    runs = []
    buf = []
    ev_i = 0

    def flush():
        nonlocal buf
        if buf:
            items.append(('text',))
            runs.append(''.join(buf))
            buf = []

    i = 0
    while i <= len(raw):
        while ev_i < len(events) and events[ev_i][0] <= i:
            e = events[ev_i]
            kind = e[3]
            if kind == 'line':
                flush()
                items.append(('ctl', 0x7530, []))
            else:
                flush()
                code, params = e[4]
                items.append(('ctl', code, params))
            ev_i += 1
        if i == len(raw):
            break
        m = TEXT_RE.match(raw, i)
        if m:
            i = m.end()
            continue
        buf.append(raw[i])
        i += 1
    flush()
    return items, runs, next_run


def simulate(items, runs):
    out = []
    ri = 0
    for it in items:
        if it[0] == 'text':
            out.append(runs[ri])
            ri += 1
        else:
            c = it[1]
            if c == 0x7530:
                out.append('\n')
            elif c in (0x7531, 0x7532, 0x7533):
                out.append('\n\n')
            elif c == 0x7540:
                out.append('{{PLAYER}}')
            elif c == 0x753E:
                out.append('{{BEAST:%d}}' % int(it[2][0], 16))
            elif c == 0x753F:
                out.append('{{WORD:%d}}' % int(it[2][0], 16))
    return ''.join(out)


def main():
    cand = parse_candidate(ROOT / 'translation' / 'story_en_constrained.txt')
    out = {}
    warnings = []
    for bank, rawf, templatef, itemsf, runsf in [
        ('story', 'build/story_messages_raw.json',
         'translation/story_en_runs_preconstrained.json',
         'translation/story_en_items.json',
         'translation/story_en_runs.json'),
        ('late', 'build/late_story_raw.json',
         'translation/late_story_en_runs_preconstrained.json',
         'translation/late_story_en_items.json',
         'translation/late_story_en_runs.json'),
    ]:
        raws = json.load(open(ROOT / rawf))['messages']
        old = json.load(open(ROOT / templatef))
        out[bank] = []
        for idx, m in enumerate(raws):
            mid = f'{idx:02d}' if bank == 'story' else f'L{idx:02d}'
            items = sx.parse_message(m['raw'])
            screens = split_screens(items)
            cand_screens = cand[mid]
            text_screens = [k for k, (cur, sep) in enumerate(screens)
                            if any(it[0] == 'text' for it in cur)]
            if len(text_screens) != len(cand_screens):
                print('COUNT MISMATCH', mid, len(text_screens), len(cand_screens))
                return 1
            new_items = []
            new_runs = []
            run_start = 0
            ci = 0
            for k, (cur, sep) in enumerate(screens):
                if k in text_screens:
                    ni, nr, run_start = build_screen(
                        cur, old[str(idx)], run_start, cand_screens[ci])
                    new_items += ni
                    new_runs += nr
                    ci += 1
                else:
                    new_items += cur
                    for it in cur:
                        if it[0] == 'text':
                            run_start += 1
                if sep is not None:
                    new_items.append(sep)
            out[bank].append({'message': idx, 'items': new_items,
                              'runs': new_runs})

            sim = simulate(new_items, new_runs)
            want = '\n\n'.join(cand_screens)
            if sim.strip('\n') != want.strip('\n'):
                print('SIM MISMATCH', mid)
                print('SIM:', repr(sim[:800]))
                print('WANT:', repr(want[:800]))
                return 1

            # Report controls and placeholder counts.
            got = [it[1] for it in new_items if it[0] == 'ctl']
            nph = sum(1 for it in new_items if it[0] == 'ctl'
                      and it[1] in INSERTS)
            nlines = sum(1 for it in new_items if it[0] == 'ctl'
                         and it[1] == 0x7530)
            warnings.append((mid, len(new_runs), nlines, nph, len(got)))

    comment = ('English text per insertion text run. Generated from '
               'translation/story_en_constrained.txt; controls and line '
               'breaks are in the matching *_en_items.json. Do not hand-edit '
               'without updating both.')
    for bank, itemsf, runsf in [
        ('story', 'translation/story_en_items.json',
         'translation/story_en_runs.json'),
        ('late', 'translation/late_story_en_items.json',
         'translation/late_story_en_runs.json'),
    ]:
        items_msgs = []
        runs = {'_comment': comment}
        for m in out[bank]:
            raw = []
            for it in m['items']:
                if it[0] == 'text':
                    raw.append('0')
                else:
                    raw.append(f'0x{it[1]:04X}')
                    raw += it[2]
            items_msgs.append({'message': m['message'], 'raw': raw})
            runs[str(m['message'])] = m['runs']
        (ROOT / itemsf).write_text(
            json.dumps({'bank': bank, 'messages': items_msgs}, indent=1) + '\n')
        (ROOT / runsf).write_text(
            json.dumps(runs, ensure_ascii=False, indent=1) + '\n')
        print(f'wrote {itemsf} and {runsf}')
    for w in warnings:
        print('%s runs=%d lines=%d inserts=%d controls=%d' % w)
    return 0


if __name__ == '__main__':
    sys.exit(main())
