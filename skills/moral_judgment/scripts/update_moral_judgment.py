#!/usr/bin/env python3
"""Update moral foundation appraisal and action tendencies."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FOUNDATIONS = {
    "care_harm": ["hurt", "harm", "pain", "help", "care", "cruel", "受伤", "伤害", "帮助", "照顾"],
    "fairness_cheating": ["fair", "cheat", "owe", "equal", "stole", "unfair", "公平", "欺骗", "偷", "欠"],
    "loyalty_betrayal": ["betray", "loyal", "team", "family", "friend", "背叛", "忠诚", "朋友", "家人"],
    "authority_subversion": ["rule", "boss", "police", "teacher", "respect", "order", "规则", "领导", "警察", "尊重"],
    "sanctity_degradation": ["dirty", "contaminated", "disgusting", "taboo", "sacred", "脏", "恶心", "禁忌"],
    "liberty_oppression": ["forced", "coerced", "controlled", "free", "oppress", "被迫", "强迫", "控制", "自由"],
}


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", default="state")
    parser.add_argument("--tick", type=int, required=True)
    return parser.parse_args()


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def score_keywords(text: str, words: list[str]) -> float:
    lowered = text.lower()
    hits = sum(1 for word in words if re.search(re.escape(word), lowered, flags=re.I))
    return clamp(hits / 3)


def max_norm_pressure(norms: dict[str, Any]) -> tuple[float, float]:
    active = norms.get("active_norms", []) if isinstance(norms.get("active_norms"), list) else []
    pressure = max([float(n.get("pressure", 0) or 0) for n in active if isinstance(n, dict)] + [0.0])
    risk = max([float(n.get("violation_risk", 0) or 0) for n in active if isinstance(n, dict)] + [0.0])
    return clamp(pressure), clamp(risk)


def main() -> int:
    args = parse_args()
    state = Path(args.state_dir)
    state.mkdir(parents=True, exist_ok=True)

    observation = read_text(state / "observation.txt")
    norms = read_json(state / "norms.json", {})
    relationships = read_json(state / "relationships.json", {})
    emotion = read_json(state / "emotion.json", {})
    previous = read_json(state / "moral_appraisal.json", {})

    pressure, violation_risk = max_norm_pressure(norms)
    foundations = {name: score_keywords(observation, words) for name, words in FOUNDATIONS.items()}
    foundations["authority_subversion"] = clamp(max(foundations["authority_subversion"], pressure * violation_risk))

    if "conflict" in observation.lower() or "冲突" in observation:
        foundations["care_harm"] = clamp(foundations["care_harm"] + 0.25)
        foundations["fairness_cheating"] = clamp(foundations["fairness_cheating"] + 0.2)

    intensities = emotion.get("intensities", {}) if isinstance(emotion.get("intensities"), dict) else {}
    anger_base = float(intensities.get("anger", 0) or 0) / 10
    disgust_base = float(intensities.get("disgust", 0) or 0) / 10
    sadness_base = float(intensities.get("sadness", 0) or 0) / 10

    self_blame = bool(re.search(r"\b(my fault|i caused|sorry|apolog|我错|抱歉|对不起)\b", observation.lower()))
    public = float(norms.get("witness_visibility", 0.0) or 0.0)
    compassion = clamp(foundations["care_harm"] * 0.55 + sadness_base * 0.35)
    guilt = clamp(0.55 * foundations["care_harm"] if self_blame else 0.1 * foundations["care_harm"])
    shame = clamp(public * violation_risk * 0.7 + (0.2 if self_blame else 0.0))
    anger = clamp(max(foundations["fairness_cheating"], foundations["liberty_oppression"]) * 0.6 + anger_base * 0.4)
    disgust = clamp(foundations["sanctity_degradation"] * 0.7 + disgust_base * 0.3)
    admiration = clamp(0.5 if re.search(r"\b(helped|kind|brave|honest|善良|勇敢|诚实)\b", observation.lower()) else 0.0)

    relationship_importance = 0.0
    people = relationships.get("people", {}) if isinstance(relationships.get("people"), dict) else {}
    if people:
        relationship_importance = max(
            [float(p.get("familiarity", 0) or 0) for p in people.values() if isinstance(p, dict)] + [0.0]
        )

    uncertainty = 0.4 if re.search(r"\b(maybe|unclear|unknown|not sure|可能|不确定)\b", observation.lower()) else 0.1
    intuition_strength = clamp(max(foundations.values()) * 0.7 + max(guilt, shame, anger, disgust, compassion, admiration) * 0.3)
    deliberation_need = clamp(uncertainty + 0.25 * relationship_importance + 0.25 * max(foundations.values()))

    tendencies: list[str] = []
    if guilt > 0.35:
        tendencies.append("repair")
    if shame > 0.35:
        tendencies.append("manage reputation")
    if anger > 0.45:
        tendencies.append("confront or enforce norm")
    if compassion > 0.4:
        tendencies.append("help")
    if disgust > 0.45:
        tendencies.append("avoid")
    if not tendencies:
        tendencies.append("monitor")

    dominant = max(foundations, key=foundations.get)
    output = {
        "_meta": {
            "skill": "moral_judgment",
            "purpose": "Current moral appraisal, moral emotions, and action tendencies.",
        },
        "_summary": f"Dominant moral concern: {dominant}; tendencies: {', '.join(tendencies[:2])}.",
        "tick": args.tick,
        "foundations": {k: round(v, 3) for k, v in foundations.items()},
        "intuition_strength": round(intuition_strength, 3),
        "deliberation_need": round(deliberation_need, 3),
        "moral_emotions": {
            "guilt": round(guilt, 3),
            "shame": round(shame, 3),
            "anger": round(anger, 3),
            "compassion": round(compassion, 3),
            "disgust": round(disgust, 3),
            "admiration": round(admiration, 3),
        },
        "action_tendencies": tendencies,
        "reasoning": "Keyword baseline with norm pressure, witness visibility, relationship importance, and current emotion.",
    }
    (state / "moral_appraisal.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "dominant": dominant, "summary": output["_summary"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
