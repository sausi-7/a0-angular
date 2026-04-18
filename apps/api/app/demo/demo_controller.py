from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.demo.demo_service import get_demo_starter_dir, seed_demo_workspace

router = APIRouter(prefix="/demo", tags=["demo"])


class DemoStartResponse(BaseModel):
	ready: bool
	preview_port: int


@router.post("/start", response_model=DemoStartResponse)
async def start_demo() -> DemoStartResponse:
	workspace_dir = Path(settings.workspace_dir).resolve()
	starter_dir = get_demo_starter_dir(settings.demo_starter_dir)

	try:
		seed_demo_workspace(workspace_dir=workspace_dir, starter_dir=starter_dir)
	except FileNotFoundError as exc:
		raise HTTPException(status_code=500, detail=str(exc)) from exc

	return DemoStartResponse(ready=True, preview_port=4300)
