# Prompt Examples

## Positive triggers

### Chinese
- 请根据我的出生时间和地点计算本命盘，并按人格、事业、情感输出 JSON。
- 帮我看太阳、月亮、上升，还有主要相位。
- 根据星盘分析我的事业方向和关系模式。

### English
- Compute a Western tropical natal chart from my birth data and interpret the houses and aspects.
- Give me a personality, career, and relationships reading from my birth chart.

## Negative / skip triggers

- Give me today's Aries horoscope.
- Please read my tarot cards.
- 帮我算八字。
- Explain astronomical precession only.

## Recommended normalized input

```json
{
  "input": {
    "birth_datetime": "1990-01-01 08:00:00",
    "location": {
      "label": "Beijing, China",
      "lat": 39.9042,
      "lon": 116.4074,
      "timezone": "Asia/Shanghai"
    },
    "house_system": "Placidus",
    "zodiac_type": "Tropical",
    "language": "zh-CN"
  }
}
```
