from __future__ import annotations

from core.services.research_service import ResearchService


def run(state: dict) -> dict:
    service = ResearchService()
    target = state.get("active_target") or {}
    claim_id = state.get("selected_claim_id")
    if not claim_id:
        return state
    items = [e.model_dump() for e in service.collect_static_evidence_for_claim(state["session_id"], target["ref"], claim_id)]
    state["evidence_items"] = items
    return state
