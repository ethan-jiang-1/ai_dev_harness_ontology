# 生命周期 · 机制

> 只写「它怎么跑」。来源盘点、四阶段与失效模式在本页 [README](./README.md)（薄页，未拆 findings/frontier）；本页补 README 没有的三件东西：**一条可执行的生命周期控制回路**、**实施/客户价值层**、**从 digest 吸收的 4 条工程发现**。工程发现是实现形态，不是论文结论；每条拆开标 `已核` / `推测`。

## 机制

生命周期不是「四个阶段依次走完」，而是一条**对单条断言反复执行的回路**。三篇 digest 各自只闭合其中一段：

1. **入口是一个候选断言**，不是整个本体：一条 `A ⊑ B`（CASTON）、一条待注入的 gap 三元组（Evontree）、一个 incoming mention 对到哪个 anchor（FIRME）。
2. **来源落账**：谁产的（专家 / LLM / 挖掘）、哪个模型哪个 prompt、在哪个语料上校准过阈值。
3. **缩窄搜索空间**：用域内适配的排序器把候选压到 `k` 条（CASTON 是每条公理取 30 条可疑、每条 10 个替代父类）；这一段的立场是「LLM 不读整个本体」。
4. **局部裁决**：LLM 只看 child / 当前父类 / 候选父类 + 定义/其他公理，返回 `verdict / confidence / reason / suggested_replacements`（JSON）。
5. **分诊**：high 可进快审；medium 的接受率三组都 ≤25%，CASTON 作者的解释是「本体里有争议时不是模型不够强，而是域内没有唯一答案」（解释，非测量）。
6. **接受并落版本**：写谁接受、依据、版本、替代关系；旧断言不删，只标弃用。
7. **复审与衰减**：按版本/时间重算「最后一次被确认」；长期未再观察到的断言降级但不删（FIRME：未匹配 `σ=0.8σ`，低于 0.01 归零而**边不删除**）。
8. **回放**：下游判定器钉住本体版本，能对上一版重跑——这是「回滚」和「定位是哪一版引入」的前提。

> 第 1–5 步的组件在 CASTON 里有一手证据；第 6 步只有专家接受判断，版本/回滚没有实现；第 7 步借 FIRME 的 registry/衰减机制（从记忆图搬到断言，`推测`）；第 8 步三篇都没有实现。**把八步连成一条生命周期回路是本页的综合判断，`推测`。**

## 证据锚点：三篇各闭合了哪一段

| 阶段 | 机制 | 一手数字与条件 | 没证什么 |
|---|---|---|---|
| 精化·定位 | CASTON 两阶段：域内微调 embedding 排候选父类（`k_r=30`、`k_a=10`）→ LLM 局部判 verdict | CASTON v1.0.0：270 classes / 306 axioms / 292 atomic subsumption；default（OnT-FT + Qwen3-8B）high 6/6 = **100%**；pretrained ensemble 4/7 = **57.1%**；GPT-4o mini 5/16 = **31.3%** | 单一本体、单一公理类型、6 条高置信；无下游 |
| 精化·验证 | 用 confidence 做分诊，medium 必须人审 | 三组设置里 medium 的接受数是 0/2（default，全 mixed）、1/4、1/5——**没有一组超过 25%** | 只有 default 是「全 mixed」；「正确答案本身有争议」是作者的解释，不是测量；换模型要重标；n 只有 2–5 条 |
| 获取/自演化 | Evontree：subclass 传递 + synonym 三角闭合出 reliable，再用 `ConfirmValue` 找低置信但事实正确的 gap，只训 gap | 15 根概念、深度 ≥3；raw 95,814 synonym / 58,309 subclass；Reliable 14,169、**Gap 1,396**；gap 准确率 74.57 vs confirmed 72.62，确认值 0.1595 vs 0.4896；Llama3 +3.1%、Med42 +3.7%（相对 raw），相对最强 baseline +0.9/+1.1 | 单医疗域、两模型、自评；规则只覆盖 subclass/synonym；explicit 注入反降 |
| 对齐/演化 | FIRME：registry（canonical + alias）→ 跨期匹配 → 五态 + σ 衰减，未匹配不删边 | CMR：Full 30.4 / 57.4；no-alias 22.2 / 46.1（+7.8–12.1 pp，4 个 dataset–backend 设置）；每期独立归一化 8.2 / 23.9（Full 是它的 2.3–3.7×）；merge precision 85.6–97.5%；semantic matching token −40.3% | 专有数据、10 个月度 period（投资人口径）/ 3 个 reporting period（S&P）；false merge 长期污染未测；CMR ≠ 任务成功率；no-alias 与「每期独立归一化」都不是零身份对齐 |

