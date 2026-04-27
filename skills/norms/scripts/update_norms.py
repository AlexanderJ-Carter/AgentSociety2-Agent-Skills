#!/usr/bin/env python3
"""Deterministic norms updater for social-human simulation skills."""

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

    prev_norms = load_json(state_dir / "norms.json", {})

    tick = int(payload.get("current_tick", int(prev_norms.get("tick", 0)) + 1))
    iso_time = str(payload.get("time") or datetime.now(timezone.utc).isoformat())

    place = str(payload.get("place", "public_space")).lower()
    role = str(payload.get("role", "stranger")).lower()
    crowd_size = max(0, int(payload.get("crowd_size", 3)))
    authority_present = bool(payload.get("authority_present", False))

    witness_visibility = clamp(0.2 + min(crowd_size, 20) / 25.0 + (0.15 if authority_present else 0.0))

    norm_templates: dict[str, list[dict[str, Any]]] = {
        "restaurant": [
            {"norm": "wait in line", "forbidden": "skip queue", "sanction": "disapproval"},
            {"norm": "pay before leaving", "forbidden": "leave without paying", "sanction": "formal_penalty"},
        ],
        "workplace": [
            {"norm": "be punctual", "forbidden": "miss meeting without notice", "sanction": "reputation_cost"},
            {"norm": "respect role hierarchy", "forbidden": "insult colleague publicly", "sanction": "social_and_institutional"},
        ],
        "hospital": [
            {"norm": "follow triage order", "forbidden": "disrupt clinical process", "sanction": "formal_warning"},
            {"norm": "keep noise low", "forbidden": "shout in ward", "sanction": "staff_intervention"},
        ],
    }

    active_set = norm_templates.get(place, [
        {"norm": "respect personal space", "forbidden": "aggressive intrusion", "sanction": "avoidance"},
        {"norm": "take turns", "forbidden": "cut in line", "sanction": "disapproval"},
    ])

    pressure_bias = 0.08 if role in {"customer", "employee", "student", "patient"} else 0.0

    active_norms = []
    forbidden = []
    permissions = []
    shame = 0.0
    guilt = 0.0

    for item in active_set:
        pressure = clamp(0.45 + 0.45 * witness_visibility + pressure_bias)
        risk = clamp(0.4 + 0.5 * witness_visibility + (0.1 if authority_present else 0.0))
        active_norms.append(
            {
                "norm": item["norm"],
                "pressure": round(pressure, 3),
                "violation_risk": round(risk, 3),
                "likely_sanction": item["sanction"],
            }
        )
        forbidden.append(item["forbidden"])
        shame += 0.18 * pressure
        guilt += 0.14 * pressure

    if place in {"restaurant", "public_space"}:
        permissions.extend(["order food", "sit at available table", "ask for information"])
    elif place == "workplace":
        permissions.extend(["start assigned task", "ask colleague for update"])
    else:
        permissions.extend(["ask staff for help", "wait for turn"])

    norms = {
        "tick": tick,
        "time": iso_time,
        "active_roles": [role],
        "active_norms": active_norms,
        "permissions": permissions,
        "forbidden_or_costly": forbidden,
        "witness_visibility": round(witness_visibility, 3),
        "moral_emotion_risk": {
            "shame": round(clamp(shame), 3),
            "guilt": round(clamp(guilt), 3),
        },
        "notes": [
            "Deterministic norm-pressure baseline with visibility and sanction risk.",
            "Use LLM refinement for culture-specific nuance and exceptions.",
        ],
    }

    (state_dir / "norms.json").write_text(json.dumps(norms, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": True,
                "artifacts": ["state/norms.json"],
                "tick": tick,
                "witness_visibility": norms["witness_visibility"],
            },
            ensure_ascii=False,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
