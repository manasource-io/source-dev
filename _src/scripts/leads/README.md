# Leads scripts

This directory is reserved for lead-ingestion tooling.

Planned responsibilities:

- fetch candidate content from configured communities and queries
- normalize raw lead metadata
- store retained lead artifacts under `_src/leads/`
- avoid embedding taxonomy assumptions that conflict with `_src/workflow/taxonomy-map.md`

Expected future scripts include:

- `harvest_reddit.py`
- `fetch_reddit_post.py`
- `harvest_search.py`
- `shared.py`
