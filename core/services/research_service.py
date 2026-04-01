from __future__ import annotations

from uuid import uuid4

from adapters.static_reva.adapter import get_static_analyzer
from core.models.claim import Claim
from core.models.evidence import Evidence
from core.models.target import TargetRef


class ResearchService:
    """围绕 target / claim / evidence 的最小研究服务。

    提供对二进制目标的静态分析能力，支持函数检查、声明提议和证据收集。
    """

    def __init__(self, use_real_analyzer: bool = False) -> None:
        """初始化研究服务。

        Args:
            use_real_analyzer: 是否使用真实的静态分析器。
                为 False 时使用模拟分析器，适用于测试场景。
        """
        self.analyzer = get_static_analyzer(use_real=use_real_analyzer)

    def inspect_function_target(self, session_id: str, address: str) -> dict:
        """检查函数目标，获取完整的上下文信息。

        对指定函数地址执行反编译、交叉引用分析和调用图生成，
        返回目标引用及相关上下文信息。

        Args:
            session_id: 会话唯一标识符。
            address: 函数地址（如 "0x401000"）。

        Returns:
            包含 target 和 context 的字典：
            - target: TargetRef 对象的序列化形式
            - context: 包含 decompile、xrefs、call_graph 的上下文信息
        """
        target = TargetRef(kind="function", ref=address, session_id=session_id)
        decomp = self.analyzer.decompile(address, include_callers=True, include_callees=True)
        xrefs = self.analyzer.list_xrefs(address, direction="both")
        call_graph = self.analyzer.get_call_graph(address, depth=1)
        return {
            "target": target.model_dump(),
            "context": {
                "decompile": decomp,
                "xrefs": xrefs,
                "call_graph": call_graph,
            },
        }

    def propose_claims_for_function(self, session_id: str, address: str) -> list[Claim]:
        """为函数目标生成可能的声明（claims）。

        基于静态分析结果，对函数行为提出可能的假设性声明，
        每个声明包含描述和置信度。

        Args:
            session_id: 会话唯一标识符。
            address: 函数地址。

        Returns:
            Claim 对象列表，每个声明包含：
            - statement: 对函数行为的假设描述
            - confidence: 置信度（0-1 范围）
        """
        decomp = self.analyzer.decompile(address)
        code = decomp.get("code", "")
        claims: list[Claim] = []
        if "0x10" in code or "+ 0x10" in code:
            claims.append(Claim(
                id=str(uuid4()),
                session_id=session_id,
                target={"kind": "function", "ref": address},
                statement="offset 0x10 may represent a frequently-read state-like field",
                confidence=0.45,
            ))
        claims.append(Claim(
            id=str(uuid4()),
            session_id=session_id,
            target={"kind": "function", "ref": address},
            statement="function likely acts as a small getter/helper around object state",
            confidence=0.35,
        ))
        return claims

    def collect_static_evidence_for_claim(self, session_id: str, address: str, claim_id: str) -> list[Evidence]:
        """为指定声明收集静态分析证据。

        通过反编译和交叉引用分析，收集支持或反驳该声明的证据。

        Args:
            session_id: 会话唯一标识符。
            address: 函数地址。
            claim_id: 声明的唯一标识符。

        Returns:
            Evidence 对象列表，每个证据包含：
            - source: 证据来源（如 "ghidra"）
            - summary: 证据摘要描述
            - payload: 原始分析数据
            - strength: 证据强度（0-1 范围）
        """
        decomp = self.analyzer.decompile(address)
        xrefs = self.analyzer.list_xrefs(address, direction="to")
        evidence: list[Evidence] = [
            Evidence(
                id=str(uuid4()),
                session_id=session_id,
                claim_id=claim_id,
                source="ghidra",
                source_ref=f"{address}:decompile",
                summary="decompilation suggests a narrow field access pattern",
                payload=decomp,
                strength=0.6,
            )
        ]
        if xrefs:
            evidence.append(Evidence(
                id=str(uuid4()),
                session_id=session_id,
                claim_id=claim_id,
                source="ghidra",
                source_ref=f"{address}:xrefs",
                summary=f"found {len(xrefs)} incoming references to the target function",
                payload={"xrefs": xrefs[:10]},
                strength=0.55,
            ))
        return evidence
