# Sourcing scripts

This directory is reserved for scripts that help maintain sourcing integrity.

Planned responsibilities:

- migrate legacy research artifacts into canonical `_src/sourcing/` paths
- reconcile resource IDs against `resources/**`
- validate required publishable-resource taxonomy contracts
- audit sourcing coverage and taxonomy drift
- classify or prune low-value lead artifacts where needed

Current scripts include:

- `reconcile_resource_ids.py`
- `audit_sourcing_coverage.py`
- `audit_resource_components.py`
- `prune_leads.py`
- `migrate_research_history.py`
