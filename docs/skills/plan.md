# `plan`

Execute intentions through the environment.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/plan/`
- 说明文件 / Skill file: `skills/plan/SKILL.md`
- 执行脚本 / Script baseline: none; use the natural-language procedure.
- 最近更新 / Last updated: `2026-05-03`
- 理论依据 / Research basis:
  - `skills/plan/references/research_basis.md`

## SKILL.md（原文）

```
---
name: plan
description: Execute intentions through the environment.
---

# Plan

## Purpose

Execute intentions by generating environment actions via `codegen`.

## Internal Logic (One Sentence)

Read the current intention, observation, needs, affordances, and any ongoing plan, then choose a one-tick action or update `state/plan_state.json` for multi-step execution through `codegen`.

Research basis: `references/research_basis.md`.

## Use When

Activate this skill when you have an intention to execute.

## Dual-Process Decision Making

Human decisions arise from two systems:

### System 1: Fast, Habitual

- Triggered by: routine situations, familiar contexts
- Characteristics: quick, automatic, low cognitive load
- Output: single-step action, no plan_state needed
- Use when:
  - Routine activity (eating, sleeping, commuting)
  - Time pressure
  - Low stakes
  - Strong habit exists

### System 2: Deliberate, Planned

- Triggered by: novel situations, complex goals, conflicts
- Characteristics: slow, analytical, requires attention
- Output: multi-step plan_state.json
- Use when:
  - New or unfamiliar goal
  - Multiple steps required
  - High stakes or uncertainty
  - Conflicting options

### System Selection

| Condition | System |
|-----------|--------|
| Routine time + routine action | System 1 |
| Familiar location + known action | System 1 |
| New intention + complex goal | System 2 |
| Multiple options + uncertainty | System 2 |
| Urgent need + known solution | System 1 |
| Conflict detected | System 2 |

## Input Files

| File | Use |
|------|-----|
| `state/intention.json` | Current goal |
| `state/observation.txt` | Environment context |
| `state/plan_state.json` | Ongoing multi-step plan |

## Output Files

### state/plan_state.json

```json
{
  "goal": "Buy groceries at the supermarket",
  "steps": ["walk to supermarket", "enter store", "pick items", "pay"],
  "current_step": 1,
  "started_tick": 42,
  "status": "in_progress",
  "decision_mode": "system2",
  "estimated_ticks": 4
}
```

## Single-Step Actions (System 1)

Most routine intentions execute in one `codegen` call:

```json
{
  "tool_name": "codegen",
  "arguments": {
    "instruction": "Move to the café on Main Street.",
    "ctx": {}
  }
}
```

No `plan_state.json` needed for single-step actions.

## Multi-Step Plans (System 2)

For complex goals, maintain `state/plan_state.json`:

1. Check if `plan_state.json` exists
2. If new intention, generate steps (max 6)
3. Execute current step via `codegen`
4. Update `plan_state.json` with progress
5. Clear when all steps complete

### Step Status

| Status | Meaning |
|--------|---------|
| `pending` | Not started |
| `in_progress` | Currently executing |
| `completed` | Successfully finished |
| `failed` | Cannot complete |

### Step Complexity

| Steps | Use Case |
|-------|----------|
| 1-2 | Simple location change, simple interaction |
| 3-4 | Multi-location trip, task with preparation |
| 5-6 | Complex project, event with multiple phases |

## Need-Driven Plan Adjustment

Plans adapt to changing physiological states.

### Adjustment Triggers

| Trigger | Action |
|---------|--------|
| `satiety < 0.2` | Pause plan, find food |
| `energy < 0.2` | Pause plan, rest |
| `safety < 0.2` | Pause plan, seek safety |
| Need satisfied mid-plan | Resume original plan |

### Plan State for Interruption

```json
{
  "goal": "Work on project",
  "status": "interrupted",
  "interrupted_at_step": 2,
  "interrupt_reason": "satiety_critical",
  "resumable": true,
  "resume_conditions": ["satiety > 0.5"]
}
```

### Resume Logic

1. Check `resumable` flag
2. Verify all `resume_conditions` met
3. Continue from `interrupted_at_step`
4. Update status to `in_progress`

## Plan Interruption

Interrupt ongoing plan when:
- New urgent need emerges (satiety/energy < 0.2)
- Current intention differs significantly
- Environment makes plan impossible
- External event requires attention

### Forced vs Voluntary

| Type | Condition | Recovery |
|------|-----------|----------|
| `forced` | Critical need | Resume when satisfied |
| `voluntary` | Better option | May abandon plan |

## Habit Integration

When a plan becomes routine, convert to habit.

### Habit Formation

| Repetitions | Status |
|-------------|--------|
| 1-2 | Novel (System 2) |
| 3-5 | Learning (mix) |
| 6+ | Habit (System 1) |

### Habit Output

For habitual actions, add to `intention.json`:

```json
{
  "intention": "Morning commute to work",
  "is_habit": true,
  "habit_strength": 0.8,
  "automatic": true
}
```

## Procedure

1. Read `state/intention.json` and `state/plan_state.json`
2. Determine decision mode (System 1 or 2)
3. Check for need-based interrupts
4. Generate or continue plan execution
5. Call `codegen` with action instruction
6. Update `plan_state.json`
7. Re-observe after action if needed

## Guidelines

- One meaningful action per tick
- Actions must match AVAILABLE ACTIONS from observation
- Handle idle gracefully with `done`
- Mark plan as `failed` after 3 consecutive failures
- Prefer System 1 for routines, System 2 for novel goals
- Always check needs before executing plan step

## Write

Write or update `state/plan_state.json` for multi-step, interrupted, failed, or completed plans. Routine one-step actions may only call `codegen` and then refresh observation state.

## Re-observation

After each `codegen` action:

1. Check the result
2. Call `codegen` with `<observe>` to get updated state
3. Update `state/observation.txt`
4. Continue reasoning

## Notes

Planning should convert intentions into feasible environment actions, not invent unavailable actions or override the intention system. If no valid action is available, mark the plan blocked or call `done`.
```

## 理论依据 / Research Basis

### `research_basis.md`

# Plan Research Basis

## Model

Dual-process action selection with bounded rationality, plus lightweight plan-state tracking for multi-step intentions.

## Update Rule

```text
if routine_or_urgent_known_action:
    decision_mode = "system1"
    execute one feasible action
else:
    decision_mode = "system2"
    create_or_continue plan_state with up to 6 steps
```

Interrupt plans when physiological need, safety, unavailable affordance, or changed intention crosses a threshold.

## Variables

- `decision_mode`: `system1` or `system2`.
- `plan_state.status`: `pending`, `in_progress`, `interrupted`, `completed`, or `failed`.
- `current_step`: active step index.
- `estimated_ticks`: rough plan duration.
- `interrupt_reason`: critical need, blocked action, external event, or changed intention.

## Defaults

Prefer one meaningful action per tick. If observation does not list a feasible action, wait, observe, or mark the plan blocked.

## Sources

- Kahneman, D. (2011). *Thinking, Fast and Slow*.
- Simon, H. A. (1955). A behavioral model of rational choice.
- Bratman, M. E. (1987). *Intention, Plans, and Practical Reason*.
