---
status: draft
updated: 2026-11-08
quality: C
based_on: card.md
claims: [E-05]
---

# Commit Boundary：能推理的证据，不等于能授权的证据

> 这篇消化不假设你读过论文。先讲清「提交边界」是什么，再看两阶段契约、三态、条件性保证与边界。

## 0. 三句话

1. **它问什么**：agentic entity resolution 里，错误身份假设会条件化后续检索，检索结果又像「确认」；这些证据能不能直接授权持久化变更？
2. **它怎么做**：把「推理可用的证据」与「有权授权变更的证据」分开；`UNVERIFIED` 只表示可进推理，不等于授权资格；需要 claim-specific promotion；两阶段 supervisor 只在所有必需命题都有授权证据、冲突解决、scope/version 有效时允许 commit。
3. **它发现什么**：这不是实证，是**概念架构**；没有实现、没有量化。价值在状态语义与授权契约，不在效果。

## 1. 它解决什么问题

### 1.1 背景

Entity resolution（ER）：判断两个 mention 是不是同一实体。agentic ER 会计划动作、检索证据、修订假设、提出图变更。

危险模式：一个错误身份假设 → 条件化后续检索 → 检索结果看起来像「确认」 → 图变更被授权。初始错误被自我强化。

### 1.2 论文的立场

不要问「这条证据能不能支持推理」，要问「它有没有资格授权这次持久化变更」。两者是两个状态机。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **commit boundary** | 推理证据与授权证据之间的边界；越过它才会改持久化状态。 |
| **UNVERIFIED** | 可进 Planner 推理，但不是 positive authorization support。 |
| **claim-specific promotion** | 把某条观察提升为「对某个具体命题有授权资格」的过程。 |
| **required claims q_m** | 这次 mutation 必须满足的命题集合。 |
| **P_auth(q_m, ω)** | 对命题 q_m、观察域 ω、policy version 有授权资格的证据。 |
| **PASS / BREACH / UNKNOWN_EVIDENCE** | 三态：通过 / 违反 / 证据不足。 |
| **scope / version** | 证据的适用范围与版本；commit 时必须仍有效。 |
| **DIO/ODI** | 数字身份优化 / 数字身份本体；本文用来组织诊断与约束。 |

## 3. 它怎么做

### 3.1 四段

1. **Diagnostic-to-constraint**：DIO/ODI 的 RRF/SCF/TRF/CAF 诊断 → domain-governed binding μΩ → identity-preserving constraints V_E。
2. **Mutation context**：Planner 提出 mutation m；supervisor 从 m、V_E、policy version 派生 required claims q_m。
3. **Evidence admission**：Observation → Quarantine → P_active (`UNVERIFIED`) → claim-specific promotion → P_auth(q_m, ω)。
4. **Two-phase supervisor + protected commit**：Phase 1 授权 proposed mutation；Phase 2 验证 realized candidate；commit gate 要求 PASS + ScopeValid + VersionsValid。

### 3.2 状态

| 状态 | 含义 |
|---|---|
| `QUARANTINE_EVIDENCE` | 有 admission conflict/indeterminate，暂不可见 |
| `UNVERIFIED` | 可进 Planner 推理；不是 positive authorization support |
| `P_auth(q_m, ω)` | 对特定命题、观察域、policy version 有授权资格 |
| `PASS` / `BREACH` / `UNKNOWN_EVIDENCE` | 三态结论；`BREACH` > `UNKNOWN` > `PASS` |

### 3.3 最小 promotion 契约

1. 评估**具体命题**，不是文档相关性/查询匹配/合理性。
2. 记录 provenance、命题、角色、时间适用性、validation basis、policy/validator version。
3. 不把 Planner 置信度、LLM `verified` 标签、多个 `UNVERIFIED` 重复当授权证据。
4. **不因为 hypothesis 诱导了检索就把结果当独立确认**；同源 query/hypothesis/source 不算 corroboration。
5. 不从「没检测到冲突」推断 positive support。
6. 不引用 shadow candidate 或引用 shadow 内容的 claim；要沿记录链传递。
7. 只在声明的命题/角色/适用性上 eligible。

### 3.4 一个具体例子

两个「张伟」看起来是同一人：

- Planner 假设：同一人；检索到同一邮箱、同一公司。
- 但邮箱/公司都是 hypothesis 诱导出来的同源记录；`UNVERIFIED` 可以用于推理，但不能授权 merge。
- 需要 claim-specific promotion：例如「身份证号一致」这条命题有授权证据；冲突（地址不同）已解决；scope/version 有效。
- 如果只有 `UNVERIFIED`，commit gate 返回 `UNKNOWN_EVIDENCE`，defer，而不是 merge。

