---
status: draft
updated: 2026-11-11
parent: ../README.md
basis: E-04/E-13/E-15/E-16/E-20；action-gate & commit-gate mechanism
---

# R6 · R8 · R9 · 约束：动作前、读路径、落盘前

> 三条都在「改变走向」的强端，但强度与成熟度不同：
>
> - **R6 动作前**：有实测，但收益不普遍、false-veto 未测；只能 shadow 起步。
> - **R8 读路径**：有代码级实现，但 fail-open、只删 subject、单实现；只能当可见性，不能当授权。
> - **R9 落盘前**：只有概念契约，没有实现；只能设计，不能声称落地。

## 0. 先选哪一条

| 你的错误 | 选 | 不能选 |
|---|---|---|
| 不可逆动作被执行（转账、删除、对外发送） | R6 | R8 只过滤读 |
| 检索结果里出现不该看的节点 | R8 | R6 不管读 |
| 错误变更要落盘/写外部系统 | R9（设计） | R6 只管动作前 |
| 只是想知道「有没有逆操作」 | R6 的 Layer A | 不要一上来做六模式分配 |

---

## R6 · 动作前可逆性闸：只在不可逆、高代价、弱模型时试

### 目标

在副作用发生前，按「是否存在可接受的逆操作序列」剪枝/审批；把「安全」从模型自评换成可检查的世界状态/本体事实。

> **不要把拦截率当保证。** 同一信息下，false-block 与 miss 是一条前沿；block-all 可以做到零 miss，但零可用性。没有可用性/合法放行指标，不能比较两个 gate。

### 适用 / 不适用

| 适用 | 不适用 |
|---|---|
| 动作不可逆且代价高（对外发送、资金、删除唯一数据） | 强模型 + 高基线（POLAR 已观察回退） |
| 模型能力弱于域要求 | 动作的复合可逆性无法计算 |
| 域规则可被查询成事实 | 判定所需事实依赖运行时状态而系统拿不到 |
| 有真实 DB/工具日志，能重建状态投影 | 合法意图主导（retail 退货/换货）且没有意图/授权层 |

### 前提

- 列出所有 mutating tools 与槽位。
- 能拿到真实状态（DB/工具日志），或至少只读投影。
- 有 curator 能写 T1–T5 逆关系与权重。
- 有 shadow 回放能力，不接线上写权限。

### 接缝 / 形态

动作前 / `compiled`。本体在动作前以**类型化逆关系**出现；约束强、覆盖窄（只覆盖 mutating tools）。

### 最小数据契约

**Layer A：静态动作本体**

```text
tool: {name, args, mutating, slots[]}
inverse_edge: {tool, tier: T1|T2|T3|T4|T5, weight, loss_class, bound?, curator, status}
```

| tier | 关系 | 每步 φ | 含义 |
|---|---|---|---|
| T1 | `inverse_of` | `w` | 有精确逆操作 |
| T2 | `bounded_reversibility` | `w · 1[Bound]` | 在边界内可逆 |
| T3 | `compensates` | `w · (1−w_loss)` | 可补偿，但有损 |
| T4 | `irreversibly_consumes` | 0 | 不可逆消费 |
| T5 | `external_side_effect` | 0 | 外部副作用，fail-closed |

**admissibility**：评分前过滤 provisional / revoked / disputed / 未接地的边；它们不进入逆序列。

**Layer B：状态投影**

```text
slot(entity_type, id) = value
state_hash
```

**输出**：

```text
{decision: APPROVE|VETO|ESCALATE, phi, pi, bottleneck}
```

`APPROVE|VETO|ESCALATE` 是 DecisionPolicy，不是本体的一部分。

**日志**：

```text
{tool, entity, tier, phi, tau, decision, reason,
 trajectory_id, approval(人/分钟), rollback}
```

### 做法

1. **列 mutating tools / 槽位**；先写 T1/T4/T5 本体 v0，不追求全。
2. **接只读状态**；反向搜索深度 3–5、环路检测；多候选取 `max min φ`，同分取最短。
3. **τ=0.80 按域保留率校准**，不跨域照搬（airline 36.6%、retail 100%、telecom 98.7%）。
4. **shadow 200–500 决策**；标 100 条 blocked 的 false-veto；报 harm/审批/task success。
5. **先做可逆性路由 + shadow**；不要一上来做六模式分配（CASEL 的 `γ_m` 是假设）。

### 可选：CASEL 六模式（第二阶段）

