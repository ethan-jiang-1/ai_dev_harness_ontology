# ADR 0011：源位阶与术语基线——规范性先于判断

- 日期：2026-11-11
- 状态：接受
- 关联：[CHARTER §4](../CHARTER.md#4-素材准入material-gate)、[ADR 0010](./0010-three-layer-information-flow.md)

## 背景

三件事暴露的是同一个错误——**先有词，后有源**：

1. `GLOSSARY.md` 30 个词，没有一条标「借来的还是自造的」。「本体」「接地」「成熟度」看起来像行业词，定义却是本仓库私义。
2. `K0–K4` 把一篇论文的五个实验条件写成「知识层级」，还叠加了论文没测的扩展（[provenance 笔记](../deliverables/_plans/2026-11-11-k-ladder-provenance.md)）。
3. EKGF 成熟度模型：组织是真的（OMG 社区），材料不是标准，讨论时却按「行业标准」对待。

结构可以留（六派、子主题、`E-xx` / `L-xx` 编号、四个交付目录都不动），要换的是**定义、锚点，以及被标准推翻的局部判断**。

## 决策

1. **新增源位阶字段** `standing: normative | informative`，只用于 `src/` 卡。
   - `normative`（规范性）：可以定义术语、定合格性、定「什么算对」。标准、规范、权威本体。
   - `informative`（资料性）：只能举例、给数据、给反例；不能定义词，不能单独撑跨组织 `E`。
   - `signal` 不作为 standing 取值，仍由 `admission` 管（只进 `frontier`）。

   术语取自 ISO/IEC Directives, Part 2 §3.2 的 normative / informative element（"sets out provisions" vs "additional information intended to assist the understanding or use"）。`已核`（2011 版文本，见 `meta/sources` 记录；现行版条款号 `待核`）。中文对应 GB/T 1.1 的「规范性要素 / 资料性要素」，不另造「主干 / 支持」。

2. **三条硬规矩**：
   - 术语定义只能引 `normative` 源；`informative` 只能佐证。
   - 自造词必须标 `local`，交付物首现处给定义，不得写成「业界 / 标准」。
   - 标准卡只能定词与合格性，**不能用来撑效应量**（「本体提升 agent 效果」仍要论文或实验）。

3. **术语条目加三字段**：`origin`（`standard` / `academic` / `local`）、`anchor`（URL#条款；local 写 `—`）、`scope`（能推什么、不能推什么）。

4. **可见的分层**：`topics/<派>/sources.md` 分 N（规范性）/ I（资料性）/ S（线索）三段；claims 编号不变，但定义性表述必须指到 N 源。

5. **偏移判定**：30 词差异表，判定分 `aligned` / `narrower` / `broader` / `divergent` / `local`。`divergent` 与「冒充行业词的 local」合计超过 1/3，就停，回到重定基调，而不是继续补卡。

6. **批次**：A 词根（ISO/IEC 21838 系列、OMG ODM、OMG Commons）→ B 领域（GB/T 42131、FIBO、HL7 FHIR、GS1 EPCIS、IOF）→ 差异表 v1 → 试点 `06-measure` → 全库。

## 备选与否决

- **自造「主干 / 支持」**：否决。这会重复我们正在纠正的错误——用一个新私词替代可引用的标准词。
- **只建标准目录、不碰术语**：否决。目录不解决「词被私义占用」；读者仍会把私义当共识。
- **把标准卡当证据**：否决。标准定词与合格性，不提供效应量。

## 后果

- 30 个词要重审；部分 `L` / `E` 换锚、降级或撤回。
- 交付物置换延后到并行整改落地后；先动 `src/`、`meta/`、`GLOSSARY`。
- 成本：A 批 3 张卡 + 差异表 v0；B 批 5 张卡 + 差异表 v1。
- `check_repo` 后续可加 `standing` 缺失检查（本轮不加，避免与并行整改冲突）。

## 什么会推翻

- 差异表 `divergent` 占比 > 1/3：说明方向偏得比修补能覆盖的多，应重定基调，而不是继续补卡。
- 标准条款无法公开核到（付费墙）：该词降为 `academic` 或 `local`，不硬挂 `normative`。
- 如果 `standing` 在实践中退化成「重要性排序」（例如拿它给论文排座次），说明字段定义失败，应改回只用于标准卡。
