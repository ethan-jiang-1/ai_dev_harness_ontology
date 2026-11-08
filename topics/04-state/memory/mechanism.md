# 跨轮记忆 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

一个回合结束、下一个回合开始时，没有立即动作，但失真是缓慢累积的：过期事实、错误合并、未解决冲突会作为前提进入下一轮。

## 事实集合 vs 状态

| | 事实集合（常见做法） | 状态（本仓库主张） |
|---|---|---|
| 单元 | 一条独立事实 | 事实 + 它与其他事实的关系 |
| 冲突 | 并存，无人裁决 | 显式记录，直到被解决 |
| 失效 | 无失效条件 | 每条带失效条件与时间 |
| 使用 | 检索回一堆条目 | 按当前请求筛选可用子集 |

丢掉关系后，模型每轮都要重做一致性推导，结论可能不同；多次运行不收敛。

## 本体在此的角色：克制（FIRME）与增量构建（EvoMem）

**FIRME：本体不承担自由推理；它承担对齐与印证条件。**

- 定义哪些是实体、哪些关系可被推翻、冲突如何表示。
- 不定义通用推理规则，不要求运行时推导任意隐含结论。
- 对关键关系的赋值可设条件（例如两种模态互相印证时才成立）。

FIRME 的本体是最小固定形态：product/topic 两类 + `CONTAINS`/`PARENT_OF`；Rule 4 只借它把 topic 讨论关联到 product，融合只加引用，topic 与 product 身份不合并（digest §3.2/§6.5）。「本体改动只影响槽位与印证条件、不扩散成不可控推理路径」是架构推断：digest 没有改动前后的对照，维护者与变更流程也未定，本体按 use-case 定制 `推测`。

**EvoMem：本体不是现成的，是从事实长出来的。**

- 每个 fact 挂到最具体 concept；`PARENT_OF`/`CONTAINS` 组织 concept/fact 图。
- 增量修订用 `CREATE/MERGE/SPLIT`；事实层用 `SUPERSEDES` 表示更新、`CONFLICTS_WITH` 保留未解决冲突。
- 代价：层级错误会通过 `concept_id` 挂载传进 relational state（digest §5.6）；CREATE/MERGE/SPLIT 的自动质量评估仍是开放问题（§9）。
- 所以「本体克制」不能读成「本体稳定」：FIRME 的本体是给定的小本体，EvoMem 的本体是持续维护的对象。

## FIRME 的设计

1. **身份先于内容。** registry 分层匹配：ID → 规范化名 → learned alias → 语义 fallback（同类型，score≥0.8）；错误匹配会把后续观察路由到错误历史。
2. **topic 与 product 分开。** 主题讨论可以印证多个产品，但不合并身份；印证是引用，不是覆盖。
3. **未匹配 ≠ 结束。** `σ=0.8σ` 衰减、边不删除、Fading 后可 Reactivated；但 miss 可能是输入缺失/没有观察机会。
4. **短期融合只加引用。** 结构化现金流 + 非结构化讨论 → strong-interest；source indicator 保留。

## EvoMemState 的两层状态

| 层 | 内容 | 由谁维护 |
|---|---|---|
| 关系状态 | 事实的有效性/scope、更新/冲突/约束 | 本体引导归纳 |
| 推理状态 | 当前请求该用哪些事实、什么角色/优先级 | 策略内化（GRPO 训练） |

前者是结构，后者是策略。混在一起会导致结构每次随请求变化，无法审计。

**边界**：Reasoning State 是自然语言/结构化规则，不是可形式验证的状态（digest §5.4）。「可审计」指字段与状态转移可回放，不是形式证明或语义真值；形式检查/审计在 §9 仍是开放问题。关系状态能检查的是 validity/scope/update/conflict 字段与确定性转移，不是事实本身对不对。

## 失效模式

- **过期事实不失效。** 新值覆盖旧值但无版本，历史结论的依据消失。
- **记忆污染难以回滚（`推测`）。** 一次错误结论进入记忆后被当作前提，错误可能自我强化；检测/回滚机制未验证。
- **检查点粒度错配（`推测`）。** 检查点若落在「任务完成」，真正需要的回滚点可能是「错误分支开始处」；两篇 digest 都未测回滚粒度，这是本页推断。
- **身份漂移。** 同一实体跨期未对齐，历史证据挂不上新版本。
- **错误合并的长期风险（`推测`）。** 一个 false merge 会把后续同名观察路由到错误 anchor（机制上成立）；「长期污染」的幅度论文未测量；merge precision 必须和 CMR 一起看。
- **本体层级错误（`已核` 机制 / `推测` 幅度）。** CREATE/MERGE/SPLIT 的误差会经 `concept_id` 挂载传进 relational state；论文未测错误率与传播幅度，自动质量评估仍开放（digest §5.6/§9）。
- **把 Reasoning State 当形式保证（`已核` 边界）。** 它是自然语言/结构化规则，不可形式验证；需要形式保证的域别用（digest §5.4/§6.3），形式审计未解（§9）。
- **把「未观察到」当「关系结束」。** 衰减不是删除；但也不能把 miss 解释成负信号。

