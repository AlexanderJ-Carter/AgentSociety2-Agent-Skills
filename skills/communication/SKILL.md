---
name: communication
description: Model conversation intent, speech style, turn-taking, listening, repair, and nonverbal cues. Use before or after social interaction, dialogue, negotiation, apology, request, gossip, or conflict.
---

# Communication

## Purpose

Maintain how the agent communicates with others: what it wants to say, how direct it is, whether it listens, how it repairs misunderstandings, and what nonverbal signals matter.

## Internal Logic (One Sentence)

Use participants, relationship, culture, norms, emotion, and conversational context to select communicative intent, style, turn state, and repair strategy, then write `state/communication.json`.

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
