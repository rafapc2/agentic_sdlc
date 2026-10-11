#!/usr/bin/env python3
"""Create a new lifecycle document from a template with the next free id.

Usage:
  python new_doc.py <sdlc_dir> <type> "<title>" [--owner NAME] [--derived-from INT-0001@1.0.0 ...]
                    [--depends-on POL-0001@1.0.0 ...] [--dir RELATIVE_DIR]

The destination folder defaults to the standard folder for the type; the filename is <ID>-<slug>.md.
Links are written into the front matter; run validate_docs.py afterwards.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sdlclib as L  # noqa: E402

DEFAULT_DIRS = {"intent": "01-plan/intents", "policy": "01-plan/policies", "spec": "02-design/specs",
                "decision": "02-design/decisions", "plan": "03-build/plans", "verification": "04-test/verification",
                "review": "05-deploy/reviews", "release": "05-deploy/releases", "operations": "06-maintain/operations"}


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48] or "untitled"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sdlc_dir"); ap.add_argument("type"); ap.add_argument("title")
    ap.add_argument("--owner", default="unassigned")
    ap.add_argument("--derived-from", nargs="*", default=[])
    ap.add_argument("--depends-on", nargs="*", default=[])
    ap.add_argument("--dir")
    a = ap.parse_args()
    sdlc = Path(a.sdlc_dir).resolve()
    cfg = L.load_config(sdlc)
    if a.type not in cfg["types"]:
        print("ERROR: unknown type %r (known: %s)" % (a.type, ", ".join(sorted(cfg["types"])))); return 1
    prefix = cfg["types"][a.type]["prefix"]
    used = [int(m.group(1)) for p, fm, b, e in L.iter_docs(sdlc) if fm and (m := re.match(r"^%s-(\d{4})$" % prefix, fm.get("id", "")))]
    new_id = "%s-%04d" % (prefix, (max(used) + 1) if used else 1)
    tpl = sdlc / "_templates" / ("%s.md" % a.type)
    if not tpl.exists():
        tpl = Path(__file__).resolve().parent.parent / "assets" / "templates" / ("%s.md" % a.type)
    text = tpl.read_text(encoding="utf-8")
    for k, v in (("{{ID}}", new_id), ("{{TITLE}}", a.title), ("{{OWNER}}", a.owner), ("{{DATE}}", date.today().isoformat())):
        text = text.replace(k, v)
    for field, vals in (("derived_from", a.derived_from), ("depends_on", a.depends_on)):
        if vals:
            text = re.sub(r"^(%s:\s*)\[\]" % field, r"\g<1>[%s]" % ", ".join(vals), text, count=1, flags=re.M)
    dest_dir = sdlc / (a.dir or DEFAULT_DIRS.get(a.type, "."))
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / ("%s-%s.md" % (new_id, slugify(a.title)))
    dest.write_text(text, encoding="utf-8")
    print("Created %s" % dest.relative_to(sdlc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
