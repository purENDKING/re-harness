from __future__ import annotations

from sqlalchemy.orm import Session

from storage.models import ReviewRecord


def upsert_review(db: Session, payload: dict) -> ReviewRecord:
    record = db.get(ReviewRecord, payload["id"])
    if record is None:
        record = ReviewRecord(id=payload["id"])
    record.session_id = payload["session_id"]
    record.item_type = payload["item_type"]
    record.target_ref = payload["target_ref"]
    record.proposal = payload.get("proposal", {})
    record.status = payload["status"]
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_review(db: Session, item_id: str) -> ReviewRecord | None:
    return db.get(ReviewRecord, item_id)


def list_by_session(db: Session, session_id: str) -> list[ReviewRecord]:
    return list(db.query(ReviewRecord).filter(ReviewRecord.session_id == session_id).all())


def update_status(db: Session, item_id: str, status: str) -> ReviewRecord | None:
    record = get_review(db, item_id)
    if record is None:
        return None
    record.status = status
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
