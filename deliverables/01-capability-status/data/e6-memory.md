---
status: draft
updated: 2026-11-11
type: evidence-note
target: X6 memory/identity
---

# X6 数据表：CMR/Acc@complete 有 prior，但跨域和 false merge 没底

> **工作底稿，不是交付正文。** 数字用于更新 D1 的 X6 verdict；正式引用走 E-05/E-17 与 [04/memory](../../../topics/04-state/memory/README.md)、[04/identity](../../../topics/04-state/identity/README.md)。来源为 FIRME/EvoMemState digest 与论文 Table 3/4、Table A2；不新增结论。

## 1. FIRME 已发表什么

| 项 | 数字 | 条件 |
|---|---|---|
| Full FIRME CMR | investor/Opus **30.4%**；S&P/Opus **57.4%** | final period |
| no-alias CMR | 22.2% / 46.1% | 仍保留 canonical ID/name + semantic fallback |
| LLM-Norm CMR | 8.2% / 23.9% | 每期独立归一化 |
| alias 增量（Full − no-alias） | **+7.8–12.1 pp** | 4 个 dataset–backend 设置 |
| Full vs LLM-Norm | **2.3–3.7×** | 4 settings |
| human audit CMR | **+9.0–16.5 pp** | 200 incoming units/setting |
| reattachment recall | **+22.5–29.0 pp** | 同上 |
| merge precision | **85.6–97.5%** | 4 settings；不是都 ≥90% |
| semantic matching token | **−40.3%** | investor × Opus × final period；不含 registry 构建 |
| total token | −7.2% | 6.20M vs 6.68M |
| 数据 | 10 个月度 period，~1,200 calls/期；final ~1,300 calls / 10.3K edges；S&P 297 公司 / 3 period，final ~6.3K edges | 专有 + transcript；S&P 无结构化现金流 |
| 公式 | `CMR = MMR × merge precision` | 单看 CMR 会把「合并更激进」误判成进步 |

## 2. EvoMemState 已发表什么

| 项 | 数字 | 条件 |
|---|---|---|
| Complete Retrieval | **85.6%** | MemoryBank 86.4%，相当 |
| Acc@complete（LoCoMo-Refined） | **70.8%** | **+11.5** |
| Acc@complete（MemSyco） | **68.5%** | **+31.2** |
| MemSyco accuracy（Qwen3-8B / GPT-4o-mini） | 57.6%（+12.2）/ 58.9%（+5.9） | — |
| ablation（MemSyco） | w/o Relational 48.7（−8.9）；w/o Reasoning 49.6（−8.0）；w/o RL 49.7（−7.9） | 两状态各有贡献 |
| 规模 | 4 基准、9 baseline、ablation、跨系统迁移 | 文本 only；GRPO 需答案/评分器 |
| 边界 | Reasoning State 不可形式验证 | 不是形式保证 |

## 3. 用 D1 的 X6 阈值去套

X6 的验收线是「CMR 或 Acc@complete 相对基线 ≥ +10pp，merge precision ≥90%」。

| 证据 | 是否过线 | 说明 |
|---|---|---|
| FIRME alias CMR +7.8–12.1pp | **部分** | 有的设置 <10pp；4 settings 不是都过 |
| FIRME human audit CMR +9.0–16.5pp | **部分** | 同上 |
| FIRME merge precision 85.6–97.5% | **部分** | 有的设置 <90%；90% 是预登记线，不是通用阈值 |
| EvoMem Acc@complete +11.5/+31.2 | **是** | 但 Complete Retrieval 85.6% ≈ baseline 86.4，增益在「会用」 |
| 跨域复现 | **没有** | 专有投资人数据 + S&P；无第二独立域 |

**结论**：X6 是 `supported（限定）`——alias/状态层在已测设置里有增量，但**不是所有设置都过 +10pp / 90%**；跨域和 false merge 传播仍是空的。D1 不应写「记忆层稳定 +10pp」，应写「有条件」。

## 4. 缺什么

- **跨域复现**：FIRME 是金融/投资人；EvoMem 是个人助手/对话；没有工业/客服/医疗的同口径。
- **false merge 的传播幅度**：一个错误 alias 会把后续同名观察路由到错误 anchor；论文未测长期污染，也无自动回滚。
- **无训练信号的 reasoning state**：EvoMem 需要 GRPO/评分器；没有信号时收益未验证。
- **客户任务指标**：CMR/Acc@complete 不等于 agent 任务成功；论文没有下游任务对照。
- **维护成本**：registry/alias/本体维护未测。

## 5. X6 verdict 候选

| 子句 | verdict | 依据 | 边界 |
|---|---|---|---|
| alias memory 提升 CMR | `supported（限定）` | E-05；+7.8–12.1pp，4 settings | 专有数据；非全部 ≥10pp |
| 状态层提升 Acc@complete | `supported（限定）` | E-17；+11.5/+31.2 | 文本 only；需训练信号 |
| merge precision ≥90% | **`unknown`/部分** | 85.6–97.5%；有的设置 <90% | 按域重标 |
| 跨域有效 | **`unknown`** | 只有两个域 | 需要第二独立域 |
| 部署有效 | `conditional` | CMR/Acc@complete 不等于任务成功 | 先定下游指标 |

## 6. 什么会改变它

- 第二个独立域（工业/客服/医疗）的同口径 CMR/Acc@complete。
- false merge 的传播测量 + 回滚机制。
- 无训练信号的 reasoning state 对照。
- 下游任务指标：同一客户历史证据的引用正确率、任务成功率。
