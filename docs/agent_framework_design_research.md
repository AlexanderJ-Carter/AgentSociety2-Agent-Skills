# Agent Framework Design Research

这份文档整理主流 agent 框架在技能、上下文、记忆、状态、日志和可观测性方面的设计，并给出适合 `PersonAgent` 的落地方案。

## 总体原则

`PersonAgent` 应该是通用运行框架，而不是某几个技能的硬编码容器。

框架只应该理解这些通用概念：

- 技能目录：`skills/<name>/SKILL.md`
- 状态文件：`state/*.json`
- 事件流：`state/*.jsonl`
- 工作区入口：`AGENT.md`
- 工具调用日志：`.runtime/logs/tool_calls.jsonl`
- 线程消息：`.runtime/logs/thread_messages.jsonl`
- 行为 trace：`.runtime/logs/behavior_trace.jsonl`
- checkpoint / replay / recovery

框架不应该理解具体技能字段，例如经济技能的 `cash`、生理技能的 `hunger_pressure`、关系技能的 `trust`。这些字段属于技能自己的语义。

## 可借鉴方案

### Claude / Cursor

可借鉴点：

- `CLAUDE.md` / Rules 是常驻短上下文，只放项目级规则和入口信息。
- Skills 是按需加载的能力包，`SKILL.md` 的 `name` 和 `description` 用于发现，正文用于执行。
- 长材料不要常驻上下文，放到 `references/` 按需读取。
- 确定性计算放到 `scripts/`，不要依赖模型每次手算。
- 文件引用要靠路径和目录约定，避免把所有文档塞进 prompt。

适配到 `PersonAgent`：

- 使用单一 `AGENT.md` 作为 workspace 入口。
- `AGENT.md` 保持短，包含当前上下文和文件索引。
- 技能默认只用 `name + description`。
- 自定义技能用 `_meta`、`_summary` 自描述状态文件。

### LangGraph

可借鉴点：

- 区分 thread-level state 和 cross-thread memory。
- 每个运行线程都有 checkpoint，可恢复、可回放、可 time travel。
- 人类介入通常通过 interrupt 暂停，然后用同一 thread id 恢复。
- 长期记忆应和当前线程状态分离。

适配到 `PersonAgent`：

- `logs/thread_messages.jsonl` 是线程级对话历史。
- `state/*.json` 是当前线程状态。
- `state/*.jsonl` 是当前 agent 的事件流。
- `memory/` 或外部 memory store 承担跨线程长期记忆。
- checkpoint 中保留 `state/*.json`、已激活技能、step 计数和必要恢复点。

### OpenAI Agents SDK

可借鉴点：

- tracing 是一等公民：一个 run 是 trace，每个 LLM 调用、tool call、handoff、guardrail 是 span。
- guardrail 用于输入、输出、工具调用前后校验。
- handoff 是显式事件，不只是普通文本。
- session 用于持久化会话状态。

适配到 `PersonAgent`：

- `logs/behavior_trace.jsonl` 应记录结构化 trace event。
- 每个 step 应有 `trace_id`，每个工具调用应有 `span_id`。
- 重要事件类型建议统一：
  - `step_start`
  - `skill_activate`
  - `tool_call`
  - `workspace_write`
  - `state_sync`
  - `plan_interrupt`
  - `guardrail_block`
  - `step_end`
- 如果未来有多 agent 或多角色协作，handoff 应作为单独事件类型记录。

### LangSmith / AutoGen / AgentOps

可借鉴点：

- 可观测性不是普通日志，而是结构化 trace。
- trace 需要保留输入、输出、耗时、错误、token、工具参数摘要、状态变化。
- 多 agent 系统尤其需要记录 handoff、共享状态变更、循环和失败原因。
- OpenTelemetry 风格有利于后续接入外部 dashboard。

适配到 `PersonAgent`：

- 当前 `tool_calls.jsonl` 和 `behavior_trace.jsonl` 可以继续保留。
- 建议新增统一 trace schema，让日志可以被外部系统读取。
- 避免把完整大文件或隐私内容写进 trace，只写摘要和路径。

## 推荐设计

### 1. 技能发现

技能目录：

```text
skills/<skill_name>/SKILL.md
skills/<skill_name>/references/
skills/<skill_name>/scripts/
skills/<skill_name>/assets/
```

框架发现规则：

- 只要求 `SKILL.md` 存在。
- frontmatter 默认只解析 `name`、`description`。
- 其他字段可以兼容，但不是标准依赖。
- 技能正文按需激活。

### 2. 状态文件自描述

任何技能写出的 JSON 都推荐带：

```json
{
  "_meta": {
    "skill": "economy",
    "purpose": "Material resources and affordability constraints."
  },
  "_summary": "Budget stress is moderate.",
  "data": {}
}
```

框架只理解：

- `_meta.skill`
- `_meta.purpose`
- `_meta.description`
- `_summary`
- `summary`

其他字段不解释、不 hardcode。

### 3. AGENT.md

`AGENT.md` 是 workspace 入口，类似 Claude 的 `CLAUDE.md`，但面向仿真 agent。

推荐结构：

```markdown
---
current_task: "..."
active_goal: "..."
state_summary:
  economy: "Budget stress is moderate."
state_purpose:
  economy: "Material resources and affordability constraints."
state_files:
  - state/economy.json
last_sync: "..."
---

# Agent Notes

短备注。

<!-- AGENT_FILE_INDEX_START -->
# Workspace Files
...
<!-- AGENT_FILE_INDEX_END -->
```

规则：

