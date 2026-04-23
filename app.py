#!/usr/bin/env python3
"""
Research Projects — master runner.

Runs every generator in `generators/` sequentially, producing all the
DOCX and PDF research project documents into `files/`.

Usage:
    python3 app.py              # run every generator
    python3 app.py faith        # run only generators whose filename
                                # contains the given substring(s)
    python3 app.py mourice cat  # run any generator matching either token
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GENERATORS_DIR = ROOT / 'generators'
FILES_DIR = ROOT / 'files'

# Order matters: figure builders run before the generators that embed them.
RUN_ORDER = [
    'generate_mourice_diagrams.py',
    'generate_mourice_docx.py',
    'generate_mourice_pdf.py',
    'generate_mourice_cat_docx.py',
    'generate_mourice_cat_pdf.py',
    'generate_mourice_bbm433_cats.py',
    'generate_mourice_bbm433_summary.py',
    'generate_mourice_bbm433_pastpapers.py',
    'generate_sophie_research.py',
    'generate_sophie_pdf.py',
    'generate_calvince_docx.py',
    'generate_calvince_pdf.py',
    'generate_calvince_cat_docx.py',
    'generate_calvince_cat_pdf.py',
    'generate_agnetta_docx.py',
    'generate_james_ngovi_docx.py',
    'generate_james_ngovi_pdf.py',
    'generate_faith_docx.py',
    'generate_faith_pdf.py',
]


def _filter(scripts: list[str], tokens: list[str]) -> list[str]:
    if not tokens:
        return scripts
    tokens = [t.lower() for t in tokens]
    return [s for s in scripts if any(t in s.lower() for t in tokens)]


def main(argv: list[str]) -> int:
    FILES_DIR.mkdir(exist_ok=True)
    scripts = _filter(RUN_ORDER, argv[1:])
    if not scripts:
        print('No generators matched the given filter.')
        return 1
    print(f'Running {len(scripts)} generator(s)...\n')
    failures: list[tuple[str, str]] = []
    started = time.time()
    for i, name in enumerate(scripts, 1):
        path = GENERATORS_DIR / name
        if not path.exists():
            failures.append((name, 'script not found'))
            print(f'[{i}/{len(scripts)}] SKIP {name} (missing)')
            continue
        print(f'[{i}/{len(scripts)}] {name}')
        result = subprocess.run([sys.executable, str(path)], cwd=ROOT)
        if result.returncode != 0:
            failures.append((name, f'exit {result.returncode}'))
    elapsed = time.time() - started
    print(f'\nFinished in {elapsed:.1f}s — {len(scripts) - len(failures)} ok, '
          f'{len(failures)} failed.')
    for name, reason in failures:
        print(f'  FAIL {name}: {reason}')
    return 0 if not failures else 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
