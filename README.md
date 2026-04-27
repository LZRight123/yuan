# Yuan

🌐 **English** · [中文](./README-CN.md)

`Yuan` is a unified destiny-reading skill for Codex, Claude Code, and any Agent Skills–compatible runtime.

Its purpose is not to stack multiple metaphysical systems on top of each other, but to collapse birth information into a **single input surface**, then render a **production-grade reading** out of whatever methods are actually defensible in the current environment.

---

## Positioning

`Yuan` cares about three things:

- **Unified input** — one set of birth data, no per-system improvisation
- **Unified delivery** — final results only; no method tour, no divergence analysis, no intermediate scaffolding
- **Unified boundary** — run what can be run, mark what cannot, never fabricate facts

In other words, `Yuan` is not a "metaphysics router" — it is a **destiny-reading renderer**.

---

## Design Principles

- **Single input surface**
  Birth datetime, birthplace, calendar type, gender, and focus topics are first reduced to one canonical input package, then derived into each reference system.
- **Final-result delivery**
  Default output is `Input Confirmation / Bone-Weight Verse / Verdict / Career / Wealth / Relationships / Five-Year Forecast / Advice`. The working process is never exposed to the end user.
- **Runnable-first**
  Prefer methods that genuinely hold up in the current environment. Anything `partial` or `blocked` is declared as a limit, not faked.
- **Zero-dependency by default**
  Input validation, result rendering, and structural constraints work without extra installs. Optional toolchains exist only for precise charting.
- **Deterministic facts, heuristic reading**
  Calculation and interpretation are strictly layered. Traditional heuristics are allowed, but never packaged as scientific proof.

---

## Capability Surface

`Yuan` orchestrates six reference systems under one umbrella skill:

| Method | Reference |
| --- | --- |
| BaZi (Four Pillars) | `references/bazi/` |
| Cheng Gu (bone-weight) | `references/chenggu/` |
| Numerology | `references/numerology/` |
| Western Astrology | `references/western-astrology/` |
| Vedic Astrology | `references/vedic-astrology/` |
| Zi Wei Dou Shu | `references/ziwei/` |

Final delivery focuses on three rendering modes:

1. `Conservative` — restrained tone, preserves boundary awareness
2. `Direct` — verdicts, judgments, and a five-year window without intermediate analysis
3. `Five-year window` — anchored at the current year, two years back and two forward

---

## Output Contract

Final delivery is always organized in this order:

1. `Input Confirmation`
2. `Bone-Weight Verse`
3. `Verdict`
4. `Career`
5. `Wealth`
6. `Relationships`
7. `Five-Year Forecast`
8. `Advice`

The following sections **never appear** in final output by default:

- Method overview
- Cross-method consensus
- Divergence and confidence
- Working-process narration
- "What methods I used" explanations

---

## Boundaries

`Yuan`'s boundaries are explicit:

- Does not present metaphysics as scientific fact
- Does not fabricate stars, palaces, Nakshatras, or Dashas when reliable charting is unavailable
- Does not leak intermediate scaffolding as final output
- Does not require dependency installs for basic interaction

When precise charting is needed, the scripts and dependencies under `references/` can be enabled. When not, the skill still completes input validation, structural control, and defensible rendering on its own.

---

## Repository Layout

```text
yuan/
├── SKILL.md
├── README.md
├── README-CN.md
├── AGENTS.md
├── agents/
│   └── openai.yaml
└── references/
    ├── bazi/
    ├── chenggu/
    ├── numerology/
    ├── western-astrology/
    ├── vedic-astrology/
    └── ziwei/
```

---

## Installation

### Codex

Project-level:

```bash
.agents/skills/yuan/
```

User-level:

```bash
$HOME/.agents/skills/yuan/
```

### Claude Code

Project-level:

```bash
.claude/skills/yuan/
```

User-level:

```bash
~/.claude/skills/yuan/
```

---

## Invocation

Explicit call:

```text
Use the yuan skill to produce a direct final reading with bone-weight verse,
verdict, career, wealth, relationship, and a five-year window.
```

Natural language call:

```text
Run yuan and give me the final reading directly, no intermediate steps.
Name: Zhang San
Gender: Male
Solar: 1992-08-14 21:30
Lunar: 1992 / 7th month / 16th, hour of Hai
Birthplace: Wuhan, Hubei
```

---

## Recommended Evolution

Three highest-leverage improvements going forward:

- Add a peer-level `SKILL.md` for BaZi so all six reference entries are isomorphic
- Document explicit runtime parameters for `style_mode / assertiveness / year_window`
- Provide clearer fallback templates for `blocked` systems so final delivery stays stable

The value of `Yuan` is not how many metaphysical names it covers, but how much its output **feels like a finished product**.
