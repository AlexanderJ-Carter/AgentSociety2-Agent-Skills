from pathlib import Path
import importlib.util
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"


class SkillRepositoryTests(unittest.TestCase):
    def test_repository_policy_files_exist(self) -> None:
        required_files = (
            "LICENSE",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "CITATION.cff",
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/ISSUE_TEMPLATE/bug_report.md",
            ".github/ISSUE_TEMPLATE/skill_request.md",
        )
        missing = [p for p in required_files if not (REPO_ROOT / p).exists()]
        self.assertEqual([], missing)

    def test_all_skills_follow_public_skill_structure(self) -> None:
        required_sections = (
            "## Purpose",
            "## Internal Logic (One Sentence)",
            "## Use When",
            "## Procedure",
            "## Write",
            "## Notes",
        )

        failures: list[str] = []
        for skill_dir in sorted(p for p in SKILLS_ROOT.iterdir() if p.is_dir()):
            skill_file = skill_dir / "SKILL.md"
            text = skill_file.read_text(encoding="utf-8")
            for section in required_sections:
                if section not in text:
                    failures.append(f"{skill_file.relative_to(REPO_ROOT)} missing {section}")
            if "state\\" in text or "skills\\" in text or "references\\" in text:
                failures.append(f"{skill_file.relative_to(REPO_ROOT)} contains Windows-style path separators")
            references_dir = skill_dir / "references"
            if not references_dir.exists() or not list(references_dir.glob("*.md")):
                failures.append(f"{skill_dir.relative_to(REPO_ROOT)} missing bundled reference notes")

        self.assertEqual([], failures)

    def test_catalog_builder_exposes_runtime_metadata(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "generate_skill_catalog",
            REPO_ROOT / "scripts" / "generate_skill_catalog.py",
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules["generate_skill_catalog"] = module
        spec.loader.exec_module(module)

        skills = [
            module._load_skill_meta(REPO_ROOT, p)
            for p in sorted(SKILLS_ROOT.iterdir())
            if p.is_dir() and (p / "SKILL.md").exists()
        ]
        catalog = module.build_catalog_md(skills)

        self.assertIn("Runtime role", catalog)
        self.assertIn("Script", catalog)
        self.assertIn("Research basis", catalog)
        self.assertIn("Claude Skill style", catalog)


if __name__ == "__main__":
    unittest.main()