- **Evontree 的增益只按报告值引用。** +3.1 / +3.7（相对 raw）与 +0.9 / +1.1（相对最强 baseline）是 digest 转述的报告值；同一张 Table 3 里 Llama3 mix 均值 61.0 低于 raw 62.5，均值与 Δ 行不可复算，故记 `存疑`（与 [generation/F6](../generation/findings.md) 一致）。

一张表读出来的结论：**CASTON 与 FIRME 的终点是「候选/身份 + 一次接受判断」，都没有测独立下游收益**（CASTON 自陈未测下游；FIRME 的 CMR 不是任务成功率）。Evontree 走到了训练 + QA 评测，但那是自评、单域、两模型，且增益只到报告值（`存疑`）。三篇合起来仍没有一篇证明「本体的改动让一个独立的判定器/agent 变好」。这不是缺陷，是分工——它决定了可落地的第一件东西是**接受记录**，不是更强的生成器（见下 A3/A4 的 D1）。`已核`（三处缺口）；合并判断 `推测`

## 工程发现（从 digest 吸收）

> 这四条来自 digest 的「工程上怎么用」，此前未进入本页。它们是**实现形态**，不是论文结论；可核的机制与推测的映射分开标。1–3 来自 FIRME（对齐/演化段），4 来自 OntoAct——后者不是本页三篇主 digest 之一，只借它的**写入准入**，不搬它的推理期机制。

### 发现 1 · 观察级契约：写一条观察，不是写一条边

- **判断**：生命周期的写入单位是**一次观察**。FIRME 的边是属性向量 `e_t=(u, h_t, v)`：每个观察带 `id / raw mention / relation / source / timestamp / context / head`，边级再带 `first_seen / last_seen / state / score`；`source_indicator ∈ {1=unstructured, 2=structured, 3=hybrid}` 留在观察里。融合（Rule 3/4）只增加引用，不覆盖原观察，也不合并 topic 与 product 的身份。
- **对台账的含义**：`axiom_ledger` 的 `evidence` 不能只存一个 `doc_id`，要存观察列表 `[(source_indicator, doc_id | period, span, observed_at)]`；一条断言被多来源印证时，记引用，不改写断言本身。这也让「来源」在事后可复核，而不只是一个枚举值。
- **等级**：FIRME 机制 `已核`（digest §3.2 融合、§3.4 边结构）；台账字段映射 `推测`。

### 发现 2 · 幂等键与「每期一次」上限

- **判断**：FIRME 的写入幂等键是 `(head_id, typed_target_id, source_id, period)`；每 period 每条边最多一次强度/状态更新，多个观察或印证路径**不重复计分**。冷启动时从 CRM/通讯录导出稳定 head 与 canonical 名，历史按 period 回填、不跨期合并；alias 只从已有 surface form 学，不从未来数据泄漏。
- **对台账的含义**：需要两层幂等——提案层 `(axiom_id, proposal_hash, version)`（本页已有，`推测`），观察层 `(axiom_id, source_id, period, span)`。同一来源同一期重复回放不能把「被印证次数」刷高，否则复审排序会被重复计数污染；`last_confirmed_version` 必须由观察层推进，而不是由提案层推进。
- **等级**：每期每边至多一次更新 `已核`（FIRME digest §3.4）；冷启动不泄漏是 digest 的工程配方（`推测`，digest §6.5）；键的具体字段组合是实现形态 `推测`；台账两层幂等 `推测`。

