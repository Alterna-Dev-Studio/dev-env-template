# Development environment template

A small, reusable home for shared development-tool configuration. Secrets live in SOPS-encrypted JSON and the age key stays outside Git. Your shell loads shared credentials and tool paths on startup, and project `.envrc` files can load more.

## Quickstart

```bash
gh repo create my-dev-env --template Alterna-Dev-Studio/dev-env-template --private --clone
cd my-dev-env && ./scripts/setup
```

Setup checks for missing tools, creates the age key and encrypted profile, wires your Bash startup files, asks (hidden input) for the Taiga login, allows the clone's `.envrc`, installs the Taiga MCP server when `uv` is present (`--skip-taiga-mcp` opts out), and ends by printing the key file to back up. Then open a new Bash shell.

## Commands

| Command | What it does |
|---|---|
| `./scripts/setup` | Installs the profile and creates the vault |
| `./scripts/envtool set <scope> NAME` | Adds a vault value (hidden input) |
| `./scripts/envtool edit <scope>` | Edits a scope in your editor |
| `./scripts/envtool list <scope>` | Lists variable names only |
| `./scripts/setup-taiga-mcp` | Installs the Taiga MCP server |
| `./scripts/taiga-mcp` | Launches the Taiga MCP server |
| `./scripts/taiga-story.sh` | Fetches a Taiga story |
| `./scripts/taiga-comment.sh` | Comments on a Taiga item |
| `python3 -m unittest discover -s tests -v` | Runs the tests |

## Secrets and scopes

Values every shell needs, such as your Taiga login, go in the profile scope. Values that differ per project or are risky if leaked go in a project scope. Back up the age key setup prints: losing it makes the vault unrecoverable. Details: [docs/secrets.md](docs/secrets.md).

## Shell profile

Setup adds guarded source lines to your Bash startup files so each shell gets the credentials, a tidy `PATH` with `~/.local/bin` first, and your optional aliases. Details: [docs/shell-profile.md](docs/shell-profile.md).

## Project variables

Store a project value with `./scripts/envtool set project/my-project NAME`, then load it from that project's `.envrc` and run `direnv allow`:

```bash
watch_file "$DEV_ENV_HOME/secrets/project/my-project.enc.json"
_dev_env_exports="$("$DEV_ENV_HOME/scripts/envtool" export project/my-project)" || exit 1
eval "$_dev_env_exports"; unset _dev_env_exports
```

Project values override profile defaults.

## Devcontainer

Each repository opts in by merging `examples/devcontainer.jsonc` into its devcontainer configuration. Only the shell fragments and selected host variables reach the container, never the age key or vault. Details: [docs/devcontainer.md](docs/devcontainer.md).

## Taiga MCP

Setup installs a local Taiga MCP server that reads its credentials from the vault, so no client configuration holds a password. Details: [docs/taiga-mcp.md](docs/taiga-mcp.md).

## Agent skills

Claude Code and Codex ship with skills that analyze a story, implement it task by task, and resolve review threads. The Taiga mapping is in `AGENTS.md`; sources and patches are recorded in [docs/saasdk-install.md](docs/saasdk-install.md).

## Testing

The tests use a temporary home directory and never touch your key or vault. Policy: [docs/testing-workflow.md](docs/testing-workflow.md).

## Security

Never commit the age identity, decrypted JSON, `.env`, or `.env.local`. Keep personal vaults private, since an encrypted repo still reveals variable names and recipients.
