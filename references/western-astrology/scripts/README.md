# Scripts

## compute_chart.py

Deterministic reference calculator for Western natal charts.

### What it does

- parses normalized JSON input
- converts local birth time to UTC
- computes Sun through Pluto
- computes Ascendant and Midheaven
- computes 12 Placidus house cusps
- assigns each planet to a house
- computes major aspects

### Dependency

```bash
pip install pyswisseph
```

### Usage

```bash
python scripts/compute_chart.py --input-file examples/sample_input.json
```

or

```bash
cat examples/sample_input.json | python scripts/compute_chart.py
```

### Output

JSON with:

- `meta`
- `input_normalized`
- `planet_positions`
- `angles`
- `houses`
- `planet_house_placement`
- `aspects`

### Current reference limits

This script intentionally supports:

- Tropical zodiac
- Placidus houses
- normalized location object with lat/lon/timezone

It does **not** geocode city names.
