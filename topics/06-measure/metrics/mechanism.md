# 度量错配 · 机制

> 只写「它怎么错、怎么选」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

文献里「本体有用」与「本体无用」两类证据长期并存。多数不是相反结论，而是用了不同的尺子去量不同的机制（`推测`；这是 C-03 的解释框架，不是已被单独检验的假设）。

## 四种量错

| 机制 | 常用尺子 | 为什么错 | 更好的尺子 |
|---|---|---|---|
| 闸门/授权（01） | 任务奖励、准确率 | 被拦住的伤害不体现在奖励；护栏还会误剪合法动作 | 不可逆错误拦截率、误剪率、审批量 |
| 判定器（02） | 判定准确率 | 掩盖漏检与误报的非对称代价 | 漏检/误报曲线 + 「被误标后修坏」计数 |
| 知识供给（03） | 基准准确率 | 基准看不见治理、集成、上手（CAI 作者主张；部署 ledger 为空，`推测`） | 部署指标 + token/轮次/时延 |
| agent 配置（06） | 单次 run 的 score | 54% 的真实尝试方差是 run-to-run 噪声；轴交互 | 重复采样 + completion + cost + calibration + variance；效率与结果分列 |

> 这张表是本仓库按六派做的分派框架（`推测`），不是论文的实证分类；跨机制映射未验证，反例见文末。

## 四个案例

1. **POLAR**：reward 衡量护栏，18 个模型-域格只有 8 个 reward 改善，看着像失败；但作者声明 reward 不是防止伤害的度量。**护栏关心的是「伤害没发生」，reward 只记录「任务完成了」**（`推测`：本页对作者立场的改写；被 veto 的风险动作不体现在 reward 里，`已核`）。
2. **Ontology Catch**：curated checker 在**真实答案**上 catch 18.9%、FA 16.8%；precision 57.1% 是**人工故障 + 假设 25% 错答案**下的数，**不能与前者拼成一组**。只看 accuracy 会把「多抓错、多杀对」混在一起。
3. **SLB**：程序跑对不代表在搜索；85% 轨迹有 SLB、24% token 是 SLB，输出评估区分不出 hardcoded 与 independent。
4. **Agents are Systems**：在真实尝试（过 hurdle）中，54% 的 score 方差来自重复同一配置；单次跑分不可靠；Information > 模型/预算；验证靠工具不靠 prompt（prompt 19→22%，oracle 翻三倍）。

## 方法要求

> 本节是选指标的工程规则（`推测`），不是论文实测；引到的数字另标 `已核`。

1. **先声明机制的失效形态，再选指标。** 是「做错」还是「没做」？是「慢」还是「不准」？是「内部没有」还是「输出对了」？
2. **主指标 + 过程指标并报。** 只看一个数，任何机制都能被证成无用。
3. **报告非对称代价。** 漏检与误报不能合并成一个「准确率」；审批量与 false-veto 单独报。
4. **重复采样 + 方差。** 5 runs/config 起步（论文设计），按噪声带决定是否加；报 CI、completion、cost、calibration。
5. **能读中间。** formalizer 看 trace；agent 看轨迹；checker 看 catch/FA；记忆看 retrieval completeness 与 conditional accuracy。
6. **按配置轴做敏感性分析。** 五轴全因子或分组对照；预算只在信息/模型足够时有用，单轴归因要标「交互未测」（`推测`）。

## 按位置分派（八行，设计）

> 2026-11-09：把原来的四行框架扩到八个位置。表是**设计（`推测`）**，不是已验证的方法；证据列只指已有 E，不指新实验。覆盖率（能不能碰到）见 [coverage](./coverage.md)；本表回答（碰到后量什么）。

