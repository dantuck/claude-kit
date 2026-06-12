#!/usr/bin/env python3
"""Dev tests for stop.py — run directly: python3 tests/test_stop.py"""
import json
import os
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "hooks", "stop.py")
CONTEXT_WINDOW = 200_000


def run_hook(char_count=0, create_file=True, session_id="test-sess", env=None):
    """Run stop.py with a temp JSONL containing char_count chars of content."""
    with tempfile.TemporaryDirectory() as tmp:
        config_dir = os.path.join(tmp, ".claude")
        slug = tmp.replace("/", "-")
        project_dir = os.path.join(config_dir, "projects", slug)
        os.makedirs(project_dir, exist_ok=True)

        if create_file:
            entry = json.dumps({
                "type": "user",
                "message": {"role": "user", "content": "x" * char_count}
            })
            with open(os.path.join(project_dir, f"{session_id}.jsonl"), "w") as f:
                f.write(entry + "\n")

        hook_env = os.environ.copy()
        hook_env["CLAUDE_CONFIG_DIR"] = config_dir
        if env:
            hook_env.update(env)

        stdin = json.dumps({
            "hook_event_name": "Stop",
            "session_id": session_id,
            "cwd": tmp,
        })
        return subprocess.run(
            [sys.executable, SCRIPT],
            input=stdin,
            capture_output=True,
            text=True,
            env=hook_env,
        )


def test_under_threshold():
    """70% context → silent exit, no output."""
    r = run_hook(char_count=int(CONTEXT_WINDOW * 0.70 * 4))
    assert r.returncode == 0, f"exit {r.returncode}, stdout={r.stdout!r}"
    assert r.stdout.strip() == "", f"expected no stdout: {r.stdout!r}"


def test_warn_threshold():
    """85% context → exit 2, warning (not urgent) in reason."""
    r = run_hook(char_count=int(CONTEXT_WINDOW * 0.85 * 4))
    assert r.returncode == 2, f"exit {r.returncode}, stdout={r.stdout!r}"
    out = json.loads(r.stdout)
    assert "context-guard" in out["reason"], f"no context-guard tag: {out['reason'][:80]}"
    assert "URGENT" not in out["reason"], "expected warning, not urgent message"


def test_urgent_threshold():
    """97% context → exit 2, URGENT in reason."""
    r = run_hook(char_count=int(CONTEXT_WINDOW * 0.97 * 4))
    assert r.returncode == 2, f"exit {r.returncode}, stdout={r.stdout!r}"
    out = json.loads(r.stdout)
    assert "URGENT" in out["reason"], f"expected URGENT: {out['reason'][:80]}"


def test_missing_jsonl():
    """No JSONL file → silent exit, no output."""
    r = run_hook(create_file=False)
    assert r.returncode == 0, f"exit {r.returncode}"
    assert r.stdout.strip() == "", f"expected no stdout: {r.stdout!r}"


def test_disabled():
    """CONTEXT_GUARD_DISABLE=1 → silent exit even at 99%."""
    r = run_hook(
        char_count=int(CONTEXT_WINDOW * 0.99 * 4),
        env={"CONTEXT_GUARD_DISABLE": "1"},
    )
    assert r.returncode == 0, f"exit {r.returncode}"


def test_custom_thresholds():
    """CONTEXT_GUARD_WARN_PCT=50 → warn at 55%."""
    r = run_hook(
        char_count=int(CONTEXT_WINDOW * 0.55 * 4),
        env={"CONTEXT_GUARD_WARN_PCT": "50", "CONTEXT_GUARD_URGENT_PCT": "90"},
    )
    assert r.returncode == 2, f"exit {r.returncode}"
    out = json.loads(r.stdout)
    assert "URGENT" not in out["reason"]


def test_list_content_blocks():
    """Assistant message with list content blocks (tool_use / text) are counted."""
    with tempfile.TemporaryDirectory() as tmp:
        config_dir = os.path.join(tmp, ".claude")
        slug = tmp.replace("/", "-")
        project_dir = os.path.join(config_dir, "projects", slug)
        os.makedirs(project_dir, exist_ok=True)

        # Content as list of blocks (assistant tool_use response format)
        chars_per_block = int(CONTEXT_WINDOW * 0.30 * 4)
        entry = json.dumps({
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "a" * chars_per_block},
                    {"type": "text", "text": "b" * chars_per_block},
                    {"type": "thinking", "thinking": "c" * chars_per_block},
                ],
            },
        })
        with open(os.path.join(project_dir, "sess.jsonl"), "w") as f:
            f.write(entry + "\n")

        hook_env = os.environ.copy()
        hook_env["CLAUDE_CONFIG_DIR"] = config_dir
        stdin = json.dumps({"hook_event_name": "Stop", "session_id": "sess", "cwd": tmp})
        r = subprocess.run(
            [sys.executable, SCRIPT],
            input=stdin, capture_output=True, text=True, env=hook_env,
        )
        # 3 blocks × 30% = 90% → warn threshold
        assert r.returncode == 2, f"exit {r.returncode}, stdout={r.stdout!r}"


if __name__ == "__main__":
    tests = [
        test_under_threshold,
        test_warn_threshold,
        test_urgent_threshold,
        test_missing_jsonl,
        test_disabled,
        test_custom_thresholds,
        test_list_content_blocks,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except (AssertionError, Exception) as e:
            print(f"FAIL  {t.__name__} — {e}")
            failed += 1
    print(f"\n{'All tests passed!' if not failed else f'{failed} test(s) failed.'}")
    sys.exit(failed)
