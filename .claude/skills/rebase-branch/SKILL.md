---
name: rebase-branch
description: Rebase a PR branch onto a target branch, resolve conflicts using story/issue/epic context, run tests, and force-push. Escalates to Jon when stuck.
argument-hint: "<PR-number> [target-branch]"
allowed-tools:
  - mcp__taiga-py__get_user_story_by_ref
  - mcp__taiga-py__get_user_story
  - mcp__taiga-py__get_epic
  - mcp__taiga-py__list_user_stories
  - mcp__taiga-py__update_user_story
  - mcp__taiga-py__assign_user_story_to_user
  - mcp__taiga-py__get_user_story_statuses
  - mcp__taiga-py__get_issue_by_ref
  - mcp__taiga-py__get_issue
  - mcp__taiga-py__update_issue
  - mcp__taiga-py__assign_issue_to_user
  - mcp__taiga-py__get_issue_statuses
  - mcp__taiga-py__get_project_members
  - Bash(python3 -m unittest *)
  - Bash(timeout 590 python3 -m unittest *)
  - Bash(python3 -m py_compile *)
  - Bash(bash -n *)
  - Bash(shellcheck *)
  - Bash(scripts/taiga-story.sh *)
  - Bash(git *)
  - Bash(gh *)
  - Read(//tmp/**)
  - Read
  - Edit
  - Write
  - Grep
  - Glob
---

# Rebase Branch — PR #$ARGUMENTS

Rebase a PR branch onto a target branch, resolve merge conflicts intelligently using story/issue and epic context, verify with tests, and force-push. Escalates to Jon when a conflict resolution requires human judgment.

## Step 1: Parse arguments and gather PR context

Parse `$ARGUMENTS`:
- First word: PR number
- Second word (optional): target branch. Do not fall back to `main` without checking. When the caller omits this argument, use the PR's own base instead:
  ```bash
  gh pr view <PR> --json baseRefName -q .baseRefName
  ```
  Step 1's `gh pr view` call below already fetches `baseRefName`, so this is the same value read from that response, not a second lookup. A stacked PR targets a `feature/*` branch, not `main` — rebasing it onto `main` would replay its commits over every sibling it was stacked behind, turning a two-file conflict into the whole stack's diff. When `/fully-implement-story` invokes this skill it always passes the base explicitly, so this fallback only fires on direct invocations.

Gather information in parallel:

1. **PR details**: `gh pr view <PR> --json title,body,headRefName,baseRefName,state,number,url`
2. **Owner/repo**: `gh repo view --json nameWithOwner -q .nameWithOwner`
3. **Current branch**: `git branch --show-current`

If the PR is closed or merged, report and stop.

## Step 2: Identify the associated Taiga item

Look for a Taiga numeric ref in the PR title, body, or branch name. Accept any of these patterns and extract the numeric portion as `<ref>`:

- `#NNN` anywhere in the PR title, body, or branch name
- Branch names matching `fix/<short-slug>-<ref>` (e.g., `fix/login-timeout-123`)
- Branch names matching `fix/<ref>` (e.g., `fix/123`)
- Title/body text like `bug <ref>` (e.g., `bug 123`)

Use the first confident match you find. If a ref is found:

1. First try a story lookup: `get_user_story_by_ref(project_id=4, ref=<ref>, verbosity="full")`.
   - If it returns a result, proceed as normal: fetch the epic if linked via `get_epic(epic_id=<epic_id>, verbosity="full")`. Extract and save the story `id`, subject, description, and epic description (if any). Record `taigaType = "story"`, `taigaId = <story id>`, and save the current `tags` list.
2. If the story lookup fails (no result or error), try an issue lookup: `get_issue_by_ref(project_id=4, ref=<ref>, verbosity="full")`.
   - If it returns a result, save the issue `id`, subject, and description. Record `taigaType = "issue"`, `taigaId = <issue id>`, and save the current `tags` list. Issues don’t have epics, so skip the epic lookup.
3. If neither lookup returns a result, proceed without Taiga context (resolve conflicts on code merit alone).

The saved subject + description serve as your **resolution context** regardless of type — they tell you what the PR is trying to accomplish so you can make informed conflict resolution decisions. The `taigaType` and `taigaId` will be needed later in Step 5c for escalation updates.

## Step 3: Prepare for rebase

1. Fetch the latest from origin, including the target branch explicitly:
   ```
   git fetch origin
   git fetch origin +<target-branch>:refs/remotes/origin/<target-branch>
   ```
   The second fetch is explicit so that `origin/<target-branch>` exists even when the clone's `remote.origin.fetch` refspec is restricted to the checked-out branch. Fetching `<target-branch>` without the `:refs/remotes/origin/<target-branch>` destination would only populate `FETCH_HEAD`, not the `origin/<target-branch>` ref every command below consumes.

2. Check out the PR branch (if not already on it):
   ```
   git checkout <head-branch>
   git pull origin <head-branch>
   ```

3. Preview what will happen — identify files that will conflict. Use `origin/<target-branch>` throughout, not the bare local name: when the omitted target resolves to a stacked PR's feature branch, a normal checkout has no local ref for it, only the fetched remote-tracking one from step 1.
   ```
   git diff --name-only <head-branch>...origin/<target-branch>
   ```
   This shows files changed on the target since the branches diverged. Cross-reference with files changed on the PR branch:
   ```
   git diff --name-only $(git merge-base <head-branch> origin/<target-branch>)..<head-branch>
   ```
   Files appearing in both lists are **potential conflict zones**. Note them.

4. Record the pre-rebase HEAD for recovery:
   ```
   git rev-parse HEAD
   ```
   Save this SHA — if the rebase goes badly, `git rebase --abort` restores to this state.

## Step 4: Start the rebase

```
git rebase origin/<target-branch>
```

If the rebase completes with no conflicts, skip to **Step 6**.

If the rebase stops with conflicts, proceed to **Step 5**.

## Step 5: Resolve conflicts

For each conflict round (the rebase may stop multiple times):

### 5a. Identify conflicting files

```
git diff --name-only --diff-filter=U
```

### 5b. For each conflicting file, analyze and resolve

1. **Read the file** to see the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).

