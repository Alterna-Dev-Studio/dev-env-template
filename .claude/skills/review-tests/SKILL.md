---
name: review-tests
description: Review test code changes against the testing strategy — fix placement, remove redundancy, improve quality
argument-hint: "<branch-name-or-pr-number>"
allowed-tools:
  - Bash(git *)
  - Bash(gh *)
  - Bash(python3 -m unittest *)
  - Bash(timeout 590 python3 -m unittest *)
  - Bash(scripts/taiga-comment.sh *)
  - mcp__taiga-py__get_user_story_by_ref
  - Read
  - Edit
  - Write
  - Grep
  - Glob
---

# Review Tests — $ARGUMENTS

Review test code changes on a branch or PR against the project testing strategy. Identify and fix test placement errors, redundancy, and quality anti-patterns. Document every change with WHY.

## Step 1: Load the testing strategy

Read `docs/testing-strategy.md` completely. This is your authority for all decisions.

Also read `docs/testing-conventions.md` for framework-specific conventions (clock usage, file layout, naming).

## Step 2: Identify test changes

1. Determine the comparison base:
   - If argument looks like a PR number (digits only): `gh pr view <number> --json headRefName -q .headRefName` to get the branch, then `git diff origin/main...<branch>`
   - If argument is a branch name: `git diff origin/main...<branch>`
2. List all changed test files:
   ```bash
   git diff --name-only origin/main...<branch> -- 'tests/**/*.fs' 'src/Client/tests/**'
   ```
3. Also list all changed production source files:
   ```bash
   git diff --name-only origin/main...<branch> -- 'src/**/*.fs' ':!src/Client/tests/**'
   ```
4. If no test files changed:
   - If production source files also changed, report an ERROR: "Production code changed on this branch with no corresponding test changes. Tests are required for all feature and bugfix changes (see CLAUDE.md). Review the changes and add appropriate tests before proceeding."
   - If no production source files changed either (e.g., config-only or docs-only PR), report "No test changes to review" and return.

## Step 3: Review each changed test file

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

## Step 4: Fix issues

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

## Step 5: Verify changes

Run `timeout 590 python3 -m unittest discover -s tests -v` per [docs/testing-workflow.md](../../../docs/testing-workflow.md) and read the unittest output for pass/fail status (there are no `test-results/*.xml` files here). If any test fails due to the review changes, fix it before proceeding.

## Step 6: Commit and document

1. Commit all changes:
   ```bash
   git commit -am "$(cat <<'EOF'
   test: review and fix test quality issues

   [List each change and why, citing testing-strategy.md sections]

   Co-Authored-By: <your session's model> <noreply@anthropic.com>
   EOF
   )"
   ```
   Use your own session's attribution trailer — see `.claude/skills/shared/commit-attribution.md`.

2. If a PR number was provided, comment on the PR:
   ```bash
   gh pr comment <number> --body "$(cat <<'EOF'
   ## Test Quality Review

   [For each change:]
   - **[File]**: [What was changed] -- [Why, citing the specific rule from testing-strategy.md]

   [If no issues found: "All test changes comply with the testing strategy."]
   EOF
   )"
   ```

3. If a Taiga story ref is available (from PR description or branch name pattern `feature/*-<ref>`):
   1. Use `mcp__taiga-py__get_user_story_by_ref` with the story ref to fetch the story.
   2. Read the `id` field from the returned object — this is the numeric `<story_id>` required by the script.
   3. Comment on the story:
      ```bash
      scripts/taiga-comment.sh <story_id> "Test quality review: [summary]"
      ```

## Step 7: Return

Report:
- Number of issues found and fixed
- Summary of changes (movements, deletions, rewrites)
- Test suite results after fixes
- Whether any issues could not be auto-fixed (explain why)
