#!/usr/bin/env python3
"""Deterministic relationship updater for social continuity state."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REL_KEYS = ["familiarity", "trust", "liking", "obligation", "conflict", "respect"]


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


def normalize_delta(delta: dict[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    for key in REL_KEYS:
        try:
            out[key] = float(delta.get(key, 0.0))
        except (TypeError, ValueError):
            out[key] = 0.0
    return out


def compute_influence_weight(entry: dict[str, Any], expertise_hint: float = 0.0) -> float:
    trust = clamp(float(entry.get("trust", 0.5)))
    respect = clamp(float(entry.get("respect", 0.5)))
    familiarity = clamp(float(entry.get("familiarity", 0.1)))
    conflict = clamp(float(entry.get("conflict", 0.0)))
    return clamp(0.35 * trust + 0.25 * respect + 0.2 * familiarity + 0.2 * expertise_hint - 0.25 * conflict)


def main() -> int:
    payload = parse_payload()

    work_dir = Path(payload.get("work_dir", ".")).resolve()
    state_dir = work_dir / "state"
    state_dir.mkdir(parents=True, exist_ok=True)

    rel_state = load_json(state_dir / "relationships.json", {"people": {}})
    people = rel_state.get("people", {})
    if not isinstance(people, dict):
        people = {}

    tick = int(payload.get("current_tick", 0))
    iso_time = str(payload.get("time") or datetime.now(timezone.utc).isoformat())

    interactions = payload.get("interactions", [])
    if not isinstance(interactions, list):
        interactions = []

    social_events: list[dict[str, Any]] = []

    for item in interactions:
        if not isinstance(item, dict):
            continue
        person_id = str(item.get("person") or item.get("agent") or "").strip().lower()
        if not person_id:
            continue

        entry = people.get(person_id, {})
        if not isinstance(entry, dict):
            entry = {}

        base = {
            "familiarity": clamp(float(entry.get("familiarity", 0.1))),
            "trust": clamp(float(entry.get("trust", 0.5))),
            "liking": clamp(float(entry.get("liking", 0.5))),
            "obligation": clamp(float(entry.get("obligation", 0.0))),
            "conflict": clamp(float(entry.get("conflict", 0.0))),
            "respect": clamp(float(entry.get("respect", 0.5))),
        }

        interaction_type = str(item.get("type", "neutral")).strip().lower()
        interaction_summary = str(item.get("summary", interaction_type)).strip()

        if interaction_type == "cooperate":
            delta = {
                "familiarity": 0.03,
                "trust": 0.04,
                "liking": 0.03,
                "obligation": -0.02,
                "conflict": -0.02,
                "respect": 0.03,
            }
        elif interaction_type == "conflict":
            delta = {
                "familiarity": 0.02,
                "trust": -0.08,
                "liking": -0.06,
                "obligation": 0.02,
                "conflict": 0.09,
                "respect": -0.05,
            }
        elif interaction_type == "help":
            delta = {
                "familiarity": 0.03,
                "trust": 0.06,
                "liking": 0.05,
                "obligation": 0.06,
                "conflict": -0.01,
                "respect": 0.04,
            }
        elif interaction_type == "betrayal":
            delta = {
                "familiarity": 0.01,
                "trust": -0.16,
                "liking": -0.12,
                "obligation": -0.04,
                "conflict": 0.12,
                "respect": -0.1,
            }
        else:
            delta = {
                "familiarity": 0.01,
                "trust": 0.0,
                "liking": 0.005,
                "obligation": 0.0,
                "conflict": -0.005,
                "respect": 0.0,
            }

        manual_delta = item.get("delta", {})
        if isinstance(manual_delta, dict):
            override = normalize_delta(manual_delta)
            for k in REL_KEYS:
                delta[k] += override[k]

        for k in REL_KEYS:
            base[k] = round(clamp(base[k] + delta[k]), 3)

        try:
            expertise_hint = float(item.get("expertise_hint", item.get("expertise", 0.0)) or 0.0)
        except (TypeError, ValueError):
            expertise_hint = 0.0
        influence_weight = round(compute_influence_weight(base, expertise_hint), 3)

        old_tags = entry.get("shared_history_tags", [])
        if not isinstance(old_tags, list):
            old_tags = []
        new_tags = item.get("tags", [])
        if not isinstance(new_tags, list):
            new_tags = []

        merged_tags = []
        for tag in [*old_tags, *new_tags]:
            t = str(tag).strip().lower()
            if t and t not in merged_tags:
                merged_tags.append(t)

        people[person_id] = {
            **base,
            "influence_weight": influence_weight,
            "last_interaction": interaction_summary,
            "last_interaction_tick": tick,
            "last_interaction_time": iso_time,
            "shared_history_tags": merged_tags[-20:],
        }

        if abs(delta["trust"]) >= 0.05 or abs(delta["conflict"]) >= 0.05:
            social_events.append(
                {
                    "tick": tick,
                    "time": iso_time,
                    "person": person_id,
                    "type": interaction_type,
                    "summary": interaction_summary,
                    "delta": {k: round(delta[k], 3) for k in REL_KEYS},
                }
            )

    rel_out = {"people": people}
    (state_dir / "relationships.json").write_text(
        json.dumps(rel_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if social_events:
        path = state_dir / "social_events.jsonl"
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        appended = "\n".join(json.dumps(e, ensure_ascii=False) for e in social_events)
        if old and not old.endswith("\n"):
            old += "\n"
        path.write_text(old + appended + "\n", encoding="utf-8")

    artifacts = ["state/relationships.json"]
    if social_events:
        artifacts.append("state/social_events.jsonl")

    print(
        json.dumps(
            {
                "ok": True,
                "artifacts": artifacts,
                "updated_people": len(interactions),
                "notable_events": len(social_events),
            },
            ensure_ascii=False,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
