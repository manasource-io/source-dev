# Internal scripts

`_src/scripts/` holds helper scripts that support the source repository.

These scripts should serve one of four purposes:

- migrate legacy research artifacts into canonical `source` structures
- reconcile resource IDs and taxonomy drift
- prune or classify raw lead caches
- ingest new candidate leads into `_src/leads/`

## Layout

- `leads/` — lead-ingestion and lead-cache utilities
- `sourcing/` — migration, audit, reconciliation, and pruning helpers

## Boundaries

- no app runtime code belongs here
- scripts should target files inside this repository only
- when a script encodes a durable rule, the matching rule should also be documented in `_src/workflow/`