### 发现 3 · 指标分解：`CMR = MMR × merge precision`

- **判断**：只报一个「匹配率」会把覆盖率与正确率混在一起。FIRME 的口径是 `CMR = MMR × Merge Precision`：MMR 是被接受为 match 的频率（Table 3 每个 strategy 都报），merge precision 是被接受的 match 里正确的比例（human audit 85.6–97.5%）。false merge 先拉低 precision，再拉低 CMR。CMR 仍不是任务成功率。
- **对客户指标的含义**：「误配可达面」「台账覆盖率」这类单比率指标要拆成 `覆盖 × 正确` 两个数分别报；否则「修得多」和「修得对」分不开。回放验收同理：报了差异条数，还要报这些差异里有多少是错误匹配带来的。
- **等级**：定义与 85.6–97.5% `已核`（FIRME 术语表 / Table 3 / human audit）；「台账也应按此分解」`推测`。

### 发现 4 · 准入闸门、覆盖率 stop 与 schema 成本（OntoAct）

- **判断**：OntoAct 把 LLM 提议的公理挡在知识库外的准入条件是：schema 类型检查 + **来源非空** + 该公理类型的测试 `C_xi` 全过 + corpus check（至多一条矛盾 transition）；不过就不进 `A_W/R_W`。这补上了本页「接受记录」缺的一层：`accept()` 之前要有 `admit()`，且**拒绝也要留记录**，否则「哪些候选被拒、为什么」不可审计。
- **stop / 参数**：配套 stop 是 `axiom` 覆盖率 <40% → 停（覆盖率低时验证器只是选择性护栏，覆盖不到的动作只能放行或 fallback）；false-block >10% 或 unresolved >30% → 降级到纯 LLM 基线 + 事后审计。**这两个阈值是 digest 的工程建议，论文没有给**，`推测`。
- **成本**：schema 建设 5–10 专家人日（`推测`）；corpus 知识构造每 1,000 条记录约 20–50 次 LLM 调用 + 人工抽检（`推测`）；eval token 不含构造成本（`已核`，成本边界）。这三项要进商业论证，不能只算运行期 LLM 调用。
- **等级**：准入步骤 `已核`（OntoAct digest §3.3）；`admit()` 前置与拒绝留痕是本页映射 `推测`；「每类 2–3 条测试」「至多一条矛盾 transition」的具体数量与两个 stop 阈值 `推测`（digest E3 配方）；成本 `推测`。

> 为什么不把 OntoAct 的其余部分搬进来：三值条件（⊤/⊥/?）、hypothesis 状态机、动作 block 属于**推理期/判定期**机制，已由 [01/reasoning-gate](../../01-constraint/reasoning-gate/README.md) 与 [02/checker](../../02-judgment/checker/README.md) 承担；本页只借它的**写入准入**。

## 实施与客户价值（A3/A4）

### 实施决策

