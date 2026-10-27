# Bug Filing Protocol

Follow this whenever a skill or agent creates a Taiga bug. The rubric lives in
[docs/bug-triage.md](../../../../docs/bug-triage.md); verify the consumer project and read that policy before filing. This file is only the procedure for applying it at filing time.

## Step 1: Resolve IDs

Fetch once per session, in parallel:

- `get_issue_types(project_id=<verified-project-id>)` — the "Bug" type ID
- `get_issue_statuses(project_id=<verified-project-id>)` — the "New" status ID
- `get_issue_severities(project_id=<verified-project-id>)` — Minor / Normal / Important / Critical (Wishlist is not used for bugs)
- `get_issue_priorities(project_id=<verified-project-id>)` — Low / Normal / High

## Step 2: Check for duplicates

`search(project_id=<verified-project-id>, text="<key terms>")`. If a matching open issue exists, do not create a new
one: reference the existing ref in your output and, if you have new evidence, add it as a comment
via `scripts/taiga-comment.sh <id> "<evidence>" --issue`.

## Step 3: Classify per the triage policy

1. **Surface** (exactly one): `devx`, `secrets`, `taiga`, `skills`. Always add the repository
   tag `repo:dev-env-template`; project 4 is shared with other repositories.
2. **Source** (exactly one): `src:manual-test`, `src:pr-review`, `src:agent`, `src:jon`.
   Skills filing on their own behalf use `src:agent`; the manual-testing agent uses
   `src:manual-test`; PR comment resolution uses `src:pr-review`.
3. **Severity**: pick from the severity table. Triage confirms or corrects it.
4. **Priority**: read it off the severity matrix, then apply the modifiers. If you
   deviate from the matrix, say why in the description.

Do not apply the `triaged` tag. Only triage sets it.

## Step 4: Create the issue

```
create_issue(
    project_id=<verified-project-id>,
    subject="<concise title>",
    type_id=<bug_type_id>,
    status_id=<new_status_id>,
    severity_id=<id>,
    priority_id=<id>,
    kwargs={
        "description": "<template below>",
        "tags": [["repo:dev-env-template", null], ["<surface>", null], ["<source>", null]]
    }
)
```

If `create_issue` rejects `tags` in `kwargs`, create the issue first and then
`update_issue(issue_id=<id>, kwargs={"tags": [...]})`.

Description template (fill every line; write "unknown" rather than omitting a line):

```
**Expected:** ...
**Actual:** ...
**Reproduce / observed at:** ...
**Preliminary cause:** ...
**Evidence:** <links, log lines, PR, commit hash>
```

Add any context the filing skill already requires (for example "Discovered during PR #N review"
with file and line) above the template.

## Step 5: Report the ref

Return the created ref number to the caller or user, and follow any skill-specific follow-up
(PR comment, PR description note).
