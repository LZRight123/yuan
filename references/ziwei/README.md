# Ziwei Analysis Skill

一个面向 **Claude Code、Codex、OpenAI Skills API、以及兼容 Agent Skills 标准的 AI 代理**的紫微斗数技能包。

## 这个技能包做什么

它把紫微斗数任务拆成三种模式：

1. `design`：做 Skill / 规则系统 / schema / API / 代码架构
2. `interpret_chart`：解释用户已经提供的命盘事实
3. `chart_from_birth`：只在有**可信排盘引擎或规则表**时，才从出生资料生成命盘

## 这个技能包不做什么

- 不在缺少确定性排盘规则时虚构星曜位置
- 不把经验性解读伪装成科学结论
- 不忽略晚子时、流派差异、闰月、时区等歧义来源

## 目录结构

```text
ziwei-analysis/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── chart-facts-schema.json
│   ├── config-example.json
│   ├── input-schema.json
│   ├── output-template.json
│   └── rules-structure.json
├── examples/
│   ├── birth-data-request.md
│   ├── design-request.md
│   └── interpret-chart-request.md
├── references/
│   ├── DOMAIN_MODEL.md
│   ├── LIMITS_AND_GUARDRAILS.md
│   └── WORKFLOW.md
└── scripts/
    ├── request_guard.py
    └── validate_output.py
```

## 安装到 Claude Code

### 项目级
把整个 `ziwei-analysis/` 目录复制到：

```bash
.claude/skills/ziwei-analysis/
```

### 个人级
复制到：

```bash
~/.claude/skills/ziwei-analysis/
```

## 安装到 Codex

### 仓库级
把整个 `ziwei-analysis/` 目录复制到：

```bash
.agents/skills/ziwei-analysis/
```

### 用户级
复制到：

```bash
$HOME/.agents/skills/ziwei-analysis/
```

## 上传到 OpenAI Skills API

你可以直接上传这个技能包 zip，或把目录作为 multipart 文件上传。

```bash
curl -X POST 'https://api.openai.com/v1/skills'   -H "Authorization: Bearer $OPENAI_API_KEY"   -F 'files=@./ziwei-analysis-skill.zip;type=application/zip'
```

## 推荐的显式调用方式

### Claude Code
```text
/ziwei-analysis 请把紫微斗数系统拆成排盘层与解释层，并输出 JSON schema
```

### Codex
```text
Use the ziwei-analysis skill to design a deterministic Ziwei charting contract and a heuristic interpretation layer.
```

## 推荐的任务输入

```json
{
  "task_mode": "auto",
  "birth_datetime": "1992-08-14 23:40",
  "gender": "female",
  "calendar_type": "solar",
  "timezone": "Asia/Shanghai",
  "late_zi_hour_rule": "cross_day",
  "school_variant": "traditional_fullbook_v1",
  "chart_facts": null,
  "question_focus": ["事业", "财运"],
  "output_locale": "zh-CN"
}
```

## Helper 脚本

### 1) 检查请求是否足够支持排盘
```bash
python scripts/request_guard.py request.json
```

### 2) 检查输出结构是否合法
```bash
python scripts/validate_output.py output.json
```

## 实战建议

- 如果是 **构建系统**：先用 `design` 模式
- 如果是 **解释现成命盘**：把用户提供的宫位/星曜转成 `chart_facts`
- 如果是 **从出生信息直接算盘**：先确认你所在环境真的有可靠排盘实现；没有就不要编造

## 版本建议

- `1.x`：规则结构、schema、输出格式稳定
- `2.x`：再引入真实排盘引擎、OCR、盘面截图解析、流月/流日支持

## 可选：增强发现率

### Codex 的 `AGENTS.md` 片段
在项目根目录的 `AGENTS.md` 里加入：

```md
## Ziwei workflow
- For 紫微斗数 / Ziwei Dou Shu system design, schema design, or chart interpretation tasks, prefer the `ziwei-analysis` skill in `.agents/skills/ziwei-analysis`.
- Do not fabricate chart facts from birth data unless a deterministic chart engine is available.
- Keep deterministic charting separate from heuristic interpretation.
```

### Claude Code 的 `CLAUDE.md` 片段
在项目根目录的 `CLAUDE.md` 或 `.claude/CLAUDE.md` 里加入：

```md
## Ziwei workflow
- For 紫微斗数 tasks, prefer the `ziwei-analysis` skill.
- Separate chart facts from interpretation.
- Surface ambiguity around calendar type, late 子时, timezone, and school variant.
```
