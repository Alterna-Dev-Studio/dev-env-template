---
name: analyze-story
description: Analyze a Taiga story into a source-grounded plan and reconciled tasks without implementing it.
---

# Codex runtime and scope

Invoke this skill as `$analyze-story <story-ref>` or `$analyze-story new`. Treat the text after the skill name as the story selector; if there is no selector, follow the `new` path. This pilot preserves the You-Thon source workflow. Before operating, read the target repository's `AGENTS.md`, any applicable nested instructions, `docs/testing-strategy.md`, and `docs/testing-workflow.md`. Its F#/Elmish paths, Taiga statuses, merge automation, and test commands apply only when that consumer actually has them. For a different consumer, stop until an explicit consumer-local mapping replaces these details.

Discover the connected Taiga tools available in this Codex session. Map the source's `mcp__taiga-py__*` calls to equivalent discovered tools by operation; do not infer IDs or use a different tracker. Before any write, verify the Taiga host and project against the target consumer configuration and resolve its project ID live. The examples below use `<verified-project-id>` for that value. Resolve human story references to internal IDs, statuses by live exact name, and current tags immediately before mutation. If the matching Taiga read/write tools, authentication, or project guard are unavailable, stop and report the missing capability. `scripts/taiga-story.sh` is a consumer-owned helper: use it only when present and verified in the target repository; otherwise use a project-scoped exact lookup plus complete task pagination that returns the same fields and post-write count evidence.

Use Codex repository search/read and patch tools for Claude's `Glob`, `Grep`, `Read`, and `Edit`; use the shell execution tool for guarded helper commands and Git inspection. Use the available web tool for source-specific web references only when needed. Claude's `allowed-tools` list was a grant, not an instruction to bypass Codex tool permissions. Follow Codex's active permissions. Read [Taiga pagination](references/taiga-pagination.md) and [merge side effects](references/merge-side-effects.md) before the related steps; those copied companions are part of this pilot package. Keep the planning-only boundary below.

# Analyze Story

Investigate a user story and produce an implementation plan detailed enough that `$implement-story` can skip investigation and go straight to TDD for each task.

**THIS SKILL IS PLANNING ONLY.** You MUST NOT write code, edit source files, create branches, run builds, or make any implementation changes. Your only outputs are: Taiga updates (story description, tasks, epic links), edits to the story's design doc Open Questions section (see Step 4c), and a summary to the user. When you finish Step 10, STOP.

## Step 1: Get or create the story in Taiga

### If the argument is a ref number (existing story)

1. Find the story and its tasks with `scripts/taiga-story.sh <story-ref> <verified-project-id> --with-tasks` when that helper is present. It returns story JSON with a `tasks` array (O(1), no pagination). Otherwise use the project-scoped Taiga lookup and fully paged task listing described above. Extract `id` and `tasks`.
2. If the matching story is already closed/done, inform the user and stop.
3. Fetch full story details: `get_user_story(user_story_id=<id from step 1>)` for the description.
4. Proceed to Step 2.

### If the argument is "new" (or no ref number provided)

The user wants to create and analyze a new story. Ask them to describe it:

1. Ask the user: "What feature or enhancement do you want? Describe what the user should be able to do and why."
2. Fetch story statuses: `get_user_story_statuses(project_id=<verified-project-id>)` — identify the "New" status ID.
3. Create the story: `create_user_story(project_id=<verified-project-id>, subject=<short summary>, kwargs={"description": <user's description>})`
4. Report the created story ref number to the user, then proceed to Step 2.

## Step 2: Evaluate story completeness

Before investigating code, check whether the story gives you enough to work with. A well-defined story needs:

- **What the user can do** — a clear description of the capability being added or changed
- **Why it matters** — the motivation or user need driving this
- **Acceptance criteria** — specific, testable conditions that define "done"
- **Scope boundaries** — what is explicitly NOT included (prevents scope creep)

If any of these are missing or ambiguous, **stop and ask the user** before investigating. Use questions like:

