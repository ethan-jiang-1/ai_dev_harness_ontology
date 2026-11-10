---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# A · 建：从契约到 `build_report`

> 本章的决定：**契约写不出，就不建；三关没过，就不算可消费。**
> 三关 = load / validate / answer；详细判据与 10 个坏样本见 [consumability](../../../topics/05-produce/representation/consumability.md)。

## A.1 消费者契约（产物）

五格写不出就停；本 fixture（[example](../example/README.md)）：

| consumer | principal | moment | answers / refuses | load |
|---|---|---|---|---|
| UI | steward | 页面加载 | 答 Email 列；不拒 | SPARQL endpoint |
| agent | steward | 查询时 | 答 4 表/7 列；不拒 | SPARQL endpoint |
| governance | analyst | 夜间 | 答未打标数据集（4）；拒 level ≥3 列 | SPARQL endpoint |

tag 是 `:Email` 等类的实例，CQ1 用 `?t a/rdfs:subClassOf*`；拒绝单位 = 列（triple subject）。

**契约字段与 `build_report` 不是一一对应**：report 只覆盖 `load`，且语义从「怎么加载」漂移成「加载结果」；`violations` ≠ `refuses`，`missing_fields` ≠ 契约缺字段。六项覆盖见 [consumability §3](../../../topics/05-produce/representation/consumability.md)。

### CQ 只是模板词：须在契约行可执行

①`?col :hasTag ?t . ?t a/rdfs:subClassOf* :Email`（UI）；②`sensitivityLevel ≥ 3` + `columnOfTable` 反查（agent）；③`FILTER NOT EXISTS { ?col :hasTag ?t }`（治理）。

依据：T:05/representation 机制/建模 · 工程产物 · 未测（无 CQ）；[consumability §3](../../../topics/05-produce/representation/consumability.md)

## A.2 表示档位：按消费者选

词表够注入；结构表够判定器；逻辑表只推隐含分类。

本例选结构表（`推测`）：三条契约无隐含分类。**薄层优先**：命名单位（K0→K1）+54.6pp（占 74.4pp 的 73.4%），再加 +19.8pp（26.6%，`O-F14`）。

三档 × 四位置矩阵见 [consumability §2](../../../topics/05-produce/representation/consumability.md)：结构表是唯一三关都 `supported` 的档；词表 validate/explain 弱；逻辑表 explain 无可移植路径。这是能力矩阵，不是效应量；E-12 的 +54.6pp 不是三档对照。

依据：T:05/representation · E-12/O-F14 · 推测

## A.3 最小本体（11 类 / 5 属性）

只建契约用得到的；等级挂 `Tag`，不挂 `Column`。

TBox：[ontology.ttl](../example/ontology.ttl)（11 类/5 属性；计数 `?c rdfs:subClassOf* :Tag` 8 + 3 = 11）；ABox：[catalog.ttl](../example/catalog.ttl)。

**标签层独立**：Glyph 275 叶标签，不产策略、不执行（`E-22`/F1）。

依据：T:01/access-control F1 · E-22/O-N28 · E-12/O-F14 · 工程产物

## A.4 约束与负例（产物：shape + 负例表）

每条约束 = shape/检查 + 已知违反 + 干净样本。

Shapes：[shapes.ttl](../example/shapes.ttl)（2 条：TagHasLevel、HasTagClass）。

| 约束 | 检查 | 已知违反 | 干净样本 |
|---|---|---|---|
| Tag 有整数等级 | `TagHasLevel` | `tag_unknown` 缺等级 | `tag_email_1` |
| hasTag 非字面量 | `sh:nodeKind sh:IRI` | `col_legacy` 指字面量 | `col_email`→Email |
| 未打标可发现（CQ3，不是 shape） | `FILTER NOT EXISTS` | `col_order_id` 等 4 列无 tag | `col_email` |

**10 个坏样本里，现有闸门只稳定抓住 2 个**（完整表见 [consumability §4](../../../topics/05-produce/representation/consumability.md)）：

| # | 坏样本 | 现在抓住？ |
|---|---|---|
| S4 | 缺 load | 否（假阳性） |
| S6 | shape 缺 target | 否（0 focus → `conforms=true`） |
| S7 | tag 是字面量 | **是**（violation） |
| S8 | level 缺失 | **是**（violation） |

其余 6 个（S1/S2/S3/S5/S9/S10）分别缺 principal/moment/refuse/version、无 dataset 边、版本不一致；现状均为 silent 或 answer undercoverage。

SFE-O 未交付可执行 shape，只借做法。分开报：违反检出/干净样本误报/人审接受率；`E-02` catch/FA = 18.9/16.8、8.2/3.5、5.0/1.8；PPV 复算见 `O-F08`。

依据：T:[consumability §4](../../../topics/05-produce/representation/consumability.md) · S:SFE-O §4.1 · E-02/O-F08 · 未测

## A.5 可消费性闸门（产物：`build_report`）

三关记录，不是一个 `parsed` 布尔：

```json
{"_note":"示例运行记录","load":{"parsed":true,"violations":2,"missing_fields":[]},"validate":{"shape_bad_samples":2,"caught":2,"clean_fp":"未测"},"answer":{"CQ1":"2/2","CQ2":"7 列/4 表","CQ3":"4 数据集"},"classes":11,"properties":5,"policy_version":"0.3.0","tag_version":"0.1.0","provenance":{"source":"synthetic"}}
```

- **load**：rdflib 解析 [ontology.ttl](../example/ontology.ttl)/[shapes.ttl](../example/shapes.ttl)/[catalog.ttl](../example/catalog.ttl)；`parsed`=语法/前缀，`missing_fields`=产物必填。
- **validate**：pyshacl 跑 shapes；`violations`=shape 违反；`caught`=已声明坏样本被抓住数；`clean_fp` 未测。
- **answer**：CQ1 返回 2、CQ2 7 列/4 表、CQ3 4 数据集；0 行必须分因。

`E-25`：三关是记录，不是产物属性；`targeted=0` 不是 pass。

**交接**：`load/violations`→B；`query_id`→C.4/`policy_version`→A.5。

**停**：`violations` ≠ 已声明坏样本数（2）或落在已知清单外；`targeted=0`（shape 无目标）当 pass；`answer` 0 行不分因；无契约/版本/来源；下游不加载。

依据：E-25 / T:[consumability §1/§6](../../../topics/05-produce/representation/consumability.md) · T:05/generation · 工程产物 · 未测

## A.6 证据边界

- **能加载 ≠ 可用**：`parsed=true` 只到语法；S4（endpoint 假阳性）、S6（无 target 静默）都可能在「加载成功」后发生。
- **`violations=2` ≠ 干净**：只证明两个已声明坏样本被抓住，不证明干净数据无误报。
- **三关过 ≠ 生产**：没有真数据误报率、延迟、权限、规模、版本回滚；fixture 是合成 5 表/13 列。
- build 无 in-scope 证据；数字只引 E/O 或标「示例」。

依据：T:05/representation · T:05/generation · S:SFE-O/Catch/N&D/Glyph
