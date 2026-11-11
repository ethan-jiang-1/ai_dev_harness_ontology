# 推理期约束 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。
> 「工程发现 1–4」是从 OntoAct / 多 agent digest 吸收的落地口径（接口/参数/成本/stop/客户指标）；标 `推测` 的是 digest 工程配方，不是论文测量。

## 位置

在动作执行前、推理进行中：本体有两种用法——限制模型能从哪些知识取候选（curated KG），或检查结论/动作的前提条件是否成立（条件公理）。后者在条件被违反时 block 该动作；缺读数只报 unresolved、转观察。它只拦条件不成立的动作，不是覆盖所有动作的闸门，也不是安全保证。

## 两种机制

| 机制 | 做法 | 代表 |
|---|---|---|
| 推理锚定 | 把候选限制在 curated KG 上，拆成可审计步骤；缺证据时追问 | 多 agent 差分诊断 |
| 符号验证 | 用条件公理检查 hypothesis/action 是否成立；违反则 block，缺证据转观察 | OntoAct |

共同点：判据来自本体，不是模型自评。区别：前者限制「从什么推」，后者限制「推出来的条件是否成立」。

## OntoAct 的流程

1. 从记录抽候选公理；类型检查 + 来源非空 + 该公理类型的测试 + corpus check 通过才进入世界知识。
2. LLM 提出 claims / hypotheses / action；claims 经 `f_admit` 检查类型/结构证据/引用模式后进入 A。
3. 每个 hypothesis 的每个条件在当前知识下求值：⊤ / ⊥ / ?。
4. 任一条件 ⊥ → refuted；全部 ⊤ → confirmed；否则 open。动作违反 R_W 的条件/禁止 → block；缺读数只报 unresolved、触发观察（缺证据本身不 block）。需要解释支持的动作要求 confirmed hypothesis；观察动作不需要。
5. 被 block 时给 revision 反馈；新观察/干预结果更新 context 与 hypothesis。

## 多 agent 诊断的流程

1. 症状映射：canonical → alternatives → synonym/HPO fallback；映射失败保留 trace，不进推理。Q4DX 上 91.3% 成功（77.3% SYMP + 14.0% HPO fallback），8.7% unmapped。
2. LLM 只做症状抽取、追问、解释；排序/评分由确定性代码算。
3. 候选病只从 curated KG（SYMP/DOID/HPO）的显式关系来。
4. 追问只问可观察、未报告、能区分候选的症状；Yes/No/unsure；最多 11 问（引 10–11 轮达峰）。
5. 评分：specificity + coverage + support/conflict（α=0.6、β=0.2）；每项回指症状与本体关系；阈值宁宽勿严。

评估另用 patient simulator 自动回答（可访问完整 profile，乐观估计）；它不是线上角色。

## 证据

- **OntoAct**：Tacit-FLE 成功率 78.6/83.3/90.0%（IfR 64.3/66.7/65.0）；spurious interventions 1.9/2.4/1.6（IfR 6.4/11.9/17.8）；共享资源条件 70/70 违规候选在执行前被重定向、发出命令 0/136 违规（IfR 0/20、20/107）；Mars 15.92 vs 10.64；ALFWorld 98.5% vs 96.3%，LLM calls 13.7 vs 28.8。
- **多 agent 诊断**：Q4DX 99 cases/29 diagnoses，Top-1 18.7→21.2%、Top-3 25.8→27.3%；症状映射 91.3%（77.3% SYMP + 14.0% HPO fallback；8.7% unmapped）；curated KG 没有的诊断（Jaundice/Vertigo 被归为症状）准确率恒 0；作者写「caps benchmark performance」。

## 失效模式

