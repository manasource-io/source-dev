#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FOUND = ROOT / '_src' / 'leads' / 'reddit' / 'found.json'
HARVEST = ROOT / '_src' / 'sourcing' / 'harvest-log.csv'
RESULTS = ROOT / '_src' / 'leads' / 'reddit' / 'results'


def retained_files() -> set[str]:
    files = set()
    if HARVEST.exists():
        lines = HARVEST.read_text(encoding='utf-8').splitlines()[1:]
        for line in lines:
            if line.strip():
                files.add(line.split(',', 1)[0])
    return files


def main() -> None:
    keep = retained_files()
    for path in RESULTS.glob('*.txt'):
        if path.name not in keep:
            path.unlink()
    if FOUND.exists():
        data = json.loads(FOUND.read_text(encoding='utf-8'))
        data = {k: v for k, v in data.items() if Path(v.get('file', '')).name in keep}
        FOUND.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
