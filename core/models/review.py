from __future__ import annotations

from pydantic import BaseModel, Field


class ReviewItem(BaseModel):
    id: str
    session_id: str
    item_type: str
    target_ref: str
    proposal: dict = Field(default_factory=dict)
    status: str
