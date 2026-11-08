# 推理期约束 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | axiom 覆盖率 | 没有 axiom 的动作只能放行/fallback | 每域统计 + 消融 | OntoAct 后续 | 高 |
| G2 | 真实传感器噪声下的三值条件 | 模拟环境太干净 | 真实工厂/临床数据 | 工业部署 | 高 |
| G3 | 推理期 vs 动作期的重复收费 | 同一本体判两次 | 共享判据/缓存 | 01 三位置 | 中 |
| G4 | 阻断的可审计信号 | 模型只是「换个说法」 | 结构化 condition report | OntoAct / checker | 中 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | axiom 覆盖率 | `ontology axiom coverage agent verification` | F4 / G1 | 中 |
| N2 | 噪声下三值条件 | `three-valued ontology verification sensor noise` | F3 / G2 | 高 |
| N3 | 推理/动作共享判据 | `shared ontology guardrail reasoning action` | F1 / G3 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | OntoAct / 多 agent 深读 | F1–F4 成形；G1–G4 明确 | 先做 G1/G4 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| axiom 覆盖率统计 | 决定是否选择性护栏 | 待扫描 | N1 |
| 结构化 condition report | 可审计 | 待扫描 | N3 |
