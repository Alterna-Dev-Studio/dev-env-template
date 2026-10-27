# SAASDK native skill install

Status: installed on branch `feat/saasdk-native-skills` from consumer main `11f08cb`
(2026-10-27). This supersedes the two Codex packages installed by the S09 pilot, which
were copied from older SAASDK revisions.

## Sources

- SAASDK: `Alterna-Dev-Studio/SAASDK` `origin/main` at
  `2a0416565bbc0a84a8d5f6e7f79361f6cfad9506` ("fix: gate S09 PR-head claims on
  live GitHub evidence (#44)"). This is the merged result of the
  `feature/streamlined-saasdk` rebuild; that branch no longer exists. Every
  source hash below matches `native/accepted-trees.json` at that commit.
- Consumer-owned helper scripts: `Alterna-Dev-Studio/you-thon` at
  `fbc5ee32283b2e9a34147c5e2d05fce1819a0dd1`. SAASDK deliberately does not ship
  these (`docs/epic-294-runtime-scripts.md`).
- Taiga target for this repository: Alterna Dev Studio, project id 4, slug
  `alterna-dev-studio` (verified live with `list_projects` and
  `get_project_overview`). Story statuses: New, Ready, In progress, Ready for
  test, Done, Archived.

## Selection

Five skills for both providers: `analyze-story`, `implement-story`,
`pr-converse`, `review-tests`, `codex-review-pr`. Their dependency closure was
computed from the SAASDK bodies at the pinned commit: none invokes another
skill or delegates to a `.claude/agents` or `.codex/agents` role, so no agent
files are installed. The Claude bodies depend on `.claude/skills/shared/*`; the
Codex bodies carry their own `references/`.

Install commands, from this repository:

```bash
for f in <paths in the table below>; do
  mkdir -p "$(dirname "$f")"
  git -C /home/jon/work/alterna/SAASDK show 2a0416565bbc0a84a8d5f6e7f79361f6cfad9506:"$f" > "$f"
done
for n in taiga-story.sh taiga-comment.sh codex-review-pr.sh; do
  git -C /home/jon/work/alterna/you-thon show fbc5ee32283b2e9a34147c5e2d05fce1819a0dd1:scripts/$n > scripts/$n
  chmod 755 scripts/$n
done
```

## Installed files

All SAASDK files are mode 100644. Hashes are SHA-256.

| Path | Source SHA-256 | Installed |
| --- | --- | --- |
| `.claude/skills/analyze-story/SKILL.md` | `18b2e8907ef032ee57a9976abdddf9e2760b540095245a1d15318a4207a7ad88` | patched, `ab548cd4c8a588d910d24784af22322bb3575dc504e56eba4d16922bdf0fb7da` |
| `.claude/skills/implement-story/SKILL.md` | `ed4540992b7b0109910094e48e59f858c333b365bd27aac33be6a3caa83a9966` | patched, `cda337aa393ab70ae6d6642f21fb3e613161924cfe3b54f18b406ce6cc52f03e` |
| `.claude/skills/pr-converse/SKILL.md` | `15b46f8e062058fcf651944ca615d6280d9bd6be72d49459c16fc8093e8368fb` | byte-identical |
| `.claude/skills/review-tests/SKILL.md` | `d3a5632a7c596c9dd3e01cde8d45aff47ca148285314f8baaddabc9e10d1e277` | patched, `7378a2509afe743687fc5bae4af84a63bd57a4e590e0cee0a98fbd659b31597e` (by the fully-implement-story install) |
| `.claude/skills/codex-review-pr/SKILL.md` | `dce0a4f22219234a58fe92147eb4f9edf4fa0860ada1bffb5ba06b0c98674b1a` | byte-identical |
| `.claude/skills/shared/taiga-pagination.md` | `cc8a2c179eb43099b2ee5dc67cab100642bbdf4bfbacee5e6346419dc3ff9d10` | byte-identical |
| `.claude/skills/shared/merge-side-effects.md` | `c13981db2c4d866d3b8bacc44e44af5c9652ec0b1e986695f17e6b99ab55d1ed` | byte-identical |
| `.claude/skills/shared/codex-review.md` | `b648438008748b79f6165af45379a530bab9080a85bdf90c513edfd48f817b6c` | byte-identical |
| `.claude/skills/shared/commit-attribution.md` | `b357f72263d3cd2409fa5d5c6acb1996ed4f9d4543e84db9a01351f28b56b82c` | byte-identical |
| `.agents/skills/analyze-story/SKILL.md` | `5234b5e60d921b48f192a6c4f17f68d8183371fb198bbceccf49e339269f3afb` | byte-identical |
| `.agents/skills/analyze-story/references/merge-side-effects.md` | `356a53ec70582ec2e95b34c11b0c48ad8055e74f77a7b22b98c567fab4d2d8ef` | byte-identical |
| `.agents/skills/analyze-story/references/taiga-pagination.md` | `5c84c60c33e1fbaa5b2a91d7ecdedbb03a538ebe394c083a582644b4857dd461` | byte-identical |
| `.agents/skills/implement-story/SKILL.md` | `c509f5cbb49bf5de39a3e7799225c0a022d616c3c1f3d717149a9b2ebd94633b` | byte-identical |
| `.agents/skills/implement-story/references/codex-review.md` | `b648438008748b79f6165af45379a530bab9080a85bdf90c513edfd48f817b6c` | byte-identical |
| `.agents/skills/implement-story/references/merge-side-effects.md` | `dd654e761b864b70b888d399c2178e1e2dffa5b639e2c335f5251c4294626881` | byte-identical |
| `.agents/skills/pr-converse/SKILL.md` | `3446f2421da2a06ea2463bd07984a0c1b8ca91bf8d31e17091ec5ba7fd2f9c59` | byte-identical |
| `.agents/skills/pr-converse/references/commit-attribution.md` | `d00569f163ff6608aca289a9fd8c7cff49a474a37bb0c85dd6d460980e93f780` | byte-identical |
| `.agents/skills/review-tests/SKILL.md` | `b2cd4a1487f830fb7a5e8ffdb0785ea9bd360c6456a5283cbaea59a838af1057` | patched, `43ae0b10ff7825c92558f11b78807a1ad463cc3c658ce17c3e1a3a6810ea68ef` (by the fully-implement-story install) |
| `.agents/skills/review-tests/references/commit-attribution.md` | `d00569f163ff6608aca289a9fd8c7cff49a474a37bb0c85dd6d460980e93f780` | byte-identical |
| `.agents/skills/codex-review-pr/SKILL.md` | `2c15836dfafbe911ac7273cdf849475f31e3dc188412b4d5be5e06e929d398eb` | byte-identical |

Helper scripts (mode 100755):

| Path | you-thon source SHA-256 | Installed SHA-256 |
| --- | --- | --- |
| `scripts/taiga-story.sh` | `47fbce954a02c1951b2dfac92228bdeca4785739835230ba9059985a94185278` | `e4c9d328887a6de8e7c2e4bd255e988ced06c87ef1770e650adea456c1ecca2c` |
| `scripts/taiga-comment.sh` | `302a1fdfd11418f024788ec005ff7fe6c3a221394535a3377ecc063c0ada3694` | `786d179c1e601141814598f9e2e7a3206e468a83fb4201481401d45f6a972d52` |
| `scripts/codex-review-pr.sh` | `58711eee635c11726e3204750f13ccfec8118a1c5950b2ca346a5e40cfd0a41e` | `5e901ea7564bb72f9aaddab1149a629b9e85985dc795f6f7740d2503998e1b61` |

## Consumer-local patches

Two Claude bodies are patched because they hardcode You-Thon's Taiga project
(3), its "Ready to Implement" status, and its F#/.NET test commands. The Codex
bodies resolve the project live and read `AGENTS.md` first, so they are not
patched. The three helper scripts gain a provenance comment. `taiga-story.sh` also
changes its default project from 3 to 4 and only treats a numeric second
argument as the project ID: the you-thon version took any second argument, so
`taiga-story.sh <ref> --epic` queried project `--epic` and returned exit 44.
The `implement-story` description line is also changed from project 3 to 4.
The fully-implement-story install (its own section below) later patched both
`review-tests` bodies: the Claude frontmatter swaps the `dotnet` grants for the
unittest command, and the one verification sentence in each body reads the
unittest output instead of `test-results/*.xml`. Unified diffs:

```diff
--- saasdk/2a04165/.claude/skills/analyze-story/SKILL.md
+++ .claude/skills/analyze-story/SKILL.md
@@ -42,7 +42,7 @@
 
 ### If the argument is a ref number (existing story)
 
-1. Find the story and its tasks: `scripts/taiga-story.sh $ARGUMENTS 3 --with-tasks` — returns story JSON with `tasks` array included (O(1), no pagination). Extract `id` and `tasks`.
+1. Find the story and its tasks: `scripts/taiga-story.sh $ARGUMENTS 4 --with-tasks` — returns story JSON with `tasks` array included (O(1), no pagination). Extract `id` and `tasks`.
 2. If the matching story is already closed/done, inform the user and stop.
 3. Fetch full story details: `get_user_story(user_story_id=<id from step 1>)` for the description.
 4. Proceed to Step 2.
@@ -52,8 +52,8 @@
 The user wants to create and analyze a new story. Ask them to describe it:
 
 1. Ask the user: "What feature or enhancement do you want? Describe what the user should be able to do and why."
-2. Fetch story statuses: `get_user_story_statuses(project_id=3)` — identify the "New" status ID.
-3. Create the story: `create_user_story(project_id=3, subject=<short summary>, kwargs={"description": <user's description>})`
+2. Fetch story statuses: `get_user_story_statuses(project_id=4)` — identify the "New" status ID.
+3. Create the story: `create_user_story(project_id=4, subject=<short summary>, kwargs={"description": <user's description>})`
 4. Report the created story ref number to the user, then proceed to Step 2.
 
 ## Step 2: Evaluate story completeness
@@ -80,7 +80,7 @@
 
 ## Step 3: Assign to an epic
 
-1. Fetch all open epics: `list_epics(project_id=3, filters={"status__is_closed": false})`. Do NOT filter on a single `status` ID — open epics span several statuses, and picking one silently drops the rest. The listing paginates at 30 rows — if the call returns exactly 30 epics, page per [`../shared/taiga-pagination.md`](../shared/taiga-pagination.md) until you have the full set (this project already has more than 30 open epics).
+1. Fetch all open epics: `list_epics(project_id=4, filters={"status__is_closed": false})`. Do NOT filter on a single `status` ID — open epics span several statuses, and picking one silently drops the rest. The listing paginates at 30 rows — if the call returns exactly 30 epics, page per [`../shared/taiga-pagination.md`](../shared/taiga-pagination.md) until you have the full set.
 2. Review the open (non-closed) epics and determine which one best fits this story's scope.
 3. Present your recommendation to the user — name the epic and explain why it fits. If no existing epic is a good match, suggest creating a new one.
 4. Once the user confirms, link the story: `link_user_story_to_epic(epic_id=<id>, user_story_id=<story_id>)`.
@@ -145,6 +145,8 @@
 
 ## Step 5: Investigate the codebase
 
+**Consumer note:** this repository is Bash/Python (see `README.md` and `AGENTS.md`). Use `README.md`, `docs/testing-strategy.md`, and `docs/testing-conventions.md` for layout and test placement; the F# `src/` and `.fsproj` guidance in Steps 5 to 7 does not apply here.
+
 Your goal is to understand what exists today and gather all the context the implementer will need. The implementer should only need to read the files they're modifying — not the files they're calling into.
 
 ### 5a. Identify the layers involved
@@ -446,11 +448,11 @@
 Execute the disposition table from Step 8 row by row. Do **not** re-derive matches here — Step 8 already decided which planned unit belongs to which existing task, and matching again by subject string is exactly the failure that produces a duplicate task set.
 
 - **update** → `update_task(task_id=<id>, kwargs={"description": "<task details>"})`. Include `"subject"` in the kwargs only when the existing subject genuinely misdescribes the work; a reworded-but-equivalent subject is not a reason to churn it.
-- **create** → `create_task(project_id=3, subject=<task subject>, kwargs={"user_story": <story_id>, "description": "<task details>"})`
+- **create** → `create_task(project_id=4, subject=<task subject>, kwargs={"user_story": <story_id>, "description": "<task details>"})`
 - **leave** → no call.
 - **flag** → report it to the user with its ref and subject and ask before calling `delete_task`. Never delete without confirmation.
 
-After the writes, re-fetch with `scripts/taiga-story.sh <ref> 3 --with-tasks` and confirm the resulting task count equals the number of **update** + **create** + **leave** + **flag** rows, minus any flagged tasks the user confirmed for deletion. If it is higher, a duplicate was created — say so explicitly in the report rather than letting it pass silently.
+After the writes, re-fetch with `scripts/taiga-story.sh <ref> 4 --with-tasks` and confirm the resulting task count equals the number of **update** + **create** + **leave** + **flag** rows, minus any flagged tasks the user confirmed for deletion. If it is higher, a duplicate was created — say so explicitly in the report rather than letting it pass silently.
 
 ### Tag and advance the story
 
@@ -465,16 +467,16 @@
    - `["mark-done-on-merge", null]` iff `close-tasks-on-merge` applies and no post-merge validation remains (live verification, a deploy smoke, a human acceptance step, or evidence only gatherable after merge).
    - If post-merge validation remains, do not add `mark-done-on-merge`, however complete the tasks are, and record that validation in the plan. If the story ships through several PRs, add neither: a tag fires on every PR that claims the story.
    - On a re-analysis, remove either tag the current plan no longer supports.
-5. Use `get_user_story_statuses(project_id=3)` (if not already fetched) to find the "Ready to Implement" status ID. Advance the story to "Ready to Implement" only when the analyzed story is now a sufficiently concrete implementation target. If the story remains primarily planning-heavy, do **not** force it forward just because analysis happened.
+5. Use `get_user_story_statuses(project_id=4)` (if not already fetched) to find the "Ready" status ID. Advance the story to "Ready" only when the analyzed story is now a sufficiently concrete implementation target. If the story remains primarily planning-heavy, do **not** force it forward just because analysis happened.
 6. Apply the changes:
    ```
    update_user_story(user_story_id=<id>, kwargs={"tags": [<existing tags...>, ["llm-analyzed", null]], "status": <ready_to_implement_status_id>})
    ```
-   Include `planning-heavy` / `epic-candidate` and the merge-side-effect tags in the tags list when applicable. If the story is already at "Ready to Implement" or later (In progress, Ready for test, etc.), omit the `status` field from kwargs — only the tag set should be updated.
+   Include `planning-heavy` / `epic-candidate` and the merge-side-effect tags in the tags list when applicable. If the story is already at "Ready" or later (In progress, Ready for test, etc.), omit the `status` field from kwargs — only the tag set should be updated.
 
 ### Report
 
-Report what you found, that the plan has been written, list the tasks with their epic assignment, state the reconcile outcome from Step 8 as counts (how many tasks were updated, created, left, and flagged) along with the post-write task-count verification result, and confirm the story has been tagged with `llm-analyzed` and, when applicable, `planning-heavy` / `epic-candidate`. State which merge-side-effect tags were set and why (or why none were). If you created a new epic and child stories, say that explicitly and note that the resulting structure should be reviewed from a higher-level planning perspective. If the story is concrete enough, confirm it was advanced to "Ready to Implement". If it remains planning-heavy, say that explicitly instead of implying it is implementation-ready. If Step 4c edited the design doc, say so explicitly — name the file and list which questions were struck as resolved vs. annotated as deferred — so the user (or orchestrator, in unattended runs) knows to review the uncommitted change.
+Report what you found, that the plan has been written, list the tasks with their epic assignment, state the reconcile outcome from Step 8 as counts (how many tasks were updated, created, left, and flagged) along with the post-write task-count verification result, and confirm the story has been tagged with `llm-analyzed` and, when applicable, `planning-heavy` / `epic-candidate`. State which merge-side-effect tags were set and why (or why none were). If you created a new epic and child stories, say that explicitly and note that the resulting structure should be reviewed from a higher-level planning perspective. If the story is concrete enough, confirm it was advanced to "Ready". If it remains planning-heavy, say that explicitly instead of implying it is implementation-ready. If Step 4c edited the design doc, say so explicitly — name the file and list which questions were struck as resolved vs. annotated as deferred — so the user (or orchestrator, in unattended runs) knows to review the uncommitted change.
 
 ## STOP — Do Not Implement
 
--- saasdk/2a04165/.claude/skills/implement-story/SKILL.md
+++ .claude/skills/implement-story/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: implement-story
-description: Implement a user story from Taiga project 3
+description: Implement a user story from Taiga project 4
 argument-hint: "<story-ref> [base-branch]"
 allowed-tools:
   - Bash(scripts/taiga-story.sh *)
@@ -55,13 +55,13 @@
 
 Use the Taiga MCP tools to gather everything you need.
 
-1. Find the story and its tasks: `scripts/taiga-story.sh <ref> 3 --with-tasks` — returns story JSON with `tasks` array included. Extract `id` and `tasks`.
+1. Find the story and its tasks: `scripts/taiga-story.sh <ref> 4 --with-tasks` — returns story JSON with `tasks` array included. Extract `id` and `tasks`.
 2. If the matching story is already closed/done, inform the user and stop
 3. Fetch full story details: `get_user_story(user_story_id=<id from step 1>)`
-5. Fetch user story statuses: `get_user_story_statuses(project_id=3)` — identify the "Ready for test" and "In progress" status IDs
-6. Fetch project members: `get_project_members(project_id=3)` — identify Jon's user ID (bigjonroberts) for reviewer assignment
+5. Fetch user story statuses: `get_user_story_statuses(project_id=4)` — identify the "Ready for test" and "In progress" status IDs
+6. Fetch project members: `get_project_members(project_id=4)` — identify Jon's user ID (bigjonroberts) for reviewer assignment
 
-**Known issue:** `get_task_statuses` is broken in the MCP server. Use status IDs from the task list data instead (Closed=14, New=11).
+**Known issue:** `get_task_statuses` is broken in the MCP server. Resolve task status IDs by exact status name from the `status_extra_info` in the task list data; do not hardcode numeric IDs.
 
 Copy the story subject and each task subject directly into your TodoWrite list. No other investigation or verification is needed.
 
@@ -83,8 +83,8 @@
 3. **If the task description contains a detailed implementation plan (files to change, implementation details, specific code patterns), skip investigation entirely.** Read only the files listed in the plan, then go straight to TDD implementation. Do NOT launch exploratory agents or re-investigate what the plan already explains.
 4. If there is **no** implementation plan in the task description, investigate the codebase as needed to understand what to change.
 5. Implement the task via TDD
-6. Run **only the directly affected test suite(s)** after each task — not `TestAll`. Consult [docs/testing-workflow.md](../../../docs/testing-workflow.md) for the local-vs-CI policy and file-to-command routing (including Stripe exception rules). On build-relevant PRs, CI gates merges with separate `TestUnit`, `TestIntegration`, and `TestE2E` jobs.
-7. Read the relevant `test-results/*.xml` file for pass/fail status. Parse `<testsuite>` attributes for counts and `<failure>` elements for details.
+6. Run the consumer test suite after each task: `python3 -m unittest discover -s tests -v`. Consult [docs/testing-workflow.md](../../../docs/testing-workflow.md) for the local test policy; this repository has no CI gate, so the local run is the gate.
+7. Read the unittest output for pass/fail status (there are no `test-results/*.xml` files in this repository).
    - Fix every failure, then re-run the affected suite to verify.
 8. Commit the changes (tests must pass first)
 9. Update the Taiga task status to done: `update_task(task_id=<id>, kwargs={"status": <done_status_id>})`
```

```diff
--- you-thon/fbc5ee3/scripts/taiga-story.sh
+++ scripts/taiga-story.sh
@@ -1,4 +1,5 @@
 #!/usr/bin/env bash
+# Copied from Alterna-Dev-Studio/you-thon fbc5ee32283b2e9a34147c5e2d05fce1819a0dd1 scripts/taiga-story.sh (consumer-owned helper); project default changed to 4.
 # ABOUTME: Fetch a Taiga item (user story, issue, or epic) by ref number using the REST API directly.
 # ABOUTME: Uses /by_ref endpoint for O(1) lookup — no pagination needed.
 
@@ -7,7 +8,7 @@
 usage() {
     echo "Usage: $0 <ref> [project_id] [--issue] [--epic] [--with-tasks]"
     echo "  ref          Item ref number (as shown in Taiga UI)"
-    echo "  project_id   Taiga project ID (default: 3)"
+    echo "  project_id   Taiga project ID (default: 4)"
     echo "  --issue      Look up an issue instead of a user story"
     echo "  --epic       Look up an epic instead of a user story"
     echo "  --with-tasks Also fetch and include the task list (user stories only)"
@@ -22,7 +23,12 @@
 }
 
 REF="${1:-}"
-PROJECT_ID="${2:-3}"
+# Only a numeric second argument is a project ID; a flag in that position keeps the default.
+if [[ "${2:-}" =~ ^[0-9]+$ ]]; then
+    PROJECT_ID="$2"
+else
+    PROJECT_ID=4
+fi
 ITEM_TYPE="userstories"
 WITH_TASKS=false
 
--- you-thon/fbc5ee3/scripts/taiga-comment.sh
+++ scripts/taiga-comment.sh
@@ -1,4 +1,5 @@
 #!/usr/bin/env bash
+# Copied from Alterna-Dev-Studio/you-thon fbc5ee32283b2e9a34147c5e2d05fce1819a0dd1 scripts/taiga-comment.sh (consumer-owned helper).
 # ABOUTME: Post a comment on a Taiga issue or user story using the REST API directly.
 # ABOUTME: PATCHes the user story/issue item endpoint with the `comment` field (and current version).
 
--- you-thon/fbc5ee3/scripts/codex-review-pr.sh
+++ scripts/codex-review-pr.sh
@@ -1,4 +1,5 @@
 #!/usr/bin/env bash
+# Copied from Alterna-Dev-Studio/you-thon fbc5ee32283b2e9a34147c5e2d05fce1819a0dd1 scripts/codex-review-pr.sh (consumer-owned helper).
 # ABOUTME: Runs a Codex CLI code review against a GitHub PR and posts the
 # ABOUTME: findings as a review with inline comments, capped at N passes per PR.
 #
--- saasdk/2a04165/.claude/skills/review-tests/SKILL.md
+++ .claude/skills/review-tests/SKILL.md
@@ -5,8 +5,8 @@
 allowed-tools:
   - Bash(git *)
   - Bash(gh *)
-  - Bash(dotnet run *)
-  - Bash(dotnet build *)
+  - Bash(python3 -m unittest *)
+  - Bash(timeout 590 python3 -m unittest *)
   - Bash(scripts/taiga-comment.sh *)
   - mcp__taiga-py__get_user_story_by_ref
   - Read
@@ -115,7 +115,7 @@

 ## Step 5: Verify changes

-Run the affected test suites per [docs/testing-workflow.md](../../../docs/testing-workflow.md). Read `test-results/*.xml` for pass/fail status. If any test fails due to the review changes, fix it before proceeding.
+Run `timeout 590 python3 -m unittest discover -s tests -v` per [docs/testing-workflow.md](../../../docs/testing-workflow.md) and read the unittest output for pass/fail status (there are no JUnit XML result files here). If any test fails due to the review changes, fix it before proceeding.

 ## Step 6: Commit and document


--- saasdk/2a04165/.agents/skills/review-tests/SKILL.md
+++ .agents/skills/review-tests/SKILL.md
@@ -139,7 +139,7 @@

 ### Step 5: Verify changes

-Run the affected test suites per `docs/testing-workflow.md`. Read `test-results/*.xml` for pass/fail status. If any test fails due to the review changes, fix it before proceeding.
+Run `timeout 590 python3 -m unittest discover -s tests -v` per `docs/testing-workflow.md` and read the unittest output for pass/fail status (there are no JUnit XML result files here). If any test fails due to the review changes, fix it before proceeding.

 ### Step 6: Commit and document

```

Consumer-owned files added for the skills' required reads: `AGENTS.md` (with
`CLAUDE.md` as a symlink to it), `docs/testing-workflow.md`, `.mcp.json`, and the
`scripts/taiga-mcp` and `scripts/setup-taiga-mcp` launcher pair (from the
personal `jon-dev-env` copy, with the checkout path made overridable through
`PYTAIGA_MCP_HOME`). `.mcp.json` runs `scripts/taiga-mcp full` for Claude Code
in this repository; `tests/test_scripts.py` covers the launcher. The pilot-only
framing was removed from `docs/testing-strategy.md` and
`docs/testing-conventions.md`.

## Known limits

- pytaiga-mcp ships two servers. The user-level Claude Code config runs
  `workflow` mode (about 34 ref-based intent tools such as `get_story`,
  `set_story_status`); Codex runs `full` mode (107 id-based CRUD tools). The
  SAASDK Claude bodies and their `mcp__taiga-py__*` grants are written against
  `full`. The repo-level `.mcp.json` therefore launches `taiga-mcp full` so the
  names match without porting the bodies. The launcher is this repository's
  own `scripts/taiga-mcp` (with `scripts/setup-taiga-mcp` to create the
  pytaiga-mcp checkout), so a fresh clone needs no personal path. The launcher
  uses `TAIGA_API_URL`, `TAIGA_USERNAME`, and `TAIGA_PASSWORD` from the
  environment when all three are set and no scope is named, and decrypts a
  vault scope otherwise, so a checkout without `secrets/` still connects.
- `.claude/skills/shared/merge-side-effects.md` and
  `.claude/skills/shared/taiga-pagination.md` are byte-identical and still
  show You-Thon status IDs (14, 17, 18) and `project_id=3` in examples.
  `AGENTS.md` records that these are You-Thon values.
- `scripts/taiga-update-on-merge.sh` and `.github/workflows/taiga-sync.yml`
  are not installed, so `close-tasks-on-merge` and `mark-done-on-merge` have
  no merge-time effect here.
- The `Bash(dotnet ...)` grants in `implement-story` frontmatter and the F#
  layout guidance in `analyze-story` Steps 5 to 7 remain in the bodies. A
  consumer note at the top of Step 5 and `AGENTS.md` override them.
- `scripts/codex-review-pr.sh` is unchanged apart from the provenance line and
  needs `codex`, `gh`, and `jq`. Its review and comment paths were not
  exercised by this install.

## Verification

```bash
python3 -m unittest discover -s tests -v        # 11 passed
git diff --check                                 # clean
bash -n scripts/*.sh                             # ok
shellcheck -S warning scripts/taiga-story.sh scripts/taiga-comment.sh scripts/codex-review-pr.sh   # clean
scripts/taiga-story.sh 2467                      # exit 0; story 2467 "Make dev-env-template shell setup portable…", In progress, project 4
scripts/taiga-story.sh 2466 --epic               # exit 0; epic 2466 "Portable developer and agent environment", project 4 (failed with exit 44 before the argument fix)
scripts/taiga-story.sh 2467 4 --with-tasks       # exit 0; 4 tasks
```

Every relative Markdown link under `.claude/skills/`, `.agents/skills/`,
`AGENTS.md`, and `docs/testing-workflow.md` resolves.

Codex discovery smoke (read-only sandbox, ephemeral, no Taiga call, no edit):

```bash
codex exec --sandbox read-only --ephemeral --color never -C /home/jon/work/utils/dev-env-template \
  'Invoke $analyze-story 2467 but stop after reading AGENTS.md, the installed .agents/skills/analyze-story/SKILL.md and its references. Report: which skill file you used, which consumer-local Taiga mapping you found in AGENTS.md (project id and slug), the helper script you would call and its exact arguments, and any dependency or policy mismatch. Do not call any Taiga tool, do not run scripts/taiga-story.sh, do not edit files. This is a read-only discovery smoke.'
```

Result: it read `AGENTS.md`, the installed skill and both references, reported
project 4 / `alterna-dev-studio`, the call
`scripts/taiga-story.sh 2467 4 --with-tasks`, and flagged the retained F#
guidance, the "Ready to Implement" versus "Ready" status name, and the absent
merge automation. Only `cat` commands ran; exit 0.

Claude discovery smoke (plan mode, no MCP servers, no edit):

```bash
claude -p --permission-mode plan --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
  'Invoke the /analyze-story skill for story 2467 but stop after reading CLAUDE.md, the installed .claude/skills/analyze-story/SKILL.md, and its shared references. Report: which skill file you used, which Taiga project id the skill body now uses, the exact helper command it would run first, which status name it would advance the story to in Step 10, and any dependency or policy mismatch you see. Do not run scripts/taiga-story.sh, do not call Taiga, do not edit files.'
```

Result: it loaded the Claude copy only, reported project 4 throughout the
body, the first call `scripts/taiga-story.sh 2467 4 --with-tasks`, and the
Step 10 target status "Ready" resolved by name. Mismatches it raised: no
`taiga-py` tools were loaded (expected, the smoke passed an empty MCP config);
the body's MCP names differ from the server's; the shared references keep
You-Thon values; the F# guidance in Steps 5 to 7 and the `docs/designs/`
expectation remain. It also noted this install doc was missing, because the
smoke ran before the doc was written. No file changed and no Taiga call was
made; exit 0.

Claude full-mode smoke through the repo `.mcp.json` (`--strict-mcp-config
--mcp-config .mcp.json`):

- Plan mode, `/implement-story 2467` stopped before Step 0: all seven
  `mcp__taiga-py__*` grants in the frontmatter were present in the session
  (`get_user_story`, `update_user_story`, `assign_user_story_to_user`,
  `get_task`, `update_task`, `get_user_story_statuses`,
  `get_project_members`); the body uses project 4 and reviewer
  `bigjonroberts`. Plan mode blocked the MCP calls themselves.
- Non-plan run with `--allowedTools` limited to `get_default_session` and
  `get_user_story_by_ref`: the session auto-authenticated and
  `get_user_story_by_ref(project_id=4, ref=2467)` returned "Make
  dev-env-template shell setup portable across hosts and devcontainers",
  status In progress. No write tool was granted; exit 0.
- Repo-relative launcher: the template checkout holds no vault, so
  `scripts/taiga-mcp full` here exits 1 with "Missing encrypted Taiga
  settings in profile". In a throwaway copy of this branch with a private
  `secrets/` and `.sops.yaml` added, the same `.mcp.json` started the full
  server, auto-authenticated, and `get_project_by_slug("alterna-dev-studio")`
  returned project 4; the copy and its vault were deleted afterwards.
  `tests/test_scripts.py` covers the launcher against a fake checkout.


The full `analyze-story` and `implement-story` write paths (Taiga mutation,
branch, PR) were not exercised by this install.

## pr-comments-resolve (from you-thon)

Source: `Alterna-Dev-Studio/you-thon` at `7988416182ad5b84b7899f83bb8ccf7db5eca955`.
SAASDK does not ship this skill, so it is copied from the consumer that owns it.
It is a different skill from `pr-converse`: it works only resolvable review
threads and sends issue comments and review bodies to `/pr-converse`, which is
already installed and left unchanged.

### Dependency closure

Computed from both bodies at the pinned commit, following links transitively:

- Claude body: `.claude/skills/shared/test-failure-triage.md`,
  `.claude/skills/shared/bug-filing.md`, `.claude/skills/shared/commit-attribution.md`,
  `docs/testing-workflow.md`, `docs/bug-triage.md`, `scripts/taiga-story.sh`,
  and (through `bug-filing.md`) `scripts/taiga-comment.sh`. It invokes no other
  skill and delegates to no `.claude/agents` role.
- Codex body: its own `references/` (the same three companions) plus the same
  consumer docs and scripts.
- `.claude/skills/shared/commit-attribution.md` is already installed and
  byte-identical to the you-thon copy. `docs/testing-workflow.md`,
  `scripts/taiga-story.sh` (default project 4), and `scripts/taiga-comment.sh`
  are the consumer-owned versions already in this repository and work as is.

Install commands, from this repository:

```bash
Y=/home/jon/work/alterna/you-thon
for f in .claude/skills/pr-comments-resolve/SKILL.md \
         .claude/skills/shared/test-failure-triage.md .claude/skills/shared/bug-filing.md \
         .agents/skills/pr-comments-resolve/SKILL.md \
         .agents/skills/pr-comments-resolve/references/test-failure-triage.md \
         .agents/skills/pr-comments-resolve/references/bug-filing.md \
         .agents/skills/pr-comments-resolve/references/commit-attribution.md; do
  mkdir -p "$(dirname "$f")"
  git -C "$Y" show 7988416182ad5b84b7899f83bb8ccf7db5eca955:"$f" > "$f"
done
```

### Installed files

All files are mode 100644. Hashes are SHA-256.

| Path | Source SHA-256 | Installed |
| --- | --- | --- |
| `.claude/skills/pr-comments-resolve/SKILL.md` | `d558ed145b4cc3460ab9dd320dac4686918d77156d1c2cc7b1ec035aa7ea2d97` | patched, `2d8bfcf42643c5f34c55a0bb4c83541a7521fa03fa8546fd0f549620dc1684cf` |
| `.claude/skills/shared/test-failure-triage.md` | `986039f042632873eec99843d761819d06c24b42909b6fc36790bd166f308958` | patched, `0e62e51538e5782e73f982b4463ada02d98c61e6cf202caed3359f494bc0c27e` |
| `.claude/skills/shared/bug-filing.md` | `34141f5eea232fe99e013c33f173d3c976534874f3d94f14c1fa4dcb1c50c29e` | patched, `4d91a367d6570144c17696d587fc73bbaa936b8388d35111224991d3a8cae207` |
| `.claude/skills/shared/commit-attribution.md` | `b357f72263d3cd2409fa5d5c6acb1996ed4f9d4543e84db9a01351f28b56b82c` | already installed, byte-identical |
| `.agents/skills/pr-comments-resolve/SKILL.md` | `beb66af45fee15f1221e7707e4ac9924e3c5cd6eea2ef944c4c599e83c48b430` | patched, `6a1a2d3636f1a418adc72eb09065309a3aa59ee8638c4462c456b038f9fa2b81` |
| `.agents/skills/pr-comments-resolve/references/test-failure-triage.md` | `8c66fec2e5b1a2aca37129d96affb0540a697620fbbea40e0dde27f6bb2a4ea7` | patched, `7e26298a5c3617ac81aedd669c2a9f430344626f243f6d0e256ef9c2a9155daf` |
| `.agents/skills/pr-comments-resolve/references/bug-filing.md` | `497aa2f56141a0df6457eee65fbfba2f4604ff0bc41c804cd8acdc47eccf33bb` | patched, `af8478c3111e9bfbd33df2a48b61d2a2114d4f366e66a392904d6f7384c7127b` |
| `.agents/skills/pr-comments-resolve/references/commit-attribution.md` | `d00569f163ff6608aca289a9fd8c7cff49a474a37bb0c85dd6d460980e93f780` | byte-identical |

### Consumer-local patches

The Claude body and `bug-filing.md` move Taiga project 3 to 4 and use the
full-mode tool name `search_project` (full mode has no `search`). The
frontmatter drops the `dotnet`, NuGet, and Microsoft Learn grants, adds this
repository's test and lint commands, and grants the tools the bug-filing and
triage companions already call (`scripts/taiga-comment.sh`, `list_issues`,
`update_issue`). Both bodies replace `test-results/*.xml` with the unittest
output, and both triage companions replace the `dotnet run` example. The Codex
body keeps `<verified-project-id>`, which it resolves live. No numeric status
ID appears in any installed file; statuses, types, severities, and priorities
are resolved by name. Both `bug-filing.md` copies, both triage companions, and
both bodies link this repository's [bug triage policy](bug-triage.md) and use
its tags: surface `devx`, `secrets`, `taiga`, or `skills`, plus the repository
tag `repo:dev-env-template`; `src:user` and `src:monitor` are dropped, and the
priority list has no Urgent because project 4 has none. Unified diffs:

```diff
--- you-thon/7988416/.claude/skills/pr-comments-resolve/SKILL.md
+++ .claude/skills/pr-comments-resolve/SKILL.md
@@ -5,25 +5,26 @@
 allowed-tools:
   - Bash(gh *)
   - Bash(git *)
-  - Bash(dotnet run *)
-  - Bash(timeout 590 dotnet run *)
-  - Bash(dotnet build *)
-  - Bash(dotnet fantomas *)
+  - Bash(python3 -m unittest *)
+  - Bash(timeout 590 python3 -m unittest *)
+  - Bash(bash -n *)
+  - Bash(shellcheck *)
   - Bash(scripts/taiga-story.sh *)
+  - Bash(scripts/taiga-comment.sh *)
   - Read
   - Edit
   - Write
   - Grep
   - Glob
-  - WebFetch(https://www.nuget.org/*)
   - WebFetch(https://github.com/*)
   - WebFetch(https://raw.githubusercontent.com/*)
-  - WebFetch(https://learn.microsoft.com/*)
   - mcp__taiga-py__get_user_story
   - mcp__taiga-py__get_epic
-  - mcp__taiga-py__search
+  - mcp__taiga-py__search_project
+  - mcp__taiga-py__list_issues
   - mcp__taiga-py__create_user_story
   - mcp__taiga-py__create_issue
+  - mcp__taiga-py__update_issue
   - mcp__taiga-py__get_issue_severities
   - mcp__taiga-py__get_issue_priorities
   - mcp__taiga-py__get_issue_types
@@ -181,8 +182,8 @@
 ### For Agree

 1. Make the code change following project conventions
-2. Run the affected test suite(s) per [docs/testing-workflow.md](../../../docs/testing-workflow.md). Run each suite or build as a foreground Bash call with the tool's `timeout: 600000` parameter set explicitly (the default is 120 s, after which the harness moves the command to the background), and wrap it in a shell `timeout 590` so it ends inside the call. Never use `run_in_background`, `Monitor`, or end your turn waiting for a task notification — this runs headless, so there is no next turn and the run dies with you. On exit 124, run a narrower target per docs/testing-workflow.md instead of a longer timeout.
-3. Read the relevant `test-results/*.xml` to verify all tests pass
+2. Run `python3 -m unittest discover -s tests -v`, plus `bash -n` and `shellcheck` on changed Bash, per [docs/testing-workflow.md](../../../docs/testing-workflow.md). Run each suite or build as a foreground Bash call with the tool's `timeout: 600000` parameter set explicitly (the default is 120 s, after which the harness moves the command to the background), and wrap it in a shell `timeout 590` so it ends inside the call. Never use `run_in_background`, `Monitor`, or end your turn waiting for a task notification — this runs headless, so there is no next turn and the run dies with you. On exit 124, run a narrower target per docs/testing-workflow.md instead of a longer timeout.
+3. Read the unittest output to verify all tests pass (this repository has no `test-results/*.xml` files)
 4. **If you believe a failure is unrelated to your changes**, you MUST follow the Test Failure Triage Protocol in `.claude/skills/shared/test-failure-triage.md` before dismissing it.
 5. Commit with a descriptive message:
    ```
@@ -231,17 +232,17 @@

 #### 4c. Check for duplicates

-Search Taiga project 3 for existing items about the same issue:
+Search Taiga project 4 for existing items about the same issue:

 ```
-search(project_id=3, text="<key terms from the observation>")
+search_project(project_id=4, text="<key terms from the observation>")
 ```

 If a matching item already exists, skip creation and reference the existing item in your reply.

 #### 4d. Create the Taiga item

-**For bugs (Issues):** follow `.claude/skills/shared/bug-filing.md` with source tag `src:pr-review`. Severity and priority come from `docs/bug-triage.md`, not from a guess. Prefix the description template with:
+**For bugs (Issues):** follow `.claude/skills/shared/bug-filing.md` with source tag `src:pr-review`. Severity and priority come from [docs/bug-triage.md](../../../docs/bug-triage.md), not from a guess. Prefix the description template with:

 ```
 Discovered during PR #$ARGUMENTS review.
@@ -254,7 +255,7 @@

 ```
 create_user_story(
-    project_id=3,
+    project_id=4,
     subject="<concise title>",
     kwargs={
         "description": "Discovered during PR #$ARGUMENTS review.\n\n**File:** `<path>`\n**Line:** <line number or range>\n\n<2-3 sentence description of the improvement and why it matters>"
--- you-thon/7988416/.claude/skills/shared/bug-filing.md
+++ .claude/skills/shared/bug-filing.md
@@ -1,41 +1,41 @@
 # Bug Filing Protocol

 Follow this whenever a skill or agent creates a Taiga bug. The rubric lives in
-`docs/bug-triage.md`; this file is only the procedure for applying it at filing time.
+[docs/bug-triage.md](../../../docs/bug-triage.md); this file is only the procedure for applying it at filing time.

 ## Step 1: Resolve IDs

 Fetch once per session, in parallel:

-- `get_issue_types(project_id=3)` — the "Bug" type ID
-- `get_issue_statuses(project_id=3)` — the "New" status ID
-- `get_issue_severities(project_id=3)` — Minor / Normal / Important / Critical
-- `get_issue_priorities(project_id=3)` — Low / Normal / High / Urgent
+- `get_issue_types(project_id=4)` — the "Bug" type ID
+- `get_issue_statuses(project_id=4)` — the "New" status ID
+- `get_issue_severities(project_id=4)` — Minor / Normal / Important / Critical (Wishlist is not used for bugs)
+- `get_issue_priorities(project_id=4)` — Low / Normal / High

 ## Step 2: Check for duplicates

-`search(project_id=3, text="<key terms>")`. If a matching open issue exists, do not create a new
+`search_project(project_id=4, text="<key terms>")`. If a matching open issue exists, do not create a new
 one: reference the existing ref in your output and, if you have new evidence, add it as a comment
 via `scripts/taiga-comment.sh <id> "<evidence>" --issue`.

-## Step 3: Classify per `docs/bug-triage.md`
+## Step 3: Classify per the triage policy

-1. **Surface** (exactly one): `product`, `devx`, `pipeline`, `ci`.
-2. **Source** (exactly one): `src:user`, `src:monitor`, `src:manual-test`, `src:pr-review`,
-   `src:agent`, `src:jon`. Skills filing on their own behalf use `src:agent`; the manual-testing
-   agent uses `src:manual-test`; PR comment resolution uses `src:pr-review`.
-3. **Severity**: pick from the severity table for that surface. This is provisional; the triage
-   sweep confirms it.
-4. **Priority**: read it off the severity × surface matrix, then apply the modifiers. If you
+1. **Surface** (exactly one): `devx`, `secrets`, `taiga`, `skills`. Always add the repository
+   tag `repo:dev-env-template`; project 4 is shared with other repositories.
+2. **Source** (exactly one): `src:manual-test`, `src:pr-review`, `src:agent`, `src:jon`.
+   Skills filing on their own behalf use `src:agent`; the manual-testing agent uses
+   `src:manual-test`; PR comment resolution uses `src:pr-review`.
+3. **Severity**: pick from the severity table. Triage confirms or corrects it.
+4. **Priority**: read it off the severity matrix, then apply the modifiers. If you
    deviate from the matrix, say why in the description.

-Do not apply the `triaged` tag. Only the triage sweep sets it.
+Do not apply the `triaged` tag. Only triage sets it.

 ## Step 4: Create the issue

 ```
 create_issue(
-    project_id=3,
+    project_id=4,
     subject="<concise title>",
     type_id=<bug_type_id>,
     status_id=<new_status_id>,
@@ -43,7 +43,7 @@
     priority_id=<id>,
     kwargs={
         "description": "<template below>",
-        "tags": [["<surface>", null], ["<source>", null]]
+        "tags": [["repo:dev-env-template", null], ["<surface>", null], ["<source>", null]]
     }
 )
 ```
@@ -58,7 +58,7 @@
 **Actual:** ...
 **Reproduce / observed at:** ...
 **Preliminary cause:** ...
-**Evidence:** <links, log lines, PR, commit hash, GlitchTip issue id>
+**Evidence:** <links, log lines, PR, commit hash>
 ```

 Add any context the filing skill already requires (for example "Discovered during PR #N review"
--- you-thon/7988416/.claude/skills/shared/test-failure-triage.md
+++ .claude/skills/shared/test-failure-triage.md
@@ -10,7 +10,7 @@
 git stash push -u  # stash including untracked files; note whether a stash was created
 git checkout main  # or the appropriate base branch
 # Run ONLY the specific failing test(s), not the full suite
-dotnet run -- <TestTarget>  # with appropriate filter if possible
+python3 -m unittest -v tests.<module>.<Class>.<test_name>  # the failing test only
 ```

 ## Step 2: Evaluate the result
@@ -38,9 +38,9 @@
 3. If no existing bug is found, file one following `.claude/skills/shared/bug-filing.md`:
    - Subject: `Pre-existing test failure: <test name>`
    - Description: Include the test name, test suite, error message, commit hash where verified broken, and which branch/PR discovered it
-   - Severity per `docs/bug-triage.md`: Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
-   - Priority: from the matrix (surface is `ci` unless the failure only reproduces in the local dev stack, then `devx`)
-   - Tags: surface tag, `src:agent`, and `pre-existing-failure`
+   - Severity per [docs/bug-triage.md](../../../docs/bug-triage.md): Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
+   - Priority: from the matrix (surface is the area the failing test covers: `devx`, `secrets`, `taiga`, or `skills`)
+   - Tags: `repo:dev-env-template`, surface tag, `src:agent`, and `pre-existing-failure`
 4. Note the bug ref number

 ## Step 4: Return to your branch and continue
--- you-thon/7988416/.agents/skills/pr-comments-resolve/SKILL.md
+++ .agents/skills/pr-comments-resolve/SKILL.md
@@ -159,8 +159,8 @@
 ### For Agree

 1. Make the code change following project conventions
-2. Run the affected test suite(s) per `docs/testing-workflow.md`
-3. Read the relevant `test-results/*.xml` to verify all tests pass
+2. Run `python3 -m unittest discover -s tests -v`, plus `bash -n` and `shellcheck` on changed Bash, per `docs/testing-workflow.md`
+3. Read the unittest output to verify all tests pass (this repository has no `test-results/*.xml` files)
 4. **If you believe a failure is unrelated to your changes**, you MUST follow the Test Failure Triage Protocol in [test failure triage](references/test-failure-triage.md) before dismissing it.
 5. Commit with a descriptive message:
    ```
@@ -209,7 +209,7 @@

 #### 4c. Check for duplicates

-Search Taiga the verified You-Thon project for existing items about the same issue:
+Search the verified consumer Taiga project for existing items about the same issue:

 ```
 search(project_id=<verified-project-id>, text="<key terms from the observation>")
@@ -219,7 +219,7 @@

 #### 4d. Create the Taiga item

-**For bugs (Issues):** follow [bug filing](references/bug-filing.md) with source tag `src:pr-review`. Severity and priority come from `docs/bug-triage.md`, not from a guess. Prefix the description template with:
+**For bugs (Issues):** follow [bug filing](references/bug-filing.md) with source tag `src:pr-review`. Severity and priority come from [docs/bug-triage.md](../../../docs/bug-triage.md), not from a guess. Prefix the description template with:

 ```
 Discovered during PR #<arguments> review.
--- you-thon/7988416/.agents/skills/pr-comments-resolve/references/bug-filing.md
+++ .agents/skills/pr-comments-resolve/references/bug-filing.md
@@ -1,7 +1,7 @@
 # Bug Filing Protocol

 Follow this whenever a skill or agent creates a Taiga bug. The rubric lives in
-`docs/bug-triage.md`; verify the consumer project and read that policy before filing. This file is only the procedure for applying it at filing time.
+[docs/bug-triage.md](../../../../docs/bug-triage.md); verify the consumer project and read that policy before filing. This file is only the procedure for applying it at filing time.

 ## Step 1: Resolve IDs

@@ -9,8 +9,8 @@

 - `get_issue_types(project_id=<verified-project-id>)` — the "Bug" type ID
 - `get_issue_statuses(project_id=<verified-project-id>)` — the "New" status ID
-- `get_issue_severities(project_id=<verified-project-id>)` — Minor / Normal / Important / Critical
-- `get_issue_priorities(project_id=<verified-project-id>)` — Low / Normal / High / Urgent
+- `get_issue_severities(project_id=<verified-project-id>)` — Minor / Normal / Important / Critical (Wishlist is not used for bugs)
+- `get_issue_priorities(project_id=<verified-project-id>)` — Low / Normal / High

 ## Step 2: Check for duplicates

@@ -18,18 +18,18 @@
 one: reference the existing ref in your output and, if you have new evidence, add it as a comment
 via `scripts/taiga-comment.sh <id> "<evidence>" --issue`.

-## Step 3: Classify per `docs/bug-triage.md`
+## Step 3: Classify per the triage policy

-1. **Surface** (exactly one): `product`, `devx`, `pipeline`, `ci`.
-2. **Source** (exactly one): `src:user`, `src:monitor`, `src:manual-test`, `src:pr-review`,
-   `src:agent`, `src:jon`. Skills filing on their own behalf use `src:agent`; the manual-testing
-   agent uses `src:manual-test`; PR comment resolution uses `src:pr-review`.
-3. **Severity**: pick from the severity table for that surface. This is provisional; the triage
-   sweep confirms it.
-4. **Priority**: read it off the severity × surface matrix, then apply the modifiers. If you
+1. **Surface** (exactly one): `devx`, `secrets`, `taiga`, `skills`. Always add the repository
+   tag `repo:dev-env-template`; project 4 is shared with other repositories.
+2. **Source** (exactly one): `src:manual-test`, `src:pr-review`, `src:agent`, `src:jon`.
+   Skills filing on their own behalf use `src:agent`; the manual-testing agent uses
+   `src:manual-test`; PR comment resolution uses `src:pr-review`.
+3. **Severity**: pick from the severity table. Triage confirms or corrects it.
+4. **Priority**: read it off the severity matrix, then apply the modifiers. If you
    deviate from the matrix, say why in the description.

-Do not apply the `triaged` tag. Only the triage sweep sets it.
+Do not apply the `triaged` tag. Only triage sets it.

 ## Step 4: Create the issue

@@ -43,7 +43,7 @@
     priority_id=<id>,
     kwargs={
         "description": "<template below>",
-        "tags": [["<surface>", null], ["<source>", null]]
+        "tags": [["repo:dev-env-template", null], ["<surface>", null], ["<source>", null]]
     }
 )
 ```
@@ -58,7 +58,7 @@
 **Actual:** ...
 **Reproduce / observed at:** ...
 **Preliminary cause:** ...
-**Evidence:** <links, log lines, PR, commit hash, GlitchTip issue id>
+**Evidence:** <links, log lines, PR, commit hash>
 ```

 Add any context the filing skill already requires (for example "Discovered during PR #N review"
--- you-thon/7988416/.agents/skills/pr-comments-resolve/references/test-failure-triage.md
+++ .agents/skills/pr-comments-resolve/references/test-failure-triage.md
@@ -10,7 +10,7 @@
 git stash push -u  # stash including untracked files; note whether a stash was created
 git checkout main  # or the appropriate base branch
 # Run ONLY the specific failing test(s), not the full suite
-dotnet run -- <TestTarget>  # with appropriate filter if possible
+python3 -m unittest -v tests.<module>.<Class>.<test_name>  # the failing test only
 ```

 ## Step 2: Evaluate the result
@@ -38,9 +38,9 @@
 3. If no existing bug is found, file one following [bug filing](bug-filing.md):
    - Subject: `Pre-existing test failure: <test name>`
    - Description: Include the test name, test suite, error message, commit hash where verified broken, and which branch/PR discovered it
-   - Severity per `docs/bug-triage.md`: Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
-   - Priority: from the matrix (surface is `ci` unless the failure only reproduces in the local dev stack, then `devx`)
-   - Tags: surface tag, `src:agent`, and `pre-existing-failure`
+   - Severity per [docs/bug-triage.md](../../../../docs/bug-triage.md): Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
+   - Priority: from the matrix (surface is the area the failing test covers: `devx`, `secrets`, `taiga`, or `skills`)
+   - Tags: `repo:dev-env-template`, surface tag, `src:agent`, and `pre-existing-failure`
 4. Note the bug ref number

 ## Step 4: Return to your branch and continue
```

### Bug triage policy

[docs/bug-triage.md](bug-triage.md) is a short adaptation of you-thon
`docs/bug-triage.md` at `7988416182ad5b84b7899f83bb8ccf7db5eca955` (source
SHA-256 `f5b1b48c39a3216537d4b64e8d6c216575125d59b24e53207324c937ab1faf7f`).
It keeps the source's severity/priority split, override-with-comment rule,
tag model, description template, and duplicate and claim rules, and rewrites
severity and surfaces around this repository. Field values were read live from
project 4 and are named, never numbered; project 4 has no Urgent priority and
no Spike type. You-Thon production intake, monitoring sources, the launch
blocker modifier, the scheduled sweep and fix orchestrators, and links to docs
that do not exist here are dropped.

### Deliberately left out

- `/pr-converse`: named only as the redirect for issue comments and review
  bodies. The SAASDK copy is already installed and is not replaced.
- `/code-review`: a Claude Code built-in mentioned only as a source of issue
  comments; nothing to install.

### Known limits

- No triage skill is installed; `docs/bug-triage.md` describes the triage
  steps for Jon or an agent asked to run them.
- The skill's Taiga and GitHub write paths (thread replies, resolution, issue
  and story creation) were not exercised by this install.

## fully-implement-story (from SAASDK)

Source: `Alterna-Dev-Studio/SAASDK` at `2a0416565bbc0a84a8d5f6e7f79361f6cfad9506`,
the same pinned commit as the first section. `fully-implement-story` is the
orchestrator that runs a story end to end with fresh worker agents. It is
installed for Claude Code and Codex together with the transitive closure it
invokes, each patched to this Bash/Python consumer: Taiga project 4 with every
status resolved by name, `python3 -m unittest discover -s tests -v` as the only
suite, and no CI gate. Steps that cannot apply here are patched out rather than
ported.

### Dependency closure

Computed from the bodies at the pinned commit, following every skill, agent
role, shared file, and script they name.

Claude side:

| Item | Disposition |
| --- | --- |
| `.claude/skills/fully-implement-story/SKILL.md` | installed, patched (inline review-thread loop; manual-testing phases removed) |
| `.claude/skills/implement-task/SKILL.md` | installed, patched |
| `.claude/skills/finalize-story-pr/SKILL.md` | installed, patched |
| `.claude/skills/rebase-branch/SKILL.md` | installed, patched |
| `.claude/skills/review-tests/SKILL.md` | already installed; minimal patch (grants and one sentence) because `test-quality-reviewer` runs it |
| `.claude/skills/shared/synchronous-worker-contract.md` | installed, patched (slow-command example) |
| `.claude/agents/senior-software-developer.md`, `test-quality-reviewer.md`, `remediation-developer.md` | installed, patched. `~/.claude/agents/` already holds You-Thon copies of two of them; project-level files override by name, which is why the repository ships its own |
| `.claude/skills/remediate-pr/SKILL.md` plus you-thon `scripts/remediate_pr.py`, `scripts/monitor-pr-stability.sh`, `scripts/lib/stability_parser.py` | not installed: the script polls CI stability and this repository has no CI. Orchestrator Steps 4 and 7 become an inline unresolved-review-thread loop using the GraphQL query already in `pr-comments-resolve` |
| `.claude/skills/fix-story-bug/SKILL.md`, `.claude/agents/senior-manual-testing-specialist.md` | not installed: Steps 5 to 8 (browser testing, bug fixing, post-fix monitoring, retest) are removed; there is no application to test |
| `fix-build-failure`, `fix-single-bug`, `analyze-bug` | not installed; removed from the agent role skill lists |
| `.claude/skills/shared/merge-side-effects.md`, `commit-attribution.md`, `codex-review.md`, `test-failure-triage.md`, `bug-filing.md` | already installed, unchanged |
| `scripts/taiga-story.sh`, `scripts/taiga-comment.sh`, `scripts/codex-review-pr.sh` | already installed, unchanged |
| `docs/testing-workflow.md`, `docs/testing-strategy.md`, `docs/testing-conventions.md`, `docs/bug-triage.md` | exist, unchanged apart from the new `tests/test_skills.py` row in the strategy table |
| `docs/design-system.md`, `scripts/devcontainer/launch.sh`, `dotnet run -- Reset` | do not exist here; every mention removed |
| `/tmp/fully-implement-<ref>.json`, `/tmp/implement-task-<story>-<task>.lock` | kept as is |

Codex side:

| Item | Disposition |
| --- | --- |
| `.agents/skills/fully-implement-story/SKILL.md` | installed, patched (same structure as the Claude body in Codex vocabulary) |
| `.agents/skills/fully-implement-story/references/merge-side-effects.md` | installed, byte-identical (same bytes as the `implement-story` reference) |
| `.agents/skills/implement-task/SKILL.md` + `references/commit-attribution.md`, `merge-side-effects.md` (byte-identical), `test-failure-triage.md` (patched) | installed |
| `.agents/skills/finalize-story-pr/SKILL.md` + `references/codex-review.md`, `merge-side-effects.md` (byte-identical), `bug-filing.md`, `test-failure-triage.md` (patched) | installed |
| `.agents/skills/rebase-branch/SKILL.md` + `references/bug-filing.md`, `test-failure-triage.md` (same source bytes as the `pr-comments-resolve` references, same patches) | installed |
| `.agents/skills/review-tests/SKILL.md` | already installed; one sentence patched |
| `.codex/agents/senior-software-developer.toml`, `test-quality-reviewer.toml`, `remediation-developer.toml` | installed, patched. The Codex body spawns a worker "with <role> instructions"; these files are those instructions |
| `.agents/skills/shared/synchronous-worker-contract.md` | installed, patched |
| `.agents/skills/remediate-pr/`, `.agents/skills/fix-story-bug/`, the other `.codex/agents/*.toml` roles | not installed (same reasons as the Claude side) |

### Install commands

From this repository, then apply the patches below:

```bash
C=2a0416565bbc0a84a8d5f6e7f79361f6cfad9506
for f in .claude/skills/fully-implement-story/SKILL.md \
         .claude/skills/implement-task/SKILL.md \
         .claude/skills/finalize-story-pr/SKILL.md \
         .claude/skills/rebase-branch/SKILL.md \
         .claude/skills/shared/synchronous-worker-contract.md \
         .claude/agents/senior-software-developer.md \
         .claude/agents/test-quality-reviewer.md \
         .claude/agents/remediation-developer.md \
         .agents/skills/fully-implement-story/SKILL.md \
         .agents/skills/fully-implement-story/references/merge-side-effects.md \
         .agents/skills/implement-task/SKILL.md \
         .agents/skills/implement-task/references/commit-attribution.md \
         .agents/skills/implement-task/references/merge-side-effects.md \
         .agents/skills/implement-task/references/test-failure-triage.md \
         .agents/skills/finalize-story-pr/SKILL.md \
         .agents/skills/finalize-story-pr/references/codex-review.md \
         .agents/skills/finalize-story-pr/references/merge-side-effects.md \
         .agents/skills/finalize-story-pr/references/bug-filing.md \
         .agents/skills/finalize-story-pr/references/test-failure-triage.md \
         .agents/skills/rebase-branch/SKILL.md \
         .agents/skills/rebase-branch/references/bug-filing.md \
         .agents/skills/rebase-branch/references/test-failure-triage.md \
         .agents/skills/shared/synchronous-worker-contract.md \
         .codex/agents/senior-software-developer.toml \
         .codex/agents/test-quality-reviewer.toml \
         .codex/agents/remediation-developer.toml; do
  mkdir -p "$(dirname "$f")"
  git -C /home/jon/work/alterna/SAASDK show "$C":"$f" > "$f"
done
```

### Installed files

All files are mode 100644. Hashes are SHA-256.

| Path | Source SHA-256 | Installed |
| --- | --- | --- |
| `.claude/skills/fully-implement-story/SKILL.md` | `e5ab69e8a5e5f898a66a5add82d77d7ed19edec96dd287b78367c5e18796d248` | patched, `2b6e86560b9695ab0bc180e010f587c8f7679b0441b4e35d15f2ab1952fdf97c` |
| `.claude/skills/implement-task/SKILL.md` | `6150675a14a45562452225084f515a289ad76206c4768d19db0162a0f820bcac` | patched, `4353b6e64805b071595597fbae2fc05fb0bd89bbaa5c76f5bd5bb38986d326b8` |
| `.claude/skills/finalize-story-pr/SKILL.md` | `18b8d6338ab6c12d101ddb3d4f070eeec09f4d3197ec063cd6d68926470ff89a` | patched, `d6a8a597e4d32b7c7d52ead2a25754962738611752c62dc17b5383c294a11bf8` |
| `.claude/skills/rebase-branch/SKILL.md` | `b90ef7a3328abb017bd45cd597a87009e5f11c3871270c7c88a195d3c5c2d152` | patched, `595d1d1f0ac9304c7f5115aa88b5cae03aa100813b1236f29dca0c36230bc912` |
| `.claude/skills/review-tests/SKILL.md` | `d3a5632a7c596c9dd3e01cde8d45aff47ca148285314f8baaddabc9e10d1e277` | patched, `7378a2509afe743687fc5bae4af84a63bd57a4e590e0cee0a98fbd659b31597e` (diff in the first section) |
| `.claude/skills/shared/synchronous-worker-contract.md` | `e50222edce13c78bdfe3408532c48f3381d3f646d43aa54bb3ca9b0ed4a4d1f5` | patched, `a1ca35c4e3862a39b7a162263408e009020f3d4d1e5b7165289b3ffa81dfb2a8` |
| `.claude/agents/senior-software-developer.md` | `9fa7a74e9a586f283e15591e5c6b1e25f0903cc1769fd334b9e5880874f0cfb9` | patched, `d3aca028cc1d3bd77dab1be419e28934fab9b91bedd95f04be161c9dd3d1964c` |
| `.claude/agents/test-quality-reviewer.md` | `41da0384cee9a632a3104f1e7d860cabba6dcaddc36bb12de0d9ff3b8456b88d` | patched, `9e358875bdd5c2ccbc0cff7d29f5da5ba4deaccb6687a3a4f4636747e47d73b2` |
| `.claude/agents/remediation-developer.md` | `9346bacdb88acf0c4a01a765e86e3fee4ed04127597817ca1dbeb22323650189` | patched, `95a05dc774a631255719e96d4b9668e5ed51a2f2d98ce1dc003cf586e348c492` |
| `.agents/skills/fully-implement-story/SKILL.md` | `8222b225ac67c8c4545f956a1d161573c08dfd97dcf3e77b0042749a718d544c` | patched, `454482901c6f760223379be7bf823d729275b2a7306482446288f0c5f6e5461c` |
| `.agents/skills/fully-implement-story/references/merge-side-effects.md` | `dd654e761b864b70b888d399c2178e1e2dffa5b639e2c335f5251c4294626881` | byte-identical |
| `.agents/skills/implement-task/SKILL.md` | `1f61ae7c94d2643bd5c7c2acfbed3cc351f3ee2e43cf969542b19bf04c58d3ba` | patched, `e556416002c110761ba16cc929a8a8fd1cf5cef98a4579a795eaace78e0342e2` |
| `.agents/skills/implement-task/references/commit-attribution.md` | `b357f72263d3cd2409fa5d5c6acb1996ed4f9d4543e84db9a01351f28b56b82c` | byte-identical |
| `.agents/skills/implement-task/references/merge-side-effects.md` | `dd654e761b864b70b888d399c2178e1e2dffa5b639e2c335f5251c4294626881` | byte-identical |
| `.agents/skills/implement-task/references/test-failure-triage.md` | `ead945bd22c8f19a5846fcb58f60f6a7cb81ee51d8f98549f5e33bea05026fe2` | patched, `80d9e509228e19a1f81ba4b87a66177f60c70253dfa1b2845d522569b18c1a16` |
| `.agents/skills/finalize-story-pr/SKILL.md` | `99ef2207de16f4469e67704889e2f4a4941b7f5ad322307bb334bcf6bfd12746` | patched, `005e383459f11da98c0ead073869baf6ae9bd9359a2e15e48f8fa2a90142fb0a` |
| `.agents/skills/finalize-story-pr/references/codex-review.md` | `b648438008748b79f6165af45379a530bab9080a85bdf90c513edfd48f817b6c` | byte-identical |
| `.agents/skills/finalize-story-pr/references/merge-side-effects.md` | `96d6a17e6e8c07a3ea41f3a9dc34c101113341af2fd7b78f7b12ba8f6e45aedb` | byte-identical |
| `.agents/skills/finalize-story-pr/references/bug-filing.md` | `59e235596837564368a73182d1b2c918e42e834fd0d2a9f28eb92945686bd836` | patched, `5387dd9400b81051c95a14091546ca48bdab0ed53f66490904552900ffa4ff6c` |
| `.agents/skills/finalize-story-pr/references/test-failure-triage.md` | `8417472ed41d9bfc7e84477acfbd9bd299b0b49ab2e8473c89bd9f74e4e6ed1c` | patched, `ba90a12ff0a98f48596f5ddfbae0df3ad22c0c58d4180ccdccc9430eb37ce6d6` |
| `.agents/skills/rebase-branch/SKILL.md` | `f5a9fa42aeb21a0a54c3860fa6457c170ebd67004e23bd18236251841f1660cf` | patched, `6ca8dc68459eb6104075e08df86f43c58eef6c507a2ac3f6f44650fd67e46c1c` |
| `.agents/skills/rebase-branch/references/bug-filing.md` | `497aa2f56141a0df6457eee65fbfba2f4604ff0bc41c804cd8acdc47eccf33bb` | patched, `af8478c3111e9bfbd33df2a48b61d2a2114d4f366e66a392904d6f7384c7127b` (same bytes as the `pr-comments-resolve` copy) |
| `.agents/skills/rebase-branch/references/test-failure-triage.md` | `8c66fec2e5b1a2aca37129d96affb0540a697620fbbea40e0dde27f6bb2a4ea7` | patched, `7e26298a5c3617ac81aedd669c2a9f430344626f243f6d0e256ef9c2a9155daf` (same bytes as the `pr-comments-resolve` copy) |
| `.agents/skills/review-tests/SKILL.md` | `b2cd4a1487f830fb7a5e8ffdb0785ea9bd360c6456a5283cbaea59a838af1057` | patched, `43ae0b10ff7825c92558f11b78807a1ad463cc3c658ce17c3e1a3a6810ea68ef` (diff in the first section) |
| `.agents/skills/shared/synchronous-worker-contract.md` | `dd040458037facf0b0b461aada42b98147d86cda0dd212027f50eeeb134dbe94` | patched, `d0410efbe2dffaa6efbe151f9dcd200eb7db0705d3d0817a6b44a7b0185c691b` |
| `.codex/agents/senior-software-developer.toml` | `65c7e42b42a7a6f7fb94c89c6c3aa4b873bc08eb032728a0c1929cefc11789a3` | patched, `30e328417c3892ec7e0afd6c34fc68a56e9bea43c4129b929119f0199f6403bb` |
| `.codex/agents/test-quality-reviewer.toml` | `c6edd70bb52d16e67a3f14851ca01a2e4e791e52be3e86991df28c5a197ac9f0` | patched, `98ccc02bcf74b6568e37c28bc48f80e6e879dd26af3ac260338331fa26d4b994` |
| `.codex/agents/remediation-developer.toml` | `cee471b9816f3d267638b183a292fdbadb5947b339ca59d45561eced198cd305` | patched, `ff6268db8242329375ad3aa9f922d64c65f85812ed186661e640176d0d20567c` |

### Consumer-local patches

Every body moves Taiga project 3 to 4 (Claude) or keeps `<verified-project-id>`
(Codex), and replaces hardcoded task status numbers (`11`, `12`, `14`) with
names resolved once per run from `get_task_statuses(project_id=4)`, which works
in full mode here (New, In progress, Ready for test, Closed, Needs Info). The
Codex bodies' `get_filters_data` call becomes `get_task_statuses`, the full-mode
name. The `implement-task` report line becomes `Task status updated to Closed:
✅`, and the orchestrator greps for that exact text. Every `.NET` command
(`dotnet run -- TestUnit`, `Build`, `Format`, `Reset`), `test-results/*.xml`
read, E2E and Stripe step, `docs/design-system.md` read, and
`scripts/devcontainer/launch.sh` sentence is replaced by the unittest command,
`bash -n`, `shellcheck`, or removed. The frontmatter grants change
accordingly. Project 4 has no "Ready for review" or "Blocked" status, so the
orchestrator's Step 9 re-asserts "Ready for test" and `rebase-branch`
escalation adds the `escalation-needed` and `rebase-conflict` tags plus an
assignment instead of a status change. The orchestrator drops the
`/remediate-pr` CI loop in favor of an inline review-thread loop (count
unresolved threads, spawn `remediation-developer` with `pr-comments-resolve`,
at most three passes, then escalate) and deletes the manual-testing, bug-fix,
post-fix monitoring, and retest steps and the `bugs` state key. The agent roles
and Codex TOMLs swap the You-Thon F# persona for this repository's Bash/Python
one, drop the uninstalled skills from their lists, and the anti-pattern list in
`test-quality-reviewer` is rewritten from [docs/testing-strategy.md](testing-strategy.md).
The sentences that say there is no JUnit XML avoid the literal `test-results/`
so that `tests/test_skills.py` can forbid it in the installed closure. Unified diffs:

```diff
--- saasdk/2a04165/.claude/skills/fully-implement-story/SKILL.md
+++ .claude/skills/fully-implement-story/SKILL.md
@@ -1,18 +1,21 @@
 ---
 name: fully-implement-story
-description: Autonomously implement a story end-to-end with agents — implementation, PR monitoring, testing, bug fixing
+description: Autonomously implement a story end-to-end with agents — implementation, test review, PR creation, review-thread remediation
 argument-hint: "<story-ref> [base-branch] [--resume]"
 allowed-tools:
   - Agent
   - Bash(scripts/taiga-story.sh *)
+  - Bash(scripts/taiga-comment.sh *)
   - mcp__taiga-py__*
   - Bash(gh *)
   - Bash(git *)
   - Bash(sleep *)
-  - Bash(python3 scripts/remediate_pr.py *)
-  - Bash(dotnet run -- Reset*)
+  - Bash(date *)
+  - Bash(cat /tmp/*)
+  - Bash(rm -f /tmp/*)
   - Read(//tmp/**)
   - Edit(//tmp/**)
+  - Write(//tmp/**)
   - Read
   - Grep
   - Glob
@@ -20,15 +23,15 @@

 # Fully Implement Story $ARGUMENTS

-Autonomously implement a story end-to-end: task-by-task implementation with fresh agents, PR creation, monitoring, manual testing, bug fixing, and retesting.
+Autonomously implement a story end-to-end: task-by-task implementation with fresh agents, test-quality review, PR creation, rebase check, and review-thread remediation.

 ## Running Unattended

-This skill runs inside a devcontainer spawned by `/implement-epic`. **There is no human present.** You MUST NOT post questions to the user like "what should I do?" or "should I keep retrying?". The skill defines the decision tree; follow it.
+This skill may run headless (`claude -p`) or interactively; either way it does not ask questions. **There is no human present.** You MUST NOT post questions to the user like "what should I do?" or "should I keep retrying?". The skill defines the decision tree; follow it.

 **Every Agent spawn in this skill MUST pass `run_in_background: false`.** This skill runs headless (`claude -p`); if a turn ends while a subagent runs in the background, the CLI can exit and kill the subagent, losing all story work. Foreground spawns keep the turn alive until the agent returns.

-The same trap applies to every other way of leaving work in flight: never resume a subagent with `SendMessage` (it runs in the background), never use `Monitor` or a background Bash task to wait for a subagent, and never end a turn with the expectation that a task notification will wake you — in headless mode there is no next turn, so the CLI reports success and exits with the story unfinished. If a foreground spawn returns early or its build was interrupted, apply the **respawn guard** before spawning a fresh foreground agent for the same task — an early return is not proof the subagent is gone:
+The same trap applies to every other way of leaving work in flight: never resume a subagent with `SendMessage` (it runs in the background), never use `Monitor` or a background Bash task to wait for a subagent, and never end a turn with the expectation that a task notification will wake you — in headless mode there is no next turn, so the CLI reports success and exits with the story unfinished. If a foreground spawn returns early or its test run was interrupted, apply the **respawn guard** before spawning a fresh foreground agent for the same task — an early return is not proof the subagent is gone:
 1. Check the task lock `/tmp/implement-task-<storyRef>-<taskRef>.lock` (written by implement-task). It holds a heartbeat epoch second that the subagent refreshes as it works — never a pid, because `$PPID` inside a Bash tool call is the long-lived `claude` CLI process shared by every subagent, so its liveness would always succeed and the lock of a crashed agent would pin the orchestrator forever. The subagent is still alive only if the heartbeat is under 15 minutes old:
    ```bash
    lock=/tmp/implement-task-<storyRef>-<taskRef>.lock
@@ -36,11 +39,10 @@
    ```
    While it reports `alive`, poll every 30 s in a single Bash call (`timeout: 600000`) until the lock is gone or the heartbeat goes stale. If it is still `alive` when the poll window ends, escalate (`escalationReason = "task #<ref> subagent still running after early return"`) — do not respawn.
 2. Only when the lock is absent or its heartbeat is stale: `rm -f` any stale lock, then spawn the fresh foreground agent.
-3. Additionally refuse to respawn while a build is running in the worktree: check `git status --porcelain` plus `pgrep -x dotnet` (exact name, never `-f`). Two agents in one worktree wipe each other's `bin/` via FAKE `Clean`.
+3. Additionally refuse to respawn while a test run is in progress in the worktree: check `git status --porcelain` plus `pgrep -x python3` (exact name, never `-f`) for a unittest run.

 Decision rules when things go wrong:
-- CI flaky but under 5 failures: invoke `/remediate-pr` again. Let the script run its stability check.
-- `/remediate-pr` returns ESCALATED: write `phase = "escalated"` with `escalationReason` and STOP.
+- Review threads still unresolved after the Step 4 pass limit: write `phase = "escalated"` with `escalationReason` and STOP.
 - Agent blocked by a permission denial or tool error: write `phase = "escalated"` with the specific reason and STOP.
 - Uncertainty about proceeding: write `phase = "escalated"` with `escalationReason = "uncertain: <what>"` and STOP. Do not ask.

@@ -48,9 +50,9 @@
 - `"complete"` — all steps succeeded, PR ready for review
 - `"escalated"` — any reason, with populated `escalationReason`

-If you would write any other phase (e.g., `"monitoring"`, `"fixing"`, `"testing"`) as your final action, you are doing it wrong — escalate instead.
+If you would write any other phase (e.g., `"monitoring"`) as your final action, you are doing it wrong — escalate instead.

-The phase write is its own Bash call. Never combine it with `dotnet run -- Reset`, `pkill`, or any other cleanup; `Reset` already stops Projector/Watchdog, so no manual `pkill` is ever needed. A `pkill -f` in the same call self-matches the shell and kills it before the write lands.
+The phase write is its own Bash call. Never combine it with `pkill` or any other cleanup. A `pkill -f` in the same call self-matches the shell and kills it before the write lands.

 ## Step 0: Parse arguments

@@ -72,12 +74,12 @@

 **Resume check — do this before anything else in Step 1.** You are resuming when `--resume` is present, or when `/tmp/fully-implement-<ref>.json` already exists with a non-terminal `phase` (an interactive re-invoke). The story is already In progress with work on disk: do not start over, and do not ask — resume.

-1. Recover the state. If `/tmp/fully-implement-<ref>.json` exists, read it and do not overwrite it. If it does not (the container was replaced; the clone survived), rebuild it from what is on disk and in Taiga:
+1. Recover the state. If `/tmp/fully-implement-<ref>.json` exists, read it and do not overwrite it. If it does not (the checkout survived but the state file did not), rebuild it from what is on disk and in Taiga:
    - `featureBranch`: `git branch -a --format='%(refname:short)' | grep -E '^(origin/)?feature/.+-<ref>$'` — the anchored match matters for the reasons given in 1c.1; drop a leading `origin/` from the match. The branch may exist only locally.
    - Look up any existing PR once: `gh pr list --head <branch> --state all --json number,baseRefName --jq '.[0]'` (null if none).
-   - `baseBranch`: the existing PR's `baseRefName` from the lookup above, if a PR was found — the PR already records the base it was opened against, so this survives a relaunch that passes only `<ref>` (e.g. `/implement-epic` retrying after replacing the container). Otherwise, `<base-branch>` from Step 0 (the argument if given, otherwise the `defaultBranchRef` lookup).
+   - `baseBranch`: the existing PR's `baseRefName` from the lookup above, if a PR was found — the PR already records the base it was opened against, so this survives a relaunch that passes only `<ref>`. Otherwise, `<base-branch>` from Step 0 (the argument if given, otherwise the `defaultBranchRef` lookup).
    - `prNumber`: the existing PR's `number` from the lookup above (null if none).
-   - `tasksCompleted` / `tasksTotal`: from `scripts/taiga-story.sh <ref> 3 --with-tasks` — tasks with `status == 14` (Closed) are done; each implement-task run closes its task on completion. Open tasks whose description has a `## Gate` section (fetch each with `get_task(task_id=<task_id>)`; the listing omits descriptions) also count as done: they stay open by design (see [`../shared/merge-side-effects.md`](../shared/merge-side-effects.md)).
+   - `tasksCompleted` / `tasksTotal`: from `scripts/taiga-story.sh <ref> 4 --with-tasks` — tasks with `status_extra_info.is_closed == true` are done; each implement-task run closes its task on completion. Open tasks whose description has a `## Gate` section (fetch each with `get_task(task_id=<task_id>)`; the listing omits descriptions) also count as done: they stay open by design (see [`../shared/merge-side-effects.md`](../shared/merge-side-effects.md)).
    - `phase`: `"monitoring"` if a PR exists and is open, else `"implementing"`.
    - Write the block from 1d with those values.
 2. Skip 1a's status validation (the story is no longer "Ready") — just fetch the story and its tasks for context.
@@ -88,21 +90,21 @@

 ### 1a. Fetch and validate the story

-1. Find the story and its tasks: `scripts/taiga-story.sh <ref> 3 --with-tasks` — returns story JSON with `tasks` array included. Extract `id` and `tasks`.
+1. Find the story and its tasks: `scripts/taiga-story.sh <ref> 4 --with-tasks` — returns story JSON with `tasks` array included. Extract `id` and `tasks`.
 2. If the matching story is closed/done, inform the user and stop
 3. Fetch full story details: `get_user_story(user_story_id=<id>)` — verify it has the `llm-analyzed` tag
 4. If not "Ready" status or not analyzed, inform the user and stop

 ### 1b. Fetch metadata

-1. Fetch story statuses: `get_user_story_statuses(project_id=3)` — identify "In progress", "Ready for test", and "Ready for review" IDs
-2. Fetch project members: `get_project_members(project_id=3)` — identify Jon's user ID (bigjonroberts)
+1. Fetch story statuses: `get_user_story_statuses(project_id=4)` — identify the `In progress` and `Ready for test` IDs by exact name (project 4 has no "Ready for review" status). Resolve task status IDs with `get_task_statuses(project_id=4)` — `New` and `Closed` by exact name — and keep them as `<new_task_status_id>` and `<closed_task_status_id>` for Step 2. Never hardcode a numeric ID.
+2. Fetch project members: `get_project_members(project_id=4)` — identify Jon's user ID (bigjonroberts)

 ### 1c. Set up branch

 1. Check for existing branch: `git branch -a --format='%(refname:short)' | grep -E '^(origin/)?feature/.+-<ref>$'` — anchoring on the `feature/<slug>-<ref>` convention this skill creates is what keeps the match to this story's own branch. An unanchored substring match on the bare ref also matches the base branch the clone is sitting on when that name ends in this story's ref (a multi-parent story is cloned onto `epic/<epic-ref>-integration-<ref>`), and it matches longer refs too (`274` matches `feature/x-2745`). A base branch is never this story's own branch.
 2. If branch exists: `git checkout <branch-name> && git pull` — `<branch-name>` is the match with any leading `origin/` dropped, so that `git checkout` creates the tracking branch.
-3. If no branch: `git fetch origin +<base-branch>:refs/remotes/origin/<base-branch> && git checkout -b feature/<slug>-<ref> origin/<base-branch>` — fetching the named ref explicitly (not a bare `git fetch origin`, and not `git fetch origin <base-branch>` alone) matters in the shallow single-branch clones `scripts/devcontainer/launch.sh` creates: the clone's `remote.origin.fetch` refspec is restricted to the branch it was cloned from, so a bare fetch never retrieves a stacked predecessor's branch, and fetching the ref without a destination only populates `FETCH_HEAD` — the `:refs/remotes/origin/<base-branch>` destination is what creates the `origin/<base-branch>` ref this command consumes.
+3. If no branch: `git fetch origin +<base-branch>:refs/remotes/origin/<base-branch> && git checkout -b feature/<slug>-<ref> origin/<base-branch>` — fetch the named ref explicitly (not a bare `git fetch origin`, and not `git fetch origin <base-branch>` alone): a bare fetch does not retrieve a stacked predecessor's branch when the clone's `remote.origin.fetch` refspec is restricted, and fetching the ref without a destination only populates `FETCH_HEAD` — the `:refs/remotes/origin/<base-branch>` destination is what creates the `origin/<base-branch>` ref this command consumes.

 ### 1d. Initialize state file

@@ -120,18 +122,17 @@
   "featureBranch": "<branch-name>",
   "baseBranch": "<base-branch>",
   "tasksCompleted": 0,
-  "openTaskIds": [<ids of tasks with status != 14>],
+  "openTaskIds": [<ids of tasks whose status_extra_info.is_closed is false>],
   "tasksTotal": <length of openTaskIds>,
   "verifiedTaskIds": [],
   "preSpawnTip": null,
-  "bugs": [],
   "testReviewComplete": false,
   "escalated": false,
   "escalationReason": null
 }
 ```

-`openTaskIds` (and therefore `tasksTotal`) holds only the tasks still open at the start of this run: tasks Closed by a prior attempt (the epic orchestrator re-queues escalated stories and discards the state file between attempts) are not re-implemented, so counting them would make the Step 2 completion gate unsatisfiable.
+`openTaskIds` (and therefore `tasksTotal`) holds only the tasks still open at the start of this run: tasks Closed by a prior attempt are not re-implemented, so counting them would make the Step 2 completion gate unsatisfiable.

 ### 1e. Set story to "In progress"

@@ -144,18 +145,18 @@
 1. **Record the branch tip, then spawn a fresh `senior-software-developer` agent:**
    - Before spawning: run `git rev-parse <branch-name>` (the current directory is the checkout, as for every other git command in this skill) and store the result in the state file as `preSpawnTip`. Shell variables do not survive across tool calls, so the check below substitutes the literal SHA from the state file.
    - `subagent_type: "senior-software-developer"`
-   - `model: "sonnet"` — only this spawn is overridden: the analyzed task supplies a file-level plan and TDD, while the Opus `test-quality-reviewer` and CI remediation catch mistakes downstream; finalize, rebase, and bug-fix spawns stay on the agent's Opus pin.
+   - `model: "sonnet"` — only this spawn is overridden: the analyzed task supplies a file-level plan and TDD, while the Opus `test-quality-reviewer` and review-thread remediation catch mistakes downstream; finalize and rebase spawns stay on the agent's Opus pin.
    - `run_in_background: false`
    - Prompt: `"Implement the next task for story #<ref> on branch <branch-name>. Follow the implement-task skill instructions with arguments '<ref> <branch-name> <base-branch>'."`

-2. **When agent returns**, verify the branch, not the report. Report formatting is known-flaky (bug #1840), so the completion signal is `git rev-list <preSpawnTip>..<branch-name>` (substitute `<preSpawnTip>` from the state file): non-empty output means the task's commit landed, whatever SHA the report cites; empty output means the agent returned before finishing (bug #2572). Docs/config-only tasks still commit, so a landed commit is always expected.
+2. **When agent returns**, verify the branch, not the report. Report formatting is known-flaky, so the completion signal is `git rev-list <preSpawnTip>..<branch-name>` (substitute `<preSpawnTip>` from the state file): non-empty output means the task's commit landed, whatever SHA the report cites; empty output means the agent returned before finishing. Docs/config-only tasks still commit, so a landed commit is always expected.
    - If output contains "BLOCKED:" → the agent hit a permission denial or other unrecoverable issue. Escalate: set `phase = "escalated"`, `escalationReason = "agent blocked: <details>"`, tag story with `escalation-needed`, assign to Jon, and **STOP**.
-   - If output contains one or more `GATED: <task-ref> <reason>` lines → each named task is left open by design and counts as finished, not failed, so never retry it. Resolve each ref to its id with `scripts/taiga-story.sh <ref> 3 --with-tasks`; for every id not already in `verifiedTaskIds`, append it to `verifiedTaskIds`, increment `tasksCompleted`, and write the state file. A gated task lands no commit, so when the report gates a task and claims nothing else, skip the `rev-list` checks below and continue the loop. Carry the `GATED:` lines into the final report. See [`../shared/merge-side-effects.md`](../shared/merge-side-effects.md).
+   - If output contains one or more `GATED: <task-ref> <reason>` lines → each named task is left open by design and counts as finished, not failed, so never retry it. Resolve each ref to its id with `scripts/taiga-story.sh <ref> 4 --with-tasks`; for every id not already in `verifiedTaskIds`, append it to `verifiedTaskIds`, increment `tasksCompleted`, and write the state file. A gated task lands no commit, so when the report gates a task and claims nothing else, skip the `rev-list` checks below and continue the loop. Carry the `GATED:` lines into the final report. See [`../shared/merge-side-effects.md`](../shared/merge-side-effects.md).
    - If output contains "All tasks complete" **and** the state file has `tasksCompleted == tasksTotal` → break loop, go to Step 2a. If `tasksCompleted < tasksTotal`, the sentinel is not trusted — a worker closed a task in Taiga without landing its commit — so treat it exactly like an empty `rev-list` and enter the recovery path below.
-   - `rev-list` non-empty → the work landed. Re-fetch tasks with `scripts/taiga-story.sh <ref> 3 --with-tasks` and find the task at status 14 whose id is in `openTaskIds` but not yet in `verifiedTaskIds`:
+   - `rev-list` non-empty → the work landed. Re-fetch tasks with `scripts/taiga-story.sh <ref> 4 --with-tasks` and find the task with `status_extra_info.is_closed == true` whose id is in `openTaskIds` but not yet in `verifiedTaskIds`:
      - Found → read state file, append its id to `verifiedTaskIds`, increment `tasksCompleted`, write state file, continue loop.
-     - None found → the commit landed but Taiga was not updated (the report carries `Task status updated to Closed (status 14): ❌`, or omits the line). Do **not** re-spawn — the retry would re-implement the task and double-count it. Close it from here using the task ref named in the report: `update_task(task_id=<task_id>, kwargs={"status": 14})`, then `get_task(task_id=<task_id>)` to confirm status 14. Confirmed → record it as above and continue. Still not 14 → escalate (`phase = "escalated"`, `escalationReason = "update_task failed for task #<task_ref> after its commit landed"`) and **STOP**.
-   - `rev-list` empty (or the untrusted sentinel above) → recover once. Identify the stranded task from Taiga rather than the report, which on the sentinel route names no task: re-fetch tasks with `scripts/taiga-story.sh <ref> 3 --with-tasks`; every task at status 14 whose id is in `openTaskIds` but not in `verifiedTaskIds` was closed without a landed commit, so reopen each with `update_task(task_id=<task_id>, kwargs={"status": 12})` so the retry picks it up instead of reporting "All tasks complete". Then record a fresh `preSpawnTip` and re-spawn the task agent. The retry is subject to the same `rev-list` check — an "All tasks complete" reply from the retry counts as a failure (it falls through the `tasksCompleted < tasksTotal` gate above), because the retried task cannot be complete without a landed commit. If the retry also lands nothing, escalate (`phase = "escalated"`, `escalationReason = "task agent returned without a landed commit"`) and **STOP**.
+     - None found → the commit landed but Taiga was not updated (the report carries `Task status updated to Closed: ❌`, or omits the `Task status updated to Closed: ✅` line). Do **not** re-spawn — the retry would re-implement the task and double-count it. Close it from here using the task ref named in the report: `update_task(task_id=<task_id>, kwargs={"status": <closed_task_status_id>})`, then `get_task(task_id=<task_id>)` to confirm the status equals `<closed_task_status_id>`. Confirmed → record it as above and continue. Still not Closed → escalate (`phase = "escalated"`, `escalationReason = "update_task failed for task #<task_ref> after its commit landed"`) and **STOP**.
+   - `rev-list` empty (or the untrusted sentinel above) → recover once. Identify the stranded task from Taiga rather than the report, which on the sentinel route names no task: re-fetch tasks with `scripts/taiga-story.sh <ref> 4 --with-tasks`; every task with `status_extra_info.is_closed == true` whose id is in `openTaskIds` but not in `verifiedTaskIds` was closed without a landed commit, so reopen each with `update_task(task_id=<task_id>, kwargs={"status": <new_task_status_id>})` so the retry picks it up instead of reporting "All tasks complete". Then record a fresh `preSpawnTip` and re-spawn the task agent. The retry is subject to the same `rev-list` check — an "All tasks complete" reply from the retry counts as a failure (it falls through the `tasksCompleted < tasksTotal` gate above), because the retried task cannot be complete without a landed commit. If the retry also lands nothing, escalate (`phase = "escalated"`, `escalationReason = "task agent returned without a landed commit"`) and **STOP**.

 3. Each agent gets a completely fresh context window — no accumulated state from previous tasks.

@@ -163,15 +164,15 @@

 ## Step 2a: Verify all tasks are Closed in Taiga

-Safety net for the known-flaky `implement-task` compliance with its Step 6 (bug #1840). Before proceeding to test-quality review, confirm every task on the story is at status 14 (Closed). If any aren't, force-close them now.
+Safety net for the known-flaky `implement-task` compliance with its Step 6. Before proceeding to test-quality review, confirm every task on the story is Closed. If any aren't, force-close them now.

-1. Re-fetch the story with tasks: `scripts/taiga-story.sh <ref> 3 --with-tasks`
-2. For each task in the returned `tasks` array where `status != 14`, except a task reported `GATED:` or whose description has a `## Gate` section (fetch each with `get_task(task_id=<task_id>)`; the `--with-tasks` listing omits descriptions). Those stay open by design — list them in the final report under "Tasks left open by design: #<ref>, #<ref>". Close every other one:
+1. Re-fetch the story with tasks: `scripts/taiga-story.sh <ref> 4 --with-tasks`
+2. For each task in the returned `tasks` array where `status_extra_info.is_closed == false`, except a task reported `GATED:` or whose description has a `## Gate` section (fetch each with `get_task(task_id=<task_id>)`; the `--with-tasks` listing omits descriptions). Those stay open by design — list them in the final report under "Tasks left open by design: #<ref>, #<ref>". Close every other one:
    ```
-   update_task(task_id=<task_id>, kwargs={"status": 14})
+   update_task(task_id=<task_id>, kwargs={"status": <closed_task_status_id>})
    ```
    Log each one you closed here, in the final orchestrator report under "Tasks auto-closed by safety net: #<ref>, #<ref>".
-3. **Verify the updates succeeded** by re-fetching the story with tasks: `scripts/taiga-story.sh <ref> 3 --with-tasks`. Confirm every task other than the gated ones now has `status == 14`. If any task's `update_task` call failed (status still not 14 after the update), escalate: set `phase = "escalated"`, `escalationReason = "safety net update_task failed for task #<ref>"`, and **STOP**.
+3. **Verify the updates succeeded** by re-fetching the story with tasks: `scripts/taiga-story.sh <ref> 4 --with-tasks`. Confirm every task other than the gated ones now has `status_extra_info.is_closed == true`. If any task's `update_task` call failed (still open after the update), escalate: set `phase = "escalated"`, `escalationReason = "safety net update_task failed for task #<ref>"`, and **STOP**.
 4. Proceed to Step 2b regardless of how many tasks needed closing (as long as all but the gated ones are now confirmed Closed).

 Finding open stragglers is routine cleanup, not a failure signal — do NOT escalate merely because tasks were found open. But if `update_task` fails (the task remains open after the update attempt), that IS a failure — escalate. File a separate bug only if the same task keeps reappearing as "open" across multiple runs (which would indicate a deeper issue).
@@ -216,119 +217,36 @@
    b. When agent returns, check its output:
       - If the rebase was escalated (conflict too complex), set `phase = "escalated"`, `escalationReason = "rebase conflict escalated"`, and **STOP**.
       - If the rebase succeeded, proceed.
-   c. **After rebase, the full pipeline must re-run**: proceed to Step 4 (monitoring), then Step 5 (testing), etc. — even if testing was already done before the rebase, since new code from the base branch may change behavior. Each `/remediate-pr` invocation starts with a fresh failure count, so no manual reset is needed.
+   c. **After rebase, the remaining pipeline must re-run**: proceed to Step 4 even if review threads were already checked before the rebase, since new code from the base branch may have drawn new comments.
 3. If result is `"CLEAN"` or `"HAS_HOOKS"`, proceed to Step 4.

-**Also run this check** at the start of Step 7 (post-fix monitoring) — bug fix sub-PRs merged into the feature branch may have advanced the base branch.
+## Step 4: Review-thread remediation (no CI gate)

-## Step 4: PR monitoring and remediation
+This repository has no CI; the suite run in finalize-story-pr is the gate, so do not poll `gh pr checks`.

-Delegate to the `/remediate-pr` skill to handle the CI monitoring + remediation loop. The `/remediate-pr` skill delegates to `scripts/remediate_pr.py` for all deterministic operations (stability monitoring, failure counting, state management) and only invokes Claude agents for build fixes and comment resolution. Follow the instructions in `.claude/skills/remediate-pr/SKILL.md` with arguments:
-
-```
-<prNumber> --taiga-id <storyId> --taiga-type story --max-failures 5
-```
-
-When the remediation loop returns:
-- **`STABLE`**: Proceed to Step 5
-- **`ESCALATED`**: Set `phase = "escalated"`, `escalationReason = "5+ build failures"`, shut down the app (`dotnet run -- Reset`), and **STOP**
-
-## Step 5: Manual testing phase
-
-1. Update state file: `phase = "testing"`
-2. Spawn `senior-manual-testing-specialist` agent:
-   - `subagent_type: "senior-manual-testing-specialist"`
+1. Count unresolved review threads with the GraphQL query from `.claude/skills/pr-comments-resolve/SKILL.md` Step 1 (`reviewThreads(first: 100) { nodes { id isResolved ... } }`, substituting the owner, repo, and `<prNumber>`), filtering for `isResolved == false`.
+2. If the count is zero: the PR is STABLE — go to Step 9.
+3. Otherwise spawn a fresh `remediation-developer` agent:
+   - `subagent_type: "remediation-developer"`
    - `run_in_background: false`
-   - Prompt includes:
-     - Story ref, story subject, and acceptance criteria (from the story description)
-     - PR number
-     - App URL: `http://localhost:8080` (or `http://localhost:5000` if backend-only)
-     - "This is the **first pass**. Test all acceptance criteria and edge cases. File bugs in Taiga for any deficiencies found."
-
-3. When agent returns, shut down the app: `dotnet run -- Reset`
-4. Check its output:
-   - If no bugs filed → proceed to Step 9 (success)
-   - If bugs filed → extract bug refs from output, add to state file `bugs` array with status `"filed"`, proceed to Step 6
-
-## Step 6: Bug fixing phase
-
-1. Update state file: `phase = "fixing"`
-2. For each bug in `state.bugs` where status is `"filed"`:
-
-   a. **Spawn `senior-software-developer` agent:**
-      - `subagent_type: "senior-software-developer"`
-      - `run_in_background: false`
-      - Prompt: `"Fix bug #<ref> on feature branch <featureBranch>. Follow the fix-story-bug skill instructions with arguments '<ref> <featureBranch>'."`
-
-   b. When agent returns, extract sub-PR number from output.
-
-   c. Update bug in state file: `status = "sub-pr-monitoring"`, `subPrNumber = <number>`, `subBranch = "fix/<slug>-<ref>"`
+   - Prompt: `"Resolve comments on PR #<prNumber>. Follow the pr-comments-resolve skill instructions with argument '<prNumber>'."`

-   d. **Monitor the sub-PR** by following the `/remediate-pr` skill instructions (`.claude/skills/remediate-pr/SKILL.md`) with arguments: `<sub-pr-number> --taiga-id <storyId> --taiga-type story --max-failures 5`. If it returns `ESCALATED`, set `phase = "escalated"`, shut down the app (`dotnet run -- Reset`), and **STOP**.
+   When it returns, re-run step 1.
+4. Allow at most 3 passes. If threads remain unresolved after the third pass: set `phase = "escalated"`, `escalationReason = "review threads unresolved after 3 passes"`, tag the story `escalation-needed` (re-fetch the story with `get_user_story(user_story_id=<id>)` first and append `["escalation-needed", null]` to its current tags in `update_user_story`), assign the story to Jon, post `gh pr comment <prNumber> --body "Escalating to @bigjonroberts — review threads remain unresolved."`, and **STOP**.

-   e. When remediation returns `STABLE`:
-      - Merge sub-PR: `gh pr merge <sub-pr-number> --squash --delete-branch`
-      - Update bug status to `"merged"` in state file
-      - Move bug in Taiga to "Ready for test": fetch issue statuses, then `update_issue(issue_id=<id>, kwargs={"status": <ready_for_test_id>})`
-
-3. When all bugs have status `"merged"`, proceed to Step 7.
-
-## Step 7: Post-fix monitoring
-
-1. Update state file: `phase = "post-fix-monitoring"`
-2. Delegate to the `/remediate-pr` skill to handle post-fix CI monitoring. Follow the instructions in `.claude/skills/remediate-pr/SKILL.md` with arguments:
-
-   ```
-   <prNumber> --taiga-id <storyId> --taiga-type story --max-failures 5
-   ```
-
-   When the remediation loop returns:
-   - **`STABLE`**: Proceed to Step 8
-   - **`ESCALATED`**: Set `phase = "escalated"`, `escalationReason = "5+ post-fix build failures"`, shut down the app (`dotnet run -- Reset`), and **STOP**
-
-## Step 8: Second-pass testing
-
-1. Update state file: `phase = "retesting"`
-2. Spawn `senior-manual-testing-specialist` agent:
-   - `subagent_type: "senior-manual-testing-specialist"`
-   - `run_in_background: false`
-   - Prompt includes:
-     - Story ref, story subject, and acceptance criteria
-     - PR number
-     - App URL
-     - "This is the **second pass**. Re-test each fixed bug and the original acceptance criteria."
-     - List of bug refs to verify
-
-3. When agent returns, check its output:
-   - **If issues found** (comments left on PR):
-     - Set `phase = "escalated"`, `escalationReason = "second-pass testing found issues"`
-     - Tag story with `escalation-needed`
-     - Assign story to Jon
-     - Post PR comment: `"Escalating to @bigjonroberts — second-pass testing found unresolved issues."`
-     - Shut down the app: `dotnet run -- Reset`
-     - **STOP**
-   - **If no issues** → proceed to Step 9
+There is no manual-testing phase in this repository: it has no application to exercise.

 ## Step 9: Success

-1. Update state file: `phase = "complete"` — its own Bash call, never combined with `Reset` or any kill
-2. **Close verified bugs**: If `state.bugs` is non-empty, fetch issue statuses (`get_issue_statuses(project_id=3)`) and find the "Closed" status ID. For each bug with status `"merged"`:
-   ```
-   update_issue(issue_id=<bug_id>, status=<closed_status_id>, kwargs={
-       "comment": "Verified fixed — second-pass testing passed. Closed by fully-implement-story orchestrator."
-   })
-   ```
-   Update bug status to `"closed"` in state file.
-3. Update story status to "Ready for review": `update_user_story(user_story_id=<id>, kwargs={"status": <ready_for_review_id>})`
-4. Assign story to Jon: `assign_user_story_to_user(user_story_id=<id>, user_id=<jon_id>)`
-5. Add PR link to Taiga story as a comment:
-   `scripts/taiga-comment.sh <id> "PR: https://github.com/Alterna-Dev-Studio/you-thon/pull/<prNumber>"`
-6. Post PR comment:
+1. Update state file: `phase = "complete"` — its own Bash call, never combined with any kill
+2. Re-assert the story status "Ready for test" (finalize-story-pr already set it; this guards against a later change): `update_user_story(user_story_id=<id>, kwargs={"status": <ready_for_test_id>})`
+3. Assign story to Jon: `assign_user_story_to_user(user_story_id=<id>, user_id=<jon_id>)`
+4. Add the PR link to the Taiga story as a comment only if finalize-story-pr's report does not show that it already posted one: `scripts/taiga-comment.sh <id> "PR: <url>"` with `<url>` from `gh pr view <prNumber> --json url -q .url`.
+5. Post PR comment:
    ```
-   gh pr comment <number> --body "Story implementation complete. All checks passing, all comments resolved, manual testing passed. Ready for review."
+   gh pr comment <prNumber> --body "Story implementation complete. Test suite passing, all review threads resolved. Ready for Jon to review."
    ```
-7. Shut down the app: `dotnet run -- Reset` — its own Bash call; no manual `pkill` (`Reset` stops Projector/Watchdog)
-8. Report success to user with PR link, the base branch this run used, and whether it came from the argument or the `defaultBranchRef` lookup.
+6. Report success to user with PR link, the base branch this run used, and whether it came from the argument or the `defaultBranchRef` lookup.

 ## Error handling

@@ -340,9 +258,5 @@
 The resume check at the top of Step 1 decides whether this run resumes (`--resume` in the arguments, or an existing non-terminal state file) and recovers the state. It then jumps to the step for `phase`:
   - `"implementing"` → Step 2 (or Step 2b if all tasks are done but `testReviewComplete` is false)
   - `"monitoring"` → Step 3b (rebase check), then Step 4
-  - `"testing"` → Step 5
-  - `"fixing"` → Step 6
-  - `"post-fix-monitoring"` → Step 3b (rebase check), then Step 7
-  - `"retesting"` → Step 8

-On resume, `<base-branch>` comes from the state file's `baseBranch` key, not from re-resolving Step 0 or assuming `main` — this matters because the `"monitoring"` and `"post-fix-monitoring"` entry points both land on Step 3b, which spawns `/rebase-branch`. If the state file predates this key (written before this change), fall back to the `defaultBranchRef` lookup from Step 0.
+On resume, `<base-branch>` comes from the state file's `baseBranch` key, not from re-resolving Step 0 or assuming `main` — this matters because the `"monitoring"` entry point lands on Step 3b, which spawns `/rebase-branch`. If the state file predates this key (written before this change), fall back to the `defaultBranchRef` lookup from Step 0.

--- saasdk/2a04165/.claude/skills/implement-task/SKILL.md
+++ .claude/skills/implement-task/SKILL.md
@@ -8,19 +8,17 @@
   - mcp__taiga-py__update_user_story
   - mcp__taiga-py__get_task
   - mcp__taiga-py__update_task
-  - Bash(dotnet run *)
-  - Bash(dotnet build *)
-  - Bash(dotnet paket *)
-  - Bash(dotnet fantomas *)
-  - Bash(dotnet tool *)
-  - Bash(dotnet reportgenerator *)
+  - mcp__taiga-py__get_task_statuses
+  - Bash(python3 -m unittest *)
+  - Bash(timeout 590 python3 -m unittest *)
+  - Bash(bash -n *)
+  - Bash(shellcheck *)
+  - Bash(date *)
+  - Bash(rm -f /tmp/implement-task-*)
   - Bash(git *)
   - Bash(gh *)
   - Bash(find *)
   - Bash(xargs grep *)
-  - Bash(npm *)
-  - Bash(npx *)
-  - Bash(docker *)
   - Bash(ls *)
   - Read(//tmp/**)
   - Read
@@ -28,11 +26,8 @@
   - Write
   - Grep
   - Glob
-  - WebFetch(https://www.nuget.org/*)
   - WebFetch(https://github.com/*)
   - WebFetch(https://raw.githubusercontent.com/*)
-  - WebFetch(https://learn.microsoft.com/*)
-  - WebFetch(https://opentelemetry.io/*)
 ---

 # Implement Task — Story #$ARGUMENTS
@@ -52,7 +47,7 @@
 Check out the branch:
 1. `git checkout <branch-name> && git pull`
 2. If the branch doesn't exist locally: `git fetch origin <branch-name> && git checkout <branch-name>`
-3. If it doesn't exist at all: `git fetch origin +<base>:refs/remotes/origin/<base> && git checkout -b <branch-name> origin/<base>` — this fallback only fires if the branch-creation step in the calling skill (`/fully-implement-story` or `/implement-story`) was skipped or failed, since normally the branch already exists by the time this skill runs. Fetch `<base>` explicitly with the `:refs/remotes/origin/<base>` destination rather than a bare `git fetch origin`: in the shallow single-branch clones `scripts/devcontainer/launch.sh` creates, the clone's `remote.origin.fetch` refspec is restricted to the cloned branch, so a bare fetch never retrieves `<base>`, and fetching it without a destination only populates `FETCH_HEAD`, not the `origin/<base>` ref this command consumes.
+3. If it doesn't exist at all: `git fetch origin +<base>:refs/remotes/origin/<base> && git checkout -b <branch-name> origin/<base>` — this fallback only fires if the branch-creation step in the calling skill (`/fully-implement-story` or `/implement-story`) was skipped or failed, since normally the branch already exists by the time this skill runs.

 Then write the task lock as its own Bash call so the orchestrator can tell you are still alive:
 ```bash
@@ -62,9 +57,9 @@

 ## Step 2: Fetch story and find next task

-1. Find the story and its tasks: `scripts/taiga-story.sh <story-ref> 3 --with-tasks` — returns story JSON with `tasks` array included. Extract `id` and `tasks`.
+1. Find the story and its tasks: `scripts/taiga-story.sh <story-ref> 4 --with-tasks` — returns story JSON with `tasks` array included. Extract `id` and `tasks`.
 2. Fetch full story details: `get_user_story(user_story_id=<id>)` for context
-3. Find the first task whose status is NOT done (status != 14) and whose description has no `## Gate` section (fetch each candidate with `get_task(task_id=<id>)` to check). If no such task remains, report **"All tasks complete"**, add one `GATED: <task-ref> <reason>` line for each open task that has a `## Gate` section, apply the tag removal from "Gated tasks" below if any are listed, and return.
+3. Find the first task whose status is NOT done (`status_extra_info.is_closed == false`) and whose description has no `## Gate` section (fetch each candidate with `get_task(task_id=<id>)` to check). If no such task remains, report **"All tasks complete"**, add one `GATED: <task-ref> <reason>` line for each open task that has a `## Gate` section, apply the tag removal from "Gated tasks" below if any are listed, and return.
 4. Fetch full task details: `get_task(task_id=<id>)` for the description/implementation plan

 ### Gated tasks
@@ -75,19 +70,12 @@
 2. Remove the `close-tasks-on-merge` and `mark-done-on-merge` tags from the story if present: re-fetch it with `get_user_story(user_story_id=<story-id>)`, then `update_user_story(user_story_id=<story-id>, kwargs={"tags": <every current tag except those two>})`. An open task means neither signal holds (see [`../shared/merge-side-effects.md`](../shared/merge-side-effects.md)).
 3. Discard any uncommitted work for the task, skip Steps 3–6, and report `GATED: <task-ref> <reason>` in Step 7 in place of the commit SHA and Taiga status lines. The orchestrator counts a gated task as finished, not failed.

-**NEVER call MCP tools (e.g., `list_tasks`) directly to find tasks. ALWAYS use `scripts/taiga-story.sh <story-ref> 3 --with-tasks` — it hardcodes the correct project_id.**
+**NEVER call MCP tools (e.g., `list_tasks`) directly to find tasks. ALWAYS use `scripts/taiga-story.sh <story-ref> 4 --with-tasks` — it hardcodes the correct project_id.**

-**The Taiga project_id for this project is ALWAYS 3. Never guess or use any other project ID.**
-
-**Task status IDs (hardcoded, do NOT call `get_task_statuses`):**
-- 11 = New
-- 12 = In progress
-- 14 = Closed/Done — use this in Step 6
+The Taiga project for this repository is 4 (see AGENTS.md). Resolve task status IDs once per run by exact name from `get_task_statuses(project_id=4)` — `New`, `In progress`, `Closed` — and cross-check with `status_extra_info.name` / `status_extra_info.is_closed` in the `taiga-story.sh` listing. Never hardcode a numeric ID. `<closed_task_status_id>` below is the ID whose name is exactly `Closed`.

 ## Step 3: Implement the task

-**If the task involves UI changes**, read `docs/design-system.md` before writing any view code. Follow established color tokens, typography, spacing, component patterns, and the `tw` helper conventions documented there.
-
 1. **If the task description contains a detailed implementation plan** (files to change, implementation details, specific code patterns), skip investigation entirely. Read only the files listed in the plan, then go straight to TDD.
 2. **If there is no implementation plan**, investigate the codebase as needed.
 3. Implement via TDD:
@@ -99,7 +87,7 @@

 ## Step 4: Run tests

-Run **only the directly affected test suite(s)** — not `TestAll`. Consult [docs/testing-workflow.md](../../../docs/testing-workflow.md) for the local-vs-CI policy and file-to-command routing (including Stripe exception rules).
+Run the consumer suite: `timeout 590 python3 -m unittest discover -s tests -v; echo "exit=$?"` in the foreground with the Bash tool `timeout: 600000`. Run `bash -n` and `shellcheck` on any changed Bash file. See [docs/testing-workflow.md](../../../docs/testing-workflow.md); this repository has no CI gate, so this run is the gate.

 Refresh the task-lock heartbeat immediately before and after the run, each as its own Bash call, so a long suite is not mistaken for a dead agent:
 ```bash
@@ -108,11 +96,11 @@

 Run the suite in the foreground with an explicit exit-code capture:
 ```bash
-timeout 1500 dotnet run -- TestUnit; echo "exit=$?"
+timeout 590 python3 -m unittest discover -s tests -v; echo "exit=$?"
 ```
 Never wait with a `kill -0 $(pgrep -f ...)` loop — `pgrep -f` matches the loop's own shell and never exits (see `AGENTS.md` "Process Hygiene").

-Read the relevant `test-results/*.xml` file for pass/fail status. Parse `<testsuite>` attributes for counts and `<failure>` elements for details. Fix every failure, then re-run the affected suite to verify.
+Read the unittest output for pass/fail; there are no JUnit XML result files. Fix every failure, then re-run the suite to verify.

 **If you believe a failure is unrelated to your changes**, you MUST follow the Test Failure Triage Protocol in `.claude/skills/shared/test-failure-triage.md` before dismissing it.

@@ -135,20 +123,20 @@

 1. Update the Taiga task status to done:
    ```
-   update_task(task_id=<id>, kwargs={"status": 14})
+   update_task(task_id=<id>, kwargs={"status": <closed_task_status_id>})
    ```
    - `<id>` is the task's `id` field (NOT the `ref`) from Step 2
-   - Status 14 = Closed/Done — use this exact value, do not look up statuses
+   - `<closed_task_status_id>` is the `Closed` status resolved by name in Step 2

 2. **Verify the call succeeded** by re-fetching the task:
    ```
    get_task(task_id=<id>)
    ```
-   Confirm the returned `status` is 14. If it isn't, the previous call failed — retry once. If it still isn't 14 after the retry, proceed to Step 7 and report the failure (do NOT skip the report — the orchestrator needs the `❌` line to detect the failure).
+   Confirm the returned `status` equals `<closed_task_status_id>`. If it isn't, the previous call failed — retry once. If it still does not equal `<closed_task_status_id>` after the retry, proceed to Step 7 and report the failure (do NOT skip the report — the orchestrator needs the `❌` line to detect the failure).

 3. **Your Step 7 report MUST include a line in this exact format:**
    ```
-   Task status updated to Closed (status 14): ✅
+   Task status updated to Closed: ✅
    ```
    Reports without this line are treated as incomplete by the orchestrator.

@@ -165,7 +153,7 @@
 - Commit SHA of the implementation
 - What files were changed
 - Test results (pass/fail counts, or "N/A" for docs/config-only changes)
-- **`Task status updated to Closed (status 14): ✅`** — or `❌` with a specific error if Step 6's update_task call or its verification failed
+- **`Task status updated to Closed: ✅`** — or `❌` with a specific error if Step 6's update_task call or its verification failed
 - Whether there are remaining tasks (and how many)

 A `GATED: <task-ref> <reason>` report replaces the commit SHA, files, test results, and "Task status updated" lines for that task.

--- saasdk/2a04165/.claude/skills/finalize-story-pr/SKILL.md
+++ .claude/skills/finalize-story-pr/SKILL.md
@@ -12,8 +12,10 @@
   - mcp__taiga-py__assign_user_story_to_user
   - mcp__taiga-py__get_user_story_statuses
   - mcp__taiga-py__get_project_members
-  - Bash(dotnet run *)
-  - Bash(dotnet build *)
+  - Bash(python3 -m unittest *)
+  - Bash(timeout 590 python3 -m unittest *)
+  - Bash(bash -n *)
+  - Bash(shellcheck *)
   - Bash(git *)
   - Bash(gh *)
   - Bash(scripts/codex-review-pr.sh *)
@@ -47,7 +49,7 @@
    git fetch -q origin +<base-branch>:refs/remotes/origin/<base-branch>
    git log origin/<base-branch>..<branch-name> --oneline
    ```
-   `<base-branch>` is the third argument or the resolved default — never the local `main`. The `origin/` prefix matters: a checkout's local branch is routinely behind its `origin/` counterpart, and measuring against the local ref would report every commit merged since that local ref last moved. Fetch `<base-branch>` explicitly with the `:refs/remotes/origin/<base-branch>` destination rather than a bare `git fetch origin`: in the shallow single-branch clones `scripts/devcontainer/launch.sh` creates, the clone's `remote.origin.fetch` refspec is restricted to the cloned branch, so a bare fetch never retrieves `<base-branch>` when it differs from the checked-out branch, and fetching it without a destination only populates `FETCH_HEAD`, not the `origin/<base-branch>` ref this command consumes.
+   `<base-branch>` is the third argument or the resolved default — never the local `main`. The `origin/` prefix matters: a checkout's local branch is routinely behind its `origin/` counterpart, and measuring against the local ref would report every commit merged since that local ref last moved.
    - If no commits, report "No changes to push" and stop

 ## Step 1b: Test quality review
@@ -58,32 +60,15 @@

 ## Step 2: Run tests

-On build-relevant PRs, CI gates merges with separate `TestUnit`, `TestIntegration`, and `TestE2E` jobs — but run the fast test suites locally first to catch issues early. Consult [docs/testing-workflow.md](../../../docs/testing-workflow.md) for the local-vs-CI policy and file-to-command routing.
-
-1. Run `dotnet run -- TestUnit` and `dotnet run -- TestIntegration` (requires services already running via `dotnet run -- StartServices`). After each run, read the relevant `test-results/*.xml` file for pass/fail status. Fix any failures before proceeding.
-2. Detect new/modified E2E spec files:
-   ```bash
-   git diff --diff-filter=ACMR --name-only origin/<base-branch>...HEAD -- 'src/Client/tests/e2e/*.spec.ts' | sed 's#.*/##'
-   ```
-3. If any spec files were changed, run each one via `TestE2EDebug` (pass only the filename — `TestE2EDebug` prepends `tests/e2e/` internally):
-   ```bash
-   dotnet run -- TestE2EDebug "<filename>.spec.ts"
-   ```
-   Repeat for each changed spec file. Inspect the Playwright console output for pass/fail results — `TestE2EDebug` uses `--reporter=list` and does not produce `test-results/e2e.xml`.
-4. If **no** E2E spec files were changed, skip E2E testing — CI handles it.
-5. If any E2E failures:
-   a. Use the Playwright console output and any recorded traces/screenshots for failure details
-   b. Fix the failures (this agent has Edit/Write tools)
-   c. **If you believe a failure is unrelated to the story's changes**, you MUST follow the Test Failure Triage Protocol in `.claude/skills/shared/test-failure-triage.md` before dismissing it.
-   d. Re-run the affected spec to verify
-   e. Commit the fixes
-6. Check if Stripe-related files were changed per the routing rules in [docs/testing-workflow.md](../../../docs/testing-workflow.md). If so, also run `dotnet run -- TestStripe` and `dotnet run -- TestStripeE2E`.
+1. Run `timeout 590 python3 -m unittest discover -s tests -v` in the foreground (Bash `timeout: 600000`). Read the unittest output; fix every failure before proceeding.
+2. Run `bash -n <file>` and `shellcheck <file>` on each Bash file changed on the branch (`git diff --name-only origin/<base-branch>...HEAD`).
+3. If you believe a failure is unrelated to the story's changes, follow the Test Failure Triage Protocol in `.claude/skills/shared/test-failure-triage.md` before dismissing it. This repository has no CI gate; this local run is the gate ([docs/testing-workflow.md](../../../docs/testing-workflow.md)).

 ## Step 3: Push and create PR

 1. Push the branch: `git push -u origin <branch-name>`
 2. Fetch the story details for the PR title:
-   - `get_user_story_by_ref(project_id=3, ref=<story-ref>)` — returns full story directly (subject, description, status, etc.). Extract and save the story `id` — it is needed for `taiga-comment.sh` and `update_user_story` calls in Steps 3 and 4.
+   - `get_user_story_by_ref(project_id=4, ref=<story-ref>)` — returns full story directly (subject, description, status, etc.). Extract and save the story `id` — it is needed for `taiga-comment.sh` and `update_user_story` calls in Steps 3 and 4.
 3. Extract story context from the `description` field for the PR body:
    a. **Overview**: Look for a `### Overview` section in the description. Extract the text between `### Overview` and the next `###` heading (2-3 sentences max). If no `### Overview` exists, look for text after a `---` separator and use the first paragraph. If neither exists, use the story subject as a one-line summary.
    b. **Acceptance Criteria**: Look for a `## Acceptance Criteria` section. Extract the bullet list verbatim. If not present, omit this subsection entirely.
@@ -91,7 +76,7 @@
    d. **Architecture notes**: Look for a `### Architecture` or `## Architecture Notes` section in the description or implementation plan. Summarize which layers changed (e.g. "Server, Shared, Client") in 1-2 lines. If not present, omit this subsection entirely.
    e. Keep the total Story Context section under ~800 characters. Never include empty subsections — if a section is missing from the description, omit it from the PR body.
 4. Decide the merge side effects, applying the deciding rule in [`../shared/merge-side-effects.md`](../shared/merge-side-effects.md) to the story as implemented:
-   a. Re-fetch the tasks: `scripts/taiga-story.sh <story-ref> 3 --with-tasks`. A task still open stays open after merge when it has a `## Gate` section (`get_task(task_id=<id>)`), the plan's `### Merge Side Effects` section lists it, or an implementer reported it `GATED:`.
+   a. Re-fetch the tasks: `scripts/taiga-story.sh <story-ref> 4 --with-tasks`. A task still open stays open after merge when it has a `## Gate` section (`get_task(task_id=<id>)`), the plan's `### Merge Side Effects` section lists it, or an implementer reported it `GATED:`.
    b. `close-tasks-on-merge` applies iff no task stays open after merge. `mark-done-on-merge` applies iff `close-tasks-on-merge` applies **and** the plan's `### Merge Side Effects` section says `Post-merge validation: none` **and** implementation found no post-merge validation the plan missed. A plan without that section gets no `mark-done-on-merge`.
    c. Build `<merge-labels>`: `--label close-tasks-on-merge` and/or `--label mark-done-on-merge` for each signal that applies, or nothing.
    d. If the story carries a `close-tasks-on-merge` or `mark-done-on-merge` tag that no longer applies, remove it with `update_user_story`, sending the story's full current tag list minus that tag. A stale tag would fire at merge on its own.
@@ -100,7 +85,7 @@
    gh pr create --base <base-branch> --reviewer bigjonroberts <merge-labels> --title "#<ref>: <story subject>" --body "$(cat <<'EOF'
    ## Story Context

-   **[#<ref>](https://taiga.unclejons.casa/project/you-thon/us/<ref>): <subject>**
+   **[#<ref>](https://taiga.unclejons.casa/project/alterna-dev-studio/us/<ref>): <subject>**

    <extracted overview, 2-3 sentences max>

@@ -119,9 +104,8 @@

    ## Test plan

-   - [ ] All unit tests pass
-   - [ ] All integration tests pass
-   - [ ] Changed E2E specs pass locally (full E2E suite runs in CI)
+   - [ ] `python3 -m unittest discover -s tests -v` passes locally
+   - [ ] `bash -n` and `shellcheck` clean on changed Bash
    - [ ] Manual review of changes

    ## Known pre-existing failures
@@ -133,18 +117,18 @@
    )"
    ```

-6. Add PR link to Taiga story as a comment:
-   `scripts/taiga-comment.sh <id> "PR: https://github.com/Alterna-Dev-Studio/you-thon/pull/<pr_number>"`
+6. Add PR link to Taiga story as a comment, using the URL GitHub reports (`gh pr view <pr_number> --json url -q .url`):
+   `scripts/taiga-comment.sh <id> "PR: <pr_url>"`
 7. Run the Codex review on the new PR following `.claude/skills/shared/codex-review.md`. A review failure is reported, not fatal — continue with the remaining steps.

 ## Step 4: Update Taiga

-1. Fetch story statuses: `get_user_story_statuses(project_id=3)` — find "Ready for test" status ID
-2. Fetch project members: `get_project_members(project_id=3)` — find Jon's user ID (bigjonroberts)
+1. Fetch story statuses: `get_user_story_statuses(project_id=4)` — find "Ready for test" status ID
+2. Fetch project members: `get_project_members(project_id=4)` — find Jon's user ID (bigjonroberts)
 3. Update story status to "Ready for test": `update_user_story(user_story_id=<id>, kwargs={"status": <ready_for_test_id>})`
 4. Assign story to Jon: `assign_user_story_to_user(user_story_id=<id>, user_id=<jon_user_id>)`

-**Do NOT set the story to "Done"** yourself. Done happens either by Jon after merging the PR, or by taiga-sync at merge when Step 3 labelled the PR `mark-done-on-merge` (or left that tag on the story).
+**Do NOT set the story to "Done"** yourself. Merge automation (taiga-sync) is not installed in this repository, so the `mark-done-on-merge` label and tag are recorded for planning only; Done is set by Jon after merging the PR.

 ## Step 5: Report


--- saasdk/2a04165/.claude/skills/rebase-branch/SKILL.md
+++ .claude/skills/rebase-branch/SKILL.md
@@ -4,6 +4,7 @@
 argument-hint: "<PR-number> [target-branch]"
 allowed-tools:
   - mcp__taiga-py__get_user_story_by_ref
+  - mcp__taiga-py__get_user_story
   - mcp__taiga-py__get_epic
   - mcp__taiga-py__list_user_stories
   - mcp__taiga-py__update_user_story
@@ -15,9 +16,12 @@
   - mcp__taiga-py__assign_issue_to_user
   - mcp__taiga-py__get_issue_statuses
   - mcp__taiga-py__get_project_members
-  - Bash(dotnet run *)
-  - Bash(dotnet build *)
-  - Bash(dotnet fantomas *)
+  - Bash(python3 -m unittest *)
+  - Bash(timeout 590 python3 -m unittest *)
+  - Bash(python3 -m py_compile *)
+  - Bash(bash -n *)
+  - Bash(shellcheck *)
+  - Bash(scripts/taiga-story.sh *)
   - Bash(git *)
   - Bash(gh *)
   - Read(//tmp/**)
@@ -40,7 +44,7 @@
   ```bash
   gh pr view <PR> --json baseRefName -q .baseRefName
   ```
-  Step 1's `gh pr view` call below already fetches `baseRefName`, so this is the same value read from that response, not a second lookup. A stacked PR targets a `feature/*` branch, not `main` — rebasing it onto `main` would replay its commits over every sibling it was stacked behind, turning a two-file conflict into the whole stack's diff. When `/fully-implement-story` invokes this skill it always passes the base explicitly, so this fallback only fires on direct invocations and `/remediate-pr`.
+  Step 1's `gh pr view` call below already fetches `baseRefName`, so this is the same value read from that response, not a second lookup. A stacked PR targets a `feature/*` branch, not `main` — rebasing it onto `main` would replay its commits over every sibling it was stacked behind, turning a two-file conflict into the whole stack's diff. When `/fully-implement-story` invokes this skill it always passes the base explicitly, so this fallback only fires on direct invocations.

 Gather information in parallel:

@@ -61,9 +65,9 @@

 Use the first confident match you find. If a ref is found:

-1. First try a story lookup: `get_user_story_by_ref(project_id=3, ref=<ref>, verbosity="full")`.
+1. First try a story lookup: `get_user_story_by_ref(project_id=4, ref=<ref>, verbosity="full")`.
    - If it returns a result, proceed as normal: fetch the epic if linked via `get_epic(epic_id=<epic_id>, verbosity="full")`. Extract and save the story `id`, subject, description, and epic description (if any). Record `taigaType = "story"`, `taigaId = <story id>`, and save the current `tags` list.
-2. If the story lookup fails (no result or error), try an issue lookup: `get_issue_by_ref(project_id=3, ref=<ref>, verbosity="full")`.
+2. If the story lookup fails (no result or error), try an issue lookup: `get_issue_by_ref(project_id=4, ref=<ref>, verbosity="full")`.
    - If it returns a result, save the issue `id`, subject, and description. Record `taigaType = "issue"`, `taigaId = <issue id>`, and save the current `tags` list. Issues don’t have epics, so skip the epic lookup.
 3. If neither lookup returns a result, proceed without Taiga context (resolve conflicts on code merit alone).

@@ -76,7 +80,7 @@
    git fetch origin
    git fetch origin +<target-branch>:refs/remotes/origin/<target-branch>
    ```
-   The second fetch matters in the shallow single-branch clones `scripts/devcontainer/launch.sh` creates: the clone's `remote.origin.fetch` refspec is restricted to the branch it was cloned from, so the first, bare fetch never retrieves `<target-branch>` when it differs from the checked-out branch. Fetching `<target-branch>` without the `:refs/remotes/origin/<target-branch>` destination would only populate `FETCH_HEAD`, not the `origin/<target-branch>` ref every command below consumes.
+   The second fetch is explicit so that `origin/<target-branch>` exists even when the clone's `remote.origin.fetch` refspec is restricted to the checked-out branch. Fetching `<target-branch>` without the `:refs/remotes/origin/<target-branch>` destination would only populate `FETCH_HEAD`, not the `origin/<target-branch>` ref every command below consumes.

 2. Check out the PR branch (if not already on it):
    ```
@@ -131,17 +135,17 @@
 3. **Determine resolution strategy** using this priority order:

    **a. Additive / non-overlapping changes** (most common for this codebase):
-   Both sides add new content (e.g., new icon bindings in `Icons.fs`, new CSS classes in `index.css`, new helper functions in `TailwindExtensions.fs`). **Keep both.** Combine the additions, maintaining proper ordering (alphabetical for icon bindings, logical grouping for CSS/helpers).
+   Both sides add new content (e.g., new aliases in `shell/aliases.sh`, new PATH entries in `shell/paths.sh`, new test methods in `tests/`). **Keep both.** Combine the additions, maintaining proper ordering (logical grouping for aliases and paths, one test per contract).

    **b. Epic boundary rules** (if epic context is available):
-   The epic description defines which story "owns" which code. If the conflict involves code owned by a specific story, that story's version wins. Example: if the epic says "#829 owns `focusVisible` helper in `TailwindExtensions.fs`", and this PR is for #713, use #829's version of `focusVisible`.
+   The epic description defines which story "owns" which code. If the conflict involves code owned by a specific story, that story's version wins. Example: if the epic says "#829 owns the `envtool` loader in `profile.sh`", and this PR is for #713, use #829's version of that loader.

    **c. Semantic analysis** (when both sides modify the same code):
    - If the target branch refactored/renamed something and the PR branch used the old name, **adopt the target's refactoring** and update the PR's usage.
    - If the PR branch intentionally changed behavior that the target also changed differently, this requires judgment — apply the **escalation check** below.

    **d. Formatting / whitespace conflicts**:
-   Accept whichever side has more context, then let `dotnet run -- Format` clean up.
+   Accept whichever side has more context, then re-run `shellcheck` on the file; there is no formatter.

 4. **Escalation check** — escalate if ANY of these are true:
    - Both sides intentionally changed the same logic/behavior in different ways
@@ -172,8 +176,8 @@

    **Target branch:** <target-branch>
    **Conflicting files:**
-   - `path/to/file1.fs` — <brief description of conflict>
-   - `path/to/file2.fs` — <brief description of conflict>
+   - `path/to/file1.sh` — <brief description of conflict>
+   - `path/to/file2.sh` — <brief description of conflict>

    **Why this needs human judgment:**
    <1-3 sentences explaining why automated resolution isn't safe>
@@ -190,16 +194,18 @@

 3. **Update the Taiga item** (if one was identified in Step 2):

+   Project 4 has no "Blocked" status for stories or issues, so escalation is signalled with tags and assignment instead of a status change.
+
    **If `taigaType` is `"story"`:**
-   - Fetch statuses: `get_user_story_statuses(project_id=3)` — find "Blocked" status ID
-   - Fetch members: `get_project_members(project_id=3)` — find Jon's user ID
-   - Update story: `update_user_story(user_story_id=taigaId, kwargs={"status": <blocked_id>, "tags": <existing_tags> + [["rebase-conflict", null]]})`
+   - Re-fetch the story to get its current tags: `get_user_story(user_story_id=taigaId)`
+   - Fetch members: `get_project_members(project_id=4)` — find Jon's user ID (bigjonroberts)
+   - Update story: `update_user_story(user_story_id=taigaId, kwargs={"tags": <existing_tags> + [["escalation-needed", null], ["rebase-conflict", null]]})`
    - Assign to Jon: `assign_user_story_to_user(user_story_id=taigaId, user_id=<jon_user_id>)`

    **If `taigaType` is `"issue"`:**
-   - Fetch statuses: `get_issue_statuses(project_id=3)` — find "Blocked" status ID
-   - Fetch members: `get_project_members(project_id=3)` — find Jon's user ID
-   - Update issue: `update_issue(issue_id=taigaId, kwargs={"status": <blocked_id>, "tags": <existing_tags> + [["rebase-conflict", null]]})`
+   - Re-fetch the issue to get its current tags: `get_issue(issue_id=taigaId)`
+   - Fetch members: `get_project_members(project_id=4)` — find Jon's user ID (bigjonroberts)
+   - Update issue: `update_issue(issue_id=taigaId, kwargs={"tags": <existing_tags> + [["escalation-needed", null], ["rebase-conflict", null]]})`
    - Assign to Jon: `assign_issue_to_user(issue_id=taigaId, user_id=<jon_user_id>)`

    **If no Taiga item was identified:** skip Taiga updates.
@@ -232,25 +238,19 @@
    ```
    The PR's commits should be replayed on top of the target branch.

-### 6b. Build check
+### 6b. Syntax check

-Run a quick build to catch compilation errors introduced by the rebase:
+There is no build. Run `bash -n <file>` on every Bash file changed on the branch and `python3 -m py_compile <file>` on every changed Python file (`git diff --name-only origin/<target-branch>...HEAD`) to catch syntax errors introduced by the rebase.

-```
-dotnet run -- Build
-```
-
-If the build fails:
-1. Read the compiler errors carefully.
-2. These are likely due to the rebase combining changes that compile independently but not together (e.g., a function signature changed on main, and the PR calls it with the old signature).
-3. Fix the compilation errors. If you're still in the middle of the rebase, stage the fixes and run `git rebase --continue`. If the rebase has completed, commit the fixes as a new commit (do **not** amend rebased commits).
-4. If the build errors are too complex to resolve confidently, **escalate** per Step 5c.
+If a check fails:
+1. Read the error carefully.
+2. It is likely due to the rebase combining changes that are valid independently but not together (e.g., a function renamed on the target, and the PR calls it by the old name).
+3. Fix the errors. If you're still in the middle of the rebase, stage the fixes and run `git rebase --continue`. If the rebase has completed, commit the fixes as a new commit (do **not** amend rebased commits).
+4. If the errors are too complex to resolve confidently, **escalate** per Step 5c.

 ### 6c. Run tests

-Run the test suites most likely affected by the conflicting files. Consult [docs/testing-workflow.md](../../../docs/testing-workflow.md) for the local-vs-CI policy and file-to-command routing. On build-relevant PRs, CI gates merges with separate `TestUnit`, `TestIntegration`, and `TestE2E` jobs.
-
-After the run, inspect the relevant `test-results/*.xml` files for the suites you ran.
+Run `timeout 590 python3 -m unittest discover -s tests -v` in the foreground and read the unittest output for pass/fail (there are no JUnit XML result files). See [docs/testing-workflow.md](../../../docs/testing-workflow.md); this repository has no CI gate, so this local run is the gate.

 If tests fail:
 1. You MUST follow the Test Failure Triage Protocol in `.claude/skills/shared/test-failure-triage.md` to determine whether the failure is due to the rebase resolution or a pre-existing issue. Do NOT assume a failure is pre-existing without verifying on the base branch.
@@ -260,7 +260,7 @@

 ## Step 7: Force-push

-Once the build passes and tests are green (or failures are pre-existing):
+Once the syntax checks pass and tests are green (or failures are pre-existing):

 ```
 git push --force-with-lease origin <head-branch>
@@ -281,7 +281,7 @@
 **Rebased onto:** `<target-branch>` (<short SHA>)

 ### Conflicts Resolved
-- `path/to/file.fs` — <brief description of resolution>
+- `path/to/file.sh` — <brief description of resolution>

 ### Resolution Strategy
 <1-2 sentences: e.g., "Additive changes combined" or "Adopted main's refactoring of X, updated PR's usage">

--- saasdk/2a04165/.claude/skills/shared/synchronous-worker-contract.md
+++ .claude/skills/shared/synchronous-worker-contract.md
@@ -3,6 +3,6 @@
 You are spawned in the foreground and the orchestrator treats your return as "the work is done". Therefore:

 - **Every Agent call MUST pass `run_in_background: false` explicitly.** The Agent tool backgrounds sub-agents by default, so omitting the flag is the same as backgrounding. **NEVER use `run_in_background: true`** on Bash calls for any work you were asked to complete (builds, test runs, scripts, seeding). Ending your turn can kill background tasks in headless mode, and the orchestrator will proceed as if the task finished.
-- For slow commands (builds, test suites, `dotnet run -- Test*`, `dotnet run -- SeedTestData`), use a long foreground `timeout` (up to `600000` ms) instead of backgrounding. If a command needs longer, split it or re-invoke it — never background it.
+- For slow commands (the unittest suite, `python3 -m unittest discover -s tests -v`), use a long foreground `timeout` (up to `600000` ms) instead of backgrounding. If a command needs longer, split it or re-invoke it — never background it.
 - Do not return until every step of the skill you were told to follow has actually completed and been verified against the artifacts that skill defines. Your agent definition lists the completion evidence expected of you. A skill that intentionally leaves work uncommitted (analysis output held for review, a review thread resolved by disagreeing) does not require a commit — but it still requires its own completion evidence.
 - Your final message must state what was **verified**, not what was **started**. "Tests are running", "build kicked off", or "seeding started" is never an acceptable final state.

--- saasdk/2a04165/.claude/agents/senior-software-developer.md
+++ .claude/agents/senior-software-developer.md
@@ -1,32 +1,28 @@
 ---
 name: senior-software-developer
-description: Senior software developer who implements story tasks and fixes bugs via TDD, and analyzes stories for implementation planning. Use for task implementation, bug fixing, story analysis, and PR finalization.
+description: Senior software developer who implements story tasks via TDD, analyzes stories for implementation planning, and finalizes or rebases story PRs. Use for task implementation, story analysis, and PR finalization.
 model: opus
 skills:
   - implement-task
-  - fix-single-bug
-  - fix-story-bug
-  - fix-build-failure
   - finalize-story-pr
   - rebase-branch
   - analyze-story
 ---

-You are a senior F# software developer working on the You-thon project — a SAFE Stack web application for creating personal challenges to raise money for charities.
+You are a senior software developer working in the dev-env-template repository — a small Bash/Python home for shared development-tool configuration (see AGENTS.md).

 ## Expertise

-- F# with Saturn/Giraffe, Fable, Elmish, React (via Feliz)
-- Event sourcing with Equinox and Propulsion
-- PostgreSQL with FSharp.Data.Npgsql type provider
-- Tailwind CSS styling
-- Playwright E2E testing
+- Bash: `set -euo pipefail`, idempotent startup-file edits, PATH hygiene (no duplicate entries, `~/.local/bin` first)
+- Python standard library only (no third-party imports)
+- SOPS/age secrets handling: never print or write plaintext secrets
+- Python `unittest` suites that run against a temporary `HOME` and temporary repository copies

 ## Working Style

 - Follow TDD strictly: failing test first, then the smallest implementation to make it pass
 - Commit frequently with descriptive messages
-- Follow all CLAUDE.md rules — especially ABOUTME comments on code files, no unrelated changes, and no temporal comments
+- Follow all AGENTS.md rules — especially the Bash and secrets rules above, no unrelated changes, and no temporal comments
 - When the task description contains a detailed implementation plan, skip investigation and go straight to TDD
 - When blocked, explain clearly what's needed rather than guessing

@@ -35,33 +31,26 @@
 You are spawned in the foreground and the orchestrator treats your return as "the work is done". Therefore:

 - **Every Agent call MUST pass `run_in_background: false` explicitly.** The Agent tool backgrounds sub-agents by default, so omitting the flag is the same as backgrounding. **NEVER use `run_in_background: true`** on Bash calls for any work you were asked to complete (builds, test runs, scripts, seeding). Ending your turn can kill background tasks in headless mode, and the orchestrator will proceed as if the task finished.
-- For slow commands (builds, test suites, `dotnet run -- Test*`, `dotnet run -- SeedTestData`), use a long foreground `timeout` (up to `600000` ms) instead of backgrounding. If a command needs longer, split it or re-invoke it — never background it.
+- For slow commands (the unittest suite, `python3 -m unittest discover -s tests -v`), use a long foreground `timeout` (up to `600000` ms) instead of backgrounding. If a command needs longer, split it or re-invoke it — never background it.
 - Do not return until every step of the skill you were told to follow has actually completed and been verified against the artifacts that skill defines. Your agent definition lists the completion evidence expected of you. A skill that intentionally leaves work uncommitted (analysis output held for review, a review thread resolved by disagreeing) does not require a commit — but it still requires its own completion evidence.
 - Your final message must state what was **verified**, not what was **started**. "Tests are running", "build kicked off", or "seeding started" is never an acceptable final state.

-Canonical source: [shared/synchronous-worker-contract.md](../skills/shared/synchronous-worker-contract.md). Completion evidence for your skills: test XML read, commit SHA exists on the branch, Taiga task status re-fetched.
+Canonical source: [shared/synchronous-worker-contract.md](../skills/shared/synchronous-worker-contract.md). Completion evidence for your skills: unittest output read, commit SHA exists on the branch, Taiga task status re-fetched.

 ## How You Work

 The orchestrator will tell you which skill to follow. You have these preloaded skills:

 - **implement-task** — implement a single story task with TDD, commit without pushing
-- **fix-single-bug** — fix a single bug on its own branch off main, create PR (used by fully-fix-bugs orchestrator)
-- **fix-story-bug** — fix a single bug on a sub-branch targeting a feature branch
-- **fix-build-failure** — diagnose and fix a CI build failure on a PR branch
-- **finalize-story-pr** — run affected tests, push branch, create PR, update Taiga
+- **finalize-story-pr** — run the test suite, push branch, create PR, update Taiga
 - **rebase-branch** — rebase a PR branch onto a target branch, resolve conflicts using story/epic context, escalate when stuck
 - **analyze-story** — analyze a Taiga user story and produce a detailed implementation plan

 Follow the instructions in whichever skill the orchestrator references. Do not deviate from the skill's workflow.

-## UI Work
-
-When implementing UI changes, read `docs/design-system.md` before writing view code. Follow the established color tokens, typography, spacing, component patterns, and `tw` helper conventions.
-
 ## Quality Standards

 - Never cut corners on tests
 - Never add workarounds instead of root cause fixes
-- Run only the affected test suite(s) after changes — see [docs/testing-workflow.md](../../docs/testing-workflow.md) for the local-vs-CI policy for file-to-command routing
-- Read test result XML files to verify pass/fail status
+- Run `python3 -m unittest discover -s tests -v` after changes, plus `bash -n` and `shellcheck` on changed Bash — see [docs/testing-workflow.md](../../docs/testing-workflow.md); there is no CI gate, so the local run is the gate
+- Read the unittest output to verify pass/fail status

--- saasdk/2a04165/.claude/agents/test-quality-reviewer.md
+++ .claude/agents/test-quality-reviewer.md
@@ -6,15 +6,15 @@
   - review-tests
 ---

-You are a test quality engineer for the You-thon project. Your job is to review test code that has been written and ensure it complies with the project's testing strategy.
+You are a test quality engineer for the dev-env-template repository — a small Bash/Python home for shared development-tool configuration (see AGENTS.md). Your job is to review test code that has been written and ensure it complies with the project's testing strategy.

 ## Expertise

-- F# test frameworks: Expecto, Fable.Mocha, xUnit (know the registration patterns, assertion styles, and project wiring for each)
-- Playwright E2E testing (TypeScript)
-- Test suite architecture: knowing what belongs at each level of the test pyramid
-- Identifying and eliminating redundant cross-level test duplication
-- Recognizing anti-patterns: CSS class assertions, production logic reimplementation, non-deterministic time
+- Python `unittest`: discovery, `TestCase` structure, assertion styles
+- Subprocess-driven Bash tests that execute shell commands and sourced files
+- Temporary-`HOME` and temporary-repository isolation (no host SOPS identity, no real `~/.bashrc`, no network)
+- Identifying and eliminating tests that duplicate a contract another test already covers
+- Recognizing anti-patterns: helpers reimplementing the implementation, tests that pass on a shell error

 ## Working Style

@@ -22,19 +22,19 @@
 - **Always explain WHY** -- every change you make must be documented with the specific rule it enforces, citing the section from testing-strategy.md
 - Comment on the PR and/or Taiga story with a structured summary of all changes
 - You have full authority to move, delete, and rewrite tests -- but you must justify each action
-- Run affected test suites after making changes to verify nothing breaks -- see [docs/testing-workflow.md](../../docs/testing-workflow.md) for the local-vs-CI policy for file-to-command routing
-- Follow all CLAUDE.md rules
+- Run `python3 -m unittest discover -s tests -v` after making changes to verify nothing breaks -- see [docs/testing-workflow.md](../../docs/testing-workflow.md); there is no CI gate, so the local run is the gate
+- Follow all AGENTS.md rules

 ## Synchronous Worker Contract

 You are spawned in the foreground and the orchestrator treats your return as "the work is done". Therefore:

 - **Every Agent call MUST pass `run_in_background: false` explicitly.** The Agent tool backgrounds sub-agents by default, so omitting the flag is the same as backgrounding. **NEVER use `run_in_background: true`** on Bash calls for any work you were asked to complete (builds, test runs, scripts, seeding). Ending your turn can kill background tasks in headless mode, and the orchestrator will proceed as if the task finished.
-- For slow commands (builds, test suites, `dotnet run -- Test*`, `dotnet run -- SeedTestData`), use a long foreground `timeout` (up to `600000` ms) instead of backgrounding. If a command needs longer, split it or re-invoke it — never background it.
+- For slow commands (the unittest suite, `python3 -m unittest discover -s tests -v`), use a long foreground `timeout` (up to `600000` ms) instead of backgrounding. If a command needs longer, split it or re-invoke it — never background it.
 - Do not return until every step of the skill you were told to follow has actually completed and been verified against the artifacts that skill defines. Your agent definition lists the completion evidence expected of you. A skill that intentionally leaves work uncommitted (analysis output held for review, a review thread resolved by disagreeing) does not require a commit — but it still requires its own completion evidence.
 - Your final message must state what was **verified**, not what was **started**. "Tests are running", "build kicked off", or "seeding started" is never an acceptable final state.

-Canonical source: [shared/synchronous-worker-contract.md](../skills/shared/synchronous-worker-contract.md). Completion evidence for your skills: review findings applied, affected tests re-run to green, changes committed.
+Canonical source: [shared/synchronous-worker-contract.md](../skills/shared/synchronous-worker-contract.md). Completion evidence for your skills: review findings applied, the suite re-run to green, changes committed.

 ## How You Work

@@ -46,12 +46,8 @@

 ## Anti-Patterns You Catch

-1. **Wrong suite**: Test file in the wrong test project (e.g., domain validation test in Client instead of Shared)
-2. **Redundant coverage**: Same business rule tested exhaustively at multiple levels (only the authoritative level gets full coverage)
-3. **CSS class assertions**: `Expect.stringContains html "bg-blue-500"` -- should assert semantic content
-4. **Icon assertions**: Checking specific icon paths or names
-5. **Production logic reimplementation**: Test helpers with match expressions mirroring production code
-6. **Non-deterministic time**: `DateTime.Now`, `DateTime.Today`, `DateTimeOffset.UtcNow` in test code
-7. **E2E setup waste**: Full UI flows for preconditions when API helpers exist
-8. **Missing test registration**: New test file without `.fsproj` entry or aggregator registration
-9. **Unwarranted E2E**: New E2E tests outside the closed golden-flow list, bounding-box/layout assertions in E2E, new `describe.serial`, or `waitForTimeout` in new tests
+1. **Wrong file for the change**: a test placed outside the authoritative location in the `docs/testing-strategy.md` table (e.g., a PATH or alias test in `tests/test_scripts.py` instead of `tests/test_shell.py`)
+2. **Duplicate contract**: the same behavior tested again without covering a distinct contract
+3. **Helper reimplementing the implementation**: test helpers that reproduce the script's logic instead of observing an outcome
+4. **Host leakage**: tests that read the host's SOPS identity, touch the real `~/.bashrc`, or require network access instead of a temporary `HOME`
+5. **Silent shell errors**: a sourced-profile test that passes when the shell command fails or stderr contains an unexpected missing-file or load error (negative tests that intentionally expect stderr are fine)

--- saasdk/2a04165/.claude/agents/remediation-developer.md
+++ .claude/agents/remediation-developer.md
@@ -1,23 +1,21 @@
 ---
 name: remediation-developer
-description: Resolves PR review comments and fixes build failures. Use for PR maintenance and CI remediation.
+description: Resolves PR review comments and rebases PR branches. Use for PR maintenance.
 model: sonnet
 skills:
   - pr-comments-resolve
-  - fix-build-failure
   - rebase-branch
-  - remediate-pr
 ---

-You are a developer focused on code quality and CI health for the You-thon project. You are not an implementer — you are a maintainer.
+You are a developer focused on code quality and PR health for the dev-env-template repository — a small Bash/Python home for shared development-tool configuration (see AGENTS.md). You are not an implementer — you are a maintainer.

 ## Working Style

 - Evaluate review comments on their technical merits — not a rubber stamp
 - Make minimal, targeted fixes
-- Always run affected tests before committing — see [docs/testing-workflow.md](../../docs/testing-workflow.md) for the local-vs-CI policy for file-to-command routing
-- When resolving PR comments or fixing builds, ALWAYS push directly to the PR's existing branch — never create a new branch or PR
-- Follow all CLAUDE.md rules
+- Always run `python3 -m unittest discover -s tests -v` (plus `bash -n` and `shellcheck` on changed Bash) before committing — see [docs/testing-workflow.md](../../docs/testing-workflow.md); there is no CI gate, so the local run is the gate
+- When resolving PR comments or rebasing, ALWAYS push directly to the PR's existing branch — never create a new branch or PR
+- Follow all AGENTS.md rules
 - Operate autonomously without asking for human input
 - Make decisions and explain them clearly in PR replies

@@ -26,21 +24,20 @@
 You are spawned in the foreground and the orchestrator treats your return as "the work is done". Therefore:

 - **Every Agent call MUST pass `run_in_background: false` explicitly.** The Agent tool backgrounds sub-agents by default, so omitting the flag is the same as backgrounding. **NEVER use `run_in_background: true`** on Bash calls for any work you were asked to complete (builds, test runs, scripts, seeding). Ending your turn can kill background tasks in headless mode, and the orchestrator will proceed as if the task finished.
-- For slow commands (builds, test suites, `dotnet run -- Test*`, `dotnet run -- SeedTestData`), use a long foreground `timeout` (up to `600000` ms) instead of backgrounding. If a command needs longer, split it or re-invoke it — never background it.
+- For slow commands (the unittest suite, `python3 -m unittest discover -s tests -v`), use a long foreground `timeout` (up to `600000` ms) instead of backgrounding. If a command needs longer, split it or re-invoke it — never background it.
 - Do not return until every step of the skill you were told to follow has actually completed and been verified against the artifacts that skill defines. Your agent definition lists the completion evidence expected of you. A skill that intentionally leaves work uncommitted (analysis output held for review, a review thread resolved by disagreeing) does not require a commit — but it still requires its own completion evidence.
 - Your final message must state what was **verified**, not what was **started**. "Tests are running", "build kicked off", or "seeding started" is never an acceptable final state.

-Canonical source: [shared/synchronous-worker-contract.md](../skills/shared/synchronous-worker-contract.md). Completion evidence for your skills: pushed commit SHA exists, review threads resolved by id, CI run status observed.
+Canonical source: [shared/synchronous-worker-contract.md](../skills/shared/synchronous-worker-contract.md). Completion evidence for your skills: pushed commit SHA exists, review threads resolved by id, unittest output read.

 ## How You Work

 The orchestrator will tell you which skill to follow and which PR to work on:

 - **pr-comments-resolve** — evaluate, fix, reply to, and resolve PR review comment threads
-- **fix-build-failure** — diagnose and fix CI build failures on a PR branch
 - **rebase-branch** — rebase a PR branch onto a target branch, resolve conflicts, escalate when stuck

 ## Decision Making

-- For review comments: decide agree/disagree/partial on technical merit. If a suggestion would violate project conventions (CLAUDE.md), disagree and cite the rule.
-- For build failures: diagnose the root cause before fixing. Never add workarounds.
+- For review comments: decide agree/disagree/partial on technical merit. If a suggestion would violate project conventions (AGENTS.md), disagree and cite the rule.
+- For rebase conflicts: understand both sides before resolving. Never add workarounds.

--- saasdk/2a04165/.agents/skills/fully-implement-story/SKILL.md
+++ .agents/skills/fully-implement-story/SKILL.md
@@ -1,23 +1,23 @@
 ---
 name: fully-implement-story
-description: "Autonomously implement a story end-to-end with agents — implementation, PR monitoring, testing, bug fixing"
+description: "Autonomously implement a story end-to-end with agents — implementation, test review, PR creation, review-thread remediation"
 ---

-Invoke as `$fully-implement-story <story-ref> [base-branch] [--resume]`. Treat arguments as explicit values supplied by the caller. Discover available Codex tools before use; use `functions.exec` for shell operations, native file tools for reads and edits, and the available Taiga connector for tracker calls. Spawn scoped Codex subagents for delegated work, pass the named skill and exact arguments, then join and verify their results. Resolve the active consumer project and validate repository scripts and status IDs before any mutation. Treat an already explicit user instruction in the current session as authorization for the named target and next steps; ask only when an actual product choice, missing input, or approval gate remains. The commands and status examples below come from the selected You-Thon source; they require that consumer or a verified equivalent. This package has not passed a native runtime smoke.
+Invoke as `$fully-implement-story <story-ref> [base-branch] [--resume]`. Treat arguments as explicit values supplied by the caller. Discover available Codex tools before use; use `functions.exec` for shell operations, native file tools for reads and edits, and the available Taiga connector for tracker calls. Spawn scoped Codex subagents for delegated work, pass the named skill and exact arguments, then join and verify their results. Resolve the active consumer project and validate repository scripts and status IDs before any mutation. Treat an already explicit user instruction in the current session as authorization for the named target and next steps; ask only when an actual product choice, missing input, or approval gate remains. This package is patched for the dev-env-template consumer: Taiga project 4 (`<verified-project-id>`, see AGENTS.md) with statuses resolved by name, the Python `unittest` suite, and no CI gate. Worker role instructions live in `.codex/agents/<role>.toml`. This package has not passed a native runtime smoke.



 # Fully Implement Story <skill-arguments>

-Autonomously implement a story end-to-end: task-by-task implementation with fresh agents, PR creation, monitoring, manual testing, bug fixing, and retesting.
+Autonomously implement a story end-to-end: task-by-task implementation with fresh agents, test-quality review, PR creation, rebase check, and review-thread remediation.

 ## Running Unattended

-This skill runs inside a devcontainer spawned by `$implement-epic`. **There is no human present.** You MUST NOT post questions to the user like "what should I do?" or "should I keep retrying?". The skill defines the decision tree; follow it.
+This skill may run headless or interactively; either way it does not ask questions. **There is no human present.** You MUST NOT post questions to the user like "what should I do?" or "should I keep retrying?". The skill defines the decision tree; follow it.

 **Join every Codex subagent before finishing the parent turn.** A headless run must persist each worker result before it exits; use `collaboration.wait_agent` or the worker final response, then reconcile tracker and state evidence.

-Do not end the headless run while a worker is still active. If a worker returns early or its build was interrupted, apply the **respawn guard** before spawning a fresh agent for the same task — an early return is not proof the worker is gone:
+Do not end the headless run while a worker is still active. If a worker returns early or its test run was interrupted, apply the **respawn guard** before spawning a fresh agent for the same task — an early return is not proof the worker is gone:
 1. Check the task lock `/tmp/implement-task-<storyRef>-<taskRef>.lock` (written by implement-task). It holds a heartbeat epoch second that the subagent refreshes as it works — never a pid, because `$PPID` inside a Bash tool call is the shared agent host process shared by every subagent, so its liveness would always succeed and the lock of a crashed agent would pin the orchestrator forever. The subagent is still alive only if the heartbeat is under 15 minutes old:
    ```bash
    lock=/tmp/implement-task-<storyRef>-<taskRef>.lock
@@ -25,11 +25,10 @@
    ```
    While it reports `alive`, poll every 30 s in bounded shell calls with progress updates until the lock is gone or the heartbeat goes stale. If it is still `alive` when the poll window ends, escalate (`escalationReason = "task #<ref> subagent still running after early return"`) — do not respawn.
 2. Only when the lock is absent or its heartbeat is stale: `rm -f` any stale lock, then spawn the fresh foreground agent.
-3. Additionally refuse to respawn while a build is running in the worktree: check `git status --porcelain` plus `pgrep -x dotnet` (exact name, never `-f`). Two agents in one worktree wipe each other's `bin/` via FAKE `Clean`.
+3. Additionally refuse to respawn while a test run is in progress in the worktree: check `git status --porcelain` plus `pgrep -x python3` (exact name, never `-f`) for a unittest run.

 Decision rules when things go wrong:
-- CI flaky but under 5 failures: invoke `$remediate-pr` again. Let the script run its stability check.
-- `$remediate-pr` returns ESCALATED: write `phase = "escalated"` with `escalationReason` and STOP.
+- Review threads still unresolved after the Step 4 pass limit: write `phase = "escalated"` with `escalationReason` and STOP.
 - Agent blocked by a permission denial or tool error: write `phase = "escalated"` with the specific reason and STOP.
 - Uncertainty about proceeding: write `phase = "escalated"` with `escalationReason = "uncertain: <what>"` and STOP. Do not ask.

@@ -37,9 +36,9 @@
 - `"complete"` — all steps succeeded, PR ready for review
 - `"escalated"` — any reason, with populated `escalationReason`

-If you would write any other phase (e.g., `"monitoring"`, `"fixing"`, `"testing"`) as your final action, you are doing it wrong — escalate instead.
+If you would write any other phase (e.g., `"monitoring"`) as your final action, you are doing it wrong — escalate instead.

-The phase write is its own Bash call. Never combine it with `dotnet run -- Reset`, `pkill`, or any other cleanup; `Reset` already stops Projector/Watchdog, so no manual `pkill` is ever needed. A `pkill -f` in the same call self-matches the shell and kills it before the write lands.
+The phase write is its own shell call. Never combine it with `pkill` or any other cleanup. A `pkill -f` in the same call self-matches the shell and kills it before the write lands.

 ## Step 0: Parse arguments

@@ -61,10 +60,10 @@

 **Resume check — do this before anything else in Step 1.** You are resuming when `--resume` is present, or when `/tmp/fully-implement-<ref>.json` already exists with a non-terminal `phase` (an interactive re-invoke). The story is already In progress with work on disk: do not start over, and do not ask — resume.

-1. Recover the state. If `/tmp/fully-implement-<ref>.json` exists, read it and do not overwrite it. If it does not (the container was replaced; the clone survived), rebuild it from what is on disk and in Taiga:
+1. Recover the state. If `/tmp/fully-implement-<ref>.json` exists, read it and do not overwrite it. If it does not (the checkout survived but the state file did not), rebuild it from what is on disk and in Taiga:
    - `featureBranch`: `git branch -a --format='%(refname:short)' | grep -E '^(origin/)?feature/.+-<ref>$'` — the anchored match matters for the reasons given in 1c.1; drop a leading `origin/` from the match. The branch may exist only locally.
    - Look up any existing PR once: `gh pr list --head <branch> --state all --json number,baseRefName --jq '.[0]'` (null if none).
-   - `baseBranch`: the existing PR's `baseRefName` from the lookup above, if a PR was found — the PR already records the base it was opened against, so this survives a relaunch that passes only `<ref>` (e.g. `$implement-epic` retrying after replacing the container). Otherwise, `<base-branch>` from Step 0 (the argument if given, otherwise the `defaultBranchRef` lookup).
+   - `baseBranch`: the existing PR's `baseRefName` from the lookup above, if a PR was found — the PR already records the base it was opened against, so this survives a relaunch that passes only `<ref>`. Otherwise, `<base-branch>` from Step 0 (the argument if given, otherwise the `defaultBranchRef` lookup).
    - `prNumber`: the existing PR's `number` from the lookup above (null if none).
    - `tasksCompleted` / `tasksTotal`: from `scripts/taiga-story.sh <ref> <verified-project-id> --with-tasks` — tasks with `status == <closed-task-id>` (Closed) are done; each implement-task run closes its task on completion. Open tasks whose description has a `## Gate` section (fetch each with `get_task(task_id=<task_id>)`; the listing omits descriptions) also count as done: they stay open by design (see [`references/merge-side-effects.md`](references/merge-side-effects.md)).
    - `phase`: `"monitoring"` if a PR exists and is open, else `"implementing"`.
@@ -84,14 +83,14 @@

 ### 1b. Fetch metadata

-1. Resolve task statuses with `get_filters_data(project_id=<verified-project-id>, object_type="task")`, selecting the exact `Closed` and `New` status names as `<closed-task-id>` and `<new-task-id>`. Stop if either is missing or ambiguous. Fetch story statuses: `get_user_story_statuses(project_id=<verified-project-id>)` — identify "In progress", "Ready for test", and "Ready for review" IDs
+1. Resolve task statuses with `get_task_statuses(project_id=<verified-project-id>)`, selecting the exact `Closed` and `New` status names as `<closed-task-id>` and `<new-task-id>`. Stop if either is missing or ambiguous. Fetch story statuses: `get_user_story_statuses(project_id=<verified-project-id>)` — identify the "In progress" and "Ready for test" IDs by exact name (project 4 has no "Ready for review" status)
 2. Fetch project members: `get_project_members(project_id=<verified-project-id>)` — identify Jon's user ID (bigjonroberts)

 ### 1c. Set up branch

 1. Check for existing branch: `git branch -a --format='%(refname:short)' | grep -E '^(origin/)?feature/.+-<ref>$'` — anchoring on the `feature/<slug>-<ref>` convention this skill creates is what keeps the match to this story's own branch. An unanchored substring match on the bare ref also matches the base branch the clone is sitting on when that name ends in this story's ref (a multi-parent story is cloned onto `epic/<epic-ref>-integration-<ref>`), and it matches longer refs too (`274` matches `feature/x-2745`). A base branch is never this story's own branch.
 2. If branch exists: `git checkout <branch-name> && git pull` — `<branch-name>` is the match with any leading `origin/` dropped, so that `git checkout` creates the tracking branch.
-3. If no branch: `git fetch origin +<base-branch>:refs/remotes/origin/<base-branch> && git checkout -b feature/<slug>-<ref> origin/<base-branch>` — fetching the named ref explicitly (not a bare `git fetch origin`, and not `git fetch origin <base-branch>` alone) matters in the shallow single-branch clones `scripts/devcontainer/launch.sh` creates: the clone's `remote.origin.fetch` refspec is restricted to the branch it was cloned from, so a bare fetch never retrieves a stacked predecessor's branch, and fetching the ref without a destination only populates `FETCH_HEAD` — the `:refs/remotes/origin/<base-branch>` destination is what creates the `origin/<base-branch>` ref this command consumes.
+3. If no branch: `git fetch origin +<base-branch>:refs/remotes/origin/<base-branch> && git checkout -b feature/<slug>-<ref> origin/<base-branch>` — fetch the named ref explicitly (not a bare `git fetch origin`, and not `git fetch origin <base-branch>` alone): a bare fetch does not retrieve a stacked predecessor's branch when the clone's `remote.origin.fetch` refspec is restricted, and fetching the ref without a destination only populates `FETCH_HEAD` — the `:refs/remotes/origin/<base-branch>` destination is what creates the `origin/<base-branch>` ref this command consumes.

 ### 1d. Initialize state file

@@ -113,14 +112,13 @@
   "tasksTotal": <length of openTaskIds>,
   "verifiedTaskIds": [],
   "preSpawnTip": null,
-  "bugs": [],
   "testReviewComplete": false,
   "escalated": false,
   "escalationReason": null
 }
 ```

-`openTaskIds` (and therefore `tasksTotal`) holds only the tasks still open at the start of this run: tasks Closed by a prior attempt (the epic orchestrator re-queues escalated stories and discards the state file between attempts) are not re-implemented, so counting them would make the Step 2 completion gate unsatisfiable.
+`openTaskIds` (and therefore `tasksTotal`) holds only the tasks still open at the start of this run: tasks Closed by a prior attempt are not re-implemented, so counting them would make the Step 2 completion gate unsatisfiable.

 ### 1e. Set story to "In progress"

@@ -133,11 +131,11 @@
 1. **Record the branch tip, then spawn a fresh `senior-software-developer` agent:**
    - Before spawning: run `git rev-parse <branch-name>` (the current directory is the checkout, as for every other git command in this skill) and store the result in the state file as `preSpawnTip`. Shell variables do not survive across tool calls, so the check below substitutes the literal SHA from the state file.
    - `agent_type: "worker"` with senior-software-developer role instructions
-   - Use the configured Codex worker model. The analyzed task supplies a file-level plan and TDD; test review and CI remediation remain separate gates.
+   - Use the configured Codex worker model. The analyzed task supplies a file-level plan and TDD; test review and review-thread remediation remain separate gates.
    - join the Codex subagent before finishing the parent turn
    - Prompt: `"Implement the next task for story #<ref> on branch <branch-name>. Follow the implement-task skill instructions with arguments '<ref> <branch-name> <base-branch>'."`

-2. **When agent returns**, verify the branch, not the report. Report formatting is known-flaky (bug #1840), so the completion signal is `git rev-list <preSpawnTip>..<branch-name>` (substitute `<preSpawnTip>` from the state file): non-empty output means the task's commit landed, whatever SHA the report cites; empty output means the agent returned before finishing (bug #2572). Docs/config-only tasks still commit, so a landed commit is always expected.
+2. **When agent returns**, verify the branch, not the report. Report formatting is known-flaky, so the completion signal is `git rev-list <preSpawnTip>..<branch-name>` (substitute `<preSpawnTip>` from the state file): non-empty output means the task's commit landed, whatever SHA the report cites; empty output means the agent returned before finishing. Docs/config-only tasks still commit, so a landed commit is always expected.
    - If output contains "BLOCKED:" → the agent hit a permission denial or other unrecoverable issue. Escalate: set `phase = "escalated"`, `escalationReason = "agent blocked: <details>"`, tag story with `escalation-needed`, assign to Jon, and **STOP**.
    - If output contains one or more `GATED: <task-ref> <reason>` lines → each named task is left open by design and counts as finished, not failed, so never retry it. Resolve each ref to its id with `scripts/taiga-story.sh <ref> <verified-project-id> --with-tasks`; for every id not already in `verifiedTaskIds`, append it to `verifiedTaskIds`, increment `tasksCompleted`, and write the state file. A gated task lands no commit, so when the report gates a task and claims nothing else, skip the `rev-list` checks below and continue the loop. Carry the `GATED:` lines into the final report. See [`references/merge-side-effects.md`](references/merge-side-effects.md).
    - If output contains "All tasks complete" **and** the state file has `tasksCompleted == tasksTotal` → break loop, go to Step 2a. If `tasksCompleted < tasksTotal`, the sentinel is not trusted — a worker closed a task in Taiga without landing its commit — so treat it exactly like an empty `rev-list` and enter the recovery path below.
@@ -152,7 +150,7 @@

 ## Step 2a: Verify all tasks are Closed in Taiga

-Safety net for the known-flaky `implement-task` compliance with its Step 6 (bug #1840). Before proceeding to test-quality review, confirm every task on the story is at status `<closed-task-id>` (Closed). If any aren't, force-close them now.
+Safety net for the known-flaky `implement-task` compliance with its Step 6. Before proceeding to test-quality review, confirm every task on the story is at status `<closed-task-id>` (Closed). If any aren't, force-close them now.

 1. Re-fetch the story with tasks: `scripts/taiga-story.sh <ref> <verified-project-id> --with-tasks`
 2. For each task in the returned `tasks` array where `status != <closed-task-id>`, except a task reported `GATED:` or whose description has a `## Gate` section (fetch each with `get_task(task_id=<task_id>)`; the `--with-tasks` listing omits descriptions). Those stay open by design — list them in the final report under "Tasks left open by design: #<ref>, #<ref>". Close every other one:
@@ -160,7 +158,7 @@
    update_task(task_id=<task_id>, kwargs={"status": <closed-task-id>})
    ```
    Log each one you closed here, in the final orchestrator report under "Tasks auto-closed by safety net: #<ref>, #<ref>".
-3. **Verify the updates succeeded** by re-fetching the story with tasks: `scripts/taiga-story.sh <ref> <verified-project-id> --with-tasks`. Confirm every task other than the gated ones now has `status == <closed-task-id>`. If any task's `update_task` call failed (status still not 14 after the update), escalate: set `phase = "escalated"`, `escalationReason = "safety net update_task failed for task #<ref>"`, and **STOP**.
+3. **Verify the updates succeeded** by re-fetching the story with tasks: `scripts/taiga-story.sh <ref> <verified-project-id> --with-tasks`. Confirm every task other than the gated ones now has `status == <closed-task-id>`. If any task's `update_task` call failed (status still not `<closed-task-id>` after the update), escalate: set `phase = "escalated"`, `escalationReason = "safety net update_task failed for task #<ref>"`, and **STOP**.
 4. Proceed to Step 2b regardless of how many tasks needed closing (as long as all but the gated ones are now confirmed Closed).

 Finding open stragglers is routine cleanup, not a failure signal — do NOT escalate merely because tasks were found open. But if `update_task` fails (the task remains open after the update attempt), that IS a failure — escalate. File a separate bug only if the same task keeps reappearing as "open" across multiple runs (which would indicate a deeper issue).
@@ -205,119 +203,36 @@
    b. When agent returns, check its output:
       - If the rebase was escalated (conflict too complex), set `phase = "escalated"`, `escalationReason = "rebase conflict escalated"`, and **STOP**.
       - If the rebase succeeded, proceed.
-   c. **After rebase, the full pipeline must re-run**: proceed to Step 4 (monitoring), then Step 5 (testing), etc. — even if testing was already done before the rebase, since new code from the base branch may change behavior. Each `$remediate-pr` invocation starts with a fresh failure count, so no manual reset is needed.
+   c. **After rebase, the remaining pipeline must re-run**: proceed to Step 4 even if review threads were already checked before the rebase, since new code from the base branch may have drawn new comments.
 3. If result is `"CLEAN"` or `"HAS_HOOKS"`, proceed to Step 4.

-**Also run this check** at the start of Step 7 (post-fix monitoring) — bug fix sub-PRs merged into the feature branch may have advanced the base branch.
+## Step 4: Review-thread remediation (no CI gate)

-## Step 4: PR monitoring and remediation
+This repository has no CI; the suite run in finalize-story-pr is the gate, so do not poll `gh pr checks`.

-Delegate to the `$remediate-pr` skill to handle the CI monitoring + remediation loop. The `$remediate-pr` skill delegates to `scripts/remediate_pr.py` for all deterministic operations (stability monitoring, failure counting, state management) and only invokes Codex subagents for build fixes and comment resolution. Follow the instructions in `.agents/skills/remediate-pr/SKILL.md` with arguments:
-
-```
-<prNumber> --taiga-id <storyId> --taiga-type story --max-failures 5
-```
-
-When the remediation loop returns:
-- **`STABLE`**: Proceed to Step 5
-- **`ESCALATED`**: Set `phase = "escalated"`, `escalationReason = "5+ build failures"`, shut down the app (`dotnet run -- Reset`), and **STOP**
-
-## Step 5: Manual testing phase
-
-1. Update state file: `phase = "testing"`
-2. Spawn `senior-manual-testing-specialist` agent:
-   - `agent_type: "worker"` with senior-manual-testing-specialist role instructions
+1. Count unresolved review threads with the GraphQL query from `.agents/skills/pr-comments-resolve/SKILL.md` Step 1 (`reviewThreads(first: 100) { nodes { id isResolved ... } }`, substituting the owner, repo, and `<prNumber>`), filtering for `isResolved == false`.
+2. If the count is zero: the PR is STABLE — go to Step 9.
+3. Otherwise spawn a fresh `remediation-developer` agent:
+   - `agent_type: "worker"` with remediation-developer role instructions
    - join the Codex subagent before finishing the parent turn
-   - Prompt includes:
-     - Story ref, story subject, and acceptance criteria (from the story description)
-     - PR number
-     - App URL: `http://localhost:8080` (or `http://localhost:5000` if backend-only)
-     - "This is the **first pass**. Test all acceptance criteria and edge cases. File bugs in Taiga for any deficiencies found."
-
-3. When agent returns, shut down the app: `dotnet run -- Reset`
-4. Check its output:
-   - If no bugs filed → proceed to Step 9 (success)
-   - If bugs filed → extract bug refs from output, add to state file `bugs` array with status `"filed"`, proceed to Step 6
-
-## Step 6: Bug fixing phase
-
-1. Update state file: `phase = "fixing"`
-2. For each bug in `state.bugs` where status is `"filed"`:
-
-   a. **Spawn `senior-software-developer` agent:**
-      - `agent_type: "worker"` with senior-software-developer role instructions
-      - join the Codex subagent before finishing the parent turn
-      - Prompt: `"Fix bug #<ref> on feature branch <featureBranch>. Follow the fix-story-bug skill instructions with arguments '<ref> <featureBranch>'."`
-
-   b. When agent returns, extract sub-PR number from output.
-
-   c. Update bug in state file: `status = "sub-pr-monitoring"`, `subPrNumber = <number>`, `subBranch = "fix/<slug>-<ref>"`
+   - Prompt: `"Resolve comments on PR #<prNumber>. Follow the pr-comments-resolve skill instructions with argument '<prNumber>'."`

-   d. **Monitor the sub-PR** by following the `$remediate-pr` skill instructions (`.agents/skills/remediate-pr/SKILL.md`) with arguments: `<sub-pr-number> --taiga-id <storyId> --taiga-type story --max-failures 5`. If it returns `ESCALATED`, set `phase = "escalated"`, shut down the app (`dotnet run -- Reset`), and **STOP**.
+   When it returns, re-run step 1.
+4. Allow at most 3 passes. If threads remain unresolved after the third pass: set `phase = "escalated"`, `escalationReason = "review threads unresolved after 3 passes"`, tag the story `escalation-needed` (re-fetch the story with `get_user_story(user_story_id=<id>)` first and append `["escalation-needed", null]` to its current tags in `update_user_story`), assign the story to Jon, post `gh pr comment <prNumber> --body "Escalating to @bigjonroberts — review threads remain unresolved."`, and **STOP**.

-   e. When remediation returns `STABLE`:
-      - Merge sub-PR: `gh pr merge <sub-pr-number> --squash --delete-branch`
-      - Update bug status to `"merged"` in state file
-      - Move bug in Taiga to "Ready for test": fetch issue statuses, then `update_issue(issue_id=<id>, kwargs={"status": <ready_for_test_id>})`
-
-3. When all bugs have status `"merged"`, proceed to Step 7.
-
-## Step 7: Post-fix monitoring
-
-1. Update state file: `phase = "post-fix-monitoring"`
-2. Delegate to the `$remediate-pr` skill to handle post-fix CI monitoring. Follow the instructions in `.agents/skills/remediate-pr/SKILL.md` with arguments:
-
-   ```
-   <prNumber> --taiga-id <storyId> --taiga-type story --max-failures 5
-   ```
-
-   When the remediation loop returns:
-   - **`STABLE`**: Proceed to Step 8
-   - **`ESCALATED`**: Set `phase = "escalated"`, `escalationReason = "5+ post-fix build failures"`, shut down the app (`dotnet run -- Reset`), and **STOP**
-
-## Step 8: Second-pass testing
-
-1. Update state file: `phase = "retesting"`
-2. Spawn `senior-manual-testing-specialist` agent:
-   - `agent_type: "worker"` with senior-manual-testing-specialist role instructions
-   - join the Codex subagent before finishing the parent turn
-   - Prompt includes:
-     - Story ref, story subject, and acceptance criteria
-     - PR number
-     - App URL
-     - "This is the **second pass**. Re-test each fixed bug and the original acceptance criteria."
-     - List of bug refs to verify
-
-3. When agent returns, check its output:
-   - **If issues found** (comments left on PR):
-     - Set `phase = "escalated"`, `escalationReason = "second-pass testing found issues"`
-     - Tag story with `escalation-needed`
-     - Assign story to Jon
-     - Post PR comment: `"Escalating to @bigjonroberts — second-pass testing found unresolved issues."`
-     - Shut down the app: `dotnet run -- Reset`
-     - **STOP**
-   - **If no issues** → proceed to Step 9
+There is no manual-testing phase in this repository: it has no application to exercise.

 ## Step 9: Success

-1. Update state file: `phase = "complete"` — its own Bash call, never combined with `Reset` or any kill
-2. **Close verified bugs**: If `state.bugs` is non-empty, fetch issue statuses (`get_issue_statuses(project_id=<verified-project-id>)`) and find the "Closed" status ID. For each bug with status `"merged"`:
-   ```
-   update_issue(issue_id=<bug_id>, status=<closed_status_id>, kwargs={
-       "comment": "Verified fixed — second-pass testing passed. Closed by fully-implement-story orchestrator."
-   })
-   ```
-   Update bug status to `"closed"` in state file.
-3. Update story status to "Ready for review": `update_user_story(user_story_id=<id>, kwargs={"status": <ready_for_review_id>})`
-4. Assign story to Jon: `assign_user_story_to_user(user_story_id=<id>, user_id=<jon_id>)`
-5. Add PR link to Taiga story as a comment:
-   `scripts/taiga-comment.sh <id> "PR: https://github.com/Alterna-Dev-Studio/you-thon/pull/<prNumber>"`
-6. Post PR comment:
+1. Update state file: `phase = "complete"` — its own shell call, never combined with any kill
+2. Re-assert the story status "Ready for test" (finalize-story-pr already set it; this guards against a later change): `update_user_story(user_story_id=<id>, kwargs={"status": <ready_for_test_id>})`
+3. Assign story to Jon: `assign_user_story_to_user(user_story_id=<id>, user_id=<jon_id>)`
+4. Add the PR link to the Taiga story as a comment only if finalize-story-pr's report does not show that it already posted one: `scripts/taiga-comment.sh <id> "PR: <url>"` with `<url>` from `gh pr view <prNumber> --json url -q .url`.
+5. Post PR comment:
    ```
-   gh pr comment <number> --body "Story implementation complete. All checks passing, all comments resolved, manual testing passed. Ready for review."
+   gh pr comment <prNumber> --body "Story implementation complete. Test suite passing, all review threads resolved. Ready for Jon to review."
    ```
-7. Shut down the app: `dotnet run -- Reset` — its own Bash call; no manual `pkill` (`Reset` stops Projector/Watchdog)
-8. Report success to user with PR link, the base branch this run used, and whether it came from the argument or the `defaultBranchRef` lookup.
+6. Report success to user with PR link, the base branch this run used, and whether it came from the argument or the `defaultBranchRef` lookup.

 ## Error handling

@@ -329,9 +244,5 @@
 The resume check at the top of Step 1 decides whether this run resumes (`--resume` in the arguments, or an existing non-terminal state file) and recovers the state. It then jumps to the step for `phase`:
   - `"implementing"` → Step 2 (or Step 2b if all tasks are done but `testReviewComplete` is false)
   - `"monitoring"` → Step 3b (rebase check), then Step 4
-  - `"testing"` → Step 5
-  - `"fixing"` → Step 6
-  - `"post-fix-monitoring"` → Step 3b (rebase check), then Step 7
-  - `"retesting"` → Step 8

-On resume, `<base-branch>` comes from the state file's `baseBranch` key, not from re-resolving Step 0 or assuming `main` — this matters because the `"monitoring"` and `"post-fix-monitoring"` entry points both land on Step 3b, which spawns `$rebase-branch`. If the state file predates this key (written before this change), fall back to the `defaultBranchRef` lookup from Step 0.
+On resume, `<base-branch>` comes from the state file's `baseBranch` key, not from re-resolving Step 0 or assuming `main` — this matters because the `"monitoring"` entry point lands on Step 3b, which spawns `$rebase-branch`. If the state file predates this key (written before this change), fall back to the `defaultBranchRef` lookup from Step 0.

--- saasdk/2a04165/.agents/skills/implement-task/SKILL.md
+++ .agents/skills/implement-task/SKILL.md
@@ -24,7 +24,7 @@
 Check out the branch:
 1. `git checkout <branch-name> && git pull`
 2. If the branch doesn't exist locally: `git fetch origin <branch-name> && git checkout <branch-name>`
-3. If it doesn't exist at all: `git fetch origin +<base>:refs/remotes/origin/<base> && git checkout -b <branch-name> origin/<base>` — this fallback only fires if the branch-creation step in the calling skill (`$fully-implement-story` or `$implement-story`) was skipped or failed, since normally the branch already exists by the time this skill runs. Fetch `<base>` explicitly with the `:refs/remotes/origin/<base>` destination rather than a bare `git fetch origin`: in the shallow single-branch clones `scripts/devcontainer/launch.sh` creates, the clone's `remote.origin.fetch` refspec is restricted to the cloned branch, so a bare fetch never retrieves `<base>`, and fetching it without a destination only populates `FETCH_HEAD`, not the `origin/<base>` ref this command consumes.
+3. If it doesn't exist at all: `git fetch origin +<base>:refs/remotes/origin/<base> && git checkout -b <branch-name> origin/<base>` — this fallback only fires if the branch-creation step in the calling skill (`$fully-implement-story` or `$implement-story`) was skipped or failed, since normally the branch already exists by the time this skill runs.

 Then write the task lock as its own Bash call so the orchestrator can tell you are still alive:
 ```bash
@@ -36,7 +36,7 @@

 Use `scripts/taiga-story.sh <story-ref> <verified-project-id> --with-tasks` for complete task enumeration. Verify that the helper accepts the resolved project ID; if it is fixed to another project, use an equivalent project-scoped paginated lookup and stop if completeness cannot be shown.

-Resolve task statuses live with `get_filters_data(project_id=<verified-project-id>, object_type="task")`; select `<closed-task-id>` by exact `Closed` name and verify it is unambiguous. `get_task_statuses` is unavailable in the selected consumer. Stop before task selection or status writes if the mapping is missing.
+Resolve task statuses live with `get_task_statuses(project_id=<verified-project-id>)`; select `<closed-task-id>` by exact `Closed` name and verify it is unambiguous, cross-checking `status_extra_info.name` / `status_extra_info.is_closed` in the helper listing. Stop before task selection or status writes if the mapping is missing.

 1. Find the story and its tasks: `scripts/taiga-story.sh <story-ref> <verified-project-id> --with-tasks` — returns story JSON with `tasks` array included. Extract `id` and `tasks`.
 2. Fetch full story details: `get_user_story(user_story_id=<id>)` for context
@@ -53,8 +53,6 @@

 ## Step 3: Implement the task

-**If the task involves UI changes**, read `docs/design-system.md` before writing any view code. Follow established color tokens, typography, spacing, component patterns, and the `tw` helper conventions documented there.
-
 1. **If the task description contains a detailed implementation plan** (files to change, implementation details, specific code patterns), skip investigation entirely. Read only the files listed in the plan, then go straight to TDD.
 2. **If there is no implementation plan**, investigate the codebase as needed.
 3. Implement via TDD:
@@ -66,7 +64,7 @@

 ## Step 4: Run tests

-Run **only the directly affected test suite(s)** — not `TestAll`. Consult `docs/testing-workflow.md` in the You-Thon consumer for the local-vs-CI policy and file-to-command routing (including Stripe exception rules).
+Run the consumer suite: `timeout 590 python3 -m unittest discover -s tests -v; echo "exit=$?"` in the foreground. Run `bash -n` and `shellcheck` on any changed Bash file. See `docs/testing-workflow.md`; this repository has no CI gate, so this run is the gate.

 Refresh the task-lock heartbeat immediately before and after the run, each as its own Bash call, so a long suite is not mistaken for a dead agent:
 ```bash
@@ -75,11 +73,11 @@

 Run the suite in the foreground with an explicit exit-code capture:
 ```bash
-timeout 1500 dotnet run -- TestUnit; echo "exit=$?"
+timeout 590 python3 -m unittest discover -s tests -v; echo "exit=$?"
 ```
 Never wait with a `kill -0 $(pgrep -f ...)` loop — `pgrep -f` matches the loop's own shell and never exits (see `AGENTS.md` "Process Hygiene").

-Read the relevant `test-results/*.xml` file for pass/fail status. Parse `<testsuite>` attributes for counts and `<failure>` elements for details. Fix every failure, then re-run the affected suite to verify.
+Read the unittest output for pass/fail; there are no JUnit XML result files. Fix every failure, then re-run the suite to verify.

 **If you believe a failure is unrelated to your changes**, you MUST follow the Test Failure Triage Protocol in `references/test-failure-triage.md` before dismissing it.


--- saasdk/2a04165/.agents/skills/implement-task/references/test-failure-triage.md
+++ .agents/skills/implement-task/references/test-failure-triage.md
@@ -1,7 +1,7 @@
 # Test Failure Triage Protocol

-This reference applies to the selected You-Thon workflows. In another consumer,
-resolve its bug-triage policy, test command, and tracker project before using it.
+This reference is patched for the dev-env-template consumer (Taiga project 4, Python
+`unittest` suite).

 When a test failure occurs and you suspect it is unrelated to your changes, you MUST follow this protocol before dismissing it. Do NOT claim a failure is "pre-existing" or "flaky" without verification.

@@ -13,7 +13,7 @@
 git stash push -u  # stash including untracked files; note whether a stash was created
 git checkout main  # or the appropriate base branch
 # Run ONLY the specific failing test(s), not the full suite
-dotnet run -- <TestTarget>  # with appropriate filter if possible
+python3 -m unittest -v tests.<module>.<Class>.<test_name>  # the failing test only
 ```

 ## Step 2: Evaluate the result
@@ -38,14 +38,13 @@
 2. Search Taiga for an existing bug about this test using a supported search method, for example:
    - Taiga web UI search with relevant test name keywords
    - The `list_issues` MCP tool with an appropriate `filters={...}` query (e.g., by subject, tags, or status)
-3. If no existing bug is found, read the active consumer's bug-filing guidance first
-   (in selected You-Thon, `.claude/skills/shared/bug-filing.md`). Verify the
-   project and status IDs before filing:
+3. If no existing bug is found, file one following `.claude/skills/shared/bug-filing.md`.
+   Verify the project and status IDs before filing:
    - Subject: `Pre-existing test failure: <test name>`
    - Description: Include the test name, test suite, error message, commit hash where verified broken, and which branch/PR discovered it
-   - Severity per `docs/bug-triage.md`: Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
-   - Priority: from the matrix (surface is `ci` unless the failure only reproduces in the local dev stack, then `devx`)
-   - Tags: surface tag, `src:agent`, and `pre-existing-failure`
+   - Severity per [docs/bug-triage.md](../../../../docs/bug-triage.md): Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
+   - Priority: from the matrix (surface is the area the failing test covers: `devx`, `secrets`, `taiga`, or `skills`)
+   - Tags: `repo:dev-env-template`, surface tag, `src:agent`, and `pre-existing-failure`
 4. Note the bug ref number

 ## Step 4: Return to your branch and continue

--- saasdk/2a04165/.agents/skills/finalize-story-pr/SKILL.md
+++ .agents/skills/finalize-story-pr/SKILL.md
@@ -5,7 +5,7 @@

 # Codex runtime and scope

-Invoke as `$finalize-story-pr <arguments>`. Treat the invocation text as the arguments shown below. This package preserves the You-Thon selected Claude-source workflow. Its repository paths, test commands, Taiga statuses, automation, and CI artifacts apply only to that consumer at the verified revision. Read the consumer's applicable `AGENTS.md` and/or `CLAUDE.md` and referenced policy documents first. For another consumer, require an explicit local mapping before execution.
+Invoke as `$finalize-story-pr <arguments>`. Treat the invocation text as the arguments shown below. This package is patched for the dev-env-template consumer: Taiga project 4 with statuses resolved by name, the Python `unittest` suite, and no CI gate. Read the consumer's `AGENTS.md` and referenced policy documents first.

 Discover the available Taiga tools by operation. Before a tracker write, verify the host and project against the consumer configuration, resolve `<verified-project-id>` live (or verify `TAIGA_PROJECT_ID` where used), and resolve status/member IDs by name. A source `mcp__taiga-py__*` operation denotes the equivalent connected Codex tool, not a guaranteed tool identifier. Stop and report a missing connection, authentication, project guard, script, or required permission. Use Codex search/read/patch tools for file inspection and edits, shell execution for Git, GitHub CLI and consumer scripts, and the available web tool when needed. Source `allowed-tools` grants do not carry over.

@@ -33,7 +33,7 @@
    git fetch -q origin +<base-branch>:refs/remotes/origin/<base-branch>
    git log origin/<base-branch>..<branch-name> --oneline
    ```
-   `<base-branch>` is the third argument or the resolved default — never the local `main`. The `origin/` prefix matters: a checkout's local branch is routinely behind its `origin/` counterpart, and measuring against the local ref would report every commit merged since that local ref last moved. Fetch `<base-branch>` explicitly with the `:refs/remotes/origin/<base-branch>` destination rather than a bare `git fetch origin`: in the shallow single-branch clones `scripts/devcontainer/launch.sh` creates, the clone's `remote.origin.fetch` refspec is restricted to the cloned branch, so a bare fetch never retrieves `<base-branch>` when it differs from the checked-out branch, and fetching it without a destination only populates `FETCH_HEAD`, not the `origin/<base-branch>` ref this command consumes.
+   `<base-branch>` is the third argument or the resolved default — never the local `main`. The `origin/` prefix matters: a checkout's local branch is routinely behind its `origin/` counterpart, and measuring against the local ref would report every commit merged since that local ref last moved.
    - If no commits, report "No changes to push" and stop

 ## Step 1b: Test quality review
@@ -44,26 +44,9 @@

 ## Step 2: Run tests

-On build-relevant PRs, CI gates merges with separate `TestUnit`, `TestIntegration`, and `TestE2E` jobs — but run the fast test suites locally first to catch issues early. Consult `docs/testing-workflow.md` in the verified consumer checkout for the local-vs-CI policy and file-to-command routing.
-
-1. Run `dotnet run -- TestUnit` and `dotnet run -- TestIntegration` (requires services already running via `dotnet run -- StartServices`). After each run, read the relevant `test-results/*.xml` file for pass/fail status. Fix any failures before proceeding.
-2. Detect new/modified E2E spec files:
-   ```bash
-   git diff --diff-filter=ACMR --name-only origin/<base-branch>...HEAD -- 'src/Client/tests/e2e/*.spec.ts' | sed 's#.*/##'
-   ```
-3. If any spec files were changed, run each one via `TestE2EDebug` (pass only the filename — `TestE2EDebug` prepends `tests/e2e/` internally):
-   ```bash
-   dotnet run -- TestE2EDebug "<filename>.spec.ts"
-   ```
-   Repeat for each changed spec file. Inspect the Playwright console output for pass/fail results — `TestE2EDebug` uses `--reporter=list` and does not produce `test-results/e2e.xml`.
-4. If **no** E2E spec files were changed, skip E2E testing — CI handles it.
-5. If any E2E failures:
-   a. Use the Playwright console output and any recorded traces/screenshots for failure details
-   b. Fix the failures (this agent has Edit/Write tools)
-   c. **If you believe a failure is unrelated to the story's changes**, you MUST follow the Test Failure Triage Protocol in `references/test-failure-triage.md` before dismissing it.
-   d. Re-run the affected spec to verify
-   e. Commit the fixes
-6. Check if Stripe-related files were changed per the routing rules in `docs/testing-workflow.md` in the verified consumer checkout. If so, also run `dotnet run -- TestStripe` and `dotnet run -- TestStripeE2E`.
+1. Run `timeout 590 python3 -m unittest discover -s tests -v` in the foreground. Read the unittest output; fix every failure before proceeding.
+2. Run `bash -n <file>` and `shellcheck <file>` on each Bash file changed on the branch (`git diff --name-only origin/<base-branch>...HEAD`).
+3. If you believe a failure is unrelated to the story's changes, follow the Test Failure Triage Protocol in `references/test-failure-triage.md` before dismissing it. This repository has no CI gate; this local run is the gate (`docs/testing-workflow.md`).

 ## Step 3: Push and create PR

@@ -86,7 +69,7 @@
    gh pr create --base <base-branch> --reviewer bigjonroberts <merge-labels> --title "#<ref>: <story subject>" --body "$(cat <<'EOF'
    ## Story Context

-   **[#<ref>](https://taiga.unclejons.casa/project/you-thon/us/<ref>): <subject>**
+   **[#<ref>](https://taiga.unclejons.casa/project/alterna-dev-studio/us/<ref>): <subject>**

    <extracted overview, 2-3 sentences max>

@@ -105,9 +88,8 @@

    ## Test plan

-   - [ ] All unit tests pass
-   - [ ] All integration tests pass
-   - [ ] Changed E2E specs pass locally (full E2E suite runs in CI)
+   - [ ] `python3 -m unittest discover -s tests -v` passes locally
+   - [ ] `bash -n` and `shellcheck` clean on changed Bash
    - [ ] Manual review of changes

    ## Known pre-existing failures
@@ -119,8 +101,8 @@
    )"
    ```

-6. Add PR link to Taiga story as a comment:
-   `scripts/taiga-comment.sh <id> "PR: https://github.com/Alterna-Dev-Studio/you-thon/pull/<pr_number>"`
+6. Add PR link to Taiga story as a comment, using the URL GitHub reports (`gh pr view <pr_number> --json url -q .url`):
+   `scripts/taiga-comment.sh <id> "PR: <pr_url>"`
 7. Run the Codex review on the new PR following `references/codex-review.md`. A review failure is reported, not fatal — continue with the remaining steps.

 ## Step 4: Update Taiga
@@ -130,7 +112,7 @@
 3. Update story status to "Ready for test": `update_user_story(user_story_id=<id>, kwargs={"status": <ready_for_test_id>})`
 4. Assign story to Jon: `assign_user_story_to_user(user_story_id=<id>, user_id=<jon_user_id>)`

-**Do NOT set the story to "Done"** yourself. Done happens either by Jon after merging the PR, or by taiga-sync at merge when Step 3 labelled the PR `mark-done-on-merge` (or left that tag on the story).
+**Do NOT set the story to "Done"** yourself. Merge automation (taiga-sync) is not installed in this repository, so the `mark-done-on-merge` label and tag are recorded for planning only; Done is set by Jon after merging the PR.

 ## Step 5: Report


--- saasdk/2a04165/.agents/skills/finalize-story-pr/references/bug-filing.md
+++ .agents/skills/finalize-story-pr/references/bug-filing.md
@@ -1,7 +1,7 @@
 # Bug Filing Protocol

 Follow this whenever a skill or agent creates a Taiga bug. The rubric lives in
-`docs/bug-triage.md`; this file is only the procedure for applying it at filing time.
+[docs/bug-triage.md](../../../../docs/bug-triage.md); this file is only the procedure for applying it at filing time.

 ## Step 1: Resolve IDs

@@ -9,8 +9,8 @@

 - `get_issue_types(project_id=<verified-project-id>)` — the "Bug" type ID
 - `get_issue_statuses(project_id=<verified-project-id>)` — the "New" status ID
-- `get_issue_severities(project_id=<verified-project-id>)` — Minor / Normal / Important / Critical
-- `get_issue_priorities(project_id=<verified-project-id>)` — Low / Normal / High / Urgent
+- `get_issue_severities(project_id=<verified-project-id>)` — Minor / Normal / Important / Critical (Wishlist is not used for bugs)
+- `get_issue_priorities(project_id=<verified-project-id>)` — Low / Normal / High

 ## Step 2: Check for duplicates

@@ -18,18 +18,18 @@
 one: reference the existing ref in your output and, if you have new evidence, add it as a comment
 via `scripts/taiga-comment.sh <id> "<evidence>" --issue`.

-## Step 3: Classify per `docs/bug-triage.md`
+## Step 3: Classify per the triage policy

-1. **Surface** (exactly one): `product`, `devx`, `pipeline`, `ci`.
-2. **Source** (exactly one): `src:user`, `src:monitor`, `src:manual-test`, `src:pr-review`,
-   `src:agent`, `src:jon`. Skills filing on their own behalf use `src:agent`; the manual-testing
-   agent uses `src:manual-test`; PR comment resolution uses `src:pr-review`.
-3. **Severity**: pick from the severity table for that surface. This is provisional; the triage
-   sweep confirms it.
-4. **Priority**: read it off the severity × surface matrix, then apply the modifiers. If you
+1. **Surface** (exactly one): `devx`, `secrets`, `taiga`, `skills`. Always add the repository
+   tag `repo:dev-env-template`; project 4 is shared with other repositories.
+2. **Source** (exactly one): `src:manual-test`, `src:pr-review`, `src:agent`, `src:jon`.
+   Skills filing on their own behalf use `src:agent`; the manual-testing agent uses
+   `src:manual-test`; PR comment resolution uses `src:pr-review`.
+3. **Severity**: pick from the severity table. Triage confirms or corrects it.
+4. **Priority**: read it off the severity matrix, then apply the modifiers. If you
    deviate from the matrix, say why in the description.

-Do not apply the `triaged` tag. Only the triage sweep sets it.
+Do not apply the `triaged` tag. Only triage sets it.

 ## Step 4: Create the issue

@@ -43,7 +43,7 @@
     priority_id=<id>,
     kwargs={
         "description": "<template below>",
-        "tags": [["<surface>", null], ["<source>", null]]
+        "tags": [["repo:dev-env-template", null], ["<surface>", null], ["<source>", null]]
     }
 )
 ```
@@ -58,7 +58,7 @@
 **Actual:** ...
 **Reproduce / observed at:** ...
 **Preliminary cause:** ...
-**Evidence:** <links, log lines, PR, commit hash, GlitchTip issue id>
+**Evidence:** <links, log lines, PR, commit hash>
 ```

 Add any context the filing skill already requires (for example "Discovered during PR #N review"

--- saasdk/2a04165/.agents/skills/finalize-story-pr/references/test-failure-triage.md
+++ .agents/skills/finalize-story-pr/references/test-failure-triage.md
@@ -10,7 +10,7 @@
 git stash push -u  # stash including untracked files; note whether a stash was created
 git checkout main  # or the appropriate base branch
 # Run ONLY the specific failing test(s), not the full suite
-dotnet run -- <TestTarget>  # with appropriate filter if possible
+python3 -m unittest -v tests.<module>.<Class>.<test_name>  # the failing test only
 ```

 ## Step 2: Evaluate the result
@@ -38,9 +38,9 @@
 3. If no existing bug is found, file one following `references/bug-filing.md`:
    - Subject: `Pre-existing test failure: <test name>`
    - Description: Include the test name, test suite, error message, commit hash where verified broken, and which branch/PR discovered it
-   - Severity per `docs/bug-triage.md`: Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
-   - Priority: from the matrix (surface is `ci` unless the failure only reproduces in the local dev stack, then `devx`)
-   - Tags: surface tag, `src:agent`, and `pre-existing-failure`
+   - Severity per [docs/bug-triage.md](../../../../docs/bug-triage.md): Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
+   - Priority: from the matrix (surface is the area the failing test covers: `devx`, `secrets`, `taiga`, or `skills`)
+   - Tags: `repo:dev-env-template`, surface tag, `src:agent`, and `pre-existing-failure`
 4. Note the bug ref number

 ## Step 4: Return to your branch and continue

--- saasdk/2a04165/.agents/skills/rebase-branch/SKILL.md
+++ .agents/skills/rebase-branch/SKILL.md
@@ -5,7 +5,7 @@

 # Codex runtime and consumer scope

-Invoke as `$rebase-branch <PR-number> [target-branch]`. Treat the invocation text as `<arguments>` below. This package preserves the selected You-Thon Claude workflow. Read the target consumer's `AGENTS.md` and applicable `CLAUDE.md`, then verify its project, scripts, documentation, GitHub repository, and status names before acting. You-Thon paths and commands are consumer-owned examples, not files bundled with this package. If a required helper or equivalent operation is absent, stop with the missing dependency; do not invent a replacement.
+Invoke as `$rebase-branch <PR-number> [target-branch]`. Treat the invocation text as `<arguments>` below. This package is patched for the dev-env-template consumer (Taiga project 4, Python `unittest` suite, no CI gate). Read the consumer's `AGENTS.md`, then verify its project, scripts, documentation, GitHub repository, and status names before acting. If a required helper or equivalent operation is absent, stop with the missing dependency; do not invent a replacement.

 Discover connected Taiga tools by semantic operation before use. Verify host and project identity, resolve `<verified-project-id>` live, and resolve status/member IDs immediately before mutation. Use Codex shell, repository search/read/edit, and web tools for the corresponding Claude tool functions under current permissions. Track checklist items in the conversation or an authorized local file. Subagent work uses Codex collaboration workers with explicit file ownership and the active agent limit. Do not invoke Claude agent roles or CLI as a substitute. Preserve each stop and verification condition below.

@@ -21,7 +21,7 @@
   ```bash
   gh pr view <PR> --json baseRefName -q .baseRefName
   ```
-  Step 1's `gh pr view` call below already fetches `baseRefName`, so this is the same value read from that response, not a second lookup. A stacked PR targets a `feature/*` branch, not `main` — rebasing it onto `main` would replay its commits over every sibling it was stacked behind, turning a two-file conflict into the whole stack's diff. When `/fully-implement-story` invokes this skill it always passes the base explicitly, so this fallback only fires on direct invocations and `$remediate-pr`.
+  Step 1's `gh pr view` call below already fetches `baseRefName`, so this is the same value read from that response, not a second lookup. A stacked PR targets a `feature/*` branch, not `main` — rebasing it onto `main` would replay its commits over every sibling it was stacked behind, turning a two-file conflict into the whole stack's diff. When `/fully-implement-story` invokes this skill it always passes the base explicitly, so this fallback only fires on direct invocations.

 Gather information in parallel:

@@ -57,7 +57,7 @@
    git fetch origin
    git fetch origin +<target-branch>:refs/remotes/origin/<target-branch>
    ```
-   The second fetch matters in the shallow single-branch clones `scripts/devcontainer/launch.sh` creates: the clone's `remote.origin.fetch` refspec is restricted to the branch it was cloned from, so the first, bare fetch never retrieves `<target-branch>` when it differs from the checked-out branch. Fetching `<target-branch>` without the `:refs/remotes/origin/<target-branch>` destination would only populate `FETCH_HEAD`, not the `origin/<target-branch>` ref every command below consumes.
+   The second fetch is explicit so that `origin/<target-branch>` exists even when the clone's `remote.origin.fetch` refspec is restricted to the checked-out branch. Fetching `<target-branch>` without the `:refs/remotes/origin/<target-branch>` destination would only populate `FETCH_HEAD`, not the `origin/<target-branch>` ref every command below consumes.

 2. Check out the PR branch (if not already on it):
    ```
@@ -112,17 +112,17 @@
 3. **Determine resolution strategy** using this priority order:

    **a. Additive / non-overlapping changes** (most common for this codebase):
-   Both sides add new content (e.g., new icon bindings in `Icons.fs`, new CSS classes in `index.css`, new helper functions in `TailwindExtensions.fs`). **Keep both.** Combine the additions, maintaining proper ordering (alphabetical for icon bindings, logical grouping for CSS/helpers).
+   Both sides add new content (e.g., new aliases in `shell/aliases.sh`, new PATH entries in `shell/paths.sh`, new test methods in `tests/`). **Keep both.** Combine the additions, maintaining proper ordering (logical grouping for aliases and paths, one test per contract).

    **b. Epic boundary rules** (if epic context is available):
-   The epic description defines which story "owns" which code. If the conflict involves code owned by a specific story, that story's version wins. Example: if the epic says "#829 owns `focusVisible` helper in `TailwindExtensions.fs`", and this PR is for #713, use #829's version of `focusVisible`.
+   The epic description defines which story "owns" which code. If the conflict involves code owned by a specific story, that story's version wins. Example: if the epic says "#829 owns the `envtool` loader in `profile.sh`", and this PR is for #713, use #829's version of that loader.

    **c. Semantic analysis** (when both sides modify the same code):
    - If the target branch refactored/renamed something and the PR branch used the old name, **adopt the target's refactoring** and update the PR's usage.
    - If the PR branch intentionally changed behavior that the target also changed differently, this requires judgment — apply the **escalation check** below.

    **d. Formatting / whitespace conflicts**:
-   Accept whichever side has more context, then let `dotnet run -- Format` clean up.
+   Accept whichever side has more context, then re-run `shellcheck` on the file; there is no formatter.

 4. **Escalation check** — escalate if ANY of these are true:
    - Both sides intentionally changed the same logic/behavior in different ways
@@ -153,8 +153,8 @@

    **Target branch:** <target-branch>
    **Conflicting files:**
-   - `path/to/file1.fs` — <brief description of conflict>
-   - `path/to/file2.fs` — <brief description of conflict>
+   - `path/to/file1.sh` — <brief description of conflict>
+   - `path/to/file2.sh` — <brief description of conflict>

    **Why this needs human judgment:**
    <1-3 sentences explaining why automated resolution isn't safe>
@@ -171,16 +171,18 @@

 3. **Update the Taiga item** (if one was identified in Step 2):

+   Project 4 has no "Blocked" status for stories or issues, so escalation is signalled with tags and assignment instead of a status change.
+
    **If `taigaType` is `"story"`:**
-   - Fetch statuses: `get_user_story_statuses(project_id=<verified-project-id>)` — find "Blocked" status ID
-   - Fetch members: `get_project_members(project_id=<verified-project-id>)` — find Jon's user ID
-   - Update story: `update_user_story(user_story_id=taigaId, kwargs={"status": <blocked_id>, "tags": <existing_tags> + [["rebase-conflict", null]]})`
+   - Re-fetch the story to get its current tags: `get_user_story(user_story_id=taigaId)`
+   - Fetch members: `get_project_members(project_id=<verified-project-id>)` — find Jon's user ID (bigjonroberts)
+   - Update story: `update_user_story(user_story_id=taigaId, kwargs={"tags": <existing_tags> + [["escalation-needed", null], ["rebase-conflict", null]]})`
    - Assign to Jon: `assign_user_story_to_user(user_story_id=taigaId, user_id=<jon_user_id>)`

    **If `taigaType` is `"issue"`:**
-   - Fetch statuses: `get_issue_statuses(project_id=<verified-project-id>)` — find "Blocked" status ID
-   - Fetch members: `get_project_members(project_id=<verified-project-id>)` — find Jon's user ID
-   - Update issue: `update_issue(issue_id=taigaId, kwargs={"status": <blocked_id>, "tags": <existing_tags> + [["rebase-conflict", null]]})`
+   - Re-fetch the issue to get its current tags: `get_issue(issue_id=taigaId)`
+   - Fetch members: `get_project_members(project_id=<verified-project-id>)` — find Jon's user ID (bigjonroberts)
+   - Update issue: `update_issue(issue_id=taigaId, kwargs={"tags": <existing_tags> + [["escalation-needed", null], ["rebase-conflict", null]]})`
    - Assign to Jon: `assign_issue_to_user(issue_id=taigaId, user_id=<jon_user_id>)`

    **If no Taiga item was identified:** skip Taiga updates.
@@ -213,25 +215,19 @@
    ```
    The PR's commits should be replayed on top of the target branch.

-### 6b. Build check
+### 6b. Syntax check

-Run a quick build to catch compilation errors introduced by the rebase:
+There is no build. Run `bash -n <file>` on every Bash file changed on the branch and `python3 -m py_compile <file>` on every changed Python file (`git diff --name-only origin/<target-branch>...HEAD`) to catch syntax errors introduced by the rebase.

-```
-dotnet run -- Build
-```
-
-If the build fails:
-1. Read the compiler errors carefully.
-2. These are likely due to the rebase combining changes that compile independently but not together (e.g., a function signature changed on main, and the PR calls it with the old signature).
-3. Fix the compilation errors. If you're still in the middle of the rebase, stage the fixes and run `git rebase --continue`. If the rebase has completed, commit the fixes as a new commit (do **not** amend rebased commits).
-4. If the build errors are too complex to resolve confidently, **escalate** per Step 5c.
+If a check fails:
+1. Read the error carefully.
+2. It is likely due to the rebase combining changes that are valid independently but not together (e.g., a function renamed on the target, and the PR calls it by the old name).
+3. Fix the errors. If you're still in the middle of the rebase, stage the fixes and run `git rebase --continue`. If the rebase has completed, commit the fixes as a new commit (do **not** amend rebased commits).
+4. If the errors are too complex to resolve confidently, **escalate** per Step 5c.

 ### 6c. Run tests

-Run the test suites most likely affected by the conflicting files. Consult `docs/testing-workflow.md` for the local-vs-CI policy and file-to-command routing. On build-relevant PRs, CI gates merges with separate `TestUnit`, `TestIntegration`, and `TestE2E` jobs.
-
-After the run, inspect the relevant `test-results/*.xml` files for the suites you ran.
+Run `timeout 590 python3 -m unittest discover -s tests -v` in the foreground and read the unittest output for pass/fail (there are no JUnit XML result files). See `docs/testing-workflow.md`; this repository has no CI gate, so this local run is the gate.

 If tests fail:
 1. You MUST follow the Test Failure Triage Protocol in [test failure triage](references/test-failure-triage.md) to determine whether the failure is due to the rebase resolution or a pre-existing issue. Do NOT assume a failure is pre-existing without verifying on the base branch.
@@ -241,7 +237,7 @@

 ## Step 7: Force-push

-Once the build passes and tests are green (or failures are pre-existing):
+Once the syntax checks pass and tests are green (or failures are pre-existing):

 ```
 git push --force-with-lease origin <head-branch>
@@ -262,7 +258,7 @@
 **Rebased onto:** `<target-branch>` (<short SHA>)

 ### Conflicts Resolved
-- `path/to/file.fs` — <brief description of resolution>
+- `path/to/file.sh` — <brief description of resolution>

 ### Resolution Strategy
 <1-2 sentences: e.g., "Additive changes combined" or "Adopted main's refactoring of X, updated PR's usage">

--- saasdk/2a04165/.agents/skills/rebase-branch/references/bug-filing.md
+++ .agents/skills/rebase-branch/references/bug-filing.md
@@ -1,7 +1,7 @@
 # Bug Filing Protocol

 Follow this whenever a skill or agent creates a Taiga bug. The rubric lives in
-`docs/bug-triage.md`; verify the consumer project and read that policy before filing. This file is only the procedure for applying it at filing time.
+[docs/bug-triage.md](../../../../docs/bug-triage.md); verify the consumer project and read that policy before filing. This file is only the procedure for applying it at filing time.

 ## Step 1: Resolve IDs

@@ -9,8 +9,8 @@

 - `get_issue_types(project_id=<verified-project-id>)` — the "Bug" type ID
 - `get_issue_statuses(project_id=<verified-project-id>)` — the "New" status ID
-- `get_issue_severities(project_id=<verified-project-id>)` — Minor / Normal / Important / Critical
-- `get_issue_priorities(project_id=<verified-project-id>)` — Low / Normal / High / Urgent
+- `get_issue_severities(project_id=<verified-project-id>)` — Minor / Normal / Important / Critical (Wishlist is not used for bugs)
+- `get_issue_priorities(project_id=<verified-project-id>)` — Low / Normal / High

 ## Step 2: Check for duplicates

@@ -18,18 +18,18 @@
 one: reference the existing ref in your output and, if you have new evidence, add it as a comment
 via `scripts/taiga-comment.sh <id> "<evidence>" --issue`.

-## Step 3: Classify per `docs/bug-triage.md`
+## Step 3: Classify per the triage policy

-1. **Surface** (exactly one): `product`, `devx`, `pipeline`, `ci`.
-2. **Source** (exactly one): `src:user`, `src:monitor`, `src:manual-test`, `src:pr-review`,
-   `src:agent`, `src:jon`. Skills filing on their own behalf use `src:agent`; the manual-testing
-   agent uses `src:manual-test`; PR comment resolution uses `src:pr-review`.
-3. **Severity**: pick from the severity table for that surface. This is provisional; the triage
-   sweep confirms it.
-4. **Priority**: read it off the severity × surface matrix, then apply the modifiers. If you
+1. **Surface** (exactly one): `devx`, `secrets`, `taiga`, `skills`. Always add the repository
+   tag `repo:dev-env-template`; project 4 is shared with other repositories.
+2. **Source** (exactly one): `src:manual-test`, `src:pr-review`, `src:agent`, `src:jon`.
+   Skills filing on their own behalf use `src:agent`; the manual-testing agent uses
+   `src:manual-test`; PR comment resolution uses `src:pr-review`.
+3. **Severity**: pick from the severity table. Triage confirms or corrects it.
+4. **Priority**: read it off the severity matrix, then apply the modifiers. If you
    deviate from the matrix, say why in the description.

-Do not apply the `triaged` tag. Only the triage sweep sets it.
+Do not apply the `triaged` tag. Only triage sets it.

 ## Step 4: Create the issue

@@ -43,7 +43,7 @@
     priority_id=<id>,
     kwargs={
         "description": "<template below>",
-        "tags": [["<surface>", null], ["<source>", null]]
+        "tags": [["repo:dev-env-template", null], ["<surface>", null], ["<source>", null]]
     }
 )
 ```
@@ -58,7 +58,7 @@
 **Actual:** ...
 **Reproduce / observed at:** ...
 **Preliminary cause:** ...
-**Evidence:** <links, log lines, PR, commit hash, GlitchTip issue id>
+**Evidence:** <links, log lines, PR, commit hash>
 ```

 Add any context the filing skill already requires (for example "Discovered during PR #N review"

--- saasdk/2a04165/.agents/skills/rebase-branch/references/test-failure-triage.md
+++ .agents/skills/rebase-branch/references/test-failure-triage.md
@@ -10,7 +10,7 @@
 git stash push -u  # stash including untracked files; note whether a stash was created
 git checkout main  # or the appropriate base branch
 # Run ONLY the specific failing test(s), not the full suite
-dotnet run -- <TestTarget>  # with appropriate filter if possible
+python3 -m unittest -v tests.<module>.<Class>.<test_name>  # the failing test only
 ```

 ## Step 2: Evaluate the result
@@ -38,9 +38,9 @@
 3. If no existing bug is found, file one following [bug filing](bug-filing.md):
    - Subject: `Pre-existing test failure: <test name>`
    - Description: Include the test name, test suite, error message, commit hash where verified broken, and which branch/PR discovered it
-   - Severity per `docs/bug-triage.md`: Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
-   - Priority: from the matrix (surface is `ci` unless the failure only reproduces in the local dev stack, then `devx`)
-   - Tags: surface tag, `src:agent`, and `pre-existing-failure`
+   - Severity per [docs/bug-triage.md](../../../../docs/bug-triage.md): Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
+   - Priority: from the matrix (surface is the area the failing test covers: `devx`, `secrets`, `taiga`, or `skills`)
+   - Tags: `repo:dev-env-template`, surface tag, `src:agent`, and `pre-existing-failure`
 4. Note the bug ref number

 ## Step 4: Return to your branch and continue

--- saasdk/2a04165/.agents/skills/shared/synchronous-worker-contract.md
+++ .agents/skills/shared/synchronous-worker-contract.md
@@ -4,16 +4,17 @@
 result as the completion of that work. The worker must:

 - Wait for every subagent it starts and every command session it opens. A
-  running build, test, script, or seed job is not completion evidence.
-- Use a sufficiently long foreground command timeout for slow work. If a
+  running test run or script is not completion evidence.
+- Use a sufficiently long foreground command timeout for slow work (the
+  unittest suite, `python3 -m unittest discover -s tests -v`). If a
   command outlives its timeout, split or rerun it and verify the final result.
 - Follow the invoked skill through its defined terminal state and inspect the
   required artifacts before returning. Some skills intentionally leave an
   analysis or review result uncommitted; their own completion evidence still
   applies.
-- Report what was verified, including any commit, CI state, tracker update,
-  or browser result. Do not report a started task as completed.
+- Report what was verified, including any commit, test result, or tracker
+  update. Do not report a started task as completed.

-This is the Codex adaptation of You-Thon's
-`.claude/skills/shared/synchronous-worker-contract.md` at
-`d9b8033a7a0b5f502bfb3120793d12ae4f17aa87`.
+This is the Codex adaptation of
+`.claude/skills/shared/synchronous-worker-contract.md`, patched for the
+dev-env-template consumer.

--- saasdk/2a04165/.codex/agents/senior-software-developer.toml
+++ .codex/agents/senior-software-developer.toml
@@ -1,64 +1,53 @@
 name = "senior-software-developer"
-description = "Senior software developer who implements story tasks and fixes bugs via TDD, and analyzes stories for implementation planning. Use for task implementation, bug fixing, story analysis, and PR finalization."
+description = "Senior software developer who implements story tasks via TDD, analyzes stories for implementation planning, and finalizes or rebases story PRs. Use for task implementation, story analysis, and PR finalization."
 model_reasoning_effort = "high"
 developer_instructions = '''
 ## Codex execution

 Use the named skill from `.agents/skills/<skill-name>/SKILL.md` when it is available in the deployed workspace. Read its instructions before acting; a source frontmatter `skills:` list does not preload a Codex skill. Follow the parent task's scope and repository rules. The parent owns any concurrency or worktree isolation. Do not assume Claude tool permissions or `run_in_background` semantics.

-You are a senior F# software developer working on the You-thon project — a SAFE Stack web application for creating personal challenges to raise money for charities.
+You are a senior software developer working in the dev-env-template repository — a small Bash/Python home for shared development-tool configuration (see AGENTS.md).

 ## Expertise

-- F# with Saturn/Giraffe, Fable, Elmish, React (via Feliz)
-- Event sourcing with Equinox and Propulsion
-- PostgreSQL with FSharp.Data.Npgsql type provider
-- Tailwind CSS styling
-- Playwright E2E testing
+- Bash: `set -euo pipefail`, idempotent startup-file edits, PATH hygiene (no duplicate entries, `~/.local/bin` first)
+- Python standard library only (no third-party imports)
+- SOPS/age secrets handling: never print or write plaintext secrets
+- Python `unittest` suites that run against a temporary `HOME` and temporary repository copies

 ## Working Style

 - Follow TDD strictly: failing test first, then the smallest implementation to make it pass
 - Commit frequently with descriptive messages
-- Follow the deployed consumer repository instructions and coding rules — especially ABOUTME comments on code files, no unrelated changes, and no temporal comments
+- Follow the deployed consumer repository instructions and coding rules — especially the Bash and secrets rules above, no unrelated changes, and no temporal comments
 - When the task description contains a detailed implementation plan, skip investigation and go straight to TDD
 - When blocked, explain clearly what's needed rather than guessing

 ## Completion contract

-Run delegated work to completion before returning. Wait for each Codex subagent or shell session you start, and inspect its final result. Do not leave tests, builds, or seeding running after your turn. Verify the evidence required by the invoked skill and report what finished, including any commit, CI status, Taiga update, or browser result. Follow `.agents/skills/shared/synchronous-worker-contract.md`, the native Codex adaptation of the source contract.
+Run delegated work to completion before returning. Wait for each Codex subagent or shell session you start, and inspect its final result. Do not leave tests or scripts running after your turn. Verify the evidence required by the invoked skill and report what finished, including any commit, test result, or Taiga update. Follow `.agents/skills/shared/synchronous-worker-contract.md`, the native Codex adaptation of the source contract.

 ## How You Work

 The orchestrator will tell you which skill to follow. Use these available Codex skills when the orchestrator names one:

 - **implement-task** — implement a single story task with TDD, commit without pushing
-- **fix-single-bug** — fix a single bug on its own branch off main, create PR (used by fully-fix-bugs orchestrator)
-- **fix-story-bug** — fix a single bug on a sub-branch targeting a feature branch
-- **fix-build-failure** — diagnose and fix a CI build failure on a PR branch
-- **finalize-story-pr** — run affected tests, push branch, create PR, update Taiga
+- **finalize-story-pr** — run the test suite, push branch, create PR, update Taiga
 - **rebase-branch** — rebase a PR branch onto a target branch, resolve conflicts using story/epic context, escalate when stuck
 - **analyze-story** — analyze a Taiga user story and produce a detailed implementation plan

 Follow the instructions in whichever skill the orchestrator references. Do not deviate from the skill's workflow.

-## UI Work
-
-When implementing UI changes, read `docs/design-system.md` before writing view code. Follow the established color tokens, typography, spacing, component patterns, and `tw` helper conventions.
-
 ## Quality Standards

 - Never cut corners on tests
 - Never add workarounds instead of root cause fixes
-- Run only the affected test suite(s) after changes — see [docs/testing-workflow.md](../../docs/testing-workflow.md) for the local-vs-CI policy for file-to-command routing
-- Read test result XML files to verify pass/fail status
+- Run `python3 -m unittest discover -s tests -v` after changes, plus `bash -n` and `shellcheck` on changed Bash — see `docs/testing-workflow.md`; there is no CI gate, so the local run is the gate
+- Read the unittest output to verify pass/fail status

 ## Available skill references

 - `.agents/skills/implement-task/SKILL.md`
-- `.agents/skills/fix-single-bug/SKILL.md`
-- `.agents/skills/fix-story-bug/SKILL.md`
-- `.agents/skills/fix-build-failure/SKILL.md`
 - `.agents/skills/finalize-story-pr/SKILL.md`
 - `.agents/skills/rebase-branch/SKILL.md`
 - `.agents/skills/analyze-story/SKILL.md`

--- saasdk/2a04165/.codex/agents/test-quality-reviewer.toml
+++ .codex/agents/test-quality-reviewer.toml
@@ -6,15 +6,15 @@

 Use the named skill from `.agents/skills/<skill-name>/SKILL.md` when it is available in the deployed workspace. Read its instructions before acting; a source frontmatter `skills:` list does not preload a Codex skill. Follow the parent task's scope and repository rules. The parent owns any concurrency or worktree isolation. Do not assume Claude tool permissions or `run_in_background` semantics.

-You are a test quality engineer for the You-thon project. Your job is to review test code that has been written and ensure it complies with the project's testing strategy.
+You are a test quality engineer for the dev-env-template repository — a small Bash/Python home for shared development-tool configuration (see AGENTS.md). Your job is to review test code that has been written and ensure it complies with the project's testing strategy.

 ## Expertise

-- F# test frameworks: Expecto, Fable.Mocha, xUnit (know the registration patterns, assertion styles, and project wiring for each)
-- Playwright E2E testing (TypeScript)
-- Test suite architecture: knowing what belongs at each level of the test pyramid
-- Identifying and eliminating redundant cross-level test duplication
-- Recognizing anti-patterns: CSS class assertions, production logic reimplementation, non-deterministic time
+- Python `unittest`: discovery, `TestCase` structure, assertion styles
+- Subprocess-driven Bash tests that execute shell commands and sourced files
+- Temporary-`HOME` and temporary-repository isolation (no host SOPS identity, no real `~/.bashrc`, no network)
+- Identifying and eliminating tests that duplicate a contract another test already covers
+- Recognizing anti-patterns: helpers reimplementing the implementation, tests that pass on a shell error

 ## Working Style

@@ -22,12 +22,12 @@
 - **Always explain WHY** -- every change you make must be documented with the specific rule it enforces, citing the section from testing-strategy.md
 - Comment on the PR and/or Taiga story with a structured summary of all changes
 - You have full authority to move, delete, and rewrite tests -- but you must justify each action
-- Run affected test suites after making changes to verify nothing breaks -- see [docs/testing-workflow.md](../../docs/testing-workflow.md) for the local-vs-CI policy for file-to-command routing
+- Run `python3 -m unittest discover -s tests -v` after making changes to verify nothing breaks -- see `docs/testing-workflow.md`; there is no CI gate, so the local run is the gate
 - Follow the deployed consumer repository instructions and coding rules

 ## Completion contract

-Run delegated work to completion before returning. Wait for each Codex subagent or shell session you start, and inspect its final result. Do not leave tests, builds, or seeding running after your turn. Verify the evidence required by the invoked skill and report what finished, including any commit, CI status, Taiga update, or browser result. Follow `.agents/skills/shared/synchronous-worker-contract.md`, the native Codex adaptation of the source contract.
+Run delegated work to completion before returning. Wait for each Codex subagent or shell session you start, and inspect its final result. Do not leave tests or scripts running after your turn. Verify the evidence required by the invoked skill and report what finished, including any commit, test result, or Taiga update. Follow `.agents/skills/shared/synchronous-worker-contract.md`, the native Codex adaptation of the source contract.

 ## How You Work

@@ -39,15 +39,11 @@

 ## Anti-Patterns You Catch

-1. **Wrong suite**: Test file in the wrong test project (e.g., domain validation test in Client instead of Shared)
-2. **Redundant coverage**: Same business rule tested exhaustively at multiple levels (only the authoritative level gets full coverage)
-3. **CSS class assertions**: `Expect.stringContains html "bg-blue-500"` -- should assert semantic content
-4. **Icon assertions**: Checking specific icon paths or names
-5. **Production logic reimplementation**: Test helpers with match expressions mirroring production code
-6. **Non-deterministic time**: `DateTime.Now`, `DateTime.Today`, `DateTimeOffset.UtcNow` in test code
-7. **E2E setup waste**: Full UI flows for preconditions when API helpers exist
-8. **Missing test registration**: New test file without `.fsproj` entry or aggregator registration
-9. **Unwarranted E2E**: New E2E tests outside the closed golden-flow list, bounding-box/layout assertions in E2E, new `describe.serial`, or `waitForTimeout` in new tests
+1. **Wrong file for the change**: a test placed outside the authoritative location in the `docs/testing-strategy.md` table (e.g., a PATH or alias test in `tests/test_scripts.py` instead of `tests/test_shell.py`)
+2. **Duplicate contract**: the same behavior tested again without covering a distinct contract
+3. **Helper reimplementing the implementation**: test helpers that reproduce the script's logic instead of observing an outcome
+4. **Host leakage**: tests that read the host's SOPS identity, touch the real `~/.bashrc`, or require network access instead of a temporary `HOME`
+5. **Silent shell errors**: a sourced-profile test that passes when the shell command fails or stderr contains an unexpected missing-file or load error (negative tests that intentionally expect stderr are fine)

 ## Available skill references


--- saasdk/2a04165/.codex/agents/remediation-developer.toml
+++ .codex/agents/remediation-developer.toml
@@ -1,45 +1,42 @@
 name = "remediation-developer"
-description = "Resolves PR review comments and fixes build failures. Use for PR maintenance and CI remediation."
+description = "Resolves PR review comments and rebases PR branches. Use for PR maintenance."
 model_reasoning_effort = "medium"
 developer_instructions = '''
 ## Codex execution

 Use the named skill from `.agents/skills/<skill-name>/SKILL.md` when it is available in the deployed workspace. Read its instructions before acting; a source frontmatter `skills:` list does not preload a Codex skill. Follow the parent task's scope and repository rules. The parent owns any concurrency or worktree isolation. Do not assume Claude tool permissions or `run_in_background` semantics.

-You are a developer focused on code quality and CI health for the You-thon project. You are not an implementer — you are a maintainer.
+You are a developer focused on code quality and PR health for the dev-env-template repository — a small Bash/Python home for shared development-tool configuration (see AGENTS.md). You are not an implementer — you are a maintainer.

 ## Working Style

 - Evaluate review comments on their technical merits — not a rubber stamp
 - Make minimal, targeted fixes
-- Always run affected tests before committing — see [docs/testing-workflow.md](../../docs/testing-workflow.md) for the local-vs-CI policy for file-to-command routing
-- When resolving PR comments or fixing builds, ALWAYS push directly to the PR's existing branch — never create a new branch or PR
+- Always run `python3 -m unittest discover -s tests -v` (plus `bash -n` and `shellcheck` on changed Bash) before committing — see `docs/testing-workflow.md`; there is no CI gate, so the local run is the gate
+- When resolving PR comments or rebasing, ALWAYS push directly to the PR's existing branch — never create a new branch or PR
 - Follow the deployed consumer repository instructions and coding rules
 - Operate autonomously without asking for human input
 - Make decisions and explain them clearly in PR replies

 ## Completion contract

-Run delegated work to completion before returning. Wait for each Codex subagent or shell session you start, and inspect its final result. Do not leave tests, builds, or seeding running after your turn. Verify the evidence required by the invoked skill and report what finished, including any commit, CI status, Taiga update, or browser result. Follow `.agents/skills/shared/synchronous-worker-contract.md`, the native Codex adaptation of the source contract.
+Run delegated work to completion before returning. Wait for each Codex subagent or shell session you start, and inspect its final result. Do not leave tests or scripts running after your turn. Verify the evidence required by the invoked skill and report what finished, including any commit, test result, or Taiga update. Follow `.agents/skills/shared/synchronous-worker-contract.md`, the native Codex adaptation of the source contract.

 ## How You Work

 The orchestrator will tell you which skill to follow and which PR to work on:

 - **pr-comments-resolve** — evaluate, fix, reply to, and resolve PR review comment threads
-- **fix-build-failure** — diagnose and fix CI build failures on a PR branch
 - **rebase-branch** — rebase a PR branch onto a target branch, resolve conflicts, escalate when stuck

 ## Decision Making

 - For review comments: decide agree/disagree/partial on technical merit. If a suggestion would violate project conventions in the deployed consumer repository instructions, disagree and cite the rule.
-- For build failures: diagnose the root cause before fixing. Never add workarounds.
+- For rebase conflicts: understand both sides before resolving. Never add workarounds.

 ## Available skill references

 - `.agents/skills/pr-comments-resolve/SKILL.md`
-- `.agents/skills/fix-build-failure/SKILL.md`
 - `.agents/skills/rebase-branch/SKILL.md`
-- `.agents/skills/remediate-pr/SKILL.md`

 '''
```

### Known limits

- No CI, so no stability monitoring: the suite run inside `finalize-story-pr`
  is the gate, and the orchestrator's Step 4 only loops on unresolved review
  threads.
- No manual-testing phase: there is no application to exercise, so
  `fix-story-bug`, `senior-manual-testing-specialist`, `remediate-pr`, and
  `implement-epic` are not installed.
- `~/.claude/agents/` may hold You-Thon copies of `senior-software-developer`
  and `remediation-developer`; the repository-level files shadow them by name
  but do not remove them.
- The Codex package has not passed a native runtime smoke; only the read-only
  discovery smoke below was run. Whether the local Codex CLI reads
  `.codex/agents/*.toml` as worker roles is not verified here.
- The orchestrator's write paths (state file, task closing, escalation tags,
  PR comments) and the `rebase-branch` conflict path were not exercised by this
  install.
- `.claude/skills/shared/merge-side-effects.md` still shows You-Thon IDs in its
  examples, as recorded in the first section.

### Verification

```bash
python3 -m unittest discover -s tests -v        # 17 passed (SkillTests adds 3)
git diff --check                                 # clean
grep -rn 'dotnet\|project_id=3\|remediate_pr\|Reset' .claude/skills/fully-implement-story \
  .claude/skills/implement-task .claude/skills/finalize-story-pr .claude/skills/rebase-branch \
  .claude/agents .agents/skills/fully-implement-story .agents/skills/implement-task \
  .agents/skills/finalize-story-pr .agents/skills/rebase-branch .codex      # no output
python3 -c 'import tomllib,sys; [tomllib.load(open(p,"rb")) for p in sys.argv[1:]]' .codex/agents/*.toml   # exit 0
sha256sum <each path above>                      # matches the Installed column
```

Every relative Markdown link under `.claude/`, `.agents/`, and `.codex/`
resolves (checked by `tests/test_skills.py` and by a shell loop over every
`](...md)` link).

Claude discovery smoke (plan mode, no MCP servers):

```bash
claude -p 'Invoke /fully-implement-story 2500 but stop before the first Taiga call. Report the skill file used, the project id, the first helper command, every skill/agent/script the body would invoke, and any that is missing.' \
  --permission-mode plan --strict-mcp-config --mcp-config '{"mcpServers":{}}'
```

Observed: it loaded `.claude/skills/fully-implement-story/SKILL.md`, reported
project 4, resolved the base branch to the repository default, found no state
file and no feature branch for 2500 (a fresh start), and named
`scripts/taiga-story.sh 2500 4 --with-tasks` as the first helper command and
first Taiga call. It listed the skills `implement-task`, `review-tests`,
`finalize-story-pr`, `rebase-branch`, and `pr-comments-resolve`, the agents
`senior-software-developer`, `test-quality-reviewer`, and
`remediation-developer`, and the `taiga-story.sh` and `taiga-comment.sh`
helpers, all present. The only item it called missing was the `mcp__taiga-py__*`
tool set, which the smoke deliberately ran without (`--mcp-config
'{"mcpServers":{}}'`); every file, script, agent, and skill resolved. The
smoke printed a warning about a wildcard permission rule in the user-level
`~/.claude/settings.json`; that rule is personal configuration, not part of
this repository.

Codex discovery smoke (read-only, ephemeral):

```bash
codex exec --sandbox read-only --ephemeral -C . 'Invoke $fully-implement-story 2500 but stop after reading AGENTS.md, the skill and its references, and before the first Taiga call. Report the skill file used, the project id, the first helper command, every skill, worker role file, and script the body would invoke, and any that is missing.'
```

Observed: it read `.agents/skills/fully-implement-story/SKILL.md` and its
`references/merge-side-effects.md`, reported project 4 from `AGENTS.md`, the
first helper command `scripts/taiga-story.sh 2500 4 --with-tasks` (after the
`gh repo view` default-branch lookup), the skills `implement-task`,
`review-tests`, `finalize-story-pr`, `rebase-branch` (conditional), and
`pr-comments-resolve` (conditional), the three `.codex/agents/*.toml` role
files, and the three `scripts/*.sh` helpers, all present. The only items it
called missing are the merge automation files that `merge-side-effects.md`
mentions and that `AGENTS.md` already records as not installed.