- **覆盖不足。** 本体只覆盖少数关系/实体；没有适用 axiom 的动作只能放行或 fallback。
- **封顶表现。** 把候选锁在 curated KG 内，本体没有的诊断永远出不来（Jaundice/Vertigo 恒 0）。
- **本体粒度/术语错。** 症状映射 8.7% 未映射；映射失败若静默丢弃，后续推理看不到这些证据。
- **知识构造成本不在 eval token 里。** 构造世界知识/本体的 LLM 调用与专家人日另计（digest §5 第 5 条）。
- **schema 固定、学习未解决。** 评估用预定义 schema；真实域的类型/关系会变（digest §5 第 2 条）。
- **不是所有任务都赢。** elimination 上 IfR 匹配或超过 OntoAct（digest §4.1）。
- **verifier 不是 safety guarantee。** 作者明确不声称可部署；安全性要求形式保证时别用。
- **block 有结构化信号，不代表模型改对。** 验证器返回 failed_conditions/unresolved；论文测最终成功率/SI，没有单独测「模型是否按 revision 修正」（`推测`）。
- **换更强 LLM 不解决结构错。** 错误多来自 KG 稀疏/粒度/术语，不是 LLM 语言能力（多 agent §6.1/§8）。
- **把 unknown 当 block。** 缺证据应触发观察；直接拒绝会把「不知道」变成「不允许」。

## 与本体 / 回路的关系

本体在推理期以 **typed schema / conditional axioms / curated KG** 出现；约束强度中到强：能拦下违反条件公理的动作，但只覆盖有 axiom 的动作，且不判可逆性/授权。被违反时能报出失败条件/候选/未解析项；不提供语义真值或安全证明。

## 实施与客户价值（A3/A4）

### 实施决策

- 在两篇论文的任务形态内，优先「验证条件」而不是「限制知识源」：前者不一定封顶，且能给出 block 理由；但两者没有头对头成本-效果，不能当普遍结论（`推测`）。
- 先做单域 schema + 条件公理；没有 axiom 的动作放行/fallback，不要假装全覆盖。
- 三值条件：? 触发观察/追问，不直接 block。
- 先做症状映射，再做诊断/验证；映射失败保留 trace，不进推理。

### 工程发现 1｜接口：症状映射、条件验证与 block 回传

- **症状映射是前置管线。** canonical → alternatives → synonym/HPO fallback；失败保留 trace，不进推理。Q4DX 上 91.3% 成功（77.3% SYMP + 14.0% HPO fallback），8.7% unmapped；这 8.7% 不进推理，必须让它在日志里可见。
- **OntoAct 接口。** `verify(action,K_t)` → `{allowed|blocked, failed_conditions[], unresolved[]}`；`?` 只进 unresolved/观察，不 block。`revise(block_payload)` 回传 `{action, failed_conditions[], unresolved[], evidence_refs[]}`；`observe(reading)` 更新 A_t；`corpus_check(axioms)` 报矛盾/覆盖。
- **数据契约。** condition `(u,p,op,z)`：实体/关系、属性、比较符、值；axiom `{id,type,action,conditions[],sources[],created_by,version}`；claim `{id,subject,predicate,object,source,confidence}`；hypothesis `{id,required_relations[],conditions[],state}`。
- **准入不是全收。** 类型检查 + 来源非空 + 每类 2–3 条测试 + corpus check（至多一条矛盾 transition）才进入世界知识；`f_admit` 的字段级规则要写死（类型/来源/引用模式/时间范围），不能只写「测试全过」（digest 工程配方）。
- **block 后回传结构固定。** 用 `{failed_conditions[], unresolved[], evidence_refs[]}` 而不是只给自然语言理由；agent 可按字段改 claims/hypotheses/action。

来源：[OntoAct digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-21983) · [多 agent digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-36325)

### 工程发现 2｜参数：能抄的是条件，不是值

- **turn budget 20–40；block 后重试 ≤3；`?` 累积 3 条转人工**（digest 工程配方，非论文测量，`推测`）。digest 未给这三个数的消融；按域从区间/保守值起步，再用 block 率与 ? 比例调。
- **追问上限 11 问**（多 agent 论文设置；引 MedDialogRubrics：10–11 轮达峰，之后下降）。
- **评分参数 α=0.6、β=0.2**（多 agent 论文设置）；阈值「保留领头分数的一小部分或至少匹配 2 个症状」，宁宽勿严。
- **axiom 准入测试 2–3 条/类、corpus check 至多一条矛盾 transition**（digest 工程配方，`推测`）。
- **三值求值不引入 LLM 自评。** 条件求值是符号检查；LLM 只提议 claims/hypotheses/action。

