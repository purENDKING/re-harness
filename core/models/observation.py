from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from core.models.enums import ObservationSource


class Observation(BaseModel):
    id: str
    session_id: str
    source: ObservationSource
    object_ref: str
    payload: dict = Field(default_factory=dict)
    timestamp: datetime
