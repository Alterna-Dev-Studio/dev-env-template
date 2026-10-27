# Development environment template

A small, reusable home for shared development-tool configuration. Secrets live in SOPS-encrypted JSON and the age key stays outside Git. Your shell loads shared credentials and tool paths on startup, and project `.envrc` files can load more.

## Quickstart

You end up with your own private copy of this repository on GitHub, cloned to your machine and set up.

1. Install the [GitHub CLI](https://cli.github.com/) and sign in with `gh auth login`. Setup also needs `sops`, `age`, and `direnv`. If any are missing it stops and tells you how to install them ([details](docs/secrets.md#prerequisites)).
2. Go to the folder that should hold your copy, for example `cd ~/work`.
3. Run this, replacing `my-dev-env` with the name you want for your repository:

   ```bash
   bash <(curl -fsSL https://raw.githubusercontent.com/Alterna-Dev-Studio/dev-env-template/main/scripts/new-dev-env) my-dev-env
   ```

4. Answer the prompts. Setup asks for your Taiga URL, username, and password, and the password is not shown as you type.
5. Back up the key file that setup prints at the end. Without it you cannot decrypt your secrets.
6. Open a new terminal. Your credentials and tool paths are now loaded.

The command above makes a private repository under your GitHub account from this template, clones it into `./my-dev-env`, and runs `./scripts/setup` inside it. To use an organization, give `owner/name`. Setup options such as `--skip-taiga-mcp` go after the name. If you'd rather not run a script straight from the web, these two commands do the same thing:

```bash
gh repo create my-dev-env --template Alterna-Dev-Studio/dev-env-template --private --clone
cd my-dev-env && ./scripts/setup
```

Setup also adds a few lines to your Bash startup files, allows the clone's `.envrc`, and installs the Taiga MCP server if `uv` is present. Running it again is safe.

## Commands

| Command | What it does |
|---|---|
| `./scripts/new-dev-env [name]` | Creates your private copy, clones it, and runs setup |
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
