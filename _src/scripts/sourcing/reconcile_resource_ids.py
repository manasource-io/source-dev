#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RESOURCE_LOG = ROOT / '_src' / 'sourcing' / 'resource-log.csv'
HARVEST_LOG = ROOT / '_src' / 'sourcing' / 'harvest-log.csv'

REWRITES = {
    'activity/infrared-light': 'exercise/infrared-light',
    'activity/sauna': 'exercise/sauna',
    'mind/sleep-quality': 'restoration/sleep-quality',
    'habits/wake-time': 'circadian/wake-time',
}


def normalize_id(resource_id: str) -> str:
    resource_id = resource_id.strip()
    if resource_id in REWRITES:
        return REWRITES[resource_id]
    if resource_id.startswith('habits/'):
        return f"habit/{resource_id.split('/', 1)[1]}"
    if resource_id == 'info/fiber':
        return 'orphan/info-fiber'
    return resource_id


def rewrite_csv(path: Path, field: str, multi: bool = False) -> None:
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if multi:
                values = [normalize_id(v) for v in row[field].split(',') if v.strip()]
                row[field] = ','.join(values)
            else:
                row[field] = normalize_id(row[field])
            rows.append(row)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if RESOURCE_LOG.exists():
        rewrite_csv(RESOURCE_LOG, 'resourceID')
    if HARVEST_LOG.exists():
        rewrite_csv(HARVEST_LOG, 'resourceIDs', multi=True)


if __name__ == '__main__':
    main()
