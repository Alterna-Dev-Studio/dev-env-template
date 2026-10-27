---
name: review-tests
description: Review test code changes against the testing strategy — fix placement, remove redundancy, improve quality
---

# Codex runtime and consumer scope

Invoke as `$review-tests <branch-name-or-pr-number>`. Treat the invocation text as `<arguments>` below. Read the target consumer's `AGENTS.md` and applicable `CLAUDE.md`, then verify its project, scripts, documentation, GitHub repository, and status names before acting. The detailed You-Thon procedure below applies only to a verified You-Thon checkout. Its paths and commands are consumer-owned, not files bundled with this package. If a required helper or equivalent operation is absent, stop with the missing dependency; do not invent a replacement.

Discover connected Taiga tools by semantic operation before use. Verify host and project identity, resolve `<verified-project-id>` live, and resolve status/member IDs immediately before mutation. Use Codex shell, repository search/read/edit, and web tools for the corresponding Claude tool functions under current permissions. Track checklist items in the conversation or an authorized local file. Subagent work uses Codex collaboration workers with explicit file ownership and the active agent limit. Do not invoke Claude agent roles or CLI as a substitute. Preserve each stop and verification condition below.

For a PR number, preflight authenticated GitHub reads in the same execution context before treating any SHA as its live head: check `gh auth status` and read the numbered PR's repository, base SHA, and head SHA, or use an available connected GitHub read tool with those exact fields. Retry connection, DNS, or API transport failures at most twice with short delays; an authorization denial needs a credential fix, not repeated network retries. A read-only Codex sandbox can have different network access from its host shell. Host-side verified evidence may be passed in as a pinned snapshot when its repository, PR number, base/head SHAs, capture time, and source are recorded; use that only for an explicitly **offline-evidence** review of those commits. It cannot establish the current remote head. If live head access remains unavailable, report **blocked: live PR head unavailable** (or **offline evidence only** if a pinned snapshot can be assessed); do not describe a recorded/local SHA as current, classify the current PR from assumed endpoints, edit, comment, or update a tracker. Do not guess at a sandbox network toggle.

# Review Tests — <arguments>

Review test code changes on a branch or PR against the project testing strategy. Identify and fix test placement errors, redundancy, and quality anti-patterns. Document every change with WHY.

## Step 0: Verify the consumer test mapping

Before classifying changed files, editing, running tests, or commenting, read the consumer's repository instructions and test policy. Record and verify all of these from that consumer's tracked documentation and actual repository layout:

- GitHub repository and comparison base, including the exact PR head when a PR number is supplied.
- Test-file and production-file paths or globs, with exclusions. Do not infer "no test changes" from source-consumer globs.
- Suite ownership and the consumer's placement, redundancy, and quality rules.
- Test command, its required tools/fixtures, and how its result is reported (for example, unittest console output rather than JUnit XML).
- Whether edits, commits, PR comments, and tracker updates are authorized in this invocation, plus the consumer's actual tracker target and any required helper for those stages.

The mapping may live across `AGENTS.md`, `CLAUDE.md`, a README, testing strategy/conventions/workflow documents, and the current test suite. Verify claims against the files and commands present; a source-consumer example is not a mapping. **If any field needed for the requested stage is absent or contradictory, stop before classifying the PR or making changes and report the exact missing dependency.** A bounded read-only review needs the first four fields; it does not require publication helpers for stages it will not run. Never silently fall back to the You-Thon globs, .NET commands, JUnit XML, or Taiga helpers.

Use the You-Thon procedure below only after verifying that the checkout is You-Thon and its named policy files, paths, commands, and helpers match. For every other mapped consumer, use the portable procedure. A caller's assertion that a mapping exists is not evidence until checked in the consumer repository.

Before a fix, re-read the live PR head (or published branch head) and confirm it still equals the reviewed commit. Confirm the editable checkout is on that commit and the intended branch; a detached or different local checkout is not an edit target. After committing fixes, verify the intended push target still points to the reviewed head, then push the exact fix commit under the consumer's branch policy. A normal push must reject an advanced remote head; do not overwrite it. Before PR comments or tracker updates, verify the live head now equals the pushed fix commit. If any check fails or live verification/write access is unavailable, stop that stage and report the precise state; do not claim publication completed.
If the review requires no fix, skip commit and push; verify the live head still equals the reviewed commit immediately before any authorized comment.

## Portable procedure for another mapped consumer

