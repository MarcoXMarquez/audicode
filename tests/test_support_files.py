import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_env_example_parses():
    text = (ROOT / ".env.example").read_text(encoding="utf-8-sig")
    pairs = {}
    commented = 0
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if re.match(r"^#\s*[A-Z][A-Z0-9_]*=", s):
            commented += 1  # documented optional variable
        if not s or s.startswith("#"):
            continue
        assert re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", s), f"line {n} not KEY=VALUE: {line!r}"
        k, _, v = s.partition("=")
        pairs[k] = v
    assert pairs or commented


def test_pyproject_parses():
    tomllib = pytest.importorskip("tomllib")
    cfg = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert cfg["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]


def test_requirements_lines_well_formed():
    for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and not s.startswith(("#", "-")):
            assert re.match(r"^[A-Za-z0-9_.\-\[\],]+\s*([<>=!~]=?.*)?(;.*)?$", s), line
