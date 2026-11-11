---
status: draft
updated: 2026-11-11
type: evidence-note
target: X3 compilation economics
---

# X3 数据表：`p_h` 能算，但不能从论文抄

> **工作底稿，不是交付正文。** 数字用于更新 D1 的 X3 verdict；正式引用走 E-08/E-14 与 [03/compilation](../../../topics/03-knowledge/compilation/README.md)。来源为 CAI digest 与论文 §4.4/§8.6；不新增结论。

## 1. 已发表什么

| 项 | 公式/数字 | 条件 |
|---|---|---|
| 无限视野盈亏平衡 | `p_h > 2.0%` | `0.019/(0.91+0.019)`；论文门 + FRAMES |
| 有限视野 | `p_min = 2.0% + c/(0.929Q)` | `c` 为**首次**编译成本（query-equivalent），`Q` 为查询次数 |
| 编译成本折算 | `c = D × T_doc / T0` | `D` 文档数、`T_doc` token/文档、`T0` 未编译时每问 token |
| 示例 | `Q=1,000, c=10` → `p_min=3.12%` | 冻结语料；`p_h=2.5%` 仍亏 5.8 query-equivalent |
| 回本示例 | `p_h≈0.43, c=10` → 约 26 次查询 | 冻结语料 |
| token 条件收益 | hit −91%、miss +1.9%、平均 −38% | FRAMES N=200；单 compiler/answer model |
| 时延 | 配对子集约 3×（46.7 s → 140 s） | **仅 7 题**；不是 p95 |
| 决策门 arm mean | 有证据 −52%、无证据 −30%；140→30 s | arm mean，题数更少，不能与 −91/−38 直接比 |
| `p_h` 实测 | **没有直接计数**；43% 由 −38% 反推 | Eq(6)；不是实测 |
| 门实现 | §7 seam 说三特征（unit count/source diversity/entity coverage）；§7 judge selection 与 Listing 1 说 Qwen/StartLux judge | 论文内部不一致；`p_h` 的测量对象随实现变 |
| φ（false-accept） | Eq(11)：`φ=(a_T−a_A)/(a_T−a_F)`；论文**没有报 φ**；100–400 条审计只设计、未跑 | 100 labels 区间约 4–16%；400 labels 约 7–13% |
| 样本量 | 100–200 问只够 smoke；判 `p_h` 约需 1,600–2,000 条 shadow 查询（±0.7–0.8pp） | digest 推算；不是论文数 |

## 2. 缺什么

- **自己的 `p_h`**：论文 43% 是反推值；你的门、语料、抽取器、服务模式不同，必须 shadow 量。
- **自己的 `c`、`Q`、miss penalty、p95**：论文只给 token 与相对时延，没有金额/机时/人日。
- **φ**：`p_h` 是接受率，不是正确率；不知道 φ 就不能自动放行。
- **门实现**：论文自己没统一「三特征规则」与「Qwen judge」；部署前要先固定一种并记版本。
- **维护成本**：变更率→重抽→重聚类、人日，论文没给；`c` 只是首次编译。

## 3. 能推断到哪一步

- **公式可以用**：`p_min = 2% + c/(0.929Q)` 是可复算的门槛；把 `c`、`Q` 换成自己的数即可。
- **2% 不能移植**：它是论文门 + FRAMES 语料的标定带（2.0–3.6%）；企业短上下文会把 `c` 抬高，`p_min` 可能到几十个百分点。
- **平均 −38% 不能立项**：它掩盖 hit/miss 两端；先量 `p_h` 与 miss，再谈 token 节省。
- **时延是硬约束**：3× 只在 7 题上测；如果 KPI 是任务完成时间，token 节省可能不划算。

## 4. X3 verdict 候选

| 子句 | verdict | 依据 | 边界 |
|---|---|---|---|
| 公式/盈亏平衡 | `supported` | E-14；论文 Eq(3)–(9) | 公式本身；不代表你的 `p_h` |
| 平均 −38% 可上线 | `contradicted` | E-08/E-14；hit/miss 混合 | 不能当部署依据 |
| 目标流量 `p_h ≥ p_min` | **`unknown`（部署前）** | 缺自己的 `p_h`/`c`/`Q`/miss | 必须 shadow 量 |
| 编译降准确率 | `supported（限定）` | E-01；强 harness 下无可检出增益 | 单基准；ontology not measured |

**结论**：X3 是 `conditional`——公式成立，部署结论取决于自己的三到五个数。D1 应写「先量 `p_h`，再谈买不买」，不是「平均省 38%」。

## 5. 什么会改变它

- 自己的 shadow：`p_h` 的 95% CI 下界 > `p_min`，且 p95 不超预算 → 可试点。
- 企业语料的 `p_h`/miss 报告：若远低于 43%，2% 门槛失效。
- φ 的审计：若 φ 高，`p_h` 高也不能自动放行。
- 门实现的统一：规则门 vs judge 门的成本/延迟差异会改变 `p_min`。

> 回 [01 目录](../README.md) ｜ 回 [01 §数据表](../README.md#数据表工作底稿)
