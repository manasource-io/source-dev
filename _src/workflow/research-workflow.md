# Research workflow

This document defines the operating sequence for maintaining the Manasource source corpus.

The workflow exists to improve `resources/**` using validated evidence while keeping a durable editorial trail in `_src/sourcing/`.

## Primary goal

Each sourcing run should leave the corpus more reliable, more current, or more complete than before.

A successful run usually does at least one of these:

- removes or downgrades weak references
- adds stronger supporting references
- updates stale resource content to reflect better evidence
- records durable sourcing notes that make later work faster and safer

## Workflow phases

### Phase 1 — pick targets

Select work from one or more of these queues:

- stale resources from `_src/sourcing/resource-log.csv`
- uncovered resources that exist in `resources/**` but have no sourcing history yet
- high-signal candidate leads from `_src/leads/`
- known audit backlog from `_src/sourcing/audits/`

Prefer resources with either:

- no sourcing history yet
- the oldest last-reviewed dates
- suspicious references
- clear evidence gaps relative to their current claims

### Phase 2 — source-check existing references

Before adding new material, review the references already attached to the resource.

For each existing reference:

1. confirm it resolves
2. confirm it is relevant to the claim it supports
3. confirm it is credible enough for the claim strength being made
4. record the outcome in the resource's `source-checks.csv`

Possible outcomes usually include:

- valid
- removed
- pending

If a reference is weak, misleading, unrelated, or redundant, remove or replace it.

### Phase 3 — harvest new leads

Review candidate material from `_src/leads/`.

For each lead under consideration:

1. identify the likely target resource or resources
2. extract any cited papers, institutional sources, or other evidence-bearing links
3. ignore sensational framing and evaluate the underlying sources directly
4. decide whether the lead is:
   - actionable now
   - useful later
   - low-value noise to archive or prune

Only validated findings should influence `resources/**`.

### Phase 4 — update the resource

Apply validated findings to the target markdown file in `resources/**`.

Typical updates include:

- replacing weak references with better ones
- improving frontmatter completeness
- adding or correcting `components` for phase 1 food, supplement, and exercise resources
- normalizing any `subCategory` values to singular form
- clarifying benefits, caveats, or mechanism sections
- tightening unsupported language
- updating `lastResearched`

All public-facing claims should remain proportional to the evidence quality.

### Phase 5 — record provenance

After touching a resource, update `_src/sourcing/`:

- append or update `source-checks.csv`
- create or update a dated research note
- update the freshness log
- record lead usage in `harvest-log.csv` if a harvested lead materially informed the update

The goal is that a later editor can understand **what changed, why it changed, and what sources were trusted or rejected**.

### Phase 6 — verify

Before concluding work, verify:

- the resource still parses as valid markdown + frontmatter
- phase 1 resources touched still satisfy the `components` contract
- any `subCategory` values touched remain singular
- every new reference was actually checked
- the sourcing notes match the resource changes
- no raw lead artifact was mistaken for validated evidence
- the resource's claims remain consistent with the evidence grading rules

## Output boundaries

### `resources/`

Only publishable content belongs here.

### `_src/sourcing/`

Validated editorial provenance belongs here.

### `_src/leads/`

Raw candidate input belongs here.

### `_src/workflow/`

Rules, contracts, and operating docs belong here.

## Minimal checklist for a sourcing run

- picked a real target resource or explicit orphan case
- checked existing references before adding new ones
- validated all new evidence directly
- updated the publishable resource only after validation
- added or preserved `components` on any phase 1 resource touched
- kept `subCategory` singular anywhere it is present
- recorded provenance in `_src/sourcing/`
- left the corpus clearer than it was before the run