## 与本体 / 回路的关系

本体在跨轮以 **identity registry / 对齐条件 / 冲突表示 / concept–fact 图** 出现：前两者来自 FIRME，后两者是 EvoMem 的 relational state 结构。约束强度中（能对齐、能保留冲突，不能保证语义真值）。被违反时通常没有即时信号，错误会跨轮累积。

## 实施与客户价值（A3/A4）

> 机制与参数 `已核`（两篇 digest）；停线阈值是 digest 的预登记建议，不是已验证边界；本体改动范围、组织、成本与客户收益 `推测`。数字只在 digest 的条件下成立，换域要重标。

### 实施决策

- **先建身份 registry，再升级检索或摘要。** 没有 canonical ID + alias，强化/衰减只是在碎片上累加；alias store 是记忆的前置，不是检索的附属（F2）。只加 RAG/摘要、不做 registry，等于把同一实体拆成多条 partial history。
- **事实、关系状态、推理状态分三处存。** 关系状态持久（validity/scope/update/conflict），推理状态按请求生成、只写「怎么用」不回写事实（F1/F3）。合成一张「记忆摘要」的代价是结构随请求漂移，事后答不出「这条为什么被用」。
- **更新要判定，冲突要保留。** 只有确认的更新才 `SUPERSEDES`；未裁决的进 `CONFLICTS_WITH` 并带冲突推进，不用「最新值覆盖」冒充更新。第一版不阻塞，先量冲突率（G2 未关，`推测`）。
- **policy 训练后置。** 没有参考答案/评分器就不训 GRPO；先用固定规则 + 弱监督拿基线，过门再谈训练。把「训 reasoning state」写进第一版计划，是这页要避免的过度承诺。
- **验收用配对指标，先过抽取层。** 先看 round-trip / 归一化误差（F5），再看 CMR 与 merge precision 同看、Complete Retrieval 与 Acc@complete 同看；检索率相当（85.6% vs 86.4%），但 Acc@complete 在同一基准内仍领先最强 baseline（LoCoMo-Refined 70.8，+11.5；MemSyco 68.5，+31.2），说明单看召回会把「检索更多」误判成进步（F4）；单看 CMR 同理会把「合并更激进」误判成进步（F2）。跨基准的 Acc@complete 不可相减。

### 数据/接口

| 对象 | 最小字段 | 来源 |
|---|---|---|
| registry | `canonical_id, type, normalized_name, aliases[], first_seen/last_seen, source_version` | FIRME §6.5 |
| relationship edge | `head_id, target_id, relation, source_indicator(1/2/3), observations[], state(五态), score(σ), first/last_seen` | FIRME §6.5 |
| persistent fact | `fact_id, text, source, timestamp, entity_ids[]` | EvoMemState §6.5 |
| memory graph | `concept_nodes[], fact_nodes[], edges(PARENT_OF/CONTAINS/SUPERSEDES/CONFLICTS_WITH)`；层级修订另有 CREATE/MERGE/SPLIT | EvoMemState §3.1/§6.5 |
| relational state | `fact_id, validity, scope, supersedes[], conflicts[], concept_id` | EvoMemState §6.5 |
| reasoning state | `request_id, used_facts[], roles[], priority[]`（每请求生成，不回写事实） | EvoMemState §6.5 |

