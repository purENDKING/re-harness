from __future__ import annotations

from fastapi import APIRouter, HTTPException

from apps.api.deps import DbSession
from core.models.enums import ReviewStatus
from core.services import review_service

router = APIRouter(prefix="/review", tags=["review"])


@router.get("/{session_id}")
def list_review_items(session_id: str, db: DbSession) -> list[dict]:
    return review_service.list_reviews(db, session_id)


@router.post("/{item_id}/approve")
def approve_review(item_id: str, db: DbSession) -> dict:
    item = review_service.update_review_status(db, item_id, ReviewStatus.APPROVED.value)
    if item is None:
        raise HTTPException(status_code=404, detail="review item not found")
    return item


@router.post("/{item_id}/reject")
def reject_review(item_id: str, db: DbSession) -> dict:
    item = review_service.update_review_status(db, item_id, ReviewStatus.REJECTED.value)
    if item is None:
        raise HTTPException(status_code=404, detail="review item not found")
    return item