- **D1：先建断言台账，再谈更强的生成器。** 三篇都产出候选、都由一次外部判断收口：CASTON 6 条高置信修复被专家接受，Evontree 1,396 条 gap 三元组，FIRME 一套 alias + 边状态；**CASTON 与 FIRME 都没有证明下游判定变好**（CASTON 明写未测下游；FIRME 的 CMR 不是任务成功率），Evontree 的 QA 增益是自评且只到报告值（`存疑`）。所以第一个可交付物是「哪条断言、谁产的、哪个模型/prompt、谁接受、哪一版、能否回滚」，不是更多候选。台账缺位时 README 那句「失效是静默的」既无法证伪也无法定位。`已核`（三处缺口）；「台账优先于生成器」是本页综合判断，`推测`
- **D2：`source` 枚举不够，来源要落成 `(source, model_id, prompt_id, calibration_id)`。** 05-L1 要求来源进判定，但 CASTON 显示同一个「high」在不同设置下含义全变：default（域内微调 embedding + Qwen3-8B）是 6/6，GPT-4o mini + pretrained ensemble 是 5/16（差 68.7 pp；这一格同时换了 embedding 与 LLM，不能全归给模型，但足以说明 high 不能跨设置沿用）。Evontree 的 `τ*` 同样是「每模型 × prompt」单独用 Youden 扫（约 1 万条 raw 定）。只标「LLM 生成」，判定器会把别人模型的 high 当 high 继承。`已核`（数字与混淆条件）；四元组的实施形态 `推测`
- **D3：专家时间花在分歧集，不花在覆盖率。** 两条证据指向不同、但投入结论一致：Evontree 的 gap 是「事实对（74.57）但模型不确定（ConfirmValue 0.1595 vs confirmed 0.4896）」的 1,396 条——低置信不等于错，要人抽检；CASTON 的 medium 三组接受 0/2、1/4、1/5，digest 只对 default 的 2 条说明是 mixed，另两组未拆分「专家拒绝」与「分歧」。所以「medium 低接受率」不能一律解释成「域里没有唯一答案」，也不能当作「模型弱」统一自动修：gap 类抽检，medium 类人审并区分分歧（挂 `contested`）与判错（回修候选/裁决）。`已核`（数字；mixed 仅 default 有据）；「先分诊再扩覆盖」的投入排序 `推测`
- **D4：演化只增不删 + 版本窗口，回滚才有意义。** FIRME 的未匹配只做 `σ=0.8σ`、低于 0.01 归零但边不删除，五态让每次变化追得到 period——这正好补 README 列的「演化无回滚」。本体侧对应：弃用写 `deprecated_at / replaced_by / last_confirmed_version`，不做 DELETE；下游按版本钉住并可回放。否则「一次错误精化污染所有下游」只能靠人工翻记录。FIRME 机制 `已核`；搬到本体 `推测`
- **D5：候选阶段与裁决阶段分开度量。** CASTON 里有一个单变量对照：同一个 Qwen3-8B，域内微调候选上 high 6/6，pretrained 候选上 4/7——差 42.9 pp 只来自 embedding。再换 GPT-4o mini 是 5/16，但那一格同时换了 LLM 与 embedding，不能拆成任一方的效应。只报「接受率」会把召回差读成「模型不会判」。接口必须能单独取 `候选召回@k` 与 `裁决接受率`。`已核`（嵌入对照，n=6/7）；「主要增益」的排序 `推测`（n 太小，且换 LLM 与换 embedding 在 68.7 pp 那格里混在一起）；分开度量 `推测`

### 数据/接口

