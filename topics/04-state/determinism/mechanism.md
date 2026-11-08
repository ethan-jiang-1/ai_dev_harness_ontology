# 跨运行确定性 · 机制

> 只写「它怎么跑」。判断回 [README](./README.md)（薄页，未拆 findings/frontier）；实施含义与客户价值见文末。
>
> 证据：E-06（类比）/ E-07 / E-09 / E-17；数字只在各 digest 的条件下成立。EvoMemState digest 没有报告跨运行重放，SLB 是单次生成、没有测跨运行方差——本页把两者的机制借到「跨运行」时只借结构与门槛；把它们的结论外推到跨运行的部分另标 `推测`。

## 问题

两次运行之间没有动作，只有一条性质：同一输入应得等价产物。单次执行内部的每个时刻都能改（拦、验、投影、编译、修），跨运行能改的主要是两样东西——一个不随运行变的参照（锚点），和一份能对上的运行记录。

缺了这两样，不一致容易被解释成「模型随机」；而一部分不一致可能不在模型侧（[README](./README.md)）。

## 三条不一致路径（分类为本页操作框架，`推测`；继承来自 SLB `已核`）

| 路径 | 现象 | 归因侧 | 处置 |
|---|---|---|---|
| 采样 | 同输入、不同种子/温度结论不同，且不复现 | 解码/采样 | 记日志；对交付物加一致性约束 |
| 输入 | 换种子仍复现同一差异 | 输入/接地 | 回输入侧补字段/约束/判据（`推测`） |
| 继承 | 轨迹先算答案，少数程序直接复述/继承（163/1,791，≈9.1%） | 验证缺失 | 过程审计 + 值/结构分离（E-09 `已核`） |

第三条与前两条不同向：继承让输出复制轨迹答案（44/45 可比较的 hardcoded 程序输出 == reasoning answer，`已核`），所以它可能把确定性做高、同时把保证做没；「跨运行更稳」是机制推断，SLB 没有做重复运行测量（`推测`）。因此一致性指标不能单独当质量指标（见反例）。

## 锚点：把产物变成可比结构（本页设计，`推测`）

1. 固定输入，跑 N 次（换种子 / 温度 / 模型）。
2. 每次产物按同一 `ontology_version` 投影成三段结构。
3. 比结构，不比文本。
4. 持续存在的差异回输入侧；一次性的差异记采样。

| 段 | 比什么 | 会丢失什么 |
|---|---|---|
| concept | 概念集与挂载 | 关系方向、约束强度 |
| relation | 关系集与端点 | 约束强度 |
| constraint | 约束集 / 可满足性 | 表述差异（通常是想要的） |
| coverage | 投影覆盖率 + `unparsed[]` | ——（这一行是防自欺的） |

`coverage/unparsed` 不能省：只报「差异少」而不同时报「看得少」，投影器会把漂移藏起来（设计判断，`推测`）。

## 归因规则（本页操作规则，`推测`）

| 现象 | 判给 | 动作 |
|---|---|---|
| 同一差异在 N 次内出现多次 | 输入侧 | 补输入/加校验，再重放 |
| 只在个别运行出现 | 采样侧 | 记日志；若影响交付，加多数/交集约束 |
| 只在换 `ontology_version` 后出现 | 锚点变更 | 历史不可比；按版本分池或迁移 |
| 差异集中在 `unparsed` | 投影器 | 修投影，不修模型 |

N=3 时「出现 1 次」与「出现 2 次」的统计含义很弱：归因是**工单路由**，不是统计检验。把它写成显著性判断，会重犯「用文本相似度度量收敛」的错。

## SLB：可能把确定性做高，同时把保证做没

