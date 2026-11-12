---
status: superseded
updated: 2026-11-08
---

> **历史快照（2026-11-08/09）**：已归档，不再维护。现行规则见 `meta/README.md`，当前状态见 `meta/status/state.md`。文中的计数与结论可能已被后续修复取代。


# 仓库质量推进计划

> 这份计划不追求“再多写几篇”，而是把现有 22 篇论文、20 个子主题、跨页结论推进到**可独立阅读、可核查、可持续增长**的质量。所有波次以质量门为准，不按数量结项。

## 0. 现状

- **src**：22 篇论文目录齐；`digest.md` 已全部重写为自包含版本（L3 150–214 行、L2 156–200、L1 81–84），但**尚未逐篇做质量复核**；`card.md` 仍是较厚的分解卡，不是来源卡；`sources.md` 里内容链接仍混用 card/digest。
- **topics**：`action-gate`、`compilation` 已迁成 dashboard + findings/frontier/mechanism；其余 18 个子主题仍是单页长文。派 README 只有 01/03 改成 index。
- **跨页**：conclusions 17 已核 / 2 推测 / 3 存疑 / 4 冲突；E-19 已进 THESIS；feasibility 已建；问题→机制目录已有雏形。
- **最大风险**：digest 的“自包含”只是长度达标，**数字条件、术语解释、不能证明什么、工程用法**可能仍有空洞；subtopic 迁移只做了两个样板，容易出现风格漂移。

## 1. 目标与非目标

**目标**：一个高质量的研究档案——读者只读 `digest.md` 就能判断一篇论文；只读子主题 dashboard 就能知道“发现了多少、还缺什么、下一步看什么”；跨页结论与计数一致；所有链接可解析。

**非目标**：

- 不新增论文（除非某个 gap 必须补一篇；需在 frontier 里先登记理由）。
- 不跑实验、不写代码；实验设计留在 `experiments/`。
- 不在 deliverables 新增判断。
- 不为“看起来完整”建空文件或占位小节。
- 不把 L1 硬扩成 L3；L1 保持 50–100 行，但必须自包含。

## 2. 质量定义（七道门）

### G1 · digest 自包含

- 有「三句话 / 问题 / 术语 / 方法 / 数字与条件 / 不能说明什么 / 工程用法 / 质量边界 / 与仓库判断 / 未解决」。
- 术语表解释读数字前必须懂的词；方法有一个具体例子。
- **不靠「详见 card」补上下文**；正文链接只放原文/代码。
- 长度：L3 150–250；L2 100–200；L1 50–100。

### G2 · 证据可核查

- 每个数字带数据、模型、样本量、设置、比较对象；没有裸数字。
- 关键数字抽 10% 回 `paper.md`/PDF 核对；页码/表号可追。
- 作者结论、读者推断、仓库判断分开；推测/存疑有理由。
- 反例与正例同权重；不准把「无可检出」写成「零效应」。

### G3 · card 是来源卡

- 40–75 行：元数据 + 一句话作者主张 + 问题/设定 + 章节/图表索引 + 作者局限 + 原文链接。
- 不放长机制、完整证据表、工程建议、跨论文比较。
- `reading` / `provenance` 如实；`updates` 列全。

### G4 · 子主题 README 是 dashboard

- 一屏以内：覆盖、已发现/未发现/下一步计数、当前判断 3–5 条、文件地图、边界。
- 发现/证据在 `findings.md` + `findings/`；gap/next 在 `frontier.md`；机制在 `mechanism.md`。
- 不把长论证塞回 README；不建空 `findings/`、`mechanism.md`、`runs/`。

### G5 · 跨页一致

- `sources.md` 的内容链接指向 `digest.md`；card 只用于 provenance。
- 计数（22 篇、17/2/3/4、20 子主题）与 README/checklist/conclusions 一致。
- 术语（证据等级/接地等级/接缝/时刻/派）不混用；新术语进 GLOSSARY。
- E-xx 与 L-xx 的引用关系可追；冲突条目保留。

### G6 · 导航可解析

- 根 README 是 router；派 README 是地图；子主题 README 是 dashboard。
- 所有相对链接目标存在；标签指向正确概念。
- 读者从根 README 三步内能到任意 digest / 子主题 dashboard。

### G7 · 复核独立

