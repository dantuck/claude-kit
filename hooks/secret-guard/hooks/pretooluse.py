#!/usr/bin/env python3
"""PreToolUse hook for secret-guard plugin.

Blocks Bash commands and Read calls that would expose secrets,
and warns when writing to known credential file paths.
"""

import json
import re
import sys

# Matches secret-named file paths
SECRET_PATH = re.compile(
    r"""
    (^|[/\\])
    (
        \.env(\.|$)             # .env, .env.local, .env.production, etc.
        | id_(rsa|ed25519|ecdsa|dsa)$
        | credentials$
        | secrets?\.(ya?ml|json|toml|txt)$
        | \.netrc$
        | \.pgpass$
    )
    | \.(pem|key|p12|pfx|jks|keystore|ppk|cer|crt|pkcs12)$
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Matches bash commands that read secret files
READ_SECRET = re.compile(
    r"""
    \b(cat|head|tail|less|more|bat|strings|xxd|od|hexdump)\b
    \s+.*?
    (
        \.env(\b|\.|$)
        | \.(pem|key|p12|pfx|jks|ppk|cer|crt)\b
        | [/\\]id_(rsa|ed25519|ecdsa|dsa)\b
        | [/\\]credentials\b
        | secrets?\.(ya?ml|json|toml)\b
        | \.netrc\b
        | \.pgpass\b
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Matches bash commands that dump env vars
ENV_DUMP = re.compile(
    r"""
    ^\s*(env|printenv)(\s|$)
    |
    \b(echo|printf)\s+['"]?\$\{?
    (AWS_|AZURE_|GCP_|API_KEY|API_SECRET|SECRET_KEY?|SECRET_TOKEN
    |TOKEN|PASSWORD|PASSWD|PRIVATE_KEY|AUTH_TOKEN|ACCESS_KEY
    |CLIENT_SECRET|OAUTH|BEARER)
    """,
    re.VERBOSE | re.IGNORECASE,
)

DENY = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
    }
}


def check_bash(command):
    if READ_SECRET.search(command):
        return {
            **DENY,
            "systemMessage": (
                "**[secret-guard]** Blocked: this command would read a secret file into "
                "the conversation context.\n\n"
                "**Safe alternatives:**\n"
                "- Verify file exists: `test -f <path> && echo exists`\n"
                "- Inspect metadata: `ls -la <path>`\n"
                "- Count lines: `wc -l <path>`"
            ),
        }
    if ENV_DUMP.search(command):
        return {
            **DENY,
            "systemMessage": (
                "**[secret-guard]** Blocked: this command would dump environment variables "
                "and may expose API keys, tokens, or passwords.\n\n"
                "**Safe alternatives:**\n"
                "- Check if a variable is set: `test -n \"$VAR\" && echo set || echo unset`\n"
                "- Count env vars without values: `env | wc -l`"
            ),
        }
    return None


def check_read(file_path):
    if SECRET_PATH.search(file_path):
        return {
            **DENY,
            "systemMessage": (
                f"**[secret-guard]** Blocked: `{file_path}` matches a known secrets file pattern.\n\n"
                "Reading this file would send credentials, keys, or tokens directly into "
                "the LLM conversation context. Reference the file path without reading it."
            ),
        }
    return None


def check_write(file_path):
    if SECRET_PATH.search(file_path):
        return {
            "systemMessage": (
                f"**[secret-guard]** Warning: `{file_path}` matches a known secrets file pattern.\n\n"
                "Ensure this file is listed in `.gitignore`. Never commit real credential values — "
                "use placeholders like `YOUR_API_KEY_HERE` in examples."
            )
        }
    return None


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        result = None
        if tool_name == "Bash":
            result = check_bash(tool_input.get("command", ""))
        elif tool_name == "Read":
            result = check_read(tool_input.get("file_path", ""))
        elif tool_name in ("Write", "Edit", "MultiEdit"):
            result = check_write(tool_input.get("file_path", ""))

        print(json.dumps(result or {}))
    except Exception as e:
        print(json.dumps({"systemMessage": f"secret-guard error: {e}"}))


if __name__ == "__main__":
    main()
