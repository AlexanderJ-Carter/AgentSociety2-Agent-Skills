#!/usr/bin/env python3
"""Deterministic physiology state updater for social-human simulation.

This script is intentionally lightweight and dependency-free so it can be called
from SkillRegistry script execution or from CLI for offline calibration.
"""

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


def parse_args() -> dict[str, Any]:
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


def activity_exertion(activity: str) -> float:
    table = {
        "sleeping": 0.0,
        "resting": 0.1,
        "sitting": 0.15,
        "walking": 0.35,
        "commuting": 0.4,
        "working": 0.5,
        "exercising": 0.8,
        "running": 0.95,
    }
    return table.get(activity.lower(), 0.3)


def main() -> int:
    payload = parse_args()

    work_dir = Path(payload.get("work_dir", ".")).resolve()
    state_dir = work_dir / "state"
    state_dir.mkdir(parents=True, exist_ok=True)

    prev = load_json(state_dir / "physiology.json", {})

    prev_tick = int(prev.get("tick", 0))
    tick = int(payload.get("current_tick", prev_tick + 1))
    iso_time = str(payload.get("time") or datetime.now(timezone.utc).isoformat())

    events_raw = payload.get("events", [])
    events = {str(e).strip().lower() for e in events_raw if str(e).strip()}

    recent_activity = str(payload.get("recent_activity", prev.get("recent_activity", "resting")))
    exertion = activity_exertion(recent_activity)

    circadian_appetite = clamp(float(payload.get("circadian_appetite", 0.5)))
    sleep_boost = clamp(float(payload.get("circadian_alertness", 0.5)))

    satiety_prev = clamp(float(prev.get("satiety", 0.5)))
    thirst_prev = clamp(float(prev.get("thirst", 0.3)))
    sleep_pressure_prev = clamp(float(prev.get("sleep_pressure", 0.4)))
    stress_prev = clamp(float(prev.get("stress_load", 0.3)))

    meal_gain = clamp(float(payload.get("meal_gain", 0.0)))
    drink_gain = clamp(float(payload.get("drink_gain", 0.0)))
    sleep_gain = clamp(float(payload.get("sleep_gain", 0.0)))

    if "eat" in events or "meal" in events:
        meal_gain = max(meal_gain, 0.35)
    if "drink" in events:
        drink_gain = max(drink_gain, 0.45)
    if "sleep" in events or "nap" in events:
        sleep_gain = max(sleep_gain, 0.55)

    satiety_decay = clamp(0.97 - 0.05 * exertion, 0.9, 0.99)
    satiety = clamp(satiety_prev * satiety_decay + meal_gain - 0.03 * exertion)

    thirst_rise = 0.012 + 0.03 * exertion
    if "heat" in events:
        thirst_rise += 0.02
    thirst = clamp(thirst_prev + thirst_rise - drink_gain)

    sleep_pressure_rise = 0.018 + 0.02 * exertion + 0.01 * (1.0 - sleep_boost)
    sleep_pressure = clamp(sleep_pressure_prev + sleep_pressure_rise - sleep_gain)

    stress_delta = 0.0
    if "threat" in events:
        stress_delta += 0.2
    if "conflict" in events:
        stress_delta += 0.12
    if "deadline" in events:
        stress_delta += 0.08
    if "rest" in events or "safe" in events:
        stress_delta -= 0.07
    stress_load = clamp(stress_prev + stress_delta)

    illness = clamp(float(payload.get("illness", prev.get("illness", 0.0))))
    pain = clamp(float(payload.get("pain", prev.get("pain", 0.0))))

    hunger_pressure = clamp(
        0.62 * (1.0 - satiety)
        + 0.18 * circadian_appetite
        + 0.12 * exertion
        + 0.08 * stress_load
    )

    fatigue = clamp(
        0.45 * sleep_pressure + 0.25 * exertion + 0.15 * stress_load + 0.1 * illness + 0.05 * pain
    )

    last_meal_tick = int(payload.get("last_meal_tick", prev.get("last_meal_tick", max(0, tick - 8))))
    last_drink_tick = int(payload.get("last_drink_tick", prev.get("last_drink_tick", max(0, tick - 3))))
    last_sleep_tick = int(payload.get("last_sleep_tick", prev.get("last_sleep_tick", max(0, tick - 16))))

    if meal_gain > 0.01:
        last_meal_tick = tick
    if drink_gain > 0.01:
        last_drink_tick = tick
    if sleep_gain > 0.01:
        last_sleep_tick = tick

    physiology = {
        "tick": tick,
        "time": iso_time,
        "hunger_pressure": round(hunger_pressure, 3),
        "satiety": round(satiety, 3),
        "thirst": round(thirst, 3),
        "sleep_pressure": round(sleep_pressure, 3),
        "fatigue": round(fatigue, 3),
        "stress_load": round(stress_load, 3),
        "pain": round(pain, 3),
        "illness": round(illness, 3),
        "recent_activity": recent_activity,
        "last_meal_tick": last_meal_tick,
        "last_drink_tick": last_drink_tick,
        "last_sleep_tick": last_sleep_tick,
        "notes": [
            "Bootstrap from deterministic physiology updater.",
            "Use LLM refinement for narrative/social context.",
        ],
    }

    satisfactions = {
        "satiety": round(1.0 - hunger_pressure, 3),
        "hydration": round(1.0 - thirst, 3),
        "energy": round(1.0 - fatigue, 3),
        "safety": round(clamp(1.0 - 0.65 * stress_load - 0.35 * pain), 3),
        "social": round(clamp(float(payload.get("social_need_satisfaction", 0.6))), 3),
    }

    action_map = {
        "satiety": "eat",
        "hydration": "drink",
        "energy": "rest",
        "safety": "seek_safety",
        "social": "connect",
    }
    current_need = min(satisfactions, key=satisfactions.get)
    urgency = round(1.0 - satisfactions[current_need], 3)

    needs = {
        "current_need": action_map[current_need],
        "urgency": urgency,
        "needs": satisfactions,
        "interrupt_plan": bool(
            urgency >= 0.82
            or hunger_pressure >= 0.88
            or thirst >= 0.88
            or fatigue >= 0.9
        ),
        "reasoning": "Deterministic baseline; refine with current observation and norms.",
    }

    (state_dir / "physiology.json").write_text(
        json.dumps(physiology, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (state_dir / "needs.json").write_text(
        json.dumps(needs, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "ok": True,
                "artifacts": ["state/physiology.json", "state/needs.json"],
                "tick": tick,
                "current_need": needs["current_need"],
                "urgency": urgency,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
