---
id: VER-0001                 # Stable unique id, never reused. Format PREFIX-NNNN.
type: verification                   # Document type; must match the id prefix (see sdlc.config.json).
title: MVP generation evals           # Short human title.
version: 0.1.0             # SemVer. 0.x = draft; 1.0.0 on first approval. See versioning-policy.
status: draft              # draft | in_review | approved | superseded | deprecated
owner: Rafa           # Accountable person or role.
approver:                  # Required when status is approved. A human, not the author agent.
approved_on:               # ISO date, required when approved.
created: 2026-11-22
updated: 2026-11-22          # Changes with every version bump.
stage: test                  # plan | design | build | test | deploy | maintain
derived_from: [SPEC-0001@0.1.0, PLAN-0001@0.1.0]           # Upstream docs this was produced from, pinned: [INT-0001@1.0.0]
depends_on: []             # Docs relied upon but not derived from, pinned: [POL-0001@1.0.0]
supersedes: []             # Ids replaced by this doc (no version).
external_refs: []          # Non-git references: [jira:PROJ-12, url:https://...]
covers: [R-1, R-2, R-3, R-4, R-5, R-6, R-7, R-8, R-9]                 # Requirement ids verified here, e.g. [R-1, R-2].
---

# Verification: MVP generation evals
<!-- The verifier is independent of the builder. Results stay empty until checks are run. -->

## Scope
All requirements R-1 to R-9 of SPEC-0001. The eval set is 20 prompts (10 simple, 5 with UI, 5 adversarial) kept
in the repository and versioned with this document.

## Checks
**Purpose:** shows the order in which checks run for each eval prompt and where evidence is stored.

```mermaid
flowchart TD
  E1([Eval prompt])
  C1[Manifest produced and no code before confirmation]
  C2[Build and static scan]
  C3[Protocol handshake and tool listing]
  C4[One call per tool with sample args]
  C5[UI sandbox and CSP probe]
  C6[Deploy to staging and auth probe]
  C7[Rollback restores earlier revision]
  EV[(Evidence folder per run)]
  F([Record failure and fix generator])
  E1 --> C1 --> C2 --> C3 --> C4 --> C5 --> C6 --> C7
  C1 & C2 & C3 & C4 & C5 & C6 & C7 --> EV
  C2 -- fail --> F
  C3 -- fail --> F
  C4 -- fail --> F
  C5 -- fail --> F
  C6 -- fail --> F
```
Key: rectangles = checks; cylinder = evidence store; every failing check ends in a recorded failure.

| id | Check | Covers | Pass condition |
|---|---|---|---|
| C-1 | Manifest-before-code | R-1 | No generated file exists before confirmation |
| C-2 | Build and scan | R-2, R-7 | Build succeeds; no secret literals or unlisted packages |
| C-3 | Handshake | R-2, R-4 | Initialize and tool listing succeed with SDK client |
| C-4 | Tool calls | R-4 | Each tool returns a valid result for sample args; 80% first-attempt pass overall |
| C-5 | Chat revision | R-5, R-8 | New revision number and manifest diff recorded |
| C-6 | UI isolation | R-3 | UI renders; requests to foreign origins are blocked |
| C-7 | Deploy auth | R-6 | Unauthenticated call rejected; authenticated call works |
| C-8 | Secret hygiene | R-7 | No secret values in code, logs or revision store |
| C-9 | Rollback | R-9 | Restored revision byte-identical to the original |

## Evidence
Per run: manifest, generated code hash, check logs and transcript, stored under the revision id. Location to be fixed in PLAN-0001 step 2.

## Results
_Not run yet._ Record pass/fail per check and prompt here, with the date and the build under test.

## Related documents
- Derived from: [SPEC-0001@0.1.0](../../02-design/specs/SPEC-0001-mcp-app-builder-mvp.md), [PLAN-0001@0.1.0](../../03-build/plans/PLAN-0001-mvp-implementation-plan.md)

## Changelog
| version | date | author | change |
|---|---|---|---|
| 0.1.0 | 2026-11-22 | Rafa | Initial draft |
