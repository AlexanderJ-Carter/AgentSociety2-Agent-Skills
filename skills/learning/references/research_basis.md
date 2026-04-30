# Learning — Research Basis

This skill combines five pragmatic models: diminishing-return practice, retention decay, spacing effects, Bandura self-efficacy, and self-determination theory.

## Diminishing-return practice

For simulation, practice should improve ability quickly at first and slowly near mastery:

\[
P_{next}=P + \alpha q (1-P)
\]

- \(P\): proficiency in `[0, 1]`
- \(\alpha\): learning rate
- \(q\): practice quality in `[0, 1]`

This is not a full cognitive tutor model; it is a stable baseline for tick-based agents.

## Retention decay

Unused knowledge and skills become less available:

\[
R(t)=R_0 \exp(-t/S)
\]

- \(R\): retention in `[0, 1]`
- \(t\): ticks since practice
- \(S\): retention strength

This intentionally mirrors the memory skill so knowledge availability and autobiographical memory decay in compatible ways.

## Spaced practice and review timing

Distributed practice is usually better than massed repetition for long-term retention. The useful gap depends on the desired retention interval: the farther away the final use/test is, the longer the review gap should generally be.

Simulation policy:

```text
target_retention_interval = ticks until likely use, or a long-term default
spacing_ratio = 0.1 to 0.3 for a conservative baseline
next_review_tick = current_tick + round(target_retention_interval * spacing_ratio)
```

Rules:

- If the topic is needed soon, review sooner.
- If the topic is meant to last, use longer gaps.
- If recall succeeds after a gap, increase retention and allow a longer next interval.
- If recall fails, shorten the next interval and lower self-efficacy slightly.
- If the same material was just reviewed successfully, immediate repetition has low marginal gain.

## Habit automaticity

Lally et al. (2010) found that automaticity in everyday habits tends to increase nonlinearly toward an asymptote, with large individual variation. We approximate this as:

\[
A_{next}=A + \beta c (1-A)
\]

- \(A\): automaticity in `[0, 1]`
- \(c\): context consistency in `[0, 1]`
- \(\beta\): automaticity learning rate

One missed opportunity should not reset the habit; it only slows growth.

## Self-efficacy

Bandura's self-efficacy theory says confidence depends on four sources:

1. Mastery experiences: direct success or failure.
2. Vicarious experiences: seeing similar others succeed.
3. Social persuasion: encouragement, criticism, instruction.
4. Physiological/affective state: anxiety, fatigue, calm, enthusiasm.

Simulation update:

\[
E_{next}=clamp(E + mastery + vicarious + persuasion + affect)
\]

Self-efficacy should influence perceived control, persistence, and willingness to try.

## Self-determination theory

Ryan and Deci's self-determination theory treats high-quality motivation as depending on three basic psychological needs:

- autonomy: the agent experiences the action as self-endorsed or value-congruent
- competence: the agent feels able to make progress
- relatedness: the agent feels understood, accepted, or supported

For simulation, store these as bounded topic-specific values:

```text
autonomous_motivation = mean(autonomy, competence, relatedness, internalization)
amotivation_risk = 1 - autonomous_motivation
```

External demands can still produce stable motivation if they become internalized. Criticism, coercion, repeated failure, or isolation should raise amotivation risk; choice, clear feedback, support, and visible progress should lower it.

## References

- Bandura, A. (1977). Self-efficacy: Toward a unifying theory of behavioral change.
- Bandura, A. (1997). *Self-Efficacy: The Exercise of Control*.
- Lally, P., van Jaarsveld, C. H. M., Potts, H. W. W., & Wardle, J. (2010). How are habits formed: Modelling habit formation in the real world. DOI: `10.1002/ejsp.674`.
- Ebbinghaus, H. (1885). *Memory: A Contribution to Experimental Psychology*.
- Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist*, 55(1), 68-78. DOI: `10.1037/0003-066X.55.1.68`.
- Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin*, 132(3), 354-380. DOI: `10.1037/0033-2909.132.3.354`.
- Cepeda, N. J., Vul, E., Rohrer, D., Wixted, J. T., & Pashler, H. (2008). Spacing effects in learning: A temporal ridgeline of optimal retention. *Psychological Science*, 19(11), 1095-1102. DOI: `10.1111/j.1467-9280.2008.02209.x`.
