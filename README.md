# Yuan

`Yuan` 是一个面向 Codex、Claude Code 与兼容 Agent Skills 运行时的综合命理 skill。

它的目标不是把多套术数机械堆在一起，而是把出生信息统一成一个输入面，再把可运行、可辩护、可交付的结果渲染成一份成品级命理阅读。

## Positioning

`Yuan` 关注的是三件事：

- 统一输入：同一份出生资料，不为不同体系临时改口径
- 统一交付：最终只交付结果，不交付方法速览、分歧分析、过程性中间件
- 统一边界：能算的就算，不能可靠排盘的部分直接标注限制，不编造事实

换句话说，`Yuan` 不是一个“玄学路由器”，而是一个“命理成品渲染器”。

## Design Principles

- **Single input surface**
  出生时间、地点、历法、性别与关注主题先收敛为统一输入包，再派生到各参考体系。
- **Final-result delivery**
  默认输出 `资料确认 / 称骨歌诀 / 结论 / 事业 / 财运 / 感情 / 五年断事 / 建议`，不把工作过程暴露给最终用户。
- **Runnable-first**
  优先运行当前环境下真正能站得住的方法；对 `partial` 或 `blocked` 的体系，明确限制，不假装有盘。
- **Zero-dependency by default**
  输入判断、结果渲染、结构约束默认不要求依赖安装；只有精确排盘才使用可选工具链。
- **Deterministic facts, heuristic reading**
  确定性计算与经验性解读严格分层；传统经验可以用，但不包装成科学证明。

## Capability Surface

`Yuan` 以一个总 skill 组织多个参考体系：

- 八字
- 称骨
- 数字命理
- 西方占星
- 吠陀占星
- 紫微斗数

并把最终交付聚焦为三个层级：

1. `Conservative`
   口径更克制，适合需要保留边界感的输出。
2. `Direct`
   直接给断语、结论与五年窗口，不展示中间分析。
3. `Five-year window`
   以前两年、当年、后两年为默认窗口，给出阶段性断事。

## Output Contract

最终交付默认按以下顺序组织：

1. `资料确认`
2. `称骨歌诀`
3. `结论`
4. `事业`
5. `财运`
6. `感情`
7. `五年断事`
8. `建议`

以下栏目默认不出现在最终结果里：

- 方法速览
- 共同结论
- 分歧与置信度
- 工作过程说明
- “我用了什么方法”的解释

## Boundaries

`Yuan` 的边界很明确：

- 不把术数说成科学定论
- 不在缺少可靠排盘事实时虚构星曜、宫位、Nakshatra 或 Dasha
- 不把中间件结构当作最终产品输出
- 不强迫安装依赖才能完成基础交互

需要精确排盘时，可以启用参考目录里的脚本与依赖；不需要时，skill 仍可完成输入判断、成品结构控制与可辩护结果渲染。

## Repository Layout

```text
yuan/
├── SKILL.md
├── README.md
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

## Installation

### Codex

项目级：

```bash
.agents/skills/yuan/
```

用户级：

```bash
$HOME/.agents/skills/yuan/
```

### Claude Code

项目级：

```bash
.claude/skills/yuan/
```

用户级：

```bash
~/.claude/skills/yuan/
```

## Invocation

显式调用：

```text
Use the yuan skill to produce a direct final reading with bone-weight verse, verdict, career, wealth, relationship, and a five-year window.
```

自然语言调用：

```text
用 yuan skill 算一下，直接给最终结果，不要中间过程。
姓名：张三
性别：男
公历：1992年8月14日21时30分
农历：1992年七月十六亥时
出生地：湖北省武汉市
```

## Recommended Evolution

如果后续继续打磨，这个 skill 最值得增强的方向有三个：

- 为八字补齐同级 `SKILL.md`，让六个参考体系入口完全同构
- 给 `Yuan` 增加显式的 `style_mode / assertiveness / year_window` 运行时参数说明
- 为 `blocked` 体系增加更清晰的降级策略模板，使最终交付更稳定

`Yuan` 的价值，不在“覆盖了多少术数名词”，而在“把结果交付得像一个成熟产品”。
