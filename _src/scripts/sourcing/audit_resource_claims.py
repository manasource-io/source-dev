#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ALL_RESOURCES_ROOT = ROOT / "resources"
CLAIM_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EXPLICIT_ANCHOR_RE = re.compile(r"\{#([a-z0-9]+(?:-[a-z0-9]+)*)\}")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TOP_LEVEL_KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*:")
MIN_LABEL_LENGTH = 30
MAX_LABEL_LENGTH = 80


def iter_all_resources() -> list[Path]:
    return sorted(ALL_RESOURCES_ROOT.rglob("*.md"))


def split_frontmatter(path: Path) -> tuple[list[str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], lines[index + 1 :]

    raise ValueError("missing closing frontmatter delimiter")


def parse_scalar(lines: list[str], key: str) -> str | None:
    prefix = f"{key}:"
    for line in lines:
        if line.startswith(prefix):
            value = line.split(":", 1)[1].strip()
            return unquote(value) if value else None
    return None


def has_legacy_benefits(lines: list[str]) -> bool:
    return any(line.startswith("benefits:") for line in lines)


def parse_key_value(line: str) -> tuple[str, str] | None:
    if ":" not in line:
        return None

    key, value = line.split(":", 1)
    return key.strip(), unquote(value.strip())


def parse_claims(lines: list[str]) -> tuple[list[dict[str, str]] | None, list[str]]:
    for index, line in enumerate(lines):
        if not line.startswith("claims:"):
            continue

        inline_value = line.split(":", 1)[1].strip()
        if inline_value == "[]":
            return [], []
        if inline_value:
            return None, ["claims must be a YAML list of id/label objects"]

        claims: list[dict[str, str]] = []
        current: dict[str, str] | None = None

        for child in lines[index + 1 :]:
            stripped = child.strip()
            if not stripped:
                continue
            if TOP_LEVEL_KEY_RE.match(child):
                break
            if child.startswith("- "):
                if current is not None:
                    claims.append(current)
                current = {}
                parsed = parse_key_value(child[2:].strip())
                if parsed:
                    key, value = parsed
                    current[key] = value
                continue
            if child.startswith("  "):
                if current is None:
                    return None, ["claims entries must begin with a list item"]
                parsed = parse_key_value(stripped)
                if parsed is None:
                    return None, [f"invalid claims entry: {stripped}"]
                key, value = parsed
                current[key] = value
                continue
            return None, [f"invalid claims indentation: {child}"]

        if current is not None:
            claims.append(current)

        return claims, []

    return None, []


def extract_body_anchors(body_lines: list[str]) -> set[str]:
    body_text = "\n".join(body_lines)
    anchors = set(EXPLICIT_ANCHOR_RE.findall(body_text))

    for line in body_lines:
        stripped = line.strip()
        match = HEADING_RE.match(stripped)
        if not match:
            continue

        heading = EXPLICIT_ANCHOR_RE.sub("", match.group(2)).strip()
        heading = re.sub(r"`([^`]*)`", r"\1", heading)
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        heading = re.sub(r"[*_~]", "", heading)
        slug = slugify(heading)
        if slug:
            anchors.add(slug)

    return anchors


def normalize_label(value: str) -> str:
    return " ".join(value.split())


def normalize_phrase(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.lower())).strip()


def build_title_phrases(title: str) -> set[str]:
    normalized_title = normalize_phrase(title)
    if not normalized_title:
        return set()

    phrases = {normalized_title}
    tokens = normalized_title.split()
    last = tokens[-1]

    singular_last = singularize_token(last)
    if singular_last != last:
        phrases.add(" ".join([*tokens[:-1], singular_last]))

    plural_last = pluralize_token(last)
    if plural_last != last:
        phrases.add(" ".join([*tokens[:-1], plural_last]))

    return {phrase for phrase in phrases if phrase}


def singularize_token(token: str) -> str:
    if token.endswith("ies") and len(token) > 3:
        return token[:-3] + "y"
    if token.endswith("s") and not token.endswith("ss") and len(token) > 1:
        return token[:-1]
    return token


def pluralize_token(token: str) -> str:
    if token.endswith("y") and len(token) > 1 and token[-2] not in "aeiou":
        return token[:-1] + "ies"
    if token.endswith("s"):
        return token
    return token + "s"


def slugify(value: str) -> str:
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", value.lower()))


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def validate_claims(path: Path) -> list[str]:
    try:
        frontmatter, body = split_frontmatter(path)
    except ValueError as exc:
        return [str(exc)]

    errors: list[str] = []
    readiness = parse_scalar(frontmatter, "readiness")
    resource_title = parse_scalar(frontmatter, "title")
    title_phrases = build_title_phrases(resource_title or "")

    if has_legacy_benefits(frontmatter):
        errors.append("legacy benefits field present; use claims instead")

    claims, parse_errors = parse_claims(frontmatter)
    errors.extend(parse_errors)

    if readiness == "ready" and claims is None:
        errors.append("ready resources must declare claims")

    if claims is None:
        return errors

    anchors = extract_body_anchors(body)
    seen_ids: set[str] = set()

    for index, claim in enumerate(claims, start=1):
        claim_id = claim.get("id", "")
        label = normalize_label(claim.get("label", ""))
        claim_name = claim_id or f"claim #{index}"

        if not claim_id:
            errors.append(f"{claim_name} is missing an id")
        elif not CLAIM_ID_RE.match(claim_id):
            errors.append(f"{claim_name} has an invalid id format")
        elif claim_id in seen_ids:
            errors.append(f"{claim_name} is duplicated")
        elif claim_id not in anchors:
            errors.append(f"{claim_name} is missing a matching body anchor")

        if claim_id:
            seen_ids.add(claim_id)

        if not label:
            errors.append(f"{claim_name} is missing a label")
            continue

        normalized_label = normalize_phrase(label)
        if any(f" {phrase} " in f" {normalized_label} " for phrase in title_phrases):
            errors.append(
                f"{claim_name} repeats the resource title; rewrite the claim without naming the resource"
            )

        label_length = len(label)
        if label_length < MIN_LABEL_LENGTH or label_length > MAX_LABEL_LENGTH:
            errors.append(
                f"{claim_name} label length {label_length} is outside "
                f"{MIN_LABEL_LENGTH}-{MAX_LABEL_LENGTH} characters"
            )

    return errors


def main() -> int:
    failures = []
    resources = iter_all_resources()

    for path in resources:
        errors = validate_claims(path)
        if errors:
            failures.append((path.relative_to(ROOT).as_posix(), errors))

    if not failures:
        print(
            f"All {len(resources)} resources use valid claims metadata and ready-resource claim labels stay within {MIN_LABEL_LENGTH}-{MAX_LABEL_LENGTH} characters."
        )
        return 0

    print("Invalid resource claims frontmatter:")
    for rel_path, errors in failures:
        print(f"- {rel_path}")
        for error in errors:
            print(f"  - {error}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
