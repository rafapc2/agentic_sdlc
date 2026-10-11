# Domain profiles

A profile maps the canonical six stages to domain vocabulary and picks default artifact types. The canonical stage ids never change (`plan, design, build, test, deploy, maintain`) so tooling and the dependency graph stay uniform; only labels and artifact names differ.

| Profile | plan | design | build | test | deploy | maintain |
|---|---|---|---|---|---|---|
| software | Plan | Design | Build | Test | Deploy | Maintain |
| research | Frame (question) | Method | Execute | Validate | Publish | Monitor / follow-up |
| operations | Identify (problem) | Design change | Prepare | Rehearse | Roll out | Run / improve |
| launch | Opportunity | Strategy | Produce | Review | Launch | Learn |
| data-content | Brief | Structure | Produce | QA | Publish | Refresh |
| program | Charter | Architecture | Workstreams | Integration | Release | Operate |

## Artifact mapping by profile

| Canonical type | software | research | operations | launch | data-content | program |
|---|---|---|---|---|---|---|
| intent | intent | research question | problem statement | opportunity brief | content brief | program charter |
| spec | requirements + design spec | study protocol | change design | launch strategy | structure/schema spec | architecture & scope |
| plan | implementation plan | execution plan | runbook draft | launch plan | production plan | workstream plans |
| verification | tests, evals | validation protocol | rehearsal/dry-run | readiness review | QA checklist | integration review |
| review | PR review findings | peer review | change board notes | go/no-go review | editorial review | steering review |
| release | release record | publication record | rollout record | launch record | publication record | release record |
| operations | incident / metric breach | follow-up findings | run record | learning report | refresh record | operating review |

## Program profile (complex projects)

For projects with several streams, create one `INT` at program level and child workstreams, each with its own `SPEC`, `PLAN`, verification and release artifacts. Children declare `derived_from` the program-level documents. Cross-workstream coupling is expressed with `depends_on`. Add a program-level `integration` review before release. The scaffold flag `--workstreams "a,b,c"` generates one subtree per workstream.

## Custom profile
If nothing fits, start from `program`, rename labels in `sdlc/sdlc.config.json` (`stage_labels`, `types`) and re-run the validator. Do not add new canonical stages; add artifact types inside an existing stage.

## Lite mode
For pilots and individuals: keep `plan`, `build`, and `maintain` folders, and add `design`/`test`/`deploy` the first time they are needed. The validator tolerates absent folders.