| 位置 | 失效形态 | 主指标 | 过程指标 | 非对称代价 | 基线 | stop（工程门，非 E） | 证据 |
|---|---|---|---|---|---|---|---|
| context | 不准 / 内部没有 | primary-trap avoidance；element score；任务准确率 | token/问、p95、投影字符数、顺序版本 | 知识没覆盖（漏） vs 投影太长/顺序错（误） | K1 命名+单位；纯文本 RAG | K2−K1 <5pp；投影 >60k 字符；维护 >2 人周/月 | E-12 / E-14 / E-01 |
| memory | 做错 / 内部没有 | CMR；Acc@complete | merge precision；reattachment recall；抽取 round-trip | false merge vs false split/漏配 | 不做 registry；LLM-Norm | merge precision <90%；Complete Retrieval <80%；冲突 >20% | E-05 / E-17 |
| evidence | 不准 / 输出对了 | 准确率；引用率 | 检索率；grounding 校准；tool calls/tokens | 无依据（漏） vs 过度引用/等级通胀（误） | 纯文本 RAG | 检索率 <50%；grounding 通胀 >90%；无独立标注 | E-03 |
| checker | 做错 | 增量 catch；FA | per-1k 成本；flag rate；净修复（fixed−corrupted） | 漏检 vs 误报后修坏 | 空结果重试 | 增量 catch <5pp；FA >15%；净修复 ≤0 | E-02 / E-20 |
| action | 做错 / 没做 | harm/HSR；false-veto；审批量 | 保留率；p95；回滚率 | 误拦合法动作 vs 漏放有害动作 | 不上护栏；blanket veto | false-veto >5%；task success 降 >2pp；保留率 <20% 或 >95% | E-04 / E-13 / E-15 / E-16 |
| commit | 做错 / 没做 | false-defer；false merge；授权正确率 | unresolved 率；审计完整率；重入时延 | 误 defer 正确变更 vs 误放行错误变更 | 不做 gate；直接 merge | false-defer >20%；unresolved >10%；无审计/事务 | E-20（否定性）+ 设计 |
| read-path | 做错 | 泄漏率（subject/object）；误拦率 | p95；缓存命中；策略异常率 | 泄漏 vs 误拦 | 不过滤 | fail-open 未修；object 方向泄漏；只有 1 个实现 | E-20 |
| determinism | 没做 | 收敛/漂移（结构投影差异）；重复运行一致率 | anchor 覆盖率；归因命中率；重放成本 | 假收敛 vs 假漂移 | 同输入重复运行；无锚点 | 无度量/无实现；漂移无法归因 | 设计（无 E） |

> 读表三条：  
> 1. **主指标跟着失效形态走**；没有「所有位置都看 accuracy」这回事。  
> 2. **非对称代价必须成对报**；漏/误、false-veto/漏放、false-defer/误放行不能合成一个数。  
> 3. **stop 是工程门，不是论文阈值**；没有基线/噪声带时，先写「不可判」，不写「无差异」。

## 失效模式

- **平均掩盖两端。** CAI 的 −38% 是 −91% 与 +1.9% 的混合。
- **准确率掩盖非对称代价。** checker 的 FA 触发重试；specific feedback 修好 28.3% 的 flagged wrong，也修坏 1.0% 的 flagged correct。
- **最终产物掩盖过程。** B1–B4 都能通过输出评估。
- **单次跑分掩盖方差。** 54% 是真实尝试上的 run-to-run 噪声。
- **配置轴不独立。** 预算只在信息/模型足够时有用；一次只动一个会误判（`推测`：交互已测，「单轴归因会误判」是推论）。

## 与本体 / 回路的关系

度量本身不在回路里；它决定回路的哪一段被看见。指标选错，可能把有效机制证成无用、把无效机制证成有用（`推测`；C-03）。

## 度量契约（工程发现 1–4，吸收自 digest）

> 以下四条来自 [Agents digest](../../../src/papers/2610.01618-agents-are-systems/digest.md)；Ontology Catch 的 catch/FA/precision 口径见 [findings](./findings.md) F2。它们改变的是**字段与分母**，不是结论。原表与限定以 digest 为准。

1. **复合指标先写定义域。** `GAP_CLOSED=(S−B)/(R−B)` 只在 specialist 优于 backbone（`R>B`）的任务上定义；`hurdle` 过滤「没真正尝试」的 run；54% 的 score 方差来自同一配置的重复运行，分母是**真实尝试**（过 hurdle）。不排除 hurdle 失败时配置只解释 39.4%，排除后 46.1%。`已核`（Agents §3.3/§4.1）；「不写分母就不可比」是本页报表规则（`推测`）。
2. **配置指纹记档位向量，不记轴名。** Information `none/identity/interface/protocol`、Reasoning `act-only/think-act/ReAct`、Verification `none/asked/reported/binding`、Budget `5/10/20 min`、Model `Qwen3.5-35B-A3B / 122B-A10B / 397B-A17B`。只写「变了 Information」无法复现；档位不同即不是同一配置（本页字段规则）。`已核`（档位表，§3.2）
3. **验证要靠工具，不靠 prompt；这条要看行为数据，不看 prompt 声明。** prompt 从 `none` 到 `binding`，reference-based verification 只从 19% 到 22%；给 oracle 才翻三倍；约 3/4 的 run 只做 format-only verification。把「要求自检」当验证指标，会把没验的 run 记成验过（`已核` 数字 / `推测` 指标后果，§4.3）。
4. **效率 ≠ 结果。** Sonnet 工具调用少、错误少、校准好，但 pooled G 更低；单看 token/时延/工具调用，会把「省事」排到「做对」前面（`已核` 数字 / `推测` 排序后果，§6.1）。

