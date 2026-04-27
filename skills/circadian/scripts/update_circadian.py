#!/usr/bin/env python3
"""Deterministic circadian/sleep-process updater.

Implements a simple two-process style approximation:
- Process S: sleep pressure rises during wake, decays in sleep.
- Process C: circadian rhythm modulates alertness and appetite.
"""

from __future__ import annotations

import argparse
import json
import math
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


def parse_clock_time(payload: dict[str, Any], prev_phase_hour: float) -> tuple[str, float]:
    raw = payload.get("clock_time")
    if isinstance(raw, str) and ":" in raw:
        hh, mm = raw.split(":", 1)
        try:
            hour = int(hh)
            minute = int(mm)
            hour = max(0, min(23, hour))
            minute = max(0, min(59, minute))
            return f"{hour:02d}:{minute:02d}", hour + minute / 60.0
        except ValueError:
            pass

    now = datetime.now(timezone.utc)
    if payload.get("use_utc_now", True):
        return now.strftime("%H:%M"), now.hour + now.minute / 60.0
    return f"{int(prev_phase_hour)%24:02d}:00", float(prev_phase_hour % 24)


def chronotype_shift_hours(chronotype: str) -> float:
    c = chronotype.lower()
    if c == "morning":
        return -1.5
    if c == "evening":
        return 1.75
    return 0.0


def circadian_wave(phase_hour: float, shift: float) -> float:
    # Peak alertness around mid-afternoon local phase.
    radians = 2.0 * math.pi * ((phase_hour + shift - 15.0) / 24.0)
    return (math.cos(radians) + 1.0) / 2.0


def appetite_wave(phase_hour: float, shift: float) -> float:
    # Appetite often higher in evening; this sets a broad evening peak.
    radians = 2.0 * math.pi * ((phase_hour + shift - 20.0) / 24.0)
    return (math.cos(radians) + 1.0) / 2.0


def main() -> int:
    payload = parse_payload()

    work_dir = Path(payload.get("work_dir", ".")).resolve()
    state_dir = work_dir / "state"
    state_dir.mkdir(parents=True, exist_ok=True)

    prev_circadian = load_json(state_dir / "circadian.json", {})
    prev_sleep = load_json(state_dir / "sleep.json", {})

    tick = int(payload.get("current_tick", int(prev_circadian.get("tick", 0)) + 1))
    prev_phase_hour = float(prev_circadian.get("phase_hour", 12.0))
    clock_time, phase_hour = parse_clock_time(payload, prev_phase_hour)

    chronotype = str(payload.get("chronotype", prev_circadian.get("chronotype", "neutral"))).lower()
    shift = chronotype_shift_hours(chronotype)

    sleep_pressure_prev = clamp(float(prev_sleep.get("sleep_pressure", 0.35)))

    events_raw = payload.get("events", [])
    events = {str(e).strip().lower() for e in events_raw if str(e).strip()}
    is_sleeping = "sleep" in events or bool(payload.get("is_sleeping", False))

    wake_gain = clamp(float(payload.get("wake_gain", 0.03)), 0.0, 0.08)
    sleep_recovery = clamp(float(payload.get("sleep_recovery", 0.12)), 0.0, 0.3)

    if is_sleeping:
        sleep_pressure = clamp(sleep_pressure_prev - sleep_recovery)
    else:
        sleep_pressure = clamp(sleep_pressure_prev + wake_gain)

    circadian_alertness = clamp(0.15 + 0.8 * circadian_wave(phase_hour, shift))
    circadian_appetite = clamp(0.2 + 0.75 * appetite_wave(phase_hour, shift))

    fatigue_modifier = clamp(float(payload.get("fatigue_modifier", 0.0)))
    effective_energy = clamp(circadian_alertness - sleep_pressure * 0.6 - fatigue_modifier)

    sleep_tendency = clamp(0.55 * sleep_pressure + 0.45 * (1.0 - circadian_alertness))
    sleep_debt = clamp(float(prev_sleep.get("sleep_debt", 0.0)) + (0.03 if sleep_pressure > 0.75 else -0.02))
    if is_sleeping:
        sleep_debt = clamp(sleep_debt - 0.05)

    should_sleep_soon = bool(sleep_tendency >= 0.72)

    last_sleep_tick = int(prev_sleep.get("last_sleep_tick", max(0, tick - 8)))
    if is_sleeping:
        last_sleep_tick = tick

    circadian = {
        "tick": tick,
        "clock_time": clock_time,
        "chronotype": chronotype,
        "phase_hour": round(phase_hour, 3),
        "circadian_alertness": round(circadian_alertness, 3),
        "circadian_appetite": round(circadian_appetite, 3),
        "sleep_tendency": round(sleep_tendency, 3),
        "light_exposure": round(clamp(float(payload.get("light_exposure", 0.5))), 3),
        "notes": [
            "Two-process style approximation with chronotype shift.",
            "Use LLM refinement for social schedule conflicts and jet-lag effects.",
        ],
    }

    sleep = {
        "sleep_pressure": round(sleep_pressure, 3),
        "effective_energy": round(effective_energy, 3),
        "sleep_debt": round(sleep_debt, 3),
        "last_sleep_tick": last_sleep_tick,
        "should_sleep_soon": should_sleep_soon,
        "reasoning": "Deterministic baseline from Process-S and circadian modulation.",
    }

    (state_dir / "circadian.json").write_text(
        json.dumps(circadian, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (state_dir / "sleep.json").write_text(
        json.dumps(sleep, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "ok": True,
                "artifacts": ["state/circadian.json", "state/sleep.json"],
                "tick": tick,
                "sleep_pressure": sleep["sleep_pressure"],
                "effective_energy": sleep["effective_energy"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
