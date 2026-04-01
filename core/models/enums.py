from __future__ import annotations

from enum import Enum


class SessionStatus(str, Enum):
    NEW = "new"
    ACTIVE = "active"
    WAITING_REVIEW = "waiting_review"
    COMPLETED = "completed"
    FAILED = "failed"


class HypothesisStatus(str, Enum):
    NEW = "new"
    TESTING = "testing"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


class ObservationSource(str, Enum):
    GHIDRA = "ghidra"
    CE = "ce"
    PATCH_RUNTIME = "patch_runtime"
    USER = "user"


class PatchMethod(str, Enum):
    HOOK = "hook"
    BRANCH_PATCH = "branch_patch"
    CONST_PATCH = "const_patch"


class ReviewStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
