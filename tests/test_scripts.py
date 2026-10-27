"""Exercise setup and envtool against a throwaway HOME and repository copy.

Run with: python3 -m unittest discover -s tests
"""
import os
from pathlib import Path
import pty
import shutil
import subprocess
import tempfile
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
        for name in ("envtool", "setup", "setup-taiga-mcp", "taiga-mcp"):
            shutil.copy2(ROOT / "scripts" / name, self.repo / "scripts" / name)
        shutil.copy2(ROOT / "profile.sh", self.repo / "profile.sh")
        shutil.copy2(ROOT / ".envrc", self.repo / ".envrc")
        shutil.copytree(ROOT / "shell", self.repo / "shell")
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

    def run_script(self, *args, check=True, skip_taiga_mcp=True):
        if args[0] == "setup" and skip_taiga_mcp and "--skip-taiga-mcp" not in args:
            args = (*args, "--skip-taiga-mcp")
        result = subprocess.run([str(self.repo / "scripts" / args[0]), *args[1:]], env=self.env,
                                cwd=self.repo, stdin=subprocess.DEVNULL, text=True, capture_output=True)
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
                         "getsops/sops/releases"):
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


class NewDevEnvTests(unittest.TestCase):
    """Drive new-dev-env with a fake gh that clones a stub setup, so no network is used."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.work = self.tmp / "work"
        self.work.mkdir()
        self.bin = self.tmp / "bin"
        self.bin.mkdir()
        self.log = self.tmp / "log"
        self.write_tool("gh", """
            echo "gh $*" >> "$LOG"
            dir="${3##*/}"; mkdir -p "$dir/scripts"
            [ -n "${EMPTY_CLONE:-}" ] && exit 0
            printf '#!/bin/sh\\necho "setup $(basename "$PWD") $*" >> "$LOG"\\n' > "$dir/scripts/setup"
            chmod +x "$dir/scripts/setup"
        """)
        self.env = {"HOME": str(self.tmp), "LOG": str(self.log),
                    "PATH": os.pathsep.join([str(self.bin), "/usr/bin", "/bin"])}

    def write_tool(self, name, body):
        tool = self.bin / name
        tool.write_text("#!/bin/sh\n" + "\n".join(line.strip() for line in body.splitlines()) + "\n")
        tool.chmod(0o755)

    def run_new(self, *args):
        return subprocess.run([str(ROOT / "scripts/new-dev-env"), *args], env=self.env, cwd=self.work,
                              stdin=subprocess.DEVNULL, text=True, capture_output=True)

    def test_creates_private_repo_from_template_and_runs_setup_in_clone(self):
        result = self.run_new("me/box", "--skip-taiga-mcp")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.log.read_text().splitlines(), [
            "gh repo create me/box --template Alterna-Dev-Studio/dev-env-template --private --clone",
            "setup box --skip-taiga-mcp",
        ])

    def test_default_name_is_my_dev_env(self):
        self.assertEqual(self.run_new().returncode, 0)
        self.assertIn("gh repo create my-dev-env ", self.log.read_text())

    def test_existing_directory_is_refused_before_creating_a_repo(self):
        (self.work / "box").mkdir()
        result = self.run_new("box")
        self.assertEqual(result.returncode, 1)
        self.assertIn("box already exists", result.stderr)
        self.assertFalse(self.log.exists())

    def test_empty_clone_is_pulled_until_template_files_arrive(self):
        self.env["EMPTY_CLONE"] = "1"
        self.write_tool("git", """
            echo "git $*" >> "$LOG"
            printf '#!/bin/sh\\necho "setup $(basename "$PWD")" >> "$LOG"\\n' > "$2/scripts/setup"
            chmod +x "$2/scripts/setup"
        """)
        result = self.run_new("box")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.log.read_text().splitlines()[1:],
                         ["git -C box pull --quiet origin HEAD", "setup box"])


if __name__ == "__main__":
    unittest.main()
