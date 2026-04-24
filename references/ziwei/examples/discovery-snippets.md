# 发现率增强片段

## AGENTS.md（Codex）

```md
## Ziwei workflow
- For 紫微斗数 / Ziwei Dou Shu system design, schema design, or chart interpretation tasks, prefer the `ziwei-analysis` skill in `.agents/skills/ziwei-analysis`.
- Do not fabricate chart facts from birth data unless a deterministic chart engine is available.
- Keep deterministic charting separate from heuristic interpretation.
```

## CLAUDE.md（Claude Code）

```md
## Ziwei workflow
- For 紫微斗数 tasks, prefer the `ziwei-analysis` skill.
- Separate chart facts from interpretation.
- Surface ambiguity around calendar type, late 子时, timezone, and school variant.
```
