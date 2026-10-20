"""Exercise Bash startup fragments without a SOPS key or real home directory."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ShellTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        for name in (".local/bin", "bin", ".volta/bin", "go/bin"):
            (self.home / name).mkdir(parents=True)
        self.env = {**os.environ, "HOME": str(self.home),
                    "PATH": f"/usr/bin:/bin:{self.home}/.local/bin"}
        for name in ("VOLTA_HOME", "PNPM_HOME", "FLYCTL_INSTALL"):
            self.env.pop(name, None)

    def bash(self, script):
        return subprocess.run(["/bin/bash", "--noprofile", "--norc", "-c", script],
                              env=self.env, text=True, capture_output=True, check=True).stdout

    def test_paths_are_repeatable_and_local_bin_wins(self):
        paths = ROOT / "shell/paths.sh"
        output = self.bash(f'source "{paths}"; source "{paths}"; '
                           'printf "%s\\n%s\\n%s\\n" "$PATH" "$VOLTA_HOME" "$PNPM_HOME"')
        path, volta, pnpm = output.splitlines()
        self.assertEqual(path.split(":")[0], str(self.home / ".local/bin"))
        self.assertEqual(path.split(":").count(str(self.home / ".local/bin")), 1)
        self.assertEqual(path.split(":").count(str(self.home / ".volta/bin")), 1)
        self.assertEqual(volta, str(self.home / ".volta"))
        self.assertEqual(pnpm, str(self.home / ".local/share/pnpm"))

    def test_container_install_is_repeatable_and_shell_only(self):
        bashrc = self.home / ".bashrc"
        bashrc.write_text('case $- in *i*) ;; *) return;; esac\n')
        installer = ROOT / "shell/install-container.sh"
        for _ in range(2):
            subprocess.run(["/bin/bash", str(installer)], env=self.env,
                           text=True, capture_output=True, check=True)
        self.assertEqual(bashrc.read_text().count('# >>> dev-env shell'), 1)
        self.assertEqual((self.home / ".profile").read_text().count('# >>> dev-env shell'), 1)
        for rc in (bashrc, self.home / ".profile"):
            output = self.bash(f'source "{rc}"; printf "%s\\n" "$PATH"')
            self.assertEqual(output.splitlines()[0].split(":")[0],
                             str(self.home / ".local/bin"))

    def test_host_setup_inserts_login_and_interactive_sources_once(self):
        (self.home / ".bashrc").write_text("# Keep direnv last\n")
        (self.home / ".profile").write_text("# login file\n")
        code = ("import runpy; m=runpy.run_path('" + str(ROOT / "scripts/setup") + "'); "
                "m['rewrite_bashrc'](False); m['rewrite_loginrc'](); "
                "m['rewrite_bashrc'](False); m['rewrite_loginrc']()")
        subprocess.run(["python3", "-c", code], env=self.env, check=True,
                       text=True, capture_output=True)
        bashrc = (self.home / ".bashrc").read_text()
        profile = (self.home / ".profile").read_text()
        self.assertEqual(bashrc.count("source " + str(ROOT / "profile.sh")), 1)
        self.assertLess(bashrc.index("source "), bashrc.index("# Keep direnv last"))
        self.assertEqual(profile.count(". " + str(ROOT / "profile.sh")), 1)


if __name__ == "__main__":
    unittest.main()
