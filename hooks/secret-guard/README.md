# secret-guard

A Claude Code hook plugin that prevents secrets from leaking into the LLM conversation context.

## What it does

Intercepts tool calls before they execute and blocks or warns on:

| Trigger | Action |
|---------|--------|
| `Bash` — `cat`, `head`, `tail`, etc. on `.env`, `*.pem`, `*.key`, credentials files | Block |
| `Bash` — `env`, `printenv`, or echoing credential env vars | Block |
| `Read` — any path matching a known secrets pattern | Block |
| `Write` / `Edit` — writing to a secrets-pattern path | Warn |

## Secret file patterns detected

- `.env`, `.env.local`, `.env.production`, etc.
- `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `*.ppk`, `*.cer`, `*.crt`
- `credentials` (e.g. `~/.aws/credentials`)
- `secrets.yml`, `secrets.json`, `secrets.toml`
- `id_rsa`, `id_ed25519`, `id_ecdsa`, `id_dsa` (SSH private keys)
- `.netrc`, `.pgpass`

## Install

```bash
claude plugin install secret-guard@claude-kit --scope user
```
