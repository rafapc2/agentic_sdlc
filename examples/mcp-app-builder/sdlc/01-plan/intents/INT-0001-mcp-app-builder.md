---
id: INT-0001                 # Stable unique id, never reused. Format PREFIX-NNNN.
type: intent                   # Document type; must match the id prefix (see sdlc.config.json).
title: MCP App Builder           # Short human title.
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

# Intent: MCP App Builder
<!-- Root of the chain. Every spec, plan and release for the product traces back to this intent. -->

## Problem
People who want an AI assistant to use their data or services need an MCP (Model Context Protocol) server, and
increasingly an *MCP App* (a tool that also returns an interactive UI rendered inside the chat client). Building
one by hand needs protocol knowledge, TypeScript or Python, hosting, auth and testing. Non-engineers cannot do it
and engineers lose hours on boilerplate. "Lovable for websites" exists; nothing equivalent exists for MCP apps.

**Purpose:** shows how a person gets an MCP app today and where the effort and failures concentrate.

```mermaid
flowchart TD
  subgraph Human
    H1([Person with an idea])
    H2[Read MCP spec and SDK docs]
    H3[Write server code by hand]
    H4[Set up hosting, auth and secrets]
    G{Works in the AI client?}
  end
  subgraph Tools
    T1[Inspector or client for manual testing]
  end
  H1 --> H2 --> H3 --> H4 --> T1 --> G
  G -- yes --> N([Usable MCP app after days])
  G -- no, protocol or schema error --> H3
```
Key: diamond = decision; rounded = start or end; the loop on failure is where most time is lost.
- The path is entirely manual and requires an engineer.
- Failures are found late, only when a real client calls the server.

## Proposed outcome
A person describes an MCP app in natural language and gets, within minutes, a tested, previewable and deployable
MCP server (optionally with an interactive UI), then iterates on it by chatting. Success means: first working
preview in under 5 minutes for a simple app, at least 80% of prompts in the eval set produce a server that passes
protocol checks on the first attempt, and a deployed app can be connected to a standard MCP client by URL.

**Purpose:** shows the target flow, where the agent does the work and where the human must decide.

```mermaid
flowchart TD
  subgraph Human
    H1([Describe the app in a prompt])
    G1{Manifest looks right?}
    G2{Preview behaves as wanted?}
    G3{Approve deploy?}
  end
  subgraph Agent
    A1[Draft app manifest: tools, resources, UI]
    A2[Generate server code from manifest]
    A3[Run automated checks in sandbox]
    A4[Deploy to hosted endpoint]
  end
  H1 --> A1 --> G1
  G1 -- no, edit the manifest --> A1
  G1 -- yes --> A2 --> A3
  A3 -- checks fail, auto-repair up to 3 times --> A2
  A3 -- checks pass --> G2
  G2 -- no, describe the change --> A1
  G2 -- yes --> G3
  G3 -- yes --> A4 --> N([Connect URL shared])
  G3 -- no --> G2
```
Key: diamond = human gate; rectangles = agent steps; every failure edge returns to an earlier step.
- The human approves the manifest before any code is written, then the preview, then the deploy.
- Automated checks gate the preview, so humans never see a server that fails the protocol.

## Affected users and systems
- Primary users: non-engineers and "citizen builders" who want AI-connected tools.
- Secondary users: developers who want a head start and will export the code.
- Systems: LLM provider, code sandbox, hosting platform, secret vault, MCP clients used for testing.

## Constraints
- Generated servers must follow the current MCP specification and the official SDKs.
- Generated code must comply with POL-0001 (safety of generated servers).
- Out of scope for the MVP: marketplace of apps, billing, team collaboration, non-HTTP transports.
- Budget and deadline are not defined yet (see open questions).

## Open questions
- [ ] Which hosting target does the MVP deploy to (own platform, Cloudflare, other)?
- [ ] Is TypeScript the only generated language for the MVP? (proposed: yes, see DEC-0001)
- [ ] Which MCP clients must the preview support for UI rendering?
- [ ] Pricing and usage limits for generation and hosting.

## Related documents
- Derived from: _none (root document)_
- Depended on by: [SPEC-0001](../../02-design/specs/SPEC-0001-mcp-app-builder-mvp.md)
- Lifecycle map: [sdlc/README.md](../../README.md)

## Changelog
| version | date | author | change |
|---|---|---|---|
| 0.1.0 | 2026-11-22 | Rafa | Initial draft |
