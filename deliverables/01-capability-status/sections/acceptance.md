---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# 5. 验收与缺口

> 本章回答：距离与期待。 ｜ 读完你应该能：写出一页 go/no-go 前必须量什么。

### 5.1 距离：还差什么，差多远

| 缺口 | 现在有什么 | 补它需要什么 | 仓库内能否推进 | 量级（工程估算，非 E） |
|---|---|---|---|---|
| false-veto / 误拦率 | 原锚撤回（W-03）；blocked log 没有 harm/授权标签；候选源也按 §4 移出 | 按 W-03 做 shadow 200–500 + 100 条 blocked 标注；报 miss–false-block 前沿，不设单点 | 部分：有评测方法；本体闸标签仍需仓库外 | 待新源 |
| 写路径授权 | 概念架构 + 四条开源否定证据；本轮检索未找到实现 | 域 policy、审计存储、事务、可控写路径；先做一个 mutation class | 否 | 需立项建设 |
| 独立复现 | 现有 27 条 E 全部是 `已核`/`推测`，无 `已证`；10 篇论文 + 8 个开源是材料基础 | 仓库外复现记录 + `EXP-xxx` 指针 | 否 | 不确定 |
| 跨域效度 | 单工厂（E-12）、单基准（E-01）、checker 无 admitted 源（E-02 撤回）、专有数据（E-05）；本轮未新增跨域来源 | 更多独立域/基准 | 部分：可继续 desk research | 数个来源 |
| 接地等级校准 | 旧等级是模型自评、且源已撤回（W-02）；数值停用 | 按 W-02：每级 100–200 条独立标注，报 precision/recall | 否 | 独立标注 |
| 第二个 read-path 实现 | trustgraph 1 个 | 再找一个 pin commit 的实现 | 部分：可继续扫开源 | 继续扫 |
| 跨运行确定性 | 设计提案；Suite v0 候选（harness 级一致性度量，未落盘） | 实现 + 投影覆盖率/归因规则 | 否 | 无路径 |
| 单位成本 | 公式有，单价全空 | 人周价、审批分钟价、事故成本、token 单价 | 否，需业务输入 | 不是研究问题 |
| 多智能体共享本体 | 空白 | 可判定设计 + 证据 | 部分：可继续扫 | 无路径 |

> **不要把这些缺口变成交付前置。** 本仓库不设实验、不请求客户资产；缺口是研究地图，不是签核门（[ADR 0007](../../../adr/0007-no-external-asset-gate.md)）。
>


<a id="9-期待与数据需求验收规格"></a>
### 5.2 期待与数据需求（验收规格）

> 这一节不是结论，是**把期待写成可证伪的句子，再倒推需要什么数据**。数据缺在哪里，就回 `topics/` 或 `frontier` 补；不在交付物里补。所有数字都是「要量什么」，不是「已经量到」。这是验收规格（非 E）。
>
> **K 代号**：K0–K4 是论文条件代号，不是标准；X1/X2 用「原始点位 / 点位语义 / 知识投影文本」描述，K 只在括号里回查。定义见 [K 页](./k-ladder.md)。

| # | 期待（可证伪） | verdict（2026-11-11 修订） | 支持它需要的数据 | 现在的证据 | 缺口 | 没过怎么办 |
|---|---|---|---|---|---|---|
| X1 | 在目标域，点位语义相对原始点位（论文 K1 vs K0）的 primary-trap avoidance ≥ +10pp | `supported（限定）` | 3 个代表性任务的 K0/K1 回放，同一模型；primary-trap 标注 | E-12 单工厂 +54.6pp | 跨域；目标域基线 | 停在点位语义，不做投影；先查单位/别名覆盖 |
| X2 | 知识投影文本相对点位语义（论文 K2 vs K1）的增益 ≥ +5pp，且投影 ≤60k 字符 | `supported（限定）` | K1/K2 回放；字符数；维护人日；顺序消融 | E-12 +19.8pp，单工厂 9 任务 | 跨域；多设备；顺序迁移 | 停在点位语义；不投影 |
| X3 | 目标流量上 `p_h ≥ p_min = 2% + c/(0.929Q)`（c=每次编译成本，Q=每问 token 预算），且 p95 不超预算 | `conditional` | `p_h`、miss penalty、`c`、`Q`、p95、轮次 | E-08/E-14 公式；[e3 数据表](../data/e3-compilation.md) | 自己的流量分布 | 不编译；先量 `p_h`、`c`、`Q` |
| X4 | checker 的增量 catch ≥5pp、FA ≤15%，per-1k 成本 ≤人工 1/3（`工程建议`） | **`unknown` / 待新源** | 按 W-01：200 题分层（类型/声明/语义各 ≥50）；catch/FA/净修复分开；per-flagged 成本 | E-02 已撤回；[e4 数据表](../data/e4-checker.md) 只作历史 | 新源；故障分布；false-veto | 不设门槛；不立 checker 项，也不承诺 catch/FA |
| X5 | 动作闸在给定 miss 预算下报 false-block 前沿；harm 降且 task success 不降 >2pp | **`unknown` / 待新源** | 按 W-03：shadow 200–500 决策 + 100 条 blocked 标注 + 同轨迹配对 | E-04/E-13 已撤回；E-15 仅非本体参照；[e5 数据表](../data/e5-false-veto.md) 只作历史 | 新源；blocked 标签；同轨迹配对 | 不设门槛；不上硬 veto；不把 CASEL 当本体证据 |
| X6 | 记忆层 CMR 或 Acc@complete 相对基线 ≥ +10pp，merge precision ≥90% | `supported（限定）` | registry on/off；200 incoming units；CMR/merge precision/Acc@complete | E-05/E-17；[e6 数据表](../data/e6-memory.md) | 自己的域；false merge 传播 | 不做 registry；先修抽取 |
| X7 | 读路径过滤在 object 方向也不泄漏 | `supported（限定）`（存在）/ **`unknown`**（object） | 第二个独立实现；object 方向用例；异常 policy 用例 | E-20；[e7/e8 代码](../data/e7-e8-code.md) | 第二个实现 | 标「单实现」；不当授权 |
| X8 | 写路径 gate 的 false-defer ≤20%，且审计可追 | **`unknown`/无实现** | 一个 mutation class 的实现；20–50 条 false-defer 样本 | E-20；[e7/e8 代码](../data/e7-e8-code.md) | 实现；false-defer 标签 | 只做设计；不声称落地 |
| X9 | 跨运行产物收敛可度量（投影覆盖率/归因规则） | **`unknown`** | 同一输入的重复运行；投影覆盖率；漂移归因 | 设计提案；[P1/P2 扫描](../data/p1-p2-source-scan.md)（Suite v0 候选，harness 级） | 实现；本体锚点度量 | 标 `unknown`；不承诺 |

**怎么用**：每条期待都是一次 go/no-go 的候选；先量「支持它需要的数据」那一列，量不出来就写「未知」，不要用「通用经验」补。

**第一轮底稿**：[`data/`](../data) 里有 e3/e4/e5/e6/e7-e8 数据表与 [P0 源扫描](../data/p0-source-scan.md)。它们是工作底稿，不是交付正文；正式引用仍走 E-xx。

**详细执行计划**：[plan.md](../../_plans/01-capability-status.md)（覆盖审计、现有 digest 回抽、需要新 `src/` 的来源、WBS、排期、DoD、停止规则）。

<a id="8-与另外两份交付物的关系"></a>