## 实施与客户价值（A3/A4）

> 读者是要验收一个机制、又不想再被尺子骗一次的评测/平台 owner。本节不重讲四种量错，只回答这把尺子改变哪个决定、要什么账本、何时必须停。**指标分派表仍是设计，不是已验证的方法**（[G1](./frontier.md) 未关）；数字出自上文与各文 digest（POLAR / Ontology Catch / SLB / Agents / CAI），未标出处的推算是 `推测`。

### 实施决策

1. **验收门从「一个分数」改成「两维 + 噪声带」。** 每个机制先填一行「失效形态 → 主指标 / 过程指标 / 非对称代价对」；报告同时给 catch（抓错/拦截率）下限、FA（误报/误剪率）上限、同配置重复运行的方差。只给 accuracy/precision 的验收材料不接收。`已核`（F2/F4 的数字与口径；[Ontology Catch digest](../../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) §4.1）→ 改的是**验收模板**；「不接收」是本页规则（`推测`），不是论文结论。
2. **评测预算先买噪声地板，再买配置轴。** 同配置 5 runs 起步，先量 run-to-run 方差再决定要不要做全因子：54% 的 score 方差来自真实尝试（过 hurdle）的重复运行、配置只解释 39.4%（不排除 hurdle 失败）/46.1%（排除后），意味着单次 run 的臂间差除非大于噪声带，否则不可解释。`已核`（F4；[Agents digest](../../../src/papers/2610.01618-agents-are-systems/digest.md) §4.1）→ 改的是**算力预算的先后**：不先量噪声的 A/B 等于掷硬币。
3. **先建基线，再建机制。** 判定器先比空结果重试（人工故障 catch 79.2%/FA 0%，真实答案 2.5%/0.1%）；编译类先比未编译 harness。没有基线的正面结果不进 memo——分不清是机制有效还是基线太弱。`已核`（数字与基线；[Ontology Catch digest](../../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) §3.6；[CAI digest](../../../src/papers/2610.41172-context-as-infrastructure/digest.md) §6.1）→ 改的是**评审材料的最低要求**（规则本身是设计，`推测`）。
4. **成本按 per-flagged 还是 per-checked，要写进报价。** 论文只给 per **flagged** answer：curated 65,976 tokens / 46.0 s，data-derived 28,076 / 17 s；折算是 `per-1k = flag_rate × per-flagged × 1000`，**66k 不是每答案成本**。`已核`（[Ontology Catch digest](../../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) §4.4/§6.5）→ 改的是**采购可比性**：按「每次检查」与按「每次告警」报价的两家不能直接比。
5. **过程指标要么带决策规则，要么不进验收。** SLB 说明只看最终产物会漏掉冗余与错误继承（85% 轨迹、24% token）；但过程指标自身会奖励「看起来在思考」——CAI 的 token 节省可能用检索轮次/时延换（配对子集约 3×，n=7）。`已核`（F3）+`推测`（后半句是本页推断）→ 改的是**评测 harness 要不要采 trace**：只采最终产物的 harness 支撑不了这条判断。

### 数据/接口

- **在 [feasibility](../feasibility/mechanism.md) 的评测账本上扩四个字段**（不另开一本账）：`config_fingerprint, repeat_idx, cost_unit(per_checked|per_flagged), trace_ref`。
  - `config_fingerprint` 至少含五轴的**档位**（不是轴名）：Information / Reasoning / Verification / Budget / Model，档位表见上节「度量契约」第 2 条（[Agents digest](../../../src/papers/2610.01618-agents-are-systems/digest.md) §3.2）；没有它，两次跑分不可比。
  - 最容易缺的两个字段是 `repeat_idx`（缺了算不出方差）与 `cost_unit`（缺了会把 66k 当每答案成本）。
