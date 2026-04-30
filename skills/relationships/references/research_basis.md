# Relationship Modeling Basis

## Why this matters

Social continuity requires memory of interaction quality, not just immediate emotion.

## Evidence anchors

- Trust/cooperation and repeated-game findings: cooperation stabilizes with memory and reciprocity signals.
- Social norm and sanction literature: violations affect trust/reputation asymmetrically.
- Relationship science: familiarity and affect can change quickly, but trust/conflict usually move slower unless high-stakes events occur.
- DeGroot consensus: repeated weighted averaging of opinions can converge to a shared estimate when the social influence network is suitably connected and weights are stable.

## Simulation translation

Per person:

- familiarity
- trust
- liking
- obligation
- conflict
- respect
- influence_weight for opinion exchange and consensus pressure
- shared_history_tags

Update policy:

- map interaction type to bounded delta vector
- apply optional context-specific delta override
- cap values in [0, 1]
- append high-impact events to social_events stream
- when opinions are exchanged, set `influence_weight` from trust, familiarity, respect, expertise cues, and conflict:

```text
influence_weight = clamp(0.35 * trust + 0.25 * respect + 0.2 * familiarity + 0.2 * expertise_hint - 0.25 * conflict)
```

If several people advise the agent on the same uncertain claim, downstream skills can use:

```text
opinion_next = sum(weight_i * opinion_i) / sum(weight_i)
```

Keep this as a local influence signal; avoid forcing consensus when the group is polarized, disconnected, coercive, or when identity-protective reasoning dominates.

## Practical notes

- Keep trust/conflict inertia higher than liking.
- Encode promises, betrayal, and public conflict as high-impact transitions.
- Do not erase old history; compress with tags and last_interaction fields.

## References

- DeGroot, M. H. (1974). Reaching a consensus. *Journal of the American Statistical Association*, 69(345), 118-121. DOI: `10.1080/01621459.1974.10480137`.