- **协议**：匹配顺序固定 identifier → normalized name → learned alias → semantic fallback（同类型，≥0.8）；命中后把 surface form 写回 alias set，未命中才新注册。每次 match 落日志 `{head_id, candidate, hit_level, score, action}`，alias 新增要可回滚（FIRME 本身没有自动回滚）——否则 merge precision 与 false merge 都无法定位（F2）。
- **接口**：`match(input)→canonical_id|new`、`upsert(observation)`、`ingest(dialogue|doc)→facts+relational states`、`retrieve(request)→seeds+邻域`、`policy(request, facts, states)→reasoning state`、`answer(...)`。
- **抽取层**：LLM2Graph 产 `(u,r,v,d)` 与 period-local 归一化 mention，**不产别名**；先过 round-trip/归一化误差，再进 registry。抽取层是独立验收层，不能由 CMR 或答案准确率替代（F5）。
- **幂等**：`(head_id, typed_target_id, source_id, period)`；每 period 每边至多一次强度更新。
- **检索**：先 seed，再沿 `SUPERSEDES`/`CONFLICTS_WITH`/`CONTAINS` 双向遍历，不用独立 top-k。
- **参数（域相关，不可照搬）**：`σ_init=0.5`、命中 `+0.2`、未命中 `×0.8`、`<0.01` 归零但边不删、五态；semantic 阈值 0.8 是在 investor T−1 上选的（FIRME §3.3）。
- **评测（三层）**：抽取层报 hallucination / normalization error / round-trip F1；身份层报 `CMR = MMR × merge precision` 与 human-audit reattachment recall；状态层报 Complete Retrieval 与 Acc@complete。三层分开报，不用单一准确率，也不能互相替代（F4/F5）。
- **边界**：身份侧的 merge/split 授权与证据门归 [identity](../identity/README.md)；本节只保留记忆侧字段。

### 五态、融合阈值与训练配方（digest 口径）

> 这三条原先只在 digest 里；数字与条件见 [FIRME digest](../../../src/papers/2610.40482-firme/digest.md) §3.4/§6.5、[EvoMemState digest](../../../src/papers/2611.03743-evomemstate/digest.md) §6.5。

- **五态边界（N=3）。** 每 period 每条边至多一次强度/状态更新；连续 miss ≤3 仍是 Stable，第 4 次 miss 才进 Fading，Fading 后再匹配为 Reactivated。σ_init=0.5、匹配 +0.2、未匹配 ×0.8、<0.01 归零但边不删。`已核`
- **短期融合门（$100K + Rule 3/4）。** 单月现金流流入 >$100K 才进 `cf-signal` 图，否则忽略弱信号——Rule 3/4 要先有这个定义才能落地。Rule 3：同一投资人、同一 product 的 discussion + cash-flow → strong-interest；Rule 4：同一投资人的 topic 讨论 + 本体关联 product 的 cash-flow → product strong-interest，topic 仍保持 discussed。融合只加引用，topic 与 product 身份不合并；source_indicator 1/2/3 保留。`已核`
- **GRPO 训练配方（进第二阶段才用）。** G=8、temperature 1.0、rollout batch 512 / global 4096、lr 1e-6、wd 0.01、KL 0.001、clip 0.2/0.28；prompt 8192 / state 512 tokens；冻结 agent Qwen3-8B、embedding bge-m3；数据约 60K 实例（FEVER/SciFact/PersonaMem，含冲突记忆与干扰项）；reward 用「有/无 reasoning state 的答案得分差」，格式违规/答案泄露有 gate/penalty。论文未定 seed 数；自建至少 3 seeds 并报 CI。`已核`（配方；seed 口径为 digest 的工程建议）

### 组织/成本

- owner：数据平台（registry/存储）1 人、领域 curator（本体/别名审核）1 人、评测标注 1 人；false merge 复核不能由建 registry 的同一人兼任（`推测`）。
- 投入（`推测`）：registry/alias 1–2 人周；本体/概念图 1–2 人周；人审 0.5–1 人日/200 条；维护 0.5 人日/月。首个 sprint 约 5 人周（2 名工程 + 0.5 名 curator，2 周）。
- 运行：抽取每文档一次（LLM2Graph 幻觉 3.3–7.4%、归一化误差 3.2–22.16%，依域）；语义匹配只在未命中时调用，alias 复用省 40.3% token（仅 investor/Opus/final period，不含 registry 构建）；检索预算 565 token（论文设置，K 自定并记录）。
- 训练（若进第二阶段）：GRPO 需 GPU 与评分器；论文未报 GPU 小时数，成本无法估算（`推测`）。
- 隐性成本（`推测`）：一次错误合并不是一次性返工，后续同名观察会持续路由到错误 anchor（机制推断，幅度未测）；回滚依赖审计轨迹（G5 未关）。

### stop condition

> 阈值取 FIRME §6.5 / EvoMemState §6.5（停线为 digest 的预登记建议，不是已验证阈值）；成本门为本页推导。

