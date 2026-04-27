---
name: media_literacy
description: Track information exposure, source credibility, motivated reasoning, misinformation risk, and belief-update resistance.
script: scripts/update_media_literacy.py
---

# Media Literacy

## Purpose

Model how agents process claims from media, friends, institutions, ads, rumors, and social platforms. This skill prevents agents from instantly accepting every statement and makes belief change depend on source credibility, prior beliefs, identity alignment, repetition, and warning/inoculation.

Research basis: `references/research_basis.md`.

## Internal Logic (One Sentence)

Read observation, memory, relationships, identity, prior beliefs, and prior media state, then estimate claim credibility, misinformation risk, confirmation bias, inoculation strength, and write `state/media_literacy.json` plus optional belief update hints.

## Use When

Use after news exposure, social media posts, rumors, advertising, political claims, health claims, scams, institutional announcements, warnings, debunks, or repeated claims.

## Procedure

1. Read `state/observation.txt`, `state/memory.jsonl`, `state/relationships.json`, `state/identity.json`, `state/beliefs.json`, and `state/media_literacy.json` if present.
2. Identify the main claim or information item.
3. Estimate:
   - source credibility
   - evidence quality
   - repetition/familiarity
   - identity alignment
   - emotional arousal
   - misinformation risk
   - inoculation/prebunking strength
4. Write `state/media_literacy.json`.
5. Optionally write `state/belief_update_hints.json` for reflection/cognition to use.

If deterministic baseline is preferred:

```bash
python skills/media_literacy/scripts/update_media_literacy.py --state-dir state --tick 120
```

## Model

Belief uptake is not just evidence:

```text
acceptance_tendency =
  source_credibility
  + evidence_quality
  + familiarity
  + identity_alignment
  + emotional_arousal
  - misinformation_risk
  - inoculation_strength
```

The output should not directly rewrite stable beliefs unless evidence is strong. It should provide a hint for `reflection`.

## Write

Always write `state/media_literacy.json`.

Optionally write `state/belief_update_hints.json`.

## Output Schema

```json
{
  "_meta": {
    "skill": "media_literacy",
    "purpose": "Current information exposure assessment and belief-update caution."
  },
  "_summary": "A health claim from an unknown source has high misinformation risk.",
  "current_claim": "A viral post says the medicine is dangerous.",
  "source_type": "social_media",
  "source_credibility": 0.32,
  "evidence_quality": 0.18,
  "familiarity": 0.61,
  "identity_alignment": 0.44,
  "emotional_arousal": 0.7,
  "misinformation_risk": 0.78,
  "inoculation_strength": 0.35,
  "acceptance_tendency": 0.22,
  "recommended_stance": "withhold belief and seek corroboration"
}
```

## Notes

- Repetition increases familiarity, not truth.
- Trust in a friend should increase attention, but not automatically evidence quality.
- Strong identity alignment can increase acceptance even when evidence is weak.
- Debunking and prebunking should add resistance to later similar manipulation tactics.