| mode | 做什么 | 前置 |
|---|---|---|
| direct | 直接执行 | — |
| verify | 调 checker | `d > τ_d` 先 verify |
| sandbox | 可回滚/dry-run | 只对 reversible mutation |
| clarify | 澄清 | `g > τ_g=0.2` |
| approve | 人审 | compensable/irreversible；模拟里 `ĉ≥0.55` |
| abstain | 不执行 | 本文未启用 |

信号：`p̂`（校准失败率）、`ĉ`（后果）、`ρ`（可逆性）、`g`（歧义）、`d`（证据新鲜度）。代价：

```text
J(m) = γ_m · p̂ĉ + λk(m) + μq(m)
```

- `γ_m` 是**干预后的残余失败比例**，论文是假设值（direct/verify/sandbox/approve = 1.00/0.42/0.15/0.04），不是测量。
- `k` = 0/1.0/1.6/2.2；`q` = 0/0/0.04/0.65；`λ:μ = 0.02:0.015`。
- **没有 `γ_m` 数据不要算 `J(m)`**；没有校准 `p̂`，阈值和账本都没有意义。
- CASEL 主表 7.02% HSR / 8.7% approvals 是 `τ̂=∞`（阈值关闭）下的结果；不能当「开了阈值」的成绩。

### 证据

- τ²-bench 上六个模型中四个在 airline 域提升 **0.11–0.18**；但 **18 个模型-域组合仅 8 个整体改善**，retail 与更强模型常回退（E-04）。
- **T1-only 接近 blanket veto，增益却不比 full 小**；结构反向组合的贡献未被隔离（E-04）。
- 作者声明 reward 不是防止伤害的直接度量；false-veto 未测。
- 约束类增益随模型基线能力升高而缩小（E-13，六点描述性拟合，不能当阈值）。
- CASEL：HSR 14.75%→7.02%、审批 8.7%；最低 HSR 是 Consequence-Menu 4.38%/13.8%，Risk-Menu 5.82%/12.6%；模拟、`γ_m` 假设、审批疲劳未建模（E-15）。
- OntoAct 的推理期条件闸（E-16）是另一条支线；它与 R6 的边界尚未稳定，本 recipe 不把它当动作闸。

### 成本

| 项 | 量级 | 等级 |
|---|---|---|
| Layer A（每域） | 2–5 curator 人日 | 推测 |
| Layer B（接真实状态） | 1–2 人周 | 推测 |
| 阈值校准 + false-veto 标注 | 3–5 人日/域 | 推测 |
| CASEL 控制器/校准/sandbox/审批集成 | 2–4 人周 | 推测 |
| 审批人时 | 未测；CASEL 只给 approvals 比例 | 未知 |

### 验收 / 停

| 指标 | 通过线（工程建议） | 停 |
|---|---|---|
| false-veto | 不设单点；报 miss–false-block 前沿 | 前沿不可接受 → 降 advisory/停 |
| 同轨迹配对 | Δ>0 且 CI 不跨零 | Δ≤0 且 T1-only≈full → 结构贡献不成立，停 |
| 保留率 | 20%–95% | <20% 或 >95% → 阈值失效，重校准 |
| task success | 不降 >2pp | 下降 → 停 |
| 审批率 | ≤10–15%（业务定） | 超过 → 降级 |
| 真实状态 | 拿得到 | 拿不到 → 不做硬 veto |
| `γ_m` | 有实测/可接受区间 | 没有 → 只上静态 `p̂ĉ` gate，不做多模式 |

### 失效模式

- **T1-only ≈ blanket veto。** 结构贡献未隔离；T1-only 增益不比 full 小。
- **可逆性 ≠ 安全性 ≠ 授权。** 外部副作用可能完全合法；retail 的 return/exchange 可能在 block log 里，但没有授权标签。
- **漏掉一条不可逆关系 → false approval。** 本体错误是 fail-open 的。
- **判据依赖运行时状态。** 静态本体不够；需要 Layer B。
- **阈值错置。** airline 在 0.80 只保留 36.6%，retail 100%。
- **只判不记。** 剪枝事件不记录，false-veto 无法算。
- **把 block 总数当正确拒绝。** 被 block 可能是 review 失败/不可用，不是授权判断；要把「拦住的未授权动作」与「放过的合法动作」分开报。
- **不验证逆执行。** 「有逆序列」不等于「恢复会成功」。
- **CASEL 的干预有效性是假设。** `γ_m` 不是测量；审批疲劳未建模。
- **把 7.02% 当阈值开启的结果。** 主表 `τ̂=∞`。

### false-veto 标注协议（工程配方，`推测`）

