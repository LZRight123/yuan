---
name: numerology-analysis
description: Compute symbolic numerology from a person's name and birthdate using deterministic mappings only. Use for numerology / 数字命理 / 生命路径数 / 姓名映射 requests and structured numerology JSON. Do not use for predictive fortune-telling or non-symbolic advice.
---

# Purpose

Return a numerology analysis using only the symbolic rules in this skill. The result must be deterministic, reproducible, and limited to symbolic mappings.

# Accepted input

Accept either:

1. A JSON object:
   ```json
   {
     "input": {
       "name": "",
       "birthdate": ""
     }
   }
   ```

2. A natural-language request that clearly includes both a name and a birthdate.

If one field is missing, ask only for the missing field.
If the birthdate is ambiguous (for example `03/04/2001`), ask for ISO `YYYY-MM-DD` before computing.

# Flow

1. Calculate
2. Map
3. Output

# Rules

## 1) Normalize birthdate

- Accept `YYYY-MM-DD`, `YYYY/MM/DD`, or `YYYYMMDD`.
- Remove all non-digit characters to produce `normalized_birthdate`.
- `normalized_birthdate` must contain exactly 8 digits.
- If the date cannot be normalized to 8 digits, request correction.

## 2) Reduce function

Use this deterministic reducer everywhere a reduction step is required:

```text
reduce_number(n):
  while n is not 11, 22, or 33 and n > 9:
      n = sum_of_digits(n)
  return n
```

This preserves the master numbers `11`, `22`, and `33`.

## 3) Life path number

Compute:

```text
life_path_number = reduce_number(sum(digits(normalized_birthdate)))
```

## 4) Normalize name

- Trim leading and trailing whitespace.
- Ignore spaces, hyphens, underscores, apostrophes, and common punctuation.
- Convert Latin letters to uppercase before mapping.
- Do not transliterate non-Latin scripts into Latin. Use the fallback mapping directly.

## 5) Name mapping

### Latin mapping

Use the following fixed mapping:

- `A J S = 1`
- `B K T = 2`
- `C L U = 3`
- `D M V = 4`
- `E N W = 5`
- `F O X = 6`
- `G P Y = 7`
- `H Q Z = 8`
- `I R = 9`

### Fallback mapping for non-Latin or unmapped characters

For every character that is not mapped by the Latin table:

1. Take the character's Unicode decimal code point.
2. Sum the digits of that decimal code point.
3. Reduce that sum to a single digit from `1` to `9`.
4. Use that value as the character mapping.

Example:
- Unicode code point `24352` -> `2 + 4 + 3 + 5 + 2 = 16` -> `1 + 6 = 7`

## 6) Name number

- Map every valid character after name normalization.
- Compute:

```text
name_number = reduce_number(sum(mapped_character_values))
```

## 7) Personality map

Use only this symbolic map:

- `1` -> 标签 `["独立", "主动", "开创"]`, 符号 `"起点型"`
- `2` -> 标签 `["协调", "敏感", "合作"]`, 符号 `"联结型"`
- `3` -> 标签 `["表达", "创意", "社交"]`, 符号 `"表达型"`
- `4` -> 标签 `["稳定", "秩序", "执行"]`, 符号 `"结构型"`
- `5` -> 标签 `["变化", "自由", "探索"]`, 符号 `"变化型"`
- `6` -> 标签 `["责任", "关怀", "和谐"]`, 符号 `"照护型"`
- `7` -> 标签 `["内省", "分析", "洞察"]`, 符号 `"思辨型"`
- `8` -> 标签 `["目标", "掌控", "成就"]`, 符号 `"成就型"`
- `9` -> 标签 `["理想", "包容", "完成"]`, 符号 `"完成型"`
- `11` -> 标签 `["直觉", "启发", "感召"]`, 符号 `"启发型"`
- `22` -> 标签 `["建构", "整合", "落地"]`, 符号 `"建构型"`
- `33` -> 标签 `["奉献", "滋养", "引导"]`, 符号 `"滋养型"`

# Output contract

Return JSON with exactly this top-level structure:

```json
{
  "核心数字": {
    "生命路径数": 0,
    "姓名数": 0,
    "主导数": 0,
    "辅助数": 0
  },
  "性格": {
    "生命路径": {
      "标签": [],
      "符号": ""
    },
    "姓名映射": {
      "标签": [],
      "符号": ""
    },
    "综合": {
      "标签": [],
      "说明": ""
    }
  }
}
```

## Output rules

- `主导数 = 生命路径数`
- `辅助数 = 姓名数`
- `生命路径` uses the symbolic map for `life_path_number`
- `姓名映射` uses the symbolic map for `name_number`
- `综合.标签` is the de-duplicated concatenation of `生命路径.标签` followed by `姓名映射.标签`
- `综合.说明` must be exactly:
  `以内在核心采用生命路径数的符号映射，以外在表达采用姓名数的符号映射`

# Constraints

- Pure symbolic mapping only.
- No event prediction.
- No luck, fate, or timing claims.
- No medical, legal, financial, or safety claims.
- Do not add astrology, tarot, zodiac, feng shui, MBTI, clinical psychology, or any external system.
- Do not infer real-world outcomes from the numbers.
- Do not add unsupported narrative beyond the provided labels and symbols unless the user explicitly asks for a short explanation.

# Formatting behavior

- Default to JSON only.
- If the user explicitly asks for an explanation, provide the JSON first and then a short explanation that stays fully consistent with the same mapping and constraints.

# Canonical machine-readable spec

The canonical internal spec id is `numerology_analysis`.
The runtime skill name is `numerology-analysis` for broad compatibility across agent tools.
Use `assets/spec.json` as the machine-readable reference when needed.
