---
status: draft
updated: 2026-11-08
---

# 05 生产派：本体从哪来、怎么修

## 核心主张

**来源影响可信度，而可信度必须能被下游看见。** `推测`——[E-02](../conclusions.md) 只测到三种来源在漏检/误报上各有偏向，没有测「可信度如何传给判定器」；按来源加权也没有对照（[generation/F5](./generation/findings.md)）。

本仓库与多数本体文献的一个差别：不假设本体已经存在。本体怎么来的，影响它能被信到什么程度——判定器的可信度继承自本体来源；这条「继承」本身没有测（`推测`）。

第二条：**我们判断精化比新建更常见。** `推测`——没有统计，四篇 digest 也没有测项目分布；文献确实更偏好从零建，这个错位仍是空档，但不能当已核事实。

## 子主题地图

| 子主题 | 回答什么 | 状态 | 已发现 / 未发现 | 先读 |
|---|---|---|---|---|
| [generation](./generation/README.md) | 本体从哪来：四条生成路线 | `draft`，已拆 F/G | 6 F / 6 G | dashboard |
| [refinement](./refinement/README.md) | 在既有本体上修子类/约束 | `draft`，已拆 F/G | 6 F / 4 G | dashboard |
| [representation](./representation/README.md) | 形式化到什么程度 | `seed` | 4 F / 5 G | 本页 |
| [lifecycle](./lifecycle/README.md) | 来源、精化、对齐、演化 | `seed`，dashboard 薄页 | 3 判断 + 4 工程发现 / 3 G | 本页 |
| [modeling](./representation/modeling.md) | 规范如何压缩自由度 | 机制页 | — | 本页 |

> 计数以各子主题 dashboard 为准（2026-11-08）。

## 本派当前判断

- **生成产出候选，不是完备本体。** 四篇都没有验证生成物能被下游判定器/agent 消费：OntoDoc 只测描述四维，ReX-GG 只测用户感知，Peeling 只测 DAG 结构，Evontree 是训练侧注入。`已核`（「四篇均未测下游」是缺口）／`推测`（「完备」无操作定义，类别判断）。详见 [generation/F1、F3](./generation/findings.md)。
- **精化能自动化到小规模，但下游未闭环、覆盖率未报。** CASTON high 6/6 接受（2 位专家）；medium 接受率 default 0/2、pretrained 1/4、GPT-4o mini 1/5——不是「全 mixed」，只有 default 的 2 条是 mixed。GPT-4o mini 那格同时换了 LLM 与 embedding，不能拆成「更大模型」的效应。recall@30 / recall@10 与「下游错误 → 该修哪条公理」都没报。`已核`（数字）／`推测`（瓶颈解释）。详见 [refinement/F1、F2、F3、F5、F6](./refinement/findings.md)。
- **来源差异有测量，「偏向标签」没有。** E-02：专家/LLM 生成/数据挖掘三种来源在漏检与误报上各有偏向、无单一向优（`已核`，限该 checker 实验）。但「专家覆盖窄、LLM 语义漂移、数据挖掘把常见当应然」在生成路线的 digest 里都没有测量，是 `推测`，不作依据（[05-L8](./claims.md)、[generation/F4](./generation/findings.md)）。来源标记进判定权重也没有测（[generation/F5](./generation/findings.md)）。
- **表示的可核结论只有「表达 ≠ 执行」。** SFE-O 单域：OWL 2 表达力够，但数值不在 OWL 求解、约束未落成可执行 SHACL、热物性/扩散系数靠外部服务（`已核`，限该文）。「按消费位置选档位」「第二档够用」「第三档不划算」都是 `推测`，三档成本差无对照（[representation/README](./representation/README.md)）。
- **生命周期先落「接受记录」，不是更强的生成器。** CASTON / FIRME 只到候选或身份对齐；Evontree 只到自评的训练收益（增益仅报告值、`存疑`）。没有一篇证明本体改动让独立判定器/agent 变好（`已核` 缺口）；八步回路与台账优先是综合判断（[05-L1](./claims.md) 的来源要求、[lifecycle/mechanism](./lifecycle/mechanism.md)）。

