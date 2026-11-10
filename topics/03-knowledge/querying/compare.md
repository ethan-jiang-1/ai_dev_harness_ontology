---
status: draft
updated: 2026-11-10
rq: [RQ1, RQ5]
evidence: [E-21]
---

# 查询 · 对照（决定表）

> 回答：给定手上的资产，选哪条路线；每条路线在哪一步会断；哪些数不能放在一起比。
> 不回答：哪条路线总分最高（没有头对头）；KG 怎么建（[05/representation](../../05-produce/representation/README.md)）；读路径权限（[01/access-control](../../01-constraint/access-control/README.md)）。

## 0. 决定与读法

**决定**：先看资产，再选路线；不要先选模型/框架。

| 你先有 | 默认路线 | 依据 |
|---|---|---|
| 关系库 + 稳定 schema + 映射 | OBDA（虚拟 KG） | 有库不物化；本体 + R2RML 在查询时重写 |
| 已有 KG + 完整 OWL，且本体进得了 context | ontology-in-context | 完整 OWL 单次进上下文；不训练 |
| 已有 KG，但没有 ontology，只有 endpoint | agentic navigation | 只用 endpoint + class index；工具探索 |
| 已有生成器 + 可标注的错例 | gate / selective correction | 只改高风险 query；不全量纠错 |
| 什么都没有 | 先建 KG/本体 | 回到 05；不要在空图上选查询路线 |

**读法**：矩阵里 `不可比` 是结论，不是空格；不同数据集/指标的数不能相加、不能排名。

## 1. 4×8 矩阵

| 维度 | GGC | NLKGQ | KGVoyager | OBDA |
|---|---|---|---|---|
| 先有什么资产 | 已有 KG + 生成器 | 完整 OWL + endpoint | 只有 endpoint | 关系库 + 映射 |
| 问题量 | 31,570（MCQA） | 1,000（DBLP-QuAD 3.1） | 394（4 个 benchmark） | 无 benchmark |
| 本体规模 | 小 schema（iMKG）；类/关系/triple 未报 | 完整 OWL 进 context；token/窗口未报 | 无 ontology；class index 35 类/2.7KB、91 类/5.3KB | 示例 1 类/1 属性；只 OWL 2 QL |
| 模型 | Llama-3.2-3B LoRA | Qwen3.6-27B；10 模型 Match 24.8–90.3 | 4 个骨干；模型间差 36.3pp | 无 LLM（查询重写） |
| 指标 | 答案集匹配 90.23→98.33；错误 2,397 语义/650 语法/38 gold | Match 89.9 / Exact 81.3 | F1 64.6 vs 60.9（+3.7pp） | 无指标；最小链路 2 行 |
| 成本 | 单跑 ~30h / 选择性 ~33h / 全量 ~60h；45% 是相对全量 | 未报 | $2.43 vs $3.94；85.6s vs 112.4s | 未报 |
| 失败模式 | 空结果无机制；单 KG/单骨干；无 2×2 | 101 非 Match：citation 24/federated 22/aggregation 23/异质 29；snapshot 漂移 | 非 `rdf:type` 要 adapter；50/56 是 gave up；benchmark 小 | 重写正确 ≠ 查询正确；超 QL 公理静默丢 |
| 可比性 | — | 与 GGC 不可比 | 与前两者不可比 | 与三者不可比 |

**锚**：GGC 见 [F1](./findings.md)；NLKGQ 见 [F2](./findings.md)；KGVoyager 见 [F3](./findings.md)；OBDA 见 [E-20](../../conclusions.md) 与 [Ontop digest](../../../src/open-source/ontop-ontop/digest.md) §3–§5。

## 2. 失败目录（17 类）

