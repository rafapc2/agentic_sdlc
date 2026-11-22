---
id: POL-0001                 # Stable unique id, never reused. Format PREFIX-NNNN.
type: policy                   # Document type; must match the id prefix (see sdlc.config.json).
title: Generated MCP server safety           # Short human title.
version: 0.1.0             # SemVer. 0.x = draft; 1.0.0 on first approval. See versioning-policy.
status: draft              # draft | in_review | approved | superseded | deprecated
owner: Rafa           # Accountable person or role.
approver:                  # Required when status is approved. A human, not the author agent.
approved_on:               # ISO date, required when approved.
created: 2026-11-22
updated: 2026-11-22          # Changes with every version bump.
stage: plan                  # plan | design | build | test | deploy | maintain
derived_from: []           # Upstream docs this was produced from, pinned: [INT-0001@1.0.0]
depends_on: []             # Docs relied upon but not derived from, pinned: [POL-0001@1.0.0]
supersedes: []             # Ids replaced by this doc (no version).
external_refs: []          # Non-git references: [jira:PROJ-12, url:https://...]
---

# Policy: Generated MCP server safety
<!-- Rules every generated MCP server and every agent that generates one must obey. -->

## Statement
1. **No secrets in code.** API keys and tokens are injected at runtime from the vault; generated source never contains them.
2. **Sandboxed execution.** Generated code runs only in an isolated sandbox with a network egress allowlist derived from the manifest.
3. **Side-effect confirmation.** Tools that write, delete or spend are annotated as such in the manifest and require explicit client-side user confirmation.
4. **Dependency allowlist.** Generated servers may use only the official MCP SDK and packages from an approved list.
5. **UI isolation.** Interactive UI resources are served for rendering in a sandboxed frame with a restrictive content security policy and no access to the host page.
6. **Authenticated endpoints.** Every deployed endpoint requires authentication; there are no anonymous deployments.

## Scope
Applies to the builder product, its generation agents, and every server produced by it. Does not apply to the SDLC documents themselves.

## Owner and source of truth
Owner: Rafa (product and security). This document is the source of truth; later it can be encoded as a skill for the generation agent.

## Enforcement
**Purpose:** shows the layers that enforce the policy, from advice to hard blocks, and what happens on violation.

```mermaid
flowchart TD
  subgraph Advice
    L1[Generation prompt and skill state the rules]
  end
  subgraph Automated blocks
    L2[Static scan rejects secrets and unlisted packages]
    L3[Sandbox denies network outside allowlist]
    L4[Deploy step refuses endpoints without auth]
  end
  subgraph Human
    L5{Reviewer approves flagged side-effect tools?}
  end
  L1 --> L2
  L2 -- violation --> X([Generation rejected, auto-repair])
  L2 -- clean --> L3 --> L4 --> L5
  L5 -- no --> X
  L5 -- yes --> OK([Allowed to deploy])
```
Key: rectangles = automated or advisory layer; diamond = human check; rounded = outcome.
- Advice alone is never relied upon: rules 1, 2, 4 and 6 are enforced by code.
- Rule 3 needs a human because intent of a tool cannot be inferred reliably.

## Related documents
- Depended on by: [SPEC-0001](../../02-design/specs/SPEC-0001-mcp-app-builder-mvp.md)

## Changelog
| version | date | author | change |
|---|---|---|---|
| 0.1.0 | 2026-11-22 | Rafa | Initial draft |
