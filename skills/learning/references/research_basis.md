# Learning — Research Basis

This skill combines three pragmatic models: diminishing-return practice, retention decay, and Bandura self-efficacy.

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

## References

- Bandura, A. (1977). Self-efficacy: Toward a unifying theory of behavioral change.
- Bandura, A. (1997). *Self-Efficacy: The Exercise of Control*.
- Lally, P., van Jaarsveld, C. H. M., Potts, H. W. W., & Wardle, J. (2010). How are habits formed: Modelling habit formation in the real world. DOI: `10.1002/ejsp.674`.
- Ebbinghaus, H. (1885). *Memory: A Contribution to Experimental Psychology*.
