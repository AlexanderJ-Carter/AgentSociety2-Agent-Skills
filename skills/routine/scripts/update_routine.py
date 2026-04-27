#!/usr/bin/env python3
"""Deterministic routine and habit updater for social-human simulation skills."""

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


def parse_hour(payload: dict[str, Any], circadian: dict[str, Any]) -> float:
    hour = payload.get("hour")
    if hour is not None:
        try:
            return float(hour) % 24.0
        except (TypeError, ValueError):
            pass

    time_text = payload.get("clock_time") or circadian.get("clock_time")
    if isinstance(time_text, str) and ":" in time_text:
        hh, mm = time_text.split(":", 1)
        try:
            return (float(hh) + float(mm) / 60.0) % 24.0
        except ValueError:
            pass

    now = datetime.now(timezone.utc)
    return float(now.hour) + float(now.minute) / 60.0


def time_block(hour: float) -> str:
    if 5 <= hour < 9:
        return "morning"
    if 9 <= hour < 12:
        return "late_morning"
    if 12 <= hour < 14:
        return "noon"
    if 14 <= hour < 18:
        return "afternoon"
    if 18 <= hour < 22:
        return "evening"
    return "night"


def expected_activity(block: str, is_workday: bool) -> str:
    if block == "morning":
        return "commute or start work" if is_workday else "breakfast and home routine"
    if block == "late_morning":
        return "work or study" if is_workday else "errands"
    if block == "noon":
        return "lunch"
    if block == "afternoon":
        return "work tasks" if is_workday else "leisure or chores"
    if block == "evening":
        return "dinner or social/leisure"
    return "sleep or winding down"


def main() -> int:
    payload = parse_payload()

    work_dir = Path(payload.get("work_dir", ".")).resolve()
    state_dir = work_dir / "state"
    state_dir.mkdir(parents=True, exist_ok=True)

    prev_routine = load_json(state_dir / "routine.json", {})
    prev_habits = load_json(state_dir / "habits.json", {"habits": []})
    circadian = load_json(state_dir / "circadian.json", {})
    needs = load_json(state_dir / "needs.json", {})

    tick = int(payload.get("current_tick", int(prev_routine.get("tick", 0)) + 1))
    iso_time = str(payload.get("time") or datetime.now(timezone.utc).isoformat())

    hour = parse_hour(payload, circadian)
    block = time_block(hour)

    day_type = str(payload.get("day_type", prev_routine.get("day_type", "workday")))
    is_workday = day_type.lower() == "workday"
    expected = expected_activity(block, is_workday)

    chronotype = str(circadian.get("chronotype", payload.get("chronotype", "neutral"))).lower()
    chronotype_shift = 0.0
    if chronotype == "morning":
        chronotype_shift = 0.08 if hour < 20 else -0.08
    elif chronotype == "evening":
        chronotype_shift = -0.06 if hour < 11 else 0.06

    urgency = clamp(float(needs.get("urgency", payload.get("need_urgency", 0.3))))
    schedule_pressure = clamp(float(payload.get("schedule_pressure", prev_routine.get("schedule_pressure", 0.35))))
    schedule_pressure = clamp(0.65 * schedule_pressure + 0.2 * urgency + 0.15 * (0.5 - chronotype_shift))

    routine_fit = clamp(0.78 - 0.45 * urgency - 0.35 * schedule_pressure + chronotype_shift)

    habits = prev_habits.get("habits", [])
    if not isinstance(habits, list):
        habits = []

    active_habits: list[dict[str, Any]] = []
    for item in habits:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        cue = str(item.get("cue", "")).strip()
        strength = clamp(float(item.get("strength", 0.4)))
        last_tick = int(item.get("last_performed_tick", max(0, tick - 10)))

        if payload.get("performed_habit") == name:
            strength = clamp(strength + 0.03)
            last_tick = tick
        else:
            strength = clamp(strength - 0.004)

        active = block in cue.lower() or strength >= 0.65
        updated = {
            "name": name,
            "cue": cue,
            "strength": round(strength, 3),
            "last_performed_tick": last_tick,
        }
        if active:
            active_habits.append(updated)

    routine = {
        "tick": tick,
        "time": iso_time,
        "day_type": day_type,
        "current_time_block": block,
        "expected_activity": expected,
        "schedule_pressure": round(schedule_pressure, 3),
        "routine_fit": round(routine_fit, 3),
        "chronotype": chronotype,
        "active_habits": active_habits[:8],
        "deviation": {
            "is_deviating": bool(routine_fit < 0.45),
            "reason": "high_need_or_time_pressure" if routine_fit < 0.45 else "",
        },
        "notes": [
            "Deterministic routine baseline with chronotype and need pressure.",
            "Use LLM refinement for richer social/calendar context.",
        ],
    }

    habits_out = {
        "tick": tick,
        "habits": active_habits,
    }

    (state_dir / "routine.json").write_text(json.dumps(routine, ensure_ascii=False, indent=2), encoding="utf-8")
    (state_dir / "habits.json").write_text(json.dumps(habits_out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": True,
                "artifacts": ["state/routine.json", "state/habits.json"],
                "tick": tick,
                "time_block": block,
                "routine_fit": routine["routine_fit"],
            },
            ensure_ascii=False,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
