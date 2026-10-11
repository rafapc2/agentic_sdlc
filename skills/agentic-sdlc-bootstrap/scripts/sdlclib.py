"""Shared helpers for the agentic SDLC tools (stdlib only).

Parses the restricted YAML front matter used by lifecycle documents:
  key: value            scalar
  key: [a, b]           inline list
  key:                  empty (None / empty string)
Trailing ' # comment' is ignored. Nested YAML is intentionally unsupported so the
tools run anywhere without PyYAML.
"""
import json
import re
from pathlib import Path

SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
PIN = re.compile(r"^([A-Z]+-\d{4})@(\d+\.\d+\.\d+)$")
ID_RE = re.compile(r"^([A-Z]+)-(\d{4})$")
LIST_FIELDS = ("derived_from", "depends_on", "supersedes", "external_refs", "covers")

DEFAULT_CONFIG = {
    "types": {  # type -> {prefix, stage, root}
        "intent": {"prefix": "INT", "stage": "plan", "root": True},
        "policy": {"prefix": "POL", "stage": "plan", "root": True},
        "spec": {"prefix": "SPEC", "stage": "design"},
        "decision": {"prefix": "DEC", "stage": "build"},
        "plan": {"prefix": "PLAN", "stage": "build"},
        "verification": {"prefix": "VER", "stage": "test"},
        "review": {"prefix": "REV", "stage": "deploy"},
        "release": {"prefix": "REL", "stage": "deploy"},
        "operations": {"prefix": "OPS", "stage": "maintain"},
    },
    # Legal derived_from pairs: downstream type -> allowed upstream types
    "chain": {
        "spec": ["intent"],
        "decision": ["spec", "plan", "intent"],
        "plan": ["spec"],
        "verification": ["spec", "plan"],
        "review": ["plan", "verification"],
        "release": ["review"],
        "operations": ["release"],
        "intent": ["operations"],  # Maintain writes the next intent (optional for roots)
    },
    # Types whose documents must embed at least one ```mermaid block (validator warning otherwise)
    "diagram_required": ["intent", "spec", "plan", "verification", "release", "operations", "policy"],
    "required_sections": {
        "intent": ["Problem", "Proposed outcome", "Affected users and systems", "Constraints", "Open questions", "Changelog"],
        "spec": ["Summary", "Requirements", "Design", "Policy compliance", "Areas of concern", "Acceptance criteria", "Changelog"],
        "plan": ["Objective", "Steps", "Deliverables touched", "Risks", "Verification", "Rollback", "Changelog"],
        "decision": ["Context", "Options", "Decision", "Consequences", "Changelog"],
        "verification": ["Scope", "Checks", "Evidence", "Results", "Changelog"],
        "review": ["Scope", "Findings", "Human sign-off", "Changelog"],
        "release": ["Contents", "Approvals", "Rollback path", "Changelog"],
        "operations": ["Trigger", "Diagnosis", "Impact", "Follow-up", "Changelog"],
        "policy": ["Statement", "Scope", "Owner and source of truth", "Enforcement", "Changelog"],
    },
}
STATUSES = ("draft", "in_review", "approved", "superseded", "deprecated")
STAGES = ("plan", "design", "build", "test", "deploy", "maintain")


