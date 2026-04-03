from __future__ import annotations

from typing import Protocol, runtime_checkable


class StaticAnalyzer(Protocol):
    """
    静态分析器协议 - 定义逆向工程工作流所需的稳定领域接口。

    设计原则：
    - 不直接暴露 ReVa 的 67 个工具，而是收束为少数高价值方法
    - 方法签名以"研究动作"为中心，而非工具原始形态
    - 支持静态分析最小闭环：ingest_context -> static_analyze -> commit_back
    """

    # ========================================
    # 发现 / 目录能力
    # ========================================

    def list_functions(
            self,
            *,
            start_index: int = 0,
            max_count: int = 100,
            filter_default_names: bool = True,
    ) -> list[dict]:
        ...

    def get_function_count(
            self,
            *,
            filter_default_name: bool = True
    ) -> int:
        ...


    def list_structures(
            self,
            *,
            name_filter: str | None = None,
            max_count: int = 100,
    ) -> list[dict]:
        """
        列出结构体目录。
        """

    def get_structure(self, name: str) -> dict:
        """
        获取结构体详情。
        """

    # ========================================
    # 上下文获取
    # ========================================

    def get_current_context(self) -> dict:
        """
        获取当前 Ghidra 上下文。
        Returns: { program_path, current_function_addr, current_selection, ... }
        """
        ...

    def decompile(
        self,
        address: str,
        *,
        offset: int = 1,
        limit: int = 50,
        include_callers: bool = False,
        include_callees: bool = False,
    ) -> dict:
        """
        反编译指定地址的函数。
        Args:
            address: 函数地址或符号名
            offset: 起始行号 (1-based)
            limit: 返回行数
            include_callers: 是否包含调用者列表
            include_callees: 是否包含被调用函数列表
        Returns: { address, name, signature, code, callers?, callees? }
        """
        ...

    def list_xrefs(
        self,
        address: str,
        *,
        direction: str = "both",
        include_data: bool = True,
        include_flow: bool = True,
        limit: int = 100,
    ) -> list[dict]:
        """
        获取交叉引用。
        Args:
            address: 目标地址或符号名
            direction: "to" (入引用), "from" (出引用), "both"
            include_data: 是否包含数据引用
            include_flow: 是否包含控制流引用 (call/jump)
            limit: 最大返回数量
        Returns: [{ from, to, type, address, context? }]
        """
        ...

    def get_call_graph(self, address: str, *, depth: int = 1) -> dict:
        """
        获取调用图。
        Args:
            address: 函数地址或符号名
            depth: 遍历深度 (1-10)
        Returns: { address, name, callers: [...], callees: [...] }
        """
        ...

    # ========================================
    # 大范围搜证
    # ========================================

    def search_decomp(
        self,
        pattern: str,
        *,
        case_sensitive: bool = False,
        max_results: int = 50,
    ) -> list[dict]:
        """
        在所有函数的反编译代码中搜索模式。
        Args:
            pattern: 正则表达式模式
            case_sensitive: 是否区分大小写
            max_results: 最大返回数量
        Returns: [{ function_name, function_address, line_numbers, matches }]
        """
        ...

    def get_callers_decompiled(
        self,
        address: str,
        *,
        max_callers: int = 10,
        include_context: bool = True,
    ) -> list[dict]:
        """
        获取调用某函数的所有函数及其反编译代码。
        Args:
            address: 目标函数地址
            max_callers: 最大返回数量
            include_context: 是否高亮调用点
        Returns: [{ function_name, address, decompile, call_site? }]
        """
        ...

    def find_constant_uses(
        self,
        value: str,
        *,
        max_results: int = 100,
    ) -> list[dict]:
        """
        查找常量值的使用位置。
        Args:
            value: 常量值 (支持十进制、十六进制 0x 前缀)
            max_results: 最大返回数量
        Returns: [{ address, instruction, function? }]
        """
        ...

    # ========================================
    # 语义整理 (回填)
    # ========================================

    def rename_symbol(self, address: str, new_name: str) -> None:
        """在指定地址创建或更新标签/符号名。"""
        ...

    def rename_variable(self, function: str, old_name: str, new_name: str) -> None:
        """重命名函数内的变量。"""
        ...

    def set_comment(
        self,
        address: str,
        comment: str,
        *,
        comment_type: str = "eol",
    ) -> None:
        """
        设置注释。
        Args:
            address: 目标地址或符号名
            comment: 注释内容
            comment_type: "pre", "eol", "plate", "post", "repeatable"
        """
        ...

    def set_function_prototype(self, address: str, signature: str) -> None:
        """
        设置函数原型。
        Args:
            address: 函数地址
            signature: C 风格函数签名，如 "int main(int argc, char** argv)"
        """
        ...

    # ========================================
    # 结构恢复
    # ========================================

    def list_structures(
        self,
        *,
        name_filter: str | None = None,
        max_count: int = 100,
    ) -> list[dict]:
        """
        列出程序中定义的结构体。
        Returns: [{ name, size, category }]
        """
        ...

    def get_structure(self, name: str) -> dict:
        """
        获取结构体详情。
        Returns: { name, size, fields: [{ name, offset, type, size }] }
        """
        ...

    def define_structure(self, c_definition: str, *, category: str = "/") -> None:
        """
        从 C 定义创建或更新结构体。
        Args:
            c_definition: C 风格结构体定义
            category: 分类路径
        """
        ...

    def apply_structure(self, address: str, structure_name: str) -> None:
        """在指定地址应用结构体。"""
        ...