- **指标分派表（本页主张的产物，一行一个机制）**：`mechanism_id, failure_form(做错|没做|慢|不准|内部没有|输出对了), primary_metric, process_metric, asymmetry_pair(漏/误), threshold, baseline_ref`。四行起步：闸门/授权、判定器、知识供给、agent 配置。`baseline_ref` 必须指向可重跑的基线，不能写「业界通常」。
- **报表接口**：每次评测输出 `n_runs/config`、CI（论文用 bootstrap；水平自定）、completion、cost、calibration；非对称代价分开列，禁止合成 accuracy/precision 一列；`GAP_CLOSED` 在 `R≤B` 时写 `n/a`，方差要带 hurdle 分母。
- **接受率 ≠ 正确率**：CAI 的 `p_h` 是证据门放行比例，不是放对比例；φ（false-accept rate）论文未测，需 100–400 条 accepted query 人工审计单独估（CAI §6.4/§6.5）；Ontology Catch 的部署度量给的是 100–400 条分层抽样 + Wilson CI（Ontology Catch §6.5）。任何「门通过率」进 memo，必须同页给 φ 或标「未知」。
- **口径固定**：token 按每问总量、伤害按轨迹级、成本显式标 per-flagged/per-checked；换口径即不可比（[C-03](../../conclusions.md)）。评测用 `arm` 字段区分位置变体；本仓库不设实验目录。

### 组织/成本

- **owner 三缺一即退化成自评**（`推测`）：评测 owner 拥有账本与分派表；机制 owner 声明失效形态与主指标（只有他知道是「做错」还是「没做」）；独立复核方管 FA 预算与抽检，不能由机制 owner 兼。
- **人日**（全为 `推测`，无出处）：账本 + 分派表骨架 3–5 人日（与 [feasibility](../feasibility/mechanism.md) 同一估计）；每个机制补一行失效形态与阈值 0.5 人日；50–100 条人工抽检 2–3 人日（规模参照 Ontology Catch 的 50 条抽检，不是它的人日）。
- **运行**：重复采样是乘数，5 runs/config 即评测成本 ×5。按「两臂 × 200 题 × 5 runs」是 2,000 runs 量级（本页算术，非论文数字，`推测`）。论文的 432 cells × 5 runs / 8,640 runs 是一次性研究规模，不是上线验收规模。
- **维护**：任务/模型/工具变更后噪声地板要重量、阈值要复核；按 0.5–1 人日/月（`推测`）。这是本页唯一的持续支出，也是停止线要盯的量。

### stop condition

- **噪声带未量出，或待检效应小于 CI 宽度 → 不做配置比较**，只做单臂记录；结论写「不可判」，不写「无差异」或「A 优于 B」。
- **机制说不清失效形态 → 不进评测**。落不进「做错 / 没做 / 慢 / 不准 / 内部没有 / 输出对了」任一格的机制，先回机制页拆，不是先买指标。
- **报告缺 completion / cost / calibration 任一项 → 判分作废**，不进 memo（F4）。
- **主指标把非对称代价合成一个数（只有 accuracy/precision）→ 只作诊断**，不作验收；上线门必须两维。
- **配置轴不独立（预算只在信息/模型足够时有用）→ 不做单轴归因**，标「交互未测」；「单轴会误判」是交互的推论（`推测`；[Agents digest](../../../src/papers/2610.01618-agents-are-systems/digest.md) §4.3）。
- **维护人时 > 它避免的返工/误上线价值 → 停**（`推测`，无实测；按季度重估）。
- **硬门槛**（`推测`）：2 周内填不满 3 行分派表，或拿不到可重跑基线 → 不出 go/no-go，只出缺口清单，回写 [G1](./frontier.md)。

### 第一个 sprint

2 周、一个机制族（判定器或护栏，二选一）、固定 harness、200 题、5 runs/config、两臂（现状 vs 加机制）：

1. **第 1–2 天 · 锁口径**：为该机制写一行「失效形态 → 主指标 / 过程指标 / 非对称代价对 / 阈值」；锁 `config_fingerprint` 的五轴**档位**（不是轴名）；定 `cost_unit`。
2. **第 3–5 天 · 量噪声地板**：同题同配置重复 5 次，报 run-to-run 方差占比与 CI 宽度。这一步没出来，不跑第二臂。
3. **第 6–7 天 · 跑两臂**：200 题 × 2 臂 × 5 runs，记 token/时延/轮次/`trace_ref`；抽 50 条人工复核主指标。
4. **第 8–9 天 · 出报表**：catch/FA（拦截/误剪）分开并各带 CI；成本按两种口径各算一遍；completion/calibration 单列。
5. **第 10 天 · 复算与出口**：换人按同一账本重算，结论一致才算数（`推测`：流程要求，无实测）；出 go/no-go memo；缺口回写 [frontier](./frontier.md)。

