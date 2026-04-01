# RE-Harness

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-green.svg)](https://www.python.org/)

面向 **C++ D3D 游戏逆向** 场景的 RE / Runtime / Patch Workflow Harness 骨架工程。

> ⚠️ **安全声明**：本工程仅包含 stub/mock 适配器与占位模板，不提供真实的 DLL 注入、内存篡改或绕过实现。请在合法授权环境下使用。

## 核心工作流

```
选择 Target → 检查上下文 → 提出假设 → 收集证据 → 设计实验 → 审阅/回填
```

## 架构概览

| 层级 | 技术栈 | 职责 |
|------|--------|------|
| API | FastAPI | HTTP 路由、会话管理 |
| Orchestration | LangGraph | 状态机编排 |
| Service | Python | 业务逻辑、审阅流程 |
| Adapter | Python/C++ | 外部工具桥接 (stub) |
| Storage | SQLite + SQLAlchemy | 持久化 |

## 快速开始

### 环境准备

```bash
# 创建 conda 环境
conda env create -f environment.yml
conda activate re-harness

# 配置环境变量
cp .env.example .env
mkdir -p data
```

### 启动服务

```bash
# 启动 API
uvicorn apps.api.main:app --reload

# 运行测试
pytest

# Docker 部署
docker-compose up -d
```

API 文档：`http://127.0.0.1:8000/docs`

## 项目结构

```
re-harness/
├── apps/
│   ├── api/              # FastAPI 路由
│   └── worker/           # LangGraph 执行器
├── core/
│   ├── graph/            # 工作流状态与节点
│   ├── models/           # 领域模型
│   ├── services/         # 服务层
│   └── skills/           # LLM 技能模板
├── adapters/
│   ├── static_reva/      # Ghidra/ReVa 适配器
│   ├── dynamic_ce/       # Cheat Engine 适配器
│   └── patch_cpp/        # C++/MinHook 模板引擎
├── storage/              # 数据库与仓储
├── templates/minhook_dll/  # C++ DLL 模板
├── docs/                 # 详细文档
└── tests/                # 测试用例
```

## 功能状态

| 功能 | 状态 |
|------|------|
| Session 管理 | ✅ 已实现 |
| Research 工作流 | ✅ Mock 版本 |
| Review 审阅 | ✅ 已实现 |
| Ghidra/ReVa 适配器 | ✅ 已实现 |
| Cheat Engine 适配器 | 🔲 Stub |
| MinHook 模板 | 🔲 占位 |

## API 示例

```bash
# 创建会话
curl -X POST http://127.0.0.1:8000/sessions/start \
  -H "Content-Type: application/json" \
  -d '{"sample_path": "samples/game.exe"}'

# 查看审阅项
curl http://127.0.0.1:8000/review/{session_id}
```

更多 API 参考 [docs/api.md](docs/api.md)。

## License

[Apache 2.0](LICENSE)
