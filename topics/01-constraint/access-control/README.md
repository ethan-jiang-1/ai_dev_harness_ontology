---
status: draft
updated: 2026-11-09
rq: [RQ2, RQ4]
evidence: [E-20]
---

# 访问控制：标签是输入，策略是空白，执行只有单实现

> 回答：敏感标签/分类从哪来、策略在哪判定、读路径在哪执行；不回答：动作前可逆性（[action-gate](../action-gate/README.md)）与落盘前授权契约（[commit-gate](../commit-gate/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 3 条（[findings](./findings.md)） |
| 未发现 / 开放 | 4 条（[frontier](./frontier.md)） |
| 下一步 | 2 个（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-09 |
| 覆盖 | 列级敏感性标签/分类、策略判定、读路径结果过滤、判定/审计；不含动作可逆性、写授权契约 |
| 来源 | Glyph（preprint，Apple 单企业）+ trustgraph（开源，pin `184f622`） |

## 当前判断

- **标签/分类是权限的输入，不是执行。** Glyph 在 Apple 单企业生产目录（~3.4M 列/98k 表、内部 275-leaf 本体、~72% `NON_SENSITIVE`）做列级敏感性标签：不读 cell value，三策略 + RRF(k=60) + sensitivity tier 重排，per-tag provenance；**不产策略判定、不执行访问控制**。`已核`（一手正文；生产部署为作者报告）/`推测`（跨企业）。[F1](./findings.md)
- **它的指标是检索/标签质量，不是授权正确性。** NDCG@10 0.5497→0.9225、MAP@100 0.1888→0.9009 是同一 stock MiniLM 微调前后的**检索**指标（9,242 query/83,229 corpus、10% 列级留出、同分布上界、未控表内泄漏）；端到端 F2 0.890 vs metadata-only 0.880（RRF 只 +0.010 F2 / −0.015 F1）。`已核`（数字与条件）。[F1](./findings.md)
- **执行层另有其物，且只有一个实现。** trustgraph 用 SHACL-AF post-filter 对查询结果做读路径过滤（pin `184f622`，31 条单测见 digest）；错误路径/方向性边界见 [commit-gate F5–F7](../commit-gate/findings.md)，本页不复述。`已核`（代码）。[F2](./findings.md)
- **策略层没有领域来源；OPA 是 adjunct 候选。** 没有 ontology/KG 来源回答标签怎么映射成策略、冲突怎么解、默认 allow/deny；OPA 只能提供通用 Rego 决策点，不解析 OWL/SHACL、不消费 Glyph 标签。`推测`（综合，负结果；缺的是领域来源，不是证明不存在）。[F3](./findings.md)

## 文件地图

| 想知道 | 去 |
|---|---|
| 五段链怎么跑、每个来源停在哪 | [mechanism](./mechanism.md) |
| F1–F3 的数字、条件、边界、来源 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 错误路径 / 对象方向 | [commit-gate F5–F7](../commit-gate/findings.md) |
| 原始材料 | [Glyph digest](../../../src/papers/2609.10430-glyph/digest.md) · [trustgraph digest](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) |

## 边界

- 不覆盖动作前可逆性/审批（[action-gate](../action-gate/README.md)）与落盘前授权契约（[commit-gate](../commit-gate/README.md)）。
- 不把「有标签」当「有策略」，不把「读路径过滤」当「写授权」，不把「检索指标」当「打标准确率」。
- `read-path` 仍是轴外位置（[E-20](../../conclusions.md)）；本页只做机制之家，不升第七时刻。
- 单企业、单实现、只读代码；无生产访问控制数据，无跨企业/OOD，无漏标率。

## 关联

- 派：[01 约束](../README.md) · 本派 claims：[01-L16–L18](../claims.md)
- 相邻：[commit-gate](../commit-gate/README.md) · [action-gate](../action-gate/README.md)
- 卡片（provenance）：[Glyph](../../../src/papers/2609.10430-glyph/card.md) · [trustgraph](../../../src/open-source/trustgraph-ai-trustgraph/card.md)
