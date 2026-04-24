---
name: chenggu-analysis
description: >
  Structured Chinese Chenggu (“bone weight”) fortune analysis for 称骨算命 / 袁天罡称骨 tasks.
  Use when the user wants a deterministic lookup + structured output pipeline from birth datetime or normalized lunar components.
---
# Goal
你要把“称骨算命”执行成一个 **可计算、可结构化、可扩展** 的民俗规则流程，而不是自由发挥的玄学散文。

## Core contract
1. **先标准化输入**：优先接受 `lunar_components`；若只有 `birth_datetime` 且是公历，先做可靠的农历转换。
2. **再查表**：严格从 JSON 查 `year/month/day/hour` 四项权重。
3. **只做整数运算**：内部统一使用“钱”。
4. **精确匹配**：`total_qian` 必须一一对应 `verse_profiles` 的唯一档位。
5. **结构化输出**：必须同时给出机器可读 JSON 与中文展示层。
6. **不臆测**：不会转换就明确限制，不要猜农历日期，不要自造权重。

## Scope
仅在以下场景使用：
- 称骨算命 / 袁天罡称骨 / 骨重 / 几两几钱 / 四两几钱
- 希望把歌诀拆成事业、财运、婚姻等结构化结果
- 需要把民俗规则做成可编排的 agent / skill / rule-engine

不要用于：
- 八字、紫微、星座、塔罗等非称骨体系
- 缺少可靠农历转换能力却仍要求你硬算公历结果
- 任何需要科学、医学、法律、投资保证的场景

## Resources
- `references/chenggu_skill_spec.json`: 完整规则总表（可直接被工具读取）
- `references/lookup_tables.json`: 年/月/日/时权重查表
- `references/verse_profiles.json`: 51 档歌诀与结构化标签
- `references/skill_contract.json`: 输入、派生特征、规则、决策流
- `references/implementation_notes.md`: 边界规则、转换要求、限制说明
- `assets/output-template.json`: 中文展示模板
- `assets/input.schema.json` / `assets/output.schema.json`: 机器可读 schema
- `references/examples.md`: 参考输入输出

## Execution flow
1. 读取输入。
2. 若存在 `lunar_components`，直接使用：
   - `year_ganzhi`
   - `month`
   - `day`
   - `hour_branch`
   - `is_leap_month`
3. 若仅有 `birth_datetime`：
   - 先识别 `calendar_type`
   - 若为 `gregorian`，调用宿主环境中可靠的农历转换能力
   - 若为 `lunar`，提取农历年月日时
4. 应用边界规则：
   - 夜子时 23:00~23:59 视为次日
   - 闰月 1~15 按本月，16~30 按下月
5. 查 `lookup_tables.json`：
   - `year_weight_qian_by_ganzhi`
   - `month_weight_qian`
   - `day_weight_qian`
   - `hour_weight_qian`
6. 计算：
   - `total_qian = year + month + day + hour`
   - `total_display = verse_profiles[total_qian].total_display`
   - `grade = verse_profiles[total_qian].grade`
7. 读取 `verse_profiles.json` 中对应档位：
   - `verse_canonical`
   - `structured.trajectory_tags`
   - `structured.career_level`
   - `structured.wealth_level`
   - `structured.marriage_level`
   - `structured.scores`
8. 生成输出：
   - 顶层 JSON 遵循 `assets/output.schema.json`
   - 同时填充 `display_zh`，键名与 `assets/output-template.json` 一致
9. 给出简短说明：
   - 说明这是民俗解释，不是科学结论
   - 点明不确定性来源：版本差异、农历转换、歌诀解释主观性

## Output requirements
- 必须先输出一个完整 JSON 对象。
- JSON 至少包括：
  - `skill_name`
  - `api_name`
  - `input_normalized`
  - `weights`
  - `total_weight`
  - `grade`
  - `verse_canonical`
  - `analysis`
  - `advice`
  - `display_zh`
  - `limitations`
- `display_zh` 内必须包含：
  - `骨重明细`
  - `总骨重`
  - `等级`
  - `原始歌诀`
  - `结构化分析`
  - `建议`

## Style
- 默认跟随用户语言；中文用户优先中文。
- 结果要简洁、可审计、便于程序后处理。
- 不要把歌诀扩写成冗长散文；重点是结构化与可复核。
