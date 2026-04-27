# Relationship Modeling Basis

## Why this matters

Social continuity requires memory of interaction quality, not just immediate emotion.

## Evidence anchors

- Trust/cooperation and repeated-game findings: cooperation stabilizes with memory and reciprocity signals.
- Social norm and sanction literature: violations affect trust/reputation asymmetrically.
- Relationship science: familiarity and affect can change quickly, but trust/conflict usually move slower unless high-stakes events occur.

## Simulation translation

Per person:

- familiarity
- trust
- liking
- obligation
- conflict
- respect
- shared_history_tags

Update policy:

- map interaction type to bounded delta vector
- apply optional context-specific delta override
- cap values in [0, 1]
- append high-impact events to social_events stream

## Practical notes

- Keep trust/conflict inertia higher than liking.
- Encode promises, betrayal, and public conflict as high-impact transitions.
- Do not erase old history; compress with tags and last_interaction fields.
