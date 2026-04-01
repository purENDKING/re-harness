from __future__ import annotations

import asyncio
import contextlib
import traceback
from typing import Any, AsyncGenerator

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from core.config import get_settings


class ReVaClientError(RuntimeError):
    pass


class ReVaToolError(ReVaClientError):
    def __init__(
            self,
            tool_name: str,
            arguments: dict[str, Any],
            message: str,
            *,
            cause: BaseException | None = None,
    ) -> None:
        super().__init__(f"[{tool_name}] {message}")
        self.tool_name = tool_name
        self.arguments = arguments
        if cause is not None:
            self.__cause__ = cause


def _flatten_exception_group(exc: BaseException) -> list[BaseException]:
    if hasattr(exc, "exceptions"):
        flat: list[BaseException] = []
        for sub in exc.exceptions:  # type: ignore[attr-defined]
            flat.extend(_flatten_exception_group(sub))
        return flat
    return [exc]


def _format_exception_details(exc: BaseException) -> str:
    errors = _flatten_exception_group(exc)
    return "\n\n".join(
        "".join(traceback.format_exception(type(e), e, e.__traceback__))
        for e in errors
    )


class ReVaClient:
    def __init__(self, url: str | None = None) -> None:
        self.url = url or get_settings().reva_mcp_url

    @contextlib.asynccontextmanager
    async def _connect(self) -> AsyncGenerator[ClientSession, None]:
        async with streamable_http_client(self.url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                yield session

    async def _ping_async(self) -> dict[str, Any]:
        async with self._connect() as session:
            tools = await session.list_tools()
            import json
            return {
                "ok": True,
                "backend": "reva-mcp",
                "tools_count": len(tools.tools),
                "tools": tools.tools
            }

    async def _call_tool_async(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        async with self._connect() as session:
            result = await session.call_tool(name=tool_name, arguments=arguments)
            content = [c.text for c in result.content if hasattr(c, "text")]
            return {
                "ok": True,
                "tool": tool_name,
                "content": content,
            }

    def ping(self) -> dict[str, Any]:
        try:
            return asyncio.run(self._ping_async())
        except BaseException as e:
            details = _format_exception_details(e)
            raise ReVaClientError(f"Ping failed:\n{details}") from e

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        try:
            return asyncio.run(self._call_tool_async(tool_name, arguments))
        except BaseException as e:
            details = _format_exception_details(e)
            raise ReVaToolError(
                tool_name,
                arguments,
                details,
                cause=e,
            ) from e
