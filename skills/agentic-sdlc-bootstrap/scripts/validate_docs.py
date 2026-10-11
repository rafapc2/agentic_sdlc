#!/usr/bin/env python3
"""Validate lifecycle documents, resolve links, detect staleness, and build the dependency graph.

Usage:
  python validate_docs.py <sdlc_dir> [--git] [--strict] [--no-write]

Exit code 1 when errors are found (warnings never fail unless --strict).
Outputs (unless --no-write): <sdlc_dir>/.index/graph.json, graph.mmd, impact.md
--git additionally detects silent edits to approved documents by comparing with HEAD.
"""
import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sdlclib as L  # noqa: E402


def git_show(path, repo_root):
    try:
        out = subprocess.run(["git", "show", "HEAD:" + str(path.relative_to(repo_root))],
                             cwd=repo_root, capture_output=True, text=True, check=True)
        return out.stdout
    except Exception:
        return None


def git_root(path):
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=path,
                             capture_output=True, text=True, check=True)
        return Path(out.stdout.strip())
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sdlc_dir")
    ap.add_argument("--git", action="store_true", help="detect silent edits to approved docs vs HEAD")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--no-write", action="store_true", help="do not write .index outputs")
    args = ap.parse_args()

    sdlc = Path(args.sdlc_dir).resolve()
    if not sdlc.is_dir():
        print("ERROR: not a directory: %s" % sdlc)
        return 1
    cfg = L.load_config(sdlc)
    types = cfg["types"]
    prefix_to_type = {v["prefix"]: k for k, v in types.items()}
    errors, warns = [], []
    err = lambda p, m: errors.append("%s: %s" % (p, m))
    warn = lambda p, m: warns.append("%s: %s" % (p, m))

    docs = {}  # id -> dict
    for path, fm, body, perr in L.iter_docs(sdlc):
        rel = path.relative_to(sdlc)
        if perr:
            err(rel, perr)
            continue
        did = fm.get("id", "")
        m = L.ID_RE.match(did)
        if not m:
            err(rel, "invalid or missing id %r (expected PREFIX-NNNN)" % did)
            continue
        if did in docs:
            err(rel, "duplicate id %s (also %s)" % (did, docs[did]["rel"]))
            continue
        docs[did] = {"fm": fm, "body": body, "path": path, "rel": rel}

    # ---- per-document checks
    for did, d in docs.items():
        fm, body, rel = d["fm"], d["body"], d["rel"]
        t = fm.get("type", "")
        if t not in types:
            err(rel, "unknown type %r (known: %s)" % (t, ", ".join(sorted(types))))
            continue
        if types[t]["prefix"] != did.split("-")[0]:
            err(rel, "id prefix %s does not match type %s (expected %s)" % (did.split("-")[0], t, types[t]["prefix"]))
        if not d["path"].name.startswith(did):
            warn(rel, "filename should start with the id %s" % did)
        for req in ("title", "version", "status", "owner", "created", "updated", "stage"):
            if not fm.get(req):
                err(rel, "missing front matter field: %s" % req)
        if fm.get("stage") and fm["stage"] not in L.STAGES:
            err(rel, "stage %r not in %s" % (fm["stage"], "/".join(L.STAGES)))
        if fm.get("version") and not L.semver(fm["version"]):
            err(rel, "version %r is not MAJOR.MINOR.PATCH" % fm["version"])
        if fm.get("status") and fm["status"] not in L.STATUSES:
            err(rel, "status %r not in %s" % (fm["status"], "/".join(L.STATUSES)))
        for f in ("created", "updated", "approved_on"):
            v = fm.get(f)
            if v:
                try:
                    date.fromisoformat(v)
                except ValueError:
                    err(rel, "%s must be an ISO date (YYYY-MM-DD), got %r" % (f, v))
        v = L.semver(fm.get("version"))
        if fm.get("status") == "approved":
            if not fm.get("approver"):
                err(rel, "approved document requires 'approver'")
            if not fm.get("approved_on"):
                err(rel, "approved document requires 'approved_on'")
            if v and v[0] == 0:
                err(rel, "approved document must be version >= 1.0.0 (0.x means draft)")
        if fm.get("status") == "draft" and v and v[0] >= 1 and not fm.get("approved_on"):
            warn(rel, "draft with version >= 1.0.0: bumped after approval? set status in_review while editing")
        last = L.changelog_last_version(body)
        if last is None:
            err(rel, "missing Changelog table")
        elif last != fm.get("version"):
            err(rel, "Changelog newest row (%s) does not match version (%s)" % (last, fm.get("version")))
        blocks, mproblems = L.mermaid_blocks(body)
        for mp in mproblems:
            err(rel, mp)
        if t in cfg.get("diagram_required", []) and not blocks and fm.get("status") != "draft":
            warn(rel, "no ```mermaid diagram found; processes and flows must be documented with a descriptive diagram (references/diagramming-guide.md)")
        elif t in cfg.get("diagram_required", []) and not blocks:
            warn(rel, "draft has no ```mermaid diagram yet (required before review)")
        for mw in L.mermaid_contrast_warnings(blocks):
            warn(rel, mw)
        have = L.headings(body)
        for sec in cfg["required_sections"].get(t, []):
            if sec not in have:
                err(rel, "missing required section '## %s'" % sec)

    # ---- links
    edges = []  # (src, dst, kind, pinned_version)
    for did, d in docs.items():
        fm, rel = d["fm"], d["rel"]
        t = fm.get("type")
        for kind in ("derived_from", "depends_on"):
            for raw in fm.get(kind, []):
                pin = L.parse_pin(raw)
                if not pin:
                    err(rel, "%s entry %r must look like ID@MAJOR.MINOR.PATCH" % (kind, raw))
                    continue
                tid, pv = pin
                if tid == did:
                    err(rel, "%s points to itself" % kind)
                    continue
                if tid not in docs:
                    err(rel, "%s %s: target does not exist (BROKEN)" % (kind, tid))
                    continue
                tgt = docs[tid]["fm"]
                edges.append((did, tid, kind, pv))
                cur, pinned = L.semver(tgt.get("version")), L.semver(pv)
                if kind == "derived_from" and t in cfg["chain"]:
                    if tgt.get("type") not in cfg["chain"][t]:
                        err(rel, "illegal lineage: %s cannot derive from %s (allowed: %s)" % (t, tgt.get("type"), ", ".join(cfg["chain"][t])))
                if tgt.get("status") in ("superseded", "deprecated"):
                    err(rel, "%s %s is %s (DEAD LINK); repoint to its replacement" % (kind, tid, tgt["status"]))
                if cur and pinned:
                    if pinned > cur:
                        err(rel, "%s pin %s@%s is newer than current %s (FUTURE)" % (kind, tid, pv, tgt["version"]))
                    elif pinned[0] < cur[0]:
                        msg = "%s %s@%s is STALE: current %s has a new MAJOR" % (kind, tid, pv, tgt["version"])
                        (err if fm.get("status") == "approved" else warn)(rel, msg)
                    elif pinned < cur:
                        warn(rel, "%s %s@%s has DRIFT: current is %s" % (kind, tid, pv, tgt["version"]))
                if fm.get("status") == "approved" and kind == "derived_from" and tgt.get("status") not in ("approved",):
                    err(rel, "approved document derives from %s which is %s" % (tid, tgt.get("status")))
        for sid in fm.get("supersedes", []):
            if sid not in docs:
                err(rel, "supersedes %s: target does not exist" % sid)
            elif docs[sid]["fm"].get("status") != "superseded":
                warn(rel, "supersedes %s but that document is not marked superseded" % sid)
        roots = [k for k, v in types.items() if v.get("root")]
        if t and t not in roots and not fm.get("derived_from") and fm.get("status") != "draft":
            warn(rel, "orphan: non-root document has no derived_from")
        elif t and t not in roots and not fm.get("derived_from"):
            warn(rel, "draft has no derived_from yet (will be an orphan until linked)")

    # superseded docs must be named by someone
    named = {s for d in docs.values() for s in d["fm"].get("supersedes", [])}
    for did, d in docs.items():
        if d["fm"].get("status") == "superseded" and did not in named:
            warn(d["rel"], "superseded but no document lists it in supersedes")

    # ---- cycles
    graph = {}
    for s, t_, _k, _v in edges:
        graph.setdefault(s, set()).add(t_)
    color = {}
    def dfs(n, stack):
        color[n] = 1
        for m in graph.get(n, ()):
            if color.get(m) == 1:
                err("graph", "cycle: " + " -> ".join(stack + [n, m]))
            elif color.get(m) is None:
                dfs(m, stack + [n])
        color[n] = 2
    for n in list(graph):
        if color.get(n) is None:
            dfs(n, [])

    # ---- requirement coverage
    reqs = {}
    for did, d in docs.items():
        if d["fm"].get("type") == "spec":
            import re
            reqs[did] = set(re.findall(r"\*\*(R-\d+)\*\*", d["body"]))
    covered = {}
    for did, d in docs.items():
        for rid in d["fm"].get("covers", []):
            for spec_id in d["fm"].get("derived_from", []):
                sp = L.parse_pin(spec_id)
                if sp and sp[0] in reqs:
                    covered.setdefault((sp[0], rid), []).append(did)
                    if rid not in reqs[sp[0]]:
                        err(d["rel"], "covers %s which is not defined in %s" % (rid, sp[0]))
    for spec_id, rs in reqs.items():
        for r in sorted(rs):
            if (spec_id, r) not in covered and docs[spec_id]["fm"].get("status") in ("approved", "in_review"):
                warn(docs[spec_id]["rel"], "requirement %s has no plan/verification covering it" % r)

    # ---- silent edits (git)
    if args.git:
        root = git_root(sdlc)
        if root is None:
            warn("git", "not a git repository; skipping silent-edit check")
        else:
            for did, d in docs.items():
                prev = git_show(d["path"], root)
                if not prev:
                    continue
                pfm, pbody, perr = L.split_front_matter(prev)
                if perr or not pfm:
                    continue
                if pfm.get("status") == "approved" and d["fm"].get("version") == pfm.get("version"):
                    strip = lambda b: b.split("## Changelog")[0].strip()
                    if strip(pbody) != strip(d["body"]):
                        err(d["rel"], "approved document body changed without a version bump (silent edit)")

    # ---- outputs
    if not args.no_write:
        out = sdlc / ".index"
        out.mkdir(exist_ok=True)
        nodes = [{"id": k, "type": v["fm"].get("type"), "title": v["fm"].get("title"), "version": v["fm"].get("version"),
                  "status": v["fm"].get("status"), "stage": v["fm"].get("stage"), "path": str(v["rel"])} for k, v in sorted(docs.items())]
        def staleness(pv, cur):
            a, b = L.semver(pv), L.semver(cur)
            if not a or not b: return "unknown"
            return "stale" if a[0] < b[0] else ("drift" if a < b else "ok")
        gedges = [{"from": s, "to": t_, "kind": k, "pinned": v, "state": staleness(v, docs[t_]["fm"].get("version"))} for s, t_, k, v in edges]
        (out / "graph.json").write_text(json.dumps({"nodes": nodes, "edges": gedges}, indent=2) + "\n", encoding="utf-8")
        ml = ["%% GENERATED by validate_docs.py - do not edit", L.MERMAID_INIT, "flowchart LR"]
        for n in nodes:
            label = "%s v%s<br/>%s" % (n["id"], n["version"], (n["title"] or "").replace('"', "'"))
            ml.append('  %s["%s"]:::%s' % (n["id"].replace("-", "_"), label, n["status"]))
        for e in gedges:
            arrow = "-->" if e["kind"] == "derived_from" else "-.->"
            mark = "" if e["state"] == "ok" else "|%s|" % e["state"]
            ml.append("  %s %s%s %s" % (e["to"].replace("-", "_"), arrow, mark, e["from"].replace("-", "_")))
        ml += ["  classDef approved fill:#bbf7d0,stroke:#166534,stroke-width:2px,color:#111827;",
               "  classDef draft fill:#f1f5f9,stroke:#475569,stroke-width:2px,color:#111827;",
               "  classDef in_review fill:#dbeafe,stroke:#1d4ed8,stroke-width:2px,color:#111827;",
               "  classDef superseded fill:#f1f5f9,stroke:#475569,stroke-width:2px,stroke-dasharray:4,color:#111827;",
               "  classDef deprecated fill:#f1f5f9,stroke:#475569,stroke-width:2px,stroke-dasharray:4,color:#111827;",
               "  linkStyle default stroke-width:2px;"]
        (out / "graph.mmd").write_text("\n".join(ml) + "\n", encoding="utf-8")
        down = {}
        for s, t_, k, _v in edges:
            down.setdefault(t_, []).append((s, k))
        il = ["# Impact report", "<!-- GENERATED by validate_docs.py - do not edit. Lists what is affected if a document changes. -->", ""]
        for n in nodes:
            ds = down.get(n["id"], [])
            il.append("## %s (v%s, %s) %s" % (n["id"], n["version"], n["status"], n["title"]))
            il += ["- %s (%s)" % (s, k) for s, k in ds] or ["- _nothing depends on this_"]
            il.append("")
        (out / "impact.md").write_text("\n".join(il), encoding="utf-8")

    for w in warns:
        print("WARN  " + w)
    for e in errors:
        print("ERROR " + e)
    print("\n%d document(s), %d error(s), %d warning(s)" % (len(docs), len(errors), len(warns)))
    return 1 if errors or (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
