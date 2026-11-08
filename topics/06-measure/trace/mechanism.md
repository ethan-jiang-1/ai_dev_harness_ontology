# 过程有效性 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

形式化器的设计初衷是：模型把问题写成程序，求解器负责搜索并给出保证。**判据通常是「程序输出对不对」——但这看不出程序是在搜索，还是在复述。**

SLB：在写程序之前，推理轨迹里已经在赋值、试算、排除变量取值，常常一路算到最终答案；程序只是把答案重述一遍。

## SLB 本体

| 部分 | 节点 | 判据 |
|---|---|---|
| A. Trace | A1 existence | trace 是否 assign/test/rule out 决策变量 |
| | A2 extent | 是否给每个变量赋值（complete/partial） |
| | ratio | SLB 段落字符数 / trace 总字符数（论文 trace 字符占比；token 口径另算，不可与阈值混用） |
| B. Program | B1 Hardcoded | 打印答案，不计算 |
| | B2 Partly fixed | 计算，但把 trace 决策写进源码 |
| | B3 Steered | 搜索，但 tiebreak/order 被选成返回 trace 答案 |
| | B4 Independent | 在所有约束下搜索；trace 的 SLB 是浪费 |
| C. Output | C1 / C2 | 输出是否匹配 reasoning answer / reasoning answer 是否正确 |

**只有 B4 真正把搜索交给 solver；B1–B4 都可能通过输出评估。**

**只有 trace 必须自己「求解」才算 SLB；从题面直接读出的限制不算**（codebook 排除项，[F6](./findings.md)）。不先写这条，标注时「读题」与「求解」不可分。

## 两种伤害（成本一条只在部分数据集成立）

1. **token 成本在部分数据集随规模上升。** paper 按问题规模分三档：Meeting Planning 的 SLB token 从 3,873 升到 10,971，ZebraLogic 从 532 升到 4,148（GPT-OSS 例外）；**Calendar 与 BlocksWorld 不增长**。只能写成条件性结论，不能当普遍规律；且这是 token 数，不是金额。`已核`（数字，paper §5-H1）/ `存疑`（普遍规律；digest §8 的 E-07 概括未带此条件）。
2. **保证失效。** solver 本该提供模型推理所缺的保证；若程序只复述轨迹答案，这层保证不存在。163/1,791 程序继承 reasoning answer；reasoning 错时 hardcoded 0/19 正确，independent 32% 正确。`已核`

## 数字

- **85%** traces 含 SLB；**BlocksWorld PDDL 例外只有 51%**；71% 占 ≥10% token；47% ≥1,000 token；**24%** 推理 token 是 SLB。
- **77–89%** 程序仍独立重算；**88%** 独立程序输出恰好等于 reasoning answer。
- **SLB 与准确率无关联**：ratio +0.1 → +0.007 [−0.011,+0.022]；+1,000 tokens → +0.005 [−0.002,+0.013]。
- **形式语言影响最大**：Python 比 Z3/PDDL 多 0.03–0.20 ratio；FL 解释 0.123 方差，数据集 0.057，模型 0.008。
- **Cautionary prompts**：ratio −0.053/−0.058（≈1/4），准确率不变；但会把 hardcode 推成更隐蔽的 partly fixed/steered。
- **Placeholders**：SLB token **−97%**，ratio 0.25→0.005（字符占比），traces 94%→15%，准确率 **+2.6**（digest 记「不降」，未给区间）。**运行 token 成本按模型/数据集不同**：Qwen Calendar 约 3×/+54%，GPT-OSS 约 −31%；TCO 不能只用「一次性集成+多值注入」估。
- **Batching**：SLB token −62%，但 reasoning 总量同步下降，ratio 几乎不变；准确率 **−5.9**。

## 为什么输出评估看不见

只看程序输出对不对，结构上无法区分 B1–B4。这不是「测不准」，是「测不到」。任何只看最终产物的判据，都会放过冗余与错误继承；要看见它们，判据必须能读中间（轨迹、程序、检索路径）。

## 失效模式

