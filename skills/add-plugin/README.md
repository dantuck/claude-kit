# add-plugin

A Claude Code plugin that scaffolds and registers new plugins in the `claude-kit` personal marketplace.

## What it does

When you ask Claude to create or add a new plugin, this skill walks through the complete workflow:

1. Gathers plugin name, description, trigger phrases, and category
2. Creates the full directory structure under `skills/`
3. Writes `plugin.json`, `SKILL.md` (at both install paths), `evals.json`, and `README.md`
4. Adds the entry to `.claude-plugin/marketplace.json`
5. Validates both the plugin and marketplace manifests
6. Updates the marketplace index and installs the plugin

## Installation

```bash
claude plugin install add-plugin@claude-kit
```

## Usage

The skill is user-invocable via `/add-plugin`, or triggers automatically on phrases like:

- "add a plugin"
- "create a new plugin"
- "scaffold a plugin"
- "add to the marketplace"

## Example

```
You: Add a plugin that enforces conventional commits
Claude: [uses add-plugin skill to scaffold conventional-commits plugin]
```
