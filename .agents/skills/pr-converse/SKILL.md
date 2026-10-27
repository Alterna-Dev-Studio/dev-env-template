---
name: pr-converse
description: Address feedback and suggestions on a GitHub PR — thoughtfully, not as a rubber stamp
---

# Codex runtime and consumer scope

Invoke as `$pr-converse <PR-number>`. Treat the invocation text as `<arguments>` below. A gather-and-assess-only invocation ends after Step 3; it must not check out a branch, pull, edit, run tests, push, or post replies. This package preserves the selected You-Thon Claude workflow. Read the target consumer's `AGENTS.md` and applicable `CLAUDE.md`, then verify its project, scripts, documentation, GitHub repository, and status names before acting. You-Thon paths and commands are consumer-owned examples, not files bundled with this package. If the consumer has no verified mapping for a later edit, test, reply, or tracker operation, stop before that operation and report the missing mapping. Do not invent a replacement.

Discover connected Taiga tools by semantic operation before use. Verify host and project identity, resolve `<verified-project-id>` live, and resolve status/member IDs immediately before mutation. Use Codex shell, repository search/read/edit, and web tools for the corresponding Claude tool functions under current permissions. Track checklist items in the conversation or an authorized local file. Subagent work uses Codex collaboration workers with explicit file ownership and the active agent limit. Do not invoke Claude agent roles or CLI as a substitute. Preserve each stop and verification condition below.

For PR reads, first check that this execution context can reach GitHub with the intended account and repository (`gh auth status`, then a read of the numbered PR), or use an available connected GitHub read tool that returns the repository identity and exact `headRefOid`. On connection, DNS, or API transport failure, retry the read at most twice with short delays; do not retry an authorization denial as though it were transient. Do not infer network access from the host shell when this skill runs inside a read-only Codex sandbox. A host-side, authenticated exact-head check may supply a pinned snapshot for offline assessment if its repository, PR number, SHA, capture time, and source are recorded, but it does not prove the head is still current in this execution context. If no live read succeeds, label the result **blocked: live PR head unavailable** (or **offline evidence only** when a pinned snapshot exists); do not call the recorded/local SHA the current head, make a final feedback disposition, edit, or publish. Do not change the sandbox or guess at a network toggle to bypass this check.

# PR Converse — PR #<arguments>

Address review feedback on a pull request. Every comment deserves genuine consideration — but consideration does not mean automatic agreement. Good code review is a dialogue, not a rubber stamp.

## Step 1: Gather context

Fetch everything about the PR in parallel:

1. PR details: `gh pr view <arguments> --json title,body,baseRefName,headRefName,headRefOid,state,author,url`
2. Review comments: `gh api repos/{owner}/{repo}/pulls/<arguments>/reviews --paginate`
3. Inline comments: `gh api repos/{owner}/{repo}/pulls/<arguments>/comments --paginate`
4. General PR comments: `gh api repos/{owner}/{repo}/issues/<arguments>/comments --paginate`
5. Record the local branch and commit without changing them: `git branch --show-current` and `git rev-parse HEAD`. Compare the local commit with the PR's `headRefOid`; a different branch name at the same commit is acceptable for gathering feedback. Report a missing or mismatched local head explicitly. Read local files as PR-head evidence only when the local commit matches the recorded `headRefOid`; otherwise use GitHub's PR diff and files.

Determine {owner}/{repo} from `gh repo view --json nameWithOwner -q .nameWithOwner`.

If the PR is closed or merged, inform Jon and stop.

Steps 1–3 are read-only. Do not check out, fetch, pull, or otherwise change the worktree while gathering and assessing feedback. If the PR head cannot be verified live from GitHub in this execution context, report that limitation and stop before any final disposition, edit, or reply. A recorded SHA or same-named local branch is not a live verification.

## Step 2: Categorize the feedback

Read through all comments and categorize each one:

- **Requested changes** — reviewer explicitly requests a code change
- **Suggestions** — reviewer proposes an alternative approach or improvement
- **Questions** — reviewer is asking for clarification or explanation
- **Observations** — reviewer notes something but isn't necessarily asking for action
- **Automated** — comments from bots (Codex, CI, linters, etc.)

Add each non-automated feedback item to your working checklist, grouped by category. For automated comments, add a single summary item (e.g., "Address Codex review findings (3)").

## Step 3: Evaluate each feedback item

For each item, do the following **before** deciding whether to act on it:

### 3a. Understand what's being said

Read the comment carefully. If it references specific code, read that code. If it references a concept or pattern, make sure you understand the suggestion fully.

### 3b. Read the surrounding context

Don't evaluate a suggestion in isolation. Read:
- The file(s) the comment refers to
- The PR diff for that area (`gh pr diff <arguments>` or read the changed files)
- Any related code that the change would affect

### 3c. Form your own assessment

