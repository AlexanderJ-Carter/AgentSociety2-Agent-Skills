#!/usr/bin/env python3
"""Deterministic affordance updater for social-human simulation skills."""

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

    economy = load_json(state_dir / "economy.json", {})
    physiology = load_json(state_dir / "physiology.json", {})
    health = load_json(state_dir / "health.json", {})

    tick = int(payload.get("current_tick", int(load_json(state_dir / "affordances.json", {}).get("tick", 0)) + 1))
    iso_time = str(payload.get("time") or datetime.now(timezone.utc).isoformat())

    cash = float(economy.get("cash", payload.get("cash", 0.0)))
    fatigue = clamp(float(physiology.get("fatigue", payload.get("fatigue", 0.35))))
    stress = clamp(float(physiology.get("stress_load", payload.get("stress", 0.3))))
    pain = clamp(float(health.get("acute_symptoms", {}).get("pain", payload.get("pain", 0.0))))

    distance = float(payload.get("distance_to_goal", 1.2))
    queue = int(payload.get("queue_length", 3))
    has_access = bool(payload.get("has_access", True))

    feasible_actions = ["wait", "observe", "talk_to_nearby_agent"]
    costly_actions: list[dict[str, Any]] = []
    blocked_actions: list[dict[str, Any]] = []
    risks: list[dict[str, Any]] = []

    if has_access:
        feasible_actions.append("enter_location")
    else:
        blocked_actions.append({"action": "enter_location", "reason": "no_access_or_closed"})

    if distance <= 2.5 and fatigue < 0.8 and pain < 0.7:
        feasible_actions.append("walk_to_target")
    else:
        risks.append(
            {
                "action": "walk_to_target",
                "risk": "fatigue_or_distance_overload",
                "severity": round(clamp(0.5 * fatigue + 0.3 * pain + 0.2 * min(distance / 5.0, 1.0)), 3),
            }
        )

    if cash >= 20:
        feasible_actions.append("buy_basic_meal")
    else:
        blocked_actions.append({"action": "buy_basic_meal", "reason": "insufficient_cash"})

    if cash >= 70:
        feasible_actions.append("take_taxi")
    else:
        costly_actions.append({"action": "take_taxi", "cost_type": "money", "severity": round(clamp((70 - cash) / 70), 3)})

    if queue > 6:
        costly_actions.append({"action": "wait_for_service", "cost_type": "time", "severity": round(clamp(queue / 12.0), 3)})

    if stress > 0.75:
        risks.append({"action": "start_conflictive_interaction", "risk": "escalation", "severity": round(clamp(stress), 3)})

    perceived_control_hint = clamp(0.75 - 0.28 * fatigue - 0.22 * stress - 0.2 * pain)

    affordances = {
        "tick": tick,
        "time": iso_time,
        "feasible_actions": sorted(set(feasible_actions)),
        "costly_actions": costly_actions,
        "blocked_actions": blocked_actions,
        "risks": risks,
        "perceived_control_hint": round(perceived_control_hint, 3),
        "notes": [
            "Deterministic affordance baseline with money/body/access/time constraints.",
            "Use LLM refinement for nuanced social affordance interpretation.",
        ],
    }

    (state_dir / "affordances.json").write_text(json.dumps(affordances, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": True,
                "artifacts": ["state/affordances.json"],
                "tick": tick,
                "feasible_count": len(affordances["feasible_actions"]),
            },
            ensure_ascii=False,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