- "The story says [X] but doesn't describe what success looks like. What are the acceptance criteria?"
- "How should this behave when [edge case]? The story doesn't specify."
- "This story could be interpreted as [interpretation A] or [interpretation B]. Which do you mean?"
- "Is this a modification of existing behavior or entirely new functionality?"
- "Does this need to work for anonymous users, authenticated users, or both?"
- "What should happen if [error condition]?"

Do NOT guess at missing details — wrong assumptions lead to wasted implementation. It's faster to ask one clarifying question than to plan the wrong feature.

Once you have clear capability description, acceptance criteria, and scope, proceed.

## Step 3: Assign to an epic

1. Fetch all open epics: `list_epics(project_id=<verified-project-id>, filters={"status__is_closed": false})`. Do NOT filter on a single `status` ID — open epics span several statuses, and picking one silently drops the rest. The listing paginates at 30 rows — if the call returns exactly 30 epics, page per [Taiga pagination](references/taiga-pagination.md) until you have the full set (this project already has more than 30 open epics).
2. Review the open (non-closed) epics and determine which one best fits this story's scope.
3. Present your recommendation to the user — name the epic and explain why it fits. If no existing epic is a good match, suggest creating a new one.
4. Once the user confirms, link the story: `link_user_story_to_epic(epic_id=<id>, user_story_id=<story_id>)`.
5. Check and update the epic's dependency diagram (see Step 3a below).

### Step 3a: Check and update epic dependency diagram

After linking the story to the epic, check whether the epic has a dependency diagram and suggest where the new story fits.

1. Fetch the full epic details: `get_epic(epic_id=<epic_id>, verbosity="full")` — read the `description` field.
2. Look for a `## Dependency Diagram` or `## Dependencies` section in the description.
3. If a dependency section exists:
   a. Read the existing dependency graph (the fenced code block with `#ref` entries and `└─►` arrows).
   b. Based on the new story's description and acceptance criteria, suggest which existing stories (if any) this new story depends on, and which stories (if any) depend on this new story.
   c. Present the suggestion to the user: "Based on the story description, I'd suggest placing #\<new_ref\> as depending on #\<dep_ref\> because [reason]. Does that look right?"
   d. If the user confirms, update the epic description by adding the new story to the dependency diagram's code block. Use `update_epic(epic_id=<id>, kwargs={"description": <updated_description>})`.
   e. If the user declines or wants changes, adjust accordingly.
4. If no dependency section exists:
   a. If the epic has more than one story linked to it, suggest creating a dependency section: "This epic has N stories but no dependency diagram. Would you like me to create one?"
   b. If the user confirms, create a basic `## Dependency Diagram` section with the stories listed in a fenced code block and ask the user to confirm the dependency relationships. Use `update_epic(epic_id=<id>, kwargs={"description": <updated_description>})`.
   c. If the user declines, skip.

## Step 4: Gather design context

Before investigating code, check whether a design document exists for this story.

### 4a. Look for a design document

1. Check `docs/designs/story-<ref>.md` (the convention from `$design-story`).
2. Also check the story description for a `## Design` section or a link to a design file — but don't rely on this alone, since the link may be missing.
3. If no design doc exists, proceed to Step 5. The story can still be analyzed without one, but note in the plan that no design doc was available.

### 4b. Incorporate the design document

If a design doc exists, read it fully. Its sections map directly to your analysis:

| Design doc section | How to use it in the plan |
|---|---|
| **Story Intent** | Use as the authoritative source for the plan's Overview. Don't re-derive intent — the design already captured it through interactive discussion with the user. |
| **Roles** | Informs auth requirements, conditional UI logic, and which test scenarios are needed. Each role's edge cases become test cases. |
| **Views** | Directly determines which files need changes (new views = new files, modified views = existing files). The route and parent info tells you where to wire things up. |
| **Wireframes** | The implementer's visual spec. Reference specific wireframe elements when describing UI tasks (e.g., "the card grid from the Desktop wireframe"). Don't re-describe layout — point to the wireframe. |
| **Interaction Flows** | Maps 1:1 to Elmish messages and API calls. Each flow's trigger → API call → success/error handling becomes implementation detail in the relevant task. Loading/empty/error states from here become explicit acceptance criteria. |
| **Component Inventory** | Tells you exactly which components to reuse vs create. "Reuse" items mean no new component code — just import and use. "New" items become their own tasks or sub-tasks. "Modified" items flag files that need changes. |
| **Responsive Behavior Summary** | Include in UI task descriptions so the implementer handles both breakpoints. Don't create separate "make it responsive" tasks — responsive behavior is part of each UI task. |
| **Design Decisions** | These are constraints the implementer must follow. Include the relevant decision (with rationale) in each task it affects — don't assume the implementer will read the design doc. |
| **Open Questions** | If any remain unresolved, **stop and ask the user** before planning. Unresolved design questions lead to wrong implementation plans. Once a question is resolved — by the user's answer here, or by a decision the analysis itself settles — sync that resolution back into the doc (Step 4c). |

