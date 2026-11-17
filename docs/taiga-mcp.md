# Taiga MCP

> How to install the local Taiga MCP server, how `scripts/taiga-mcp` launches it, and how to
> register it with Claude Code and Codex. Overview and Quickstart: [README.md](../README.md).

## Install

`dv taiga-mcp install` (the script is `./scripts/setup-taiga-mcp`) clones
[pytaiga-mcp](https://github.com/Alterna-Dev-Studio/pytaiga-mcp) into
`~/work/utils/pytaiga-mcp` and runs `uv sync --frozen` there. It requires `git` and `uv`.

- Set `PYTAIGA_MCP_HOME` to use another location. The launcher reads the same variable, so
  the MCP client must see it too. It must be an absolute path; a leading `~` is expanded.
- If the directory already exists it must be a pytaiga-mcp checkout (`pyproject.toml`,
  `uv.lock`, `src/server_workflow.py`, and `src/server_full.py`). Otherwise the script
  refuses and changes nothing.
- `scripts/setup` runs this install for you when it can find `uv`. If `uv` is missing it
  prints a note and skips the install. Pass `--skip-taiga-mcp` to skip the install and the
  Codex registration on purpose.
- When `codex` is on `PATH`, it also registers the launcher with Codex (see
  [Client registration](#client-registration)). Otherwise it prints the command to run later.

## Launch

`scripts/taiga-mcp workflow|full [profile|project/NAME]` starts the server over stdio.
`dv taiga-mcp workflow|full [scope]` runs the same launcher from any directory; the client
registrations below keep the script path because MCP clients start it without a shell profile.

- With no scope named and `TAIGA_API_URL`, `TAIGA_USERNAME`, and `TAIGA_PASSWORD` all set in
  the environment, it uses them.
- Otherwise it decrypts the named vault scope (default `profile`) through `scripts/envtool`.
  Scopes are described in [secrets.md](secrets.md).
- Taiga and Pangolin settings come only from that source; the checkout's own `.env` cannot
  supply them.
- Neither client configuration below holds credentials.

Errors name the fix:

- `Install pytaiga-mcp and its virtual environment at ... (run scripts/setup-taiga-mcp)`
  means the checkout or its `.venv` is missing.
- `Missing Taiga settings: set ... in the environment or in vault scope ...` means a
  required variable is empty in the source the launcher chose.

## Taiga behind Pangolin

Pangolin is the login proxy in front of our Taiga server. If the Taiga site asks you to sign in
through Pangolin in your browser, the MCP server needs a Pangolin credential too. Pick one path:

| You are | Use |
|---|---|
| A person with a Pangolin account | [Your own login](#your-own-login) |
| Setting up a shared or automation account | [Share Link from an admin](#share-link-from-an-admin) |

Either way, a scope holds one Pangolin credential: saving one kind removes the other.
`dv pangolin-configure <scope> --clear` removes them all. Restart the MCP server after any
change.

### Your own login

Replace `https://pangolin.example` with the address of the page where you sign in to Pangolin.

1. Run both commands as one pipeline. `--stdin` is required when piping:

   ```bash
   dv pangolin-login --dashboard-url https://pangolin.example | dv pangolin-configure profile --session --dashboard-url https://pangolin.example --stdin
   ```

2. A browser tab opens on Pangolin's confirm page showing a short device code. The same code
   and URL are printed in the terminal. Sign in with your usual account (password, 2FA, or your
   company identity provider) and confirm the code. It expires in a few minutes.
3. Success prints `Saved PANGOLIN_SESSION_TOKEN and PANGOLIN_DASHBOARD_URL in profile. Restart
   the Taiga MCP server to use it.` Restart the server and you are done.

The token is the only thing on stdout, so the pipe keeps it off your screen. The session lasts
30 days and renews each time it is used. It ends if you log out of Pangolin or an admin revokes
it. For a project scope, replace `profile` with `project/<name>`.

- `--no-browser` stops the tab opening; copy the printed URL yourself (useful over SSH).
- On a network that reaches Taiga directly, the server logs `Taiga is not behind Pangolin from
  this network; skipping` and logs in to Taiga as usual. Nothing to do.

When it breaks:

- `Pangolin session expired or has no access to this resource; run pangolin-login again`
  (in the MCP server's log): rerun step 1. If it fails again right after a fresh login, your Pangolin account cannot open
  Taiga; ask an admin.
- `device code expired before it was confirmed`: rerun step 1 and confirm sooner.
- `interactive input is unavailable; use --stdin`: you piped into `pangolin-configure`
  without `--stdin`.

### Share Link from an admin

For shared or automation accounts only. A Share Link is a URL a Pangolin admin creates that
opens one protected site without a user login.

1. Ask a Pangolin admin for a Share Link to the Taiga API hostname. (Admin: View as Admin,
   Settings > Share Links, search for the hostname, create the link.)
2. Run this, then paste the link at the hidden prompt:

   ```bash
   dv pangolin-token | dv pangolin-configure profile --stdin
   ```

   Accepted: `https://pangolin.example/s/<token>`, a Taiga URL containing
   `p_token=<id>.<secret>`, or the bare `<id>.<secret>`. A `pangolin-key-<...>` AI Gateway key
   is refused. Organization API keys are not Share Links and will not open Taiga.
3. Success prints `Saved PANGOLIN_RESOURCE_TOKEN in profile.` Restart the server.

`dv pangolin-token --stdin` reads the link from a pipe instead of the prompt.

The scripts are `./scripts/pangolin-login`, `./scripts/pangolin-token`, and
`./scripts/pangolin-configure` when the profile is not loaded.

## Modes

- `full` is the complete tool set (`get_user_story`, `get_user_story_statuses`,
  `list_epics`, and so on). The skills installed under `.claude/skills/` and
  `.agents/skills/` are written against it.
- `workflow` is the smaller tool set, suitable for a user-wide entry.

## Client registration

- **Claude Code in this repository:** the committed `.mcp.json` runs `scripts/taiga-mcp full`
  as server `taiga-py`, overriding any user-level server of the same name. Nothing to do.
- **Codex:** `codex mcp add taiga-py -- "$PWD/scripts/taiga-mcp" full`, run from the
  repository root. `setup-taiga-mcp` does this when `codex` is installed.
- **User-wide Claude entry:**
  `claude mcp add -s user taiga-py -- "$PWD/scripts/taiga-mcp" workflow`.

In a session, call `get_default_session` first and prefer `login()` without explicit
credentials.
