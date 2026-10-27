---
name: codex-review-pr
description: Run a Codex (GPT-5.6 Luna) code review on a GitHub PR and post the findings as review threads
---

# Codex runtime and scope

Invoke as `$codex-review-pr <arguments>`. Treat the invocation text as the arguments shown below. This package preserves the You-Thon selected Claude-source workflow. Its repository paths, test commands, Taiga statuses, automation, and CI artifacts apply only to that consumer at the verified revision. Read the consumer's applicable `AGENTS.md` and/or `CLAUDE.md` and referenced policy documents first. For another consumer, require an explicit local mapping before execution.

Discover the available Taiga tools by operation. Before a tracker write, verify the host and project against the consumer configuration, resolve `<verified-project-id>` live (or verify `TAIGA_PROJECT_ID` where used), and resolve status/member IDs by name. A source `mcp__taiga-py__*` operation denotes the equivalent connected Codex tool, not a guaranteed tool identifier. Stop and report a missing connection, authentication, project guard, script, or required permission. Use Codex search/read/patch tools for file inspection and edits, shell execution for Git, GitHub CLI and consumer scripts, and the available web tool when needed. Source `allowed-tools` grants do not carry over.

The consumer-owned `scripts/codex-review-pr.sh` and its exit/status contract must exist before invoking it. This is a compatibility entrypoint; `$peer-review-pr` is the native review workflow.

# Codex Review PR — #<arguments>

Trigger or re-run a Codex review on a PR without remembering the script invocation.

## Step 1: Parse arguments

Parse `<pr-number>` and the optional `--dry-run` flag from `<arguments>`. If no PR number is given, ask for one.

## Step 2: Run the review

Run `scripts/codex-review-pr.sh <pr> [--dry-run]` as a foreground Bash call using a yielded execution session and polling it to completion (xhigh reasoning is thorough, so a pass takes 10-20 minutes on large PRs; the script hands back `REVIEW_PENDING` before the 10-minute Bash cap, so the call itself always returns in time).

## Step 3: Report the result

Report the last stdout line verbatim, and translate it for the reader:

- `REVIEW_POSTED:<pass>/<max>:<inline>:<body_only>` — pass N of M posted, X inline threads and Y body-only findings.
- `REVIEW_SKIPPED:same-head` — this head SHA was already reviewed; push a change first.
- `REVIEW_SKIPPED:cap` — the per-PR pass cap is exhausted; note that `CODEX_REVIEW_MAX_PASSES` can override it for a deliberate extra pass.
- `REVIEW_DRYRUN:<pass>/<max>:<inline>:<body_only>` — `--dry-run` only: the review that pass N of M *would* have posted, with X inline threads and Y body-only findings. Nothing was posted. The lines before it are the GitHub review payload JSON; summarize it rather than pasting it, and offer to re-run without `--dry-run` to post.
- `REVIEW_PENDING:<pass>/<max>` — the review is still running in a detached worker; it posts on its own even without a re-invoke. Re-run the exact same command to join the worker and wait again; keep re-invoking until the result changes to `REVIEW_POSTED`, `REVIEW_SKIPPED:same-head`, or a non-zero exit.

On a non-zero exit, report the stderr message and state that nothing was posted. Do not retry automatically.

Note that the posted threads block the merge gate and are worked by `$pr-comments-resolve`.

For script internals or env var defaults beyond the override mentioned above, point at `scripts/codex-review-pr.sh --help`/`usage()` rather than restating them here.
