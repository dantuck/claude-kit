#!/usr/bin/env python3
"""SessionStart hook for context-guard plugin.

Injects the compact rule from SKILL.md as additionalContext so it becomes
a standing instruction in every session without requiring manual invocation.
"""

import json
import os
import sys


def _skill_body(plugin_root):
    """Read SKILL.md and return only the body (strip YAML frontmatter)."""
    skill_path = os.path.join(plugin_root, "SKILL.md")
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()


def main():
    plugin_root = os.environ.get(
        "CLAUDE_PLUGIN_ROOT",
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )

    try:
        body = _skill_body(plugin_root)
    except Exception:
        print(json.dumps({}), flush=True)
        sys.exit(0)

    print(
        json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": body,
            }
        }),
        flush=True,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
