# `civic_institution`

Track institutional encounters, procedural justice, legitimacy, compliance, service access, and civic trust.

本页由 `scripts/generate_skill_catalog.py` 自动生成。不要手工编辑。

This page is generated from the skill folder. It includes the executable skill instructions and any bundled research notes.

## 快速查看 / Quick View

- 技能目录 / Skill folder: `skills/civic_institution/`
- 说明文件 / Skill file: `skills/civic_institution/SKILL.md`
- 理论依据 / Research basis:
  - `skills/civic_institution/references/research_basis.md`

## SKILL.md（原文）

```
---
name: civic_institution
description: Track institutional encounters, procedural justice, legitimacy, compliance, service access, and civic trust.
script: scripts/update_civic_institution.py
---

# Civic Institution

## Purpose

Model how agents interact with institutions such as government offices, schools, hospitals, courts, police, employers, landlords, banks, and public services. Institutions shape compliance, trust, rights, obligations, access, and stress.

Research basis: `references/research_basis.md`.

## Internal Logic (One Sentence)

Read observation, norms, economy, identity, relationships, health, and prior institution state, then update institutional trust, procedural justice, access barriers, compliance pressure, and service outcomes in `state/institutions.json`.

## Use When

Use when the agent encounters bureaucracy, public services, policing, school rules, workplace authority, healthcare systems, legal obligations, welfare benefits, voting, permits, debt collection, rent, or institutional discrimination.

## Procedure

1. Read `state/observation.txt`, `state/norms.json`, `state/economy.json`, `state/identity.json`, `state/health.json`, `state/relationships.json`, and `state/institutions.json` if present.
2. Identify the institution and role:
   - patient, student, employee, tenant, citizen, customer, suspect, applicant, parent, client
3. Estimate:
   - procedural justice
   - access barriers
   - legitimacy/trust
   - compliance pressure
   - perceived rights and obligations
   - service outcome
4. Write `state/institutions.json`.
5. Append `state/institution_events.jsonl` for high-stakes encounters.

If deterministic baseline is preferred:

```bash
python skills/civic_institution/scripts/update_civic_institution.py --state-dir state --tick 120
```

## Model

Procedural justice is treated as a major driver of legitimacy:

```text
procedural_justice = voice + neutrality + respect + trustworthy_motives
legitimacy_next = legitimacy + learning_rate * (procedural_justice - legitimacy)
```

Access barriers raise stress and lower perceived control:

```text
access_barrier = cost + paperwork + wait_time + discrimination_risk + transport_or_health_limit
```

## Write

Always write `state/institutions.json`.

## Output Schema

```json
{
  "_meta": {
    "skill": "civic_institution",
    "purpose": "Current institutional trust, access, obligations, and compliance context."
  },
  "_summary": "Hospital access is possible but waiting and cost barriers are high.",
  "active_institution": "hospital",
  "role": "patient",
  "procedural_justice": 0.58,
  "legitimacy": 0.62,
  "institutional_trust": {
    "hospital": 0.62,
    "police": 0.41,
    "employer": 0.55
  },
  "access_barriers": {
    "cost": 0.46,
    "paperwork": 0.31,
    "wait_time": 0.72,
    "discrimination_risk": 0.12,
    "transport_or_health_limit": 0.2
  },
  "compliance_pressure": 0.68,
  "rights_or_entitlements": ["ask for explanation"],
  "obligations": ["wait for registration"],
  "service_outcome": "pending"
}
```

## Notes

- Institutions are not just locations. They create rules, paperwork, waiting, gatekeeping, legitimacy, and unequal access.
- Bad treatment should affect future institutional trust and willingness to comply or seek help.
- High legitimacy can increase voluntary compliance even when enforcement is weak.
```

## 理论依据 / Research Basis

### `research_basis.md`

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
