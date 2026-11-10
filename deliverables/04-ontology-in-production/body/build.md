---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# A · 建：从契约到 `build_report`

> **本章回答**：消费者要什么、建到什么程度算可消费。
> **你需要准备**：3 个 consumer、6 项契约、一个能解析 TTL 的环境。
> **做完得到**：契约、`ontology.ttl`、`shapes.ttl`、`build_report`。
> **怎么算做完**：A.5 三关 + A.6 证据与边界；清单见 [acceptance](../sections/acceptance.md)。
>
> 三关 = load / validate / answer；详细判据与 10 个坏样本见 [参考表 §1–§2](../sections/reference.md)。

## A.1 消费者契约（产物）

6 项写不出就停。**怎么找**：UI/agent 的 owner（谁读）、数据 owner（谁能给列）、治理（谁能拒）各拉 1 人；每人给「在什么时刻、要答什么 / 拒什么」。填不出的格就是需求缺口，不要编。

本 fixture（[example](../example/README.md)）：

| consumer | principal | moment | answers | refuses | load |
|---|---|---|---|---|---|
| UI | steward | 页面加载 | 答 Email 列 | — | SPARQL endpoint |
| agent | steward | 查询时 | 答 4 表/7 列 | — | SPARQL endpoint |
| governance | analyst | 夜间 | 答未打标数据集（4） | 拒 level ≥3 列 | SPARQL endpoint |

tag 是 `:Email` 等类的实例，CQ1 用 `?t a/rdfs:subClassOf*`；拒绝单位 = 列（triple subject）。

**你的表**：

| consumer | principal | moment | answers | refuses | load |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

> `refuses` 写 `—` 表示「明确不拒」，不算空；契约本身带 `contract_version`（第 7 项，A.5 回填），不在 6 列里。

**契约六项与 `build_report` 只部分对应**：`violations` ≠ `refuses`，`missing_fields` ≠ 契约缺字段；覆盖表见 [参考表 §2](../sections/reference.md)。

### CQ 只是模板词：须在契约行可执行

①`?col :hasTag ?t . ?t a/rdfs:subClassOf* :Email`（UI）；②`sensitivityLevel ≥ 3` + `columnOfTable` 反查（agent）；③`FILTER NOT EXISTS { ?col :hasTag ?t }`（治理）。

## A.2 表示档位：按消费者选

| 消费者要什么 | 选 | 判据 |
|---|---|---|
| 只把知识拼进 prompt / 检索 | 词表 | 不需要判定，形式化只占预算 |
| 要跑 shape / 查询 / 授权判定 | 结构表 | 有可判定的关系与约束 |
| 要从公理推出隐含分类 | 逻辑表 | 需要 reasoner；解释成本高 |

本例选结构表（`推测`）：三条契约无隐含分类。**薄层优先**：命名单位（K0→K1）+54.6pp（占 74.4pp 的 73.4%），再加 +19.8pp（26.6%，`O-F14`）。

三档 × 四位置矩阵见 [参考表 §1](../sections/reference.md)：结构表是唯一三关都 `supported` 的档；词表 validate/explain 弱；逻辑表 explain 无可移植路径。能力矩阵，不是效应量；薄层优先的 +54.6pp 不是三档对照。

## A.3 最小本体（11 类 / 5 属性）

只建契约用得到的；等级挂 `Tag`，不挂 `Column`。

TBox：[ontology.ttl](../example/ontology.ttl)（11 类/5 属性；计数 `?c rdfs:subClassOf* :Tag` 8 + 3 = 11）；ABox：[catalog.ttl](../example/catalog.ttl)。

**标签层独立**：Glyph 275 叶标签，不产策略、不执行。

## A.4 约束与负例（产物：shape + 负例表）

每条约束 = shape/检查 + 已知违反 + 干净样本。

Shapes：[shapes.ttl](../example/shapes.ttl)（2 条：TagHasLevel、HasTagClass）。

