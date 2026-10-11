---
id: {{ID}}                 # Stable unique id, never reused. Format PREFIX-NNNN.
type: plan                   # Document type; must match the id prefix (see sdlc.config.json).
title: {{TITLE}}           # Short human title.
version: 0.1.0             # SemVer. 0.x = draft; 1.0.0 on first approval. See versioning-policy.
status: draft              # draft | in_review | approved | superseded | deprecated
owner: {{OWNER}}           # Accountable person or role.
approver:                  # Required when status is approved. A human, not the author agent.
approved_on:               # ISO date, required when approved.
created: {{DATE}}
updated: {{DATE}}          # Changes with every version bump.
stage: build                  # plan | design | build | test | deploy | maintain
derived_from: []           # Upstream docs this was produced from, pinned: [INT-0001@1.0.0]
depends_on: []             # Docs relied upon but not derived from, pinned: [POL-0001@1.0.0]
supersedes: []             # Ids replaced by this doc (no version).
external_refs: []          # Non-git references: [jira:PROJ-12, url:https://...]
covers: []                 # Requirement ids this plan implements, e.g. [R-1, R-2].
---

# Plan: {{TITLE}}
<!-- Reviewed BEFORE execution. The reviewer should see the approach first, then details. -->

## Objective
<!-- One paragraph tying back to the spec. -->

## Steps

<!-- DIAGRAM REQUIRED (see references/diagramming-guide.md): order and dependencies of the steps, with verification points.
     Keep the purpose line, label every decision edge, show roles and gates, add a legend, then 2-4 bullets narrating the key path. Replace the placeholder nodes. -->
**Purpose:** _one sentence: what this diagram shows and the question it answers._

```mermaid
flowchart TD
  S1[Step 1: describe deliverable] --> V1{Verified?}
  V1 -- yes --> S2[Step 2: describe deliverable]
  V1 -- no --> F1[Fix and re-verify] --> V1
  S2 --> V2{Verified?}
  V2 -- yes --> Done([Plan complete])
  V2 -- no --> F1
```
Key: diamonds = verification points; the loop shows where rework happens.
- _Narrate the critical path._
- _Narrate what happens when a check fails._
1. _step_ - deliverable touched - how it is verified

## Deliverables touched
<!-- Files, documents, systems, datasets. -->

## Risks
<!-- What could go wrong, how it would be noticed. -->

## Verification
<!-- Commands, checks or evals that prove each step. Reference VER-* when it exists. -->

## Rollback
<!-- How to undo safely. -->

## Related documents
<!-- Mirror the front matter links with relative Markdown links so readers can click through. -->
- Derived from: _none yet_
- Depends on: _none yet_

## Changelog
<!-- Newest row last. Its version must equal the front matter version. scripts/bump.py maintains this. -->
| version | date | author | change |
|---|---|---|---|
| 0.1.0 | {{DATE}} | {{OWNER}} | Initial draft |
