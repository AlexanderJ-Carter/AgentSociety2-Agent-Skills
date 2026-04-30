# `culture`

Apply cultural values, etiquette, rituals, symbols, taboos, and local meaning to perception and decisions.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/culture/`
- 说明文件 / Skill file: `skills/culture/SKILL.md`
- 最近更新 / Last updated: `2026-04-27`
- 理论依据 / Research basis: no bundled reference file.

## SKILL.md（原文）

```
---
name: culture
description: Apply cultural values, etiquette, rituals, symbols, taboos, and local meaning to perception and decisions.
---

# Culture

## Purpose

Model the agent as a cultural person. Culture shapes what feels polite, shameful, prestigious, intimate, sacred, ordinary, rude, festive, or taboo.

## Use When

Use this skill before social interaction, food choice, clothing choice, gift giving, public behavior, festival behavior, family obligations, workplace etiquette, or cross-cultural misunderstanding.

## Procedure

1. Read `state/observation.txt`, `state/observation_ctx.json`, `state/culture.json`, `state/norms.json`, `state/relationships.json`, and profile context if present.
2. Identify active cultural context: place, group, language, holiday, institution, role, and audience.
3. Determine relevant scripts, values, etiquette, symbols, and taboos.
4. Estimate cultural comfort and risk of offense or embarrassment.
5. Write cultural state for `cognition`, `relationships`, and `plan`.

## Write

Write `state/culture.json`.

## Output Schema

```json
{
  "active_context": "workplace lunch",
  "values_in_play": ["professionalism", "face-saving", "reciprocity"],
  "etiquette": ["be punctual", "avoid direct confrontation"],
  "taboos": ["publicly embarrassing a colleague"],
  "cultural_comfort": 0.74,
  "misunderstanding_risk": 0.18,
  "recommended_style": "polite and indirect"
}
```

## Notes

Culture should not be a stereotype. Use profile, setting, relationship, and observed behavior. If evidence is weak, write uncertainty instead of forcing a cultural explanation.
```
