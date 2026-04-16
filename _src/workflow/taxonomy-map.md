# Taxonomy map

This document defines the canonical resource-ID model for the `source` repository and records the main legacy-to-canonical rewrite decisions for the research migration.

## Canonical source of truth

The canonical identity of a resource is derived from its path under `resources/**`.

That means the filesystem in `source` is the source of truth for:

- resource category
- resource slug
- canonical ID used by sourcing records

Legacy `poc/research` paths should be rewritten to match the `source` filesystem, not the other way around.

## Canonical ID rules

### Top-level categories

These map directly from `resources/<category>/<slug>.md`:

- `abstinence/<slug>`
- `circadian/<slug>`
- `exercise/<slug>`
- `restoration/<slug>`
- `wellbeing/<slug>`

### Habits

Publishable files live in `resources/habits/<slug>.md`.

For sourcing IDs, the preferred canonical form is:

- `habit/<slug>`

This preserves continuity with much of the legacy editorial vocabulary while keeping the filesystem folder plural.

### Nutrition subdomains

`resources/nutrition/**` maps to canonical sourcing IDs as:

- `food/<slug>`
- `diet/<slug>`
- `supplement/<slug>`

## Current resource inventory summary

Current `resources/**` counts:

- abstinence: 3
- circadian: 2
- exercise: 33
- habits: 5
- nutrition/diet: 4
- nutrition/food: 40
- nutrition/supplements: 25
- restoration: 1
- wellbeing: 4
- total resources: 117

## Rewrite rules from known legacy drift

The following rewrites should be applied during sourcing migration unless a later content decision explicitly changes the destination taxonomy.

### Category rewrites

- `activity/infrared-light` → `exercise/infrared-light`
- `activity/sauna` → `exercise/sauna`
- `mind/sleep-quality` → `restoration/sleep-quality`
- `habits/sunlight-exposure` → `habit/sunlight-exposure`
- `habits/wake-time` → `circadian/wake-time`

### Folder vs ID normalization

- `resources/habits/<slug>.md` remains the publishable path
- sourcing records should normalize to `habit/<slug>`

## Ambiguous or duplicate concepts

### `social-connection`

Current publishable paths include both:

- `resources/habits/social-connection.md`
- `resources/wellbeing/social-connection.md`

This is an unresolved duplication.

For Pass A, do **not** silently collapse it.
Instead:

- record it as a known taxonomy conflict
- require Pass B migration work to choose one canonical sourcing target or explicitly document why both survive

### `info/fiber`

Legacy sourcing history includes `info/fiber`, but there is no matching publishable resource under `resources/**`.

For Pass A, treat it as a planned orphan case.
Pass B should either:

- promote it into a real publishable target, or
- archive its history under an orphan path in `_src/sourcing/`

## Migration rule

If a legacy sourcing artifact points to a path that does not exist in the canonical `resources/**` model, migration should do one of three things explicitly:

1. rewrite it to a canonical target
2. preserve it as an explicitly documented orphan
3. halt for manual review if the correct target is unclear

Silent drift is not acceptable.