- **Hardcode 被输出正确掩盖。**
- **Partly fixed/steered 更隐蔽**；cautionary prompt 可能把它们推得更深。
- **Batching 砍 reasoning 总量**，SLB 比例不变但准确率下降。
- **闭源模型无完整 trace**，无法测。
- **Placeholders 不适用于值与结构不可分的任务。**

## 与本体 / 回路的关系

本体/形式化在 formalizer 里是 **目标语言 + 约束**；它只能限制程序结构，不能保证 solver 真搜索。被违反时通常没有信号，除非读 trace。

## 实施与客户价值（A3/A4）

> 读者是「要不要为 trace 审计与 placeholders 批预算的人」。机制见上，判断见 [findings](./findings.md)，缺口见 [frontier](./frontier.md)；本节只回答改变哪个决定、要什么数据、何时必须停。未标来源的推算一律 `推测`。

### 实施决策

1. **把 trace 指标写进发布闸门，而不是再加一个 benchmark 分数。** 只看 program accuracy，B1–B4 结构上不可区分；163/1,791 程序继承轨迹答案，reasoning 错时 hardcoded 0/19 正确、independent 32% 正确。`已核` → 改变的是**评测报告与上线清单的字段**：必须报 SLB ratio、B1–B4 分布、继承率；只有 program accuracy 的评测不能作为 formalizer 上线依据。
2. **预算给 placeholders 的数据契约，不给 cautionary prompt。** placeholders 把 SLB token 降 97%、准确率 +2.6（不降）；cautionary 只减约 1/4（ratio −0.053/−0.058），且可能把 hardcode 推成更隐蔽的 B2/B3。**但论文只按 SLB 降幅排序，没有单位成本/维护性对照；placeholders「最强」不等于「最便宜」。**`已核` → 改变的是**工作项**：sprint 里做 prompt 构造与运行时值注入，不是再写一句「别 precompute」。
3. **B 类判定必须读程序源码，不能拿输出一致性当代理。** 88%（1,027/1,174）的独立程序输出恰好等于 reasoning answer；用 C1 代理继承会把绝大多数 B4 误标成继承。`已核`（数字；代理失效是直接推论）→ 改变的是**日志/存储**：trace 全文与程序源码必须配对留存，只存 stdout 的管线做不了这项审计。
4. **形式语言按「谁在搜」选，不按表达力选。** Python 比 Z3/PDDL 多 0.03–0.20 SLB ratio；解释方差 FL 0.123 > 数据集 0.057 > 模型 0.008。`已核`（PDDL 臂带参考 problem file，语言差异幅度 `存疑`）→ 改变的是**架构默认值**：域能声明式表达时默认 Z3/PDDL，Python 只在约束表达不了时用。
5. **闭源模型先按 audit-only 立项，不承诺 SLB 降幅；无完整 trace 的闭源 API 直接出局，不进 trace 工具的 buy 短名单。** 闭源 API 常只回摘要，没有完整 trace 就测不了 SLB，这是结构性盲区而非采样问题。能提供 trace 的评测/审计工具才进入 buy 臂，按 seat/trace 报价 + 集成人周算 NPV，低于 build 才买。`已核`（盲区）/ `推测`（出局、报价、NPV 与采购后果；digest E4 是决策框架）→ 改变的是**选型与合同**：把「返回完整 trace」写成资格项而不是评分项，没有 trace 的供应商不进短名单。

### 数据/接口

