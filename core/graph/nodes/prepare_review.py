from __future__ import annotations


def run(state: dict) -> dict:
    target = state.get("active_target") or {}
    claim = next((c for c in state.get("claims", []) if c.get("id") == state.get("selected_claim_id")), None)
    state["review_items"] = [{
        "id": f"review-{state['session_id']}",
        "session_id": state["session_id"],
        "item_type": "claim_review",
        "target_ref": target.get("ref", ""),
        "proposal": {
            "claim": claim,
            "evidence_count": len(state.get("evidence_items", [])),
            "experiment_plan": state.get("experiment_plan"),
        },
        "status": "pending",
    }]
    return state
