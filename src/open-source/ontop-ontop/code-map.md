---
status: seed
updated: 2026-11-09
repo: ontop/ontop
commit: 964dbb79431fb958fce9de0784424f7c0e35f9bf
---

# ontop/ontop · 代码地图

> 只做定位：文件 / 符号 / 谁调用谁。不贴代码、不写判断；判断在 `digest.md`。
> 路径相对仓库根；commit `964dbb7`。

## 入口

| 入口 | 形态 | 说明 |
|---|---|---|
| `ontop`（CLI 5.5.0） | CLI | `query` / `validate` / `materialize` / `endpoint` / `bootstrap` |
| `engine/reformulation/core/.../QuestQueryProcessor` | 核心类 | SPARQL/KG 查询 → 重写 → 展开映射 → SQL |
| `client/...` | 客户端/API | 嵌入式/远程调用（未逐条读） |

## 本体 / 映射相关文件

| 文件 | 符号 | 作用 | 被谁调用 |
|---|---|---|---|
| `mapping/sql/r2rml/src/main/java/it/unibz/inf/ontop/spec/mapping/parser/impl/R2RMLMappingParser.java` | `parse(File)` | 解析 R2RML 映射 | CLI / 引擎启动 |
| `mapping/sql/r2rml/.../R2RMLToSQLPPTriplesMapConverter.java` | 转换器 | R2RML → SQLPP triples map | `R2RMLMappingParser` |
| `engine/reformulation/core/.../QuestQueryProcessor.java` | `reformulateIntoNativeQuery` | 查询重写主流程 | `QueryReformulator` |
| `.../QuestQueryProcessor.java` | `rewriter.setTBox(obdaSpecification.getSaturatedTBox())` | 用本体 TBox 做饱和/重写 | 构造时 |
| `engine/system/core/.../QuestStatement.java` | `QuestStatement` | 执行 native query / 结果转换 | 查询引擎 |

## 调用链

```
# CLI: ontop query -m mapping.ttl -t ontology.ttl -q query.rq -p db.properties
mapping.ttl + ontology.ttl
 → R2RMLMappingParser.parse → R2RMLToSQLPPTriplesMapConverter → SQLPPMapping
 → OBDASpecification（含 SaturatedTBox：本体公理先饱和）
 → KGQueryTranslator：SPARQL → KGQuery
 → QueryRewriter.rewrite：按 TBox 重写（子类/等价类等）
 → QueryUnfolder.optimize：按映射展开成 SQL 结构
 → GeneralStructuralAndSemanticIQOptimizer → QueryPlanner
 → NativeQueryGenerator：生成 SQL
 → QuestStatement：在 JDBC 上执行，结果转回 SPARQL 绑定
```

## 测试与示例

| 路径 | 覆盖什么 | 怎么跑 |
|---|---|---|
| `test/docker-tests/` | 多 DB/多映射/并行场景 | Docker（本机 daemon 未起） |
| `ontop validate` | 本体 + 映射一致性 | `ontop validate -m mapping.ttl -t ontology.ttl` |
| 本次最小示例（`/tmp/ontop-cli`） | H2 + R2RML + SPARQL | 见运行记录 |

## 运行记录（C2）

```bash
# 环境：Java 11；ontop-cli 5.5.0（GitHub release zip）；H2 2.2.224 驱动放进 jdbc/
java -cp jdbc/h2-2.2.224.jar org.h2.tools.Shell -url jdbc:h2:/tmp/ontopdb \
  -user sa -password "" -sql "CREATE TABLE PERSON(ID INT PRIMARY KEY, NAME VARCHAR(50)); INSERT ..."

./ontop query -m mapping.ttl -t ontology.ttl -q query.rq -p db.properties
# → p,name
#   http://example.org/person/1,Alice
#   http://example.org/person/2,Bob
# 日志：Ontop has completed the setup and it is ready for query answering!

./ontop validate -m mapping.ttl -t ontology.ttl -p db.properties
# → Validation completed
```

- 本体：`ontology.ttl`（`:Person`、`:name` domain/range）；映射：`mapping.ttl`（R2RML，`PERSON` 表）；查询：`?p a :Person ; :name ?name`。
- 未跑：Docker 测试套件（daemon 未启动）；大规模/并发/延迟。

## 未定位

- TBox 饱和的具体公理集（OWL 2 QL 支持范围）与「本体对结果的实际贡献」消融。
- `ontop endpoint` 的 HTTP/SPARQL 接口与 agent 工具封装。
- 查询重写日志（本次只看到结果，没开 debug 拿 SQL）。
