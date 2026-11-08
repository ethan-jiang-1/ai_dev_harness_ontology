---
status: draft
updated: 2026-11-08
quality: B
based_on: card.md
claims: [E-05]
---

# FIRME：跨源、跨期的记忆，先解决「谁是谁」

> 这篇消化不假设你读过论文。先讲清「身份 registry + 记忆图」是什么，再看它在一个真实投资人数据上的增益、代价与边界。

## 0. 三句话

1. **它问什么**：同一投资人/产品/主题在不同来源、不同时期以不同名字出现；不锚定身份，关系历史会碎成多个 partial history，证据无法累积，provenance 丢失。
2. **它怎么做**：registry 保存 canonical 身份 + learned aliases；短期用产品-主题本体做证据融合；长期用确定性强化/衰减与五态生命周期维护关系历史。
3. **它发现什么**：alias memory 让 final-period CMR 提升 7.8–12.1 pp（4 个 dataset–backend 设置），human audit 的 reattachment recall 提升 22.5–29.0 pp；semantic matching token 降 40.3%。但专有数据、10 个月度 period（S&P 3 个 reporting period）、false merge **可能**长期污染。

## 1. 它解决什么问题

### 1.1 背景

个人/投资人记忆不是「存一堆事实」，而是「同一段关系的历史」。例如：

- 1 月：通话里提到「关心市场波动」；
- 3 月：又提到「市场波动」；
- 6 月：没提；8 月：又提。

如果每次都用不同 surface form 建一条新边，这段历史会被劈成多条 partial history；证据无法累积，agent 每次只能看到碎片。

### 1.2 论文的立场

**身份先于内容。** 先把 incoming observation 对到持久关系身份，再谈强化/衰减。registry 是记忆的前置，不是附属。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **entity resolution（ER）** | 判断两个 mention 是不是同一个实体。 |
| **registry** | 持久身份表：canonical ID + aliases。 |
| **alias memory** | 记住**实体侧**的历史 surface forms，下次直接匹配；关系没有 alias。alias 不是 LLM2Graph 的抽取产物，而是 registry 匹配后把 target surface form 加到 anchor。 |
| **canonical relationship** | 一条持久关系（head + typed target），不是一次观察。 |
| **observation** | 抽出的 incoming edge/关系单元；CMR/MMR 的分母是 observations（final period 约 10.3K investor / 6.3K S&P edges，**是 Opus 4.6 reconciliation inputs；GPT 的 edge set 不同，不是通用分母**），不是 1,300 通电话。 |
| **short-term fusion** | 当期把非结构化 discussion 与结构化 cash-flow 合起来。 |
| **product–topic ontology** | 产品/主题的固定本体；用来把 topic 讨论关联到 product。 |
| **lifecycle** | Emerging / Reinforced / Stable / Fading / Reactivated。 |
| **CMR** | Correct Match Rate：incoming edge 被正确对到 prior memory 的比例。 |
| **MMR** | Match Rate：被接受为 match 的比例（频率）；Table 3 每个 strategy 都报，CMR = MMR × Merge Precision。 |
| **round-trip** | graph→text→graph 的重建 F1；用参考图/生成文档测抽取保真。 |
| **LLM2Graph** | 本文的抽取管线：LLM 从文档抽 (u,r,v,d) 与 period-local normalized mention；**不产别名**。 |
| **merge precision** | 被接受的 match 里正确的比例。 |

## 3. 它怎么做

### 3.1 数据

- **专有投资人数据**：10 个月度 period，每期约 1,200 calls；final period 约 1,300 calls / 10.3K incoming edges；配对月度组合现金流。
- **S&P 500 earnings transcripts**：297 家公司、3 个 reporting period；final period 约 6.3K edges；**无结构化现金流**。
- 模型：Claude Opus 4.6、GPT-5.4-mini；judge Gemini 3.1 Pro；human audit 200 incoming units/setting。

### 3.2 短期融合（within period）

