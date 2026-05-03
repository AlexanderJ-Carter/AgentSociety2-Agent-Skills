# `moral_judgment`

Appraise events through moral foundations, social intuition, deliberation, guilt, shame, anger, and repair tendencies.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/moral_judgment/`
- 说明文件 / Skill file: `skills/moral_judgment/SKILL.md`
- 执行脚本 / Script baseline: `scripts/update_moral_judgment.py`
- 最近更新 / Last updated: `2026-04-27`
- 理论依据 / Research basis:
  - `skills/moral_judgment/references/research_basis.md`

## SKILL.md（原文）

```
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
```

## 理论依据 / Research Basis

### `research_basis.md`

# Moral Judgment — Research Basis

This skill uses moral foundations as a feature set and the social intuitionist model as a process model.

## Moral foundations

Moral Foundations Theory proposes several recurring domains of moral concern:

| Foundation | Violation pattern |
|------------|-------------------|
| Care / harm | suffering, protection, cruelty |
| Fairness / cheating | reciprocity, exploitation, unequal treatment |
| Loyalty / betrayal | group commitment, abandonment, betrayal |
| Authority / subversion | role obligations, disrespect, rule defiance |
| Sanctity / degradation | contamination, taboo, degradation |
| Liberty / oppression | coercion, domination, loss of autonomy |

For simulation, each foundation is a bounded activation in `[0, 1]`.

## Social intuition plus deliberation

Haidt's social intuitionist model argues that moral judgments are often fast, intuitive, and affect-laden, with reasoning sometimes used afterward to justify or revise the judgment.

Simulation translation:

```text
intuition_strength = max(foundation_activation, moral_emotion_intensity)
deliberation_need = uncertainty + role_conflict + consequence_severity + relationship_importance
```

Use intuition for immediate anger, disgust, guilt, shame, admiration, or compassion. Use deliberation when intent is unclear, rules conflict, or consequences are serious.

## Moral emotions

Moral emotions help connect judgment to behavior:

- guilt -> repair, apology, compensation
- shame -> hiding, withdrawal, reputation management
- anger -> confrontation, punishment, norm enforcement
- compassion -> helping
- disgust -> avoidance, rejection
- admiration -> affiliation, imitation

## References

- Haidt, J. (2001). The emotional dog and its rational tail: A social intuitionist approach to moral judgment.
- Graham, J., Haidt, J., & Nosek, B. A. (2009). Liberals and conservatives rely on different sets of moral foundations.
- Haidt, J. (2012). *The Righteous Mind*.
- Kohlberg, L. (1981). *Essays on Moral Development*.
