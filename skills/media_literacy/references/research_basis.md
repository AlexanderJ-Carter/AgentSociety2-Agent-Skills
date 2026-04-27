# Media Literacy — Research Basis

This skill combines source credibility, motivated reasoning, familiarity effects, and inoculation theory.

## Source credibility

People weigh information partly by perceived source expertise, trustworthiness, and institutional legitimacy. For simulation:

```text
source_credibility = expertise * trustworthiness * context_relevance
```

Unknown social posts, advertising, and forwarded rumors should start lower than direct observation, official records, or trusted experts.

## Motivated reasoning and identity alignment

People are more likely to accept information that fits prior beliefs, group identity, or desired conclusions. This is useful for simulation because two agents can see the same claim and update differently.

```text
identity_alignment in [0, 1]
acceptance += identity_alignment_bias
```

Do not let identity alignment override strong evidence automatically; it is a bias, not a truth rule.

## Familiarity and repetition

Repeated claims can feel more believable through familiarity. The script tracks approximate familiarity, but treats it separately from evidence quality.

## Inoculation / prebunking

Inoculation theory suggests that warning people about manipulation tactics and giving weakened examples can increase resistance to later misinformation.

Simulation translation:

```text
acceptance_tendency -= inoculation_strength
misinformation_risk += manipulation_tactic_flags
```

Useful tactic flags: urgency pressure, no source, conspiracy framing, emotional bait, fake authority, impossible certainty.

## References

- McGuire, W. J. (1964). Inducing resistance to persuasion.
- Petty, R. E. & Cacioppo, J. T. (1986). The elaboration likelihood model of persuasion.
- Kunda, Z. (1990). The case for motivated reasoning.
- Pennycook, G. & Rand, D. G. (2019). Lazy, not biased: Susceptibility to partisan fake news is better explained by lack of reasoning than by motivated reasoning.
- van der Linden, S., Leiserowitz, A., Rosenthal, S., & Maibach, E. (2017). Inoculating the public against misinformation about climate change.
