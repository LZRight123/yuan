# 示例输入与输出

以下示例都直接使用已归一化的农历组件，避免把误差引入农历转换步骤。

## 示例 1

输入：
```json
{
  "lunar_components": {
    "year_ganzhi": "甲子",
    "month": 1,
    "day": 1,
    "hour_branch": "子",
    "is_leap_month": false
  }
}
```

输出：
```json
{
  "skill_name": "chenggu-analysis",
  "api_name": "chenggu_analysis",
  "input_normalized": {
    "calendar_type_used": "lunar_components",
    "year_ganzhi": "甲子",
    "lunar_month": 1,
    "lunar_day": 1,
    "hour_branch": "子",
    "is_leap_month": false
  },
  "weights": {
    "year_weight_qian": 12,
    "month_weight_qian": 6,
    "day_weight_qian": 5,
    "hour_weight_qian": 16
  },
  "total_weight": {
    "qian": 39,
    "display": "三两九钱",
    "decimal_liang": 3.9
  },
  "grade": "中",
  "verse_canonical": "此命终身运不通，劳劳作事尽皆空。苦心竭力成家计，到得那时在梦中。",
  "analysis": {
    "trajectory_tags": [
      "early_hardship"
    ],
    "career": "略弱",
    "wealth": "偏弱",
    "marriage": "中性",
    "scores": {
      "career": -1,
      "wealth": -2,
      "marriage": 0
    }
  },
  "advice": "宜稳步推进，少做高杠杆冒进决策，先补基本盘。；歌诀偏向先难后成或资源承接不足，建议把注意力放在稳定积累、长期技能与风险控制上。；婚姻维度仅依据歌诀显词做弱规则映射，宜谨慎解读。",
  "display_zh": {
    "骨重明细": {
      "年": "12钱",
      "月": "6钱",
      "日": "5钱",
      "时": "16钱"
    },
    "总骨重": "三两九钱",
    "等级": "中",
    "原始歌诀": "此命终身运不通，劳劳作事尽皆空。苦心竭力成家计，到得那时在梦中。",
    "结构化分析": {
      "事业": "略弱",
      "财运": "偏弱",
      "婚姻": "中性"
    },
    "建议": "宜稳步推进，少做高杠杆冒进决策，先补基本盘。；歌诀偏向先难后成或资源承接不足，建议把注意力放在稳定积累、长期技能与风险控制上。；婚姻维度仅依据歌诀显词做弱规则映射，宜谨慎解读。"
  },
  "limitations": [
    "权重查表是确定规则，但歌诀解释属于民俗文本映射。",
    "若输入为公历，农历转换结果会影响最终骨重。",
    "不同流派存在异表；本技能固定采用 standard-51qian 版本。"
  ]
}
```

## 示例 2

输入：
```json
{
  "lunar_components": {
    "year_ganzhi": "甲午",
    "month": 8,
    "day": 18,
    "hour_branch": "午",
    "is_leap_month": false
  }
}
```

