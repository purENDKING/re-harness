from __future__ import annotations

import json

from apps.worker.graph_factory import run_workflow
from core.graph.state import WorkflowState


def run_demo() -> WorkflowState:
    initial = WorkflowState(
        session_id="demo-session",
        sample_path="samples/game.exe",
        target_process="game.exe",
        current_function_addr="0x140001000",
        current_selection="player->inventory",
        goals=["verify structure field meaning", "prepare a minimal logging hook"],
    )
    return run_workflow(initial)


if __name__ == "__main__":
    result = run_demo()
    print(json.dumps(result.model_dump(), indent=2))
