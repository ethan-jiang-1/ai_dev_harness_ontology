---
status: draft
updated: 2026-11-08
rq: [RQ1, RQ5]
evidence: [E-01, E-08, E-14]
---

# 编译：把检索前的整理当成供给层

> 在检索之前把源文档加工成带类型/版本/lineage 的工件；这里问「编译值不值、在什么条件下省预算」，不负责投影成文（[projection](../projection/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 6 条（[findings](./findings.md)） |
| 未发现 / 开放 | 6 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选/检索式（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 编译工件（claim-leaf/树/图/wiki）、成本模型、受监管知识系统；不含投影文本（03/projection）与判定器（02） |

## 当前判断

- **编译不解决准确率。** 强词法 harness 下结构化工件无可检出增益；PageIndex 大规模负面。`已核`
- **claim-leaf 的收益是条件性 token 节省。** 充分 −91%、不充分 +1.9%、平均 −38%；2% 是无限视野，有限视野 `p_min=2%+c/(0.929Q)`。`已核`
- **省 token 可能用轮次/时延换。** 配对子集时延约 3×；时延硬约束时不要买。`已核`
- **「编译」不是一种东西。** CAI 编译证据（claim+span）；Grid 编译法规知识系统 + solver。共同点是证据可追溯、数字不靠模型。`已核`

## 文件地图

| 想知道 | 去 |
|---|---|
| 三层结构/六段流水线/三种服务模式 | [mechanism](./mechanism.md) |
| 每条判断的证据/数字/条件 | [findings](./findings.md) |
| 还缺什么、下一步看什么 | [frontier](./frontier.md) |
| CAI 原卡 | `src/papers/2610.41172-context-as-infrastructure/card.md` · [digest](../../../src/papers/2610.41172-context-as-infrastructure/digest.md) |
| Grid 原卡 | `src/papers/2611.03534-power-system-agentic/card.md` · [digest](../../../src/papers/2611.03534-power-system-agentic/digest.md) |

## 边界

- **编译不是检索器。** 树是 carrier，不是 router；检索仍用词法/flat evidence。
- **本体在 CAI 里未被测量。** 不能拿 CAI 证明本体有用/无用；它只给 ledger 位置。
- **与投影的分界**：编译投影证据；投影投影领域知识（规则/手册/设备）。

## 关联

- 派：[03 知识](../README.md) · 结论：[E-01 / E-08 / E-14](../../conclusions.md)
- 相邻：[projection](../projection/README.md) · [02 evidence](../../02-judgment/evidence/README.md)
- 成本：[06-measure/feasibility](../../06-measure/feasibility/README.md)
