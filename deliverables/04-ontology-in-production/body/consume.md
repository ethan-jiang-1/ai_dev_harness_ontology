---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# B · 用：KG 构建、Text2SPARQL、语义层

> 本章回答：本体建好后，怎么变成能被查的 KG/查询接口。 ｜ 读完你应该能：选 KG 构建 / Text2SPARQL / OBDA / 语义层，并写出查询契约。

## B.1 三条路，不要混

| 路线 | 做什么 | 什么时候用 | 不代表 |
|---|---|---|---|
| **KG 构建** | 文本 → 实体/关系/triples，按本体落图 | 有非结构化文本、需要结构化检索 | 抽取对 = 本体对 |
| **Text2SPARQL** | 自然语言 → SPARQL → 执行 | 已有 KG/本体、问题需要结构化查询 | execution accuracy = 业务正确 |
| **OBDA / 语义层** | 本体+映射 → SQL/virtual KG；agent 通过工具查 | 关系库稳定、想复用现有数据 | OBDA = NL→query |

## B.2 KG 构建：schema 先于抽取

外部信号（未入库，仅作旁证；不引旧数字）：

- [工业 KG](https://arxiv.org/abs/2609.31663)：法语电网事故报告，schema-guided prompting 的工程做法。
- [法律 KG](https://arxiv.org/abs/2607.24551)：法规本体 + 闭式抽取；predicate normalization 与 domain-range 校验是 refinement 重点。

**做法**：

1. 先定 schema slice（哪些类/关系/约束），不要全本体塞 prompt；
2. 抽取输出必须带 `subject/predicate/object`、source span、confidence；
3. 用本体做类型/domain/range 校验；不通过进人审，不静默丢；
4. 记录 `source_version/extractor_version`，支持重放。

## B.3 Text2SPARQL：瓶颈常在 grounding

**E-21（引）**：

- **GGC**：生成后选择性纠错；MCQA（电影域、单 KG、31,570 题、Llama-3.2-3B 单骨干）答案集匹配 **90.23%→98.33%**；全量纠错只到 92.34%；45% 是相对全量纠错的墙钟（比单跑 +10%）。
- **NLKGQ**：完整 OWL 放进单次上下文，零样本生成；DBLP-QuAD 3.1（单 snapshot、作者修订参考）**89.9% Match / 81.3% Exact**；Match 允许 superset。
- **KGVoyager**：不依赖 ontology/examples 的 agentic navigation；4 个小型 benchmark 平均 F1 **64.6 vs 60.9（+3.7pp，不是 4×）**；只要 endpoint + class index。

外部信号（未入库，仅作旁证）：SAGA、SchemaForge、Build2SPARQL、Researcher Agents。**不再引 CK25/SPARQL-LLM**。

**工程执行层候选**：Qlever（SPARQL 1.1 运行时；不做 OWL 推理；未入 E）。

**做法**：

1. 先做 schema slice，不做全库检索；
2. 维护类型状态（entity type / property domain-range / expected answer type）；
3. 生成 → 执行 → 空结果/错误 → **选择性纠错**（只改高风险 query，不要全改）；
4. 报 execution accuracy + 空结果率 + 纠错净收益；不要只报准确率。

## B.4 语义层 / OBDA / MCP

行业信号（厂商指南，不作效果依据）：

- [AWS 语义层指南](https://docs.aws.amazon.com/prescriptive-guidance/latest/semantic-layer-agentic-ai-ontology-reasoning-virtual-knowledge-graph/semantic-layer-agentic-ai-ontology-reasoning-virtual-knowledge-graph.html)：Data/Knowledge/Intelligence/Orchestration 四层；OBDA virtual KG；MCP/A2A；SHACL；human-in-the-loop governance。

**做法**：

1. 先判断数据在关系库还是 RDF：关系库稳定 → OBDA/virtual KG；RDF/事件 → KG 查询；
2. 给 agent 的工具面要小：`intent → schema slice → query → execute → verify`；
3. 工具返回必须带 `source/version/query`，否则不能审计；
4. 不要把“语义层”当“更懂业务的 prompt”；它是接口 + 映射 + 权限。

## B.5 查询契约

```text
request: {question, user_context, domain, budget}
schema_slice: {classes[], properties[], constraints[]}
query: {sparql|sql, parameters, expected_type}
result: {rows, empty_reason: coverage|query|data, latency}
verify: {executed, answer_type_ok, citations[], verdict}
```

**空结果要分因**：覆盖不足 / 查询写错 / 数据缺失；否则会把“schema 不够”误判成“模型不行”。

## B.6 验收

| 指标 | 工程建议（`推测`） | 数据 |
|---|---|---|
| execution accuracy | 自域 ≥0.8 起步 | 问题-SPARQL-答案 |
| 空结果率 | 按域设上限；分因 | query 日志 |
| schema 覆盖 | 目标 predicate 在 slice 内 | schema/query |
| 纠错净收益 | 改对 > 改坏 | 配对样本 |
| 延迟/token | 业务预算 | 账本 |

**E-21 的边界**：三条路线各一个单设置，没有头对头；自域 execution accuracy 仍要自己量，不能拿 98.33/89.9/64.6 当跨域基线。

## B.7 停 / 反模式

- schema 覆盖不足 → 先扩 schema，不加 agent；
- 空结果率高分不清原因 → 先修覆盖/查询；
- 纠错改坏正确 query → 收紧 gate；
- 用 execution accuracy 当业务正确率 → 停；
- 没有 `source/version` → 不可审计。

## B.8 不能证明

- benchmark 数字跨域可迁移；
- Text2SPARQL 能替代检索/人工；
- OBDA 能回答开放域问题；
- 语义层厂商架构能带来效果。
