from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from apps.api.deps import DbSession
from core.services import session_service

router = APIRouter(prefix="/sessions", tags=["sessions"])


class StartSessionRequest(BaseModel):
    sample_path: str
    ghidra_project: str | None = None
    target_process: str | None = None


@router.post("/start")
def start_session(payload: StartSessionRequest, db: DbSession) -> dict:
    session = session_service.create_session(
        db=db,
        sample_path=payload.sample_path,
        ghidra_project=payload.ghidra_project,
        target_process=payload.target_process,
    )
    return session.model_dump()


@router.get("/{session_id}")
def get_session(session_id: str, db: DbSession) -> dict:
    session = session_service.get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")
    return session.model_dump()
