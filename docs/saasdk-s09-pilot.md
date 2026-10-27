# S09 native skill pilot for dev-env epic #2466

> Superseded: the packages below were refreshed from SAASDK main and joined by three more skills in [saasdk-install.md](saasdk-install.md).

## Scope and revisions

- Consumer: `Alterna-Dev-Studio/dev-env-template`, isolated worktree at
  `/home/jon/work/utils/dev-env-template-s09`, branch
  `pilot/saasdk-s09-2466`, based on `feat/portable-shell-profile-2467` at
  `1bf5156e8b50e82a5a029913733907615e16494d`.
- Native source: SAASDK draft PR #18, commit
  `ec4a7a4a8d04dda40744b5b2a0ad0bbf2e98aa58`.
- Target: dev-env-template PR #2, head
  `1bf5156e8b50e82a5a029913733907615e16494d` at verification time.
- Pilot review: draft [dev-env-template PR #3](https://github.com/Alterna-Dev-Studio/dev-env-template/pull/3),
  targeting the existing portable-profile feature branch.
- Existing consumer guidance: `README.md`. There is no tracked `AGENTS.md`
  or `CLAUDE.md` in this consumer. The first pass did not alter the README,
  shell profile, tests, secrets, or consumer policy.

## Install diff

The first pass copied only the applicable `pr-converse` native package,
byte for byte:

| Path | Lines | SHA-256 |
| --- | ---: | --- |
| `.agents/skills/pr-converse/SKILL.md` | 153 | `be8886849fe610a943cbc219953328ad80bb8e4b47180301b9ce57666a194c57` |
| `.agents/skills/pr-converse/references/commit-attribution.md` | 11 | `d00569f163ff6608aca289a9fd8c7cff49a474a37bb0c85dd6d460980e93f780` |

No SAASDK agent TOML was selected: this read-only PR feedback check does not
delegate. No other skill or shared package was installed in the first pass.
The package's later steps are You-Thon-specific and are not authorized by
this pilot.

## Commands and result

```bash
git worktree add -b pilot/saasdk-s09-2466 /home/jon/work/utils/dev-env-template-s09 feat/portable-shell-profile-2467
mkdir -p .agents/skills
cp -a /home/jon/work/alterna/SAASDK/.agents/skills/pr-converse .agents/skills/
cmp .agents/skills/pr-converse/SKILL.md /home/jon/work/alterna/SAASDK/.agents/skills/pr-converse/SKILL.md
cmp .agents/skills/pr-converse/references/commit-attribution.md /home/jon/work/alterna/SAASDK/.agents/skills/pr-converse/references/commit-attribution.md
```

From the isolated worktree, Codex CLI 0.163.0 ran with a read-only sandbox:

```bash
codex exec --sandbox read-only --ephemeral --color never \
  -C /home/jon/work/utils/dev-env-template-s09 \
  -o /tmp/dev-env-s09-pr-converse-result.txt \
  'Invoke $pr-converse 2 for this repository, bounded to its read-only gathering and assessment steps (Steps 1 through 3). Read the installed skill and this consumer README first. Verify the repository identity and exact PR head. Read PR details, review comments, inline comments, general comments, and the diff. Classify any feedback and report findings or lack of feedback. The consumer is Bash/Python dev-env-template, not You-Thon; do not apply You-Thon-specific scripts, testing strategy, statuses, or assumptions. Do not switch branches, edit files, run tests, post comments, or execute Steps 4-6. State which skill file you used and any dependency or policy mismatch. This is an S09 read-only pilot, not deployment validation.'
```

The skill read its installed `SKILL.md` and the README, verified the GitHub
repository and exact PR head, then used `gh pr view 2`, `gh pr diff 2`, and
read-only GitHub API calls for PR reviews, inline comments, and issue comments.
All three comment lists were empty. There was no feedback to classify. It
reported the result without changing files or posting to GitHub or Taiga.

The first `gh pr view` call returned `error connecting to api.github.com`.
The subsequent read-only retry succeeded, as did the other GitHub reads.
The local branch name differs from the PR head branch, but its HEAD matched
the exact PR head SHA. The skill's normal checkout/pull instruction was
skipped to preserve this isolated, read-only verification.

The first publish command, `git push -u origin pilot/saasdk-s09-2466`, failed
with `Permission denied (publickey)` because this checkout's remote uses SSH.
The same commit was pushed with the existing GitHub CLI credential helper,
without changing the remote or printing a token:

```bash
git -c credential.helper='!gh auth git-credential' push \
  https://github.com/Alterna-Dev-Studio/dev-env-template.git \
  pilot/saasdk-s09-2466:pilot/saasdk-s09-2466
```

This demonstrates native skill discovery and a bounded authenticated PR read
in this consumer. It does not validate the skill's edit, push, comment, or
Taiga paths, or establish full deployment readiness for epic #2466.

## Deeper `review-tests` handoff from merged SAASDK

Source: merged SAASDK epic #294 PR #18 at
`7a110cc7ca84b048926272ffc490a93152ae377d`. The installed
`review-tests` package is copied byte for byte from that Git revision:

| Path | SHA-256 |
| --- | --- |
| `.agents/skills/review-tests/SKILL.md` | `6fdacac52a7d4e78abd517c53e6fb3fe5781f416f9e3439589e456af9d89ad5f` |
| `.agents/skills/review-tests/references/commit-attribution.md` | `d00569f163ff6608aca289a9fd8c7cff49a474a37bb0c85dd6d460980e93f780` |

The skill requires `docs/testing-strategy.md` and
`docs/testing-conventions.md`; this consumer previously had neither.
Those new documents map its test review to the README's Python unittest
command and the current temporary-home test fixtures. They explicitly exclude
the source skill's F#, .NET, browser, and You-Thon tracker procedures. This
mapping is proposed in this draft PR for review; it is not evidence that
the entire You-Thon-selected skill can run here.

Install commands from the isolated worktree:

```bash
mkdir -p .agents/skills/review-tests/references
git -C /home/jon/work/alterna/SAASDK show 7a110cc7:.agents/skills/review-tests/SKILL.md > .agents/skills/review-tests/SKILL.md
git -C /home/jon/work/alterna/SAASDK show 7a110cc7:.agents/skills/review-tests/references/commit-attribution.md > .agents/skills/review-tests/references/commit-attribution.md
```

Exact bounded invocation (Codex CLI 0.163.0):

```bash
codex exec --sandbox read-only --ephemeral --color never \
  -C /home/jon/work/utils/dev-env-template-s09 \
  -o /tmp/dev-env-s09-review-tests-result.txt \
  'Invoke $review-tests 2 as a bounded read-only S09 review of dev-env-template PR #2. Read the installed skill, README.md, docs/testing-strategy.md, and docs/testing-conventions.md. These docs are the explicit Bash/Python consumer mapping; verify each mapping claim from the repository. Use the actual PR head and main comparison, inspect changed tests/*.py and corresponding profile/shell/setup code. Perform Steps 1-3 and report specific test-quality findings with file and line evidence. Stop before Step 4 edits, Step 5 tests, and Step 6 GitHub/Taiga comments or commits. Do not apply the skill’s You-Thon F#, dotnet, suite, status, or helper assumptions. State any mapping gap. No files or external state may be changed.'
```

The read-only skill review found three issues: shell helper calls could hide
source errors on stderr; the existing SOPS profile test fixture copied
`profile.sh` but omitted its new `shell/` dependency; and the container
test did not prove its shell-only claim. It also found that the first mapping
omitted ownership of sourced-profile integration and called the new shell
test file existing. The mapping now assigns that integration to
`tests/test_scripts.py` and records the file's provenance accurately.

The skill's first `gh pr view` failed with `error connecting to
api.github.com`; a subsequent `git ls-remote` failed DNS inside its
read-only sandbox. It compared the local feature ref and the PR head SHA
recorded by the first pilot instead. Outside that sandbox, a fresh
`gh pr view 2 --json headRefOid,state` verified the still-open PR head
as `1bf5156e8b50e82a5a029913733907615e16494d`.

The agent stopped before editing or posting. I then made these test-only
changes on the isolated branch:

- `tests/test_scripts.py` copies the `shell/` dependency into its throwaway
  repository and checks that the sourced profile emits no unexpected stderr.
- `tests/test_shell.py` checks stderr for each Bash source operation. The
  devcontainer test installs from an isolated shell-fragment directory with
  no profile or envtool, and checks that neither is placed in startup files.

Verification commands and outcomes:

```bash
python3 -m unittest discover -s tests -p test_scripts.py -k test_profile_exports_values_in_bash -v
# Before fixture repair: 1 failure; source reported missing shell/paths.sh.
python3 -m unittest discover -s tests -v
# After repair: 11 tests passed.
git diff --check
# Passed.
```

No shell implementation, secret, host startup file, or Taiga item changed.
The full `review-tests` workflow still requires a reconciled dev-env variant
before using its edit, commit, PR comment, or tracker stages. This pass
validates the local read-only review and a concrete test repair only.
