# claude-kit — Personal Claude Code Plugin Marketplace

This directory is the `claude-kit` personal marketplace. Plugins live under `skills/` or `hooks/`, each in its own subdirectory. The marketplace manifest is at `.claude-plugin/marketplace.json`.

## Directory conventions

- Plugin names: lowercase, hyphen-separated (e.g., `conventional-commits`, `add-plugin`)
- Each plugin is fully self-contained — it can be installed standalone or via the marketplace
- The skill file lives in **two places** for dual-install support:
  - `skills/<name>/SKILL.md` — loaded when cloned directly as a standalone skill
  - `skills/<name>/skills/<name>/SKILL.md` — loaded when installed as a plugin
- Evals go in `skills/<name>/evals/evals.json` — minimum 3 cases

## Adding a new plugin

Use the `add-plugin` skill. It handles the full flow:
1. Scaffolds the directory structure under `skills/`
2. Writes `plugin.json`, `SKILL.md` (both locations), `evals.json`, and `README.md`
3. Adds the entry to `.claude-plugin/marketplace.json`
4. Validates and installs

## Key commands

```bash
# Validate a plugin manifest
claude plugin validate skills/<name>

# Validate the marketplace manifest
claude plugin validate ~/claude-kit

# Sync marketplace after manual edits to marketplace.json
claude plugin marketplace update claude-kit

# Install a plugin from this marketplace
claude plugin install <name>@claude-kit

# List installed plugins
claude plugin list

# Tag a release (bumps version tag on git)
claude plugin tag skills/<name>
```

## marketplace.json — adding a plugin entry

Each entry in the `plugins` array requires:

```json
{
  "name": "<plugin-name>",
  "description": "One sentence — what it does and when.",
  "version": "1.0.0",
  "category": "productivity | development | security | learning | deployment | database | monitoring",
  "source": "https://github.com/dantuck/claude-kit/tree/main/skills/<plugin-name>",
  "author": {
    "name": "dantuck"
  },
  "homepage": "https://github.com/dantuck/claude-kit"
}
```

The `category` field belongs here, not in `plugin.json`.

## plugin.json — required fields

```json
{
  "name": "<plugin-name>",
  "description": "Same one-sentence description as marketplace entry.",
  "version": "1.0.0",
  "author": { "name": "dantuck" },
  "homepage": "https://github.com/dantuck/claude-kit",
  "repository": "https://github.com/dantuck/claude-kit",
  "license": "MIT",
  "keywords": ["relevant", "tags"]
}
```

Do NOT include `category` in `plugin.json` — the validator will warn.

## SKILL.md frontmatter

```yaml
---
name: <plugin-name>
description: >-
  Concise semantic description of when to activate. Include trigger phrases.
  Claude uses this for automatic matching, so be specific about actions.
user-invocable: false   # true for explicit workflow skills (/slash-command)
---
```

## Evals format

```json
{
  "skill_name": "<plugin-name>",
  "evals": [
    {
      "id": 0,
      "prompt": "User prompt that should trigger the skill",
      "expected_output": "Human description of what a correct response looks like",
      "files": [],
      "assertions": [
        {
          "id": "assertion_id",
          "description": "What this checks",
          "type": "contains | not_contains | regex | not_regex | contains_any",
          "value": "string to match"
        }
      ]
    }
  ]
}
```
