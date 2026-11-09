---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 5. 验收与缺口

> 本章回答：怎么验收、什么时候停、还缺什么。 ｜ 读完你应该能：写出一页 go/no-go memo。

### 5.1 验收与 stop：按机制选尺

| 机制 | 主指标 | 过程指标 | 反事实 | 停线（工程建议，非 E） |
|---|---|---|---|---|
| R0 | 四项检查 pass/flag/unknown | 修复清单 | 无检查直接上 | 任一 unknown 当 pass |
| K1 | primary-trap avoidance | token | K0 | 剩余 trap 与深知识无关 → 停 |
| 投影 | primary-trap/element | 字符数/维护人日 | K1 | <5pp、>60k、>2 人周/月 |
| 编译 | token/问、p95 | `p_h`/miss、`c`、`Q` | 词法检索 | `p_h < p_min` |
| evidence | 准确率、引用率 | 检索率、grounding 校准 | 纯文本 RAG | 检索率 <50% |
| checker | 增量 catch、FA、净修复 | per-1k 成本 | 空结果重试 | catch <5pp、FA >15% |
| action | harm、审批、false-veto、task success | 保留率、φ、miss–false-block 前沿 | 不上护栏 | 在 miss 预算下 false-block 前沿不可接受（不要用单点 5%） |
| memory | CMR、merge precision、Acc@complete | 抽取层误差 | 不做 registry | precision <90% |
| read-path | 泄漏率、误拦 | 延迟 | 不过滤 | fail-open 未修/object 方向未测 |
| commit | false-defer、unresolved、审计可追 | 人审工时 | 直接 merge | >20%、>10%、不可追 |
| 离线 SHACL | 负例检出、干净误报 | checked/passed/undetermined | 无 CI | 三态折叠/覆盖不明 |
| OBDA | 查询结果一致、时延 | 映射/本体版本 | 手写 SQL | 需要 DL/事务写入 |
| 受监管 | citation precision、strict-pass 违规 | 人签核分钟 | 人工流程/只做检索 | 违规 >0、精度 <0.95 |


### 5.2 还缺什么

| 缺口 | 现在有什么 | 缺什么 | 对 02 的影响 |
|---|---|---|---|
| false-veto | E-04 明确未测；blocked log 无 harm/授权标签 | 100 条 blocked 人工标注；同轨迹配对 | R6 只能 shadow；不能承诺「误拦 ≤5%」 |
| 写路径授权 | Commit Boundary 概念；E-20 无实现 | 一个 mutation class 的实现 + 20–50 false-defer | R9 只能设计 |
| 第二 read-path | trustgraph 一个；外部扫描有 sparql-guard 候选（未入库） | 第二实现（入库）+ harness 调用点 + 泄漏率/时延 | R8 保持条件性；不升第七时刻 |
| 接地等级校准 | E-03 自评、未校准 | 每级 100–200 条独立标注 | R4 只能排序/人工分流 |
| 跨域效度 | 单工厂/单基准/专有数据 | 更多独立域/基准 | R1–R7 阈值要重标 |
| 独立复现 | 20 条 E 无 `已证` | 仓库外复现 + EXP 指针 | 所有效应量仍是 `已核`/`推测` |
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
| R1 K1 | 目标域 primary-trap avoidance ≥0.90 | K0/K1 回放；3 任务；trap 标注 | E-12 | 跨域 |
| R2 投影 | K2 相对 K1 ≥ +5pp，且 ≤60k 字符、维护 ≤2 人周/月 | K1/K2 回放；字符；维护工时；顺序消融 | E-12 | 跨域；多设备 |
| R3 编译 | `p_h ≥ p_min`，p95 不超预算 | `p_h`/miss/`c`/`Q`/p95/span 覆盖 | E-14 | 自己的流量 |
| R4 证据契约 | 检索率 ≥50%，引用率 ≥85%，grounding 可校准 | 200 题；检索率/引用率/等级标注 | E-03 | 等级校准；句级 span |
| R5 checker | 增量 catch ≥5pp、FA ≤15%、净修复 >0 | 200 题；空结果基线；catch/FA/per-1k/净修复 | E-02 | 自己的故障分布 |
| R6 动作闸 | 在 miss 预算下报 false-block 前沿；低 miss 不能靠 block-all；harm 降，task success 不降 >2pp | 200–500 shadow；100 blocked 标注；四轴指标 + 前沿 | E-04/E-15；[E5 校准理论](../../01-capability-status/data/e5-calibration-theory.md) | false-veto；同轨迹配对 |
| R7 记忆 | CMR/Acc@complete ≥ +10pp，merge precision ≥90% | registry on/off；200 units；三层评测 | E-05/E-17 | 自己的域；传播 |
| R8 读路径 | 泄漏率 0（含 object 方向），误拦可接受 | 第二实现；异常/对象用例；延迟 | E-20 | 第二实现/调用点 |
| R9 落盘授权 | false-defer ≤20%，unresolved ≤10%，审计可追 | 一个 mutation class 实现；20–50 样本 | 概念 | 实现；标签 |
| R10 离线 SHACL | 负例 100% 检出、干净误报 ≤5%、三态可报 | 负例集；派生 vs 手写；CI | E-20 | 派生 shapes 质量 |
| R11 OBDA | 查询结果与手写 SQL 一致；有/无本体消融可解释 | 映射/本体/查询集；SQL 日志 | E-20 | agent 集成/规模 |
| R12 受监管 | citation ≥0.95、strict-pass 违规 0、签核可追 | 20–50 单；citation/state/签核 | Grid | 真实运营商/客户指标 |

**怎么用**：每条期待对应一个 stop line；先量「支持它需要的数据」那一列，量不出来就停在这一步，不要用「平均收益」替代。


<a id="12-与另外两份交付物的关系"></a>
