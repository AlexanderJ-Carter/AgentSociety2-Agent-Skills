# 极简 ClaudeSkill 风格规范

这个仓库不是普通文档库，而是一组可以被 `PersonAgent` 发现和激活的 `SKILL.md` 技能。设计目标是尽量接近 Cursor/ClaudeSkill 的处理方式：目录即技能，`SKILL.md` 即说明书，frontmatter 尽量少。

## 目录结构

每个技能一个目录：

```text
skills/<skill_name>/SKILL.md
skills/<skill_name>/references/
skills/<skill_name>/scripts/
skills/<skill_name>/assets/
```

## Frontmatter

默认只写两个字段：

```yaml
---
name: skill_name
description: One sentence shown in the skill catalog.
---
```

说明：

- `name`：技能名，使用 lowercase snake_case，并和目录名一致。
- `description`：技能目录里展示的一句话。模型激活技能前通常只看到这个。

`PersonAgent.SkillRegistry` 目前支持更多字段，比如 `requires`、`inputs`、`outputs`、`allowed_tools`、`script`、`executor`、`priority` 等。但这些都是框架扩展，不是本仓库的默认写法。除非某个技能必须依赖脚本或强约束工具，否则不要写。

## 正文结构

正文写成“激活后怎么做”，不要写成论文式设计文档。推荐结构：

1. `# <Skill Title>`
2. `## Purpose`
3. `## Internal Logic (One Sentence)`
3. `## Use When`
4. `## Procedure`
5. `## Write`
6. `## Notes`

如果技能需要输出结构化状态，再加 `## Output Schema`。

## 设计原则

- 技能本身要简单，复杂性放在自然语言步骤和状态文件里，不放在 frontmatter 里。
- 理论依据、曲线/模型、公式、变量定义放在 `references/`，在技能正文里按需引用。
- 确定性计算、校验、批处理放在 `scripts/`，不要让模型每次靠自然语言重复算。
- 当前状态写到 `state/*.json`，历史事件写到 `state/*.jsonl`。
- 如果希望 `AGENT.md` 里稳定展示摘要，在输出 JSON 中写 `_summary` 或 `summary`。
- 如果希望 `AGENT.md` 知道“这个文件是干什么的”，在输出 JSON 中写 `_meta.purpose` 或 `_meta.description`。
- 技能负责更新某一类“人的能力或状态”，不直接抢 `cognition` 的最终意图选择。
- 动态过程不要只写静态标签，比如饥饿要随时间、进食、活动、昼夜节律变化。
- 如果一个设计还没正式稳定，不做向后兼容包袱，直接改成清晰的新格式。

## “公开发布”额外要求（本仓库约束）

### 1) 必须有“一句话内部逻辑”

每个 `SKILL.md` 在 `## Purpose` 之后必须有一段 `## Internal Logic (One Sentence)`，用于回答：

- **它在一个 tick 内做什么更新？**
- **它用什么输入驱动？**
- **它把什么写入哪些 `state/*` 文件？**

例子（仅示例表达，不要求固定措辞）：

> “基于当前时间与上次睡眠，按 Two-Process Model 更新 `sleep_pressure` 与 `circadian_alertness`，写入 `state/circadian.json` 与 `state/sleep.json`。”

### 2) 用到曲线/模型/公式必须写 references

如果技能提到了“遗忘曲线、昼夜节律、两过程睡眠模型、习惯形成、应激恢复、社会规范压力”等模型化内容，必须在：

`skills/<skill_name>/references/*.md`

里写清楚：

- **模型名**
- **核心公式/更新规则**（可伪代码或数学表达）
- **变量含义与范围**（尤其是是否归一化到 `[0, 1]`）
- **参数建议与默认值**
- **引用来源**（论文/书/综述/权威公开资料）

`SKILL.md` 里只保留一句 “Research basis: `references/...`” 即可，避免把长引用塞进技能正文。

### 3) 状态文件自描述（强烈建议）

写 `state/*.json` 时建议包含：

- `_meta.purpose`：一句话说明文件用途
- `_summary` 或 `summary`：一句话摘要（用于 `AGENT.md` 稳定展示）

## 和 PersonAgent 的关系

当前 `PersonAgent` 的逻辑已经能扫描这种极简技能：

- 有 `SKILL.md` 就能被发现。
- `name` 和 `description` 会进入技能 catalog。
- 激活后，模型会读取完整 `SKILL.md` 并按正文执行。
- 技能写出的 `state/*.json` 会被 workspace 摘要、checkpoint 和后续技能自然读取。
- `AGENT.md` 是统一入口：包含短上下文和自动文件索引。

因此，本仓库的默认策略是：少字段、强正文、状态文件解耦。

## 自描述状态文件

推荐每个 `state/*.json` 都可以带一个通用 `_meta`，但不要把它当成复杂 schema：

```json
{
  "_meta": {
    "skill": "physiology",
    "purpose": "Current body pressures and physiological needs."
  },
  "_summary": "Hungry and slightly tired; eating soon is likely."
}
```

运行时只理解 `_meta`、`_summary`、`summary` 这些通用字段。其他字段属于技能自己的语义，运行时不会特殊处理。
