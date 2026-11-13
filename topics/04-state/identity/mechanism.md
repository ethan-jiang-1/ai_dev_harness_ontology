# 身份 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

同一实体在不同来源、不同时期以不同名字出现，被当成多个实体；或者两个相似实体被合并。身份不稳，后面的状态、冲突、失效都挂不住。

## 两种做法

| 做法 | 机制 | 代表 |
|---|---|---|
| registry 锚定 | 固定 product–topic 本体 + 规范身份/持久别名；重复观察定向到同一段历史 | FIRME |
| 时序属性图 | 领域无关本体把对话组织成带时间的事件；append-only 保留演化；检索时消解冲突 | APEX-MEM（摘要级，`待核`） |

## FIRME 的 registry

1. **分层匹配**：identifier → normalized name → learned alias → LLM semantic matching（同类型候选，score ≥0.8，取最高；否则新注册）。
2. **alias 复用**：匹配后的 surface form 加入 anchor 的 alias set；下次直接匹配，减少语义调用。
3. **错误匹配的后果**：alias 命中把 surface form 挂到 anchor 后，同一 surface form 的后续出现会被路由到错误历史；传播幅度论文未测，也没有自动回滚（机制推断，`推测`）。
4. **本体克制**：本体主要做对齐与印证条件，不承担自由推理。

## 身份变更是 commit 问题

Commit Boundary（概念架构）把「可推理的证据」与「可授权身份变更的证据」分开：

- `UNVERIFIED` 可以进 Planner 推理，但不能授权 merge/split。
- 需要 claim-specific promotion：命题级证据、provenance、角色、scope/version。
- 同源检索不算独立确认；「没检测到冲突」不是 positive support。
- 两阶段 supervisor + 原子 commit：Phase 1 授权 proposed mutation；Phase 2 验证 realized candidate。

### commit 失败模式与处置（Commit Boundary 失败表）

| 失败 | 信号 | 检测 | 处置 |
|---|---|---|---|
| promotion 被绕过 | 直接写 P_auth | 审计 promotion 记录 | 拒绝 commit |
| scope/version 过期 | version mismatch | 同 snapshot 检查 | defer |
| 部分提交 | graph 与 evidence 不一致 | 事务/对账 | 回滚 |
| 同源 lineage 误判 | 多个 `UNVERIFIED` 被当确认 | 共享 query/hypothesis/source | 降级为 `UNVERIFIED` |
| policy 本身错 | 规则与域不符 | 专家评审 | 停，修 policy |

这张表只规定「看到什么信号怎么处置」，没有实现、没有触发率，false-defer 多少仍未知。`推测`（契约）

## 失效模式

- **合并错误。** 两个相似实体被当成一个，历史被污染。
- **拆分错误。** 同一实体跨期碎裂，证据挂不上新版本。
- **别名漂移。** 规范名与持久别名失配。
- **来源/时间丢失。** 无法判断某条关系属于哪个版本。
- **registry 过时。** 本体升级后，旧身份无法对齐。
- **错误合并的传播。** 一个 false merge 会把后续同一 surface form 的出现路由到错误 anchor（机制推断，论文未测传播幅度）；merge precision 必须和 CMR 一起看。`已核`（precision 口径）/ `推测`（污染幅度）
- **把「没观察到」当「不是同一实体」。** 未匹配只说明当前证据不足，不是否定。

## 与本体 / 回路的关系

本体在身份层以 **规范 ID / 别名 / 对齐条件 / 类型约束** 出现；约束强度中（能对齐、能约束合并类型，不能保证语义同一）。被违反时通常没有即时信号，错误跨轮累积。

## 实施与客户价值（A3/A4）

### 实施决策

- **先锚身份，再谈记忆内容与检索。** 跨期碎裂不是检索问题：同一实体的多个 surface form 不锚定，冲突、失效、证据累积都挂不住；预算顺序建议 registry/alias → 内容 → 检索。`已核`（前者）/ `推测`（预算顺序）
- **alias 层是已测的增量，但只在 canonical registry + 语义兜底之上。** no-alias 对照仍保留 canonical ID/name 匹配与跨期 semantic fallback；加 alias 得 final-period CMR +7.8–12.1 pp、semantic matching token −40.3%（investor calls × Opus × final period；不含 registry 构建）。`已核` 至于「这笔钱给 alias 还是更强的语义匹配器」：registry / alias / semantic fallback 的分别贡献作者自述未拆分，只能当 `推测`。
- **写入侧单独一道授权门：低置信只挂起，不自动 merge/split。** `UNVERIFIED` 可进 Planner 推理，但不构成授权证据；没有 claim-specific promotion、冲突解决与 scope/version 检查，就不开自动合并写路径。契约部分 `已核`；效果部分 `推测`（Commit Boundary 是概念架构，无实现）。
- **验收拆成 MMR × merge precision，再单列 reattachment recall。** CMR = MMR × merge precision：CMR 本身已经惩罚「少匹配」（MMR 低），单看 precision 才会奖励「不匹配/少匹配」（分母变小）；单看 CMR 看不出低 CMR 是覆盖不足还是错配。`已核`
- **0.8 与五态参数不跨域搬。** 0.8 在 investor-call 的 T−1 上选、再到 final period 评，有调参乐观偏差；换域重标，并把阈值版本与 alias 开关一起入档。`已核`

