---
status: draft
deliverable_status: draft
updated: 2026-11-09
target: 工程负责人 / 架构师
basis: E-01–E-20, C-03; topics 各派 mechanism
---

# 02 · 工程实施：把本体接进 harness 的做法

> 这份交付物回答：**本体拿进来之后，到底能帮什么；如果我要做某件事，工程上从哪一步开始、接口长什么样、开源/论文里有没有能照抄的东西。**
>
> 它不建本体，也不评价本体质量；它假设你已经有（或能拿到）一份领域本体，问题是怎么让它被机器执行。
>
> **证据等级**：接口/公式/代码锚点标 `已核` 或 `已核（代码）`；工程配方、阈值、人日估算标 `推测`。交付物只引 E-xx，细节回 `topics/`。
>
> **R1–R9 是从 `topics/` 各派 `mechanism.md` 抽取的工程配方，不是新的 E。** 它们回答「怎么做」，不回答「做了有没有用」；效应量仍以 E-xx 为准。

## 0. 一句话与五步法

**本体的工程问题不是「建什么本体」，而是「把哪条判据放在哪个时刻、以什么形态执行、用什么尺子验收」。**

五步：

1. **定错**：你要防的是什么错？可逆吗？会扩散吗？
2. **选位置**：动作前 / 输出时 / 输出后 / 落盘前 / 跨轮 / 跨运行；或者轴外的读路径/供给。
3. **选形态**：engine（引擎求值）/ compiled（编译成约束）/ context（注入）/ label（只当标签）。
4. **定接口**：这个位置拿得到什么事实？输出什么字段？三态怎么表示？
5. **定尺子**：按机制选指标；先建账本，再谈效果。

**先看你要做什么：**

```
你要让本体帮你做什么？
├─ 让模型知道得对 ──────────────▶ R1（K1）/ R2（投影）/ R3（编译）
├─ 让产出可审计 ────────────────▶ R4（证据契约）
├─ 让错误被抓住 ────────────────▶ R5（checker）
├─ 让不该做的动作做不了 ────────▶ R6（可逆性闸）
├─ 让跨轮记得对 ────────────────▶ R7（身份/记忆）
├─ 让检索结果可见/不可见 ───────▶ R8（读路径）
└─ 让落盘有授权 ────────────────▶ R9（只能设计，无实现）
```

## 1. 先定错：五个问题

| 问题 | 如果答案是 | 去哪 |
|---|---|---|
| 错误可逆吗？ | 可撤销 | 判定/checker 优先 |
| 错误会扩散到下游吗？ | 会 | 加 evidence/checker；不要只做事后审计 |
| 错误会污染后续轮次吗？ | 会 | memory/身份 |
| 错误不可逆且代价高吗？ | 是 | 动作前/落盘前 |
| 判定所需事实拿得到吗？ | 拿不到 | 先补状态/观测；不要做硬闸 |

> 这五个问题不是评分卡，是**排除法**：答不出「错误是什么/可逆吗」，就不要选机制。组织建议（非 E）。

## 2. 选位置：六个时刻 + 四个轴外位置

| 位置 | 问什么 | 本体角色 | 能阻断 | 主要代价 | 主证据 |
|---|---|---|---|---|---|
| 动作前 | 动作能不能做 | 可逆性/前置条件 | 是 | 审批/误拦 | E-04/E-13/E-15/E-16 |
| 输出时 | 产出带什么依据 | 证据契约/接地等级 | 否（只约束） | token/集成 | E-03 |
| 输出后 | 产出对不对 | 外部判据 | 是 | 每条判定/维护 | E-02/E-20 |
| 落盘前 | 证据够不够授权 | 授权判据 | 是（设计） | 无实现 | E-20 + gap |
| 跨轮 | 下一轮还记得对吗 | 状态结构/对齐 | 否（只改状态） | 维护/训练信号 | E-05/E-17 |
| 跨运行 | 同一输入能复现吗 | 一致性锚点 | 设计 | 无实现 | 设计提案 |
| 读路径（轴外） | 检索结果能不能看 | 策略过滤 | 是（best-effort） | 每批×每节点查询 | E-20 |
| 供给（轴外） | 查询怎么编译 | TBox/映射/重写 | 否 | 映射维护 | E-20 |
| 推理期（轴外） | 条件成不成立 | 条件公理/三值 | 是（条件） | 覆盖率 | E-16 |
| 训练（轴外） | 训练数据怎么筛 | 规则 | 否 | 离线 | 无 E |

