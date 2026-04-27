# `memory`

Persist important outcomes from this step to long-term storage with automatic forgetting curve.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/memory/`
- 说明文件 / Skill file: `skills/memory/SKILL.md`
- 理论依据 / Research basis:
  - `skills/memory/references/research_basis.md`

## SKILL.md（原文）

```
---
name: memory
description: Persist important outcomes from this step to long-term storage with automatic forgetting curve.
---

# Memory

You are the agent's long-term memory system with automatic forgetting and retrieval reinforcement. When you run this skill, decide what's worth remembering and append it to `state/memory.jsonl`.

## Internal Logic (One Sentence)

Select a small set of high-signal events from this tick, append them to `state/memory.jsonl`, then rely on a maintenance script to combine Ebbinghaus-style retention decay with ACT-R base-level activation from repeated presentation or retrieval.

## Architecture (conceptual)

Three layers:

### 1. Working context (implicit)

- **What**: Recent tool-loop messages plus any workspace files you choose to read in this step.
- **Purpose**: Immediate reasoning; there is no separate hidden memory buffer beyond workspace + thread.
- **Usage**: Read only files that exist; skip missing paths.

### 2. Long-term store (`state/memory.jsonl`)

- **What**: JSONL in the agent workspace with automatic forgetting.
- **Purpose**: Persist what should survive across ticks (events, decisions, plan outcomes).
- **Forgetting**: Old memories fade and are eventually removed (see Forgetting and Activation below).
- **Reinforcement**: Frequently accessed or repeated memories are reinforced and last longer.

### 3. Optional "step bundle" (convention)

- If you want one rich JSONL line per tick, you may bundle highlights into `summary` from whatever files you read in this step-purely optional.

## Forgetting and Activation

Memories naturally decay over time, but repeated experience and retrieval should make a memory easier to recover. This skill therefore uses two complementary signals:

- **Ebbinghaus-style retention** for simple time decay.
- **ACT-R base-level activation** for repeated presentation/retrieval.

Research basis: `references/research_basis.md`.

### Retention Formula

```
retention = e^(-t / (S x importance_multiplier))
```

Where:
- `t` = ticks since memory creation
- `S` = memory strength coefficient (default: 100 ticks, configurable via `AGENT_MEMORY_STRENGTH` env var)
- `importance_multiplier` = high: 1.5, medium: 1.0, low: 0.5

### ACT-R Base-Level Activation

The maintenance script also computes:

```text
activation = ln(sum((current_tick - presentation_tick)^(-d))) + importance_bonus + access_bonus
retrieval_probability = logistic(activation - threshold)
retention = max(ebbinghaus_retention, retrieval_probability)
```

Where:
- `_presentations` stores the ticks when the memory was encoded or strongly re-encountered.
- `d` defaults to `0.5`, a common ACT-R decay value.
- `_access_count` provides a small retrieval-practice bonus.
- The max rule keeps the simple forgetting curve as a conservative floor while allowing repeated social facts, names, promises, and routes to persist.

### Decay Rules

| Retention Level | Status | Behavior |
|-----------------|--------|----------|
| `retention > 0.5` | Active | Memory is fully accessible |
| `0.1 < retention < 0.5` | Fading | Memory marked as `_faded: true` |
| `retention < 0.1` | Forgotten | Memory is removed from the store |

### Reinforcement

When a memory is accessed or re-encoded:

- Increase `_access_count` by 1 when the runtime can identify retrieval.
- Append current tick to `_presentations` when the same fact/event is strongly re-encountered.
- Keep `_presentations` short if needed by retaining the newest and most important ticks.

This models retrieval practice and repeated exposure without pretending the simulation has exact human neural memory.

### Memory Limits

To prevent unbounded growth:
- Default maximum: 1000 entries (configurable via `AGENT_MEMORY_MAX_ENTRIES`)
- When over limit, lowest-retention memories are removed first

## Importance Guidelines

When writing memories, set `importance` appropriately:

| Importance | Use Case | Retention (approx) |
|------------|----------|-------------------|
| `high` | Life-changing events, critical decisions, major discoveries | ~150 ticks |
| `medium` | Notable events, moderate decisions (default) | ~100 ticks |
| `low` | Minor observations, routine activities | ~50 ticks |

