# Health Research Basis

## Model

Biopsychosocial health with allostatic load and recovery dynamics.

## Update Rule

```text
stress_burden_next = clamp(stress_burden + stressor_load - recovery, 0, 1)
recovery_capacity = clamp(sleep_quality + rest + support + fitness - illness_load, 0, 1)
overall_health = clamp(1 - weighted_sum(acute_symptoms, chronic_factors, stress_burden), 0, 1)
```

## Variables

- `overall_health`: broad health signal, `[0, 1]`.
- `acute_symptoms`: pain, illness, nausea, dizziness, fever, injury, each `[0, 1]`.
- `chronic_factors`: fitness, chronic condition burden, stress burden, recovery capacity, each `[0, 1]`.
- `behavior_effects`: mobility, appetite, social withdrawal, and perceived-control modifiers, usually `[-1, 1]`.

## Defaults

Health changes slowly unless observation or memory reports an acute event. Ordinary tiredness should usually stay in physiology rather than becoming illness.

## Sources

- Engel, G. L. (1977). The need for a new medical model.
- McEwen, B. S. (1998). Protective and damaging effects of stress mediators.
- WHO. (1948). Constitution of the World Health Organization.
