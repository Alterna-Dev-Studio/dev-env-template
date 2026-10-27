"""Lint the installed skill and agent bodies: frontmatter, links, consumer values.

Run with: python3 -m unittest discover -s tests
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK = re.compile(r"\]\(([^)#:]+?\.md)(?:#[^)]*)?\)")
LINK_ROOTS = (".claude/skills", ".claude/agents", ".agents/skills")
CLOSURE = [
    ".claude/skills/fully-implement-story/SKILL.md",
    ".claude/skills/implement-task/SKILL.md",
    ".claude/skills/finalize-story-pr/SKILL.md",
    ".claude/skills/rebase-branch/SKILL.md",
    ".claude/skills/review-tests/SKILL.md",
    ".claude/skills/shared/synchronous-worker-contract.md",
    ".claude/agents/senior-software-developer.md",
    ".claude/agents/test-quality-reviewer.md",
    ".claude/agents/remediation-developer.md",
    ".agents/skills/fully-implement-story/SKILL.md",
    ".agents/skills/implement-task/SKILL.md",
    ".agents/skills/finalize-story-pr/SKILL.md",
    ".agents/skills/rebase-branch/SKILL.md",
]
FORBIDDEN = ("project_id=3", "dotnet", "remediate_pr.py", "TestUnit", "test-results/")


class SkillTests(unittest.TestCase):
    def test_claude_skill_frontmatter_has_required_keys(self):
        skills = sorted((ROOT / ".claude/skills").glob("*/SKILL.md"))
        self.assertTrue(skills, "no .claude/skills/*/SKILL.md found")
        for skill in skills:
            with self.subTest(skill=str(skill.relative_to(ROOT))):
                match = FRONTMATTER.match(skill.read_text(encoding="utf-8"))
                self.assertIsNotNone(match, "missing --- frontmatter block")
                lines = match.group(1).splitlines()
                for key in ("name:", "description:", "allowed-tools:"):
                    self.assertTrue(any(line.startswith(key) for line in lines), f"missing {key}")
                name = next(line for line in lines if line.startswith("name:"))
                self.assertEqual(name.split(":", 1)[1].strip(), skill.parent.name)
        orchestrator = (ROOT / ".claude/skills/fully-implement-story/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("argument-hint:", FRONTMATTER.match(orchestrator).group(1))

    def test_relative_markdown_links_resolve(self):
        checked = 0
        for root in LINK_ROOTS:
            for doc in sorted((ROOT / root).rglob("*.md")):
                for link in LINK.findall(doc.read_text(encoding="utf-8")):
                    if link.startswith("http"):
                        continue
                    checked += 1
                    with self.subTest(file=str(doc.relative_to(ROOT)), link=link):
                        self.assertTrue((doc.parent / link).is_file(), "link target does not exist")
        self.assertGreater(checked, 0, "no relative Markdown links found")

    def test_fully_implement_closure_has_no_youthon_values(self):
        for rel in CLOSURE:
            path = ROOT / rel
            with self.subTest(file=rel):
                self.assertTrue(path.is_file(), "closure file missing")
                text = path.read_text(encoding="utf-8")
                for needle in FORBIDDEN:
                    self.assertFalse(needle in text, f"{needle!r} found in {rel}")


if __name__ == "__main__":
    unittest.main()
