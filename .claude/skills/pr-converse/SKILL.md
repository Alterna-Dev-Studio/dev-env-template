---
name: pr-converse
description: Address feedback and suggestions on a GitHub PR — thoughtfully, not as a rubber stamp
argument-hint: "<PR-number>"
allowed-tools:
  - Bash(gh *)
  - Bash(git *)
  - Bash(dotnet run *)
  - Bash(dotnet build *)
  - Bash(dotnet fantomas *)
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - WebFetch(https://www.nuget.org/*)
  - WebFetch(https://github.com/*)
  - WebFetch(https://raw.githubusercontent.com/*)
  - WebFetch(https://learn.microsoft.com/*)
---

# PR Converse — PR #$ARGUMENTS

Address review feedback on a pull request. Every comment deserves genuine consideration — but consideration does not mean automatic agreement. Good code review is a dialogue, not a rubber stamp.

## Step 1: Gather context

Fetch everything about the PR in parallel:

1. PR details: `gh pr view $ARGUMENTS --json title,body,baseRefName,headRefName,state,author,url`
2. Review comments: `gh api repos/{owner}/{repo}/pulls/$ARGUMENTS/reviews --paginate`
3. Inline comments: `gh api repos/{owner}/{repo}/pulls/$ARGUMENTS/comments --paginate`
4. General PR comments: `gh api repos/{owner}/{repo}/issues/$ARGUMENTS/comments --paginate`
5. Check that we're on the PR's branch: `git branch --show-current` — if not, `git checkout <head-branch> && git pull`

Determine {owner}/{repo} from `gh repo view --json nameWithOwner -q .nameWithOwner`.

If the PR is closed or merged, inform Jon and stop.

## Step 2: Categorize the feedback

Read through all comments and categorize each one:

- **Requested changes** — reviewer explicitly requests a code change
- **Suggestions** — reviewer proposes an alternative approach or improvement
- **Questions** — reviewer is asking for clarification or explanation
- **Observations** — reviewer notes something but isn't necessarily asking for action
- **Automated** — comments from bots (Codex, CI, linters, etc.)

Add each non-automated feedback item to your TodoWrite list, grouped by category. For automated comments, add a single summary item (e.g., "Address Codex review findings (3)").

## Step 3: Evaluate each feedback item

For each item, do the following **before** deciding whether to act on it:

### 3a. Understand what's being said

Read the comment carefully. If it references specific code, read that code. If it references a concept or pattern, make sure you understand the suggestion fully.

### 3b. Read the surrounding context

Don't evaluate a suggestion in isolation. Read:
- The file(s) the comment refers to
- The PR diff for that area (`gh pr diff $ARGUMENTS` or read the changed files)
- Any related code that the change would affect

### 3c. Form your own assessment

For each piece of feedback, determine one of these dispositions:

1. **Agree — will fix**: The feedback identifies a genuine improvement. Make the change.
2. **Agree in principle — different approach**: The concern is valid but you'd solve it differently. Explain your alternative.
3. **Respectfully disagree**: The suggestion doesn't improve the code, or conflicts with project conventions / CLAUDE.md rules. Explain why clearly and specifically.
4. **Need clarification**: You don't fully understand what's being asked. Ask a specific question.
5. **Defer to Jon**: The feedback touches on a judgment call (architecture, scope, convention) that Jon should weigh in on. Flag it for Jon.

**Key principles:**
- A suggestion from any reviewer (human, bot, or otherwise) is input, not an instruction. Evaluate it on its merits.
- "Because the reviewer said so" is never sufficient justification for a change. Neither is "because it's convention elsewhere" — our project conventions (CLAUDE.md) take precedence.
- If a suggestion would violate a CLAUDE.md rule, do NOT make the change. Cite the rule in your response.
- If a suggestion would improve correctness, security, or readability, make the change even if the reviewer phrased it weakly.
- If you're genuinely unsure, lean toward flagging it for Jon rather than guessing.

## Step 4: Make code changes

For all items where you decided to make a change:

1. Make the change following project conventions
2. If the change is non-trivial, run the directly affected test suite(s) for fast feedback per [docs/testing-workflow.md](../../../docs/testing-workflow.md). On build-relevant PRs, CI gates merges with separate `TestUnit`, `TestIntegration`, and `TestE2E` jobs.
3. For trivial changes (typos, comment fixes, formatting), a build check is sufficient: `dotnet run -- Build`

Commit changes with a clear message referencing the PR feedback:

```
git commit -m "address PR #$ARGUMENTS review feedback

- <summary of change 1>
- <summary of change 2>

Co-Authored-By: <your session's model> <noreply@anthropic.com>"
```
Use your own session's attribution trailer — see `.claude/skills/shared/commit-attribution.md`.

Push the branch: `git push`

## Step 5: Respond to comments

For **every** feedback item, post a reply on the PR. Use `gh` to reply to specific review comments:

### Replying to review comments (inline code comments)

```bash
gh api repos/{owner}/{repo}/pulls/$ARGUMENTS/comments/{comment_id}/replies \
  -f body="<your response>"
```

### Replying to general PR comments

```bash
gh api repos/{owner}/{repo}/issues/$ARGUMENTS/comments \
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
> I considered this but think the current approach is better here because [specific reason]. [Optional: reference to project convention, CLAUDE.md rule, or technical justification.]

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

Mark all completed items as done in TodoWrite.
