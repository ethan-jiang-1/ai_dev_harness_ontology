# 生成 · 未发现与下一步

> `G` = gap（还没站住的判断）；`N` = next（下一步看什么）。稳定判断回 [findings](./findings.md)；参数/接口/stop 回 [mechanism](./mechanism.md)。

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 可消费性怎么测 | 生成结构能否被判定器/agent 用 | 加载/解释/复现的评测 | 02 checker / 05 lifecycle | 高 |
| G2 | 最小人工种子 | 冷启动成本：Evontree 要 15 根概念、OntoDoc 要实例数据 | 种子阶梯实验 | Evontree/OntoDoc | 中 |
| G3 | 来源标记进判定权重 | 来源标记是判定器继承可信度的前提；digest E3 有建议字段（`provenance_triples`/`generator_version`/`evidence_span`，`推测`，非论文产物），论文侧只有 assumption 引用 triple 编号、互评匿名化、`ConfirmValue` 分级；加权是否降误判没测 | 来源标注 + 加权判定的对照实验 | 02/05 | 高 |
| G4 | 下游任务收益 | 说明更全 ≠ 任务更好 | 生成前后对照 | OntoDoc 后续 | 高 |
| G5 | 高频模式被写成约束（「把常见当应然」） | 五条 digest 都没测；这是选约束时的常见担心，不是已核失效 | 生成约束的频次–正确率曲线 | 无（待检索） | 中 |
| G6 | 增量重生成的组织/成本 | OntoDoc 明确写「未实现」，其余三篇未报告；频繁变更时维护可能吃掉收益 | 变更集重跑实验 + 工时记录 | OntoDoc / 05 lifecycle | 中 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | 可消费性评测 | `ontology generation consumability checker` | F1/F3 / G1 | 中 |
| N2 | 来源加权 | `provenance weighted ontology constraint` | F5 / G3 | 中 |
| N3 | 下游对照 | `ontology description downstream task` | F2/F3 / G4 | 高 |
| N4 | 增量重生成 | `incremental ontology description regeneration change set` | G6 / mechanism 的维护段 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | OntoDoc/ReX-GG/Peeling/Evontree | F1–F5、G1–G6 成形 | 先做 G1/G4 |
| 2026-11-08 | 四条 digest 反向核对（T-12） | 删掉 SFE-O 被误挂的「覆盖窄/维护贵」与两条无测量失效；补 4 条工程发现（接口/参数/成本/stop/客户指标）；G5/G6 新增 | 按 N1 先跑可消费性 |
| 2026-11-08 | T-12 二级残留（复跑前） | F2 条件改为「LLM judge 评 naive/模板，人工只评 OntoDoc」；F5/G3/README 把 E3 建议 schema 从「论文产物/已核字段」降级为 `推测`；补 Evontree +3.1/+3.7 与 implicit/mix 安全/通用能力（F6） | 复跑 G-X |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 可消费性基准 | 补核心空缺 | 待扫描 | N1 |
| 来源加权判定 | 来源字段只有 E3 建议，缺效果证据 | 待扫描 | N2 |
| 增量重生成/变更成本 | 维护可能吃掉全部收益 | 待扫描 | N4 |