When the design doc exists, the plan's task descriptions should reference it: e.g., "See wireframe in `docs/designs/story-<ref>.md` § Wireframes > View Name — Desktop". This avoids duplicating the visual spec in task descriptions while giving the implementer a precise pointer.

### 4c. Sync resolved Open Questions back into the design doc

The design doc's Open Questions section often defers a decision to analysis (e.g., "decide in $analyze-story"). If this analysis resolves any open question — by an explicit user answer, or by a decision the plan itself settles — the doc must reflect that, not just the Taiga plan. Otherwise the doc keeps reading as pending after the question is actually settled.

For each open question this analysis resolves:

1. Edit `docs/designs/story-<ref>.md` in the working tree: strike the question and record the resolution inline, e.g. `~~Which label maps to the client Label type?~~ — **resolved**: use \`Label.Fee\`.`
2. If a question genuinely can't be answered until implementation (not something this analysis decides), leave it unstruck but annotate it: `<question> — **deferred to implementation**: <what still needs deciding and why>`.
3. Leave any question this analysis didn't touch exactly as written — don't strike questions you didn't actually resolve.

Leave the edit in the working tree; this skill does not commit or create branches. Note in the Step 10 report which questions were struck or annotated so the user (or, in unattended runs, the orchestrator) knows the doc has an uncommitted change to review.

## Step 5: Investigate the codebase

Your goal is to understand what exists today and gather all the context the implementer will need. The implementer should only need to read the files they're modifying — not the files they're calling into.

### 5a. Identify the layers involved

From the story description and acceptance criteria, determine which layers need changes:

- **Shared types** (`src/Shared/`) — API contract types, client types, view models
- **Server** (`src/Server/`) — API endpoints, authentication, routing
- **Infrastructure** (`src/Infrastructure/`) — domain aggregates, event store, view DB, external services
- **Client** (`src/Client/`) — Elmish model/update, routing, UI components
- **Shared views** (`src/Shared/`) — React view components (Feliz), layout components
- **Database** (`db/up/`) — schema migrations

### 5b. Find existing patterns to follow

For each type of change needed, find the closest existing pattern in the codebase:

1. If adding a new API endpoint: read an existing endpoint in the relevant `*Api.fs` file and the corresponding type in `src/Shared/Shared.fs`
2. If adding a new view/page: read an existing page component in `src/Shared/`
3. If adding domain logic: read the existing aggregate in `src/Infrastructure/`
4. If adding a new DB query: read existing queries in `src/Infrastructure/ViewDb.fs`
5. If adding client-side state: read the Elmish model/messages in `src/Client/Index.fs` and `src/Shared/ClientTypes.fs`

Read the actual code for each pattern — don't just name it. The implementer needs to see the code to follow it.

### 5c. Map changes to files

For each acceptance criterion, trace what needs to change:

1. Start from the user-facing behavior (UI or API)
2. Follow through to the data layer
3. Note every file that needs a change and what that change is

### 5d. Gather implementation context

For each file that needs to change, read it and note:
- The exact function signatures and types involved
- The surrounding code patterns and conventions
- Any related tests that already exist
- Import/open statements needed

For any pattern the plan will reference (e.g., "follow the createChallenge pattern"), read and capture the actual code so the implementer doesn't have to.

## Step 6: Determine which tests are needed

### Documentation-only stories

If the story produces only documentation (no source code, no CSS, no configuration changes), tests are not applicable. Note this in the plan:

