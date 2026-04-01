from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from core.graph.factory import run_research_round

router = APIRouter(prefix="/research", tags=["research"])


class InspectRequest(BaseModel):
    session_id: str
    function_address: str


@router.post("/run-round")
def run_round(payload: InspectRequest) -> dict:
    state = {
        "session_id": payload.session_id,
        "active_target": {"kind": "function", "ref": payload.function_address},
    }
    return run_research_round(state)
