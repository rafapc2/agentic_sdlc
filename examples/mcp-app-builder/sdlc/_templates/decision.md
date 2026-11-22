---
id: {{ID}}                 # Stable unique id, never reused. Format PREFIX-NNNN.
type: decision                   # Document type; must match the id prefix (see sdlc.config.json).
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
---

# Decision: {{TITLE}}
<!-- Append-only record. Never edit an approved decision; supersede it with a new DEC. -->

## Context
<!-- Forces at play and why a decision is needed now. -->

## Options
| Option | Pros | Cons |
|---|---|---|
| A | | |
| B | | |

## Decision
<!-- OPTIONAL: if this describes a process or flow, embed a Mermaid diagram (see references/diagramming-guide.md). -->
<!-- The chosen option and the reason, in one or two sentences. -->

## Consequences
<!-- What becomes easier, harder, or required. Follow-up work. -->

## Related documents
<!-- Mirror the front matter links with relative Markdown links so readers can click through. -->
- Derived from: _none yet_
- Depends on: _none yet_

## Changelog
<!-- Newest row last. Its version must equal the front matter version. scripts/bump.py maintains this. -->
| version | date | author | change |
|---|---|---|---|
| 0.1.0 | {{DATE}} | {{OWNER}} | Initial draft |
