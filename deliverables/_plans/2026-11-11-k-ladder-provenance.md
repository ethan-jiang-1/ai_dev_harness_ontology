---
status: draft
type: work-note
updated: 2026-11-11
target: deliverables/01-capability-status
scope: terminology-provenance
---

# K0–K4 是谁定义的？——术语来源核查

> **一句话**：K0–K4 是 **Narrow & Deep 一篇论文自己的五个累积实验条件**（Joo & Kim, arXiv:2610.11768, 2026-10-08），不是行业标准，也不是本体成熟度模型。我们此前把它写成「知识层级」，又给 K1 加了「别名/槽位」、给 K2 加了「固定分节/整塔」，这三处是**我们的工程扩展**，不是论文测到的东西。本笔记记录核查过程与修正决定。

## 1. 问题

01 的读者一进来就遇到 K0/K1/K2；有人问「K3 呢」「这是谁定的」「有共识吗」。需要回答：

1. K0–K4 的原始定义在哪、作者是谁、有没有被采用？
2. 业界有没有一个公认的「知识层级/本体成熟度」阶梯可以替代？
3. 如果没有，01 应该怎么用这些编号，才不把「一篇论文的实验条件」冒充成「行业共识」？

## 2. 结论

1. **K0–K4 是论文自用的实验条件编号。** 论文 Table 1 的标题是 "Knowledge conditions of the evaluation"；§2.8 写 "five cumulative conditions, K0 to K4"。K 是条件编号；论文称这一组为 knowledge conditions，但没有单独解释字母缩写。不是 knowledge level。`已核`（原文）
2. **它不是标准，也没有形成共识。** 截至 2026-11-11，OpenAlex 记录为 preprint、`is_published: false`、`cited_by_count: 0`；作者 2 人（韩国能源研究院/UST）；没有标准组织、没有第二来源，也未见同行评议版本。`已核`（OpenAlex 快照；引用数会变）
3. **「没有第二来源」是检索判断，不是穷尽证明。** 仓库内只有 N&D 一篇用这套 K；公开检索也没有发现同一套 K0–K4。`推测`（检索非穷尽）
4. **K 记号在相邻文献里已经撞车。** 2026-05 的 *Knowledge Operations: A Capability Model for AI Systems* 用 **K0–K6** 表示七种「知识操作原型」（retrieving / scoping / interpreting / combining / computing / traversing / orchestrating），与 N&D 的「供给条件」不是一回事。`已核`（Zenodo 记录）
5. **真正有共识的是「点位元数据」这一层，不是 K 阶梯。** tag 名、单位、质量码、量程在 OPC UA、IEC 61360 / AAS 里是标准字段；但「K1」这个编号不是。`已核`（规范）
6. **因此：01 保留 K 只作回查标签，正文用人话名字。** 数字（+54.6pp / +19.8pp）仍然只属于 N&D 的单工厂、9 任务实验；不因为编号被正名而变成普遍规律，也不因为作者不出名而失效。`已核`（E-12 的限定不变）

## 3. 原始定义：论文到底写了什么

出处：Joo, Y.; Kim, S. *Narrow and Deep: An Ontology Tower as the Knowledge of an LLM Agent for an Industrial Equipment System.* arXiv:2610.11768, 2026-10-08. Table 1（p.11）+ §2.8。

| 论文代号 | 原文 "What the agent receives in addition" | 原文知识位置 | 人话 |
|---|---|---|---|
| **K0, address level** | PLC addresses and raw integer values only | Bindings without names | 只有 PLC 地址和原始整数；没有 tag 名 |
| **K1, tag level** | Tag names, units, and quality flags, as on the plant's display | Tags | 现场显示上的 tag 名、单位、质量码 |
| **K2, structured knowledge** | The text projected from the tower (Section 2.5) | Tag attributes, couplings, envelopes, and knowledge nodes with the incorporated lessons; **no derived quantities** | 从塔投影出的约 45k 字符文本；**不含 16 个推导量与假设** |
| **K3, procedural** | Summaries of the six operating workflows | None (outside the tower) | 六个操作流程的摘要；在塔外 |
| **K4, experiential** | A search tool over the operating journal and investigation documents | Journal records (outside the tower) | 日志/调查文档的检索工具；在塔外 |

变体（同一张表）：

