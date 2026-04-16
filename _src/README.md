# Internal source infrastructure

`_src/` contains the internal machinery that supports the Manasource content repository while keeping the repo root clean.

## Subsystems

- `workflow/` — the human-readable operating manual for how sourcing work is done
- `sourcing/` — validated editorial provenance and per-resource research history
- `leads/` — raw candidate leads and future ingestion config
- `scripts/` — helper scripts for migration, reconciliation, pruning, and lead ingestion

## Contract

- Nothing in `_src/` is part of the publishable resource surface
- `resources/` remains the canonical public content area
- If a file exists mainly to help humans or tooling maintain the corpus, it should usually live under `_src/`
