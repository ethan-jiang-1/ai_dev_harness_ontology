# 持久化前 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。
> 「工程发现 1–4」里的字段名/记录结构来自 [digest](../../../src/papers/2610.37407-commit-boundary/digest.md) §6.5 的工程配方（论文只给抽象对象，未给 schema），标 `推测`；commit 条件、promotion 规则、stop 门来自论文契约或 digest 明确条目，逐条标等级。

## 位置

变更即将落盘或写入外部系统的那一刻。前面所有环节都是「推理」，这里是唯一「改变世界」的时刻。

## 核心区分

| | 推理证据 | 授权证据 |
|---|---|---|
| 要什么 | 能支持假设 | 证据齐、冲突清、版本有效 |
| 不足时 | 结论标为低等级 | defer，不丢弃证据 |
| 谁定 | 域策略/本体约束定义的证据类型 | 域策略/本体约束定义的授权谓词 |

混成一个判据会得到两种失败：过度保守（推理阶段就要求授权级证据）或错误落盘（推理级证据直接放行）。

## 三段式放行

1. **证据齐**：`q_m` 的每条命题是否都有 claim-specific eligible evidence 覆盖。
2. **冲突清**：已识别的冲突是否被显式解决，而非被忽略。
3. **版本有效**：依据的版本是否仍是当前版本。

三条全过才允许持久化。实现上，前两条聚合成 `PASS`；commit gate 再检查 `ScopeValid` 与 `VersionsValid`。任何一条不满足时，mutation 与证据留在 defer，不丢弃证据。

## 证据状态机（Commit Boundary）

| 状态 | 含义 |
|---|---|
| `QUARANTINE_EVIDENCE` | 有 admission conflict/indeterminate，暂不可见 |
| `UNVERIFIED` | 可进 Planner 推理；**不是** positive authorization support |
| `P_auth(q_m, ω)` | 对特定命题、观察域、policy version 有授权资格 |
| `PASS` / `BREACH` / `UNKNOWN_EVIDENCE` | 三态结论；`BREACH` > `UNKNOWN` > `PASS` |

`UNKNOWN_EVIDENCE` 表示授权未建立（证据不足或冲突未解），不是「两个实体不同」的证明；不可逆变更被 defer 不等于反证。`已核`（digest §6.1 第 8 条）

## promotion 契约（digest §3.3，七条）

1. 评估**具体命题**，不是文档相关性/查询匹配/合理性。
2. 记录 provenance、命题、角色、时间适用性、validation basis、policy/validator version。
3. 不把 Planner 置信度、LLM `verified` 标签、多个 `UNVERIFIED` 重复当授权证据。
4. **不因为 hypothesis 诱导了检索就把结果当独立确认**；同源 query/hypothesis/source 不算 corroboration。
5. 不从「没检测到冲突」推断 positive support。
6. 不引用 shadow candidate 或引用 shadow 内容的 claim；要沿记录链传递。
7. 只在声明的命题/角色/适用性上 eligible。

## 两阶段

Phase 1 授权 proposed mutation；Phase 2 验证 realized candidate；commit 时 scope/version/graph/evidence 必须在同一 snapshot。Phase 1 的批准只绑定当次 mutation 的 `q_m`/scope 与 graph/evidence/policy 版本，不是会话级通行证。`已核`（digest §3.1/§6.5；arXiv:2610.37407 §6.1）

## 失效模式

> 以下是契约边界或实现风险，不是实测发生率；digest 明确无实现。标 `已核` 指论文/契约明确；标 `推测` 指工程判断或未测发生率；表内处置动作来自 digest §6.5 失败模式表（工程配方）。

