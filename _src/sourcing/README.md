# Sourcing

`_src/sourcing/` stores the validated editorial history behind the resource corpus.

This is the canonical home for provenance once a source, claim, or lead has been reviewed by a human or agent.

## Intended contents

- resource freshness logs
- processed lead tracking
- per-resource `source-checks.csv`
- dated research notes
- sourcing audits
- explicit orphan or migration notes when a research artifact has no current public resource target

## Intended structure

```text
_src/sourcing/
  README.md
  resource-log.csv
  harvest-log.csv
  audits/
  resources/
    supplement/
      creatine/
        source-checks.csv
        2026-04-09.md
```

## Boundaries

- `_src/sourcing/` is for validated editorial provenance
- `_src/leads/` is for raw candidate intake
- `resources/` is for publishable content only
