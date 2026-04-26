# claude-kit

A personal Claude Code plugin marketplace. Marketplace ID: `claude-kit`.

## Plugins

| Plugin | Type | Category | Description |
|--------|------|----------|-------------|
| [conventional-commits](skills/conventional-commits) | skill | productivity | Enforces Conventional Commits v1.0.0 for all git commit messages |
| [wt-workflow](skills/wt-workflow) | skill | productivity | Skill for the `wt` git worktree CLI — all subcommands and the core workflow |
| [add-plugin](skills/add-plugin) | skill | productivity | Scaffolds and registers new plugins in this marketplace |
| [secret-guard](hooks/secret-guard) | hook | security | Blocks reading secret files, env var dumps, and warns on writing credentials |

---

## Setup

### 1. Register the marketplace

```bash
claude plugin marketplace add https://github.com/dantuck/claude-kit
```

Verify it was registered:

```bash
claude plugin marketplace list
# claude-kit → https://github.com/dantuck/claude-kit
```

### 2. Install plugins

Install any plugin from the marketplace with:

```bash
claude plugin install <plugin-name>@claude-kit --scope user
```

The `--scope user` flag installs the plugin for all your projects. Omit it to install for the current project only.

**Install all plugins at once:**

```bash
claude plugin install conventional-commits@claude-kit --scope user
claude plugin install wt-workflow@claude-kit --scope user
claude plugin install add-plugin@claude-kit --scope user
claude plugin install secret-guard@claude-kit --scope user
```

### 3. Verify installation

```bash
claude plugin list
```

---

## Plugin details

### conventional-commits

Enforces [Conventional Commits v1.0.0](https://www.conventionalcommits.org/) for every git commit. Activates automatically whenever Claude creates or suggests a commit message.

- Structured commit types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- Optional scope in parentheses: `feat(auth): add OAuth2`
- Breaking change notation: `!` suffix or `BREAKING CHANGE:` footer
- Never adds `Co-Authored-By` or AI attribution footers
- User-invocable as `/conventional-commits:commit`

```bash
claude plugin install conventional-commits@claude-kit --scope user
```

### wt-workflow

Teaches Claude the [`wt`](https://codeberg.org/tuck/wt) git worktree CLI. Activates on any mention of `wt` commands, `.worktreekeep`, or worktree management tasks.

- Covers installation (fish shell and bash/zsh)
- All subcommands: `wt switch`, `wt update`, `wt remove`, `wt prune`, `wt review`, `wt -w`, `wt doctor`
- The stable workflow pattern for keeping `main` clean
- `.worktreekeep` config for persisting worktrees across `wt prune`

```bash
claude plugin install wt-workflow@claude-kit --scope user
```

### add-plugin

Guides Claude through creating a new plugin in this marketplace. Activates on requests like "add a plugin", "create a plugin", or "scaffold a plugin".

- Scaffolds the full directory structure for skill or hook-only plugins
- Writes `SKILL.md`, `plugin.json`, `evals/evals.json`, and `README.md`
- Updates `marketplace.json` and validates the manifest
- Installs the plugin immediately after creation
- User-invocable as `/add-plugin:add-plugin`

```bash
claude plugin install add-plugin@claude-kit --scope user
```

### secret-guard

A hook plugin that intercepts tool calls before they execute and prevents secrets from leaking into the conversation.

| Trigger | Action |
|---------|--------|
| `Bash` reading `.env`, `*.pem`, `*.key`, credentials files | Block |
| `Bash` running `env`, `printenv`, or echoing credential vars | Block |
| `Read` on any secrets-pattern path | Block |
| `Write` / `Edit` to a secrets-pattern path | Warn |

Detected patterns: `.env*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `*.ppk`, `*.cer`, `*.crt`, `credentials`, `secrets.yml/json/toml`, `id_rsa`, `id_ed25519`, `.netrc`, `.pgpass`.

```bash
claude plugin install secret-guard@claude-kit --scope user
```

---

## Repository structure

```
claude-kit/
├── .claude-plugin/
│   └── marketplace.json        ← marketplace manifest
├── skills/
│   └── <plugin-name>/          ← skill plugins
│       ├── .claude-plugin/
│       │   └── plugin.json     ← plugin manifest
│       ├── skills/
│       │   └── <plugin-name>/
│       │       └── SKILL.md    ← skill loaded when installed as plugin
│       ├── evals/
│       │   └── evals.json
│       ├── SKILL.md            ← skill loaded when used standalone
│       └── README.md
└── hooks/
    └── <plugin-name>/          ← hook-only plugins (no SKILL.md)
        ├── .claude-plugin/
        │   └── plugin.json
        ├── hooks/
        │   ├── hooks.json
        │   └── pretooluse.py
        ├── evals/
        │   └── evals.json
        └── README.md
```

---

## Adding a new plugin

Use the `add-plugin` skill — it handles scaffolding, writing all files, updating `marketplace.json`, validating, and installing. Do not scaffold manually unless the skill is unavailable.

After adding a plugin, update the table at the top of this README.

---

## Maintenance commands

```bash
# Validate a plugin manifest
claude plugin validate skills/<name>
claude plugin validate hooks/<name>

# Validate the marketplace manifest
claude plugin validate ~/claude-kit

# Sync the marketplace index after editing marketplace.json
claude plugin marketplace update claude-kit

# Tag a release
claude plugin tag skills/<name>
claude plugin tag hooks/<name>
```

---

## Contributing

Plugins in this repo are personal tools, but suggestions and improvements are welcome.

- Open an issue to propose a new plugin or report a bug
- Fork and submit a pull request for fixes or enhancements
- All commit messages must follow [Conventional Commits v1.0.0](https://www.conventionalcommits.org/)
- New plugins require at least 3 evals (happy path, edge case, negative case)

---

## License

MIT © Plan To Live LLC
