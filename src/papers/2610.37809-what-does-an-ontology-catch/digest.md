---
status: draft
updated: 2026-11-07
quality: A
based_on: card.md
claims: [E-02]
---

# What Does an Ontology Catch? · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**如果你要把本体接成 checker，按这个顺序：**

1. **先建空结果重试基线。** 查询返回空就重试；它在人工故障上 catch 79.2%、false alarm 0%。**任何 ontology check 必须先超过这个基线**，否则只是多一次重试。
2. **先做 data-derived summary，再决定要不要 curated。** 从数据总结类/属性/模式（≥5 次），成本 <$1；用它审计 curated 本体：**缺声明是 false alarm 的主要来源**。
3. **按错误类型选 checker。** 类型/声明/模式错误 → data-derived 或 declaration check；语义错误（查询对但问错问题）→ 本体检查基本抓不到，需要别的信号（LLM judge、执行结果、用户确认）。
4. **同时量 catch 与 false alarm。** 只看 accuracy 会把「多抓了错、也多杀了对」混在一起；precision 才是 agent 开发者能感知的指标。
5. **不要盲目组合来源。** curated + data-derived 组合 catch 更多，但 false alarm 也更多；C4 没有净收益。
6. **不要让同一个本体既做 context 又做 checker。** 论文的探索性结果显示：同源 context+check 的 catch 更少（self-confirmation）。判定器应与被判定对象不同源。
7. **反馈消息要验证。** specific message 修复 28.3% 的 flagged wrong，但也 corrupt 1.0% 的 flagged correct；generic 修复 20.2%、corrupt 0.2%。没有验证前，generic 更安全。
8. **把 false alarm 当预算。** Google 的静态分析要求 effective FP <10%；你的 agent 能承受多少？超过预算，用户会学会忽略 flag。
9. **记录成本。** curated check 每答案 65,976 tokens / 46 s；data-derived 28,076 / 17 s；重试次数与 false alarm 直接相关。
10. **发布本体时附带 data summary。** curated 本体要与自己的数据对账；缺声明/矛盾 axiom 会在部署时变成 false alarm 工厂。

## 实用意义

它解决的操作问题：

- **「agent 的 SPARQL 语法对、执行也成功，但答错了。」** → 用本体检查类型/声明/模式；但要先知道它抓不到语义错。
- **「上了 curated 本体，结果 agent 把正确答案改错了。」** → false alarm 16.8%，precision 只比随机高 1.6 点；先量再上。
- **「专家本体很贵，值不值？」** → 作为 checker，curated 不如 data-derived 的 precision；作为 context，data-derived 也略好（C1a）。
- **「数据里用了本体没声明的属性。」** → 每个缺失声明都会误报每一条用到它的正确答案；用 data summary 审计。
- **「多个 checker 组合会不会更好？」** → 不一定；组合增加 false alarm，C4 没有净收益。
- **「LLM 写的本体能不能用？」** → 不稳定：draw 3 catch 43.4% 但 false alarm 24.3%；masked 版 precision 93.7% 但 catch 5.0%。

**何时用**：知识图谱有可执行 schema；任务主要是类型/声明/模式错误；有正确答案或能人工标注；false alarm 预算明确。

**何时别用**：语义错误为主；没有正确答案、无法估 precision；curated 本体与数据不一致且没人维护；agent 的查询大量使用 UNION/subquery（checker 返回 unknown）；false alarm 会直接损害用户信任。

## 质量评估

- **证据类型**：实证·基准（`已核`，一手正文；UniProt confirmatory）。
- **样本与对照**：4,410 条真实答案（3,383 可检查）；9,753 个人工 fault + 3,630 control；7 个模型；5 个图；三种来源 × 三种用法；预注册 C1–C5。
- **优点**：把 checker 本身当对象；catch/FA 分开；真实答案 + 人工故障双轨；同一 compiler；成本表；代码/数据公开。
- **主要威胁**：只有 UniProt confirmatory；人工故障可能不代表真实错误；真实错误稀疏；private 图只报率；curated setup 成本未测；部分注册分析未跑。
- **`quality: A` 理由**：预注册 + 多模型 + 多图 + 真实/人工双轨 + 成本 + 可复现，强于多数本体评测；但外部效度仍受「知道正确答案」限制。

## 洞察

