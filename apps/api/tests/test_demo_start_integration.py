from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

client = TestClient(app)


def _collect_tree(root: Path) -> tuple[set[str], dict[str, bytes]]:
    dirs: set[str] = set()
    files: dict[str, bytes] = {}

    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        if path.is_dir():
            dirs.add(rel)
        else:
            files[rel] = path.read_bytes()

    return dirs, files


def test_demo_start_seeds_workspace_and_is_idempotent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    starter_dir = tmp_path / "starter"
    (starter_dir / "src").mkdir(parents=True)
    (starter_dir / "src" / "app.txt").write_text("starter-content", encoding="utf-8")
    (starter_dir / "README.md").write_text("starter-readme", encoding="utf-8")

    workspace_dir = tmp_path / "workspace"

    monkeypatch.setattr(settings, "workspace_dir", str(workspace_dir))
    monkeypatch.setattr(settings, "demo_starter_dir", str(starter_dir))

    first_response = client.post("/demo/start")
    assert first_response.status_code == 200
    assert first_response.json() == {"ready": True, "preview_port": 4300}

    starter_dirs, starter_files = _collect_tree(starter_dir)
    seeded_dirs, seeded_files = _collect_tree(workspace_dir / "demo")
    assert seeded_dirs == starter_dirs
    assert seeded_files == starter_files

    (workspace_dir / "demo" / "src" / "app.txt").write_text("changed", encoding="utf-8")
    (workspace_dir / "demo" / "extra.txt").write_text("should-be-removed", encoding="utf-8")

    second_response = client.post("/demo/start")
    assert second_response.status_code == 200

    reseeded_dirs, reseeded_files = _collect_tree(workspace_dir / "demo")
    assert reseeded_dirs == starter_dirs
    assert reseeded_files == starter_files
