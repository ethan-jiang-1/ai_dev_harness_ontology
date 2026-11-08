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

### 4.1 为什么授权要单独状态机

- **推理证据与授权证据的目标不同。** 前者要「能支持假设」，后者要「证据齐、冲突清、版本有效」；混成一个判据会过度保守或错误落盘。
- **同源检索不是独立确认。** 初始错误假设会条件化后续检索，结果看起来像确认，其实共享同一个 query/hypothesis；把它当 corroboration 会自我强化。
- **保证是条件性的。** 它依赖 domain policy、promotion 正确、强制执行、scope/version 完整；架构只保证「按 contract 执行」，不保证 contract 本身对。
- **没有实现。** 所以它只能作设计规范，不能当效果证据；false-defer 率未知。

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

### 6.4 最小落地清单

1. **先写 domain policy。** mutation class、required claims、constraints；没有 policy，状态机无法判。
2. **mutation 派生 required claims。** merge/split/un-merge 各需要哪些命题；supervisor 从 m、V_E、policy version 派生 q_m。
3. **证据分状态。** QUARANTINE → UNVERIFIED → claim-specific P_auth；UNVERIFIED 可进推理，不能授权。
4. **promotion 命题级。** 记录 provenance、角色、时间适用性、validation basis、version；不接受 Planner 置信度/LLM verified/重复 UNVERIFIED。
5. **同源不算确认。** 共享 query/hypothesis/source/derivation 的观察不能互相印证。
6. **两阶段 + 原子 commit。** Phase 1 授权 proposed；Phase 2 验证 realized；scope/version/graph/evidence 同 snapshot。
7. **状态聚合 fail-closed。** BREACH > UNKNOWN > PASS；缺证据/未解决冲突 → defer。
8. **上线前测 false-defer。** 正确变更被 UNKNOWN 拦住的比例；没有这个数，不知道代价。

## 6.5 工程配方（E3）

### 数据契约

| 对象 | 字段 |
|---|---|
| mutation context | `{mutation_id, class: merge|split|unmerge, head_id, target_id, policy_version, snapshot_id}` |
| required claims | `q_m = [{claim_id, predicate, scope, version}]` |
| evidence | `{obs_id, claim_id, role: support|contradiction|unresolved, provenance, hypothesis_id, source_id}` |
| promotion record | `{claim_id, obs_id, role, validation_basis, policy_version, promoted_by, promoted_at}` |
| verdict | `{PASS|BREACH|UNKNOWN_EVIDENCE, failed_claims[], unresolved[], scope_valid, versions_valid}` |

### 两阶段时序

1. Planner 提 mutation m。
2. Supervisor 从 m、V_E、policy version 派生 q_m。
3. 证据进 QUARANTINE/UNVERIFIED；promotion 到 P_auth(q_m, ω)。
4. Phase 1 授权 proposed mutation；Phase 2 验证 realized candidate；同 snapshot 的 scope/version/graph/evidence。
5. commit gate：PASS + scope/version valid；否则 defer，不丢弃证据。

### 失败模式表

| 失败 | 信号 | 检测 | 处置 |
|---|---|---|---|
| promotion 被绕过 | 直接写 P_auth | 审计 promotion 记录 | 拒绝 commit |
| scope/version 过期 | version mismatch | 同 snapshot 检查 | defer |
| 部分提交 | graph 与 evidence 不一致 | 事务/对账 | 回滚 |
| 同源 lineage 误判 | 多 UNVERIFIED 被当确认 | 共享 query/hypothesis/source | 降级为 UNVERIFIED |
| policy 本身错 | 规则与域不符 | 专家评审 | 停，修 policy |

### stop condition

- false-defer >20% → 停，放宽 claim 范围或补证据。
- unresolved conflict >10% → 停，先解决冲突。
- policy 未评审/版本不可追 → 不做写路径。
- 无审计存储/无事务 → 不做。

### 第一个 sprint

2 周、单 mutation class（person merge）、20 案例：

1. 写 domain policy：required claims 表（身份证/邮箱/地址/冲突）。
2. 实现 QUARANTINE→UNVERIFIED→P_auth 状态机 + promotion 记录。
3. 两阶段 fail-closed gate + 同 snapshot 检查。
4. 20 条历史/合成案例回放：UNVERIFIED 必须 defer；同源检索不得当确认。
5. 交付状态机 + 案例报告 + false-defer 初测。

### 成本

- policy/claim 表：2–4 专家人日（`推测`）。
- 状态机/审计存储：2–3 人周（`推测`）。
- 人审：false-defer 样本 20–50 条。
- 维护：policy/本体版本变更重审。

### 替代方案

- 规则引擎/工作流引擎；人工审批；现成 MDM/ER 产品；不做 commit gate。
- 论文无实现/成本；build/buy 只能给框架。

## 6.6 客户价值假设（V2/V3，`推测`）

- **受益者**：MDM/CRM/身份团队；痛点：错误合并、重复实体、审计不可追。
- **指标**：false merge 率、false-defer 率、合并审计通过率、每千次合并人审工时。
- **反事实**：不做 gate → 直接 merge；错误合并长期污染。
- **V3 试点**：单 mutation class、20–50 案例；成功 = false merge 0、false-defer ≤20%、审计可追；失败 = false-defer >30% 或无法回滚；停止线 = 年省返工 < 建设/维护。
- **反例**：policy 不全；同源 lineage；无实现；审计成本高。

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
