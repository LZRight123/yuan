# Vedic Reference

## 默认前提
- 这是一个**传统吠陀占星**技能，不做科学证明。
- 若必须自行计算星盘，默认使用**恒星黄道（sidereal zodiac）**。
- 若用户未指定 ayanamsa，而又确需外部计算，优先按 **Lahiri** 理解。
- 月亮星宿（Janma Nakshatra）是主轴。

## Nakshatra 计算提示
- 27 个 Nakshatra 平分黄道。
- 每个 Nakshatra 跨度 = **13°20'** = **13.333333°**
- 每个 Pada 跨度 = **3°20'** = **3.333333°**
- 先把月亮换算成 **0°–360° 的恒星黄道绝对经度**
- 公式：
  - `nakshatra_index = floor(longitude / 13.333333)`
  - `longitude_within_nakshatra = longitude % 13.333333`
  - `pada = floor(longitude_within_nakshatra / 3.333333) + 1`
  - `fraction_remaining = 1 - (longitude_within_nakshatra / 13.333333)`

## 27 Nakshatra 顺序、守护星与关键词
1. **Ashwini** — Ketu — 启动、速度、疗愈、先行
2. **Bharani** — Venus — 容纳、欲望、负担、转化
3. **Krittika** — Sun — 切割、净化、辨别、锐利
4. **Rohini** — Moon — 滋养、吸引、生长、丰饶
5. **Mrigashira** — Mars — 探索、追寻、试探、好奇
6. **Ardra** — Rahu — 风暴、破局、强烈体验、重组
7. **Punarvasu** — Jupiter — 回归、修复、再生、重启
8. **Pushya** — Saturn — 养成、责任、秩序、供养
9. **Ashlesha** — Mercury — 缠绕、洞察、策略、控制
10. **Magha** — Ketu — 祖系、权威、尊位、传承
11. **Purva Phalguni** — Venus — 享受、创造、关系、放松
12. **Uttara Phalguni** — Sun — 契约、责任、维系、承诺
13. **Hasta** — Moon — 技巧、掌控、手艺、组织
14. **Chitra** — Mars — 设计、魅力、修饰、建构
15. **Swati** — Rahu — 独立、流动、贸易、分散
16. **Vishakha** — Jupiter — 目标、执着、分岔、成就
17. **Anuradha** — Saturn — 忠诚、友谊、协作、纪律
18. **Jyeshtha** — Mercury — 资历、保护、竞争、承压
19. **Mula** — Ketu — 追根究底、拆解、剥离、根因
20. **Purva Ashadha** — Venus — 宣示、扩张、魅力、信念
21. **Uttara Ashadha** — Sun — 定局、责任、长期胜利、名誉
22. **Shravana** — Moon — 学习、倾听、传播、路径
23. **Dhanishta** — Mars — 节奏、资源、团队、行动
24. **Shatabhisha** — Rahu — 隔离、修复、系统、边界
25. **Purva Bhadrapada** — Jupiter — 极端、誓愿、理想、两极
26. **Uttara Bhadrapada** — Saturn — 深度、稳定、承受、收束
27. **Revati** — Mercury — 引导、过渡、保护、完成

## Vimshottari Dasha 年数
- Ketu — 7
- Venus — 20
- Sun — 6
- Moon — 10
- Mars — 7
- Rahu — 18
- Jupiter — 16
- Saturn — 19
- Mercury — 17

总计 = **120 年**

## Vimshottari Dasha 计算提示
### 1) 出生起始 Mahadasha
- 起始 Mahadasha 主星 = 月亮出生 Nakshatra 的守护星

### 2) 出生余额
- `birth_balance = fraction_remaining × mahadasha_years`
- `fraction_remaining` 来自“月亮在出生 Nakshatra 内还剩多少弧度”

### 3) Mahadasha 顺序
- Ketu → Venus → Sun → Moon → Mars → Rahu → Jupiter → Saturn → Mercury →（循环）

### 4) Antardasha 顺序
- 从当前 Mahadasha 主星开始，按同样顺序轮转

### 5) Antardasha 时长
- `antardasha_duration = mahadasha_duration × sublord_years / 120`

## 解读原则
- 月亮星宿决定情绪底色、习惯反应、业力牵引、内在需求。
- 守护星决定驱动力、课题方向与阶段风格。
- Pada 细化表达方式，但在数据不完整时，不要假装精确。
- 土星更常用于“责任、压力、延迟、成熟”；木星更常用于“意义、保护、扩展”；罗喉/计都更常用于“放大、执念、抽离、旧业”。

## 诚实边界
- 如果用户只给了公历生日，没有出生时间，也没有已计算星盘，就**不能**可靠推出精确的月亮星宿与大运余额。
- 如果用户给的是**热带黄道**而不是恒星黄道，不要直接当作吠陀结果使用；应先说明需要转换或要求用户提供 sidereal 数据。
- 不要把占星解释写成不可更改的命运判决。