- 实体：person/org、product、topic。
- 关系：`discussed`（非结构化）、`cf-signal`（结构化现金流）、`strong-interest`（融合）。
- **Rule 1–2**：保留未印证关系。
- **Rule 3**：同一投资人、同一 product 的 discussion + cash-flow → strong-interest。
- **Rule 4**：同一投资人的 topic discussion + 本体关联 product 的 cash-flow → product strong-interest；topic 仍保持 discussed。
- **关键**：topic 与 product 身份**不合并**；融合只增加引用，不覆盖原观察；source indicator 1/2/3 = unstructured / structured / hybrid，保留在 observation 里。

### 3.3 长期 registry

跨期匹配顺序：

1. identifier；
2. normalized name；
3. learned alias；
4. LLM semantic matching（同类型候选，score ≥0.8，取最高；否则新注册）。**0.8 是在 investor-call 语料的 T−1 上选的，再用于 final-period 评估**；不是通用默认值，存在阈值调优的乐观偏差。

匹配后的 surface form 加入该 anchor 的 alias set；**错误匹配可能把后续出现路由到错误历史**（不是所有同名出现；alias 在 identifier/name 之后）。

### 3.4 记忆强度与生命周期

- `σ_init=0.5`；匹配 `σ=min(1, σ+0.2)`；未匹配 `σ=γσ, γ=0.8`；低于 0.01 归零但**边不删除**。
- 每 period 每条 edge 至多一次强度/状态更新；多个观察/印证路径不重复计分。
- 五态：Emerging、Reinforced、Stable（≤3 misses）、Fading（>3 misses）、Reactivated（Fading 后再次匹配）。
- 边是 attribute vector `e_t=(u, h_t, v)`：每个观察的 id、原始 typed target、relation、source、timestamp、context、head，加 first/last seen、state、score。

### 3.5 一个具体例子

3 月通话提到「市场波动」，4–6 月没提，7 月也没提，8 月又提（月度 period）：

- 3 月：新建 edge `(investor, discussed, market_volatility)`，state Emerging，σ=0.5。
- 4/5/6 月：连续 3 次 miss → σ=0.5×0.8³≈0.256，state 仍 **Stable**（Fading 要第 4 次 miss）。
- 7 月：第 4 次 miss → state **Fading**（σ≈0.205）。
- 8 月：同一 surface form / alias 匹配 → σ=min(1, 0.205+0.2)≈0.405，state **Reactivated**。
- 边从未删除；只是强度/状态变化。

## 4. 结果：数字与条件

### 4.1 memory usability

> **no-alias** = 去掉 alias memory，但仍保留 canonical ID/name 匹配与跨期 semantic fallback；**LLM-Norm** = 每期独立做语义归一化，再跨期确定性匹配。两者都不是「完全不做身份对齐」。

| 设置 | Full FIRME CMR | no-alias CMR | LLM-Norm CMR |
|---|---|---|---|
| investor + Opus 4.6 | **30.4%** | 22.2% | 8.2% |
| S&P 500 + Opus 4.6 | **57.4%** | 46.1% | 23.9% |

- Full vs no-alias：**+7.8–12.1 pp**（4 个 dataset–backend 设置；另外两个 GPT-5.4-mini 端点是 CMR 26.5−18.7、36.7−24.6、比值 36.7/16.1=2.3×）。
- Full vs LLM-Norm：**2.3–3.7×**。
- human audit（200 units/setting）：CMR **+9.0–16.5 pp**；reattachment recall **+22.5–29.0 pp**；merge precision **85.6–97.5%**。
- token：final-period Full 6.20M vs no-alias 6.68M（−7.2%）；semantic matching token **−40.3%**。

### 4.2 抽取/round-trip

