---
status: draft
updated: 2026-11-13
rq: [RQ1, RQ5]
evidence: [E-01, E-08, E-14]
---

# 编译：把检索前的整理当成供给层

> **2026-11-11 素材重置注**：本页两条线索中 CAI（E-01/E-08/E-14）为 `admitted`；**Grid Agents（2611.03534，03-L9/03-L11）因厂商自证未过准入门已移出**（[审计](../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534)），受监管支线判断（F5/F8–F11）同步降为`推测（源已撤回）`，仅作工程结构参考，不作现役实证。
>
> **薄页（<2 篇独立来源）**：本页判断只作候选/边界，**不承担稳定判断**；引用时必须带「单来源」限定。

> 在检索之前把源文档加工成带类型/版本/lineage 的工件；这里问「编译值不值、在什么条件下省预算」，不负责投影成文（[projection](../projection/README.md)）。

## 状态

| 项 | 值 |
|---|---|
| 已发现 | 11 条（[findings](./findings.md)） |
| 未发现 / 开放 | 8 条（[frontier](./frontier.md)） |
| 下一步 | 3 个候选 · 7 个检索式（[frontier](./frontier.md)） |
| 最后扫描 | 2026-11-08 |
| 覆盖 | 编译工件（claim-leaf/树/图/wiki）、成本模型、受监管知识系统；不含投影文本（03/projection）与判定器（02） |

## 当前判断

- **编译不解决准确率。** 强词法 harness 下结构化工件无可检出增益；PageIndex 在 FRAMES 规模实测为负（小规模中性；10^5 的 75% routing 是解析模型，不是实测）。`已核`
- **claim-leaf 的收益是条件性 token 节省。** 充分 −91%、不充分 +1.9%、平均 −38%；2% 是无限视野，有限视野 `p_min=2%+c/(0.929Q)`。`已核`
- **省 token 可能用轮次/时延换。** 配对子集时延约 3×（仅 7 题）；时延硬约束时不要买。`已核`
- **决策门的结果不能和 hit/miss 对读。** E3 arm mean 有证据 −52%、无证据 −30%；140→30 s 是 gate arm 的均值，不是未编译基线。`已核`
- **盈亏平衡先看 miss，不看 hit。** miss 端 ±1.5pp 让 `p_h*` 在 0.4–3.6% 间移动，hit 端只动 2.0–2.1%（解析推导）。`已核`
- **「编译」不是一种东西（待重证）。** CAI 编译证据（claim+span），无 solver；原 Grid 线编译法规知识系统 + solver，但 2611.03534 已移出，`03-L9` 已撤回。`推测`（原 Grid 源已撤回）
- **Grid 对最强 agent baseline 只有 0.5pp 优势（原源已撤回）。** 原技术报告数字仅作历史/单报告参考，不再作现役定锚。`推测`（源已撤回）
- **受监管支线的可审计性契约（工程配方，待新源）。** citation+拒答、state_hash/study_type/solver_version 与记忆/决策点签核源自已移出的 Grid 报告，保留为架构配方参考，不作实证；客户指标亦无基线。`推测`（源已撤回）

## 文件地图

| 想知道 | 去 |
|---|---|
| 三层结构/六段流水线/三种服务模式 | [mechanism](./mechanism.md) |
| 每条判断的证据/数字/条件 | [findings](./findings.md) |
| 盈亏平衡敏感度（为什么先量 miss） | [F7](./findings/economics.md#f7) |
| 决策门 E3 的 −52%/−30% 与 140→30 s | [F3](./findings/economics.md#f3) |
| Grid 99.9% 与 near baseline | [F5](./findings/regulatory.md#f5) |
| 受监管支线的接口/stop/拒答/客户指标 | [F8](./findings/regulatory.md#f8) · [F9](./findings/regulatory.md#f9) · [F10](./findings/regulatory.md#f10) · [F11](./findings/regulatory.md#f11) |
| 还缺什么、下一步看什么 | [frontier](./frontier.md) |
| CAI 原卡 | `src/papers/2610.41172-context-as-infrastructure/card.md` · [digest](../../../src/papers/2610.41172-context-as-infrastructure/digest.md) |
| Grid 原卡（已移出） | [审计 tombstone](../../../meta/audits/2026-11-11-source-purge.md#src-2611-03534)（原 2611.03534 已移出） |

## 边界

- **编译不是检索器。** 树是 carrier，不是 router；检索仍用词法/flat evidence。
- **本体在 CAI 里未被测量。** 不能拿 CAI 证明本体有用/无用；它只给 ledger 位置。
- **与投影的分界**：编译投影证据；投影投影领域知识（规则/手册/设备）。

## 关联

- 派：[03 知识](../README.md) · 结论：[E-01 / E-08 / E-14](../../conclusions.md)
- 相邻：[projection](../projection/README.md) · [02 evidence](../../02-judgment/evidence/README.md)
- 成本：[06-measure/feasibility](../../06-measure/feasibility/README.md)
