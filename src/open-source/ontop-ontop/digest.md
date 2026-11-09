---
status: draft
updated: 2026-11-09
quality: B
based_on: card.md
commit: 964dbb79431fb958fce9de0784424f7c0e35f9bf
claims: []
---

# ontop：本体在查询重写时被执行，而不是在输出后判定

> **自包含**：不假设读者读过 README、card 或论文。代码位置写到 `文件:类/方法`，不贴大段代码。
> **证据等级**（四档）：
> - `已核`：读过代码，能指到文件/函数；或读过一手文档原文。
> - `已证`：不仅跑通，且能用 `EXP-xxx` 在本仓库外复现；**跑通示例不等于机制有效**。
> - `推测`：只读 README/文档/issue，没有代码定位。
> - `存疑`：README 与代码/issue 冲突，或核心闭源。
> `reading: 未读` 指还没通读代码；本页证据来自调用链阅读 + 最小运行。

## 0. 三句话

1. **它是什么**：Ontop 是 OBDA/虚拟知识图引擎（Apache-2.0，2013 年起）：数据库不动，本体 + R2RML 映射把关系库「暴露成」知识图。
2. **本体怎么被用**：**查询重写时执行**。SPARQL 先经 TBox 饱和/重写（`rewriter.setTBox(getSaturatedTBox())`），再按映射展开成 SQL；不是校验、也不是提示词。
3. **证据到哪**：CLI 最小链路跑通（H2 + R2RML + SPARQL → Alice/Bob），`ontop validate` 通过；没有延迟/规模/agent 集成证据（`已核` 代码与运行，`推测` 效果）。

## 1. 项目与维护状态

- 仓库：`ontop/ontop`，Apache-2.0，本次 pin `964dbb79`；release 5.5.0。
- 规模：1,016★；2013-07 起，2026-11-04 仍在推送；Free University of Bozen-Bolzano + Ontopic 维护。
- 结构：`engine/`（重写/优化/执行）、`mapping/`（R2RML/OBDA 解析）、`client/`、`test/docker-tests/`。
- 与本研究的关系：它是「本体被执行」的**供给型**极端案例——执行发生在查询编译，不发生在输出判定。

## 2. 本体在哪

| 形态 | 位置 | 格式 | 谁提供 | 用途 |
|---|---|---|---|---|
| 本体 | 用户文件（本示例 `ontology.ttl`） | OWL 2 QL（Turtle 等） | 用户 | TBox 饱和 + 查询重写 |
| 映射 | 用户文件（本示例 `mapping.ttl`） | R2RML / OBDA | 用户 | 关系表 → RDF 三元组 |
| 解析 | `mapping/sql/r2rml/.../R2RMLMappingParser.java` | Java | 引擎 | R2RML → `SQLPPMapping` |
| 饱和 TBox | `OBDASpecification.getSaturatedTBox()` | 内存 | 引擎 | 重写用 |

**关键**：仓库不自带领域本体；本体是**用户资产**。Ontop 的贡献是「把本体 + 映射编译成 SQL」的执行器。

## 3. 调用链

```
ontop query -m mapping.ttl -t ontology.ttl -q query.rq -p db.properties
 → R2RMLMappingParser.parse(file)
     → R2RMLToSQLPPTriplesMapConverter → SQLPPMapping
 → OBDASpecification（SaturatedTBox：本体公理先饱和）
 → KGQueryTranslator：SPARQL → KGQuery
 → QuestQueryProcessor.reformulateIntoNativeQuery
     → QueryRewriter.rewrite（按 TBox）
     → QueryUnfolder.optimize（按映射展开）
     → 结构/语义优化 → QueryPlanner → NativeQueryGenerator（SQL）
 → QuestStatement 在 JDBC 上执行；结果转回 SPARQL 绑定
```

关键点（可核对）：

- **本体在构造期就进重写器**：`QuestQueryProcessor` 构造时 `rewriter.setTBox(obdaSpecification.getSaturatedTBox())`。
- **重写与展开分离**：`rewrite` 管 TBox 蕴含，`QueryUnfolder` 管映射展开；两者都在生成 SQL 之前。
- `ontop validate` 只做本体+映射校验，不需要查询。
- **2026-11-09 代码核对（pin `964dbb7`）**：`QuestQueryProcessor.java:31` 类、构造器 `rewriter.setTBox(getSaturatedTBox())`、`:79` `reformulateIntoNativeQuery`；`QuestStatement.java:131` 调用执行。

## 4. 接缝判定

