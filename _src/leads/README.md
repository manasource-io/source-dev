# Leads

`_src/leads/` is the intake layer for candidate external material that may eventually improve resource pages.

This is the successor to the older `research-finding` concept from `poc`, but renamed to reflect function more clearly.

## Purpose

This area stores:

- curated lead-source definitions
- raw harvested candidate leads
- cached result files that survive pruning
- future intake metadata such as dedupe tracking and query bundles

## Intended structure

```text
_src/leads/
  README.md
  config/
    communities.json
    queries.json
    pruning-rules.json
  reddit/
    found.json
    results/
```

## Boundaries

- Leads are **inputs**, not validated source history
- Once a lead is reviewed and used to improve a resource, the durable editorial record belongs in `_src/sourcing/`
- Low-value or noisy leads should be archived or pruned rather than accumulated indefinitely
