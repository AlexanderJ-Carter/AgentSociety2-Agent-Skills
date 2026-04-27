# `relationships`

Update interpersonal familiarity, trust, liking, obligation, conflict, and shared history.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/relationships/`
- 说明文件 / Skill file: `skills/relationships/SKILL.md`
- 理论依据 / Research basis:
  - `skills/relationships/references/research_basis.md`

## SKILL.md（原文）

```
---
name: relationships
description: Update interpersonal familiarity, trust, liking, obligation, conflict, and shared history.
script: scripts/update_relationships.py
---

# Relationships

## Purpose

Maintain social continuity between agents. This skill turns repeated interaction into relationship state instead of treating every encounter as new.

Research basis: `references/research_basis.md`.

## Use When

Use this skill after conversations, cooperation, conflict, promises, favors, gifts, avoidance, betrayal, or repeated co-presence.

## Procedure

1. Read `state/observation.txt`, `state/observation_ctx.json`, `state/relationships.json`, `state/memory.jsonl`, `state/emotion.json`, and profile context if present.
2. Identify people involved and what happened.
3. Update familiarity, trust, liking, obligation, conflict, respect, and last interaction.
4. Add or revise shared history tags.
5. Write relationship state. If the event is notable, append a social memory through the memory skill or directly to `state/social_events.jsonl`.

If deterministic baseline is preferred, run `scripts/update_relationships.py` first, then optionally refine subtle social interpretation with LLM reasoning.

## Write

Write `state/relationships.json`. Optionally append `state/social_events.jsonl`.

## Output Schema

```json
{
  "people": {
    "alice": {
      "familiarity": 0.62,
      "trust": 0.71,
      "liking": 0.55,
      "obligation": 0.2,
      "conflict": 0.05,
      "respect": 0.58,
      "last_interaction": "brief friendly chat at cafe",
      "shared_history_tags": ["cafe", "work"]
    }
  }
}
```

## Notes

Trust and conflict should change more slowly than momentary emotion. A single event can strongly affect a relationship only if it is high-stakes, public, repeated, or identity-relevant.
```

## 理论依据 / Research Basis

### `research_basis.md`

# Relationship Modeling Basis

## Why this matters

Social continuity requires memory of interaction quality, not just immediate emotion.

## Evidence anchors

- Trust/cooperation and repeated-game findings: cooperation stabilizes with memory and reciprocity signals.
- Social norm and sanction literature: violations affect trust/reputation asymmetrically.
- Relationship science: familiarity and affect can change quickly, but trust/conflict usually move slower unless high-stakes events occur.

## Simulation translation

Per person:

- familiarity
- trust
- liking
- obligation
- conflict
- respect
- shared_history_tags

Update policy:

- map interaction type to bounded delta vector
- apply optional context-specific delta override
- cap values in [0, 1]
- append high-impact events to social_events stream

## Practical notes

- Keep trust/conflict inertia higher than liking.
- Encode promises, betrayal, and public conflict as high-impact transitions.
- Do not erase old history; compress with tags and last_interaction fields.
