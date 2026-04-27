---
name: moral_judgment
description: Appraise events through moral foundations, social intuition, deliberation, guilt, shame, anger, and repair tendencies.
script: scripts/update_moral_judgment.py
---

# Moral Judgment

## Purpose

Model the agent as a moral social person, not only a utility maximizer. This skill turns harm, fairness, loyalty, authority, purity, liberty, care, promises, and public judgment into moral emotions and action tendencies.

Research basis: `references/research_basis.md`.

## Internal Logic (One Sentence)

Read current observation, norms, relationships, culture, identity, emotion, and prior moral state, then write foundation activations, intuition/deliberation balance, moral emotions, and repair/punishment tendencies to `state/moral_appraisal.json`.

## Use When

Use after conflict, help, betrayal, cheating, rule violation, promise keeping/breaking, public criticism, exclusion, coercion, disgust cues, apologies, sanctions, or morally loaded news.

## Procedure

1. Read `state/observation.txt`, `state/norms.json`, `state/relationships.json`, `state/culture.json`, `state/identity.json`, `state/emotion.json`, and `state/moral_appraisal.json` if present.
2. Estimate activation for moral foundations:
   - care/harm
   - fairness/cheating
   - loyalty/betrayal
   - authority/subversion
   - sanctity/degradation
   - liberty/oppression
3. Determine whether the response is mostly intuitive, deliberative, or mixed.
4. Estimate moral emotions: guilt, shame, anger, disgust, compassion, admiration.
5. Write `state/moral_appraisal.json`.
6. Append `state/moral_events.jsonl` only for high-intensity moral events.

If deterministic baseline is preferred:

```bash
python skills/moral_judgment/scripts/update_moral_judgment.py --state-dir state --tick 120
```

## Model

This skill separates:

- **Moral intuition**: fast affective response, often driven by harm, disgust, betrayal, or public norm violation.
- **Moral deliberation**: slower reasoning about intent, context, proportionality, role obligations, and consequences.
- **Repair tendency**: apology, compensation, explanation, withdrawal, punishment, forgiveness, or norm enforcement.

## Write

Always write `state/moral_appraisal.json`.

## Output Schema

```json
{
  "_meta": {
    "skill": "moral_judgment",
    "purpose": "Current moral appraisal and moral action tendencies."
  },
  "_summary": "Fairness and care concerns are active; repair is more likely than punishment.",
  "foundations": {
    "care_harm": 0.72,
    "fairness_cheating": 0.64,
    "loyalty_betrayal": 0.2,
    "authority_subversion": 0.31,
    "sanctity_degradation": 0.1,
    "liberty_oppression": 0.18
  },
  "intuition_strength": 0.66,
  "deliberation_need": 0.54,
  "moral_emotions": {
    "guilt": 0.2,
    "shame": 0.34,
    "anger": 0.51,
    "compassion": 0.44,
    "disgust": 0.08,
    "admiration": 0.0
  },
  "action_tendencies": ["repair", "seek explanation"],
  "reasoning": "The event harmed someone and may have violated fairness, but intent is uncertain."
}
```

## Notes

- Do not make the agent morally perfect. People rationalize, avoid blame, follow groups, and care more about close others.
- Culture and identity can weight foundations differently, but avoid stereotyping. Use explicit profile/context evidence.
- Moral judgment should influence `cognition.subjective_norm`, `emotion`, and relationship trust/conflict.
