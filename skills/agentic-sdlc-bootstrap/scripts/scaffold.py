#!/usr/bin/env python3
"""Generate an agentic SDLC project skeleton.

Usage:
  python scaffold.py --name "Project" --profile software|research|operations|launch|data-content|program|custom
                     --out DIR [--owner NAME] [--workstreams "a,b"] [--mode full|lite] [--force]

Creates (never overwriting unless --force): CLAUDE.md, sdlc/ (config, README, gates, stage folders,
templates, tools, first intent), and .claude/ (agent roles, validation hook, settings).
"""
import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets" / "templates"
sys.path.insert(0, str(HERE))
import sdlclib as L  # noqa: E402

LABELS = {
    "software": ["Plan", "Design", "Build", "Test", "Deploy", "Maintain"],
    "research": ["Frame", "Method", "Execute", "Validate", "Publish", "Monitor"],
    "operations": ["Identify", "Design change", "Prepare", "Rehearse", "Roll out", "Run"],
    "launch": ["Opportunity", "Strategy", "Produce", "Review", "Launch", "Learn"],
    "data-content": ["Brief", "Structure", "Produce", "QA", "Publish", "Refresh"],
    "program": ["Charter", "Architecture", "Workstreams", "Integration", "Release", "Operate"],
    "custom": ["Plan", "Design", "Build", "Test", "Deploy", "Maintain"],
}
FOLDERS = ["01-plan/intents", "01-plan/policies", "02-design/specs", "02-design/decisions", "03-build/plans",
           "04-test/verification", "05-deploy/reviews", "05-deploy/releases", "06-maintain/operations"]
LITE_FOLDERS = ["01-plan/intents", "01-plan/policies", "02-design/specs", "03-build/plans", "06-maintain/operations"]
MERMAID_INIT = '%%{init: {"theme":"base","themeVariables":{"fontFamily":"Arial, sans-serif","fontSize":"16px","lineColor":"#8b9bb0","textColor":"#111827","primaryTextColor":"#111827","primaryColor":"#dbeafe","primaryBorderColor":"#1d4ed8","edgeLabelBackground":"#ffffff","clusterBkg":"#f1f5f9","clusterBorder":"#475569","titleColor":"#111827"},"flowchart":{"curve":"basis","padding":14}}}%%'
ROLES = {
    "drafter": ("Drafts intents and specs from conversation and policies; flags areas of concern.",
                "Read, Grep, Glob, Write, Edit",
                "- Turn the originator's words into `intent` documents.\n- Turn an approved intent into a `spec` with numbered requirements (R-n).\n- Check every policy listed in depends_on and record compliance.",
                "- The approved INT-* you derive from.\n- Every POL-* that applies.", "A draft document using `sdlc/_templates/`, status `draft`."),
    "planner": ("Produces implementation or execution plans from an approved spec before any work starts.",
                "Read, Grep, Glob, Write, Edit",
                "- Produce a `plan` covering requirements with `covers`.\n- State risks, verification and rollback before execution.",
                "- The approved SPEC-* and relevant DEC-*.", "A `plan` document in `03-build/plans/`."),
    "builder": ("Executes an approved plan and produces the deliverables; runs the project checks.",
                "Read, Grep, Glob, Write, Edit, Bash",
                "- Follow the approved PLAN-* step by step.\n- Run the verification commands from CLAUDE.md before reporting done.",
                "- The approved PLAN-* and CLAUDE.md.", "Deliverables plus an updated plan Results/notes; never change the spec."),
    "verifier": ("Independent, read-only checker that evaluates deliverables against the spec and records evidence.",
                 "Read, Grep, Glob, Bash",
                 "- Run the checks defined in the `verification` document and record results.\n- Never edit deliverables or tests to make checks pass.",
                 "- The SPEC-*, PLAN-* and VER-* involved.", "Updated `verification` Results/Evidence sections; findings as a `review` input."),
    "reviewer": ("Layered reviewer that checks deliverables against policies and flags items for human attention.",
                 "Read, Grep, Glob",
                 "- Review for correctness, policy compliance and risk.\n- Prepare a `review` document; mark which items need human examination.",
                 "- PLAN-*, VER-*, POL-* and the deliverables.", "A `review` document with findings."),
    "operator": ("Monitors the running result, diagnoses control-band breaches and writes follow-up intents.",
                 "Read, Grep, Glob, Write, Edit, Bash",
                 "- Record incidents, breaches and learnings as `operations` documents.\n- Open a new `intent` derived from the record when action is needed.",
                 "- The latest REL-* and the metrics defined in the spec.", "An `operations` document and, if needed, a new draft `intent`."),
}


def fill(text, **kw):
    for k, v in kw.items():
        text = text.replace("{{%s}}" % k, v)
    return text


