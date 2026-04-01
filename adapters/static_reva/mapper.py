"""
ReVa 响应映射器。

负责将 ReVa MCP 工具返回的原始数据结构映射为领域模型友好的格式。
设计原则：
- 隔离 ReVa 特有的响应格式，使 Adapter 层更清晰
- 提供一致的错误处理和默认值
- 保留原始数据以供调试
"""

from __future__ import annotations

import json
from typing import Any


# ========================================
# 基础工具函数
# ========================================


def _extract_content(result: dict[str, Any]) -> str:
    """从 MCP 工具响应中提取文本内容。"""
    if not result.get("ok"):
        return ""

    content = result.get("content", [])
    if isinstance(content, list) and content:
        # MCP 返回的是文本块列表
        return "\n".join(str(c) for c in content)
    return ""


def _parse_json_content(result: dict[str, Any]) -> dict[str, Any]:
    """尝试将 MCP 响应解析为 JSON。"""
    text = _extract_content(result)
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw_text": text}


# ========================================
# 上下文获取映射
# ========================================


def map_current_program(result: dict[str, Any]) -> dict[str, Any]:
    """
    映射 get-current-program 响应。
    Returns: { program_path, program_name, language, ... }
    """
    data = _parse_json_content(result)
    return {
        "program_path": data.get("programPath") or data.get("path") or "",
        "program_name": data.get("name") or "",
        "language": data.get("language") or data.get("languageId") or "",
        "image_base": data.get("imageBase") or "",
        "executable_path": data.get("executablePath") or "",
        "_raw": data,
    }


def map_decompilation(result: dict[str, Any]) -> dict[str, Any]:
    """
    映射 get-decompilation 响应。
    Returns: { address, name, signature, code, callers?, callees?, line_map? }
    """
    data = _parse_json_content(result)

    # 提取基础信息
    mapped = {
        "address": data.get("address") or "",
        "name": data.get("name") or data.get("functionName") or "",
        "signature": data.get("signature") or "",
        "code": data.get("decompiled") or data.get("code") or "",
        "_raw": data,
    }

    # 提取调用者/被调用者信息
    if "callers" in data:
        mapped["callers"] = [
            {
                "name": c.get("name") or "",
                "address": c.get("address") or "",
                "signature": c.get("signature") or "",
            }
            for c in data["callers"]
        ]

    if "callees" in data:
        mapped["callees"] = [
            {
                "name": c.get("name") or "",
                "address": c.get("address") or "",
                "signature": c.get("signature") or "",
            }
            for c in data["callees"]
        ]

    return mapped


def map_xrefs(result: dict[str, Any]) -> list[dict[str, Any]]:
    """
    映射 find-cross-references 响应。
    Returns: [{ from, to, type, address, context? }]
    """
    data = _parse_json_content(result)

    xrefs = []

    # 处理入引用 (to)
    for ref in data.get("referencesTo", []) or data.get("to", []) or []:
        xrefs.append({
            "from": ref.get("fromAddress") or ref.get("from") or "",
            "to": ref.get("toAddress") or ref.get("to") or "",
            "type": ref.get("type") or "unknown",
            "address": ref.get("fromAddress") or ref.get("address") or "",
            "context": ref.get("context") or "",
        })

    # 处理出引用 (from)
    for ref in data.get("referencesFrom", []) or data.get("from", []) or []:
        xrefs.append({
            "from": ref.get("fromAddress") or ref.get("from") or "",
            "to": ref.get("toAddress") or ref.get("to") or "",
            "type": ref.get("type") or "unknown",
            "address": ref.get("toAddress") or ref.get("address") or "",
            "context": ref.get("context") or "",
        })

    return xrefs


