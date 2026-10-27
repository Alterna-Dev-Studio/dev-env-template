---
name: finalize-story-pr
description: Push a story branch, run tests, create PR, and update Taiga status
---

# Codex runtime and scope

Invoke as `$finalize-story-pr <arguments>`. Treat the invocation text as the arguments shown below. This package is patched for the dev-env-template consumer: Taiga project 4 with statuses resolved by name, the Python `unittest` suite, and no CI gate. Read the consumer's `AGENTS.md` and referenced policy documents first.

Discover the available Taiga tools by operation. Before a tracker write, verify the host and project against the consumer configuration, resolve `<verified-project-id>` live (or verify `TAIGA_PROJECT_ID` where used), and resolve status/member IDs by name. A source `mcp__taiga-py__*` operation denotes the equivalent connected Codex tool, not a guaranteed tool identifier. Stop and report a missing connection, authentication, project guard, script, or required permission. Use Codex search/read/patch tools for file inspection and edits, shell execution for Git, GitHub CLI and consumer scripts, and the available web tool when needed. Source `allowed-tools` grants do not carry over.

Read package-local references before the steps that cite them: [codex-review.md](references/codex-review.md), [merge-side-effects.md](references/merge-side-effects.md), [test-failure-triage.md](references/test-failure-triage.md).

# Finalize Story PR — <arguments>

Push a story branch, run tests, create a PR, and update Taiga. This skill runs after all tasks have been implemented and committed locally.

## Step 1: Verify branch state

Parse arguments from `<arguments>`:
- First word: story ref number
- Second word: branch name
- Third word (optional): the base branch this PR targets. `$fully-implement-story` passes its own `[base-branch]` straight through when it has one. When the third word is absent, resolve the repository default rather than assuming `main`:
  ```bash
  gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
  ```
  Call the result `<base-branch>` for the rest of this skill. Getting it wrong silently attributes the predecessor branch's commits to this story.

1. Verify we're on the correct branch: `git branch --show-current`
2. If not, check it out: `git checkout <branch-name>`
3. Verify there are commits ahead of the PR's base:
   ```bash
   git fetch -q origin +<base-branch>:refs/remotes/origin/<base-branch>
   git log origin/<base-branch>..<branch-name> --oneline
   ```
   `<base-branch>` is the third argument or the resolved default — never the local `main`. The `origin/` prefix matters: a checkout's local branch is routinely behind its `origin/` counterpart, and measuring against the local ref would report every commit merged since that local ref last moved.
   - If no commits, report "No changes to push" and stop

## Step 1b: Test quality review

Before running tests, review all test changes on this branch for testing strategy compliance using the shared review skill.

Follow the `$review-tests` skill instructions with argument `<branch-name>`. Read `.agents/skills/review-tests/SKILL.md` and execute the steps in this conversation — no subagent spawn needed here.

## Step 2: Run tests

1. Run `timeout 590 python3 -m unittest discover -s tests -v` in the foreground. Read the unittest output; fix every failure before proceeding.
2. Run `bash -n <file>` and `shellcheck <file>` on each Bash file changed on the branch (`git diff --name-only origin/<base-branch>...HEAD`).
3. If you believe a failure is unrelated to the story's changes, follow the Test Failure Triage Protocol in `references/test-failure-triage.md` before dismissing it. This repository has no CI gate; this local run is the gate (`docs/testing-workflow.md`).

## Step 3: Push and create PR

1. Push the branch: `git push -u origin <branch-name>`
2. Fetch the story details for the PR title:
   - `get_user_story_by_ref(project_id=<verified-project-id>, ref=<story-ref>)` — returns full story directly (subject, description, status, etc.). Extract and save the story `id` — it is needed for `taiga-comment.sh` and `update_user_story` calls in Steps 3 and 4.
3. Extract story context from the `description` field for the PR body:
   a. **Overview**: Look for a `### Overview` section in the description. Extract the text between `### Overview` and the next `###` heading (2-3 sentences max). If no `### Overview` exists, look for text after a `---` separator and use the first paragraph. If neither exists, use the story subject as a one-line summary.
   b. **Acceptance Criteria**: Look for a `## Acceptance Criteria` section. Extract the bullet list verbatim. If not present, omit this subsection entirely.
   c. **Scope Boundaries**: Look for a `### What Does NOT Need to Change` or `## Scope Boundaries` section. Summarize to 1-2 lines. If not present, omit this subsection entirely.
   d. **Architecture notes**: Look for a `### Architecture` or `## Architecture Notes` section in the description or implementation plan. Summarize which layers changed (e.g. "Server, Shared, Client") in 1-2 lines. If not present, omit this subsection entirely.
   e. Keep the total Story Context section under ~800 characters. Never include empty subsections — if a section is missing from the description, omit it from the PR body.
