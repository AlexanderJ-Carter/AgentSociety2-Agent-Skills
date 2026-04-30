---
name: relationships
description: Update interpersonal familiarity, trust, liking, obligation, conflict, and shared history.
script: scripts/update_relationships.py
---

# Relationships

## Purpose

Maintain social continuity between agents. This skill turns repeated interaction into relationship state instead of treating every encounter as new.

Research basis: `references/research_basis.md`.

## Internal Logic (One Sentence)

Read recent social interaction and prior relationship state, update bounded familiarity, trust, liking, obligation, conflict, respect, and optional opinion-influence weights, then write `state/relationships.json` and notable social events.

## Use When

Use this skill after conversations, cooperation, conflict, promises, favors, gifts, avoidance, betrayal, or repeated co-presence.

## Procedure

1. Read `state/observation.txt`, `state/observation_ctx.json`, `state/relationships.json`, `state/memory.jsonl`, `state/emotion.json`, and profile context if present.
2. Identify people involved and what happened.
3. Update familiarity, trust, liking, obligation, conflict, respect, and last interaction.
4. Add or revise shared history tags.
5. If agents exchanged opinions, update a lightweight influence weight: repeated trust and expertise increase weight; betrayal, conflict, or low credibility decrease it.
6. Write relationship state. If the event is notable, append a social memory through the memory skill or directly to `state/social_events.jsonl`.

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
      "influence_weight": 0.34,
      "last_interaction": "brief friendly chat at cafe",
      "shared_history_tags": ["cafe", "work"]
    }
  }
}
```

## Notes

Trust and conflict should change more slowly than momentary emotion. A single event can strongly affect a relationship only if it is high-stakes, public, repeated, or identity-relevant.

Consensus note: if multiple trusted people provide opinions about the same uncertain issue, later `cognition` or `media_literacy` can average those opinions using relationship influence weights. This follows DeGroot-style consensus as a simple social influence baseline, not as a claim that real groups always converge.