1. 从 shadow 的 blocked decisions 分层抽 100 条（覆盖工具/域/模型）。
2. **同一操作构造 lawful/forbidden 成对样本，只变授权证据**；否则 always-block/always-allow 也能在单边指标上好看。
3. 每条标三件事：`本可合法执行?`（yes/no/unsure）、`若不拦会造成的 harm`（none/low/high）、`授权依据`（有/无）。
4. false-veto = `本可合法执行=yes` 且 `harm=none/low` 的比例；报 Wilson CI；`unsure` 单列，不并进 yes/no；没有授权标签的，不判 false-veto。
5. 同轨迹配对：同一 baseline、同一轨迹，比较 full vs T1-only vs no-gate。

**没有这个标注，R6 的 false-veto 只能写 unknown；不要用 retention 或 block count 代算。**

### 可抄锚点

- [action-gate 机制](../../../topics/01-constraint/action-gate/mechanism.md) 的「两层本体」「失效模式」「工程发现 1–4」。
- POLAR 的 T1–T5、反向搜索、τ、日志字段；不要抄「结构有效」。
- CASEL 的六模式与 `J(m)` 框架；不要抄 `γ_m` 数值当测量。

---

## R8 · 读路径过滤：只做可见性，不要当授权

### 目标

在检索结果进入上下文前，按用户上下文过滤；把「谁能看哪些节点」变成可执行的策略求值。

### 适用 / 不适用

| 适用 | 不适用 |
|---|---|
| 读侧信息屏障/可见性 | 写授权/落盘变更 |
| 有策略图 + `user_context` | 需要对象方向也受控 |
| 能接受 best-effort/fail-open | 需要审计级「为什么允许」 |
| 有第二个执行点可对照（rewrite/scan 候选；无独立泄漏率） | 只有 trustgraph 一个已入库实现 |

### 前提

- 策略图 `urn:graph:policy`；SHACL-AF `NodeShape` + `sh:SPARQLTarget` + `sh:SPARQLRule` + `tg-pol:blocks`。
- 请求带 `user_context`。
- 能对候选节点跑 target + rule；能删除命中节点。
- 能构造异常 policy 与 object 方向用例。

### 接缝 / 形态

`read-path`（轴外）/ `engine`。它是查询结果返回前的 best-effort gate，不是动作前闸门，也不是 commit gate。

### 最小数据契约

```text
policy_graph: urn:graph:policy
shape: NodeShape + sh:SPARQLTarget + sh:SPARQLRule + tg-pol:blocks
request: {query, user_context}
output: filtered triples/nodes + block reason (if logged)
```

### 做法

1. **有策略时，缺 `user_context` 直接报错**（fail-closed）；无策略时明确 open mode。
2. **对候选节点跑 target + rule**；命中 `tg-pol:blocks` 的节点剔除。
3. **写清边界**：异常时 fail-open；只删 subject 侧；首命中即停；缓存 30–60s。
4. **构造异常 policy 和 object 方向用例**，先测泄漏，再上线。
5. **不要把它叫「授权」**；它不回答「为什么允许」，也不覆盖写路径。

### 证据

- trustgraph `policy/policy_filter.py` 代码级：策略图 + `user_context` 契约；SHACL-AF target/rule；被 block 的 **subject 侧**三元组删除（E-20；commit-gate F5/F6/F7）。
- **fail-open**：target/rule 异常 → 当作不命中/无判定；缺 `sh:select`/`sh:construct` → 跳过；无策略 → 原样返回。只有「有策略 + 缺 user_context」是 fail-closed（F6）。**SHACL-AF 对不支持的 custom target 只写「behavior undefined」+ SHOULD warn，不要求拒绝**；fail-open 是实现选择，不是标准要求（[SHACL-AF 卡](../../../src/web/w3c-shacl-af/w3c-shacl-af.card.md)）。
- **只删 subject 侧**：`_triple_blocked` 只查 `triple.s`；object 方向可能泄漏（F7）。
- **单实现（已入库）**：四个开源项目里只有 trustgraph 做读路径；read-path 仍是轴外位置（E-20；seams）。
- **重写 vs 结果过滤有形式化对照**：Kirrane 2020 用 secure/sound/maximum 比较两者，指出 FILTER 式重写在否定/子查询/聚合下不正确；[卡](../../../src/web/kirrane-2020-qbac/kirrane-2020-qbac.card.md)。
- **第二执行点（候选，未入库）**：`Matdata-eu/sparql-guard`（Apache-2.0，HEAD `6b68d769`）：TS 代理，用**查询重写**而非返回后过滤；fail-closed、subject+object 两侧、SHACL Core 子集；**2026-11-11 仓库外复跑 76/76 通过（EXP-001）**。它仍未按仓库标准入库（单作者/1★/无 harness 调用点/无独立泄漏率），只能当执行点线索。
- **第三执行点（候选，未入库）**：`pwin/triplestore`（holosdb，`666238f`）：扫描期按 **predicate/graph** 过滤，默认 deny、fail-closed；`holos-engine/src/view.rs` 有调用点；20 条 security 单测（未复跑）。**EXP-002**：sparql-guard 10 用例实跑 7 pass、1 alias leak、0 false-block；alias 是策略建模边界。**EXP-003**：前置解析能修 node-level（post-filter/rewrite），不修 predicate-level（scan）。规范只强制「已断言 sameAs 则展开」（OWL 2 RL），不强制「先于过滤」；授权按 alias 逐个判，合并单独授权。`Scope` 没有 Subject/Object，**不能表达 node-level**，所以不是 trustgraph 的替代。
- 31 条策略单测存在；未做异常注入/对象方向测试。

