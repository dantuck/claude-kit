# Conventional Commits Plugin for Claude Code

A [Claude Code](https://code.claude.com) plugin that automatically enforces [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) formatting for all git commit messages.

## What it does

This plugin activates automatically whenever you ask Claude Code to create a commit, write a commit message, or perform any git commit-related task. Every commit message follows the Conventional Commits specification:

- **Structured types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- **Optional scopes**: `feat(auth):`, `fix(parser):`, etc.
- **Breaking change notation**: `feat!:` or `BREAKING CHANGE:` footer
- **Imperative mood**: "add feature" not "added feature"
- **72-character line limit** on the first line
- **No attribution footers**: Prevents Claude from adding Co-Authored-By or AI attribution to commits

## Installation

### As a plugin (recommended)

```bash
claude plugin install conventional-commits@claude-kit --scope user
```

### As a standalone skill

Clone to your Claude skills directory. The skill works at two levels:

**Per-user (all projects):**
```bash
git clone https://github.com/dantuck/claude-kit.git /tmp/claude-kit
cp -r /tmp/claude-kit/skills/conventional-commits ~/.claude/skills/conventional-commits
```

**Per-project:**
```bash
git clone https://github.com/dantuck/claude-kit.git /tmp/claude-kit
cp -r /tmp/claude-kit/skills/conventional-commits .claude/skills/conventional-commits
```

The root `SKILL.md` supports standalone skill installation. When installed as a plugin, Claude Code loads the skill from `skills/conventional-commits/SKILL.md`.

### Update

```bash
# Plugin
claude plugin update conventional-commits

# Standalone skill
cd ~/.claude/skills/conventional-commits && git pull
```

## How it works

The skill uses Claude Code's **semantic matching** to detect commit-related tasks. When matched, Claude follows the Conventional Commits rules.

**Automatic triggers** (examples):
- "commit these changes"
- "create a commit"
- "write a commit message for this"
- "stage and commit"

**What Claude does:**
1. Analyzes the staged/changed files
2. Determines the correct commit type using the decision guide
3. Writes a properly formatted message
4. Omits any Co-Authored-By or attribution footer

## Plugin structure

```
conventional-commits/
├── .claude-plugin/
│   └── plugin.json                          # Plugin manifest
├── skills/
│   └── conventional-commits/
│       ├── SKILL.md                         # Skill instructions (plugin install)
│       └── references/
│           └── specification.md             # Full Conventional Commits v1.0.0 spec
├── evals/
│   └── evals.json                           # Automated skill evals
├── SKILL.md                                 # Skill instructions (standalone install)
├── references/
│   └── specification.md                     # Spec reference (standalone install)
├── README.md
└── LICENSE
```

## Quick reference

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

| Type       | Use for                                           |
|------------|---------------------------------------------------|
| `feat`     | New feature (SemVer MINOR)                        |
| `fix`      | Bug fix (SemVer PATCH)                            |
| `docs`     | Documentation changes                             |
| `style`    | Formatting, whitespace (no code change)           |
| `refactor` | Code restructuring (no feature/fix)               |
| `perf`     | Performance improvement                           |
| `test`     | Adding or fixing tests                            |
| `build`    | Build system or dependencies                      |
| `ci`       | CI configuration                                  |
| `chore`    | Other non-src/test changes                        |
| `revert`   | Reverting a previous commit                       |

## License

MIT
