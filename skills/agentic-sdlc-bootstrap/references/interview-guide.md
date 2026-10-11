# Interview guide

Goal: learn enough to pick a profile, set gates and tailor artifacts, without interrogating the user. Infer from files, repos and prior conversation first. Ask in rounds of at most six questions, recommend a default for each.

## Round 1 - Purpose and shape
1. What are you trying to accomplish, and what does "done" look like?
2. What kind of work is it (software, research, operations change, launch, content/data, multi-workstream program)?
3. Who is involved (owner, approvers, contributors, non-technical stakeholders)?
4. What exists already (repo, tickets, documents, policies, past incidents)?
5. Is there a deadline or external dependency?
6. Is this a single deliverable or several parallel workstreams?

## Round 2 - Control and risk
1. Which decisions must a human always make (budget, legal, safety, publication)?
2. Any regulation, compliance or confidentiality constraint?
3. How much autonomy do you want per stage: *assist* (agent drafts, human does), *gated* (agent acts, human approves each artifact), *supervised-auto* (agent acts, human reviews exceptions)?
4. Where do documents live (git repo, shared drive, wiki)? Git is strongly preferred for versioning.
5. Which tools must integrate (CI, ticketing, chat, metrics store)?

## Round 3 - Measures
1. What would tell you the loop works (time from idea to approved intent, rework rate, defect or incident rate)?
2. What breach of a control band should trigger a new intent automatically?

## Output of the interview
Write the answers into `INT-0001` (problem, outcome, constraints, open questions) and into `sdlc/sdlc.config.json` (profile, gates, autonomy). Unknowns become *open questions*, never assumptions presented as facts.