> **Tests**: Not applicable — this story produces documentation only. No source code changes to test.

Skip the rest of Step 6 and proceed to Step 7.

### Code-changing stories

Based on what the story changes, identify which test projects need new tests:

### Server tests (Expecto)
- **Location**: `tests/Server/`
- **Framework**: Expecto — `test "name" { ... }` syntax
- **Registration**: Add `<Compile Include="YourTest.fs" />` to `tests/Server/Server.Tests.fsproj` BEFORE the final `Server.Tests.fs` entry. Then add the test list binding to the `all` list in `tests/Server/Server.Tests.fs`.
- **Attribute**: Mark exported test lists with `[<Tests>]`

### Client tests (Fable.Mocha)
- **Location**: `tests/Client/`
- **Framework**: Fable.Mocha — `testCase "name" <| fun _ -> ...` syntax
- **Registration**: Add `<Compile Include="YourTest.fs" />` to `tests/Client/Client.Tests.fsproj` BEFORE the final `Client.Tests.fs` entry. Then add the test list binding to the `all` list in `tests/Client/Client.Tests.fs`.
- **No attribute needed** — just export a `let` binding with the test list

### Infrastructure tests (xUnit)
- **Location**: `tests/Infrastructure/`
- **Framework**: xUnit — `[<Fact>]` attribute, standard xUnit discovery (no Expecto `[<Tests>]` lists or aggregators)
- **Registration**: Add `<Compile Include="YourTest.fs" />` to `tests/Infrastructure/Infrastructure.Tests.fsproj` only — no aggregator file to update

### Shared tests (Expecto)
- **Location**: `tests/Shared/`
- **Framework**: Expecto (same as Server)
- **Registration**: Add to `.fsproj` and `Shared.Tests.fs` aggregator. Shared tests run independently from Server tests — each project has its own test runner.

### E2E tests (Playwright)
- **Location**: `src/Client/tests/e2e/`
- **Framework**: Playwright — TypeScript `.spec.ts` files
- **No registration needed** — Playwright discovers `.spec.ts` files automatically

### Stripe tests (xUnit + Playwright)
- **Integration tests location**: `tests/Stripe/`
- **E2E tests location**: `src/Client/tests/e2e/stripe-checkout.spec.ts`
- **Run with**: `dotnet run -- TestStripe` (integration) and `dotnet run -- TestStripeE2E` (E2E)
- **NOT included in `TestAll`** — require real Stripe API keys (`STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`)
- **When to include**: If the story changes any file with `Stripe` or `stripe` in its name/path, or changes `src/Shared/Challenge.fs` (fee amounts) or `src/Client/tests/e2e/checkout.spec.ts`
- **Result files**: `test-results/stripe.xml`, `test-results/stripe-e2e.xml`

### Step 6b: Validate test plan against testing strategy

Before proceeding to Step 7, validate every test case you planned in Step 6 against the rules in `docs/testing-strategy.md`. Read the strategy doc if you haven't already.

**Check each planned test against:**

1. **Suite Definitions** (SS Suite Definitions): Is each test planned for the correct suite? Key placements:
   - Domain validation (smart constructors, validated types) -> Shared
   - Aggregate invariants (fold/decide, event codecs) -> Infrastructure
   - API handler contracts (auth guards, error mapping) -> Server
   - Elmish update logic (client-only state) -> Client
   - User-critical workflows -> E2E

2. **Business Rule Ownership** (SS Cross-Cutting Rules > Business Rule Ownership): Each business rule has ONE authoritative test level. If you're planning tests for a rule at multiple levels, ensure only the authoritative level has full coverage. Other levels get at most one contract check (happy + sad path).

3. **Intentional Duplication** (SS Cross-Cutting Rules > Intentional Duplication): Cross-level duplication is acceptable ONLY for:
   - Shared domain + Infrastructure aggregate (different boundaries)
   - Shared validation + one E2E smoke (verifies UI feedback mechanism, not every variant)

4. **Render Test Guidelines** (SS Render Test Guidelines): If planning render tests, they must assert on semantic content (text, ARIA attributes, element presence) -- NOT CSS classes, icon names, or pixel layout.

