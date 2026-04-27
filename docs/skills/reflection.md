# `reflection`

Synthesize memories into stable beliefs, preferences, self-concept, and future behavioral tendencies.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/reflection/`
- 说明文件 / Skill file: `skills/reflection/SKILL.md`
- 理论依据 / Research basis: no bundled reference file.

## SKILL.md（原文）

```
---
name: reflection
description: Synthesize memories into stable beliefs, preferences, self-concept, and future behavioral tendencies.
---

# Reflection

## Purpose

Convert repeated experiences into higher-level understanding. This skill lets the agent learn patterns about self, others, places, routines, culture, and consequences.

## Use When

Use this skill periodically, after major events, after repeated similar memories, at the end of a day, or before long-horizon planning.

## Procedure

1. Read `state/memory.jsonl`, `memory/memory.jsonl`, `state/relationships.json`, `state/routine.json`, `state/emotion.json`, `state/physiology.json`, and existing `state/reflections.jsonl` if present.
2. Look for repeated patterns, contradictions, strong emotions, completed goals, failures, and social consequences.
3. Create concise reflections that can guide future choices.
4. Update beliefs, preferences, and self-concept only when evidence is strong enough.
5. Write new reflections and current belief state.

## Write

Append `state/reflections.jsonl`. Write `state/beliefs.json`, `state/preferences.json`, and `state/self_concept.json` when changed.

## Output Schema

Reflection JSONL line:

```json
{
  "tick": 180,
  "type": "pattern",
  "summary": "I often become tired and irritable after skipping lunch.",
  "evidence": ["missed lunch", "anger rose", "plan interrupted"],
  "confidence": 0.74,
  "tags": ["physiology", "routine", "emotion"]
}
```

`state/beliefs.json`:

```json
{
  "self": {
    "late_meals_reduce_mood": {
      "belief": "Skipping lunch tends to make me tired and irritable.",
      "confidence": 0.74
    }
  },
  "others": {},
  "places": {}
}
```

## Notes

Do not reflect every tick. Reflection should be slower than memory. It should compress experience into useful patterns without erasing the raw memory trail.
```
