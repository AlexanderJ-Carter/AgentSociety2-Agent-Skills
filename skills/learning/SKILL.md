---
name: learning
description: Track skill learning, knowledge retention, self-efficacy, and practice-driven proficiency for human-like agents.
script: scripts/update_learning.py
---

# Learning

## Purpose

Maintain what the agent is learning: factual knowledge, procedural skills, confidence, and practice history. This skill makes agents improve through repeated practice, lose unused ability slowly, and act differently when they believe they can succeed.

Research basis: `references/research_basis.md`.

## Internal Logic (One Sentence)

Read recent observations, memory, plan outcomes, emotion, and prior `state/learning.json`, then update per-topic proficiency, retention, automaticity, self-efficacy, motivation need satisfaction, and review timing in `state/learning.json`.

## Use When

Use after studying, training, practicing a job task, receiving feedback, watching someone demonstrate a behavior, teaching others, making mistakes, or repeatedly performing the same action.

## Procedure

1. Read `state/observation.txt`, `state/memory.jsonl`, `state/plan_state.json`, `state/emotion.json`, `state/routine.json`, and `state/learning.json` if present.
2. Identify learning events:
   - direct practice or study
   - success/failure feedback
   - social demonstration by another person
   - encouragement or criticism
   - emotionally stressful practice
3. Update each relevant topic using bounded values in `[0, 1]`.
4. Track SDT motivation signals: autonomy, competence, relatedness, internalization, and amotivation risk.
5. Track spaced-review timing: target retention horizon, next review tick, and whether review is currently due.
6. Write `state/learning.json`.
7. Optionally append `state/learning_events.jsonl` for notable milestones.

If deterministic baseline is preferred:

```bash
python skills/learning/scripts/update_learning.py --state-dir state --tick 120
```

## Model

Use four coupled variables per topic:

| Field | Meaning |
|-------|---------|
| `proficiency` | How well the agent can perform the skill now |
| `retention` | How available the knowledge/skill is without re-study |
| `automaticity` | How habit-like or low-effort the behavior has become |
| `self_efficacy` | Belief that the agent can perform the task successfully |
| `motivation` | Autonomy, competence, relatedness, internalization, and amotivation risk |
| `review` | Spaced-review scheduling metadata |

Practice has diminishing returns:

```text
proficiency_next = proficiency + learning_rate * practice_quality * (1 - proficiency)
```

Unused knowledge decays slowly:

```text
retention_next = retention * exp(-ticks_since_practice / retention_strength)
```

Self-efficacy is not the same as proficiency. It changes through mastery, observed models, persuasion, and emotional state.

Motivation quality depends on basic psychological need satisfaction:

```text
autonomous_motivation = mean(autonomy, competence, relatedness, internalization)
amotivation_risk = 1 - autonomous_motivation
```

Spacing rule:

```text
next_review_tick = current_tick + max(1, round(target_retention_interval * spacing_ratio))
```

Use shorter intervals for soon-needed knowledge and longer intervals for long-term retention. Repeating immediately after a successful review has lower marginal gain than a well-spaced retrieval attempt.

## Write

Always write `state/learning.json`.

## Output Schema

```json
{
  "_meta": {
    "skill": "learning",
    "purpose": "Current knowledge, skill proficiency, practice history, and self-efficacy."
  },
  "_summary": "Cooking is improving through repeated practice; self-efficacy is moderate.",
  "topics": {
    "cooking": {
      "proficiency": 0.48,
      "retention": 0.77,
      "automaticity": 0.31,
      "self_efficacy": 0.56,
      "motivation": {
        "autonomy": 0.62,
        "competence": 0.56,
        "relatedness": 0.4,
        "internalization": 0.58,
        "amotivation_risk": 0.46
      },
      "review": {
        "target_retention_interval": 240,
        "spacing_ratio": 0.2,
        "next_review_tick": 168,
        "review_due": false
      },
      "practice_count": 7,
      "last_practice_tick": 120,
      "evidence": ["made dinner successfully"]
    }
  }
}
```

## Notes

- Keep learning domain-specific. A person can be confident at cooking and anxious about public speaking.
- Treat one failure as information, not permanent incompetence.
- Let stress lower immediate performance without necessarily lowering long-term proficiency.
- Feed high `self_efficacy` into `cognition.perceived_control` and low `self_efficacy` into avoidance or help-seeking.
- Treat autonomy as "endorsed by the agent's own values", not isolation from others. Cooperation and advice can still support autonomy.
- Relatedness should come from being understood, supported, or socially connected during learning.
