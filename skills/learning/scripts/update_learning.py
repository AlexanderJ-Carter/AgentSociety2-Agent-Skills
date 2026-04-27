#!/usr/bin/env python3
"""Update learning, proficiency, automaticity, and self-efficacy state."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", default="state")
    parser.add_argument("--tick", type=int, required=True)
    parser.add_argument("--learning-rate", type=float, default=0.08)
    parser.add_argument("--automaticity-rate", type=float, default=0.05)
    parser.add_argument("--retention-strength", type=float, default=240.0)
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


def infer_topic(text: str) -> str | None:
    lowered = text.lower()
    candidates = [
        ("cooking", ["cook", "meal", "recipe", "厨房", "做饭", "烹饪"]),
        ("work_skill", ["work", "task", "job", "report", "code", "工作", "任务", "写代码"]),
        ("social_skill", ["conversation", "apolog", "negotiate", "talk", "explain", "symptoms", "聊天", "道歉", "协商", "解释"]),
        ("navigation", ["route", "map", "walked to", "bus", "路线", "地图", "通勤"]),
        ("health_habit", ["exercise", "medication", "sleep routine", "运动", "服药", "作息"]),
        ("media_literacy", ["source", "claim", "misinformation", "来源", "谣言", "事实核查"]),
    ]
    for topic, words in candidates:
        if any(word in lowered for word in words):
            return topic
    if re.search(r"\b(practice|learn|study|trained|练习|学习|训练)\b", lowered):
        return "general_skill"
    return None


def event_scores(text: str, plan_state: dict[str, Any], emotion: dict[str, Any]) -> dict[str, float]:
    lowered = text.lower()
    success = any(w in lowered for w in ["success", "finished", "improved", "solved", "成功", "完成", "进步"])
    failure = any(w in lowered for w in ["failed", "mistake", "could not", "forgot", "失败", "错误", "不会"])
    practiced = any(w in lowered for w in ["practice", "learn", "study", "trained", "tried", "练习", "学习", "训练", "尝试"])
    watched = any(w in lowered for w in ["watched", "observed", "demonstrated", "showed me", "看到", "示范"])
    encouraged = any(w in lowered for w in ["encouraged", "praised", "feedback", "taught", "鼓励", "表扬", "反馈", "教"])
    criticized = any(w in lowered for w in ["criticized", "scolded", "mocked", "批评", "责备", "嘲笑"])

    if str(plan_state.get("status", "")).lower() in {"completed", "success"}:
        success = True
    if str(plan_state.get("status", "")).lower() in {"failed", "blocked"}:
        failure = True

    intensities = emotion.get("intensities", {}) if isinstance(emotion.get("intensities"), dict) else {}
    anxiety = max(float(intensities.get("fear", 0) or 0), float(intensities.get("sadness", 0) or 0)) / 10
    joy = float(intensities.get("joy", 0) or 0) / 10

    return {
        "practice_quality": 0.75 if success else 0.35 if failure else 0.55 if practiced else 0.0,
        "mastery": 0.05 if success else -0.04 if failure else 0.0,
        "vicarious": 0.025 if watched else 0.0,
        "persuasion": 0.025 if encouraged else -0.025 if criticized else 0.0,
        "affect": 0.02 * joy - 0.03 * anxiety,
        "context_consistency": 0.8 if practiced else 0.3,
    }


def update_topic(
    topic_state: dict[str, Any],
    tick: int,
    scores: dict[str, float],
    learning_rate: float,
    automaticity_rate: float,
    retention_strength: float,
    evidence: str,
) -> dict[str, Any]:
    previous_tick = int(topic_state.get("last_practice_tick", tick))
    age = max(0, tick - previous_tick)
    proficiency = clamp(float(topic_state.get("proficiency", 0.2) or 0.2))
    retention = clamp(float(topic_state.get("retention", 0.7) or 0.7) * math.exp(-age / max(1.0, retention_strength)))
    automaticity = clamp(float(topic_state.get("automaticity", 0.1) or 0.1))
    self_efficacy = clamp(float(topic_state.get("self_efficacy", 0.5) or 0.5))
    practice_count = int(topic_state.get("practice_count", 0) or 0)

    quality = scores["practice_quality"]
    if quality > 0:
        proficiency = clamp(proficiency + learning_rate * quality * (1 - proficiency))
        retention = clamp(max(retention, 0.45) + 0.08 * quality)
        automaticity = clamp(automaticity + automaticity_rate * scores["context_consistency"] * (1 - automaticity))
        practice_count += 1
        previous_tick = tick

    self_efficacy = clamp(
        self_efficacy + scores["mastery"] + scores["vicarious"] + scores["persuasion"] + scores["affect"]
    )

    old_evidence = topic_state.get("evidence", [])
    if not isinstance(old_evidence, list):
        old_evidence = []
    evidence_items = (old_evidence + ([evidence] if evidence else []))[-5:]

    return {
        "proficiency": round(proficiency, 3),
        "retention": round(retention, 3),
        "automaticity": round(automaticity, 3),
        "self_efficacy": round(self_efficacy, 3),
        "practice_count": practice_count,
        "last_practice_tick": previous_tick,
        "evidence": evidence_items,
    }


def main() -> int:
    args = parse_args()
    state = Path(args.state_dir)
    state.mkdir(parents=True, exist_ok=True)

    observation = read_text(state / "observation.txt")
    plan_state = read_json(state / "plan_state.json", {})
    emotion = read_json(state / "emotion.json", {})
    learning = read_json(state / "learning.json", {})
    topics = learning.get("topics", {}) if isinstance(learning.get("topics"), dict) else {}

    topic = infer_topic(observation)
    summary = "No clear learning event detected."
    if topic:
        scores = event_scores(observation, plan_state, emotion)
        topics[topic] = update_topic(
            topics.get(topic, {}) if isinstance(topics.get(topic), dict) else {},
            args.tick,
            scores,
            args.learning_rate,
            args.automaticity_rate,
            args.retention_strength,
            observation[:160],
        )
        summary = f"{topic} updated: proficiency {topics[topic]['proficiency']}, self-efficacy {topics[topic]['self_efficacy']}."

    output = {
        "_meta": {
            "skill": "learning",
            "purpose": "Current knowledge, skill proficiency, practice history, automaticity, and self-efficacy.",
        },
        "_summary": summary,
        "tick": args.tick,
        "topics": topics,
    }
    (state / "learning.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "updated_topic": topic, "summary": summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
