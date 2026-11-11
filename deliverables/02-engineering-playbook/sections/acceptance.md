---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# 5. 验收与缺口

> **证据重置**：R4/R5/R6/R12 的原锚已撤回/移出（W 表见 [canonical §1.1](./canonical.md#w-table)）；这 4 行改按 W 协议重测，不再设旧门槛。当前可验收的是 R1/R2/R3/R7/R8/R10/R11；R9 只有设计。


> 本章回答：怎么验收、什么时候停、还缺什么。 ｜ 读完你应该能：写出一页 go/no-go memo。

### 5.1 验收与 stop：按机制选尺

| 机制 | 主指标 | 过程指标 | 反事实 | 停线 | 出处（O/E） | 量不出时 |
|---|---|---|---|---|---|---|
| R0 | 四项检查 pass/flag/unknown | 修复清单 | 无检查直接上 | 任一 unknown 当 pass | 工程建议（O-T01） | 改人工清单；不宣称 pass |
| K1 | primary-trap avoidance | token | K0 | 剩余 trap 与深知识无关 → 停 | 工程建议 + E-12（O-T02） | 先做 K0 回放；量不出就停在 K1 |
| 投影 | primary-trap/element | 字符数/维护人日 | K1 | <5pp、>60k、>2 人周/月 | 工程建议 + E-12（O-T03） | 先量 K1 基线；<5pp 就停 |
| 编译 | token/问、p95 | `p_h`/miss、`c`、`Q` | 词法检索 | `p_h < p_min` | E-14 / O-F01（O-T04） | 先量 p_h；量不出就不编译 |
| evidence **gap** | 准确率、引用率 | 检索率、grounding 校准 | 纯文本 RAG | 原 E-03 撤回；不设门槛 | E-03 withdrawn | 先找新源；不设门槛 |
| checker **gap** | 增量 catch、FA、净修复 | per-1k 成本 | 空结果重试 | 原 E-02 撤回；不设门槛 | E-02 withdrawn | 先找新源；不设门槛 |
| action **gap** | harm、审批、false-veto、task success | 保留率、φ（可逆性分数）、miss–false-block 前沿 | 不上护栏 | 原 E-04/E-13 撤回；不设门槛 | E-04/E-13 withdrawn；E-15 参照 | 先找新源；不上硬 veto |
| memory | CMR、merge precision、Acc@complete | 抽取层误差 | 不做 registry | precision <90% | 工程建议 + E-05（O-T08） | 先量 merge precision；<90% 停 |
| read-path | 泄漏率、误拦 | 延迟 | 不过滤 | fail-open 未修/object 方向未测 | E-20（O-T09） | 标「单实现」；不升第七时刻 |
| commit | false-defer、unresolved、审计可追 | 人审工时 | 直接 merge | >20%、>10%、不可追 | 工程建议 / gap（O-T10） | 标 gap；只做设计 |
| 离线 SHACL | 负例检出、干净误报 | checked/passed/undetermined | 无 CI | 三态折叠/覆盖不明 | E-20（O-T11） | 三态报不出就停 |
| OBDA | 查询结果一致、时延 | 映射/本体版本 | 手写 SQL | 需要 DL/事务写入 | E-20（O-T12） | 需 DL/事务写入就停 |
| 受监管 **gap** | citation precision、strict-pass 违规 | 人签核分钟 | 人工流程/只做检索 | 原 Grid 已移出；不设门槛 | Grid 移出 | 先找新源；不设门槛 |

> `出处` 只许三类：`E-xx`（结论）、`O-xx`（地址：公式/代码/表）、`工程建议`。O 不是结论，是「这条 E/建议的数在哪」（[ADR 0009](../../../adr/0009-object-layer.md)）。标 `gap` 的行不进验收，只作方向。


### 5.2 还缺什么

| 缺口 | 现在有什么 | 缺什么 | 对 02 的影响 |
|---|---|---|---|
| false-veto | E-04/E-13 撤回（W-03） | 按 W-03：shadow 200–500 + 100 条 blocked 标注 + 同轨迹配对 | R6 现为 gap；不能承诺「误拦 ≤5%」 |
| 写路径授权 | 原 Commit Boundary 概念（源已移出）；E-20 无实现 | 一个 mutation class 的实现 + 20–50 false-defer | R9 只能设计 |
| 第二 read-path | trustgraph 一个；外部扫描有 sparql-guard 候选（未入库） | 第二实现（入库）+ harness 调用点 + 泄漏率/时延 | R8 保持条件性；不升第七时刻 |
| 接地等级校准 | E-03 撤回（W-02） | 按 W-02：每级 100–200 条独立标注 | R4 现为 gap |
| 跨域效度 | 单工厂/单基准/专有数据 | 更多独立域/基准 | R1–R7 阈值要重标 |
| 独立复现 | 本份所引 E-01–E-20 无一为 `已证` | 仓库外复现 + EXP 指针 | 所有效应量仍是 `已核`/`推测` |
| 单位成本 | 公式有，单价空 | 人周价/审批分钟价/事故成本 | 不能出 build/buy 点估计 |
| 跨运行确定性 | 设计提案 | 实现 + 度量 | 不写成 R |
| 多智能体共享本体 | 空白 | 可判定设计 + 证据 | 不写成 R |

**这些不是本交付物的前置**；它们是下一步研究/工程的方向。


<a id="13-期待与数据需求验收规格"></a>
### 5.3 期待与数据需求（验收规格）

> 这一节不是结论，是**每条 recipe 的验收规格**：把「做完应该看到什么」写成可证伪的句子，再倒推要量什么。数据缺在哪里，就回 `topics/` 或 `frontier` 补。这是验收规格（非 E）。

| Recipe | 期待（可证伪） | 支持它需要的数据 | 现在的来源 | 缺口 |
|---|---|---|---|---|
| R0 | 四项检查能预测「能不能执行」 | 30–60 分钟检查 + 后续失败记录 | 工程配方 | 无对照 |
| R1 K1 | 绝对 `primary-trap avoidance ≥0.90` **或** 相对 `K1−K0 ≥+10pp`（预注册一个，不要混用） | K0/K1 回放；3 任务；trap 标注 | E-12 | 跨域 |
| R2 投影 | K2 相对 K1 ≥ +5pp，且 ≤60k 字符、维护 ≤2 人周/月 | K1/K2 回放；字符；维护工时；顺序消融 | E-12 | 跨域；多设备 |
| R3 编译 | `p_h ≥ p_min`，p95 不超预算 | `p_h`/miss/`c`/`Q`/p95/span 覆盖 | E-14 | 自己的流量 |
| R4 证据契约 **gap** | **按 W-02 重测；原门槛作废** | 200 题；检索率/引用率；每级 100–200 标注 | E-03 withdrawn | 新源；等级校准；句级 span |
| R5 checker **gap** | **按 W-01 重测；原门槛作废** | 200 题分层；catch/FA/净修复 | E-02 withdrawn | 新源；自己的故障分布 |
| R6 动作闸 **gap** | **按 W-03 重测；原门槛作废** | shadow 200–500；100 blocked；同轨迹配对 | E-04/E-13 withdrawn；E-15 仅参照 | 新源；false-veto；同轨迹配对 |
| R7 记忆 | CMR/Acc@complete ≥ +10pp，merge precision ≥90% | registry on/off；200 units；三层评测 | E-05/E-17 | 自己的域；传播 |
| R8 读路径 | 泄漏率 0（含 object 方向），误拦可接受 | 第二实现；异常/对象用例；延迟 | E-20 | 第二实现/调用点 |
| R9 落盘授权 | false-defer ≤20%，unresolved ≤10%，审计可追 | 一个 mutation class 实现；20–50 样本 | 概念 | 实现；标签 |
| R10 离线 SHACL | 负例 100% 检出、干净误报 ≤5%、三态可报 | 负例集；派生 vs 手写；CI | E-20 | 派生 shapes 质量 |
| R11 OBDA | 查询结果与手写 SQL 一致；有/无本体消融可解释 | 映射/本体/查询集；SQL 日志 | E-20 | agent 集成/规模 |
| R12 受监管 **gap** | **按 W-05 重测；原门槛作废** | 20–50 held-out；citation precision；签核 | Grid 已移出 | 新源；真实运营商/客户指标 |

**怎么用**：每条期待对应一个 stop line；先量「支持它需要的数据」那一列，量不出来就停在这一步，不要用「平均收益」替代。


### 5.4 读者检查（5 组）

> 逐组勾。**没做就写「未做」，不要写「通过」**。这 5 组不是新结论，是把 §5.1–5.3 变成你能自己核对的动作。

| # | 检查 | 怎么查 | 通过 | 未通过 |
|---|---|---|---|---|
| 1 | R0 四项有结论 | 填 [artifact-pack §1](../appendices/artifact-pack.md) | 四项都有 pass/flag/unknown；unknown 没被当 pass | 回 R0；不要选 recipe |
| 2 | 只选了一条 recipe | 用 [map §2](./map.md) 的分诊表 | 一个错误只落一个「先看」；落了两个就写下优先级 | 回 §2；不要并行 |
| 3 | 接口/数据契约填得出 | 目标 recipe 的「最小数据契约」 | 字段齐；填不出的格标 `untested` 并写上游任务 | 不要写「行业通常」 |
| 4 | 停线与出处对得上 | [canonical §2](./canonical.md) | 主指标/停线/出处/量不出时四列都有值 | 回 canonical；不要自造阈值 |
| 5 | 能说出不能证明什么 | [boundaries](./boundaries.md) + 目标 recipe §「不能证明」 | 至少 3 条「不能证明」+ 1 条反模式 | 回 boundaries；不要承诺效果 |

**五组全过 = 可以交一份 shadow 方案；不等于可以上线。** 上线还要过 [operations/rollout](../operations/rollout.md) 与真实数据。

<a id="12-与另外两份交付物的关系"></a>