from __future__ import annotations

from pydantic import BaseModel, Field


class WorkflowState(BaseModel):
    session_id: str
    active_target: dict | None = None

    context_bundle: dict | None = None

    claims: list[dict] = Field(default_factory=list)
    selected_claim_id: str | None = None

    evidence_items: list[dict] = Field(default_factory=list)
    observation_items: list[dict] = Field(default_factory=list)

    experiment_plan: dict | None = None
    review_items: list[dict] = Field(default_factory=list)

    finding: dict | None = None
    error: str | None = None