def write(path, content, force, created, skipped):
    if path.exists() and not force:
        skipped.append(path); return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--profile", required=True, choices=sorted(LABELS))
    ap.add_argument("--out", required=True)
    ap.add_argument("--owner", default="unassigned")
    ap.add_argument("--workstreams", default="")
    ap.add_argument("--mode", choices=["full", "lite"], default="full")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    out = Path(a.out).resolve()
    sdlc = out / "sdlc"
    created, skipped = [], []
    today = date.today().isoformat()
    ws = [w.strip() for w in a.workstreams.split(",") if w.strip()]
    if ws and a.profile != "program":
        print("note: workstreams given; consider --profile program")

    # config
    cfg = {
        "_comment": "Edit types/chain/required_sections to customise. Canonical stage ids never change; only labels do.",
        "project": a.name, "profile": a.profile, "mode": a.mode, "created": today,
        "stage_labels": dict(zip(L.STAGES, LABELS[a.profile])),
        "autonomy": {s: "gated" for s in L.STAGES},
        "workstreams": ws,
        "types": L.DEFAULT_CONFIG["types"], "chain": L.DEFAULT_CONFIG["chain"],
        "required_sections": L.DEFAULT_CONFIG["required_sections"],
        "diagram_required": L.DEFAULT_CONFIG["diagram_required"],
    }
    write(sdlc / "sdlc.config.json", json.dumps(cfg, indent=2) + "\n", a.force, created, skipped)

    # folders
    for f in (FOLDERS if a.mode == "full" else LITE_FOLDERS):
        (sdlc / f).mkdir(parents=True, exist_ok=True)
        gk = sdlc / f / ".gitkeep"
        if not gk.exists():
            gk.write_text("")
    for w in ws:
        for f in ("02-design/specs", "03-build/plans", "04-test/verification", "05-deploy/releases", "06-maintain/operations"):
            (sdlc / "workstreams" / w / f).mkdir(parents=True, exist_ok=True)
            (sdlc / "workstreams" / w / f / ".gitkeep").write_text("")

    # templates and tools
    for t in sorted(ASSETS.glob("*.md")):
        if t.name in ("CLAUDE.md", "agent-role.md"):
            continue
        write(sdlc / "_templates" / t.name, t.read_text(encoding="utf-8"), a.force, created, skipped)
    for s in ("sdlclib.py", "validate_docs.py", "bump.py", "new_doc.py"):
        write(sdlc / "_tools" / s, (HERE / s).read_text(encoding="utf-8"), a.force, created, skipped)

    # README + gates
    labels = cfg["stage_labels"]
    rows = "\n".join("| %d | %s (`%s`) | %s |" % (i + 1, labels[s], s, "gated") for i, s in enumerate(L.STAGES))
    readme = f"""# {a.name} - lifecycle documents
<!-- Entry point for humans. Generated by the agentic-sdlc-bootstrap skill; safe to edit. -->

Profile: **{a.profile}** | Mode: **{a.mode}** | Created: {today}

## How it works
Each stage ends by committing one artifact; the next stage starts by reading it. Every document has an id,
a version and pinned links to its upstream documents. Humans approve at the gates in `governance/gates.md`.

| # | Stage | Autonomy |
|---|---|---|
{rows}

## Lifecycle at a glance
Purpose: shows the loop, the artifact each stage commits, and where a human must approve.

```mermaid
@@INIT@@
flowchart TD
  P[Plan<br/>INT intent] --> G1{{"G1 owner accepts"}}
  G1 --> D[Design<br/>SPEC spec]
  D --> G2{{"G2 owner approves"}}
  G2 --> B[Build<br/>PLAN plan + deliverables]
  B --> G3{{"G3 lead approves plan"}}
  G3 --> T[Test<br/>VER verification]
  T --> G4{{"G4 review signed"}}
  G4 --> R[Deploy<br/>REV review, REL release]
  R --> G5{{"G5 release approved"}}
  G5 --> M[Maintain<br/>OPS record]
  M -- breach or learning --> P
  classDef gate fill:#fde68a,stroke:#92400e,stroke-width:2px,color:#111827;
  class G1,G2,G3,G4,G5 gate;
  linkStyle default stroke-width:2px;
```
Key: amber diamonds = human approval gates (details in `governance/gates.md`).
- Each stage commits one artifact that the next stage reads.
- Maintain closes the loop by writing the next intent.

## Folders
- `01-plan/` intents and policies - `02-design/` specs and decisions - `03-build/` plans
- `04-test/` verification - `05-deploy/` reviews and releases - `06-maintain/` operations records
- `workstreams/` per-workstream stages (program profile)
- `_templates/` document templates - `_tools/` validator and helpers - `.index/` GENERATED graph and impact reports

## Everyday commands
```bash
python sdlc/_tools/new_doc.py sdlc spec "Checkout redesign" --derived-from INT-0001@1.0.0
python sdlc/_tools/bump.py sdlc SPEC-0001 minor --note "Added R-4"
python sdlc/_tools/validate_docs.py sdlc          # add --git in CI to catch silent edits
```
View the dependency graph: open `.index/graph.mmd` in any Mermaid renderer. What depends on what: `.index/impact.md`.
"""
    readme = readme.replace("@@INIT@@", MERMAID_INIT)
    write(sdlc / "README.md", readme, a.force, created, skipped)
    gates = f"""# Gates
<!-- A gate is the human decision point that ends a stage. Fill approver names; keep evidence concrete. -->

| Gate | Artifact approved | Approver (role/name) | Evidence required | Triggers next |
|---|---|---|---|---|
| G1 | INT accepted | {a.owner} | Problem, outcome, constraints, open questions answered or deferred | Design pass |
| G2 | SPEC approved | {a.owner} | Requirements numbered; policy compliance filled; concerns reviewed | Planning |
| G3 | PLAN approved | _name_ | Risks, verification and rollback present | Execution |
| G4 | VER passed + REV signed | _name_ | All covered requirements verified; findings resolved | Release |
| G5 | REL approved | _name_ | Rollback path confirmed | Rollout |
| G6 | OPS reviewed | _name_ | Cause and follow-up intent recorded | New intent (loop) |

## Approval flow
Purpose: shows how any artifact moves from draft to approved and what happens on rejection or later change.

```mermaid
@@INIT@@
flowchart LR
  draft(["draft"]):::neutral -- author requests review --> in_review(["in_review"]):::agent
  in_review -- changes requested --> draft
  in_review -- "approver signs off (human)" --> approved(["approved"]):::ok
  approved -- "version bump after content change" --> in_review
  approved -- replaced --> superseded(["superseded"]):::neutral
  classDef neutral fill:#f1f5f9,stroke:#475569,stroke-width:2px,color:#111827;
  classDef agent fill:#dbeafe,stroke:#1d4ed8,stroke-width:2px,color:#111827;
  classDef ok fill:#bbf7d0,stroke:#166534,stroke-width:2px,color:#111827;
  linkStyle default stroke-width:2px;
```
- Only a human approver moves a document to `approved`.
- Editing approved content always creates a new version that re-enters review.

## Rules
- Status `approved` is set only by the named human approver, in a separate commit/PR approval from content edits.
- Raise a stage's autonomy tier (`sdlc.config.json` -> `autonomy`) only after its gate, checks and rollback path exist.
- Actions that publish, delete or spend money require human approval regardless of tier.
"""
    gates = gates.replace("@@INIT@@", MERMAID_INIT)
    write(sdlc / "governance" / "gates.md", gates, a.force, created, skipped)

    # first intent
    intent = fill((ASSETS / "intent.md").read_text(encoding="utf-8"), ID="INT-0001", TITLE=a.name, OWNER=a.owner, DATE=today)
    slug = re.sub(r"[^a-z0-9]+", "-", a.name.lower()).strip("-")[:48]
    write(sdlc / "01-plan" / "intents" / ("INT-0001-%s.md" % slug), intent, a.force, created, skipped)

    # CLAUDE.md, agents, hook, settings
    write(out / "CLAUDE.md", fill((ASSETS / "CLAUDE.md").read_text(encoding="utf-8"), PROJECT=a.name, PROFILE=a.profile), a.force, created, skipped)
    role_tpl = (ASSETS / "agent-role.md").read_text(encoding="utf-8")
    for role, (desc, tools, resp, inputs, output) in ROLES.items():
        write(out / ".claude" / "agents" / ("%s.md" % role),
              fill(role_tpl, ROLE=role, ROLE_DESCRIPTION=desc, TOOLS=tools, PROJECT=a.name, RESPONSIBILITIES=resp, INPUTS=inputs, OUTPUT=output),
              a.force, created, skipped)
    hook = out / ".claude" / "hooks" / "validate-docs.sh"
    write(hook, (ASSETS / "validate-docs.sh").read_text(encoding="utf-8"), a.force, created, skipped)
    if hook.exists():
        hook.chmod(0o755)
    settings = {"hooks": {"PostToolUse": [{"matcher": "Edit|Write|MultiEdit", "hooks": [
        {"type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-docs.sh"}]}]}}
    write(out / ".claude" / "settings.json", json.dumps(settings, indent=2) + "\n", a.force, created, skipped)

    print("Created %d file(s) under %s" % (len(created), out))
    if skipped:
        print("Skipped %d existing file(s) (use --force to overwrite):" % len(skipped))
        for p in skipped[:10]:
            print("  - %s" % p.relative_to(out))
    print("Next: python %s/_tools/validate_docs.py %s" % ("sdlc", "sdlc"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
