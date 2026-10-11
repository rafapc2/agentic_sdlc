---
name: agentic-sdlc-bootstrap
description: Bootstrap a complete agentic SDLC (AI-native lifecycle) from scratch for any project, software or not - research programs, operations changes, product launches, content or data pipelines, business processes. Interviews the user, selects a domain profile, designs the artifact chain and dependency graph, scaffolds a versioned and cross-linked document system (intent, spec, plan, verification, release, operations, decisions), wires human approval gates, CLAUDE.md, agent roles and validation hooks, then validates it. Use whenever the user wants to set up, design, adopt, or migrate to an agentic or AI-native SDLC/lifecycle/workflow, create a project operating system for agents, define stages, gates, artifacts, versioning or document traceability for a new initiative, even if they never say "SDLC".
---

# Agentic SDLC Bootstrap

Build a working, versioned, traceable operating system for a project in which humans decide and agents execute. The model comes from the AI-Native SDLC Playbook: every stage ends by committing one artifact, and the next stage starts by reading it. Humans concentrate attention at the gates between stages.

All generated files are written in **English**, even if the user speaks another language. Talk to the user in their language; write artifacts, comments, templates and config in English so they stay portable across teams and tools.

## Why this shape

- A loop beats a line: Plan -> Design -> Build -> Test -> Deploy -> Maintain, where Maintain writes the next intent. Keep the loop even for non-software work (see `references/domain-profiles.md` for stage renames).
- The committed artifact is the contract between stages. Without a stable ID, a version and explicit links, nobody can tell which spec a plan was built against, so the audit trail breaks. This skill makes that linkage mechanical, not aspirational.
- Skills advise, hooks enforce. Anything that must hold without exception becomes a hook or a CI check, never only a sentence in a prompt.

## Workflow

Follow these phases in order. Stop at each user checkpoint; a wrong assumption here is expensive to unwind later.

### 1. Discover (interview)
Read `references/interview-guide.md`. Ask only what you cannot infer; batch questions (max 6 per round). Capture: goal, domain, team and roles, existing tools/repos/docs, risk and compliance level, autonomy appetite, and scale (single deliverable vs multi-workstream program).

### 2. Choose profile and stage mapping
Read `references/domain-profiles.md`. Pick the closest profile (`software`, `research`, `operations`, `launch`, `data-content`, `program`, or `custom`) and state the stage labels and artifact types you will use. For a mixed or complex project, use the `program` profile: one program-level intent with child workstreams, each running its own loop.

### 3. Design the artifact chain (CHECKPOINT)
Read `references/artifact-catalog.md` and `references/linking-and-dependencies.md`. Produce a short proposal for the user containing:
- the stages and their gate (who approves, what evidence),
- the artifact types with ID prefixes,
- the dependency graph and the lifecycle flow as embedded Mermaid diagrams,
- the adoption order (which plays first; some need nothing, others need prerequisites).

Wait for the user's edits before scaffolding. This is the "plan the plan" gate.

### 4. Scaffold
Run the scaffold script with the agreed config (it never overwrites existing files unless `--force`):

```bash
python scripts/scaffold.py --name "<project name>" --profile <profile> --out <target-dir> \
  [--workstreams "ws1,ws2"] [--owner "<name>"] [--force]
```

Then adapt the generated files to the interview answers: fill the first intent, tailor `CLAUDE.md`, adjust gates and agent roles. Generated templates contain explanatory comments; keep them, they teach contributors the rules.

### 5. Wire governance
Read `references/governance-and-gates.md`. Configure gates (`sdlc/governance/gates.md`), the validation hook (`.claude/hooks/validate-docs.sh`) and, where CI exists, a CI job running `scripts/validate_docs.py`. Record autonomy tier per stage.

### 6. Validate and hand off
```bash
python scripts/validate_docs.py <target-dir>/sdlc
```
Fix every error. Then give the user a bootstrap report: structure created, graph, open decisions, first three actions. Offer to run the first stage (usually: finish `INT-0001`).

## Diagrams are mandatory for processes and flows

Whenever you describe or document a process, workflow, lifecycle, dependency or interaction, in generated files and in your own proposals, embed a **Mermaid** diagram inside the Markdown (a fenced `mermaid` block). A reviewer sees branches, loops, owners and gates at a glance, and the diagram diffs in git. Make every diagram descriptive **and readable on light and dark backgrounds**: start from the standard init header and shared colour palette (explicit fill and dark text colour on every style, white edge-label pills, flowcharts instead of `stateDiagram`, `participant` boxes in sequence diagrams); never rely on Mermaid's default theme. Make every diagram descriptive: a purpose line, meaningful node labels, labelled decisions, roles as subgraphs, gates and failure paths, a legend, and a short text narration. Full rules, diagram-type guide and patterns: `references/diagramming-guide.md`. Templates ship with placeholder diagrams; the validator warns when a type listed in `diagram_required` has none and errors on unclosed or unknown Mermaid blocks.

## Versioning and linking (summary)

Full rules live in `references/versioning-policy.md` and `references/linking-and-dependencies.md`. Essentials:

- Every document has YAML front matter with `id`, `type`, `version` (SemVer), `status`, `derived_from`, `depends_on`, `supersedes`.
- `derived_from` / `depends_on` entries are `ID@version` pins (the version the author reviewed against).
- MAJOR = meaning or scope changed, downstream must be re-derived. MINOR = additive. PATCH = editorial.
- Approved documents are immutable: change them by bumping the version (`scripts/bump.py`) or superseding them.
- `scripts/validate_docs.py` rebuilds `sdlc/.index/graph.json` and `graph.mmd`, flags broken links, cycles, stale pins and silent edits to approved documents.

## Resources

| Path | Use it when |
|---|---|
| `references/interview-guide.md` | Starting discovery |
| `references/domain-profiles.md` | Choosing profile and stage labels |
| `references/artifact-catalog.md` | Defining artifact types, owners, gates |
| `references/versioning-policy.md` | Deciding how to version and approve documents |
| `references/linking-and-dependencies.md` | Designing links, pins, graph, staleness |
| `references/governance-and-gates.md` | Setting gates, hooks, autonomy tiers, metrics |
| `references/diagramming-guide.md` | Drawing any process, flow, lifecycle or interaction (Mermaid) |
| `assets/templates/` | Source of every generated document |
| `scripts/scaffold.py` | Generating the project tree |
| `scripts/validate_docs.py` | Checking integrity, building the graph |
| `scripts/bump.py` | Bumping a version and listing impacted downstream documents |

## Gotchas

- Do not scaffold before the user confirms the artifact chain.
- Do not invent compliance requirements; ask, and record unknowns as open questions in the intent.
- Keep the system proportional: a one-person pilot needs 3 stages of ceremony, not 6. Offer the `lite` mode (`--mode lite`) which skips verification/release folders until needed.
- Never describe a process in prose only; add the Mermaid diagram.
- Never put secrets, credentials or personal data in generated documents.
