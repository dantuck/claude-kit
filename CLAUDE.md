# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal Claude Code plugin marketplace registered as `claude-kit`. Plugins are organised by type:

- `skills/` — skill plugins (expose a SKILL.md loaded by the agent)
- `hooks/` — hook-only plugins (no SKILL.md; pure `PreToolUse`/`PostToolUse`/etc. behaviour)

Skills follow the [agentskills.io](https://agentskills.io) open standard. All SKILL.md files must conform to that specification.

## Key commands

```bash
# Validate a plugin manifest (use skills/ or hooks/ prefix as appropriate)
claude plugin validate skills/<name>
claude plugin validate hooks/<name>

# Validate the marketplace manifest
claude plugin validate ~/claude-kit

# Sync the marketplace index after editing marketplace.json
# (push changes first — marketplace is registered from GitHub)
claude plugin marketplace update claude-kit

# Install a plugin from this marketplace
claude plugin install <name>@claude-kit --scope user

# List installed plugins
claude plugin list

# Tag a release
claude plugin tag skills/<name>
claude plugin tag hooks/<name>
```

## Plugin structure

### Skill plugin (`skills/<name>/`)

```
skills/<name>/
├── .claude-plugin/plugin.json
├── agents/                        ← optional, one .md per agent
│   └── <agent-name>.md
├── hooks/                         ← optional
│   └── hooks.json
├── scripts/                       ← optional, per agentskills.io spec
├── references/                    ← optional, per agentskills.io spec
├── assets/                        ← optional, per agentskills.io spec
├── skills/<name>/SKILL.md         ← loaded when installed as plugin
├── SKILL.md                       ← identical content, loaded standalone
├── evals/evals.json
└── README.md
```

SKILL.md must exist at **both paths** — standalone and plugin install paths are different locations. The content is identical.

### Hook-only plugin (`hooks/<name>/`)

No SKILL.md. Used for plugins that only modify tool behaviour via hooks.

```
hooks/<name>/
├── .claude-plugin/plugin.json
├── hooks/
│   ├── hooks.json
│   └── pretooluse.py              ← or other hook scripts
├── evals/evals.json
└── README.md
```

## Agents

Agent files live at `agents/<agent-name>.md` inside the plugin directory. Frontmatter fields:

```yaml
---
name: <agent-name>
description: What this agent does and when it should be used
tools: Glob, Grep, LS, Read, Bash, Write, Edit   # comma-separated subset
model: sonnet | opus | haiku | inherit
color: green | blue | red | yellow | purple       # optional, for UI
---
```

The body is the agent's system prompt. Write it as direct instructions to the agent — what it is, what it does, and how it should behave.

## Hooks

Hooks live at `hooks/hooks.json` inside the plugin directory. Supported events: `PreToolUse`, `PostToolUse`, `Stop`, `UserPromptSubmit`, `SessionStart`.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "optional-tool-name-pattern",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/pretooluse.py",
            "timeout": 10,
            "async": false
          }
        ]
      }
    ]
  }
}
```

`CLAUDE_PLUGIN_ROOT` is set to the installed plugin directory at runtime. `matcher` is optional — omit to match all events for that hook type. `async: true` lets the hook run without blocking Claude.

## Manifest field rules

**`plugin.json`** — do NOT include `category` (validator warns if present).

**`marketplace.json`** — `category` goes here, not in `plugin.json`. Required fields per entry: `name`, `description`, `version`, `category`, `source`, `author`, `homepage`.

**SKILL.md frontmatter** (see [agentskills.io/specification](https://agentskills.io/specification) for the authoritative spec):

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Lowercase letters, numbers, hyphens only. Max 64 chars. No leading/trailing/consecutive hyphens. Must match the parent directory name. |
| `description` | Yes | Max 1024 chars. Use imperative phrasing: "Use when…". Describe what the skill does AND when to use it. Include keywords matching user intent, not implementation. |
| `license` | No | License name or path to bundled license file. |
| `compatibility` | No | Max 500 chars. Only include if the skill has specific environment requirements (tools, OS, network, etc.). |
| `metadata` | No | Arbitrary key-value map for additional properties. |
| `allowed-tools` | No | Space-separated string of pre-approved tools (experimental). |
| `user-invocable` | No | Claude Code extension — `true` if the skill can be triggered by the user with a slash command. |

```yaml
---
name: my-skill                          # must match directory name
description: >-
  Use when … — imperative, max 1024 chars, keyword-rich.
license: MIT
compatibility: Requires Claude Code
metadata:
  author: claude-kit
  version: "1.0"
user-invocable: false                   # Claude Code extension
---
```

**SKILL.md body:** Keep under 500 lines / 5 000 tokens. Move detailed reference material to `references/` files and load them on demand with explicit instructions ("Read `references/foo.md` if X").

## Adding a new plugin

Use the `add-plugin` skill — it handles scaffolding, writing all files, updating `marketplace.json`, validating, and installing. Do not scaffold manually unless the skill is unavailable.

After adding a plugin, update the table in `README.md` at the repo root.

## Evals

Each plugin requires at least 3 eval cases in `evals/evals.json`: a happy path, an edge case, and a negative case (`not_contains` / `not_regex`). Assertion types: `contains`, `not_contains`, `regex`, `not_regex`, `contains_any`.

## Commit messages

The `conventional-commits` plugin is active. All commits must follow Conventional Commits v1.0.0: `<type>[optional scope]: <description>`. Never add `Co-Authored-By` or AI attribution footers.
