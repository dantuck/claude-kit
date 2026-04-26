# wt-workflow

A Claude Code skill for the [`wt`](https://codeberg.org/tuck/wt) git worktree CLI.

`wt` keeps each branch in its own isolated directory under `~/.wt/<project>/<branch>/` so you can switch tasks without stashing, losing state, or touching other branches.

## What this skill covers

- Installing `wt` for fish shell or bash/zsh
- Starting work on a new or existing branch (`wt <branch>`)
- Carrying unstaged changes to a new branch (`wt -w <branch>`)
- Switching between tasks (`wt switch`)
- Syncing with upstream (`wt update`, `wt -r update`)
- Cleaning up merged work (`wt remove -d <branch>`)
- Housekeeping across all projects (`wt prune`, `wt review`)
- Sharing gitignored config via `.worktreekeep`

## Install

```bash
claude plugin install wt-workflow@claude-kit --scope user
```