- **配对记录（审计最小单元）**：`{trace_id, model, dataset, fl, prompt, reasoning_trace, program_src, stdout, validator_verdict, token_trace, token_slb}`。`reasoning_trace` 要全文、`program_src` 要源码；缺任一项只剩输出级评估。审计放在哪一步、是否阻断生成，digest 未写；若选择只读旁路接入，属产品选择（`推测`）。
- **SLB 标注字段**：A1 existence、A2 complete/partial、ratio（SLB 段落字符数 / trace 总字符数；论文是 trace 字符占比，不是 token 占比）、B1–B4、C1/C2、judge evidence。**标注前先把排除项写进 codebook**：只有 trace 必须自己求解才算 SLB，从题面直接读出的限制不算（[F6](./findings.md)）。B2/B3 分歧由第三人裁决；digest 记 A1 只查段落不查整条 trace，要整条结论得另定口径。
- **Placeholder 契约**：`VALUES` 是扁平值表 `{Person1:"Ann", D1:30, …}`；**不含 schedules/lists/constraints**，TRAVEL 等独立字段另放。只替换事实值，不替换结构/约束名；prompt 构造前替换，程序运行时注入，solver/validator 只看注入后的值；日期/多值/表格/自然语言条件不能塞进 `VALUES`；值与结构不可分的任务不用（[G3](./frontier.md)）。
- **分母与采样**：继承率分母是「能跑的程序」（1,791/2,000），ratio 按 SLB 段落字符 / trace 总字符，准确率按题——换分母/口径即不可比。9% 基准率要估 ±5pp（95%）约需 126 条；100 题只能看方向。B/C 覆盖的是非随机子集（只程序能跑、只完整 reasoning answer），报告要写明这个选择偏差。
- **判据流程**：trace/program/output 三段一起给 judge，要求逐条给证据；先人工标 30 条校准到 ≥90% 一致再冻结；judge 只做批量筛查，发布门用人工抽检。`推测`（digest 只给一致率，未给 judge 误报率）。

### 组织/成本

- **owner（`推测`，digest 未写组织分工）**：平台/评测 owner 拥有 trace 管线、codebook 与基线；formalizer/模型 owner 拥有 placeholders 契约与 FL 选型；域 owner 提供 solver/validator 与 ground truth。缺域 owner，C2 没人能标。
- **人周（`推测`，digest 给的是估算不是实测）**：审计脚本 1–2 人周、placeholders 集成 1–2 人周；人工校准 30 条 × 2 人 × 1–2 小时另计。三项相加就是首轮预算，改 solver/validator 接口另计。
- **运行成本**：每千条 trace 的存储 + judge token（digest 未给金额；`推测` 为可变成本主体）；placeholders 是一次性集成，但运行 token 仍按模型/数据集成：Qwen Calendar 约 3×/+54%、GPT-OSS 约 −31%；不能只算「多值注入」。batching 省 62% SLB token 但准确率 −5.9，不能当净省（`已核` 数字）。
- **维护（`推测`）**：codebook 冻结后模型/FL 变更要重标 30 条抽检；trace schema 变更要回填历史；按季度重估人时。没有版本化 codebook，跨季度 ratio 不可比。**评估算力要按模型/配置另计**，不能并进一次性集成。

### stop condition

- 拿不到完整 trace（闭源）→ audit-only，不声称 SLB ratio。
- 要求单次低延迟、或不需要 solver 保证 → 不做 trace 审计/placeholders；这两类不在本页收益范围内（`已核`：digest §6.3 列为别用；具体项目归类 `推测`）。
- SLB ratio <2% → 不值得建。
- trace 有 SLB 但程序全 B4 → 不修，只记录浪费。
- 值与结构不可分、placeholders 不可用 → 换 Z3/PDDL 或退回 validator 审计。
- 试点程序准确率降 >5pp，或 placeholders 引入运行时错误 → 停 placeholders。
- 为省 token 上 batching 且准确率降 >2pp → 停（batching 实测 −5.9；2pp 是本页阈值，`推测`）。
- 年省返工 < 集成成本 → 停。
- 样本 <126 条却要报稳定比例 → 只出方向，不写比例。

### 第一个 sprint

2 周、1 类 CSP、1 个开源 reasoning model、100 题；范围是 audit-only 基线 + 50 题 placeholders A/B，不接线上写权限，不碰闭源。

1. **第 1–3 天 · 打通配对**：trace 全文 + 程序源码落盘；冻结 ratio、继承率分母、准确率三个口径。
2. **第 4–5 天 · 校准**：人工标 30 条，judge 校准到 ≥90%，冻结 codebook。
3. **第 6–8 天 · 基线**：出 SLB ratio、B1–B4 分布、C1/C2、继承率；标区间，不标点估计。
4. **第 9–12 天 · 干预**：50 题 placeholders on/off，量 ratio 与准确率差。
5. **第 13–14 天 · 收口**：一页基线 + go/no-go memo。

