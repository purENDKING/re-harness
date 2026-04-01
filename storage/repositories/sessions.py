from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from core.models.enums import SessionStatus
from storage.models import SessionRecord


def create_session(
    db: Session,
    sample_path: str,
    ghidra_project: str | None,
    target_process: str | None,
) -> SessionRecord:
    now = datetime.now(timezone.utc)
    record = SessionRecord(
        id=uuid4().hex,
        sample_path=sample_path,
        ghidra_project=ghidra_project,
        target_process=target_process,
        status=SessionStatus.NEW.value,
        created_at=now,
        updated_at=now,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_session(db: Session, session_id: str) -> SessionRecord | None:
    return db.get(SessionRecord, session_id)


def update_status(db: Session, session_id: str, status: str) -> SessionRecord | None:
    record = get_session(db, session_id)
    if record is None:
        return None
    record.status = status
    record.updated_at = datetime.now(timezone.utc)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
