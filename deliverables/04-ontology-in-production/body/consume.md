---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# B · 用：从资产到 3 条能跑的查询

> 接 [A](./build.md)。示例是合成的（5 表/13 列）；200/5,000 只是 Glyph 参照。标「示例」的数字只证明这张例子跑通。
>
> **本章回答**：按你手上的资产选哪条路线、3 条 CQ 怎么跑、0 行怎么办。
> **你需要准备**：A 的 TBox/ABox；你的资产（RDF / 关系库 / endpoint）。
> **做完得到**：3 条 SPARQL、空结果分因表、纠错/OBDA 协议。
> **怎么算做完**：B.6 验收；清单见 [acceptance](../sections/acceptance.md)。

## B.0 决定表

| 你先有 | 默认路线 | 反例 | 停 |
|---|---|---|---|
| 关系库 + 稳定 schema + 映射 | OBDA（B.4） | 重写跑通但结果集与原生 SQL 不一致 | `ontop validate` 失败或公理被拒 |
| 已有 KG + 完整 OWL，进得了 context | ontology-in-context（B.1） | 本体超窗口；slice 后分数掉 | token 超预算 / snapshot 不能固定 |
| 已有 KG，无 ontology，只有 endpoint | agentic navigation（B.1） | 图不是 `rdf:type` 体系；class index 建不出 | 探索成本超预算 |
| 已有生成器 + 可标注错例 | gate / selective correction（B.3） | Gate 分布外，trigger 漂移 | 没有 100 条目标分布标注 |
| 什么都没有 | 先建 KG/本体 | 空图上选查询路线 | 回到 05 派（造与修） |

按资产条件选，不按总分排。**四条路线在资产/规模/指标/成本上不可比**：三条路线各单设置、无头对头；OBDA 是另一种形态。完整矩阵、失败目录与「不可比清单」在 [参考表 §3–§4](../sections/reference.md)；本章只取 04 用得到的部分。

## B.1 四条路线各停在哪

资产选择见 B.0。四条路线各停在哪：

- **GGC**：生成后 Gate 判该不该改，只改高风险；单 KG/单骨干、无 2×2，空结果不进 Gate。
- **NLKGQ**：完整 OWL 单次进上下文；单 snapshot、本体超窗口要 slice，wrapper 手工。
- **KGVoyager**：think–act–observe + search/explore/execute；只支持 `rdf:type` 图，benchmark 小。
- **OBDA**：本体 + R2RML → 查询时重写 SQL；只支持 OWL 2 QL，重写正确 ≠ 查询正确。

## B.2 三条查询 + 空结果分因

前缀：`PREFIX : <https://ex.org/c#>`、`PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>`；ABox 在 [catalog.ttl](../example/catalog.ttl)。

**CQ1** 哪些列是 `:Email`（含子类）

```sparql
SELECT ?col ?table WHERE {
  ?col :hasTag ?t ; :columnOfTable ?table .
  ?t a/rdfs:subClassOf* :Email .
}
```

期望 2 列 / 2 表（UI/steward，raw）。

**CQ2** 哪些表至少有一列等级 ≥3

```sparql
SELECT DISTINCT ?table ?col WHERE {
  ?col :columnOfTable ?table ; :hasTag ?t .
  ?t :sensitivityLevel ?level .
  FILTER(?level >= 3)
}
```

期望 4 表 / 7 列（agent/steward，raw）。

**CQ3** 哪些数据集有「没有带 level 的 tag」的列

```sparql
SELECT ?dataset (COUNT(?col) AS ?n) WHERE {
  ?col a :Column ; :columnOfTable ?table .
  ?table :tableInDataset ?dataset .
  FILTER NOT EXISTS { ?col :hasTag ?t . ?t :sensitivityLevel ?l }
} GROUP BY ?dataset
```

期望 4 数据集 ×1（governance，raw；R8 dataset allow）。

> CQ3 依赖 ABox 显式写 `?col a :Column`；不写类型会 0 行，这是查询前置，不是 coverage 问题。它数的是「没有 `hasTag` + `sensitivityLevel`」的列，不是「没有任何 tag」。

> 上面三个期望都是 **raw**，不是 policy 后的结果。policy 后：CQ1/CQ2 在 analyst 下会变 0；CQ3 只给 governance（R8 dataset allow），analyst 不适用。见 [C.4](./govern.md)。

**0 行不是错，先分因**：

