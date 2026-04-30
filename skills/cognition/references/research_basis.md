# Cognition Modeling Basis

## Why this matters

Intentions in social settings are rarely pure utility maximization. They are influenced by attitudes, social pressure, perceived control, and current affective state.

## Evidence anchors

- Theory of Planned Behavior (Ajzen): intention is shaped by attitude, subjective norm, and perceived behavioral control.
- Bounded rationality (Simon): choice under limited information and computation often uses satisficing rather than global optimization.
- Heuristics and biases (Tversky & Kahneman): representativeness, availability, and anchoring are efficient shortcuts that can systematically bias judgment under uncertainty.
- Meta-analytic support: TPB predicts many social/health behaviors with moderate effect sizes.
- Emotion-cognition interaction literature: affect shifts risk perception, confidence, and action tendency.
- Scherer Component Process Model (CPM): emotion differentiation can be modeled as repeated appraisal checks over relevance, implications, coping potential, and normative significance.

## Simulation translation

### Appraisal state

Use bounded appraisal variables in `[0, 1]`:

| Variable | Meaning | Typical inputs |
|----------|---------|----------------|
| `novelty` | unexpectedness / unfamiliarity | observation keywords, new agents, sudden events |
| `pleasantness` | intrinsic positive/negative tone | success, help, comfort, threat, conflict |
| `goal_conduciveness` | whether the event helps current goals | plan state, obstacles, success/failure |
| `urgency` | need for immediate response | needs, danger, deadlines |
| `perceived_control` | controllability / coping potential | affordances, money, health, blocked actions |
| `norm_pressure` | external standards and sanctions | norms, witnesses, role obligations |
| `norm_violation_risk` | risk of shame/guilt/sanction | forbidden actions, moral emotion risk |

### Emotion update

The script maps appraisal to six intensity dimensions:

```text
fear    ~= threat + urgency - perceived_control
anger   ~= conflict + blocked goal - perceived_control
sadness ~= unpleasantness + social disconnection
joy     ~= pleasantness + goal conduciveness
surprise ~= novelty
disgust ~= norm violation / contamination cues
```

Then it applies continuity:

```text
emotion_next = clamp(previous +/- max_delta_per_tick)
```

This prevents single-tick emotional jumps unless the LLM has strong contextual evidence to override the baseline.

### Intention scoring

For each candidate intention:

- base_attitude in [0, 1]
- subjective_norm in [0, 1]
- perceived_control in [0, 1]
- apply emotion modifiers to attitude/control
- final_score = weighted sum

Then output only top candidate with brief reasoning.

### Bounded search and heuristics

Use a two-stage decision policy when context is uncertain:

1. Generate a small candidate set from needs, affordances, routines, relationships, and memories.
2. If the decision is routine, urgent, low-stakes, or cognitively loaded, accept the first feasible candidate whose score clears `aspiration_level`.
3. If the decision is novel, high-stakes, morally loaded, or institutionally risky, compare candidates more deliberately.

Represent common judgment shortcuts explicitly:

| Heuristic | Simulation signal | Bias risk |
|---|---|---|
| Representativeness | current case resembles a known category or prior episode | base rates may be ignored |
| Availability | recent, vivid, emotional, or frequently retrieved memory is easy to recall | probability may be overestimated |
| Anchoring | prior estimate, first price, first plan, or social suggestion is present | adjustment may be insufficient |

These fields should be logged as biasing influences, not treated as verified facts.

## Practical notes

- Preserve continuity: do not allow huge emotion swings without a major event.
- Separate immediate emotion and slower mood components.
- Let hard constraints from affordance/economy lower perceived_control.

## References

- Ajzen, I. (1991). The theory of planned behavior. *Organizational Behavior and Human Decision Processes*.
- Simon, H. A. (1955). A behavioral model of rational choice. *The Quarterly Journal of Economics*, 69(1), 99-118. DOI: `10.2307/1884852`.
- Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124-1131. DOI: `10.1126/science.185.4157.1124`.
- Scherer, K. R. (2001). Appraisal considered as a process of multilevel sequential checking. In *Appraisal Processes in Emotion*.
- Ortony, A., Clore, G. L., & Collins, A. (1988). *The Cognitive Structure of Emotions*.
