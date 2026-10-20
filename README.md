# Development environment template

A small, reusable home for shared development-tool configuration. Secrets live in SOPS-encrypted JSON; the age identity stays outside Git. `profile.sh` loads shared credentials in Bash, while project `.envrc` files can load additional encrypted values.

## Setup

Requirements: Bash, Python 3, `direnv`, `sops` (3.9 or newer), and `age-keygen`. On Debian or Ubuntu, `sudo apt install direnv age` covers direnv and age; install SOPS from the `.deb` on its [releases page](https://github.com/getsops/sops/releases) and compare its SHA-256 with the digest GitHub shows for that file (the release checksum list omits packages). With Go, `go install github.com/getsops/sops/v3/cmd/sops@latest` and `go install filippo.io/age/cmd/age-keygen@latest` also work; the scripts find binaries in `~/go/bin` too.

The age identity is read from `$SOPS_AGE_KEY_FILE`, else `$XDG_CONFIG_HOME/sops/age/keys.txt`, else `~/.config/sops/age/keys.txt`, matching SOPS. Encryption always uses the recipients in `.sops.yaml`, so the key file may hold other identities too. To let another key decrypt the vault, add it to the `age:` list in `.sops.yaml` (comma-separated) and run `sops updatekeys` on each file under `secrets/`.

1. Create a private repository from this GitHub template and clone it.
2. Run `./scripts/setup --add-keys`. This creates `~/.config/sops/age/keys.txt`, `.sops.yaml`, and an encrypted profile, prompts for shared tool credentials with hidden input, then adds one guarded source line to `~/.bashrc`, followed by the direnv hook if `.bashrc` lacks one (an existing hook stays last). Plain `./scripts/setup` skips the prompts.
3. Back up the age identity securely. Anyone with that file can decrypt the vault; losing it makes the vault unrecoverable.
4. Add shared credentials with `./scripts/envtool set profile TAIGA_PASSWORD` (input is hidden), or `./scripts/envtool edit profile`.
5. Start a new Bash shell. `./scripts/envtool list profile` displays names only.

If existing shared exports are already in `.bashrc` and present in the current shell, use `./scripts/setup --migrate-bashrc`. It encrypts and verifies them before removing their old export lines. Review the encrypted variable names with `envtool list`; secret values are never printed by setup.

## Project variables

Add a project value with `./scripts/envtool set project/my-project STRIPE_SECRET_KEY`. In that project's `.envrc`, use:

```bash
watch_file "$HOME/work/utils/jon-dev-env/secrets/project/my-project.enc.json"
_dev_env_exports="$("$HOME/work/utils/jon-dev-env/scripts/envtool" export project/my-project)" || exit 1
eval "$_dev_env_exports"; unset _dev_env_exports
```

Run `direnv allow` in the project. Project values override profile defaults. The included `.envrc` shows the pattern and can load an ignored `.env.local` for nonsecret local settings.

For a devcontainer, launch VS Code or the devcontainer CLI from a shell that has loaded the desired environment. Its `containerEnv` can then use `${localEnv:TAIGA_API_URL}` and similar entries. See `examples/devcontainer.jsonc` for mounts and variable wiring. Claude and Codex authentication files remain in their existing home directories and are mounted from there; they are not copied into this repository.

Run the tests with `python3 -m unittest discover -s tests`. They use a temporary home directory and never touch your key or vault.

Never commit the age identity, decrypted JSON, `.env`, or `.env.local`. An encrypted repo still reveals variable names and recipient metadata, so keep personal vaults private.
