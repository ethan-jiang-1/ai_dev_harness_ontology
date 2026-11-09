---
status: draft
updated: 2026-11-09
---

# 03 知识派：怎么让它知道得对

## 核心主张

两条，都与直觉相反：

1. **投影文本 pooled 分最高，但不是普适排序。** 同一塔上文本 0.777 > JSON 0.717 > 查询工具 0.638 > 文档检索 0.597；但 JSON/工具是事后比较，GLM-5.2 的 JSON 反超其文本、Qwen 的工具低于其检索。`已核`（分数）/`存疑`（排序）
2. **编译解决的是预算，不是准确率；预算收益只在 claim–leaf 上测出。** 平均 −38% token（充分 −91%、不充分 +1.9%），准确率仍 neutral；PageIndex 大纲在 FRAMES 规模实测为负。`已核`（FRAMES、单 compiler 限定）

这一派在六派里约束最弱，因为投影只在上下文里、不承担拒绝逻辑（「投影写了规则仍会被忽略」未做 prompt-vs-code 对照），编译也不阻止动作。`推测`（约束强度）

工程上这一派却最常被问——「让模型知道业务规则」几乎所有项目都从这里起步，但知识供给本身不是约束。

## 子主题地图

| 子主题 | 回答什么 | 状态 | 已发现 / 未发现 | 先读 |
|---|---|---|---|---|
| [projection](./projection/README.md) | 把领域知识投影成文本/JSON/工具 | `draft`，已拆 F/G | 4 F / 5 G | dashboard |
| [compilation](./compilation/README.md) | 把证据预编译成 claim–leaf 工件 | `draft`，已拆 F/G | 11 F / 8 G | dashboard |
| [querying](./querying/README.md) | 自然语言 → SPARQL 的三条路线 | `draft`，已拆 F/G | 3 F / 4 G | dashboard |

**薄页（<2 篇独立来源）**：projection（1 篇，单工厂）、compilation（2 篇，同一 CAI 的两种切法）。薄页的结论不能外推为跨域规律。

## 本派当前判断

- **投影文本 pooled 分最高，但不是普适排序。** 文本 0.777、JSON 0.717、查询工具 0.638、检索 0.597；JSON/工具是事后描述性比较，GLM-5.2 的 JSON 0.900 反超其文本 0.891，Qwen 的工具 0.407 低于其检索 0.538。详见 [projection/F1](./projection/findings.md)。`已核`（分数）/`存疑`（普适排序）
- **已测得的最大一层增益是命名+单位，不是物理深度（未测）。** K0→K1 +54.6 pp，K1→K2 +19.8 pp；16 个推导量在塔里、不在投影里，9 个任务也不要求推导量。H2（增益随容量上升）未支持，p=0.85。详见 [projection/F2](./projection/findings.md)。`已核`（已测两层）
- **运行教训在抽取时并入塔才常被用；日志里的本事故记录不提升诊断。** 日志检索仅 4/80；H3 未支持（K4 0.644 vs K4x 0.645，差 <0.01）。「投影=把归纳提前做掉」是解释，`推测`。详见 [projection/F3](./projection/findings.md)。`已核`（现象）
- **编译只解决预算，且是条件性的。** claim–leaf 平均 −38% token，准确率仍 neutral；PageIndex 大纲在 FRAMES 规模为负；盈亏平衡 `p_min=2%+c/(0.929Q)`，先量 miss。详见 [compilation/F1](./compilation/findings/accuracy.md#f1) · [F2](./compilation/findings/economics.md#f2) · [F7](./compilation/findings/economics.md#f7)。`已核`
- **受监管支线：Grid 对最强 agent baseline 只高 0.5pp，可审计性靠契约。** 99.9% vs Codex/Power-Agent 99.4%；Power-Agent 仅 46/519 调用 PowerMCP 仍到 99.4%；citation/拒答、strict pass、记忆批准与决策点签核是契约，客户指标尚无基线。详见 [compilation/F5](./compilation/findings/regulatory.md#f5) · [F11](./compilation/findings/regulatory.md#f11)。`已核`（数字/契约）/`推测`（工具归因、客户指标）
- **两条不矛盾，差别不只在答案位置，还在投影什么。** 知识即答案 → 投影领域知识；答案要从语料检索 → 编译证据/检索。`推测`（分析框架）。详见 [C-04](../conclusions.md)。
- **查询生成有三条路线，但没有头对头。** GGC 选择性纠错（MCQA 答案集匹配 90.23→98.33，全量纠错 92.34）；NLKGQ 完整 OWL 进上下文（DBLP-QuAD 3.1 89.9 Match/81.3 Exact）；KGVoyager 无 ontology 的 agentic navigation（4 小 benchmark F1 +3.7pp，不是 4×）。详见 [querying](./querying/README.md)。`已核`（各自数字）/`推测`（综合）

## 三种供给形态

| 形态 | 做法 | 何时 |
|---|---|---|
| [投影](./projection/README.md) | 把本体成段写成文本/记录 | 知识小而深、就是答案 |
| [编译](./compilation/README.md) | 预整理成 claim–leaf/树/图/wiki | 语料大、需要反复检索 |
| 集成 | 知识并入既有系统（法规库、工单） | 有存量系统、需要治理（暂无专文） |

## 何时用 · 何时别用

**用**：封闭域、操作手册型知识、答案基本写在文本里；需要模型照着规则做时，硬执行另进 01/02。

**别用**：开放域检索、多跳问答——如果目标是准确率增益，此时该投资的是检索 harness 本身，而不是工件。编译只在算过 `p_h > p_min` 后才买；`p_h < p_min` 或时延是硬约束时不要买。投影不承担拒绝逻辑，硬约束进 01/02。

## 本目录怎么长

| 文件/目录 | 作用 |
|---|---|
| `README.md` | 本页：派地图 + top claims；不展开机制 |
| `claims.md` | 本派局部结论账本（`03-Lx`） |
| `sources.md` | 本派 digest/card 索引 |
| `frontier.md` | 本派候选队列 |
| `<子主题>/README.md` | dashboard：覆盖/计数/当前判断/文件地图 |
| `<子主题>/findings.md` | 该子主题的发现与证据（F1、F2…；大了再拆 `findings/`） |
| `<子主题>/findings/*.md` | 按证据线拆开的详细发现（accuracy/economics/regulatory…） |
| `<子主题>/frontier.md` | 该子主题的 gap/next |
| `<子主题>/mechanism.md` | 机制怎么跑（按需） |

## 持续挖掘

派级前沿、检索式与候选见 [frontier.md](./frontier.md)；子主题的 gap/next 在各自 `frontier.md`。