### 成本

| 项 | 量级 | 等级 |
|---|---|---|
| 策略图/形状编写 | 按策略数；未测 | 未知 |
| 每批 × 每节点查询 | 时延随候选数上升 | 已核（机制） |
| 缓存 30–60s | 降低重复求值 | 推测 |

### 验收 / 停

| 指标 | 通过线 | 停 |
|---|---|---|
| 泄漏率 | 0（含 object 方向） | object 方向泄漏 → 不能上线 |
| 误拦 | 可接受（业务定） | 误拦高 → 先修策略 |
| 异常路径 | fail-closed 或显式告警 | fail-open 未修 → 不能当安全控制 |
| 第二实现 | 有独立实现 + harness 调用点/泄漏测量 | 只有候选/未入库 → 不升第七时刻；只当可见性 |

**以下任一需求 → 这个实现不够**：对象方向也受控、写授权、审计级「为什么允许」。先补**独立评测**（共同 10 用例 + 标签），不是再找一个引擎。

### 失效模式

- **把 fail-open 当安全。** 异常时放行；攻击面在错误路径。
- **只删 subject 侧。** 敏感节点作为 object 仍可能返回。
- **把读路径当写授权。** 它拦检索结果，不拦落盘。
- **单实现当标准。** 没有第二个实现，不能证明这是可复用的接缝。
- **缓存吞掉策略变更。** 30–60s 内旧策略仍生效；变更要清缓存。

### 可抄锚点

- [trustgraph digest](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) 的 `policy_filter.py` 调用链、fail-open、subject-only。
- [commit-gate findings F5–F7](../../../topics/01-constraint/commit-gate/findings.md)。
- 不要抄「fail-open + subject-only」当默认；要抄的是「策略图 + user_context 契约」。

---

## R9 · 落盘前授权：现在只能设计，不要声称已落地

### 目标

把「可推理的证据」与「有权推动持久化的证据」分开；在 mutation 落盘前，按证据齐/冲突清/版本有效三条放行。

### 适用 / 不适用

| 适用 | 不适用 |
|---|---|
| 身份 merge/split、主数据写入、图合并 | 读路径过滤（那是 R8） |
| 有 domain policy、审计存储、事务、可控写路径 | 没有 policy/审计/事务/可控写路径 |
| 能先做一个 mutation class | 想一次覆盖所有写路径 |
| 能接受 defer/人工队列 | 要求全自动、零人工 |

### 前提

- 一个 mutation class（如 person merge）。
- `q_m` 所需 claims 表 + domain policy。
- promotion 流程 + 审计存储。
- 版本化存储/事务；能记录 provenance。
- **没有这些 → 不做写路径，只做只读/影子。**

### 接缝 / 形态

落盘前 / 无实现（设计）。本体在落盘前以 **authorization predicates / claim-specific promotion / scope-version** 出现；约束强，但覆盖率取决于 domain policy。

### 最小数据契约

```text
mutation_context: {mutation_id, class: merge|split|unmerge,
                   head_id, target_id, policy_version, snapshot_id}

q_m[]: {claim_id, predicate, scope, version}

evidence: {obs_id, claim_id, role: support|contradiction|unresolved,
           provenance, hypothesis_id, source_id}

promotion: {claim_id, obs_id, role, validation_basis,
            policy_version, promoted_by, promoted_at}

verdict: {status: PASS|BREACH|UNKNOWN_EVIDENCE,
          failed_claims[], unresolved[], scope_valid, versions_valid}
```

