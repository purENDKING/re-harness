# RE Harness

一个面向 **C++ D3D 游戏逆向** 场景的 **RE / Runtime / Patch Workflow Harness** 骨架工程。

当前版本重点不是“全功能”，而是先打通一条**可运行的 mock workflow**：

**Ghidra 上下文 → static analyze → dynamic probe → patch prototype → review**

> 安全说明  
> 这个 skeleton 只包含 **stub/mock 适配器** 与 **占位模板**。不会提供真实的 DLL 注入、内存篡改、绕过或可直接投入使用的 hook 实现。后续你可以在合法授权环境下，将占位模块替换为你自己的实际集成。

## 项目简介

这个项目把几个分散的逆向实验动作串成一个有状态流程：

- 静态理解：从 Ghidra / ReVa 上下文进入
- 动态验证：用 Cheat Engine / MCP bridge 的占位 adapter 模拟验证
- Patch 原型：生成最小 C++ / MinHook 模板工程占位
- Review：把候选结论、观察和 patch 提案沉淀为可审阅项
- Writeback：把审阅通过的结果回填到静态分析上下文（当前为 mock）

## 架构图的文字说明

整体架构分成 5 层：

1. **API 层（FastAPI）**  
   提供 sessions、context、workflow、review 等 HTTP 路由。

2. **Graph / Orchestration 层（LangGraph）**  
   负责把输入上下文编排成一个可恢复的状态机流程。

3. **Domain / Service 层**  
   负责领域对象、服务逻辑、状态同步、审阅项生成和写回策略。

4. **Adapter 层**  
   对接 Ghidra/ReVa、Cheat Engine MCP bridge、C++ patch 模板引擎。  
   当前全部是 stub，可替换成真实实现。

5. **Storage 层（SQLite + SQLAlchemy）**  
   存储 sessions、observations、hypotheses、patch_candidates、reviews。

## 目录说明

- `apps/api/`：FastAPI 应用与路由
- `apps/worker/`：graph factory 和 runner
- `apps/cli/`：开发与 graph demo 命令
- `scripts/`：Windows PowerShell 开发脚本
- `core/graph/`：工作流 state、节点和边
- `core/models/`：领域模型
- `core/services/`：服务层
- `core/policies/`：模型路由、写回和证据策略占位
- `adapters/`：静态分析、动态探针、patch 生成适配器 stub
- `storage/`：数据库、ORM、schema 与仓储
- `templates/minhook_dll/`：C++/MinHook 模板占位
- `docs/`：架构、工作流、API 示例
- `tests/`：基础测试

## 本地运行

### 1. 使用 conda 创建环境

```bash
conda env create -f environment.yml
conda activate re-harness
```

如果你更新了依赖：

```bash
conda env update -f environment.yml --prune
```

说明：

- 当前项目默认以 `environment.yml` 作为开发环境入口
- `pyproject.toml` 仍然保留，主要用于 Docker 安装、包元数据和未来发布
- `langgraph` 目前通过 `pip` 段安装，因为它在 conda 生态里的可用性通常不如 PyPI 稳定

### 2. 配置环境变量

```bash
cp .env.example .env
mkdir -p data
```

### 3. 启动 API

```powershell
./scripts/dev.ps1
```

API 默认监听：`http://127.0.0.1:8000`

### 4. 跑一个 graph demo

```powershell
./scripts/run_graph.ps1
```

### 5. 运行测试

```powershell
./scripts/test.ps1
```


### 6. Windows 下的脚本入口

项目已不再依赖 `make`。常用命令如下：

- 启动 API：`./scripts/dev.ps1`
- 运行测试：`./scripts/test.ps1`
- 跑 graph demo：`./scripts/run_graph.ps1`
- 检查代码：`./scripts/lint.ps1`
- 启动 Docker：`./scripts/up.ps1`
- 停止 Docker：`./scripts/down.ps1`

如果 PowerShell 默认禁止脚本执行，可以在当前终端临时执行：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

## Docker 启动方法

当前 `docker-compose.yml` 只起一个 `api` 容器，原因是第一阶段目标是先把：

**Ghidra 上下文 → static analyze → dynamic probe → patch prototype → review**

这条主链打通，而不是先付出微服务编排成本。


```powershell
./scripts/up.ps1
```

访问：

- API: `http://127.0.0.1:8000`
- OpenAPI: `http://127.0.0.1:8000/docs`

停止容器：

```powershell
./scripts/down.ps1
```

## 关于是否要把 MCP / 数据库 / Worker 全拆成微服务

当前不建议一开始就全拆。更合适的节奏是：

### 现阶段为什么先保留单体 + adapter 边界

- workflow 还在快速变化，状态模型和节点职责还会频繁调整
- 真正复杂的是 RE 流程本身，不是服务间通信
- 现在就拆成多个服务，会过早引入：
  - 服务发现
  - 重试 / 超时 / 幂等
  - 分布式日志与 tracing
  - 多容器调试成本
  - 更复杂的本地开发体验

### 当前容器里在干什么

现在容器主要承担：

- 运行 FastAPI
- 通过挂载卷读写项目源码和 `data/` 下的 SQLite 文件
- 提供统一入口，方便后续逐步挂上真实 adapter

也就是说，它现在是一个 **开发用单体容器**，不是生产化部署拓扑。

### 什么时候值得拆

当下面任一条件出现时，再拆会更值：

- graph 执行要异步排队，需要独立 worker
- ReVa / Ghidra / CE bridge 本身就是单独进程或远端服务
- patch build 需要隔离的 Windows builder / sandbox
- SQLite 已经不够，要切 PostgreSQL
- 需要多个 analyst / session 并发

### 更合理的未来拆分方式

届时建议优先拆成这几个边界，而不是一开始全微服务化：

1. `api`：FastAPI，同步请求、审阅入口、状态查询
2. `worker`：LangGraph 执行器，异步跑 workflow
3. `postgres`：替换 SQLite
4. `reva-adapter`：静态分析桥接服务
5. `ce-bridge`：动态探针桥接服务
6. `patch-builder`：模板生成 / 编译 / 构建产物收集

这样拆的好处是边界和你的真实外部依赖一致。

## 当前已实现内容

- FastAPI 基础应用和健康检查
- Session 创建 / 查询
- Context push
- LangGraph 风格 mock workflow
- Static / dynamic / patch / review 节点 stub
- SQLite + SQLAlchemy 最小存储
- Review item 持久化和审批/拒绝
- MinHook DLL 模板目录占位
- Makefile、Dockerfile、compose、基础测试

## 下一步 TODO

- 接入真实 Ghidra / ReVa context adapter
- 接入 Cheat Engine MCP bridge
- 把 patch 生成与模板渲染做成可配置 skill
- 增加 artifact 管理与 patch build 产物索引
- 引入 PostgreSQL 和 Alembic
- 增加恢复执行、断点续跑、审阅回放
- 为高价值节点增加强模型路由，其他节点默认 cheap model

## 便宜 API 是否适合开发期

适合。当前阶段重点是：

- 跑通 workflow
- 验证 adapter 接口
- 固化状态流转
- 验证 CRUD / 审阅 / 模板生成

真正需要强模型的部分，通常只出现在：

- 复杂静态语义归纳
- patch 策略选择
- runtime → static 的高质量回填总结

所以项目里已经预留了 `core/policies/model_routing.py`，默认使用 cheap model，后续再按节点切换。
