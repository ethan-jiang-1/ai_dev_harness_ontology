---
status: draft
updated: 2026-11-12
---

# 05 生产派：本体从哪来、怎么修

> **2026-11-12 对账（重要）**：本派多数来源已撤回——OntoDoc、ReX-GG、Peeling、Evontree、SFE-O、E-02(Ontology Catch)（见 [黑名单](../../meta/rules/excluded-sources.md)）。**仍 admitted 的只有 CASTON 与 FIRME。** 下文引用撤回源的「已核」数字/结论一律作历史/机制参考，不作活证据，相关判断降为 `推测`。本派方向（来源影响可信度、精化、表示≠执行）作为研究框架保留，但证据基座已被大幅削薄。

## 核心主张

**来源影响可信度，而可信度必须能被下游看见。** `推测`——原 [E-02](../conclusions.md)（已于 2026-11-11 随源撤回，仅作历史参考）曾报告三种来源在漏检/误报上各有偏向，仍未测「可信度如何传给判定器」；按来源加权也没有对照（[generation/F5](./generation/findings.md)）。

本仓库与多数本体文献的一个差别：不假设本体已经存在。本体怎么来的，影响它能被信到什么程度——判定器的可信度继承自本体来源；这条「继承」本身没有测（`推测`）。

第二条：**我们判断精化比新建更常见。** `推测`——没有统计，四篇 digest 也没有测项目分布；文献确实更偏好从零建，这个错位仍是空档，但不能当已核事实。

## 子主题地图

> **计数只写在子主题 dashboard**（`<子主题>/README.md`）与 `findings.md`；本表不抄数字，避免派级与叶级漂移。

| 子主题 | 回答什么 | 状态 | 计数 | 先读 |
|---|---|---|---|---|
| [generation](./generation/README.md) | 本体从哪来：四条生成路线 | `draft`，已拆 F/G | **不在此抄数** → dashboard | dashboard |
| [refinement](./refinement/README.md) | 在既有本体上修子类/约束 | `draft`，已拆 F/G | **不在此抄数** → dashboard | dashboard |
| [representation](./representation/README.md) | 形式化到什么程度 | `seed` | **不在此抄数** → dashboard | 本页 |
| [lifecycle](./lifecycle/README.md) | 来源、精化、对齐、演化 | `seed`，dashboard 薄页 | **不在此抄数** → dashboard | 本页 |
| [modeling](./representation/modeling.md) | 规范如何压缩自由度 | 机制页 | — | 本页 |

> 计数以各子主题 dashboard 为准（2026-11-08）。

**薄页（<2 篇独立来源）**：refinement（1 篇）、representation（1 篇）、lifecycle（1 篇）。薄页只作候选/边界，不承担稳定判断。

## 本派当前判断

- **生成产出候选，不是完备本体。** 四篇都没有验证生成物能被下游判定器/agent 消费：OntoDoc 只测描述四维，ReX-GG 只测用户感知，Peeling 只测 DAG 结构，Evontree 是训练侧注入。`推测`（四篇源均已撤回；「均未测下游」作历史缺口观察）／`推测`（「完备」无操作定义）。详见 [generation/F1、F3](./generation/findings.md)。
- **精化能自动化到小规模，但下游未闭环、覆盖率未报。** CASTON high 6/6 接受（2 位专家）；medium 接受率 default 0/2、pretrained 1/4、GPT-4o mini 1/5——不是「全 mixed」，只有 default 的 2 条是 mixed。GPT-4o mini 那格同时换了 LLM 与 embedding，不能拆成「更大模型」的效应。recall@30 / recall@10 与「下游错误 → 该修哪条公理」都没报。`已核`（数字）／`推测`（瓶颈解释）。详见 [refinement/F1、F2、F3、F5、F6](./refinement/findings.md)。
- **来源差异有测量，「偏向标签」没有。** E-02（已撤回）：专家/LLM 生成/数据挖掘三种来源在漏检与误报上各有偏向、无单一向优（历史示例，不作活证据）。但「专家覆盖窄、LLM 语义漂移、数据挖掘把常见当应然」在生成路线的 digest 里都没有测量，是 `推测`，不作依据（[05-L8](./claims.md)、[generation/F4](./generation/findings.md)）。来源标记进判定权重也没有测（[generation/F5](./generation/findings.md)）。
- **表示的可核结论只有「表达 ≠ 执行」。** SFE-O（已撤回）单域：OWL 2 表达力够，但数值不在 OWL 求解、约束未落成可执行 SHACL、热物性/扩散系数靠外部服务（历史示例，不作活证据）。「按消费位置选档位」「第二档够用」「第三档不划算」都是 `推测`，三档成本差无对照（[representation/README](./representation/README.md)）。
- **生命周期先落「接受记录」，不是更强的生成器。** CASTON / FIRME（admitted）只到候选或身份对齐；Evontree（已撤回）只到自评的训练收益（增益仅报告值、`存疑`）。没有一篇证明本体改动让独立判定器/agent 变好（`已核` 缺口，据 CASTON/FIRME）；八步回路与台账优先是综合判断（[05-L1](./claims.md) 的来源要求、[lifecycle/mechanism](./lifecycle/mechanism.md)）。

