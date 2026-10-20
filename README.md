# Development environment template

A small, reusable home for shared development-tool configuration. Secrets live in SOPS-encrypted JSON; the age identity stays outside Git. `profile.sh` sources portable PATH and optional alias fragments, then loads shared credentials. Project `.envrc` files can load additional encrypted values.

## Setup

Requirements: Bash, Python 3, `direnv`, `sops` (3.9 or newer), and `age-keygen`. On Debian or Ubuntu, `sudo apt install direnv age` covers direnv and age; install SOPS from the `.deb` on its [releases page](https://github.com/getsops/sops/releases) and compare its SHA-256 with the digest GitHub shows for that file (the release checksum list omits packages). With Go, `go install github.com/getsops/sops/v3/cmd/sops@latest` and `go install filippo.io/age/cmd/age-keygen@latest` also work; the scripts find binaries in `~/go/bin` too.

The age identity is read from `$SOPS_AGE_KEY_FILE`, else `$XDG_CONFIG_HOME/sops/age/keys.txt`, else `~/.config/sops/age/keys.txt`, matching SOPS. Encryption always uses the recipients in `.sops.yaml`, so the key file may hold other identities too. To let another key decrypt the vault, add it to the `age:` list in `.sops.yaml` (comma-separated) and run `sops updatekeys` on each file under `secrets/`.

1. Create a private repository from this GitHub template and clone it.
2. Run `./scripts/setup --add-keys`. This creates `~/.config/sops/age/keys.txt`, `.sops.yaml`, and an encrypted profile, prompts for shared tool credentials with hidden input, then adds guarded source lines to `~/.bashrc` and the Bash login file (`~/.profile` unless `~/.bash_profile` or `~/.bash_login` exists). It adds the direnv hook if `.bashrc` lacks one, after the profile source. Plain `./scripts/setup` skips the prompts.
3. Back up the age identity securely. Anyone with that file can decrypt the vault; losing it makes the vault unrecoverable.
4. Add shared credentials with `./scripts/envtool set profile TAIGA_PASSWORD` (input is hidden), or `./scripts/envtool edit profile`.
5. Start a new Bash shell. `./scripts/envtool list profile` displays names only.

If existing shared exports are already in `.bashrc` and present in the current shell, use `./scripts/setup --migrate-bashrc`. It encrypts and verifies them before removing their old export lines. Review the encrypted variable names with `envtool list`; secret values are never printed by setup.

`shell/paths.sh` adds existing user tool directories without duplicating PATH entries, keeping `~/.local/bin` first for Herdr and Collie. It sets Volta, pnpm, and Fly home variables. Put personal interactive Bash aliases in `shell/aliases.sh` in your private copy. Keep machine-specific display, SSH relay, Docker, and system installation settings in the machine bootstrap. If you previously set the same portable paths or aliases in `.bashrc` or `.profile`, remove those old lines after confirming the new profile works.

## Project variables

Add a project value with `./scripts/envtool set project/my-project STRIPE_SECRET_KEY`. In that project's `.envrc`, use:

```bash
watch_file "$HOME/work/utils/jon-dev-env/secrets/project/my-project.enc.json"
_dev_env_exports="$("$HOME/work/utils/jon-dev-env/scripts/envtool" export project/my-project)" || exit 1
eval "$_dev_env_exports"; unset _dev_env_exports
```

Run `direnv allow` in the project. Project values override profile defaults. The included `.envrc` shows the pattern and can load an ignored `.env.local` for nonsecret local settings.

For a devcontainer, launch VS Code or the devcontainer CLI from a host shell that has loaded the desired environment. Explicitly opt in each repository by merging `examples/devcontainer.jsonc` into its devcontainer configuration. Its read-only bind mount exposes only `shell/` at `/opt/dev-env-shell`; `postCreateCommand` installs source blocks into the container user's Bash startup files. If the project already has a `postCreateCommand`, add `bash /opt/dev-env-shell/install-container.sh` to that command. Adjust the sample `/home/vscode` credential mount targets to the project's container user. `containerEnv` passes selected host variables, including `GH_TOKEN_FOR_PACKAGES`; neither the age identity nor encrypted vault is mounted or decrypted in the container. Claude and Codex authentication files remain in their existing home directories and are mounted from there; they are not copied into this repository.

Run the tests with `python3 -m unittest discover -s tests`. They use a temporary home directory and never touch your key or vault.

Never commit the age identity, decrypted JSON, `.env`, or `.env.local`. An encrypted repo still reveals variable names and recipient metadata, so keep personal vaults private.

Run `python3 -m unittest discover -s tests -v` to verify repeatable PATH setup and the shell-only devcontainer installer without a SOPS key.