- **批准越界复用（把 `P_auth` 当会话级通行证）。** `P_auth(q_m, ω)` 只对已声明命题、角色、观察域、policy version 有效；把一次批准复用到别的 mutation 或新版本，需要重新 promotion，不能继承。`已核`（digest §3.3 第 7 条）
- **promotion 被绕过。** 直接写 `P_auth`，跳过 promotion 记录；审计 promotion 记录可发现，拒绝 commit。`已核`（digest §6.5 失败模式表）
- **scope/version 过期。** Phase 1 后 policy/本体/图/证据版本变化，旧批准仍被使用；必须同 snapshot 检查 `ScopeValid`/`VersionsValid`，否则 defer。`已核`（契约；digest §6.5）
- **部分提交。** graph 与 evidence 不一致；用事务/对账回滚。`已核`（digest §6.5 失败模式表）
- **同源 lineage 误判。** 多个 `UNVERIFIED` 被当确认；按共享 query/hypothesis/source 降级为 `UNVERIFIED`。`已核`（契约）
- **policy 本身错。** 规则与域不符；专家评审，停，修 policy。`已核`（digest §6.5 失败模式表）
- **冲突被静默消解。** 实现若把冲突压成单一分数/标签，就绕过 `unresolved` 阻塞；digest 要求未解决冲突 → `UNKNOWN_EVIDENCE`/defer，但未测实现发生率。`推测`
- **defer 无重入路径。** digest 只说 defer、不丢弃证据，没有给队列/重入协议；若没有队列，被阻塞 mutation 会停在系统外。`推测`（缺口 G3）
- **依赖链未记录。** 架构不控制 hypothesis-conditioned retrieval；没有 dependency-aware lineage，promotion 仍可能被污染。`已核`（digest §5）
- **Policy/promotion 正确性外包。** 架构只保证「按 contract 执行」，不保证 contract 本身对。`已核`（digest §4.1/§5）
- **把「没有冲突」当「支持」。** 没检测到冲突只是没检测到，不是 positive support。`已核`（§3.3 第 5 条）

## 与本体 / 回路的关系

本体在落盘前以 **authorization predicates / claim-specific promotion / scope/version** 出现；约束强度强（能阻止持久化），但覆盖率取决于 domain policy。被违反时能报出缺哪条证据/冲突/版本；不能保证 policy 本身正确。

## 实施与客户价值（A3/A4）

> 本节把 digest 的工程口径落到接口/字段/成本/stop；重点补 3 类：`verdict` 字段（`scope_valid`/`versions_valid`/`failed_claims[]`/`unresolved[]`）、`promotion` 审计字段（`promoted_by`；shadow/eligible 边界）、持续审计成本。字段名是 digest §6.5 的工程配方（论文未给 schema），不把它们说成论文实测。

### 实施决策

- 身份变更/图合并/主数据写入前：`UNVERIFIED` 只能推理，不能授权 merge/split；commit gate 只放行 `PASS`（`q_m` 全覆盖 + 冲突清）+ `ScopeValid` + `VersionsValid`。
- **批准不继承。** `P_auth(q_m, ω)` 只对已声明命题/角色/观察域/policy version 有效；下一个 mutation 重新派生 `q_m` 并重新 promotion，不能沿用上一笔批准。`已核`（digest §3.3 第 7 条；arXiv:2610.37407 §6.1）
- 先做一个 mutation class（person merge），不要一次覆盖所有写路径。
- 使能条件：可控写路径、domain policy、promotion 流程、版本化存储、能记录 provenance；缺一不做。`已核`（digest §6.2）

### 工程发现 1｜接口：mutation context、q_m 与 verdict

- `mutation_context {mutation_id, class: merge|split|unmerge, head_id, target_id, policy_version, snapshot_id}`。`推测`（digest §6.5 数据契约）
- `evidence {obs_id, claim_id, role: support|contradiction|unresolved, provenance, hypothesis_id, source_id}`；`hypothesis_id`/`source_id` 是同源检测的钩子，缺了只能靠文本相似度猜。`推测`（digest §6.5 数据契约；同源检测必要性为工程判断）
- `q_m = [{claim_id, predicate, scope, version}]`，由 supervisor 从 mutation、`V_E`、policy version 派生；Planner 不能替换或弱化。`已核`（派生规则：digest §3.1；不可替换：arXiv:2610.37407 Assumption 5）；字段结构 `推测`
- `verdict {status: PASS|BREACH|UNKNOWN_EVIDENCE, failed_claims[], unresolved[], scope_valid, versions_valid}`。commit 只在 `PASS ∧ scope_valid ∧ versions_valid` 时放行；`BREACH` 拒绝/升级，`UNKNOWN_EVIDENCE` defer。`已核`（commit 条件；digest §6.5）；字段结构 `推测`
- **为什么 verdict 不能只有三态。** 只有 `status` 时，defer 无法回答「缺哪条 claim / 哪条冲突未解 / 是 scope 还是 version 过期」，重入和审计都做不了；`failed_claims[]` 与 `unresolved[]` 是重入的输入。`推测`（工程判断；digest 只给字段，未给重入协议）
- 两阶段：Phase 1 授权 proposed；Phase 2 验证 realized；同 snapshot 的 scope/version/graph/evidence。`已核`（digest §3.1）

### 工程发现 2｜接口：promotion 记录要能独立审计