class StubStaticAnalyzer:
    """用于测试和开发的静态分析器桩实现。"""

    def get_current_context(self) -> dict:
        return {
            "program_path": "/Hatchery.exe",
            "current_function_addr": "0x140001000",
            "current_selection": "player->inventory",
            "current_decompile": "int __fastcall sub_140001000(Player *player) { return player->hp; }",
        }

    def decompile(
        self,
        address: str,
        *,
        offset: int = 1,
        limit: int = 50,
        include_callers: bool = False,
        include_callees: bool = False,
    ) -> dict:
        result = {
            "address": address,
            "name": f"sub_{address.replace('0x', '')}",
            "signature": f"int __fastcall sub_{address.replace('0x', '')}(void* ctx)",
            "code": f"int __fastcall sub_{address.replace('0x', '')}(void* ctx) {{ return *(int*)((char*)ctx + 0x10); }}",
        }
        if include_callers:
            result["callers"] = [{"name": "caller_func", "address": "0x1400008F0"}]
        if include_callees:
            result["callees"] = [{"name": "callee_func", "address": "0x140002000"}]
        return result

    def list_xrefs(
        self,
        address: str,
        *,
        direction: str = "both",
        include_data: bool = True,
        include_flow: bool = True,
        limit: int = 100,
    ) -> list[dict]:
        return [
            {"from": "0x1400008F0", "to": address, "type": "call", "address": "0x1400008F5"},
            {"from": "0x140010A20", "to": address, "type": "call", "address": "0x140010A25"},
        ]

    def get_call_graph(self, address: str, *, depth: int = 1) -> dict:
        return {
            "address": address,
            "name": f"sub_{address.replace('0x', '')}",
            "callers": [{"name": "parent_func", "address": "0x140000800"}],
            "callees": [{"name": "child_func", "address": "0x140002000"}],
        }

    def search_decomp(
        self,
        pattern: str,
        *,
        case_sensitive: bool = False,
        max_results: int = 50,
    ) -> list[dict]:
        return [
            {"function_name": "func_1", "function_address": "0x140001000", "line_numbers": [5, 12]},
        ]

    def get_callers_decompiled(
        self,
        address: str,
        *,
        max_callers: int = 10,
        include_context: bool = True,
    ) -> list[dict]:
        return [
            {
                "function_name": "caller_func",
                "address": "0x1400008F0",
                "decompile": "void caller_func() { sub_140001000(); }",
                "call_site": {"line": 1, "address": "0x1400008F5"},
            }
        ]

    def find_constant_uses(
        self,
        value: str,
        *,
        max_results: int = 100,
    ) -> list[dict]:
        return [
            {"address": "0x14000100A", "instruction": "mov eax, 0x42", "function": "func_1"},
        ]

    def rename_symbol(self, address: str, new_name: str) -> None:
        return None

    def rename_variable(self, function: str, old_name: str, new_name: str) -> None:
        return None

    def set_comment(
        self,
        address: str,
        comment: str,
        *,
        comment_type: str = "eol",
    ) -> None:
        return None

    def set_function_prototype(self, address: str, signature: str) -> None:
        return None

    def list_structures(
        self,
        *,
        name_filter: str | None = None,
        max_count: int = 100,
    ) -> list[dict]:
        return [
            {"name": "Player", "size": 64, "category": "/"},
            {"name": "Inventory", "size": 128, "category": "/"},
        ]

    def get_structure(self, name: str) -> dict:
        return {
            "name": name,
            "size": 64,
            "fields": [
                {"name": "hp", "offset": 0, "type": "int", "size": 4},
                {"name": "mp", "offset": 4, "type": "int", "size": 4},
            ],
        }

    def define_structure(self, c_definition: str, *, category: str = "/") -> None:
        return None

    def apply_structure(self, address: str, structure_name: str) -> None:
        return None


