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
| `.claude/skills/review-tests/SKILL.md` | `d3a5632a7c596c9dd3e01cde8d45aff47ca148285314f8baaddabc9e10d1e277` | byte-identical |
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
| `.agents/skills/review-tests/SKILL.md` | `b2cd4a1487f830fb7a5e8ffdb0785ea9bd360c6456a5283cbaea59a838af1057` | byte-identical |
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
Unified diffs:

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
| `.claude/skills/pr-comments-resolve/SKILL.md` | `d558ed145b4cc3460ab9dd320dac4686918d77156d1c2cc7b1ec035aa7ea2d97` | patched, `7ed39412ea3888d1dfc4bc2a677ed7d7ca1107b0658cbd6c85866dd690ae4b9f` |
| `.claude/skills/shared/test-failure-triage.md` | `986039f042632873eec99843d761819d06c24b42909b6fc36790bd166f308958` | patched, `a5f200abe63499f37eea24283ea8e77c0c1dfc6a1183703c2b52fedf4cb094bf` |
| `.claude/skills/shared/bug-filing.md` | `34141f5eea232fe99e013c33f173d3c976534874f3d94f14c1fa4dcb1c50c29e` | patched, `acc0bcbc5ebc15200ff4a62d5069f8258824235273320f87fc3f5ae38ff50bd0` |
| `.claude/skills/shared/commit-attribution.md` | `b357f72263d3cd2409fa5d5c6acb1996ed4f9d4543e84db9a01351f28b56b82c` | already installed, byte-identical |
| `.agents/skills/pr-comments-resolve/SKILL.md` | `beb66af45fee15f1221e7707e4ac9924e3c5cd6eea2ef944c4c599e83c48b430` | patched, `57de6bf0c963957a1b8263248c0e3108699313fb62ab9bfbfb2109de826c79c1` |
| `.agents/skills/pr-comments-resolve/references/test-failure-triage.md` | `8c66fec2e5b1a2aca37129d96affb0540a697620fbbea40e0dde27f6bb2a4ea7` | patched, `79d23a969bd222d6896e55f31b21f7b4a7373398f12c0d9641eca179aab6036f` |
| `.agents/skills/pr-comments-resolve/references/bug-filing.md` | `497aa2f56141a0df6457eee65fbfba2f4604ff0bc41c804cd8acdc47eccf33bb` | patched, `0cfdbb088b0456cc9e46ca81c9e4aa54dcc22973cca81d6b5a9716cfbd2bb1ca` |
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
are resolved by name. Unified diffs:

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
+**For bugs (Issues):** follow `.claude/skills/shared/bug-filing.md` with source tag `src:pr-review`. Severity and priority come from `docs/bug-triage.md`, not from a guess; that policy is not installed in this repository, so follow the consumer note in `bug-filing.md`. Prefix the description template with:

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
@@ -3,18 +3,24 @@
 Follow this whenever a skill or agent creates a Taiga bug. The rubric lives in
 `docs/bug-triage.md`; this file is only the procedure for applying it at filing time.

+**Consumer note:** this repository does not install `docs/bug-triage.md` (You-Thon's
+product-specific policy). Until a consumer policy exists, use the surface and source tags below,
+choose a provisional severity and priority by name from the project's lists based on the bug's
+actual impact, and add `Severity and priority are provisional: no consumer triage policy.` to the
+description.
+
 ## Step 1: Resolve IDs

 Fetch once per session, in parallel:

-- `get_issue_types(project_id=3)` — the "Bug" type ID
-- `get_issue_statuses(project_id=3)` — the "New" status ID
-- `get_issue_severities(project_id=3)` — Minor / Normal / Important / Critical
-- `get_issue_priorities(project_id=3)` — Low / Normal / High / Urgent
+- `get_issue_types(project_id=4)` — the "Bug" type ID
+- `get_issue_statuses(project_id=4)` — the "New" status ID
+- `get_issue_severities(project_id=4)` — Minor / Normal / Important / Critical
+- `get_issue_priorities(project_id=4)` — Low / Normal / High / Urgent

 ## Step 2: Check for duplicates

