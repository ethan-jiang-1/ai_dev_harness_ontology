---
status: draft
updated: 2026-11-09
type: evidence-note
target: E5 false-veto
---

# E5 数据表：false-veto 能不能从已发表数据估出来？

> **工作底稿，不是交付正文。** 数字用于更新 D1 的 E5 verdict；正式引用仍走 E-xx 与 [01/action-gate](../../../topics/01-constraint/action-gate/README.md)。来源为 POLAR digest 与论文 Table 5/6、Appendix B.3；不在这里新增结论。

## 1. 已发表什么

| 项 | 数字/事实 | 出处 |
|---|---|---|
| blocked decisions | **1,745 条** | POLAR §4.6 / Appendix B.3 |
| 主 block 工具 | GPT-OSS-120B retail `return_delivered_order_items` 150 次、`exchange_delivered_order_items` 103 次；Nemotron-9B airline `update_reservation_flights` 77 次 | Table 6 |
| block 原因 | airline：`NO_CANDIDATE`（反向搜索凑不出完整逆序列）；retail：`EXTERNAL_SIDE_EFFECT` | §4.6 |
| 阈值保留率 τ=0.80 | airline **36.6%**、retail **100%**、telecom **98.7%** | Table 4 |
| 阈值保留率 τ=0.50 / 0.90 | 100/100/100；17.6/48.9/98.7 | Table 4 |
| tier ablation（qwen3-8B airline，150 runs/arm） | full 0.080；no T3 0.073；T1+T3 0.087；**T1-only 0.087**；no irreversible 0.060 | Table 5 |
| 主实验 18 格 | 8 格改善；airline 六模型四个 +0.11–0.18；retail/强模型回退 | Table 3 |
| 论文自述 | blocked log **没有独立的 harm/authorization 标签**；不能建立 false-veto 率或 prevented harm | §4.6 / §7 |

## 2. 缺什么

- **没有「这条 blocked decision 本来是否合法」的标签。** 这是 false-veto 的定义所需；没有它，只能看 block 原因和工具名。
- **没有 harm 标签。** 不知道被拦的动作是否真的会造成伤害；reward 也不是 harm 度量。
- **没有意图/授权信息。** retail 的 return/exchange 可能是合法用户请求；airline 的 cancel/update 也可能是。
- **没有同轨迹配对。** T1-only 与 full 的增益差 0.007（0.087 vs 0.080），CI 重叠；不能分离「结构」与「保守拒绝」。

## 3. 能推断到哪一步

- **retail 的 return/exchange 是 false-veto 的高风险候选**：论文自己说这些可能是合法请求，且 block 原因是 `EXTERNAL_SIDE_EFFECT`。但**没有标签，不能量化**。
- **airline 的 `NO_CANDIDATE` 不必然是误拦**：可能是本体没写全（漏了 T1/T2 边），也可能是动作真的不可逆；论文没有区分。
- **保留率不是 false-veto 率**：airline 36.6% 是「有非空候选池的 logged decisions」在固定轨迹上的保留率，不是「拦对了多少」。
- **T1-only ≈ blanket veto**：airline 没有 T1 注释，T1-only 对所有 mutating 调用 veto；它的增益与 full 相近，说明收益可能来自保守拒绝，而不是结构反向组合。

## 4. E5 verdict 候选

| 子句 | verdict | 依据 | 边界 |
|---|---|---|---|
| harm 降低 | `supported（限定）` | E-04：airline 4/6 模型 +0.11–0.18，18 格 8 格改善 | τ²-bench、单 wrapper、reward 不是 harm |
| false-veto ≤5% | **`unknown`** | 1,745 条 blocked 无标签；论文明确说不能算 | 需要人工标注或部署标签 |
| 部署有效 | `conditional` | 弱模型/高不可逆风险下有信号；强模型/retail 回退 | 能力梯度是六点拟合，无阈值 |

**结论**：E5 的 false-veto 不能从已发表数据估出来；**不要用 retention 或 block count 代算**。D1 应写 `unknown`，并把它列为「距离」里最硬的一块。

## 5. 什么会改变它

- 拿到 POLAR 的 blocked log（或抽样）并标「本可合法执行」→ 可直接算 false-veto。
- 有第二个部署报告 false-veto/误拦率，且给出 harm/授权标签。
- 有同轨迹配对实验，分离 T1-only 与 full。

**没有这些，E5 的 false-veto 保持 `unknown`；D1 的能力地图不分层改变。**
