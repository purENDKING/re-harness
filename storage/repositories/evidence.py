from __future__ import annotations

from typing import Any


class EvidenceRepository:
    def __init__(self) -> None:
        self._items: dict[str, dict[str, Any]] = {}

    def upsert(self, item: dict[str, Any]) -> dict[str, Any]:
        self._items[item["id"]] = item
        return item

    def list_by_session(self, session_id: str) -> list[dict[str, Any]]:
        return [v for v in self._items.values() if v.get("session_id") == session_id]
