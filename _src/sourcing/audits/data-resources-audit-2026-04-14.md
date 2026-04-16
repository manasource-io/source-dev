# Data Resources Audit

- **Date**: 2026-04-14
- **Scope**: `resources/**/*.md`
- **Purpose**: Reusable backlog for the next resource-quality pass after the structural normalization and first 50-reference metadata enrichment.

## Current State

- The resource corpus now passes the structural audit:
  - object-based `references`
  - benefit anchors present for all declared `benefits`
  - no remaining `publicationDate` field usage
  - no missing required frontmatter for the file's current `readiness`
- The shared reference schema now uses `date` instead of `publicationDate`.
- 56 reference entries have been enriched with `title` and `date` metadata or repaired via source replacement.

## Remaining Metadata Work

- **260 reference entries** still need `title` and/or `date`.
- Highest-volume remaining files from the quick inventory:
  - `resources/nutrition/food/avocado.md`: 7
  - `resources/nutrition/diet/fasting-period.md`: 6
  - `resources/nutrition/food/cacao.md`: 6
  - `resources/nutrition/food/flaxseeds.md`: 6
  - `resources/nutrition/food/nuts.md`: 6
  - `resources/nutrition/food/olive-oil.md`: 6
  - `resources/nutrition/supplements/vitamin-d.md`: 6
  - `resources/nutrition/food/black-beans.md`: 5
  - `resources/nutrition/food/green-tea.md`: 5
  - `resources/nutrition/food/pomegranate.md`: 5
  - `resources/nutrition/supplements/creatine.md`: 5
  - `resources/nutrition/supplements/curcumin.md`: 5

## Cleared This Session

- Replaced the clearly wrong references in:
  - [`resources/exercise/burpees.md`](../../../resources/exercise/burpees.md)
  - [`resources/exercise/crunches.md`](../../../resources/exercise/crunches.md)
  - [`resources/exercise/planks.md`](../../../resources/exercise/planks.md)
- Resolved the previously blocked metadata recovery on:
  - [`resources/circadian/wake-time.md`](../../../resources/circadian/wake-time.md)
- Added metadata and one new validated literature reference to:
  - [`resources/nutrition/diet/avoid-alcohol.md`](../../../resources/nutrition/diet/avoid-alcohol.md)

## Known Bad Or Suspicious References

These URLs resolved, but the actual title suggests the citation is mismatched to the resource topic and should likely be replaced rather than just enriched:

- [`resources/exercise/infrared-light.md`](../../../resources/exercise/infrared-light.md)
  - `https://pubmed.ncbi.nlm.nih.gov/27272075/`
  - Resolved title: `New Atrophic Acne Scar Classification...`
- [`resources/exercise/lunges.md`](../../../resources/exercise/lunges.md)
  - `https://pubmed.ncbi.nlm.nih.gov/22592177/`
  - Resolved title: `Intrarater reliability of the functional movement screen.`
- [`resources/exercise/push-ups.md`](../../../resources/exercise/push-ups.md)
  - `https://pubmed.ncbi.nlm.nih.gov/30900831/`
  - Resolved title: `Modulation of Autonomic Function by Physical Exercise in Patients with Fibromyalgia Syndrome...`
- [`resources/exercise/resistance-bands.md`](../../../resources/exercise/resistance-bands.md)
  - `https://pubmed.ncbi.nlm.nih.gov/31733051/`
  - Resolved title: `Changes in Morbidity, Physical Fitness, and Perceived Quality of Life among Schoolchildren...`
- [`resources/exercise/squats.md`](../../../resources/exercise/squats.md)
  - `https://pubmed.ncbi.nlm.nih.gov/24552919/`
  - Resolved title: `Time is tight.`

## Low-Quality Placeholder Titles To Replace

These are structurally populated but should be replaced with stronger source metadata or better sources:

- [`resources/exercise/breathwork.md`](../../../resources/exercise/breathwork.md)
  - `https://examine.com/topics/deep-breathing/`
  - Current resolved title: `Examine.com`
- [`resources/exercise/cycling.md`](../../../resources/exercise/cycling.md)
  - `https://examine.com/topics/cycling/`
  - Current resolved title: `Examine.com`
- [`resources/exercise/static-stretching.md`](../../../resources/exercise/static-stretching.md)
  - `https://examine.com/topics/stretching/`
  - Current resolved title: `Examine.com`
- [`resources/nutrition/supplements/ashwagandha.md`](../../../resources/nutrition/supplements/ashwagandha.md)
  - Examine reference still present and unresolved
- [`resources/nutrition/supplements/vitamin-d.md`](../../../resources/nutrition/supplements/vitamin-d.md)
  - Examine reference still present and unresolved

## Blocked / Retry Items

- [`resources/exercise/jump-rope.md`](../../../resources/exercise/jump-rope.md)
  - `https://pubmed.ncbi.nlm.nih.gov/30325617/`
  - Date resolved, title came back blank in the quick script; retry manually

## Recommended Next Pass

1. Continue replacing the remaining clearly wrong exercise reference URLs.
2. Continue the metadata enrichment in batches of 50-75 references, prioritizing high-volume files.
3. For each touched file, prefer primary literature over generic topic pages where possible.
4. Where only topic pages are available, replace weak `Examine.com` placeholder titles with the actual page title or a stronger source.
5. After replacements, update the matching `research/[type]/[name]/source-checks.csv` and session notes for the touched resources.

## Suggested Priority Files

- [`resources/exercise/lunges.md`](../../../resources/exercise/lunges.md)
- [`resources/exercise/push-ups.md`](../../../resources/exercise/push-ups.md)
- [`resources/exercise/resistance-bands.md`](../../../resources/exercise/resistance-bands.md)
- [`resources/exercise/squats.md`](../../../resources/exercise/squats.md)
- [`resources/exercise/infrared-light.md`](../../../resources/exercise/infrared-light.md)
- [`resources/nutrition/diet/fasting-period.md`](../../../resources/nutrition/diet/fasting-period.md)
- [`resources/nutrition/food/avocado.md`](../../../resources/nutrition/food/avocado.md)
- [`resources/nutrition/food/cacao.md`](../../../resources/nutrition/food/cacao.md)
- [`resources/nutrition/supplements/omega-3.md`](../../../resources/nutrition/supplements/omega-3.md)
