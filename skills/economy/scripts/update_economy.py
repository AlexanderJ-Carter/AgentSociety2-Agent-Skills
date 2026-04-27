#!/usr/bin/env python3
"""Deterministic economy updater for social-human simulation skills."""

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


def sum_numbers(items: list[Any]) -> float:
    total = 0.0
    for item in items:
        try:
            total += float(item)
        except (TypeError, ValueError):
            continue
    return total


def main() -> int:
    payload = parse_payload()

    work_dir = Path(payload.get("work_dir", ".")).resolve()
    state_dir = work_dir / "state"
    state_dir.mkdir(parents=True, exist_ok=True)

    prev_economy = load_json(state_dir / "economy.json", {})
    prev_resources = load_json(state_dir / "resources.json", {})

    tick = int(payload.get("current_tick", int(prev_economy.get("tick", 0)) + 1))
    iso_time = str(payload.get("time") or datetime.now(timezone.utc).isoformat())

    cash_prev = float(prev_economy.get("cash", payload.get("starting_cash", 120.0)))
    debt_prev = float(prev_economy.get("debt", payload.get("starting_debt", 0.0)))

    incomes = payload.get("incomes", [])
    expenses = payload.get("expenses", [])
    purchases = payload.get("purchases", [])

    income_total = sum_numbers(incomes)
    expense_total = sum_numbers(expenses)

    purchase_total = 0.0
    for p in purchases:
        if not isinstance(p, dict):
            continue
        try:
            cost = float(p.get("cost", 0.0))
            qty = float(p.get("quantity", 1.0))
        except (TypeError, ValueError):
            continue
        purchase_total += max(0.0, cost) * max(0.0, qty)

    cash = cash_prev + income_total - expense_total - purchase_total
    debt = debt_prev
    if cash < 0.0:
        debt += abs(cash)
        cash = 0.0

    fixed_reserve = max(1.0, float(payload.get("fixed_reserve", 150.0)))
    scarcity_pressure = clamp((fixed_reserve - cash) / fixed_reserve)
    debt_pressure = clamp(debt / (fixed_reserve * 2.0))
    recurring_pressure = clamp(float(payload.get("recurring_expenses_pressure", 0.35)))
    budget_stress = clamp(0.45 * scarcity_pressure + 0.3 * debt_pressure + 0.25 * recurring_pressure)

    if cash >= 80:
        meal_afford = "affordable"
    elif cash >= 25:
        meal_afford = "limited"
    else:
        meal_afford = "risky"

    if cash >= 120:
        taxi_afford = "affordable"
    elif cash >= 45:
        taxi_afford = "expensive"
    else:
        taxi_afford = "not_recommended"

    if cash >= 150:
        leisure_afford = "affordable"
    elif cash >= 60:
        leisure_afford = "limited"
    else:
        leisure_afford = "defer"

    income_status = str(payload.get("income_status", prev_economy.get("income_status", "unknown")))
    next_income_expected = str(
        payload.get("next_income_expected", prev_economy.get("next_income_expected", "unknown"))
    )

    work_obligation = payload.get("work_obligation")
    if not isinstance(work_obligation, dict):
        work_obligation = prev_economy.get(
            "work_obligation",
            {"active": False, "next_shift": None, "lateness_risk": 0.0},
        )

    inventory = prev_resources.get("inventory", {})
    if not isinstance(inventory, dict):
        inventory = {}

    for p in purchases:
        if not isinstance(p, dict):
            continue
        item = str(p.get("item", "")).strip().lower()
        if not item:
            continue
        qty = float(p.get("quantity", 1.0))
        inventory[item] = round(float(inventory.get(item, 0.0)) + max(0.0, qty), 3)

    consumptions = payload.get("consumptions", [])
    for c in consumptions:
        if not isinstance(c, dict):
            continue
        item = str(c.get("item", "")).strip().lower()
        if not item:
            continue
        qty = max(0.0, float(c.get("quantity", 1.0)))
        inventory[item] = round(max(0.0, float(inventory.get(item, 0.0)) - qty), 3)

    economy = {
        "tick": tick,
        "time": iso_time,
        "cash": round(cash, 2),
        "debt": round(debt, 2),
        "income_status": income_status,
        "next_income_expected": next_income_expected,
        "income_flow": {
            "income_total": round(income_total, 2),
            "expense_total": round(expense_total, 2),
            "purchase_total": round(purchase_total, 2),
        },
        "recurring_expenses_pressure": round(recurring_pressure, 3),
        "scarcity_pressure": round(scarcity_pressure, 3),
        "budget_stress": round(budget_stress, 3),
        "work_obligation": {
            "active": bool(work_obligation.get("active", False)),
            "next_shift": work_obligation.get("next_shift"),
            "lateness_risk": round(clamp(float(work_obligation.get("lateness_risk", 0.0))), 3),
        },
        "affordability": {
            "meal": meal_afford,
            "taxi": taxi_afford,
            "leisure": leisure_afford,
        },
        "notes": [
            "Deterministic economy baseline.",
            "Use LLM refinement for social/status spending preferences.",
        ],
    }

    resources = {
        "tick": tick,
        "cash": round(cash, 2),
        "debt": round(debt, 2),
        "inventory": inventory,
        "liquidity_band": "high" if cash >= 120 else "medium" if cash >= 40 else "low",
    }

    (state_dir / "economy.json").write_text(
        json.dumps(economy, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (state_dir / "resources.json").write_text(
        json.dumps(resources, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "ok": True,
                "artifacts": ["state/economy.json", "state/resources.json"],
                "tick": tick,
                "cash": economy["cash"],
                "budget_stress": economy["budget_stress"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