| # | 类型 | 来源 | 触发 | 可观察症状 | 检测 |
|---|---|---|---|---|---|
| 1 | Gate 分布外 | GGC | 换生成器/换 KG/换 schema | trigger/FPR 漂移，纠错反而改坏 | 在目标分布上重标 100 条，报 trigger/FPR/recall |
| 2 | 无 2×2 配对 | GGC | 只报总准确率 | 分不清「选得准」还是「改得准」 | 按初始对/错 × 改后对/错 建 2×2 |
| 3 | 空结果不进 Gate | GGC | 查询返回 0 行 | Gate 看不到空结果；错因被漏掉 | 对 0 行 query 单独采样，分因 |
| 4 | 本体超上下文 | NLKGQ | 完整 OWL 超过窗口 | 截断/丢公理；分数掉 | 统计 ontology token；做 slice vs full 对照 |
| 5 | snapshot 漂移 | NLKGQ | endpoint/数据更新 | 同题不同分 | 记录 `endpoint/snapshot/version`；重放同一题集 |
| 6 | wrapper 手工 | NLKGQ | 原生词汇不透明 | wrapper 词与原生谓词不同步 | wrapper→native 的映射表单测；一条 wrapper 展开多条 triple |
| 7 | 非 `rdf:type` 图 | KGVoyager | Wikidata 类自有类型体系 | class index 建不出/探索错 | `ASK { ?s a ?c }` 抽样；检查 class index 覆盖率 |
| 8 | 探索成本膨胀 | KGVoyager | 图/属性规模大 | 迭代数、墙钟、工具调用上升 | 记录 iterations / tool calls / wall-clock |
| 9 | benchmark 小且同源 | KGVoyager | 4 个 benchmark 88–108 题、3 个同源 | +3.7pp 不稳 | 换独立域；报 CI/重复运行 |
| 10 | 重写正确 ≠ 查询正确 | OBDA | SPARQL→SQL 重写成功 | SQL 跑通但语义错 | 同一查询集：原生 SQL vs 重写 SQL 的结果集比对 |
| 11 | OWL 2 QL 表达力 | OBDA | 用了 QL 外的公理 | 查询不支持/静默丢公理 | `ontop validate`；列出被拒公理 |
| 12 | 执行准确 ≠ 业务正确 | 全部 | 只看 execution accuracy | 答案集对但业务语义错 | 自域配对 + 人工抽检；报空结果分因 |
| 13 | 实体未链接 | NLKGQ / KGVoyager | 只给自然语言名 | 0 行；换别名后变非 0 | `ASK { ?e rdfs:label "…"@en }` / `skos:altLabel` |
| 14 | 聚合/去重错 | NLKGQ / KGVoyager | 非 DISTINCT、join 放大 | 数值偏大 | `COUNT(*)` vs `COUNT(DISTINCT ?x)`；不等即重复 |
| 15 | `LIMIT` 无 `ORDER BY` | NLKGQ | 998/1,000 带 LIMIT，723 条无 ORDER BY | 同 query 两次结果不同 | 同 query 连跑 5 次，`MINUS` 双向比结果集 |
| 16 | 假空（超时/放弃） | KGVoyager / NLKGQ | 超时、agent 不提交、失败记 0 | 0 行但题可解 | 查超时/放弃日志；gold query 执行一次 |
| 17 | 参考本身错 | GGC | benchmark 缺陷 | 所有系统同题错 | 执行 gold query：0 行/报错 → `gold_invalid`，剔除并报数 |

> 这 12 类里，1–3 是「生成后」、4–6 是「生成前」、7–9 是「探索」、10–11 是「重写」、12 是「度量」。04 的失败目录直接从这里取，不再另写一套。

## 3. 条件决策树

```
有关系的库 + 稳定 schema + 映射？
├─ 是 → OBDA：先 ontop validate，再跑最小查询；做去公理消融
└─ 否 → 有 KG？
        ├─ 是 → 本体进得了 context？
        │       ├─ 是 → ontology-in-context：完整 OWL + 固定 snapshot
        │       └─ 否 → agentic navigation：endpoint + class index；或先做 ontology slice
        └─ 否 → 有生成器 + 可标注错例？
                ├─ 是 → gate/correction：只改高风险；先建 2×2
                └─ 否 → 先建 KG/本体（05）；不要在空图上选路线
```

**每支的反例/停**：

