---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# 3. 主体：R0–R12 与参考实现

> 本章回答：R0–R12 怎么选、开源/论文能抄什么、架构和路线怎么排。 ｜ 读完你应该能：选一条 recipe 并写出接口。

<a id="4-九条工程做法r1r9"></a>
<a id="4-十二条工程做法r0r12"></a>
### 3.1 十二条工程做法（R0–R12）

> 本节只做索引；完整配方（十字段：目标与适用 / 前提 / 接缝与形态 / 数据契约 / 步骤 / 证据 / 成本 / 验收与 stop / 失效模式 / 可抄锚点）在 [`recipes/`](../recipes/README.md)。每条 recipe 都与 E-xx 和 mechanism.md 对齐；见 [appendices/traceability](../appendices/traceability.md)。
>
> **2026-11-11 证据重置**：R4/R5/R6/R12 转 gap；当前 A=3 / B=4 / C=1 / gap=4（不含 R0 配方）。

| R | 一句话 | 接缝/形态 | 主证据 | 成熟度 | 完整配方 |
|---|---|---|---|---|---|
| **R0** | 先证明本体能被执行（名字/单位、声明、覆盖、落点） | 准入 | E-12/E-20；E-02/E-03 已撤回 | 配方 | [readiness](../recipes/readiness.md) |
| **R1** | 先把 tag 名/单位/质量码对齐（可加别名/槽位）；K1 够就停 | 供给 / context | E-12 | A | [knowledge](../recipes/knowledge.md#r1--点位语义k1先把-tag-名和单位对齐) |
| **R2** | 知识投影文本（固定分节是工程建议）；先 K1 再投影 | 供给 / context | E-12 | B | [knowledge](../recipes/knowledge.md#r2--知识投影文本把领域知识写成文本固定分节是工程建议) |
| **R3** | 只买 claim+span；先算 `p_min` | 供给 / compiled | E-08/E-14 | B | [knowledge](../recipes/knowledge.md#r3--证据编译只买-claim--逐字-span) |
| **R4** | 输出带观察与 grounding；等级要校准 | 输出时 / compiled | E-03 withdrawn | **gap** | [judgment](../recipes/judgment.md#r4--输出证据契约让答案带依据和接地等级) |
| **R5** | 先超过空结果重试；catch/FA 分开 | 输出后 / compiled | E-02 withdrawn | **gap** | [judgment](../recipes/judgment.md#r5--输出后-checker先超过空结果重试) |
| **R6** | 只在不可逆/高代价/弱模型时试；先 shadow | 动作前 / compiled | E-04/E-13 withdrawn；E-15 参照 | **gap** | [constraint](../recipes/constraint.md#r6--动作前可逆性闸只在不可逆高代价弱模型时试) |
| **R7** | 先 registry，再状态；CMR 与 precision 同看 | 跨轮 / compiled | E-05/E-17 | B | [state](../recipes/state.md) |
| **R8** | 只做可见性，不当授权；已入库单实现/ fail-open 未修 | read-path / engine | E-20 | B（条件性） | [constraint](../recipes/constraint.md#r8--读路径过滤只做可见性不要当授权) |
| **R9** | 只能设计，不能声称落地 | 落盘前 / 无实现 | E-20 | C | [constraint](../recipes/constraint.md#r9--落盘前授权现在只能设计不要声称已落地) |
| **R10** | 离线/CI SHACL；三态不可折叠 | 离线/CI / compiled | E-20 | A | [offline-and-obda](../recipes/offline-and-obda.md#r10--离线ci-shacl把没检查完做成第三态) |
| **R11** | 查询时编译；不是闸/判定器 | supply / engine | E-20 | A | [offline-and-obda](../recipes/offline-and-obda.md#r11--obda-查询重写本体在查询编译时被执行) |
| **R12** | 证据 + solver + 人签核；不是准确率项目 | 供给+输出+人 | Grid 已移出 | **gap** | [regulated](../recipes/regulated.md) |

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

> 出处：E-20 与 [execution-forms](../../../topics/execution-forms.md#代码级核对2026-11-09)。四者都是只读代码、未做对照实验；**代码能跑 ≠ 机制有效**。

**第二 read-path 实现（外部扫描线索，未入库）**：2026-11-09 定向扫描发现 [`Matdata-eu/sparql-guard`](https://github.com/Matdata-eu/sparql-guard)（Apache-2.0，HEAD `6b68d769`）：TS 写的 SPARQL 代理，用 **查询重写** 而不是返回后过滤；fail-closed、subject+object 两侧、SHACL Core 子集；有一组 vitest 用例（外部复核报告 76/76 通过，未在仓库内复跑）。它**不是**已入库证据：单作者、1★、无 harness 调用点、无泄漏率/时延测量；而且它把「read-path」拆成两种执行点（返回后过滤 vs 查询重写）。所以：**read-path 至少有两种执行点，但 seam 语义未定；01 的 B 评级不因此升级。**


### 3.3 论文/开源给的「准确指示」到什么程度

| 层级 | 能给什么 | 例子 | 能不能照抄 |
|---|---|---|---|
| 代码级 | 真实接口、调用链、失败行为 | 4 个开源项目（E-20） | 抄接口与边界；不抄效果 |
| 公式级 | 可算的盈亏平衡/代价 | 编译 `p_min = 2% + c/(0.929Q)`（E-14）；CASEL `J(m)`（E-15，`γ_m` 是假设） | 代自己的数；不抄论文的 `c`/`γ` |
| 协议级 | 判定/标注/三态 | 原 E-02/E-03 撤回；这些协议只作历史模板；promotion 七条来自已删 Commit Boundary，只作概念 | 不抄阈值；待新源再抄协议 |
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
- 每个箭头都要有数据契约；没有契约的「接缝」只是概念。逐箭头字段见 [appendices/interfaces](../appendices/interfaces.md)。
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

- 账本字段 → [operations/ledger](../operations/ledger.md)
- 噪声/样本/预注册 → [operations/evaluation](../operations/evaluation.md)
- 成本/TCO → [operations/cost](../operations/cost.md)
- 上线/回滚/审批 → [operations/rollout](../operations/rollout.md)
- 域约束 → [operations/domains](../operations/domains.md)
