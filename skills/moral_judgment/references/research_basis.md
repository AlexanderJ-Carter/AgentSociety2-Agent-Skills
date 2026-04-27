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
