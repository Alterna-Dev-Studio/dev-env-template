# Bug Triage

How bugs in this repository get a severity, a priority, and tags. Bugs live in Taiga project 4
(Alterna Dev Studio, slug `alterna-dev-studio`), which other repositories share, so every bug
for this repository carries the `dev-env-template` tag. The filing procedure for skills is
[.claude/skills/shared/bug-filing.md](../.claude/skills/shared/bug-filing.md).

## Principles

- **Severity is impact. Priority is scheduling.** Severity says what the bug does and never
  changes because of deadlines. Priority says when we fix it and is derived from severity.
- **Default, then override with a reason.** Any override, or later change to severity or
  priority, needs a comment on the issue explaining why.
- **Triaged is a checkable state.** A bug is triaged when every field and tag below is set.

## Taiga fields

| Field | Values in project 4 (low to high) |
|---|---|
| Type | Bug (this document applies), Question, Enhancement |
| Severity | Wishlist (not used for bugs), Minor, Normal, Important, Critical |
| Priority | Low, Normal, High |
| Status | New, In progress, Ready for test, Closed, Needs Info, Rejected, Postponed |

Resolve IDs by exact name at run time and never hardcode them: `get_issue_types`,
`get_issue_severities`, `get_issue_priorities`, and `get_issue_statuses` with `project_id=4`.

## Tags

Spell tags exactly as below.

- **Repository** (required): `dev-env-template`.
- **Surface** (exactly one):

  | Tag | Covers |
  |---|---|
  | `devx` | Shell startup and setup: `profile.sh`, `shell/`, PATH, `scripts/setup`, the devcontainer example, the test suite |
  | `secrets` | SOPS vault and credentials: `scripts/envtool`, encrypted profiles, `.envrc` loading, `--migrate-bashrc`, and any secret leak wherever it happens |
  | `taiga` | `scripts/taiga-story.sh`, `scripts/taiga-comment.sh`, `scripts/taiga-mcp`, `scripts/setup-taiga-mcp`, `.mcp.json` |
  | `skills` | Installed skills under `.claude/skills/` and `.agents/skills/`, and `scripts/codex-review-pr.sh` |

  A documentation bug takes the surface of what the document describes.
- **Source** (exactly one): `src:manual-test`, `src:pr-review` (found while reviewing or
  resolving a PR), `src:agent` (found by an agent doing other work), `src:jon`.
- **State**: `triaged` (set only by triage), `pre-existing-failure` (a test failure verified on
  the base branch).

## Severity

| Level | What it looks like here |
|---|---|
| **Critical** | A secret value printed, logged, committed, or written to disk in plaintext; the age identity, decrypted JSON, `.env`, or `.env.local` can be committed. The vault or a startup file is lost or corrupted. New Bash shells exit, hang, or fail to start. |
| **Important** | `scripts/setup` duplicates lines on re-run or fails on a clean clone. PATH gains duplicates or `~/.local/bin` is not first. Credentials do not load. A Taiga helper or the MCP launcher fails with valid credentials. A skill writes to the wrong Taiga project or sets a wrong status. Tests are red on `main`. |
| **Normal** | Degraded with a known workaround. A flaky test. Docs wrong in a way that costs time. |
| **Minor** | Cosmetic output, typos, stale hints. No functional impact. |

Any confirmed secret exposure is Critical. A request for new behavior is an Enhancement, not a
bug.

## Priority

| Severity | Priority |
|---|---|
| Critical | High, fixed the same day |
| Important | High |
| Normal | Normal |
| Minor | Low |

Modifiers: one level up (at most High) when the bug blocks a story in flight and the issue says
so; one level down when it only reproduces on an unusual setup with a documented workaround.

## Filing

Set severity, derived priority, and the repository, surface, and source tags at creation, and
use this description template. Never apply `triaged` when filing.

```
**Expected:** ...
**Actual:** ...
**Reproduce / observed at:** ...
**Preliminary cause:** ... (or "unknown")
**Evidence:** links, log lines, PR, commit hash
```

## Triage

Jon, or an agent asked to triage, takes open Bug issues in project 4 tagged `dev-env-template`
and not `triaged`, in ref order:

1. If expected, actual, or reproduce is missing, set Needs Info with a comment saying what is
   missing. After 14 days without a reply, move it to Rejected.
2. Search for duplicates (`search_project(project_id=4, text=<token>)`, one or two distinctive
   tokens at a time). A duplicate goes to Rejected with `Duplicate of #<ref>`. A bug a merged PR
   claims (ref in the title, or a `Fixes`/`Closes`/`Resolves #<ref>` line) goes to Closed.
3. Confirm the surface, source, and severity, derive priority, and write them with the `triaged`
   tag and a comment stating the choice and any override.

Fix work takes triaged bugs by priority, then severity (both descending), then ref.
