from __future__ import annotations

from fastapi import FastAPI

from apps.api.routes import review, sessions, research
from core.logging import configure_logging
from storage.db import init_db


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="RE Harness",
        version="0.1.0",
        description="Stubbed RE / Runtime / Patch Workflow Harness",
    )

    @app.on_event("startup")
    def _startup() -> None:
        init_db()

    @app.get("/health")
    def health() -> dict:
        return {"ok": True}

    app.include_router(sessions.router)
            app.include_router(review.router)
        return app


app = create_app()

app.include_router(research.router)
