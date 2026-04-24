#!/usr/bin/env python3
"""参考实现：八字算命 Skill 规则引擎

依赖：pyswisseph（import 名称为 swisseph）
用法：
  python bazi_skill_engine.py --birth-datetime "1992-08-14T21:30:00+08:00" --gender male --output result.json
"""
from __future__ import annotations
import argparse
import json
import math
from datetime import datetime, timedelta, timezone
import swisseph as swe

STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

STEM_META = {'甲': {'element': '木', 'polarity': '阳', 'index': 1}, '乙': {'element': '木', 'polarity': '阴', 'index': 2}, '丙': {'element': '火', 'polarity': '阳', 'index': 3}, '丁': {'element': '火', 'polarity': '阴', 'index': 4}, '戊': {'element': '土', 'polarity': '阳', 'index': 5}, '己': {'element': '土', 'polarity': '阴', 'index': 6}, '庚': {'element': '金', 'polarity': '阳', 'index': 7}, '辛': {'element': '金', 'polarity': '阴', 'index': 8}, '壬': {'element': '水', 'polarity': '阳', 'index': 9}, '癸': {'element': '水', 'polarity': '阴', 'index': 10}}

BRANCH_PRIMARY_ELEMENT = {'子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'}

BRANCH_HIDDEN_STEMS = {'子': ['癸'], '丑': ['己', '癸', '辛'], '寅': ['甲', '丙', '戊'], '卯': ['乙'], '辰': ['戊', '乙', '癸'], '巳': ['丙', '戊', '庚'], '午': ['丁', '己'], '未': ['己', '丁', '乙'], '申': ['庚', '壬', '戊'], '酉': ['辛'], '戌': ['戊', '辛', '丁'], '亥': ['壬', '甲']}

FIVE_ELEMENT_GENERATE = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}

FIVE_ELEMENT_CONTROL = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}

HIDDEN_STEM_WEIGHTS = {1: [1.0], 2: [0.7, 0.3], 3: [0.7, 0.2, 0.1]}

JIE_RULES = [{'name': '立春', 'angle': 315.0, 'month_order': 1, 'branch': '寅'}, {'name': '惊蛰', 'angle': 345.0, 'month_order': 2, 'branch': '卯'}, {'name': '清明', 'angle': 15.0, 'month_order': 3, 'branch': '辰'}, {'name': '立夏', 'angle': 45.0, 'month_order': 4, 'branch': '巳'}, {'name': '芒种', 'angle': 75.0, 'month_order': 5, 'branch': '午'}, {'name': '小暑', 'angle': 105.0, 'month_order': 6, 'branch': '未'}, {'name': '立秋', 'angle': 135.0, 'month_order': 7, 'branch': '申'}, {'name': '白露', 'angle': 165.0, 'month_order': 8, 'branch': '酉'}, {'name': '寒露', 'angle': 195.0, 'month_order': 9, 'branch': '戌'}, {'name': '立冬', 'angle': 225.0, 'month_order': 10, 'branch': '亥'}, {'name': '大雪', 'angle': 255.0, 'month_order': 11, 'branch': '子'}, {'name': '小寒', 'angle': 285.0, 'month_order': 12, 'branch': '丑'}]

PEACH_MAP = {'申': '酉', '子': '酉', '辰': '酉', '寅': '卯', '午': '卯', '戌': '卯', '亥': '子', '卯': '子', '未': '子', '巳': '午', '酉': '午', '丑': '午'}

TIANYI_MAP = {'甲': ['丑', '未'], '戊': ['丑', '未'], '庚': ['丑', '未'], '乙': ['子', '申'], '己': ['子', '申'], '丙': ['亥', '酉'], '丁': ['亥', '酉'], '辛': ['寅', '午'], '壬': ['卯', '巳'], '癸': ['卯', '巳']}

TEN_GOD_ORDER = ['比肩', '劫财', '食神', '伤官', '偏财', '正财', '七杀', '正官', '偏印', '正印']

TEN_GOD_CATEGORY_MAP = {'比肩': '比劫', '劫财': '比劫', '食神': '食伤', '伤官': '食伤', '偏财': '财', '正财': '财', '七杀': '官杀', '正官': '官杀', '偏印': '印', '正印': '印'}