| 约束 | 检查 | 已知违反 | 干净样本 |
|---|---|---|---|
| Tag 有整数等级 | `TagHasLevel` | `tag_unknown` 缺等级 | `tag_email_1` |
| hasTag 非字面量 | `sh:nodeKind sh:IRI` | `col_legacy` 指字面量 | `col_email`→Email |
| 未打标可发现（CQ3，不是 shape） | `FILTER NOT EXISTS` | `col_order_id` 等 4 列无 tag | `col_email` |

**10 个坏样本里，现有闸门只稳定抓住 2 个**（完整表见 [参考表 §2](../sections/reference.md)）：

| # | 坏样本 | 现在抓住？ |
|---|---|---|
| S4 | 缺 load | 否（假阳性） |
| S6 | shape 缺 target | 否（0 focus → `conforms=true`） |
| S7 | tag 是字面量 | **是**（violation） |
| S8 | level 缺失 | **是**（violation） |

其余 6 个（S1/S2/S3/S5/S9/S10）分别缺 principal/moment/refuse/version、无 dataset 边、版本不一致；现状均为 silent 或 answer undercoverage。

SFE-O 未交付可执行 shape，只借做法。分开报：违反检出/干净样本误报/人审接受率；Ontology Catch 的 catch/FA = 18.9/16.8、8.2/3.5、5.0/1.8；PPV 复算见 evidence。

## A.5 可消费性闸门（产物：`build_report`）

三关记录，不是一个 `parsed` 布尔：

```json
{"_note":"fixture 期望，非实测","load":{"parsed":true,"missing_fields":[]},"validate":{"violations":2,"targeted":2,"declared_shape_samples":2,"caught":2,"contract_bad_samples":10,"contract_caught":2,"clean_fp":"未测"},"answer":{"CQ1":"2/2","CQ2":"7 列/4 表","CQ3":"4 数据集"},"classes":11,"properties":5,"policy_version":"0.3.0","tag_version":"0.1.0","contract_version":"0.1.0","provenance":{"source":"synthetic"}}
```

- **load**：rdflib 解析 [ontology.ttl](../example/ontology.ttl)/[shapes.ttl](../example/shapes.ttl)/[catalog.ttl](../example/catalog.ttl)；`parsed`=语法/前缀，`missing_fields`=产物必填。
- **validate**：pyshacl 跑 shapes；`targeted`=有目标且实际被检查的 shape 数；`violations`=shape 违反；`caught`=已声明 shape 坏样本被抓住数；`clean_fp` 未测。**两个分母不要混**：`2/2` 是 shape 声明样本；10 个契约坏样本只抓 2 个（`contract_caught/contract_bad_samples`）。分子就是 S7/S8，别把它当第二个独立测试。
- **answer**：CQ1 返回 2、CQ2 7 列/4 表、CQ3 4 数据集；查询文本在 [B.2](./consume.md)，没写 B.2 就先跑 CQ1 再回填；0 行必须分因。

三关是记录，不是产物属性；`targeted=0` 不是 pass。

**交接**：`build_report` 的 `targeted/violations`→B 的先决条件；`query_id`→C.4；`policy_version`→A.5。

**停**：`violations` ≠ 已声明坏样本数（2）或落在已知清单外；`targeted=0`（shape 无目标）当 pass；`answer` 0 行不分因；无契约/版本/来源；下游不加载。

## A.6 证据与边界

> 证据见 [evidence](../evidence/README.md)。

- **能加载 ≠ 可用**：`parsed=true` 只到语法；S4（endpoint 假阳性）、S6（无 target 静默）都可能在「加载成功」后发生。
- **`violations=2` ≠ 干净**：只证明两个已声明坏样本被抓住，不证明干净数据无误报。
- **三关过 ≠ 生产**：没有真数据误报率、延迟、权限、规模、版本回滚；fixture 是合成 5 表/13 列。