- investor calls hallucination：Opus 3.3% vs GPT 6.6%。
- normalization error（investor calls）：Opus 3.2% vs GPT 7.74%；S&P 500 上是 Opus 2.8% vs GPT 22.16%，**没有 backend 全面占优**（GPT 幻觉更低，但归一化误差约 8 倍）。
- investor calls round-trip F1：0.923–0.931。
- S&P 500 round-trip F1：Opus 0.862–0.865；GPT 0.786–0.805。
- Full fusion 输出有有效 evidence path：293/300（final-period investor-call data、Opus 4.6、short-term fusion 人工审计 precision；不是抽取指标）。

> 出处：Table 3, p.7（CMR/MMR/alias；固定 Gemini 3.1 Pro judge + 两标注者 fallback review 协议）；Table 4, p.8（token；investor/Opus/final period，**不含 registry 构建**）；Table 5, p.8（final-period、fusion 前的抽取关系）；round-trip 在 Table 6, p.9 / §4.3–4.4（每语料 1,000 个参考图，文档由固定 Opus 4.6 生成并共享）；human-audit CMR/merge precision 在 Table A2 / Appendix A（p.13，另一套 blinded 标注）；293/300 在 Table 7 / §4.5。

### 4.3 这些数字之间的逻辑

- **alias 为什么有用？** 历史 surface form 被记住后，下次出现直接命中，不必再走 LLM 语义匹配；CMR 提升、token 下降都是这条机制。
- **为什么 false merge 可怕？** 一个错误 alias 可能把后续同名观察路由到错误 anchor；错误不是一次性的，但「长期污染」是机制推断，未测量。
- **为什么 semantic matching token 降 40.3%？** 作者说与 alias reuse 一致；alias 命中会跳过语义调用，但这是相关性解释，不是因果隔离。
- **CMR 是什么、不是什么？** 它是「incoming edge 被正确对到 prior memory」的比例，不是答案正确率；CMR 高不等于 agent 任务成功。

## 5. 这些数字不能说明什么

1. **不是公开可复现。** 专有投资人数据与内部本体不公开；S&P 只有 transcript、无结构化现金流。
2. **不是年度周期。** 10 个月度 period / 3 个 reporting period；seasonality/long-term 结论受限。
3. **不是全量人工审计。** 200 units/setting 是抽样；依赖 historical search/reference labeling。
4. **不是通用参数。** 产品-主题本体、$100K 阈值、α=0.2 / γ=0.8 / N=3、semantic threshold 0.8 都是 use-case specific。
5. **未匹配 ≠ 关系结束。** 可能是输入缺失/没有观察机会；模型分不清。
6. **不是 latent preference。** 状态估计的是 observed evidence，不是投资人真实偏好。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先定稳定 head。** 投资人/公司必须有稳定 ID；speaker 变化不改 head。
2. **registry 分层匹配。** identifier → normalized name → learned alias → LLM semantic fallback（同类型、阈值 0.8）。alias 要存下来复用。
3. **短期融合只加引用，不合并身份。** topic 和 product 保持独立；印证是 strong-interest 标签 + 引用路径。
4. **边 key = head + typed canonical target。** relation/source 保留在每个 observation 里，但不进 key；每 period 每条边最多一次强度更新。
5. **衰减不等于删除。** 未匹配 → `σ=0.8σ`；低于 0.01 归零但边保留；Fading 后再次匹配 → Reactivated。
6. **生命周期用确定性状态机。** 状态可追溯到观察与 miss 的 period。
7. **评估分三层。** CMR、human-audit recall、extraction faithfulness/round-trip。CMR = MMR × Merge Precision，false merge 会拉低 merge precision，进而拉低 CMR；CMR 单独看不出的是覆盖率与正确率的分解。
8. **把 false merge 当一等风险。** 一个错误匹配会把后续所有同名出现路由到错误历史；merge precision 必须和 CMR 一起看。
9. **别名复用可能省钱，但不是免费。** Full FIRME 的 semantic matching token 比 no-alias 低 40.3%（仅 investor calls × Opus × final period，不含 registry 构建）；alias store 的构建/维护成本要单独算。

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| Registry / alias store | 一次性 + 持续 | canonical ID、alias set、semantic fallback |
| 短期融合规则 | 每域一次性 | 4 条规则 + product-topic 本体 + $100K 阈值 |
| Extraction | 每文档 | LLM2Graph；幻觉率 3.3–7.4%（investor calls 3.3–6.6%；S&P LLM2Graph 7.4%/5.87%） |
| 语义匹配 | 未匹配候选 | threshold 0.8；alias 复用可降 40.3% token |
| 记忆更新 | 每 period | 每边一次；确定性 |
| Human audit | 评估期 | 200 units/setting；部署可抽样 |
| 维护 | 本体/阈值/参数变更 | use-case specific |