5. **E2E Setup Policy** (SS E2E Setup Policy): E2E specs should use API/helper setup for preconditions. Full UI-driven setup only when the setup flow IS the behavior under test.

6. **Deterministic Time** (SS Cross-Cutting Rules > Deterministic Time): Any test involving dates/times must use `IClock` (`Clock.fixed'` or `Clock.Manual`). Flag if the plan doesn't mention clock usage for time-dependent tests.

If any planned tests violate these rules, correct the test plan before writing it into Step 9. Note the corrections and their rationale in the plan.

## Step 7: Identify documentation updates

Review what human-readable documentation exists and whether the story requires updates. Check:

- **Project README.md** (root) — does the feature change setup steps, add new commands, or alter the project overview?
- **Feature-specific docs in `docs/`** — does an existing doc cover this area (e.g., `docs/zitadel-setup.md` for auth changes)? Does a new doc need to be created? Are any new docs linked from README.md either directly or via another document (e.g., a new `docs/feature-x.md` linked from `docs/README.md` or `docs/features.md`)?
- **Repository agent instructions** (`AGENTS.md`, `CLAUDE.md`, or both as present) — does the change add env vars, alter architecture, or change development workflow? Keep the active provider instructions current; the `docs/` files are the human-facing ones.

If documentation changes are needed, include them as a dedicated task in the breakdown (Step 8). If nothing needs updating, note that explicitly in the plan so the implementer doesn't have to re-evaluate.

## Step 8: Break down into tasks

### Reconcile against the story's existing tasks

The `tasks` array returned by Step 1 is a required input to this step. If it is non-empty, this is a **reconcile**, not a fresh breakdown — composing the breakdown without consulting it leaves the story with two parallel task sets covering the same work, which makes `$implement-task` redo work that is already done.

1. Compose the ideal breakdown for the story as it stands now.
2. Map each planned unit of work onto the existing tasks **by the work it describes, not by subject string**. Two subjects that name the same files and the same change are the same task even when worded differently.
3. Treat closed tasks as completed work — plan around them, do not re-create them. A task is closed when `status_extra_info.is_closed` is `true` in the fetched array; that status-level flag is authoritative, and the top-level `is_closed` is only a fallback when the status info is absent (Taiga can return the top-level flag stale).
4. Emit an explicit disposition table before writing anything, with one row per existing task and one per planned unit:

| Existing task | Planned unit | Disposition |
|---|---|---|
| #1588 Replace inline Step 6b… | Replace Step 6b with agent-spawned Step 11 | **update** — same work, refresh description |
| — | Add regression test for X | **create** — genuinely new |
| #1591 Old approach task | — | **flag** — no longer in plan, surface to user |
| #1592 Already-closed task | (covered) | **leave** — closed, do not touch |

The dispositions are:

- **update** — the same unit of work already has a task. Refresh its description in place and keep the existing subject unless it is actively wrong.
- **create** — no existing task covers this unit of work.
- **leave** — the existing task is fine as-is, or is already closed.
- **flag** — the existing task no longer belongs to the plan. Surface it; never silently delete it.

When you cannot tell whether a planned unit matches an existing task, fetch that task's description with `get_task(task_id=<id>)` and compare the files-to-change lists. If it is still ambiguous, **ask the user** — creating a parallel task is the worse failure, because it silently makes `$implement-task` redo finished work.

Never leave the story with two tasks covering the same unit of work. If the reconcile produces one, that is a bug in the reconcile, not an acceptable outcome.

### Task shape

Each task should be:

- **Independently committable** — completing it leaves the codebase in a valid state
- **Appropriately scoped** — roughly 1-3 files changed, completable in one TDD cycle
- **Ordered by dependency** — later tasks can depend on earlier ones

Common task ordering for features:

1. **Add shared types** — new request/response types, API interface changes
2. **Add DB migration** — schema changes needed by the feature
3. **Add infrastructure logic** — domain aggregates, view DB queries/commands, event store
4. **Add server endpoint** — API handler, routing, authentication
5. **Add client state** — Elmish model/messages/update, routing
6. **Add UI component** — view components, styling
7. **Add tests** — can be split across tasks or combined with the code they test (TDD means tests come first within each task)
8. **Update documentation** — README.md, `docs/` files, and/or repository agent instructions as identified in Step 7

