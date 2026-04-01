from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from core.models.enums import SessionStatus


class Session(BaseModel):
    id: str
    sample_path: str
    ghidra_project: str | None = None
    target_process: str | None = None
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
