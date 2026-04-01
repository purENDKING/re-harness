from __future__ import annotations

from sqlalchemy.orm import Session

from core.models.session import Session as SessionModel
from storage.repositories import sessions as session_repo


def create_session(
    db: Session,
    sample_path: str,
    ghidra_project: str | None,
    target_process: str | None,
) -> SessionModel:
    """创建新的分析会话。

    Args:
        db: 数据库会话对象。
        sample_path: 样本文件路径。
        ghidra_project: Ghidra 项目路径（可选）。
        target_process: 目标进程名称（可选）。

    Returns:
        创建的 SessionModel 实例。
    """
    record = session_repo.create_session(db, sample_path, ghidra_project, target_process)
    return SessionModel.model_validate(record, from_attributes=True)


def get_session(db: Session, session_id: str) -> SessionModel | None:
    """根据 ID 获取会话信息。

    Args:
        db: 数据库会话对象。
        session_id: 会话唯一标识符。

    Returns:
        SessionModel 实例，若不存在则返回 None。
    """
    record = session_repo.get_session(db, session_id)
    if record is None:
        return None
    return SessionModel.model_validate(record, from_attributes=True)


def update_session_status(db: Session, session_id: str, status: str) -> SessionModel | None:
    """更新会话状态。

    Args:
        db: 数据库会话对象。
        session_id: 会话唯一标识符。
        status: 新状态值（如 "active"、"completed"、"error"）。

    Returns:
        更新后的 SessionModel 实例，若会话不存在则返回 None。
    """
    record = session_repo.update_status(db, session_id, status)
    if record is None:
        return None
    return SessionModel.model_validate(record, from_attributes=True)
