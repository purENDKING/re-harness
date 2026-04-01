from __future__ import annotations

from typing import Literal
from pydantic import BaseModel


class TargetRef(BaseModel):
    kind: Literal["function", "field", "structure", "global", "branch", "opcode"]
    ref: str
    session_id: str
    parent_ref: str | None = None
