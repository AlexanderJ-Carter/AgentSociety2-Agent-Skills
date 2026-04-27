#!/usr/bin/env python3
"""Update institutional trust, procedural justice, access, and compliance state."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


INSTITUTIONS = {
    "hospital": ["hospital", "clinic", "doctor", "nurse", "医院", "诊所", "医生", "护士"],
    "police": ["police", "officer", "court", "ticket", "警察", "法院", "罚单"],
    "employer": ["boss", "manager", "workplace", "company", "shift", "老板", "经理", "公司", "班次"],
    "school": ["school", "teacher", "student", "class", "学校", "老师", "学生", "课堂"],
    "government": ["government", "permit", "benefit", "office", "政府", "许可", "办事处", "福利"],
    "bank": ["bank", "loan", "debt", "account", "银行", "贷款", "债务", "账户"],
    "landlord": ["landlord", "rent", "lease", "housing", "房东", "租金", "租约", "住房"],
}


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", default="state")
    parser.add_argument("--tick", type=int, required=True)
    parser.add_argument("--learning-rate", type=float, default=0.15)
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


def infer_institution(text: str) -> str:
    lowered = text.lower()
    for name, words in INSTITUTIONS.items():
        if any(word in lowered for word in words):
            return name
    return "none"


def infer_role(institution: str, text: str) -> str:
    lowered = text.lower()
    if institution == "hospital":
        return "patient"
    if institution == "school":
        return "student" if contains_any(lowered, ["student", "学生"]) else "parent_or_visitor"
    if institution == "employer":
        return "employee"
    if institution == "police":
        return "citizen_or_suspect"
    if institution == "landlord":
        return "tenant"
    if institution == "bank":
        return "customer_or_debtor"
    if institution == "government":
        return "citizen_or_applicant"
    return "none"


def justice_scores(text: str) -> dict[str, float]:
    positive = {
        "voice": ["listened", "explained my side", "heard me", "倾听", "解释"],
        "neutrality": ["fair", "rule", "evidence", "公平", "规则", "证据"],
        "respect": ["respect", "polite", "dignity", "尊重", "礼貌"],
        "trustworthy_motives": ["helped", "transparent", "honest", "帮助", "透明", "诚实"],
    }
    negative = {
        "voice": ["ignored", "no chance", "不理", "没机会"],
        "neutrality": ["biased", "unfair", "random", "偏见", "不公平", "随意"],
        "respect": ["rude", "insult", "humiliated", "粗鲁", "羞辱"],
        "trustworthy_motives": ["bribe", "exploit", "lied", "贿赂", "剥削", "撒谎"],
    }
    scores: dict[str, float] = {}
    for key in positive:
        score = 0.5
        if contains_any(text, positive[key]):
            score += 0.25
        if contains_any(text, negative[key]):
            score -= 0.3
        scores[key] = clamp(score)
    return scores


def barrier_scores(text: str, economy: dict[str, Any], health: dict[str, Any]) -> dict[str, float]:
    scarcity = float(economy.get("scarcity_pressure", 0.0) or 0.0)
    pain = float(health.get("pain", 0.0) or 0.0)
    illness = float(health.get("illness", 0.0) or 0.0)
    return {
        "cost": clamp(max(scarcity, 0.65 if contains_any(text, ["expensive", "fee", "cost", "贵", "费用"]) else 0.2)),
        "paperwork": 0.7 if contains_any(text, ["form", "document", "paperwork", "表格", "材料", "文件"]) else 0.25,
        "wait_time": 0.75 if contains_any(text, ["queue", "waiting", "delay", "排队", "等待", "延迟"]) else 0.25,
        "discrimination_risk": 0.65 if contains_any(text, ["discriminated", "profiled", "stigma", "歧视", "污名"]) else 0.15,
        "transport_or_health_limit": clamp(max(pain, illness, 0.55 if contains_any(text, ["far", "transport", "远", "交通"]) else 0.15)),
    }


def main() -> int:
    args = parse_args()
    state = Path(args.state_dir)
    state.mkdir(parents=True, exist_ok=True)

    observation = read_text(state / "observation.txt")
    norms = read_json(state / "norms.json", {})
    economy = read_json(state / "economy.json", {})
    health = read_json(state / "health.json", {})
    previous = read_json(state / "institutions.json", {})

    institution = infer_institution(observation)
    role = infer_role(institution, observation)
    trust = previous.get("institutional_trust", {}) if isinstance(previous.get("institutional_trust"), dict) else {}

    justice = justice_scores(observation)
    procedural_justice = sum(justice.values()) / len(justice)
    old_legitimacy = float(trust.get(institution, 0.55) or 0.55) if institution != "none" else 0.5
    legitimacy = old_legitimacy + args.learning_rate * (procedural_justice - old_legitimacy)
    if institution != "none":
        trust[institution] = round(clamp(legitimacy), 3)

    barriers = barrier_scores(observation, economy, health)
    access_barrier = sum(barriers.values()) / len(barriers)

    active_norms = norms.get("active_norms", []) if isinstance(norms.get("active_norms"), list) else []
    norm_pressure = max([float(n.get("pressure", 0) or 0) for n in active_norms if isinstance(n, dict)] + [0.0])
    sanction_risk = max([float(n.get("violation_risk", 0) or 0) for n in active_norms if isinstance(n, dict)] + [0.0])
    dependency = 0.7 if institution in {"hospital", "employer", "landlord", "government"} else 0.35
    compliance_pressure = clamp(0.35 * legitimacy + 0.25 * sanction_risk + 0.25 * dependency + 0.15 * norm_pressure)

    if contains_any(observation, ["approved", "served", "helped", "accepted", "批准", "办成", "帮助"]):
        outcome = "successful"
    elif contains_any(observation, ["denied", "rejected", "failed", "closed", "拒绝", "失败", "关门"]):
        outcome = "denied_or_blocked"
    else:
        outcome = "pending" if institution != "none" else "none"

    output = {
        "_meta": {
            "skill": "civic_institution",
            "purpose": "Current institutional trust, access, obligations, and compliance context.",
        },
        "_summary": f"{institution} encounter as {role}; procedural justice {procedural_justice:.2f}, access barrier {access_barrier:.2f}.",
        "tick": args.tick,
        "active_institution": institution,
        "role": role,
        "procedural_justice": round(procedural_justice, 3),
        "procedural_components": {k: round(v, 3) for k, v in justice.items()},
        "legitimacy": round(clamp(legitimacy), 3),
        "institutional_trust": trust,
        "access_barriers": {k: round(v, 3) for k, v in barriers.items()},
        "access_barrier": round(access_barrier, 3),
        "compliance_pressure": round(compliance_pressure, 3),
        "rights_or_entitlements": ["ask for explanation", "request fair treatment"] if institution != "none" else [],
        "obligations": ["follow posted rules", "provide required information"] if institution != "none" else [],
        "service_outcome": outcome,
    }
    (state / "institutions.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "institution": institution, "outcome": outcome}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
