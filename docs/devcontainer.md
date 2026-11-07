# Devcontainer

> How a repository opts in to the shared shell fragments and tool credentials inside a
> devcontainer: what `examples/devcontainer.jsonc` configures entry by entry and what
> `shell/install-container.sh` installs. Overview and Quickstart: [README.md](../README.md).

## How it works

- Launch VS Code or the devcontainer CLI from a host shell that has already loaded the
  environment you want. The container only sees what that shell exported.
- Each repository opts in explicitly by merging `examples/devcontainer.jsonc` into its
  `.devcontainer/devcontainer.json`. Repositories that do not merge it are unaffected.
- Neither the age identity nor the encrypted vault is mounted or decrypted in the container.

## What the example configures

- `initializeCommand` runs on the host. It creates `~/.claude` and `~/.codex` and touches
  `~/.claude.json`, so the mounts below always have a source.
- `mounts` has four entries:
  - `${localEnv:DEV_ENV_HOME}/shell` is bound read-only at `/opt/dev-env-shell`. Only `shell/`
    is exposed. `DEV_ENV_HOME` must be set in the launching shell, which `profile.sh`
    guarantees (see [shell-profile.md](shell-profile.md)).
  - `~/.claude`, `~/.claude.json`, and `~/.codex` are bound into `/home/vscode`. Claude and
    Codex authentication stays in those host locations and is never copied into this
    repository. Change `/home/vscode` to the project's container user.
- `postCreateCommand` is `bash /opt/dev-env-shell/install-container.sh`. If the project already
  has a `postCreateCommand`, append this command to it (for example with `&&`) instead of
  replacing it.
- `containerEnv` passes `TAIGA_API_URL`, `TAIGA_USERNAME`, `TAIGA_PASSWORD`, `GH_TOKEN`, and
  `GH_TOKEN_FOR_PACKAGES` from the launching process's environment (`${localEnv:...}`). If
  VS Code or the devcontainer CLI is started from a direnv-activated project shell, any exported
  project value with one of those names, such as a project-scoped `TAIGA_PASSWORD` or
  `GH_TOKEN`, is forwarded into the container. Launch from a shell outside the project, or leave
  those names out of the project scope. Put anything the container needs in the profile scope
  (see [secrets.md](secrets.md)).

## What install-container.sh does

- Writes a managed block, from `# >>> dev-env shell (managed by install-container.sh) >>>` to
  `# <<< dev-env shell <<<`. It sources `paths.sh` always and `aliases.sh` in interactive
  shells, both from the mounted `/opt/dev-env-shell`.
- Installs the block at the top of `~/.bashrc`, because Ubuntu's `.bashrc` returns early in
  non-interactive shells, and at the end of `~/.profile`.
- Skips a file that already contains the marker, so re-running is safe. It builds each file
  through a temporary copy and `mv`, keeping the original file mode.
- Installs shell fragments only: no profile, no secrets.
