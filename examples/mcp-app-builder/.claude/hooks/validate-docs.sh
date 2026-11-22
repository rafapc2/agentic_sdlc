#!/usr/bin/env bash
# PostToolUse hook: re-validates lifecycle documents after an agent edits anything under sdlc/.
# Why a hook: instructions in CLAUDE.md are advisory; this makes broken links and silent edits impossible to miss.
# Reads the hook payload (JSON) from stdin; exits 2 with a message on stderr to feed errors back to the agent.
set -u
payload="$(cat)"
file="$(printf '%s' "$payload" | python3 -c 'import sys,json
try:
    d=json.load(sys.stdin); print((d.get("tool_input") or {}).get("file_path",""))
except Exception:
    print("")')"
case "$file" in
  */sdlc/*.md) ;;
  *) exit 0 ;;
esac
root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
if ! out="$(python3 "$root/sdlc/_tools/validate_docs.py" "$root/sdlc" 2>&1)"; then
  printf '%s\n' "$out" >&2
  exit 2
fi
exit 0