**选择规则**（组织建议，非 E）：

- 可撤销、会扩散 → evidence + checker。
- 会污染后续轮次 → memory。
- 不可逆、对外 → action。
- 不可逆、持久化 → commit（但先看 R9：现在没有实现）。
- 要求可复现 → determinism（同样没有实现）。

## 3. 选形态：五种，别把 context 当低配 engine

| 形态 | 机器做什么 | 什么时候用 | 不代表 |
|---|---|---|---|
| `engine` | 推理器/引擎直接求值：DL、SHACL、查询重写 | 需要「本体一变，输出就变」的求值 | 不等于会拦/有授权 |
| `compiled` | 本体→SHACL/规则/状态结构，再由代码执行 | 需要把本体变成可测试的约束 | 不等于编译正确 |
| `context` | 进入 prompt/上下文，模型自行使用 | 知识供给、可读性优先 | 不是弱执行，是不执行 |
| `label` | 只当标签表/schema/分类 | 命名、类型、路由 | 不参与判定 |
| `none` | 没有执行，或本体不是被测变量 | 概念/生成/评测 | 不能当「执行了但无效」 |

**一个反直觉的结论**：`engine` 内部至少四种语义（E-20）；「有引擎」不是强度刻度。选型时先问「机器到底做了什么」，再问「它能不能改变走向」。

## 4. 九条工程做法（R1–R9）

> 每条都按「目标—接缝/形态—最小数据契约—做法—证据—验收/停」写。接口字段和阈值多数是工程配方（`推测`）；效应量来自 E-xx。

### R1 · K1 语义层：先把名字和单位对齐

**目标**：用最低成本拿到已测最大的一层知识增益。

**接缝/形态**：供给 / `context`。

**最小数据契约**：tag registry `{label, unit, quality_flag, aliases[]}`；slot map `{entity_type, slot, unit}`。

**做法**：

1. 从历史误判里选 3 个代表性任务，标出 primary trap。
2. 统一命名、单位、别名；补单位换算；不改结构。
3. 用同一模型回放 K0/K1；报 primary-trap avoidance，不只看总分。

**证据**：K0→K1 +54.6pp（E-12；单工厂、9 任务、答案基本写在文本里）。

**验收/停**：3 个任务的 primary-trap avoidance ≥0.90（工程建议），且剩余 trap 与深知识无关 → 停在 K1，不建塔。

### R2 · 知识投影：把领域知识写成固定分节的文本

**目标**：让模型在封闭域「知道得对」，而不是「查得到」。

**接缝/形态**：供给 / `context`。

**最小数据契约**：

- 投影头：`system_id, tower_version, projection_version, generated_at, covered_sections, projection_chars, rubric_version`。
- 投影体：固定分节顺序（概览 → tags/bindings → assumptions → derivations → knowledge → 安全边界），每条陈述带 `[node_id]`。
- 映射表：`statement_id → node_id`（与投影同版本）。

**做法**：

1. 先做 K1；K1 不够再做投影。
2. 从描述记录生成约 45k 字符的文本；冻结分节顺序，顺序变更按行为变更处理（打乱句序 0.777→0.685）。
3. 本体/投影/知识节点同步；tag/单位/假设/推导任一变更 → 重生成 + 递增版本。
4. 运行教训在抽取时并入 knowledge node，不要让 agent 查询时自己查日志（日志检索 4/80 次被调用）。

**证据**：K1→K2 +19.8pp；文本 pooled 0.777，但排序非普适；9B 带投影 0.737 > 750B 不带 0.672（E-12）。

**验收/停**：K2 相对 K1 <5pp → 停；投影 >60k 字符或维护 >2 人周/月 → 停；工具调用率 <20% → 不把审计寄托在工具上。

### R3 · 证据编译：只买 claim + 逐字 span

