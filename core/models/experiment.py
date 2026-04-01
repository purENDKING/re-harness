from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


class ExperimentPlan(BaseModel):
    id: str
    session_id: str
    target: dict
    purpose: str
    steps: list[dict[str, Any]] = Field(default_factory=list)
    expected_signal: str = ""
    status: Literal["new", "running", "done", "failed", "cancelled"] = "new"