Not every story needs all of these. Only create tasks for work that actually needs doing.

### Task description format

Each task description in Taiga must contain enough detail that `$implement-story` can implement it without investigation. Use this format for each task description:

```
## What

[1-2 sentences describing what this task accomplishes]

## Files to Change

- `path/to/file.fs` — [what changes and why]

## Implementation Details

[Specific code changes. Include:]
- Exact function signatures and types
- The pattern to follow (with actual code from the codebase)
- Any new imports/opens needed

## Tests

- [Test project]: [test file] — [test cases to write]

## Acceptance

- [Specific condition that proves this task is done]
```

A task that must stay open after the story's PR merges (gated on a live step, a human, or another epic) adds a `## Gate` section to its description naming what it waits for. `$implement-task` skips such a task and reports it `GATED:`, and the story's merge-side-effect tags depend on it (see [merge side effects](references/merge-side-effects.md)).

## Step 9: Write the implementation plan

Compose the story-level plan using this template. This goes in the story description. Every section is required — don't skip any.

```markdown
## Implementation Plan

### Design Document

`docs/designs/story-<ref>.md` — [Status: Approved/Draft/None]

[If a design doc exists, note it here. If none exists, write "No design document available for this story." The implementer should read the design doc before starting — it contains wireframes, interaction flows, and component inventory that task descriptions reference.]

### Overview

[1-3 sentences. What capability is being added/changed and the high-level approach.]

### Architecture

[Which layers are involved and how they connect. Name the specific files.]

### What Does NOT Need to Change

[Bullet list of things the implementer might be tempted to modify but shouldn't. This prevents over-engineering and scope creep.]

### Merge Side Effects

- Completes through PR(s): [yes, one PR | yes, N PRs | no: <why>]
- Tasks that stay open after merge: [none | #<task-ref>: <reason>, one per `## Gate` task]
- Post-merge validation: [none | <live verification, deploy smoke, human acceptance step, or post-merge-only evidence>]
- Taiga tags set: [`close-tasks-on-merge`, `mark-done-on-merge` | `close-tasks-on-merge` only | none], per [merge side effects](references/merge-side-effects.md)

### Task Breakdown

1. [Task subject] — [1-sentence summary]
2. [Task subject] — [1-sentence summary]
...

### Tests

#### [Test file path] — [test framework]

**Registration steps:**
1. Add `<Compile Include="YourTest.fs" />` to `[.fsproj path]` before `[aggregator file]`
2. Add `YourModule.tests` to the `all` list in `[aggregator file path]`

**Test cases to write:**
1. [Test name] — [what it verifies]
2. [Test name] — [what it verifies]

**Pattern to follow:**
\```fsharp
// From tests/Server/SomeExistingTest.fs:
[<Tests>]
let tests =
    testList "Example" [
        test "case name" {
            // actual test code showing the pattern
        }
    ]
\```

### Verification

**Automated:**
- Run only the directly affected test suite(s) — not `TestAll`. See the consumer's `docs/testing-workflow.md` for the local-vs-CI policy and file-to-command routing (including Stripe and E2E rules).

**Manual:**
1. [Step-by-step manual verification scenario]
2. [Another scenario if applicable]
```

## Step 10: Update Taiga

### Update the story description

Write the plan into the Taiga story description.

**Replace the description — do not append to it or preserve a copy of the original.** Taiga keeps full version history, so the prior text is already retrievable via `get_history`; carrying a duplicate in the live description is redundant state that then rots independently of the version it came from. The description must read as current state only.

```
update_user_story(user_story_id=<id>, kwargs={"description": "<plan>"})
```

Carry forward any *fact* from the original the plan still depends on — the capability description, acceptance criteria, scope boundaries — by folding it into the plan where it belongs. What must not survive is a verbatim second copy of the original text.

### Create or update tasks

Execute the disposition table from Step 8 row by row. Do **not** re-derive matches here — Step 8 already decided which planned unit belongs to which existing task, and matching again by subject string is exactly the failure that produces a duplicate task set.

