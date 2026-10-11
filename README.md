# agentic_sdlc

Enterprise agentic SDLC. This repository is a Claude Code plugin marketplace that ships the `agentic-sdlc-bootstrap` skill.

## What the skill does

`agentic-sdlc-bootstrap` sets up a complete, versioned and traceable agentic SDLC for any project, software or not (research programs, operations changes, launches, content or data pipelines, multi-workstream programs). It interviews you, proposes the artifact chain and its dependency graph, then scaffolds the document system with gates, agent roles and validation. Every process or flow is documented with an embedded Mermaid diagram. See [`skills/agentic-sdlc-bootstrap/SKILL.md`](skills/agentic-sdlc-bootstrap/SKILL.md).

## Install

### Claude Code (plugin marketplace, recommended)

One step (Claude Code 2.1.275 or later):

```bash
/plugin install agentic-sdlc --marketplace rafapc2/agentic_sdlc
```

Or in two steps:

```bash
/plugin marketplace add rafapc2/agentic_sdlc
/plugin install agentic-sdlc@agentic-sdlc-marketplace
```

From a shell, use `claude plugin marketplace add ...` and `claude plugin install ...` with the same arguments. Update later with `/plugin marketplace update agentic-sdlc-marketplace`.

### Claude Code (manual copy)

```bash
git clone https://github.com/rafapc2/agentic_sdlc
cp -r agentic_sdlc/skills/agentic-sdlc-bootstrap ~/.claude/skills/        # all projects
# or: cp -r ... <project>/.claude/skills/                                  # one project
```

### Claude.ai / Claude desktop

Zip the skill folder so that `agentic-sdlc-bootstrap/SKILL.md` is at the top level of the archive, then upload it under Settings, Capabilities, Skills. Organization admins can provision it for the whole team from the same place.

## Use

Ask for what you need in your own words; the skill triggers on requests to set up an agentic SDLC or workflow. When installed as a plugin the explicit command is `/agentic-sdlc:agentic-sdlc-bootstrap`. Example first prompt:

> I want to set up an agentic SDLC from scratch for moving our 120-truck fleet to electric: procurement, charging, driver training and budget. It is not software.

Day to day in a generated project:

```bash
python sdlc/_tools/new_doc.py sdlc spec "Title" --derived-from INT-0001@1.0.0   # new document
python sdlc/_tools/bump.py sdlc SPEC-0001 minor --note "Added R-4"              # new version + impact
python sdlc/_tools/validate_docs.py sdlc                                         # links, versions, diagrams, graph
```

## Repository layout

```
.claude-plugin/
  plugin.json            plugin manifest (name: agentic-sdlc)
  marketplace.json       marketplace manifest (name: agentic-sdlc-marketplace)
skills/
  agentic-sdlc-bootstrap/
    SKILL.md             workflow and rules
    references/          profiles, artifact catalog, versioning, linking, governance, diagramming
    assets/templates/    document, CLAUDE.md, agent-role and hook templates
    scripts/             scaffold.py, validate_docs.py, bump.py, new_doc.py
    evals/               example prompts
```

## Develop and test locally

```bash
claude plugin validate .                           # must print "Validation passed"
claude plugin marketplace add ./                   # use the working copy
claude plugin install agentic-sdlc@agentic-sdlc-marketplace
```

Release by bumping `version` in `.claude-plugin/plugin.json`; users get the new version on their next marketplace update.

## License

MIT, see [LICENSE](LICENSE).
