# Test Failure Triage Protocol

When a test failure occurs and you suspect it is unrelated to your changes, you MUST follow this protocol before dismissing it. Do NOT claim a failure is "pre-existing" or "flaky" without verification.

## Step 1: Verify on the base branch

Stash your changes and check out the base branch to run the specific failing test(s):

```bash
git stash push -u  # stash including untracked files; note whether a stash was created
git checkout main  # or the appropriate base branch
# Run ONLY the specific failing test(s), not the full suite
python3 -m unittest -v tests.<module>.<Class>.<test_name>  # the failing test only
```

## Step 2: Evaluate the result

### If the test PASSES on the base branch

Your changes caused the failure. Return to your feature branch, pop the stash, and fix it:

```bash
git checkout <feature-branch>
git stash pop  # only run this if you actually created a stash in Step 1
# Fix the regression
```

### If the test FAILS on the base branch

The failure is genuinely pre-existing. Proceed to Step 3.

## Step 3: File or find a Taiga bug for the pre-existing failure

1. Record the base branch commit hash: `git rev-parse HEAD`
2. Search Taiga for an existing bug about this test using a supported search method, for example:
   - Taiga web UI search with relevant test name keywords
   - The `list_issues` MCP tool with an appropriate `filters={...}` query (e.g., by subject, tags, or status)
3. If no existing bug is found, file one following [bug filing](bug-filing.md):
   - Subject: `Pre-existing test failure: <test name>`
   - Description: Include the test name, test suite, error message, commit hash where verified broken, and which branch/PR discovered it
   - Severity per [docs/bug-triage.md](../../../../docs/bug-triage.md): Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
   - Priority: from the matrix (surface is the area the failing test covers: `devx`, `secrets`, `taiga`, or `skills`)
   - Tags: `dev-env-template`, surface tag, `src:agent`, and `pre-existing-failure`
4. Note the bug ref number

## Step 4: Return to your branch and continue

```bash
git checkout <feature-branch>
git stash pop  # only run this if you actually created a stash in Step 1
```

Continue with your current task. Add the following to the PR description (or note it for whoever creates the PR):

> **Known pre-existing failure:** #NNN — <test name>

## Summary

- NEVER dismiss a test failure as pre-existing without running it on the base branch
- NEVER leave a genuinely pre-existing failure untracked — always file a Taiga bug
- ALWAYS reference pre-existing failure bugs in the PR description
