# Agent Context And File Index Design

## 目标

`PersonAgent` 的 workspace 需要一个类似 Claude Code `CLAUDE.md` 的入口文件，帮助 agent 快速理解：

- 当前自己是谁、在做什么。
- 有哪些状态文件。
- 应该去哪里找记忆、输入、日志和自定义技能。

当前推荐使用单一文件：

```text
AGENT.md
```

不要再拆成 `AGENT_CONTEXT.md` 和 `AGENT_FILES.md`。上下文和文件索引放在同一个文件里，减少 agent 找不到入口的概率。

## AGENT.md 结构

`AGENT.md` 使用 YAML frontmatter + Markdown body：

```markdown
---
current_task: "..."
state_summary:
  physiology: "..."
state_files:
  - state/physiology.json
last_sync: "..."
---

# Agent Notes

人工或 agent 自己保留的短备注。

<!-- AGENT_FILE_INDEX_START -->
# Workspace Files
...
<!-- AGENT_FILE_INDEX_END -->
```

## 运行时职责

runtime 只做通用工作：

- 扫描 `state/`、`memory/`、`input/`、`custom/`。
- 为 `state/*.json` 生成通用短摘要。
- 为 `state/*.jsonl` 统计事件数量。
- 把自动文件索引写入 `AGENT.md` 的标记区块。
- 保留标记区块外的人工内容。

## Workspace 目录约定

仿真人 workspace 应区分“人的可见状态”和“框架运行时内部数据”。

可见目录：

- `state/`：当前身体、认知、经济、关系等状态。
- `memory/`：长期记忆或跨线程记忆。
- `input/`：环境或实验外部输入。
- `custom/skills/`：自定义技能。

运行时内部目录：

- `.runtime/logs/`：thread、tool、trace、step replay、压缩历史。
- `.runtime/checkpoints/`：checkpoint。
- `.runtime/wal/`：预写日志。
- `.runtime/archive/`：清理归档。

默认不把 `.runtime/` 当作 agent 的生活状态来源。需要调试或做实验分析时可以读取它。

runtime 不应该知道任何具体技能字段，例如：

- `hunger_pressure`
- `scarcity_pressure`
- `trust`
- `circadian_alertness`

这些都是技能语义，不属于文件系统或上下文运行时。

## 技能摘要约定

如果某个技能希望自己在 `AGENT.md` 中有稳定摘要，它可以在输出 JSON 里写：

```json
{
  "_meta": {
    "skill": "physiology",
    "purpose": "Current body pressures and physiological needs."
  },
  "_summary": "Hungry and slightly tired; eating soon is likely.",
  "hunger_pressure": 0.72,
  "fatigue": 0.41
}
```

或者：

```json
{
  "summary": "Budget stress is moderate; expensive leisure should be avoided."
}
```

runtime 可以读取 `_summary` 或 `summary`，但不解释其他字段。没有摘要字段时，runtime 只展示少量顶层结构，帮助定位文件。

如果需要告诉 runtime “这个文件是干什么的”，使用 `_meta.purpose` 或 `_meta.description`。这仍然是通用自描述，不是 runtime 对某个技能的特殊适配。

## 技能仓库文件组织

ClaudeSkill 风格推荐：

```text
skills/<skill_name>/SKILL.md
skills/<skill_name>/scripts/
skills/<skill_name>/references/
skills/<skill_name>/assets/
```

- `SKILL.md`：必须有，包含 `name`、`description` 和执行说明。
- `scripts/`：可选，用于确定性计算、校验、批处理。
- `references/`：可选，用于理论依据、公式、长说明，按需读取。
- `assets/`：可选，用于模板、静态数据、示例配置。

## 为什么这样设计

这种设计和 Claude/Cursor 的思路一致：

- catalog 只放轻量信息。
- 技能正文按需激活。
- 长理论材料放 `references/`，避免常驻上下文。
- 可计算逻辑放 `scripts/`，避免靠自然语言重复算。
- runtime 不绑定具体技能，技能可以自由增长。
