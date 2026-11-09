# ai_dev_harness_ontology

**研究 harness。本体是研究它的切口，不是目的。**

这个仓库不是一次性成文的文档，而是一条**持续运转的消化流水线**：材料进来 → 精读成卡 → 沉淀成主题 → 抽成交付物。本页只做 **router**；判断在 topics，材料在 src，方法在 meta。

---

## 0. 路由

| 想知道 | 去 |
|---|---|
| 研究问题与假设 | [THESIS](./THESIS.md) |
| 六派地图、子主题、三轴 | [topics/README](./topics/README.md) |
| 跨主题结论（E-xx） | [topics/conclusions](./topics/conclusions.md) |
| 时刻 / 接缝 | [topics/seams](./topics/seams.md) |
| 控制回路七部件 | [topics/00-harness](./topics/00-harness/README.md) |
| 材料、卡、消化 | [src/README](./src/README.md) |
| 落地成本 / 可行性 | [topics/06-measure/feasibility](./topics/06-measure/feasibility/README.md) |
| 交付物 | [deliverables](./deliverables/README.md) |
| 实验设计 | [experiments](./experiments/README.md) |
| 写作约定与模板 | [meta/](./meta/) |
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

一级目录不套 `docs/`：**目录名即地图**。前三个是流水线，后三个是支撑。

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
| [`src/`](./src/) | 一篇一目录：PDF + `paper.md` / `references.md` / `appendix.md` + `card.md` + `digest.md` + `figures/` | 原文落盘 + 三份 MD 齐 + digest 有 `quality` |
| [`topics/`](./topics/) | 按六派沉淀；派 README 是地图，子主题 README 是 dashboard | 结论带等级，冲突显式保留，gap/next 可见 |
| [`deliverables/`](./deliverables/) | 手册、Deck、图等对外物 | 每条可反查回 topics |

支撑目录：`experiments/`（实验设计，实现放仓库外）、`adr/`（结构决策）、`meta/`（约定与模板）。

**三条规矩**：单向不可反向（deliverables 只从 topics 抽）；上游可以领先下游；每级自带台账。

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

六派是 **4+1+1**：`01-04` 回路内，`05` 回路前，`06` 回路外。底座是 [00-harness](./topics/00-harness/README.md)（控制回路七部件）。四轴说明、边界规则、强度谱见 [topics/README](./topics/README.md)；形态轴见 [execution-forms](./topics/execution-forms.md)。

## 4. 当前状态

- `src/` — 22 个论文目录（20 基础 + 2 扫描）；每目录 PDF + 三份 MD + `card.md` + `digest.md` + `figures/`；4 个开源项目（已 pin commit、已消化）；1 张材料卡 + 一本合并后的 [manifest](./src/papers/manifest.md)。
- `topics/` — 六派成文；17 条已核 + 2 条推测 + 3 条存疑 + 4 条冲突；26 个来源里 **9 篇把本体当被测变量并测了执行效果**，其余是机制/评测/边界证据（见各卡 `evidence_role`）。新增 [execution-forms](./topics/execution-forms.md) 形态轴。
- `deliverables/` — 手册大纲 7 章。
- `experiments/` — 6 个协议，其中 3 个已冻结为试点（EXP-004/005/006）；**D0 资产门未签核，暂不可开跑**。

**最大空缺是没有一条结论被独立复现。** 全审结论是「内部可签 / 对外 no-go」；当前真正的瓶颈是 [D0 外部资产](./meta/state.md)（具名域、日志、题库、人、单价），不是再读论文。部署层回报、false-veto/false-defer、维护成本仍缺量化。

自检：`python3 meta/tools/check_repo.py`（链接、枚举、ID、清单、计数；见 [ADR 0005](./adr/0005-repo-self-check.md)）。

## 5. 怎么增长

- 材料 → `src/README`：一篇一目录；先转 MD（正文/参考文献/附录），再建卡、消化。
- 子主题 → [meta/subtopic-template](./meta/subtopic-template/README.md)：README 是 dashboard；findings / frontier / mechanism 分文件。
- 派 → [meta/topic-research-protocol](./meta/topic-research-protocol.md)：README 是地图；claims / sources / frontier 各司其职。
- 交稿 → [meta/checklist](./meta/checklist.md)。

**不要做的**：不把 findings 堆回 README；不为「看起来完整」建空文件；不在 deliverables 里新增判断。
