# Taiga MCP

> How to install the local Taiga MCP server, how `scripts/taiga-mcp` launches it, and how to
> register it with Claude Code and Codex. Overview and Quickstart: [README.md](../README.md).

## Install

`./scripts/setup-taiga-mcp` clones
[pytaiga-mcp](https://github.com/Alterna-Dev-Studio/pytaiga-mcp) into
`~/work/utils/pytaiga-mcp` and runs `uv sync --frozen` there. It requires `git` and `uv`.

- Set `PYTAIGA_MCP_HOME` to use another location. The launcher reads the same variable, so
  export it in both places.
- If the directory already exists it must be a pytaiga-mcp checkout (`pyproject.toml`,
  `uv.lock`, `src/server_workflow.py`, and `src/server_full.py`). Otherwise the script
  refuses and changes nothing.
- `scripts/setup` runs this install for you when it can find `uv`. If `uv` is missing it
  prints a note and skips the install. Pass `--skip-taiga-mcp` to skip the install and the
  Codex registration on purpose.
- When `codex` is on `PATH`, `setup-taiga-mcp` also registers this clone's launcher for
  Codex with `codex mcp add taiga-py -- "$PWD/scripts/taiga-mcp" full`. That command
  replaces an entry of the same name, so re-running is safe. Without `codex` the script
  prints the command so you can run it later.

## Launch

`scripts/taiga-mcp workflow|full [profile|project/NAME]` starts the server over stdio.

- With no scope named and `TAIGA_API_URL`, `TAIGA_USERNAME`, and `TAIGA_PASSWORD` all set in
  the environment, it uses them.
- Otherwise it decrypts the named vault scope (default `profile`) through `scripts/envtool`.
  Scopes are described in [secrets.md](secrets.md).
- The `PANGOLIN_RESOURCE_TOKEN`, `PANGOLIN_ACCESS_TOKEN_ID`, `PANGOLIN_ACCESS_TOKEN`, and
  `PANGOLIN_SESSION_REQUEST_PARAM` variables are passed through when present and cleared
  otherwise, so the checkout's legacy `.env` cannot supply them.
- Neither client configuration below holds credentials.

Errors name the fix:

- `Install pytaiga-mcp and its virtual environment at ... (run scripts/setup-taiga-mcp)`
  means the checkout or its `.venv` is missing.
- `Missing Taiga settings: set ... in the environment or in vault scope ...` means a
  required variable is empty in the source the launcher chose.

## Modes

- `full` is the complete tool set (`get_user_story`, `get_user_story_statuses`,
  `list_epics`, and so on). The skills installed under `.claude/skills/` and
  `.agents/skills/` are written against it.
- `workflow` is the smaller ref-based tool set, suitable for a user-wide entry.

## Client registration

- **Claude Code in this repository:** the committed `.mcp.json` runs `scripts/taiga-mcp full`
  as server `taiga-py`, overriding any user-level server of the same name. Nothing to do.
- **Codex:** `codex mcp add taiga-py -- "$PWD/scripts/taiga-mcp" full`, run from the
  repository root. `setup-taiga-mcp` does this when `codex` is installed.
- **User-wide Claude entry:**
  `claude mcp add -s user taiga-py -- "$PWD/scripts/taiga-mcp" workflow`.

In a session, call `get_default_session` first and prefer `login()` without explicit
credentials.
