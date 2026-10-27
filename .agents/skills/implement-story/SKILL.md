---
name: implement-story
description: "Implement a user story from the verified Taiga project"
---

Invoke as `$implement-story <story-ref> [base-branch]`. Treat arguments as explicit values supplied by the caller. Discover available Codex tools before use; use `functions.exec` for shell operations, native file tools for reads and edits, and the available Taiga connector for tracker calls. Spawn scoped Codex subagents for delegated work, pass the named skill and exact arguments, then join and verify their results. Resolve the active consumer project and validate repository scripts and status IDs before any mutation. Treat an already explicit user instruction in the current session as authorization for the named target and next steps; ask only when an actual product choice, missing input, or approval gate remains. The commands and status examples below come from the selected You-Thon source; they require that consumer or a verified equivalent. This package has not passed a native runtime smoke.



# Implement Story <skill-arguments>

## Step 0: Parse arguments

`<skill-arguments>` is `<ref> [base-branch]`. The first token is `<ref>` — a **ref number** (what shows in the Taiga UI), not a story_id. Use `<ref>` alone (never the raw `<skill-arguments>`) wherever a step below calls Taiga tooling; passing the base branch through as a second positional argument would make `scripts/taiga-story.sh` misread it as the project ID.

If a second token is present, it is `<base>` — the branch to cut this story's feature branch from. If absent, resolve the repository default:

```bash
gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
```

## Step 1: Fetch story and tasks from Taiga

Use the Taiga MCP tools to gather everything you need.

1. Find the story and its tasks: `scripts/taiga-story.sh <ref> <verified-project-id> --with-tasks` — returns story JSON with `tasks` array included. Extract `id` and `tasks`.
2. If the matching story is already closed/done, inform the user and stop
3. Fetch full story details: `get_user_story(user_story_id=<id from step 1>)`
5. Fetch user story statuses: `get_user_story_statuses(project_id=<verified-project-id>)` — identify the "Ready for test" and "In progress" status IDs
6. Fetch project members: `get_project_members(project_id=<verified-project-id>)` — identify Jon's user ID (bigjonroberts) for reviewer assignment

**Known issue:** `get_task_statuses` is broken in the selected consumer. Use `get_filters_data(project_id=<verified-project-id>, object_type="task")` and resolve task status IDs by exact name; stop if the mapping is missing or ambiguous.

Copy the story subject and each task subject directly into your progress notes list. No other investigation or verification is needed.

## Step 2: Set story to In progress

Update the Taiga story status to "In progress": `update_user_story(user_story_id=<story_id>, kwargs={"status": <in_progress_status_id>})`

## Step 2.5: Set up a working branch

1. Check for an existing branch for this story: `git branch -a --format='%(refname:short)' | grep -E '^(origin/)?feature/.+-<ref>$'` (e.g., `git branch -a --format='%(refname:short)' | grep -E '^(origin/)?feature/.+-399$'`) — anchoring on the `feature/<slug>-<ref>` convention keeps the match to this story's own branch. An unanchored substring match on the bare ref also matches the base branch the clone is sitting on when that name ends in this story's ref (a multi-parent story is cloned onto `epic/<epic-ref>-integration-<ref>`), and it matches longer refs too (`399` matches `feature/x-3991`).
2. If a branch exists, switch to it: `git checkout <branch-name> && git pull` — `<branch-name>` is the match with any leading `origin/` dropped, so that `git checkout` creates the tracking branch.
3. If no branch exists, create one from the branch the story is based on — the repository default branch for a standalone story, the predecessor's branch when the story is part of a stack: `git fetch origin +<base>:refs/remotes/origin/<base> && git checkout -b feature/<short-slug>-<ref> origin/<base>` — a bare `git fetch origin` won't retrieve `<base>` in the shallow single-branch clones `scripts/devcontainer/launch.sh` creates (its `remote.origin.fetch` refspec is restricted to the cloned branch), and fetching `<base>` without the `:refs/remotes/origin/<base>` destination only populates `FETCH_HEAD`, not the `origin/<base>` ref this command consumes.

## Step 3: Implement each task

For each task in order:
1. Mark it as `in_progress` in progress notes
2. Fetch the task details: `get_task(task_id=<id>)` for the description. If it has a `## Gate` section, or turns out mid-work to be impossible to finish before merge (a live step, a human, or another epic), leave it open, note it as `GATED: <task-ref> <reason>`, and move to the next task
3. **If the task description contains a detailed implementation plan (files to change, implementation details, specific code patterns), skip investigation entirely.** Read only the files listed in the plan, then go straight to TDD implementation. Do NOT launch exploratory agents or re-investigate what the plan already explains.
4. If there is **no** implementation plan in the task description, investigate the codebase as needed to understand what to change.
5. Implement the task via TDD
6. Run **only the directly affected test suite(s)** after each task — not `TestAll`. Consult `docs/testing-workflow.md` in the You-Thon consumer for the local-vs-CI policy and file-to-command routing (including Stripe exception rules). On build-relevant PRs, CI gates merges with separate `TestUnit`, `TestIntegration`, and `TestE2E` jobs.
7. Read the relevant `test-results/*.xml` file for pass/fail status. Parse `<testsuite>` attributes for counts and `<failure>` elements for details.
   - Fix every failure, then re-run the affected suite to verify.
8. Commit the changes (tests must pass first)
9. Update the Taiga task status to done: `update_task(task_id=<id>, kwargs={"status": <done_status_id>})`
10. Mark it as `completed` in progress notes
11. Move to the next task

## Step 4: Finish — set story to "Ready for review"

When all tasks are done:

1. Push the branch and create a PR targeting the base branch parsed in Step 0: `gh pr create --base <base> --reviewer bigjonroberts <merge-labels>`. Decide `<merge-labels>` first with the same rule `$finalize-story-pr` Step 3.4 applies, from [`references/merge-side-effects.md`](references/merge-side-effects.md): `--label close-tasks-on-merge` iff no task stays open after merge, plus `--label mark-done-on-merge` iff additionally the plan records no post-merge validation and implementation found none. Remove any `close-tasks-on-merge` / `mark-done-on-merge` tag on the story that no longer applies.
2. Run the Codex review on the new PR following `references/codex-review.md`. A review failure is reported, not fatal — continue with the remaining steps.
3. Update the Taiga story status to **"Ready for test"**: `update_user_story(user_story_id=<story_id>, kwargs={"status": <ready_for_test_status_id>})`
4. Assign the story to Jon for review: `assign_user_story_to_user(user_story_id=<story_id>, user_id=<jon_user_id>)`
5. **Do NOT set the story to "Done"** yourself. Done happens either by Jon after merging the PR, or by taiga-sync at merge when the PR carries `mark-done-on-merge` (or the story keeps that tag).
6. Report what was completed, link the PR, and include the Codex review result (the `REVIEW_POSTED`/`REVIEW_SKIPPED` line).

Remind the user to run `/clear` before invoking `$implement-story` again, to avoid context pollution from the previous story.
