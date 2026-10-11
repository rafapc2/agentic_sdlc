# {{PROJECT}} - agent operating guide
<!-- CLAUDE.md gives every agent session the context a new team member would need. Keep it short;
     move detail into sdlc/ documents and skills. Review it whenever an agent repeats a mistake. -->

## What this project is
{{PROJECT}} runs on an agentic SDLC (profile: {{PROFILE}}). Work moves through stages; each stage ends by
committing one artifact in `sdlc/`, and the next stage starts by reading it. Humans approve at gates.

## Where things live
- `sdlc/` - all lifecycle documents, one folder per stage (see `sdlc/README.md`).
- `sdlc/sdlc.config.json` - profile, id prefixes, allowed lineage, autonomy tier per stage.
- `sdlc/governance/gates.md` - who approves what.
- `sdlc/.index/` - GENERATED graph and impact reports. Never edit by hand.
- `.claude/agents/` - role definitions; `.claude/hooks/` - enforcement.

## Document rules (the agent must follow)
1. Every document has YAML front matter with id, type, version, status, derived_from, depends_on. Copy from `assets` templates in `sdlc/_templates/`.
2. Never edit the body of an `approved` document. Bump its version (`python sdlc/_tools/bump.py <ID> <major|minor|patch> --note "..."`) and send it back to review, or supersede it.
3. Link upstream documents with pinned versions (`ID@1.2.0`). When an upstream document changes, update the pin in the same change.
4. Run `python sdlc/_tools/validate_docs.py sdlc` before finishing any task that touched `sdlc/`. Fix all errors.
5. Do not set `status: approved` yourself; only a human approver does that.
6. Whenever you describe or document a process, flow, lifecycle, dependency or interaction, embed a descriptive Mermaid diagram (```mermaid fenced block) in the Markdown file: purpose line, labelled decisions, roles, gates, failure path, legend, and a short text narration. See `.claude/skills` or the bootstrap skill's `references/diagramming-guide.md`.

## Commands
<!-- List exact commands so agents verify their own work. Replace with real ones. -->
- Validate documents: `python sdlc/_tools/validate_docs.py sdlc`
- Project verification: _add test / lint / build / check commands here_

## Conventions
<!-- Add naming, style, tooling and domain rules discovered while working. -->
- Write documents in English, concise, with numbered requirements (R-1...).

## Verification before "done"
Work is done only when the relevant checks pass and the validator reports no errors.