- 每波至少一次 **critic pass**：由另一个 subagent/读者按 G1–G6 抽样复核，不只看作者自述。
- 抽样比例：每波 ≥30% 文件或 ≥3 篇，取较大者；数字抽 10%。
- 复核发现的问题先修，再进下一波；修完记录在 `meta/quality-report.md`。

## 3. 工作流

| 工作流 | 范围 | 产出 |
|---|---|---|
| **A. 来源层** | 22 篇 digest 质量复核 + 必要修订；22 张 card 来源卡化；sources 表改链 digest | digest 全部过 G1/G2；card 过 G3；sources 一致 |
| **B. 主题层** | 20 个子主题：dashboard + findings + frontier + mechanism（按需） | 全部过 G4；派 README 过 G6 |
| **C. 综合层** | conclusions / THESIS / C-04 / E-19 / 问题→机制目录 / feasibility | 计数一致、判断可追、冲突保留 |
| **D. 验收层** | 链接、抽样、报告 | `meta/quality-report.md` + 审计表 |

## 4. 波次

### Wave 0 · 校准（1–2 轮）

- 冻结 G1–G7 与模板；建 `meta/quality-report.md` 骨架。
- 抽 3 篇做 critic：MIOE（机制型）、CAI（成本型）、POLAR（反例型）。
- 根据 critic 结果修模板/checklist；不改内容，只校准标准。

**出口**：3 篇过 G1/G2；critic 记录可复用。

### Wave 1 · L3 来源层（12 篇，3–5 轮）

- 每批 3 篇：逐篇读 digest + 抽 5 个数字回原文；检查术语/方法/不能证明什么/工程用法。
- 重点：MIOE、CAI、POLAR、N&D、Ontology Catch、CASEL、FIRME、OntoAct、SLB、Grid、Diagnose、OntoDoc。
- 每篇更新 `digest-audit` 状态；发现模板问题回改模板。

**出口**：12 篇全部 G1/G2；抽 10% 数字有页码/表号；0 处「详见 card」。

### Wave 2 · L2/L1 来源层 + card（10 篇 + 22 张卡，2–4 轮）

- L2 6 篇：确认自包含、数字条件、例子；L1 4 篇：保持短，但术语/边界清楚。
- 22 张 card 压成来源卡：删长机制/证据表/工程建议；保留元数据/索引/局限。
- `sources.md` 内容链接改 digest；card 只留 provenance。

**出口**：22 篇 digest 全过 G1/G2；22 张 card 过 G3；sources 表一致。

### Wave 3 · 重子主题迁移（8–10 个，4–6 轮）

优先：`02/checker`、`02/evidence`、`04/memory`、`04/identity`、`03/projection`、`01/reasoning-gate`、`01/commit-gate`、`05/generation`、`05/refinement`、`06/trace`、`06/metrics`、`06/mechanism`、`06/failure-attribution`。

每个：README dashboard + findings.md（F 编号）+ findings/（按需）+ frontier.md（G/N）+ mechanism.md（按需）。不建空文件。

**出口**：每个 README ≤1 屏；F/G/N 可数；派 README 链 dashboard。

### Wave 4 · 剩余子主题 + 派 README（2–4 轮）

- 其余子主题只做 dashboard（有内容才拆 findings/frontier）；薄页不硬拆。
- 6 个派 README 改成 index：子主题表 + 状态 + top claims + 目录怎么长。
- `topics/README` 补「子主题怎么长」与源文献归位。

**出口**：20 个子主题 README 全过 G4；6 个派 README 过 G6。

### Wave 5 · 综合与一致（2–3 轮）

- conclusions：核对 17/2/3/4；E-19/C-04/Q 的表述与证据一致。
- THESIS：P1–P3 + E-19；不新增 P4，除非有实验。
- feasibility：三个盈亏平衡与 digest 数字对齐；问题→机制目录补全。
- 计数、术语、source 表、manifest/checklist 全扫。

**出口**：G5 全过；无悬空 E/L；无重复/矛盾计数。

### Wave 6 · digest 深打磨（新增，40–50 轮）

**结构过关不等于好读。** 这一轮从头再读 22 篇，逐篇重写/扩写 digest；2–3 篇/轮，允许慢。

深打磨标准（D1–D6）：

