# Physiology Modeling Basis

## Why this matters

Believable social agents should not use a single static hunger or energy counter. Human body signals interact with rhythm, activity, stress, and health.

## Evidence anchors

- Homeostatic control and allostatic load concepts: stress and demand reshape physiological regulation.
- Sleep-pressure and circadian interaction affects fatigue and self-control.
- Appetite and hydration are context-sensitive and partially rhythmic.

## Simulation translation

Maintain continuous pressures in [0, 1]:

- hunger_pressure
- satiety
- thirst
- fatigue
- stress_load
- pain
- illness

Recommended structure:

- satiety_next = clamp(satiety * decay + meal_gain - exertion_cost)
- hunger_pressure = weighted(time_since_meal, circadian_appetite, exertion, stress, satiety)
- fatigue = weighted(sleep_pressure, exertion, stress, illness, pain)

Need projection (for cognition/plan):

- current_need from minimum satisfaction dimension
- urgency = 1 - satisfaction[current_need]
- interrupt_plan true only under high urgency/critical thresholds

## Practical notes

- Keep fast variables (hunger/thirst) and slow variables (illness/chronic stress) distinct.
- Avoid binary states when uncertain; write uncertainty notes rather than forcing extreme values.
