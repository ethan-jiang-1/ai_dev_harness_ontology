---
status: draft
updated: 2026-11-08
rq: [RQ2, RQ4]
evidence: [E-03]
---

# 输出时证据契约

> 模型生成结论时。判定尚未发生，但输出格式已被约束：每个结论必须附带依据，以及依据与本体的关系强度。这里不负责输出后的 checker（[checker](../checker/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 3 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 2 个候选（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 输出时的证据/接地等级；不含输出后的 checker 与推理期约束 |

## 当前判断

- **显式接地等级整体最优。** 强制报告本体观察 + entailed/supported/related/unrelated，比只给文本 RAG 更可审计。`已核`
- **等级是模型自评，不是保证。** OA-RAG 自己写明「不提供形式正确性保证」；等级与正确率正相关，但未校准。`已核`
- **检索是主瓶颈。** gold evidence 完全检索 MCQ 61.7% vs OQ 23.6%；检索到后 MCQ 95.1–98.4% 被引用。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| 四个等级/为什么有用/失效 | [mechanism](./mechanism.md) |
| 三条判断的证据/数字 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | `src/papers/2610.36335-oa-rag/` · [digest](../../../src/papers/2610.36335-oa-rag/digest.md) |

## 边界

- **不是形式保证。** 等级是模型自评；不能当自动放行依据。
- **不是输出后判定。** 它约束输出的格式与证据声明；是否放行仍由 checker/人决定。
- **不解决检索覆盖。** 检索不到时，等级只能标 unrelated，不能补内容。

## 关联

- 派：[02 判定](../README.md) · 结论：[E-03](../../conclusions.md)
- 相邻：[checker](../checker/README.md) · [03 知识 projection](../../03-knowledge/projection/README.md)
- 成本：[06-measure/feasibility](../../06-measure/feasibility/README.md)