- 规模：85% traces 含 SLB（BlocksWorld PDDL 仅 51%）、24% 推理 token 是 SLB；77–89% 程序仍独立重算（B4），但 163/1,791 继承轨迹答案（47 hardcoded / 88 partly fixed / 28 steered）（E-07 / E-09 `已核`）。
- 继承的代价：轨迹答案错时，hardcoded 0/19 正确、partly fixed 1/13、independent 32%（E-07 `已核`）。
- 干预：placeholders（值藏到运行时）SLB token −97%、ratio 0.25→0.005、含 SLB 的 traces 94%→15%，准确率 +2.6（95% CI −0.5–+5.9）；cautionary prompt 只减约 1/4，还把 hardcode 推成更隐蔽的 B2/B3；batching 准确率 −5.9（E-09 `已核`）。
- 因此：solver 链的验收要报 trace 指标（SLB ratio / B1–B4 / 继承率）；只报 program accuracy 分不出 B1–B4，四者都可能输出正确答案。
- **量与准确率无关（`已核`）**：SLB ratio +0.1 → 程序正确率 +0.007 [−0.011,+0.022]；每 +1,000 SLB token → +0.005 [−0.002,+0.013]（SLB §4.3）。所以不能用「SLB 少」推断「答案更可靠」；它只描述模型替 solver 干了多少活（placeholders 的 +2.6 是干预效应，不是 SLB 量的自然关联）。
- **形式语言是 SLB ratio 的最大解释变量（`已核` 数字 / `推测` 外推）**：Python 比 Z3/PDDL 的 SLB ratio 高 0.03–0.20（Calendar +0.06、Meeting +0.20、Zebra +0.03、BlocksWorld +0.16；Qwen 在 Zebra 例外）；解释方差 FL 0.123 > 数据集 0.057 > 模型 0.008（SLB §4.4；三因素线性模型 R²=0.27）。工程含义：先改接口（把搜索交给声明式 solver），再换模型/种子；论文测的是 SLB ratio，不是跨运行重放方差，外推到确定性要另测。

> 口径：9% 是 163/1,791 的占比，出自 4 个 CSP、3 个 reasoning model、单次生成；闭源模型无完整 trace，不能外推。

## 失效模式（本页归纳，`推测`）

- **把多样性当噪声。** 多次不一致被当作模型随机性接受，不回输入侧（[README](./README.md)）。
- **用文本相似度度量收敛。** 语义等价判不一致，反之亦然。
- **锚点本身漂移。** 本体升级后历史产物不可比，差异曲线断。
- **无回滚。** 一次错误收紧污染后续运行，定位不到是哪一版引入的。
- **把 coverage 当 0 差异。** 投影器覆盖不到的部分，读起来像「很稳定」。
- **重放不是同一输入。** 状态/上下文没冻结，测的是状态差（见反例）。
- **确定地错。** 硬编码或一致地错，收敛率满格而正确性为 0。

## 与本体 / 回路的关系

本体在此以**投影 schema + 版本号**出现，不是推理规则：它定义哪些结构可被比较、粒度多细。约束强度中到弱——能定义可比结构，不能保证两次产物语义等价；被违反时没有即时信号，通常只能靠重放 + diff 发现（时刻 6；以上为本页设计判断，`推测`）。

## 实施与客户价值（A3/A4）

> 读者是「批不批预算的人」。本节只回答这页改变哪个决定、要什么数据、何时必须停；机制与数字见上，未实测的组织/成本与收益一律标 `推测`。
>
> 自评：A4（有实施含义 + 可设计的价值假设）；V3 停在设计，未跑实验。

### 实施决策

1. **先建锚点与重放记录，再谈「换模型/调参数求稳定」。** 判定漂移需要两样东西：可比较的投影、N 次运行的重放记录。缺了它们，「这次不一样」容易被归给随机性，预算流去重试/换模型，可能存在的输入缺口没动。E-06 把本体接地任务的失败主因放在工作流（输入/接地/校验/修复），而不是只归给生成模型（`已核`，position paper、单案例）；推广到跨运行是仓库推断（`推测`）→ **改变的决定**：确定性预算的第一笔花在记录与投影，不是解码参数。
2. **归因按「是否复现」分叉，不按差异大小。** 换种子仍出现 → 输入侧；只在某次出现 → 采样侧；换 `ontology_version` 才出现 → 锚点侧。三分法本身是操作规则（`推测`），但它把「漂移」从形容词变成可分派的工单 → **改变的决定**：不一致必须带 verdict 才能结案，禁止「重跑一次好了」关单。
3. **一致性指标必须与正确性指标配对报。** 5 次一致地错也是确定；SLB 的 B1–B4 都可能输出正确答案（163/1,791 继承、hardcoded 错时 0/19 对），EvoMemState 的 Complete Retrieval 与最强 baseline MemoryBank 相当（85.6% vs 86.4%），但 Acc@complete 在 LoCoMo-Refined 是 70.8（同基准最强 baseline +11.5）、在 MemSyco 是 68.5（+31.2；E-17 `已核`），两个基准不可相减或平均（本页口径）；SLB 侧 SLB ratio 与准确率无关联（+0.007/+0.005，E-09 `已核`）→ **改变的决定**：验收表两列，缺一列不算通过。
4. **solver/形式化链的确定性看 trace，不看输出。** 85% traces 含 SLB、24% token 是 SLB（`已核`）；程序跑对不代表它在搜索。hardcode 的产物看起来更稳（同一程序重复打印同一答案），但「跨运行更稳」是机制推断、未测（`推测`）→ **改变的决定**：solver-backed pipeline 的验收加 trace 指标，并把值/结构分离（placeholders）写进接口；cautionary prompt 只减约 1/4 且会把 hardcode 推成更隐蔽的 B2/B3，不作主修复。
5. **状态是确定性的前置条件，不是相邻话题。** 上一轮的关系状态（有效/失效/冲突）会作为下一轮前提（机制推断，`推测`）；不冻结 `ontology_version` 与状态快照，「同一输入」不成立。EvoMemState 提供 `SUPERSEDES`/`CONFLICTS_WITH` 结构（结构 `已核`），但把它当跨运行锚点用是仓库推断（`推测`）→ **改变的决定**：确定性试点接在状态存储之后，先冻结版本、过状态门（见 stop condition）再重放。

