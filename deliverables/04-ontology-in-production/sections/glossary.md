---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# 术语与内码速查

> 第一次读 04 先看这一页。定义只到“能读懂 04”；完整术语见仓库根 [GLOSSARY](../../../GLOSSARY.md)。
>
> **术语基线**：ADR 0011 / 2026-11；K0–K4 标 `local`（论文条件，非 normative 源）。

<a id="term-sources"></a>
## 0. 名词从哪来（N / local）

> **读法**：`N:` = 规范性锚（标准/权威本体），只定「这个词是什么意思、什么叫合格」，**不撑效果**；`local` = 本仓库/本工程的工作词，没有标准锚，按本页解释读，不得写成行业共识。标准清单与「不能定义什么」见 [规范主干](../../../topics/trunk.md)；逐词判定见 [术语基线](../../../meta/term-baseline.md)。

| 词 | 来源 | 一句话（只到读懂 04） |
|---|---|---|
| 本体 / 顶层本体 | `N: ISO/IEC 21838-1/-2`（本仓库「本体」义更宽，判 `broader`） | 概念/关系/约束的显式规范；标准只给 TLO 的合格性 |
| 类 / 属性 / 实例 | `N: W3C OWL 2 Profiles`（类与属性的语义边界） | 概念 / 关系 / 具体对象；profile 只定语义子集 |
| TBox / ABox | `local`（DL 文献常用词，未入卡 normative 源） | schema / 实例层；本仓库只作描述 |
| SHACL / shape / `targeted` | `N: W3C SHACL` | 图约束、可检查条件、被检查的 shape 数；不是推理器 |
| 策略 / principal / effect | `N: W3C ODRL 2.2`（策略表达）/ `N: OASIS XACML 3.0`（判定架构） | 许可-禁止-义务的写法与 PDP/PEP；**`principal` 与 `level 1–4` 是本工程的 `local` 映射** |
| `skip` | `local` | 本工程加的「未判定」第 4 种效果；XACML/ODRL 都没有 |
| 数据分级（核心/重要/一般） | `N: GB/T 43697-2024` | 三级框架；04 的 `level 1–4` 与 2/3 阈值是工程映射（`local`） |
| 个人信息 / 敏感个人信息 | `N: GB/T 35273-2020` | 个人信息处理要求；不是机密性分级 |
| 数据契约 | `N: ODCS v3.1.0` | contract 的结构/SLA/质量字段；不保证运行时执行 |
| OBDA / R2RML / OWL 2 QL | `N: W3C OWL 2 Profiles`（profile 语义）；OBDA/R2RML 是 `local` 工程词 | 本体+映射→查询时重写；只支持轻量 profile |
| audit / replay / snapshot | `local` | 本工程的记录、重跑与快照词；snapshot 是日期标签，不是 hash |
| leak oracle / governed / raw / fail-open | `local` | 本工程的验收与执行词；没有标准定义 |

> **只定词，不撑效果**：`N:` 行只回答「什么意思、什么叫合格」；「跑出来的结果对不对、泄漏多少」只能引 E-xx 与 fixture 的期望值。

## 1. 概念（按出现顺序）

