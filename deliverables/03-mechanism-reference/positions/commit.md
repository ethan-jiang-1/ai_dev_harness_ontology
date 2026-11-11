---
status: draft
deliverable_status: draft
updated: 2026-11-09
position: commit
evidence: [E-20]
---

# commit：证据够不够授权

> **一句话**：这是六个位置里证据最薄的一格。它的机制是「把可推理的证据」与「有权推动持久化的证据」分开；但只有概念架构，没有实现、没有 false-defer 数据。**不能把设计当已落地。**

**为什么只有设计（D1）**：commit gate 要把「可推理证据」与「有权落盘的证据」分开；四个开源项目没有单次写授权（E-20），也没有 false-defer 标签。**条件**：三条契约；**反例**：把设计当已落地；**决策**：只读/影子，不声称落地。 commit 的三条契约（证据齐/冲突清/版本有效）没有 mutation class 实现；false-defer 未测；四个项目都没有单次写授权。

**为什么不是相邻位置**：不是 action（action 在副作用前拦动作，commit 在落盘/merge 前判授权）；不是 checker（checker 判输出对不对，commit 判有没有权写）。

## 1. 机制

| 区分 | 推理证据 | 授权证据 |
|---|---|---|
| 要什么 | 能支持假设 | 证据齐、冲突清、版本有效 |
| 不足时 | 结论标低等级 | defer，不丢弃证据 |
| 谁定 | 域策略/本体约束定义的证据类型 | 域策略/本体约束定义的授权谓词 |

三段式放行：**证据齐**（`q_m` 每条命题都有 claim-specific eligible evidence）→ **冲突清**（已识别冲突被显式解决，不是忽略）→ **版本有效**（依据版本仍是当前版本）。三条全过才允许持久化；前两条聚合成 `PASS`，commit gate 再检查 `ScopeValid` 与 `VersionsValid`。

证据状态机：`QUARANTINE_EVIDENCE` → `UNVERIFIED`（可进 Planner 推理，**不是** positive authorization support）→ `P_auth(q_m, ω)`（对特定命题/观察域/policy version 有授权资格）→ `PASS`/`BREACH`/`UNKNOWN_EVIDENCE`。两阶段：Phase 1 授权 proposed mutation；Phase 2 验证 realized candidate；commit 时 scope/version/graph/evidence 必须在同一 snapshot。

## 2. 触发、输入、输出

| 项 | 内容 |
|---|---|
| 触发 | 变更即将落盘/写入外部系统 |
| 输入 | `mutation_context`（mutation_id/class/head_id/target_id/policy_version/snapshot_id）；`q_m[]`；证据（role/provenance/hypothesis_id/source_id）；promotion 记录 |
| 输出 | `verdict {status: PASS / BREACH / UNKNOWN_EVIDENCE, failed_claims[], unresolved[], scope_valid, versions_valid}` |
| 下一步 | PASS + scope/version 有效才 commit；BREACH 拒绝/升级；UNKNOWN defer，不丢弃证据 |

> 字段名是 digest 的工程配方（论文只给抽象对象，未给 schema），标 `推测`；commit 条件、promotion 规则来自论文契约，标 `已核（概念架构）`。

## 3. 能改变什么（设计上）

- **阻止错误变更落盘。** 错误合并/主数据写入前，只有 `PASS` + `ScopeValid` + `VersionsValid` 才放行；`UNKNOWN_EVIDENCE` 不会被当成「两实体不同」的证明，也不等于反证。`已核`（概念架构）
- **把同源检索排除出授权。** hypothesis 诱导的多个 `UNVERIFIED` 不能互相印证；「没检测到冲突」不是 positive support。`已核`（概念架构）
- **批准不继承。** `P_auth(q_m, ω)` 只对已声明命题/角色/观察域/policy version 有效；下一个 mutation 重新派生 `q_m`、重新 promotion。`已核`（概念架构）
- **审计可追。** promotion 记录要能回答「谁、何时、基于什么 validation basis」；缺 `promoted_by`/`promoted_at` 就只能看到「已授权」。`推测`（接口设计）

## 4. 拦不住什么 / 失效模式

| 失效 | 说明 | 证据/等级 |
|---|---|---|
| 无实现 | commit-gate 概念架构：无实现、无实证；四个开源项目没有单次写授权 | `已核`（E-20 + 概念架构） |
| false-defer 未测 | 正确变更被 `UNKNOWN_EVIDENCE` 拦住的比例未知 | `已核`（缺口） |
| 批准越界复用 | 把一次 `P_auth` 当会话级通行证 | `已核`（契约边界） |
| promotion 被绕过 | 直接写 `P_auth`，跳过 promotion 记录 | `已核`（失败模式表） |
| scope/version 过期 | Phase 1 后 policy/本体/图/证据版本变化，旧批准仍被使用 | `已核`（契约边界） |
| 部分提交 | graph 与 evidence 不一致；需事务/对账 | `已核`（失败模式表） |
| 同源 lineage 误判 | 多个 `UNVERIFIED` 被当确认 | `已核`（契约边界） |
| policy 本身错 | 规则与域不符；gate 只保证按 contract 执行 | `已核`（E-20 的边界 + 概念架构） |
| defer 无重入路径 | 没有队列/重入协议，被阻塞 mutation 会停在系统外 | `推测`（接口缺口） |
| 审计成本 | 审计存储是持续成本；无数字 | `已核`（类别）/ `推测`（量级） |

## 5. 使能条件

- 可控写路径、domain policy、promotion 流程、版本化存储、能记录 provenance；缺一不做；
- 先做一个 mutation class（如 person merge），不要覆盖所有写路径；
- 有人审队列与回滚/重入路径；没有就不要开自动写；
- 能接受 false-defer 成本，并准备 20–50 条样本先测。

## 6. 证据与边界

| 证据 | 等级 | 支持什么 | 不能证明什么 |
|---|---|---|---|
| E-20 | 已核（代码） | 四个项目没有单次写授权；执行≠授权；三态折叠 | 写路径不可实现；效应量；false-defer |
| commit-gate 概念架构 | 已核（概念架构） | 三条件、状态机、promotion、两阶段 | 已落地；false-defer；policy 正确 |

> 这一格的「能阻断」是**设计属性**，不是已实现属性。03 的位置表里必须写「是（设计）」；任何「已落地」的写法都是过度解读。

## 7. 可证伪条件

- 出现一个可运行的写授权实现，且 false-defer ≤20%、审计可追 → 从 D 升为「有实现」；
- 实测显示「证据齐/冲突清/版本有效」与写正确性无关 → 收窄三段式放行；
- false-defer >30%，或 gate 拦住的正确变更成本高于错误落盘成本 → 机制不划算；
- policy 错误率高于无 gate 的错误率 → gate 只是把错误执行得更一致。

## 8. 上游指针

- 机制：[commit-gate/mechanism](../../../topics/01-constraint/commit-gate/mechanism.md)
- 判断：[01-constraint/README](../../../topics/01-constraint/README.md) · [conclusions](../../../topics/conclusions.md) E-20
- 施工：[02 R9（recipes）](../../02-engineering-playbook/recipes/README.md) · [01 能力 13](../../01-capability-status/sections/map.md#22-一张表)
- 执行链：[execution-forms §执行链](../../../topics/execution-forms.md#执行链求值决策执行授权审计)
- 长版论证：[附录 §3.4.6](../appendix-constraint-spectrum.md#346-commit落盘前的授权)
