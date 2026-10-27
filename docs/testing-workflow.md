# Testing Workflow

> Suite boundaries: [testing-strategy.md](testing-strategy.md). Naming and layout:
> [testing-conventions.md](testing-conventions.md).

This repository has one test suite and no CI test gate, so the local run is the gate.

## What to run

| What you changed | Command |
| --- | --- |
| Anything under `scripts/`, `shell/`, `tests/`, or `profile.sh` | `python3 -m unittest discover -s tests -v` |
| A Bash file (in addition to the suite) | `bash -n <file>` and `shellcheck <file>` |
| Documentation only | Nothing required; `git diff --check` for whitespace |

Run the full suite after each task and before opening a PR. It finishes in seconds. The
SOPS-backed tests in `tests/test_scripts.py` skip themselves unless `sops`, `age-keygen`, and
`direnv` are installed; a skipped SOPS suite on a change to `scripts/envtool` or `scripts/setup`
is not a pass, so install those tools or say the suite was skipped.

Results are the unittest output itself. There are no `test-results/*.xml` files, no `dotnet`
targets, and no separate unit, integration, or end-to-end jobs.