| 词 | 一句话 | 在 04 哪里 |
|---|---|---|
| 本体（ontology） | 一组类、属性、约束，用来把“表/列/标签”说清楚 | A.3 |
| TBox | 类与属性的定义（schema） | [A.3](../body/build.md) |
| ABox | 具体实例（表、列、标签） | [A.3](../body/build.md) |
| 类 / 属性 / 实例 | 概念 / 关系 / 具体对象 | A.3 |
| Turtle（TTL） | RDF 的一种文本写法 | example |
| SPARQL | RDF 的查询语言 | B.2 |
| CQ | competency question，消费者要回答的问题；04 用 CQ1–CQ3 | A.1/B.2 |
| SHACL | W3C 约束语言：用 target 选节点，用 property/条件检查图；不是推理器 | A.4 |
| shape | 一条可检查的约束（target + property + 条件） | A.4 |
| `targeted` | 有目标且实际被检查的 shape 数；0 不是 pass | A.5 |
| principal | 以什么身份读（steward/analyst/governance/service） | A.1/C.2 |
| clearance | 用户 clearance；04 只记录，不参与判定 | C.2 |
| raw | 查询本身的结果，未经 policy | B.2 |
| governed | policy + 执行层之后的结果 | C.4 |
| skip | 策略的“未判定”效果，不是 allow，也不是 deny | C.2/C.3 |
| leak oracle | 独立的安全期望：敏感 object 不出现；不等于“0 行” | C.3 |
| PPV | positive predictive value / precision；04 只在 A.4 / O-F08 用，指「假设错答案基率下的 precision」，不是论文直接报告值 | A.4 / O-F08 |
| audit | 一次 decision 的记录；04 用 per-subject 样例 + query log 表 | C.4 |
| replay | 同版本/快照重跑并对照 decision/reason/outcome | C.4 |
| snapshot | 数据/策略的快照；04 的 `example/ 2026-11-10` 是日期标签，不是 hash | A.5/C.4 |
| OBDA | 本体 + R2RML 映射 → 查询时重写 SQL | B.4 |
| R2RML | 关系库 → RDF 的映射语言 | B.4 |
| Ontop | OBDA 引擎；TBox 饱和 + SQL 重写 | B.4 |
| OWL 2 QL | OBDA 支持的 OWL profile | B.4 |
| fail-open / fail-closed | 出错时放行 / 拒绝；trustgraph 多处 fail-open | C.3 |

## 2. 内码

| 码 | 意思 | 读者要不要跟 |
|---|---|---|
| `E-xx` | 跨派结论，在 `topics/conclusions.md` | 想核证据时跟；正文首遍可跳过 |
| `T:` | topics 页（如 `T:querying`） | 可选 |
| `S:` | src digest/材料 | 可选 |
| `O-xx` | 对象地址（数值/公式/反例），不是结论 | 想复算时跟 |
| `L-xx` | 派内局部判断，只在 `claims.md` 工作 | 一般不需要 |
| `Q-xx` / `C-xx` | 开放问题 / 冲突 | 看 frontier/conclusions 时跟 |
| `F1` / `K0–K4` | 派内 finding / N&D 实验条件代号（原始点位、点位语义、知识投影文本、流程摘要、运行记录检索；**非标准**） | A.2/C.1 里出现；定义见 [01 K 页](../../01-capability-status/sections/k-ladder.md) |
| `GGC` / `NLKGQ` / `KGVoyager` | 三条 Text2SPARQL 路线 | B.1 有一句话 |
| `Glyph` / `trustgraph` / `SFE-O` | 标签来源 / 读路径实现 / 本体工程做法 | C.1/C.3/A.4 有一句话 |

## 3. 版本词

| 词 | 来源 | 备注 |
|---|---|---|
| `policy_version` | `example/policy.json` | 0.4.0 |
| `ontology_version` | `ontology.ttl` 的 `owl:versionInfo` | 0.1.0 |
| `tag_version` | `ontology.ttl` 的 `:tagVersion` | fixture 约定 |
| `contract_version` | A.1 契约表 | fixture 约定 0.1.0 |
| `snapshot` | `example/ 2026-11-10` | 日期标签，不是内容 hash |
| `parser` | rdflib/pyshacl | 本次未记版本；跨版本可能不同 |

## 4. 四个容易混的点

1. **CQ1–CQ3 ≠ 策略测试 T1–T11**：前者是查询，后者是 decision 输入。
2. **LEAK-T1 ≠ T1**：前者是表页泄漏探针，后者是策略测试的第一条。
3. **skip ≠ allow**：skip 是未判定；执行层可以返回或 withhold，审计单列 `execution_effect`。
4. **`kind` ≠ `subject_kind`**：`kind` 是 policy 输入（column/table/dataset）；`subject_kind` 是 audit 字段（judged subject 的类型）。同一层的两个名字，不要混。
