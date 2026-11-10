---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# B · 用：3 个 CQ 变成能跑的查询

> 接 [A](./build.md)。示例是合成的（200 表 / 5,000 列）；标「示例」的数字只证明这张例子跑通。

## B.1 路线：先看资产，三选一

本例 substrate 是 RDF（无 entailment），走 KG + Text2SPARQL。选择顺序：RDF→KG；关系库→OBDA；有 KG 且数值/反连接→Text2SPARQL；否则 in-context/navigation。

| 你先有 | 选 | 判定键 |
|---|---|---|
| 关系库 + 稳定 schema + 映射 | OBDA（B.4） | 有库 → 不物化 |
| 无 KG，来源非结构化 | KG 构建（用 A.3 的 12 类做 slice） | 无 KG 且要反连接 → 先建 |
| 已有 KG，要数值过滤/反连接 | Text2SPARQL（B.2） | 有 KG → 生成查询 |
| schema 小（11 类/5 属性）进得了 context | ontology-in-context | 小 → 全量 OWL |
| schema 大、只有 endpoint | ontology-free navigation | 大 → 只给 class index |

数据侧二选一（KG 构建 / OBDA）；查询侧三选一（Text2SPARQL / in-context / navigation），可与数据侧叠。三选一是选入口，不是排序（`E-21`）。

依据：模板（选路表）/ T:[03/querying §5](../../../topics/03-knowledge/querying/mechanism.md#5-工程接线给-04-b3-用)

## B.2 三条查询 + 空结果分因

前缀：`PREFIX : <https://ex.org/c#>`、`PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>`；ABox 在 [catalog.ttl](../example/catalog.ttl)。

**CQ1** 哪些列是 `PII.Email`（含子类）

```sparql
SELECT ?col ?table WHERE {
  ?col :hasTag ?t ; :columnOfTable ?table .
  ?t a/rdfs:subClassOf* :Email .
}
```

期望 2 列 / 2 表。

**CQ2** 哪些表至少有一列等级 ≥3

```sparql
SELECT DISTINCT ?table ?col WHERE {
  ?col :columnOfTable ?table ; :hasTag ?t .
  ?t :sensitivityLevel ?level .
  FILTER(?level >= 3)
}
```

期望 4 表 / 7 列。

**CQ3** 哪些数据集有未打标列

```sparql
SELECT ?dataset (COUNT(?col) AS ?n) WHERE {
  ?col a :Column ; :columnOfTable ?table .
  ?table :tableInDataset ?dataset .
  FILTER NOT EXISTS { ?col :hasTag ?t . ?t :sensitivityLevel ?l }
} GROUP BY ?dataset
```

期望 4 数据集 ×1（fixture）。

| 先问（假 →） | 处置 |
|---|---|
| `ASK { ?t a :Email }` | CQ1 覆盖不足 |
| `ASK { ?t a :Email ; :sensitivityLevel ?l }` | CQ1 数据（有标签缺 level） |
| `ASK { ?c :hasTag ?t . ?t a :Email }` | CQ1 查询/链接错 |
| CQ3 `ASK { ?c :Column . FILTER NOT EXISTS { ?c :hasTag ?t . ?t :sensitivityLevel ?l } }` | 0 行是答案，不是 data |
| `ASK { ?t :tableInDataset ?d }` | CQ3 覆盖（无 dataset 边） |

记 `query_id`（`CQ1|CQ2|CQ3`）、执行器/snapshot/version：执行层只跑 SPARQL、不 entail、不解释空结果。

依据：模板（3 条 SPARQL）/ T:[03/querying §5](../../../topics/03-knowledge/querying/mechanism.md#5-工程接线给-04-b3-用) / S:[Qlever](../../../src/open-source/ad-freiburg-qlever/digest.md)

## B.3 纠错：只对高风险 query 做

只把高风险 query 送 Gate→Corrector（GGC）；不做全量纠错。依据不是「纠错更好」，而是 `E-21` 里全量纠错 92.34%、选择性 98.33%，墙钟是全量纠错的 45%。无 2×2 改对/改坏配对、空结果不进 Gate，净收益只能自域配对测。

依据：E-21 / T:[findings F1](../../../topics/03-knowledge/querying/findings.md) / gap

## B.4 OBDA：标签留在关系库时

本体 + R2RML 映射 → 虚拟 KG；SPARQL 在编译期重写成 SQL（ontop：TBox 饱和 + `reformulateIntoNativeQuery`）。先 `ontop validate`，再跑最小查询并存生成的 SQL；工具面只留 `sparql_query(query)`；做「去公理」消融再谈本体贡献。只支持 OWL 2 QL，不是 gate；OBDA ≠ NL→query。

依据：E-20 / O-C08 / T:[02 R11](../../02-engineering-playbook/recipes/offline-and-obda.md) / S:[ontop](../../../src/open-source/ontop-ontop/digest.md)

## B.5 验收

| 指标 | 示例（20 题 smoke） | 工程建议（`推测`） |
|---|---|---|
| execution accuracy | 17/20（85%） | 自域 ≥0.8 起步，按风险定 |
| 空结果 | 2 条：覆盖 1、数据 1 | 必须分因 |
| 延迟 p95 | 0.8 s | 按预算 |

20 题只是 smoke；85%、0.8 s 是示例，不外推。

依据：模板（验收表）/ E-21 / gap

## B.6 证据边界

- `E-21`：三条路线各单设置、无头对头 → 不能排序，不能当自域基线。
- `E-20`：重写落到 SQL，不证明查询正确或本体独立贡献。
- 示例数字只证明本例跑通；gap：空结果分布、纠错配对样本。
- **停**：拿 85% 当生产正确率，或空结果不分因就调 prompt → 停。
