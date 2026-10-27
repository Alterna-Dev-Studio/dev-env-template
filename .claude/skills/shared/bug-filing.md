# Bug Filing Protocol

Follow this whenever a skill or agent creates a Taiga bug. The rubric lives in
`docs/bug-triage.md`; this file is only the procedure for applying it at filing time.

**Consumer note:** this repository does not install `docs/bug-triage.md` (You-Thon's
product-specific policy). Until a consumer policy exists, use the surface and source tags below,
choose a provisional severity and priority by name from the project's lists based on the bug's
actual impact, and add `Severity and priority are provisional: no consumer triage policy.` to the
description.

## Step 1: Resolve IDs

Fetch once per session, in parallel:

- `get_issue_types(project_id=4)` — the "Bug" type ID
- `get_issue_statuses(project_id=4)` — the "New" status ID
- `get_issue_severities(project_id=4)` — Minor / Normal / Important / Critical
- `get_issue_priorities(project_id=4)` — Low / Normal / High / Urgent

## Step 2: Check for duplicates

`search_project(project_id=4, text="<key terms>")`. If a matching open issue exists, do not create a new
one: reference the existing ref in your output and, if you have new evidence, add it as a comment
via `scripts/taiga-comment.sh <id> "<evidence>" --issue`.

## Step 3: Classify per `docs/bug-triage.md`

1. **Surface** (exactly one): `product`, `devx`, `pipeline`, `ci`.
2. **Source** (exactly one): `src:user`, `src:monitor`, `src:manual-test`, `src:pr-review`,
   `src:agent`, `src:jon`. Skills filing on their own behalf use `src:agent`; the manual-testing
   agent uses `src:manual-test`; PR comment resolution uses `src:pr-review`.
3. **Severity**: pick from the severity table for that surface. This is provisional; the triage
   sweep confirms it.
4. **Priority**: read it off the severity × surface matrix, then apply the modifiers. If you
   deviate from the matrix, say why in the description.

Do not apply the `triaged` tag. Only the triage sweep sets it.

## Step 4: Create the issue

```
create_issue(
    project_id=4,
    subject="<concise title>",
    type_id=<bug_type_id>,
    status_id=<new_status_id>,
    severity_id=<id>,
    priority_id=<id>,
    kwargs={
        "description": "<template below>",
        "tags": [["<surface>", null], ["<source>", null]]
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
**Evidence:** <links, log lines, PR, commit hash, GlitchTip issue id>
```

Add any context the filing skill already requires (for example "Discovered during PR #N review"
with file and line) above the template.

## Step 5: Report the ref

Return the created ref number to the caller or user, and follow any skill-specific follow-up
(PR comment, PR description note).