| 原因 | 先问（假 →） | 处置 |
|---|---|---|
| 覆盖不足 | `ASK { ?t a :Email }` | 补标签/子类边；不要先调 prompt |
| 数据缺失 | `ASK { ?t a :Email ; :sensitivityLevel ?l }` | 补 level；记录 snapshot |
| 查询/链接错 | `ASK { ?c :hasTag ?t . ?t a :Email }` | 改 join/前缀；不要重试同一条 |
| 过滤过严 | 去掉 `FILTER` 的行数 vs 原行数 | 放宽阈值；记录理由 |
| CQ3 的 0 行是答案 | `ASK { ?c :Column . FILTER NOT EXISTS { ?c :hasTag ?t . ?t :sensitivityLevel ?l } }` | 0 行 = 全部有 level，不是 data |
| 无 dataset 边 | `ASK { ?t :tableInDataset ?d }` | 补边；否则 CQ3 覆盖不足 |
| 版本/snapshot 不一致 | 同一 query 在两个 snapshot 跑；记录版本 | 固定 snapshot/版本；重放 |

记 `query_id`（`CQ1|CQ2|CQ3`）、执行器/snapshot/version：执行层只跑 SPARQL、不 entail、不解释空结果。

## B.3 纠错：只对高风险 query 做

只把高风险 query 送 Gate→Corrector（GGC）；不做全量纠错。依据不是「纠错更好」，而是 GGC 里 Generator 单跑 90.23%、全量纠错 92.34%、选择性 98.33%；墙钟约为全量纠错的 55%（降幅 45%），比单跑多约 10%。**但 GGC 没有 2×2 配对**：分不清「选得准」还是「改得准」，也没有空结果机制。

**上线前先补 2×2**：

| 初始 | 改后对 | 改后错 |
|---|---:|---:|
| 初始错 | 改对（收益） | 仍错 |
| 初始对 | 保持 | **改坏（代价）** |

没有这张表，只能写「全量低于选择性」，不能写「全量会把对的改坏」，也不能报净收益。自域配对步骤：抽 100–200 条、固定生成器与 Corrector、人工判初始对错与改后对错、报改对/改坏/不变四格与成本。

## B.4 OBDA：标签留在关系库时

本体 + R2RML 映射 → 虚拟 KG；SPARQL 在编译期重写成 SQL（ontop：TBox 饱和 + `reformulateIntoNativeQuery`）。

**最小步骤**：

1. `ontop validate`：先看公理是否被支持（只 OWL 2 QL）。
2. 跑最小查询，存生成的 SQL 与结果集。
3. **去公理消融**：去掉 TBox 公理（记录去掉哪几条），同一查询集重跑。
4. 结果集一致 → 本体贡献未被隔离；不一致 → 差在哪几条公理。

工具面只留 `sparql_query(query)`；OBDA ≠ NL→query；重写正确 ≠ 查询正确。

## B.5 失败目录（本章 5 条）

| # | 失败 | 触发 | 症状 | 检测 |
|---|---|---|---|---|
| 1 | 空结果被当错 | 0 行 | 重试/调 prompt | 按 B.2 分因 |
| 2 | 全量纠错 | 所有 query 都改 | 改坏对的 | 2×2 配对 |
| 3 | Gate 分布外 | 换图/换生成器 | trigger/FPR 漂移 | 目标分布 100 条重标 |
| 4 | 本体超窗口 | 完整 OWL 太大 | 截断/丢公理 | ontology token 计数 + slice 对照 |
| 5 | execution accuracy 当业务正确 | 只看分数 | 答案集对、业务错 | 自域配对 + 人工抽检 |

完整 17 类与检测 query 见 [参考表 §4](../sections/reference.md)。

## B.6 验收

| 检查 | principal | raw | governed | 不通过时 |
|---|---|---|---|---|
| CQ1 | UI/steward | 2 行 / 2 表 | 2 行 / 2 表（analyst: 0） | 0 行先分因，不要改 prompt |
| CQ2 | agent/steward | 7 列 / 4 表 | 7 列 / 4 表（analyst: 0/7） | 查 `FILTER`/类型/重复 |
| CQ3 | governance | 4 个 dataset | 4 个 dataset（analyst: 不适用） | 查 `?col a :Column` 与 dataset 边 |
| 0 行 | — | 每条有原因 | — | 不要重试同一条 |
| 纠错 2×2 | — | 未测 | — | 不要报净收益 |
| 延迟 | — | 未测 | — | 按预算 |

## B.7 证据与边界

> 证据见 [evidence](../evidence/README.md)。

- 三条路线各单设置、无头对头 → 不能排序，不能当自域基线。
- OBDA 重写落到 SQL，不证明查询正确或本体独立贡献。
- 示例数字只证明本例跑通；未测：空结果分布、纠错 2×2 配对、跨路线成本口径。
- **停**：拿任一 benchmark 分数当生产正确率，或空结果不分因就调 prompt → 停。
