---
name: ziwei-analysis
description: Perform structured Ziwei Dou Shu (紫微斗数 / Zi Wei Dou Shu) system design, chart interpretation, and implementation planning. Use when the user asks to build a Ziwei skill or engine, define palaces/stars/four-transformations/limits, interpret an existing chart JSON/table, or produce deterministic-vs-heuristic output. Do not use for birth-data-only personal readings unless verified chart facts or a deterministic chart engine are available.
compatibility: Claude Code, Codex, OpenAI Skills, and Agent Skills-compatible clients. Optional helper scripts require Python 3. No bundled charting engine is included.
metadata:
  author: custom
  version: "1.0.0"
  locale: zh-CN
  domain: ziwei-doushu
  mode: design-interpretation
---

# Ziwei Analysis

这是一个给 AI 代理使用的 **紫微斗数 Skill**。目标不是“神秘发挥”，而是把紫微斗数任务拆成**确定性的排盘层**与**经验性的解读层**，并用结构化输出保证可复核、可集成、可版本化。

## 核心原则

1. **先分模式，再执行**
   - `design`：构建/评审 Skill、Prompt、接口、JSON schema、规则引擎、代码架构。
   - `interpret_chart`：用户已经提供命盘事实（JSON、表格、转写后的截图信息），基于事实解释。
   - `chart_from_birth`：用户只提供出生资料；仅在你能访问**可信、确定、可复现**的排盘规则或外部排盘引擎时执行。

2. **排盘是确定层，解读是经验层**
   - 确定层：历法换算、命身宫、十二宫布宫、主星/辅星落宫、四化、大限/流年。
   - 经验层：性格、事业、财务、婚姻、健康、阶段趋势等解释。
   - 输出时必须把这两层分开写。

3. **绝不虚构星曜位置**
   - 如果没有可信排盘引擎、规则表、或现成命盘事实，就不要假装算出了主星、辅星、四化。
   - 此时只能：
     - 转为 `design` 模式，输出实现方案；或
     - 要求用户提供现成命盘 / Chart JSON / 截图转写结果；或
     - 明确说明当前只能给出“实现规范”，不能给出“个人命盘结论”。

4. **显式处理歧义**
   下列因素可能影响排盘，必须在结果里显式列出：
   - `calendar_type`：公历 / 农历 / 自动判断
   - `gender`
   - `timezone`
   - `late_zi_hour_rule`：晚子时算次日还是当日
   - `school_variant`：四化表/流派差异
   - `use_true_solar_time`
   - 闰月与地理位置

## 使用时机

当用户出现以下需求时使用本 Skill：

- “帮我做一个紫微斗数 Skill / Agent / Prompt / 规则系统”
- “把紫微斗数做成 Claude Code / Codex 可用的技能包”
- “定义 12 宫位、主星、辅星、四化、大限/流年的数据结构”
- “根据这份命盘 JSON 帮我做结构化解读”
- “把排盘与解读拆成确定层和经验层”
- “为紫微斗数系统设计 API、schema、输出模板、测试策略”

## 不使用的场景

- 你无法访问可靠排盘规则时，却被要求只凭出生资料直接给出个体命盘结论
- 用户要的是通用星座娱乐、塔罗、八字、奇门遁甲等其他术数任务
- 用户要求把经验解读包装成科学事实、医疗结论、法律结论或财务保证

## 输入合同

优先接受如下结构；如果用户只给自然语言，也要先转换成这个结构：

```json
{
  "task_mode": "auto",
  "birth_datetime": "",
  "gender": "unknown",
  "calendar_type": "solar",
  "timezone": "Asia/Shanghai",
  "latitude": null,
  "longitude": null,
  "use_true_solar_time": false,
  "late_zi_hour_rule": "cross_day",
  "school_variant": "traditional_fullbook_v1",
  "chart_facts": null,
  "question_focus": [],
  "output_locale": "zh-CN"
}
```

- 详细 schema：`assets/input-schema.json`
- 如果用户已提供命盘事实，请参考：`assets/chart-facts-schema.json`

## 工作流程

### A. 模式识别
1. 若用户要的是“做 Skill / 做系统 / 做 schema / 做代码 / 做规则” → `design`
2. 若用户已给命盘 JSON / 表格 / OCR 后的宫位星曜 → `interpret_chart`
3. 若只有出生信息 → `chart_from_birth`

### B. 先跑请求护栏
如果环境支持运行 Python，可先执行：

```bash
python scripts/request_guard.py <request.json>
```

该脚本会告诉你：
- 推断出的 `task_mode`
- 当前输入是否足以支持排盘
- 缺失字段与潜在歧义
- 建议的下一步动作

### C. 确定性排盘层（仅在规则可用时）
按以下顺序输出事实层：