- **断言台账 `axiom_ledger`**（字段是实施形态，`推测`；字段语义来自三篇）：`axiom_id`、`subject / predicate / object`、`source ∈ {expert, llm, mined}`、`producer {model_id, prompt_id, embedding_id}`、`confidence {value, label, calibration_id}`、`evidence [{source_indicator, doc_id | period, span, observed_at}]`（观察级，见工程发现 1）、`status ∈ {proposed, accepted, contested, deprecated}`、`first_seen_version / last_confirmed_version / deprecated_at / replaced_by`、`accepted_by / accepted_at / review_minutes`。
- **候选契约**：`candidates(axiom_id, k_r, k_a) -> [{rank, candidate_parent, score, embedding_id}]`；候选集**排除 A 与所有已断言父类**（CASTON 原设计），另用 `rank_of_asserted_parent`（在**全量**父类排序里的名次）单独记「可疑」判据。`k_r=30 / k_a=10` 是论文取法，换本体要重标。`已核`（设计）；迁移 `推测`
- **裁决契约**：`judge(axiom, current_parent, candidates[], definitions, other_axioms) -> {per_parent: [{candidate_parent, verdict: correct|incorrect|partial}], confidence, reason, suggested_replacements[]}`——CASTON 的 verdict 是**逐候选父类**给的，不是整条公理一个 verdict；只收 JSON、只做局部判断。`已核`
- **准入/接受契约**：`admit(axiom, sources, T) -> {admitted | rejected, reasons[]}`（工程发现 4；拒绝也落记录）→ `accept(proposal_hash, reviewer, decision, basis) -> ledger_entry`；提案层幂等键 `(axiom_id, proposal_hash, version)`，观察层幂等键 `(axiom_id, source_id, period, span)`，同一提案/同一观察重跑不产生第二条记录或第二次印证。`推测`（论文无此层）
- **实体/别名表**（本体里的类和属性同样会换名）：`canonical_id / type / normalized_name / aliases[] / source_version`；匹配顺序 identifier → normalized name → alias → semantic fallback，阈值按域重标（**0.8 是在 investor-call T−1 上选的，不跨域搬**）；冷启动只从已有 surface form 建 alias，不用未来数据回填（工程发现 2）。`已核`（匹配顺序与阈值来源）；冷启动规则 `推测`（digest 配方）
- **复审/衰减**：`review_due(axiom, last_confirmed_version, decay_rule)`；只降状态不删行，低于阈值的进「待重确认」队列。`推测`
- **导出**：`snapshot(version)` 供下游钉版本回放；没有 snapshot 就没有反事实，也做不了归因。
- **不做**：topic 与 product 不合并身份（FIRME Rule 4）；不用「最近没出现」推断「不再成立」（未匹配可能是没机会观察）；不把别家模型的 high 当 high（CASTON）；不用 explicit 模板注入训模型（Evontree 的硬反例）。`已核`

### 组织/成本

- **owner**（`推测`，三篇 digest 都没有组织出处）：本体/主数据 owner 拿发布权（谁接受、谁签字）；域专家拿 medium/分歧的裁决权；平台团队维护台账、候选管线、版本导出；下游判定器 owner 必须签「钉哪一版」。缺任一方，台账退化成谁都能写。
- **建设人日**（逐项是 digest 的 `推测` 值；合计是本页按区间相加的 `推测`，不是实测）：registry/alias 5–10 人日（FIRME digest：1–2 人周，`推测`）；台账 schema + 存量迁移 2–4 人日（`推测`）；候选/裁决管线 3–5 人日（`推测`）；域专家**合计** 2–3 人日做规则/阈值/首轮盲标（Evontree digest 给的是合计，不是每人；`推测`）。**不含准入时合计约 12–22 人日**；若把 OntoAct 式准入做全，另加 schema 建设 5–10 专家人日（工程发现 4，`推测`），约 17–32 人日。
- **每次运行**：每条可疑公理一次 LLM 裁决（CASTON：30 条 × 10 候选，`已核` 设计）；embedding 域内微调每本体一次性（论文只说需要 GPU，无金额，`推测`）；Evontree 路径要对约 1 万条 raw 三元组 × 4–5 个 prompt 算 ConfirmValue（条数 `已核`），GPU 小时数未给（`推测`）。
- **人审**：high/medium 两档；评估期按 200 incoming units 抽样（FIRME 样本量 `已核`），折 0.5–1 人日/200 条（`推测`）；CASTON 的复核是 2 位专家、5 分制、6 条高置信（`已核`），扩到 30 条后的工时论文没给（`推测`）。
- **维护**：本体/阈值/alias 审核 0.5 人日/月（FIRME digest，`推测`）；**模型升级必须重标置信**（CASTON 与 Evontree 都要求），重标成本三篇都没测（`推测`）——这是唯一会随模型迭代反复发生的成本。
- **省钱项**：alias 复用把 semantic matching token 降 40.3%（`已核`，仅 investor calls × Opus × final period，且不含 registry 构建）；这条不能平移到本体侧，除非先有同级别名表。

