# Dev-env template test strategy

This is the consumer test mapping that `analyze-story` and `review-tests`
rely on. The [README](../README.md) supplies the test command
and the requirement that tests use a temporary home without touching personal
keys or the vault. The test files supply the suite boundaries below.
This mapping does not import You-Thon's application test policy.

| Change | Authoritative test location | Evidence |
| --- | --- | --- |
| Bash PATH, aliases, and startup-file behavior | `tests/test_shell.py` | `ShellTests` execute Bash with a temporary `HOME`. |
| Setup and encrypted envtool behavior | `tests/test_scripts.py` | `ScriptTests` copy scripts into a temporary repository and use a temporary SOPS identity. |
| Sourced `profile.sh` integration | `tests/test_scripts.py` | `ScriptTests` copy the profile, envtool, and shell fragments together before sourcing them. |

Review the changed `tests/*.py` against the changed Bash/Python files. Check
that each test exercises the relevant command or sourced file, isolates its
home and credentials, checks the behavior it claims, and does not duplicate
another test without covering a distinct contract. A sourced profile is
successful only if the shell command succeeds and its stderr does not contain
an unexpected missing-file or load error. Preserve negative tests that
intentionally expect stderr. Use an observable outcome instead of reproducing
the implementation in test helpers.

Run `python3 -m unittest discover -s tests -v` for this suite. `bash -n` and
`shellcheck` are useful static checks for changed Bash files, but neither
replaces the Python integration tests. There are no F#, `.fsproj`, .NET,
browser, or JUnit XML suites in this consumer.
