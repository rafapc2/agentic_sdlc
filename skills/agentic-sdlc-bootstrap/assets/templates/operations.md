---
id: {{ID}}                 # Stable unique id, never reused. Format PREFIX-NNNN.
type: operations                   # Document type; must match the id prefix (see sdlc.config.json).
title: {{TITLE}}           # Short human title.
version: 0.1.0             # SemVer. 0.x = draft; 1.0.0 on first approval. See versioning-policy.
status: draft              # draft | in_review | approved | superseded | deprecated
owner: {{OWNER}}           # Accountable person or role.
approver:                  # Required when status is approved. A human, not the author agent.
approved_on:               # ISO date, required when approved.
created: {{DATE}}
updated: {{DATE}}          # Changes with every version bump.
stage: maintain                  # plan | design | build | test | deploy | maintain
derived_from: []           # Upstream docs this was produced from, pinned: [INT-0001@1.0.0]
depends_on: []             # Docs relied upon but not derived from, pinned: [POL-0001@1.0.0]
supersedes: []             # Ids replaced by this doc (no version).
external_refs: []          # Non-git references: [jira:PROJ-12, url:https://...]
---

# Operations record: {{TITLE}}
<!-- Incident, metric breach, learning or refresh. If follow-up work is needed, create a new INT that derives from this record. -->

## Trigger
<!-- What happened or which control band was breached, when, detected by whom/what. -->

<!-- DIAGRAM REQUIRED (see references/diagramming-guide.md): the sequence of events from detection to resolution.
     Keep the purpose line, label every decision edge, show roles and gates, add a legend, then 2-4 bullets narrating the key path. Replace the placeholder nodes. -->
**Purpose:** _one sentence: what this diagram shows and the question it answers._

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Arial, sans-serif","fontSize":"16px","actorBkg":"#dbeafe","actorBorder":"#1d4ed8","actorTextColor":"#111827","actorLineColor":"#475569","signalColor":"#1f2937","signalTextColor":"#111827","noteBkgColor":"#fde68a","noteBorderColor":"#92400e","noteTextColor":"#111827","labelBoxBkgColor":"#f1f5f9","labelBoxBorderColor":"#475569","labelTextColor":"#111827"}}}%%
sequenceDiagram
  rect rgb(241, 245, 249)
  participant M as Monitor / person
  participant O as operator agent
  participant H as Human owner
  M->>O: Alert / breach detected
  O->>O: Diagnose with evidence
  O->>H: Propose follow-up (new intent?)
  H-->>O: Decision
  end
```
Key: solid arrows = requests; dashed = responses.
- _Narrate detection and diagnosis._
- _State the follow-up decision._

## Diagnosis
<!-- Cause analysis, evidence. -->

## Impact
<!-- Who/what was affected and for how long. -->

## Follow-up
<!-- New intent(s) opened: INT-xxxx. Controls to add (policy, hook, test). -->

## Related documents
<!-- Mirror the front matter links with relative Markdown links so readers can click through. -->
- Derived from: _none yet_
- Depends on: _none yet_

## Changelog
<!-- Newest row last. Its version must equal the front matter version. scripts/bump.py maintains this. -->
| version | date | author | change |
|---|---|---|---|
| 0.1.0 | {{DATE}} | {{OWNER}} | Initial draft |
