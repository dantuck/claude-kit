#!/usr/bin/env python3
"""Stop hook for context-guard plugin.

Reads the session JSONL from $CLAUDE_CONFIG_DIR/projects/<slug>/<session_id>.jsonl,
estimates total context size, and signals Claude to compact when thresholds are hit.

Exit codes:
  0 — under threshold, silent
  2 — at or above warn/urgent threshold; JSON reason written to stdout

Environment variables:
  CONTEXT_GUARD_DISABLE=1       Disable all checks (silent exit 0)
  CONTEXT_GUARD_WARN_PCT=80     Warn threshold percentage (default 80)
  CONTEXT_GUARD_URGENT_PCT=95   Urgent threshold percentage (default 95)
  CONTEXT_GUARD_WINDOW=200000   Context window token size (default 200000)
"""

import json
import os
import sys

# Approximate chars-per-token ratio used for estimation
CHARS_PER_TOKEN = 4


def _content_chars(content) -> int:
    """Return the number of characters in a message content field."""
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        total = 0
        for block in content:
            if not isinstance(block, dict):
                continue
            for key in ("text", "thinking", "input"):
                val = block.get(key)
                if isinstance(val, str):
                    total += len(val)
                elif isinstance(val, dict):
                    total += len(json.dumps(val))
        return total
    return 0


def count_chars(jsonl_path: str) -> int:
    """Sum chars across all message content entries in a JSONL session file."""
    total = 0
    try:
        with open(jsonl_path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = entry.get("message", {})
                content = msg.get("content", "")
                total += _content_chars(content)
    except OSError:
        return 0
    return total


def find_jsonl(config_dir: str, cwd: str, session_id: str) -> str | None:
    """Locate the session JSONL file using the same slug logic as Claude Code."""
    slug = cwd.replace("/", "-")
    candidate = os.path.join(config_dir, "projects", slug, f"{session_id}.jsonl")
    if os.path.isfile(candidate):
        return candidate
    return None


def main() -> int:
    # Parse hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # Can't parse input — fail open

    if os.environ.get("CONTEXT_GUARD_DISABLE", "").strip() in ("1", "true", "yes"):
        return 0

    session_id = hook_input.get("session_id", "")
    cwd = hook_input.get("cwd", os.getcwd())
    config_dir = os.environ.get(
        "CLAUDE_CONFIG_DIR", os.path.expanduser("~/.claude")
    )

    try:
        warn_pct = int(os.environ.get("CONTEXT_GUARD_WARN_PCT", "80"))
        urgent_pct = int(os.environ.get("CONTEXT_GUARD_URGENT_PCT", "95"))
        window_tokens = int(os.environ.get("CONTEXT_GUARD_WINDOW", "200000"))
    except ValueError:
        return 0  # bad env var — fail open

    if not session_id:
        return 0

    jsonl_path = find_jsonl(config_dir, cwd, session_id)
    if jsonl_path is None:
        return 0

    total_chars = count_chars(jsonl_path)
    estimated_tokens = total_chars / CHARS_PER_TOKEN
    pct_used = (estimated_tokens / window_tokens) * 100

    if pct_used >= urgent_pct:
        reason = (
            f"[context-guard] URGENT: context window is ~{pct_used:.0f}% full "
            f"({estimated_tokens:,.0f} / {window_tokens:,} estimated tokens). "
            "Compact the conversation now to avoid silent context loss."
        )
        print(json.dumps({"decision": "block", "reason": reason}))
        return 2

    if pct_used >= warn_pct:
        reason = (
            f"[context-guard] WARNING: context window is ~{pct_used:.0f}% full "
            f"({estimated_tokens:,.0f} / {window_tokens:,} estimated tokens). "
            "Consider compacting the conversation soon."
        )
        print(json.dumps({"decision": "block", "reason": reason}))
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
