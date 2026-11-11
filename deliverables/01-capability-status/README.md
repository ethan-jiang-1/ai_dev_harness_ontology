---
status: draft
deliverable_status: draft
updated: 2026-11-11
target: 决策者 / 工程负责人
basis: E-01–E-20, C-01–C-04
---

# 01 · 现状：本体接进 harness，今天能完成什么

> **读者**：决策者 / 工程负责人 ｜ **回答**：今天能做成什么、不能承诺什么 ｜ **不回答**：具体怎么做（去 02）、为什么是这些位置（去 03）。
>
> **第一次来**：先读 [START](../START.md)（10 分钟）；只想拍板，读本页 §0 + 决策记录 1。
>
> **2026-11-11 证据重置**：5 条 E 撤回；#4/#5/#6/#11 转 gap（W 表见 [canonical §5](./sections/canonical.md#5-撤回与历史w-表)）。状态见 [_plans/status](../_plans/2026-11-11-status.md)。

## 先看一个决定

在一个真实工厂的 9 个任务上，agent 一开始只看到「PLC 地址 + 原始整数」；把这些点位换成「tag 名 + 单位 + 质量码」后，避坑率相对原始点位提高 **54.6 个百分点**。再把这座设备本体的知识写成一段约 45k 字符的文本放进上下文，避坑率从 0.605 升到 0.802，只再提高 **19.8 个百分点**（E-12；单工厂、9 任务、答案基本写在文本里）。

这篇论文（Joo & Kim, arXiv:2610.11768）把前一种条件叫 **K1**、后一种叫 **K2**，把只有地址和裸值的基线叫 **K0**——**这是论文的实验条件编号，不是术语，也不是行业标准/成熟度**。本文正文只用「原始点位 / 点位语义 / 知识投影文本」；K 只在出处与回查里出现，见 [K0–K4 来源说明](./sections/k-ladder.md)。

所以第一个决定不是「建什么本体」，而是：**先把点位语义（tag 名/单位/质量码）对齐，还是先做知识投影文本？** 01 的答案是：先点位语义；它不过，不做投影。

**三条判断（读完能复述）：**

1. 本体今天最确定的角色是「可求值的约束/查询对象」，不是「更懂业务的提示词」；有引擎 ≠ 会拦 ≠ 有授权（E-20）。**「可求值」= 能当查询/校验对象被引擎执行**，不是「模型读着更懂」。
2. 最大知识增益来自薄语义层，不是深度结构；点位语义 +54.6pp，知识投影文本只再加 +19.8pp（E-12）。
3. 约束/判定这条线今天不能承诺：原锚 E-04/E-13（动作闸）与 E-02（checker）已撤回；只剩 CASEL 的非本体参照（E-15）。