### 数据/接口

- **registry**：`canonical_id`（永不变）、`type`（person / org / product / topic）、`normalized_name`、`aliases[]`（只存实体侧 surface form）、`first_seen` / `last_seen`、`source_version`。
- **match 契约**：identifier → normalized name → learned alias → semantic fallback（同类型候选、阈值按域重标）；命中即把 surface form 写回 alias set，未命中才新注册。
- **边**：key = `head_id` + typed canonical target；`relation` / `source` / `source_indicator`（1=unstructured、2=structured、3=hybrid）留在 observation、不进 key；融合只加引用、不改来源；幂等键 `(head_id, typed_target_id, source_id, period)`，每 period 每边最多一次强度更新。
- **写侧契约**（原 Commit Boundary 2610.37407 §6.5，已移出；作概念契约参考）：`mutation_context {mutation_id, class: merge|split|unmerge, head_id, target_id, policy_version, snapshot_id}`；`q_m[] = {claim_id, predicate, scope, version}`；证据 `{obs_id, claim_id, role: support|contradiction|unresolved, provenance, hypothesis_id, source_id}`；promotion `{claim_id, obs_id, role, validation_basis, policy_version, promoted_by, promoted_at}`；verdict `{PASS|BREACH|UNKNOWN_EVIDENCE, failed_claims[], unresolved[], scope_valid, versions_valid}`。`hypothesis_id` / `source_id` 是同源判定与 lineage 的钥匙：没有它们，hypothesis 诱导出来的检索会被当成独立确认。Phase 1 授权 proposed、Phase 2 验证 realized，scope/version/graph/evidence 同一 snapshot。`推测`（概念契约参考；无实现，原源已移出）
- **冷启动**（FIRME §6.5）：period 1 无 prior memory → 从 CRM/通讯录导出稳定 head + canonical 名，先建 registry；历史数据按 period 回填、不跨期合并；alias 只从**已出现过的** surface form 学，不从未来数据回填——这是 final-period alias 增益可信的前提。`已核`（契约）
- **match 日志**（`推测`，两篇 digest 未给 schema，按可回算倒推）：`{surface, layer_hit, score, anchor, alias_written, period}`；没有它算不出 alias 贡献，也回溯不了 false merge。
- **不做**：topic 与 product 不合并身份（融合只加引用）；未匹配不删边（σ 归零也保留）；未匹配不推断「不是同一实体」。`已核`
- **工具**：现成 ER/去重或 MDM 产品可承接前三级匹配；论文没有与它们的头对头成本，build/buy 在 digest 层面只能给框架。`推测`

### 组织/成本

- **owner**（`推测`，两篇 digest 无组织出处）：registry/alias store 归数据平台或 MDM；merge/split 的 domain policy 由业务域 owner + 合规签字；抽取/匹配管线归应用团队。三个 owner 缺一个，registry 就会退化成谁都能写。
- **建设**：registry/alias store 1–2 人周（`推测`）；policy/claim 表 2–4 专家人日（`推测`）；状态机/审计存储 2–3 人周（`推测`）。
- **每次运行**：每文档一次 LLM 抽取，幻觉 3.3–7.4%、normalization error 3.2–22.16%（随域变化）。`已核`
- **人审**：评估期 200 units/setting（`已核`）；按 0.5–1 人日/200 条估（`推测`）；写侧另加 20–50 条 false-defer 样本。
- **省钱项**：semantic matching token −40.3%（`已核`，仅 investor calls × Opus × final period）；alias store 的构建/维护要单列——别名复用会省钱，但不是免费。
- **维护**：本体/阈值/alias 审核 0.5 人日/月（`推测`）；policy 版本变更需重审，重审成本未测。

### stop condition

