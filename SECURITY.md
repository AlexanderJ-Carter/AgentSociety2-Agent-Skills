# Security Policy

## Supported Scope

This repository contains Claude Skill style instructions, documentation, deterministic baseline scripts, and static site assets for AgentSociety2-style simulations.

Security reports are in scope when they involve:

- A script or workflow that can execute unintended code or overwrite unexpected files.
- A documentation or example pattern that encourages leaking API keys, tokens, private workspace data, or real personal data.
- A supply-chain issue in the documentation build or generated site workflow.
- A vulnerability in generated files that would affect users who browse or deploy the static documentation site.

Out of scope:

- General disagreements with a social-science model or parameter choice.
- Simulation behavior that is unrealistic but not security-relevant.
- Vulnerabilities in downstream projects that copied and heavily modified these skills.

## Reporting a Vulnerability

Do not open a public issue for a security vulnerability.

Preferred reporting path:

1. Use GitHub private vulnerability reporting if it is enabled for this repository.
2. If private reporting is not enabled, contact the repository maintainer through the GitHub profile or an existing private channel.
3. Include a minimal reproduction, affected file paths, impact, and any suggested fix.

Please do not include real secrets, personal data, private simulation data, or exploit payloads beyond what is necessary to reproduce the issue.

## Response Expectations

Maintainers should acknowledge a valid report within a reasonable time, triage severity, and publish a fix or mitigation note when appropriate. This is a research-oriented skill repository, so response time may depend on maintainer availability.

## Handling Sensitive Simulation Data

Do not commit:

- API keys, tokens, private keys, passwords, or service credentials.
- Real personal identifiers, location traces, health records, financial records, or private messages.
- Private agent workspace dumps unless they are synthetic and scrubbed.

Use synthetic examples in `docs/`, `skills/*/references/`, and tests.

## Model and Safety Boundaries

Skills in this repository approximate human behavior for simulation. They are not medical, legal, financial, psychological, or public-policy advice. When adding or changing a skill, state modeling limits clearly and avoid presenting simplified formulas as exact human diagnosis or prediction.