4. Decide the merge side effects, applying the deciding rule in [`references/merge-side-effects.md`](references/merge-side-effects.md) to the story as implemented:
   a. Re-fetch the tasks: `scripts/taiga-story.sh <story-ref> <verified-project-id> --with-tasks`. A task still open stays open after merge when it has a `## Gate` section (`get_task(task_id=<id>)`), the plan's `### Merge Side Effects` section lists it, or an implementer reported it `GATED:`.
   b. `close-tasks-on-merge` applies iff no task stays open after merge. `mark-done-on-merge` applies iff `close-tasks-on-merge` applies **and** the plan's `### Merge Side Effects` section says `Post-merge validation: none` **and** implementation found no post-merge validation the plan missed. A plan without that section gets no `mark-done-on-merge`.
   c. Build `<merge-labels>`: `--label close-tasks-on-merge` and/or `--label mark-done-on-merge` for each signal that applies, or nothing.
   d. If the story carries a `close-tasks-on-merge` or `mark-done-on-merge` tag that no longer applies, remove it with `update_user_story`, sending the story's full current tag list minus that tag. A stale tag would fire at merge on its own.
5. Create PR:
   ```bash
   gh pr create --base <base-branch> --reviewer bigjonroberts <merge-labels> --title "#<ref>: <story subject>" --body "$(cat <<'EOF'
   ## Story Context

   **[#<ref>](https://taiga.unclejons.casa/project/alterna-dev-studio/us/<ref>): <subject>**

   <extracted overview, 2-3 sentences max>

   **Acceptance criteria:**
   <extracted bullet list from story — if the story has no Acceptance Criteria section, DELETE THIS HEADING AND THE FOLLOWING LINE FROM THE PR BODY ENTIRELY>

   **Scope:** <summarized scope boundaries — if the story has no Scope Boundaries section, DELETE THIS ENTIRE LINE FROM THE PR BODY>

   **Architecture:** <summary of which layers changed — if no architecture section exists in the story, DELETE THIS ENTIRE LINE FROM THE PR BODY>

   ## Tasks completed

   - <task 1 subject>
   - <task 2 subject>
   - ...

   ## Test plan

   - [ ] `python3 -m unittest discover -s tests -v` passes locally
   - [ ] `bash -n` and `shellcheck` clean on changed Bash
   - [ ] Manual review of changes

   ## Known pre-existing failures

   <If any test failures were verified as pre-existing via the Test Failure Triage Protocol and bugs were filed, list them here: "- #NNN — <test name>". If none, omit this section entirely.>

   🤖 Generated with Codex
   EOF
   )"
   ```

6. Add PR link to Taiga story as a comment, using the URL GitHub reports (`gh pr view <pr_number> --json url -q .url`):
   `scripts/taiga-comment.sh <id> "PR: <pr_url>"`
7. Run the Codex review on the new PR following `references/codex-review.md`. A review failure is reported, not fatal — continue with the remaining steps.

## Step 4: Update Taiga

1. Fetch story statuses: `get_user_story_statuses(project_id=<verified-project-id>)` — find "Ready for test" status ID
2. Fetch project members: `get_project_members(project_id=<verified-project-id>)` — find Jon's user ID (bigjonroberts)
3. Update story status to "Ready for test": `update_user_story(user_story_id=<id>, kwargs={"status": <ready_for_test_id>})`
4. Assign story to Jon: `assign_user_story_to_user(user_story_id=<id>, user_id=<jon_user_id>)`

**Do NOT set the story to "Done"** yourself. Merge automation (taiga-sync) is not installed in this repository, so the `mark-done-on-merge` label and tag are recorded for planning only; Done is set by Jon after merging the PR.

## Step 5: Report

Return:
- PR number and URL
- Which base branch the PR targets
- Test results summary (pass/fail/skip counts)
- Codex review result (the `REVIEW_POSTED`/`REVIEW_SKIPPED` line)
- Merge side effects: which labels the PR carries, which tags were removed, and why
- Story status update confirmation

## What this skill does NOT do

- Does NOT implement any tasks (implement-task does that)
- Does NOT monitor the PR after creation (orchestrator does that)
- Does NOT mark the story as "Done"
