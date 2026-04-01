from __future__ import annotations

from core.services.research_service import ResearchService


def run(state: dict) -> dict:
    service = ResearchService()
    target = state.get("active_target") or {}
    claims = [c.model_dump() for c in service.propose_claims_for_function(state["session_id"], target["ref"])]
    state["claims"] = claims
    state["selected_claim_id"] = claims[0]["id"] if claims else None
    return state
