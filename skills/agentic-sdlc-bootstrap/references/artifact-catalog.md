# Artifact catalog

Each stage ends by committing exactly one primary artifact. Definitions below are the contract that templates in `assets/templates/` implement.

| Type | Prefix | Stage | Purpose | Author | Approver (gate) | Derived from |
|---|---|---|---|---|---|---|
| policy | POL | any | A rule or standard that other artifacts must obey (security, brand, compliance). Encoded also as a skill when repeatable. | domain owner | lead | - |
| intent | INT | plan | What is wanted, why, for whom, under which constraints, plus open questions. Human readable and machine actionable. | originator + agent | product/business owner | event, idea, or an `OPS` record |
| spec | SPEC | design | Requirements and design in one document, constrained by policies, with flagged areas of concern. | agent | product owner (+ security/compliance when flagged) | INT |
| decision | DEC | any | A single decision with context, options, outcome, consequences (ADR). Immutable; replaced by superseding. | agent or human | owner of the decision | SPEC or PLAN |
| plan | PLAN | build | Ordered steps, files/deliverables touched, risks, verification steps, rollback. Reviewed before execution. | agent (plan mode) | engineer/lead | SPEC |
| verification | VER | test | How correctness is checked: test or eval list, acceptance criteria, evidence locations, results. | agent | lead/QA | SPEC (+ PLAN) |
| review | REV | deploy | Findings of layered agent review plus human sign-off notes. | review agents + human | reviewer | PLAN, VER |
| release | REL | deploy | What shipped, when, by whom, approvals, rollback path. | agent | release approver | REV |
| operations | OPS | maintain | Incident, metric breach, learning, or refresh record. May spawn a new INT. | agent | operator | REL |

## Required front matter (all types)
`id, type, title, version, status, owner, created, updated, stage, derived_from, depends_on, supersedes`. Approved documents also require `approver` and `approved_on`. See `versioning-policy.md`.

## Required sections by type
- **intent**: Problem, Proposed outcome, Affected users and systems, Constraints, Open questions, Changelog.
- **spec**: Summary, Requirements (numbered `R-n`), Design, Policy compliance, Areas of concern, Acceptance criteria, Changelog.
- **plan**: Objective, Steps, Deliverables touched, Risks, Verification, Rollback, Changelog.
- **decision**: Context, Options, Decision, Consequences, Changelog.
- **verification**: Scope, Checks, Evidence, Results, Changelog.
- **review**: Scope, Findings, Human sign-off, Changelog.
- **release**: Contents, Approvals, Rollback path, Changelog.
- **operations**: Trigger, Diagnosis, Impact, Follow-up (new intent?), Changelog.
- **policy**: Statement, Scope, Owner and source of truth, Enforcement (skill/hook/CI), Changelog.

The validator checks these headings so no artifact is silently incomplete.

## Requirement-level traceability
Number requirements `R-1, R-2...` in the spec. Plans, verification items and reviews cite them (`covers: R-1, R-3`). This lets the validator report requirements without verification coverage.
