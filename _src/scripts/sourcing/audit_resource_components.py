#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COMPONENT_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
ALL_RESOURCES_ROOT = ROOT / 'resources'
PHASE1_DIRS = [
    ROOT / 'resources' / 'nutrition' / 'food',
    ROOT / 'resources' / 'nutrition' / 'supplements',
    ROOT / 'resources' / 'exercise',
]
SUBCATEGORY_REWRITES = {
    'fruits': 'fruit',
    'vegetables': 'vegetable',
    'grains': 'grain',
    'legumes': 'legume',
    'spices': 'spice',
    'proteins': 'protein',
    'juices': 'juice',
    'seeds-nuts': 'seed-nut',
}


def iter_phase1_resources() -> list[Path]:
    files: list[Path] = []
    for directory in PHASE1_DIRS:
        files.extend(sorted(directory.glob('*.md')))
    return files


def iter_all_resources() -> list[Path]:
    return sorted(ALL_RESOURCES_ROOT.rglob('*.md'))


def frontmatter_lines(path: Path) -> list[str]:
    lines = path.read_text(encoding='utf-8').splitlines()
    if not lines or lines[0].strip() != '---':
        raise ValueError('missing opening frontmatter delimiter')

    for index in range(1, len(lines)):
        if lines[index].strip() == '---':
            return lines[1:index]

    raise ValueError('missing closing frontmatter delimiter')


def parse_components(lines: list[str]) -> list[str] | None:
    for index, line in enumerate(lines):
        if not line.startswith('components:'):
            continue

        inline_value = line.split(':', 1)[1].strip()
        if inline_value:
            return [
                item.strip()
                for item in inline_value.strip('[]').split(',')
                if item.strip()
            ]

        components: list[str] = []
        for child in lines[index + 1 :]:
            stripped = child.strip()
            if not stripped:
                continue
            if stripped.startswith('- '):
                components.append(stripped[2:].strip())
                continue
            if not child.startswith(' '):
                break
        return components

    return None


def parse_scalar(lines: list[str], key: str) -> str | None:
    prefix = f'{key}:'
    for line in lines:
        if line.startswith(prefix):
            value = line.split(':', 1)[1].strip()
            return value or None
    return None


def validate_components(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        components = parse_components(frontmatter_lines(path))
    except ValueError as exc:
        return [str(exc)]

    if components is None:
        return ['missing components field']

    if len(components) < 2:
        errors.append('components must contain at least 2 entries')

    seen: set[str] = set()
    for component in components:
        if not COMPONENT_RE.match(component):
            errors.append(f'invalid component tag: {component}')
        if component in seen:
            errors.append(f'duplicate component tag: {component}')
        seen.add(component)

    return errors


def validate_subcategory(path: Path) -> list[str]:
    try:
        lines = frontmatter_lines(path)
    except ValueError as exc:
        return [str(exc)]

    subcategory = parse_scalar(lines, 'subCategory')
    if not subcategory:
        return []

    rewrite = SUBCATEGORY_REWRITES.get(subcategory)
    if rewrite:
        return [f'subCategory must be singular: use {rewrite} instead of {subcategory}']

    return []


def main() -> int:
    failures = []
    for path in iter_all_resources():
        errors = validate_subcategory(path)
        if errors:
            failures.append((path.relative_to(ROOT).as_posix(), errors))

    for path in iter_phase1_resources():
        errors = validate_components(path)
        if errors:
            failures.append((path.relative_to(ROOT).as_posix(), errors))

    if not failures:
        print(
            f'All {len(iter_phase1_resources())} phase 1 resources have valid components and all subCategory values are singular.'
        )
        return 0

    print('Invalid resource taxonomy frontmatter:')
    for rel_path, errors in failures:
        print(f'- {rel_path}')
        for error in errors:
            print(f'  - {error}')
    return 1


if __name__ == '__main__':
    sys.exit(main())