- merge precision <90%，或 alias 组 reattachment recall 增益 <5pp → 停，回滚这批 alias。`推测`（停线是 digest 的预登记建议，不是论文验证过的阈值：Full FIRME 自己的 merge precision 就是 85.6–97.5%（4 settings），部分设置已低于 90%）
- 200 条人审的 Wilson CI 宽于 ±10pp → 扩样本，不扩域。`已核`（digest 建议线；区间可算，±10pp 未校准）
- false merge 引起的下游任务错误超过预写可接受线 → 停，先修 registry。`推测`（「可接受线」论文未给，也没有下游错误测量）
- 写侧：false-defer >20% → 放宽 claim 范围或补证据；unresolved conflict >10% → 先解决冲突。`推测`（契约来自 Commit Boundary，阈值是 digest 的建议线）
- 无 domain policy、审计存储、事务或可控写路径 → 不开写路径，只做只读/影子。
- 单域试点算不过账：年省工时 < registry + 人审 + 维护 → 停（成本项多为 `推测`，此线只能当预登记假设）。

### 第一个 sprint

2 周、单域、1 个 period 影子运行（period 长度按域定：investor 式月度，或 S&P 式 reporting period；不接线上写权限）；不做 short-term fusion（避开 $100K 阈值——单月现金流流入 > $100K 才进 cf-signal 图——与 product–topic 本体）：

1. 从 CRM/通讯录导出稳定 head + canonical 名；冻结「speaker 变、head 不变」。
2. 建 registry 表，实现 identifier → normalized name → alias 三级匹配；alias 持久化；semantic fallback 先关、留开关。
3. 200–500 份文档过抽取，按 head + typed target 建边；五态 + σ（0.5 起、匹配 +0.2、未匹配 ×0.8、<0.01 归零但不删边）。
4. merge/split 提议只进队列不落盘；`UNVERIFIED` 只进推理；同源检索不算确认；每次 match 落日志。
5. 标 200 incoming units，出 alias on/off 的 CMR、merge precision、reattachment recall；20–50 条 merge 案例出 false-defer。
6. 交付：registry 表 + edge 表 + match 日志、三数基线报告、阈值/参数记录、预写 go/no-go、alias 回滚预案。

**出口**：三数可复算；alias 增益与 false merge 都有初值；merge precision 过不过 90% 有明确答案；false-defer 有初测。任一缺失就不扩域。

### 客户指标/V3

- **受益者**：投研/CRM/MDM 团队与合规审计。痛点：同一客户/产品跨源碎裂、证据挂不上、重复调研、错误合并后返工。`推测`
- **指标**：CMR、merge precision、reattachment recall、每千条观察的调研工时、false merge 返工单、false-defer 率、每千次合并的人审工时。
- **反事实**：最接近「不做 registry」的对照臂是 LLM-Norm（每期独立语义归一化，再做跨期确定性匹配；不是完全无身份对齐）：investor/Opus CMR 8.2%、S&P/Opus 23.9%，同设置 Full 为 30.4% / 57.4%，4 个 dataset–backend 设置上比值 2.3–3.7×。`已核`（CMR 不等于任务成功率）
- **试点**（`推测`）：单域、200–500 文档、alias on/off。成功 = CMR 相对 +10pp、merge precision ≥90%、调研工时降 ≥10%、20–50 案例 false merge 0 且 false-defer ≤20%；失败 = merge precision <90% 或 alias 增益 <5pp 或 false-defer >30%；停止线 = 年省工时 < 维护成本。
- **补一个任务级指标，别只报 CMR**：例如同一客户历史证据的引用正确率（指标本身待试点时定义，`推测`）。

### 反例

- **外部效度差。** 专有投资人数据（10 个月度 period）与 S&P 500 transcript（297 家公司、3 个 reporting period、无结构化现金流）是两个 period 口径；单一 product–topic 本体；阈值在 T−1 上选再评 final period。换域 alias 增益可能不到 5pp，registry 就变成固定成本。`推测`
- **alias store 自己就是污染通道。** Full FIRME 的 human-audit merge precision 85.6–97.5%（对应错误率约 2.5–14.4%，由该区间补算）；错误 alias 会把后续同一 surface form 的出现持续路由到错误历史——污染幅度论文未测、无自动回滚。所以「一次 false merge 的代价超过全部 alias 收益」是 `推测`；对错误合并零容忍的下游要先测传播再开 alias 写。
- **写侧这一半没有实现证据。** Commit Boundary 是概念架构，无实现、无 false-defer 数字；domain policy 编写成本未测，promotion 正确性依赖外部标注。真建 gate 可能拦住大量正确变更，把成本转给人工。
- **不划算的常规情形**：实体名稳定、单次会话、无跨期观察——FIRME 自己列了这些「别用」条件；此时 registry + alias + 人审是纯固定成本，而论文没有与现成 MDM/ER 的 build/buy 头对头。`推测`
- **可能修错地方。** 客户痛点是「忘了」而不是「认错了」时，钱应先进 memory/检索；CMR 高不等于 agent 任务成功。`推测`

## 关联

- [FIRME digest](../../../src/papers/2610.40482-firme/digest.md)
- [Commit Boundary digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37407)
- [findings](./findings.md) · [frontier](./frontier.md)