CATEGORY_ORDER = ['比劫', '食伤', '财', '官杀', '印']

PERSONALITY_TAGS = {'比劫': ['独立', '竞争', '主导'], '食伤': ['表达', '创意', '输出'], '财': ['务实', '结果导向', '资源意识'], '官杀': ['责任', '规则', '执行'], '印': ['学习', '内省', '稳定']}

SIxty = ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯', '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑', '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥']

CYCLE_TO_INDEX = {'甲子': 0, '乙丑': 1, '丙寅': 2, '丁卯': 3, '戊辰': 4, '己巳': 5, '庚午': 6, '辛未': 7, '壬申': 8, '癸酉': 9, '甲戌': 10, '乙亥': 11, '丙子': 12, '丁丑': 13, '戊寅': 14, '己卯': 15, '庚辰': 16, '辛巳': 17, '壬午': 18, '癸未': 19, '甲申': 20, '乙酉': 21, '丙戌': 22, '丁亥': 23, '戊子': 24, '己丑': 25, '庚寅': 26, '辛卯': 27, '壬辰': 28, '癸巳': 29, '甲午': 30, '乙未': 31, '丙申': 32, '丁酉': 33, '戊戌': 34, '己亥': 35, '庚子': 36, '辛丑': 37, '壬寅': 38, '癸卯': 39, '甲辰': 40, '乙巳': 41, '丙午': 42, '丁未': 43, '戊申': 44, '己酉': 45, '庚戌': 46, '辛亥': 47, '壬子': 48, '癸丑': 49, '甲寅': 50, '乙卯': 51, '丙辰': 52, '丁巳': 53, '戊午': 54, '己未': 55, '庚申': 56, '辛酉': 57, '壬戌': 58, '癸亥': 59}

def parse_iso_datetime(value: str) -> datetime:
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("birth_datetime 必须包含时区，例如 1992-08-14T21:30:00+08:00")
    return dt


def to_jd_ut(dt: datetime) -> float:
    dt_utc = dt.astimezone(timezone.utc)
    hour = dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600 + dt_utc.microsecond/3_600_000_000
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour)


def jd_ut_to_datetime(jd: float, tzinfo) -> datetime:
    y,m,d,hour = swe.revjul(jd, swe.GREG_CAL)
    base = datetime(y,m,d,tzinfo=timezone.utc)
    dt_utc = base + timedelta(hours=hour)
    return dt_utc.astimezone(tzinfo)


def sun_longitude(dt: datetime) -> float:
    jd = to_jd_ut(dt)
    lon = swe.calc_ut(jd, swe.SUN)[0][0] % 360.0
    return lon


def stem_by_index(idx: int) -> str:
    return STEMS[idx-1]


def branch_by_index(idx: int) -> str:
    return BRANCHES[idx-1]


def in_cyclic_interval(value: float, start: float, end: float) -> bool:
    if start < end:
        return start <= value < end
    return value >= start or value < end


def get_lichun(year: int, tzinfo) -> datetime:
    start = datetime(year,1,1,tzinfo=timezone.utc)
    jd = swe.solcross_ut(315.0, to_jd_ut(start))
    return jd_ut_to_datetime(jd, tzinfo)


def determine_month_rule(lon: float):
    for i, rule in enumerate(JIE_RULES):
        start = rule["angle"]
        end = JIE_RULES[(i+1)%12]["angle"]
        if in_cyclic_interval(lon, start, end):
            return i, rule
    raise RuntimeError(f"无法判定月令: {lon}")


def jdn_from_date(y: int, m: int, d: int) -> int:
    a = math.floor((14 - m) / 12)
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    return d + math.floor((153*m2 + 2)/5) + 365*y2 + math.floor(y2/4) - math.floor(y2/100) + math.floor(y2/400) - 32045


def next_jie_after(birth_dt: datetime, current_rule_index: int, epsilon_days: float = 1e-6) -> dict:
    tzinfo = birth_dt.tzinfo
    next_rule = JIE_RULES[(current_rule_index + 1) % 12]
    jd = swe.solcross_ut(next_rule["angle"], to_jd_ut(birth_dt) + epsilon_days)
    return {**next_rule, "datetime": jd_ut_to_datetime(jd, tzinfo)}


