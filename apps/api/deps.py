from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.graph.state import WorkflowState
from core.services import session_service
from storage.db import get_db_session

DbSession = Annotated[Session, Depends(get_db_session)]

_STATE_STORE: dict[str, WorkflowState] = {}


def get_state_store() -> dict[str, WorkflowState]:
    return _STATE_STORE


def get_or_create_state(db: Session, session_id: str) -> WorkflowState:
    state = _STATE_STORE.get(session_id)
    if state is not None:
        return state

    session = session_service.get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")

    state = WorkflowState(
        session_id=session.id,
        sample_path=session.sample_path,
        target_process=session.target_process,
    )
    _STATE_STORE[session_id] = state
    return state
