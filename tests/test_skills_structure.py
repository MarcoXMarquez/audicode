import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIRS = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())


def parse_frontmatter(text):
    m = re.match(r"\A﻿?---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    assert m, "missing YAML frontmatter"
    data = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        k, sep, v = line.partition(":")
        assert sep, f"bad frontmatter line: {line!r}"
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def test_skills_exist():
    assert SKILL_DIRS


@pytest.mark.parametrize("skill", SKILL_DIRS, ids=lambda p: p.name)
def test_skill_md_frontmatter(skill):
    md = skill / "SKILL.md"
    assert md.is_file()
    fm = parse_frontmatter(md.read_text(encoding="utf-8"))
    assert fm.get("name") == skill.name
    assert len(fm.get("description", "")) > 20


@pytest.mark.parametrize("skill", SKILL_DIRS, ids=lambda p: p.name)
def test_skill_has_scripts_and_evals(skill):
    assert list((skill / "scripts").glob("*.py"))
    assert (skill / "evals" / "evals.json").is_file()


@pytest.mark.parametrize("skill", SKILL_DIRS, ids=lambda p: p.name)
def test_evals_json_valid_and_files_exist(skill):
    data = json.loads((skill / "evals" / "evals.json").read_text(encoding="utf-8"))
    assert data["evals"]
    for ev in data["evals"]:
        for f in ev.get("files", []) + ev.get("input_files", []):
            assert (ROOT / f).is_file(), f"{skill.name}: missing eval file {f}"


def test_data_skills_mirror_skills():
    data_dir = ROOT / "data" / "skills"
    if not data_dir.is_dir():
        pytest.skip("no data/skills")
    for skill in SKILL_DIRS:
        assert (data_dir / skill.name / "SKILL.md").is_file()
