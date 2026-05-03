# `norms`

Track social norms, roles, obligations, permissions, sanctions, and place-specific expectations.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/norms/`
- 说明文件 / Skill file: `skills/norms/SKILL.md`
- 执行脚本 / Script baseline: none; use the natural-language procedure.
- 最近更新 / Last updated: `2026-05-03`
- 理论依据 / Research basis:
  - `skills/norms/references/research_basis.md`

## SKILL.md（原文）

```
---
name: norms
description: Track social norms, roles, obligations, permissions, sanctions, and place-specific expectations.
---

# Norms

## Purpose

Model the agent as someone living under social rules. Norms shape what the agent feels expected, allowed, forbidden, admired, or punishable.

## Internal Logic (One Sentence)

Use place, role, audience, culture, relationship, routine, and observation context to estimate active norms, permissions, sanctions, visibility, and moral emotion risk in `state/norms.json`.

Research basis: `references/research_basis.md`.

## Use When

Use this skill in workplaces, schools, homes, public spaces, queues, restaurants, hospitals, religious places, legal settings, or any situation involving role expectations.

## Procedure

1. Read `state/observation.txt`, `state/observation_ctx.json`, `state/norms.json`, `state/culture.json`, `state/relationships.json`, `state/routine.json`, and profile context if present.
2. Identify active roles: worker, customer, parent, friend, stranger, patient, student, neighbor, host, guest.
3. Identify place-specific expectations and forbidden behaviors.
4. Estimate norm pressure, witness visibility, sanction risk, and moral emotion risk.
5. Write norm state for `cognition` and `plan`.

## Write

Write `state/norms.json`.

## Output Schema

```json
{
  "active_roles": ["customer", "stranger"],
  "active_norms": [
    {
      "norm": "wait in line",
      "pressure": 0.83,
      "violation_risk": 0.7,
      "likely_sanction": "disapproval"
    }
  ],
  "permissions": ["order food", "sit at available table"],
  "forbidden_or_costly": ["skip queue", "shout at staff"],
  "witness_visibility": 0.65,
  "moral_emotion_risk": {
    "shame": 0.35,
    "guilt": 0.2
  }
}
```

## Notes

Norms should influence `subjective_norm` in intention selection. A norm can be violated, but the violation should have social, emotional, or institutional consequences when visible or important.
```

## 理论依据 / Research Basis

### `research_basis.md`

# Norms Research Basis

## Model

Social norms combine empirical expectations, normative expectations, role obligations, visibility, and sanction risk.

## Update Rule

```text
norm_pressure = clamp(
  empirical_expectation * 0.3
  + normative_expectation * 0.35
  + role_obligation * 0.2
  + witness_visibility * sanction_risk * 0.15,
  0,
  1
)
```

## Variables

- `active_roles`: roles currently applying to the agent.
- `active_norms`: expectations relevant to the setting.
- `pressure`: force of a norm, `[0, 1]`.
- `violation_risk`: chance a violation will be noticed or matter, `[0, 1]`.
- `witness_visibility`: how observable the behavior is, `[0, 1]`.
- `moral_emotion_risk`: shame and guilt risks, each `[0, 1]`.

## Defaults

Use setting and role first. If the norm is uncertain, mark it as low-confidence rather than hard-forbidden.

## Sources

- Bicchieri, C. (2006). *The Grammar of Society*.
- Cialdini, R. B., Reno, R. R., & Kallgren, C. A. (1990). A focus theory of normative conduct.
- Goffman, E. (1963). *Behavior in Public Places*.
