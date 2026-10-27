---
name: implement-task
description: Implement the next incomplete task from a story — single task, fresh context
argument-hint: "<story-ref> <branch-name> [base-branch]"
allowed-tools:
  - Bash(scripts/taiga-story.sh *)
  - mcp__taiga-py__get_user_story
  - mcp__taiga-py__update_user_story
  - mcp__taiga-py__get_task
  - mcp__taiga-py__update_task
  - mcp__taiga-py__get_task_statuses
  - Bash(python3 -m unittest *)
  - Bash(timeout 590 python3 -m unittest *)
  - Bash(bash -n *)
  - Bash(shellcheck *)
  - Bash(date *)
  - Bash(rm -f /tmp/implement-task-*)
  - Bash(git *)
  - Bash(gh *)
  - Bash(find *)
  - Bash(xargs grep *)
  - Bash(ls *)
  - Read(//tmp/**)
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - WebFetch(https://github.com/*)
  - WebFetch(https://raw.githubusercontent.com/*)
---

# Implement Task — Story #$ARGUMENTS

Implement the next incomplete task from a story. This skill handles exactly one task, then returns. The orchestrator calls it repeatedly with fresh agents until all tasks are done.

## Step 1: Set up the branch

Parse arguments from `$ARGUMENTS`:
- First word: story ref number (e.g., `399`)
- Second word: branch name (e.g., `feature/my-feature-399`)
- Third word (optional): `<base>` — the branch this story's feature branch was cut from. `/fully-implement-story` always passes this when it spawns this skill. If absent (a direct/manual invocation), resolve the repository default:
  ```bash
  gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
  ```

Check out the branch:
1. `git checkout <branch-name> && git pull`
2. If the branch doesn't exist locally: `git fetch origin <branch-name> && git checkout <branch-name>`
3. If it doesn't exist at all: `git fetch origin +<base>:refs/remotes/origin/<base> && git checkout -b <branch-name> origin/<base>` — this fallback only fires if the branch-creation step in the calling skill (`/fully-implement-story` or `/implement-story`) was skipped or failed, since normally the branch already exists by the time this skill runs.

Then write the task lock as its own Bash call so the orchestrator can tell you are still alive:
```bash
date +%s > /tmp/implement-task-<story-ref>-<task-ref>.lock
```
The lock carries a heartbeat timestamp, not a pid. `$PPID` inside a Bash tool call is the long-lived `claude` CLI process shared by every subagent in the session, so its liveness says nothing about whether *this* agent is still working. Refresh the heartbeat with the same command at the start of each later step and immediately before and after any long-running command (test runs, builds) — the orchestrator treats a heartbeat older than 15 minutes as a dead agent and respawns. Write the lock as soon as the task ref is known (after Step 2 if it is not known yet).

## Step 2: Fetch story and find next task

1. Find the story and its tasks: `scripts/taiga-story.sh <story-ref> 4 --with-tasks` — returns story JSON with `tasks` array included. Extract `id` and `tasks`.
2. Fetch full story details: `get_user_story(user_story_id=<id>)` for context
3. Find the first task whose status is NOT done (`status_extra_info.is_closed == false`) and whose description has no `## Gate` section (fetch each candidate with `get_task(task_id=<id>)` to check). If no such task remains, report **"All tasks complete"**, add one `GATED: <task-ref> <reason>` line for each open task that has a `## Gate` section, apply the tag removal from "Gated tasks" below if any are listed, and return.
4. Fetch full task details: `get_task(task_id=<id>)` for the description/implementation plan

### Gated tasks

A task gated on something outside this branch (a live step, a human, or another epic) stays open after the story's PR merges. If the task you picked turns out mid-work to be impossible to finish for that reason, do not implement or close it:

1. Record why on the task itself, so later runs skip it: `update_task(task_id=<id>, kwargs={"description": "<current description>\n\n## Gate\n\n<what it waits for>"})`.
2. Remove the `close-tasks-on-merge` and `mark-done-on-merge` tags from the story if present: re-fetch it with `get_user_story(user_story_id=<story-id>)`, then `update_user_story(user_story_id=<story-id>, kwargs={"tags": <every current tag except those two>})`. An open task means neither signal holds (see [`../shared/merge-side-effects.md`](../shared/merge-side-effects.md)).
3. Discard any uncommitted work for the task, skip Steps 3–6, and report `GATED: <task-ref> <reason>` in Step 7 in place of the commit SHA and Taiga status lines. The orchestrator counts a gated task as finished, not failed.

**NEVER call MCP tools (e.g., `list_tasks`) directly to find tasks. ALWAYS use `scripts/taiga-story.sh <story-ref> 4 --with-tasks` — it hardcodes the correct project_id.**

The Taiga project for this repository is 4 (see AGENTS.md). Resolve task status IDs once per run by exact name from `get_task_statuses(project_id=4)` — `New`, `In progress`, `Closed` — and cross-check with `status_extra_info.name` / `status_extra_info.is_closed` in the `taiga-story.sh` listing. Never hardcode a numeric ID. `<closed_task_status_id>` below is the ID whose name is exactly `Closed`.

## Step 3: Implement the task

1. **If the task description contains a detailed implementation plan** (files to change, implementation details, specific code patterns), skip investigation entirely. Read only the files listed in the plan, then go straight to TDD.
2. **If there is no implementation plan**, investigate the codebase as needed.
3. Implement via TDD:
   a. Write a failing test that correctly validates the desired functionality
   b. Run the test to confirm it fails as expected
   c. Write ONLY enough code to make the failing test pass
   d. Run the test to confirm success
   e. Refactor if needed while keeping tests green

## Step 4: Run tests

Run the consumer suite: `timeout 590 python3 -m unittest discover -s tests -v; echo "exit=$?"` in the foreground with the Bash tool `timeout: 600000`. Run `bash -n` and `shellcheck` on any changed Bash file. See [docs/testing-workflow.md](../../../docs/testing-workflow.md); this repository has no CI gate, so this run is the gate.

Refresh the task-lock heartbeat immediately before and after the run, each as its own Bash call, so a long suite is not mistaken for a dead agent:
```bash
date +%s > /tmp/implement-task-<story-ref>-<task-ref>.lock
```

Run the suite in the foreground with an explicit exit-code capture:
```bash
timeout 590 python3 -m unittest discover -s tests -v; echo "exit=$?"
```
Never wait with a `kill -0 $(pgrep -f ...)` loop — `pgrep -f` matches the loop's own shell and never exits (see `AGENTS.md` "Process Hygiene").

Read the unittest output for pass/fail; there are no JUnit XML result files. Fix every failure, then re-run the suite to verify.

**If you believe a failure is unrelated to your changes**, you MUST follow the Test Failure Triage Protocol in `.claude/skills/shared/test-failure-triage.md` before dismissing it.

## Step 5: Commit

Stage and commit changes with a descriptive message referencing the task:

```
git commit -m "<description of what was implemented>

Co-Authored-By: <your session's model> <noreply@anthropic.com>"
```
Use your own session's attribution trailer — see `.claude/skills/shared/commit-attribution.md`.

Do NOT push — the orchestrator handles pushing after all tasks are done.

## Step 6: Mark task done

**This step is MANDATORY — do not skip it. The orchestrator checks your report for the Taiga status line and treats its absence as a failure.**

1. Update the Taiga task status to done:
   ```
   update_task(task_id=<id>, kwargs={"status": <closed_task_status_id>})
   ```
   - `<id>` is the task's `id` field (NOT the `ref`) from Step 2
   - `<closed_task_status_id>` is the `Closed` status resolved by name in Step 2

2. **Verify the call succeeded** by re-fetching the task:
   ```
   get_task(task_id=<id>)
   ```
   Confirm the returned `status` equals `<closed_task_status_id>`. If it isn't, the previous call failed — retry once. If it still does not equal `<closed_task_status_id>` after the retry, proceed to Step 7 and report the failure (do NOT skip the report — the orchestrator needs the `❌` line to detect the failure).

3. **Your Step 7 report MUST include a line in this exact format:**
   ```
   Task status updated to Closed: ✅
   ```
   Reports without this line are treated as incomplete by the orchestrator.

## Step 7: Report

Before returning — including when reporting BLOCKED — remove the task lock as its own Bash call:
```bash
rm -f /tmp/implement-task-<story-ref>-<task-ref>.lock
```

Return a clear summary. **The report MUST include all of the following lines:**

- Which task was implemented (subject and ref)
- Commit SHA of the implementation
- What files were changed
- Test results (pass/fail counts, or "N/A" for docs/config-only changes)
- **`Task status updated to Closed: ✅`** — or `❌` with a specific error if Step 6's update_task call or its verification failed
- Whether there are remaining tasks (and how many)

A `GATED: <task-ref> <reason>` report replaces the commit SHA, files, test results, and "Task status updated" lines for that task.

Omitting the "Task status updated" line (outside a `GATED:` report) or reporting `❌` indicates an incomplete run — the orchestrator will treat the task as not-implemented and may retry.

## Handling tool permission denials

If a tool call (Edit, Write, Bash, etc.) is blocked by a permission denial:
1. Do NOT ask the user to approve permissions — this skill runs in headless devcontainers where no human can respond.
2. If the denied tool is listed in this skill's `allowed-tools` frontmatter, try an alternative approach (e.g., use `Write` instead of `Edit`, or use a different `Bash` command pattern).
3. If you cannot complete the task after 2 alternative attempts, report the failure clearly: **"BLOCKED: Repeated permission denials on [tool]. Cannot complete task."** and exit. Do NOT mark the task as done.

## What this skill does NOT do

- Does NOT push to remote (orchestrator does this)
- Does NOT create PRs (orchestrator does this via finalize-story-pr)
- Does NOT update story status (orchestrator does this)
- Does NOT implement or close a gated task (see "Gated tasks" in Step 2)
- Does NOT implement multiple tasks — exactly one per invocation
