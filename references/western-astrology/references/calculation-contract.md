# Calculation Contract

This skill separates **deterministic chart computation** from **heuristic interpretation**.

## 1. Supported default mode

- Zodiac: Tropical
- House system: Placidus
- Planets:
  - Sun
  - Moon
  - Mercury
  - Venus
  - Mars
  - Jupiter
  - Saturn
  - Uranus
  - Neptune
  - Pluto
- Angles:
  - Ascendant
  - Midheaven

## 2. Required normalized inputs

The calculation stage should work from:

```json
{
  "input": {
    "birth_datetime": "1990-01-01 08:00:00",
    "location": {
      "lat": 39.9042,
      "lon": 116.4074,
      "timezone": "Asia/Shanghai"
    },
    "house_system": "Placidus",
    "zodiac_type": "Tropical"
  }
}
```

## 3. Time normalization

1. Parse the birth datetime in local time.
2. Determine the timezone from:
   - an offset already present in the datetime string, or
   - `location.timezone`
3. Convert to UTC.
4. Compute Julian Day from UTC.

Never silently assume a timezone if neither the input datetime nor the normalized location provides one.

## 4. Longitude and sign mapping

Normalize every longitude to the half-open interval `[0, 360)`.

Sign index:

- 0: Aries
- 1: Taurus
- 2: Gemini
- 3: Cancer
- 4: Leo
- 5: Virgo
- 6: Libra
- 7: Scorpio
- 8: Sagittarius
- 9: Capricorn
- 10: Aquarius
- 11: Pisces

Derive:

- `sign = floor(longitude / 30)`
- `degree_in_sign = longitude % 30`

## 5. House cusps and placements

Return:

- 12 house cusps
- Ascendant
- Midheaven
- each planet's house placement

A planet belongs to the house whose cusp interval contains its longitude, using wrap-around logic between House 12 and House 1.

## 6. Aspects

For any two longitudes:

```text
delta = abs(long1 - long2)
if delta > 180:
    delta = 360 - delta
```

Detect these major aspects:

- Conjunction: 0° ± 8°
- Sextile: 60° ± 4°
- Square: 90° ± 6°
- Trine: 120° ± 6°
- Opposition: 180° ± 8°

Recommended aspect objects:

- all planet ↔ planet pairs
- planet ↔ Ascendant
- planet ↔ Midheaven

## 7. Required derived features

The deterministic stage should produce:

- `planet_positions`
- `angles`
- `houses`
- `planet_house_placement`
- `aspects`

## 8. Unknown or weak inputs

### Missing birth time
Do not fabricate:

- Ascendant
- Midheaven
- house cusps
- exact house placements

A limited sign-based reading is acceptable only if explicitly marked as partial.

### Fuzzy location
A city string may be acceptable during normalization, but not as the final deterministic calculation input.

## 9. Interpretation boundary

Everything after chart computation is heuristic:

- personality
- career
- relationships
- advice

Those outputs must be framed as interpretive rules, not scientific proof.
