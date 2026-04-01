from __future__ import annotations

from typing import Any, Callable

from core.graph.edges import (
    ACTION_DYNAMIC_PROBE,
    ACTION_GENERATE_PATCH,
    ACTION_REQUEST_REVIEW,
    route_next_action,
)
from core.graph.nodes import (
    commit_back,
    decide_next_action,
    dynamic_probe,
    generate_patch_prototype,
    ingest_context,
    request_human_review,
    static_analyze,
    verify_patch_build,
    verify_runtime_effect,
)
from core.graph.state import WorkflowState

try:
    from langgraph.graph import END, START, StateGraph

    HAS_LANGGRAPH = True
except Exception:  # pragma: no cover - fallback if langgraph is not installed
    HAS_LANGGRAPH = False
    END = "__end__"
    START = "__start__"


class _ManualGraph:
    def invoke(self, state: dict[str, Any]) -> dict[str, Any]:
        current = dict(state)
        current.update(ingest_context.run(current))
        current.update(static_analyze.run(current))

        while True:
            current.update(decide_next_action.run(current))
            action = route_next_action(current)
            if action == ACTION_DYNAMIC_PROBE:
                current.update(dynamic_probe.run(current))
                continue
            if action == ACTION_GENERATE_PATCH:
                current.update(generate_patch_prototype.run(current))
                current.update(verify_patch_build.run(current))
                current.update(verify_runtime_effect.run(current))
                current.update(request_human_review.run(current))
                current.update(commit_back.run(current))
                return current
            current.update(request_human_review.run(current))
            current.update(commit_back.run(current))
            return current


def create_workflow_graph():
    if not HAS_LANGGRAPH:
        return _ManualGraph()

    graph = StateGraph(dict)
    graph.add_node("ingest_context", ingest_context.run)
    graph.add_node("static_analyze", static_analyze.run)
    graph.add_node("decide_next_action", decide_next_action.run)
    graph.add_node("dynamic_probe", dynamic_probe.run)
    graph.add_node("generate_patch_prototype", generate_patch_prototype.run)
    graph.add_node("verify_patch_build", verify_patch_build.run)
    graph.add_node("verify_runtime_effect", verify_runtime_effect.run)
    graph.add_node("request_human_review", request_human_review.run)
    graph.add_node("commit_back", commit_back.run)

    graph.add_edge(START, "ingest_context")
    graph.add_edge("ingest_context", "static_analyze")
    graph.add_edge("static_analyze", "decide_next_action")
    graph.add_conditional_edges(
        "decide_next_action",
        route_next_action,
        {
            ACTION_DYNAMIC_PROBE: "dynamic_probe",
            ACTION_GENERATE_PATCH: "generate_patch_prototype",
            ACTION_REQUEST_REVIEW: "request_human_review",
        },
    )
    graph.add_edge("dynamic_probe", "decide_next_action")
    graph.add_edge("generate_patch_prototype", "verify_patch_build")
    graph.add_edge("verify_patch_build", "verify_runtime_effect")
    graph.add_edge("verify_runtime_effect", "request_human_review")
    graph.add_edge("request_human_review", "commit_back")
    graph.add_edge("commit_back", END)
    return graph.compile()


def run_workflow(state: WorkflowState) -> WorkflowState:
    compiled = create_workflow_graph()
    result = compiled.invoke(state.model_dump())
    return WorkflowState.model_validate(result)


def run_generate_hook_path(state: WorkflowState) -> WorkflowState:
    current = state.model_dump()
    current.update(generate_patch_prototype.run(current))
    current.update(verify_patch_build.run(current))
    current.update(verify_runtime_effect.run(current))
    current.update(request_human_review.run(current))
    current.update(commit_back.run(current))
    return WorkflowState.model_validate(current)
