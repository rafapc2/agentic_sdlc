# Versioning policy

Goal: any reader can tell *which version of what* a downstream document was built from, and detect when it is out of date. Git provides history; the front matter provides meaning.

## Version number (SemVer for documents)
`MAJOR.MINOR.PATCH`, starting at `0.1.0` for drafts.

| Bump | Use when | Downstream effect |
|---|---|---|
| MAJOR | Meaning, scope, goal, constraint or requirement changed or removed | Every document derived from it is **stale** and must be re-derived or re-approved |
| MINOR | Additive, backward-compatible content (new requirement, new section) | Downstream shows **drift** (warning); review whether it should absorb the change |
| PATCH | Editorial: typos, clarifications, formatting, links | No downstream action |

`0.x` means draft: anything may change. First approval promotes to `1.0.0`.

## Status lifecycle
`draft -> in_review -> approved -> superseded | deprecated`

- `draft`: author editing; any change allowed, version stays `0.x`.
- `in_review`: frozen for review; changes only in response to review comments.
- `approved`: immutable. Requires `approver` and `approved_on`. Content changes require a new version (re-enter `in_review`) or a superseding document.
- `superseded`: replaced; must be named by another document's `supersedes`.
- `deprecated`: no longer applies, nothing replaces it.

## Changelog
Each document ends with a `## Changelog` table: `| version | date | author | change |`. The newest row must match the front matter `version`. The validator enforces this; `scripts/bump.py` writes it.

## Git conventions
- One commit per approval, message `approve(<ID>): v<version>`; one per bump `bump(<ID>): <old> -> <new>`.
- Tag approved baselines `<ID>@<version>` (e.g. `SPEC-0003@1.0.0`) so releases can cite exact inputs.
- Approval = the merge of a PR that sets `status: approved`. The merge record is the audit evidence; do not self-approve by editing status in the same commit that edits content.
- Silent edit detection: if a file was `approved` at the previous commit and its body changed without a version bump, the validator reports an error (`--git` mode).

## Superseding vs bumping
Bump when the same document evolves (same ID). Supersede (new ID, `supersedes: [OLD-ID]`) when the document is replaced by a different framing, or for decisions (DEC), which are append-only: never rewrite a decision, record a new one.

## IDs
`<PREFIX>-<4 digits>` (e.g. `INT-0001`). IDs are never reused or renumbered. Filenames are `<ID>-<slug>.md`; renaming the slug is allowed, changing the ID is not.

## Dates
ISO 8601 (`YYYY-MM-DD`). `updated` changes with every version bump.
