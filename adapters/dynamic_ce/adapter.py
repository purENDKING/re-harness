from __future__ import annotations

from typing import Protocol


class DynamicProbe(Protocol):
    def attach(self, process: str) -> dict: ...
    def read_memory(self, address: str, size: int) -> bytes: ...
    def write_memory(self, address: str, data: bytes) -> None: ...
    def scan_pattern(self, pattern: str) -> list[str]: ...
    def resolve_pointer_chain(self, base: str, offsets: list[int]) -> dict: ...
    def set_breakpoint(self, address: str) -> dict: ...


class StubDynamicProbe:
    def attach(self, process: str) -> dict:
        return {"ok": True, "process": process, "pid": 4242}

    def read_memory(self, address: str, size: int) -> bytes:
        return b"\x90" * min(size, 16)

    def write_memory(self, address: str, data: bytes) -> None:
        return None

    def scan_pattern(self, pattern: str) -> list[str]:
        return ["0x140200000", "0x140200080"]

    def resolve_pointer_chain(self, base: str, offsets: list[int]) -> dict:
        return {"base": base, "offsets": offsets, "resolved": "0x0000000140302010"}

    def set_breakpoint(self, address: str) -> dict:
        return {"ok": True, "address": address}
