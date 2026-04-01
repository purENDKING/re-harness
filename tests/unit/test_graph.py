from __future__ import annotations

from apps.worker.graph_factory import run_workflow
from core.graph.state import WorkflowState


def test_mock_graph_flow_completes() -> None:
    initial = WorkflowState(
        session_id="graph-test",
        sample_path="samples/game.exe",
        target_process="game.exe",
        current_function_addr="0x140001000",
        current_selection="player->inventory",
        goals=["verify structure", "build patch prototype"],
    )

    result = run_workflow(initial)

    assert result.current_decompile is not None
    assert len(result.hypotheses) >= 1
    assert len(result.observations) >= 2
    assert result.patch_project_path is not None
    assert result.build_result is not None
    assert result.runtime_result is not None
    assert len(result.review_items) >= 1
    assert result.final_summary is not None