2. **Understand both sides in a rebase conflict:**
   - **Upstream (HEAD)** (above `=======`, from `<<<<<<< HEAD`): the target branch state you're rebasing onto — what was merged since the PR branched off
   - **Rebased commit (PR branch)** (below `=======`, from `>>>>>>> <commit>`): the commit from the PR branch currently being replayed — what this story intended

3. **Determine resolution strategy** using this priority order:

   **a. Additive / non-overlapping changes** (most common for this codebase):
   Both sides add new content (e.g., new aliases in `shell/aliases.sh`, new PATH entries in `shell/paths.sh`, new test methods in `tests/`). **Keep both.** Combine the additions, maintaining proper ordering (logical grouping for aliases and paths, one test per contract).

   **b. Epic boundary rules** (if epic context is available):
   The epic description defines which story "owns" which code. If the conflict involves code owned by a specific story, that story's version wins. Example: if the epic says "#829 owns the `envtool` loader in `profile.sh`", and this PR is for #713, use #829's version of that loader.

   **c. Semantic analysis** (when both sides modify the same code):
   - If the target branch refactored/renamed something and the PR branch used the old name, **adopt the target's refactoring** and update the PR's usage.
   - If the PR branch intentionally changed behavior that the target also changed differently, this requires judgment — apply the **escalation check** below.

   **d. Formatting / whitespace conflicts**:
   Accept whichever side has more context, then re-run `shellcheck` on the file; there is no formatter.

4. **Escalation check** — escalate if ANY of these are true:
   - Both sides intentionally changed the same logic/behavior in different ways
   - The resolution would change the functional intent of either story
   - You're uncertain which side is correct after reading both stories
   - The conflict involves shared types, API contracts, or database schema
   - More than 10 files have non-trivial conflicts in a single rebase round

   If escalation is needed, proceed to **Step 5c** (Escalate).

5. **Apply the resolution**: Edit the file to remove conflict markers and produce the correct merged content. Do NOT leave any conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) in the file.

6. **Stage the resolved file**: `git add <file>`

### 5c. Escalate (when stuck)

If you hit an escalation trigger:

1. **Abort the rebase** to leave the branch in a clean state:
   ```
   git rebase --abort
   ```

2. **Document what happened** in a PR comment:
   ```bash
   gh pr comment <PR> --body "$(cat <<'EOF'
   ## Rebase Conflict — Needs Human Resolution

   **Target branch:** <target-branch>
   **Conflicting files:**
   - `path/to/file1.sh` — <brief description of conflict>
   - `path/to/file2.sh` — <brief description of conflict>

   **Why this needs human judgment:**
   <1-3 sentences explaining why automated resolution isn't safe>

   **Story/Issue context:**
   - This PR: #<ref> — <subject>
   - Conflicting with changes from: <commit range or PR that introduced the other side>

   ---
   cc @bigjonroberts
   EOF
   )"
   ```