**Tip**: Set `importance: high` for memories that should persist across the entire simulation.

## Entry `type` values (recommended)

Use `type` to help future `grep` / manual scanning:

| Type | When it applies | Example |
|------|------------------|---------|
| `need` | After notable need change | "Satiety dropped; decided to find food" |
| `emotion` | After strong emotion / regulation | "Relieved after plan succeeded" |
| `cognition` | Thought / appraisal update | "Reframed delay as acceptable" |
| `intention` | Intention changed | "Switched intention to head home" |
| `plan` | Plan created or revised | "New plan: 3 steps to reach clinic" |
| `react` | Notable environment interaction | "codegen: move to cafe" |
| `plan_execution` | Step finished or failed | "Step 'walk to cafe' completed" |
| `event` | General occurrence | "Met Alice; she mentioned the job" |
| `observation` | Notable perception to recall later | Short summary of what you saw / heard |
| `social` / `decision` / `discovery` / `plan_outcome` | As in the table below |

Use **`type`** + **`tags`** so grep and tail-scans stay useful.

## When to Write a Memory

**Write a memory when:**
- You had a meaningful interaction (conversation, transaction, conflict)
- You discovered something new (a new location, a new agent, useful information)
- An important state change occurred (need became critical, plan completed/failed)
- You made a significant decision (changed plans, formed an opinion)
- Something emotionally notable happened

**Skip memory when:**
- Nothing happened (idle tick, walking without events)
- The observation is essentially the same as last tick
- The information is already captured in a recent memory entry

## Memory Entry Format

Each entry is a single JSON line in `state/memory.jsonl`:

```json
{"tick": 42, "time": "2024-01-15T10:30:00", "type": "event", "summary": "Met Alice at the park. She mentioned a job opening at the library.", "tags": ["social", "alice", "job"], "importance": "medium"}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `tick` | int | Current tick number (from the step context) |
| `time` | string | ISO format timestamp |
| `type` | string | Category - see Memory Types below |
| `summary` | string | 1-2 sentence factual description of what happened |
| `tags` | list | 2-5 short keywords for retrieval (agent names, locations, topics) |
| `importance` | string | `high` (life-changing), `medium` (notable), `low` (minor) |

## How to Write

1. Optionally `workspace_read` any relevant context files.
2. Decide if anything is worth remembering (see criteria above).
3. If yes, construct the memory entry and append:

```json
{
  "tool_name": "workspace_write",
  "arguments": {
    "path": "state/memory.jsonl",
    "content": "<existing content>\n<new JSON line>"
  }
}
```

**Important**: Since `workspace_write` overwrites the file, first `workspace_read("state/memory.jsonl")` to get existing content, then append the new entry.

4. If nothing notable happened, call `done` immediately.

## Memory Retrieval

Readers of `state/memory.jsonl` typically scan the last few lines for recent context.

### Reading Recent Memories

Focus on the most recent entries (last 5-10) when you need continuity.

### Searching older memories

Use `grep` on `state/memory.jsonl` to search for names or tags.

## Maintenance Script

Run periodically to apply forgetting curve:

```bash
python skills/memory/scripts/memory_maintenance.py \
  --memory-file state/memory.jsonl \
  --current-tick 100
```

Configuration via environment variables:
- `AGENT_MEMORY_STRENGTH`: Memory strength coefficient (default: 100)
- `AGENT_MEMORY_ACTR_DECAY`: ACT-R decay parameter (default: 0.5)
- `AGENT_MEMORY_RETRIEVAL_THRESHOLD`: logistic retrieval threshold (default: -2.5)
- `AGENT_MEMORY_MAX_ENTRIES`: Maximum memories to keep (default: 1000)

## Guidelines

- Keep summaries **concise** (1-2 sentences max). This is a log, not a diary.
- Use **specific names and locations**, not vague references.
- Don't duplicate information already in the most recent memory entry.
- **Timestamp all entries** for temporal reasoning.
- **Tag entries** with relevant keywords for efficient retrieval.
- Set **importance** based on how long the memory should persist.
```

## 理论依据 / Research Basis

### `research_basis.md`

# Memory — Research Basis

