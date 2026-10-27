# Development environment template

A small, reusable home for shared development-tool configuration. Secrets live in SOPS-encrypted JSON; the age identity stays outside Git. `profile.sh` sources portable PATH and optional alias fragments, then loads shared credentials. Project `.envrc` files can load additional encrypted values.

## Quickstart

```bash
gh repo create my-dev-env --template Alterna-Dev-Studio/dev-env-template --private --clone
cd my-dev-env && ./scripts/setup
```

Setup checks for `sops`, `age-keygen`, and `direnv`, creates the age identity and encrypted profile, wires the Bash startup files, prompts (hidden input) for the three [required variables](#shared-variables), allows the clone's `.envrc` with direnv, installs the Taiga MCP server when `uv` is present (`--skip-taiga-mcp` opts out), and ends by printing the key file to back up. Then open a new Bash shell. Everything below explains what setup did and how to add project-scoped secrets.

## Setup

Requirements: Bash, Python 3, `direnv`, `sops` (3.9 or newer), and `age-keygen`. On Debian or Ubuntu, `sudo apt install direnv age` covers direnv and age; install SOPS from the `.deb` on its [releases page](https://github.com/getsops/sops/releases) and compare its SHA-256 with the digest GitHub shows for that file (the release checksum list omits packages). With Go, `go install github.com/getsops/sops/v3/cmd/sops@latest` and `go install filippo.io/age/cmd/age-keygen@latest` also work; the scripts find binaries in `~/go/bin` too.

The age identity is read from `$SOPS_AGE_KEY_FILE`, else `$XDG_CONFIG_HOME/sops/age/keys.txt`, else `~/.config/sops/age/keys.txt`, matching SOPS. Encryption always uses the recipients in `.sops.yaml`, so the key file may hold other identities too. To let another key decrypt the vault, add it to the `age:` list in `.sops.yaml` (comma-separated) and run `sops updatekeys` on each file under `secrets/`.

1. Create a private repository from this GitHub template and clone it.
2. Run `./scripts/setup`. It first checks the prerequisites and names any missing tool with an install hint before creating anything. It then creates `~/.config/sops/age/keys.txt`, `.sops.yaml`, and an encrypted profile, then adds guarded source lines to `~/.bashrc` and the Bash login file (`~/.profile` unless `~/.bash_profile` or `~/.bash_login` exists). It adds the direnv hook if `.bashrc` lacks one, after the profile source, and names any [required variable](#shared-variables) the profile still lacks.
3. Back up the age identity securely; setup prints its path. Anyone with that file can decrypt the vault; losing it makes the vault unrecoverable.
4. If you skipped a prompt, add the value later with `./scripts/envtool set profile NAME` (input is hidden), or use `./scripts/envtool edit profile`. `./scripts/envtool --help` documents every subcommand.
5. Start a new Bash shell. `./scripts/envtool list profile` displays names only.

If `.bashrc` already exports values you want in the vault, run `./scripts/setup --migrate-bashrc NAME...` from a shell where they are set. It encrypts and verifies the named values before removing their export lines; other exports are left alone. Review the encrypted variable names with `envtool list`; secret values are never printed by setup.

`shell/paths.sh` adds existing user tool directories without duplicating PATH entries, keeping `~/.local/bin` first for Herdr and Collie. It sets Volta, pnpm, and Fly home variables. Put personal interactive Bash aliases in `shell/aliases.sh` in your private copy. Keep machine-specific display, SSH relay, Docker, and system installation settings in the machine bootstrap. If you previously set the same portable paths or aliases in `.bashrc` or `.profile`, remove those old lines after confirming the new profile works.

## Shared variables

The profile scope holds values every shell gets. The repository's own tooling needs only these:

| Variable | Needed by | |
|---|---|---|
| `TAIGA_API_URL`, `TAIGA_USERNAME`, `TAIGA_PASSWORD` | `scripts/taiga-story.sh`, `scripts/taiga-comment.sh`, and the Taiga MCP launcher | Required; setup reports any that are missing |
| `GH_TOKEN` | `gh`, and the devcontainer example's `containerEnv` | Optional; `gh auth login` works instead |

Add anything else your own tools read, such as package or API tokens, the same way.

Choose a scope by who reads the value:

- Use the profile when a tool starts outside a project directory: user-wide MCP servers, `gh`, and devcontainer `containerEnv`, which reads the host shell at launch, so direnv values never reach it.
- Use the profile for values that are the same in every repository, such as your Taiga login.
- Use a project scope through direnv for values that differ per project or carry a large blast radius, such as a production Stripe key; it then exists only inside that project's directory.
- When the same value shows up in several project scopes, move it: `./scripts/envtool set profile NAME`, then remove it from each project with `./scripts/envtool edit project/<project>`.

## Project variables

Add a project value with `./scripts/envtool set project/my-project STRIPE_SECRET_KEY`. `profile.sh` exports `DEV_ENV_HOME`, the directory of this clone, so project `.envrc` files never hardcode its location. In that project's `.envrc`, use:

```bash
watch_file "$DEV_ENV_HOME/secrets/project/my-project.enc.json"
_dev_env_exports="$("$DEV_ENV_HOME/scripts/envtool" export project/my-project)" || exit 1
eval "$_dev_env_exports"; unset _dev_env_exports
```

Run `direnv allow` in the project. Project values override profile defaults. The included `.envrc` shows the pattern and can load an ignored `.env.local` for nonsecret local settings.

For a devcontainer, launch VS Code or the devcontainer CLI from a host shell that has loaded the desired environment. Explicitly opt in each repository by merging `examples/devcontainer.jsonc` into its devcontainer configuration. Its read-only bind mount exposes only `shell/` at `/opt/dev-env-shell`; `postCreateCommand` installs source blocks into the container user's Bash startup files. If the project already has a `postCreateCommand`, add `bash /opt/dev-env-shell/install-container.sh` to that command. Adjust the sample `/home/vscode` credential mount targets to the project's container user. `containerEnv` passes selected host variables, including `GH_TOKEN_FOR_PACKAGES`; neither the age identity nor encrypted vault is mounted or decrypted in the container. Claude and Codex authentication files remain in their existing home directories and are mounted from there; they are not copied into this repository.

## Taiga MCP

`./scripts/setup-taiga-mcp` clones [pytaiga-mcp](https://github.com/Alterna-Dev-Studio/pytaiga-mcp) into `~/work/utils/pytaiga-mcp` (override with `PYTAIGA_MCP_HOME`) and installs its locked dependencies with `uv`. `scripts/taiga-mcp workflow|full [profile|project/NAME]` then launches it over stdio with `TAIGA_API_URL`, `TAIGA_USERNAME`, and `TAIGA_PASSWORD` decrypted from the chosen vault scope; neither client configuration holds credentials. The committed `.mcp.json` points Claude Code at `scripts/taiga-mcp full` for this repository, which is the tool set the installed skills expect. `./scripts/setup-taiga-mcp` (run by setup when `uv` is available) also registers the launcher for Codex when `codex` is on PATH. For a user-wide Claude entry, `claude mcp add -s user taiga-py -- "$PWD/scripts/taiga-mcp" workflow` gives the smaller ref-based tool set.

## Agent skills

SAASDK native skills `analyze-story`, `implement-story`, `pr-converse`, `review-tests`, and `codex-review-pr` are installed for Claude Code (`.claude/skills/`) and Codex (`.agents/skills/`). `pr-comments-resolve`, copied from you-thon, is installed for both and resolves PR review threads. `fully-implement-story` (with `implement-task`, `finalize-story-pr`, `rebase-branch`, and the worker roles under `.claude/agents/` and `.codex/agents/`) runs a story end to end: it implements each task with a fresh agent, reviews the tests, opens the PR, and resolves review threads; there is no CI gate (the local suite is the gate) and no manual-testing phase. `AGENTS.md` holds the consumer-local Taiga mapping they read first; `docs/saasdk-install.md` records the pinned sources, per-file hashes, patches, and verification.

Run the tests with `python3 -m unittest discover -s tests`. They use a temporary home directory and never touch your key or vault.

Never commit the age identity, decrypted JSON, `.env`, or `.env.local`. An encrypted repo still reveals variable names and recipient metadata, so keep personal vaults private.

Run `python3 -m unittest discover -s tests -v` to verify repeatable PATH setup and the shell-only devcontainer installer without a SOPS key.
