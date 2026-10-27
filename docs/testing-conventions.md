# Dev-env template test conventions

The current suite uses Python `unittest` in `tests/test_shell.py` and
`tests/test_scripts.py`. Tests invoke Bash and repository scripts with
`subprocess.run`, capture output, and use temporary home and repository
directories. `tests/test_scripts.py` skips the SOPS-backed suite unless
`sops`, `age-keygen`, and `direnv` are installed.

Follow those existing patterns. Assert return codes and the
specific stdout or stderr contract being tested. A successful profile load
must not silently pass with a shell source error. Do not read the host's
personal SOPS identity, write to the real home directory, or print secrets.
The command is `python3 -m unittest discover -s tests -v`, as documented in
the [README](../README.md).
