# ai_dev_harness_ontology

**研究 harness。本体是研究它的切口，不是目的。**

这个仓库不是一次性成文的文档，而是一条**持续运转的消化流水线**：材料进来 → 精读成卡 → 沉淀成主题 → 抽成交付物。本页只做 **router**；判断在 topics，材料在 src，方法在 meta。

> **先读宪章**：[CHARTER](./CHARTER.md)。这是研究档案，不是软件项目；我们消化、组织、研究资料，交付物是文档，不是可运行系统。
>
> **2026-11-11 证据重置**：宪章 §4 素材准入已生效——论文 28→10、9 条 E 撤回。只有 `admitted`（含 probation）材料能撑 E/L/交付物；`signal` 只进 `frontier`；源撤回后，引用它的判断同步失效。入口：[CHARTER §4](./CHARTER.md#4-素材准入material-gate) · [状态页](./deliverables/_plans/2026-11-11-status.md) · [术语基线 v0](./meta/term-baseline.md)。

---

## 0. 路由

| 想知道 | 去 |
|---|---|
| **宪章（最高约束）** | **[CHARTER](./CHARTER.md)** |
| 研究问题与假设 | [THESIS](./THESIS.md) |
| 术语（动笔前对齐） | [GLOSSARY](./GLOSSARY.md) |
| 六派地图、子主题、四轴 | [topics/README](./topics/README.md) |
| 规范主干（N/I/S） | [topics/trunk](./topics/trunk.md) |
| 跨主题结论（E-xx） | [topics/conclusions](./topics/conclusions.md) |
| 时刻 / 接缝 | [topics/seams](./topics/seams.md) |
| 执行形态（第四轴） | [topics/execution-forms](./topics/execution-forms.md) |
| 结构决策（为什么长这样） | [adr/README](./adr/README.md) |
| 控制回路七部件 | [topics/00-harness](./topics/00-harness/README.md) |
| 材料、卡、消化 | [src/README](./src/README.md) |
| 落地成本 / 可行性 | [topics/06-measure/feasibility](./topics/06-measure/feasibility/README.md) |
| 交付物 | [deliverables](./deliverables/README.md) |
| 写作约定与模板 | [meta/README](./meta/README.md) |
| 当前计数与阻塞 | [meta/state](./meta/state.md) |
| 素材准入（G1–G5） | [CHARTER §4](./CHARTER.md#4-素材准入material-gate) |
| 术语基线 v0 | [meta/term-baseline](./meta/term-baseline.md) |
| 证据重置状态 | [meta/2026-11-11-status](./deliverables/_plans/2026-11-11-status.md) |
| 第一次接触（人，10 分钟） | [START](./deliverables/START.md) |
| 质量口径 / 最新评分 | [rubric](./meta/deliverable-quality.md) · [review](./deliverables/_plans/2026-11-11-quality-review.md) |
| 按需加载 | [meta/loading](./meta/loading.md) |

## 1. 一句话问题

模型能力外溢之后，同一模型在同一任务上仍然拉开差距——差距不在模型，在模型外围那一圈工程：上下文怎么给、状态怎么存、动作怎么放行、结果怎么验、过程怎么看得见。这一圈就是 **harness**。

本体在这个语境里反复被提起，但多停在「把业务语义注入提示词」。本仓库追问更靠工程的一层：

> **本体在 harness 的控制回路里，究竟以什么形式被执行？**

三条工作假设（2026-11-09 拆成可分别检验的子命题；细节与反驳条件见 [THESIS](./THESIS.md)）：

| # | 假设 | 若成立意味着 |
|---|---|---|
| P1a | 本体的价值在**约束与控制**；用准确率度量会低估它 | 「上本体提准确率」类论证应被降权 |
| P1b | **薄语义层**（命名/单位/槽位）先起量，深度结构的边际更小 | 先对齐词汇与单位，再谈本体深度 |
| P1c | 注入增益是**任务形态的函数**，不是普遍常数 | 不承诺跨域准确率增益 |
| P2 | **位置/形态**改变本体效果；不存在位置无关的收益 | 本体工程不能脱离 harness 单独立项 |
| P3a | 判定质量是**权衡**——漏检/误报/审批此消彼长 | 不存在单一向优的判定器 |
| P3b | 不存在单一向优的**本体来源** | curated / LLM / 数据挖掘各有偏向 |

## 2. 目录 = 流水线

一级目录不套 `docs/`：**目录名即地图**。前三个是流水线，其余是支撑。

```
   源头池               主题沉淀            对外抽取
 ┌──────────┐      ┌──────────┐      ┌──────────────┐
 │  src/    │ ───▶ │ topics/  │ ───▶ │deliverables/ │
 │原文/分解 │      │ 深度研究 │      │     交付     │
 └──────────┘      └──────────┘      └──────────────┘
  PDF/card/digest     结论可被引用       只抽取不新增
```

| 工位 | 职责 | 完成信号 |
|---|---|---|
| [`src/`](./src/) | 一篇一目录：PDF + `paper.md` / `references.md` / `appendix.md` + `card.md` + `digest.md` + `figures/`（有图才建） | Agent 不读原文能取用事实/锚点 |
| [`topics/`](./topics/) | 按六派沉淀；派 README 是地图，子主题 README 是 dashboard | 结论带等级，冲突显式保留，gap/next 可见 |
| [`deliverables/`](./deliverables/) | 手册、Deck、图等对外物 | 读者不打开 topics 能完成任务；细节可链 |

支撑目录：`adr/`（结构决策）、`meta/`（约定与模板）。

**三条规矩**：单向不可反向（deliverables 只从 topics 抽）；上游可以领先下游；每级自带台账。

**2026-11-11 起加一条硬约束**：只有 `admitted`（含 probation）材料能撑判断；`signal` 只进 `frontier`；源撤回后，引用它的 E/L/交付段落同步失效。细则见 [CHARTER §4](./CHARTER.md#4-素材准入material-gate)。

### 2.1 三层信息流：各写给谁

> 三层不是“三套深浅”，是**三种读者**。细则见 [ADR 0010](./adr/0010-three-layer-information-flow.md)。

| 层 | 读者 | 写什么 | 不写什么 | 完成信号 |
|---|---|---|---|---|
| [`src/`](./src/) | **Agent** | 干货：思想、工程实践、事实、数字与条件、代码锚、失败模式；digest 自包含 | 面向人的导读、路线图、总结陈词 | Agent 不读原文就能取用一条事实/锚点 |
| [`topics/`](./topics/) | **Agent + 人** | 组织话题：findings、compare、mechanism、frontier；把 src 压成判断、对照、边界 | 最终交付文案、通俗导读 | 同一话题的判断/边界/缺口可查 |
| [`deliverables/`](./deliverables/) | **人** | 通俗、按任务组织；把 topics 消化成读者能照着做/判断的文档；细节可链 topics | 让读者自己拼 topics；内部术语堆叠 | 读者不打开 topics 也能完成任务；要细节时知道去哪 |

**一条链**：`src` 是原料，`topics` 是加工，`deliverables` 是成品。成品不要求读者回原料；可以给“细节/出处”链接，但**主路径必须自包含**。

## 3. 六派

`topics/` 按**本体凭什么起作用**分六派；目录名本身就是问题：

| 派 | 回答的问题 | 核心工程思想 |
|---|---|---|
| [01 约束](./topics/01-constraint/README.md) | 怎么不让它做错事 | 安全是结构问题：问「存在可逆序列吗」 |
| [02 判定](./topics/02-judgment/README.md) | 怎么知道它做错了 | 判据必须外部且可度量 |
| [03 知识](./topics/03-knowledge/README.md) | 怎么让它知道得对 | 投影 pooled 最高但非普适；编译只省预算、准确率 neutral |
| [04 状态](./topics/04-state/README.md) | 怎么让它记得对 | 记忆是状态不是集合 |
| [05 生产](./topics/05-produce/README.md) | 本体从哪来、怎么修 | 来源影响可信度（推测）；精化比新建常见（推测） |
| [06 测量](./topics/06-measure/README.md) | 它到底有没有用 | 答对≠内部有本体；失败多归工作流 |

> 下表只做索引；“核心工程思想”以各派 README 为准，本页不复述细节。

六派是 **4+1+1**：`01-04` 回路内，`05` 回路前，`06` 回路外。底座是 [00-harness](./topics/00-harness/README.md)（控制回路七部件）。四轴说明、边界规则、强度谱见 [topics/README](./topics/README.md)；形态轴见 [execution-forms](./topics/execution-forms.md)。

## 4. 当前状态

- `src/` — **10 个论文目录**（6 `admitted` + 4 `admitted (probation)`；18 篇按 [准入审计](./meta/audits/2026-11-11-source-purge.md) 移出）；每目录 PDF + 三份 MD + `card.md` + `digest.md`；8 个开源项目（已 pin commit、已消化）；9 张材料卡（1 张 HN + 8 张在役标准卡）+ [manifest](./src/papers/manifest.md)。
- `topics/` — 六派成文；27 条 E（**14 已核原文 + 2 已核代码 + 2 推测 + 9 已撤回**）、3 条 Q、4 条冲突；10 篇论文 + 8 个开源里，**3 个 execution-test / 11 个 mechanism-only / 4 个 harness-evidence / 0 个 boundary-ruler**；8 个开源项目提供代码级机制证据。新增 [execution-forms](./topics/execution-forms.md) 形态轴。
- `deliverables/` — 4 个子目录（3 层 + 1 条生命周期）：[01 现状](./deliverables/01-capability-status/README.md) / [02 工程实施](./deliverables/02-engineering-playbook/README.md) / [03 机制参考](./deliverables/03-mechanism-reference/README.md) / [04 建用治](./deliverables/04-ontology-in-production/README.md)；03 内含[约束强度谱长版附录](./deliverables/03-mechanism-reference/appendix-constraint-spectrum.md)。原 7 章书稿计划已废弃，没有独立 handbook。

**2026-11-11 证据重置**：18 篇论文 + 3 个旧网页材料移出，9 条 E 撤回；主题页/交付物里仍有段落按被删源写成，重写完成前不得作为结论。这是当前第一优先级。

**最大空缺是没有一条结论被独立复现。** 这是研究深度的缺口，不是阻塞：外部客户试点线已于 2026-11-09 删除，不再请求任何域/日志/题库/人/单价。当前可自主推进的是代码级执行证据与 digest 消化；不设实验；若未来要做验证，在仓库外做并只留指针。部署层回报、false-veto/false-defer、维护成本仍缺量化。

以上摘要数字以 [meta/state](./meta/state.md) 为准。自检：`python3 meta/tools/check_repo.py`（文件链/锚点、枚举、ID、清单、计数；见 [ADR 0005](./adr/0005-repo-self-check.md)）。

## 5. 怎么增长

本页只指路，不复制流程（流程复制一次就会漂一次）：

- 加论文/开源 → [src/README](./src/README.md) §5；登记只在 [manifest](./src/papers/manifest.md)。
- 加子主题/做扫描 → [topic 协议](./meta/topic-research-protocol.md) + [子主题模板](./meta/subtopic-template/README.md)。
- 改派判断 → 该派 `claims.md`；跨派才动 [conclusions](./topics/conclusions.md)。
- 交稿 → [checklist](./meta/checklist.md)，先跑 `python3 meta/tools/check_repo.py`。

**不要做的**：不把 findings 堆回 README；不为「看起来完整」建空文件；不在 deliverables 里新增判断。