**交付物**：分派表（≥3 行）+ 账本 schema + 噪声地板报告 + 两臂对照报告（含非对称代价、两种成本口径、completion、calibration）+ 复算记录 + go/no-go memo。

**出口**（阈值是工程门槛，非论文实测，`推测`）：
- **go**：效应量大于噪声带，且 FA 落在自定预算内 → 进第二阶段（扩样或 shadow）。
- **no-go**：效应量落在噪声带内；或主指标与过程指标结论相反且无决策规则 → 停，回写 [G1](./frontier.md)/[G3](./frontier.md)。
- **不出结论**：成本口径缺项、抽检样本不足、或只有单次 run → 补数据，不硬判。

### 客户指标/V3

- **受益者**：评测/平台 owner（要向上证明机制值不值）；业务方（少事故、少返工）；以及**被错判的机制 owner**。痛点不是「没有指标」，是**两把尺子可能给出相反结论**（`推测`）：同一护栏在 reward 下 18 个模型-域格只有 8 个改善（`已核`），在防伤害口径下是否成功仍未知（`推测`）；同一 checker 的 precision 在**人工故障 + 假设 25% 错答案**下是 57.1%（`已核`），在真实答案上只比随机高 1.6 点、CI 跨零（`已核`）。
- **指标（尺子本身）**：口径相反结论的机制数 / 被评审机制数（目标下降，`推测`）；复算一致率——同数据换人重算结论一致的比例（可审计的最低形式，`推测`）；决策返工率——因口径/成本单位缺失而重开的验收次数（目标 0，`推测`）。
- **指标（被正确量出来的机制收益）**：不可逆错误拦截/千次、误剪率、每千问 query-equivalent、per-1k token 与工时、p95 时延、task success、completion。
- **反事实**：不做 → 继续用单一 score/accuracy 验收、用单次 run 比配置、把 FA 混进 precision。代价是双向的：**把有效机制判死**（护栏被 reward 判失败）与**把无效机制上线**（把 25% 错答案假设下的 57.1% 当成够好）都会发生，且很少被看见（`推测`）。
- **试点成功**（2 周，`推测`）：对一个机制给出可复算的 go/no-go，且满足其一——(a) 结论与旧尺子下不同（错配确实在这条链上）；(b) 结论相同但 CI 收窄到能过一个决策点（尺子提高的是置信度，不是重复直觉）。两者都不满足即**试点失败**：换尺子没改变任何决定，本页对这条机制没有价值。
- **试点失败**：2 周后仍只有单次 run 的分数；或分派表填不满 3 行；或两臂差小于噪声带且样本无法扩大。
- **停止线**：账本 + 分派表的维护人时 > 它避免的返工/误上线价值（`推测`，按季度重估）。

### 反例

- **效应可能本来就小于噪声。** 54% 是真实尝试上的 run-to-run 噪声；若机制真实效应只有几个点，而 5 runs 的 CI 仍宽于效应量（`推测`），那么分派指标只是把「不可判」变成「有结构的不可判」。此时正确动作是加样本或明说不可判，不是换更精细的尺子。
- **分派表可能退化成「每个机制都要全部指标」。** 四个机制的分类来自本仓库六派，不是论文的实证分类；论文各自只给了一个机制的单点，跨机制映射从未被验证（[G1](./frontier.md) 未关）。把分析框架当测量标准，会得到预算黑洞。
- **过程指标会制造新的错配。** 输出尺子漏掉过程（F3）是真的；反过来，轮次/token/轨迹长度会同时奖励多探索（好）与重复劳动（坏）——CAI 的 token 节省可能用检索轮次/时延换（配对子集约 3×，n=7），同一份过程指标会把「省 token」与「多轮次」都判成改善。
- **54% 是别人的估计，不是你的。** 4 tasks / 2 domains / 真实尝试 / 5 runs per cell；换到软件工程或客服可能不同（[G3](./frontier.md) 未关）。把它当常数写进预算，会系统性错配重复采样的钱。
- **可复算不等于正确。** 账本让两个人算出同一个数；主指标选错时（用 reward 量护栏），可复算只是让错误更可信。

## 关联

- [findings](./findings.md) · [frontier](./frontier.md)
- [trace](../trace/README.md) · [mechanism](../mechanism/README.md) · [failure-attribution](../failure-attribution/README.md)
