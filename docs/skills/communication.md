# `communication`

Model conversation intent, speech style, turn-taking, listening, repair, and nonverbal cues. Use before or after social interaction, dialogue, negotiation, apology, request, gossip, or conflict.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/communication/`
- 说明文件 / Skill file: `skills/communication/SKILL.md`
- 理论依据 / Research basis:
  - `skills/communication/references/theory.md`

## SKILL.md（原文）

```
---
name: communication
description: Model conversation intent, speech style, turn-taking, listening, repair, and nonverbal cues. Use before or after social interaction, dialogue, negotiation, apology, request, gossip, or conflict.
---

# Communication

## Purpose

Maintain how the agent communicates with others: what it wants to say, how direct it is, whether it listens, how it repairs misunderstandings, and what nonverbal signals matter.

## Use When

Use this skill around conversations, requests, refusals, apologies, negotiation, gossip, teaching, conflict, small talk, or public speaking.

## Procedure

1. Read `state/observation.txt`, `state/observation_ctx.json`, `state/relationships.json`, `state/culture.json`, `state/norms.json`, `state/emotion.json`, and previous `state/communication.json` if present.
2. Identify participants, relationship, setting, power distance, audience, and active goal.
3. Choose a communicative intent: inform, ask, request, refuse, comfort, apologize, persuade, coordinate, joke, signal status, avoid, or repair.
4. Select style: direct/indirect, formal/informal, warm/cold, brief/elaborate, assertive/deferential.
5. Track turn state: whether the agent should speak, listen, clarify, or end the interaction.
6. Write `state/communication.json`.

## Write

Write `state/communication.json`.

## Output Schema

```json
{
  "_meta": {
    "skill": "communication",
    "purpose": "Conversation intent, style, turn state, and repair strategy."
  },
  "_summary": "Use a polite indirect request and listen for Alice's response.",
  "participants": ["alice"],
  "intent": "request",
  "style": {
    "directness": 0.35,
    "formality": 0.62,
    "warmth": 0.74,
    "assertiveness": 0.42
  },
  "turn_state": "speak_next",
  "repair_needed": false,
  "recommended_utterance_goal": "Ask Alice if she can share the schedule without pressuring her."
}
```

## Notes

Communication is not just text generation. It should reflect relationship, emotion, norms, culture, and purpose. If uncertain, prefer asking clarifying questions or listening.

For theory notes, see `references/theory.md`.
```

## 理论依据 / Research Basis

### `theory.md`

# Communication Theory Notes

Useful foundations:

- Speech act theory: utterances can inform, request, promise, apologize, command, invite, refuse, or repair.
- Gricean pragmatics: people infer meaning from relevance, quantity, quality, and manner, not only literal words.
- Politeness theory: directness and face-saving depend on power, distance, imposition, and culture.
- Conversation analysis: turn-taking, repair, adjacency pairs, and openings/closings shape interaction.
- Nonverbal communication: gaze, distance, gesture, posture, timing, and silence carry social meaning.

Implementation guidance:

- Keep a separate `intent` from final utterance text.
- Use relationship and norms to tune directness and formality.
- Use emotion to tune warmth, patience, and repair probability.
- Track misunderstandings explicitly instead of assuming every conversation succeeds.