来源：[OntoAct digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-21983) · [多 agent digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-36325)

### 工程发现 3｜成本与测量口径

- **schema 建设 5–10 专家人日**（`推测`，digest 工程配方；论文未测）。
- **corpus 知识构造每 1,000 条记录约 20–50 次 LLM 调用 + 人工抽检**（`推测`，同上）；eval token 不含这部分。
- **运行成本**：符号求值轻量；LLM 提议调用为主（ALFWorld 13.7 vs 28.8 calls）。
- **维护**：schema/环境变更后重跑准入与 corpus check；规则过期复审。
- **测量口径**：只看最终成功率会被「重复失败后终于成功」骗；同时报 spurious interventions（SI）与 turns。OntoAct SI 1.9/2.4/1.6 vs IfR 6.4/11.9/17.8。
- **多 agent 的聚合会掩盖 case-level。** 同时报 Top-1/Top-3 与「可解决歧义」子集；追问可能伤 Top-3（50% 完整度 26.3→24.2）。

来源：[OntoAct digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-21983) · [多 agent digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-36325)

### 工程发现 4｜stop 与客户指标

- **覆盖率 stop**（工程门，不是论文阈值，`推测`）：axiom 覆盖率 <40% → 停（选择性护栏）。
- **质量 stop**（同上）：false-block >10% 或 unresolved >30% → 降级到纯 LLM + 事后审计。
- **噪声 stop**（`推测`；论文未测噪声）：真实传感器噪声下 `?` 洪水 → 先补观察/传感器，不要靠调阈值硬压。
- **何时别用**：没有稳定 schema/类型关系；记录质量差；环境机制频繁变化；需要实时低延迟；需要确诊（多 agent 只做 differential，最终诊断靠医生）；安全性要求形式保证（verifier 不是 safety guarantee）。
- **任务形态**：elimination 上 IfR 匹配/超过 OntoAct；不要假设所有任务都赢。
- **受益者/痛点**（`推测`，digest §6.6）：工厂维护/值班班组；误诊、无效干预、专家工时、停机。
- **指标**（`推测`）：MTTR、每千次干预的无效干预数、专家工时/次、false-block 率、停机分钟。
- **反事实**（`推测`）：不上验证器 → 纯 LLM 诊断；先测 MTTR/SI 基线。
- **V3**（`推测`）：单域 20–30 episode；成功 = SI 降 ≥30% 且 false-block ≤10%、专家工时降 ≥10%；失败 = 覆盖率 <40% 或 SI 不降；停止线 = 年省专家工时 < 维护成本。
- **替代方案**（`推测`/缺口）：纯 LLM + 事后审计；curated KG/规则引擎；买 CMMS/知识图谱产品；开源 ontology + tool-calling。论文只与 IfR/WALL-E/ReAct* 比，没有与这些工程替代做同口径成本-效果。

来源：[OntoAct digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-21983) · [多 agent digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-36325)

### 第一个 sprint

2 周、单域单故障类、10–15 人日（digest 工程配方，`推测`）：

1. 从 20–40 条维护记录定 schema（3 实体 + 2 关系 + 可观察属性 + 公理形式）。
2. LLM 抽 30–50 条带来源候选公理，实现准入门 + 每类 2–3 测试；人工抽检 20 条。
3. 实现三值求值 + condition report + block→revision；先用记录脚本回放，不接真 LLM 循环。
4. 20–30 个历史 episode 回放；报 SI/成功率/block 率/? 比例/公理覆盖率。
5. 预写 go/no-go：覆盖率 <40% 或 false-block >10% 停，退回纯 LLM 基线。

### 反例

schema 覆盖低；真实传感器噪声；环境机制频繁变化；无专家维护；curated KG 封顶；需要形式安全保证；elimination 任务。

## 关联

- [OntoAct digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-21983)
- [多 agent digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-36325)
- [findings](./findings.md) · [frontier](./frontier.md)
