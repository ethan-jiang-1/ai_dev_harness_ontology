# 推理期约束 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | axiom 覆盖率 | 没有 axiom 的动作只能放行/fallback；覆盖率决定是否选择性护栏 | 每域统计 + 消融 | OntoAct §9；自有域 | 高 |
| G2 | 真实传感器噪声下的三值条件 | 模拟环境太干净；噪声下 ? 可能洪水（`推测`） | 真实工厂/临床数据；? 比例与 false-block | 工业部署 | 高 |
| G3 | 知识构造成本 vs eval 成本 | digest 明确列为未解决：什么规模下值得 | 统计构造 LLM 调用 + 专家人日，和 eval token/成功率对比 | OntoAct §9；自有试点 | 中 |
| G4 | condition report 能否标准化为审计格式 | block 已有 failed_conditions/unresolved，但还不是通用审计格式 | 定义 report schema，跨域复用测试 | OntoAct §9；02/checker | 中 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | axiom 覆盖率 | `ontology axiom coverage agent verification` | F4 / G1 | 中 |
| N2 | 噪声下三值条件 | `three-valued ontology verification sensor noise` | F3 / G2 | 高 |
| N3 | 结构化 condition report 的审计格式 | `structured verification report ontology audit` | G4 | 低 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | OntoAct / 多 agent 深读 + digest 对齐 | F1–F4 重写；G1–G4 对齐 digest §9 | 先做 G1/G4 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| axiom 覆盖率统计 | 决定是否选择性护栏 | 待扫描 | N1 |
| 结构化 condition report | 可审计 | 待扫描 | N3 |
