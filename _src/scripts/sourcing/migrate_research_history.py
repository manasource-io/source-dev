#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> None:
    print('This repository has already been seeded with the Pass B destination layout.')
    print('For future migrations, use explicit one-off scripts or repurpose reconcile/prune utilities in this directory.')
    print(f'Root: {ROOT}')


if __name__ == '__main__':
    main()