本技能把“长时记忆维护”拆成两层：写入（LLM 决定哪些值得记）与维护（脚本按模型衰减、检索激活与清理）。

## 采用的遗忘曲线：Ebbinghaus Forgetting Curve（指数衰减形式）

我们使用指数衰减作为可控、可解释、可实现的 baseline：

\[
R(t)=\exp\left(-\frac{t}{S \cdot k}\right)
\]

- \(R(t)\)：保留度（retention），范围 \([0,1]\)
- \(t\)：距离该记忆创建的 tick 数
- \(S\)：强度系数（strength），控制衰减速度（默认建议 \(S=100\) ticks）
- \(k\)：重要性乘子（importance multiplier），例如：high=1.5、medium=1.0、low=0.5

### 为什么选指数形式

- **实现简单**：只需要 tick 差与少量参数
- **可解释**：衰减速度与“强度/重要性”可直觉调参
- **稳定**：不会出现奇异点或不可控的长尾

### 强化（rehearsal / retrieval practice）

被检索或反复提及的记忆会更不容易忘。脚本可用两种简单策略之一：

1) **加性强化**：访问一次使 \(R\leftarrow \min(0.95, R+\Delta)\)
2) **等效时间回拨**：访问一次使 \(t\leftarrow \max(0, t-\tau)\)

仓库脚本默认采用简单可控的加性强化（见 `../scripts/memory_maintenance.py`）。

## ACT-R Base-Level Learning：多次经历/回忆的叠加

只用“创建时间”会低估社会仿真的一个关键事实：一个人反复见到的同事、路线、承诺、冲突，即使第一次发生很久以前，也应当比一次性事件更容易被想起。

因此维护脚本额外计算 ACT-R 风格的 base-level activation：

\[
B_i=\ln\left(\sum_j t_j^{-d}\right)
\]

- \(B_i\)：记忆块 \(i\) 的基础激活。
- \(t_j\)：距离第 \(j\) 次呈现/检索的 tick 间隔，最小按 1 处理，避免除零。
- \(d\)：衰减参数，默认 \(0.5\)。
- 多次呈现以求和方式叠加，因此重复经历会形成更高激活。

脚本实现中还加了两个仿真友好的项：

\[
B_i' = B_i + \ln(k) + 0.08 \cdot \min(10, access\_count)
\]

- \(k\)：重要性乘子，沿用 high=1.5、medium=1.0、low=0.5。
- `access_count`：检索次数，用小幅 bonus 表示 retrieval practice。

再用 logistic 函数把激活转成可解释概率：

\[
P(retrieve)=\frac{1}{1+\exp(-(B_i' - \theta))}
\]

最后：

\[
retention=\max(R_{Ebbinghaus}, P(retrieve))
\]

这样做的好处是：

- 单次低价值事件仍会自然淡出；
- 被反复遇到的人、地点、规则、承诺会更稳定；
- 模拟中“熟悉感”和“社会连续性”不必完全依赖 LLM 临场回忆。

## 参数建议

| 参数 | 默认 | 含义 | 调参方向 |
|------|------|------|----------|
| `AGENT_MEMORY_STRENGTH` | `100` | Ebbinghaus 指数衰减强度 | tick 很短时调大 |
| `AGENT_MEMORY_ACTR_DECAY` | `0.5` | ACT-R 呈现项的幂律衰减 | 想让重复经历更快淡出时调大 |
| `AGENT_MEMORY_RETRIEVAL_THRESHOLD` | `-2.5` | retrieval probability 的阈值 | 想更严格保留时调高 |
| `AGENT_MEMORY_MAX_ENTRIES` | `1000` | 文件容量上限 | 大规模仿真按成本调节 |

## 参考

- Hermann Ebbinghaus. *Memory: A Contribution to Experimental Psychology* (1885).
- Anderson, J. R. & Schooler, L. J. (1991). Reflections of the environment in memory.
- ACT-R base-level learning equation: repeated presentations add as power-law terms; common decay default \(d=0.5\).
- Roediger, H. L. & Karpicke, J. D. (2006). Test-enhanced learning: taking memory tests improves long-term retention.
- 现代 retrieval practice 综述可用于解释“检索强化”。
