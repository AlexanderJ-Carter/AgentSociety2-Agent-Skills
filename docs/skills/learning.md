# `learning`

Track skill learning, knowledge retention, self-efficacy, and practice-driven proficiency for human-like agents.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/learning/`
- 说明文件 / Skill file: `skills/learning/SKILL.md`
- 理论依据 / Research basis:
  - `skills/learning/references/research_basis.md`

## SKILL.md（原文）

```
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

Read recent observations, memory, plan outcomes, emotion, and prior `state/learning.json`, then update per-topic proficiency, retention, automaticity, and self-efficacy in `state/learning.json`.

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
4. Write `state/learning.json`.
5. Optionally append `state/learning_events.jsonl` for notable milestones.

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

Practice has diminishing returns:

```text
proficiency_next = proficiency + learning_rate * practice_quality * (1 - proficiency)
```

Unused knowledge decays slowly:

```text
retention_next = retention * exp(-ticks_since_practice / retention_strength)
```

Self-efficacy is not the same as proficiency. It changes through mastery, observed models, persuasion, and emotional state.

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
```

## 理论依据 / Research Basis

### `research_basis.md`

# Learning — Research Basis

This skill combines three pragmatic models: diminishing-return practice, retention decay, and Bandura self-efficacy.

## Diminishing-return practice

For simulation, practice should improve ability quickly at first and slowly near mastery:

\[
P_{next}=P + \alpha q (1-P)
\]

- \(P\): proficiency in `[0, 1]`
- \(\alpha\): learning rate
- \(q\): practice quality in `[0, 1]`

This is not a full cognitive tutor model; it is a stable baseline for tick-based agents.

## Retention decay

Unused knowledge and skills become less available:

\[
R(t)=R_0 \exp(-t/S)
\]

- \(R\): retention in `[0, 1]`
- \(t\): ticks since practice
- \(S\): retention strength

This intentionally mirrors the memory skill so knowledge availability and autobiographical memory decay in compatible ways.

## Habit automaticity

Lally et al. (2010) found that automaticity in everyday habits tends to increase nonlinearly toward an asymptote, with large individual variation. We approximate this as:

\[
A_{next}=A + \beta c (1-A)
\]

- \(A\): automaticity in `[0, 1]`
- \(c\): context consistency in `[0, 1]`
- \(\beta\): automaticity learning rate

One missed opportunity should not reset the habit; it only slows growth.

## Self-efficacy

Bandura's self-efficacy theory says confidence depends on four sources:

1. Mastery experiences: direct success or failure.
2. Vicarious experiences: seeing similar others succeed.
3. Social persuasion: encouragement, criticism, instruction.
4. Physiological/affective state: anxiety, fatigue, calm, enthusiasm.

Simulation update:

\[
E_{next}=clamp(E + mastery + vicarious + persuasion + affect)
\]

Self-efficacy should influence perceived control, persistence, and willingness to try.

## References

- Bandura, A. (1977). Self-efficacy: Toward a unifying theory of behavioral change.
- Bandura, A. (1997). *Self-Efficacy: The Exercise of Control*.
- Lally, P., van Jaarsveld, C. H. M., Potts, H. W. W., & Wardle, J. (2010). How are habits formed: Modelling habit formation in the real world. DOI: `10.1002/ejsp.674`.
- Ebbinghaus, H. (1885). *Memory: A Contribution to Experimental Psychology*.