**目标**：在重复检索多的语料上省 token，不承诺准确率。

**接缝/形态**：供给 / `compiled`。

**最小数据契约**：claim index `{claim_id, text, span_start, span_end, chunk_id, source_version, extractor_version, acl}`；per-tool policy `off|compiled-only|compiled-first`；评测表 `{query_id, arm, hit/miss, token_in/out, latency, rounds, gate_verdict, citations}`。

> claim–leaf = 主张 + 逐字证据 span 的叶子节点；不是摘要，也不是整段 chunk。

**做法**：

1. 先跑基线：同语料、同 harness 的准确率、token/问、p95、轮次。
2. compiler v0 只抽 claim + span；span 对不上就丢，不让模型修。
3. 保留原词法检索器；树只做 carrier，不做 router；默认证据替换 + raw chunk fallback。
4. 量 `p_h`、miss penalty、`c`、`Q`；算 `p_min = 2% + c/(0.929Q)`。

**证据**：hit −91%、miss +1.9%、平均 −38%；准确率 neutral；PageIndex 在 FRAMES 规模为负；配对子集时延约 3×（E-08/E-14）。

**验收/停**：`p_h < p_min` → 停，转 harness 侧（收紧读预算、改停策略、缓存、并行检索）；p95 超预算 → 只在小片流量灰度；span 覆盖 <50% → 不买。

### R4 · 输出证据契约：让答案带依据和接地等级

**目标**：把「无根据的结论」变成可审计的字段。

**接缝/形态**：输出时 / `compiled` 或 `context`。

**最小数据契约**：`{answer, observations[], grounding: entailed|supported|related|unrelated}`；E=∅ 时不报 grounding；observations 引用 concept card / ASK / SELECT bindings。

> grounding = 接地等级，描述答案与本体观察的关系强度；它不是本仓库的证据等级（已核/推测/存疑）。

**做法**：

1. 生成 concept cards（1–2k 字符/卡）；接 `DESCRIBE` / `ASK` / `SELECT`；空结果走 BM25 fallback。
2. 名字链接：精确 → 多义候选 → 未知名字先 BM25 取候选再重排。
3. 200 题回放；报检索率、引用率、每问 calls/tokens；grounding 等级单独校准。

**证据**：平均 50.5%/68.1%；Tests 1–2 +10–15pp；同 8k 预算 84.9% vs 66.7%；等级是模型自评、未校准；检索是主瓶颈（E-03）。

**验收/停**：检索率 <50% → 先修检索；未知 IRI >20% → 先补本体；tool actions >10 或 generated tokens >5,000 → 停/降级；grounding 通胀（entailed+supported >90%）→ 抽样校准，不自动放行。

### R5 · 输出后 checker：先超过空结果重试

**目标**：用本体当外部判据，查出结构/声明/模式错误。

**接缝/形态**：输出后 / `compiled`（本体→SHACL/checker）或 `engine`。

**最小数据契约**：输入 `{query, bindings, ontology/schema, data_summary}`；输出 `{verdict: pass|flag|unknown, constraint_id, query_fragment, message, evidence}`；unknown 不阻断。

**做法**：

1. 先建空结果重试基线；只有能抓「有结果但答错」的增量，才建 checker。
2. 选来源：data-derived（FA 低）或 curated（catch 高但 FA 高）；不要盲目组合；curated 先审计/补声明。
3. 200 题回放；报 catch / FA / precision / per-1k cost；人工抽 50 条。
4. 三态显式化：pass / flag / unknown；不要把 unknown 合并进 pass。

**证据**：curated catch/FA 18.9/16.8、data-derived 8.2/3.5、masked LLM 5.0/1.8；precision 57.1/72.3/93.7；空结果重试 catch 79.2/FA 0；LLM judge 40 修好/83 修坏（E-02）。E-20 的代码核对发现第三态在 shell 退出码被折叠。

**验收/停**：增量 catch <5pp 或 FA >15% → 停；per-1k 成本 >人工审核 1/3 → 停；语义错为主 → 换 LLM judge/人工，但 judge 要先测净修复（fixed − corrupted）/成本/稳定性。

