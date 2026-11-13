---
status: draft
type: work-plan
updated: 2026-11-10
target: deliverables/04-worked-example
scope: w0-skeletons
---

# 04 内容供给 · W0 矩阵骨架

> 这是 [04 内容供给计划](./2026-11-10-04-content-supply.md) 的 W0 工作底稿：把 12 条承重句冻结成 12 张空表。
> 规则：每格只允许 `数+条件+锚`、`空`、`不可比+理由`；空格必须对应一条 `src` 订单或一条 stop。
> 状态：`空` / `部分` / `满`。每次填格后更新状态，不在这里写结论。
> **2026-11-10 执行**：W0 完成；W1（T2/T5/consume）、W2（T3/T4/govern）、W3（T1/T6/build）主体已落；来源入库（M1–M12）仍待。

## A1 契约 → 可消费

- **决定**：契约五格写不全时，是否停止建本体。
- **落点**：`04/body/build.md` A.1/A.5；topics `05/representation/consumability.md`。
- **表**：

| 维度 | 契约字段 | build_report 字段 | 失败类型 | 坏样本 | 状态 |
|---|---|---|---|---|---|
| consumer | consumer | consumer | 缺消费者 → 无验收对象 | S1 | 空 |
| principal | principal | principal | 缺主体 → 无法判权 | S2 | 空 |
| moment | moment | moment | 缺时刻 → 选错接缝 | S3 | 空 |
| answers/refuses | answers / refuses | expected / refused | 缺拒绝 → 全放行 | S4 | 空 |
| load | load | load.parsed | 缺加载方式 → 跑不起来 | S5 | 空 |

- **空单元订单**：M9 ODCS 字段；M8 SHACL test suite 的 load/validate 用例。
- **stop**：五格缺任一格 → 不进入 A.2。

## A2 表示档位 × 消费位置

- **决定**：按消费位置选词表/结构/逻辑哪一档。
- **落点**：`04/body/build.md` A.2；topics `05/representation/consumability.md`。
- **表**：

| 档 \ 消费 | load | validate | query | explain |
|---|---|---|---|---|
| 词表 | 空 | 空 | 空 | 空 |
| 结构表 | 空 | 空 | 空 | 空 |
| 逻辑表 | 空 | 空 | 空 | 空 |

- **空单元订单**：M8 SHACL（validate）；M10 LinkML（结构表）；OWL 2 profile（逻辑表）。
- **stop**：三档都填不出 load/validate 两列 → 只写「薄层优先 + 边界」，不写选型矩阵。

## A3 生成物可消费性

- **决定**：生成的本体/说明能不能被下游加载、校验、回答。
- **落点**：`04/body/build.md` A.5；topics `05/representation/consumability.md`。
- **表**：

| 生成物 | load | validate | answer | 失败类型 | 来源 |
|---|---|---|---|---|---|
| CASTON 公理 | 空 | 空 | 空 | 空 | CASTON digest |
| OntoDoc 说明 | 空 | 空 | 空 | 空 | OntoDoc digest |
| SFE-O 本体 | 空 | 空 | 空 | 空 | SFE-O digest |

- **空单元订单**：P5（N）可消费性论文；仓库外 EXP。
- **stop**：三关只测一关 → 写「只测了 X，不写可消费」。

## B1 路线选择

- **决定**：按资产条件选 Text2SPARQL / ontology-in-context / agentic navigation / OBDA。
- **落点**：`04/body/consume.md` B.1；topics `03/querying/compare.md`。
- **表**：

| 维度 | GGC | NLKGQ | KGVoyager | OBDA |
|---|---|---|---|---|
| 先有什么资产 | 空 | 空 | 空 | 空 |
| 本体规模 | 空 | 空 | 空 | 空 |
| 问题量 | 空 | 空 | 空 | 空 |
| 指标 | 空 | 空 | 空 | 空 |
| 成本 | 空 | 空 | 空 | 空 |
| 失败模式 | 空 | 空 | 空 | 空 |
| 可比性 | — | 空 | 空 | 空 |

- **空单元订单**：P1 头对头（M）；现有三篇 + Ontop。
- **stop**：找不到头对头 → 删「排序」句，只留条件树。