**交付物**：可复跑审计脚本 + 一页基线（含 B 分布与区间）+ 可开关 placeholder 模式 + go/no-go memo（写明阈值与样本量限制）。

**出口**：
- **go**：ratio ≥2%、继承 >0、placeholders 后 ratio ≤0.02 且准确率降 ≤2pp → 进第二 sprint，扩到第二个 CSP/模型，样本补到 ≥126 条。
- **no-go**：ratio <2%；或全 B4；或准确率降 >2pp / placeholders 不可分离 → 停修，转 audit-only（digest E4：>2pp 即只 audit-only）。
- **不出结论**：100 题区间宽，继承样本约个位数 → digest 的「继承率降 ≥50%」在本 sprint 测不了，只作观察项；硬门放在 ratio 与准确率上（`推测`）。

### 客户指标/V3

- **受益者**：formalizer 平台/产品团队（直接）；依赖 solver 保证的下游——审计、合规、需要可解释证明的场景（间接）。**痛点**：程序跑对但没在搜；reasoning 算错时程序继承错误；solver 保证静默失效，现有输出评估看不见。
- **指标**：SLB ratio、继承率、**无保证通过率**（输出判对且程序属 B1–B3 的占比；digest 的「静默错答率」在本页按这个可计算口径落地，`推测`）、审计发现数（报告时注明分母，`推测`）、返工人时。尺子本身看 judge–人一致率（digest 给 90–98%，参考样本 A1 110 段 / A2 40 traces / B 60 programs）与人工抽检误标率（`推测`：digest 未给 judge 误报率）。
- **反事实**：只报 program accuracy → 上述全部不可见；不做 trace 审计 → 由平均准确率或 vendor demo 决定是否上 formalizer；不上 placeholders → 靠 cautionary，减 1/4 且可能推深。
- **V3 试点**：100 题、1 模型、placeholders on/off。**成功** = ratio ≤0.02 且程序准确率降 ≤2pp；**失败** = 准确率降 >5pp 或不可分离；**停止线** = 12 个月 `(年省返工×工时价 + 审计发现数×处理成本) < TCO`；继承率降 ≥50% 列为观察项，不作硬门。
- **口径警告**：SLB 与准确率无关联（ratio +0.1 → +0.007 [−0.011,+0.022]），试点不能把「准确率提升」写成收益；收益只能落在保证、审计与返工。`已核`

### 反例

- **收益可能落在准确率之外。** SLB 量与准确率无关联，digest 对 placeholders 只记 +2.6「不降」、未给区间；若客户只为 task accuracy 买单，这页的机制不产生可测收益，价值必须记在保证/审计/返工上，而那三项本仓库没有部署数据（可见性缺口见 [G1](./frontier.md)）。`已核`（无关联）/ `推测`（收益）。
- **事件稀疏，ROI 可能为负。** 继承只有 9%（163/1,791），hardcoded 仅 47；要靠「少返工」回本轮集成 1–2 人周 + 每千条 trace 的存储/judge，低流量团队可能永远回不了本。`推测`
- **SLB 多不等于程序错。** 88% 的独立程序输出恰好等于 reasoning answer；伤害集中在「reasoning 错且程序继承」这一小块（hardcoded 0/19、partly fixed 1/13）。reasoning 本身准确率高的域，这块很小。`已核`（数字）/ `推测`（域间外推）
- **placeholders 不是万能，语言建议也有混淆。** 值与结构不可分（交互式规划）不能用；运行时注入本身可能引入映射/类型错（digest 未测，`推测`）；H4 的 PDDL 臂额外给了参考 problem file，照「换 Z3/PDDL」执行可能把 prompt 差异当语言收益。`已核`（混淆自述）
- **指标自己也可能偏。** A1 只查段落不查整条 trace，judge 参考样本 A1 110 段 / A2 40 traces / B 60 programs，B/C 又只覆盖能跑的程序与完整 reasoning answer；ratio 与继承率的绝对值不宜跨团队比较，只能同管线前后比。`已核`（局限自述）/ `推测`（可比性）

## 关联

- [SLB digest](../../../src/papers/2611.02395-solver-like-behavior/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [metrics](../metrics/README.md)