1. Resolve the branch and comparison base from the verified mapping. For a PR, verify its repository identity and live base/head commit SHAs, then compare those immutable commits. If using a local diff, check that both commits exist locally and that its endpoints equal the verified SHAs; otherwise fetch them if permitted or stop. Never substitute a same-named local branch or an assumed `origin/main` base. List changed test and production files using the mapped paths/globs. Inspect the complete diff and changed-file list as a cross-check so an omitted glob cannot turn a changed test into a false "no test changes" result.
2. If the mapped production files changed without mapped test changes, apply the consumer's documented test requirement and report the gap. If neither changed, report "No test changes to review" only after the mapping and complete changed-file list have been checked.
3. Read each changed test file and relevant production source. Check suite ownership, redundant coverage, and quality against the verified consumer policy. Cite the consumer rule and file evidence for every finding; do not import the You-Thon suite table or F#/browser anti-pattern list as requirements for another language.
4. If edits are authorized, fix confirmed issues according to that consumer's suite and framework conventions. Verify with its documented command and read its actual result format. If a required tool or fixture is unavailable, report the precise verification gap; do not substitute a different test command and claim success.
5. Commit and publish review comments or tracker updates only when those stages are authorized and their repository-specific instructions, targets, and helpers have been verified. Use the consumer's attribution and branch policy. Otherwise return the findings and verification results without writes.

For the dev-env-template S09 pilot, `docs/testing-strategy.md`, `docs/testing-conventions.md`, `README.md`, and the actual `tests/*.py` suite provide the Bash/Python mapping. Verify that `tests/test_shell.py` and `tests/test_scripts.py` cover changed Bash/Python code, and run `python3 -m unittest discover -s tests -v` when test execution is authorized. Its result is unittest console output; it has no F#, `.fsproj`, .NET, browser, or JUnit XML suite. The S09 read-only pilot authorizes review only, so stop before edits, tests, commits, PR comments, or tracker updates.

## You-Thon procedure (verified You-Thon checkout only)

### Step 1: Load the testing strategy

Read `docs/testing-strategy.md` completely. This is your authority for all decisions.

Also read `docs/testing-conventions.md` for framework-specific conventions (clock usage, file layout, naming).

### Step 2: Identify test changes

1. Determine the comparison base:
   - If argument looks like a PR number (digits only): read the live PR's `base.sha`, `head.sha`, and repository identity with `gh api repos/<verified-owner>/<verified-repo>/pulls/<number>`. Verify that both commits exist locally (`git cat-file -e <sha>^{commit}`); fetch the exact SHAs if allowed, or stop if unavailable. Use `git diff <verified-base-sha>...<verified-head-sha>` for every changed-file list and review diff. A local branch name or `origin/main` is not proof of either PR endpoint.
   - If argument is a branch name: verify its intended comparison base from the consumer's branch policy, then resolve and record the actual base and branch commit SHAs. Confirm against the remote when the branch is published. Use those SHAs for every diff; stop if the branch/base cannot be verified.
2. List all changed test files:
   ```bash
   git diff --name-only <verified-base-sha>...<verified-head-sha> -- 'tests/**/*.fs' 'src/Client/tests/**'
   ```
3. Also list all changed production source files:
   ```bash
   git diff --name-only <verified-base-sha>...<verified-head-sha> -- 'src/**/*.fs' ':!src/Client/tests/**'
   ```
4. If no test files changed:
   - If production source files also changed, report an ERROR: "Production code changed on this branch with no corresponding test changes. Tests are required for all feature and bugfix changes (see AGENTS.md or CLAUDE.md). Review the changes and add appropriate tests before proceeding."
   - If no production source files changed either (e.g., config-only or docs-only PR), report "No test changes to review" and return.

### Step 3: Review each changed test file

For each changed test file, read the full file and check:

### 3a. Suite placement

- Determine which suite this file is in (from its directory path)
- Read the test cases and determine what they're testing
- Cross-reference against Suite Definitions in `docs/testing-strategy.md`:
  - Domain validation tests -> must be in `tests/Shared/`
  - Aggregate invariant tests -> must be in `tests/Infrastructure/`
  - API handler/auth tests -> must be in `tests/Server/`
  - Elmish/client-state tests -> must be in `tests/Client/`
  - Pure utility tests -> must be in `tests/SharedUtils/` or `tests/DotNetUtils/`
  - Lifecycle/watchdog tests -> must be in `tests/Watchdog/`
- If a test is in the wrong suite, flag it for movement

### 3b. Redundancy

- For each test case, check if the same behavior is already tested at the authoritative level:
  - Use Grep to search for existing tests of the same function/type in other test directories
  - If the authoritative level already has coverage, this test should be at most a contract check (one happy + one sad path)
  - If this IS the authoritative level, full coverage is appropriate
- Flag tests that duplicate coverage beyond what the strategy allows

### 3c. Quality anti-patterns

Check for these specific anti-patterns:

