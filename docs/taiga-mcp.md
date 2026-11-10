# Taiga MCP

> How to install the local Taiga MCP server, how `scripts/taiga-mcp` launches it, and how to
> register it with Claude Code and Codex. Overview and Quickstart: [README.md](../README.md).

## Install

`dv taiga-mcp install` (the script is `./scripts/setup-taiga-mcp`) clones
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
`dv taiga-mcp workflow|full [scope]` runs the same launcher from any directory; the client
registrations below keep the script path because MCP clients start it without a shell profile.

- With no scope named and `TAIGA_API_URL`, `TAIGA_USERNAME`, and `TAIGA_PASSWORD` all set in
  the environment, it uses them.
- Otherwise it decrypts the named vault scope (default `profile`) through `scripts/envtool`.
  Scopes are described in [secrets.md](secrets.md).
- The `PANGOLIN_*` variables (see [Taiga behind Pangolin](#taiga-behind-pangolin)) are passed
  through when present and cleared otherwise, so the checkout's legacy `.env` cannot supply
  them.
- Neither client configuration below holds credentials.

Errors name the fix:

- `Install pytaiga-mcp and its virtual environment at ... (run scripts/setup-taiga-mcp)`
  means the checkout or its `.venv` is missing.
- `Missing Taiga settings: set ... in the environment or in vault scope ...` means a
  required variable is empty in the source the launcher chose.

## Taiga behind Pangolin

When Pangolin protects the Taiga API, the server needs a Pangolin credential in addition to
the Taiga login. Obtaining it and storing it are separate scripts, so the secret never has
to appear on the terminal; both are also `dv` commands.

**Your own login (any user).** `scripts/pangolin-login --dashboard-url URL` requests a
device code, prints it with the confirm URL (`URL/auth/login/device?code=…`), opens that
page, and polls until you sign in with your own Pangolin account (password, 2FA or an
external identity provider all work in the browser) and confirm. It prints the resulting
user session token on stdout. `scripts/pangolin-configure SCOPE --session --dashboard-url URL`
stores it as `PANGOLIN_SESSION_TOKEN` with `PANGOLIN_DASHBOARD_URL`:

```bash
dv pangolin-login --dashboard-url https://pangolin.example | dv pangolin-configure profile --session --dashboard-url https://pangolin.example --stdin
```

The session lasts as long as a Pangolin dashboard login (30 days by default, extended on
use) and ends when you log out of Pangolin or an admin revokes it. Access follows your
Pangolin roles, so the resource must allow SSO for your role or user. At startup the server
requests the Taiga root like a browser; when Pangolin redirects to the configured dashboard
it presents the session there and keeps the resource cookie Pangolin sets. A plain `200`
(for example on a LAN with split DNS) means Taiga is not proxied from that network, and the
server logs in directly. `Pangolin session expired or has no access to this resource; run
pangolin-login again` means exactly that: run the pair again. `--no-browser` prints the
confirm URL only.

**Share Link (admin-created, for service accounts).** `scripts/pangolin-token` prints the
admin steps (View as Admin, Settings → Share Links, search the resource picker for the
protected hostname, create a link), optionally opens the dashboard with `--dashboard-url URL`,
reads the pasted link with hidden input, validates it, and prints only the token on stdout.
`scripts/pangolin-configure SCOPE` without `--session` saves it as `PANGOLIN_RESOURCE_TOKEN`:

```bash
dv pangolin-token --dashboard-url https://pangolin.example | dv pangolin-configure profile --stdin
```

A dashboard `https://…/s/<token>` link, a resource URL with `p_token=ID.token`, or a bare
`ID.token` value is accepted; organization API keys and `pangolin-key-…` AI Gateway keys are
rejected because they cannot authorize a protected HTTP resource.

Storing one kind of credential removes the other, so a scope holds either a session or a
Share Link. `pangolin-configure SCOPE --clear` removes all Pangolin variables. Both
configure modes accept `--stdin`. Restart the MCP server after changing a scope.

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
