---
status: draft
updated: 2026-11-07
quality: B
based_on: card.md
claims: [E-05]
---

# FIRME · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**要做「跨源、跨期、可审计的关系记忆」，按这个顺序：**

1. **先定稳定 head。** 记忆图的主体（投资人/公司）必须有稳定 ID；speaker 变化不改 head。
2. **registry 分层匹配。** identifier → normalized name → learned alias → LLM semantic fallback（同类型、阈值 0.8）。**alias 要存下来复用**，否则每次都走语义匹配。
3. **短期融合只加引用，不合并身份。** topic 和 product 保持独立；discussion + cash-flow 的印证是 strong-interest 标签 + 引用路径，不是把 topic 并进 product。
4. **边 key = head + typed canonical target。** relation/source 保留在每个 observation 里，但不进 key；每 period 每条边最多一次强度更新。
5. **衰减不等于删除。** 未匹配 → `σ=0.8σ`；低于 0.01 归零但边保留；Fading 后再次匹配 → Reactivated。
6. **生命周期用确定性状态机。** Emerging / Reinforced / Stable / Fading / Reactivated；状态可追溯到观察与 miss 的 period。
7. **评估分三层。** CMR（MMR × merge precision）、human-audit recall、extraction faithfulness / round-trip；只看 CMR 会漏掉 false merge 与 extraction 丢失。
8. **把 false merge 当一等风险。** 一个错误匹配会把后续所有同名出现路由到错误历史；merge precision 必须和 CMR 一起看。
9. **别名复用是省钱机制。** Full FIRME 的 semantic matching token 比 no-alias 低 40.3%；记忆不只是准确率，也是成本。

## 实用意义

它解决的操作问题：

- **「同一客户在 CRM 与工单系统里被建成两个实体，历史被劈成两半。」** → registry + alias memory，跨源对齐到同一关系历史。
- **「客户三个月没来，是流失还是没记录？」** → 衰减而非删除；未匹配是「当前证据弱」，不是「关系结束」。
- **「讨论的主题和实际买入的产品不是一回事。」** → topic/product 分开；印证用引用，不合并身份。
- **「记忆越存越乱，不知道哪条还有效。」** → 五态生命周期 + 记忆强度；可审计。
- **「换一个模型，记忆就漂移。」** → 身份与状态是确定性的；只有 extraction/semantic matching 依赖模型。
- **「语义匹配太贵。」** → alias 复用，semantic token −40.3%。

**何时用**：跨源、跨期、实体名漂移；需要 provenance；关系会休眠/复苏；有稳定 head ID。

**何时别用**：单次会话；实体名稳定；没有跨期观察；需要 latent preference 估计；无法承担 false merge 的下游污染。

## 质量评估

- **证据类型**：实证·真实专有数据 + 公开 transcript（`已核`，一手正文）。
- **样本与对照**：10 个月度 period（~1,200 calls/期）；S&P 500 297 公司 × 3 period；4 dataset–backend 设置；5 策略；human audit 200 units/setting；token 账。
- **优点**：真实数据；human audit 与 judge 双轨；alias ablation 干净；生命周期/衰减参数透明；token 成本；诚实写 false merge 风险。
- **主要威胁**：专有数据不可复现；S&P 无结构化融合；3 period 不覆盖年度；human audit 抽样；ontology/threshold use-case specific；两个 backend/一个 judge。
- **`quality: B` 理由**：内部效度强、真实数据、human audit；但复现性与外部效度受限，不够 A。

## 洞察

1. **身份是记忆的瓶颈，不是抽取。** alias memory 在 4 个设置上把 CMR 提升 7.8–12.1 pp；canonical-only + semantic fallback 已经比 LLM-Norm 好，alias 再加一层。`已核`
2. **「没观察到」不等于「关系结束」。** 未匹配只降低当前强度，不删除边；Fading 后可以 Reactivated。**但作者也承认：未匹配可能是输入缺失/没有机会，模型分不清。** `已核`
3. **topic 与 product 必须分开。** 同一主题讨论可以印证多个产品，但不能把 topic 并进 product；否则身份历史会被污染。`已核`（设计）
4. **确定性生命周期是可审计的代价。** 状态由 match/miss 规则决定，不依赖模型；这让「为什么这条关系是 Fading」可追溯。`已核`
5. **False merge 是长期污染。** 一个错误匹配会把后续同名出现路由到错误 anchor；merge precision 必须和 CMR 一起报。`已核`
6. **别名复用是记忆的成本优势。** semantic matching token −40.3%；记忆不仅提高准确率，还减少重复计算。`已核`
7. **Human audit 与 judge 的 CMR 排序一致。** 精度差 0.3–5.8 pp；说明 judge 协议在这个任务上可用，但不能替代 audit。`已核`
8. **生命周期参数是 use-case specific。** α=0.2、γ=0.8、N=3 是默认值；换域/换周期要重标。`推测`（工程判断）

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| Registry / alias store | 一次性 + 持续 | canonical ID、alias set、semantic fallback |
| 短期融合规则 | 每域一次性 | 4 条规则 + product-topic 本体 + $100K 阈值 |
| Extraction | 每文档 | LLM2Graph；幻觉率 3.3–6.6% |
| 语义匹配 | 未匹配候选 | threshold 0.8；alias 复用可降 40.3% token |
| 记忆更新 | 每 period | 每边一次；确定性 |
| Human audit | 评估期 | 200 units/setting；部署可抽样 |
| 维护 | 本体/阈值/参数变更 | use-case specific |

**使能条件**：稳定 head ID；跨期数据；可维护的 alias registry；可接受 LLM 抽取误差；有 audit 能力。

**2022 年做会卡在哪**：LLM 抽取/语义匹配不稳；没有 Opus/GPT-5 级模型；temporal KG 的 provenance 工具不成熟；但 registry 思路本身不依赖模型。

**反向条件**：单会话；实体名稳定；无跨期观察；需要 latent preference；false merge 代价极高且无法 audit。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **E-05** | **一手依据**：本体在记忆系统中承担**对齐与印证条件**（跨期身份 registry、双模态互证），而非自由推理；克制的用法更易落地。补充：alias memory 是增量；未匹配≠结束；false merge 是主要风险。 |
| **P1** | 支撑「价值在约束/结构」：身份 registry + 规则融合，不是让模型自由记。 |
| **P2** | 支撑「harness 不可分离」：同一抽取器，换 registry/lifecycle，CMR 差 2.3–3.7×。 |
| [memory](../../../topics/04-state/memory/README.md) | 核心文献；机制细节回 card。 |
| [identity](../../../topics/04-state/identity/README.md) | 跨期身份对齐的直接案例。 |

## 不可迁移

- 专有投资人数据与内部本体不可公开；不能独立复现。
- S&P 500 无结构化现金流；只测抽取+时间对齐。
- 3 个 period（月度/报告期），不覆盖年度周期/季节性。
- 产品-主题本体、$100K 阈值、α/γ/N 都是 use-case specific。
- 两个 backend、一个 judge；不能外推到所有模型。

## 开放问题

- alias memory 与 canonical registry/semantic fallback 的分别贡献？作者说未拆分。
- False merge 的长期污染：一个错误匹配影响多少后续观察？能否检测/回滚？
- 年度周期/季节性对衰减参数的影响；能否学习 entity/relation-specific decay？
- 负信号（outflow/不满意）如何进生命周期？当前只有正向/缺失。
- 公开数据上能否复现 CMR 增益？
- 多域（CRM/医疗/工业）是否同样适用？尤其是 topic/product 本体介导的规则。
