---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# A · 建：从契约到 `build_report`

## A.1 消费者契约（产物）

五格写不出就停；本 fixture（[example](../example/README.md)）：

| consumer | principal | moment | answers / refuses | load |
|---|---|---|---|---|
| UI | steward | 页面加载 | 答 Email 列；不拒 | SPARQL endpoint |
| agent | steward | 查询时 | 答 4 表/7 列；不拒 | SPARQL endpoint |
| governance | analyst | 夜间 | 答未打标数据集（4）；拒 level ≥3 列 | SPARQL endpoint |

tag 是 `:Email` 等类的实例，CQ1 用 `?t a/rdfs:subClassOf*`；拒绝单位 = 列（triple subject）。

### CQ 只是模板词：须在契约行可执行

①`?col :hasTag ?t . ?t a/rdfs:subClassOf* :Email`（UI）；②`sensitivityLevel ≥ 3` + `columnOfTable` 反查（agent）；③`FILTER NOT EXISTS { ?col :hasTag ?t }`（治理）。

依据：T:05/representation 机制/建模 · 模板 · gap（无 CQ）

## A.2 表示档位：按消费者选

词表够注入；结构表够判定器；逻辑表只推隐含分类。

本例选结构表（`推测`）：三条契约无隐含分类。**薄层优先**：命名单位（K0→K1）+54.6pp（占 74.4pp 的 73.4%），再加 +19.8pp（26.6%，`O-F14`）。

依据：T:05/representation · E-12/O-F14 · 推测

## A.3 最小本体（11 类 / 5 属性）

只建契约用得到的；等级挂 `Tag`，不挂 `Column`。

TBox：[ontology.ttl](../example/ontology.ttl)（11 类/5 属性；计数 `?c rdfs:subClassOf* :Tag` 8 + 3 = 11）；ABox：[catalog.ttl](../example/catalog.ttl)。

**标签层独立**：Glyph 275 叶标签，不产策略、不执行（`E-22`/F1）。

依据：T:01/access-control F1 · E-22/O-N28 · E-12/O-F14 · 模板

## A.4 约束与负例（产物：shape + 负例表）

每条约束=shape/检查 + 已知违反 + 干净样本。

Shapes：[shapes.ttl](../example/shapes.ttl)（2 条：TagHasLevel、HasTagClass）。

| 约束 | 检查 | 已知违反 | 干净样本 |
|---|---|---|---|
| Tag 有整数等级 | `TagHasLevel` | `tag_unknown` 缺等级 | `tag_email_1` |
| hasTag 非字面量 | `sh:nodeKind sh:IRI` | `col_legacy` 指字面量 | `col_email`→Email |
| 未打标可发现（CQ3，不是 shape） | `FILTER NOT EXISTS` | `col_new` 无 tag | `col_email` |

SFE-O 未交付可执行 shape，只借做法。分开报：违反检出/干净样本误报/人审接受率；`E-02` catch/FA = 18.9/16.8、8.2/3.5、5.0/1.8；PPV 复算见 `O-F08`。

依据：T:05/representation · S:SFE-O §4.1 · E-02/O-F08 · gap

## A.5 可消费性闸门（产物：`build_report`）

`load(artifact) → {parsed, violations, missing_fields}` + 一次真实任务。

load = rdflib 解析 [ontology.ttl](../example/ontology.ttl)/[shapes.ttl](../example/shapes.ttl)/[catalog.ttl](../example/catalog.ttl) + pyshacl；`parsed`=语法/前缀，`violations`=shape，`missing_fields`=必填；真实任务=CQ1 返回 2。

```json
{"_note":"模板+示例","load":{"parsed":true,"violations":2,"missing_fields":[]},"classes":11,"properties":5,"policy_version":"0.3.0","tag_version":"0.1.0","provenance":{"source":"synthetic"}}
```

**交接**：`load/violations`→B；`query_id`→C.4/`policy_version`→A.5。

**停**：`violations` ≠ 已声明坏样本数（2）或落在已知清单外；无契约/`load`；无版本/来源；下游不加载。

依据：T:05/generation · T:05/representation（stop 1–7）· 模板 · gap

## A.6 证据边界

build 无 in-scope 证据；数字只引 E/O 或标「示例」。

依据：T:05/representation · T:05/generation · S:SFE-O/Catch/N&D/Glyph
