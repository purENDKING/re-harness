from __future__ import annotations

from core.services.research_service import ResearchService


def run(state: dict) -> dict:
    service = ResearchService()
    target = state.get("active_target") or {}
    if target.get("kind") != "function" or not target.get("ref"):
        return {**state, "error": "active_target must be a function target"}
    bundle = service.inspect_function_target(state["session_id"], target["ref"])
    state["context_bundle"] = bundle["context"]
    return state
