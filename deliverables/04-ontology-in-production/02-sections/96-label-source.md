---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 标签来源：从哪来、怎么验、没有就停

> **给谁**：准备把列级标签/等级接进 04 的 policy 的团队。
> **回答**：04 需要的 tag/level 从哪来；怎么判断一个 label source 能不能接；没有时停在哪。
> **不回答**：怎么训练 labeler、选哪家厂商、报价。04 不提供打标算法，也不把 Glyph 当通用方案。

## 0. 一句话

04 的 fixture **假设你已经有列级 tag + level**；它不提供打标方法。没有可信来源，A.3 的 TBox 和 C.2 的 policy 都只是空转——**未标注 ≠ 不敏感**；在执行层，未标注列可能被当「无标签」放行（`推测`；E-22 的边界）。

## 1. 04 需要 label source 给什么

| 字段 | 要求 | 为什么 | 没有会怎样 |
|---|---|---|---|
| `column_id` | 稳定 IRI（库/表/列） | 和 ABox 的 `:Column` 对上 | 标签挂不到列；CQ1/CQ2 少行 |
| `tag(s)` | 一个或多个叶标签 | 多标签是常态；fixture 是单标签 | 多标签列无法判；见 [transfer §6.2](92-transfer.md#p-multitag) |
| `level` | 每个 tag 一个 1–4 | policy 的 condition | policy 没有输入；R1–R4 无法判 |

> **1–4 的工程含义（`推测`，不是标准原文）**：1=公开、2=内部、3=敏感、4=严格受限。GB/T 43697 只分三级；04 的 1–4 是「一般/重要/核心」加一档的工程映射，具体边界由 policy owner 定。
| `confidence` / `provenance` | per-tag 来源/分数/理由 | audit 的 `evidence`；复核 | 审计答不出「为什么是这个标签」 |
| `as_of` / taxonomy version | 标签/本体的版本 | replay、变更对账 | 版本漂移；审计不可回放 |
| `owner` | 谁维护标签/等级 | 出事时找谁 | 无人对漏标/错标负责 |
| `coverage` | 已标/未标列数、按表分布 | 未标列不能当安全 | 漏标列静默进结果 |
| `leak_estimate` | 独立抽样的漏标率/未标注率 | 授权链路的前置 | 「接受率」会被误当覆盖率 |

> fixture 的 1 列 1 tag 是**约定**，不是模型约束；真实标签源多为列级多标签（Glyph：`Y ⊆ O`，每 tag 带 confidence/justification）。先定多标签规则，再接 policy。

## 2. 三种来源，不是三种推荐

| 路径 | 输入/做法 | 证据 | 能做什么 | 不能做什么 | 停在哪 |
|---|---|---|---|---|---|
| **A 现成受治理目录** | 已有 catalog + tag/level + owner | 04 fixture 假设这种；无外部证据 | 直接做 coverage/leak 审计，最快接 04 | 不能假设目录完整/最新 | coverage/leak 不明 → 只做只读试点 |
| **B 买/建 labeler** | 元数据 + 可选描述 + 生产代码；不读 cell value | Glyph：单企业、275 叶、多标签、per-tag provenance；metadata F2 0.880，description 0.238，regex 0.050 | 列级多标签 + 理由；可人工复核 | 方法只在一家企业；无公开代码/本体；漏标率/OOD/成本未报告；不是插件 | 没 taxonomy/复核/覆盖率 → 不接 policy |
| **C 人工/专家标注** | 小范围、预定义 tag/level、双人标 + 裁决 | 无仓库证据；`推测` | 5–50 列的小域可做；质量可控 | 不可扩展；一致性/成本未测 | 没有双人/裁决 → 只做样本 |

**选哪条（`推测`，不是结论）**：

| 你的情况 | 更现实的路 | 为什么 |
|---|---|---|
| 已有受治理目录 + owner | A + 50 列抽检 | 最快；但必须先量 coverage/leak |
| 200+ 列、有元数据/代码、能复核 | B | Glyph 类方法；但单企业证据，不能当通用 |
| <50 列、tag/level 已定义、有人工 | C + 抽样 | 小域可控；但不可扩展 |
| 没有 owner / 没有 taxonomy | **停** | 先解决标签治理，不要先建 TBox |

## 3. 准入清单（8 问）

| # | 问题 | 为什么是硬门 | 不满足就 |
|---|---|---|---|
| 1 | 每列有 tag + level？ | policy 的输入 | 停；未标列不能当安全 |
| 2 | 多标签怎么表示/取 level？ | 真实数据多标签 | 先定 [transfer §6.2](92-transfer.md#p-multitag) 的 A/B/C |
| 3 | 已标/未标覆盖率？ | 未标 = fail-open | 先量 coverage；不要接 policy |
| 4 | 漏标率/未标注率有独立抽样？ | 授权链路最关键的 FN | 只做只读试点；不接 deny |
| 5 | taxonomy 封闭/可版本化？ | 标签空间漂移 | 先定版本；否则不可 replay |
| 6 | 输入是否读 cell value？ | 合规/敏感表前置 | 不能读值的表先用元数据/代码路线 |
| 7 | 人工复核/回写/更新周期？ | 错标/漏标要能被发现 | 没有复核 = 不可运营 |
| 8 | owner / SLA / 成本？ | 出事有人负责 | 没有 owner = 不上线 |

> **1/2 是前置**：没有 tag/level 或没定多标签规则，直接停。**3/4/5 任一为「否」→ 不要把标签接进 policy**；标签层可以先用，但只能做检索/提示，不能做 allow/deny。

**Glyph 的教训**：它的接受率是 precision-like、对 FN 盲；漏标率/未标注率/覆盖率**全文未报告**，而且是单企业、无 OOD/公开基准。所以「Glyph 能打标」不等于「你的标签源可以接授权」——第 3/4/5 问仍要你自己回答。

## 4. 最小验证（50 列 + 1 周 shadow）

1. **抽样**：按表/敏感级分层抽 50 列，**必须包含未标注列**；只抽已标列会系统性低估漏标。
2. **双人标 + 裁决**：两人独立标，分歧由第三人裁决；记 agreement、漏标候选、错标。
3. **覆盖率**：`已标列 / 总列`，按表分布；未标列单列清单。
4. **漏标代理**：对未标列做敏感词/代码/元数据抽查，估计「本应标但没标」的比例；不是正式漏标率，但能暴露 fail-open。
5. **1 周 shadow**：标签源 vs 人工抽检，记 coverage/agreement/耗时；不接 policy。
6. **版本/owner**：taxonomy version、`as_of`、谁回写；写进 label contract。

> 这套是工程方法（`推测`），不是测量标准；50 列/1 周是最小起点，不是统计保证。样本设计见 [02 evaluation](../../02-engineering-playbook/04-operations/02-evaluation.md)。

## 5. 停

- 没有 owner / taxonomy / coverage / 漏标估计 → **停在 A.1**，不要建 TBox 和 policy。
- 未标注列**不能当安全**；在 policy 里它是 `level=null`（R3 deny/skip），但在执行层它可能被当「无标签」放行。
- 「接受率」不能当覆盖率；「能打标」不能当「能接授权」。
- 多标签没定规则 → 不要写 shape/policy；先选 A/B/C。

## 6. 证据与边界

- **Glyph**：单企业、275 叶、多标签、per-tag provenance、不读 cell value；metadata F2 0.880、description 0.238、regex 0.050；接受率 precision-like、对 FN 盲；漏标率/覆盖率/OOD/成本未报告（`已核` 机制 / `未测` 覆盖与跨企业；E-22，[Glyph digest](../../../src/papers/2609.10430-glyph/digest.md)）。
- **策略层**：标签 ≠ 策略；标签层不产 allow/deny（E-22；[access-control mechanism](../../../topics/01-constraint/access-control/mechanism.md)）。
- **本页**：三种路径与 50 列/1 周验证是工程建议（`推测`/`未测`），不是效果承诺；04 不证明任一 label source 在你的域可用。
- **不新增 E**：本页只把「接 policy 前必须回答什么」摆出来；缺的数据回 `frontier`。

## 7. 和 04 其他页的关系

- 标签/等级写进 TBox：见 [A.3](../03-body/01-build.md) / [transfer §2](92-transfer.md)。
- 多标签规则：见 [transfer §6.2](92-transfer.md#p-multitag)。
- 标签 → level → policy：见 [C.1](../03-body/03-govern.md) / [C.2](../03-body/03-govern.md)。
- 没有标签来源时怎么决策：见 [decision §5.1](06-decision.md)。
- 第二个域的标签长什么样：见 [worked-example](94-worked-example.md)。
