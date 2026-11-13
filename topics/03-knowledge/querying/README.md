---
status: draft
updated: 2026-11-10
rq: [RQ1, RQ5]
evidence: [E-21]
---

# 查询：自然语言 → 可执行 SPARQL 的三条路线

> 回答：领域 KG 上，自然语言问题怎么变成可执行查询、瓶颈在哪；不回答：KG 怎么构建（去 [05/representation](../../05-produce/representation/README.md)）、读路径权限怎么过滤（去 [01/access-control](../../01-constraint/access-control/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 3 条（[findings](./findings.md)）+ 1 页对照（[compare](./compare.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 2 个（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-10 |
| 覆盖 | selective correction、ontology-in-context、ontology-free agentic navigation、OBDA 对照；不含 KG 构建、本体生成 |
| 来源 | GGC（新加坡 NTU/A*STAR）+ NLKGQ（德国 Max Planck）+ KGVoyager（美国 UT Arlington） |

## 当前判断

- **GGC：生成后选择性纠错。** MCQA（电影域、iMKG、31,570 题、Llama-3.2-3B 单骨干）上，`Query Acc.`（**答案集匹配率**）从 90.23%（Generator 单跑）到 98.33%（选择性纠错）；**全量纠错只有 92.34%**；45% 是相对全量纠错的墙钟，比单跑多约 10%；Gate FPR 0.31%、trigger 9.31%。`已核`（数字）/`推测`（跨域）。[F1](./findings.md)
- **NLKGQ：ontology 进上下文。** 完整 OWL ontology + system prompt + domain rider，单次调用零样本生成；DBLP-QuAD 3.1（1,000 题、作者修订的确定性参考）**89.9% Match / 81.3% Exact**；2.0 确定性协议 **57.6% / 20.1%**；wrapper + rewriter 在 3.1 上 +15.0 Match / +25.3 Exact。`已核`（单系统）/`推测`（跨域）。[F2](./findings.md)
- **KGVoyager：不依赖 ontology 的 agentic navigation。** 4 个领域 benchmark（394 题）× 4 骨干 × 3 次运行，平均 F1 **64.6% vs GRASP 60.9%（+3.7pp，不是 4×）**；成本 $2.43 vs $3.94（−38.3%）、墙钟 85.6s vs 112.4s（−23.8%）；只要 endpoint + lightweight class index。`已核`（数字）/`推测`（跨域）。[F3](./findings.md)
- **按资产条件选，不按总分排。** 四条路线（含 OBDA）在资产/规模/指标/成本上不可比；只能按「先有什么」分支。`推测`（综合）。[compare](./compare.md)

## 文件地图

| 想知道 | 去 |
|---|---|
| 三条路线怎么跑、各停在哪 | [mechanism](./mechanism.md) |
| F1–F3 的数字、条件、边界、来源 | [findings](./findings.md) |
| 按资产选路线、失败目录、不可比清单 | [compare](./compare.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始材料 | [GGC digest](../../../src/papers/2607.28082-ggc/digest.md) · [NLKGQ digest](../../../meta/audits/2026-11-11-source-purge.md#src-2609-14652) · [KGVoyager digest](../../../meta/audits/2026-11-11-source-purge.md#src-2609-01780) |

## 边界

- 不覆盖 **KG 构建**（05/representation）与 **本体生成**（05/generation）。
- 不覆盖 **OBDA / 查询重写**：那是 [E-20](../../conclusions.md) 与 02 R11 的机制面；“OBDA ≠ NL→query”是 04 的边界，不挂 E-20。
- 三条路线**没有头对头**：GGC 是生成后纠错、NLKGQ 是 ontology-in-context、KGVoyager 是 ontology-free navigation；数据集/指标/模型都不同。
- 不把 query-level accuracy 当业务正确率；GGC 没有 2×2 改对/改坏配对；NLKGQ 的 Match 允许 superset；KGVoyager 的 +3.7pp 不是 4×，且 4 个 benchmark 都小（88–108 题）。

## 关联

- 派：[03 知识](../README.md) · 本派 claims：[03-L12–L16](../claims.md)（仅 `03-L13`/GGC 仍 admitted；`03-L12/L14/L15/L16` 已随 NLKGQ/KGVoyager 移出标 `withdrawn`）
- 结论：[E-21](../../conclusions.md)（P1 新 E）；对照页：[compare](./compare.md)
- 卡片（provenance）：[GGC](../../../src/papers/2607.28082-ggc/card.md) · [NLKGQ](../../../meta/audits/2026-11-11-source-purge.md#src-2609-14652) · [KGVoyager](../../../meta/audits/2026-11-11-source-purge.md#src-2609-01780)
