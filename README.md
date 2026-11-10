# Development environment template

A small, reusable home for shared development-tool configuration. Secrets live in SOPS-encrypted JSON. The key that decrypts them, the age identity, stays outside Git. Your shell loads shared credentials and tool paths on startup, and project `.envrc` files can load more.

## Quickstart

You end up with your own private copy of this repository on GitHub, cloned to your machine and set up.

1. Install the [GitHub CLI](https://cli.github.com/) and sign in with `gh auth login`. Setup also needs `sops`, `age`, `direnv`, and `uv` (for the Taiga MCP server). If any are missing, setup stops before changing anything and prints how to install them; install them, then run `./scripts/setup` inside the clone ([details](docs/secrets.md#prerequisites)).
2. `cd` to the folder that will hold your copy. Step 3 creates the clone **inside this directory**, not under your home directory. `~/work/utils` is the usual choice; the Taiga MCP server is installed there too, as `~/work/utils/pytaiga-mcp`.

   ```bash
   mkdir -p ~/work/utils && cd ~/work/utils
   ```

3. Create your copy and run setup. Replace `my-dev-env` with the name you want for your repository; it becomes the folder name too (here `~/work/utils/my-dev-env`). `gh dev-env` creates the private repository from this template, clones it, and then runs `./scripts/setup` inside the clone:

   ```bash
   gh extension install Alterna-Dev-Studio/gh-dev-env
   gh dev-env my-dev-env
   ```

   Already have a copy on GitHub? Clone it and run setup yourself:

   ```bash
   git clone git@github.com:<your-user>/my-dev-env.git
   cd my-dev-env && ./scripts/setup
   ```

4. Answer setup's prompts for `TAIGA_API_URL`, `TAIGA_USERNAME`, and `TAIGA_PASSWORD`. Only the password is hidden as you type. Setup then creates the vault and your age identity, adds the profile to your Bash startup files, and installs the Taiga MCP server.
5. Back up the file setup prints as `Age identity:`. Without it you cannot decrypt your secrets.
6. Open a new terminal. Your credentials and tool paths are now loaded.

`gh dev-env` works for an organization too: give `owner/name`. Setup options such as `--skip-taiga-mcp` go after the name. Without the extension, `gh repo create my-dev-env --template Alterna-Dev-Studio/dev-env-template --private --clone` followed by `cd my-dev-env && ./scripts/setup` does the same thing. Running setup again is safe.

## Commands

| Command | What it does |
|---|---|
| `gh dev-env <name>` | Creates your private copy, clones it, and runs setup |
| `./scripts/setup` | Installs the profile and creates the vault |
| `dv set <scope> NAME` | Adds a vault value (secrets are hidden as you type) |
| `dv edit <scope>` | Edits a scope in your editor |
| `dv list <scope>` | Lists variable names only |
| `dv taiga-mcp install` | Installs the Taiga MCP server |
| `dv taiga-mcp workflow\|full [scope]` | Launches the Taiga MCP server |
| `dv pangolin-login --dashboard-url URL` | Signs in to Pangolin in your browser; prints a session token |
| `dv pangolin-token` | Checks a pasted Pangolin Share Link; prints its token |
| `dv pangolin-configure <scope> --stdin [--session --dashboard-url URL]` | Stores a piped Pangolin token in a scope |
| `dv taiga-login [scope]` | Signs in to Taiga with your identity provider; prints a Taiga token |
| `dv taiga-configure <scope> --stdin` | Stores a piped Taiga token in a scope (replaces the password) |
| `./scripts/taiga-story.sh` | Fetches a Taiga story |
| `./scripts/taiga-comment.sh` | Comments on a Taiga item |
| `python3 -m unittest discover -s tests -v` | Runs the tests |

`dv` (also `dev-env`) is on `PATH` in every shell that has loaded the profile and runs the scripts in `scripts/` from any directory; `dv --help` lists its commands. Scopes are `profile` or `project/<name>`. Before setup has run, or in a script that may start without the profile, call the scripts by path instead.

## Secrets and scopes

Values every shell needs, such as your Taiga login, go in the profile scope. Values that differ per project or are risky if leaked go in a project scope. Details: [docs/secrets.md](docs/secrets.md).

## Shell profile

Setup adds source lines to your Bash startup files. Each shell then gets the credentials, your optional aliases, and a `PATH` with `~/.local/bin` first and this clone's `bin/` (`dv`, `dev-env`) after your own directories. Details: [docs/shell-profile.md](docs/shell-profile.md).

## Project variables

Store a project value with `dv set project/my-project NAME`, then load it from that project's `.envrc` and run `direnv allow`. The `.envrc` calls the script by path (`$DEV_ENV_HOME`, set by the profile) because direnv may run before any shell has put `dv` on `PATH`:

```bash
watch_file "$DEV_ENV_HOME/secrets/project/my-project.enc.json"
_dev_env_exports="$("$DEV_ENV_HOME/scripts/envtool" export project/my-project)" || exit 1
eval "$_dev_env_exports"; unset _dev_env_exports
```

Project values override profile defaults.

## Devcontainer

Each repository opts in by merging `examples/devcontainer.jsonc` into its devcontainer configuration. Only the shell fragments and selected host variables reach the container, never the age key or vault. Details: [docs/devcontainer.md](docs/devcontainer.md).

## Taiga MCP

Setup installs a local Taiga MCP server that reads its credentials from the vault, so no client configuration holds a password. If Taiga signs you in through an identity provider, `dv taiga-login` gives the server a token tied to your account instead of a Taiga password. If Taiga sits behind Pangolin, our login proxy, the server also needs a Pangolin token from the vault. Details: [docs/taiga-mcp.md](docs/taiga-mcp.md).

## Agent skills

Claude Code and Codex ship with skills that analyze a story, implement it task by task, and resolve review threads. The Taiga mapping is in `AGENTS.md`; sources and patches are recorded in [docs/saasdk-install.md](docs/saasdk-install.md).

## Testing

The tests use a temporary home directory and never touch your key or vault. Policy: [docs/testing-workflow.md](docs/testing-workflow.md).

## Security

Never commit the age identity, decrypted JSON, `.env`, or `.env.local`. Keep personal vaults private, since an encrypted repo still reveals variable names and recipients.