| 条件 | 是否成立 | 证据 |
|---|---|---|
| 有外部判据（来自本体，不是模型自评） | **不适用** | 它不是判定，是查询回答 |
| 有阻断能力 | **不成立** | 不拦任何东西；只改变「能查到什么」 |
| 位置明确 | **成立，但不是六时刻** | 位置是「查询编译」，在检索/供给层 |

**结论**：它**不是接缝**，是**供给层的执行器**。硬要归类，最接近 03 知识派的「按需供给」，但现有子主题（compilation/projection）都不覆盖 OBDA：compilation 是预编译文档，OBDA 是查询时编译。

## 5. 证据与最小复现

**环境**：Java 11；ontop-cli 5.5.0（GitHub release zip）；H2 2.2.224 驱动放入 `jdbc/`（Docker daemon 未启动，改用本地 CLI）。

**准备**：H2 建 `PERSON(ID, NAME)` 两行；`ontology.ttl` 定义 `:Person` / `:name`；`mapping.ttl` 用 R2RML 把 `PERSON` 映射成 `:Person` + `:name`；`query.rq` 查 `?p a :Person ; :name ?name`。

**运行**：

```bash
./ontop query -m mapping.ttl -t ontology.ttl -q query.rq -p db.properties
# p,name
# http://example.org/person/1,Alice
# http://example.org/person/2,Bob
# log: Ontop has completed the setup and it is ready for query answering!
./ontop validate -m mapping.ttl -t ontology.ttl -p db.properties
# Validation completed
```

**quality: B 的理由**：真实执行链路 + 可复现示例 + 代码定位；但没有基准/规模/agent 集成，也没有「本体 vs 无本体」的消融。

## 6. 不能证明什么

1. **不能证明本体有独立贡献**：这个示例里，仅靠映射也能查出 `:Person`/`:name`；没有「去掉本体公理后结果如何变化」的消融。
2. **不能证明适合 agent 回路**：没有 in-loop 调用、没有延迟/并发数据；`ontop endpoint` 的 HTTP 接口未测。
3. **不能证明支持完整 OWL**：只支持 OWL 2 QL profile；DL 推理/一致性检查不是它的职责。
4. **不能证明查询重写正确**：只看到结果对，没看生成的 SQL；复杂映射/子类/等价类的边界未测。
5. **不能证明 star/机构背书等于采用**：1,016★ 与学术背景是影响力信号，不是效果。
6. **不能证明它解决「知识过期」**：虚拟图跟随数据库，但本体/映射的版本管理不在它这里。

## 7. 与论文 digest 对照

| digest | 论文机制 | 代码里对应 | 缺什么 / 差异 |
|---|---|---|---|
| [CAI](../../../src/papers/2610.41172-context-as-infrastructure/digest.md) | 预编译上下文，按需检索省 token | **形态相反**：OBDA 查询时编译，不预存语料；共同点是「把整理成本前移/结构化」 | 没有 token/预算测量；不是上下文编译 |
| [Narrow & Deep](../../../src/papers/2610.11768-narrow-and-deep/digest.md) | 把领域知识投影成可读结构 | 投影的是「查询接口」，不是文本 | 没有可读性/避坑测量 |

**一句话**：它证明「本体可以作为查询编译的一部分被执行」，但不证明这种执行对 agent 的任务表现有增益。

## 8. 工程含义

- **接口**：CLI（`query`/`validate`/`materialize`/`endpoint`）；嵌入式 API 未读；对 agent 最自然的是把它包成 SPARQL 工具。
- **数据**：需要关系库 + R2RML 映射 + OWL 2 QL 本体；三者的维护成本都在用户侧。
- **成本**：查询重写 + SQL 执行；小示例秒级；大规模/复杂映射未测。
- **失败模式**：映射与本体不一致（`validate` 能抓一部分）、超出 QL 的公理被忽略/拒绝、SQL 生成不优。
- **什么时候别用**：需要 DL 推理、需要事务写入、没有稳定关系库 schema 时。

## 9. 代码地图

见同目录 [`code-map.md`](./code-map.md)：入口、本体/映射符号、调用链、运行记录、未定位项。

## 10. 下一步

- **G**：把 Ontop 包成 LLM 的 SPARQL 工具，测「有/无本体公理」的查询差异（消融），再判断它是否值得进 03 的子主题。
- 打开 debug 日志，保存一条生成的 SQL，作为「重写真的发生」的直接证据。
- 回 topics：03 派 frontier 加候选；不改 claims（没有改变判断）。