### stop condition

- **候选阶段坏了先修召回，别改 prompt**：专家标注的**真替换父类**（池内合法目标）落进 `k_a` 候选的命中率（recall@k_a）低于预登记线 → 停，回修 embedding/域适配，不进裁决。`k_a` 候选排除 A 与所有已断言父类，所以既不能拿「当前父类是否在候选里」当召回（恒 0），也不能把「补回一个已断言父类」算成召回失败；CASTON 用自己的可疑判据（asserted parent 在全量排序里排名低）挑公理，也只给 `k_r=30 / k_a=10` 的取法、没给命中率下限，阈值必须团队预登记。`推测`（阈值）；`已核`（取法与排除规则）
- **medium 接受率始终 ≤25%**（0/2、1/4、1/5）→ 停自动修复 medium 档，状态改 `contested`，只留人判通道；只有 default 那组是 0/2 全 mixed，另外两组各有 1 条被接受。`已核`（三组设置）
- **高置信被专家推翻超过预登记比例** → 停自动接受，回查校准集。CASTON 的 6/6 只有 6 条，一条推翻就是 5/6，不能当稳定性证据。`已核`（n=6）；止损线 `推测`
- **Evontree 侧**：规则覆盖率 <50%（subclass/synonym 之外的关系多）→ 停；explicit 注入安全面掉 >5pp → 停；gap <500 条或 confirmed/gap 的 ConfirmValue 分不开 → 停；held-out 增益 <1pp 或主要来自数据清洗 → 停。**这些阈值是 digest 的工程建议，论文没有给**（`推测`）；已测的触发信号是 explicit 安全面 96.35→83.65 / 60.19→45.19、规则只覆盖 subclass/synonym（`已核`），报告增益 +3.1 / +3.7 只按报告值记（`存疑`，见 [generation/F6](../generation/findings.md)）。
- **FIRME 侧**：merge precision <90%，或 alias 组 reattachment recall 增益 <5pp → 停并回滚这批 alias；200 条 audit 的 Wilson CI 宽于 ±10pp → 扩样本不扩域；false merge 引起的下游错误超可接受线 → 停，先修 registry。**阈值是 digest 的建议**（`推测`）；已测的是 merge precision 85.6–97.5%、audit 200 units/setting（`已核`）——注意 85.6% 已低于这条 90% 线，按此线论文自己的低端设置就应停（把建议线套到论文数字上的推断，`推测`）。
- **没有版本回放能力** → 不许宣称「本体更正确」，只能影子运行。`推测`
- **试点算不过账**：年省专家工时 < 台账 + 管线 + 复审维护 → 停（成本多为 `推测`，只能当预登记假设）。

### 第一个 sprint

2 周、单一中等本体（200–300 类，CASTON 是 270 类 / 292 subsumption 量级）、**只做 subsumption 一种公理**、只读影子（不自动写本体、不训模型）：

1. 建 `axiom_ledger`，把现有全部 subsumption 迁进去；来源不明的标 `unknown`、接受人空缺的留空——**空值比例本身就是第一项读数**。
2. 候选阶段：域内微调 embedding vs 原 pretrained 各排一遍；记录 asserted parent 在**全量**父类排序里的名次分布（这是 CASTON 的「可疑」判据），取前 30 条可疑、每条 10 个替代父类（候选排除 A 与所有已断言父类）。召回指标用**专家标出的真替换父类**是否落进这 10 条（recall@10），目标只算池内合法的替换；**不要**用「当前父类是否在候选里」——原设计排除已断言父类，这个数恒为 0。
3. 裁决阶段：LLM 局部判断 JSON；在 20–30 条专家盲标上校准 high/medium；**不许跨模型沿用别人的阈值**。
4. 接受记录：2 位专家 5 分制复核 high/medium，逐条记 `review_minutes` 与终态（accepted / contested / rejected）。
5. 复审：算每条断言的 `last_confirmed_version`，输出「本版未被再确认」清单；**只标状态，不删任何行**。
6. 下游回放：拿一个现成判定器（规则 / checker 均可）在「迁移前快照」与「本版快照」上各跑一遍，报判定差异条数——**差异为 0 也是结论**。
7. 交付物：台账 + 迁移报告（unknown 比例）、候选召回报告、high/medium 接受率与专家工时、未确认清单、回放差异、预写 go/no-go、按版本回退的预案。
8. **出口**：`axiom_id` 100% 能追到 source 与版本字段；真替换父类的 recall@10 有基线、asserted parent 名次分布有记录，且「候选差」与「裁决差」分得开；high/medium 两类接受率可复算；未确认清单可执行；回放差异有数（含 0）；跨模型沿用阈值的情况为 0。任一缺失 → 不扩公理类型、不扩本体。

