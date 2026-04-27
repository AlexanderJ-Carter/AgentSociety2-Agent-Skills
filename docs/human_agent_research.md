# Human-Like Social Agent Research Notes

## What the Current Skills Already Cover

The copied skills already cover the core loop emphasized by modern generative-agent work:

- `observation`: gather situated perception from the simulated world.
- `memory`: store important experience traces and let unimportant memories decay.
- `cognition`: appraise the current situation into emotion and intention.
- `plan`: turn intentions into habitual or deliberate action.

This maps well to the Generative Agents architecture, which highlights observation, memory retrieval/reflection, and planning as critical for believable behavior.

## Research Signals

Relevant research directions:

- Generative Agents: believable agents store full experience traces, retrieve memories dynamically, reflect over them, and plan daily/social behavior.
- Cognitive architectures for bodies and minds: more realistic agents model both mental state and body state; physiological variables influence attention, goals, and action choice.
- ACT-R base-level learning: memory activation should reflect repeated presentations/retrievals, not only the original encoding time.
- Bandura-style self-efficacy: willingness to attempt a behavior depends on mastery experience, observed models, persuasion, and affective/physiological state, not just true ability.
- Appraisal theories of emotion: emotion can be approximated from novelty, pleasantness, goal conduciveness, coping potential, and norm compatibility checks.
- Moral judgment research: moral reactions are often fast and affective, but can be revised by deliberation, intent, role conflict, and consequences.
- Media psychology: source credibility, motivated reasoning, repetition/familiarity, and inoculation against misinformation shape belief uptake.
- Procedural justice: fair treatment by institutions affects legitimacy, trust, and voluntary compliance.
- Two-process sleep regulation: sleepiness is not just an `energy` number. It should combine homeostatic sleep pressure, which rises during wake and falls during sleep, with a circadian wake/sleep rhythm.
- Circadian appetite studies: hunger and appetite have endogenous rhythms; hunger can be lower in the biological morning and higher in the evening, independent of recent food intake.
- Social-norm agent-based modeling: social behavior is shaped by norms, roles, obligations, reputation, identity, and the observed behavior of peers, not only by private utility.

Useful references:

- Park et al., "Generative Agents: Interactive Simulacra of Human Behavior", 2023.
- McShane et al., "A Cognitive Architecture for Simulating Bodies and Minds", 2011.
- Anderson and Schooler, "Reflections of the Environment in Memory", 1991.
- Bandura, "Self-efficacy: Toward a unifying theory of behavioral change", 1977.
- Lally et al., "How are habits formed", 2010.
- Scherer, "Appraisal considered as a process of multilevel sequential checking", 2001.
- Ajzen, "The Theory of Planned Behavior", 1991.
- Haidt, "The emotional dog and its rational tail", 2001.
- Kunda, "The case for motivated reasoning", 1990.
- Tyler, "Why People Obey the Law", 1990/2006.
- Research on circadian and homeostatic regulation of sleep and cognitive performance.
- Scheer et al., "The Internal Circadian Clock Increases Hunger and Appetite in the Evening Independent of Food Intake and Other Behaviors", 2013.
- Agent-based social norms literature, including norm-driven enrollment and social identity dynamics.

## Skills to Add Next

### 1. Physiology

Purpose: maintain internal body state and expose need pressures to cognition and planning.

Recommended outputs:

- `state/physiology.json`
- `state/needs.json`
- `state/body_events.jsonl`

Core variables:

- `hunger`: derived from time since meal, meal size, meal quality, exertion, stress, and circadian appetite.
- `satiety`: rises after eating, decays nonlinearly, and depends on food properties.
- `thirst`: rises with time, exertion, temperature, salt intake, illness, and alcohol/caffeine.
- `sleep_pressure`: rises while awake and falls during sleep.
- `circadian_phase`: endogenous 24-hour oscillator shifted by light, sleep timing, and routine.
- `fatigue`: combines sleep pressure, physical exertion, cognitive load, illness, and stress.
- `stress_load`: accumulates under threat, overload, social conflict, and unmet needs; recovers with rest and safety.
- `pain_or_illness`: affects attention, movement, mood, appetite, and plan feasibility.

Key rule: do not model hunger as a simple linear value. Model it as a pressure:

```text
hunger_pressure =
  baseline_metabolic_need
  + time_since_meal_effect
  + circadian_appetite_effect
  + exertion_effect
  + stress_effect
  - satiety_effect
```

### 2. Sleep And Circadian Rhythm

Purpose: make daily behavior time-sensitive.

Recommended outputs:

- `state/sleep.json`
- `state/circadian.json`

Rules:

