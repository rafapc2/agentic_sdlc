---
id: {{ID}}                 # Stable unique id, never reused. Format PREFIX-NNNN.
type: intent                   # Document type; must match the id prefix (see sdlc.config.json).
title: {{TITLE}}           # Short human title.
version: 0.1.0             # SemVer. 0.x = draft; 1.0.0 on first approval. See versioning-policy.
status: draft              # draft | in_review | approved | superseded | deprecated
owner: {{OWNER}}           # Accountable person or role.
approver:                  # Required when status is approved. A human, not the author agent.
approved_on:               # ISO date, required when approved.
created: {{DATE}}
updated: {{DATE}}          # Changes with every version bump.
stage: plan                  # plan | design | build | test | deploy | maintain
derived_from: []           # Upstream docs this was produced from, pinned: [INT-0001@1.0.0]
depends_on: []             # Docs relied upon but not derived from, pinned: [POL-0001@1.0.0]
supersedes: []             # Ids replaced by this doc (no version).
external_refs: []          # Non-git references: [jira:PROJ-12, url:https://...]
---

# Intent: {{TITLE}}
<!-- An intent captures what is wanted, why and under which constraints, in the originator's own words.
     It is the root of the chain: every spec, plan and release traces back to an intent. -->

## Problem
<!-- What can people not do today? Who is affected? Evidence or numbers if available. -->

<!-- DIAGRAM REQUIRED (see references/diagramming-guide.md): how the work happens TODAY (current process), including the pain points.
     Keep the purpose line, label every decision edge, show roles and gates, add a legend, then 2-4 bullets narrating the key path. Replace the placeholder nodes. -->
**Purpose:** _one sentence: what this diagram shows and the question it answers._

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Arial, sans-serif","fontSize":"16px","lineColor":"#8b9bb0","textColor":"#111827","primaryTextColor":"#111827","primaryColor":"#dbeafe","primaryBorderColor":"#1d4ed8","edgeLabelBackground":"#ffffff","clusterBkg":"#f1f5f9","clusterBorder":"#475569","titleColor":"#111827"},"flowchart":{"curve":"basis","padding":14}}}%%
flowchart TD
  subgraph Human
    H1([Originator])
    G{Owner approves?}
  end
  subgraph Agent
    A1[Current manual step]
  end
  H1 --> A1 --> G
  G -- yes --> N[Painful outcome]
  G -- no, changes requested --> A1
  classDef gate fill:#fde68a,stroke:#92400e,stroke-width:2px,color:#111827;
  class G gate;
  linkStyle default stroke-width:2px;
```
Key: blue diamond = human approval gate; arrows are labelled with the outcome.
- _Narrate the main path._
- _Narrate the exception or failure path._

## Proposed outcome
<!-- What better looks like. Describe results, not solutions. Include how success will be recognised. -->

<!-- DIAGRAM REQUIRED (see references/diagramming-guide.md): how the work should happen AFTER the change (proposed process).
     Keep the purpose line, label every decision edge, show roles and gates, add a legend, then 2-4 bullets narrating the key path. Replace the placeholder nodes. -->
**Purpose:** _one sentence: what this diagram shows and the question it answers._

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Arial, sans-serif","fontSize":"16px","lineColor":"#8b9bb0","textColor":"#111827","primaryTextColor":"#111827","primaryColor":"#dbeafe","primaryBorderColor":"#1d4ed8","edgeLabelBackground":"#ffffff","clusterBkg":"#f1f5f9","clusterBorder":"#475569","titleColor":"#111827"},"flowchart":{"curve":"basis","padding":14}}}%%
flowchart TD
  subgraph Human
    H1([Originator])
    G{Owner approves?}
  end
  subgraph Agent
    A1[Step performed by agent]
  end
  H1 --> A1 --> G
  G -- yes --> N[Next stage]
  G -- no, changes requested --> A1
  classDef gate fill:#fde68a,stroke:#92400e,stroke-width:2px,color:#111827;
  class G gate;
  linkStyle default stroke-width:2px;
```
Key: blue diamond = human approval gate; arrows are labelled with the outcome.
- _Narrate the main path._
- _Narrate the exception or failure path._

## Affected users and systems
<!-- People, teams, systems, documents, processes touched. -->

## Constraints
<!-- Hard limits: legal, budget, deadline, security, brand, technology, "out of scope". -->

## Open questions
<!-- Unknowns that must be answered before design. Do not hide assumptions here as facts. -->
- [ ] _question_

## Related documents
<!-- Mirror the front matter links with relative Markdown links so readers can click through. -->
- Derived from: _none yet_
- Depends on: _none yet_

## Changelog
<!-- Newest row last. Its version must equal the front matter version. scripts/bump.py maintains this. -->
| version | date | author | change |
|---|---|---|---|
| 0.1.0 | {{DATE}} | {{OWNER}} | Initial draft |
