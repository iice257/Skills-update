import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "skills-update" / "scripts" / "update_skills.py"
SPEC = importlib.util.spec_from_file_location("update_skills", SCRIPT)
update_skills = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["update_skills"] = update_skills
SPEC.loader.exec_module(update_skills)


class SourceParsingTests(unittest.TestCase):
    def test_parses_owner_repo_path_ref_source(self):
        source = update_skills.parse_source_value(
            "my-skill",
            "owner/repo:skills/my-skill@dev",
            "test",
        )

        self.assertEqual(source.skill, "my-skill")
        self.assertEqual(source.repo, "owner/repo")
        self.assertEqual(source.path, "skills/my-skill")
        self.assertEqual(source.ref, "dev")

    def test_parses_github_tree_url(self):
        source = update_skills.parse_source_value(
            "my-skill",
            "https://github.com/owner/repo/tree/main/skills/my-skill",
            "test",
        )

        self.assertEqual(source.repo, "owner/repo")
        self.assertEqual(source.path, "skills/my-skill")
        self.assertEqual(source.ref, "main")


class DigestTests(unittest.TestCase):
    def test_digest_ignores_updater_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp)
            (skill_dir / "SKILL.md").write_text("---\nname: x\ndescription: x\n---\n", encoding="utf-8")
            before = update_skills.digest_dir(skill_dir)

            (skill_dir / update_skills.METADATA_FILE_NAME).write_text(
                json.dumps({"repo": "owner/repo"}),
                encoding="utf-8",
            )
            after = update_skills.digest_dir(skill_dir)

        self.assertEqual(before, after)


class SkillDiscoveryTests(unittest.TestCase):
    def test_skips_system_skills_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills_dir = Path(tmp)
            regular = skills_dir / "regular-skill"
            regular.mkdir()
            (regular / "SKILL.md").write_text("---\nname: regular-skill\ndescription: x\n---\n", encoding="utf-8")
            system = skills_dir / ".system" / "system-skill"
            system.mkdir(parents=True)
            (system / "SKILL.md").write_text("---\nname: system-skill\ndescription: x\n---\n", encoding="utf-8")

            found = update_skills.list_skill_dirs(skills_dir, include_system=False, only=set())

        self.assertEqual([name for name, _path in found], ["regular-skill"])


if __name__ == "__main__":
    unittest.main()
