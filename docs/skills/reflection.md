# `reflection`

Synthesize memories into stable beliefs, preferences, self-concept, and future behavioral tendencies.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/reflection/`
- 说明文件 / Skill file: `skills/reflection/SKILL.md`
- 执行脚本 / Script baseline: none; use the natural-language procedure.
- 最近更新 / Last updated: `2026-05-03`
- 理论依据 / Research basis:
  - `skills/reflection/references/research_basis.md`

## SKILL.md（原文）

```
---
name: reflection
description: Synthesize memories into stable beliefs, preferences, self-concept, and future behavioral tendencies.
---

# Reflection

## Purpose

Convert repeated experiences into higher-level understanding. This skill lets the agent learn patterns about self, others, places, routines, culture, and consequences.

## Internal Logic (One Sentence)

Compress repeated memories, emotions, plans, relationship changes, and routine outcomes into concise reflections, then append `state/reflections.jsonl` and update beliefs, preferences, or self-concept when evidence is strong.

Research basis: `references/research_basis.md`.

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

## 理论依据 / Research Basis

### `research_basis.md`

# Reflection Research Basis

## Model

Autobiographical memory abstraction, self-schema updating, and reflective learning from repeated evidence.

## Update Rule

```text
pattern_confidence = clamp(repetition_strength + emotional_weight + outcome_consistency - contradiction_penalty, 0, 1)
if pattern_confidence >= 0.65:
    append reflection
if pattern_confidence >= 0.75:
    update belief, preference, or self_concept
```

## Variables

- `repetition_strength`: how often the pattern appears, `[0, 1]`.
- `emotional_weight`: intensity of associated emotions, `[0, 1]`.
- `outcome_consistency`: consistency of consequences, `[0, 1]`.
- `contradiction_penalty`: strength of counter-evidence, `[0, 1]`.
- `confidence`: evidence-backed confidence for the reflection, `[0, 1]`.

## Defaults

Do not reflect every tick. Reflection should compress repeated evidence, not replace raw memory.

## Sources

- Conway, M. A., & Pleydell-Pearce, C. W. (2000). The construction of autobiographical memories.
- Markus, H. (1977). Self-schemata and processing information about the self.
- Kolb, D. A. (1984). *Experiential Learning*.