输出：
```json
{
  "skill_name": "chenggu-analysis",
  "api_name": "chenggu_analysis",
  "input_normalized": {
    "calendar_type_used": "lunar_components",
    "year_ganzhi": "甲午",
    "lunar_month": 8,
    "lunar_day": 18,
    "hour_branch": "午",
    "is_leap_month": false
  },
  "weights": {
    "year_weight_qian": 15,
    "month_weight_qian": 15,
    "day_weight_qian": 18,
    "hour_weight_qian": 10
  },
  "total_weight": {
    "qian": 58,
    "display": "五两八钱",
    "decimal_liang": 5.8
  },
  "grade": "高",
  "verse_canonical": "平生衣食自然来，名利双全富贵偕。金榜题名登甲第，紫袍玉带走金阶。",
  "analysis": {
    "trajectory_tags": [
      "scholar_official"
    ],
    "career": "很强",
    "wealth": "很强",
    "marriage": "中性",
    "scores": {
      "career": 4,
      "wealth": 3,
      "marriage": 0
    }
  },
  "advice": "歌诀偏吉，但仍应把“优势兑现”为长期纪律、能力与合作质量。；歌诀偏吉，但仍应把“优势兑现”为长期纪律、能力与合作质量。；婚姻维度仅依据歌诀显词做弱规则映射，宜谨慎解读。",
  "display_zh": {
    "骨重明细": {
      "年": "15钱",
      "月": "15钱",
      "日": "18钱",
      "时": "10钱"
    },
    "总骨重": "五两八钱",
    "等级": "高",
    "原始歌诀": "平生衣食自然来，名利双全富贵偕。金榜题名登甲第，紫袍玉带走金阶。",
    "结构化分析": {
      "事业": "很强",
      "财运": "很强",
      "婚姻": "中性"
    },
    "建议": "歌诀偏吉，但仍应把“优势兑现”为长期纪律、能力与合作质量。；歌诀偏吉，但仍应把“优势兑现”为长期纪律、能力与合作质量。；婚姻维度仅依据歌诀显词做弱规则映射，宜谨慎解读。"
  },
  "limitations": [
    "权重查表是确定规则，但歌诀解释属于民俗文本映射。",
    "若输入为公历，农历转换结果会影响最终骨重。",
    "不同流派存在异表；本技能固定采用 standard-51qian 版本。"
  ]
}
```

## 示例 3

输入：
```json
{
  "lunar_components": {
    "year_ganzhi": "己卯",
    "month": 9,
    "day": 18,
    "hour_branch": "巳",
    "is_leap_month": false
  }
}
```

输出：
```json
{
  "skill_name": "chenggu-analysis",
  "api_name": "chenggu_analysis",
  "input_normalized": {
    "calendar_type_used": "lunar_components",
    "year_ganzhi": "己卯",
    "lunar_month": 9,
    "lunar_day": 18,
    "hour_branch": "巳",
    "is_leap_month": false
  },
  "weights": {
    "year_weight_qian": 19,
    "month_weight_qian": 18,
    "day_weight_qian": 18,
    "hour_weight_qian": 16
  },
  "total_weight": {
    "qian": 71,
    "display": "七两一钱",
    "decimal_liang": 7.1
  },
  "grade": "高",
  "verse_canonical": "此命生成大不同，公侯卿相在其中。一生自有逍遥福，富贵荣华极品隆。",
  "analysis": {
    "trajectory_tags": [
      "scholar_official"
    ],
    "career": "很强",
    "wealth": "很强",
    "marriage": "中性",
    "scores": {
      "career": 2,
      "wealth": 4,
      "marriage": 0
    }
  },
  "advice": "歌诀偏吉，但仍应把“优势兑现”为长期纪律、能力与合作质量。；歌诀偏吉，但仍应把“优势兑现”为长期纪律、能力与合作质量。；婚姻维度仅依据歌诀显词做弱规则映射，宜谨慎解读。",
  "display_zh": {
    "骨重明细": {
      "年": "19钱",
      "月": "18钱",
      "日": "18钱",
      "时": "16钱"
    },
    "总骨重": "七两一钱",
    "等级": "高",
    "原始歌诀": "此命生成大不同，公侯卿相在其中。一生自有逍遥福，富贵荣华极品隆。",
    "结构化分析": {
      "事业": "很强",
      "财运": "很强",
      "婚姻": "中性"
    },
    "建议": "歌诀偏吉，但仍应把“优势兑现”为长期纪律、能力与合作质量。；歌诀偏吉，但仍应把“优势兑现”为长期纪律、能力与合作质量。；婚姻维度仅依据歌诀显词做弱规则映射，宜谨慎解读。"
  },
  "limitations": [
    "权重查表是确定规则，但歌诀解释属于民俗文本映射。",
    "若输入为公历，农历转换结果会影响最终骨重。",
    "不同流派存在异表；本技能固定采用 standard-51qian 版本。"
  ]
}
```