| 条件 | 改了什么 | 用途 |
|---|---|---|
| **K4x** | K4 去掉本事故记录 | H3 的操纵条件；K4 0.644 vs K4x 0.645（element score，4 个诊断任务） |
| **K2-sub** | 用工厂文档检索替代投影 | 比较「投影文本」和「文档检索」 |
| **K3-sub** | 用完整流程文本替代摘要 | 预注册条件之一 |
| **Scrambled-order** | 投影文本句序打乱 | 顺序是不是有效成分 |
| **K2-json** | 整塔 JSON（含推导量/假设，约 99k 字符） | 事后描述性比较；不是 1,304 预注册批次 |
| **K2-tool** | 三个塔查询工具（查节点/边/假设） | 事后描述性比较；明确不在 1,304 预注册批次 |

## 4. 我们此前的三处过度外推

| 我们写过的 | 论文原文 | 问题 | 修正 |
|---|---|---|---|
| K0 =「地址级标签：tag 名、点位、原始字段」 | K0 只有 PLC 地址 + 原始整数，**没有 tag 名** | 自相矛盾；把 K1 的东西塞进 K0 | 改成「原始点位：PLC 地址 + 原始整数，没有 tag 名」 |
| K1 =「名字 + 单位 + 别名 + 槽位对齐」 | K1 = tag names, units, quality flags | 别名/槽位是我们的工程扩展，论文没测；不能算进 +54.6pp | 正文写「tag 名/单位/质量码（论文 K1）」；别名/槽位另标「工程扩展」 |
| K2 =「整座塔投影 / 固定分节文本」 | K2 = 从塔投影出的文本（prose + structured blocks），**不含推导量** | 「整塔」错（漏了推导量）；「固定分节」是我们的建议，原文只说 prose + structured blocks | 改成「知识投影文本（不含推导量）」；固定模板另标「工程建议」 |
| K3/K4 被略去，读者以为 K2 是最后一层 | 论文还有 K3/K4，但增益小、探索性 | 读者看不到「为什么 01 停在 K2」 | 新增 K 页，完整列出 K3/K4 与停止理由 |

## 5. 业界有没有共识？相邻框架各量什么

检索到的「成熟度/层级」框架都不是「agent 拿到什么知识」的阶梯：

| 框架 | 它量什么 | 为什么不能直接替代 |
|---|---|---|
| **DIKW**（data → information → knowledge → wisdom） | 抽象程度 | 概念层级，没有工程判据；常被批评为不可操作（Frické 2009） |
| **Ontology Maturity Model**（Obrst 2009） | 组织从术语表/词表迁移到本体驱动企业的过程，仿 CMM | 组织/流程成熟度，不是单次任务的知识供给 |
| **EKG Maturity**（EKGF） | 企业知识图谱采纳的 5 级（试点 → 企业平台 → 战略基础设施） | 组织能力/治理，不是 agent 输入 |
| **Ontology Spectrum**（Uschold & Grüninger 1996） | 表示形式：词表 → 弱/强本体 → 逻辑约束 | 表示形式，不是知识内容多少 |
| **Semantic Web layer cake** | 表示语言栈：RDF → RDFS → OWL → logic | 语言栈，不是供给形态 |
| **ISA-95 Levels 0–4** | 制造活动层级：物理过程 → 传感器/执行器 → PLC → MOM → ERP | 数字像，轴完全不同；最容易被误读 |
| **OPC UA / IEC 61360 / AAS** | 点位元数据：tag/信号名、工程单位、量程、质量码、语义 ID | **这是 K1 内容的行业锚**，但它不定义 K 阶梯，也不含 K2–K4 |

> 结论：**有共识的是「点位元数据字段」，不是「K0–K4 阶梯」。** 把 K1 的内容说成「OPC UA/IEC 61360 里的 tag/单位/质量码」是稳的；把「K1」说成行业层级是不稳的。

## 6. 决定

1. **K0–K4 降级为「论文条件代号」**，只用于回查 N&D；正文优先用人话名字：
   - K0 → 原始点位
   - K1 → 点位语义（tag 名/单位/质量码）
   - K2 → 知识投影文本（不含推导量）
   - K3 → 流程摘要
   - K4 → 运行记录检索
2. **新增 01 的 [K0–K4 来源说明](../01-capability-status/sections/k-ladder.md)**，把「谁定义/是不是标准/五个条件/变体/为什么停在 K2/相邻框架」一次讲清。
3. **修正三处过度外推**：K0 不再叫「地址级标签」；K1 不再默认含别名/槽位；K2 不再叫「整塔/固定分节」。
4. **不做全仓重命名**（K→人话名字）。02/03/04 里还有大量 K 引用；本轮先改定义锚点与首用处，避免一次改动过大。若用户要求，再做一次全仓去 K。
5. **对外沟通禁用裸 K**：必须写「N&D 的 K1」或「点位语义（论文 K1）」，不能写「K1 级本体」「K2 成熟度」。
6. **与 [ADR 0011](../../adr/0011-source-standing-and-term-baseline.md) 对齐**：K0–K4 标 `local`（论文条件，不是 normative 源）；交付物首现处给定义，并加「术语基线：ADR 0011 / 2026-11」。ADR 把本笔记列为源位阶规则的触发例之一。

