---
status: draft
deliverable_status: draft
updated: 2026-11-09
target: 工程负责人 / 架构师
basis: E-01–E-20, C-03; recipes R0–R12
---

# 02 · 工程实施：把本体接进 harness 的做法

> **读者**：工程负责人 / 架构师 ｜ **回答**：拿本体做某件事，具体怎么做 ｜ **不回答**：值不值得做（去 01）、为什么是这些位置（去 03）。

> 这份交付物回答：**本体拿进来之后，到底能帮什么；如果我要做某件事，工程上从哪一步开始、接口长什么样、开源/论文里有没有能照抄的东西。**
>
> 它不建本体，也不评价本体质量；它假设你已经有（或能拿到）一份领域本体，问题是怎么让它被机器执行。
>
> **证据等级**：接口/公式/代码锚点标 `已核` 或 `已核（代码）`；工程配方、阈值、人日估算标 `推测`。交付物只引 E-xx，细节回 `topics/`。
>
> **R0–R12 是从 `topics/` 各派 `mechanism.md` 与代码级核对抽取的工程配方，不是新的 E。** 它们回答「怎么做」，不回答「做了有没有用」；效应量仍以 E-xx 为准。


## 0. 一页结论

**这份交付物只回答「怎么做」，不回答「做了有没有用」。**

1. **先过 R0**：名字/单位、声明、覆盖、执行落点四项检查不过，后面的 recipe 都是沙上。
2. **只选一条主 recipe**：按错误类型选 R1–R12；先 shadow，不要同时上三个。
3. **每条 recipe 十字段**：目标/前提/接口/步骤/证据/成本/验收/失效/锚点；填不满的字段就是上游任务。
4. **证据只到 E-xx**：recipe 是工程配方，不是新结论；效应量仍看 E-xx 的限定。
5. **如果只做一件事**：R0 + 账本 + K1；不要先建整座塔。

## 1. 怎么读

### 1.1 加载集（按需披露）

