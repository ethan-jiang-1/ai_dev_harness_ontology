# 输出后判定 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

输出已形成、尚未被使用；需要判断「它是否忠于本体/数据」。格式检查只能看语法，测试只能看行为；本体提供外部结构判据，能查类型/声明/模式约束——但 checker 自己也会错，且结构检查对 changes of meaning 基本抓不到（curated/data-derived/masked LLM 为 0%）。

## 三种来源

| 来源 | 怎么来 | 能查什么 | 系统性偏向 |
|---|---|---|---|
| curated | 图作者发布，按原样用 | domain/range/disjointness、类/属性声明 | FA 主源是 domain/range 与 declaration check（缺声明/闭世界）；「与数据矛盾」另见 Table 5，不是 FA 主因（data clash=0） |
| data-derived | 从数据总结类/属性/常见模式；模式≥5 次才允许 | 类型、属性使用、join 模式 | 只抓数据里没见过的组合；抓不到语义错 |
| LLM-generated | 从同一 summary + 实例样本写；可加 disjointness | 同上 + 可能补声明 | 不稳定；同 recipe 不同 draw 差异大 |

**FA 归因（curated）**：盲审 32 个 FA 的双标注一致项中，undeclared term 17、closed-world 11，data clash 0（Table 6）；消融上，curated 与 masked LLM 的人工故障 FA 差异（C3）由 domain/range 与 term declaration 承担，disjointness 不贡献额外 flag（Appendix D.1）。「curated schema 与自身数据矛盾」是 Table 5 的独立观察，不能直接当 FA 归因；审计仍必要，但别把它写成 FA 主源。`已核`

## 判定回路

`Question → LLM agent → SPARQL → KG → answers → check → pass/flag → answer kept`。

- flag 触发**一次重试**；消息 specific（指出失败约束/查询片段）或 generic。
- 每个 verdict 对正确答案打分：caught / missed / false alarm / correct pass。
- 重试后：fixed（错→对）、corrupted（对→错）。
- 不支持的 fragment（UNION、subquery）返回 **unknown**，不是 pass/flag。

## 检查类型

- **Query checks**：解析 SPARQL，推断变量类型；检查 term 存在、class membership、domain/range、disjointness、datatype range。
- **Binding checks**：对结果绑定重新求值；检查类/属性/数据类型。
- **data-derived pattern checks**：属性与数据从未共现的类、没有类支持≥5 次的 join。
- **空结果重试**：查询返回空就重试；不需要本体，是强基线。

## 建库参数（data-derived）

- **模式阈值**：属性/类共现 ≥5 次才允许；低于 5 次不 flag，避免把长尾当异常。
- **summary 规模**：类/属性/模式列表；论文未给上限；工程上按 1–2 万实体估，超过就分域重建（digest 工程配方，非论文测量；`推测`）。
- **重建**：数据/本体变更触发；全量按周/月、增量按日（digest 工程配方，非论文测量）。
- **disjointness**：不贡献额外 flag；curated 的 7 对与 masked LLM 的 73–759 对都没有 flag 任何未被其他公理 flag 的答案（Appendix D.1）。不要把它当主检查。

## curated 审计

- **缺声明**：缺声明会经 declaration check 对每条用到它的正确答案误报；先自动补声明（domain/range），补不了的进人工队列（digest 工程配方；补后 FA 降幅未测，`推测`）。
- **与自身数据矛盾（Table 5）**：这是发布状态的本体与数据的差异清单；盲审的 data clash=0，不能把它当 FA 主因。先审计，但不要把整张表当 FA 归因。
- **工期**：curated 审计/补声明未测；`1–2 人日` 是 digest 对 data-derived setup 的估算，不是 curated 审计，不能挪用。

## 三种用法

- **as context**：把本体渲染进 prompt，让 agent 自己参考。
- **as check**：编译成 checker，对查询/答案做结构检查。
- **both**：两者都用；同源 context+checker 的 catch 下降是探索性观察，机制未定。

