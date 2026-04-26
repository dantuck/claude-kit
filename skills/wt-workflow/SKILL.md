---
name: wt-workflow
description: ALWAYS use this skill for any task involving the `wt` git worktree CLI tool. Trigger on any mention of `wt` commands (`wt switch`, `wt update`, `wt remove`, `wt prune`, `wt review`, `wt -w`, `wt doctor`), `.worktreekeep`, or "worktree workflow". Also trigger when the user wants to start work on a feature or bugfix in a git repo and keep main clean, switch between active branches/tasks without losing state, clean up merged worktrees or gone branches, sync a feature branch with upstream, or carry unstaged changes to a new branch. Covers wt installation (fish shell and bash/zsh), the stable workflow pattern, and all wt subcommands. If there is any chance this involves the wt tool or worktree management, use this skill.
---

# wt Workflow

`wt` keeps each branch in its own isolated directory under `~/.wt/<project>/<branch>/`. This means you can switch tasks without stashing, losing state, or touching other branches. The main branch stays clean; all real work happens in worktrees.

## Step 0: Ensure wt is Installed

```bash
which wt
```

If missing, install for the user's shell:

```bash
# Fish shell
curl -fsSL https://codeberg.org/tuck/wt/raw/branch/main/wt.fish -o ~/.config/fish/conf.d/wt.fish

# Bash / zsh
curl -fsSL https://codeberg.org/tuck/wt/raw/branch/main/wt.sh -o ~/.local/bin/wt && chmod +x ~/.local/bin/wt
```

Then run `wt doctor` to verify dependencies (it also checks for optional `fzf`, which enables interactive selection menus).

## The Core Workflow

```
main (never worked in directly — always clean)
  └── ~/.wt/myproject/feature-auth/      ← one task, one directory
  └── ~/.wt/myproject/fix-login-bug/     ← another task, isolated
```

### Starting Work

```bash
# On an existing branch (local or remote — wt detects automatically)
wt <branch-name>

# On a new branch from a specific base
wt <new-branch> main

# Carry current unstaged changes into the new worktree
wt -w <branch-name>
```

The `-w` flag is important: it stashes changes, creates the worktree, and applies the stash there. If worktree creation fails, the stash is restored automatically — no lost work.

### Navigating Between Tasks

```bash
wt switch      # interactive fzf picker (falls back to numbered menu without fzf)
wt list        # show all worktrees for this project
```

The `switch` command won't switch to the current directory, and the main repo always appears as "📁 main".

### Staying Synced with Upstream

Run from any worktree whenever upstream moves:

```bash
wt update        # fetch + merge from origin's default branch
wt -r update     # fetch + rebase instead
```

If on the default branch, it pulls. If on a feature branch, it merges (or rebases). Merge conflicts halt with guidance.

### Finishing Work

After a PR is merged or work is done:

```bash
wt remove -d <branch>    # remove worktree AND delete the branch
wt remove                # interactive: pick from list
```

### Periodic Housekeeping

```bash
wt prune        # remove worktrees/branches where remote was deleted (shows "gone" in git branch -vv)
wt review       # audit ALL worktrees across ALL projects
wt review -n    # dry run — shows what would be removed without prompting
```

`wt review` categorizes each worktree:
- ✓ **Active** — branch still on remote
- ⊘ **Merged/Closed** — safe to delete
- ✗ **Orphaned** — directory not recognized by git (`wt doctor` can repair these)
- △ **Has Changes** — uncommitted work present
- ○ **Disconnected** — remote unreachable

## .worktreekeep: Sharing Config Across Worktrees

Create `.worktreekeep` in the repo root to automatically copy gitignored files into each new worktree:

```
# .worktreekeep
.env
.env.local
config/local/*.yml
```

This is essential for projects with local config that can't be committed. Set this up early — every new worktree will get the copies automatically.

## Quick Reference

| Situation | Command |
|-----------|---------|
| Start work on a branch | `wt <branch> [base]` |
| Carry current changes to new branch | `wt -w <branch>` |
| Switch between tasks | `wt switch` |
| See all worktrees | `wt list` |
| Sync with upstream | `wt update` / `wt -r update` |
| Done — clean up | `wt remove -d <branch>` |
| Clean up after remote deletes | `wt prune` |
| Audit all projects | `wt review` |
| Diagnose install issues | `wt doctor` |

## Common Situations

**"I want to start on a new feature"**
Ask what branch name they want (and what base if it's a new branch), then run `wt <branch>` or `wt <branch> main`.

**"I have half-done changes but there's a critical bug to fix"**
`wt -w fix/<bug>` — carries the current changes into the new worktree so neither task loses state.

**"How do I get back to my other feature?"**
`wt switch` for interactive picker. Or `cd ~/.wt/<project>/<branch>` directly.

**"My PR got merged, now what?"**
`wt remove -d <branch>` to delete the worktree and branch. Then `wt prune` to clean up any other gone branches.

**"My worktrees are a mess, I don't know what's what"**
`wt review` across all projects. Start with `-n` (dry run) to see the picture before any deletions.

**"I need to pull in the latest changes from main"**
`wt update` from the worktree. Use `-r` if you prefer a clean linear history.

**"Something seems broken with wt"**
`wt doctor` — diagnoses the installation and optional dependencies.