## B2 空结果分因

- **决定**：0 行时先补数据、改 query，还是重试。
- **落点**：`04/body/consume.md` B.2；topics `03/querying/compare.md`。
- **表**：

| 原因 | 检测查询 | 处置 | 失败样本 | 状态 |
|---|---|---|---|---|
| 覆盖不足（标签/边缺失） | 空 | 空 | 空 | 空 |
| 数据缺失（实体/快照） | 空 | 空 | 空 | 空 |
| 查询/链接错 | 空 | 空 | 空 | 空 |
| 过滤过严 | 空 | 空 | 空 | 空 |

- **空单元订单**：P2（N）空结果/失败分析。
- **stop**：空结果不分因 → 不写「调 prompt」。

## B3 选择性纠错

- **决定**：全量纠错还是只对高风险 query 纠错。
- **落点**：`04/body/consume.md` B.3；topics `03/querying/compare.md`。
- **表**：

| 配对 | 改对 | 改坏 | 不变 |
|---|---|---|---|
| 初始错 | 空 | 空 | 空 |
| 初始对 | 空 | 空 | 空 |

- **空单元订单**：P1/P2（N）；GGC 已有子集级。
- **stop**：没有 2×2 → 只写「全量低于选择性」，不写「改坏」。

## B4 OBDA 消融

- **决定**：要不要保留 TBox 公理。
- **落点**：`04/body/consume.md` B.4；topics `03/querying/compare.md`。
- **表**：

| 配置 | 查询集 | 正确率 | 延迟 | 生成 SQL | 状态 |
|---|---|---|---|---|---|
| 有 TBox 公理 | 空 | 空 | 空 | 空 | 空 |
| 去 TBox 公理 | 空 | 空 | 空 | 空 | 空 |

- **空单元订单**：P4（N）OBDA 消融；Ontop 已有。
- **stop**：做不了消融 → 只写重写机制，不写本体贡献。

## C1 标签 → 策略

- **决定**：标签等级能不能直接推出 allow/deny。
- **落点**：`04/body/govern.md` C.1/C.2；topics `01/policy/`。
- **表**：

| 列 | 来源 | 取值 | 不能推出什么 | 状态 |
|---|---|---|---|---|
| principal | 空 | 空 | 空 | 空 |
| action | 空 | 空 | 空 | 空 |
| resource_kind | 空 | 空 | 空 | 空 |
| condition（level/clearance） | 空 | 空 | 空 | 空 |
| effect | 空 | 空 | 空 | 空 |
| obligation | 空 | 空 | 空 | 空 |
| version | 空 | 空 | 空 | 空 |

- **空单元订单**：M1 GB/T 43697（level）；M5 Atlas（标签库）；M6 Ranger（执行/审计）。
- **stop**：只有标签、没有策略来源 → C.2 删表，只写「标签 ≠ 策略」。

## C2 冲突与默认

- **决定**：deny-overrides / default deny / skip≠allow 怎么落。
- **落点**：`04/body/govern.md` C.2；topics `01/policy/`。
- **表**：

| 语义 | XACML | ODRL | Rego/OPA | OpenFGA | 我们的选择 |
|---|---|---|---|---|---|
| 冲突 | 空 | 空 | 空 | 空 | 空 |
| 默认 | 空 | 空 | 空 | 空 | 空 |
| 义务 | 空 | 空 | 空 | 空 | 空 |
| 版本 | 空 | 空 | 空 | 空 | 空 |

- **空单元订单**：M3 ODRL；M4 XACML；M7 OpenFGA。
- **stop**：7 条规则跑不出期望 decision → 不写「策略可判定」。

## C3 读路径两实现

- **决定**：trustgraph 的单实现行为能不能外推。
- **落点**：`04/body/govern.md` C.3；topics `01/commit-gate/read-path.md`。
- **表**：

