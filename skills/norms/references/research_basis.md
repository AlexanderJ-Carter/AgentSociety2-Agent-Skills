# Norms Research Basis

## Model

Social norms combine empirical expectations, normative expectations, role obligations, visibility, and sanction risk.

## Update Rule

```text
norm_pressure = clamp(
  empirical_expectation * 0.3
  + normative_expectation * 0.35
  + role_obligation * 0.2
  + witness_visibility * sanction_risk * 0.15,
  0,
  1
)
```

## Variables

- `active_roles`: roles currently applying to the agent.
- `active_norms`: expectations relevant to the setting.
- `pressure`: force of a norm, `[0, 1]`.
- `violation_risk`: chance a violation will be noticed or matter, `[0, 1]`.
- `witness_visibility`: how observable the behavior is, `[0, 1]`.
- `moral_emotion_risk`: shame and guilt risks, each `[0, 1]`.

## Defaults

Use setting and role first. If the norm is uncertain, mark it as low-confidence rather than hard-forbidden.

## Sources

- Bicchieri, C. (2006). *The Grammar of Society*.
- Cialdini, R. B., Reno, R. R., & Kallgren, C. A. (1990). A focus theory of normative conduct.
- Goffman, E. (1963). *Behavior in Public Places*.
