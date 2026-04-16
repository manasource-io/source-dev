# Migration plan

This document defines Pass A of the research-to-source migration and sets the intended path for Pass B.

## Migration objective

Move research-related workflow, provenance, and lead-ingestion infrastructure out of `poc` and into `source` while keeping the repo root clean.

## Two-pass execution model

### Pass A

Pass A establishes the destination architecture and workflow canon.

Deliverables:

- `_src/workflow/`
- `_src/leads/`
- `_src/sourcing/`
- `_src/scripts/`
- root README updated to reflect the internal `_src` split
- workflow, schema, taxonomy, pruning, and migration docs written in the destination repo

Pass A intentionally does **not** migrate all historical data or refactor the lead scripts yet.

### Pass B

Pass B performs the heavy migration and implementation work.

Planned scope:

- migrate legacy sourcing history from `poc/research`
- rewrite legacy IDs to canonical IDs derived from `resources/**`
- reconcile uncovered resources and explicit orphans
- migrate and prune retained lead artifacts from `poc/research-finding`
- refactor lead scripts into `_src/scripts/`
- replace hardcoded single-subreddit assumptions with config-driven intake

## Why the split exists

The split is primarily about:

- reviewability
- reversibility
- making taxonomy decisions explicit before they are encoded in migrated data

It is safer to finalize the destination rules before moving historical artifacts into them.

## Main known migration issues

### Known legacy drift

- `activity/infrared-light`
- `activity/sauna`
- `mind/sleep-quality`
- mixed `habit` vs `habits`
- unresolved duplicate `social-connection`
- orphaned `info/fiber`

### Pass B requirements

Pass B should not silently preserve any of these mismatches.
Every mismatch should be:

- rewritten
- documented as an orphan
- or flagged for explicit manual review

## Pass A completion criteria

Pass A is complete when:

- the repo has the destination `_src` scaffolding
- the root README documents the new contract
- workflow rules exist in the destination repo
- taxonomy and pruning rules are explicit enough to guide Pass B

## Pass B completion criteria

Pass B should leave the repo in a state where:

- `source` is the canonical home of the content and its sourcing machinery
- no active sourcing records point to deprecated legacy IDs
- lead intake targets the new structure rather than `poc`
- raw lead clutter is reduced to a maintainable active corpus plus any intentional archive
