# Repository Guidelines

## Project Structure
A small Bash/Python home for shared development-tool configuration. `profile.sh` sources
`shell/paths.sh` and `shell/aliases.sh`, then loads SOPS-encrypted credentials through
`scripts/envtool`. `scripts/setup` installs the profile into Bash startup files. `examples/`
holds the devcontainer opt-in. Tests live in `tests/` and use Python `unittest`. There is no
application code, no F#, no .NET, and no CI test gate. See [README.md](README.md) for setup.

## Build, Test, and Development Commands
- Tests: `python3 -m unittest discover -s tests -v`. This is the only suite and the merge gate.
- Static checks for changed Bash: `bash -n <file>` and `shellcheck <file>`.
- Policy: [docs/testing-workflow.md](docs/testing-workflow.md), suite boundaries in
  [docs/testing-strategy.md](docs/testing-strategy.md), conventions in
  [docs/testing-conventions.md](docs/testing-conventions.md).

## Taiga Mapping (consumer-local)
- Tracker: Taiga at `$TAIGA_API_URL`. Project **Alterna Dev Studio**, id **4**, slug
  `alterna-dev-studio`. You-Thon is project 3; never use it from this repository.
- Story statuses in project 4 are New, Ready, In progress, Ready for test, Done, Archived.
  Resolve every status and task status ID by exact name at run time. Do not hardcode numeric
  IDs; any numbers that appear in installed skill bodies or `.claude/skills/shared/merge-side-effects.md`
  are You-Thon values.
- Helpers: `scripts/taiga-story.sh <ref> [project] [--issue|--epic] [--with-tasks]` (default
  project 4) and `scripts/taiga-comment.sh <item-id> "<comment>" [--issue]`. Both read
  `TAIGA_API_URL`, `TAIGA_USERNAME`, `TAIGA_PASSWORD` from the environment and never print them.
- MCP: `.mcp.json` launches `scripts/taiga-mcp full` (pytaiga-mcp in **full** mode, stdio)
  for Claude Code in this repository, overriding any user-level `workflow` server. The installed
  Claude skill bodies and their `mcp__taiga-py__*` grants are written against full mode
  (`get_user_story`, `get_user_story_statuses`, `list_epics`, ...), so the names match as is.
  The launcher uses `TAIGA_*` from the environment when present and otherwise decrypts this
  repository's SOPS profile; it needs the pytaiga-mcp checkout from `scripts/setup-taiga-mcp`. Check `get_default_session` first and
  prefer `login()` without explicit credentials.
- Merge automation (`taiga-update-on-merge.sh`, `taiga-sync.yml`) is **not** installed here.
  The `close-tasks-on-merge` and `mark-done-on-merge` labels and tags are recorded for
  planning only and have no effect on merge.

## Agent Skills
Native SAASDK skills are installed under `.claude/skills/` (Claude Code) and `.agents/skills/`
(Codex): `analyze-story`, `implement-story`, `pr-converse`, `review-tests`, `codex-review-pr`.
`pr-comments-resolve` (resolve review threads) is installed for both from you-thon.
Provenance, per-file hashes, and the consumer-local patches are in
[docs/saasdk-install.md](docs/saasdk-install.md). Codex bodies read this file first; the
section above is the consumer-local mapping they require.

## Commit & Pull Request Guidelines
Short imperative subjects with conventional prefixes (`feat:`, `fix:`, `docs:`, `test:`).
Run the test suite before opening a PR. Attribution rules:
[.claude/skills/shared/commit-attribution.md](.claude/skills/shared/commit-attribution.md).
Never commit the age identity, decrypted JSON, `.env`, or `.env.local`.

## Code Review Rules
- Bash scripts start with `set -euo pipefail` (or `set -uo pipefail` where a command's failure
  is handled explicitly) and must never print secret values or write plaintext secrets to disk.
- Python is standard library only; no third-party imports.
- Tests run against a temporary `HOME` and temporary repository copies. They must not read the
  host's SOPS identity, touch the real `~/.bashrc`, or require network access.
- Startup-file edits are idempotent: re-running `scripts/setup` must not duplicate lines.
- PATH changes must not duplicate entries and must keep `~/.local/bin` first.
