# 落地经济学 · 未发现与下一步

## 未发现（G）

| ID | 缺什么 | 为什么重要 | 关闭它需要什么 | 去哪找 | 优先级 |
|---|---|---|---|---|---|
| G1 | 部署层回报 | 治理/上手/审计仍定性 | 部署测量协议 | CAI/N&D | 高 |
| G2 | false-veto / false-defer | 护栏/授权的隐性成本 | 标注 blocked decisions | POLAR/Commit Boundary | 高 |
| G3 | 维护成本 | 本体/投影/registry 长期人工 | 工时测量 | 工程复盘 | 高 |
| G4 | 自有配置方差 | 54% 是别人的估计 | 重复采样 | experiments | 中 |
| G5 | 跨域迁移 | 工业/金融/医学/电网边界不同 | 统一对照 | 多域案例 | 中 |

## 下一步（N）

| ID | 看什么 | 来源 / 检索式 | 预期改变 | 成本 |
|---|---|---|---|---|
| N1 | 部署指标 | `deployment metrics ontology governance` | F1 / G1 | 高 |
| N2 | false-veto 标注 | POLAR block log；`false veto guardrail annotation` | F1/F3 / G2 | 中 |
| N3 | 维护工时 | `ontology maintenance cost case study` | F1 / G3 | 中 |

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-08 | 22 篇综合 | F1–F6 成形；G1–G5 明确 | 先做 G1/G2/G3 |
| 2026-11-08 | G-X 吸收复核（CAI/POLAR/CASEL） | 单位经济学/NPV、校准协议、γ CI stop 已补进 mechanism/findings；其余机制细节归各派 | 复跑 G-X |

## digest 吸收边界（G-X）

> 本页引用一律写 arXiv 编号或论文名，不用审计矩阵的 D-ID——`absorption-matrix.md` 的 D-03、D-06–D-10 与 [digest-ledger](../../../meta/full-audit/digest-ledger.md) 不一致（例：矩阵 D-03=POLAR、D-06=CASEL、D-10=Grid；ledger D-03=CASEL、D-06=FIRME、D-10=POLAR）。矩阵侧待整表对齐，不在本页范围。

| digest 工程发现 | 状态 | 落在哪 / 为什么不进来 |
|---|---|---|
| CAI `p_min`/`c`/`Q`、miss 敏感度、φ 抽样 100→400、3× 时延（仅 7 题） | 吸收 | [mechanism §三个可算的盈亏平衡](./mechanism.md#三个可算的盈亏平衡)、§实施与客户价值 |
| POLAR 人日（Layer A 2–5、Layer B 1–2 人周）、φ/τ 账本字段、false-veto stop | 吸收（成本/账本/stop 视角） | [mechanism §组织/成本](./mechanism.md#组织成本)、[§数据/接口](./mechanism.md#数据接口)、§stop condition |
| POLAR Layer A/B schema、DecisionPolicy 接口、反向搜索参数 | 不重复 | 控制器细节已由 [01/action-gate](../../01-constraint/action-gate/mechanism.md) 吸收 |
| CASEL E4 单位经济学、NPV 决策线 | 吸收 | [mechanism §单位经济学](./mechanism.md#单位经济学e4把单价代进公式)、[findings F5](./findings.md) |
| CASEL 校准协议（Eq(5) 40k/160k、disjoint、one record/trajectory、κ≥0.6） | 吸收 | [mechanism §数据/接口](./mechanism.md#数据接口)、[findings F6](./findings.md) |
| CASEL γ CI stop（±3pp、只上静态 gate、AUC 未显著更低） | 吸收 | [mechanism §stop condition](./mechanism.md#stop-condition) |
| CASEL `c_base` 锚点、动作混合 58/28/14、approve `ĉ≥0.55` | 不重复 | 控制器参数已由 [01/action-gate](../../01-constraint/action-gate/mechanism.md) 吸收；本页只在账本与分母敏感性里用到动作混合 |
| CAI 工具 schema、topN=20/k=100/anchor 20 | 不适用 | 检索参数归 [03/compilation](../../03-knowledge/compilation/mechanism.md) |

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| 部署测量协议 | 补治理回报 | 待扫描 | N1 |
| false-veto 标注 | 护栏隐性成本 | 待扫描 | N2 |
