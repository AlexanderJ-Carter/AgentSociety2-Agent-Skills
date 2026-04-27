#!/usr/bin/env python3
"""Assess information exposure, credibility, misinformation risk, and belief uptake."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


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


def contains_any(text: str, words: list[str]) -> bool:
    lowered = text.lower()
    return any(word in lowered for word in words)


def infer_source_type(text: str) -> str:
    lowered = text.lower()
    if contains_any(lowered, ["post", "viral", "forwarded", "social media", "rumor", "帖子", "转发", "谣言"]):
        return "social_media"
    if contains_any(lowered, ["official", "government", "doctor", "teacher", "report", "官方", "医生", "老师", "报告"]):
        return "institution_or_expert"
    if contains_any(lowered, ["friend", "alice", "family", "coworker", "朋友", "家人", "同事"]):
        return "interpersonal"
    if contains_any(lowered, ["ad", "sponsor", "discount", "buy now", "广告", "促销", "购买"]):
        return "advertising"
    return "unknown"


def extract_claim(text: str) -> str:
    clean = " ".join(text.split())
    if len(clean) <= 180:
        return clean
    return clean[:177] + "..."


def source_credibility(source_type: str, relationships: dict[str, Any]) -> float:
    base = {
        "institution_or_expert": 0.72,
        "interpersonal": 0.55,
        "advertising": 0.32,
        "social_media": 0.28,
        "unknown": 0.38,
    }.get(source_type, 0.38)
    if source_type == "interpersonal":
        people = relationships.get("people", {}) if isinstance(relationships.get("people"), dict) else {}
        trust = max([float(p.get("trust", 0.0) or 0.0) for p in people.values() if isinstance(p, dict)] + [0.0])
        base = max(base, 0.35 + 0.45 * trust)
    return clamp(base)


def evidence_quality(text: str) -> float:
    quality = 0.25
    if contains_any(text, ["data", "study", "evidence", "source", "link", "record", "数据", "研究", "证据", "来源", "记录"]):
        quality += 0.3
    if contains_any(text, ["because", "explained", "measured", "verified", "因为", "解释", "测量", "核实"]):
        quality += 0.15
    if contains_any(text, ["everyone knows", "trust me", "no proof", "secret", "都知道", "相信我", "秘密"]):
        quality -= 0.2
    return clamp(quality)


def misinformation_risk(text: str, source_type: str) -> float:
    risk = 0.2
    if source_type in {"social_media", "advertising", "unknown"}:
        risk += 0.2
    flags = [
        ["urgent", "act now", "before deleted", "马上", "赶紧", "删前"],
        ["secret", "cover up", "they don't want you to know", "秘密", "隐瞒", "不想让你知道"],
        ["miracle", "guaranteed", "100%", "神奇", "保证", "百分百"],
        ["no source", "anonymous", "unverified", "无来源", "匿名", "未经证实"],
        ["outrage", "shocking", "angry", "震惊", "愤怒"],
    ]
    risk += 0.12 * sum(1 for group in flags if contains_any(text, group))
    return clamp(risk)


def main() -> int:
    args = parse_args()
    state = Path(args.state_dir)
    state.mkdir(parents=True, exist_ok=True)

    observation = read_text(state / "observation.txt")
    relationships = read_json(state / "relationships.json", {})
    previous = read_json(state / "media_literacy.json", {})

    source_type = infer_source_type(observation)
    credibility = source_credibility(source_type, relationships)
    evidence = evidence_quality(observation)
    risk = misinformation_risk(observation, source_type)

    prior_claims = previous.get("recent_claims", []) if isinstance(previous.get("recent_claims"), list) else []
    claim = extract_claim(observation)
    familiarity = clamp(0.15 + 0.2 * sum(1 for c in prior_claims if isinstance(c, str) and c[:40] == claim[:40]))

    identity_alignment = 0.55 if contains_any(observation, ["my group", "people like me", "our", "我们", "自己人"]) else 0.4
    emotional_arousal = 0.7 if contains_any(observation, ["shocking", "danger", "angry", "fear", "震惊", "危险", "愤怒", "害怕"]) else 0.35
    inoculation = float(previous.get("inoculation_strength", 0.0) or 0.0)
    if contains_any(observation, ["debunk", "prebunk", "fact check", "warning about misinformation", "辟谣", "事实核查", "预警"]):
        inoculation = clamp(inoculation + 0.25)

    acceptance = clamp(
        0.3 * credibility
        + 0.3 * evidence
        + 0.15 * familiarity
        + 0.15 * identity_alignment
        + 0.1 * emotional_arousal
        - 0.35 * risk
        - 0.2 * inoculation
    )

    if acceptance > 0.7 and risk < 0.4:
        stance = "tentatively accept"
    elif risk > 0.65 or acceptance < 0.35:
        stance = "withhold belief and seek corroboration"
    else:
        stance = "keep uncertain"

    recent_claims = ([claim] + [c for c in prior_claims if isinstance(c, str) and c != claim])[:10]
    output = {
        "_meta": {
            "skill": "media_literacy",
            "purpose": "Current information exposure assessment and belief-update caution.",
        },
        "_summary": f"{source_type} claim assessed as {stance}.",
        "tick": args.tick,
        "current_claim": claim,
        "source_type": source_type,
        "source_credibility": round(credibility, 3),
        "evidence_quality": round(evidence, 3),
        "familiarity": round(familiarity, 3),
        "identity_alignment": round(identity_alignment, 3),
        "emotional_arousal": round(emotional_arousal, 3),
        "misinformation_risk": round(risk, 3),
        "inoculation_strength": round(inoculation, 3),
        "acceptance_tendency": round(acceptance, 3),
        "recommended_stance": stance,
        "recent_claims": recent_claims,
    }
    (state / "media_literacy.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    hints = {
        "_meta": {
            "skill": "media_literacy",
            "purpose": "Belief update suggestions for reflection; not authoritative facts.",
        },
        "claim": claim,
        "acceptance_tendency": round(acceptance, 3),
        "recommended_stance": stance,
        "reason": "Credibility/evidence/familiarity/identity/risk/inoculation weighted baseline.",
    }
    (state / "belief_update_hints.json").write_text(json.dumps(hints, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "source_type": source_type, "stance": stance}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