def map_call_graph(result: dict[str, Any]) -> dict[str, Any]:
    """
    映射 get-call-graph / get-call-tree 响应。
    Returns: { address, name, callers: [...], callees: [...] }
    """
    data = _parse_json_content(result)

    return {
        "address": data.get("address") or data.get("root") or "",
        "name": data.get("name") or data.get("functionName") or "",
        "callers": [
            {
                "name": c.get("name") or "",
                "address": c.get("address") or "",
            }
            for c in data.get("callers", []) or []
        ],
        "callees": [
            {
                "name": c.get("name") or "",
                "address": c.get("address") or "",
            }
            for c in data.get("callees", []) or data.get("children", []) or []
        ],
        "_raw": data,
    }


# ========================================
# 大范围搜证映射
# ========================================


def map_search_decomp(result: dict[str, Any]) -> list[dict[str, Any]]:
    """
    映射 search-decompilation 响应。
    Returns: [{ function_name, function_address, line_numbers, matches }]
    """
    data = _parse_json_content(result)

    results = []
    for item in data.get("results", []) or data.get("matches", []) or []:
        results.append({
            "function_name": item.get("functionName") or item.get("function") or "",
            "function_address": item.get("functionAddress") or item.get("address") or "",
            "line_numbers": item.get("lineNumbers") or item.get("lines") or [],
            "matches": item.get("matches") or [],
        })

    return results


def map_callers_decompiled(result: dict[str, Any]) -> list[dict[str, Any]]:
    """
    映射 get-callers-decompiled 响应。
    Returns: [{ function_name, address, decompile, call_site? }]
    """
    data = _parse_json_content(result)

    results = []
    for item in data.get("callers", []) or data.get("results", []) or []:
        caller = {
            "function_name": item.get("name") or item.get("functionName") or "",
            "address": item.get("address") or "",
            "decompile": item.get("decompiled") or item.get("code") or "",
        }

        # 提取调用点信息
        if "callSite" in item or "call_site" in item:
            cs = item.get("callSite") or item.get("call_site") or {}
            caller["call_site"] = {
                "line": cs.get("line") or 0,
                "address": cs.get("address") or "",
            }

        results.append(caller)

    return results


def map_constant_uses(result: dict[str, Any]) -> list[dict[str, Any]]:
    """
    映射 find-constant-uses 响应。
    Returns: [{ address, instruction, function? }]
    """
    data = _parse_json_content(result)

    results = []
    for item in data.get("results", []) or data.get("uses", []) or []:
        results.append({
            "address": item.get("address") or "",
            "instruction": item.get("instruction") or item.get("assembly") or "",
            "function": item.get("functionName") or item.get("function") or "",
        })

    return results


# ========================================
# 结构恢复映射
# ========================================


def map_structures_list(result: dict[str, Any]) -> list[dict[str, Any]]:
    """
    映射 list-structures 响应。
    Returns: [{ name, size, category }]
    """
    data = _parse_json_content(result)

    results = []
    for item in data.get("structures", []) or data.get("results", []) or []:
        results.append({
            "name": item.get("name") or "",
            "size": item.get("size") or item.get("length") or 0,
            "category": item.get("category") or "",
        })

    return results


def map_structure_info(result: dict[str, Any]) -> dict[str, Any]:
    """
    映射 get-structure-info 响应。
    Returns: { name, size, fields: [{ name, offset, type, size }] }
    """
    data = _parse_json_content(result)

    fields = []
    for f in data.get("fields", []) or data.get("components", []) or []:
        fields.append({
            "name": f.get("fieldName") or f.get("name") or "",
            "offset": f.get("offset") or 0,
            "type": f.get("dataType") or f.get("type") or "",
            "size": f.get("length") or f.get("size") or 0,
        })

    return {
        "name": data.get("name") or "",
        "size": data.get("size") or data.get("length") or 0,
        "fields": fields,
        "_raw": data,
    }


# ========================================
# 操作结果映射
# ========================================


def map_operation_result(result: dict[str, Any]) -> dict[str, Any]:
    """
    映射通用操作结果（如 rename, set_comment 等）。
    Returns: { success, message, error? }
    """
    if not result.get("ok"):
        return {
            "success": False,
            "error": result.get("error") or "Unknown error",
        }

    data = _parse_json_content(result)
    return {
        "success": data.get("success", True),
        "message": data.get("message") or data.get("result") or "",
    }
