from __future__ import annotations


def inject_stub(dll_path: str, pid: int) -> dict:
    return {"ok": True, "dll_path": dll_path, "pid": pid, "mode": "stub"}
