"""Exercise setup and envtool against a throwaway HOME and repository copy.

Run with: python3 -m unittest discover -s tests
"""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ("sops", "age-keygen", "direnv")


@unittest.skipUnless(all(shutil.which(tool) for tool in TOOLS), "requires " + ", ".join(TOOLS))
class ScriptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.repo = self.tmp / "repo"
        (self.repo / "scripts").mkdir(parents=True)
        for name in ("envtool", "setup", "taiga-mcp"):
            shutil.copy2(ROOT / "scripts" / name, self.repo / "scripts" / name)
        shutil.copy2(ROOT / "profile.sh", self.repo / "profile.sh")
        shutil.copy2(ROOT / "shared-variables.txt", self.repo / "shared-variables.txt")
        shutil.copytree(ROOT / "shell", self.repo / "shell")
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith(("SOPS_", "XDG_CONFIG_HOME", "TAIGA_"))}
        self.env["HOME"] = str(self.home)
        self.key = self.home / ".config/sops/age/keys.txt"
        self.bashrc = self.home / ".bashrc"

    def run_script(self, *args, check=True):
        result = subprocess.run([str(self.repo / "scripts" / args[0]), *args[1:]], env=self.env,
                                cwd=self.repo, text=True, capture_output=True)
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
        # A PATH without direnv: setup should then leave the hook out.
        (self.home / "bin").mkdir()
        for tool in ("python3", "sops", "age-keygen"):
            os.symlink(shutil.which(tool), self.home / "bin" / tool)
        self.env["PATH"] = str(self.home / "bin")
        self.run_script("setup")
        lines = self.bashrc.read_text().splitlines()
        self.assertEqual(lines[0], "export EDITOR=vim")
        self.assertFalse(any("direnv" in line for line in lines))

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

    def test_migrate_bashrc_uses_shared_variables_file(self):
        (self.repo / "shared-variables.txt").write_text("# names\nFOO\n\nBAR # trailing\n")
        self.bashrc.write_text("export FOO=1\nexport BAR=2\nexport BAZ=3\n")
        self.env.update({"FOO": "1", "BAR": "2", "BAZ": "3"})
        self.run_script("setup")
        self.run_script("setup", "--migrate-bashrc")
        self.assertEqual(self.run_script("envtool", "list", "profile").stdout.split(), ["BAR", "FOO"])
        bashrc = self.bashrc.read_text()
        self.assertNotIn("export FOO=", bashrc)
        self.assertNotIn("export BAR=", bashrc)
        self.assertIn("export BAZ=3", bashrc)
        (self.repo / "shared-variables.txt").write_text("FOO\nnot-a-name\n")
        result = self.run_script("setup", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("shared-variables.txt", result.stderr)

    def test_profile_exports_values_in_bash(self):
        self.run_script("setup")
        self.store("profile", {"FOO": "it's here"})
        result = subprocess.run(["bash", "-c", f'source {self.repo}/profile.sh; printf %s "$FOO"'],
                                env=self.env, text=True, capture_output=True, check=True)
        self.assertEqual(result.stdout, "it's here")
        self.assertEqual(result.stderr, "")
        result = subprocess.run(["bash", "-c", f'source {self.repo}/profile.sh; printf %s "$DEV_ENV_HOME"'],
                                env=self.env, text=True, capture_output=True, check=True)
        self.assertEqual(result.stdout, str(self.repo))


if __name__ == "__main__":
    unittest.main()
