from __future__ import annotations

from typing import Literal, Any
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    id: str
    session_id: str
    claim_id: str | None = None
    source: Literal["ghidra", "ce", "patch_runtime", "user", "document"]
    source_ref: str
    summary: str
    payload: dict[str, Any] = Field(default_factory=dict)
    strength: float = Field(default=0.5, ge=0.0, le=1.0)