### R6 · 动作前可逆性闸：只在不可逆、高代价、弱模型时试

**目标**：在副作用发生前，按「是否存在可接受的逆操作序列」剪枝/审批。

**接缝/形态**：动作前 / `compiled`。

**最小数据契约**：

- Layer A：静态动作本体，mutating tool 的 T1–T5 逆关系 + curator 权重。T1 精确逆；T2 边界内可逆；T3 可补偿但有损；T4 不可逆消费；T5 外部副作用（fail-closed）。
- Layer B：状态投影 `slot(entity,id)=value` + `state_hash`。
- 输出：`{decision, phi, pi, bottleneck}`；`APPROVE|VETO|ESCALATE` 是 DecisionPolicy，不是本体。
- 日志：`{tool, entity, tier, phi, tau, decision, reason}` + 审批人/时间/回滚。

**做法**：

1. 列 mutating tools / 槽位；写 T1/T4/T5 本体 v0。
2. 接只读状态；反向搜索深度 3–5、环路检测；多候选取 `max min φ`，同分取最短；τ=0.80 按域保留率校准，不跨域照搬。
3. shadow 200–500 决策；标 100 条 blocked 的 false-veto；报 harm/审批/task success。
4. 先做可逆性路由 + shadow；不要一上来做六模式分配（CASEL 的 `γ_m` 是假设）。

**证据**：airline 4/6 模型 +0.11–0.18；18 格仅 8 改善；retail/强模型回退；T1-only ≈ blanket veto；false-veto 未测（E-04）。CASEL 的 harm–approval–cost 前沿是模拟，无本体变量（E-15）。

**验收/停**：shadow false-veto >5% → 降 advisory/停；同轨迹配对 Δ≤0 且 T1-only≈full → 结构贡献不成立，停；保留率 <20% 或 >95% → 阈值失效；拿不到真实状态 → 不做硬 veto。

### R7 · 跨轮身份/记忆：先 registry，再状态

**目标**：让同一实体跨期可对齐，让冲突/失效可保留。

**接缝/形态**：跨轮 / `compiled`。

**最小数据契约**：

- registry `{canonical_id, type, normalized_name, aliases[], first_seen, last_seen, source_version}`。
- edge `{head_id, target_id, relation, source_indicator, observations[], state, score, first/last_seen}`。
- relational state `{fact_id, validity, scope, supersedes[], conflicts[], concept_id}`。
- reasoning state `{request_id, used_facts[], roles[], priority[]}`（每请求生成，不回写事实）。
- match log `{surface, layer_hit, score, anchor, alias_written, period}`。

**做法**：

1. 从 CRM/通讯录导出稳定 head + canonical name；冻结「speaker 变、head 不变」。
2. registry v0：identifier → normalized name → learned alias → semantic fallback；alias 持久化；记录命中层级。
3. 200–500 份文档过抽取；按 head + typed target 建边；落五态 + σ；`SUPERSEDES`/`CONFLICTS_WITH` 先用人工规则。
4. 评测三层：抽取（round-trip/归一化）、身份（CMR = MMR × merge precision、reattachment recall）、状态（Complete Retrieval、Acc@complete）。CMR 是跨期匹配率；单看 CMR 会把「合并更激进」误判成进步，要和 merge precision 一起看。
5. 写侧 merge/split 只进队列，不自动落盘；`UNVERIFIED` 只进推理，不授权。

**证据**：alias CMR +7.8–12.1pp；EvoMem Acc@complete +11.5/+31.2；merge precision 85.6–97.5%；false merge 污染未测（E-05/E-17）。

**验收/停**：merge precision <90% 或 alias 增益 <5pp → 停/回滚（90% 是预登记线，FIRME 自身部分设置已低于 90%，按域重标）；Complete Retrieval <80% → 先修检索；冲突 >20% → 先修冲突；没有训练信号 → 不训 GRPO。

### R8 · 读路径过滤：只做可见性，不要当授权

**目标**：在检索结果进入上下文前，按用户上下文过滤。

**接缝/形态**：`read-path` / `engine`。