1. 时间标准化
2. 历法转换
3. 生年干支 / 生月 / 生日 / 生时地支
4. 命宫 / 身宫
5. 十二宫位与宫干支
6. 五行局
7. 主星落宫
8. 辅星落宫
9. 四化
10. 三方四正 / 对宫关系
11. 大限
12. 流年（如用户指定年份）

### D. 经验性解读层
基于事实层，按主题聚合：
- 命宫：人格结构、行事风格
- 官禄/事业：职业模式、管理/执行/创作倾向
- 财帛：收入模式、现金流风险、理财习惯
- 夫妻 / 婚姻：关系模式、互动张力、承诺方式
- 疾厄 / 福德：压力来源与恢复方式
- 大限 / 流年：阶段变化与提醒

### E. 输出验证
如环境支持，生成结果后执行：

```bash
python scripts/validate_output.py <output.json>
```

如果校验器发现你把“经验推断”写成了“排盘事实”，或漏掉了歧义/置信度提示，应先修正再交付。

## 解释规则

1. **先事实，后结论**
   - 每个结论都应能追溯到宫位、星曜、四化或运限来源。
   - 最少提供一个“证据句”：例如“官禄宫见某类主星 + 三方会照 + 化权，因此……”。

2. **多宫交叉**
   - 婚姻不要只看夫妻宫；至少联看命宫、福德宫、迁移宫。
   - 事业不要只看官禄宫；至少联看命宫、财帛宫、迁移宫。
   - 财务不要只看财帛宫；至少联看官禄宫、田宅宫、福德宫。

3. **三方四正优先于单点断语**
   - 单颗星的传统标签只能作为起点。
   - 若三方四正与对宫信息冲突，优先做“张力解释”，不要硬合并成单一好坏。

4. **四化是动态修正层**
   - 禄：资源/机会/吸引
   - 权：掌控/推动/负担
   - 科：名誉/可见性/修饰
   - 忌：阻滞/执著/代价/波动
   - 四化必须依附到“所在宫位 + 触发主题 + 风险建议”来解释。

5. **用词边界**
   - 使用“倾向、常见、容易、通常、可能、建议关注”
   - 避免“注定、一定、必然、绝对、肯定成功/失败”

## 结果模板

默认产出如下 JSON；必要时可加字段，但不要删掉核心结构：

```json
{
  "meta": {
    "version": "1.0.0",
    "task_mode": "",
    "school_variant": "",
    "deterministic_part": true,
    "interpretive_part": true,
    "ambiguity_warnings": [],
    "confidence_notes": []
  },
  "命宫": {
    "排盘事实": {
      "宫位": "",
      "主星": [],
      "辅星": [],
      "四化": [],
      "三方四正": []
    },
    "经验解读": {
      "关键词": [],
      "优势": [],
      "风险": [],
      "建议": [],
      "confidence": 0.0
    }
  },
  "事业宫": {
    "来源宫位": "官禄宫",
    "排盘事实": {},
    "经验解读": {}
  },
  "财帛宫": {
    "排盘事实": {},
    "经验解读": {}
  },
  "婚姻": {
    "来源宫位": ["夫妻宫", "福德宫", "命宫", "迁移宫"],
    "排盘事实": {},
    "经验解读": {}
  },
  "综合分析": {
    "命盘主轴": [],
    "大限趋势": [],
    "流年提示": [],
    "关键机会": [],
    "关键风险": [],
    "行动建议": []
  }
}
```

更详细模板见：`assets/output-template.json`

## 设计模式（给 Claude Code / Codex）

当任务是“做系统”而不是“算命盘”时，请优先输出以下内容：

1. `input_schema`
2. `derived_features`
3. `deterministic_rules`
4. `interpretive_rules`
5. `decision_flow`
6. `output_template`
7. `ambiguity_policy`
8. `test_cases`
9. `versioning_strategy`

推荐把系统拆成三层：
- `chart_engine`：只负责确定性排盘
- `interpretation_engine`：只负责经验解读
- `renderer`：把结构化结果转成 JSON / Markdown / API Response

## 默认结论策略

- **有命盘事实**：直接解释
- **只有出生信息且缺规则**：不给个人命盘结论，只给设计规范 / 缺失清单 / 需要补充的数据
- **只有“我想做一个紫微斗数 Skill”**：输出跨平台代理友好的技能包、schema、规则结构、使用示例、安装方式

## 推荐引用文件

- 领域模型：`references/DOMAIN_MODEL.md`
- 详细工作流：`references/WORKFLOW.md`
- 边界与限制：`references/LIMITS_AND_GUARDRAILS.md`
- 安装说明：`README.md`
- 示例请求：`examples/`

## 最终行为准则

- 不把模糊推断伪装成精确计算
- 不把流派差异偷偷省略
- 不把单宫位单星曜结论写成最终结论
- 不把解读写成绝对论断
- 始终在输出里保留“歧义警告 + 置信度 + 事实/推断分层”
