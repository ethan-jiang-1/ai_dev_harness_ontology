---
status: draft
updated: 2026-11-07
rq: [RQ2, RQ3]
---

# 05 生产派 · 前沿与挖掘

> 活页。稳定判断见 [README](./README.md)；证据见 [notes](../../notes/)；时刻位置见 [seams](../seams.md#六个时刻)。

## 这一派现在的前沿问题

1. **精化能否产品化**：给定一个本体和一批下游错误，自动定位该修哪条子类关系？
2. **来源标记如何进入判定权重**，而不让判定变得不可解释？
3. **本体是否需要“测试”**：一组必须成立/必须不成立的事实对，能不能当回归测试？
4. **生成本体的评估**：除了完整性 +12%，怎么测“可消费性”（下游判定器能不能加载/使用）？
5. **表示形式按消费位置选**：第二档（结构表）能否覆盖大多数判定场景？

## 信号源

- **会议/期刊**：ISWC、ESWC、K-CAP、JIST；ACL/EMNLP 的 ontology generation 线。
- **标准/工具**：OWL 2、SHACL、SPARQL、ontology testing 工具。
- **领域本体**：工业设备（SFE-O）、生物医学/农业 KG（OntoDoc）、金融/电网。
- **实验室/团队**：CASTON、OntoDoc、Peeling、Evontree、ReX-GG。
- **arXiv**：cs.AI / cs.CL / cs.DB / cs.LG。

## 检索式

- `ontology refinement LLM embedding`
- `ontology generation evaluation LLM`
- `SHACL constraints LLM agent`
- `ontology learning from embeddings`
- `ontology source provenance trust`

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| CASTON（2610.21466） | 精化路线；专家判定全部正确，但规模小 | 已入档 | 找后续/可复现实现 |
| SFE-O（2610.37123） | 参数溯源建进本体；表示≠执行 | 已入档 | 拆“执行缺口”清单 |
| OntoDoc（2611.01276） | 为任意 IRI 生成说明；151 术语 | 已入档 | 看“可消费性”有没有测 |
| Peeling（2610.41785） | 从嵌入抽层级；未测下游 | 已入档 | 找下游效用 follow-up |
| Evontree（2510.26683） | 规则引导自演化；需人工种子 | 已入档 | 看“人工种子”成本 |
| 本体测试线 | 必须成立/不成立的事实对 | 待扫描 | 用检索式 2/3 |

## 入档判据

- 报告 **精化精度、下游可用性、来源元数据** 中的至少一个。
- 给出可复现的本体/约束，而不只是生成文本。
- 会改变 05 的“来源决定可信度”或“表示不是瓶颈，执行才是”。

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-07 | 本地 20 篇复筛 | CASTON 规模小；SFE-O 执行缺口；Peeling 未测下游 | 三条进候选队列头 |

## 本轮计划

1. 用检索式 1/2 找 2026 年的本体精化/生成评估 follow-up。
2. 读 SFE-O 正文，抽“OWL 能表达但跑不起来”的具体缺口。
3. 起草一个“本体测试”模板：必须成立 / 必须不成立 / 待定。
