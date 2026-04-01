from __future__ import annotations

import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field(default="dev", alias="APP_ENV")
    database_url: str = Field(default="sqlite:///./data/re_harness.db", alias="DATABASE_URL")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    reva_mcp_url: str = Field(default="http://127.0.0.1:49225/mcp/message", alias="REVA_MCP_URL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
