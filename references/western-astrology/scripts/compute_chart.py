#!/usr/bin/env python3
"""Deterministic Western astrology natal-chart calculator.

This reference implementation intentionally focuses on:
- Tropical zodiac
- Placidus houses
- Sun through Pluto
- Ascendant / Midheaven
- Major aspects

It prefers explicit, normalized location input and does not geocode fuzzy place names.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from zoneinfo import ZoneInfo

try:
    import swisseph as swe
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: pyswisseph (import swisseph failed). "
        "Install with: pip install pyswisseph"
    ) from exc


SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

ASPECT_SPECS = {
    "Conjunction": {"angle": 0.0, "orb": 8.0},
    "Sextile": {"angle": 60.0, "orb": 4.0},
    "Square": {"angle": 90.0, "orb": 6.0},
    "Trine": {"angle": 120.0, "orb": 6.0},
    "Opposition": {"angle": 180.0, "orb": 8.0},
}

DEFAULT_FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED


def load_json_payload(input_file: Optional[str]) -> Dict[str, Any]:
    if input_file:
        return json.loads(Path(input_file).read_text(encoding="utf-8"))
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw:
            return json.loads(raw)
    raise SystemExit(
        "No JSON input provided. Use --input-file path/to/input.json or pipe JSON via stdin."
    )


def extract_input(payload: Dict[str, Any]) -> Dict[str, Any]:
    if "input" in payload and isinstance(payload["input"], dict):
        return payload["input"]
    return payload


def parse_datetime_local(value: str) -> datetime:
    # Allow common local-time formats as well as ISO-8601.
    value = value.strip()
    candidates = [
        value,
        value.replace(" ", "T"),
    ]
    for item in candidates:
        try:
            return datetime.fromisoformat(item)
        except ValueError:
            pass

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise SystemExit(f"Unsupported birth_datetime format: {value!r}")


def normalize_longitude(value: float) -> float:
    return value % 360.0


def sign_info(longitude: float) -> Dict[str, Any]:
    longitude = normalize_longitude(longitude)
    sign_index = int(math.floor(longitude / 30.0))
    degree_in_sign = longitude % 30.0
    return {
        "longitude": round(longitude, 6),
        "sign": SIGNS[sign_index],
        "degree_in_sign": round(degree_in_sign, 6),
    }


def parse_location(location: Any) -> Dict[str, Any]:
    if isinstance(location, str):
        raise SystemExit(
            "Location must be normalized before deterministic calculation. "
            "Provide an object with lat, lon, and timezone."
        )
    if not isinstance(location, dict):
        raise SystemExit("location must be an object or a string.")

    lat = location.get("lat", location.get("latitude"))
    lon = location.get("lon", location.get("longitude"))
    tz_name = location.get("timezone", location.get("tz"))
    label = location.get("label")

    missing = [k for k, v in {"lat": lat, "lon": lon, "timezone": tz_name}.items() if v is None]
    if missing:
        raise SystemExit(
            f"Normalized location is missing required fields: {', '.join(missing)}"
        )

    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError) as exc:
        raise SystemExit("lat and lon must be numeric.") from exc

    if not -90.0 <= lat <= 90.0:
        raise SystemExit("lat must be between -90 and 90.")
    if not -180.0 <= lon <= 180.0:
        raise SystemExit("lon must be between -180 and 180.")

    try:
        ZoneInfo(str(tz_name))
    except Exception as exc:
        raise SystemExit(f"Invalid timezone: {tz_name!r}") from exc

    return {
        "label": label,
        "lat": lat,
        "lon": lon,
        "timezone": str(tz_name),
    }


def normalize_birth_datetime(dt_value: str, tz_name: Optional[str]) -> Tuple[datetime, datetime]:
    local_dt = parse_datetime_local(dt_value)
    if local_dt.tzinfo is None:
        if not tz_name:
            raise SystemExit(
                "birth_datetime is timezone-naive and no location.timezone was provided."
            )
        local_dt = local_dt.replace(tzinfo=ZoneInfo(tz_name))
    utc_dt = local_dt.astimezone(timezone.utc)
    return local_dt, utc_dt


def julian_day_from_utc(utc_dt: datetime) -> float:
    hour = (
        utc_dt.hour
        + utc_dt.minute / 60.0
        + utc_dt.second / 3600.0
        + utc_dt.microsecond / 3_600_000_000.0
    )
    return float(swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, hour))


def resolve_house_system(name: Optional[str]) -> bytes:
    if not name:
        return b"P"
    normalized = str(name).strip().lower()
    if normalized in {"placidus", "p"}:
        return b"P"
    raise SystemExit(
        f"Unsupported house_system: {name!r}. "
        "This reference calculator currently supports Placidus only."
    )


def build_position(longitude: float, speed_longitude: float) -> Dict[str, Any]:
    data = sign_info(longitude)
    data["retrograde"] = speed_longitude < 0
    data["speed_longitude"] = round(speed_longitude, 8)
    return data


def calc_planets(jd_ut: float) -> Dict[str, Dict[str, Any]]:
    results: Dict[str, Dict[str, Any]] = {}
    for name, planet_id in PLANETS.items():
        xx, _retflags = swe.calc_ut(jd_ut, planet_id, DEFAULT_FLAGS)
        longitude = xx[0]
        speed_longitude = xx[3]
        results[name] = build_position(longitude, speed_longitude)
    return results


def calc_houses(jd_ut: float, lat: float, lon: float, hsys: bytes) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, hsys, 0)
    houses: Dict[str, Dict[str, Any]] = {}
    for idx, cusp_longitude in enumerate(cusps, start=1):
        info = sign_info(cusp_longitude)
        houses[str(idx)] = {
            "cusp_longitude": info["longitude"],
            "sign": info["sign"],
            "degree_in_sign": info["degree_in_sign"],
        }

    asc_info = sign_info(ascmc[0])
    mc_info = sign_info(ascmc[1])
    angles = {
        "Ascendant": {
            "longitude": asc_info["longitude"],
            "sign": asc_info["sign"],
            "degree_in_sign": asc_info["degree_in_sign"],
        },
        "Midheaven": {
            "longitude": mc_info["longitude"],
            "sign": mc_info["sign"],
            "degree_in_sign": mc_info["degree_in_sign"],
        },
    }
    return houses, angles


def longitude_in_arc(x: float, start: float, end: float) -> bool:
    x = normalize_longitude(x)
    start = normalize_longitude(start)
    end = normalize_longitude(end)
    if start < end:
        return start <= x < end
    return x >= start or x < end


def assign_houses(
    planet_positions: Dict[str, Dict[str, Any]],
    houses: Dict[str, Dict[str, Any]],
) -> Dict[str, int]:
    cusp_map = {int(k): v["cusp_longitude"] for k, v in houses.items()}
    placements: Dict[str, int] = {}
    for planet_name, pdata in planet_positions.items():
        lon = pdata["longitude"]
        assigned = None
        for house_num in range(1, 13):
            start = cusp_map[house_num]
            end = cusp_map[1] if house_num == 12 else cusp_map[house_num + 1]
            if longitude_in_arc(lon, start, end):
                assigned = house_num
                break
        placements[planet_name] = assigned if assigned is not None else 12
    return placements


def angular_distance(long1: float, long2: float) -> float:
    delta = abs(normalize_longitude(long1) - normalize_longitude(long2))
    if delta > 180.0:
        delta = 360.0 - delta
    return delta


def compute_aspects(objects: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    names = list(objects.keys())
    aspects: List[Dict[str, Any]] = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            name1 = names[i]
            name2 = names[j]
            lon1 = objects[name1]["longitude"]
            lon2 = objects[name2]["longitude"]
            delta = angular_distance(lon1, lon2)
            for aspect_name, spec in ASPECT_SPECS.items():
                orb = abs(delta - spec["angle"])
                if orb <= spec["orb"]:
                    aspects.append(
                        {
                            "object1": name1,
                            "object2": name2,
                            "type": aspect_name,
                            "exact_angle": spec["angle"],
                            "actual_angle": round(delta, 6),
                            "orb": round(orb, 6),
                        }
                    )
                    break
    aspects.sort(key=lambda item: (item["orb"], item["type"], item["object1"], item["object2"]))
    return aspects


def build_chart(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = extract_input(payload)
    birth_datetime = data.get("birth_datetime")
    location = data.get("location")
    house_system = data.get("house_system", "Placidus")
    zodiac_type = data.get("zodiac_type", "Tropical")

    if not birth_datetime:
        raise SystemExit("Missing required field: birth_datetime")
    if location is None:
        raise SystemExit("Missing required field: location")

    normalized_location = parse_location(location)
    if str(zodiac_type).strip().lower() not in {"tropical", ""}:
        raise SystemExit(
            "This reference calculator currently supports Tropical zodiac only."
        )

    local_dt, utc_dt = normalize_birth_datetime(str(birth_datetime), normalized_location["timezone"])
    jd_ut = julian_day_from_utc(utc_dt)
    hsys = resolve_house_system(house_system)

    ephe_path = os.environ.get("SE_EPHE_PATH")
    if ephe_path:
        swe.set_ephe_path(ephe_path)

    planet_positions = calc_planets(jd_ut)
    houses, angles = calc_houses(jd_ut, normalized_location["lat"], normalized_location["lon"], hsys)
    planet_house_placement = assign_houses(planet_positions, houses)

    aspect_objects: Dict[str, Dict[str, Any]] = {}
    aspect_objects.update(planet_positions)
    aspect_objects.update(angles)
    aspects = compute_aspects(aspect_objects)

    return {
        "meta": {
            "calculator": "scripts/compute_chart.py",
            "backend": "pyswisseph",
            "logical_name": "astrology_analysis",
            "cross_tool_slug": "astrology-analysis",
            "zodiac_type": "Tropical",
            "house_system": "Placidus",
            "julian_day_ut": round(jd_ut, 8),
        },
        "input_normalized": {
            "birth_datetime_local": local_dt.isoformat(),
            "birth_datetime_utc": utc_dt.isoformat(),
            "location": normalized_location,
        },
        "planet_positions": planet_positions,
        "angles": angles,
        "houses": houses,
        "planet_house_placement": planet_house_placement,
        "aspects": aspects,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic natal-chart calculator.")
    parser.add_argument("--input-file", help="Path to input JSON.")
    parser.add_argument("--output-file", help="Optional path to write output JSON.")
    args = parser.parse_args()

    payload = load_json_payload(args.input_file)
    chart = build_chart(payload)

    text = json.dumps(chart, ensure_ascii=False, indent=2)
    if args.output_file:
        Path(args.output_file).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
