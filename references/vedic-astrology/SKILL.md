---
name: vedic-analysis
description: 使用传统吠陀占星（Vedic astrology）流程“星盘 → Nakshatra → Vimshottari Dasha”分析出生信息，输出只含“业力”和“阶段”的结构化 JSON。Use when a user asks for Vedic astrology, Nakshatra, Janma Nakshatra, Dasha, Vimshottari, karmic themes, or life-stage interpretation from birth data. Do not use for Western astrology-only requests or for scientific proof claims.
---

# Vedic Analysis Skill

## 目标
把用户提供的出生资料或已计算星盘资料，按照传统吠陀占星顺序 **星盘 → 星宿（Nakshatra）→ Vimshottari Dasha** 进行分析，并返回结构化结果。  
除非用户明确要求额外解释，否则默认只输出一个 JSON 对象，顶层只有 `业力` 和 `阶段` 两个键。

## 何时使用
- 用户要做吠陀占星、Nakshatra、Janma Nakshatra、Dasha、Vimshottari、业力主题、人生阶段解读。
- 用户提供了出生日期/时间/地点，或已提供月亮位置、星宿、Pada、大运/子运等资料。
- 用户希望得到传统经验式、象征式、结构化的解读。

## 不适用
- 只讨论西洋占星、塔罗、数秘，且不需要吠陀占星框架。
- 用户要求科学证明、统计验证或天文学论文式论证。
- 缺少可用资料且又要求精确到日期、度数、宫位，但当前环境没有可靠星历/占星计算能力。

## 必须遵守
1. **分析顺序固定**：星盘 → 星宿 → Dasha。
2. **解释依赖传统经验**：使用传统吠陀占星的象征、经验、守护星、阶段逻辑，不把解读表述成科学因果。
3. **优先使用月亮**：月亮星宿是主轴；上升、土星、木星、罗喉/计都只作补充修正。
4. **默认使用 Vimshottari Dasha**：除非用户明确指定其他 Dasha 系统。
5. **默认采用恒星黄道的吠陀框架**：若必须自行计算且用户未指定 ayanamsa，优先按 Lahiri 处理；如果当前环境无法可靠计算，必须明确说明，不能捏造度数或起运时间。
6. **避免绝对化与恐吓式表达**：使用“倾向、课题、阶段重点、修正方向、窗口期”等措辞，不用“注定、必然、一定发生”等措辞。
7. **资料不足时做部分分析**：输出最大程度可辩护的结果，并在 JSON 的 `依据` 或 `完整度` 中标注不确定性。
8. **不得伪造精确信息**：不能编造行星度数、Nakshatra、Pada、Dasha 起止时间、宫位落点。

## 可接受的输入形式
- **完整出生资料**：出生日期、出生时间、出生地点、时区。
- **已计算星盘资料**：月亮星座与度数、上升、行星落点、当前大运/子运。
- **最小可用资料**：已知 Nakshatra + Pada，或已知当前 Mahadasha / Antardasha。
- **自然语言或 JSON 都可**。

## 工作流程

### 1) 星盘
先整理用户输入，判断当前是否足以确定：
- 恒星黄道下的月亮绝对黄经
- 月亮所在 Nakshatra
- Pada
- 起始 Mahadasha 与其余额

如果当前环境没有可靠的星历/占星计算能力，而用户也没有提供已计算好的关键资料，则**不要硬算**。只基于用户已给出的数据继续分析，并明确说明限制。

### 2) 星宿
依据月亮的 Nakshatra（必要时细化到 Pada）提炼：
- 核心牵引
- 天赋模式
- 障碍模式
- 修正方向

如果有补充资料，可进一步参考：
- 上升：人格表达与外在路径
- 土星：责任、业力负担、长期课题
- 木星：意义、保护、成长资源
- 罗喉 / 计都：执念、放大、抽离、前后业力轴

### 3) Dasha
默认使用 **Vimshottari Dasha**。

必须掌握的规则：
- 出生起始 Mahadasha 主星 = 月亮出生 Nakshatra 的守护星
- 出生时剩余 Mahadasha 余额 = **月亮在出生 Nakshatra 中剩余的弧度比例 × 该 Mahadasha 总年数**
- Mahadasha 顺序固定为：  
  **Ketu 7 → Venus 20 → Sun 6 → Moon 10 → Mars 7 → Rahu 18 → Jupiter 16 → Saturn 19 → Mercury 17**
- Antardasha 顺序从当前 Mahadasha 主星开始，按同样顺序轮转
- Antardasha 时长 = **Mahadasha 总时长 × 子运主星年数 / 120**

如果无法可靠推出精确日期，也要给出**阶段主题判断**，同时把 `时间精度` 标成 `估算` 或 `无法计算`。

## 输出要求
返回 **且只返回** 一个 JSON 对象，顶层只允许以下两个键：

```json
{
  "业力": {},
  "阶段": {}
}
```

推荐使用这个扩展结构：

```json
{
  "业力": {
    "核心牵引": "",
    "天赋模式": [],
    "障碍模式": [],
    "修正方向": [],
    "依据": {
      "月亮星宿": "",
      "Pada": "",
      "守护星": "",
      "补充因子": []
    },
    "完整度": "高|中|低"
  },
  "阶段": {
    "当前大运": {
      "名称": "",
      "起止": "",
      "主题": []
    },
    "当前子运": {
      "名称": "",
      "起止": "",
      "主题": []
    },
    "阶段说明": [],
    "注意事项": [],
    "依据": {
      "系统": "Vimshottari Dasha",
      "起运依据": "",
      "时间精度": "精确|估算|无法计算"
    }
  }
}
```

## 缺失信息时的处理
- **没有出生时间，且没有月亮度数**：不要假装知道 Nakshatra、Pada 或 Dasha 余额。
- **只知道 Nakshatra，不知道 Pada**：可以给出 Nakshatra 层面的判断，并降低 `完整度`。
- **只知道当前大运/子运，不知道起止日期**：可以分析阶段主题，把时间精度标为 `无法计算`。
- **无法判断的字段**：优先用 `null`、空数组，或简短说明如 `依据不足`。

## 风格
- 保持简洁、稳定、传统、可操作。
- 以“主题”“牵引”“修正”为中心，不做灾难式预言。
- 如果用户用中文，就用中文填写 JSON 值。
- 如果用户用其他语言，可以本地化 JSON 值，但**键名仍保持中文**。

## 支持文件
只在需要时再读取以下文件，避免把全部细节都塞进当前上下文：
- [references/vedic-reference.md](references/vedic-reference.md)：Nakshatra 顺序、守护星、Dasha 公式
- [assets/input-template.json](assets/input-template.json)：建议输入模板
- [assets/output-template.json](assets/output-template.json)：建议输出模板
- [assets/skill-spec.json](assets/skill-spec.json)：精简版机器可读规格
- [examples/minimal-example.md](examples/minimal-example.md)：最小示例