### 数据/接口

| 对象 | 最小字段 | 为什么必须 |
|---|---|---|
| run record | `run_id, input_id, input_hash, model, seed, temperature, prompt_hash, ontology_version, state_snapshot_id, output_ref, trace_ref, ts` | 没有 `input_hash` 与 `ontology_version`，分不清「输入变了」和「输出漂移」 |
| projection | `run_id, concepts[], relations[], constraints[], coverage, unparsed[]` | 结构比对；`coverage/unparsed` 防止投影器把差异藏起来 |
| diff | `input_id, run_a, run_b, kind(concept/relation/constraint/coverage), element, recurrence, verdict(input-gap/sampling/anchor-change)` | 归因与分派；没有 `verdict` 就不能结案 |
| gold set | `input_id, gold, validator, level` | 正确性门；没有 gold 只能 audit-only |
| SLB bundle | `trace, program, output, VALUES, labels(A1/A2/B1–B4/C1/C2)` | 仅当链路含 solver；placeholders 在运行时注入 `VALUES` |

- **接口**：`record(run)`、`project(artifact, ontology_version)→structure`、`diff(a,b)→Δ`、`classify(Δ, runs)→verdict`、`gate(verdicts, thresholds)`、`score(answer, gold)`；SLB 侧加 `inject(VALUES)` 与 `audit(trace, program, output)`。
- **口径固定**：重放固定 `prompt_hash` / `ontology_version` / `state_snapshot_id`；模型、温度、种子只作分桶维度，不混进一条曲线。
- **N 与样本量**：重放 N≥3 并报区间（借 EvoMemState digest 的 seeds 建议；论文未定 seed 数，`推测`）。样本量按基准率反推——SLB 给了参照：9% 基准率估 ±5pp（95%）约需 126 条（SLB §6.5）。确定性侧没有现成基准率，先 100 题重放拿基线，再决定扩样（`推测`）。
- **有出处的阈值只在借鉴侧**：SLB ratio ≤0.02、程序准确率降 ≤2pp（SLB §6.5 第一个 sprint 出口）；EvoMem 的 80%/20% 是状态门（EvoMemState §6.5）；确定性侧的差异阈值本页不给数，sprint 里用基线分布定。
- **只读回放**：记录、投影、diff 都在离线或影子流量上做，不接线上写权限。

### 组织/成本