### 客户指标/V3

- **受益者**：把本体放进生产回路的产品团队（制造/设备、金融、医疗等跨系统口径的域）、本体/主数据 owner、下游判定器 owner、内审/合规。`推测`
- **痛点**：本体静默失效、没人对「今天仍成立」负责；一次错误精化污染全部下游且定位不到版本；专家时间被低价值覆盖吃掉。`推测`
- **指标**（前两项为主）：
  1. **定位时延 MTTL**：从「下游判错」到「指出哪条公理、哪一版引入」；改前按人天、改后按小时。基线必须自己测，论文没给。`推测`
  2. **台账覆盖率**：同时具备 source + acceptor + `last_confirmed_version` 的断言占比（sprint 直接测）；按工程发现 3 拆成 `覆盖 × 正确` 两个数报，不只报一个合计。`推测`
  3. **翻转率**：系统建议接受、后被专家推翻的比例（CASTON 的 6 条 high 全部被接受、翻转 0；n=6 不足以当基线）。`已核`（数字）/ `推测`（作为指标）
  4. **每条被接受改动的专家分钟数**。`推测`
  5. **可回放比例**：下游判定能在上一版重跑的比例。`推测`
  6. **误配可达面**：被错误 alias/错误同义关系带进来的断言数（借 FIRME 的 false merge 风险）。`推测`
- **反事实**：
  - 不做台账 → 定位不到哪一版引入，回退只能整版重来（`推测`）；「精化修复让下游判定变好」在三篇里都没有证据，只能当假设（`已核` 缺口）
  - 不做域内适配的候选阶段 → 同一 Qwen3-8B 判断，high 接受率从 6/6 掉到 4/7（42.9 pp，单变量对照）；再换 GPT-4o mini 是 5/16（这一格同时换了 embedding 与 LLM）。`已核`（条件：CASTON 本体、6/7/16 条）
  - 不做 alias 记忆与跨期语义 fallback → 跨期证据挂不上：Full 30.4 / 57.4 vs 每期独立归一化（LLM-Norm）8.2 / 23.9，2.3–3.7×。注意两侧都不是「零身份对齐」：no-alias 仍保留 canonical ID/name 匹配与语义 fallback，LLM-Norm 是每期独立归一化后再确定性匹配。`已核`（数字）；把 LLM-Norm 当「不做对齐」的上界 `推测`
- **试点**（`推测`）：单域、200–300 类、一种公理、台账 on/off（或 alias on/off）。
  - **成功** = 台账覆盖率 ≥90%；MTTL ≤1 人日；high 接受率达到预登记线且 30 天内翻转 0 条；每条接受改动的专家分钟数不高于改前；回放至少归因到 1 条真实版本变更；medium 全进 `contested` 且自动写入 0 条。
  - **失败** = high 翻转率 >10%；medium 有任一条被自动接受；真替换父类 recall@10 低于预登记线；回放无法归因任何差异。
  - **停止线** = 年省专家工时 < 台账 + 管线 + 复审维护（定价全为 `推测`），或换模型后重标置信的成本超过节省。
