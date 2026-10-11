---
id: {{ID}}                 # Stable unique id, never reused. Format PREFIX-NNNN.
type: release                   # Document type; must match the id prefix (see sdlc.config.json).
title: {{TITLE}}           # Short human title.
version: 0.1.0             # SemVer. 0.x = draft; 1.0.0 on first approval. See versioning-policy.
status: draft              # draft | in_review | approved | superseded | deprecated
owner: {{OWNER}}           # Accountable person or role.
approver:                  # Required when status is approved. A human, not the author agent.
approved_on:               # ISO date, required when approved.
created: {{DATE}}
updated: {{DATE}}          # Changes with every version bump.
stage: deploy                  # plan | design | build | test | deploy | maintain
derived_from: []           # Upstream docs this was produced from, pinned: [INT-0001@1.0.0]
depends_on: []             # Docs relied upon but not derived from, pinned: [POL-0001@1.0.0]
supersedes: []             # Ids replaced by this doc (no version).
external_refs: []          # Non-git references: [jira:PROJ-12, url:https://...]
---

# Release: {{TITLE}}
<!-- Record of what shipped. Cites exact input versions via derived_from. -->

## Contents
<!-- Versions of deliverables released, environment/audience, date. -->

## Approvals
<!-- Who approved, per gate, with links to the approvals. -->

## Rollback path
<!-- Concrete steps and the trigger that invokes them. -->

<!-- DIAGRAM REQUIRED (see references/diagramming-guide.md): rollout steps and the trigger and path for rollback.
     Keep the purpose line, label every decision edge, show roles and gates, add a legend, then 2-4 bullets narrating the key path. Replace the placeholder nodes. -->
**Purpose:** _one sentence: what this diagram shows and the question it answers._

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Arial, sans-serif","fontSize":"16px","lineColor":"#8b9bb0","textColor":"#111827","primaryTextColor":"#111827","primaryColor":"#dbeafe","primaryBorderColor":"#1d4ed8","edgeLabelBackground":"#ffffff","clusterBkg":"#f1f5f9","clusterBorder":"#475569","titleColor":"#111827"},"flowchart":{"curve":"basis","padding":14}}}%%
flowchart LR
  A[Approved release] --> R[Roll out to audience]
  R --> M{Control bands healthy?}
  M -- yes --> Done([Release complete])
  M -- breach --> B[Rollback] --> O[Open operations record] 
  classDef risk fill:#fecaca,stroke:#991b1b,stroke-width:2px,color:#111827;
  class B,O risk;
  linkStyle default stroke-width:2px;
```
Key: red = rollback path.
- _Narrate the trigger that invokes rollback._
- _State who can invoke it._

## Related documents
<!-- Mirror the front matter links with relative Markdown links so readers can click through. -->
- Derived from: _none yet_
- Depends on: _none yet_

## Changelog
<!-- Newest row last. Its version must equal the front matter version. scripts/bump.py maintains this. -->
| version | date | author | change |
|---|---|---|---|
| 0.1.0 | {{DATE}} | {{OWNER}} | Initial draft |