def prev_jie_before(birth_dt: datetime, current_rule_index: int) -> dict:
    tzinfo = birth_dt.tzinfo
    current_rule = JIE_RULES[current_rule_index]
    jd = swe.solcross_ut(current_rule["angle"], to_jd_ut(birth_dt) - 40.0)
    dt = jd_ut_to_datetime(jd, tzinfo)
    # if numeric weirdness returns slightly after birth (e.g. when birth exactly on boundary), step a bit more back
    if dt > birth_dt + timedelta(seconds=1):
        jd = swe.solcross_ut(current_rule["angle"], to_jd_ut(birth_dt) - 370.0)
        dt = jd_ut_to_datetime(jd, tzinfo)
    return {**current_rule, "datetime": dt}


def pillar_index(stem: str, branch: str) -> int:
    return CYCLE_TO_INDEX[stem + branch]


def shift_pillar(stem: str, branch: str, offset: int) -> tuple[str,str]:
    idx = pillar_index(stem, branch)
    new = SIxty[(idx + offset) % 60]
    return new[0], new[1]


def relation_category(dm_element: str, target_element: str) -> str:
    if target_element == dm_element:
        return "same"
    if FIVE_ELEMENT_GENERATE[dm_element] == target_element:
        return "output"
    if FIVE_ELEMENT_CONTROL[dm_element] == target_element:
        return "wealth"
    if FIVE_ELEMENT_CONTROL[target_element] == dm_element:
        return "authority"
    if FIVE_ELEMENT_GENERATE[target_element] == dm_element:
        return "resource"
    raise RuntimeError("无效五行关系")


def ten_god(day_stem: str, target_stem: str) -> str:
    dm = STEM_META[day_stem]
    tg = STEM_META[target_stem]
    cat = relation_category(dm["element"], tg["element"])
    same_polarity = dm["polarity"] == tg["polarity"]
    if cat == "same":
        return "比肩" if same_polarity else "劫财"
    if cat == "output":
        return "食神" if same_polarity else "伤官"
    if cat == "wealth":
        return "偏财" if same_polarity else "正财"
    if cat == "authority":
        return "七杀" if same_polarity else "正官"
    if cat == "resource":
        return "偏印" if same_polarity else "正印"
    raise RuntimeError("无效十神关系")


def round2(x: float) -> float:
    return round(float(x), 2)


def normalize_year_month_day(years: int, months: int, days: int):
    if days >= 30:
        months += days // 30
        days = days % 30
    if months >= 12:
        years += months // 12
        months = months % 12
    return years, months, days


def five_element_status(score: float) -> str:
    if score < 1.0:
        return "偏缺"
    if score < 1.5:
        return "偏弱"
    if score < 2.5:
        return "平衡"
    if score < 3.0:
        return "偏旺"
    return "过旺"


def month_bonus_for(dm_element: str, month_element: str) -> float:
    if month_element == dm_element:
        return 1.5
    if FIVE_ELEMENT_GENERATE[month_element] == dm_element:
        return 1.2
    if FIVE_ELEMENT_GENERATE[dm_element] == month_element:
        return -0.8
    if FIVE_ELEMENT_CONTROL[dm_element] == month_element:
        return -1.0
    if FIVE_ELEMENT_CONTROL[month_element] == dm_element:
        return -1.2
    raise RuntimeError("无法计算月令加权")


def strength_level(ratio: float) -> str:
    if ratio >= 0.68:
        return "强"
    if ratio >= 0.58:
        return "偏强"
    if ratio >= 0.42:
        return "中和"
    if ratio >= 0.32:
        return "偏弱"
    return "弱"


def aggregate_ten_gods(weighted: dict[str,float]) -> dict[str,float]:
    result = {k:0.0 for k in CATEGORY_ORDER}
    for tg, v in weighted.items():
        result[TEN_GOD_CATEGORY_MAP[tg]] += v
    return {k: round2(v) for k,v in result.items()}


def ordered_categories(agg: dict[str,float]) -> list[str]:
    return [k for k,_ in sorted(agg.items(), key=lambda kv: (-kv[1], CATEGORY_ORDER.index(kv[0])))]