> **词源速查（只定词，不撑效果）**：`本体` = `N: ISO/IEC 21838-1`（本仓库义更宽，判 `broader`；不要当成「标准认证的领域本体」）；`约束 / 校验` = `N: W3C SHACL`（只到 RDF 图约束，**不到动作授权**）。其余词的来源与 `local` 清单见 [术语速查 §0](./sections/glossary.md#term-sources)。

> **只读 5 页（约 30 分钟）**：① [本页 §0](#0-一页结论) → ② [地图 §2.1](./sections/map.md#21-判定口径) → ③ [决策记录 1](./sections/decision-record.md) → ④ [边界 §4.3](./sections/boundaries.md#43-反向在已测条件下不要做) → ⑤ [验收 §5.2](./sections/acceptance.md#52-期待与数据需求验收规格)。不要从目录逐页读。
>
> **内码**：A/B/C/D = 可先落地 / 可试点 / 只能设计 / 反向；X1–X9 = 9 条期待；E-xx = 跨派证据；W-xx = 撤回依据与重测协议（[canonical §5](./sections/canonical.md#5-撤回与历史w-表)）。**K0–K4 是论文条件代号，不是行业标准**；对照见 [K 页](./sections/k-ladder.md)。
>
> **术语来源（读法）**：定义后标 `（N: 标准名）` = 有规范性锚，**只定词与合格性、不撑效果**；标 `（local）` = 本仓库工作词，没有标准锚。规则与标准清单见 [规范主干](../../topics/trunk.md)，逐词判定见 [术语基线](../../meta/term-baseline.md)。K0–K4 判 `local`（论文条件，非 normative 源）。
>
> **证据等级**：本仓库没有独立复现，最高等级是 `已核`；「能落地」只表示「有实现/公式 + 一手证据 + 边界可写进验收」，**不表示「已证」**。A/B/C/D 是交付层排序，不是新 E；排序依据在 [map §2.1](./sections/map.md#21-判定口径)。




## 0. 一页结论

| 判定 | 清单 | 一句话 |
|---|---|---|
| **A 可先落地** | 点位语义（K1）；离线/CI SHACL；OBDA 查询重写 | 有实现或可复算公式，失败可回退；但仍需本地复测 |
| **B 可试点** | 知识投影文本（K2）、编译、记忆、读路径过滤 | 有一手效应量、源仍 admitted，限定强；先量 1–3 个数再决定 |
| **C 只能设计** | 落盘授权、跨运行确定性 | 有机制/设计，但只有模拟或无实现；不能承诺 |
| **非本体（参照）** | 审批/多模式分配（CASEL） | 没有本体变量；只作参照，不进 A/B/C |
| **gap / 待新源** | 证据契约、checker、动作闸、推理期条件验证 | **原锚 E-02/E-03/E-04/E-13/E-16 已撤回**；不判 A/B/C，等新源 |
| **D 反向** | 见 [§4.3](./sections/boundaries.md#43-反向在已测条件下不要做)：强 RAG 下为准确率买工件、commit 概念架构当落地、没有账本就上机制；curated/reward 两条原锚撤回→待新源 | 在已测且源仍 admitted 的条件下会得出错误结论或负收益 |

> **多智能体共享本体**：只有方向，没有机制/设计/一手证据，标 **`undetermined`**。**本体自动生成/精化**是 source（[05 生产](../../topics/05-produce/README.md)），不在本表；不要硬塞进 A/B/C。判定规则见 [map §2.1](./sections/map.md#21-判定口径)。

**最像「可以先做」的只有一件：先把点位语义对齐——tag 名、单位、质量码（论文的 K1）。** 工程上常再加别名/槽位，但那是我们的扩展，不在论文的 K1 里。其余都是「有条件能试」或「还差得远」；点位语义也只在单工厂、9 任务里测过，换域要重测。

> 还有一类方向尚未形成 E（例如本体自动生成/精化到可消费），只在派内判断里，本表不把它们当结论；见 [05 生产](../../topics/05-produce/README.md)。


<a id="1-三句话"></a>
### 0.1 三句话

1. **最确定的角色是「可求值的约束/查询对象」，不是「更懂业务的提示词」。** 四个开源项目在 pin commit 上给出四种不同的执行语义：OWL 2 QL 查询重写、SHACL-AF 策略求值、SHACL 校验、SHACL→SPARQL/verified Core（E-20）。「有引擎」不等于「会拦」，更不等于「有授权」。
2. **今天能拿到的最大知识增益来自薄语义层，不是深度结构。** 点位语义（论文 K0→K1）避坑率 +54.6pp；把塔投影成文本（K1→K2）再加 +19.8pp，且只在单工厂、9 个任务、答案基本写在文本里的条件下测过（E-12）。强检索 harness 下，被测量的结构化工件没有可检出的准确率增益；原文的 ontology 还是 `not measured`（E-01）。
3. **约束/判定这条线今天不能承诺。** 原锚 E-04/E-13（可逆性闸）与 E-02（checker）已撤回；只剩 CASEL 的审批/分配模拟（E-15，非本体）。所以「护栏能改变走向」不再是本仓库的结论；今天能说的是：**落盘写路径的授权仍然没有实现**（E-20）。

如果只记一句：**今天能拿到的，不是「让模型更准」，而是「在少数供给/读路径接缝上有可验收的实现」；动作前的「拦」还缺 admitted 证据，不能先承诺。**

**第一轮 verdict（2026-11-09；2026-11-11 证据重置后修订）**：9 条期待里，X1/X2/X6/X7 仍有 `supported（限定）` 半边，X3 仍 `conditional`；**X4/X5 因 E-02/E-04/E-13 撤回，改为 `unknown/待新源`**；X8/X9 仍 `unknown`。**没有 9/9 supported；X4/X5 的旧 supported 已撤回，不能再引用。** 详见 [§2.4](./sections/map.md#24-x1x9-verdict2026-11-09-第一轮) 与 [`data/`](./data/)。


<a id="6-如果只做一件事"></a>
### 0.2 如果只做一件事

**先做点位语义（K1），再建账本。**

- 点位语义（tag 名/单位/质量码；论文 K1）是已测最大增益、最便宜、最可回退；它不需要先建整座本体塔。
- 账本（per-query 或 per-decision 的 token、时延、审批、决策、回滚）是所有 go/no-go 的前提；没有它，`p_h`、false-veto、审批成本都算不出来。
- 然后只选**一个**接缝做 shadow：今天优先在供给或读路径里选（投影、编译、读路径）；判定/动作线（checker、动作闸）等新源，不要拿 gap 行当试点。

**不要先做的**：整座本体塔（一台设备的窄而深本体，不是整座企业本体）、自动生成本体、commit gate、跨运行确定性、多智能体共享本体。它们要么没有实现，要么没有下游证据。




## 目录

| 节 | 文件 | 内容 |
|---|---|---|
| 导读 | [GUIDE.md](./GUIDE.md) | 先读哪一页、按什么顺序 |
| 2 地图 | [sections/map.md](./sections/map.md) | 能力矩阵、判定口径、X1–X9 verdict |
| 3 主体 | [capabilities/README.md](./capabilities/README.md) | 六组能力条目 |
| 4 边界 | [sections/boundaries.md](./sections/boundaries.md) | 工作前提、反例、证据边界 |
| 5 验收 | [sections/acceptance.md](./sections/acceptance.md) | 距离、期待与数据需求 |
| 6 关系 | [关系与维护](../README.md#关系与维护) | 与 02/03 的关系、维护 |
| 术语 | [sections/glossary.md](./sections/glossary.md) | X1–X9 vs E-01–E-20、A/B/C/D、K0–K4 一句话对照 |
| K0–K4 来源 | [sections/k-ladder.md](./sections/k-ladder.md) | K 是谁定义的、是不是标准、K3/K4 为什么不在主路径 |
| 阈值 | [sections/canonical.md](./sections/canonical.md) | 14 行计数、X1–X9 门槛、一个数只写一次 |
| 决策记录 | [sections/decision-record.md](./sections/decision-record.md) | 点位语义→A、读路径→B、离线 SHACL→A、落盘→C、投影→B、checker→B、OBDA 对照 |
| 模板 | [sections/templates.md](./sections/templates.md) | 决策记录/能力行/期待行空表 |
| 数据表 | [本页 §数据表](#数据表工作底稿) | e3/e4/e5/e6/e7-e8 数据表、P0/P1 扫描 |

## 数据表（工作底稿）

> 工作底稿，不是交付正文；数字用于 verdict，正式引用仍走 E-xx。表里的 `unknown` 不是失败，是缺口。

| 文件 | 内容 |
|---|---|
| [e3-compilation.md](./data/e3-compilation.md) | X3 编译：p_min、43% 反推、φ 未测 |
| [e4-checker.md](./data/e4-checker.md) | X4 checker：data-derived 过线、curated FA 超线 |
| [e5-false-veto.md](./data/e5-false-veto.md) | X5 动作闸：1,745 blocked 无标签、false-veto unknown |
| [e5-calibration-theory.md](./data/e5-calibration-theory.md) | X5 校准理论：false-block/miss 前沿、block-all |
| [e6-memory.md](./data/e6-memory.md) | X6 记忆：alias/CMR、部分设置未过线 |
| [e7-e8-code.md](./data/e7-e8-code.md) | X7/X8 代码：read-path fail-open、无写授权 |
| [p0-source-scan.md](./data/p0-source-scan.md) | P0 源扫描：授权 benchmark、false-block 前沿 |
| [p1-p2-source-scan.md](./data/p1-p2-source-scan.md) | P1/P2 源扫描：第二 read-path、X9 候选 |

## 关注什么 / 需要什么材料

| 项 | 内容 |
|---|---|
| 关心 | 哪些能力能先落地（A）、哪些只能试点（B）、哪些只能设计（C）、哪些方向是反向（D）；距离有多远 |
| 需要材料 | E-xx 的限定、digest §5「不能说明什么」、`data/` 数据表、各派 `frontier.md` |
| 不做什么 | 不做实验、不建本体、不请求客户资产；只把已有证据摆成可决策地图 |