- `hypothesis_id` / `source_id` 是同源检测的钩子；没有它们，hypothesis 诱导的检索会被当独立确认。
- `promoted_by` / `promoted_at` 不能省；否则审计只能看到「已授权」。
- `role` 必须是命题级：support / contradiction / unresolved；不能只有一个全局「已验证」。

### 做法

1. **先做一个 mutation class**（如 person merge），不要覆盖所有写路径。
2. **三条全过才 commit**：证据齐 + 冲突清 + 版本有效；不满足时 defer，不丢弃证据。
3. **两阶段**：Phase 1 授权 proposed；Phase 2 验证 realized；同 snapshot 检查 scope/version。
4. **批准不继承**：`P_auth(q_m, ω)` 只对声明的命题/角色/观察域/policy version 有效；下一个 mutation 重新 promotion。
5. **先测 false-defer**：20–50 条样本；没有这个数，不知道 gate 的代价。

### 证据

- 只有概念架构；四个开源项目里没有单次写授权（E-20；commit-gate F4/F5）。
- Commit Boundary 自述无实现、无实证；保证依赖 7 条假设（域策略充分、promotion 可靠、强制执行等）。
- 读路径有实现（trustgraph），但那是 R8，不是 commit gate；不能外推成「授权不可执行」。
- false-defer 未测；domain policy 编写成本未测。

### 成本

| 项 | 量级 | 等级 |
|---|---|---|
| domain policy / claim 表 | 2–4 专家人日 | 推测 |
| 状态机 / 审计存储 | 2–3 人周 | 推测 |
| false-defer 标注 | 20–50 样本；人日未测 | 推测 |
| 持续审计/版本管理 | 未给数字 | 未知 |

### 验收 / 停

| 指标 | 通过线（工程建议） | 停 |
|---|---|---|
| false-defer | ≤20% | >20% → 放宽 claim/补证据 |
| unresolved conflict | ≤10% | >10% → 先解决冲突 |
| 审计可追 | `promoted_by/at`、scope/version 可查 | 不可追 → 不做 |
| 事务/回滚 | 有 | 没有 → 不做 |
| policy 评审 | 已评审/版本可追 | 未评审 → 不做 |
| 错误授权 | 0（单 class 试点） | >0 → 停，先修 policy/证据 |

### 失效模式

- **批准越界复用。** 把 `P_auth` 当会话级通行证；只对声明命题/角色/观察域/policy version 有效。
- **promotion 被绕过。** 直接写 `P_auth`，跳过 promotion 记录。
- **scope/version 过期。** Phase 1 后 policy/本体/图/证据变化，旧批准仍被使用。
- **部分提交。** graph 与 evidence 不一致；用事务/对账回滚。
- **同源 lineage 误判。** 多个 `UNVERIFIED` 被当确认。
- **冲突被静默消解。** 实现把冲突压成单一分数/标签，绕过 `unresolved` 阻塞。
- **defer 无重入路径。** 被阻塞 mutation 停在系统外。
- **policy 本身错。** 规则与域不符；专家评审，停，修 policy。
- **把「没有冲突」当「支持」。** 没检测到冲突只是没检测到。

### 最小实现 spec（若要做）

1. **一个 mutation class**（person merge）+ 一个 `q_m` 表。
2. **状态机**：QUARANTINE_EVIDENCE / UNVERIFIED / P_auth / PASS / BREACH / UNKNOWN_EVIDENCE。
3. **promotion 记录**：命题级 role、provenance、validation basis、policy version、promoted_by/at。
4. **两阶段 gate**：Phase 1 授权 proposed；Phase 2 验证 realized；同 snapshot。
5. **verdict 字段**：`failed_claims[]` / `unresolved[]` / `scope_valid` / `versions_valid`；没有它们，defer 无法重入。
6. **false-defer 回放**：20–50 条正确变更；测被 `UNKNOWN_EVIDENCE` 拦住的比例。
7. **审计查询**：给定 mutation_id，能回答「谁、何时、基于哪条 claim/哪版 policy 批准」。

**没有 1–7，不要声称 commit gate 已落地。**

### 可抄锚点

- [commit-gate 机制](../../../topics/01-constraint/commit-gate/mechanism.md) 的「三段式放行」「promotion 契约」「工程发现 1–4」。
- Commit Boundary 的 `q_m`/promotion/verdict 语义；不要抄「已实现」。
- [identity 机制](../../../topics/04-state/identity/mechanism.md) 的 merge/split 写侧契约。

**出处**：[action-gate 机制](../../../topics/01-constraint/action-gate/mechanism.md) · [commit-gate 机制](../../../topics/01-constraint/commit-gate/mechanism.md) · [E-04/E-15/E-20](../../../topics/conclusions.md)
