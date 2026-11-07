---
status: draft
updated: 2026-11-07
quality: C
based_on: card.md
claims: [E-05]
---

# Constraining the Commit Boundary · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**要做一个「落盘前授权门」，按这个顺序：**

1. **先分两类证据：可推理的 vs 可授权的。** `P_active` 可以包含 `UNVERIFIED`，让 Planner 继续工作；`P_auth(q_m, ω)` 只放 claim-specific 授权证据。**这是整个架构的核心。**
2. **定义 mutation class 与 required claims。** merge/split/un-merge 各自需要哪些命题；由 supervisor 从 policy 派生 `q_m`，Planner 不能替换/削弱。
3. **每条证据记录角色。** support / contradiction / unresolved indication；角色是命题级的，不是全局标签。
4. **promotion 必须独立审计。** 不接受 Planner 置信度、LLM `verified` 标签、多个 `UNVERIFIED` 重复；不从「没检测到冲突」推断支持。
5. **同源检索不算独立确认。** 如果多条观察共享 query/hypothesis/source/derivation，不能当 independent corroboration；要沿记录链排除 shadow。
6. **两阶段 + 原子 commit。** Phase 1 授权 proposed mutation；Phase 2 验证 realized candidate；commit 时 scope/version/graph/evidence 必须在同一 snapshot。
7. **状态聚合 fail-closed。** `BREACH` > `UNKNOWN` > `PASS`；缺证据/未解决冲突 → defer，不是放行。
8. **把「不知道」与「证明为假」分开。** `UNKNOWN_EVIDENCE` 阻止不可逆变更，但不是「这两个实体不同」的证明。
9. **承认上游漏洞。** 架构不控制 hypothesis-conditioned retrieval；dependency-aware lineage 是 future work。上线前要单独评估这个漏洞。

## 实用意义

它解决的操作问题：

- **「agent 检索到的东西看起来支持，但其实是它自己的假设带出来的。」** → 同源 evidence 不算独立确认；claim-specific promotion。
- **「UNVERIFIED 数据被当成已授权。」** → 状态分层：admission ≠ authorization。
- **「图合并了一半，发现版本过期。」** → 两阶段 + version/scope 检查 + 原子 commit。
- **「冲突没解决，但系统还是提交了。」** → `UNKNOWN_EVIDENCE`/`BREACH` 阻止 PASS。
- **「审批记录说不清依据。」** → promotion 记录命题/角色/provenance/validation basis/version。
- **「合规要求可追溯。」** → 条件性保证 + 审计记录；但不要宣称语义正确。

**何时用**：身份变更/图合并/主数据写入；需要审计；有 domain policy；能实现 promotion 流程。

**何时别用**：没有 domain policy；promotion 只能靠 LLM 自评；无法控制写路径；需要语义真值保证（本文不提供）；依赖链无法记录。

## 质量评估

- **证据类型**：概念架构（`已核` 到「作者提出了这套契约」；无实现/实证）。
- **样本与对照**：无；第 8 节只是 proposed evaluation protocol。
- **优点**：状态语义清晰；promotion 契约具体；两阶段/版本/scope 完整；诚实划边界（dependency-aware flow 未解决）。
- **主要威胁**：无实现；无量化；promotion correctness 依赖外部；domain policy 编写成本未测；不控制上游 hypothesis-conditioned retrieval。
- **`quality: C` 理由**：概念贡献强，但没有实证；只能当设计规范，不能当效果证据。

## 洞察

1. **「可推理」≠「可授权」是全文最有价值的区分。** 大多数 agent 记忆/图变更系统把「检索到」当「可写入」；这篇把它拆成两个状态机。`已核`（概念）
2. **`UNVERIFIED` 不是 verdict。** 它是 admission-level 状态；授权资格是命题级、policy 级、时间级的。`已核`
3. **「没检测到冲突」不是 positive support。** 这是很多审核系统的隐性错误；本文明确禁止。`已核`
4. **假设诱导的检索不是独立确认。** 这是 agentic ER 的核心失败模式；同源 query/hypothesis 的多个结果不能互相印证。`已核`
5. **两阶段 + 原子 commit 是工程上可复用的骨架。** Phase 1 授权 proposed mutation，Phase 2 验证 realized candidate；版本/scope 同 snapshot。`已核`（设计）
6. **Fail-closed 的语义要写清：UNKNOWN 阻止的是「授权未建立」，不是「证明为假」。** 这避免了「不知道就拒绝」与「不知道就放行」的混淆。`已核`
7. **条件性保证的七条假设，就是部署清单。** 任何一条不成立，commit invariant 就不成立；不要把它当定理。`已核`
8. **最难的漏洞在上游。** Dependency-aware evidence lineage 不在架构内；没有它，promotion 仍可能被 hypothesis-conditioned retrieval 污染。`已核`（作者自述）

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| Domain policy | 每域一次性 | mutation class、required claims、constraints；需专家 |
| Promotion 流程 | 集成一次性 | 命题级评估、provenance、角色、version |
| 两阶段 supervisor | 集成一次性 | Phase 1/2、snapshot、scope/version |
| 审计存储 | 持续 | 证据、角色、validation basis、policy version |
| 维护 | policy/本体变更 | 重新验证；版本管理 |

**使能条件**：可控写路径；domain policy；promotion 流程；版本化存储；能记录 provenance。

**2022 年做会卡在哪**：agentic ER/图变更不普遍；没有成熟的 evidence promotion 工具；但契约本身不依赖模型版本。

**反向条件**：没有 policy；promotion 靠 LLM 自评；写路径不可控；依赖链无法记录；需要语义真值保证。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **E-05** | 支撑「本体承担对齐与印证条件」：commit gate 用 claim-specific 命题/证据，不让本体自由推理。 |
| **P1** | 强支撑：价值在约束/授权，不在知识注入。 |
| **P2** | 强支撑：同一证据，换 commit contract，行为不同。 |
| [commit-gate](../../../topics/01-constraint/commit-gate/README.md) | 核心文献；机制细节回 card。 |
| [04 identity](../../../topics/04-state/identity/README.md) | 与 FIRME 的 identity registry 相接：FIRME 解决「谁是同一实体」，本文解决「什么时候有权改」。 |

## 不可迁移

- 概念架构，无实现/实证；不能引用为「有效」。
- 依赖 domain policy 与 promotion 正确性；两者都不是本文解决的。
- 不控制 hypothesis-conditioned retrieval；上游依赖链未解决。
- 不保护 unmanaged write path / 系统性 misclassification / false authoritative source。
- 没有量化评估；第 8 节只是协议。

## 开放问题

- 是否有后续实现/实证？目前正文明确无。
- Promotion 的正确性如何验证？需要独立标注/审计。
- Dependency-aware lineage 能否落地？这是整个架构的上游漏洞。
- Domain policy 的编写成本与一致性；谁来维护？
- 与 SHACL/transaction/versioning 的工程集成细节。
- 在 FIRME 这类记忆写入上，commit gate 的 false-defer 率会是多少？