def favorable_unfavorable_categories(structure_type: str, structure_subtype: str, level: str):
    if structure_type == "正格":
        if level in {"强","偏强"}:
            fav = ["食伤","财","官杀"]
            unfav = ["比劫","印"]
        elif level in {"弱","偏弱"}:
            fav = ["比劫","印"]
            unfav = ["食伤","财","官杀"]
        else:
            fav = ["财","官杀","印"]
            unfav = []
    else:
        if structure_subtype == "从旺":
            fav = ["比劫","印"]
            unfav = ["食伤","财","官杀"]
        elif structure_subtype in {"从财","从官杀","从儿"}:
            dominant = {"从财":"财","从官杀":"官杀","从儿":"食伤"}[structure_subtype]
            fav = [dominant]
            unfav = ["比劫","印"]
        else:
            fav = []
            unfav = []
    return fav, unfav


def categories_to_elements(dm_element: str, categories: list[str]) -> list[str]:
    mapping = {
        "比劫": dm_element,
        "印": next(k for k,v in FIVE_ELEMENT_GENERATE.items() if v == dm_element),
        "食伤": FIVE_ELEMENT_GENERATE[dm_element],
        "财": FIVE_ELEMENT_CONTROL[dm_element],
        "官杀": next(k for k,v in FIVE_ELEMENT_CONTROL.items() if v == dm_element),
    }
    out = []
    for c in categories:
        elem = mapping.get(c)
        if elem and elem not in out:
            out.append(elem)
    return out


