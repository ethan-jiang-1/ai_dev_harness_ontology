---
status: draft
updated: 2026-11-11
type: evidence-note
target: X5 false-veto / false-block
---

# X5 校准理论：false-veto 是一个前沿，不是一个阈值

> **2026-11-11 素材重置注**：原来源 `2607.22868`（与下文的 POLAR `2610.08082`）均因未过准入门于 2026-11-11 移出（见 [黑名单](../../../meta/rules/excluded-sources.md) 与 [tombstone](../../../meta/audits/2026-11-11-source-purge.md#src-2607-22868)）。本页保留为「为什么 X5 应理解为前沿曲线而非单点阈值」的概念注记，不作现行实证定锚。
>
> **工作底稿，不是交付正文。** 原为改写 X5 表述而作，不新增 E。

## 1. 它证明什么

| 结论 | 内容 |
|---|---|
| **Neyman–Pearson 前沿** | 固定一步决策、固定外生 law 时，给定 miss 上限 β，最小 false-block 概率是 `roc_I(β)`；任何使用同一信息 I 的规则/集成/wrapper 都不能低于这个前沿。 |
| **信息 refinement** | 如果 I' 比 I 更细（Blackwell），`roc_I'(β) ≤ roc_I(β)`；但「条件依赖」本身不够，必须扩大可达 error region。 |
| **闭环改变前沿** | 一旦 block 改变未来 proposal，静态分数与 ungated 轨迹不必识别闭环前沿；需要有限受控模型 + occupancy program。 |
| **Conformal 证书** | label-conditional exchangeability 给有限样本边际证书；**可能是 vacuous 的 block-all**。它证明风险，不证明接近 population ROC 前沿。 |
| **表示攻击** | 对 judge 可见表示的 bounded attack 会加 robustness margin；benign calibration 不自动迁移。 |

## 2. 它测了什么（摘要级/正文片段）

- AgentDojo 132 条（97 user-task + 35 injection-goal），23 个 open/closed/dedicated guard judges 打同一批。
- **δ=.05 时，每个 judge 的 split threshold 都是 block-all**；也就是说，要在 5% miss 下给证书，校准可能只能「全拦」。
- Gemma-2-9B：δ=.10 → miss .010（同时上界 .021），**false block .780**（95% 同时区间 [.660,.901]）；δ=.20 → miss .138，但上界 .264，未被这个诊断认证。
- 有限受控两步 retry 模型：perfect recall cost .551；current-score/time policies .863；stationary thresholds 1.137；这是 analytic model check，不是 AgentDojo 的未知 kernel。
- 表示攻击：simultaneous inference 在 8/11 fully cached judges 上检测到 miss 增加；第 9 个点估计为正。它诊断一个 operating point，不能单独认证/否证 margin-aware calibration。
- 代码/缓存分数：`https://github.com/shawnray-research/certified-agent-guardrails`（未读/未跑）。

## 3. 对 X5 的改写

**不要写「false-veto ≤5%」当作单一验收线。** 更准确的写法：

> false-veto 是「在给定 miss 上限下的 false-block 前沿」；要报 **miss–false-block 曲线**（或至少几个 operating points），而不是一个点。低 miss 证书可能只能靠 block-all 获得；那样的「零漏检」没有可用性。

这把 X5 从「false-veto 未测 → unknown」推进到「**false-veto 可校准，但要报前沿；POLAR 没有标签，仍不能算**」。verdict 仍是 `unknown`（POLAR 一手数），但 expectation 的写法要改：D1 的 X5 不应只写 `≤5%`，应写「在 miss 预算下报 false-block 前沿」。

## 4. 边界

- 它是理论 + 诊断，不是 POLAR/CASEL 的替代；没有 ontology，没有本体的可逆性判据。
- AgentDojo 是 prompt-injection 安全评测，不是工具授权/commit gate；外推要谨慎。
- Conformal 证书是 marginal、label-conditional、per deployment proposal；不是 within-episode independence，也不是语义正确性。
- block-all 的「零 miss」是 vacuous certificate；不能当「安全」。
- digest 已入档（L2）；本页是摘要级笔记，不是精读。

## 5. 什么会改变它

- 在 POLAR 的 blocked log 上标授权标签 → 可把 retention 换成 false-block 点。
- 有部署把 miss 预算与 false-block 曲线一起报 → 可给 X5 一个可操作的验收线。
- 有本体-specific 的校准实验 → 才能谈「本体闸的 false-veto 前沿」。

> 回到 [数据表索引](../README.md)。