- `promotion {claim_id, obs_id, role: support|contradiction|unresolved, validation_basis, policy_version, promoted_by, promoted_at}`。`推测`（digest §6.5 数据契约；论文只给抽象对象）
- **`promoted_by` / `promoted_at` 不能省。** 缺 `promoted_by` 不能追是谁做的 promotion；缺 `promoted_at` 不能追何时。两者都缺，审计只能看到「已授权」。`推测`（审计判断；digest 只给字段）
- `role` 必须是命题级：support / contradiction / unresolved；不能只有一个全局「已验证」标签。`已核`（§3.3 第 1–2 条）
- promotion 不接受 Planner 置信度、LLM `verified` 标签、多个 `UNVERIFIED` 重复；也不从「没冲突」推断 support。`已核`（§3.3 第 3–5 条）

### 工程发现 3｜约束：shadow 与 eligible 是 promotion 的硬边界

- **shadow 排除。** promotion 的 provenance/validation basis 不得引用 shadow candidate，也不得引用「其 recorded basis 引用了 shadow」的 claim；限制要沿记录链传递。`已核`（§3.3 第 6 条）
- **eligible 范围。** 证据只在声明的命题、角色、适用性上 eligible；同一来源换一个命题要重新评估，不能把「对 A 命题可用」当成「对 B 命题也可用」。`已核`（§3.3 第 7 条）
- **工程含义：** promotion 表要能表达 `shadow` 标记与 `eligible_scope`；否则实现只能把 eligibility 做成全局布尔（promotion 一次生效、对所有命题都算数）。`推测`（接口设计判断）

### 工程发现 4｜成本与指标：审计存储是持续成本，false-defer 必须先测

- 一次性：domain policy/claim 表 2–4 专家人日；状态机/审计存储 2–3 人周。`推测`（digest §6.5 估算；论文无实测）
- 持续：审计存储保存证据、角色、validation basis、policy version；policy/本体每次变更要重新验证并做版本管理。digest 把它列为持续成本，没有给数字。`已核`（§6.2 类别）；量级 `推测`
- 人审：准备 20–50 条 false-defer 样本（digest 给量级，未给工时）。`推测`
- **上线前先测 false-defer。** 正确变更被 `UNKNOWN_EVIDENCE` 拦住的比例；没有这个数，就不知道 gate 的代价。`已核`（§6.4 最小落地清单第 8 条）
- **stop 门（工程门，不是论文阈值；数字是 digest 给的起点，`推测`）：**
  - false-defer >20% → 停，放宽 claim 范围/补证据。
  - unresolved conflict >10% → 停，先解决冲突。
  - policy 未评审/版本不可追 → 不做写路径。
  - 无审计存储/无事务 → 不做。

### 客户指标/V3（`推测`）

- 受益者：MDM/CRM/身份团队；痛点：错误合并、重复实体、审计不可追（digest §6.6）。
- 指标：false merge 率、false-defer 率、合并审计通过率、每千次合并人审工时。
- 反事实：不做 gate → 直接 merge，错误长期污染。
- V3：单 class 20–50 案例；成功 = false merge 0、false-defer ≤20%、审计可追；失败 = false-defer >30% 或无法回滚；停止线 = 年省返工 < 建设/维护。
- 这些是 digest §6.6 的客户价值假设，不是实测；不能当效果证据。

### 第一个 sprint

2 周、person merge、20 案例（digest §6.5 工程配方）：写 required claims 表 → 状态机 + promotion 记录（含 `promoted_by`；能表达 shadow/eligible）→ 两阶段 fail-closed gate + 同 snapshot 的 scope/version 检查 + 完整 `verdict` 字段 → 回放 20 案例（UNVERIFIED 必须 defer、同源不算确认、scope/version 变了必须重新授权）→ 出案例报告与 false-defer 初测。

### 反例

- policy 不全（digest §6.3/§6.6）。
- 同源 lineage（§5/§6.6）。
- 无实现（§4）。
- 审计成本高（§6.2 持续成本；§6.6 列为反例，`推测`）。
- 无法控制写路径；依赖链无法记录；需要语义真值保证（§6.3「别用」）。

### 替代方案（digest §6.5，工程框架，无同口径数字）

- 规则引擎/工作流引擎；人工审批；现成 MDM/ER 产品；不做 commit gate。
- 论文无实现/成本；build/buy 只能给框架，不能从论文得到同口径 TCO。`推测`

## 关联

- [Commit Boundary digest](../../../src/papers/2610.37407-commit-boundary/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [memory](../../04-state/memory/README.md)