- **owner（`推测`）**：harness/平台 1 人（记录、重放、diff）；本体 curator 1 人（投影定义、`ontology_version` 策略）；领域评测 1 人（gold set、归因复核）。归因复核不能由写投影器的人独任——SLB 的 B2/B3 分歧要第三人裁决，同理。
- **人日（`推测`）**：run record + 重放管线 1 人周；投影器 v0 1–2 人周；gold set 100–200 条 × 5–10 分钟/条 ≈ 1–4 人日；SLB 侧 placeholders 集成 1–2 人周（SLB §6.5 自身也标 `推测`）。
- **运行成本**：每次重放 ≈ N × 单次推理 token 与时延；含状态检索时按 EvoMemState 的 565 token 候选上下文量级另计（论文设置，非本域实测）。SLB 侧是每千条 trace 的存储 + judge token，论文未给金额。
- **SLB 侧决策线（SLB digest §6.6；金额/单价未给，`推测`）**：TCO = 审计脚本 1–2 人周 + placeholders 集成 1–2 人周（见上）+ 每千条 trace 存储/judge token + 人工校准；12 个月收益 > TCO 且 placeholders 的准确率降幅 ≤2pp 才做，否则只 audit-only。闭源 API 无完整 trace 直接出局（buy 臂）。
- **训练**：不走 GRPO 就没有 GPU 训练成本；后续若要训 reasoning-state policy，EvoMemState 未报 GPU 时，只能按约 60K 实例 × G=8 估（EvoMemState §6.5，`推测`）。
- **隐性成本（`推测`）**：本体每升一版，历史 run 不可比；不迁移或不按版本分池，锚点漂移会伪装成「到处都漂」。
- **维护（`推测`）**：投影 schema 与 codebook 冻结后季度复核；口径一变（例如比约束文本 vs 比语义），历史曲线断。

### stop condition

- **没有 gold/validator** → 只做 audit-only，不报收敛率；一致地错也是「确定」。
- **投影覆盖率低于预设线，或差异集中在 `unparsed`** → 停，先修投影；否则量到的是投影器噪声。
- **重放内没有复现差异、且正确性已达标** → 不建漂移治理，只留日志。
- **输入侧本就不完备**（缺字段/缺约束/无接地）→ 先补输入，不做「稳定性工程」。
- **状态侧未过 EvoMemState 门**（门槛来自 EvoMemState §6.5；借到确定性是 `推测`）：Complete Retrieval <80% → 先修检索，不测「状态导致的漂移」；Acc@complete 无提升或下降 → 停，查 state 是否噪声；未解决冲突 >20% → 先修冲突；没有答案/评分器 → 不训 GRPO，确定性侧只做 audit-only。
- **本体槽位仍在建设期**（04 派 `别用` 条件）→ 不做。
- **SLB 侧**：无完整 trace（闭源）→ audit-only，不声称继承率；SLB ratio <2% → 不值得建；placeholders 不可分离 → 换声明式 solver 或只做 validator 审计；第一个 sprint 准确率降 >2pp → 不达标；V3 失败线 >5pp → 回退。
- **成本门**：年省返工/审批/事故 < 记录 + 投影维护 + 人审 + 重放增量 → 停，按季度重算。
- **确定性阈值不预设**：本页只定义「怎么算」，差异阈值用基线分布定；上面 SLB/EvoMem 的数字是借用的门槛，不直接当本域阈值。

### 第一个 sprint

2 周、单域单任务、离线回放、N=3、不做自动修复。

1. **第 1–2 天 · 选任务**：挑一条已有 gold 的任务链（没有 evaluator 就降级为 audit-only），冻结 `prompt_hash` / `ontology_version` / `state_snapshot_id` 三件套。
2. **第 3–5 天 · 记录与投影**：接 run record；投影器 v0 只做 concept/relation/constraint + coverage/unparsed；先人工核 30 条产物的投影（数量与 90% 门槛类比 SLB 的 judge 校准；投影侧阈值按基线定，`推测`），不达标不改 schema。
3. **第 6–9 天 · 重放与 diff**：100 题 × 3 次（`推测`），出正确性分、跨运行 Δ、复现清单（按三段分桶）。
4. **第 10–11 天 · 归因**：复现差异逐条判 input-gap / sampling / anchor-change；抽 20 条人工复核（`推测`），出分歧率。
5. **第 12–13 天 · SLB 支线**（仅当链路含 solver）：配 trace/program/output，标 30 条出 B1–B4 与 C1/C2 基线；50 题开 placeholders，验收 ratio ≤0.02、准确率降 ≤2pp（SLB §6.5）。
6. **第 14 天 · 出 memo**：go/no-go + 阈值建议（用基线分布，不用本页数字）。

**交付物**：run/projection/diff schema 一页；重放基线报告（正确性 + Δ 分布 + 复现清单 + coverage）；归因表（20 条复核记录）；SLB 基线（如适用）；go/no-go memo 与阈值草案；降级说明（关掉 diff 不影响主链路）。

