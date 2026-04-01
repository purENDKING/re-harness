from __future__ import annotations

from pathlib import Path


def read_stub_logs(project_path: str) -> list[dict]:
    log_file = Path(project_path) / "runtime.log"
    if not log_file.exists():
        log_file.write_text("hook installed\nvalue observed: 1337\n", encoding="utf-8")
    return [
        {"level": "INFO", "message": line.strip()}
        for line in log_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
