# Circadian Modeling Basis

## Why this matters

Human alertness, appetite, and sleep propensity are not static. They are shaped by at least two partially independent processes:

- Process S (homeostatic): sleep pressure increases while awake and decreases during sleep.
- Process C (circadian): an endogenous roughly 24-hour rhythm modulates alertness and sleep tendency.

## Evidence anchors

- Borbely's two-process framework for sleep regulation and later refinements in sleep science.
- Circadian appetite findings: internal clock increases hunger/appetite in evening independent of behavior context.
- Chronotype literature: morning/evening preference shifts peak performance and sleep timing.

## Simulation translation

Use bounded state variables in [0, 1]:

- sleep_pressure
- circadian_alertness
- circadian_appetite
- sleep_tendency
- effective_energy

Update template:

- sleep_pressure_next = clamp(sleep_pressure + wake_gain - sleep_recovery)
- circadian_alertness = f(clock_time, chronotype_shift)
- sleep_tendency = g(sleep_pressure, circadian_alertness)
- effective_energy = circadian_alertness - alpha * sleep_pressure - fatigue_modifier

## Practical notes

- This is a phenomenological approximation, not a clinical model.
- Keep chronotype as a per-agent latent trait, not a hard label for every behavior.
- Let social obligations and norms override biological tendency when needed, but record the resulting strain in fatigue/stress.