## 成本

> 口径：per **被 flag 的答案**，不是 per checked；66k 不能当每答案成本。

| Check | 每被 flag 的答案 token（median） | 时间（median） | 备注 |
|---|---|---|---|
| curated | 65,976 | 46.0 s | false alarm 多 → 重试多 |
| data-derived | 28,076 | 17 s | FA 少；setup 成本未记录 |
| 空结果重试 | 低 | 低 | FA≈0；真实答案 catch 仅 2.5% |

- 折算：`per-1k cost = flag_rate × per-flagged cost × 1000`；先测 flag_rate。
- setup：LLM-generated ontology <$1/个（Claude Opus 5.5）；data-derived setup 未记录；curated 由发布方承担、未测。
- **LLM judge**：按每条答案计费（一次模型调用），不是 per flagged；单位成本未测，见下节。

## LLM judge（替代分支；论文比较器）

- **输入/成本**：问题 + 查询 + 结果 + 答案；每条答案一次模型调用（单位成本未测）。
- **收益**：UniProt 真实答案 catch 40.3%、FA 16.2%、precision 31.3；catch 高于 curated（18.9）与 data-derived（8.2），FA 与 curated（16.8）接近、高于 data-derived（3.5）。人工故障上，curated/data-derived/masked LLM 对 changes of meaning 的 catch 是 0%（Table 4）；judge 能抓这类语义错（它判定的 41 个 changes of meaning 全抓到；Appendix C.2）。
- **代价**：把 flag 当行动信号后，40 条修好 / 83 条修坏；人工故障（有题面文本的 2,238 条）上 catch 98.7/98.0（Sonnet/Haiku），但会 flag 30–38% 答案仍正确的故障查询（Table 11）。
- **条件**：UniProt 主表；Appendix C.2 比较器；真实答案由 agent 自己的模型扮演，人工故障由 Claude Sonnet 5.5 / Haiku 5.5 扮演。
- **结论**：检错多 ≠ 净收益；先测净修复（fixed − corrupted）、成本、稳定性，不能默认更好（`推测`）。

## 失效模式

- **误报导致「修坏」。** 正确答案被 flag，agent 去修，把对的改成错的；specific feedback corrupt 1.0%。
- **漏检语义错误。** 类型都对、关系方向反了/边界划错（changes of meaning），curated/data-derived/masked LLM 的结构检查抓不到；judge 能抓但修坏多于修好。
- **判定器不可解释。** 只说错、不说哪条约束，模型只能换姿势重试。
- **串联放大误报。** 前一级误报引发下游大量无效工作。
- **把 curated 当权威 / 把 FA 归因于「与数据矛盾」。** 缺声明会让 declaration check 对每条用到它的正确答案误报；FA 主源是 domain/range 与 declaration check（盲审 32 个 FA 的双标注一致项：undeclared term 17、closed-world 11，data clash 0）。「schema 与自身数据矛盾」是 Table 5 的独立观察，不能当 FA 主因；上线前仍要补声明/审计。
- **把 LLM judge 当更好替代。** judge 检错更多，但修坏多于修好（40/83），且每条答案一次模型调用；见 LLM judge 节。
- **用 accuracy 评估 checker。** catch 与 FA 混在一起，会得出反向结论。
- **同源 context + checker。** catch 下降是探索性观察；机制（确认偏差 vs 信息冗余）未定，不要写成「判定器必须不同源」的部署规则。

## 与本体 / 回路的关系

本体在输出后以 **schema/约束** 出现；约束强度中（能 flag，不保证语义真值），覆盖率取决于错误类型。被违反时 checker 能报出约束/查询片段；不能报「意义不对」。要补语义错可上 LLM judge；但 judge 修坏多于修好（F6），别把它当免费升级。

## 实施与客户价值（A3/A4）

### 实施决策

