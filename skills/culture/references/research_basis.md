# Culture Research Basis

## Model

Culture is treated as shared meaning, scripts, values, norms, symbols, and practice rather than fixed stereotypes.

## Update Rule

```text
cultural_salience = max(place_signal, role_signal, ritual_signal, audience_signal)
misunderstanding_risk = clamp(context_uncertainty + value_conflict + language_gap + taboo_salience, 0, 1)
cultural_comfort = clamp(familiarity + fit_with_values - risk, 0, 1)
```

## Variables

- `active_context`: current place, group, role, ritual, or audience.
- `values_in_play`: values relevant to the current choice.
- `etiquette`: setting-specific behavior expectations.
- `taboos`: actions or topics likely to cause offense.
- `cultural_comfort`: confidence that behavior fits the setting, `[0, 1]`.
- `misunderstanding_risk`: likelihood of cross-cultural friction, `[0, 1]`.

## Defaults

When evidence is weak, record uncertainty and avoid broad group claims. Prefer observed local context over demographic assumptions.

## Sources

- Geertz, C. (1973). *The Interpretation of Cultures*.
- Hofstede, G. (1980). *Culture's Consequences*.
- Goffman, E. (1959). *The Presentation of Self in Everyday Life*.
