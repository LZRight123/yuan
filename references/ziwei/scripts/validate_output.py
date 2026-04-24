\
#!/usr/bin/env python3
"""Validate structure of a Ziwei skill output JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_TOP_LEVEL = ["meta", "命宫", "事业宫", "财帛宫", "婚姻", "综合分析"]
REQUIRED_FACT_INTERPRET = ["排盘事实", "经验解读"]


def load_json(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate(data: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"缺少顶层字段: {key}")

    meta = data.get("meta", {})
    if not isinstance(meta, dict):
        errors.append("meta 必须是对象。")
    else:
        for k in ["deterministic_part", "interpretive_part", "ambiguity_warnings"]:
            if k not in meta:
                warnings.append(f"meta 建议包含字段: {k}")

    for section_name in ["命宫", "事业宫", "财帛宫", "婚姻"]:
        section = data.get(section_name)
        if section is None:
            continue
        if not isinstance(section, dict):
            errors.append(f"{section_name} 必须是对象。")
            continue
        for k in REQUIRED_FACT_INTERPRET:
            if k not in section:
                warnings.append(f"{section_name} 建议包含字段: {k}")

        interp = section.get("经验解读", {})
        if isinstance(interp, dict) and "confidence" in interp:
            conf = interp["confidence"]
            if not isinstance(conf, (int, float)):
                errors.append(f"{section_name}.经验解读.confidence 必须是数字。")
            elif not (0.0 <= float(conf) <= 1.0):
                errors.append(f"{section_name}.经验解读.confidence 必须在 0 到 1 之间。")
        else:
            warnings.append(f"{section_name}.经验解读 建议包含 confidence。")

    overall = data.get("综合分析")
    if isinstance(overall, dict):
        for k in ["命盘主轴", "关键机会", "关键风险", "行动建议"]:
            if k not in overall:
                warnings.append(f"综合分析 建议包含字段: {k}")

    valid = not errors
    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_output.py <output.json>", file=sys.stderr)
        return 2

    try:
        data = load_json(sys.argv[1])
        report = validate(data)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["valid"] else 1
    except Exception as exc:  # pragma: no cover - simple CLI tool
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
