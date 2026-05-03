# Plan Research Basis

## Model

Dual-process action selection with bounded rationality, plus lightweight plan-state tracking for multi-step intentions.

## Update Rule

```text
if routine_or_urgent_known_action:
    decision_mode = "system1"
    execute one feasible action
else:
    decision_mode = "system2"
    create_or_continue plan_state with up to 6 steps
```

Interrupt plans when physiological need, safety, unavailable affordance, or changed intention crosses a threshold.

## Variables

- `decision_mode`: `system1` or `system2`.
- `plan_state.status`: `pending`, `in_progress`, `interrupted`, `completed`, or `failed`.
- `current_step`: active step index.
- `estimated_ticks`: rough plan duration.
- `interrupt_reason`: critical need, blocked action, external event, or changed intention.

## Defaults

Prefer one meaningful action per tick. If observation does not list a feasible action, wait, observe, or mark the plan blocked.

## Sources

- Kahneman, D. (2011). *Thinking, Fast and Slow*.
- Simon, H. A. (1955). A behavioral model of rational choice.
- Bratman, M. E. (1987). *Intention, Plans, and Practical Reason*.
