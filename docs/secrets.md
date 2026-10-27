# Secrets

> How the SOPS/age vault works: tools, the age identity, recipients, `envtool`, and which
> variables to store where. Overview and Quickstart: [README.md](../README.md).

## Prerequisites

Bash, Python 3, `direnv`, `sops` 3.9 or newer, and `age-keygen`. `uv` is needed only for the
optional Taiga MCP install ([taiga-mcp.md](taiga-mcp.md)).

- Debian or Ubuntu: `sudo apt install direnv age` covers direnv and age. Install SOPS from the
  `.deb` on its [releases page](https://github.com/getsops/sops/releases) and compare its
  SHA-256 with the digest GitHub shows for that file (the release checksum list omits packages).
- Go: `go install github.com/getsops/sops/v3/cmd/sops@latest` and
  `go install filippo.io/age/cmd/age-keygen@latest`. The scripts also look in `~/go/bin`.

`scripts/setup` checks `sops`, `age-keygen`, and `direnv` before creating anything. It exits
non-zero with a `setup: missing required tools:` message that lists each missing tool with an
install hint. A missing `uv` is only a note; the rest of setup still runs.

## The age identity

The key file is read from `$SOPS_AGE_KEY_FILE`, else `$XDG_CONFIG_HOME/sops/age/keys.txt`, else
`~/.config/sops/age/keys.txt`, the same order SOPS uses on Linux. `SOPS_AGE_KEY` in the
environment also satisfies the identity check.

- First run: setup creates the key file with `age-keygen` if it is absent (directory mode 0700,
  file mode 0600), writes `.sops.yaml` naming the first local public key as the `age:` recipient
  for `secrets/.*\.enc\.json`, and creates an empty encrypted `secrets/profile.enc.json`.
  Neither `.sops.yaml` nor `secrets/` ships in the template; setup creates them in your private
  copy. It ends by printing the key path with a reminder to back it up.
- Second machine or restore: put the key file in place before running setup. If `.sops.yaml`
  exists and the key file is missing, setup stops and asks you to restore it. If no local
  identity matches a `.sops.yaml` recipient, it stops with `No identity in ... matches a
  .sops.yaml recipient`.
- Backup: anyone with the key file can decrypt the vault, and losing it makes the vault
  unrecoverable. Encryption always uses the recipients in `.sops.yaml`, so the key file may hold
  other identities too.

## Adding recipients

To let another key decrypt the vault, add its public key to the `age:` list in `.sops.yaml`
(comma-separated), then run `sops updatekeys` on each file under `secrets/`.

## Vault layout and envtool

Each scope is one encrypted JSON file of string values keyed by valid environment variable names:

| Scope | File |
|---|---|
| `profile` | `secrets/profile.enc.json` |
| `project/<name>` | `secrets/project/<name>.enc.json` (name uses letters, digits, `_`, `-`) |

| Command | What it does |
|---|---|
| `envtool set <scope> NAME` | Reads the value with hidden input and re-encrypts the scope |
| `envtool edit <scope>` | Opens the scope in SOPS, which honors `$EDITOR`; creates the scope if missing |
| `envtool list <scope>` | Prints variable names only |
| `envtool export <scope>` | Prints `export NAME=value` lines; used by `profile.sh` and `.envrc` |
| `envtool init` | Creates the identity, `.sops.yaml`, and empty profile; called by setup |

`./scripts/envtool --help` documents every subcommand. Secret values are never printed by setup
or `list`, and no plaintext file is written.

## Shared variables and scopes

The profile scope holds values every shell gets. The repository's own tooling needs only these:

| Variable | Needed by | |
|---|---|---|
| `TAIGA_API_URL`, `TAIGA_USERNAME`, `TAIGA_PASSWORD` | `scripts/taiga-story.sh`, `scripts/taiga-comment.sh`, and the Taiga MCP launcher | Required. Setup prompts for them (hidden input) when stdin is a terminal, otherwise it names the missing ones |
| `GH_TOKEN` | `gh`, and the devcontainer example's `containerEnv` | Optional; `gh auth login` works instead |

Add anything else your own tools read, such as package or API tokens, the same way. If you skip
a prompt, add the value later with `./scripts/envtool set profile NAME`.

Choose a scope by who reads the value:

- Use the profile when a tool starts outside a project directory: user-wide MCP servers, `gh`,
  and devcontainer `containerEnv`, which reads the host shell at launch, so direnv values never
  reach it.
- Use the profile for values that are the same in every repository, such as your Taiga login.
- Use a project scope through direnv for values that differ per project or carry a large blast
  radius, such as a production Stripe key; it then exists only inside that project's directory.
- When the same value shows up in several project scopes, move it:
  `./scripts/envtool set profile NAME`, then remove it from each project with
  `./scripts/envtool edit project/<project>`.

## Migrating exports from .bashrc

If `~/.bashrc` already exports values you want in the vault, run
`./scripts/setup --migrate-bashrc NAME...` from a shell where they are set. It encrypts and
verifies the named values, then removes only their `export` lines; other lines stay. Review the
result with `./scripts/envtool list profile`.

## Never committed

Never commit the age identity, decrypted JSON, `.env`, or `.env.local`; `.gitignore` covers
`.env`, `.env.local`, `*.dec.json`, and `*.plaintext.json`. An encrypted repository still reveals
variable names and recipient metadata, so keep personal vaults private.
