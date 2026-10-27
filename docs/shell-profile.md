# Shell profile

> How the profile gets into Bash: what `profile.sh` does, which startup files `scripts/setup`
> edits and in what order, what `shell/paths.sh` and `shell/aliases.sh` set up, and
> `DEV_ENV_HOME`. Overview and Quickstart: [README.md](../README.md).

## What profile.sh does

Bash startup files source `profile.sh` from your clone. It:

- Always sources `shell/paths.sh`. It sources `shell/aliases.sh` only in interactive shells.
- Loads the `profile` scope of the vault once per clone. It runs `scripts/envtool export profile`,
  evaluates the output, and records that this clone has loaded, so a nested shell does not
  decrypt again. If decryption fails it prints `dev-env: could not load encrypted profile` to
  stderr and the shell carries on. It never prints secret values or writes a plaintext file.
  The vault itself is described in [secrets.md](secrets.md).
- Exports `DEV_ENV_HOME` as the clone directory after the profile loads, so a `DEV_ENV_HOME`
  stored in the vault cannot redirect it. Project `.envrc` files use it to find
  `scripts/envtool` and `secrets/` without hardcoding the clone path (see the `.envrc` snippet
  in [README.md](../README.md)).

## What setup edits

`scripts/setup` edits two Bash startup files. Re-running it is idempotent: it rewrites its own
managed lines rather than adding copies. Each edit goes through a temporary file and an atomic
replace, and keeps the file's mode.

- `~/.bashrc` gets the comment `# Shared development tooling environment (managed by dev-env setup).`
  and a guarded line, `[ -f .../profile.sh ] && source .../profile.sh`.
  - If `.bashrc` has no direnv hook and `direnv` is installed, setup appends
    `eval "$(direnv hook bash)"` after the profile line, under `# Keep direnv last (managed by dev-env setup).`
  - If `.bashrc` already has a direnv hook, setup places the profile lines before it.

  Either way the profile loads first. Project `.envrc` files need the hook, and the hook must
  run after the profile so that `DEV_ENV_HOME` already exists.
- The Bash login file is `~/.bash_profile` or `~/.bash_login` if one exists, otherwise
  `~/.profile`. It gets
  `if [ -n "${BASH_VERSION:-}" ] && [ -f .../profile.sh ]; then . .../profile.sh; fi` under
  `# Development tooling profile (managed by dev-env setup).`

Setup also runs `direnv allow` on the clone's own `.envrc`. Open a new Bash shell after setup so
the profile is loaded.

## shell/paths.sh

Sourced in Bash login and interactive shells, and inside opted-in devcontainers
([devcontainer.md](devcontainer.md)).

- It prepends directories that exist, never duplicating a PATH entry. It adds them in reverse
  order so the final order puts `~/.local/bin` first (where Herdr and Collie live), then
  `~/bin`, `$VOLTA_HOME/bin`, `$PNPM_HOME`, `$FLYCTL_INSTALL/bin`, `~/go/bin`,
  `~/.dotnet/tools`, `/usr/local/go/bin`, and `/go/bin`. A directory that does not exist is
  skipped.
- It sets each of these only when it is not already set: `VOLTA_HOME` (`~/.volta`),
  `VOLTA_FEATURE_PNPM` (`1`), `PNPM_HOME` (`~/.local/share/pnpm`), and `FLYCTL_INSTALL`
  (`~/.fly`).

## shell/aliases.sh

Empty in the template. Put personal interactive aliases there in your private copy. Keep
machine-specific display, SSH relay, Docker, and system installation settings in the machine
bootstrap, not here. If you previously set the same portable paths or aliases in `.bashrc` or
`.profile`, remove those old lines after confirming the new profile works.