| 用例 | trustgraph | 第二实现 | 差异 | 状态 |
|---|---|---|---|---|
| subject 命中 | 空 | 空 | 空 | 空 |
| object 命中 | 空 | 空 | 空 | 空 |
| 两侧命中 | 空 | 空 | 空 | 空 |
| 都不中 | 空 | 空 | 空 | 空 |
| target 异常 | 空 | 空 | 空 | 空 |
| 缺 user_context | 空 | 空 | 空 | 空 |
| alias | 空 | 空 | 空 | 空 |
| 聚合 | 空 | 空 | 空 | 空 |
| 无策略 | 空 | 空 | 空 | 空 |
| 版本不匹配 | 空 | 空 | 空 | 空 |

- **空单元订单**：N4 sparql-guard/第二实现；AuthorizationPairs 已有。
- **stop**：第二实现不合格 → 只写单实现 + 风险。

## C4 泄漏 + 审计

- **决定**：object 方向/别名/聚合泄漏能不能测；审计能不能 replay。
- **落点**：`04/body/govern.md` C.3/C.4；topics `01/policy/`、`02/checker/output-validation.md`。
- **表**：

| 用例 | 检测查询 | 期望 | 实际 | 状态 |
|---|---|---|---|---|
| object 方向 | 空 | 空 | 空 | 空 |
| 别名 | 空 | 空 | 空 | 空 |
| 聚合推断 | 空 | 空 | 空 | 空 |
| 版本不匹配 | 空 | 空 | 空 | 空 |

- **空单元订单**：M12 OpenLineage；PROV-O（N）；trustgraph 已有。
- **stop**：object 泄漏未修 → 不上线；audit 无 schema → 只写字段表。

## D1 跨段传播

- **决定**：单段指标看不见的故障，在哪一段放大、在哪看得见。
- **落点**：`04/sections/boundaries.md`、`04/body/govern.md` C.5；topics `06/metrics/propagation.md`。
- **表**：

| 故障 | build | query | govern | 观测信号 | 状态 |
|---|---|---|---|---|---|
| 坏 shape | 空 | 空 | 空 | 空 | 空 |
| 缺 tag | 空 | 空 | 空 | 空 | 空 |
| 错 level | 空 | 空 | 空 | 空 | 空 |
| 空结果 | 空 | 空 | 空 | 空 | 空 |
| 错 join | 空 | 空 | 空 | 空 | 空 |
| policy skip | 空 | 空 | 空 | 空 | 空 |
| object 泄漏 | 空 | 空 | 空 | 空 | 空 |
| 快照过期 | 空 | 空 | 空 | 空 | 空 |
| 版本不匹配 | 空 | 空 | 空 | 空 | 空 |
| 超时 | 空 | 空 | 空 | 空 | 空 |

- **空单元订单**：M12 OpenLineage/Marquez；P4（N）；E-06/E-05 已有。
- **stop**：一条传播路径都指不出 → 只写「单段指标有盲区」，不写「传播矩阵」。

## 进度

| 表 | 状态 | 已填格 | 空单元订单 | 下一步 |
|---|---|---|---|---|
| A1 | 部分 | 5 | M9/M8 | 三关与 6 项映射已落；来源待入库 |
| A2 | 部分 | 6/12 | M8/M10 | 3×4 矩阵已落；成本列是估算 |
| A3 | 部分 | 0 | P5 | 协议已写；CASTON/OntoDoc 未试跑 |
| B1 | 满 | 8/8 | P1 | 4×8 矩阵 + 决策树已落；头对头待 P1 |
| B2 | 满 | 6/6 | P2 | 空结果分因 6 类已落；分布待 P2 |
| B3 | 部分 | 0/4 | P1/P2 | 2×2 骨架已写；矩阵空 |
| B4 | 部分 | 0/2 | P4 | 消融步骤已写；结果空 |
| C1 | 部分 | 5/7 | M1/M5/M6 | schema 已落；领域映射待标准 |
| C2 | 满 | 7/7 | M3/M4/M7 | 10 条测试已落；T9 优先级空洞 |
| C3 | 部分 | 6/10 | N4 | trustgraph 6 条已核；第二实现空 |
| C4 | 部分 | 3/4 | M12 | 12 条泄漏用例已落；replay 未跑 |
| D1 | 部分 | 10/10 | M12/P4 | 10 类×3 段矩阵已落；无注入实验 |
