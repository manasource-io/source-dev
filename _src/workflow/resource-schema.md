# Resource schema

This document defines the content contract for publishable resource pages in `resources/**`.

## Scope

This schema applies to public resource markdown files, not internal sourcing artifacts.

## Required shape

Each resource should be a markdown file with YAML frontmatter followed by a body.

Typical frontmatter fields include:

- `draft`
- `title`
- `category`
- `subCategory`
- `components`
- `description`
- `score`
- `updatedAt`
- `createdAt`
- `associations`
- `claims`
- `references`

## Frontmatter expectations

### `subCategory`

`subCategory` remains an editorial/display field.

When present, keep it singular and lower-case kebab-case.

Examples:

- `vegetable`
- `fruit`
- `legume`
- `seed-nut`

### `components`

For phase 1 food, supplement, and exercise resources, `components` is required.

Use an ordered `components` list as the machine-readable taxonomy layer.

See [`resource-components.md`](./resource-components.md) for:

- ordering rules
- required scope
- examples
- authoring guidance

Do not start `components` with a broad family tag that simply repeats what `category` or `subCategory` already says.

When adding or backfilling phase 1 resources, verify the field with:

`python3 _src/scripts/sourcing/audit_resource_components.py`

### `description`

- concise
- human-readable
- focused on what the resource is and does
- should not become a long disclaimer block

### `claims`

Claims should be structured entries with stable IDs that map to headings in the body.

Expected shape:

```yaml
claims:
  - id: blood-sugar-control
    label: Improves post-meal glucose control in randomized feeding trials
```

Rules:

- use stable kebab-case IDs
- keep each `label` between 30 and 80 characters inclusive
- do not repeat the resource title inside the claim label
- each claim ID should have a matching body section anchor
- `benefits` is a legacy field name and should not be used in new or updated files

### `draft`

Optional boolean flag.

Rules:

- place it at the top of the frontmatter, above `title`
- default new documents to `true`
- set `draft: false` only when the page is ready to publish as a public resource

### `score`

The single top-line editorial score for the resource.

Use an integer score when the resource has enough evidence and editorial coverage to justify one.

`score` replaces older multi-field rating patterns such as `benefitLevel`, `overallScore`, and `credibility`.

### `updatedAt`

Should be updated when the resource is materially reviewed or improved through sourcing work.

### `createdAt`

Should reflect the document creation date.

Use ISO date form (`YYYY-MM-DD`).

### `associations`

Associations are the standardized cross-resource effect tags that power shared UI rendering and comparison.

Expected shape:

```yaml
associations:
  - id: mortality
    delta: -5
    benefit: 5
    trust: 3
```

Rules:

- place `associations` above `claims`
- use only standardized IDs from the shared registry in `data/src/associations.ts`
- each entry must include `id`, `delta`, `benefit`, and `trust`
- `delta` ranges from `-5` to `5`
- `benefit` ranges from `0` to `5`
- `trust` ranges from `1` to `5`
- the old association key `level` has been renamed to `benefit`

The shared association registry also assigns each ID a priority from `1` to `6`.

- priorities `1` to `5` are the normal range
- priority `6` is reserved for special associations that should be rendered above the others
- `mortality` is the current highest-priority association

## References

References should use structured objects rather than raw strings whenever a resource is touched.

Preferred shape:

```yaml
references:
  - title: Example paper title
    url: https://pubmed.ncbi.nlm.nih.gov/12345678/
    date: 2024-01-15
```

### Reference rules

- order matters if body prose cites references by position
- use the smallest stable set of strong references needed to support the page
- prefer primary literature, systematic reviews, and major journals where practical
- include `title` and `date` whenever they can be verified reliably

## Body requirements

A resource body should:

- explain the resource in readable terms
- map clearly to the declared claims
- avoid overstating evidence
- maintain section anchors that match claim IDs when claim deep-linking is used

## YAML safety

Quote frontmatter strings when they contain punctuation or structure that could make YAML ambiguous.

Common cases include:

- titles containing `: `
- values starting with reserved YAML punctuation
- any string where quoting is the clearest and safest choice

## Boundary rule

Do not store sourcing notes, research-session logs, or lead-harvest artifacts inside publishable resource files.
Those belong in `_src/sourcing/` or `_src/leads/`.
