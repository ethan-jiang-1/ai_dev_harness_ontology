---
status: draft
reading: 已消化
provenance: 综述转述
updated: 2026-11-07
source: ../source/weixin-laoliu/otology.md
author: 刘焕勇（老刘说NLP）
published: 2026-11-04
updates: []
---

# 深夜总结：近期本体 ontology 的 4 个方向、20 个工作索引

## 它主张什么

1. 近期本体研究可分四类：**当判定器/约束层**、**构建与生成**、**机制/评测/反例**、**当记忆/自演化骨架**。
2. 其中「本体当判定器」这一支的重心不是「本体有用」，而是**判定器本身的质量**（漏检 vs 误报）。
3. 给「上本体就提准确率」提供了一个直接反例（强检索 harness 下结构化工件无增益）。

## 证据强度

- 一手还是转述：**二手综述**。作者对 20 篇各给一段判断，未做交叉验证。
- 有数据吗：只有转述的数字，无独立实验。
- 结论强度：作为**索引**极有价值（20 个 ID 全部有效、标题准确）；作为**结论**必须逐篇回原文。

> 已核：20 篇 ID 有效、标题与 PDF 首页一致（2026-11-07）。见 [manifest](../source/papers/manifest.md)。

## 四个方向（附本仓库判断）

> 下表的「综述可信度」只表示综述这段转述的可靠度，**不代表本仓库卡片的阅读级别**；20 张论文卡均为 `reading: 摘要级`、`provenance: 原文摘要`。

### 1 · 本体当判定器 / 约束层（6 篇）

| 论文 | 一句话 | 综述可信度 |
|---|---|---|
| [What Does an Ontology Catch?](./papers/2610.37809-what-does-an-ontology-catch.md) | 把 checker 本身当研究对象；三种本体来源在漏检/误报上各有权衡 | 摘要已读 |
| [OA-RAG](./papers/2610.36335-oa-rag.md) | 强制输出所用证据 + 接地等级（entailed/supported/related/unrelated） | 摘要已读 |
| [POLAR](./papers/2610.08082-polar.md) | 两层本体给工具调用打可逆性分，低于阈值执行前剪掉 | 摘要已读 |
| [Commit Boundary](./papers/2610.37407-commit-boundary.md) | 区分「推理可用证据」与「有权授权持久化变更的证据」 | 摘要已读 |
| Agentic Power System Studies | 电网规划：本体承载法规标准，数字由求解器算，答案须引用证据 | 转述 |
| Ontology-guided multi-agent diagnosis | 多 agent 差分诊断，缺证据时主动追问 | 转述 |

**本仓库判断**：这一组不是本体研究，是**接缝研究**——每篇都在回答「本体被放在回路的哪一格」。归位到 [topics/README.md](../topics/README.md)。

### 2 · 本体构建与生成（5 篇）

| 论文 | 一句话 | 综述可信度 |
|---|---|---|
| OntoDoc | 四阶段多 agent 为任意 IRI 生成说明，完整性较基线 +12% | 转述 |
| Peeling the Matryoshka | MRL embedding 前缀维度与 taxonomy 粒度对齐，冻结 embedding 上训探针 | 转述 |
| ReX-GG | LLM 集成 + 结构化输出 + 匿名互评做关系抽取，关系类型由本体定义 | 转述 |
| CASTON Refinement | 既有本体的精化，不是从零建 | 转述 |
| SFE-O | 超临界 CO₂ 萃取域 OWL 本体，显式表达参数溯源 | 转述 |

**本仓库判断**：回答「本体从哪来、怎么修」，归位到 [topics/05-produce/lifecycle.md](../topics/05-produce/lifecycle.md)。其中「已有本体怎么修」被文献系统性低估。

### 3 · 机制、评测与反例（4 篇）

| 论文 | 一句话 | 综述可信度 |
|---|---|---|
| [Before Blaming the LLM](./papers/2610.35267-diagnose-workflow.md) | 失败归因到工作流：输入不足、接地弱、模板缺口、校验弱、非局部修复 | 摘要已读 |
| [Solver-Like Behavior](./papers/2611.02395-solver-like-behavior.md) | 形式化器自己在轨迹里把答案算出来；冗余且会继承错误 | 摘要已读 |
| [Context as Infrastructure](./papers/2610.41172-context-as-infrastructure.md) | 强 harness 下（仅 BM25+grep）结构化工件无可检出增益 | 摘要已读 |
| MIOE | 本体预测机制上可干预，但知识无法与类别信息干净分离 | 转述 |