## 7. 改了什么

- 新增：`deliverables/01-capability-status/sections/k-ladder.md`（2026-11-11）
- 01：README 首屏/内码/目录、GUIDE、glossary、capabilities/README、map、decision-record、acceptance、canonical
- 02：glossary、README 内码、recipes/knowledge 首段、appendices/case、sections/acceptance
- 03：glossary、positions/context
- 04：glossary、body/build
- 顶层：START、根 GLOSSARY
- 计数：`meta/state.md` 的文件数随新增页 +1；`meta/state-log.md` 记一笔

## 8. 尚未做 / 可选

- **全仓去 K**：把 02/03/04 正文里的 K0/K1/K2 全部换成「原始点位/点位语义/知识投影文本」。工作量大，且会动到大量锚点与标题；本轮不做。
- **等外部标准**：如果未来有标准组织给出「agent 知识供给」的正式分级，再替换 K；目前没有。
- **论文更新**：若 N&D 有 peer-reviewed 版本并改表，K 页需跟着改；`updated` 与「最后核查」要更新。

## 9. 来源（访问日期 2026-11-11）

- 论文：Joo & Kim, arXiv:2610.11768 — https://arxiv.org/abs/2610.11768
- OpenAlex 记录（preprint / 0 citations）— https://api.openalex.org/works/https://doi.org/10.48550/arXiv.2610.11768
- Obrst, *The Ontology Maturity Model* (2009) — http://ontolog.cim3.net/file/work/OntologySummit2011/reference/ontologyMaturityModel-obrst-2009.pdf
- EKGF, *The Five Maturity Levels* — https://maturity.ekgf.org/intro/structure/levels/
- ISA-95 levels（OPC UA 规范页）— https://reference.opcfoundation.org/specs/OPC-10030/4.2.3
- OPC UA for Machinery, Process Values（SignalTag / EngineeringUnits / Status 示例）— https://reference.opcfoundation.org/specs/OPC-40001-2/v1.00/b-1
- IDTA, AAS Part 3a / IEC 61360 Data Specification（PreferredName / unit / unitId）— https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2025/06/IDTA_01003a-25-01_AAS-Specification_Part3a_Data-Specification_IEC61360.pdf
- Uschold & Grüninger, *Ontologies: principles, methods and applications* (1996) — https://doi.org/10.1017/S0269888900007797
- Frické, *The knowledge pyramid: a critique of the DIKW hierarchy* (2009) — https://doi.org/10.1177/0165551508094050
- Xydas, *Knowledge Operations: A Capability Model for AI Systems*（K0–K6 操作原型）— https://zenodo.org/records/20083456

## 10. 证据等级说明

- `已核`：直接读了论文 Table 1/§2.8、OpenAlex JSON、规范页或 PDF 原文。
- `推测`：「没有第二来源」是检索范围内的判断，不是穷尽证明；检索词与日期见上。
- 本笔记不新增 E；所有数字沿用 E-12 的限定（单工厂、9 任务、答案基本写在文本里）。

## 11. 按交付物 rubric 的局部影响

> 只评本次改动涉及的维度，不重评 01 全份；整份分数待复评。

| 维度 | 改动前 | 改动后 | 依据 |
|---|---|---|---|
| B1 入门坡道 | 首屏直接用 K1/K2，未解释 | 先讲「PLC 地址 → tag 名/单位/质量码 → 投影文本」，再引 K；K 页给完整来源 | README 首屏、K 页 §1–2 |
| B3 术语负担 | K0–K2 与 X/E/A-B-C-D 混排；K1 含未定义扩展 | K 降为回查标签；首现处给人话名字与「非标准」 | 01 内码行、glossary §4、K 页 §5/§7 |
| C3 单一真相 | 01 与 02 对 K0 的定义互相矛盾（「地址级标签」vs「无 tag 名」） | 统一到 K 页；01/02/03/04 定义锚点一致 | 各 glossary + K 页 |
| D1 证据纪律 | K 被写成「知识层级」，未标标准/论文 | 标 `local`、OpenAlex 0 引用、单工厂限定；区分论文操纵与工程扩展 | K 页 §1/§3、ADR 0011 |
| D2 引文保真 | K1 含别名/槽位、K2 叫「整塔/固定分节」 | 与 Table 1 对齐；三处扩展单独标出 | K 页 §3 |

**仍未做**：全仓去 K（见 §8）；术语差异表（ADR 0011 S3）中的 K 行由基线条目补。
