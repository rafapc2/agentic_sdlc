# Governance and gates

Governance is enforced as the agent acts, not reconstructed later. Skills advise; hooks and CI enforce.

## Gates
A gate sits at the end of each stage. Define in `sdlc/governance/gates.md`:
- **Gate id** (G1..G6), the artifact approved, the approver role, evidence required, and the next stage it triggers.
- Default triggers: accepted INT -> design pass; approved SPEC -> plan mode; approved PLAN -> build; verification green + REV -> deploy; breached control band -> new INT.

## Autonomy tiers (per stage)
| Tier | Agent may | Human does |
|---|---|---|
| assist | draft only | does the stage, uses draft |
| gated | act and produce the artifact | approves every artifact |
| supervised-auto | act and advance on green checks | reviews exceptions and a sample |
Start every stage at `gated`. Raise a tier only after the gate, the checks behind it and the rollback path exist (the playbook's dependency order). Record the tier in `sdlc.config.json`.

## Enforcement mechanisms
| Need | Mechanism |
|---|---|
| Documents valid, links resolve, no silent edits | `validate-docs` hook on edits under `sdlc/` + CI job |
| Approved docs cannot be edited in place | validator `--git` mode in CI; branch protection |
| Policy that must hold | skill (advice) + hook (block) |
| Human approval before risky action | hook that returns "ask" for deploy/delete/publish commands |
| Tests or checks not weakened | hook blocking edits to test/eval files during fixes |

## Roles
Define agent roles as `.claude/agents/*.md`: `drafter` (intent/spec), `planner`, `builder`, `verifier` (read-only checks, independent of builder), `reviewer`, `operator`. Keep verifier and reviewer separate from the builder so approval is not self-graded.

## Metrics (leading and lagging)
| Stage | Leading | Lagging |
|---|---|---|
| plan | time from first conversation to committed INT | share of INTs accepted vs closed |
| design | time INT commit -> SPEC commit | SPEC rework after build starts |
| build | plan approval -> first verified change | repeat mistakes CLAUDE.md should have caught |
| test | checks run per change | defects escaping to deploy |
| deploy | review turnaround | changes rolled back |
| maintain | time breach -> diagnosed INT | recurrence of same OPS cause |
Read all of them from git history and the generated graph; avoid separate tracking systems.

## Audit trail
The chain of commits plus the graph answers: who asked for what (INT), what was decided (SPEC/DEC), what the agent produced (diff), who approved (approver, merge), and what happened in production (OPS).
