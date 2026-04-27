#!/usr/bin/env python3
"""Create a Claude-skill style scaffold under skills/<name>/."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="skill name, lowercase snake_case")
    parser.add_argument("--desc", default="One-sentence skill description.")
    parser.add_argument("--root", default=".", help="repo root path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    skill_dir = root / "skills" / args.name
    if skill_dir.exists():
        raise SystemExit(f"Skill directory already exists: {skill_dir}")

    (skill_dir / "references").mkdir(parents=True, exist_ok=False)
    (skill_dir / "scripts").mkdir(parents=True, exist_ok=False)

    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {args.name}",
                f"description: {args.desc}",
                "---",
                "",
                f"# {args.name.replace('_', ' ').title()}",
                "",
                "## Purpose",
                "",
                "Describe what this skill changes in the social-human simulation.",
                "",
                "## Use When",
                "",
                "List situations when this skill should be selected.",
                "",
                "## Procedure",
                "",
                "1. Read required state files if present.",
                "2. Update state with bounded values and clear uncertainty notes.",
                "3. Write output state files.",
                "",
                "## Write",
                "",
                "List output files under state/.",
                "",
                "## Notes",
                "",
                "Keep this skill narrow and composable with cognition/plan.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    (skill_dir / "references" / "research_basis.md").write_text(
        "# Research Basis\n\nList key papers and simulation translation rules.\n",
        encoding="utf-8",
    )

    print(f"Created scaffold: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