- **CSS class assertions**: Tests that assert on Tailwind classes, color classes, or layout classes (e.g., `Expect.stringContains html "bg-blue-500"`) -- should assert on semantic content instead
- **Icon name assertions**: Tests checking for specific icon paths or names
- **Production logic reimplementation**: Test helpers that contain match expressions mirroring production decide/fold logic. Tests should call the production function with specific inputs and assert specific outputs.
- **DateTime.Now/UtcNow**: Any use of `DateTime.Now`, `DateTime.Today`, `DateTime.UtcNow`, or `DateTimeOffset.UtcNow` in test code -- must use `Clock.fixed'` or `Clock.Manual`, **except** for the narrow cases explicitly allowed in `docs/testing-strategy.md` (e.g., tests whose subject is `Clock.system` itself, or tests of external verifiers that must observe real system time such as Stripe signature validation). Do **not** replace system time usage in those allowed cases.
- **Inline E2E setup**: E2E specs that create preconditions through full UI flows when API helpers exist -- check `src/Client/tests/e2e/helpers/` for available API helpers
- **E2E outside the golden-flow list**: A new/added E2E test that does not correspond
  to a named golden flow in `src/Client/tests/e2e/TESTING-STRATEGY.md`. Flag for
  push-down to render/Client/Shared unless it exercises a golden-flow mechanism.
- **Bounding-box / layout assertions in E2E**: `boundingBox()`, pixel coordinates, or
  overlap/positioning checks added to E2E specs — visual-regression checks, not
  mechanism tests. Flag for removal or push-down.
- **New `describe.serial` blocks**: A newly-added `test.describe.serial(...)` in changed
  specs — serial state is the flakiest pattern in the suite. Flag and require
  justification (or refactor to independent tests).
- **`waitForTimeout` in new tests**: Any `page.waitForTimeout(...)` added in the diff —
  replace with an explicit wait on a condition/locator.

### Step 4: Fix issues

For each issue found:

### Suite movement

1. Move the test file to the correct directory
2. Update the source `.fsproj` (remove `<Compile Include>`) and target `.fsproj` (add `<Compile Include>`)
3. If the suite uses **Expecto** (Shared/Server), update the source aggregator file (remove from `all` list) and target aggregator file (add to `all` list)
4. If the suite uses **xUnit** (Infrastructure/Watchdog/Stripe), do **not** look for or edit aggregator files — tests are discovered via `[<Fact>]`, so only the `.fsproj` `<Compile Include>` entries need updating
5. Adapt framework if needed (e.g., Fable.Mocha -> Expecto when moving Client -> Shared)
6. Verify the test still compiles and passes

### Redundancy removal

1. Delete redundant test cases (keep at most one contract check at non-authoritative levels)
2. If an entire file becomes empty after removal, delete the file and its `.fsproj`/aggregator references

### Quality fixes

1. Rewrite CSS class assertions to assert on semantic content (text, ARIA attributes, element presence)
2. Replace DateTime.Now with Clock.fixed' or Clock.Manual
3. Replace production logic reimplementation with direct calls to production functions

### Step 5: Verify changes

Run `timeout 590 python3 -m unittest discover -s tests -v` per `docs/testing-workflow.md` and read the unittest output for pass/fail status (there are no `test-results/*.xml` files here). If any test fails due to the review changes, fix it before proceeding.

### Step 6: Commit and document

1. Commit all changes:
   ```bash
   git commit -am "$(cat <<'EOF'
   test: review and fix test quality issues

   [List each change and why, citing testing-strategy.md sections]

   Co-Authored-By: <your session's model> <configured-attribution-email>
   EOF
   )"
   ```
   Use your own session's attribution trailer — see [commit attribution](references/commit-attribution.md).

2. Verify the PR's head repository and branch (or the consumer's published branch target), confirm its live head is still the reviewed commit, and push the new commit to that exact branch under the consumer's branch policy. Confirm the live head is now the pushed commit. Stop if the remote advanced or the target cannot be verified.

3. If a PR number was provided, comment on the PR:
   ```bash
   gh pr comment <number> --body "$(cat <<'EOF'
   ## Test Quality Review

   [For each change:]
   - **[File]**: [What was changed] -- [Why, citing the specific rule from testing-strategy.md]

   [If no issues found: "All test changes comply with the testing strategy."]
   EOF
   )"
   ```

4. If a Taiga story ref is available (from PR description or branch name pattern `feature/*-<ref>`):
   1. Use the discovered Taiga `get_user_story_by_ref` operation with the story ref to fetch the story.
   2. Read the `id` field from the returned object — this is the numeric `<story_id>` required by the script.
   3. Comment on the story:
      ```bash
      scripts/taiga-comment.sh <story_id> "Test quality review: [summary]"
      ```

### Step 7: Return

Report:
- Number of issues found and fixed
- Summary of changes (movements, deletions, rewrites)
- Test suite results after fixes
- Whether any issues could not be auto-fixed (explain why)