- 标记区块由 runtime 维护。
- 标记区块外可由人工或 agent 写备注。
- 不把长日志塞进 `AGENT.md`。
- 不把具体技能逻辑写进 runtime。

### 4. 日志和 Trace

建议区分三层：

`logs/thread_messages.jsonl`
实际路径：`.runtime/logs/thread_messages.jsonl`

- 保存喂给 LLM 的 user/assistant 消息。
- 用于上下文恢复和压缩。

`logs/tool_calls.jsonl`
实际路径：`.runtime/logs/tool_calls.jsonl`

- 保存工具调用事实。
- 适合调试单步工具行为。

`logs/behavior_trace.jsonl`
实际路径：`.runtime/logs/behavior_trace.jsonl`

- 保存结构化行为事件。
- 适合观测 agent 行为、统计技能使用、回放关键事件。

推荐 trace event：

```json
{
  "trace_id": "agent_0001_tick_120",
  "span_id": "tool_3",
  "parent_span_id": "step",
  "timestamp": "2026-04-27T03:30:00Z",
  "agent_id": 1,
  "tick": 120,
  "event_type": "tool_call",
  "name": "workspace_write",
  "input_summary": {
    "path": "state/economy.json"
  },
  "output_summary": {
    "ok": true
  },
  "error": null,
  "duration_ms": 12
}
```

### 5. 记忆分层

建议区分：

- 工作上下文：当前 LLM thread 和当前 step。
- 当前状态：`state/*.json`。
- 当前事件流：`state/*.jsonl`。
- 长期记忆：`memory/` 或外部 memory store。
- 反思结果：`state/reflections.jsonl`、`state/beliefs.json`、`state/preferences.json`。

这样可以避免所有东西都写进一个 `memory.jsonl`。

### 6. Guardrail

建议框架级 guardrail 只处理通用风险：

- 路径越界。
- 未知工具。
- 重复循环。
- 过大文件读取。
- 危险 bash。
- 结构化 JSON 写入失败。

技能级 guardrail 由技能自己定义，例如经济技能检查金额不能为负，生理技能检查值在 `[0, 1]`。

### 7. 权限模式和安全边界

借鉴 Codex 的 approval modes，`PersonAgent` 可以把权限分成几类：

- `read_only`：只能读取 workspace 和 skill，不能写文件、执行环境动作或 bash。
- `auto`：允许在 agent workspace 内读写和执行低风险工具，危险操作需要环境或上层策略阻止。
- `full_access`：用于受控实验或调试，允许更大范围工具能力。

当前代码已有这些基础：

- workspace 路径越界保护。
- bash 安全检查。
- skill `allowed_tools` 作用域。
- 环境模块的 step constraints。
- 循环检测。

后续可以把这些能力统一成一个 `PermissionPolicy`，而不是散落在工具分支里。

### 8. 内置技能适配边界

四个基础技能可以被框架轻微适配：

- `observation`：世界输入入口。
- `cognition`：情绪和意图入口。
- `plan`：执行入口。
- `memory`：长期记忆入口。

但这种适配只应该发生在框架流程层面，不应该扩展成“runtime 知道某个状态字段是什么意思”。

可以接受：

- 默认 prompt 提醒 agent 优先使用 `observation -> cognition -> plan -> memory`。
- checkpoint 默认保存它们的状态文件。
- `AGENT.md` 可以显示它们的文件名。

不应该接受：

- runtime 硬编码 `hunger_pressure`、`trust`、`cash` 这类扩展字段。
- `PersonAgent` 为每个新技能写 if/else。

### 9. 观测性标准

借鉴 OpenAI Agents SDK 和 LangSmith，行为日志应优先使用 trace/span，而不是只写普通日志文本。

当前推荐事件：

- `step_start`
- `tool_call`
- `tool_result`
- `skill_activate`
- `state_sync`
- `step_end`

每条事件都应尽量包含：

- `trace_id`
- `span_id`
- `parent_span_id`
- `name`
- `input_summary`
- `output_summary`
- `error`
- `duration_ms`

trace 中不要写大文件内容、完整 prompt 或隐私字段，只写摘要和路径。

## 后续可做

1. 给技能脚本约定统一输入输出：读取 `AGENT_WORK_DIR`，写 `state/*.json`。
2. 给 `state/*.json` 增加 `_meta/_summary` 示例。
3. 把长期记忆统一到一个清晰位置，避免 `state/memory.jsonl`、`memory/memory.jsonl`、`memory.jsonl` 混用。
4. 增加一个 `validate_state.py` 工具，用来检查自描述状态文件是否符合约定。

## 已落地的框架升级

当前已经落地：

- `AGENT.md` 作为统一入口，替代分散的上下文和文件索引。
- 文件索引写入 `AGENT.md` 的自动生成区块，保留人工备注。
- checkpoint、WAL、thread 历史和 trace 已收敛到 `.runtime/`，避免污染仿真人可见状态目录。
- runtime 只识别 `_meta`、`_summary`、`summary` 这些通用自描述字段。
- runtime 不再硬编码任何自定义技能字段。
- `behavior_trace.jsonl` 使用 trace/span 风格记录：
  - `trace_id`
  - `span_id`
  - `parent_span_id`
  - `name`
  - `input_summary`
  - `output_summary`
  - `duration_ms`
- `PersonAgent` 每个 step 记录 `step_start` / `step_end`。
- 每轮工具选择记录 `tool_call`。
- 每次工具结果通过统一出口记录 `tool_result`。
- 技能激活记录 `skill_activate` 子 span。
- workspace 文档刷新记录 `state_sync`。

这套改造保持了一个边界：框架可以观测“发生了什么”，但不解释“某个技能字段是什么意思”。