def parse_value(raw):
    raw = re.sub(r"(^|\s)#.*$", "", raw).strip()  # drop trailing comment (needs whitespace before '#')
    if raw.startswith("["):
        end = raw.rfind("]")
        inner = raw[1:end] if end != -1 else raw[1:]
        return [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
    return raw.strip("'\"")


def split_front_matter(text):
    """Return (front_matter_dict, body, error). error is None when parsing succeeded."""
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*(?:\n(.*))?$", text, re.S)
    if not m:
        return None, text, "missing or unclosed front matter"
    head, body = m.group(1), m.group(2) or ""
    fm = {}
    for line in head.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        km = re.match(r"^([A-Za-z_]\w*)\s*:\s*(.*)$", line)
        if not km:
            return None, body, "unparseable front matter line: %r" % line
        key, val = km.group(1), parse_value(km.group(2))
        if key in LIST_FIELDS and not isinstance(val, list):
            val = [val] if val else []
        fm[key] = val
    return fm, body, None


def load_config(sdlc_dir):
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    p = Path(sdlc_dir) / "sdlc.config.json"
    if p.exists():
        user = json.loads(p.read_text(encoding="utf-8"))
        for k in ("types", "chain", "required_sections"):
            if k in user:
                cfg[k].update(user[k])
        for k, v in user.items():
            if k not in ("types", "chain", "required_sections"):
                cfg[k] = v
    return cfg


def iter_docs(sdlc_dir):
    """Yield (path, fm, body, error) for every markdown file carrying front matter under sdlc/.
    Skips generated, template and tool folders and plain README/gates files without front matter."""
    skip = {".index", "_templates", "_tools"}
    for p in sorted(Path(sdlc_dir).rglob("*.md")):
        if any(part in skip for part in p.relative_to(sdlc_dir).parts):
            continue
        text = p.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue  # not a lifecycle document (README, gates)
        fm, body, err = split_front_matter(text)
        yield p, fm, body, err


def semver(v):
    m = SEMVER.match(v or "")
    return tuple(int(x) for x in m.groups()) if m else None


def parse_pin(s):
    m = PIN.match(s or "")
    return (m.group(1), m.group(2)) if m else None


def changelog_last_version(body):
    idx = body.rfind("## Changelog")
    if idx == -1:
        return None
    last = None
    for line in body[idx:].splitlines():
        m = re.match(r"^\|\s*(\d+\.\d+\.\d+)\s*\|", line)
        if m:
            last = m.group(1)
    return last


def headings(body):
    return {m.group(1).strip() for m in re.finditer(r"^##\s+(.+?)\s*$", body, re.M)}


MERMAID_TYPES = ("flowchart", "graph", "sequenceDiagram", "stateDiagram", "stateDiagram-v2", "classDiagram", "erDiagram",
                 "gantt", "timeline", "journey", "pie", "mindmap", "gitGraph", "C4Context", "quadrantChart", "requirementDiagram")


def mermaid_blocks(body):
    """Return (blocks, problems). A block is the text inside a ```mermaid fence; problems lists unclosed fences
    and blocks whose first keyword is not a known Mermaid diagram type."""
    blocks, problems, lines, i = [], [], body.splitlines(), 0
    while i < len(lines):
        if lines[i].strip().startswith("```mermaid"):
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            if j >= len(lines):
                problems.append("unclosed ```mermaid fence at body line %d" % (i + 1))
                break
            block = "\n".join(lines[i + 1:j]).strip()
            blocks.append(block)
            code = "\n".join(l for l in block.splitlines() if l.strip() and not l.strip().startswith("%%"))
            first = (code.split() or [""])[0].rstrip(";")
            if not any(first == t for t in MERMAID_TYPES):
                problems.append("mermaid block at body line %d starts with unknown diagram type %r" % (i + 1, first))
            i = j
        i += 1
    return blocks, problems


MERMAID_INIT = '%%{init: {"theme":"base","themeVariables":{"fontFamily":"Arial, sans-serif","fontSize":"16px","lineColor":"#8b9bb0","textColor":"#111827","primaryTextColor":"#111827","primaryColor":"#dbeafe","primaryBorderColor":"#1d4ed8","edgeLabelBackground":"#ffffff","clusterBkg":"#f1f5f9","clusterBorder":"#475569","titleColor":"#111827"},"flowchart":{"curve":"basis","padding":14}}}%%'


def mermaid_contrast_warnings(blocks):
    """Readability rules from references/diagramming-guide.md: explicit theme header and explicit text colour on styles."""
    out = []
    for i, b in enumerate(blocks, 1):
        code = [l for l in b.splitlines() if l.strip()]
        kind = next((l.split()[0].rstrip(";") for l in code if not l.strip().startswith("%")), "")
        if "%{init" not in b:
            out.append("diagram %d (%s) lacks the standard %%{init ...}%% theme header; it may be unreadable on dark backgrounds" % (i, kind))
        for l in code:
            if re.match(r"\s*(classDef|style)\s", l) and "fill:" in l and "color:" not in l:
                out.append("diagram %d: style sets fill without text color (add color:#111827): %s" % (i, l.strip()[:60]))
                break
        if kind == "stateDiagram" or kind == "stateDiagram-v2":
            out.append("diagram %d uses stateDiagram; use a flowchart with rounded state nodes (readability)" % i)
        if kind == "sequenceDiagram" and re.search(r"^\s*actor\s", b, re.M):
            out.append("diagram %d uses 'actor' in a sequenceDiagram; use 'participant' so names are readable" % i)
    return out
