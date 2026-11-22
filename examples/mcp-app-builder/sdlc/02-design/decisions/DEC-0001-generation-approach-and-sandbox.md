---
id: DEC-0001                 # Stable unique id, never reused. Format PREFIX-NNNN.
type: decision                   # Document type; must match the id prefix (see sdlc.config.json).
title: Generation approach and sandbox           # Short human title.
version: 0.1.0             # SemVer. 0.x = draft; 1.0.0 on first approval. See versioning-policy.
status: draft              # draft | in_review | approved | superseded | deprecated
owner: Rafa           # Accountable person or role.
approver:                  # Required when status is approved. A human, not the author agent.
approved_on:               # ISO date, required when approved.
created: 2026-11-22
updated: 2026-11-22          # Changes with every version bump.
stage: build                  # plan | design | build | test | deploy | maintain
derived_from: [SPEC-0001@0.1.0]           # Upstream docs this was produced from, pinned: [INT-0001@1.0.0]
depends_on: []             # Docs relied upon but not derived from, pinned: [POL-0001@1.0.0]
supersedes: []             # Ids replaced by this doc (no version).
external_refs: []          # Non-git references: [jira:PROJ-12, url:https://...]
---

# Decision: Generation approach and sandbox
<!-- One decision, immutable once approved. Replace by superseding. -->

## Context
SPEC-0001 needs a way to turn prompts into working MCP servers that humans can review cheaply and that can be
verified automatically. Free-form code generation is flexible but hard to review and to constrain by policy.

## Options
- **A. Free-form generation:** the agent writes the whole repository. Maximum flexibility; hard to review, easy to violate POL-0001.
- **B. Manifest-first:** the agent drafts a typed manifest, then generates code from templates plus small handler bodies. Reviewable and checkable; less flexible for unusual apps.
- **C. Interpreter runtime:** one generic server reads the manifest at runtime, with no code generated. Safest; cannot express custom logic and no code export.

## Decision
Choose **B (manifest-first)** with TypeScript and the official SDK for the MVP. Each preview runs in its own
container-style sandbox with egress limited to the allowlist in the manifest. Revisit C as a fast path for
simple apps after the MVP.

## Consequences
- The human gate reviews a small manifest (R-1), improving trust and speed.
- Policy checks run on the manifest and on handler code only.
- Unusual apps may hit template limits; an escape hatch for free-form handlers is required.
- Only TypeScript at first; other languages need a new decision.

## Related documents
- Derived from: [SPEC-0001@0.1.0](../specs/SPEC-0001-mcp-app-builder-mvp.md)

## Changelog
| version | date | author | change |
|---|---|---|---|
| 0.1.0 | 2026-11-22 | Rafa | Initial draft |
