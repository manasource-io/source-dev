# Pruning policy

This document defines how raw lead material should be retained, archived, or removed.

The goal is to keep `_src/leads/` useful rather than turning it into a permanent dump of loosely related internet content.

## Core principle

The active lead corpus should optimize for **signal density**, not total volume.

A smaller set of better leads is more valuable than a large archive of noisy or sensational material.

## Lead states

A raw lead should eventually fall into one of these buckets:

- keep active
- archive
- prune

## Keep active

Retain a lead in the active corpus when it is one or more of the following:

- clearly relevant to an existing resource
- rich in traceable evidence links
- likely to generate a real resource improvement soon
- already referenced by sourcing history or harvest logs
- uniquely useful for a thin or under-covered topic area

## Archive

Archive rather than keep active when a lead is:

- potentially useful later but not currently high priority
- partially duplicative of a stronger active lead
- relevant to a topic that is not yet represented cleanly in the public corpus
- historically informative but not worth keeping in the primary active queue

Archived leads should remain recoverable, but should not clutter the active sourcing surface.

## Prune

Prune a lead when it is predominantly:

- sensational framing with weak or missing evidence
- off-topic for the source corpus
- purely conversational with little durable sourcing value
- a lower-quality duplicate of a stronger retained lead
- not meaningfully actionable for a current or planned resource

## Practical signals

Useful pruning signals include:

- whether the lead maps to a current resource ID
- whether the lead contains primary literature or credible institutional links
- whether it duplicates better material already retained
- whether it has already produced a real sourcing update
- whether its main value is rhetoric rather than evidence

## Safety rule

Do not permanently delete borderline material in the same step where it is first classified unless the lead is clearly low-value noise.

A safer rollout is:

1. keep high-signal leads active
2. move uncertain leads to archive
3. fully remove only clearly low-value clutter

## Relationship to sourcing history

Once a lead has been processed into validated editorial work, the durable record belongs in `_src/sourcing/`.
A retained raw lead should never be treated as a substitute for sourcing notes or source checks.
