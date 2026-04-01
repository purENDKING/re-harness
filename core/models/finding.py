from __future__ import annotations

from pydantic import BaseModel, Field


class Finding(BaseModel):
    id: str
    session_id: str
    target: dict
    summary: str
    supporting_claim_ids: list[str] = Field(default_factory=list)
    writeback_ready: bool = False