- **update** → `update_task(task_id=<id>, kwargs={"description": "<task details>"})`. Include `"subject"` in the kwargs only when the existing subject genuinely misdescribes the work; a reworded-but-equivalent subject is not a reason to churn it.
- **create** → `create_task(project_id=<verified-project-id>, subject=<task subject>, kwargs={"user_story": <story_id>, "description": "<task details>"})`
- **leave** → no call.
- **flag** → report it to the user with its ref and subject and ask before calling `delete_task`. Never delete without confirmation.

After the writes, re-fetch with the verified helper or equivalent project-scoped Taiga lookup and complete task listing; confirm the resulting task count equals the number of **update** + **create** + **leave** + **flag** rows, minus any flagged tasks the user confirmed for deletion. If it is higher, a duplicate was created — say so explicitly in the report rather than letting it pass silently.

### Tag and advance the story

1. Read the story's current tags from the fetched story data (tags appear as `[["tag-name", color], ...]`).
2. Add the `llm-analyzed` tag by appending `["llm-analyzed", null]` to the existing tags list.
3. If the story still represents substantial planning or likely future breakdown rather than a clean implementation-ready slice, also add:
   - `["planning-heavy", null]` when the story still needs significant design, architecture, open questions, or planning work before straightforward implementation
   - `["epic-candidate", null]` when the story is likely to split into multiple follow-on stories or become an epic after further breakdown
   - If it is truly an `epic-candidate`, you may create a new epic and child stories to represent the real breakdown. When you do this, keep the planning visibility explicit by tagging the umbrella/planning story and relevant child stories with `planning-heavy` and `epic-candidate` so Codex can review the structure afterward.
4. Add the merge-side-effect tags the plan's `### Merge Side Effects` section names, applying the deciding rule in [merge side effects](references/merge-side-effects.md):
   - `["close-tasks-on-merge", null]` iff the story completes through a single PR and no task stays open after merge.
   - `["mark-done-on-merge", null]` iff `close-tasks-on-merge` applies and no post-merge validation remains (live verification, a deploy smoke, a human acceptance step, or evidence only gatherable after merge).
   - If post-merge validation remains, do not add `mark-done-on-merge`, however complete the tasks are, and record that validation in the plan. If the story ships through several PRs, add neither: a tag fires on every PR that claims the story.
   - On a re-analysis, remove either tag the current plan no longer supports.
5. Use `get_user_story_statuses(project_id=<verified-project-id>)` (if not already fetched) to find the "Ready to Implement" status ID. Advance the story to "Ready to Implement" only when the analyzed story is now a sufficiently concrete implementation target. If the story remains primarily planning-heavy, do **not** force it forward just because analysis happened.
6. Apply the changes:
   ```
   update_user_story(user_story_id=<id>, kwargs={"tags": [<existing tags...>, ["llm-analyzed", null]], "status": <ready_to_implement_status_id>})
   ```
   Include `planning-heavy` / `epic-candidate` and the merge-side-effect tags in the tags list when applicable. If the story is already at "Ready to Implement" or later (In progress, Ready for test, etc.), omit the `status` field from kwargs — only the tag set should be updated.

### Report

Report what you found, that the plan has been written, list the tasks with their epic assignment, state the reconcile outcome from Step 8 as counts (how many tasks were updated, created, left, and flagged) along with the post-write task-count verification result, and confirm the story has been tagged with `llm-analyzed` and, when applicable, `planning-heavy` / `epic-candidate`. State which merge-side-effect tags were set and why (or why none were). If you created a new epic and child stories, say that explicitly and note that the resulting structure should be reviewed from a higher-level planning perspective. If the story is concrete enough, confirm it was advanced to "Ready to Implement". If it remains planning-heavy, say that explicitly instead of implying it is implementation-ready. If Step 4c edited the design doc, say so explicitly — name the file and list which questions were struck as resolved vs. annotated as deferred — so the user (or orchestrator, in unattended runs) knows to review the uncommitted change.

## STOP — Do Not Implement

This skill ends here. Do NOT proceed to implementation, code changes, branch creation, or any other modification. The user will invoke `$implement-story` separately when they're ready to begin coding.