## 来源与路线（索引）

| 来源/路线 | 代表 | 可核边界（digest 口径） | 常见偏向——`推测`，未测 |
|---|---|---|---|
| 专家手工 | SFE-O | 表达力够，瓶颈在执行/集成；数据矛盾显式标记 | 覆盖窄、维护贵、易过时 |
| LLM 生成 | OntoDoc、ReX-GG | OntoDoc 无下游、简单图 naive 更好；ReX 本体只当标签表（4 种关系） | 语义漂移、关系方向易错 |
| 数据挖掘 | 无独立 digest 案例 | — | 把「常见」当「应然」 |
| 表征挖掘 | Peeling | 只在 MRL 嵌入上成立；零样本迁移有深度条件；未测下游 | 只在特定嵌入族上成立 |
| 规则引导自演化 | Evontree | 15 根概念人工种子；规则只覆盖 subclass/synonym；增益仅报告值（`存疑`） | 需要人工种子、覆盖有限 |
| 精化（不是来源） | CASTON | 修既有本体；单一本体/单一公理类型；high 6/6、medium 0–25% | 只覆盖少量高置信修复、候选池有排除规则 |

> 专家手工、LLM、表征挖掘、规则自演化是 generation 的四条路线；「数据挖掘」常被列作第五种，但五条 digest 里没有独立案例，本表不给它编偏向。精化不是来源，是在既有本体上修，单列。最后一列是工程常识或待验假设，不是测量——尤其「覆盖窄/维护贵」「语义漂移」「把常见当应然」在 digest 中无数据（[generation/F4](./generation/findings.md)）。

## 三条工程判断

1. **来源标记要能进判定逻辑，否则不同可信度的约束被平等使用。** `推测`——字段可加，按来源加权是否减少误判没测（[generation/F5](./generation/findings.md)）。
2. **冲突显式化优于静默消解。** SFE-O 的做法可核：三处数据矛盾显式标记（前两处确定、第三处 `possible`），不静默修正（`已核`，限 [representation/F1](./representation/findings.md)）；「优于」没有对照，`推测`。
3. **表示不是瓶颈，执行才是。** `已核`（限 SFE-O）：OWL 2 表达力够，但数值求解、SHACL 执行、外部服务都在 OWL 外；「形式化程度按消费位置选」`推测`，三档成本差未测（[representation/README](./representation/README.md)）。

## 何时用 · 何时别用

**用**：有存量本体需要维护，且下游要追溯「这条约束是谁加的、哪一版」——精化比新建常见是 `推测`；领域术语密集、错误代价高，愿意维护断言台账与来源字段。

**别用**：指望自动生成一个「完备」本体——四篇生成 digest 都没测下游可消费性，生成物只能当候选（`推测`）；没有专家复核或没有下游判定器时，自动接受与自动注入都不划算（explicit 注入掉点是 `已核` 反例，成本判断是 `推测`）。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 本页：派地图 + top claims；不展开机制 |
| `claims.md` | 本派局部结论账本（`05-Lx`） |
| `sources.md` | 本派 digest/card 索引 |
| `frontier.md` | 本派候选队列 |
| `<子主题>/README.md` | dashboard：覆盖/计数/当前判断/文件地图 |
| `<子主题>/findings.md` | 该子主题的发现与证据 |
| `<子主题>/frontier.md` | 该子主题的 gap/next |
| `<子主题>/mechanism.md` | 机制怎么跑（按需） |

> `representation` 的开放问题在它的 README，候选/检索式汇总在派级 [frontier](./frontier.md)；`lifecycle` 未拆 findings/frontier，判断在 README，机制/实施/工程发现在 [mechanism](./lifecycle/mechanism.md)。

## 持续挖掘

派级前沿、检索式与候选见 [frontier.md](./frontier.md)；子主题的 gap/next 在各自 `frontier.md`。
