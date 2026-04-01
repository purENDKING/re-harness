from __future__ import annotations

from core.graph.nodes import (
    inspect_target_context,
    propose_claims,
    collect_evidence,
    draft_experiment,
    prepare_review,
)


def run_research_round(state: dict) -> dict:
    state = inspect_target_context.run(state)
    if state.get("error"):
        return state
    state = propose_claims.run(state)
    state = collect_evidence.run(state)
    state = draft_experiment.run(state)
    state = prepare_review.run(state)
    return state
