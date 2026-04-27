#!/usr/bin/env python3
"""Deterministic health updater for social-human simulation skills."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default
    return data if isinstance(data, dict) else default


def parse_payload() -> dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--args-json", type=str, default="{}")
    args = parser.parse_args()
    try:
        payload = json.loads(args.args_json)
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    return payload


def main() -> int:
    payload = parse_payload()

    work_dir = Path(payload.get("work_dir", ".")).resolve()
    state_dir = work_dir / "state"
    state_dir.mkdir(parents=True, exist_ok=True)

    prev_health = load_json(state_dir / "health.json", {})
    physiology = load_json(state_dir / "physiology.json", {})

    tick = int(payload.get("current_tick", int(prev_health.get("tick", 0)) + 1))
    iso_time = str(payload.get("time") or datetime.now(timezone.utc).isoformat())

    sleep_pressure = clamp(float(physiology.get("sleep_pressure", payload.get("sleep_pressure", 0.4))))
    fatigue = clamp(float(physiology.get("fatigue", payload.get("fatigue", 0.35))))
    stress_load = clamp(float(physiology.get("stress_load", payload.get("stress_load", 0.3))))
    pain = clamp(float(payload.get("pain", physiology.get("pain", prev_health.get("acute_symptoms", {}).get("pain", 0.0)))))
    illness = clamp(float(payload.get("illness", physiology.get("illness", prev_health.get("acute_symptoms", {}).get("illness", 0.0)))))

    acute_prev = prev_health.get("acute_symptoms", {})
    chronic_prev = prev_health.get("chronic_factors", {})

    fitness = clamp(float(payload.get("fitness", chronic_prev.get("fitness", 0.5))))
    recovery_capacity = clamp(float(payload.get("recovery_capacity", chronic_prev.get("recovery_capacity", 0.6))))
    stress_burden_prev = clamp(float(chronic_prev.get("stress_burden", 0.3)))

    events = payload.get("events", [])
    if not isinstance(events, list):
        events = []
    ev = {str(e).strip().lower() for e in events if str(e).strip()}

    if "exercise" in ev or "workout" in ev:
        fitness = clamp(fitness + 0.02)
        recovery_capacity = clamp(recovery_capacity + 0.01)
    if "poor_sleep" in ev:
        recovery_capacity = clamp(recovery_capacity - 0.015)
    if "social_support" in ev:
        stress_burden_prev = clamp(stress_burden_prev - 0.02)
    if "conflict" in ev or "deadline" in ev:
        stress_burden_prev = clamp(stress_burden_prev + 0.02)

    stress_burden = clamp(0.75 * stress_burden_prev + 0.25 * stress_load)

    allostatic_load = clamp(
        0.28 * stress_burden
        + 0.22 * sleep_pressure
        + 0.18 * fatigue
        + 0.16 * illness
        + 0.16 * pain
    )

    recovery_score = clamp(0.45 * recovery_capacity + 0.3 * (1.0 - stress_burden) + 0.25 * (1.0 - fatigue))

    overall_health = clamp(
        0.38 * (1.0 - allostatic_load)
        + 0.22 * (1.0 - illness)
        + 0.15 * (1.0 - pain)
        + 0.15 * fitness
        + 0.1 * recovery_score
    )

    appetite_modifier = clamp(-0.25 * illness - 0.15 * pain + 0.1 * fitness, -1.0, 1.0)
    mobility_limit = clamp(0.5 * pain + 0.35 * fatigue + 0.15 * illness)
    social_withdrawal = clamp(0.4 * stress_burden + 0.35 * fatigue + 0.25 * illness)
    perceived_control_modifier = clamp(-(0.45 * stress_burden + 0.3 * fatigue + 0.25 * pain), -1.0, 1.0)

    health = {
        "tick": tick,
        "time": iso_time,
        "overall_health": round(overall_health, 3),
        "allostatic_load": round(allostatic_load, 3),
        "acute_symptoms": {
            "pain": round(pain, 3),
            "illness": round(illness, 3),
            "nausea": round(clamp(float(acute_prev.get("nausea", 0.0))), 3),
        },
        "chronic_factors": {
            "fitness": round(fitness, 3),
            "stress_burden": round(stress_burden, 3),
            "recovery_capacity": round(recovery_capacity, 3),
        },
        "behavior_effects": {
            "mobility_limit": round(mobility_limit, 3),
            "appetite_modifier": round(appetite_modifier, 3),
            "social_withdrawal": round(social_withdrawal, 3),
            "perceived_control_modifier": round(perceived_control_modifier, 3),
        },
        "notes": [
            "Deterministic health baseline using allostatic load style aggregation.",
            "Use LLM refinement for symptom narrative and edge cases.",
        ],
    }

    (state_dir / "health.json").write_text(json.dumps(health, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": True,
                "artifacts": ["state/health.json"],
                "tick": tick,
                "overall_health": health["overall_health"],
                "allostatic_load": health["allostatic_load"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