After reading the PR diff, comments, and referenced files, re-read `headRefOid` from GitHub. A numbered PR diff can change during assessment; if the head differs from Step 1, discard the assessment and repeat Steps 1–3 for the new head. If the head cannot be reverified, report the limitation and stop before making a disposition, edit, or reply. Local file evidence is valid only while its commit equals the reverified PR head.

For each piece of feedback, determine one of these dispositions:

1. **Agree — will fix**: The feedback identifies a genuine improvement. Make the change.
2. **Agree in principle — different approach**: The concern is valid but you'd solve it differently. Explain your alternative.
3. **Respectfully disagree**: The suggestion doesn't improve the code, or conflicts with project conventions / AGENTS.md or CLAUDE.md rules. Explain why clearly and specifically.
4. **Need clarification**: You don't fully understand what's being asked. Ask a specific question.
5. **Defer to Jon**: The feedback touches on a judgment call (architecture, scope, convention) that Jon should weigh in on. Flag it for Jon.

**Key principles:**
- A suggestion from any reviewer (human, bot, or otherwise) is input, not an instruction. Evaluate it on its merits.
- "Because the reviewer said so" is never sufficient justification for a change. Neither is "because it's convention elsewhere" — our project conventions (AGENTS.md or CLAUDE.md) take precedence.
- If a suggestion would violate a AGENTS.md or CLAUDE.md rule, do NOT make the change. Cite the rule in your response.
- If a suggestion would improve correctness, security, or readability, make the change even if the reviewer phrased it weakly.
- If you're genuinely unsure, lean toward flagging it for Jon rather than guessing.

## Step 4: Make code changes

For all items where you decided to make a change:

Before editing, verify that the consumer's policy and commands cover the planned edit, test, commit, push, and response. Refresh the PR's `headRefOid` and confirm that the editable checkout's `git rev-parse HEAD` equals that exact SHA. Verify the PR head repository and push target, not just its branch name. If the local head is stale or mismatched, stop and report both SHAs; reconcile the checkout separately, then repeat the comparison. If the local branch differs from the PR's head branch, prepare an editable checkout only in this phase, after confirming that doing so will preserve existing work, and repeat the exact-SHA check before editing. A same-named branch at a different commit is not ready to edit. Do not run an automatic `git pull` as part of this check.

1. Make the change following project conventions
2. If the change is non-trivial, run the directly affected test suite(s) for fast feedback per `docs/testing-workflow.md`. On build-relevant PRs, CI gates merges with separate `TestUnit`, `TestIntegration`, and `TestE2E` jobs.
3. For trivial changes (typos, comment fixes, formatting), a build check is sufficient: `dotnet run -- Build`

Commit changes with a clear message referencing the PR feedback:

```
git commit -m "address PR #<arguments> review feedback

- <summary of change 1>
- <summary of change 2>

Co-Authored-By: <your session's model> <configured-attribution-email>"
```
Use your own session's attribution trailer — see [commit attribution](references/commit-attribution.md).

Push to the verified PR head repository and branch, then confirm the PR's new `headRefOid` equals the pushed commit before replying. Do not rely on an unverified default push target.

## Step 5: Respond to comments

For **every** feedback item, post a reply on the PR. Use `gh` to reply to specific review comments:

### Replying to review comments (inline code comments)

```bash
gh api repos/{owner}/{repo}/pulls/<arguments>/comments/{comment_id}/replies \
  -f body="<your response>"
```

### Replying to general PR comments

```bash
gh api repos/{owner}/{repo}/issues/<arguments>/comments \
  -f body="<your response>"
```

### Response tone and format

- **Be direct.** Don't hedge excessively or apologize for disagreeing.
- **Be specific.** Reference line numbers, function names, and concrete reasons.
- **Be brief.** A few sentences is usually enough. Don't write essays.
- **Acknowledge the reviewer's point** before disagreeing — show you understood them.
- **Never be dismissive.** Every comment took someone's time and attention.

### Response templates by disposition

**Agree — will fix:**
> Good catch. Fixed in <commit-sha>.

or

> Agreed, that's clearer. Updated in <commit-sha>.

**Agree in principle — different approach:**
> You're right that [the concern]. I went with [alternative approach] instead because [specific reason]. See <commit-sha>.

**Respectfully disagree:**
> I considered this but think the current approach is better here because [specific reason]. [Optional: reference to project convention, AGENTS.md or CLAUDE.md rule, or technical justification.]

**Need clarification:**
> I want to make sure I understand — are you suggesting [interpretation A] or [interpretation B]? [Specific question about what they mean.]

**Defer to Jon:**
> This is a judgment call I'd like Jon to weigh in on. [Brief summary of the trade-off as you see it.] @bigjonroberts what do you think?

## Step 6: Report

Summarize what you did:

1. How many feedback items were addressed
2. What code changes were made (if any), with commit SHA
3. Which items you disagreed with and why (brief)
4. Which items are deferred to Jon for a decision
5. Any items that need further clarification from the reviewer

Mark all completed items as done in working checklist.
