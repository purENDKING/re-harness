from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class Claim(BaseModel):
    id: str
    session_id: str
    target: dict
    statement: str
    status: Literal["new", "testing", "supported", "confirmed", "rejected"] = "new"
    confidence: float = Field(default=0.3, ge=0.0, le=1.0)
