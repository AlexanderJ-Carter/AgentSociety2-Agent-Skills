# AgentSociety2 社会人仿真技能仓库

这是一个**独立的技能库**，用于在 AgentSociety 风格环境中模拟“真实社会人”：有身体节律、有社会关系、有规范压力、有经济约束，也会遗忘与学习。

## 你能在这里得到什么

- **可直接复制使用的技能目录**：每个技能一个 `skills/<name>/SKILL.md`
- **可复用的确定性脚本 baseline**：`skills/*/scripts/*.py`（减少 LLM 重复计算）
- **公开可审计的理论依据**：技能若使用曲线/模型/公式，应放在 `skills/*/references/*.md`
- **与 agentsociety2 PersonAgent 的对接约定**：通过 workspace 的 `state/*.json` / `state/*.jsonl` 解耦

## 文档入口

- 技能规范：`docs/skill_standard.md`
- 技能说明（面向使用者）：`docs/技能说明.md`
- `AGENT.md` 与 workspace 机制：`docs/agent_context_design.md`
- 研究与框架设计笔记：`docs/human_agent_research.md`、`docs/agent_framework_design_research.md`
- 文档索引：`docs/index.md`

## 本地预览静态说明站点（MkDocs）

```bash
python -m pip install -r requirements-docs.txt
python scripts/generate_skill_catalog.py
python -m mkdocs serve
```

## 当前技能（按目录）

基础技能（通常与 PersonAgent 运行链路直接配合）：

- `skills/observation`：获取环境观察并写入 workspace
- `skills/cognition`：把观察 + 状态综合成情绪/意图
- `skills/plan`：把意图转成环境动作
- `skills/memory`：把重要事件写入长时记忆并做遗忘维护

社会人能力层技能（示例）：

- 身体与节律：`circadian`、`physiology`、`health`
- 日常生活：`routine`
- 社会结构：`relationships`、`norms`、`culture`、`identity`、`communication`
- 约束与资源：`affordance`、`economy`
- 高层社会逻辑：`learning`、`moral_judgment`、`media_literacy`、`civic_institution`

## 确定性脚本（baseline）

当前已提供的脚本包括（以 `SKILL.md` 为准）：

- `skills/circadian/scripts/update_circadian.py`
- `skills/physiology/scripts/update_physiology.py`
- `skills/cognition/scripts/update_cognition.py`
- `skills/economy/scripts/update_economy.py`
- `skills/relationships/scripts/update_relationships.py`
- `skills/memory/scripts/memory_maintenance.py`
- `skills/health/scripts/update_health.py`
- `skills/routine/scripts/update_routine.py`
- `skills/norms/scripts/update_norms.py`
- `skills/affordance/scripts/update_affordance.py`
- `skills/learning/scripts/update_learning.py`
- `skills/moral_judgment/scripts/update_moral_judgment.py`
- `skills/media_literacy/scripts/update_media_literacy.py`
- `skills/civic_institution/scripts/update_civic_institution.py`

推荐用法：**先跑脚本得到可解释的数值状态**，再用 LLM 做情境化判断与叙述补全（而不是让 LLM 每次重复算数）。例如 `memory` 的维护脚本会同时记录 Ebbinghaus retention 与 ACT-R 风格 activation，`cognition` 的脚本会输出 Scherer-style appraisal 值，便于调参与回放。

## 与 agentsociety2 PersonAgent 的集成

推荐流程：

1. 把需要的技能目录复制进仿真 workspace（例如 `custom/skills/`）。
2. `SKILL.md` frontmatter 默认只写 `name` + `description`；如确实需要脚本，再加 `script`。
3. 技能输出写入 `state/*.json` 或 `state/*.jsonl`，并尽量提供 `_meta.purpose` 与 `_summary/summary`，方便 `AGENT.md` 自动索引与摘要。

## 贡献

请阅读 `CONTRIBUTING.md`。

## License

MIT，见 `LICENSE`。
