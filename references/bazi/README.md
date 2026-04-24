# 八字算命 Skill 交付包

这个包包含 4 类内容：

1. **规则文档**  
   - `bazi_skill_spec.docx`：面向产品/策划/算法的说明文档。

2. **机器可读配置**  
   - `bazi_analysis_skill.json`
   - `bazi_analysis_skill.yaml`

3. **参考实现**  
   - `bazi_skill_engine.py`：可直接运行的 Python CLI，内置节气换算、四柱排盘、十神、旺衰、格局、神煞、大运与流年规则。

4. **示例**  
   - `examples/sample_request.json`
   - `examples/sample_output.json`

## 统一口径

- 年柱：**立春切年**
- 月柱：**12 节切月**
- 日柱：**23:00 子初换日**
- 时柱：**两小时一时辰**
- 旺衰：**月令 + 五行加权**
- 格局：**只判正格 / 从格**
- 神煞：**只保留桃花、天乙贵人**
- 真太阳时：**不修正**

## 快速运行

```bash
python bazi_skill_engine.py \
  --birth-datetime "1992-08-14T21:30:00+08:00" \
  --gender male \
  --dayun-count 8 \
  --liunian-start-year 2026 \
  --liunian-count 10 \
  --output result.json
```

## 运行依赖

```bash
pip install pyswisseph
```

> 代码里使用的是 `import swisseph as swe`。

## 输出结构

参考实现输出三个顶层字段：

- `chart`：排盘、藏干、十神、节令、神煞、大运、流年
- `analysis`：五行、旺衰、格局、性格、事业、财运、婚姻、建议
- `template_output`：按“命盘 / 五行分析 / 性格分析 / 事业 / 财运 / 婚姻 / 建议”模板展开

## 示例文件

`examples/sample_request.json` 使用的示例输入：

```json
{
  "birth_datetime": "1992-08-14T21:30:00+08:00",
  "gender": "male"
}
```

对应输出已经写入 `examples/sample_output.json`。

## 说明

这套 Skill 已经尽量做成**规则可计算**版本；其中：

- **确定性部分**：节气、四柱、五行、十神、神煞、大运/流年顺逆与起运
- **经验推断部分**：旺衰阈值、正格/从格工程化判定、性格/事业/财运/婚姻文案映射