3. **Update the Taiga item** (if one was identified in Step 2):

   Project 4 has no "Blocked" status for stories or issues, so escalation is signalled with tags and assignment instead of a status change.

   **If `taigaType` is `"story"`:**
   - Re-fetch the story to get its current tags: `get_user_story(user_story_id=taigaId)`
   - Fetch members: `get_project_members(project_id=4)` — find Jon's user ID (bigjonroberts)
   - Update story: `update_user_story(user_story_id=taigaId, kwargs={"tags": <existing_tags> + [["escalation-needed", null], ["rebase-conflict", null]]})`
   - Assign to Jon: `assign_user_story_to_user(user_story_id=taigaId, user_id=<jon_user_id>)`

   **If `taigaType` is `"issue"`:**
   - Re-fetch the issue to get its current tags: `get_issue(issue_id=taigaId)`
   - Fetch members: `get_project_members(project_id=4)` — find Jon's user ID (bigjonroberts)
   - Update issue: `update_issue(issue_id=taigaId, kwargs={"tags": <existing_tags> + [["escalation-needed", null], ["rebase-conflict", null]]})`
   - Assign to Jon: `assign_issue_to_user(issue_id=taigaId, user_id=<jon_user_id>)`

   **If no Taiga item was identified:** skip Taiga updates.

4. **Report** the escalation and stop. Do NOT proceed with a partial or uncertain resolution.

### 5d. Continue the rebase

After resolving all conflicts in the current round:

```
git rebase --continue
```

If the rebase stops again with more conflicts, repeat Step 5. If it completes, proceed to Step 6.

## Step 6: Verify the rebase

### 6a. Sanity check

1. Verify no conflict markers remain anywhere in tracked files:
   ```
   git grep -l '<<<<<<<' || echo "No conflict markers found"
   ```
   If any are found, resolve them before continuing.

2. Verify the commit history looks right:
   ```
   git log --oneline origin/<target-branch>..HEAD
   ```
   The PR's commits should be replayed on top of the target branch.

### 6b. Syntax check

There is no build. Run `bash -n <file>` on every Bash file changed on the branch and `python3 -m py_compile <file>` on every changed Python file (`git diff --name-only origin/<target-branch>...HEAD`) to catch syntax errors introduced by the rebase.

If a check fails:
1. Read the error carefully.
2. It is likely due to the rebase combining changes that are valid independently but not together (e.g., a function renamed on the target, and the PR calls it by the old name).
3. Fix the errors. If you're still in the middle of the rebase, stage the fixes and run `git rebase --continue`. If the rebase has completed, commit the fixes as a new commit (do **not** amend rebased commits).
4. If the errors are too complex to resolve confidently, **escalate** per Step 5c.

### 6c. Run tests

Run `timeout 590 python3 -m unittest discover -s tests -v` in the foreground and read the unittest output for pass/fail (there are no `test-results/*.xml` files). See [docs/testing-workflow.md](../../../docs/testing-workflow.md); this repository has no CI gate, so this local run is the gate.

If tests fail:
1. You MUST follow the Test Failure Triage Protocol in `.claude/skills/shared/test-failure-triage.md` to determine whether the failure is due to the rebase resolution or a pre-existing issue. Do NOT assume a failure is pre-existing without verifying on the base branch.
2. If due to the rebase: fix the issue, commit the fix as a new commit (not amending a rebased commit).
3. If verified as pre-existing: file a Taiga bug per the triage protocol, note it in the report, and don't block on it.
4. Re-run the affected suite to verify.

## Step 7: Force-push

Once the syntax checks pass and tests are green (or failures are pre-existing):

```
git push --force-with-lease origin <head-branch>
```

Use `--force-with-lease` (not `--force`) to avoid overwriting changes pushed by someone else since we fetched.

If force-with-lease is rejected, someone else pushed to the branch. Fetch, check what changed, and re-evaluate.

## Step 8: Report

Post a comment on the PR summarizing the rebase:

```bash
gh pr comment <PR> --body "$(cat <<'EOF'
## Rebase Complete

**Rebased onto:** `<target-branch>` (<short SHA>)

### Conflicts Resolved
- `path/to/file.sh` — <brief description of resolution>

### Resolution Strategy
<1-2 sentences: e.g., "Additive changes combined" or "Adopted main's refactoring of X, updated PR's usage">

### Test Results
<pass/fail summary>

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Tell the caller:
- Whether the rebase succeeded or was escalated
- Which target branch was rebased onto, and whether it came from the argument or from `baseRefName`
- How many conflicts were resolved and how
- Test results summary
- The force-push SHA