- `sleep_pressure` increases during wake and decreases during sleep.
- `circadian_alertness` follows an approximately 24-hour rhythm.
- `effective_energy` should be computed from sleep pressure, circadian alertness, recent exertion, and illness.
- Late-night decisions should show lower inhibition, lower patience, slower planning, and stronger routine bias.
- Chronotype should be per-agent: morning type, neutral, evening type.

### 3. Routine And Habit

Purpose: make agents less random and more life-like across days.

Recommended outputs:

- `state/routine.json`
- `state/habits.json`

Rules:

- Routines should constrain likely actions by time, day type, role, and location.
- Habits should have cue, routine, reward, strength, and last_performed.
- Repetition strengthens habit; disruption weakens or reschedules it.
- Strong habits should bias `plan` toward System 1 execution.

### 4. Social Relationship

Purpose: preserve social continuity beyond one-off conversations.

Recommended outputs:

- `state/relationships.json`
- `state/social_obligations.json`

Variables per other agent:

- familiarity
- trust
- liking
- obligation
- conflict
- status asymmetry
- last_interaction
- shared_history_tags

Rules:

- A relationship should update after each meaningful interaction.
- Trust changes slowly; emotion changes quickly.
- Unfulfilled promises should create obligations and reputational risk.
- Social closeness should affect conversation probability, help probability, and avoidance.

### 5. Norms And Roles

Purpose: represent behavior that is socially expected, not just personally useful.

Recommended outputs:

- `state/norms.json`
- `state/roles.json`

Rules:

- Roles define expected behaviors, responsibilities, and constraints.
- Norm pressure should influence intention selection through subjective norm.
- Norm violation should produce social risk, shame/guilt, or conflict depending on personality and witnesses.
- Different locations can activate different norms: workplace, home, restaurant, hospital, school, street.

### 6. Reflection And Belief Revision

Purpose: convert raw memory into stable self-knowledge and world beliefs.

Recommended outputs:

- `state/reflections.jsonl`
- `state/beliefs.json`
- `state/preferences.json`

Rules:

- Reflect periodically, not every tick.
- Summarize repeated patterns: "Alice often helps me", "I get tired after late shifts".
- Update beliefs only when evidence accumulates or a high-importance event occurs.
- Reflections should feed cognition, not replace raw memories.

### 7. Affordance And Constraint Assessment

Purpose: prevent impossible or unrealistic action choices.

Recommended outputs:

- `state/affordances.json`
- `state/constraints.json`

Factors:

- distance and travel time
- opening hours
- money
- weather
- queues and crowding
- physical fatigue
- social access
- legal or institutional rules

Rules:

- Plans should fail early if key constraints make them impossible.
- Feasibility should affect perceived control in `cognition`.

### 8. Economy And Material Life

Purpose: make work, consumption, and scarcity matter.

Recommended outputs:

- `state/resources.json`
- `state/budget.json`

Variables:

- cash
- recurring income
- recurring expenses
- inventory
- debt
- job schedule
- consumption preferences

Rules:

- Money scarcity should change food choice, travel choice, leisure choice, and stress.
- Work obligations should compete with sleep, social life, and health.

## Suggested Implementation Order

1. Add `physiology` first because it will improve hunger, energy, fatigue, sleep, and plan interruption.
2. Add `routine` next because daily rhythm makes behavior stable across ticks.
3. Add `social_relationship` and `norms` together because realistic social action needs both personal history and social expectation.
4. Add `reflection` after enough memory data exists.
5. Add `affordance` and `economy` once the environment exposes enough structured state.

## Minimal Physiology State Schema

```json
{
  "tick": 120,
  "time": "2026-04-27T18:30:00",
  "chronotype": "neutral",
  "circadian_phase": 18.5,
  "circadian_alertness": 0.62,
  "sleep_pressure": 0.48,
  "hunger_pressure": 0.71,
  "satiety": 0.22,
  "thirst": 0.55,
  "fatigue": 0.44,
  "stress_load": 0.31,
  "pain": 0.0,
  "illness": 0.0,
  "last_meal_tick": 78,
  "last_sleep_tick": 20,
  "notes": ["Evening circadian appetite is increasing hunger."]
}
```

## Minimal Rule For Hunger

Use a bounded continuous update per tick:

```text
satiety_next = clamp(satiety * decay - exertion_cost + meal_gain, 0, 1)
hunger_next = clamp(
  metabolic_rate * time_awake
  + circadian_appetite
  + exertion
  + stress_appetite_modifier
  - satiety_next,
  0,
  1
)
```

This keeps hunger dynamic, time-dependent, and tied to behavior instead of treating it as a manually assigned scalar.