1. **curated 本体不是可靠判定器。** 真实答案上 catch 18.9%、false alarm 16.8%、precision 57.1%；相对随机 flag 只高 1.6 点（CI 跨零）。**「正式 schema」不等于「可靠 judge」。** `已核`
2. **data-derived 是更好的 precision/recall 折中，但只能抓结构错。** catch 8.2%、FA 3.5%、precision 72.3%；它抓不到「类型都对、语义错」的查询。`已核`
3. **空结果重试被低估。** 人工故障上 catch 79.2%、FA 0%；在真实答案上 catch 2.5%、FA 0.1%。**先问「执行结果是否已经暴露了这个错」，再问「要不要加 checker」。** `已核`
4. **LLM 生成本体不稳定。** 同一 recipe 的三个 draw：catch 6.7/8.6/43.4，FA 3.2/6.6/24.3；masked 版 precision 93.7% 但 catch 5.0%。**不要让「LLM 能写本体」变成「LLM 写的本体能当 judge」。** `已核`
5. **组合不等于更好。** curated + data-derived 的 catch 19.5%、FA 17.8%；比 curated 单用只多 0.6 点 catch，却多 1.0 点 FA；C4 无净收益。`已核`
6. **同源 context + checker 会降低 catch。** 用 curated 本体做 context 时，curated check 抓到的错更少；data-derived 也有同样方向。**判定器应与被判定对象不同源。** `已核`（探索性）
7. **specific feedback 是双刃剑。** 修复 28.3% vs generic 20.2%，但 corrupt 1.0% vs 0.2%。没有验证前，specific 不一定更好。`已核`
8. **本体检查的真实成本在 false alarm 与重试。** curated 每答案 65,976 tokens / 46 s，data-derived 28,076 / 17 s；false alarm 直接变成重试与信任损失。`已核`

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| curated 本体 | 发布方一次性（本文未测） | 可能缺声明/与数据矛盾；维护成本高 |
| data-derived summary | 一次性，<$1 | 从数据总结类/属性/模式；可自动生成 |
| LLM-generated 本体 | 一次性，<$1/个 | 不稳定；需多个 draw + 评估 |
| check | 每次答案 | curated 66k tokens / 46 s；data 28k / 17 s |
| 重试 | 每次 flag | 直接由 false alarm 触发；成本随 FA 上升 |
| 人工标注 | 评估期 | 需要正确答案/抽样标注；部署时通常没有 |

**使能条件**：可执行 schema（OWL/SHACL/SPARQL）、能读数据生成 summary、有 SPARQL endpoint、能拿到正确答案或抽样标注。

**2022 年做会卡在哪**：LLM 生成 SPARQL 不稳；没有 7 个模型/多图对照；data-derived summary 的自动化不成熟；agent 的查询分布与现在不同。

**反向条件**：语义错误为主；没有正确答案；false alarm 预算极低；curated 本体与数据不一致；查询大量使用 UNION/subquery。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **E-02** | **支撑并细化**：三种来源在漏检/误报上各有偏向；curated 精确度仅略优于随机；**新增 data-derived 的 precision 72.3 vs curated 57.1，以及空结果重试基线**。 |
| **P3** | **强支撑**：不存在单一向优的本体来源；curated 高 catch/高 FA，data-derived 低 FA/低 catch，LLM 不稳定。 |
| **02-L?** | 见 [02 claims](../../../topics/02-judgment/claims.md)：新增「本体 checker 必须先超过空结果重试基线」。 |
| **C-03** | 又一例：用 accuracy 量 checker 会把 catch 与 FA 混在一起；必须分开报。 |
| [checker](../../../topics/02-judgment/checker/README.md) | 核心文献；机制细节回 card。 |

## 不可迁移

- UniProt 是 confirmatory；其他图 exploratory；private 图只报率。
- 人工故障可能不代表真实错误；真实 agent 错误稀疏且分布不均。
- 7 个模型的结果不能外推到其他模型/版本。
- 本文知道每题正确答案；真实部署没有这个条件。
- 检查器不支持 UNION/subquery，返回 unknown；覆盖率受查询形态影响。

## 开放问题

- 真实 agent 错误上的 catch 能不能提高到 >30%，而不把 FA 推到 >10%？
- 语义错误（类型都对、问错问题）用什么 checker？LLM judge 的 precision 更高（+15.8），但成本/稳定性如何？
- 空结果重试 + ontology check 的组合净收益是多少？本文没给组合相对空结果基线的增益。
- false alarm 的信任成本怎么量？Google 的 10% 预算是静态分析的，agent 场景是否适用？
- curated 本体维护成本与 data-derived 自动生成的长期对比；发布方是否应该附带 data summary？
- 同源 context+checker 的 catch 下降是确认偏差还是信息冗余？能否用独立 checker 避免？
