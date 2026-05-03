# `affordance`

Assess what actions are realistically available under environment, time, distance, access, money, body, and social constraints.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/affordance/`
- 说明文件 / Skill file: `skills/affordance/SKILL.md`
- 执行脚本 / Script baseline: none; use the natural-language procedure.
- 最近更新 / Last updated: `2026-05-03`
- 理论依据 / Research basis:
  - `skills/affordance/references/research_basis.md`

## SKILL.md（原文）

```
---
name: affordance
description: Assess what actions are realistically available under environment, time, distance, access, money, body, and social constraints.
---

# Affordance

## Purpose

Prevent unrealistic action choices. This skill translates the current world and internal state into feasible, costly, risky, or unavailable actions.

## Internal Logic (One Sentence)

Combine environment context with body, money, time, access, norm, and relationship constraints, then write feasible, costly, risky, blocked, and unknown action options to `state/affordances.json`.

Research basis: `references/research_basis.md`.

## Use When

Use this skill before planning, travel, purchase, social approach, work attendance, event participation, or any action that may fail because of constraints.

## Procedure

1. Read `state/observation.txt`, `state/observation_ctx.json`, `state/affordances.json`, `state/economy.json`, `state/physiology.json`, `state/health.json`, `state/norms.json`, and `state/routine.json` if present.
2. Identify available actions from the environment.
3. Estimate constraints: distance, time, opening hours, money, access rights, weather, fatigue, pain, safety, crowding, queues, and social permission.
4. Classify candidate actions as feasible, costly, risky, blocked, or unknown.
5. Write action affordances for `plan`.

## Write

Write `state/affordances.json`.

## Output Schema

```json
{
  "feasible_actions": ["walk to cafe", "talk to Alice", "buy cheap meal"],
  "costly_actions": [
    {
      "action": "take taxi",
      "cost_type": "money",
      "severity": 0.65
    }
  ],
  "blocked_actions": [
    {
      "action": "enter office",
      "reason": "closed or no access"
    }
  ],
  "risks": [
    {
      "action": "walk far while fatigued",
      "risk": "increased exhaustion",
      "severity": 0.42
    }
  ],
  "perceived_control_hint": 0.7
}
```

## Notes

Affordance is not intention. It should not decide what the agent wants; it should clarify what the agent can realistically do and what each option costs.
```

## 理论依据 / Research Basis

### `research_basis.md`

# Affordance Research Basis

## Model

Ecological affordance theory and constraint-based planning.

## Update Rule

For each candidate action, estimate:

```text
availability = environment_match * access * time_window
cost = weighted_sum(distance, money, fatigue, social_friction, risk)
feasibility = clamp(availability * (1 - cost), 0, 1)
```

Classify actions as:

- `feasible`: `feasibility >= 0.65`
- `costly`: `0.35 <= feasibility < 0.65`
- `blocked`: known access, time, money, physical, or social constraint prevents action
- `unknown`: missing evidence prevents a confident classification

## Variables

- `environment_match`: whether the object/place/action exists now, `[0, 1]`
- `access`: legal, social, physical, and role-based permission, `[0, 1]`
- `time_window`: whether the action can happen at the current time, `[0, 1]`
- `cost`: normalized burden across money, effort, distance, risk, and social friction, `[0, 1]`
- `perceived_control_hint`: feasibility signal for cognition, `[0, 1]`

## Defaults

Use conservative defaults when evidence is missing. Unknown is better than pretending an action is available.

## Sources

- Gibson, J. J. (1979). *The Ecological Approach to Visual Perception*.
- Norman, D. A. (1988). *The Psychology of Everyday Things*.
- Simon, H. A. (1955). A behavioral model of rational choice.
