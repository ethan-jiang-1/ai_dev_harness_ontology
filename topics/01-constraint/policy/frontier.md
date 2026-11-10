# 策略层 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 优先级 |
|---|---|---|---|---|
| G1 | 领域映射来源 | 标准给等级，不给 principal/action | 标准/监管文件直接给「级别 × 角色 × 动作」表；或 2 个独立企业的策略样本 | 高 |
| G2 | 策略版本/审计回放 | 没有版本，decision 不可复现 | policy_version + tag_version + snapshot + replay 用例 | 高 |
| G3 | 第二实现/对象方向 | 读路径单实现、fail-open、只删 subject | 第二实现 + 10 条一致性用例（见 [read-path](../commit-gate/read-path.md)） | 高（与 commit-gate 共享） |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | GB/T 43697 / GB/T 35273 条款 | 已入材料卡；条款待核 | F3 | 已完成（卡） |
| N2 | XACML 3.0 / ODRL 2.2 | 已入材料卡；条款待核 | F2 条款核对 | 已完成（卡） |
| N3 | Atlas / Ranger / OpenFGA | 官方文档 + 代码 | F1/F2 实现对照 | 中 |
| N4 | 7 条测试套件 | 04 policy.json + 本页 §7 测试 | 04 C.2 从模板变测试 | 低 |
| N5 | 标签→level 映射 | GB/T 43697 + Glyph 275-leaf | F3 / 04 C.2 | 中 |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| [GB/T 43697-2024](../../../src/web/gbt-43697/gbt-43697.card.md) | 中国数据分类分级规则；level/处置 | 已入库（卡） | N1 条款 |
| [GB/T 35273-2020](../../../src/web/gbt-35273/gbt-35273.card.md) | PII 类别/处理规则 | 已入库（卡） | N1 条款 |
| [XACML 3.0](../../../src/web/oasis-xacml-3.0/oasis-xacml-3.0.card.md) | 合并算法/obligation | 已入库（卡） | N2 条款 |
| [ODRL 2.2](../../../src/web/w3c-odrl-2.2/w3c-odrl-2.2.card.md) | permission/prohibition/duty/conflict | 已入库（卡） | N2 条款 |
| Apache Atlas | 标签/分类库 | 待入库 | N3 |
| Apache Ranger | tag policy + audit | 待入库 | N3 |
| OpenFGA | ReBAC/decision/audit | 待入库 | N3 |
| OPA | 通用策略引擎（adjunct） | 已入库 | 不重复 |

## 入档判据

- 标准：条款号 +  normative/informative + 能填哪一列。
- 实现：pin commit + `file:symbol` + 测试/审计证据。
- 映射：≥1 个标准 + 1 个实现，且写清「标准要求」vs「工程选择」。
- 只有一个厂商/一个标准 → 标 `推测`，不升 E。
