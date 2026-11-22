---
id: PLAN-0001                 # Stable unique id, never reused. Format PREFIX-NNNN.
type: plan                   # Document type; must match the id prefix (see sdlc.config.json).
title: MVP implementation plan           # Short human title.
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
covers: [R-1, R-2, R-3, R-4, R-5, R-6, R-7, R-8, R-9]                 # Requirement ids this plan implements, e.g. [R-1, R-2].
---

# Plan: MVP implementation plan
<!-- Reviewed by a human before any code is written (gate G3). -->

## Objective
Build the smallest end-to-end slice of SPEC-0001: prompt to manifest to generated server to checks to preview
to deploy, with revision history. Covers R-1 to R-9.

## Steps
**Purpose:** shows the build order, dependencies between steps, and where verification runs.

```mermaid
flowchart TD
  S1[1. Manifest schema and validator - R-1]
  S2[2. Revision store - R-8, R-9]
  S3[3. Code generator from manifest - R-2]
  S4[4. Sandbox runner and checker - R-4]
  S5[5. Preview UI and chat loop - R-5]
  S6[6. UI resource support - R-3]
  S7[7. Vault and deploy with auth - R-6, R-7]
  V1{Run VER-0001 checks}
  S1 --> S3
  S1 --> S2
  S3 --> S4 --> S5
  S5 --> S6
  S2 --> S7
  S5 --> S7
  S6 --> V1
  S7 --> V1
  V1 -- failures --> S3
  V1 -- all pass --> DONE([Ready for review gate G4])
```
Key: rectangles = build steps with the requirements they cover; diamond = verification checkpoint.
- Steps 1 to 5 form the walking skeleton; each ends with its own automated check.
- Steps 6 and 7 can proceed in parallel once the preview works.
- Any failure at the checkpoint returns to the generator, the most common cause.

1. Define the manifest JSON schema and validator.
2. Implement the revision store with rollback.
3. Implement the generator (templates plus handler generation).
4. Implement the sandbox runner and the checker (build, handshake, tool calls, static scan).
5. Build the preview UI and chat iteration loop.
6. Add UI resource support behind an adapter.
7. Add vault integration and authenticated deploy.

## Deliverables touched
Manifest schema, generator service, sandbox runner, checker, web app, deploy service, eval set (see VER-0001).

## Risks
- Hosting target undecided (INT-0001 open question): mitigate by isolating deploy behind an interface.
- Repair loop cost and latency: cap at 3 attempts and track cost per generation.
- Client differences in rendering UI resources: support one reference client first.

## Verification
Run all checks in [VER-0001](../../04-test/verification/VER-0001-mvp-generation-evals.md) after step 7 and the per-step checks along the way.

## Rollback
Each step ships behind a feature flag; revert the flag or the commit. Deployed user apps are unaffected because they run from stored revisions.

## Related documents
- Derived from: [SPEC-0001@0.1.0](../../02-design/specs/SPEC-0001-mcp-app-builder-mvp.md)

## Changelog
| version | date | author | change |
|---|---|---|---|
| 0.1.0 | 2026-11-22 | Rafa | Initial draft |
