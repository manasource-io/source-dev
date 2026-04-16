#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RESOURCES_ROOT = ROOT / 'resources'
SOURCING_ROOT = ROOT / '_src' / 'sourcing' / 'resources'


def public_ids() -> set[str]:
    ids = set()
    for md in RESOURCES_ROOT.rglob('*.md'):
        rel = md.relative_to(RESOURCES_ROOT)
        parts = rel.parts
        stem = md.stem
        if parts[0] == 'nutrition':
            category = parts[1]
            ids.add(f"{category[:-1] if category.endswith('s') else category}/{stem}")
        elif parts[0] == 'habits':
            ids.add(f'habit/{stem}')
        else:
            ids.add(f'{parts[0]}/{stem}')
    return ids


def sourcing_ids() -> set[str]:
    ids = set()
    if not SOURCING_ROOT.exists():
        return ids
    for d in SOURCING_ROOT.rglob('*'):
        if not d.is_dir() or d == SOURCING_ROOT:
            continue
        files = [c.name for c in d.iterdir() if c.is_file()]
        if 'source-checks.csv' in files or any(name.endswith('.md') for name in files):
            ids.add(d.relative_to(SOURCING_ROOT).as_posix())
    return ids


def main() -> None:
    pub = public_ids()
    src = sourcing_ids()
    print('Uncovered public resources:')
    for item in sorted(pub - src):
        print(item)
    print('\nSourcing records without public target:')
    for item in sorted(src - pub):
        print(item)


if __name__ == '__main__':
    main()
