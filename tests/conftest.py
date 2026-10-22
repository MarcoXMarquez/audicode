"""Shared fixtures. Env vars are set before ``app`` is ever imported."""
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ["AUTH_ENABLED"] = "false"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def client(tmp_path_factory):
    """TestClient on the real app, with the data dir isolated in a tmp dir."""
    pytest.importorskip("fastapi")
    pytest.importorskip("httpx")
    os.environ["AUTH_ENABLED"] = "false"
    os.environ["ODYSSEUS_DATA_DIR"] = str(tmp_path_factory.mktemp("odysseus_data"))
    from fastapi.testclient import TestClient

    import app as app_module

    with TestClient(app_module.app) as c:
        yield c