| 分支 | 反例 | 停 |
|---|---|---|
| OBDA | 重写跑通但结果集与原生 SQL 不一致 | `ontop validate` 失败 / 公理被拒 → 不用这条 |
| ontology-in-context | 本体超窗口，slice 后分数掉 | token 超预算 / snapshot 不可固定 → 停 |
| agentic navigation | 图不是 `rdf:type` 体系，class index 建不出 | 探索成本 > 预算 / 无 class index → 停 |
| gate/correction | Gate 分布外，trigger 漂移 | 没有 100 条目标分布标注 → 只做全量基线，不做 gate |

## 4. 空结果分因

| 原因 | 检测 | 处置 |
|---|---|---|
| 覆盖不足（缺 tag/边） | `ASK { ?s a :Email }` / `FILTER NOT EXISTS` 计数 | 补标签/边；不要先调 prompt |
| 数据缺失（实体/快照） | `ASK { :col_email :hasTag ?t }`；对比 snapshot 计数 | 补数据/换 snapshot；记录版本 |
| 查询/链接错 | 去掉一个 triple 逐步加回；`ASK` 最小模式 | 改 query/link；不要重试同一条 |
| 过滤过严 | 去掉 `FILTER` 后的行数 vs 原行数 | 放宽阈值/分档；记录放宽理由 |
| endpoint/版本错 | 同一 query 在两个 endpoint 的结果 | 固定 endpoint/snapshot；重放 |

**规则**：0 行不是错；先分因，再决定重试/补数据/改 query。GGC 的 Gate 不看空结果，所以空结果必须单独处理。

## 5. 不可比清单（不能写进 04 的句子）

1. **不能写「98.33 > 89.9 > 64.6」**：三个指标不同（答案集匹配 / Match-Exact / F1）、数据不同、模型不同，没有头对头。
2. **不能写「GGC 的执行准确率 98.33%」**：它是答案集匹配率，不是 execution accuracy，也不是业务正确率。
3. **不能写「NLKGQ 89.9% 准确」**：89.9 是 Match（允许 superset），Exact 是 81.3；参考集还是作者修订的 3.1。
4. **不能写「KGVoyager 提升 4 倍」**：是 +3.7pp（64.6 vs 60.9），相对约 +6.1%。
5. **不能写「OBDA 查询正确」**：重写正确不等于结果正确；要做原生 SQL 对照。
6. **不能写「三条路线可以排序」**：E-21 明确不支撑排序；只能按资产条件选。
7. **不能写「空结果重试就行」**：GGC 没有空结果机制；E-02 的空结果重试是 checker 基线，不是查询路线。

## 6. 空单元与订单

| 空单元 | 订单 | 状态 |
|---|---|---|
| OBDA 的问题量/指标/成本 | P4（N）OBDA 消融；Ontop 文档 | 空 |
| 三路线头对头 | P1（M）同 KG/同题/同指标论文 | 空 |
| 空结果分布 | P2（N）空结果/失败分析 | 空 |
| 2×2 配对 | P1/P2；或自域实验（仓库外 EXP） | 空 |
| 跨路线成本口径 | 统一 token/墙钟/美元；现有只有 GGC/KGVoyager 部分 | 空 |

## 7. 与 04 的接口

- **consume B.1**：用 §0 的资产表 + §3 决策树；不写排序。
- **consume B.2**：用 §4 的空结果分因表；每条附一条检测 query。
- **consume B.3**：用 §2 的失败 1–3 + §6 的 2×2 空单元；没有 2×2 就写「未测」。
- **consume B.4**：用 §2 的失败 10–11 + Ontop 最小命令；做去公理消融。
- **E24（拟）**：本页 + E-21 收成一条「按资产条件选路线」的 E；单源/无可比性时标 `推测（综合）`。

## 8. 边界

- 三条路线各单设置；没有头对头；不能当自域基线。
- KGVoyager 4 个 benchmark 都小（88–108 题），3 个同源；+3.7pp 不是跨域效应量。
- NLKGQ 单作者 preprint、单 snapshot、单系统；89.9 是 Match 不是 Exact。
- OBDA 只支持 OWL 2 QL；不是 gate；OBDA ≠ NL→query。
- 本页是综合，不新增实验；空单元不填，不拿「工程经验」补。