**最小数据契约**：策略图 `urn:graph:policy`；SHACL-AF（SHACL Advanced Features）`NodeShape` + `sh:SPARQLTarget` + `sh:SPARQLRule` + `tg-pol:blocks`；请求带 `user_context`。

**做法**：

1. 有策略时，缺 `user_context` 直接报错（fail-closed）。
2. 对候选节点跑 target + rule；命中 block 的节点剔除。
3. 明确写清：异常时 fail-open、只删 subject 侧、首命中即停、缓存 30–60s。
4. 构造异常 policy 和 object 方向用例，先测泄漏，再上线。

**证据**：trustgraph 代码级；fail-open、只删 subject、单实现（E-20）。

**验收/停**：需要对象方向也受控、需要写授权、需要审计级「为什么允许」→ 这个实现不够；先补第二个独立实现，再谈升时刻。

### R9 · 落盘前授权：现在只能设计，不要声称已落地

**目标**：把「可推理的证据」与「有权推动持久化的证据」分开。

**接缝/形态**：落盘前 / 无实现（设计）。

**最小数据契约**：

- `mutation_context {mutation_id, class, head_id, target_id, policy_version, snapshot_id}`。
- `q_m[] {claim_id, predicate, scope, version}`。
- `evidence {obs_id, claim_id, role, provenance, hypothesis_id, source_id}`。
- `promotion {claim_id, obs_id, role, validation_basis, policy_version, promoted_by, promoted_at}`。
- `verdict {status: PASS|BREACH|UNKNOWN_EVIDENCE, failed_claims[], unresolved[], scope_valid, versions_valid}`。

**做法**：

1. 先做一个 mutation class（如 person merge），不要覆盖所有写路径。
2. 证据齐 + 冲突清 + 版本有效三条全过才 commit；`UNVERIFIED` 只进推理。
3. 两阶段：Phase 1 授权 proposed；Phase 2 验证 realized；同 snapshot 检查 scope/version。
4. 先测 false-defer：20–50 条样本。

**证据**：只有概念架构；四个开源项目里没有单次写授权（E-20）。false-defer 未测。

**验收/停**：没有 domain policy/审计存储/事务/可控写路径 → 不做；false-defer >20% → 放宽 claim/补证据；unresolved >10% → 先解决冲突。

## 5. 开源参考实现：能抄什么，别抄什么

| 项目（commit） | 位置 | 形态 | 能抄 | 别抄 | 代码锚点 |
|---|---|---|---|---|---|
| trustgraph `184f622` | `read-path` | `engine` | 策略图 + `user_context` 契约；SHACL-AF target/rule | fail-open、只删 subject、单实现 | `policy_filter.py` |
| semantica `39cf721` | `checker` | `compiled` | 本体→SHACL 的派生路径；pyshacl `inference="none"` | 把 CLI 校验当 in-loop；派生 shapes 未测 | `OntologyEngine.to_shacl` |
| ontop `964dbb7` | `supply` | `engine` | TBox 饱和 + 查询重写 → SQL；R2RML 映射 | 把它当闸/判定器；只支持 OWL 2 QL | `QuestQueryProcessor` |
| open-ontologies `375fbc4` | `none`（工具面/CI） | `engine` | JSON 三态（通过/违反/未检查完）；`closure_diff` 影响报告；verified/Core 边界 | 把它当写授权；只看 shell 退出码（第三态会被折叠）；本次未跑通 | `shacl.rs` / `shacl_verified.rs` |