| 要做 | 只读 | 不读 |
|---|---|---|
| 10 分钟判断要不要做 | 本页 §0 + §3.1 的 R 索引 + [01 §0](../01-capability-status/README.md#0-一页结论) | 全部 recipe |
| 选一条 recipe / 定接口 | 本页 §0–§3 + 对应 recipe + [appendices/interfaces](appendices/interfaces.md) + [execution-forms](../../topics/execution-forms.md) | 24 篇 `paper.md`、`card.md`/`references.md`/`appendix.md`、其他派 |
| 定验收/停线 | 本页 §5 + [operations/ledger](operations/ledger.md) + [operations/evaluation](operations/evaluation.md) + 对应 `mechanism.md` | `conclusions` 全表 |
| 做预算 | 本页 §3.5 + [operations/cost](operations/cost.md) + 对应 recipe §7 | 全部论文 |
| 上线/回滚 | [operations/rollout](operations/rollout.md) + [operations/domains](operations/domains.md) | 其他 recipe |

> 反向链：recipe → `mechanism.md` → digest §6.5；见 [meta/loading §从交付物倒查](../../meta/loading.md#从交付物倒查反向加载)。

### 1.2 三条阅读路径

| 时间 | 读什么 | 得到什么 |
|---|---|---|
| 10 分钟 | §0 + §2 | 知道这份交付物的结论与地图 |
| 1 小时 | §1 + §2 + §3 | 能指到具体能力/条目与证据 |
| 深读 | §3 + §4 + §5 | 能复述条件、边界、验收与缺口 |



<a id="0-一句话与五步法"></a>
## 2. 地图：先定错、再选位置/形态

### 2.1 五步法与决策树

**本体的工程问题不是「建什么本体」，而是「把哪条判据放在哪个时刻、以什么形态执行、用什么尺子验收」。**

五步：

1. **定错**：你要防的是什么错？可逆吗？会扩散吗？
2. **准入**：本体能被执行吗？先过 R0。
3. **选位置**：动作前 / 输出时 / 输出后 / 落盘前 / 跨轮 / 跨运行；或者轴外的读路径/供给。
4. **选形态 + 定接口**：engine / compiled / context / label；这个位置拿得到什么事实？输出什么字段？三态怎么表示？
5. **定尺子**：按机制选指标；先建账本，再谈效果。

**先看你要做什么：**

```
你要让本体帮你做什么？
├─ 还没确认本体能不能用 ──────────▶ R0（准入体检）
├─ 让模型知道得对 ──────────────▶ R1（K1）/ R2（投影）/ R3（编译）
├─ 让产出可审计 ────────────────▶ R4（证据契约）
├─ 让错误被抓住 ────────────────▶ R5（checker）
├─ 让不该做的动作做不了 ────────▶ R6（可逆性闸）
├─ 让跨轮记得对 ────────────────▶ R7（身份/记忆）
├─ 让检索结果可见/不可见 ───────▶ R8（读路径）
├─ 让落盘有授权 ────────────────▶ R9（只能设计，无实现）
├─ 做离线/CI 校验 ──────────────▶ R10（SHACL）
├─ 用本体编译查询 ──────────────▶ R11（OBDA）
└─ 受监管、要引用/solver/签核 ──▶ R12（受监管供给）
```


<a id="1-先定错五个问题"></a>
### 2.2 先定错：五个问题

| 问题 | 如果答案是 | 去哪 |
|---|---|---|
| 错误可逆吗？ | 可撤销 | 判定/checker 优先（R5） |
| 错误会扩散到下游吗？ | 会 | 加 evidence/checker；不要只做事后审计 |
| 错误会污染后续轮次吗？ | 会 | memory/身份（R7） |
| 错误不可逆且代价高吗？ | 是 | 动作前/落盘前（R6/R9） |
| 判定所需事实拿得到吗？ | 拿不到 | 先补状态/观测；不要做硬闸 |

> 这五个问题不是评分卡，是**排除法**：答不出「错误是什么/可逆吗」，就不要选机制。组织建议（非 E）。

#### 2.2.1 分诊表（组织建议，非 E）

> 依据 E-06 的五角色/七变量与 [06/failure-attribution](../../topics/06-measure/failure-attribution/mechanism.md)；分诊本身没有效应量。

| 失败表现 | 更像哪类问题 | 先看 | 不要先做 |
|---|---|---|---|
| 叫错名字、单位混、槽位对不上 | 词汇/数据契约 | R1 | R2/R3 |
| 答案对但没依据、无法审计 | 输出契约 | R4 | R5（不能补检索） |
| 类型/关系/模式错 | 结构判据 | R5 | R4（不检查语义） |
| 不可逆动作被执行 | 动作授权 | R6 | R8（只读） |
| 同一实体跨期碎裂/错并 | 身份/状态 | R7 | R3（检索） |
| 检索结果越权可见 | 读路径 | R8 | R6（动作前） |
| 错误变更落盘 | 写授权 | R9（设计） | R6（动作前） |
| 产物需要法规引用/solver/签核 | 受监管工作流 | R12 | 只做 R2 |

**分诊的出口**：一条错误只能落到一个「先看」；落不下，说明还没定义错误，不要选机制。


<a id="2-选位置六个时刻--四个轴外位置"></a>
### 2.3 选位置：六个时刻 + 四个轴外位置

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

- 可撤销、会扩散 → R4 + R5。
- 会污染后续轮次 → R7。
- 不可逆、对外 → R6。
- 不可逆、持久化 → R9（先看：没有实现）。
- 要求可复现 → determinism（没有实现）。
- 离线/CI 数据质量 → R10；关系库查询 → R11。

**R0 不是位置**：它是准入；四项检查不过，位置选了也白选。

**R10/R11 不新增时刻**：R10 是输出后/离线的 CI 校验；R11 是供给/查询编译。它们改变「在哪跑」，不改变六时刻分类。


<a id="3-选形态五种别把-context-当低配-engine"></a>
### 2.4 选形态：五种，别把 context 当低配 engine

| 形态 | 机器做什么 | 什么时候用 | 不代表 |
|---|---|---|---|
| `engine` | 推理器/引擎直接求值：DL、SHACL、查询重写 | 需要「本体一变，输出就变」的求值 | 不等于会拦/有授权 |
| `compiled` | 本体→SHACL/规则/状态结构，再由代码执行 | 需要把本体变成可测试的约束 | 不等于编译正确 |
| `context` | 进入 prompt/上下文，模型自行使用 | 知识供给、可读性优先 | 不是弱执行，是不执行 |
| `label` | 只当标签表/schema/分类 | 命名、类型、路由 | 不参与判定 |
| `none` | 没有执行，或本体不是被测变量 | 概念/生成/评测 | 不能当「执行了但无效」 |

**一个反直觉的结论**：`engine` 内部至少四种语义（E-20）；「有引擎」不是强度刻度。选型时先问「机器到底做了什么」，再问「它能不能改变走向」。

## 3. 主体：R0–R12 与参考实现

<a id="4-九条工程做法r1r9"></a>
<a id="4-十二条工程做法r0r12"></a>
### 3.1 十二条工程做法（R0–R12）

> 本节只做索引；完整配方（十字段：目标/前提/接口/步骤/证据/成本/验收/失效/锚点）在 [`recipes/`](recipes/README.md)。每条 recipe 都与 E-xx 和 mechanism.md 对齐；见 [appendices/traceability](appendices/traceability.md)。

| R | 一句话 | 接缝/形态 | 主证据 | 成熟度 | 完整配方 |
|---|---|---|---|---|---|
| **R0** | 先证明本体能被执行（名字/单位、声明、覆盖、落点） | 准入 | E-02/E-03/E-12/E-20 | 配方 | [readiness](recipes/readiness.md) |
| **R1** | 先把名字、单位、别名对齐；K1 够就停 | 供给 / context | E-12 | A | [knowledge](recipes/knowledge.md#r1--k1-语义层先把名字和单位对齐) |
| **R2** | 固定分节文本投影；先 K1 再投影 | 供给 / context | E-12 | B | [knowledge](recipes/knowledge.md#r2--知识投影把领域知识写成固定分节的文本) |
| **R3** | 只买 claim+span；先算 `p_min` | 供给 / compiled | E-08/E-14 | B | [knowledge](recipes/knowledge.md#r3--证据编译只买-claim--逐字-span) |
| **R4** | 输出带观察与 grounding；等级要校准 | 输出时 / compiled | E-03 | B | [judgment](recipes/judgment.md#r4--输出证据契约让答案带依据和接地等级) |
| **R5** | 先超过空结果重试；catch/FA 分开 | 输出后 / compiled | E-02 | B | [judgment](recipes/judgment.md#r5--输出后-checker先超过空结果重试) |
| **R6** | 只在不可逆/高代价/弱模型时试；先 shadow | 动作前 / compiled | E-04/E-15 | B | [constraint](recipes/constraint.md#r6--动作前可逆性闸只在不可逆高代价弱模型时试) |
| **R7** | 先 registry，再状态；CMR 与 precision 同看 | 跨轮 / compiled | E-05/E-17 | B | [state](recipes/state.md) |
| **R8** | 只做可见性，不当授权；已入库单实现/ fail-open 未修 | read-path / engine | E-20 | B（条件性） | [constraint](recipes/constraint.md#r8--读路径过滤只做可见性不要当授权) |
| **R9** | 只能设计，不能声称落地 | 落盘前 / 无实现 | E-20 | C | [constraint](recipes/constraint.md#r9--落盘前授权现在只能设计不要声称已落地) |
| **R10** | 离线/CI SHACL；三态不可折叠 | 离线/CI / compiled | E-20 | A | [axis-out](recipes/axis-out.md#r10--离线ci-shacl把没检查完做成第三态) |
| **R11** | 查询时编译；不是闸/判定器 | supply / engine | E-20 | A | [axis-out](recipes/axis-out.md#r11--obda-查询重写本体在查询编译时被执行) |
| **R12** | 证据 + solver + 人签核；不是准确率项目 | 供给+输出+人 | Grid | B（benchmark） | [regulated](recipes/regulated.md) |

#### 3.1.1 为什么 R0 在 R1 前

- 02 假设「你已经有一份领域本体」；但「有」不等于「能执行」。
- R0 的四检（名字/单位、声明、覆盖、落点）任何一项不过，R1–R12 都会在沙上：投影抄错单位、checker 误报、action gate 拿过期状态做硬 veto。
- R0 只要有现成任务/样本，30–60 分钟即可；它不建本体，只决定「先修哪一项」。

#### 3.1.2 三条典型组合

| 场景 | 先做 | 后做 | 不要做 |
|---|---|---|---|
| 工业设备知识问答 | R0 → R1 | 若 K1 不够 → R2 → R5 | 一上来建塔/上写路径 |
| 受监管工程（法规+solver） | R0 → R12（含 citation/solver/签核） | R10（CI 校验） | 只做 R2 投影，不做 solver/签核 |
| 跨期客户/身份 | R0 → R7 | R9（设计，先 shadow） | 直接自动 merge |

**不要一次上三条。** 先一条 shadow，拿到自己的 `p_h`/false-veto/FA，再扩。


### 3.2 开源参考实现：能抄什么，别抄什么

| 项目（commit） | 位置 | 形态 | 能抄 | 别抄 | 代码锚点 |
|---|---|---|---|---|---|
| trustgraph `184f622` | `read-path` | `engine` | 策略图 + `user_context` 契约；SHACL-AF target/rule | fail-open、只删 subject、已入库单实现 | `policy_filter.py` |
| semantica `39cf721` | `checker` | `compiled` | 本体→SHACL 的派生路径；pyshacl `inference="none"` | 把 CLI 校验当 in-loop；派生 shapes 未测 | `OntologyEngine.to_shacl` |
| ontop `964dbb7` | `supply` | `engine` | TBox 饱和 + 查询重写 → SQL；R2RML 映射 | 把它当闸/判定器；只支持 OWL 2 QL | `QuestQueryProcessor` |
| open-ontologies `375fbc4` | `none`（工具面/CI） | `engine` | JSON 三态（通过/违反/未检查完）；`closure_diff` 影响报告；verified/Core 边界 | 把它当写授权；只看 shell 退出码（第三态会被折叠）；本次未跑通 | `shacl.rs` / `shacl_verified.rs` |

> 出处：E-20 与 [execution-forms](../../topics/execution-forms.md#代码级核对2026-11-09)。四者都是只读代码、未做对照实验；**代码能跑 ≠ 机制有效**。

**第二 read-path 实现（外部扫描线索，未入库）**：2026-11-09 定向扫描发现 [`Matdata-eu/sparql-guard`](https://github.com/Matdata-eu/sparql-guard)（Apache-2.0，HEAD `6b68d769`）：TS 写的 SPARQL 代理，用 **查询重写** 而不是返回后过滤；fail-closed、subject+object 两侧、SHACL Core 子集；有一组 vitest 用例（外部复核报告 76/76 通过，未在仓库内复跑）。它**不是**已入库证据：单作者、1★、无 harness 调用点、无泄漏率/时延测量；而且它把「read-path」拆成两种执行点（返回后过滤 vs 查询重写）。所以：**read-path 至少有两种执行点，但 seam 语义未定；01 的 B 评级不因此升级。**


### 3.3 论文/开源给的「准确指示」到什么程度

| 层级 | 能给什么 | 例子 | 能不能照抄 |
|---|---|---|---|
| 代码级 | 真实接口、调用链、失败行为 | 4 个开源项目（E-20） | 抄接口与边界；不抄效果 |
| 公式级 | 可算的盈亏平衡/代价 | 编译 `p_min = 2% + c/(0.929Q)`（E-14）；CASEL `J(m)`（E-15，`γ_m` 是假设） | 代自己的数；不抄论文的 `c`/`γ` |
| 协议级 | 判定/标注/三态 | catch/FA 分开报（E-02）；grounding 四等级（E-03）；promotion 七条（Commit Boundary，概念） | 抄协议；不抄阈值 |
| 参数级 | 具体设置 | POLAR T1–T5/τ=0.80；OntoAct 三值；FIRME 匹配顺序/0.8 | 只当起点，按域重标 |
| 流程级 | 步骤顺序 | CAI parse→chunk→enrich→validate→assemble→register；OA-RAG DESCRIBE/ASK/SELECT | 抄流程；不抄规模 |
| 概念级 | 设计问题 | commit gate；determinism；多智能体共享本体 | 只能当设计清单，不能当实现 |

**结论**：论文/开源在**接口、公式、协议、参数**上给了可操作的指示；在**端到端架构**和**效应量**上没有。不要指望一篇论文给出「拿本体做 X」的完整 recipe；能抄的是零件，组装要自己测。


### 3.4 参考架构（组织建议，非 E）

```
request
  │
  ├─▶ R0 准入（名字/单位/声明/覆盖/落点）
  ▼
context builder ──◀ R1 K1 / R2 投影 / R3 编译（03）
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
- 每个箭头都要有数据契约；没有契约的「接缝」只是概念。逐箭头字段见 [appendices/interfaces](appendices/interfaces.md)。
- `commit gate` 标注为「设计、无实现」：它没有实现（E-20）。
- 离线/CI（R10）与 OBDA（R11）不在主回路；不要画进「实时链路」。


### 3.5 最小落地路线

| 阶段 | 时间 | 做什么 | 产出 | 出口 |
|---|---|---|---|---|
| 0 | 3–5 天 | R0 准入 + 建账本：token/时延/决策/审批/回滚；跑基线 | `readiness_report` + 账本 schema + 基线分布 | 能按机制出分布 |
| 1 | 2 周 | R1 + 一个接缝 shadow（R2/R5/R6 三选一） | 回放结果 + 工时 + 噪声地板 | 有增量，且不是平均掩盖 |
| 2 | 2 周 | 扩样本；标 false-veto/FA；算 stop 线 | go/no-go memo | 过门/停 |

**不要**：同时上三个接缝；先建整座塔；用平均 −38% 立项；没有账本就上机制。

**配套**：

- 账本字段 → [operations/ledger](operations/ledger.md)
- 噪声/样本/预注册 → [operations/evaluation](operations/evaluation.md)
- 成本/TCO → [operations/cost](operations/cost.md)
- 上线/回滚/审批 → [operations/rollout](operations/rollout.md)
- 域约束 → [operations/domains](operations/domains.md)


## 4. 边界与反例

### 4.1 反模式

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
13. **跳过 R0。** 名字/单位/声明/覆盖不过，后面全是沙上。
14. **把离线 SHACL 当 in-loop。** CLI 校验不等于输出后自动拒收；要自己接。
15. **把 OBDA 当判定器。** 它只改变「能查到什么」，不校验答案。
16. **把 R12 的 99.9% 当部署。** 它相对最强 agent baseline 只高 0.5pp；benchmark 不是运营商规模。
17. **把 blocked 当正确拒绝。** 被 block 可能是 review 失败/不可用；要同操作、不同权限成对测，并同时报合法放行。


<a id="9-验收与-stop按机制选尺"></a>
## 5. 验收与缺口

### 5.1 验收与 stop：按机制选尺

| 机制 | 主指标 | 过程指标 | 反事实 | 停线（工程建议，非 E） |
|---|---|---|---|---|
| R0 | 四项检查 pass/flag/unknown | 修复清单 | 无检查直接上 | 任一 unknown 当 pass |
| K1 | primary-trap avoidance | token | K0 | 剩余 trap 与深知识无关 → 停 |
| 投影 | primary-trap/element | 字符数/维护人日 | K1 | <5pp、>60k、>2 人周/月 |
| 编译 | token/问、p95 | `p_h`/miss、`c`、`Q` | 词法检索 | `p_h < p_min` |
| evidence | 准确率、引用率 | 检索率、grounding 校准 | 纯文本 RAG | 检索率 <50% |
| checker | 增量 catch、FA、净修复 | per-1k 成本 | 空结果重试 | catch <5pp、FA >15% |
| action | harm、审批、false-veto、task success | 保留率、φ、miss–false-block 前沿 | 不上护栏 | 在 miss 预算下 false-block 前沿不可接受（不要用单点 5%） |
| memory | CMR、merge precision、Acc@complete | 抽取层误差 | 不做 registry | precision <90% |
| read-path | 泄漏率、误拦 | 延迟 | 不过滤 | fail-open 未修/object 方向未测 |
| commit | false-defer、unresolved、审计可追 | 人审工时 | 直接 merge | >20%、>10%、不可追 |
| 离线 SHACL | 负例检出、干净误报 | checked/passed/undetermined | 无 CI | 三态折叠/覆盖不明 |
| OBDA | 查询结果一致、时延 | 映射/本体版本 | 手写 SQL | 需要 DL/事务写入 |
| 受监管 | citation precision、strict-pass 违规 | 人签核分钟 | 人工流程/只做检索 | 违规 >0、精度 <0.95 |


### 5.2 还缺什么

| 缺口 | 现在有什么 | 缺什么 | 对 02 的影响 |
|---|---|---|---|
| false-veto | E-04 明确未测；blocked log 无 harm/授权标签 | 100 条 blocked 人工标注；同轨迹配对 | R6 只能 shadow；不能承诺「误拦 ≤5%」 |
| 写路径授权 | Commit Boundary 概念；E-20 无实现 | 一个 mutation class 的实现 + 20–50 false-defer | R9 只能设计 |
| 第二 read-path | trustgraph 一个；外部扫描有 sparql-guard 候选（未入库） | 第二实现（入库）+ harness 调用点 + 泄漏率/时延 | R8 保持条件性；不升第七时刻 |
| 接地等级校准 | E-03 自评、未校准 | 每级 100–200 条独立标注 | R4 只能排序/人工分流 |
| 跨域效度 | 单工厂/单基准/专有数据 | 更多独立域/基准 | R1–R7 阈值要重标 |
| 独立复现 | 20 条 E 无 `已证` | 仓库外复现 + EXP 指针 | 所有效应量仍是 `已核`/`推测` |
| 单位成本 | 公式有，单价空 | 人周价/审批分钟价/事故成本 | 不能出 build/buy 点估计 |
| 跨运行确定性 | 设计提案 | 实现 + 度量 | 不写成 R |
| 多智能体共享本体 | 空白 | 可判定设计 + 证据 | 不写成 R |

**这些不是本交付物的前置**；它们是下一步研究/工程的方向。


<a id="13-期待与数据需求验收规格"></a>
### 5.3 期待与数据需求（验收规格）

> 这一节不是结论，是**每条 recipe 的验收规格**：把「做完应该看到什么」写成可证伪的句子，再倒推要量什么。数据缺在哪里，就回 `topics/` 或 `frontier` 补。这是验收规格（非 E）。

| Recipe | 期待（可证伪） | 支持它需要的数据 | 现在的来源 | 缺口 |
|---|---|---|---|---|
| R0 | 四项检查能预测「能不能执行」 | 30–60 分钟检查 + 后续失败记录 | 工程配方 | 无对照 |
| R1 K1 | 目标域 primary-trap avoidance ≥0.90 | K0/K1 回放；3 任务；trap 标注 | E-12 | 跨域 |
| R2 投影 | K2 相对 K1 ≥ +5pp，且 ≤60k 字符、维护 ≤2 人周/月 | K1/K2 回放；字符；维护工时；顺序消融 | E-12 | 跨域；多设备 |
| R3 编译 | `p_h ≥ p_min`，p95 不超预算 | `p_h`/miss/`c`/`Q`/p95/span 覆盖 | E-14 | 自己的流量 |
| R4 证据契约 | 检索率 ≥50%，引用率 ≥85%，grounding 可校准 | 200 题；检索率/引用率/等级标注 | E-03 | 等级校准；句级 span |
| R5 checker | 增量 catch ≥5pp、FA ≤15%、净修复 >0 | 200 题；空结果基线；catch/FA/per-1k/净修复 | E-02 | 自己的故障分布 |
| R6 动作闸 | 在 miss 预算下报 false-block 前沿；低 miss 不能靠 block-all；harm 降，task success 不降 >2pp | 200–500 shadow；100 blocked 标注；四轴指标 + 前沿 | E-04/E-15；[E5 校准理论](../01-capability-status/data/e5-calibration-theory.md) | false-veto；同轨迹配对 |
| R7 记忆 | CMR/Acc@complete ≥ +10pp，merge precision ≥90% | registry on/off；200 units；三层评测 | E-05/E-17 | 自己的域；传播 |
| R8 读路径 | 泄漏率 0（含 object 方向），误拦可接受 | 第二实现；异常/对象用例；延迟 | E-20 | 第二实现/调用点 |
| R9 落盘授权 | false-defer ≤20%，unresolved ≤10%，审计可追 | 一个 mutation class 实现；20–50 样本 | 概念 | 实现；标签 |
| R10 离线 SHACL | 负例 100% 检出、干净误报 ≤5%、三态可报 | 负例集；派生 vs 手写；CI | E-20 | 派生 shapes 质量 |
| R11 OBDA | 查询结果与手写 SQL 一致；有/无本体消融可解释 | 映射/本体/查询集；SQL 日志 | E-20 | agent 集成/规模 |
| R12 受监管 | citation ≥0.95、strict-pass 违规 0、签核可追 | 20–50 单；citation/state/签核 | Grid | 真实运营商/客户指标 |

**怎么用**：每条期待对应一个 stop line；先量「支持它需要的数据」那一列，量不出来就停在这一步，不要用「平均收益」替代。


<a id="12-与另外两份交付物的关系"></a>
## 6. 关系与维护

### 6.1 与另外两份交付物的关系

| 交付物 | 回答 | 读者 | 形态 |
|---|---|---|---|
| [01 现状](../01-capability-status/README.md) | 今天能做成什么、不能承诺什么 | 决策者/工程负责人 | 判断 + 矩阵 |
| [02 工程实施](../02-engineering-playbook/README.md) | 拿本体做某件事，具体怎么做 | 工程负责人/架构师 | 步骤 + 接口 + 验收 |
| [03 机制参考](../03-mechanism-reference/README.md) | 为什么是这些位置/形态，证据边界在哪 | 架构师/研究者 | 参考 + 边界 |

**一句话**：01 告诉你「值不值得做」，02 告诉你「怎么做」，03 告诉你「凭什么这么说、说到哪为止」。


### 6.2 附录

- [A · 接口总表](appendices/interfaces.md)：R0–R12 的字段、三态、版本。
- [B · 追溯表](appendices/traceability.md)：R → E → mechanism → 边界；与 01/03 的 crosswalk。
- [C · 端到端示例](appendices/case.md)：示意走查，不是部署。
- [recipes/](recipes/README.md)：13 条完整配方。
- [operations/](operations/ledger.md)：账本、评测、成本、上线、领域。

### 6.3 维护

- 本页是 02 的门厅；新增/修改 recipe 先改 `recipes/`，再回本页索引。
- 任何新判断先回 `topics/` 的 claims/E；02 不新增 E。
- 每次改动后跑 `python3 meta/tools/check_repo.py`；坏链不提交。
