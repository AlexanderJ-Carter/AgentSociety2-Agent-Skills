# Civic Institution — Research Basis

This skill uses procedural justice and institutional trust as the main simulation handles.

## Procedural justice

Procedural justice research, especially Tyler's work, emphasizes that people are more likely to view authorities as legitimate and comply voluntarily when procedures feel fair.

Core components:

| Component | Meaning |
|-----------|---------|
| Voice | The person can explain their side |
| Neutrality | Decisions appear unbiased and rule-based |
| Respect | The person is treated with dignity |
| Trustworthy motives | Authorities appear sincere and not exploitative |

Simulation:

\[
PJ = mean(voice, neutrality, respect, trustworthy\_motives)
\]

\[
legitimacy_{next}=legitimacy+\alpha(PJ-legitimacy)
\]

## Access barriers

Institutional access often depends on more than eligibility. Waiting, cost, paperwork, transport, language, stigma, and discrimination risk affect whether a person uses services.

```text
access_barrier = weighted_sum(cost, paperwork, wait_time, discrimination_risk, transport_or_health_limit)
```

High barriers should lower `perceived_control` and raise stress.

## Compliance pressure

Compliance may come from:

- legitimacy: "this rule is rightful"
- sanction risk: "I may be punished"
- dependency: "I need the service/job/benefit"
- norms: "people expect me to comply"

Voluntary compliance should be more stable than fear-only compliance.

## References

- Tyler, T. R. (1990). *Why People Obey the Law*.
- Tyler, T. R. (2006). *Why People Obey the Law* (revised edition).
- Lipsky, M. (1980). *Street-Level Bureaucracy*.
- Levi, M. & Stoker, L. (2000). Political trust and trustworthiness.
