from __future__ import annotations

from pathlib import Path


def compile_stub(project_path: str) -> dict:
    build_dir = Path(project_path) / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    artifact = build_dir / "mock_patch.dll"
    artifact.write_text("stub dll artifact placeholder", encoding="utf-8")
    return {"ok": True, "artifact_path": str(artifact)}
