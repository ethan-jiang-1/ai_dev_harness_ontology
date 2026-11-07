---
status: draft
updated: 2026-11-07
---

# 02 判定派：怎么知道它做错了

## 核心主张

**判据必须外部、且必须可度量。**

「挂个本体就变准」是本派最想否掉的直觉。The Ontology Catch 把判定器本身当研究对象，结论是：判定器也是一个会犯错的法官——它会漏掉错误，也会把正确答案标错，并把 agent 推去「修复」本来没错的东西。

所以本派的工程问题不是「用不用本体」，而是**这条漏检/误报曲线在哪**。

## 三种判定形态

格式 / 语义 / 行为三者的机制定义与串联关系见 [00-harness/verification.md](../00-harness/verification.md#三种判定器)。本派只关注中间那行：**本体作为语义判据**。

## 两条硬结论

1. **curated 不等于可靠。** 真实答案上 curated catch/FA/precision = 18.9/16.8/57.1%；data-derived = 8.2/3.5/72.3%；masked LLM = 5.0/1.8/93.7%。curated 精确度**仅略优于随机**（+1.6 点，CI 跨零）；按发布状态使用的 curated schema 甚至可能与自身数据矛盾。**空结果重试**在人工 fault 上 catch 79.2%、FA 0%，是必须先超过的基线。
2. **接地等级要显式化，但别把它当保证。** OA-RAG 让每个答案报告本体观察 + 接地等级（entailed/supported/related/unrelated），平均 50.5%/68.1%；Test 3 同 8k 预算 84.9% vs 66.7%，9.7k vs 96.7k tokens/问。但等级是**模型自评**、未校准；作者自述不提供形式保证。

## 误报比漏检更贵

漏检只是放过一个错误；误报会让 agent 去改对的东西。后者会产生**新的、更隐蔽的错误**——因为它带着「已修复」的外观。

这条推论目前是**推测**，但与本派的失败模式一致，值得做成实验（见 [EXP-002](../../experiments/README.md)）。

## 何时用 · 何时别用

**用**：产出可被结构性检查（有 schema、有约束、有可查的关系）；需要在不看全量人工复核的前提下筛出可疑项。

**别用**：判定器与生成器同源（自我审核几乎总失效）；没有标注集就无法知道曲线，此时判定器只是给人一种安全感。

## 子主题

- [checker](./checker/README.md) —— 判定器的位置、来源与失效模式
- [evidence](./evidence/README.md) —— 输出时的证据契约
- [calibration](./calibration/README.md) —— 判定器的曲线与代价

## 开放问题

- 误报的破坏力能否被量化？需要测「被误标后修改造成的新错误」。
- 等级判定该由谁做：OA-RAG 是模型自评；需要独立判定器/本体推导/抽样人工，并给出每个 level 的 precision/recall。
- 检索瓶颈怎么修？OA-RAG 的 gold evidence 完整检索 MCQ 61.7% vs OQ 23.6%。
- 串联判定时，早期误报如何避免放大成下游大量无效工作？

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 地图 + 硬证据；只做索引 |
| `claims.md` | 本派局部结论账本（`02-Lx`） |
| `sources.md` | 本派卡片索引 |
| `frontier.md` | 本派候选队列 |
| `<子主题>/README.md` | 详细机制 |
| `<子主题>/prompt.md` + `runs/` | 常驻 prompt 与按日期输出（模板见 [meta/subtopic-template](../../meta/subtopic-template/README.md)） |

新增内容只改本目录；只有跨派结论或进 `deliverables/` 时，才升到 [conclusions](../conclusions.md) 的 E-xx。卡片 `home` 指向本派，`subtopic` 指向子主题。

子主题按 [模板](../../meta/subtopic-template/README.md) 起；没有 `prompt.md` 就先不建 `runs/`。

## 持续挖掘

前沿问题、信号源、检索式与候选队列见 [frontier.md](./frontier.md)。稳定判断只在本页被改变时改写。