## 来源与路线（索引）

| 来源/路线 | 代表 | 可核边界（digest 口径） | 常见偏向——`推测`，未测 |
|---|---|---|---|
| 专家手工 | SFE-O（已移出，历史示例） | 表达力够，瓶颈在执行/集成；数据矛盾显式标记 | 覆盖窄、维护贵、易过时 |
| LLM 生成 | OntoDoc、ReX-GG（均已移出，历史示例） | OntoDoc 无下游、简单图 naive 更好；ReX 本体只当标签表（4 种关系） | 语义漂移、关系方向易错 |
| 数据挖掘 | 无独立 digest 案例 | — | 把「常见」当「应然」 |
| 表征挖掘 | Peeling（已移出，历史示例） | 只在 MRL 嵌入上成立；零样本迁移有深度条件；未测下游 | 只在特定嵌入族上成立 |
| 规则引导自演化 | Evontree（已移出，历史示例） | 15 根概念人工种子；规则只覆盖 subclass/synonym；增益仅报告值（`存疑`） | 需要人工种子、覆盖有限 |
| 精化（不是来源） | CASTON（admitted） | 修既有本体；单一本体/单一公理类型；high 6/6、medium 0–25% | 只覆盖少量高置信修复、候选池有排除规则 |

> 专家手工、LLM、表征挖掘、规则自演化是 generation 的四条路线；「数据挖掘」常被列作第五种，但五条 digest 里没有独立案例，本表不给它编偏向。精化不是来源，是在既有本体上修，单列。最后一列是工程常识或待验假设，不是测量——尤其「覆盖窄/维护贵」「语义漂移」「把常见当应然」在 digest 中无数据（[generation/F4](./generation/findings.md)）。

## 三条工程判断

1. **来源标记要能进判定逻辑，否则不同可信度的约束被平等使用。** `推测`——字段可加，按来源加权是否减少误判没测（[generation/F5](./generation/findings.md)）。
2. **冲突显式化优于静默消解。** SFE-O（已撤回）的做法作历史参考：三处数据矛盾显式标记（前两处确定、第三处 `possible`），不静默修正；「优于」没有对照，`推测`（[representation/F1](./representation/findings.md)）。
3. **表示不是瓶颈，执行才是。** `推测`（原 SFE-O 已撤回，作历史参考）：OWL 2 表达力够，但数值求解、SHACL 执行、外部服务都在 OWL 外；「形式化程度按消费位置选」`推测`，三档成本差未测（[representation/README](./representation/README.md)）。

## 何时用 · 何时别用

**用**：有存量本体需要维护，且下游要追溯「这条约束是谁加的、哪一版」——精化比新建常见是 `推测`；领域术语密集、错误代价高，愿意维护断言台账与来源字段。

**别用**：指望自动生成一个「完备」本体——四篇生成 digest 都没测下游可消费性，生成物只能当候选（`推测`）；没有专家复核或没有下游判定器时，自动接受与自动注入都不划算（explicit 注入掉点是 `已核` 反例，成本判断是 `推测`）。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 本页：派地图 + top claims；不展开机制 |
| [claims.md](./claims.md) | 本派局部结论账本（`05-Lx`） |
| [sources.md](./sources.md) | 本派 digest/card 索引 |
| [frontier.md](./frontier.md) | 本派候选队列 |
| `<子主题>/README.md` | dashboard：覆盖/计数/当前判断/文件地图 |
| `<子主题>/findings.md` | 该子主题的发现与证据 |
| `<子主题>/frontier.md` | 该子主题的 gap/next |
| `<子主题>/mechanism.md` | 机制怎么跑（按需） |

> `representation` 的开放问题在它的 README，候选/检索式汇总在派级 [frontier](./frontier.md)；`lifecycle` 未拆 findings/frontier，判断在 README，机制/实施/工程发现在 [mechanism](./lifecycle/mechanism.md)。

## 持续挖掘

派级前沿、检索式与候选见 [frontier.md](./frontier.md)；子主题的 gap/next 在各自 `frontier.md`。
