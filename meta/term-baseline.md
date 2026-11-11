---
status: draft
updated: 2026-11-11
type: term-baseline
scope: ADR 0011 §S3 v0（10 词）
---

# 术语差异表 v0：先标来源，再谈定义

> 依据 [ADR 0011](../adr/0011-source-standing-and-term-baseline.md) 与 [基线整改计划](../deliverables/_plans/2026-11-11-baseline-correction-plan.md)。**本表只做判定与动作，不新增 E/L。**
>
> **v0 范围**：先做 10 个高频词；其余 20 词待 v1。**未读标准正文的条款号一律写 `待核`**；`local` 不是“错”，是“本仓库自造/限定义”，必须首现解释、不得写成行业标准。
>
> **主干索引**：N（规范性）标准与「能/不能定义什么」见 [topics/trunk.md](../topics/trunk.md)；本表只判 10 个词的来源与动作。

## 0. 规则（与 ADR 0011 一致）

- `origin`：`standard` / `academic` / `local`；只有 `standard` 可定术语与合格性。
- 判定五类：`aligned`（换锚）/ `narrower`（标范围）/ `broader`（拆开）/ `divergent`（改名或限定）/ `local`（标自造）。
- **偏移阈值**：`divergent` + **冒充行业词的** `local` 合计 > 1/3 → 停，重定基调；本表 `local` 都显式标注，不算“冒充”。
- 标准卡只定词与合格性，不撑效应量。

## 1. 十词 v0

| 词 | 我们现在的定义 | 标准锚 | origin | 判定 | 动作 | 状态 |
|---|---|---|---|---|---|---|
| **本体** | 领域概念、关系与约束的显式规范 | ISO/IEC 21838-1（TLO 要求；条款号 `待核`） | `standard` | `broader` | 保留通用义；**顶层本体**另列标准义；领域本体标 `local`，不要拿 TLO 标准给领域塔发合格证 | v0 |
| **顶层本体** | 小、通用、不含领域词的上层本体 | ISO/IEC 21838-1/-2（BFO 为参考 TLO；条款号 `待核`） | `standard` | `aligned` | 用标准义；不要与「本体塔 / domain tower」混用 | v0 |
| **领域本体** | 面向一个领域的概念/关系/约束 | ISO/IEC 21838 **不定义**领域本体 | `local` | `local` | 标 local；首现解释；不要写成“标准认证的领域本体” | v0 |
| **知识图谱** | 实例层的事实图，区别于本体（概念层） | 本仓库无 normative 锚 | `local` | `local` | 只作描述词；不要拿它定义“本体”；要定义先引 academic/standard 源 | v0 |
| **语义层** | 把领域语义叠到数据/接口上的那一层 | 本仓库无 normative 锚 | `local` | `local` | 标 local；不与“本体”同义使用 | v0 |
| **成熟度** | 组织能力分级 | 本仓库无 normative 锚；EKGF 判 `excluded` | `local` | `local` | **禁止**写成“行业成熟度标准”；只作组织讨论词 | v0 |
| **知识层级** | 曾用来指 K0–K4 | 论文实验条件，不是标准；见 [K 页](../deliverables/01-capability-status/sections/k-ladder.md) | `local` | `local` | 改叫「论文条件」；不写“层级/等级”；**不作为术语，只作出处/回查** | v0 |
| **接地（grounding）** | 输出与本体证据之间的关系强度 | 本仓库无 normative 锚；E-03 已撤回 | `local` | `local` | 只作机制词；不引旧效应量；首现解释 | v0 |
| **数据产品** | 可交付、可治理的数据/知识产物 | 本仓库无 normative 锚 | `local` | `local` | 标 local；不要写成标准术语 | v0 |
| **约束** | 对数据/查询/动作的前置条件 | W3C SHACL（RDF 图约束；SHACL Core 为 W3C Recommendation） | `standard` | `narrower` | 标准义只到 RDF 图约束；动作前授权/闸门另标 local，不能拿 SHACL 证明“会拦动作” | v0 |

## 2. 计数与风险

| 判定 | 计数 | 备注 |
|---|---|---|
| `aligned` | 1 | 顶层本体 |
| `narrower` | 1 | 约束 |
| `broader` | 1 | 本体 |
| `divergent` | 0 | — |
| `local` | 7 | 均显式标注；**不冒充行业词**，不计入偏移阈值的“冒充”分子 |

> **v0 的结论**：10 词里只有 2 词有 `standard` 锚；其余 7 词是 `local`。这不代表“没救”，代表**它们只能作本仓库的工作词**。交付物首现处必须解释；对外文档不要把它们写成行业共识。

## 3. 与交付物的接口

- 01 的 K0–K4 已按 `local` 处理（[K 页](../deliverables/01-capability-status/sections/k-ladder.md)）；**K0–K4 本身不是术语，不列入 10 词**；本表「知识层级」行只用于回查旧说法。
- 01/02/03/04 的术语页与首现定义，按本表 v0 判定改；**只改定义段/首现/锚点，不重写结构**。
- 标准卡 `standing` 已补到 8 张 W3C/GB/T/OASIS/ODCS 卡；HN 是 `engineering`，不标 `standing`。

## 4. 待核 / 下一版

- [ ] ISO/IEC 21838-1/-2 的具体条款号（当前只到目录摘要）。
- [ ] 知识图谱、语义层、数据产品、接地：是否值得引 academic 源；若引，改 `origin` 并给 anchor。
- [ ] 其余 20 词（本体塔、接缝、执行形态、证据角色、覆盖率、失效类别等）。
- [ ] 06-measure 试点：逐条 L 检查术语用法；冲突换锚/降级，记录到 `meta/audits/2026-11-11-term-baseline.md`（待建）。

> 本表是 v0 工作稿，不是标准；引用时带「本仓库术语基线 v0」。
