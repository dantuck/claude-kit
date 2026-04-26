---
name: add-plugin
description: >-
  Use when creating a new Claude Code plugin for the claude-kit personal
  marketplace at ~/claude-kit. Guides through scaffolding the full plugin
  structure, writing SKILL.md and plugin.json, creating evals, updating the marketplace
  manifest, and installing. Trigger on: "add a plugin", "create a plugin", "new plugin",
  "scaffold a plugin", "add to marketplace".
user-invocable: true
---

# Add Plugin to Personal Marketplace

This skill creates a new plugin in the personal marketplace at `~/claude-kit`.

## Step 1: Gather Requirements

Before writing any files, collect (or infer from context):

- **Plugin name**: lowercase, hyphen-separated (e.g., `my-plugin`)
- **One-line description**: what it does and when Claude should use it — used in both `plugin.json` and `marketplace.json`
- **Trigger phrases**: what user requests should activate this skill automatically
- **`user-invocable`**: `true` if it should appear as a `/plugin-name` slash command; `false` for skills that activate automatically
- **Category**: one of `productivity`, `development`, `security`, `learning`, `deployment`, `database`, `monitoring`

If anything is unclear, ask before proceeding.

## Step 2: Create Directory Structure

All paths are relative to `~/claude-kit/`.

```
skills/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── <plugin-name>/
│       ├── SKILL.md          ← loaded when installed as plugin
│       └── references/       ← create only if needed for supporting docs
├── evals/
│   └── evals.json
├── SKILL.md                  ← loaded when cloned as standalone skill (same content)
└── README.md
```

Create all directories first:

```bash
mkdir -p skills/<plugin-name>/.claude-plugin \
         skills/<plugin-name>/skills/<plugin-name> \
         skills/<plugin-name>/evals
```

## Step 3: Write `plugin.json`

File: `skills/<plugin-name>/.claude-plugin/plugin.json`

```json
{
  "name": "<plugin-name>",
  "description": "<one-line description>",
  "version": "1.0.0",
  "author": {
    "name": "dantuck"
  },
  "homepage": "https://github.com/dantuck/claude-kit",
  "repository": "https://github.com/dantuck/claude-kit",
  "license": "MIT",
  "keywords": ["<relevant>", "<tags>"]
}
```

Do NOT include `category` — it belongs in `marketplace.json`, and the validator will warn if it's here.

## Step 4: Write the SKILL.md

The skill is the core of the plugin. Write it at BOTH locations:
- `skills/<plugin-name>/skills/<plugin-name>/SKILL.md` (plugin install path)
- `skills/<plugin-name>/SKILL.md` (standalone install path — identical content)

### Frontmatter

```yaml
---
name: <plugin-name>
description: >-
  Semantic description of when to activate. Include specific trigger phrases.
  Claude uses this for automatic matching — be concrete about the actions that
  should trigger this skill.
user-invocable: <true|false>
---
```

### Skill body

Write the skill to be clear and directive. Structure:
1. **What this skill does** — one-paragraph summary
2. **Rules or steps** — the actual instructions Claude must follow
3. **Examples** — concrete input/output pairs where helpful
4. **Decision guide** — if the skill involves choices (e.g., type selection)

Rules for good skill content:
- Use MUST/MUST NOT for hard requirements
- Use present imperative tense for instructions
- Keep rules specific and verifiable — avoid vague guidance
- Include forbidden patterns explicitly (what Claude should never do)

## Step 5: Write `evals.json`

File: `skills/<plugin-name>/evals/evals.json`

Write at least 3 eval cases:
1. **Happy path** — the most common trigger, expected to produce correct output
2. **Edge case** — a trickier variant that tests a specific rule
3. **Negative case** — something the skill should NOT do (use `not_contains` or `not_regex`)

```json
{
  "skill_name": "<plugin-name>",
  "evals": [
    {
      "id": 0,
      "prompt": "User prompt that should trigger the skill",
      "expected_output": "Human-readable description of correct output",
      "files": [],
      "assertions": [
        {
          "id": "assertion_id",
          "description": "What this assertion checks",
          "type": "contains",
          "value": "expected string in response"
        }
      ]
    }
  ]
}
```

Assertion types: `contains`, `not_contains`, `regex`, `not_regex`, `contains_any`

## Step 6: Write `README.md`

File: `skills/<plugin-name>/README.md`

Cover:
1. What the plugin does (2–3 sentences)
2. Installation (plugin and standalone)
3. How it activates (trigger phrases or slash command)
4. Quick reference (if relevant)

## Step 7: Update the Marketplace Manifest

File: `~/claude-kit/.claude-plugin/marketplace.json`

Add an entry to the `plugins` array:

```json
{
  "name": "<plugin-name>",
  "description": "<same one-line description as plugin.json>",
  "version": "1.0.0",
  "category": "<category>",
  "source": "https://github.com/dantuck/claude-kit/tree/main/skills/<plugin-name>",
  "author": {
    "name": "dantuck"
  },
  "homepage": "https://github.com/dantuck/claude-kit"
}
```

## Step 8: Validate

```bash
claude plugin validate ~/claude-kit/skills/<plugin-name>
```

Fix any errors before proceeding. Warnings about missing fields are worth addressing. The one expected clean state is "Validation passed" with zero warnings.

Also validate the marketplace:

```bash
claude plugin validate ~/claude-kit
```

## Step 9: Update and Install

```bash
# Sync the marketplace index with the updated manifest
claude plugin marketplace update claude-kit

# Install the new plugin
claude plugin install <plugin-name>@claude-kit --scope user
```

Confirm installation with:

```bash
claude plugin list | grep <plugin-name>
```

## Step 10: Update README.md

Add the new plugin to the table in `~/claude-kit/README.md`:

```markdown
| [<plugin-name>](skills/<plugin-name>) | <description> |
```

## Checklist

Before declaring the plugin complete:

- [ ] `plugin.json` validates without warnings
- [ ] `marketplace.json` validates without warnings  
- [ ] SKILL.md exists at both `skills/<name>/SKILL.md` and `skills/<name>/skills/<name>/SKILL.md`
- [ ] Evals have at least 3 cases with meaningful assertions
- [ ] Plugin appears in `claude plugin list` as enabled
- [ ] `README.md` table updated at the marketplace root
