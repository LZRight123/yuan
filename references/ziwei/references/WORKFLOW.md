# 工作流

## 1. 识别任务模式

- 构建系统、写 Skill、写 schema、写代码、拆规则：`design`
- 已有命盘事实：`interpret_chart`
- 仅出生资料：`chart_from_birth`

## 2. 标准化输入

统一转换为请求对象：

- `birth_datetime`
- `gender`
- `calendar_type`
- `timezone`
- `latitude` / `longitude`
- `use_true_solar_time`
- `late_zi_hour_rule`
- `school_variant`
- `chart_facts`
- `question_focus`
- `output_locale`

## 3. 先做可行性判断

### 如果是 `chart_from_birth`
必须确认：
- 是否可做公历/农历转换
- 是否可处理闰月
- 是否已配置晚子时规则
- 是否有四化表流派配置
- 是否可复现地算命宫/身宫、五行局、主辅星、运限

若无法满足，上升为设计/实现任务，不给虚构盘面。

## 4. 生成“排盘事实层”

建议顺序：

1. 时间标准化
2. 历法转换
3. 年干支 / 月 / 日 / 时支
4. 命宫 / 身宫
5. 十二宫
6. 五行局
7. 主星
8. 辅星
9. 四化
10. 三方四正 / 对宫
11. 大限
12. 流年

## 5. 生成“经验解读层”

每个主题建议包含：

- 关键词
- 优势
- 风险
- 建议
- 置信度

## 6. 输出格式

优先输出 JSON 或者“JSON + 摘要说明”，便于后续系统消费。

## 7. 校验与修正

运行：

```bash
python scripts/validate_output.py output.json
```

若输出把经验层和事实层混写，必须修正。
