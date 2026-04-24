# Resource components

This document defines the source-side contract for the `components` frontmatter field used on publishable resources.

## Purpose

`components` is the machine-readable taxonomy layer for resource content.

It exists so downstream consumers can classify resources more consistently than `category` and `subCategory` alone allow.

The initial planned use is compact semantic resource-code generation in `mana`, but the field should be treated as a durable source-content contract rather than a one-off app concern.

## Scope

Phase 1 requires `components` on:

- `resources/nutrition/food/*.md`
- `resources/nutrition/supplements/*.md`
- `resources/exercise/*.md`

Phase 1 does not require `components` on:

- `resources/nutrition/diet/*.md`
- `resources/habits/*.md`
- `resources/restoration/*.md`
- `resources/abstinence/*.md`
- `resources/wellbeing/*.md`
- `resources/circadian/*.md`

Those domains may adopt the same pattern later if it proves useful.

## Field shape

`components` should be a YAML list of lower-case kebab-case strings.

Example:

```yaml
components:
  - vitamin
  - fat-soluble
  - immune-support
```

Rules:

- use lower-case kebab-case only
- do not repeat entries
- prefer canonical taxonomy tags, not free-form prose
- for phase 1 resources in food, supplements, and exercise, include at least 2 entries

## Ordering contract

`components` is ordered.

- `components[0]`: primary component, compound, supplement type, or dominant mechanism
- `components[1+]`: additional descriptors

This order matters because downstream code allocation is expected to derive semantic prefixes from the first two entries.

## Meaning by domain

### Food

For food resources:

- keep `subCategory` singular when present, for example `fruit` or `vegetable`
- `components[0]` should describe the most important nutrient, compound, or mechanism
- do not repeat the food family in `components` if `subCategory` already covers it

Examples:

```yaml
subCategory: fruit
components:
  - anthocyanin
  - polyphenol
  - glucose-support
```

```yaml
subCategory: grain
components:
  - fiber
  - beta-glucan
```

```yaml
subCategory: protein
components:
  - fatty-acid
  - omega-3
```

### Supplements

For supplement resources:

- `components[0]` should describe the primary supplement type, compound class, or dominant mechanism
- do not lead with a broad family tag that just restates that the resource is a supplement

Examples:

```yaml
components:
  - vitamin
  - fat-soluble
  - immune-support
```

```yaml
components:
  - fatty-acid
  - omega-3
```

```yaml
components:
  - probiotic
  - microbiome
```

```yaml
components:
  - drug
  - mtor
```

### Exercise

For exercise resources:

- `components[0]` should describe the dominant training effect, stressor, or physiological mechanism
- do not lead with a broad exercise family tag that simply repeats the editorial category

Examples:

```yaml
components:
  - endurance
  - aerobic
```

```yaml
components:
  - strength
  - hypertrophy
```

```yaml
components:
  - flexibility
  - recovery
```

```yaml
components:
  - heat
  - recovery
```

## Relationship to existing fields

`components` is not a replacement for editorial metadata.

- `category` remains an editorial/display field
- `subCategory` remains an editorial/display field
- `components` is the machine taxonomy field

Do not overload `category` or `subCategory` with responsibilities that belong in `components`.
Do not duplicate editorial family labels in `components` when those are already obvious from `category` or `subCategory`.

## Authoring guidance

When adding or editing `components`:

- choose the smallest stable set of tags that classify the resource well
- make the first two entries intentional, because they carry structural meaning
- prefer the first non-editorial taxonomy signal, not a repeated family label
- prefer tags that can be reused across multiple resources
- avoid one-off synonyms when an existing tag already captures the concept
- use manual review for ambiguous resources instead of guessing

## Initial backfill target

Phase 1 backfill should cover all current food, supplement, and exercise resources.

Suggested workflow:

1. set `subCategory` in singular form when that field is used
2. assign the dominant primary component, supplement type, or training effect as `components[0]`
3. add secondary descriptors only when they provide real reuse value
4. flag ambiguous cases for review instead of forcing a weak taxonomy

## Validation

Use the audit script after backfills or new resource additions. It validates required phase 1 `components` coverage and singular `subCategory` values:

`python3 _src/scripts/sourcing/audit_resource_components.py`

## Downstream dependency

`mana` is expected to consume `components` for semantic compact resource codes.

That means changes to:

- allowed tag vocabulary
- ordering rules
- family meanings

should be treated as source-contract changes, not casual editorial tweaks.
