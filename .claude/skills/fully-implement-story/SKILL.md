---
name: fully-implement-story
description: Autonomously implement a story end-to-end with agents — implementation, test review, PR creation, review-thread remediation
argument-hint: "<story-ref> [base-branch] [--resume]"
allowed-tools:
  - Agent
  - Bash(scripts/taiga-story.sh *)
  - Bash(scripts/taiga-comment.sh *)
  - mcp__taiga-py__*
  - Bash(gh *)
  - Bash(git *)
  - Bash(sleep *)
  - Bash(pgrep *)
  - Bash(date *)
  - Bash(cat /tmp/*)
  - Bash(rm -f /tmp/*)
  - Read(//tmp/**)
  - Edit(//tmp/**)
  - Write(//tmp/**)
  - Read
  - Grep
  - Glob
---

# Fully Implement Story $ARGUMENTS

Autonomously implement a story end-to-end: task-by-task implementation with fresh agents, test-quality review, PR creation, rebase check, and review-thread remediation.

## Running Unattended

This skill may run headless (`claude -p`) or interactively; either way it does not ask questions. **There is no human present.** You MUST NOT post questions to the user like "what should I do?" or "should I keep retrying?". The skill defines the decision tree; follow it.

**Every Agent spawn in this skill MUST pass `run_in_background: false`.** This skill runs headless (`claude -p`); if a turn ends while a subagent runs in the background, the CLI can exit and kill the subagent, losing all story work. Foreground spawns keep the turn alive until the agent returns.

The same trap applies to every other way of leaving work in flight: never resume a subagent with `SendMessage` (it runs in the background), never use `Monitor` or a background Bash task to wait for a subagent, and never end a turn with the expectation that a task notification will wake you — in headless mode there is no next turn, so the CLI reports success and exits with the story unfinished. If a foreground spawn returns early or its test run was interrupted, apply the **respawn guard** before spawning a fresh foreground agent for the same task — an early return is not proof the subagent is gone:
1. Check the task lock `/tmp/implement-task-<storyRef>-<taskRef>.lock` (written by implement-task). It holds a heartbeat epoch second that the subagent refreshes as it works — never a pid, because `$PPID` inside a Bash tool call is the long-lived `claude` CLI process shared by every subagent, so its liveness would always succeed and the lock of a crashed agent would pin the orchestrator forever. The subagent is still alive only if the heartbeat is under 15 minutes old:
   ```bash
   lock=/tmp/implement-task-<storyRef>-<taskRef>.lock
   [ -f "$lock" ] && [ $(( $(date +%s) - $(cat "$lock") )) -lt 900 ] && echo alive || echo dead
   ```
   While it reports `alive`, poll every 30 s in a single Bash call (`timeout: 600000`) until the lock is gone or the heartbeat goes stale. If it is still `alive` when the poll window ends, escalate (`escalationReason = "task #<ref> subagent still running after early return"`) — do not respawn.
2. Only when the lock is absent or its heartbeat is stale: `rm -f` any stale lock, then spawn the fresh foreground agent.
3. Additionally refuse to respawn while a test run is in progress in the worktree: check `git status --porcelain` plus `pgrep -x python3` (exact name, never `-f`) for a unittest run.

Decision rules when things go wrong:
- Review threads still unresolved after the Step 4 pass limit: write `phase = "escalated"` with `escalationReason` and STOP.
- Agent blocked by a permission denial or tool error: write `phase = "escalated"` with the specific reason and STOP.
- Uncertainty about proceeding: write `phase = "escalated"` with `escalationReason = "uncertain: <what>"` and STOP. Do not ask.

**Terminal phases** — the state file must end in one of these before you exit:
- `"complete"` — all steps succeeded, PR ready for review
- `"escalated"` — any reason, with populated `escalationReason`

If you would write any other phase (e.g., `"monitoring"`) as your final action, you are doing it wrong — escalate instead.

The phase write is its own Bash call. Never combine it with `pkill` or any other cleanup. A `pkill -f` in the same call self-matches the shell and kills it before the write lands.

## Step 0: Parse arguments

`$ARGUMENTS` is `<ref> [base-branch] [--resume]`. The first token is `<ref>`; use it wherever a step below says `<ref>`. `--resume` (see Step 1's resume check) can appear with or without a base branch — strip it before deciding whether a second token remains.

If a second token remains after stripping `--resume`, it is `<base-branch>` — the branch this story's feature branch is cut from and the PR targets. If it is absent, resolve the repository default instead of assuming `main`:

```bash
gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
```

Every later step uses `<base-branch>`, never `main`.

**An explicit base is not advisory.** A story stack bases each story on the branch of the story before it, so cutting from or targeting the wrong branch puts the predecessor's whole diff into this story's PR. Carry the base you were given through unchanged, pass it as an argument to `/finalize-story-pr` and `/rebase-branch`, and do **not** also patch their commands to compensate — two mechanisms for one fact is how a stack ends up half-targeted.

## Step 1: Validate and initialize

`<ref>` is the first token of `$ARGUMENTS`, as established in Step 0.

**Resume check — do this before anything else in Step 1.** You are resuming when `--resume` is present, or when `/tmp/fully-implement-<ref>.json` already exists with a non-terminal `phase` (an interactive re-invoke). The story is already In progress with work on disk: do not start over, and do not ask — resume.

1. Recover the state. If `/tmp/fully-implement-<ref>.json` exists, read it and do not overwrite it. If it does not (the checkout survived but the state file did not), rebuild it from what is on disk and in Taiga:
   - `featureBranch`: `git branch -a --format='%(refname:short)' | grep -E '^(origin/)?feature/.+-<ref>$' | sed 's#^origin/##' | sort -u` — the anchored match matters for the reasons given in 1c.1; the `sed`/`sort -u` collapse a local branch and its `origin/` counterpart into one name, so expect exactly one line (more than one means two stories' branches share the ref: escalate). The branch may exist only locally.
   - Look up any existing PR once: `gh pr list --head <branch> --state all --json number,baseRefName --jq '.[0]'` (null if none).
   - `baseBranch`: the existing PR's `baseRefName` from the lookup above, if a PR was found — the PR already records the base it was opened against, so this survives a relaunch that passes only `<ref>`. Otherwise, `<base-branch>` from Step 0 (the argument if given, otherwise the `defaultBranchRef` lookup).
   - `prNumber`: the existing PR's `number` from the lookup above (null if none).
   - `tasksCompleted` / `tasksTotal`: from `scripts/taiga-story.sh <ref> 4 --with-tasks` — tasks with `status_extra_info.is_closed == true` are done; each implement-task run closes its task on completion. Open tasks whose description has a `## Gate` section (fetch each with `get_task(task_id=<task_id>)`; the listing omits descriptions) also count as done: they stay open by design (see [`../shared/merge-side-effects.md`](../shared/merge-side-effects.md)).
   - `phase`: `"monitoring"` if a PR exists and is open, else `"implementing"`.
   - Write the block from 1d with those values.
2. Skip 1a's status validation (the story is no longer "Ready") — just fetch the story and its tasks for context.
3. Do 1b as normal.
4. In 1c, check out `featureBranch` **without pulling** — its latest commits may be unpushed. If the branch does not exist at all, nothing was done before the interruption: fall through to a normal Step 1 from 1a (treating an In-progress status as valid).
5. Skip 1d (already handled in 1.) and 1e (the story is already In progress).
6. Jump to the step for the recorded `phase` (see the table in "Resumability" below), continuing at `tasksCompleted`.

### 1a. Fetch and validate the story

1. Find the story and its tasks: `scripts/taiga-story.sh <ref> 4 --with-tasks` — returns story JSON with `tasks` array included. Extract `id` and `tasks`.
2. If the matching story is closed/done, inform the user and stop
3. Fetch full story details: `get_user_story(user_story_id=<id>)` — verify it has the `llm-analyzed` tag
4. If not "Ready" status or not analyzed, inform the user and stop

### 1b. Fetch metadata

1. Fetch story statuses: `get_user_story_statuses(project_id=4)` — identify the `In progress` and `Ready for test` IDs by exact name (project 4 has no "Ready for review" status). Resolve task status IDs with `get_task_statuses(project_id=4)` — `New` and `Closed` by exact name — and keep them as `<new_task_status_id>` and `<closed_task_status_id>` for Step 2. Never hardcode a numeric ID.
2. Fetch project members: `get_project_members(project_id=4)` — identify Jon's user ID (bigjonroberts)

### 1c. Set up branch

1. Check for existing branch: `git branch -a --format='%(refname:short)' | grep -E '^(origin/)?feature/.+-<ref>$' | sed 's#^origin/##' | sort -u` — expect at most one line (the `sed`/`sort -u` collapse a local branch and its `origin/` counterpart); anchoring on the `feature/<slug>-<ref>` convention this skill creates is what keeps the match to this story's own branch. An unanchored substring match on the bare ref also matches the base branch the clone is sitting on when that name ends in this story's ref (a multi-parent story is cloned onto `epic/<epic-ref>-integration-<ref>`), and it matches longer refs too (`274` matches `feature/x-2745`). A base branch is never this story's own branch.
2. If branch exists: `git checkout <branch-name>` (the deduplicated name, so that `git checkout` creates the tracking branch when only `origin/` has it), then `git pull origin <branch-name>` only if `git ls-remote --exit-code --heads origin <branch-name>` succeeds. Never a bare `git pull`: a local-only branch cut from `origin/<base-branch>` tracks the base, and a bare pull would merge base commits into the story branch.
3. If no branch: `git fetch origin +<base-branch>:refs/remotes/origin/<base-branch> && git checkout -b feature/<slug>-<ref> origin/<base-branch>` — fetch the named ref explicitly (not a bare `git fetch origin`, and not `git fetch origin <base-branch>` alone): a bare fetch does not retrieve a stacked predecessor's branch when the clone's `remote.origin.fetch` refspec is restricted, and fetching the ref without a destination only populates `FETCH_HEAD` — the `:refs/remotes/origin/<base-branch>` destination is what creates the `origin/<base-branch>` ref this command consumes.

### 1d. Initialize state file

Skip this step on a resume (see the resume check at the top of Step 1) — only write the initial state block below on a fresh start.

Write the initial state to `/tmp/fully-implement-<ref>.json`:

```json
{
  "storyRef": <ref>,
  "storyId": <story_id>,
  "phase": "implementing",
  "prNumber": null,
  "prCreatedAt": null,
  "featureBranch": "<branch-name>",
  "baseBranch": "<base-branch>",
  "tasksCompleted": 0,
  "openTaskIds": [<ids of tasks whose status_extra_info.is_closed is false>],
  "tasksTotal": <length of openTaskIds>,
  "verifiedTaskIds": [],
  "preSpawnTip": null,
  "testReviewComplete": false,
  "escalated": false,
  "escalationReason": null
}
```

`openTaskIds` (and therefore `tasksTotal`) holds only the tasks still open at the start of this run: tasks Closed by a prior attempt are not re-implemented, so counting them would make the Step 2 completion gate unsatisfiable.

### 1e. Set story to "In progress"

`update_user_story(user_story_id=<id>, kwargs={"status": <in_progress_id>})`

## Step 2: Task-by-task implementation

Loop until all tasks are done:

1. **Record the branch tip, then spawn a fresh `senior-software-developer` agent:**
   - Before spawning: run `git rev-parse <branch-name>` (the current directory is the checkout, as for every other git command in this skill) and store the result in the state file as `preSpawnTip`. Shell variables do not survive across tool calls, so the check below substitutes the literal SHA from the state file.
   - `subagent_type: "senior-software-developer"`
   - `model: "sonnet"` — only this spawn is overridden: the analyzed task supplies a file-level plan and TDD, while the Opus `test-quality-reviewer` and review-thread remediation catch mistakes downstream; finalize and rebase spawns stay on the agent's Opus pin.
   - `run_in_background: false`
   - Prompt: `"Implement the next task for story #<ref> on branch <branch-name>. Follow the implement-task skill instructions with arguments '<ref> <branch-name> <base-branch>'."`

2. **When agent returns**, verify the branch, not the report. Report formatting is known-flaky, so the completion signal is `git rev-list <preSpawnTip>..<branch-name>` (substitute `<preSpawnTip>` from the state file): non-empty output means the task's commit landed, whatever SHA the report cites; empty output means the agent returned before finishing. Docs/config-only tasks still commit, so a landed commit is always expected.
   - If output contains "BLOCKED:" → the agent hit a permission denial or other unrecoverable issue. Escalate: set `phase = "escalated"`, `escalationReason = "agent blocked: <details>"`, tag story with `escalation-needed`, assign to Jon, and **STOP**.
   - If output contains one or more `GATED: <task-ref> <reason>` lines → each named task is left open by design and counts as finished, not failed, so never retry it. Resolve each gated task ref to its task id by fetching the story's task list with `scripts/taiga-story.sh <ref> 4 --with-tasks` (the story ref, not the task ref: the helper resolves stories, issues, and epics only) and matching the task ref against `tasks[].ref`; for every id not already in `verifiedTaskIds`, append it to `verifiedTaskIds`, increment `tasksCompleted`, and write the state file. A gated task lands no commit, so when the report gates a task and claims nothing else, skip the `rev-list` checks below and continue the loop. Carry the `GATED:` lines into the final report. See [`../shared/merge-side-effects.md`](../shared/merge-side-effects.md).
   - If output contains "All tasks complete" **and** the state file has `tasksCompleted == tasksTotal` → break loop, go to Step 2a. If `tasksCompleted < tasksTotal`, the sentinel is not trusted — a worker closed a task in Taiga without landing its commit — so treat it exactly like an empty `rev-list` and enter the recovery path below.
   - `rev-list` non-empty → the work landed. Re-fetch tasks with `scripts/taiga-story.sh <ref> 4 --with-tasks` and find the task with `status_extra_info.is_closed == true` whose id is in `openTaskIds` but not yet in `verifiedTaskIds`:
     - Found → read state file, append its id to `verifiedTaskIds`, increment `tasksCompleted`, write state file, continue loop.
     - None found → the commit landed but Taiga was not updated (the report carries `Task status updated to Closed: ❌`, or omits the `Task status updated to Closed: ✅` line). Do **not** re-spawn — the retry would re-implement the task and double-count it. Close it from here using the task ref named in the report: `update_task(task_id=<task_id>, kwargs={"status": <closed_task_status_id>})`, then `get_task(task_id=<task_id>)` to confirm the status equals `<closed_task_status_id>`. Confirmed → record it as above and continue. Still not Closed → escalate (`phase = "escalated"`, `escalationReason = "update_task failed for task #<task_ref> after its commit landed"`) and **STOP**.
   - `rev-list` empty (or the untrusted sentinel above) → recover once. Identify the stranded task from Taiga rather than the report, which on the sentinel route names no task: re-fetch tasks with `scripts/taiga-story.sh <ref> 4 --with-tasks`; every task with `status_extra_info.is_closed == true` whose id is in `openTaskIds` but not in `verifiedTaskIds` was closed without a landed commit, so reopen each with `update_task(task_id=<task_id>, kwargs={"status": <new_task_status_id>})` so the retry picks it up instead of reporting "All tasks complete". Then record a fresh `preSpawnTip` and re-spawn the task agent. The retry is subject to the same `rev-list` check — an "All tasks complete" reply from the retry counts as a failure (it falls through the `tasksCompleted < tasksTotal` gate above), because the retried task cannot be complete without a landed commit. If the retry also lands nothing, escalate (`phase = "escalated"`, `escalationReason = "task agent returned without a landed commit"`) and **STOP**.

3. Each agent gets a completely fresh context window — no accumulated state from previous tasks.

4. When the loop exits (all tasks done or BLOCKED), proceed to **Step 2a** to verify Taiga task statuses.

## Step 2a: Verify all tasks are Closed in Taiga

Safety net for the known-flaky `implement-task` compliance with its Step 6. Before proceeding to test-quality review, confirm every task on the story is Closed. If any aren't, force-close them now.

1. Re-fetch the story with tasks: `scripts/taiga-story.sh <ref> 4 --with-tasks`
2. For each task in the returned `tasks` array where `status_extra_info.is_closed == false`, except a task reported `GATED:` or whose description has a `## Gate` section (fetch each with `get_task(task_id=<task_id>)`; the `--with-tasks` listing omits descriptions). Those stay open by design — list them in the final report under "Tasks left open by design: #<ref>, #<ref>". Close every other one:
   ```
   update_task(task_id=<task_id>, kwargs={"status": <closed_task_status_id>})
   ```
   Log each one you closed here, in the final orchestrator report under "Tasks auto-closed by safety net: #<ref>, #<ref>".
3. **Verify the updates succeeded** by re-fetching the story with tasks: `scripts/taiga-story.sh <ref> 4 --with-tasks`. Confirm every task other than the gated ones now has `status_extra_info.is_closed == true`. If any task's `update_task` call failed (still open after the update), escalate: set `phase = "escalated"`, `escalationReason = "safety net update_task failed for task #<ref>"`, and **STOP**.
4. Proceed to Step 2b regardless of how many tasks needed closing (as long as all but the gated ones are now confirmed Closed).

Finding open stragglers is routine cleanup, not a failure signal — do NOT escalate merely because tasks were found open. But if `update_task` fails (the task remains open after the update attempt), that IS a failure — escalate. File a separate bug only if the same task keeps reappearing as "open" across multiple runs (which would indicate a deeper issue).

## Step 2b: Test quality review

After all tasks are complete, review the test changes for strategy compliance before creating the PR.

1. **Spawn a fresh `test-quality-reviewer` agent:**
   - `subagent_type: "test-quality-reviewer"`
   - `run_in_background: false`
   - Prompt: `"Review all test changes on branch <branch-name> against the testing strategy. Follow the review-tests skill instructions with arguments '<branch-name>'."`

2. **When agent returns**, check its output:
   - If the agent made changes (moved/deleted/rewritten tests), the changes are already committed on the branch
   - If the agent reports "No test changes to review" or "All test changes comply", proceed
   - If the agent reports issues it could not auto-fix, **treat this as BLOCKED**: set `phase = "escalated"`, `escalationReason = "test-quality-review issues: <summary>"`, tag story with `escalation-needed`, assign to Jon, and **STOP**. Do **not** proceed to Step 3 until the issues are resolved.

3. Update state file: set `testReviewComplete = true`

## Step 3: Finalize PR

1. **Spawn a fresh `senior-software-developer` agent:**
   - `subagent_type: "senior-software-developer"`
   - `run_in_background: false`
   - Prompt: `"Finalize the PR for story #<ref> on branch <branch-name>. Follow the finalize-story-pr skill instructions with arguments '<ref> <branch-name> <base-branch>'."`

2. **When agent returns**, extract PR number from output.

3. Update state file: `phase = "monitoring"`, `prNumber = <number>`, `prCreatedAt = <now>`

## Step 3b: Rebase check

Before monitoring, check if the branch needs a rebase onto the base branch:

1. Run: `gh pr view <prNumber> --json mergeStateStatus -q .mergeStateStatus`
2. If result is `"BEHIND"` or `"DIRTY"`:
   a. Spawn `senior-software-developer` agent to rebase using the `/rebase-branch` skill:
      - `subagent_type: "senior-software-developer"`
      - `run_in_background: false`
      - Prompt: `"Rebase the PR branch onto <base-branch>. Follow the rebase-branch skill instructions with arguments '<prNumber> <base-branch>'."`
   b. When agent returns, check its output:
      - If the rebase was escalated (conflict too complex), set `phase = "escalated"`, `escalationReason = "rebase conflict escalated"`, and **STOP**.
      - If the rebase succeeded, proceed.
   c. **After rebase, the remaining pipeline must re-run**: proceed to Step 4 even if review threads were already checked before the rebase, since new code from the base branch may have drawn new comments.
3. If result is `"CLEAN"` or `"HAS_HOOKS"`, proceed to Step 4.

## Step 4: Review-thread remediation (no CI gate)

This repository has no CI; the suite run in finalize-story-pr is the gate, so do not poll `gh pr checks`.

1. Count unresolved review threads with the GraphQL query from `.claude/skills/pr-comments-resolve/SKILL.md` Step 1 (`reviewThreads(first: 100) { nodes { id isResolved ... } }`, substituting the owner, repo, and `<prNumber>`), filtering for `isResolved == false`.
2. If the count is zero: the PR is STABLE — go to Step 9.
3. Otherwise spawn a fresh `remediation-developer` agent:
   - `subagent_type: "remediation-developer"`
   - `run_in_background: false`
   - Prompt: `"Resolve comments on PR #<prNumber>. Follow the pr-comments-resolve skill instructions with argument '<prNumber>'."`

   When it returns, re-run step 1.
4. Allow at most 3 passes. If threads remain unresolved after the third pass: set `phase = "escalated"`, `escalationReason = "review threads unresolved after 3 passes"`, tag the story `escalation-needed` (re-fetch the story with `get_user_story(user_story_id=<id>)` first and append `["escalation-needed", null]` to its current tags in `update_user_story`), assign the story to Jon, post `gh pr comment <prNumber> --body "Escalating to @bigjonroberts — review threads remain unresolved."`, and **STOP**.

There is no manual-testing phase in this repository: it has no application to exercise.

## Step 9: Success

1. Re-assert the story status "Ready for test" (finalize-story-pr already set it; this guards against a later change): `update_user_story(user_story_id=<id>, kwargs={"status": <ready_for_test_id>})`
2. Assign story to Jon: `assign_user_story_to_user(user_story_id=<id>, user_id=<jon_id>)`
3. Add the PR link to the Taiga story as a comment only if finalize-story-pr's report does not show that it already posted one: `scripts/taiga-comment.sh <id> "PR: <url>"` with `<url>` from `gh pr view <prNumber> --json url -q .url`.
4. Post PR comment:
   ```
   gh pr comment <prNumber> --body "Story implementation complete. Test suite passing, all review threads resolved. Ready for Jon to review."
   ```
5. Only after items 1 to 4 have all succeeded, update state file: `phase = "complete"` — its own Bash call, never combined with any kill. Writing the terminal phase last means an interrupted run resumes at `"monitoring"` and redoes the tracker and PR writes instead of treating them as done.
6. Report success to user with PR link, the base branch this run used, and whether it came from the argument or the `defaultBranchRef` lookup.

## Error handling

- If any agent spawn fails, log the error, set `phase = "escalated"`, and stop.
- The state file at `/tmp/fully-implement-<ref>.json` enables resumability — if the conversation is interrupted, re-invoking the skill can read the state file and continue from the current phase.

## Resumability

The resume check at the top of Step 1 decides whether this run resumes (`--resume` in the arguments, or an existing non-terminal state file) and recovers the state. It then jumps to the step for `phase`:
  - `"implementing"` → Step 2 (or Step 2b if all tasks are done but `testReviewComplete` is false)
  - `"monitoring"` → Step 3b (rebase check), then Step 4

On resume, `<base-branch>` comes from the state file's `baseBranch` key, not from re-resolving Step 0 or assuming `main` — this matters because the `"monitoring"` entry point lands on Step 3b, which spawns `/rebase-branch`. If the state file predates this key (written before this change), fall back to the `defaultBranchRef` lookup from Step 0.
