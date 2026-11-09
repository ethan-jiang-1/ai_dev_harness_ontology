---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 2. 地图：能力矩阵

> 本章回答：能力矩阵怎么读、E1–E9 verdict 从哪来。 ｜ 读完你应该能：给一项能力判 A/B/C/D，并说出它的证据边界。

<img src="../../_figures/01-capability-map.svg" alt="本章地图" width="100%">

### 2.1 判定口径

| 判定 | 含义 | 不等于 |
|---|---|---|
| **A 可先落地** | 有可运行实现或可复算公式，边界能写进验收；仍需本地复测 | 已证 / 跨域有效 |
| **B 可试点** | 有一手效应量，但限定强；先量 1–3 个数再决定 | 可以直接上线 |
| **C 只能设计** | 模拟、概念或没有实现；不能承诺效果 | 不值得研究 |
| **D 反向** | 在已测条件下会得出错误结论或负收益 | 永远不能用 |

> **没有 A+。** 本仓库没有独立复现，任何一项都升不到「已证」。A 是「工程上可以先做、失败也能回退」，不是「肯定没问题」。

### 2.2 一张表

| # | 能力 | 接在哪 | 机器做什么 | 一手证据 | 判定 | 主要距离 |
|---|---|---|---|---|---|---|
| 1 | 命名/单位/槽位（K1） | 供给 | context | E-12：+54.6pp | **A** | 单工厂；先做这个 |
| 2 | 领域知识投影（K2） | 供给 | context | E-12：+19.8pp；0.777 | **B** | 单工厂/9 任务/45k 字符；顺序敏感 |
| 3 | 证据编译（claim–leaf） | 供给 | compiled | E-08/E-14：平均 −38%，条件性 | **B** | 先量 `p_h`；时延约 3× |
| 4 | 输出证据契约（grounding） | 输出时 | compiled/context | E-03：+10–15pp | **B** | 等级是模型自评；检索是瓶颈 |
| 5 | 输出后 checker | 输出后 | compiled/engine | E-02：catch/FA 可测 | **B** | 先超过空结果重试；curated 精度近随机 |
| 6 | 动作前可逆性闸 | 动作前 | compiled | E-04：4/6 模型 airline 提升；8/18 | **B** | false-veto 未测；强模型回退 |
| 7 | 跨轮身份/记忆 | 跨轮 | compiled | E-05/E-17：CMR/Acc@complete 提升 | **B** | 专有数据/文本 only/需训练信号 |
| 8 | 读路径过滤 | 检索返回前 | engine | E-20：trustgraph 代码级 | **B** | fail-open；只删 subject 侧；单实现 |
| 9 | 查询重写/OBDA | 供给 | engine | E-20：ontop 代码级 | **A** | 只支持 OWL 2 QL；不是闸 |
| 10 | 离线/CI 的 SHACL 校验 | 离线/CI | engine/compiled | E-20：semantica/open-ontologies | **A** | 不在回路内；派生 shapes 未测 |
| 11 | 推理期条件验证 | 推理期 | compiled | E-16：模拟；成功率↑、SI↓ | **C** | 合成环境、固定 schema、覆盖率 |
| 12 | 审批/多模式分配 | 动作前 | 非本体 | E-15：模拟 | **C** | 无本体变量；`γ_m` 是假设 |
| 13 | 落盘前授权 | 落盘前 | 无实现 | E-20：否定性证据 | **C** | 无实现；false-defer 未测 |
| 14 | 跨运行确定性 | 跨运行 | 无实现 | 设计提案（未升 E） | **C** | 无实现、无度量 |

> 表中 1–10 是「本体在回路里被执行」；11–12 是「同一时刻的另一种机制」；13–14 是「还没有实现」。**不要把 11–12 的数字当成本体增益**——E-15 没有本体变量，E-16 是固定 schema 的模拟。
>
> `context` / `compiled` / `engine` 是执行形态（机器拿本体做了什么），定义见 [02 §3](../../02-engineering-playbook/sections/map.md#24-选形态五种别把-context-当低配-engine)；不要把 `context` 当 `engine` 的低配。

### 2.3 怎么读这张表

- **A 不是「更好」，是「更可验收」。** 离线 SHACL 校验不会让 agent 变准，但它能在 CI 里给出一个可复算的通过/违反/未检查完；OBDA 不会拦动作，但它能把本体+映射编译成 SQL。
- **B 的共同点是「有效应量，但限定强」。** 它们都值得做一次 shadow，而不是直接上线。
- **C 的共同点是「机制在，效果没被独立测」。** 可以设计，不能承诺。

### 2.4 E1–E9 verdict（2026-11-09 第一轮）

> verdict 的定义见 [plan §1](../../_plans/01-capability-status.md#1-先定义支持是什么)。这一轮只做 desk research 与代码阅读；没有新增实验。数据表在 [`data/`](../data)。

| 期待 | verdict | 证据/数据表 | 边界 |
|---|---|---|---|
| E1 K1 | `supported（限定）` | E-12；单工厂 +54.6pp | 跨域未知 |
| E2 投影 | `supported（限定）` | E-12；单工厂 +19.8pp | 跨域/多设备/顺序迁移未知 |
| E3 编译 | `conditional` | E-08/E-14；[e3 数据表](../data/e3-compilation.md) | 公式成立；自己的 `p_h`/`c`/`Q` 未量 |
| E4 checker | `supported（限定）` | E-02；[e4 数据表](../data/e4-checker.md) | UniProt 上 data-derived 过线；你的故障分布未知 |
| E5 动作闸 | `supported（限定）`（harm）/ **`unknown`**（false-veto） | E-04/E-13；[e5 数据表](../data/e5-false-veto.md)、[校准理论](../data/e5-calibration-theory.md)、[P0 扫描](../data/p0-source-scan.md) | false-veto 无标签；它是前沿不是阈值；2610.16838 / 2607.22868 已入档，但非本体闸 |
| E6 记忆 | `supported（限定）` | E-05/E-17；[e6 数据表](../data/e6-memory.md) | 非全部设置过 +10pp/90%；跨域未知 |
| E7 读路径 | `supported（限定）`（存在）/ **`unknown`**（object 方向） | E-20；[e7/e8 代码](../data/e7-e8-code.md) | 单实现；fail-open；只删 subject |
| E8 写路径 | **`unknown`/无实现** | E-20；[e7/e8 代码](../data/e7-e8-code.md) | 四个开源项目都无单次写授权 |
| E9 确定性 | **`unknown`** | 设计提案；[P1/P2 扫描](../data/p1-p2-source-scan.md)（Suite v0 是 harness 级候选，未落盘） | 无本体锚点实现、无度量 |

**读法**：`supported（限定）` 只表示「在已测域里有证据」，不表示跨域有效；`unknown` 不是「无效」，是「还没有一手证据」。9 条里没有一条 `supported`（无限定）。
