---
status: draft
updated: 2026-11-09
parent: ../README.md
basis: E-20；execution-forms 代码核对；semantica / open-ontologies / ontop digest
---

# R10–R11 · 离线校验与 OBDA：不在回路里的执行

> 这两条不在 agent 控制回路里，但它们是 01 里少数被评为 **A（可先落地）** 的能力。它们不改变模型走向，改变的是**数据/查询的可靠性**与**验证的时机**。
>
> 别把它们叫「闸门」：R10 是离线/CI 检查，R11 是查询编译；两者都不能替代 R5/R6/R9。

## 0. 先选哪一条

| 你的问题 | 选 | 不要选 |
|---|---|---|
| 数据入库/发布前要查 SHACL，CI 要有通过/违反/没检查完 | R10 | R5 的 in-loop checker |
| 本体 + 关系库 + 映射，想用 SPARQL 查关系库 | R11 | R10 的 shapes 校验 |
| 需要「本体一变，查询结果就变」 | R11 | R10 只校验数据 |
| 需要「为什么允许写」 | 都不行 | 走 R9（设计） |

---

## R10 · 离线/CI SHACL：把「没检查完」做成第三态

### 目标

在数据入库、发布、CI 合入前，用本体派生的 SHACL 检查数据；把「通过/违反/没检查完」显式化，避免把「没查」算成「查过且通过」。

### 适用 / 不适用

| 适用 | 不适用 |
|---|---|
| 数据发布/ETL/CI 门 | agent 输出后的自动拒收（R5） |
| 有本体 + 能派生/手写 SHACL | 需要 OWL 推理/子类展开 |
| 能接受 CLI/批处理时延 | 需要单次写授权（R9） |
| 需要变更影响报告 | 需要「对象方向可见性」（R8） |

### 前提

- RDF/OWL 数据 + SHACL shapes（手写或从本体派生）。
- 能跑 pyshacl/Oxigraph 或等价求值器。
- 有负例集：已知违反、干净数据、未覆盖约束。
- 能记录 checked/passed/undetermined。

### 接缝 / 形态

`checker` / `compiled` 或 `engine`；位置是**离线/CI**，不是 in-loop。semantica 是 CLI 校验；open-ontologies 是工具面/CI 规则门。

### 最小数据契约

**派生**：

```text
to_shacl(ontology, quality_tier?, target_namespace?) → shapes
```

**校验**：

```text
validate_graph(data, shacl) → {
  conforms: true|false|null,
  violations: [{focus_node, path, constraint, severity, message, source}],
  checked: n, passed: n, undetermined: n
}
```

**变更影响**（open-ontologies）：

```text
closure_diff → {entailments_lost, lost_by_warrant,
                monotonicity_violations, skipped, exit_code}
```

### 做法

1. **先写负例**：已知违反、干净数据、未覆盖约束各一组；没有负例的 shape 不算验收。
2. **派生或手写 shapes**：semantica 的 `OntologyEngine.to_shacl` 可把本体转成 shapes；派生结果要人工审。
3. **跑两条路径**（若用 open-ontologies）：
   - 默认 SHACL：支持 `sh:sparql`，但会 skip 不支持的约束。
   - verified：覆盖 SHACL Core，拒绝 `sh:sparql`/自定义组件（120 条里 22 条）。
4. **三态输出**：`conforms:true` / `false` / `null` + `undetermined`；不要只看 shell exit code（外层会把 `null` 映射成 exit 2，与解析失败同码）。
5. **CI 门**：`conforms:false` 或 `undetermined` 按策略阻断；`undetermined` 不能当 pass。
6. **变更影响**：本体/shapes 变更时跑 `closure_diff`，把 entailment loss/跳过项写进报告。

### 证据

- semantica `to_shacl`：小本体派生 **1,729 字符 / 54ms**；`validate_graph` 能返回结构化 violation；`inference="none"`，不展开子类（E-20；semantica digest）。
- open-ontologies：默认 `ShaclValidator` 把 SHACL 编译成 SPARQL 交 Oxigraph；`--verified` 走 `oo-shacl`，exit 3 = undetermined；但**本次未跑通**（网络/工具链阻塞；quality C）。
- 三态在 JSON 保留（`conforms:null` + `undetermined`），在 shell 退出码被折叠（execution-forms 代码核对）。
- **不能证明**：派生 shapes 正确；catch/FA 未测；CLI 不在 agent 回路；不能替代手写 shapes；不能当写授权。

### 成本

| 项 | 量级 | 等级 |
|---|---|---|
| 本体→shapes 派生 | 小本体 54ms；大本体未测 | 已核（小样本） |
| pyshacl 校验 | 随图规模；未测 | 未知 |
| 依赖 | numpy/scipy/pydantic；不适合轻量工具 | 已核（代码） |
| CI 集成 | 按流水线；未测 | 未知 |

### 验收 / 停

| 指标 | 通过线 | 停 |
|---|---|---|
| 负例 | 已知违反全标红；干净数据误报 ≤5%（工程建议） | 负例不过 → 不发布 |
| 三态 | checked/passed/undetermined 都报 | 只报 pass/fail → 不可比 |
| 覆盖 | 明确哪些约束被 skip/拒绝 | 不说明覆盖 → 不能当保证 |
| 用途 | 离线/CI | 需要 in-loop 自动拒收 → 用 R5 |
| 语义 | 只查结构/声明/模式 | 需要语义正确 → 用 R5 judge/人工 |

### 失效模式

- **把 SHACL 通过当语义正确。** 结构检查抓不到 changes of meaning；`inference=none` 不展开子类。
- **派生 shapes 过度/不足。** 派生错误会静默变成「检查通过」。
- **只看 `conforms`。** 默认路径会 skip；verified 路径会 undetermined；两者都要求调用方正确解释。
- **把 CLI 当 in-loop。** 没有输出后自动校验/拒绝/重试策略；要自己接。
- **把影响报告当授权。** `closure_diff` 只报告影响，不做单次写授权。

