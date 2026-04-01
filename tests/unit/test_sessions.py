from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import create_app
from storage.db import init_db, reset_engine


def test_session_create_and_fetch(tmp_path: Path) -> None:
    db_url = f"sqlite:///{tmp_path / 'test_sessions.db'}"
    reset_engine(db_url)
    init_db(drop_all=True)

    app = create_app()
    client = TestClient(app)

    create_resp = client.post(
        "/sessions/start",
        json={
            "sample_path": "samples/game.exe",
            "ghidra_project": "projects/demo.gpr",
            "target_process": "game.exe",
        },
    )
    assert create_resp.status_code == 200
    created = create_resp.json()
    assert created["sample_path"] == "samples/game.exe"
    assert created["status"] == "new"

    fetch_resp = client.get(f"/sessions/{created['id']}")
    assert fetch_resp.status_code == 200
    fetched = fetch_resp.json()
    assert fetched["id"] == created["id"]
    assert fetched["target_process"] == "game.exe"
