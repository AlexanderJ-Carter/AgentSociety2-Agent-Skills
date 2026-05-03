# Observation Research Basis

## Model

Situated cognition and perception-action coupling. The agent should reason from current perceptual grounding rather than only from static profile text.

## Update Rule

```text
observation_state = environment.observe(agent_id)
state/observation.txt = observation_state.stdout
state/observation_ctx.json = observation_state.ctx when available
```

## Variables

- `agent_id`: current simulated person.
- `stdout`: natural-language observation.
- `ctx`: structured world context such as location, time, nearby agents, nearby objects, and available actions.
- `status`: environment processing status.

## Defaults

If observation is unavailable, preserve a concise error or uncertainty note so later skills know the state is stale.

## Sources

- Suchman, L. A. (1987). *Plans and Situated Actions*.
- Hutchins, E. (1995). *Cognition in the Wild*.
- Clark, A. (1997). *Being There*.