### 可抄锚点

- [semantica digest](../../../src/open-source/semantica-agi-semantica/digest.md) 的 `to_shacl`/`validate_graph`、`inference="none"`、依赖成本。
- [open-ontologies digest](../../../src/open-source/fabio-rovai-open-ontologies/digest.md) 的三态、verified/Core 边界、`closure_diff`。
- 不要抄「verified 覆盖全量 SHACL」；它拒绝 `sh:sparql`（22/120）。

---

## R11 · OBDA 查询重写：本体在查询编译时被执行

### 目标

把本体 + R2RML 映射 + 关系库编译成 SQL；让 SPARQL 查询在本体层写，执行落在关系库。本体在这里的角色是**查询编译的一部分**，不是判定器。

### 适用 / 不适用

| 适用 | 不适用 |
|---|---|
| OWL 2 QL 本体 + 稳定关系库 schema | 需要 DL 推理/一致性检查 |
| 有 R2RML 映射，能维护 | 没有稳定 schema；映射频繁变 |
| 查询多、想复用关系库 | 需要事务写入 |
| 能接受查询重写时延 | 需要「本体独立贡献」的效应量 |

### 前提

- 关系库 + R2RML 映射 + OWL 2 QL 本体。
- 能跑 ontop CLI 或嵌入式 API。
- 能保存生成的 SQL/查询计划（debug 日志）。
- 有「去掉本体公理」的对照计划（否则无法归因）。

### 接缝 / 形态

`supply`（轴外）/ `engine`。ontop 构造时 `rewriter.setTBox(saturatedTBox)`，`reformulateIntoNativeQuery` 做 rewrite → unfold → SQL；`QuestStatement` 执行。它不是 gate，不校验输出。

### 最小数据契约

```text
ontology.ttl   # OWL 2 QL
mapping.ttl    # R2RML
query.rq       # SPARQL
db.properties  # JDBC

CLI: ontop query -m mapping.ttl -t ontology.ttl -q query.rq -p db.properties
     ontop validate -m mapping.ttl -t ontology.ttl -p db.properties
```

**对 agent 的接口**：包成 `sparql_query(query)` 工具；输入 SPARQL，输出 bindings；错误要可读（映射/QL 超界/连接失败）。

### 做法

1. **先 validate**：映射与本体一致性；能抓一部分映射错误。
2. **跑最小查询**：确认 rewrite → SQL → 结果；打开 debug 日志保存一条生成的 SQL。
3. **包成工具**：给 agent 一个 SPARQL 工具；限制 query 复杂度/超时；记录 SQL/行数/时延。
4. **做消融**：同一查询，去掉本体公理/只靠映射，比较结果/时延；没有消融，不能声称「本体贡献」。
5. **版本化**：本体/映射/DB schema 变更 → 重跑 validate + 回归查询。

### 证据

- ontop `QuestQueryProcessor` 构造时 `rewriter.setTBox(saturatedTBox)`；`reformulateIntoNativeQuery` 做 rewrite → unfold → SQL；`QuestStatement` 执行（E-20；ontop digest）。
- 最小示例跑通：H2 `PERSON(ID, NAME)` + `ontology.ttl` + `mapping.ttl` + `query.rq`，`ontop query` 返回两行；`ontop validate` 通过。
- **不能证明**：本体有独立贡献（只靠映射也能查出 `:Person`/`:name`，无消融）；适合 agent 回路（无 in-loop/延迟/并发）；支持完整 OWL（只 OWL 2 QL）；查询重写正确（没看 SQL）；解决知识过期（本体/映射版本管理不在它这里）。

### 成本

| 项 | 量级 | 等级 |
|---|---|---|
| 关系库 + R2RML 映射 + 本体维护 | 在用户侧；未测 | 未知 |
| 查询重写 + SQL 执行 | 小示例秒级；大规模未测 | 已核（小样本） |
| agent 集成 | 未测 | 未知 |

### 验收 / 停

| 指标 | 通过线 | 停 |
|---|---|---|
| validate | 通过；映射/本体一致 | 失败 → 先修映射/本体 |
| 查询结果 | 与手写 SQL/基线一致 | 不一致 → 先查重写 |
| 时延 | 业务可接受 | 超预算 → 不包成在线工具 |
| 消融 | 有/无本体公理的差异可解释 | 没有 → 不声称本体贡献 |
| 用途 | 查询回答 | 需要判定/授权/事务写入 → 停 |

### 失效模式

- **映射与本体不一致。** `validate` 能抓一部分；抓不到的会在查询时错。
- **超出 QL 的公理被忽略/拒绝。** 只支持 OWL 2 QL；DL 推理不是它的职责。
- **SQL 生成不优。** 复杂映射/子类/等价类边界未测。
- **把 OBDA 当闸/判定器。** 它只改变「能查到什么」。
- **没有消融就归因。** 只靠映射也能查出同样结果；不能把「能查」当「本体有效」。

### 可抄锚点

- [ontop digest](../../../src/open-source/ontop-ontop/digest.md) 的调用链、CLI、工程含义、不能证明什么。
- 只抄「TBox 饱和 + 查询重写」的接口与边界；不要抄「本体有效果」。

**出处**：[execution-forms 代码核对](../../../topics/execution-forms.md#代码级核对2026-11-09) · [semantica digest](../../../src/open-source/semantica-agi-semantica/digest.md) · [open-ontologies digest](../../../src/open-source/fabio-rovai-open-ontologies/digest.md) · [ontop digest](../../../src/open-source/ontop-ontop/digest.md)
