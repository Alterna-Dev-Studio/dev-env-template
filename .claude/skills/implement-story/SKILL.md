---
name: implement-story
description: Implement a user story from Taiga project 4
argument-hint: "<story-ref> [base-branch]"
allowed-tools:
  - Bash(scripts/taiga-story.sh *)
  - mcp__taiga-py__get_user_story
  - mcp__taiga-py__update_user_story
  - mcp__taiga-py__assign_user_story_to_user
  - mcp__taiga-py__get_task
  - mcp__taiga-py__update_task
  - mcp__taiga-py__get_user_story_statuses
  - mcp__taiga-py__get_project_members
  - Bash(dotnet run *)
  - Bash(dotnet build *)
  - Bash(dotnet paket *)
  - Bash(dotnet fantomas *)
  - Bash(dotnet tool *)
  - Bash(dotnet reportgenerator *)
  - Bash(git *)
  - Bash(gh *)
  - Bash(scripts/codex-review-pr.sh *)
  - Bash(find *)
  - Bash(xargs grep *)
  - Bash(npm *)
  - Bash(npx *)
  - Bash(docker *)
  - Bash(ls *)
  - Read(//tmp/**)
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - WebFetch(https://www.nuget.org/*)
  - WebFetch(https://github.com/*)
  - WebFetch(https://raw.githubusercontent.com/*)
  - WebFetch(https://learn.microsoft.com/*)
  - WebFetch(https://opentelemetry.io/*)
---

# Implement Story $ARGUMENTS

## Step 0: Parse arguments

`$ARGUMENTS` is `<ref> [base-branch]`. The first token is `<ref>` — a **ref number** (what shows in the Taiga UI), not a story_id. Use `<ref>` alone (never the raw `$ARGUMENTS`) wherever a step below calls Taiga tooling; passing the base branch through as a second positional argument would make `scripts/taiga-story.sh` misread it as the project ID.

If a second token is present, it is `<base>` — the branch to cut this story's feature branch from. If absent, resolve the repository default:

```bash
gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
```

## Step 1: Fetch story and tasks from Taiga

Use the Taiga MCP tools to gather everything you need.

1. Find the story and its tasks: `scripts/taiga-story.sh <ref> 4 --with-tasks` — returns story JSON with `tasks` array included. Extract `id` and `tasks`.
2. If the matching story is already closed/done, inform the user and stop
3. Fetch full story details: `get_user_story(user_story_id=<id from step 1>)`
5. Fetch user story statuses: `get_user_story_statuses(project_id=4)` — identify the "Ready for test" and "In progress" status IDs
6. Fetch project members: `get_project_members(project_id=4)` — identify Jon's user ID (bigjonroberts) for reviewer assignment

**Known issue:** `get_task_statuses` is broken in the MCP server. Resolve task status IDs by exact status name from the `status_extra_info` in the task list data; do not hardcode numeric IDs.

Copy the story subject and each task subject directly into your TodoWrite list. No other investigation or verification is needed.

## Step 2: Set story to In progress

Update the Taiga story status to "In progress": `update_user_story(user_story_id=<story_id>, kwargs={"status": <in_progress_status_id>})`

## Step 2.5: Set up a working branch

1. Check for an existing branch for this story: `git branch -a --format='%(refname:short)' | grep -E '^(origin/)?feature/.+-<ref>$'` (e.g., `git branch -a --format='%(refname:short)' | grep -E '^(origin/)?feature/.+-399$'`) — anchoring on the `feature/<slug>-<ref>` convention keeps the match to this story's own branch. An unanchored substring match on the bare ref also matches the base branch the clone is sitting on when that name ends in this story's ref (a multi-parent story is cloned onto `epic/<epic-ref>-integration-<ref>`), and it matches longer refs too (`399` matches `feature/x-3991`).
2. If a branch exists, switch to it: `git checkout <branch-name> && git pull` — `<branch-name>` is the match with any leading `origin/` dropped, so that `git checkout` creates the tracking branch.
3. If no branch exists, create one from the branch the story is based on — the repository default branch for a standalone story, the predecessor's branch when the story is part of a stack: `git fetch origin +<base>:refs/remotes/origin/<base> && git checkout -b feature/<short-slug>-<ref> origin/<base>` — a bare `git fetch origin` won't retrieve `<base>` in the shallow single-branch clones `scripts/devcontainer/launch.sh` creates (its `remote.origin.fetch` refspec is restricted to the cloned branch), and fetching `<base>` without the `:refs/remotes/origin/<base>` destination only populates `FETCH_HEAD`, not the `origin/<base>` ref this command consumes.

## Step 3: Implement each task

For each task in order:
1. Mark it as `in_progress` in TodoWrite
2. Fetch the task details: `get_task(task_id=<id>)` for the description. If it has a `## Gate` section, or turns out mid-work to be impossible to finish before merge (a live step, a human, or another epic), leave it open, note it as `GATED: <task-ref> <reason>`, and move to the next task
3. **If the task description contains a detailed implementation plan (files to change, implementation details, specific code patterns), skip investigation entirely.** Read only the files listed in the plan, then go straight to TDD implementation. Do NOT launch exploratory agents or re-investigate what the plan already explains.
4. If there is **no** implementation plan in the task description, investigate the codebase as needed to understand what to change.
5. Implement the task via TDD
6. Run the consumer test suite after each task: `python3 -m unittest discover -s tests -v`. Consult [docs/testing-workflow.md](../../../docs/testing-workflow.md) for the local test policy; this repository has no CI gate, so the local run is the gate.
7. Read the unittest output for pass/fail status (there are no `test-results/*.xml` files in this repository).
   - Fix every failure, then re-run the affected suite to verify.
8. Commit the changes (tests must pass first)
9. Update the Taiga task status to done: `update_task(task_id=<id>, kwargs={"status": <done_status_id>})`
10. Mark it as `completed` in TodoWrite
11. Move to the next task

## Step 4: Finish — set story to "Ready for review"

When all tasks are done:

1. Push the branch and create a PR targeting the base branch parsed in Step 0: `gh pr create --base <base> --reviewer bigjonroberts <merge-labels>`. Decide `<merge-labels>` first with the same rule `/finalize-story-pr` Step 3.4 applies, from [`../shared/merge-side-effects.md`](../shared/merge-side-effects.md): `--label close-tasks-on-merge` iff no task stays open after merge, plus `--label mark-done-on-merge` iff additionally the plan records no post-merge validation and implementation found none. Remove any `close-tasks-on-merge` / `mark-done-on-merge` tag on the story that no longer applies.
2. Run the Codex review on the new PR following `.claude/skills/shared/codex-review.md`. A review failure is reported, not fatal — continue with the remaining steps.
3. Update the Taiga story status to **"Ready for test"**: `update_user_story(user_story_id=<story_id>, kwargs={"status": <ready_for_test_status_id>})`
4. Assign the story to Jon for review: `assign_user_story_to_user(user_story_id=<story_id>, user_id=<jon_user_id>)`
5. **Do NOT set the story to "Done"** yourself. Done happens either by Jon after merging the PR, or by taiga-sync at merge when the PR carries `mark-done-on-merge` (or the story keeps that tag).
6. Report what was completed, link the PR, and include the Codex review result (the `REVIEW_POSTED`/`REVIEW_SKIPPED` line).

Remind the user to run `/clear` before invoking `/implement-story` again, to avoid context pollution from the previous story.
