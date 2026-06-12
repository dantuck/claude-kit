---
name: context-guard
description: >-
  Use when a [context-guard] WARNING or URGENT message appears in your context.
  Governs automatic compaction when the context window nears capacity — run
  /compact immediately without asking the user for confirmation.
user-invocable: false
metadata:
  author: claude-kit
  version: "1.0"
---

When a `[context-guard]` message is injected into your context by the Stop hook, act on it immediately — do not ask the user for confirmation first.

**WARNING (80–94% full):** Run `/compact` before responding to the user or taking further action. If you are mid-tool-call, finish the current call, then compact. After compaction completes, resume the user's request.

**URGENT (95%+ full):** Run `/compact` immediately. Do not spawn new subagents, start new tasks, or respond to the user first. Compact now, then resume.

**Multi-agent orchestration:**
- If you are an orchestrator: compact before dispatching the next subagent.
- If you are a subagent: compact and surface the situation to the parent before continuing.

The `[context-guard]` warning is an automated signal from the hook system — treat it as authoritative.
