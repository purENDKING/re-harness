from __future__ import annotations

import asyncio
import contextlib
from typing import Any, AsyncGenerator

from mcp import ClientSession
from mcp.client.sse import sse_client

from core.config import get_settings


class ReVaClient:
    """
    真正的 ReVa MCP 客户端。
    负责维护底层的 SSE 连接并执行 JSON-RPC 工具调用。
    """

    def __init__(self, url: str | None = None) -> None:
        self.url = url or get_settings().reva_mcp_url

    @contextlib.asynccontextmanager
    async def _connect(self) -> AsyncGenerator[ClientSession, None]:
        """建立 SSE 连接并初始化 MCP Session"""
        async with sse_client(self.url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                yield session

    async def _ping_async(self) -> dict[str, Any]:
        """异步 ping：通过请求工具列表来测试连通性"""
        try:
            async with self._connect() as session:
                tools = await session.list_tools()
                return {"ok": True, "backend": "reva-mcp", "tools_count": len(tools.tools)}
        except Exception as e:
            return {"ok": False, "backend": "reva-mcp", "error": str(e)}

    async def _call_tool_async(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """异步执行 MCP 工具调用"""
        try:
            async with self._connect() as session:
                result = await session.call_tool(name=tool_name, arguments=arguments)

                # 提取 MCP 返回的文本内容
                content = [c.text for c in result.content if hasattr(c, "text")]
                return {"ok": True, "tool": tool_name, "content": content}
        except Exception as e:
            return {"ok": False, "tool": tool_name, "error": str(e)}

    # ==========================================
    # 暴露给 Adapter 层的同步 API
    # ==========================================

    def ping(self) -> dict[str, Any]:
        """同步 ping 测试（替代原来的 stub 方法）"""
        return asyncio.run(self._ping_async())

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        同步调用 ReVa 工具。
        Adapter 层将使用此方法调用反编译、获取交叉引用等具体功能。
        """
        return asyncio.run(self._call_tool_async(tool_name, arguments))