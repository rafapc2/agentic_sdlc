#!/usr/bin/env python3
"""Bump a lifecycle document's version, update `updated`, append a changelog row, and
report which downstream documents become stale or drift.

Usage:
  python bump.py <sdlc_dir> <ID> <major|minor|patch> --note "what changed" [--author NAME] [--status in_review] [--dry-run]

Rules (see references/versioning-policy.md):
  major  meaning/scope changed  -> dependants STALE
  minor  additive               -> dependants DRIFT
  patch  editorial              -> no action
Bumping an `approved` document moves it back to `in_review` unless --status is given,
because the changed content needs a fresh approval.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sdlclib as L  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sdlc_dir")
    ap.add_argument("doc_id")
    ap.add_argument("level", choices=["major", "minor", "patch"])
    ap.add_argument("--note", required=True)
    ap.add_argument("--author", default="agent")
    ap.add_argument("--status", choices=L.STATUSES)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    sdlc = Path(a.sdlc_dir).resolve()
    docs = {}
    for p, fm, body, perr in L.iter_docs(sdlc):
        if not perr and fm:
            docs[fm.get("id")] = (p, fm)
    if a.doc_id not in docs:
        print("ERROR: %s not found under %s" % (a.doc_id, sdlc)); return 1
    path, fm = docs[a.doc_id]
    old = fm["version"]
    maj, mnr, pat = L.semver(old)
    new = {"major": (maj + 1, 0, 0), "minor": (maj, mnr + 1, 0), "patch": (maj, mnr, pat + 1)}[a.level]
    new_v = "%d.%d.%d" % new
    today = date.today().isoformat()

    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^(version:\s*)\S+", r"\g<1>" + new_v, text, count=1, flags=re.M)
    text = re.sub(r"^(updated:\s*)\S+", r"\g<1>" + today, text, count=1, flags=re.M)
    status = a.status or ("in_review" if fm.get("status") == "approved" else fm.get("status"))
    if status != fm.get("status"):
        text = re.sub(r"^(status:\s*)\S+", r"\g<1>" + status, text, count=1, flags=re.M)
        text = re.sub(r"^(approved_on:).*$", r"\1", text, count=1, flags=re.M)
    row = "| %s | %s | %s | %s |" % (new_v, today, a.author, a.note.replace("|", "/"))
    text = text.rstrip("\n") + "\n" + row + "\n"

    print("%s: %s -> %s (%s), status %s -> %s" % (a.doc_id, old, new_v, a.level, fm.get("status"), status))
    impacted = []
    for did, (p, f) in docs.items():
        for kind in ("derived_from", "depends_on"):
            for raw in f.get(kind, []):
                pin = L.parse_pin(raw)
                if pin and pin[0] == a.doc_id:
                    impacted.append((did, kind, pin[1], f.get("status")))
    if impacted and a.level != "patch":
        label = "STALE (re-derive)" if a.level == "major" else "DRIFT (review)"
        print("Downstream impact - %s:" % label)
        for did, kind, pv, st in impacted:
            print("  - %s [%s, %s] pins %s@%s -> update to %s@%s" % (did, st, kind, a.doc_id, pv, a.doc_id, new_v))
    elif not impacted:
        print("No downstream documents depend on %s." % a.doc_id)
    if a.dry_run:
        print("(dry run, nothing written)"); return 0
    path.write_text(text, encoding="utf-8")
    print("Updated %s. Commit as: bump(%s): %s -> %s" % (path.relative_to(sdlc), a.doc_id, old, new_v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