**使能条件**：稳定 head ID；跨期数据；可维护的 alias registry；可接受 LLM 抽取误差；有 audit 能力。

### 6.3 何时用 / 何时别用

**用**：跨源、跨期、实体名漂移；需要 provenance；关系会休眠/复苏；有稳定 head ID。

**别用**：单次会话；实体名稳定；没有跨期观察；需要 latent preference 估计；无法承担 false merge 的下游污染。

### 6.4 最小落地清单

1. **先定稳定 head。** 投资人/公司必须有稳定 ID；speaker 变化不改 head。
2. **registry 分层匹配。** identifier → normalized name → learned alias → LLM semantic fallback（同类型，阈值 0.8）。
3. **alias 必须持久化。** 匹配后的 surface form 存回 alias set；否则每次都重新语义匹配。
4. **短期融合只加引用。** topic 与 product 保持独立；印证是 strong-interest 标签 + 引用路径。
5. **生命周期用确定性规则。** 匹配 `σ=min(1,σ+0.2)`；未匹配 `σ=0.8σ`；低于 0.01 归零但边不删除。
6. **把 false merge 当一等风险。** 抽样 audit reattachment；merge precision 与 CMR 一起报。
7. **不要用「未匹配」推断关系结束。** 它可能是输入缺失/没有观察机会。

## 7. 质量与边界

- **证据类型**：实证·真实专有数据 + 公开 transcript（一手正文）。
- **强项**：真实数据；human audit 与 judge 双轨；alias ablation 干净；生命周期/衰减参数透明；token 成本；诚实写 false merge 风险。
- **主要威胁**：专有数据不可复现；S&P 无结构化融合；3 period 不覆盖年度；human audit 抽样；ontology/threshold use-case specific；两个 backend/一个 judge。
- **`quality: B`**：内部效度强、真实数据、human audit；但复现性与外部效度受限。

## 8. 与仓库判断的关系

- **E-05（已核）**：本体在记忆系统中承担**对齐与印证条件**（跨期 identity registry、双模态互证），而非自由推理；alias memory 是增量；未匹配≠结束。false merge 是主要风险属于 **04-L5**，不是 E-05。
- **P1**：支撑「价值在约束/结构」：身份 registry + 规则融合，不是让模型自由记。
- **P2**：同一抽取器，换 historical registry + alias + 跨期 semantic fallback，CMR 差 2.3–3.7×；lifecycle/decay 是同一套，不是该比较的变量。
- **04-L3**：身份是状态的前置；alias memory +7.8–12.1 pp。
- **04-L5**：false merge 会长期污染。

## 9. 还没解决 / 下一步

- **alias memory 与 canonical registry/semantic fallback 的分别贡献？** 作者说未拆分。
- **false merge 的长期污染**：一个错误匹配影响多少后续观察？能否检测/回滚？
- **年度周期/季节性**对衰减参数的影响；能否学习 entity/relation-specific decay？
- **负信号（outflow/不满意）** 如何进生命周期？
- **公开数据上能否复现 CMR 增益？**
- **多域（CRM/医疗/工业）** 是否同样适用？

## 10. 原文

- arXiv:2610.40482
- PDF：同目录 `2610.40482-firme.pdf`
- 数据：专有；S&P 500 transcripts 公开。
