---
status: draft
updated: 2026-11-08
rq: [RQ2, RQ3]
evidence: []
---

# 精化：在既有本体上修

> **薄页（<2 篇独立来源）**：本页判断只作候选/边界，**不承担稳定判断**；引用时必须带「单来源」限定。

> 真实项目很少从零建本体；更常见的是「已经有一个，但不够用/有错/过时」。这里问「怎么定位该修哪条、怎么验证」，不负责生成（[generation](../generation/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 6 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | N1–N3（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 既有本体的子类/约束精化；不含从零生成、生命周期 |

## 当前判断

- **精化可以自动化到小规模。** CASTON default（fine-tuned OnT + Qwen3-8B）high-confidence 6/6 被两位专家接受；pretrained ensemble 4/7（57.1%）；GPT-4o mini 5/16（31.3%，行内同时换了 LLM 与 embedding）。限定：单一本体、单一公理类型、作者自述 preliminary。`已核`
- **同 LLM 下，fine-tune embedding 是最大的一阶增益。** 6/6 vs 4/7 = −42.9 pp；同 embedding 只换 LLM（Qwen3-8B → GPT-4o mini）是 −25.8 pp——但这是全文唯一一次换 LLM，GPT-4o mini 的规模未披露，不能当「更大/更小模型」的代表。**「换个更大 LLM 不能补」没测过**；论文报的 68.7 pp 是 default 对 GPT-4o mini，两个变量同换，不能拆。`已核`（两个单变量差值）／`推测`（外推）
- **medium 不可靠，但不是「全 mixed」。** default 的 2 条 medium 全部 mixed（0 接受）；pretrained 1/4（25%）、GPT-4o mini 1/5（20%）是被两位专家同时判负，不是 mixed。medium 一律人审。`已核`
- **「瓶颈」与覆盖率都没测。** CASTON 固定 30×10 只测池内接受率：既不拆「定位错」与「验证错」，也不报 recall@30（真错公理进不进前 30）/ recall@10（正确父类在不在候选池，池子还排除已断言父类）。旧版把「瓶颈是定位与验证」挂在 `05-L5` 上，而 `05-L5` 的证据就是本页——循环引证；本仓库只当工作假设。`推测`（瓶颈）／`已核`（缺口：两个召回未报）
- **下游未闭环。** 修复是否让判定器/应用变好，没测。`已核`（缺口）

## 文件地图

| 想知道 | 去 |
|---|---|
| 两种做法/CASTON 数字/失效 | [mechanism](./mechanism.md) |
| 接口 / 参数与 recall@30/@10 / 成本 / stop 与「别用」5 条 | [mechanism](./mechanism.md) 的「工程发现 1–4」 |
| 客户指标与试点判据（V3） | [mechanism](./mechanism.md) 的「客户指标/V3」 |
| 六条判断的证据/边界 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [CASTON digest](../../../src/papers/2610.21466-caston-refinement/digest.md) |
| 研究提示词与输出 | [prompt.md](./prompt.md)；run 记在 `runs/`（有 prompt 才建） |

## 边界

- **不是大规模。** 单一本体、单一公理类型、6 条高置信修复。
- **不是关系公理。** 只覆盖 asserted atomic subsumption；∃r.B、cardinality、disjointness 是作者 future work。
- **不是下游闭环。** 修复是否让判定器/应用变好，没测。
- **不是通用 confidence。** 换模型要重测校准。
- **不是全覆盖。** recall@30 / recall@10 未报，6/6 不能当覆盖率。

## 关联

- 派：[05 生产](../README.md) · 局部结论：[05-L2](../claims.md)；`05-L5` 的「瓶颈」已降为推测（见 [F6](./findings.md)）
- 相邻：[generation](../generation/README.md) · [lifecycle](../lifecycle/README.md)
- 判定：[02 checker](../../02-judgment/checker/README.md)
