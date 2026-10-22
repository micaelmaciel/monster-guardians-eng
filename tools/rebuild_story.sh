#!/usr/bin/env bash
# Rebuild the English patch after editing translation/story_en_constrained.txt.
#
#   tools/rebuild_story.sh            regenerate text + run QA + build patch
#   tools/rebuild_story.sh --no-build regenerate text + run QA only
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"

BUILD=1
if [[ "${1:-}" == "--no-build" ]]; then
    BUILD=0
elif [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    sed -n '2,6p' "$0"
    exit 0
elif [[ $# -gt 0 ]]; then
    echo "usage: $0 [--no-build]" >&2
    exit 2
fi

step() { printf '\n==> %s\n' "$*"; }

step "Regenerating story item streams and runs"
"$PY" tools/story_insert_rebuild.py

step "Exporting and QA-checking the early bank"
"$PY" tools/story_en_export.py --bank story

step "Exporting and QA-checking the late bank"
"$PY" tools/story_en_export.py --bank late

step "Checking real insert widths"
"$PY" tools/check_insert_rows.py

step "Checking the encoded story streams"
"$PY" tools/insert_story.py --check

if (( BUILD )); then
    step "Building the patched ROM and BPS"
    "$PY" tools/build_patch.py --stage all
    printf '\nDone: dist/monster-guardians-en.bps\n'
else
    printf '\nText checks passed (patch not rebuilt).\n'
fi
