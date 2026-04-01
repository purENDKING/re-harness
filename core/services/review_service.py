from __future__ import annotations

from sqlalchemy.orm import Session

from storage.repositories import reviews as review_repo


def sync_reviews(db: Session, review_items: list[dict]) -> list[dict]:
    """同步保存 review 项列表到数据库。

    对每个 review 项执行 upsert 操作（存在则更新，不存在则创建）。

    Args:
        db: 数据库会话对象。
        review_items: 待同步的 review 项列表，每项为字典格式。

    Returns:
        已保存的 review 项列表，包含 id、session_id、item_type、target_ref、
        proposal、status 等字段。
    """
    saved = []
    for item in review_items:
        record = review_repo.upsert_review(db, item)
        saved.append(
            {
                "id": record.id,
                "session_id": record.session_id,
                "item_type": record.item_type,
                "target_ref": record.target_ref,
                "proposal": record.proposal,
                "status": record.status,
            }
        )
    return saved


def list_reviews(db: Session, session_id: str) -> list[dict]:
    """获取指定会话的所有 review 项。

    Args:
        db: 数据库会话对象。
        session_id: 会话唯一标识符。

    Returns:
        该会话下所有 review 项的列表，每项包含 id、session_id、item_type、
        target_ref、proposal、status 等字段。
    """
    return [
        {
            "id": item.id,
            "session_id": item.session_id,
            "item_type": item.item_type,
            "target_ref": item.target_ref,
            "proposal": item.proposal,
            "status": item.status,
        }
        for item in review_repo.list_by_session(db, session_id)
    ]


def update_review_status(db: Session, item_id: str, status: str) -> dict | None:
    """更新指定 review 项的状态。

    Args:
        db: 数据库会话对象。
        item_id: review 项的唯一标识符。
        status: 新状态值（如 "pending"、"approved"、"rejected"）。

    Returns:
        更新后的 review 项信息字典，若 review 项不存在则返回 None。
    """
    record = review_repo.update_status(db, item_id, status)
    if record is None:
        return None
    return {
        "id": record.id,
        "session_id": record.session_id,
        "item_type": record.item_type,
        "target_ref": record.target_ref,
        "proposal": record.proposal,
        "status": record.status,
    }
