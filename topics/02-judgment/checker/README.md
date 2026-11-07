---
status: draft
updated: 2026-11-07
rq: [RQ4, RQ5]
evidence: [E-02]
---

# 时刻 3 · 输出后

## 位置

产出已经形成、尚未被使用。判定器在此检查一致性，决定放行、退回或标注。

## 本体作为语义判据

三种判定形态（格式 / 语义 / 行为）的机制定义见 [00-harness/verification.md](../../00-harness/verification.md#三种判定器)。本派只关注中间那行：本体是唯一既外部、又能覆盖语义的判据；格式检查管不到语义，测试管不到语义，人工复核无法规模化。

## 核心结论：判定器本身是研究对象

不是问「本体有没有用」，而是问**「用哪种本体当判定器，代价是什么」**。What Does an Ontology Catch? 在 UniProt（confirmatory）和其他四个图上，用 7 个模型、4,410 条真实答案、9,753 个人工 fault 测了三种来源：

| 本体来源 | 真实答案 catch / FA / precision | 优势 | 系统性偏向 |
|---|---|---|---|
| 专家手工 curated | **18.9% / 16.8% / 57.1%** | 覆盖语义、可审计、能抓类型冲突 | 缺声明/与数据矛盾 → **误报高**；precision 仅比随机高 1.6 点 |
| 数据派生 data-derived | **8.2% / 3.5% / 72.3%** | 贴合数据、便宜（<$1）、FA 低 | catch 低；把「常见」当「应然」；抓不到语义错 |
| LLM 生成 | masked：5.0% / 1.8% / 93.7% | 启动快、可加 disjointness | **不稳定**：同 recipe 三个 draw 的 catch 6.7–43.4%，FA 3.2–24.3% |

**先超过空结果重试基线。** 查询返回空就重试：人工 fault 上 catch 79.2%、FA 0%；真实答案上 catch 2.5%、FA 0.1%。**ontology check 只有抓到这个基线抓不到的错，才有价值。**

关键发现（一手正文，[card](../../../src/papers/2610.37809-what-does-an-ontology-catch/card.md) / [digest](../../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) → [E-02](../../conclusions.md)）：

- 三种来源在**漏检与误报**之间有不同权衡，无单一向优者。
- curated 本体在真实答案上的 precision 只略优于随机（+1.6 点，CI −2.3~+6.3）。
- 一个按发布状态使用的 curated schema，可能**与它自己的数据矛盾**；14.3% 的 Linked Data triples 使用未声明属性（引文），每个缺失声明都会误报每一条用到它的正确答案。
- 组合 curated + data-derived 没有净收益（C4）：catch 19.5%、FA 17.8%，比 curated 单用只多 0.6 点 catch，却多 1.0 点 FA。
- specific feedback 修复 28.3% 的 flagged wrong，但 corrupt 1.0% 的 flagged correct；generic 是 20.2% / 0.2%。

> 这几条合起来，基本否定了「挂个本体就变准」的朴素假设。判定器的价值必须按漏检/误报曲线来算，而不是按「用没用本体」来算。

## 一条可执行的判定流程

1. **先建空结果重试基线。** 不加本体，先看执行结果本身能暴露多少错。
2. **做 data-derived summary 审计 curated 本体。** 缺声明、矛盾 axiom 是最便宜的 false alarm 来源。
3. **按错误类型选 checker。** 类型/声明/模式错 → data-derived / declaration check；语义错 → 本体检查抓不到，换 LLM judge 或人工。
4. **同时报 catch 与 FA。** 只看 accuracy 会把「多抓错、多杀对」混在一起。
5. **不要同源。** 同一个本体既做 context 又做 checker，catch 反而下降（探索性）；判定器应与被判定对象不同源。
6. **不要盲目组合。** 组合往往增加 FA 而不增加净收益。
7. **把 FA 当预算。** Google 的静态分析要求 effective FP <10%；agent 场景要自己定。

## 为什么判定器必须与被判对象不同源

同一上下文内的自我审核几乎总是失效——不是不诚实，而是它已经形成倾向，复核时沿同一路径重走一遍。What Does an Ontology Catch? 给了一个探索性证据：用 curated 本体做 context 时，curated check 抓到的错更少；data-derived 也有同样方向。有效验证需要独立上下文或外部判据。

## 成本

| Check | 每答案 token（median） | 时间（median） | 备注 |
|---|---|---|---|
| curated | 65,976 | 46.0 s | false alarm 多 → 重试多 |
| data-derived | 28,076 | 17 s | FA 少；生成 <$1 |
| 空结果重试 | 低 | 低 | FA≈0；catch 在真实答案上仅 2.5% |

## 失效模式

- **误报导致「修坏」。** 判定器错误地标记了正确输出，agent 遂去「修复」它，把对的改成错的。curated 的 16.8% FA 是直接证据；specific feedback 的 1.0% corrupt 是机制。
- **漏检结构化错误。** 结构性检查查不出语义错误（关系方向反了、边界划错），而这类错误最危险，因为通过了所有形式检查。
- **判定器自身不可解释。** 判定为错但说不清哪条约束被违反，模型无法学习，只会换姿势重试。
- **串联时早期误报放大。** 多级判定中，前一级的误报会引发下游大量无效工作。
- **把 curated 当权威。** 发布状态的本体可能缺声明/与数据矛盾；不审计就上线，FA 会系统性偏高。
- **用 accuracy 评估 checker。** catch 与 FA 混在一起，会得出「有用/没用」的错结论。
- **同源 context + checker。** 确认偏差会降低 catch；不要让同一份 artifact 既喂又判。

## 开放问题

- 真实 agent 错误上的 catch 能否 >30%，同时 FA <10%？
- 语义错误（类型都对、问错问题）用什么 checker？LLM judge precision +15.8，但成本/稳定性如何？
- 空结果重试 + ontology check 的组合净收益是多少？本文没给组合相对空结果基线的增益。
- false alarm 的信任成本怎么量？Google 的 10% 预算是否适用于 agent？
- 能否离线测量判定器曲线？需要标注集，而标注集从哪来。
- 只想标「可疑」不想阻断时，如何避免 agent 过度修正？是否需要「仅标注、不驱动修改」模式。
- 漏检链接：判定器可信度是否应继承本体来源的可信度（见 [lifecycle](../../05-produce/lifecycle/README.md)）。