- 质量门（`推测`）：merge precision <90%，或 alias 组 reattachment recall 增益 <5pp → 停用 alias 集并回滚，不扩域。90% 是 digest 的预登记停线，不是已验证阈值——Full FIRME 自身为 85.6–97.5%，部分设置已低于 90%，目标域要重标。
- 抽取门（`推测`）：round-trip F1 / 归一化误差未达域内基线 → 先修 LLM2Graph，不扩 registry/状态；digest 只给三层评估，没有给 stop 阈值，这条是本页推导。
- 样本门：200 条 audit 的 Wilson CI 宽于 ±10pp → 扩样本，不扩域。
- 污染门：false merge 导致的下游任务错误超过业务预设线 → 停，先修 registry；没有这条线就不上线。
- 检索门：Complete Retrieval <80% → 先修检索，不训 policy；Acc@complete 无提升或下降 → 停，检查 state 是否噪声。
- 冲突门：未解决冲突 >20% → 停，先修冲突处理。
- 训练门：没有答案/评分器 → 不训 GRPO。
- 数据门：无稳定 head ID、无跨期观察、实体名稳定、单次会话 → 不做。
- 成本门：年省工时/纠错 < 维护 + 人审 + 推理增量 → 停。

### 第一个 sprint

2 周、单域、1 个 period、shadow、可回滚；不做 policy 训练、不做 short-term fusion（避开 $100K 阈值）。

1. 定稳定 head：从 CRM/通讯录导出 canonical ID + 规范名，冻结「speaker 变、head 不变」。
2. registry v0：identifier → normalized name → alias 三级匹配，alias 持久化；semantic fallback 关（留开关），记录命中层级。
3. 事实/关系状态分存：200–500 份文档过抽取，按 `head + typed target` 建边，落五态 + σ 状态机；`SUPERSEDES`/`CONFLICTS_WITH` 先用人工规则。
4. 评测：先记抽取层 hallucination / normalization error（子样本；round-trip 按域抽样），再标 200 incoming units，出 CMR、merge precision、reattachment recall（alias on/off）；另取 200 请求，出 Complete Retrieval 与 Acc@complete 基线。
5. 预写 go/no-go 与回滚：阈值先冻结，alias 回滚脚本/流程当场跑一次。

交付物：registry + edge 表；匹配日志；三层基线报告（抽取/身份/状态）；阈值记录与 go/no-go memo；alias 回滚记录。
出口：抽取层误差在预写阈值内，且 merge precision ≥90%（按域重标）且 alias 增益 ≥5pp 且 Complete Retrieval ≥80% → 进第二阶段（关系状态 + 固定 reasoning 规则）；任一不达标 → 停在本层修 registry 或放弃记忆层。

### 客户指标/V3

- 受益者：投研/CRM（同一客户/产品跨源碎裂、重复调研）；个人助手/客服（偏好更新、冲突记忆、跨会话不一致）。`推测`
- 指标：CMR、merge precision、reattachment recall、冲突漏检率、Complete Retrieval、Acc@complete、每千条观察的调研/纠错工时、每请求 token 与时延。
- 反事实：不做 registry/状态 → 每次重新识别、独立事实 + 固定 prompt；先测当前 CMR 与 Acc@complete，否则增益不可归因。
- 试点：单域 200–500 文档 + 200–500 请求，alias on/off、state on/off 对照（`推测`）。
- 成功：CMR 相对 +10pp、merge precision ≥90%、alias 增益 ≥5pp；Acc@complete +10pp、冲突漏检 ≤10%、token 增幅 ≤20%；调研/纠错工时降 ≥10%（`推测`）。
- 失败：merge precision <90%、alias 增益 <5pp、Acc@complete 无提升或冲突率恶化。
- 停止线：年省工时/纠错 < registry 维护 + 人审 + 推理增量成本。

### 反例

- **CMR 涨不等于客户指标涨。** CMR 是 incoming edge 对到 prior memory 的比例，不是答案正确率；合并更激进也能抬 CMR。若下游是问答/建议，+10pp 可能完全不体现在任务成功上——这是本页最可能不成立处。
- **false merge 的代价不对称。** merge precision 85.6–97.5% 意味着 2.5–14.4% 的被接受匹配是错的；一个错 alias 会把后续同名观察持续路由到错误历史（机制推断，幅度未测 `推测`），回滚还要审计轨迹（G5 未关）。省下的 token/工时可能小于一次返工。
- **Fading 可能把噪声写成状态。** 未匹配不等于结束，也不等于休眠；若 miss 来自输入缺失或没有观察机会，五态只是给噪声一个确定外观，反而制造错误前提。
- **无评分器时 reasoning state 的收益未验证。** GRPO 要答案/评分器；固定 self-reflection 的初步结果甚至可能帮倒忙（50.5→48.9），说明「没有训练信号的 state」不必然优于不做。
- **两篇的合体没被验证。** FIRME 是金融跨期 ER，EvoMemState 是个人助手基准；「registry + 两层状态」是本页拼的，没有同口径实验（`推测`）。

## 关联

- [FIRME digest](../../../src/papers/2610.40482-firme/digest.md)
- [EvoMemState digest](../../../src/papers/2611.03743-evomemstate/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
