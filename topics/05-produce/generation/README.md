---
status: draft
updated: 2026-11-12
rq: [RQ2, RQ3]
evidence: []
---

# 生成：本体从哪来

> 多数本体文献默认本体已经存在；真实项目第一步往往是「造一个」。这里问「来源怎么影响可信度、生成物怎么被消费」，不负责精化（[refinement](../refinement/README.md)）。
>
> **2026-11-12 对账**：本页四篇来源 OntoDoc / ReX-GG / Peeling / Evontree（及 SFE-O）均已撤回（[黑名单](../../../meta/rules/excluded-sources.md)）。下列判断的数字/结论作**历史/机制参考，不作活证据**，原「已核」降 `推测`；「生成产出候选、可消费性未测」的问题意识保留，证据待新源。代码侧 semantica 消费路径（E-20）仍 admitted。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 7 条（[findings](./findings.md)） |
| 未发现 / 开放 | 6 条（[frontier](./frontier.md)） |
| 下一步 | N1–N4（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-09 |
| 覆盖 | 本体/说明的生成路线；不含精化、表示、生命周期 |

## 当前判断

- **生成产出候选，不是完备本体。** 四篇都没有验证生成物能被下游判定器/agent 消费：OntoDoc 只测描述四维，ReX-GG 只测用户感知，Peeling 只测 DAG 结构，Evontree 是训练侧注入。**代码侧已有消费路径**（semantica：ontology → SHACL → pyshacl，F7），但只证明管线能跑，不证明生成物可消费。`推测`（「四篇均未测下游」`推测`）
- **先写 assumptions 再写描述，提升完整性。** OntoDoc：win 54–61%（LLM judge 偏好消融），completeness 3.43→3.84；没有下游任务；DBpedia 上 naive 的 accuracy/clarity 反而更高。`推测`（限 OntoDoc；人工 11 人只评 OntoDoc、无 baseline 盲评）
- **可消费性评估缺失。** 判定器能否加载/解释/复现生成结构，四条路线都没有测；工程侧已有跑通的消费链路（semantica，F7），但质量/覆盖仍未测。`推测`（缺口，限四篇）
- **四条路线各有可核边界，但没有跨路线排序。** 专家手工（SFE-O）的瓶颈在执行/集成（数值不在 OWL 求解、约束未落 SHACL 只是文档）；LLM 路线里 OntoDoc 只产出说明、不测下游，ReX 的本体只当标签表（4 种关系）、不参与判定；表征挖掘只在 MRL 嵌入上；规则自演化要 15 个种子且只覆盖 subclass/synonym。`推测`（分项）／把来源排成「谁更窄、谁更漂」是 `推测`
- **训练侧注入：explicit 掉点可核，implicit/mix 增益只到报告值。** Evontree 报告的 +3.1/+3.7 与 +0.9/+1.1 仅按报告值引用；digest Table 3 的均值与 Δ 行不可复算（Llama3 mix 均值 61.0 反而低于 raw 62.5），两者都不得当净增益或相对百分比（F6 的 `存疑`）。explicit 模板注入在 QA 与安全面都掉；implicit/mix 报告无显著安全下降。`推测`（explicit 掉点，限 Evontree；两模型单域自评）／`存疑`（implicit/mix 增益，仅报告值）
- **来源字段是 E3 建议，来源权重没有测过。** `provenance_triples`/`generator_version`/`evidence_span` 出自 digest 的工程配方（E3），不是论文报告的产物字段（`推测`）；论文侧只有 OntoDoc 的 assumption 引用 triple 编号、ReX 的匿名互评隐藏模型名、Evontree 的 `ConfirmValue` 分级。没有一篇测过按生成者身份加权；「判定器不知道约束是谁写的」`推测`。

## 文件地图

| 想知道 | 去 |
|---|---|
| 四条路线怎么跑、证据、失效模式 | [mechanism](./mechanism.md) |
| 接口/参数/成本/stop/客户指标（从 digest 吸收的 4 条工程发现；schema 是 E3 建议、成本/收益决策框架是 E4，均非论文产物） | [mechanism](./mechanism.md)「工程发现 1–4」（接口、参数、成本、stop 与客户指标） |
| F1–F7 的证据/等级/边界 | [findings](./findings.md) |
| 还缺什么、下一步 | [frontier](./frontier.md) |
| 原始论文 | [OntoDoc digest](../../../meta/audits/2026-11-11-source-purge.md#src-2611-01276) · [ReX-GG digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-41901) · [Peeling digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-41785) · [Evontree digest](../../../meta/audits/2026-11-11-source-purge.md#src-2510-26683) · [SFE-O digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37123) |
| 研究提示词与输出 | [prompt.md](./prompt.md)；run 记在 `runs/`（有 prompt 才建） |

## 边界

- **不保证可消费。** 说明/结构生成后，判定器能否加载未测（F1/F3）。
- **不保证来源可信。** 四篇没有报告带来源权重的成品 schema；`provenance_triples`/`generator_version`/`evidence_span` 是 E3 建议（`推测`），按来源加权没有测过（F5）。
- **不解决维护。** 增量重生成只有 OntoDoc 明确未实现；同步/版本管理在 [lifecycle](../lifecycle/README.md)。
- **不做路线排名。** 四条路线证据强度不同，跨路线同口径比较不存在（F4）。

## 关联

- 派：[05 生产](../README.md) · 本派结论：[05-L3 / 05-L7](../claims.md)（生成/可消费性缺口暂无直接 `E-xx`）
- 相邻：[refinement](../refinement/README.md) · [representation](../representation/README.md)
- 判定：[02 checker](../../02-judgment/checker/README.md)