- **别拿来当价值的指标**：「本体更完整 / 更一致」。CASTON 与 FIRME 都没把「更正确」换成独立下游任务数字（CASTON §4.1 自陈没有下游；FIRME 的 CMR 不是任务成功率）；Evontree 有 QA 数字，但是自评、单域、两模型，且只到报告值。`已核`（CASTON/FIRME 的缺口）／`存疑`（Evontree 增益）

### 反例

- **反例 1：三篇证的是「候选/对齐质量」，不是「本体仍然成立」。** CASTON 明说修复是否让下游变好没测；Evontree 自评、两模型、单域，报告相对 raw +3.1% / +3.7%、相对最强 baseline +0.9 / +1.1（`存疑`，Table 3 均值不可复算）；FIRME 的 CMR 只是「边有没有对到 prior memory」，不是任务成功率。台账 + 分诊可能只买到**可审计性与定位时延，买不到准确率**。如果客户痛点是「答错」而不是「说不清为什么错」，这套不该先上。`已核`（三处缺口）
- **反例 2：置信校准会被模型升级反复作废。** CASTON 要求换模型重测（同一个 high 标签：default 100% → GPT-4o mini 31.3%，这一格同时换了 embedding），Evontree 的 `τ*` 每模型 × prompt 单独扫、约 1 万条 raw 定；每升一次模型重标一遍，而重标成本没人测。更便宜的替代是「干脆不自动接受」，在收益本来就小的场景可能直接占优。`已核`（机制）；成本判断 `推测`
- **反例 3：自动注入这条路有硬反例。** Evontree 的 explicit 模板注入把 Llama3 平均从 62.5 拉到 56.1、Med42 从 63.5 拉到 62.3，安全面 96.35→83.65 / 60.19→45.19。生命周期若自动把「被接受的断言」喂进训练，可能净亏。`已核`
- **反例 4：错误合并/错误别名没有回滚证据。** FIRME merge precision 85.6–97.5%，反推错误率 2.5–14.4%；一个错误 alias 会把后续同名观察持续路由到错误历史，「长期污染」作者只做机制推断、未测、也无自动回滚。本体侧的错误同义/错误父类替换形态相同；对零容忍下游，一次错误就可能吃掉全部收益。`已核`（precision 区间）/ `推测`（污染规模）
- **反例 5：样本太小，100% 不可当计划输入。** CASTON 的 100% 是 6/6；medium 每组只有 2–5 条（default 0/2，另两组各 1 条被接受）；Evontree 的 gap 只有 1,396 条。拿这些数当 KPI 目标会系统性高估。`已核`
- **反例 6：替代方案没被正面比较。** 现成的本体管理/版本库（git-for-ontology、MDM 去重）在 digest 层面没有与「台账 + 两阶段精化」的头对头成本；自己 build 也可能输给「买 + 只补流程」。`推测`

## 关联

- [CASTON digest](../../../src/papers/2610.21466-caston-refinement/digest.md)（精化·定位与验证）
- [Evontree digest](../../../src/papers/2510.26683-evontree/digest.md)（获取 / 训练侧自演化）
- [FIRME digest](../../../src/papers/2610.40482-firme/digest.md)（对齐·身份 registry 与衰减）
- [OntoAct digest](../../../src/papers/2610.21983-ontoact/digest.md)（**只**为工程发现 4 的写入准入/覆盖率 stop/schema 成本；推理期机制归 [01/reasoning-gate](../../01-constraint/reasoning-gate/README.md)）
- 本页 dashboard：[lifecycle README](./README.md)；兄弟主题：[generation](../generation/README.md) · [refinement](../refinement/README.md)
- 下游消费者：[checker](../../02-judgment/checker/README.md) · [identity](../../04-state/identity/README.md) · [memory](../../04-state/memory/README.md)
- 本派结论：[claims](../claims.md)（05-L1 / 05-L2 / 05-L5 / 05-L9）
