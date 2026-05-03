# Reflection Research Basis

## Model

Autobiographical memory abstraction, self-schema updating, and reflective learning from repeated evidence.

## Update Rule

```text
pattern_confidence = clamp(repetition_strength + emotional_weight + outcome_consistency - contradiction_penalty, 0, 1)
if pattern_confidence >= 0.65:
    append reflection
if pattern_confidence >= 0.75:
    update belief, preference, or self_concept
```

## Variables

- `repetition_strength`: how often the pattern appears, `[0, 1]`.
- `emotional_weight`: intensity of associated emotions, `[0, 1]`.
- `outcome_consistency`: consistency of consequences, `[0, 1]`.
- `contradiction_penalty`: strength of counter-evidence, `[0, 1]`.
- `confidence`: evidence-backed confidence for the reflection, `[0, 1]`.

## Defaults

Do not reflect every tick. Reflection should compress repeated evidence, not replace raw memory.

## Sources

- Conway, M. A., & Pleydell-Pearce, C. W. (2000). The construction of autobiographical memories.
- Markus, H. (1977). Self-schemata and processing information about the self.
- Kolb, D. A. (1984). *Experiential Learning*.