-`search(project_id=3, text="<key terms>")`. If a matching open issue exists, do not create a new
+`search_project(project_id=4, text="<key terms>")`. If a matching open issue exists, do not create a new
 one: reference the existing ref in your output and, if you have new evidence, add it as a comment
 via `scripts/taiga-comment.sh <id> "<evidence>" --issue`.

@@ -35,7 +41,7 @@

 ```
 create_issue(
-    project_id=3,
+    project_id=4,
     subject="<concise title>",
     type_id=<bug_type_id>,
     status_id=<new_status_id>,
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
@@ -38,7 +38,7 @@
 3. If no existing bug is found, file one following `.claude/skills/shared/bug-filing.md`:
    - Subject: `Pre-existing test failure: <test name>`
    - Description: Include the test name, test suite, error message, commit hash where verified broken, and which branch/PR discovered it
-   - Severity per `docs/bug-triage.md`: Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
+   - Severity per `docs/bug-triage.md` (not installed here; see the consumer note in bug filing): Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
    - Priority: from the matrix (surface is `ci` unless the failure only reproduces in the local dev stack, then `devx`)
    - Tags: surface tag, `src:agent`, and `pre-existing-failure`
 4. Note the bug ref number
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
+**For bugs (Issues):** follow [bug filing](references/bug-filing.md) with source tag `src:pr-review`. Severity and priority come from `docs/bug-triage.md`, not from a guess; that policy is not installed in this repository, so follow the consumer note in [bug filing](references/bug-filing.md). Prefix the description template with:

 ```
 Discovered during PR #<arguments> review.
--- you-thon/7988416/.agents/skills/pr-comments-resolve/references/bug-filing.md
+++ .agents/skills/pr-comments-resolve/references/bug-filing.md
@@ -3,6 +3,12 @@
 Follow this whenever a skill or agent creates a Taiga bug. The rubric lives in
 `docs/bug-triage.md`; verify the consumer project and read that policy before filing. This file is only the procedure for applying it at filing time.

+**Consumer note:** this repository does not install `docs/bug-triage.md` (You-Thon's
+product-specific policy). Until a consumer policy exists, use the surface and source tags below,
+choose a provisional severity and priority by name from the project's lists based on the bug's
+actual impact, and add `Severity and priority are provisional: no consumer triage policy.` to the
+description.
+
 ## Step 1: Resolve IDs

 Fetch once per session, in parallel:
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
@@ -38,7 +38,7 @@
 3. If no existing bug is found, file one following [bug filing](bug-filing.md):
    - Subject: `Pre-existing test failure: <test name>`
    - Description: Include the test name, test suite, error message, commit hash where verified broken, and which branch/PR discovered it
-   - Severity per `docs/bug-triage.md`: Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
+   - Severity per `docs/bug-triage.md` (not installed here; see the consumer note in bug filing): Important if the failure is deterministic on `main` (main is red for that suite), Normal if it is flaky or environment-dependent
    - Priority: from the matrix (surface is `ci` unless the failure only reproduces in the local dev stack, then `devx`)
    - Tags: surface tag, `src:agent`, and `pre-existing-failure`
 4. Note the bug ref number
```

### Deliberately left out

- `docs/bug-triage.md`: You-Thon's product-specific severity and priority
  policy (project 3 REST calls, You-Thon product surfaces, links to roadmap,
  observability, and support docs that do not exist here). It is reached only
  on the optional bug-filing branch for out-of-scope observations and
  pre-existing test failures. The consumer note in both `bug-filing.md` copies
  makes the severity and priority provisional until this repository adopts its
  own policy.
- `/pr-converse`: named only as the redirect for issue comments and review
  bodies. The SAASDK copy is already installed and is not replaced.
- `/code-review`: a Claude Code built-in mentioned only as a source of issue
  comments; nothing to install.

### Known limits

- Bugs filed by this skill carry provisional severity and priority until a
  consumer `docs/bug-triage.md` exists.
- The surface tags in `bug-filing.md` (`product`, `devx`, `pipeline`, `ci`) are
  You-Thon's taxonomy, and this repository has no CI.
- The skill's Taiga and GitHub write paths (thread replies, resolution, issue
  and story creation) were not exercised by this install.
