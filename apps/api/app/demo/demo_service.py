import shutil
from pathlib import Path


def get_demo_starter_dir(configured_starter_dir: str) -> Path:
    if configured_starter_dir.strip():
        return Path(configured_starter_dir).resolve()

    repo_root = Path(__file__).resolve().parents[4]
    return repo_root / "packages" / "templates" / "demo-starter"


def seed_demo_workspace(workspace_dir: Path, starter_dir: Path) -> None:
    if not starter_dir.is_dir():
        raise FileNotFoundError(f"Demo starter template not found at: {starter_dir}")

    workspace_dir.mkdir(parents=True, exist_ok=True)
    demo_dir = workspace_dir / "demo"

    if demo_dir.exists():
        shutil.rmtree(demo_dir)

    shutil.copytree(starter_dir, demo_dir)
