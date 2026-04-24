\
#!/usr/bin/env python3
"""Validate a Ziwei request payload and report ambiguity / readiness."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def infer_mode(data: Dict[str, Any]) -> str:
    explicit = data.get("task_mode")
    if explicit and explicit != "auto":
        return explicit
    if data.get("chart_facts"):
        return "interpret_chart"
    if data.get("birth_datetime"):
        return "chart_from_birth"
    return "design"


def guard_request(data: Dict[str, Any]) -> Dict[str, Any]:
    mode = infer_mode(data)
    ambiguities: List[str] = []
    missing: List[str] = []
    notes: List[str] = []
    recommended_actions: List[str] = []

    if mode == "chart_from_birth":
        required_for_exact = [
            "birth_datetime",
            "gender",
            "calendar_type",
            "timezone",
            "late_zi_hour_rule",
            "school_variant",
        ]
        for key in required_for_exact:
            value = data.get(key)
            if value in (None, "", "unknown"):
                missing.append(key)

        if data.get("calendar_type", "auto") == "auto":
            ambiguities.append("calendar_type=auto 可能导致公历/农历识别歧义。")
        if data.get("gender", "unknown") == "unknown":
            ambiguities.append("gender 未明确，可能影响大限顺逆等实现。")
        if data.get("late_zi_hour_rule") in (None, ""):
            ambiguities.append("late_zi_hour_rule 未配置，晚子时切日存在歧义。")
        if data.get("school_variant") in (None, ""):
            ambiguities.append("school_variant 未配置，四化表/流派差异未冻结。")
        if data.get("latitude") is None or data.get("longitude") is None:
            notes.append("未提供经纬度；如实现真太阳时或高精度切时，可能需要地理位置。")
        if not data.get("birth_datetime"):
            recommended_actions.append("补充 birth_datetime。")
        if missing:
            recommended_actions.append("当前不适合直接输出个人命盘结论；优先补充参数或转为设计/实现任务。")

    if mode == "interpret_chart":
        chart = data.get("chart_facts") or {}
        palaces = chart.get("palaces")
        if not palaces:
            missing.append("chart_facts.palaces")
            recommended_actions.append("补充至少一个 palace map，包含主星/辅星/四化等事实。")
        else:
            notes.append(f"已检测到 {len(palaces)} 个宫位事实对象。")

    if mode == "design":
        notes.append("当前输入更适合输出 schema、规则结构、接口、测试策略与安装说明。")

    status = "ready"
    if missing and mode == "chart_from_birth":
        status = "needs_more_context"
    elif missing:
        status = "partial"

    return {
        "resolved_task_mode": mode,
        "status": status,
        "missing_fields": missing,
        "ambiguities": ambiguities,
        "notes": notes,
        "recommended_actions": recommended_actions,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/request_guard.py <request.json>", file=sys.stderr)
        return 2

    try:
        data = load_json(sys.argv[1])
        report = guard_request(data)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:  # pragma: no cover - simple CLI tool
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