**本仓库判断**：这一组是**全仓库最重要的证据来源**——它们共同指向「差距在 harness，不在模型」。归位到 [topics/conclusions.md](../topics/conclusions.md)。

### 4 · 本体当记忆 / 自演化骨架（5 篇）

| 论文 | 一句话 | 综述可信度 |
|---|---|---|
| EvoMemState | 记忆从「事实集合」改为「状态」：关系状态 + 推理状态 | 转述 |
| [FIRME](./papers/2610.40482-firme.md) | 固定 product-topic 本体 + registry 做跨期身份对齐 | 摘要已读 |
| OntoAct | 把动作空间压到本体概念层再做假设检验 | 转述 |
| Narrow and Deep | 工业设备域建「本体塔」，窄而深 | 转述 |
| Evontree | 本体规则引导低资源域自演化 | 转述 |

**本仓库判断**：记忆是 harness 机制，本体在此充当状态结构——归位到 [topics/04-state/memory-as-state.md](../topics/04-state/memory-as-state.md)。注意 FIRME 的克制定位（不承担自由推理，只承担对齐与印证条件），这可能是同类工作里最可落地的取向。

## 转述与原文的差异

这是本仓库把 `source/` 与 `notes/` 分开的直接收益。首批 8 篇做了综述转述与原文的逐条对照，其中 3 篇的转述**丢失了限定条件**，而限定条件恰好决定结论可否被引用。其余 12 篇在后续建卡时补读了摘要，但未逐条对照综述。

| 论文 | 综述的转述 | 原文的限定 | 影响 |
|---|---|---|---|
| POLAR | 「本体用在安全护栏而非知识注入，比多数本体+RAG 更硬」 | 18 个模型-域组合中仅 8 个改善；retail 与更强模型常回退；明确声明「reward 不是防止伤害的直接度量」 | 这是**权衡证据**，不是成功案例。直接支撑 P3，削弱「剪枝必然更好」 |
| Commit Boundary | 平铺描述三段式放行机制 | 明确自述「**无实现、无实证验证**的概念架构」；保证是条件性的 | 只能作**设计提案**引用，不能作证据 |
| Context as Infrastructure | 「编译解决上下文预算而非检索准确率」 | 无增益的结论限定在 **FRAMES**、针对结构化工件；PageIndex 式大纲在 FRAMES 规模上反而退化；85%/91% 两个基准数字作者自己声明不可比 | 引用时必须带范围，否则会变成过强断言 |

另有两处待核：

- **FIRME**：综述称「本体只承担槽位定义、不做推理」；[FIRME 卡](./papers/2610.40482-firme.md)已修正为「不承担自由推理，只承担对齐与印证条件」。原限定待回正文核对。
- **MIOE**：综述归入「机制」方向，但其结论是**削弱**「模型内在本体」的强主张（答对不等于内部有结构）。分类掩盖了结论方向。

## 它的局限

1. **无一手验证。** 20 段判断都是作者对摘要的转述，且部分转述削弱了原文的条件。
2. **分类掩盖强度差异。** 「方向」按主题分，不按证据强度分——同一方向里既有实证工作，也有纯概念提案。
3. **聚焦「本体做了什么」。** 几乎不问「本体没起作用时是哪里出了问题」，而后者对 harness 研究更有价值。

## 待核项

- [ ] 逐篇读正文，补齐「未测范围」与「数字」两栏
- [x] 确认 FIRME 的「不做推理」限定（已修正为「不承担自由推理，只承担对齐与印证条件」；原文措辞待核）
- [ ] 确认 MIOE 结论的适用范围（是否只在小模型上成立）

## 喂到哪个主题

- [tool-gate](../topics/01-constraint/tool-gate.md) ← POLAR
- [commit-boundary](../topics/01-constraint/commit-boundary.md) ← Commit Boundary
- [checker](../topics/02-judgment/checker.md) ← What Does an Ontology Catch
- [evidence-grading](../topics/02-judgment/evidence-grading.md) ← OA-RAG
- [memory-as-state](../topics/04-state/memory-as-state.md) ← EvoMemState、FIRME
- [projection](../topics/03-knowledge/projection.md) ← Narrow and Deep
- [compilation](../topics/03-knowledge/compilation.md) ← Context as Infrastructure
- [topics/05-produce/lifecycle](../topics/05-produce/lifecycle.md) ← CASTON、SFE-O、OntoDoc
- [topics/00-harness/context](../topics/00-harness/context.md) ← Context as Infrastructure
- [topics/conclusions](../topics/conclusions.md) ← 全部
