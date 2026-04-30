# `media_literacy`

Track information exposure, source credibility, motivated reasoning, misinformation risk, and belief-update resistance.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/media_literacy/`
- 说明文件 / Skill file: `skills/media_literacy/SKILL.md`
- 最近更新 / Last updated: `2026-04-27`
- 理论依据 / Research basis:
  - `skills/media_literacy/references/research_basis.md`

## SKILL.md（原文）

```
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
```

## 理论依据 / Research Basis

### `research_basis.md`

# Media Literacy — Research Basis

This skill combines source credibility, motivated reasoning, familiarity effects, and inoculation theory.

## Source credibility

People weigh information partly by perceived source expertise, trustworthiness, and institutional legitimacy. For simulation:

```text
source_credibility = expertise * trustworthiness * context_relevance
```

Unknown social posts, advertising, and forwarded rumors should start lower than direct observation, official records, or trusted experts.

## Motivated reasoning and identity alignment

People are more likely to accept information that fits prior beliefs, group identity, or desired conclusions. This is useful for simulation because two agents can see the same claim and update differently.

```text
identity_alignment in [0, 1]
acceptance += identity_alignment_bias
```

Do not let identity alignment override strong evidence automatically; it is a bias, not a truth rule.

## Familiarity and repetition

Repeated claims can feel more believable through familiarity. The script tracks approximate familiarity, but treats it separately from evidence quality.

## Inoculation / prebunking

Inoculation theory suggests that warning people about manipulation tactics and giving weakened examples can increase resistance to later misinformation.

Simulation translation:

```text
acceptance_tendency -= inoculation_strength
misinformation_risk += manipulation_tactic_flags
```

Useful tactic flags: urgency pressure, no source, conspiracy framing, emotional bait, fake authority, impossible certainty.

## References

- McGuire, W. J. (1964). Inducing resistance to persuasion.
- Petty, R. E. & Cacioppo, J. T. (1986). The elaboration likelihood model of persuasion.
- Kunda, Z. (1990). The case for motivated reasoning.
- Pennycook, G. & Rand, D. G. (2019). Lazy, not biased: Susceptibility to partisan fake news is better explained by lack of reasoning than by motivated reasoning.
- van der Linden, S., Leiserowitz, A., Rosenthal, S., & Maibach, E. (2017). Inoculating the public against misinformation about climate change.