> 出处：E-20 与 [execution-forms](../../topics/execution-forms.md#代码级核对2026-11-09)。四者都是只读代码、未做对照实验；**代码能跑 ≠ 机制有效**。要读代码细节，从 execution-forms 的代码核对段进 4 个 digest；本页只抽接口与边界。

## 6. 论文/开源给的「准确指示」到什么程度

| 层级 | 能给什么 | 例子 | 能不能照抄 |
|---|---|---|---|
| 代码级 | 真实接口、调用链、失败行为 | 4 个开源项目（E-20） | 抄接口与边界；不抄效果 |
| 公式级 | 可算的盈亏平衡/代价 | 编译 `p_min = 2% + c/(0.929Q)`（E-14）；CASEL `J(m)`（E-15，`γ_m` 是假设） | 代自己的数；不抄论文的 `c`/`γ` |
| 协议级 | 判定/标注/三态 | catch/FA 分开报（E-02）；grounding 四等级（E-03）；promotion 七条（Commit Boundary，概念） | 抄协议；不抄阈值 |
| 参数级 | 具体设置 | POLAR T1–T5/τ=0.80；OntoAct 三值；FIRME 匹配顺序/0.8 | 只当起点，按域重标 |
| 流程级 | 步骤顺序 | CAI parse→chunk→enrich→validate→assemble→register；OA-RAG DESCRIBE/ASK/SELECT | 抄流程；不抄规模 |
| 概念级 | 设计问题 | commit gate；determinism；多智能体共享本体 | 只能当设计清单，不能当实现 |

**结论**：论文/开源在**接口、公式、协议、参数**上给了可操作的指示；在**端到端架构**和**效应量**上没有。不要指望一篇论文给出「拿本体做 X」的完整 recipe；能抄的是零件，组装要自己测。

## 7. 参考架构（组织建议，非 E）

```
request
  │
  ▼
context builder ──◀ K1 / 投影 / 编译（03）
  │
  ▼
agent
  │
  ├──▶ tool call ──▶ action gate ──◀ T1–T5 + 状态投影（01）
  │                     │ allow / veto / escalate
  │                     ▼
  │                   execute
  │
  ▼
output
  ├──▶ evidence contract ──◀ grounding levels（02）
  └──▶ checker ──◀ 本体→SHACL/规则（02）
          │ pass / flag / unknown
          ▼
      commit gate ──◀ 授权判据（01；设计，无实现）
          │
          ▼
      memory ──◀ registry + relational state（04）
```

**读法**：

- 不是每个位置都要上；按 §1 的错误性质选 1–2 个。
- 每个箭头都要有数据契约；没有契约的「接缝」只是概念。
- `commit gate` 标注为「设计、无实现」：它没有实现（E-20）。

## 8. 最小落地路线

| 阶段 | 时间 | 做什么 | 产出 | 出口 |
|---|---|---|---|---|
| 0 | 3–5 天 | 建账本：token/时延/决策/审批/回滚；跑基线 | 账本 schema + 基线分布 | 能按机制出分布 |
| 1 | 2 周 | K1 + 一个接缝 shadow（投影/checker/action 三选一） | 回放结果 + 工时 | 有增量，且不是平均掩盖 |
| 2 | 2 周 | 扩样本；标 false-veto/FA；算 stop 线 | go/no-go memo | 过门/停 |

**不要**：同时上三个接缝；先建整座塔；用平均 −38% 立项；没有账本就上机制。

## 9. 验收与 stop：按机制选尺

| 机制 | 主指标 | 过程指标 | 反事实 | 停线（工程建议，非 E） |
|---|---|---|---|---|
| K1 | primary-trap avoidance | token | K0 | 剩余 trap 与深知识无关 → 停 |
| 投影 | primary-trap/element | 字符数/维护人日 | K1 | <5pp、>60k、>2 人周/月 |
| 编译 | token/问、p95 | `p_h`/miss、`c`、`Q` | 词法检索 | `p_h < p_min` |
| evidence | 准确率、引用率 | 检索率、grounding 校准 | 纯文本 RAG | 检索率 <50% |
| checker | 增量 catch、FA、净修复 | per-1k 成本 | 空结果重试 | catch <5pp、FA >15% |
| action | harm、审批、false-veto、task success | 保留率、φ | 不上护栏 | false-veto >5% |
| memory | CMR、merge precision、Acc@complete | 抽取层误差 | 不做 registry | precision <90% |
| read-path | 泄漏率、误拦 | 延迟 | 不过滤 | fail-open 未修 |

## 10. 反模式

1. **把 context 当约束。** 投影里写规则 ≠ 规则被执行；硬约束另进 01/02。
2. **把 engine 当授权。** 有求值器 ≠ 有 commit gate；open-ontologies 只做影响报告/CI 门（E-20）。
3. **把 curated 当权威。** curated checker 的 precision 仅略优于随机；先审计/补声明（E-02）。
4. **用平均 −38% 立项。** 它是 −91% 与 +1.9% 的混合；先量 `p_h`（E-08/E-14）。
5. **用 reward/accuracy 证明护栏。** 用任务账验收风险机制会漏掉「被拦住的伤害」和「被误拦的正确动作」（C-03/E-04）。
6. **把 T1-only 当结构有效。** T1-only ≈ blanket veto，增益不比 full 小；结构贡献未隔离（E-04）。
7. **把 grounding 当形式保证。** 等级是模型自评、未校准（E-03）。
8. **把 LLM judge 当免费升级。** 检错更多，但 40 修好/83 修坏；先测净修复/成本/稳定性（E-02）。
9. **把 SHACL 通过当语义正确。** shapes 派生可能过度/不足；`inference="none"` 不展开子类（E-20）。
10. **把 commit gate 概念当实现。** 没有实现、没有 false-defer 数据（E-20）。
11. **把本体质量当落地条件。** 落地取决于「位置 × 成本 × 使能条件」，不是本体多完整（E-19，`推测`）。
12. **没有账本就上机制。** 算不出 false-veto/`p_h`/审批成本，就无法 go/no-go。

## 11. 还缺什么

与 [01 现状 §5](../01-capability-status/README.md#5-距离还差什么差多远) 同一张缺口表：false-veto 标注、写路径实现、独立复现、跨域效度、接地等级校准、第二个 read-path 实现、跨运行确定性、单位成本、多智能体共享本体。

**这些不是本交付物的前置**；它们是下一步研究/工程的方向。

## 12. 与另外两份交付物的关系

- **[01 现状](../01-capability-status/README.md)**：哪些能做、哪些不能。
- **02（本份）**：拿本体做某件事的具体做法。
- **[03 机制参考](../03-mechanism-reference/README.md)**：为什么是这些位置/形态，证据边界在哪。

## 13. 期待与数据需求（验收规格）

> 这一节不是结论，是**每条 recipe 的验收规格**：把「做完应该看到什么」写成可证伪的句子，再倒推要量什么。数据缺在哪里，就回 `topics/` 或 `frontier` 补。这是验收规格（非 E）。

| Recipe | 期待（可证伪） | 支持它需要的数据 | 现在的来源 | 缺口 |
|---|---|---|---|---|
| R1 K1 | 目标域 primary-trap avoidance ≥0.90 | K0/K1 回放；3 任务；trap 标注 | E-12 | 跨域 |
| R2 投影 | K2 相对 K1 ≥ +5pp，且 ≤60k 字符、维护 ≤2 人周/月 | K1/K2 回放；字符；维护工时；顺序消融 | E-12 | 跨域；多设备 |
| R3 编译 | `p_h ≥ p_min`，p95 不超预算 | `p_h`/miss/`c`/`Q`/p95/span 覆盖 | E-14 | 自己的流量 |
| R4 证据契约 | 检索率 ≥50%，引用率 ≥85%，grounding 可校准 | 200 题；检索率/引用率/等级标注 | E-03 | 等级校准；句级 span |
| R5 checker | 增量 catch ≥5pp、FA ≤15%、净修复 >0 | 200 题；空结果基线；catch/FA/per-1k/净修复 | E-02 | 自己的故障分布 |
| R6 动作闸 | false-veto ≤5%，harm 降，task success 不降 >2pp | 200–500 shadow；100 blocked 标注；四轴指标 | E-04/E-15 | false-veto；同轨迹配对 |
| R7 记忆 | CMR/Acc@complete ≥ +10pp，merge precision ≥90% | registry on/off；200 units；三层评测 | E-05/E-17 | 自己的域；传播 |
| R8 读路径 | 泄漏率 0（含 object 方向），误拦可接受 | 第二实现；异常/对象用例；延迟 | E-20 | 第二实现 |
| R9 落盘授权 | false-defer ≤20%，unresolved ≤10%，审计可追 | 一个 mutation class 实现；20–50 样本 | 概念 | 实现；标签 |

**怎么用**：每条期待对应一个 stop line；先量「支持它需要的数据」那一列，量不出来就停在这一步，不要用「平均收益」替代。
