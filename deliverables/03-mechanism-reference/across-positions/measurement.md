---
status: draft
deliverable_status: draft
updated: 2026-11-10
section: measurement
evidence: [E-01, E-02, E-03, E-04, E-05, E-08, E-12, E-14, E-15, E-16, E-17, E-18, E-20, C-03]
---

# 尺子跟机制走：八行分派

> 03 的方法论主轴是 C-03：**用准确率/reward 量控制类机制，会得出错误结论。** 本页把它落成一张按位置分派的表。
>
> **这是设计（D），不是已验证的方法。** 上游在 [topics/06-measure/metrics/mechanism.md](../../../topics/06-measure/metrics/mechanism.md#按位置分派八行设计)；施工细节与 stop 线在 [02 §9](../../02-engineering-playbook/sections/acceptance.md#51-验收与-stop按机制选尺)。

## 1. 两本账

| 账 | 记什么 | 适用位置 | 看不见什么 |
|---|---|---|---|
| 任务账 | 答对/答错、token、时延、轮次 | context、evidence（不改变走向） | 被拦住的伤害、被误拦的正确动作 |
| 风险账 | 被拦住的伤害、误拦、审批量、false-defer | checker、action、commit（能改变走向） | 任务是否完成、用户是否等待更久 |

> 用任务账验收风险机制，会把「没发生的伤害」记成 0，把「误拦」记成「没做成」。这不是说任务账没用，而是说它只回答任务问题，不回答风险问题。`推测`（C-03 的展开，不是新 E）

## 2. 八行分派

| 位置 | 失效形态 | 主指标 | 非对称代价 | 基线 | 证据 |
|---|---|---|---|---|---|
| context | 不准 / 内部没有 | primary-trap avoidance；element score；准确率 | 知识没覆盖 vs 投影太长/顺序错 | K1；纯文本 RAG | E-12/E-14/E-01 |
| memory | 做错 / 内部没有 | CMR；Acc@complete | false merge vs false split/漏配 | 不做 registry；LLM-Norm | E-05/E-17 |
| evidence | 不准 / 输出对了 | 准确率；引用率 | 无依据 vs 过度引用/等级通胀 | 纯文本 RAG | E-03 |
| checker | 做错 | 增量 catch；FA | 漏检 vs 误报后修坏 | 空结果重试 | E-02/E-20 |
| action | 做错 / 没做 | harm/HSR；false-veto；审批量 | 误拦合法动作 vs 漏放有害动作 | 不上护栏；blanket veto | E-04/E-13/E-15/E-16 |
| commit | 做错 / 没做 | false-defer；false merge；授权正确率 | 误 defer vs 误放行 | 不做 gate；直接 merge | E-20 + 设计 |
| read-path | 做错 | 泄漏率（subject/object）；误拦率 | 泄漏 vs 误拦 | 不过滤 | E-20 |
| determinism | 没做 | 收敛/漂移；重复运行一致率 | 假收敛 vs 假漂移 | 同输入重复运行；无锚点 | 设计（无 E） |

> 每行的过程指标、stop 线、成本口径在 [02 §9](../../02-engineering-playbook/sections/acceptance.md#51-验收与-stop按机制选尺) 与 [topics metrics](../../../topics/06-measure/metrics/mechanism.md#按位置分派八行设计)；本页不复制，避免两处漂移。

## 2.5 机制类型与尺子分派

> 这是 C-03 的 2×2：**逐格已核，方向翻转是跨来源综合**（没有同一机制、同一数据、两把尺子的对照）。完整记录见 [O-M04](../../../topics/objects.md)。

| 机制类型 | 任务账（accuracy / reward） | 风险/成本账（harm–approval / token） |
|---|---|---|
| **约束**（action / checker） | E-04：18 格仅 8 格改善；retail 与强模型回退；T1-only 0.087 ≈ full 0.080 | E-15：CASEL 7.02% HSR / 8.7% approvals；比 Risk-Menu 少约 31% 审批（HSR 5.82% 更高） |
| **知识供给**（context） | E-01：被测工件 acc. neutral；E-12：K2 在单工厂 +19.8pp（薄层） | E-08/E-14：平均 −38%，但 −91%/+1.9% 两端；O-F15：同预算 token 效率 12.7×（派生） |

**读法**：同一行的两格方向可以相反——约束类在任务账上混合/负，在风险账上前沿更优；知识供给在准确率上 neutral，在 token 上正收益。**这是 C-03 的具体化，不是新实验**：逐格标 `已核`，翻转标 `推测（综合）`（[06-L16](../../../topics/06-measure/claims.md)）。要升 E，需要「同一机制、同一数据、两把尺子」的对照。

## 3. 四条读表规则

1. **主指标跟着失效形态走。** 没有「所有位置都看 accuracy」这回事；闸门看 harm/审批，判定器看 catch/FA，记忆看 CMR/Acc@complete。
2. **非对称代价必须成对报。** 漏/误、false-veto/漏放、false-defer/误放行不能合成一个数；合成会丢掉代价。
3. **先建基线，再建机制。** checker 先比空结果重试；编译先比未编译 harness；action 先比不上护栏。没有基线，分不清机制有效还是基线太弱。
4. **先量噪声，再比配置。** 同一配置 5 runs 起步；E-18 的 54% 方差来自真实尝试上的 run-to-run 噪声。效应量小于噪声带时，写「不可判」，不写「无差异」。

## 4. 为什么不能合成一个分数

- 每个位置量的是不同的东西：token、catch/FA、审批量、false-defer、伤害率。
- 合成一个分数会丢掉「代价/误拦/审批」；同一机制可以在任务账上变好、风险账上变坏。
- 同一场景可能要叠加多个位置；表里的先后是**错误传播路径**，不是优先级。
- 强端不是默认答案：E-04 的 retail/强模型回退、E-13 的能力梯度都说明，强端在高基线下可能只剩代价。

> **组织建议（非 E）**：不要用单一 score 做 go/no-go；至少给「主指标 + 非对称代价 + 成本口径 + 噪声带」四栏。没有这四栏，评审材料只作诊断。

## 5. 证据边界

| 证据 | 支持什么 | 不能证明什么 |
|---|---|---|
| E-02 | catch/FA 可测；空结果基线 | 部署 precision；false-veto |
| E-04 | reward 不是防伤害度量；回退 | 结构判据有效；所有护栏 |
| E-15 | harm–approval–cost 前沿 | 本体增益；审批疲劳 |
| E-18 | 噪声地板；配置轴 | 跨域常数 |
| C-03 | 度量错配是冲突主因（`推测`） | 不是新证据；不能替代机制级测量 |

## 6. 什么会改变这张表

- 某位置出现「主指标与非对称代价结论相反」的实测 → 加决策规则，或拆主指标；
- 噪声带大于所有可用效应量 → 该行只能写「不可判」；
- commit/determinism 出现实现与指标 → 把「无 E」改成「有实现/有限证据」；
- 跨域复现显示某行不适用 → 加域维，不强行统一。

## 7. 上游

- [topics/06-measure/metrics/mechanism.md](../../../topics/06-measure/metrics/mechanism.md)（八行原始表 + 方法要求）
- [topics/06-measure/metrics/coverage.md](../../../topics/06-measure/metrics/coverage.md)（能不能碰到）
- [topics/06-measure/feasibility](../../../topics/06-measure/feasibility/README.md)（成本/盈亏平衡）
- [conclusions](../../../topics/conclusions.md) 的 C-03 与相关 E