class ReVaStaticAdapter:
    """
    ReVa 静态分析适配器。

    将 StaticAnalyzer Protocol 映射到 ReVa MCP 工具调用。
    设计原则：
    - 一个方法可能调用多个 ReVa 工具（如 get_current_context 需要先获取 programPath）
    - 使用 mapper 层处理响应格式差异
    - 保持方法签名与 Protocol 一致
    """

    def __init__(self, client) -> None:
        """
        初始化适配器。

        Args:
            client: ReVaClient 实例，用于执行 MCP 工具调用
        """
        self._client = client
        self._program_path: str | None = None

    def _get_program_path(self) -> str:
        """获取当前程序路径，用于后续工具调用。"""
        if self._program_path:
            return self._program_path

        result = self._client.call_tool("get-current-program", {})
        from adapters.static_reva.mapper import map_current_program

        ctx = map_current_program(result)
        self._program_path = ctx.get("program_path", "")
        return self._program_path

    # ========================================
    # 上下文获取
    # ========================================

    def get_current_context(self) -> dict:
        """获取当前 Ghidra 上下文。"""
        from adapters.static_reva.mapper import map_current_program

        result = self._client.call_tool("get-current-program", {})
        print(result)
        ctx = map_current_program(result)

        # 缓存 program_path
        if ctx.get("program_path"):
            self._program_path = ctx["program_path"]

        return ctx

    def decompile(
        self,
        address: str,
        *,
        offset: int = 1,
        limit: int = 50,
        include_callers: bool = False,
        include_callees: bool = False,
    ) -> dict:
        """反编译指定地址的函数。"""
        from adapters.static_reva.mapper import map_decompilation

        program_path = self._get_program_path()

        result = self._client.call_tool(
            "get-decompilation",
            {
                "programPath": program_path,
                "functionNameOrAddress": address,
                "offset": offset,
                "limit": limit,
                "includeCallers": include_callers,
                "includeCallees": include_callees,
            },
        )

        return map_decompilation(result)

    def list_xrefs(
        self,
        address: str,
        *,
        direction: str = "both",
        include_data: bool = True,
        include_flow: bool = True,
        limit: int = 100,
    ) -> list[dict]:
        """获取交叉引用。"""
        from adapters.static_reva.mapper import map_xrefs

        program_path = self._get_program_path()

        result = self._client.call_tool(
            "find-cross-references",
            {
                "programPath": program_path,
                "location": address,
                "direction": direction,
                "includeData": include_data,
                "includeFlow": include_flow,
                "limit": limit,
            },
        )

        return map_xrefs(result)

    def get_call_graph(self, address: str, *, depth: int = 1) -> dict:
        """获取调用图。"""
        from adapters.static_reva.mapper import map_call_graph

        program_path = self._get_program_path()

        result = self._client.call_tool(
            "get-call-graph",
            {
                "programPath": program_path,
                "functionAddress": address,
                "depth": min(depth, 10),  # ReVa 限制最大深度为 10
            },
        )

        return map_call_graph(result)

    # ========================================
    # 大范围搜证
    # ========================================

    def search_decomp(
        self,
        pattern: str,
        *,
        case_sensitive: bool = False,
        max_results: int = 50,
    ) -> list[dict]:
        """在所有函数的反编译代码中搜索模式。"""
        from adapters.static_reva.mapper import map_search_decomp

        program_path = self._get_program_path()

        result = self._client.call_tool(
            "search-decompilation",
            {
                "programPath": program_path,
                "pattern": pattern,
                "caseSensitive": case_sensitive,
                "maxResults": max_results,
            },
        )

        return map_search_decomp(result)

    def get_callers_decompiled(
        self,
        address: str,
        *,
        max_callers: int = 10,
        include_context: bool = True,
    ) -> list[dict]:
        """获取调用某函数的所有函数及其反编译代码。"""
        from adapters.static_reva.mapper import map_callers_decompiled

        program_path = self._get_program_path()

        result = self._client.call_tool(
            "get-callers-decompiled",
            {
                "programPath": program_path,
                "functionNameOrAddress": address,
                "maxCallers": max_callers,
                "includeCallContext": include_context,
            },
        )

        return map_callers_decompiled(result)

    def find_constant_uses(
        self,
        value: str,
        *,
        max_results: int = 100,
    ) -> list[dict]:
        """查找常量值的使用位置。"""
        from adapters.static_reva.mapper import map_constant_uses

        program_path = self._get_program_path()

        result = self._client.call_tool(
            "find-constant-uses",
            {
                "programPath": program_path,
                "value": value,
                "maxResults": max_results,
            },
        )

        return map_constant_uses(result)

    # ========================================
    # 语义整理 (回填)
    # ========================================

    def rename_symbol(self, address: str, new_name: str) -> None:
        """在指定地址创建或更新标签。"""
        program_path = self._get_program_path()

        self._client.call_tool(
            "create-label",
            {
                "programPath": program_path,
                "addressOrSymbol": address,
                "labelName": new_name,
                "setAsPrimary": True,
            },
        )

    def rename_variable(self, function: str, old_name: str, new_name: str) -> None:
        """重命名函数内的变量。"""
        program_path = self._get_program_path()

        self._client.call_tool(
            "rename-variables",
            {
                "programPath": program_path,
                "functionNameOrAddress": function,
                "variableMappings": {old_name: new_name},
            },
        )

    def set_comment(
        self,
        address: str,
        comment: str,
        *,
        comment_type: str = "eol",
    ) -> None:
        """设置注释。"""
        program_path = self._get_program_path()

        self._client.call_tool(
            "set-comment",
            {
                "programPath": program_path,
                "addressOrSymbol": address,
                "comment": comment,
                "commentType": comment_type,
            },
        )

    def set_function_prototype(self, address: str, signature: str) -> None:
        """设置函数原型。"""
        program_path = self._get_program_path()

        self._client.call_tool(
            "set-function-prototype",
            {
                "programPath": program_path,
                "location": address,
                "signature": signature,
                "createIfNotExists": False,
            },
        )

    # ========================================
    # 结构恢复
    # ========================================

    def list_structures(
        self,
        *,
        name_filter: str | None = None,
        max_count: int = 100,
    ) -> list[dict]:
        """列出程序中定义的结构体。"""
        from adapters.static_reva.mapper import map_structures_list

        program_path = self._get_program_path()

        args = {
            "programPath": program_path,
            "maxCount": max_count,
        }
        if name_filter:
            args["nameFilter"] = name_filter

        result = self._client.call_tool("list-structures", args)
        return map_structures_list(result)

    def get_structure(self, name: str) -> dict:
        """获取结构体详情。"""
        from adapters.static_reva.mapper import map_structure_info

        program_path = self._get_program_path()

        result = self._client.call_tool(
            "get-structure-info",
            {
                "programPath": program_path,
                "structureName": name,
            },
        )

        return map_structure_info(result)

    def define_structure(self, c_definition: str, *, category: str = "/") -> None:
        """从 C 定义创建或更新结构体。"""
        program_path = self._get_program_path()

        self._client.call_tool(
            "parse-c-structure",
            {
                "programPath": program_path,
                "cDefinition": c_definition,
                "category": category,
            },
        )

    def apply_structure(self, address: str, structure_name: str) -> None:
        """在指定地址应用结构体。"""
        program_path = self._get_program_path()

        self._client.call_tool(
            "apply-structure",
            {
                "programPath": program_path,
                "structureName": structure_name,
                "addressOrSymbol": address,
            },
        )


# ========================================
# 工厂函数
# ========================================

_analyzer_instance: StaticAnalyzer | None = None


def get_static_analyzer(use_real: bool = False) -> StaticAnalyzer:
    """
    获取静态分析器实例。

    Args:
        use_real: 如果为 True，尝试连接真正的 ReVa 服务；
                  如果为 False，返回 Stub 实现（用于开发/测试）

    Returns:
        StaticAnalyzer 实例
    """
    global _analyzer_instance

    if _analyzer_instance is not None:
        return _analyzer_instance

    if use_real:
        from adapters.static_reva.client import ReVaClient

        client = ReVaClient()
        _analyzer_instance = ReVaStaticAdapter(client)
    else:
        _analyzer_instance = StubStaticAnalyzer()

    return _analyzer_instance


def set_static_analyzer(analyzer: StaticAnalyzer) -> None:
    """
    设置全局静态分析器实例（用于依赖注入）。

    Args:
        analyzer: StaticAnalyzer 实例
    """
    global _analyzer_instance
    _analyzer_instance = analyzer
