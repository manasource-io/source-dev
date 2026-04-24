# manasource source

`source` is the standalone content repository for Manasource.

It remains **content-first** at the repo root:

- publishable markdown resource pages live in `resources/`
- internal authoring, sourcing, workflow, and lead-ingestion infrastructure lives in `_src/`
- no app runtime code belongs here

## Root structure

- `resources/`
- `_src/`

### Publishable content

`resources/` is the public knowledge surface consumed by downstream apps and sites.

Current resource buckets:

- `resources/nutrition/food`
- `resources/nutrition/diet`
- `resources/nutrition/supplements`
- `resources/exercise`
- `resources/abstinence`
- `resources/habits`
- `resources/restoration`
- `resources/circadian`
- `resources/wellbeing`

Each resource is a markdown file with frontmatter fields such as:

- `title`
- `category`
- `subCategory` (singular when present)
- `components` (required for phase 1 food, supplement, and exercise resources)
- `description`
- `benefits`
- `benefitLevel`
- `overallScore`
- `credibility`
- `lastResearched`
- `readiness`
- `references`

### Internal authoring infrastructure

`_src/` is the internal system that supports the content repo while keeping the root clean.

It is organized into:

- `_src/workflow/` — sourcing workflow, schema rules, taxonomy decisions, pruning policy, and migration notes
- `_src/sourcing/` — editorial provenance such as source-check history, freshness logs, audits, and dated research notes
- `_src/leads/` — raw candidate lead intake and future lead-source config
- `_src/scripts/` — helper scripts for sourcing migration, reconciliation, pruning, and lead ingestion

## Repo contract

- `resources/` should stay publishable and content-focused
- `_src/` should hold non-publishable operational material
- root-level operational sprawl should be avoided unless there is a strong reason

## Downstream consumption

The downstream website consumes this repository as a versioned build input.
`web` should pin a specific tag or commit via build-time configuration rather than reading a local checkout directly.