- 先建空结果重试基线；只有能抓「有结果但答错」的增量，才建 checker。
- 选 data-derived 做 check（FA 低）还是 curated（catch 高但 FA 高）；不盲目组合。
- 验收用 catch/FA/per-1k 成本，不用 accuracy。
- **feedback 默认**：specific 28.3% 修复 / 1.0% corrupt，generic 20.2% / 0.2%；未验证前先 generic，验证后再 specific（工程默认；C5 最终准确率差异未确立，不能写成「generic 更安全」）。
- **judge 分支**：LLM judge 检错更多但修坏多于修好（40 修好 / 83 修坏）；先测净修复/成本/稳定性，不能默认替代结构 checker（`推测`）。

### 数据/接口

- 输入：SPARQL 查询、结果绑定、本体/schema、数据 summary。输出 `{verdict, constraint_id, query_fragment, message, evidence}`；unknown 不阻断。
- 挂载：query check / binding check；specific/generic 可切。specific 带约束/片段但 corrupt 更高，未验证前默认先 generic（工程默认，不是安全结论）。
- LLM judge 输入问题/查询/结果/答案，每条答案一次模型调用；成本/稳定性未测（Appendix C.2）。
- 评测：200 题、空结果重试基线、data-derived check；人工抽 50 条（工程配方）。

### 组织/成本

- 标注：200 题 × 人工复核；curated 审计/补声明工期未测（论文未测，需自测）；data-derived setup 未记录，digest 按 1–2 人日估（`推测`）。
- 运行：per-flagged 66k/28k tokens；LLM judge 每条答案一次模型调用（成本未测）；审批/告警处置 0.5–1 人日/月（`推测`）。

### 部署度量（无 ground truth）

- **抽样**：100–400 条分层抽样人工审计，报 Wilson CI；每季度重抽（digest 工程配方，非论文测量）。
- **在线 A/B**：同一流量分「空结果重试」vs「空结果重试 + data-derived check」；主指标 catch/FA、per-1k token、告警处置工时。
- **LLM judge 分支**：同样抽样/A-B，但主指标加净修复（fixed − corrupted）与每条答案模型调用成本；不能只看 catch。

### stop condition

- **采纳门（工程门，`推测`）**：真实/人工混合集上 catch ≥30% 且 FA ≤10%，per-1k 成本 ≤ 人工审核的 1/3；否则不做。
- 增量 catch <5pp 或 FA >15% → 停，不接 curated（工程门）。
- per-1k 成本 > 人工审核 1/3 → 停（工程门）。
- 语义错为主 → 换 LLM judge/人工，不用结构 checker；judge 分支另测净修复/成本/稳定性，不直接套用结构 checker 的门。

### 第一个 sprint

2 周、本方 KG、200 题：空结果重试基线 → data-derived summary + declaration/pattern check → 增量 catch/FA/成本 → 人工抽 50 条 → 预写 go/no-go。

### 替代方案

- 空结果重试（最便宜）；LLM judge（语义错更强，但修坏>修好、每条答案一次模型调用、成本/稳定性未定）；人工审核；采购 SHACL/校验服务；curated 本体（需先审计）。
- 论文没有与 LLM judge/人工/SHACL 服务的头对头成本；build/buy 只能给公式。

### 客户指标/V3（`推测`）

- 指标：每千次产出真实语义错误拦截数、误判正确数、per-1k token/工时、告警处置时长。
- 反事实：不做 → 空结果重试 + 人工抽检；先测基线。
- V3：200 题；成功 = 增量 catch ≥5pp、FA ≤10%、per-1k 成本 ≤人工 1/3；失败 = 增量 <5pp 或 FA >15%；停止线 = 年省审核 < 维护。
- judge 分支：另测净修复（fixed − corrupted）、每条答案模型调用成本；不能只看 catch，也不能默认 judge 更好。
- 反例：语义错；无 ground truth；curated 与数据矛盾；FA 修坏 > 拦下；judge 修坏 > 修好。

## 关联

- [Ontology Catch digest](../../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [00-harness/verification](../../00-harness/verification.md)
