from __future__ import annotations


def run(state: dict) -> dict:
    target = state.get("active_target") or {}
    state["experiment_plan"] = {
        "kind": "logging_probe",
        "target": target,
        "purpose": "collect runtime evidence for selected claim",
        "steps": [
            {"type": "attach", "target_process": "<fill-at-runtime>"},
            {"type": "log_field_access", "address": target.get("ref")},
        ],
    }
    return state
