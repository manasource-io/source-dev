# manasource source

`source` is the standalone content repository for manasource.

It is intentionally content-only:

- Markdown bodies
- YAML frontmatter
- No app runtime code

Current structure:

- `resources/`
- `resources/nutrition/food`
- `resources/nutrition/diet`
- `resources/nutrition/supplements`
- `resources/exercise`
- `resources/abstinence`
- `resources/habits`
- `resources/restoration`
- `resources/circadian`
- `resources/wellbeing`

Each resource is a markdown file with frontmatter fields such as:

- `title`
- `category`
- `subCategory`
- `description`
- `benefits`
- `benefitLevel`
- `overallScore`
- `credibility`
- `lastResearched`
- `readiness`
- `references`

The downstream website consumes this repository as a versioned build input.
`web` should pin a specific tag or commit via build-time configuration rather
than reading a local checkout directly.