## 4. 结果：数字与条件

| 数字 | 条件 | 说明 |
|---|---|---|
| 无 | 概念架构，无实现/实验 | 所有保证是条件性的 |

**没有准确率/延迟/成本数字。** 第 8 节只是 proposed evaluation protocol。

## 5. 这些数字不能说明什么

1. **不是实证。** 没有实现；不能引用为「有效」。
2. **不是语义正确性定理。** 保证依赖 7 条假设：domain policy adequacy、promotion correctness、fail-closed、enforced write path、derived claims、scope/version integrity、recorded-basis integrity。
3. **不阻止错误假设。** 也不消除 hypothesis-conditioned retrieval；dependency-aware lineage 是 future work。
4. **不保护 unmanaged write path / 系统性 misclassification / false authoritative source。**
5. **没有量化评估。** 不能比较 false-defer / false-approve 率。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先分两类证据。** 可推理的 vs 可授权的；`UNVERIFIED` 可以进 Planner，但不能当授权证据。
2. **定义 mutation class 与 required claims。** merge/split/un-merge 各自需要哪些命题；supervisor 派生 q_m。
3. **每条证据记录角色。** support / contradiction / unresolved indication；命题级，不是全局标签。
4. **promotion 必须独立审计。** 不接受 Planner 置信度、LLM `verified`、多个 `UNVERIFIED` 重复；不从「没冲突」推断支持。
5. **同源检索不算独立确认。** 共享 query/hypothesis/source/derivation 的观察不能互相印证。
6. **两阶段 + 原子 commit。** Phase 1 授权 proposed mutation；Phase 2 验证 realized candidate；scope/version/graph/evidence 同 snapshot。
7. **状态聚合 fail-closed。** `BREACH` > `UNKNOWN` > `PASS`；缺证据/未解决冲突 → defer。
8. **把「不知道」与「证明为假」分开。** `UNKNOWN_EVIDENCE` 阻止不可逆变更，但不是「两个实体不同」的证明。
9. **承认上游漏洞。** 不控制 hypothesis-conditioned retrieval；dependency-aware lineage 要单独评估。

### 6.2 成本与使能

| 成本 | 一次性/每次 | 说明 |
|---|---|---|
| Domain policy | 每域一次性 | mutation class、required claims、constraints；需专家 |
| Promotion 流程 | 集成一次性 | 命题级评估、provenance、角色、version |
| 两阶段 supervisor | 集成一次性 | Phase 1/2、snapshot、scope/version |
| 审计存储 | 持续 | 证据、角色、validation basis、policy version |
| 维护 | policy/本体变更 | 重新验证；版本管理 |

**使能条件**：可控写路径；domain policy；promotion 流程；版本化存储；能记录 provenance。

### 6.3 何时用 / 何时别用

**用**：身份变更/图合并/主数据写入；需要审计；有 domain policy；能实现 promotion 流程。

**别用**：没有 policy；promotion 只能靠 LLM 自评；无法控制写路径；需要语义真值保证；依赖链无法记录。

## 7. 质量与边界

- **证据类型**：概念架构（无实现/实证）。
- **强项**：状态语义清晰；promotion 契约具体；两阶段/版本/scope 完整；诚实划边界（dependency-aware flow 未解决）。
- **主要威胁**：无实现；无量化；promotion correctness 依赖外部；domain policy 成本未测；不控制上游 hypothesis-conditioned retrieval。
- **`quality: C`**：概念贡献强，但没有实证；只能当设计规范，不能当效果证据。

## 8. 与仓库判断的关系

- **E-05（已核）**：本体承担对齐与印证条件；commit gate 用 claim-specific 命题/证据，不让本体自由推理。
- **01-L13**：可推理 ≠ 可授权；`UNVERIFIED` 不能当 positive authorization support。
- **01-L14**：同源检索不算独立确认；「没检测到冲突」不是 positive support。
- **P1/P2**：价值在约束/授权；同一证据，换 commit contract，行为不同。

## 9. 还没解决 / 下一步

- **是否有后续实现/实证？** 目前正文明确无。
- **Promotion 正确性如何验证？** 需要独立标注/审计。
- **Dependency-aware lineage 能否落地？** 这是上游漏洞。
- **Domain policy 的编写成本与一致性？**
- **与 SHACL/transaction/versioning 的工程集成细节？**
- **在 FIRME 这类记忆写入上，false-defer 率会是多少？**

## 10. 原文

- arXiv:2610.37407
- PDF：`src/papers/2610.37407-commit-boundary/`
- 代码/数据：无实现。