**出口**：
- **go**：投影人工校准达到基线门槛（本页不预设数值；SLB 的 30 条 ≥90% 只作类比）、复现差异可归因（无法归因比例低于预设线）、正确性门有 evaluator → 进第二阶段（补输入 / 挂校验门 / 把 diff 接进 CI）。
- **no-go**：重放内没有复现差异且正确性达标 → 停在本层；或投影覆盖率不达标、差异无法归因 → 停，回 [README](./README.md) 的开放问题。
- **不做**：没有 gold、本体槽位不稳、闭源无 trace 且没有其它可投影产物。

### 客户指标/V3

- **受益者**：交付/上线的工程团队（同一输入两次跑出不同结论，评审卡在「哪版对」）；合规/审计（要证明结论可复现）；LLM-as-formalizer 平台（solver 保证名存实亡，静默错答）。`推测`
- **指标（设计，`推测`）**：
  - 机制侧：跨运行结构差异率（每对 run 的差异数）、复现差异数、input-gap 占比、投影覆盖率、归因分歧率；SLB 侧 SLB ratio、继承率、C1/C2。
  - 客户侧：返工小时/千次运行、审批时长、「两版不一致」工单数、静默错答率、审计发现数。
- **反事实**：不做锚点 → 把不一致当模型随机性，用重试 / 换模型 / 温度归零解决；不做 trace 指标 → 只看 program accuracy，B1–B4 都可能通过，错误被输出正确掩盖。**先测当前差异率与当前正确性**，否则增益不可归因。
- **试点**：单域 100 题 × N=3 重放；含 solver 链时加 100 题 placeholders on/off（`推测`）。
- **成功**：input-gap 修完后复现差异下降（幅度按基线定，`推测`），正确性门不降；SLB 侧 SLB ratio ≤0.02、准确率降 ≤2pp、继承率降 ≥50%（SLB §6.5 出口 / §6.6 V3）。
- **失败**：复现差异为 0 或差异全部为采样（该任务不需要这层）；投影覆盖不足无法判定；placeholders 不可分离或准确率降 >5pp（SLB §6.6 V3）。
- **停止线**：年省返工/审批/事故 < 记录 + 投影维护 + 人审 + 重放增量（`推测`，按季度重估）。

### 反例

- **「同一输入」很少真的成立。** 上一轮状态/上下文会进入下一轮；不做状态快照与版本冻结，重放测的是状态差，不是模型随机性。这是本页最可能不成立处（`推测`）。
- **投影分辨率两头都会错。** 太粗（只比 concept 集合）抹平语义差异；太细（比每条约束文本）把表述差异当漂移。SLB 的同构教训：只看输出看不见过程（B1–B4 都可能输出正确答案，`已核`）→ 只看最终结构也会漏掉「结论怎么来的」（后半句是类比，`推测`）。
- **一致性会掩盖错误。** EvoMemState 的 Complete Retrieval 与最强 baseline MemoryBank 相当（85.6% vs 86.4%），但 Acc@complete 在 LoCoMo-Refined 是 70.8（+11.5）、MemSyco 是 68.5（+31.2）——「都拿到了」不等于「都用对了」（E-17 `已核`）；把它推成「每次投影一致也可能是稳定地错」是类比（`推测`）。
- **继承率不能当自己的基线。** 163/1,791（≈9.1%，§4.2 一手计数）出自 4 个 CSP、3 个 reasoning model；闭源模型无完整 trace（E-09 限定），是结构性盲区。套到自家任务前必须先测。
- **成本可能不对称。** N 倍重放是线性成本，收益是一次性（发现输入缺口后只需抽样重放）；把全量 N 次重放做成常态，成本可能反超收益（`推测`）。任务本身确定（模板化、短输出、有 validator）时漂移率近 0（`推测`），建锚点不划算——SLB 侧的同构判据是 SLB ratio <2% 不值得建（SLB §6.5）。

## 关联

- [README](./README.md)（薄页 dashboard；`findings`/`frontier` 尚未拆）
- [memory 机制](../memory/mechanism.md) · [trace](../../06-measure/trace/README.md) · [seams · 时刻 6](../../seams.md)
- [E-06](../../conclusions.md) · [E-07](../../conclusions.md) · [E-09](../../conclusions.md) · [E-17](../../conclusions.md)
- [SLB digest](../../../src/papers/2611.02395-solver-like-behavior/digest.md)
- [EvoMemState digest](../../../src/papers/2611.03743-evomemstate/digest.md)