def analyze_bazi(birth_datetime: str, gender: str, dayun_count: int = 8, liunian_start_year: int | None = None, liunian_count: int = 10):
    gender = gender.lower()
    if gender not in {"male","female"}:
        raise ValueError("gender 必须为 male 或 female")
    birth_dt = parse_iso_datetime(birth_datetime)
    tzinfo = birth_dt.tzinfo
    lon = sun_longitude(birth_dt)
    local_year = birth_dt.astimezone(tzinfo).year
    lichun = get_lichun(local_year, tzinfo)
    gz_year = local_year if birth_dt >= lichun else local_year - 1

    year_stem_idx = ((gz_year - 4) % 10) + 1
    year_branch_idx = ((gz_year - 4) % 12) + 1
    year_stem, year_branch = stem_by_index(year_stem_idx), branch_by_index(year_branch_idx)

    month_rule_index, month_rule = determine_month_rule(lon)
    month_order = month_rule["month_order"]
    month_branch = month_rule["branch"]
    yin_month_start_stem_idx = ((2 * year_stem_idx) % 10) + 1
    month_stem_idx = ((yin_month_start_stem_idx + month_order - 2) % 10) + 1
    month_stem = stem_by_index(month_stem_idx)

    local_for_day = birth_dt
    if birth_dt.hour >= 23:
        local_for_day = birth_dt + timedelta(days=1)
    adj_date = local_for_day.date()
    jdn = jdn_from_date(adj_date.year, adj_date.month, adj_date.day)
    day_stem_idx = ((jdn - 1) % 10) + 1
    day_branch_idx = ((jdn + 1) % 12) + 1
    day_stem, day_branch = stem_by_index(day_stem_idx), branch_by_index(day_branch_idx)

    hour_branch_idx = ((birth_dt.hour + 1) % 24) // 2 + 1
    hour_branch = branch_by_index(hour_branch_idx)
    zi_hour_start_stem_idx = (((day_stem_idx - 1) % 5) * 2) + 1
    hour_stem_idx = ((zi_hour_start_stem_idx + hour_branch_idx - 2) % 10) + 1
    hour_stem = stem_by_index(hour_stem_idx)

    four_pillars = {
        "年柱": year_stem + year_branch,
        "月柱": month_stem + month_branch,
        "日柱": day_stem + day_branch,
        "时柱": hour_stem + hour_branch
    }

    hidden_stems = {
        "年支": BRANCH_HIDDEN_STEMS[year_branch],
        "月支": BRANCH_HIDDEN_STEMS[month_branch],
        "日支": BRANCH_HIDDEN_STEMS[day_branch],
        "时支": BRANCH_HIDDEN_STEMS[hour_branch],
    }

    five_scores = {"木":0.0,"火":0.0,"土":0.0,"金":0.0,"水":0.0}
    visible_stems = [year_stem, month_stem, day_stem, hour_stem]
    for s in visible_stems:
        five_scores[STEM_META[s]["element"]] += 1.0
    pillar_branches = [year_branch, month_branch, day_branch, hour_branch]
    for b in pillar_branches:
        hs = BRANCH_HIDDEN_STEMS[b]
        weights = HIDDEN_STEM_WEIGHTS[len(hs)]
        for stem, wt in zip(hs, weights):
            five_scores[STEM_META[stem]["element"]] += wt
    five_scores = {k: round2(v) for k,v in five_scores.items()}
    five_status = {k: five_element_status(v) for k,v in five_scores.items()}

    ten_gods_visible = {
        "年干": ten_god(day_stem, year_stem),
        "月干": ten_god(day_stem, month_stem),
        "时干": ten_god(day_stem, hour_stem)
    }
    ten_gods_hidden = {}
    ten_gods_weighted = {k:0.0 for k in TEN_GOD_ORDER}
    for pos, stem in [("年干", year_stem), ("月干", month_stem), ("时干", hour_stem)]:
        tg = ten_god(day_stem, stem)
        ten_gods_weighted[tg] += 1.0
    for pos_name, branch in [("年支", year_branch), ("月支", month_branch), ("日支", day_branch), ("时支", hour_branch)]:
        hs = BRANCH_HIDDEN_STEMS[branch]
        weights = HIDDEN_STEM_WEIGHTS[len(hs)]
        arr = []
        for stem, wt in zip(hs, weights):
            tg = ten_god(day_stem, stem)
            arr.append({"藏干": stem, "十神": tg, "权重": round2(wt)})
            ten_gods_weighted[tg] += wt
        ten_gods_hidden[pos_name] = arr
    ten_gods_weighted = {k: round2(v) for k,v in ten_gods_weighted.items()}
    agg = aggregate_ten_gods(ten_gods_weighted)

    dm_element = STEM_META[day_stem]["element"]
    resource_element = next(k for k,v in FIVE_ELEMENT_GENERATE.items() if v == dm_element)
    output_element = FIVE_ELEMENT_GENERATE[dm_element]
    wealth_element = FIVE_ELEMENT_CONTROL[dm_element]
    authority_element = next(k for k,v in FIVE_ELEMENT_CONTROL.items() if v == dm_element)

    same_score = five_scores[dm_element]
    resource_score = five_scores[resource_element]
    output_score = five_scores[output_element]
    wealth_score = five_scores[wealth_element]
    authority_score = five_scores[authority_element]
    month_element = BRANCH_PRIMARY_ELEMENT[month_branch]
    month_bonus = month_bonus_for(dm_element, month_element)
    support_total = same_score + resource_score + max(month_bonus, 0)
    drain_total = output_score + wealth_score + authority_score + max(-month_bonus, 0)
    ratio = support_total / (support_total + drain_total) if (support_total + drain_total) else 0.5
    level = strength_level(ratio)
    strength = {
        "same_score": round2(same_score),
        "resource_score": round2(resource_score),
        "output_score": round2(output_score),
        "wealth_score": round2(wealth_score),
        "authority_score": round2(authority_score),
        "month_bonus": round2(month_bonus),
        "support_total": round2(support_total),
        "drain_total": round2(drain_total),
        "strength_ratio": round2(ratio),
        "level": level
    }

    base_total = same_score + resource_score + output_score + wealth_score + authority_score
    support_ratio_base = (same_score + resource_score) / base_total if base_total else 0.5
    support_elements = {dm_element, resource_element}
    visible_support_count = sum(1 for stem in [year_stem, month_stem, hour_stem] if STEM_META[stem]["element"] in support_elements)
    root_support_count = sum(1 for branch in pillar_branches if any(STEM_META[s]["element"] in support_elements for s in BRANCH_HIDDEN_STEMS[branch]))
    structure_type = "正格"
    structure_subtype = "扶抑正格"
    if level == "强" and support_ratio_base >= 0.70 and month_bonus > 0 and (output_score + wealth_score + authority_score) <= 2.0:
        structure_type = "从格"
        structure_subtype = "从旺"
    elif level == "弱" and support_ratio_base <= 0.25 and month_bonus < 0 and visible_support_count == 0 and root_support_count == 0:
        structure_type = "从格"
        dominant = max({"食伤":output_score, "财":wealth_score, "官杀":authority_score}.items(), key=lambda kv: kv[1])[0]
        structure_subtype = {"食伤":"从儿","财":"从财","官杀":"从官杀"}[dominant]
    structure = {
        "type": structure_type,
        "subtype": structure_subtype,
        "support_ratio_base": round2(support_ratio_base),
        "visible_support_count": visible_support_count,
        "root_support_count": root_support_count
    }

    peach_targets = []
    for ref_branch in [year_branch, day_branch]:
        t = PEACH_MAP[ref_branch]
        if t not in peach_targets:
            peach_targets.append(t)
    peach_hits = [pos for pos, b in [("年支",year_branch),("月支",month_branch),("日支",day_branch),("时支",hour_branch)] if b in peach_targets]
    taohua = {
        "has": bool(peach_hits),
        "targets": peach_targets,
        "hit_positions": peach_hits
    }
    tianyi_targets = TIANYI_MAP[day_stem]
    tianyi_hits = [pos for pos, b in [("年支",year_branch),("月支",month_branch),("日支",day_branch),("时支",hour_branch)] if b in tianyi_targets]
    tianyi = {
        "has": bool(tianyi_hits),
        "targets": tianyi_targets,
        "hit_positions": tianyi_hits
    }
    shensha = {"桃花": taohua, "天乙贵人": tianyi}

    # dayun
    year_polarity = STEM_META[year_stem]["polarity"]
    direction = "顺排" if ((year_polarity == "阳" and gender == "male") or (year_polarity == "阴" and gender == "female")) else "逆排"
    prev_jie = prev_jie_before(birth_dt, month_rule_index)
    next_jie = next_jie_after(birth_dt, month_rule_index)
    if direction == "顺排":
        delta_hours = (next_jie["datetime"] - birth_dt).total_seconds() / 3600
        dayun_reference_jie = next_jie
        direction_step = 1
    else:
        delta_hours = (birth_dt - prev_jie["datetime"]).total_seconds() / 3600
        dayun_reference_jie = prev_jie
        direction_step = -1
    start_age_decimal = delta_hours / 72.0
    years = int(delta_hours // 72)
    remain_1 = delta_hours - years * 72
    months = int(remain_1 // 6)
    remain_2 = remain_1 - months * 6
    days = int(round(remain_2 * 5))
    years, months, days = normalize_year_month_day(years, months, days)

    month_pillar_idx = pillar_index(month_stem, month_branch)
    dayun = []
    for i in range(1, dayun_count + 1):
        p = SIxty[(month_pillar_idx + direction_step * i) % 60]
        start_age = round2(start_age_decimal + (i-1)*10)
        end_age = round2(start_age_decimal + i*10)
        dayun.append({
            "序号": i,
            "方向": direction,
            "柱": p,
            "起始年龄": start_age,
            "结束年龄": end_age
        })
    dayun_meta = {
        "方向": direction,
        "参考节气": {
            "名称": dayun_reference_jie["name"],
            "时间": dayun_reference_jie["datetime"].isoformat()
        },
        "起运时差小时": round2(delta_hours),
        "起运年龄": {
            "decimal_years": round2(start_age_decimal),
            "years": years,
            "months": months,
            "days": days
        },
        "列表": dayun
    }

    if liunian_start_year is None:
        liunian_start_year = datetime.now(tzinfo).year
    liunian = []
    for y in range(liunian_start_year, liunian_start_year + liunian_count):
        stem_idx = ((y - 4) % 10) + 1
        branch_idx = ((y - 4) % 12) + 1
        liunian.append({"年份": y, "柱": stem_by_index(stem_idx) + branch_by_index(branch_idx)})

    dominant, secondary = ordered_categories(agg)[:2]
    personality_tags = []
    for tag in PERSONALITY_TAGS[dominant]:
        if tag not in personality_tags:
            personality_tags.append(tag)
    for tag in PERSONALITY_TAGS[secondary][:1]:
        if tag not in personality_tags:
            personality_tags.append(tag)
    if level in {"强","偏强"}:
        extra = ["主动性强","决策偏快"]
    elif level == "中和":
        extra = ["适应性较好"]
    else:
        extra = ["更依赖环境与支持系统"]
    for tag in extra:
        if tag not in personality_tags:
            personality_tags.append(tag)
    personality_summary = f"命局以{dominant}为主、{secondary}为辅，行为风格更偏向{PERSONALITY_TAGS[dominant][0]}与{PERSONALITY_TAGS[dominant][1]}；整体强弱为“{level}”，因此{extra[0]}。"

    if agg["官杀"] + agg["印"] >= 3.0:
        career_axis = ["管理","体制","行政","法务","标准化岗位"]
    elif agg["食伤"] + agg["财"] >= 3.0:
        career_axis = ["市场","销售","产品","内容","经营","创业型岗位"]
    elif agg["印"] + agg["比劫"] >= 3.0:
        career_axis = ["研究","教育","技术","咨询","策划"]
    else:
        career_axis = ["按喜用五行对应行业优先"]
    career_risks = []
    if agg["官杀"] >= 2.5 and level in {"弱","偏弱"}:
        career_risks.append("高压规则环境会放大消耗")
    if agg["食伤"] >= 2.5 and agg["官杀"] < 1.0:
        career_risks.append("规则过密的岗位容易压制发挥")
    if not career_risks:
        career_risks.append("优先选择与喜用神一致的岗位环境")
    career_summary = f"职业主轴偏向{'、'.join(career_axis[:3])}；当前命局更适合在{('输出/经营' if agg['食伤']+agg['财']>=3.0 else '稳定/专业')}路径中建立优势。"

    wealth_total = agg["财"]
    peer_total = agg["比劫"]
    output_total = agg["食伤"]
    if wealth_total >= 2.5 and level in {"强","偏强","中和"}:
        wealth_mode = "主动经营型"
    elif wealth_total >= 2.5 and level in {"弱","偏弱"}:
        wealth_mode = "有财机但承压明显"
    elif wealth_total < 1.2:
        wealth_mode = "财不是核心驱动力"
    else:
        wealth_mode = "稳健积累型"
    wealth_risks = []
    if peer_total - wealth_total >= 1.0:
        wealth_risks.append("合伙/人情/竞争性破财风险高")
    if output_total >= 2.0 and wealth_total >= 1.5:
        wealth_risks.append("适合技能/表达/产品化变现")
    if not wealth_risks:
        wealth_risks.append("以职业能力和节奏管理作为主要抓手")
    wealth_summary = f"财运模式为“{wealth_mode}”，当前更适合{'主动拓展收益来源' if wealth_total >= 2.0 else '先稳住现金流与专业能力'}。"

    relationship_star = "财星" if gender == "male" else "官杀"
    relationship_total = agg["财"] if gender == "male" else agg["官杀"]
    if relationship_total >= 2.0 and taohua["has"]:
        taohua_effect = "缘分机会多，但选择成本高"
    elif relationship_total < 1.0:
        taohua_effect = "婚恋驱动力偏弱或偏晚"
    else:
        taohua_effect = "关系发展更依赖阶段匹配与现实条件"
    marriage_risks = []
    if agg["比劫"] >= 2.0 and level in {"强","偏强"}:
        marriage_risks.append("关系中主导欲较强")
    if agg["印"] >= 2.0 and level in {"弱","偏弱"}:
        marriage_risks.append("安全感需求高，容易慢热或防御")
    if not marriage_risks:
        marriage_risks.append("重视沟通节奏与边界感更有利")
    marriage_summary = f"婚恋核心观察点是{relationship_star}；整体表现为“{taohua_effect}”。"

    fav_cat, unfav_cat = favorable_unfavorable_categories(structure_type, structure_subtype, level)
    fav_elements = categories_to_elements(dm_element, fav_cat)
    unfav_elements = categories_to_elements(dm_element, unfav_cat)

    advice = {
        "职业建议": [
            f"优先选择与喜用类别{('、'.join(fav_cat) if fav_cat else '无')}对应的工作内容",
            f"重点关注{('、'.join(fav_elements) if fav_elements else '环境匹配')}属性的行业、团队与职责",
            "避免长期处在与忌神一致且压力无法转化的环境中"
        ],
        "关系建议": [
            "把稳定沟通、边界协商与现实节奏放在情感判断之前",
            marriage_risks[0],
            "重要关系决策尽量避开高压或高波动阶段"
        ],
        "阶段建议": [
            "先看大运方向，再决定是做扩张、变现还是补基础",
            "弱局先补资源与支持系统，强局先疏导输出与商业化",
            "把五行失衡最明显的部分作为调节重点"
        ]
    }

    chart = {
        "four_pillars": four_pillars,
        "hidden_stems": hidden_stems,
        "day_master": {"天干": day_stem, "五行": dm_element, "阴阳": STEM_META[day_stem]["polarity"]},
        "ten_gods": {
            "visible": ten_gods_visible,
            "hidden": ten_gods_hidden,
            "weighted_score": ten_gods_weighted,
            "aggregated": agg
        },
        "solar_terms": {
            "当前节令": month_rule["name"],
            "当前节令开始": prev_jie["datetime"].isoformat(),
            "下一节令": next_jie["name"],
            "下一节令时间": next_jie["datetime"].isoformat(),
            "当年立春": lichun.isoformat()
        },
        "shensha": shensha,
        "dayun": dayun_meta,
        "liunian": liunian
    }
    analysis = {
        "five_elements_score": five_scores,
        "five_elements_status": five_status,
        "strength": strength,
        "structure": structure,
        "favorable": {
            "categories": fav_cat,
            "elements": fav_elements,
            "unfavorable_categories": unfav_cat,
            "unfavorable_elements": unfav_elements
        },
        "personality": {
            "dominant_star": dominant,
            "secondary_star": secondary,
            "tags": personality_tags,
            "summary": personality_summary
        },
        "career": {
            "career_axis": career_axis,
            "risk_points": career_risks,
            "summary": career_summary
        },
        "wealth": {
            "wealth_mode": wealth_mode,
            "risk_points": wealth_risks,
            "summary": wealth_summary
        },
        "marriage": {
            "relationship_star": relationship_star,
            "taohua_effect": taohua_effect,
            "risk_points": marriage_risks,
            "summary": marriage_summary
        },
        "advice": advice
    }
    template_output = {
        "命盘": {
            "四柱": four_pillars,
            "藏干": hidden_stems,
            "日主": {"天干": day_stem, "五行": dm_element, "阴阳": STEM_META[day_stem]["polarity"]},
            "十神": {
                "天干十神": ten_gods_visible,
                "地支藏干十神": ten_gods_hidden,
                "十神计分": ten_gods_weighted
            },
            "神煞": shensha,
            "大运": dayun_meta,
            "流年": liunian
        },
        "五行分析": {
            "五行得分": five_scores,
            "五行状态": five_status,
            "旺衰": strength,
            "格局": structure,
            "喜忌": {
                "favorable_categories": fav_cat,
                "unfavorable_categories": unfav_cat,
                "favorable_elements": fav_elements,
                "unfavorable_elements": unfav_elements
            }
        },
        "性格分析": analysis["personality"],
        "事业": analysis["career"],
        "财运": analysis["wealth"],
        "婚姻": analysis["marriage"],
        "建议": advice
    }
    return {
        "input": {"birth_datetime": birth_datetime, "gender": gender},
        "chart": chart,
        "analysis": analysis,
        "template_output": template_output
    }



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="八字算命 Skill 参考实现")
    parser.add_argument("--birth-datetime", required=True, help="ISO-8601 datetime with timezone")
    parser.add_argument("--gender", required=True, choices=["male", "female"], help="male 或 female")
    parser.add_argument("--dayun-count", type=int, default=8, help="输出多少步大运，默认 8")
    parser.add_argument("--liunian-start-year", type=int, default=None, help="流年起始年份，默认当前年份")
    parser.add_argument("--liunian-count", type=int, default=10, help="输出多少个流年，默认 10")
    parser.add_argument("--output", type=str, default=None, help="输出文件路径；不填则打印到 stdout")
    parser.add_argument("--compact", action="store_true", help="紧凑 JSON 输出")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    result = analyze_bazi(
        birth_datetime=args.birth_datetime,
        gender=args.gender,
        dayun_count=args.dayun_count,
        liunian_start_year=args.liunian_start_year,
        liunian_count=args.liunian_count
    )
    if args.compact:
        content = json.dumps(result, ensure_ascii=False, separators=(",", ":"))
    else:
        content = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(content)


if __name__ == "__main__":
    main()
