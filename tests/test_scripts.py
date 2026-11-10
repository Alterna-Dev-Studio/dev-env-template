"""Exercise setup and envtool against a throwaway HOME and repository copy.

Run with: python3 -m unittest discover -s tests
"""
import http.server
import json
import os
from pathlib import Path
import pty
import shutil
import subprocess
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ("sops", "age-keygen", "direnv")
# Exactly what setup, envtool, and setup-taiga-mcp run; PATH-sensitive tests use only these.
SETUP_TOOLS = ("python3", "bash", "sh", "dirname", "git", *TOOLS)


@unittest.skipUnless(all(shutil.which(tool) for tool in TOOLS), "requires " + ", ".join(TOOLS))
class ScriptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.repo = self.tmp / "repo"
        (self.repo / "scripts").mkdir(parents=True)
        for name in ("envtool", "setup", "setup-taiga-mcp", "taiga-mcp", *('pangolin-token', 'pangolin-configure', 'pangolin-login',
                       'taiga-login', 'taiga-configure')):
            shutil.copy2(ROOT / "scripts" / name, self.repo / "scripts" / name)
        shutil.copy2(ROOT / "profile.sh", self.repo / "profile.sh")
        shutil.copy2(ROOT / ".envrc", self.repo / ".envrc")
        shutil.copytree(ROOT / "shell", self.repo / "shell")
        shutil.copytree(ROOT / "bin", self.repo / "bin", symlinks=True)
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith(("SOPS_", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "TAIGA_"))}
        self.env["HOME"] = str(self.home)
        self.key = self.home / ".config/sops/age/keys.txt"
        self.bashrc = self.home / ".bashrc"

    def minimal_path(self, *dirs, without=()):
        """PATH of `dirs` then a bin dir holding only SETUP_TOOLS (minus `without`) from the host."""
        bin_dir = self.tmp / "minimal-bin"
        if not bin_dir.exists():
            bin_dir.mkdir()
            for name in SETUP_TOOLS:
                found = shutil.which(name)
                if found is None:
                    self.skipTest(f"requires {name} on the host")
                (bin_dir / name).symlink_to(found)
        for name in without:
            (bin_dir / name).unlink(missing_ok=True)
        return os.pathsep.join([*map(str, dirs), str(bin_dir)])

    def run_script(self, *args, check=True, skip_taiga_mcp=True, stdin=None):
        if args[0] == "setup" and skip_taiga_mcp and "--skip-taiga-mcp" not in args:
            args = (*args, "--skip-taiga-mcp")
        result = subprocess.run([str(self.repo / "scripts" / args[0]), *args[1:]], env=self.env,
                                cwd=self.repo, stdin=None if stdin is not None else subprocess.DEVNULL,
                                input=stdin, text=True, capture_output=True)
        if check and result.returncode:
            self.fail(f"{args} failed: {result.stderr}")
        return result

    def store(self, scope, values):
        code = ("import runpy, sys, json; tool = runpy.run_path(sys.argv[1]); "
                "data = tool['decrypt'](sys.argv[2]); data.update(json.loads(sys.argv[3])); "
                "tool['encrypt'](sys.argv[2], data)")
        subprocess.run(["python3", "-I", "-c", code, str(self.repo / "scripts/envtool"), scope,
                        __import__("json").dumps(values)], env=self.env, check=True,
                       capture_output=True)

    def vault_recipients(self, scope="profile"):
        text = (self.repo / "secrets" / f"{scope}.enc.json").read_text()
        return set(__import__("re").findall(r"age1[0-9a-z]+", text))

    def public_key(self, path):
        return subprocess.run(["age-keygen", "-y", str(path)], text=True, check=True,
                              capture_output=True).stdout.split()

    def test_fresh_setup_is_idempotent_and_adds_direnv_hook_last(self):
        self.run_script("setup")
        first = self.bashrc.read_text()
        self.assertEqual(self.key.stat().st_mode & 0o777, 0o600)
        lines = first.splitlines()
        source = next(i for i, line in enumerate(lines) if "profile.sh" in line)
        hook = next(i for i, line in enumerate(lines) if "direnv hook bash" in line)
        self.assertLess(source, hook)
        self.run_script("setup")
        self.assertEqual(self.bashrc.read_text(), first)

    def test_setup_allows_the_clone_envrc(self):
        allow = self.home / ".local/share/direnv/allow"
        for _ in range(2):
            self.run_script("setup")
            records = list(allow.iterdir())
            self.assertEqual(len(records), 1)
            self.assertIn(str(self.repo / ".envrc"), records[0].read_text())

    def test_setup_ends_with_key_backup_reminder(self):
        result = self.run_script("setup")
        last = result.stdout.splitlines()[-2:]
        self.assertIn(str(self.key), last[0])
        self.assertIn("Back it up", last[1])
        secret = next(line for line in self.key.read_text().splitlines()
                      if line.startswith("AGE-SECRET-KEY-"))
        self.assertNotIn(secret, result.stdout + result.stderr)

    def test_profile_line_goes_before_existing_direnv_hook(self):
        self.bashrc.write_text('alias ll="ls -l"\neval "$(direnv hook bash)"\nexport EDITOR=vim')
        self.run_script("setup")
        lines = self.bashrc.read_text().splitlines()
        self.assertEqual(sum("direnv hook" in line for line in lines), 1)
        self.assertLess(next(i for i, line in enumerate(lines) if "profile.sh" in line),
                        next(i for i, line in enumerate(lines) if "direnv hook" in line))
        self.assertIn("export EDITOR=vim", lines)

    def test_missing_trailing_newline_is_not_joined(self):
        self.bashrc.write_text("export EDITOR=vim")
        self.run_script("setup")
        lines = self.bashrc.read_text().splitlines()
        self.assertEqual(lines[0], "export EDITOR=vim")
        self.assertTrue(any("profile.sh" in line for line in lines[1:]))

    def test_encrypt_uses_sops_config_not_first_local_identity(self):
        self.run_script("setup")
        vault_key = self.public_key(self.key)
        other = self.tmp / "other.txt"
        subprocess.run(["age-keygen", "-o", str(other)], check=True, capture_output=True)
        self.key.write_text(other.read_text() + self.key.read_text())
        self.store("profile", {"FOO": "bar"})
        self.assertEqual(self.vault_recipients(), set(vault_key))
        self.assertIn("FOO", self.run_script("envtool", "list", "profile").stdout.split())
        self.run_script("setup")

    def test_setup_rejects_identity_that_does_not_match_vault(self):
        self.run_script("setup")
        config = (self.repo / ".sops.yaml").read_text()
        self.key.unlink()
        subprocess.run(["age-keygen", "-o", str(self.key)], check=True, capture_output=True)
        result = self.run_script("setup", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("matches a .sops.yaml recipient", result.stderr)
        self.assertEqual((self.repo / ".sops.yaml").read_text(), config)

    def test_missing_identity_gives_short_error(self):
        self.run_script("setup")
        self.store("profile", {"FOO": "bar"})
        self.key.unlink()
        result = self.run_script("envtool", "export", "profile", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stderr.strip().splitlines(),
                         [f"envtool: No age identity at {self.key}; restore it before using the vault"])

    def test_xdg_config_home_matches_sops_lookup(self):
        self.env["XDG_CONFIG_HOME"] = str(self.tmp / "xdg")
        self.run_script("setup")
        self.assertTrue((self.tmp / "xdg/sops/age/keys.txt").is_file())
        self.assertFalse(self.key.exists())
        self.store("profile", {"FOO": "bar"})
        self.assertEqual(self.run_script("envtool", "export", "profile").stdout,
                         "export FOO=bar\n")

    def test_taiga_mcp_launches_checkout_with_decrypted_credentials(self):
        self.run_script("setup")
        self.store("profile", {"TAIGA_API_URL": "https://taiga.example", "TAIGA_USERNAME": "u",
                               "TAIGA_PASSWORD": "p"})
        checkout = self.tmp / "pytaiga-mcp"
        (checkout / ".venv/bin").mkdir(parents=True)
        (checkout / ".venv/bin/python").symlink_to(shutil.which("python3"))
        (checkout / "src").mkdir()
        (checkout / "src/server_full.py").write_text(
            "import os, sys; print(os.getcwd()); "
            "print(*(os.environ.get(n) for n in ('TAIGA_API_URL', 'TAIGA_USERNAME', 'TAIGA_PASSWORD', "
            "'TAIGA_TRANSPORT', 'PANGOLIN_RESOURCE_TOKEN')), sep='|')\n")
        self.env["PYTAIGA_MCP_HOME"] = str(checkout)
        self.env["PANGOLIN_RESOURCE_TOKEN"] = "stale-host-value"
        result = self.run_script("taiga-mcp", "full")
        self.assertEqual(result.stdout.splitlines(),
                         [str(checkout), "https://taiga.example|u|p|stdio|"])
        self.assertEqual(result.stderr, "")
        self.env.update({"TAIGA_API_URL": "env.example", "TAIGA_USERNAME": "eu", "TAIGA_PASSWORD": "ep"})
        result = self.run_script("taiga-mcp", "full")
        # Environment mode passes Pangolin settings through from the same environment.
        self.assertEqual(result.stdout.splitlines()[1], "env.example|eu|ep|stdio|stale-host-value")
        result = self.run_script("taiga-mcp", "full", "profile")
        self.assertEqual(result.stdout.splitlines()[1], "https://taiga.example|u|p|stdio|")
        # A taiga-login token replaces the username and password.
        self.store("project/token", {"TAIGA_API_URL": "https://taiga.example",
                                     "TAIGA_AUTH_TOKEN": "app-t0ken"})
        result = self.run_script("taiga-mcp", "full", "project/token")
        self.assertEqual(result.stdout.splitlines()[1], "https://taiga.example|||stdio|")
        for name in ("TAIGA_API_URL", "TAIGA_USERNAME", "TAIGA_PASSWORD"):
            del self.env[name]
        result = self.run_script("taiga-mcp", "full", "project/empty", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing Taiga settings", result.stderr)
        self.assertNotIn("p", result.stdout)
        self.env["PYTAIGA_MCP_HOME"] = str(self.tmp / "absent")
        result = self.run_script("taiga-mcp", "full", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("run scripts/setup-taiga-mcp", result.stderr)
        self.assertNotIn("p", result.stdout)
        result = self.run_script("taiga-mcp", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("usage:", result.stderr)

    def run_dv(self, *args, check=True):
        """Run the dispatcher through its `dv` symlink from outside the checkout."""
        result = subprocess.run([str(self.repo / "bin/dv"), *args], env=self.env, cwd=self.home,
                                stdin=subprocess.DEVNULL, text=True, capture_output=True)
        if check and result.returncode:
            self.fail(f"dv {args} failed: {result.stderr}")
        return result

    def test_dv_dispatches_to_the_scripts_from_any_directory(self):
        self.run_script("setup")
        self.store("profile", {"FOO": "bar"})
        self.assertEqual(self.run_dv("export", "profile").stdout, "export FOO=bar\n")
        self.assertEqual(self.run_dv("list", "profile").stdout.split(), ["FOO"])
        self.assertIn("--skip-taiga-mcp", self.run_dv("setup", "--help").stdout)
        result = self.run_dv("taiga-mcp", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("usage: taiga-mcp workflow|full", result.stderr)
        result = self.run_dv("bogus", check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("dv: unknown command 'bogus'", result.stderr)
        self.assertIn("usage: dv COMMAND", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_dv_taiga_mcp_install_runs_setup_taiga_mcp(self):
        checkout, _, uv_log, codex_log = self.fake_taiga_mcp()
        result = self.run_dv("taiga-mcp", "install")
        self.assertEqual(uv_log.read_text(), f"sync --frozen --directory {checkout}\n")
        self.assertEqual(codex_log.read_text(), f"mcp add taiga-py -- {self.repo / 'scripts/taiga-mcp'} full\n")
        self.assertIn("Registered taiga-py for Codex", result.stdout)

    def test_migrate_bashrc_moves_only_named_exports(self):
        self.bashrc.write_text("export FOO=1\nexport BAR=2\nexport BAZ=3\n")
        self.env.update({"FOO": "1", "BAR": "2", "BAZ": "3"})
        self.run_script("setup")
        self.run_script("setup", "--migrate-bashrc", "FOO", "BAR")
        self.assertEqual(self.run_script("envtool", "list", "profile").stdout.split(), ["BAR", "FOO"])
        bashrc = self.bashrc.read_text()
        self.assertNotIn("export FOO=", bashrc)
        self.assertNotIn("export BAR=", bashrc)
        self.assertIn("export BAZ=3", bashrc)
        result = self.run_script("setup", "--migrate-bashrc", "not-a-name", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid variable name", result.stderr)

    def test_setup_without_tty_names_missing_values_without_prompting(self):
        result = self.run_script("setup")
        self.assertIn("Missing required profile values: TAIGA_API_URL, TAIGA_USERNAME, TAIGA_PASSWORD",
                      result.stdout)
        self.assertEqual(self.run_script("envtool", "list", "profile").stdout.strip(), "")
        self.store("profile", {"TAIGA_API_URL": "https://taiga.example", "TAIGA_USERNAME": "u",
                               "TAIGA_PASSWORD": "secret-value"})
        result = self.run_script("setup")
        self.assertNotIn("Missing", result.stdout)
        self.assertNotIn("Still missing", result.stdout)
        self.assertNotIn("secret-value", result.stdout + result.stderr)

    def pty_setup(self, *answers):
        pid, fd = pty.fork()
        if pid == 0:
            os.chdir(self.repo)
            # --skip-taiga-mcp: with uv on the host PATH, setup would otherwise clone pytaiga-mcp.
            os.execve(str(self.repo / "scripts/setup"),
                      [str(self.repo / "scripts/setup"), "--skip-taiga-mcp"], self.env)
        output = b""
        pending = list(answers)
        while True:
            try:
                chunk = os.read(fd, 4096)
            except OSError:
                break
            if not chunk:
                break
            output += chunk
            if pending and output.endswith(b": "):
                os.write(fd, pending.pop(0).encode() + b"\n")
        _, status = os.waitpid(pid, 0)
        os.close(fd)
        return os.waitstatus_to_exitcode(status), output.decode()

    def test_setup_prompts_on_a_tty_and_round_trips_values(self):
        code, output = self.pty_setup("https://taiga.example", "u", "p")
        self.assertEqual(code, 0, output)
        self.assertIn("Saved TAIGA_API_URL, TAIGA_PASSWORD, TAIGA_USERNAME in profile.", output)
        exported = self.run_script("envtool", "export", "profile").stdout
        for value in ("https://taiga.example", "u", "p"):
            self.assertIn(value, exported)
        code, output = self.pty_setup()
        self.assertEqual(code, 0, output)
        self.assertNotIn("TAIGA_", output)

    def test_profile_exports_values_in_bash(self):
        self.run_script("setup")
        self.store("profile", {"FOO": "it's here", "DEV_ENV_HOME": "/stale/clone",
                               "_dev_env_root": "/stale/root"})
        result = subprocess.run(["bash", "-c", f'source {self.repo}/profile.sh; printf %s "$FOO"'],
                                env=self.env, text=True, capture_output=True, check=True)
        self.assertEqual(result.stdout, "it's here")
        self.assertEqual(result.stderr, "")
        result = subprocess.run(["bash", "-c", f'source {self.repo}/profile.sh; printf %s "$DEV_ENV_HOME"'],
                                env=self.env, text=True, capture_output=True, check=True)
        self.assertEqual(result.stdout, str(self.repo))
        result = subprocess.run(["bash", "-c", f'source {self.repo}/profile.sh; printf %s "$_DEV_ENV_PROFILE_LOADED"'],
                                env=self.env, text=True, capture_output=True, check=True)
        self.assertEqual(result.stdout, str(self.repo))

    def fake_taiga_mcp(self, uv_dir=None):
        checkout = self.tmp / "pytaiga-mcp"
        (checkout / "src").mkdir(parents=True)
        for name in ("pyproject.toml", "uv.lock", "src/server_workflow.py", "src/server_full.py"):
            (checkout / name).touch()
        shims = self.home / "bin"
        shims.mkdir()
        for name, log, directory in (("uv", "UV_LOG", uv_dir or shims), ("codex", "CODEX_LOG", shims)):
            directory.mkdir(parents=True, exist_ok=True)
            shim = directory / name
            shim.write_text(f"#!/bin/sh\nprintf '%s\\n' \"$*\" >> \"${log}\"\n")
            shim.chmod(0o755)
        uv_log, codex_log = self.tmp / "uv.log", self.tmp / "codex.log"
        self.env.update(PYTAIGA_MCP_HOME=str(checkout), UV_LOG=str(uv_log), CODEX_LOG=str(codex_log),
                        PATH=self.minimal_path(shims))
        return checkout, shims, uv_log, codex_log

    def test_setup_taiga_mcp_registers_launcher_for_codex(self):
        checkout, shims, uv_log, codex_log = self.fake_taiga_mcp()
        launcher = self.repo / "scripts/taiga-mcp"
        entry = f"mcp add taiga-py -- {launcher} full"

        result = self.run_script("setup-taiga-mcp")
        self.assertEqual(uv_log.read_text(), f"sync --frozen --directory {checkout}\n")
        self.assertEqual(codex_log.read_text(), entry + "\n")
        self.assertIn("Registered taiga-py for Codex", result.stdout)

        self.run_script("setup-taiga-mcp")
        self.assertEqual(codex_log.read_text(), (entry + "\n") * 2)

        (shims / "codex").unlink()
        self.assertIsNone(shutil.which("codex", path=self.env["PATH"]))
        result = self.run_script("setup-taiga-mcp")
        self.assertIn("codex is not on PATH", result.stdout)

    def test_setup_runs_taiga_mcp_install_when_uv_present(self):
        checkout, shims, uv_log, codex_log = self.fake_taiga_mcp()
        entry = f"mcp add taiga-py -- {self.repo / 'scripts/taiga-mcp'} full"

        result = self.run_script("setup", skip_taiga_mcp=False)
        self.assertIn(entry, codex_log.read_text())
        self.assertIn("Registered taiga-py for Codex", result.stdout)
        self.assertIn("Back it up now", result.stdout.splitlines()[-1])

        before = (uv_log.read_text(), codex_log.read_text())
        self.run_script("setup")
        self.assertEqual((uv_log.read_text(), codex_log.read_text()), before)

        (shims / "uv").unlink()
        self.assertIsNone(shutil.which("uv", path=self.env["PATH"]))
        result = self.run_script("setup", skip_taiga_mcp=False)
        self.assertIn("uv is not installed", result.stdout)

    def test_setup_installs_taiga_mcp_with_uv_found_only_in_go_bin(self):
        checkout, _, uv_log, codex_log = self.fake_taiga_mcp(uv_dir=self.home / "go/bin")
        self.assertIsNone(shutil.which("uv", path=self.env["PATH"]))
        result = self.run_script("setup", check=False, skip_taiga_mcp=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(uv_log.read_text(), f"sync --frozen --directory {checkout}\n")
        self.assertIn("Registered taiga-py for Codex", result.stdout)
        for missing in ("uv is not installed", "uv is required"):
            self.assertNotIn(missing, result.stdout + result.stderr)

    def test_setup_uses_direnv_found_only_in_go_bin(self):
        go_bin = self.home / "go/bin"
        go_bin.mkdir(parents=True)
        (go_bin / "direnv").symlink_to(shutil.which("direnv"))
        self.env["PATH"] = self.minimal_path(without=("direnv",))
        self.assertIsNone(shutil.which("direnv", path=self.env["PATH"]))
        self.run_script("setup")
        lines = self.bashrc.read_text().splitlines()
        self.assertEqual(sum("direnv hook bash" in line for line in lines), 1)
        self.assertLess(next(i for i, line in enumerate(lines) if "profile.sh" in line),
                        next(i for i, line in enumerate(lines) if "direnv hook bash" in line))
        records = list((self.home / ".local/share/direnv/allow").iterdir())
        self.assertEqual(len(records), 1)
        self.assertIn(str(self.repo / ".envrc"), records[0].read_text())


    def exported(self, scope="profile"):
        return dict(line.removeprefix("export ").split("=", 1)
                    for line in self.run_script("envtool", "export", scope).stdout.splitlines())

    def test_envtool_hides_only_secret_values(self):
        tool = __import__("runpy").run_path(str(ROOT / "scripts/envtool"))
        for name in ("TAIGA_PASSWORD", "GH_TOKEN_FOR_CHECKS", "OPENROUTER_API_KEY",
                     "PANGOLIN_SESSION_TOKEN", "STRIPE_SECRET"):
            self.assertTrue(tool["is_secret"](name), name)
        for name in ("TAIGA_API_URL", "TAIGA_USERNAME", "TAIGA_HOST", "DEV_HOME"):
            self.assertFalse(tool["is_secret"](name), name)

    def fake_pytaiga(self):
        """A stand-in pytaiga-mcp checkout whose login module prints the environment it got."""
        checkout = self.tmp / "pytaiga-mcp"
        (checkout / ".venv/bin").mkdir(parents=True)
        (checkout / ".venv/bin/python").symlink_to(shutil.which("python3"))
        (checkout / "src").mkdir()
        (checkout / "src/__init__.py").write_text("")
        (checkout / "src/taiga_login.py").write_text(
            "import os, sys; print(*(os.environ.get(n, '<unset>') for n in ('TAIGA_API_URL', "
            "'TAIGA_OIDC_ISSUER', 'TAIGA_OIDC_CLIENT_ID', 'TAIGA_APPLICATION_ID', "
            "'PANGOLIN_SESSION_TOKEN', 'TAIGA_PASSWORD')), *sys.argv[1:], sep='|')\n")
        self.env["PYTAIGA_MCP_HOME"] = str(checkout)
        return checkout

    def test_taiga_login_passes_scope_values_to_pytaiga(self):
        self.run_script("setup")
        self.fake_pytaiga()
        self.store("profile", {"TAIGA_API_URL": "https://taiga.example", "TAIGA_PASSWORD": "p",
                               "TAIGA_OIDC_ISSUER": "https://login.example",
                               "TAIGA_OIDC_CLIENT_ID": "cli", "TAIGA_APPLICATION_ID": "app",
                               "PANGOLIN_SESSION_TOKEN": "sess"})
        result = self.run_script("taiga-login", "--no-browser")
        self.assertEqual(result.stdout.strip(),
                         "https://taiga.example|https://login.example|cli|app|sess||--no-browser")
        self.store("project/bare", {"TAIGA_API_URL": "https://taiga.example"})
        result = self.run_script("taiga-login", "project/bare", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("lacks TAIGA_OIDC_ISSUER, TAIGA_OIDC_CLIENT_ID, TAIGA_APPLICATION_ID",
                      result.stderr)
        result = self.run_script("taiga-login", "profile", "--bogus", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("usage:", result.stderr)

    def test_taiga_configure_stores_application_token(self):
        self.run_script("setup")
        self.store("profile", {"TAIGA_API_URL": "https://taiga.example", "TAIGA_PASSWORD": "p"})
        result = self.run_script("taiga-configure", "profile", "--stdin", stdin="app-t0ken\n")
        self.assertIn("Saved TAIGA_AUTH_TOKEN in profile.", result.stdout)
        self.assertNotIn("app-t0ken", result.stdout + result.stderr)
        self.assertEqual(self.exported(), {"TAIGA_API_URL": "https://taiga.example",
                                           "TAIGA_PASSWORD": "p", "TAIGA_AUTH_TOKEN": "app-t0ken",
                                           "TAIGA_TOKEN_TYPE": "Application"})
        bad = self.run_script("taiga-configure", "profile", "--stdin", stdin="two words\n", check=False)
        self.assertEqual(bad.returncode, 1)
        self.assertIn("single word", bad.stderr)
        self.run_script("taiga-configure", "profile", "--clear")
        self.assertEqual(self.exported(), {"TAIGA_API_URL": "https://taiga.example",
                                           "TAIGA_PASSWORD": "p"})

    def test_pangolin_token_normalizes_share_links(self):
        cases = {
            "https://pangolin.example/s/abc123\n": "https://pangolin.example/s/abc123",
            "https://taiga.example/?p_token=id1.secret\n": "id1.secret",
            "id1.secret\n": "id1.secret",
        }
        for pasted, expected in cases.items():
            result = self.run_script("pangolin-token", "--stdin", stdin=pasted)
            self.assertEqual(result.stdout, expected + "\n")
            self.assertIn("Share Links", result.stderr)
            self.assertNotIn("secret", result.stderr)
            self.assertNotIn("abc123", result.stderr)

    def test_pangolin_token_rejects_other_keys(self):
        for pasted in ("pangolin-key-abc.def", "http://pangolin.example/s/abc", "a.b.c",
                       "https://pangolin.example/s/abc?x=1", "https://taiga.example/?q=1", ""):
            result = self.run_script("pangolin-token", "--stdin", stdin=pasted, check=False)
            self.assertEqual(result.returncode, 1, pasted)
            self.assertEqual(result.stdout, "", pasted)
            self.assertIn("pangolin-token:", result.stderr, pasted)

    def test_pangolin_configure_replaces_legacy_pair(self):
        self.run_script("setup")
        self.store("profile", {"PANGOLIN_ACCESS_TOKEN_ID": "x", "PANGOLIN_ACCESS_TOKEN": "y",
                               "TAIGA_PASSWORD": "p"})
        result = self.run_script("pangolin-configure", "profile", "--stdin",
                                 stdin="https://pangolin.example/s/abc123\n")
        self.assertNotIn("abc123", result.stdout + result.stderr)
        self.assertEqual(self.exported(), {"PANGOLIN_RESOURCE_TOKEN":
                                           "https://pangolin.example/s/abc123",
                                           "TAIGA_PASSWORD": "p"})
        self.run_script("pangolin-configure", "profile", "--clear")
        self.assertEqual(self.exported(), {"TAIGA_PASSWORD": "p"})

    def fake_pangolin(self, polls_before_verified, expired=False):
        """Serve Pangolin's device-web-auth start/poll endpoints on a loopback port."""
        state = {"polls": 0}

        class Handler(http.server.BaseHTTPRequestHandler):
            def reply(self, payload):
                body = json.dumps(payload).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                assert self.path == "/api/v1/auth/device-web-auth/start"
                assert self.headers["X-CSRF-Token"] == "x-csrf-protection"
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                assert body["applicationName"] == "pytaiga-mcp" and body["deviceName"]
                self.reply({"data": {"code": "AB12-CD34", "expiresInSeconds": 300}})

            def do_GET(self):
                assert self.path == "/api/v1/auth/device-web-auth/poll/AB12-CD34"
                state["polls"] += 1
                if expired:
                    self.reply({"data": {"verified": False}, "message": "Code expired"})
                elif state["polls"] > polls_before_verified:
                    self.reply({"data": {"verified": True, "token": "sess10n"}})
                else:
                    self.reply({"data": {"verified": False}, "message": "Code not yet verified"})

            def log_message(self, *args):
                pass

        server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return f"http://127.0.0.1:{server.server_port}", state

    def test_pangolin_login_polls_until_confirmed(self):
        dashboard, state = self.fake_pangolin(polls_before_verified=2)
        result = self.run_script("pangolin-login", "--dashboard-url", dashboard, "--no-browser",
                                 "--poll-interval", "0.01")
        self.assertEqual(result.stdout, "sess10n\n")
        self.assertEqual(state["polls"], 3)
        self.assertIn("AB12-CD34", result.stderr)
        self.assertIn(f"{dashboard}/auth/login/device?code=AB12-CD34", result.stderr)
        self.assertNotIn("sess10n", result.stderr)

    def test_pangolin_login_reports_expired_code(self):
        dashboard, _ = self.fake_pangolin(polls_before_verified=0, expired=True)
        result = self.run_script("pangolin-login", "--dashboard-url", dashboard, "--no-browser",
                                 check=False)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("expired", result.stderr)
        rejected = self.run_script("pangolin-login", "--dashboard-url", "http://pangolin.example",
                                   "--no-browser", check=False)
        self.assertEqual(rejected.returncode, 1)
        self.assertIn("https://", rejected.stderr)

    def test_pangolin_configure_session_replaces_share_link(self):
        self.run_script("setup")
        self.store("profile", {"PANGOLIN_RESOURCE_TOKEN": "id.secret", "TAIGA_PASSWORD": "p"})
        result = self.run_script("pangolin-configure", "profile", "--session", "--dashboard-url",
                                 "https://connect.example/", "--stdin", stdin="sess10n\n")
        self.assertNotIn("sess10n", result.stdout + result.stderr)
        self.assertEqual(self.exported(), {"PANGOLIN_SESSION_TOKEN": "sess10n",
                                           "PANGOLIN_DASHBOARD_URL": "https://connect.example",
                                           "TAIGA_PASSWORD": "p"})
        self.run_script("pangolin-configure", "profile", "--stdin", stdin="id.secret\n")
        self.assertEqual(self.exported(), {"PANGOLIN_RESOURCE_TOKEN": "id.secret",
                                           "TAIGA_PASSWORD": "p"})
        self.run_script("pangolin-configure", "profile", "--clear")
        self.assertEqual(self.exported(), {"TAIGA_PASSWORD": "p"})

    def test_pangolin_configure_session_rejects_bad_arguments(self):
        self.run_script("setup")
        self.store("profile", {"TAIGA_PASSWORD": "p"})
        before = (self.repo / "secrets/profile.enc.json").read_text()
        for args, stdin in ((("profile", "--session", "--stdin"), "sess10n\n"),
                            (("profile", "--dashboard-url", "https://c.example", "--stdin"), "x\n"),
                            (("profile", "--session", "--dashboard-url", "http://c.example",
                              "--stdin"), "sess10n\n"),
                            (("profile", "--session", "--dashboard-url", "https://c.example",
                              "--stdin"), "https://c.example/s/abc\n")):
            result = self.run_script("pangolin-configure", *args, stdin=stdin, check=False)
            self.assertNotEqual(result.returncode, 0, args)
            self.assertEqual(result.stdout, "", args)
        self.assertEqual((self.repo / "secrets/profile.enc.json").read_text(), before)

    def test_pangolin_configure_leaves_vault_alone_on_bad_input(self):
        self.run_script("setup")
        self.store("profile", {"TAIGA_PASSWORD": "p"})
        before = (self.repo / "secrets/profile.enc.json").read_text()
        for args, stdin in ((("profile", "--stdin"), "pangolin-key-abc.def\n"),
                            (("profile", "--stdin"), "\n"),
                            (("../etc", "--stdin"), "id1.secret\n")):
            result = self.run_script("pangolin-configure", *args, stdin=stdin, check=False)
            self.assertEqual(result.returncode, 1, args)
            self.assertIn("pangolin-configure:", result.stderr, args)
        self.assertEqual((self.repo / "secrets/profile.enc.json").read_text(), before)

class HelpAndPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.home = self.tmp / "home"
        self.home.mkdir()
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        (bin_dir / "python3").symlink_to(shutil.which("python3"))
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith(("SOPS_", "XDG_", "TAIGA_"))}
        self.env.update(HOME=str(self.home), PATH=str(bin_dir))

    def run_script(self, *args):
        return subprocess.run([str(ROOT / "scripts" / args[0]), *args[1:]], env=self.env,
                              stdin=subprocess.DEVNULL, text=True, capture_output=True)

    def test_envtool_help_describes_every_subcommand(self):
        result = self.run_script("envtool", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for command in ("init", "export", "list", "edit", "set"):
            self.assertIn(command, result.stdout)
        self.assertIn("called by setup", result.stdout)

    def test_envtool_subcommand_help_documents_scope(self):
        for command in ("export", "list", "edit", "set"):
            result = self.run_script("envtool", command, "--help")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("profile or project/<name>", result.stdout)
        self.assertIn("hidden", self.run_script("envtool", "set", "--help").stdout)

    def test_envtool_init_help_says_called_by_setup(self):
        result = self.run_script("envtool", "init", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("called by setup", result.stdout)

    def test_dev_env_and_dv_help_list_every_command(self):
        for name in ("dev-env", "dv"):
            result = subprocess.run([str(ROOT / "bin" / name), "--help"], env=self.env,
                                    stdin=subprocess.DEVNULL, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(result.stdout.startswith(f"usage: {name} COMMAND"), result.stdout)
            for command in ("export", "set", "list", "edit", "setup", "taiga-mcp install",
                            "taiga-mcp workflow|full"):
                self.assertIn(command, result.stdout)
            self.assertNotIn("init", result.stdout)
            bare = subprocess.run([str(ROOT / "bin" / name)], env=self.env, stdin=subprocess.DEVNULL,
                                  text=True, capture_output=True)
            self.assertEqual((bare.returncode, bare.stdout), (0, result.stdout))

    def test_setup_help_lists_skip_flag(self):
        result = self.run_script("setup", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--skip-taiga-mcp", result.stdout)
        self.assertIn("--migrate-bashrc", result.stdout)

    def copy_repo(self):
        repo = self.tmp / "repo"
        (repo / "scripts").mkdir(parents=True)
        for name in ("envtool", "setup"):
            shutil.copy2(ROOT / "scripts" / name, repo / "scripts" / name)
        shutil.copy2(ROOT / "profile.sh", repo / "profile.sh")
        return repo

    def run_setup_copy(self, repo):
        return subprocess.run([str(repo / "scripts/setup")], env=self.env, cwd=repo,
                              stdin=subprocess.DEVNULL, text=True, capture_output=True)

    def test_setup_preflight_names_every_missing_tool_and_touches_nothing(self):
        repo = self.copy_repo()
        result = self.run_setup_copy(repo)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertTrue(result.stderr.startswith("setup: missing required tools:"), result.stderr)
        for expected in ("sops:", "age-keygen:", "direnv:", "sudo apt install direnv",
                         "getsops/sops/releases", f"then run: cd {repo} && ./scripts/setup"):
            self.assertIn(expected, result.stderr)
        for name in (".config", ".bashrc", ".profile"):
            self.assertFalse((self.home / name).exists(), name)
        self.assertFalse((repo / ".sops.yaml").exists())
        self.assertFalse((repo / "secrets").exists())

    def test_setup_preflight_reports_only_the_absent_tools(self):
        if not (shutil.which("sops") and shutil.which("age-keygen")):
            self.skipTest("requires sops and age-keygen on the host")
        for name in ("sops", "age-keygen"):
            (self.tmp / "bin" / name).symlink_to(shutil.which(name))
        result = self.run_setup_copy(self.copy_repo())
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("direnv:", result.stderr)
        self.assertNotIn("sops:", result.stderr)
        self.assertNotIn("age-keygen:", result.stderr)


if __name__ == "__main__":
    unittest.main()
