---
status: draft
updated: 2026-11-10
parent: README.md
---

# 5 分钟跑通（可选）

> 这是**可选的阅读对照**，不是交付标准，也不是运行记录。需要 `rdflib` + `pyshacl`（`pip install rdflib pyshacl`）。
> 命令在本目录跑；下面的数字是 fixture 期望，不是实测。跑之前先看 [README](./README.md) 的 fixture 说明；跑不通先看 [症状地图](../sections/map.md)。

## 1. 解析三个 TTL（期望 3/3 parsed）

```bash
python3 - <<'PY'
import rdflib
for f in ["ontology.ttl", "shapes.ttl", "catalog.ttl"]:
    g = rdflib.Graph(); g.parse(f); print(f, len(g), "triples")
PY
```

## 2. 跑 shapes（期望 2 violations：tag_unknown / col_legacy）

```bash
python3 - <<'PY'
import rdflib
from pyshacl import validate
data = rdflib.Graph()
data.parse("ontology.ttl")   # TagHasLevel 的 targetClass 需要子类边
data.parse("catalog.ttl")
conforms, _, text = validate(data, shacl_graph="shapes.ttl",
                             inference="none", advanced=False)
print("conforms:", conforms); print(text[-800:])
PY
```

## 3. 跑 CQ1（期望 2 列 / 2 表）

```bash
python3 - <<'PY'
import rdflib
g = rdflib.Graph()
g.parse("ontology.ttl")   # CQ1 的 subClassOf* 需要 TBox 同图
g.parse("catalog.ttl")
q = """PREFIX : <https://ex.org/c#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?col ?table WHERE {
  ?col :hasTag ?t ; :columnOfTable ?table .
  ?t a/rdfs:subClassOf* :Email .
}"""
for row in g.query(q): print(row)
PY
```

## 期望（与 [A.5](../body/build.md)/[B.2](../body/consume.md) 一致）

- 解析：3/3；TBox 11 类/5 属性；shapes 2。
- `pyshacl`：`conforms=false`，2 violations（`tag_unknown` 缺 `sensitivityLevel`；`col_legacy` 的 `hasTag` 是字面量）；需 `ontology.ttl` 同图，否则 `TagHasLevel` 只检查显式 `a :Tag` 的个体，干净样本 `tag_email_1` 不会被 target。
- CQ1：2 行（`col_email`、`col_customer_email`）/ 2 表；需 `ontology.ttl` 与 `catalog.ttl` 同图，只加载 ABox 会得到 1 行。
- CQ2：4 表 / 7 列；CQ3：4 个 dataset 各 1。

**跑不通时**：先看 [症状地图](../sections/map.md)；`0 violation` 可能是 shape 没有 target，不是数据干净。数据与坏样本见 [data.md](./data.md)。
