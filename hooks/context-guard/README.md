# context-guard

A Claude Code hook plugin that monitors context window usage and forces compaction at configurable thresholds, preventing silent context loss in long sessions and multi-agent orchestrations.

## How it works

`context-guard` installs a `Stop` hook that runs every time Claude finishes a response. It reads the session's JSONL transcript, estimates how many tokens have been used, and compares that against the configured context window size.

| Usage | Action |
|-------|--------|
| Below warn threshold | Silent — no output |
| At or above warn threshold (default 80%) | Exit 2 with a compaction warning |
| At or above urgent threshold (default 95%) | Exit 2 with an URGENT compaction message |

When the hook exits 2, Claude Code surfaces the `reason` message to the user, prompting them to compact before context is silently dropped.

## Install

```bash
claude plugin install context-guard@claude-kit --scope user
```

## Configuration

All configuration is via environment variables. Set them in your shell profile or in `.claude/settings.json` under `env`.

| Variable | Default | Description |
|----------|---------|-------------|
| `CONTEXT_GUARD_DISABLE` | unset | Set to `1` to disable all checks |
| `CONTEXT_GUARD_WARN_PCT` | `80` | Percentage at which to issue a warning |
| `CONTEXT_GUARD_URGENT_PCT` | `95` | Percentage at which to issue an urgent alert |
| `CONTEXT_GUARD_WINDOW` | `200000` | Context window size in tokens |

### Example: lower thresholds for sensitive work

```json
{
  "env": {
    "CONTEXT_GUARD_WARN_PCT": "70",
    "CONTEXT_GUARD_URGENT_PCT": "85"
  }
}
```

### Example: larger context window (claude-opus-4 / future models)

```json
{
  "env": {
    "CONTEXT_GUARD_WINDOW": "1000000"
  }
}
```

## Token estimation

The hook estimates tokens from the JSONL transcript using a **4 chars ≈ 1 token** approximation. This is a conservative heuristic — actual token usage may differ depending on language and content type. The estimate intentionally errs on the side of early warning.

## Why this exists

Claude Code does not visibly warn when you are approaching context limits. When the window fills up, earlier messages are silently dropped, which can cause:

- Lost tool results in multi-step tasks
- Forgotten requirements in long coding sessions
- Broken continuity in multi-agent orchestrations

`context-guard` surfaces the problem before it happens so you can `/compact` at a sensible moment.

## Testing

```bash
python3 tests/test_stop.py
```

7 tests covering: under-threshold silence, warn/urgent thresholds, missing JSONL, disabled mode, custom thresholds, and list-format content blocks.
