"""Exercise scripts/update-from-template against throwaway template and copy repositories.

Run with: python3 -m unittest discover -s tests
"""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


@unittest.skipUnless(shutil.which("git"), "requires git")
class UpdateFromTemplateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith(("GIT_", "DEV_ENV_"))}
        self.env.update(HOME=str(self.tmp), GIT_CONFIG_NOSYSTEM="1",
                        GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com",
                        GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
        self.template = self.tmp / "template"
        self.template.mkdir()
        self.git(self.template, "init", "-q", "-b", "main")
        (self.template / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/update-from-template", self.template / "scripts")
        (self.template / "README.md").write_text("one\ntwo\nthree\n")
        self.commit(self.template, "initial")

    def git(self, repo, *args, check=True):
        result = subprocess.run(["git", *args], cwd=repo, env=self.env, text=True, capture_output=True)
        if check and result.returncode:
            self.fail(f"git {args} failed: {result.stderr}")
        return result.stdout.strip()

    def commit(self, repo, message):
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", message)

    def copy_from_template(self):
        """What `gh repo create --template` makes: the template's files in a fresh history."""
        copy = self.tmp / "copy"
        shutil.copytree(self.template, copy, ignore=shutil.ignore_patterns(".git"))
        self.git(copy, "init", "-q", "-b", "main")
        self.commit(copy, "Initial commit")
        self.git(copy, "remote", "add", "origin", "git@github.com:someone/my-dev-env.git")
        return copy

    def update(self, repo, *args):
        return subprocess.run([str(repo / "scripts/update-from-template"), "--url", str(self.template), *args],
                              cwd=self.tmp, env=self.env, stdin=subprocess.DEVNULL, text=True,
                              capture_output=True)

    def test_first_sync_merges_from_the_matching_template_commit(self):
        copy = self.copy_from_template()
        (copy / "README.md").write_text("ONE\ntwo\nthree\n")
        self.commit(copy, "personal change")
        (self.template / "README.md").write_text("one\ntwo\nTHREE\n")
        (self.template / "new.txt").write_text("new\n")
        self.commit(self.template, "template change")

        result = self.update(copy)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("First sync: merging from template commit", result.stdout)
        self.assertEqual(self.git(copy, "branch", "--show-current"), "template-sync")
        self.assertEqual((copy / "README.md").read_text(), "ONE\ntwo\nTHREE\n")
        self.assertTrue((copy / "new.txt").is_file())
        parents = self.git(copy, "log", "-1", "--format=%P").split()
        self.assertEqual(parents[1], self.git(self.template, "rev-parse", "HEAD"))
        self.assertEqual(self.git(copy, "status", "--porcelain"), "")

        # The histories are now linked, so the next sync is an ordinary merge.
        self.git(copy, "switch", "-q", "main")
        self.git(copy, "merge", "-q", "--ff-only", "template-sync")
        self.git(copy, "branch", "-q", "-d", "template-sync")
        (self.template / "later.txt").write_text("later\n")
        self.commit(self.template, "later change")
        result = self.update(copy)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("First sync", result.stdout)
        self.assertTrue((copy / "later.txt").is_file())

    def test_reports_up_to_date_without_creating_a_branch(self):
        copy = self.copy_from_template()
        (self.template / "new.txt").write_text("new\n")
        self.commit(self.template, "template change")
        self.assertEqual(self.update(copy).returncode, 0)
        self.git(copy, "switch", "-q", "main")
        self.git(copy, "merge", "-q", "--ff-only", "template-sync")
        self.git(copy, "branch", "-q", "-d", "template-sync")

        result = self.update(copy)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Already up to date", result.stdout)
        self.assertEqual(self.git(copy, "branch", "--list", "template-sync"), "")

    def test_conflict_leaves_merge_for_the_user_and_exits_1(self):
        copy = self.copy_from_template()
        (copy / "README.md").write_text("mine\ntwo\nthree\n")
        self.commit(copy, "personal change")
        (self.template / "README.md").write_text("theirs\ntwo\nthree\n")
        self.commit(self.template, "template change")

        result = self.update(copy)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Conflicts on branch template-sync:\n  README.md", result.stdout)
        self.assertEqual(self.git(copy, "rev-parse", "MERGE_HEAD"), self.git(self.template, "rev-parse", "HEAD"))

        (copy / "README.md").write_text("both\ntwo\nthree\n")
        self.git(copy, "add", "README.md")
        self.git(copy, "commit", "-q", "--no-edit")
        self.assertEqual(len(self.git(copy, "log", "-1", "--format=%P").split()), 2)

    def test_unrelated_copy_without_a_base_falls_back_to_a_two_way_merge(self):
        copy = self.tmp / "copy"
        (copy / "scripts").mkdir(parents=True)
        shutil.copy2(ROOT / "scripts/update-from-template", copy / "scripts")
        (copy / "mine.txt").write_text("mine\n")
        self.git(copy, "init", "-q", "-b", "main")
        self.commit(copy, "started elsewhere")

        result = self.update(copy)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("no common template commit found", result.stdout)
        self.assertTrue((copy / "README.md").is_file() and (copy / "mine.txt").is_file())

    def test_refuses_a_dirty_tree_an_existing_branch_and_the_template_itself(self):
        copy = self.copy_from_template()
        (copy / "README.md").write_text("dirty\n")
        result = self.update(copy)
        self.assertEqual(result.returncode, 1)
        self.assertIn("commit or stash your changes first", result.stderr)
        self.git(copy, "checkout", "-q", "--", "README.md")

        self.git(copy, "branch", "template-sync")
        result = self.update(copy)
        self.assertEqual(result.returncode, 1)
        self.assertIn("branch template-sync already exists", result.stderr)

        self.git(self.template, "remote", "add", "origin",
                 "git@github.com:Alterna-Dev-Studio/dev-env-template.git")
        result = subprocess.run([str(self.template / "scripts/update-from-template")], cwd=self.tmp,
                                env=self.env, stdin=subprocess.DEVNULL, text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("this is the template itself", result.stderr)

    def test_help_and_bad_arguments(self):
        script = str(ROOT / "scripts/update-from-template")
        result = subprocess.run([script, "--help"], env=self.env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--base COMMIT", result.stdout)
        result = subprocess.run([script, "--bogus"], env=self.env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage: update-from-template", result.stderr)


if __name__ == "__main__":
    unittest.main()