| 标准 | 要什么 |
|---|---|
| D1 术语直觉 | 每个术语先给一句人话，再给论文用法；不堆定义 |
| D2 方法可复述 | step-by-step + 一个具体输入例子；读者能向同事复述 |
| D3 数字有含义 | 每个关键数字：条件、出处、和谁比、说明什么、不能说明什么 |
| D4 边界清楚 | 作者局限 / 读者推断 / 仓库判断三分；反例保留 |
| D5 工程可用 | 复刻第一步、关键参数/成本、何时用/别用；不是泛泛“有价值” |
| D6 语言去模板 | 删“本文提出/具有重要意义”这类空话；每段要有信息增量 |

每篇完成后写一句「这页教会读者什么」；如果写不出，说明还没打磨好。每批 2–3 篇做一次 critic 抽样（G7 可用时）；不可用时至少做数字回原文 + 自评双遍。

**出口**：22 篇 D1–D6 全过；每篇能独立回答「它问什么/怎么做/发现什么/不能说明什么/怎么用」；模板腔显著减少。

### Wave 7 · 验收（1–2 轮）

- 全仓链接检查；digest 抽 10% 数字回原文；20 个子主题 dashboard 抽查；派 README 三步导航。
- 写 `meta/quality-report.md`：通过项、未通过项、已知边界、下一阶段（experiments/deliverables）。
- 不过的门列成 gap，不掩盖。

**出口**：报告可交付；未通过项有明确负责人/下一步。

## 5. 复核协议

1. **作者 pass**：按 G1–G4 自检，更新 `updated` 与审计表。
2. **critic pass**：另一个 subagent 抽 ≥30% 文件，按 G1–G6 打分；只报问题，不改文件。
3. **数字 spot-check**：每篇抽 5 个数字回 `paper.md`/PDF；记录页码/表号。
4. **链接检查**：`python` 脚本全仓；0 broken 才进下一波。
5. **变更记录**：每波在 `meta/quality-report.md` 记「改了什么、为什么、还剩什么」。

## 6. 停止条件（stop the line）

- digest 仍靠 card 补上下文 → 停，补内容。
- 数字无来源/无条件 → 停，回原文。
- 子主题 README 超过一屏 → 停，下沉 findings/mechanism。
- 链接 broken → 停，修完再走。
- 计数不一致 → 停，先对账。
- critic 抽样合格率 <80% → 停，重做该波。

## 7. 预算

- 总轮次：120 轮（含复核与深打磨）；Wave 0 2、Wave 1 6、Wave 2 6、Wave 3 8、Wave 4 4、Wave 5 4、Wave 6 40–50、Wave 7 2；剩余为返工 buffer。
- 每轮只做一类事；不在一轮里同时改 digest + 子主题 + conclusions。
- 超预算时优先保 G1/G2/G5，砍“好看但不关键”的排版。

## 8. 产出

- 更新后的 repo：22 篇 digest、22 张 card、20 个子主题 dashboard、6 个派 README、conclusions/THESIS/feasibility 一致。
- `meta/digest-audit.md`：逐篇行数/状态/复核结果。
- `meta/quality-report.md`：质量门通过表、抽样记录、未通过项、下一阶段。
- 不新增空文件；不为“完整”造占位。

## 9. 风险

| 风险 | 应对 |
|---|---|
| 追求数量，digest 又变回摘要 | G1/G2 门 + critic 抽样；不合格不进下一波 |
| card 与 digest 继续重复 | G3 卡 40–75 行；card 只索引，细节进 digest |
| 子主题迁移风格漂移 | Wave 0 冻结模板；每波抽 2 个对照 |
| 数字抄错/条件丢失 | 10% 回原文；每篇至少 5 个数字带页码 |
| 跨页计数/链接漂移 | 每波末全仓链接 + 计数脚本 |
| L1 被硬扩成 L3 | L1 50–100 行；只要求自包含，不要求深度 |
| 只有作者自评 | G7 critic pass；抽样 ≥30% |

## 10. 完成定义

- 22 篇 digest 全部过 G1/G2 + D1–D6 深打磨；22 张 card 过 G3。
- 20 个子主题 README 过 G4；6 个派 README 过 G6。
- G5 计数/术语/链接全过；0 broken links。
- `meta/quality-report.md` 完成，未通过项显式列出；含深打磨前后对比。
- 任何一条判断都能从根 README 三步内追到 digest/子主题，再从子主题追到 E/L。
