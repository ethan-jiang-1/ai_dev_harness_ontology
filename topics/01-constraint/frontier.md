---
status: draft
updated: 2026-11-12
rq: [RQ2, RQ4]
---

# 01 约束派 · 前沿与挖掘

> 活页。稳定判断见 [README](./README.md)；证据见 [src](../../src/)；时刻位置见 [seams](../seams.md#六个时刻)。

## 这一派现在的前沿问题

> 2026-11-12 注：下文引用的 E-04/E-13 已随源撤回（[审计](../../meta/audits/2026-11-11-source-purge.md)）；问题仍开放，证据待过门新源。

1. **护栏收益与模型能力反向**（原 E-04/E-13，已撤回）能否写成可预测的曲线，给出零交叉的部署阈值？
2. **误剪率 / 剪枝率**：POLAR 没有报告；不补这两个数，就算不出护栏的真实代价。
3. **复合动作的可逆性**：单步都可逆，组合可能不可逆；有没有可计算的判定？
4. **提交边界**（`01-L13/L14` 之外的授权判据）：Commit Boundary 自述是概念架构，缺实现与实证；**写路径**是否真的落地？**读路径**已有开源实现（trustgraph），已在 [seams](../seams.md#轴外位置可记录但不是六时刻) 登记为轴外位置 `read-path`；等第二个独立实现再决定是否升第七时刻。
5. **推理期约束**（OntoAct、多 agent 诊断）与动作期约束是否应合为一派？判据来源相同，但介入位置不同。
6. **访问控制策略层**：标签层有 Glyph，执行层有 trustgraph；但策略语言/冲突消解/默认策略/审计没有来源（[access-control G1/G2](./access-control/frontier.md)）。

## 信号源

- **Benchmark**：τ²-bench（POLAR 的主战场）、AgentBench、工具安全/权限类评测。
- **会议/期刊**：NeurIPS、ICML、ICLR、ACL、EMNLP；安全与形式化方法侧（CAV、FAccT）也值得扫。
- **实验室/团队**：POLAR 作者（韩国）、OntoAct（首尔大学）、Commit Boundary（DIO/ODI 线）。
- **工程侧**：agent 授权、tool permission、human-in-the-loop 审批的产品复盘。
- **arXiv**：cs.AI / cs.SE / cs.LG / cs.CR。

## 检索式

- `ontology guardrail tool calling agent`
- `reversible action authorization LLM agent`
- `commit boundary agent entity resolution`
- `risk-aware tool pruning ontology`
- `agent permission model least privilege`

## 候选队列（2026-11-12 按 [清除审计](../../meta/audits/2026-11-11-source-purge.md) 对账）

> 「已移出」= 原源未过准入，不再撑任何判断；方向仍开放，按五门找新源。「G1 不过」= 首公开早于 2026-06-01，除非有窗口内新版本，不建卡。

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| POLAR（2610.08082） | 曾是本派最强证据；未报 false-veto/剪枝率 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-08082)：单机构） | 方向开放：找报误剪率/剪枝率的过门新源 |
| Commit Boundary（2610.37407） | 最值得研究的治理命题；仅设计提案 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-37407)：单作者/质量 C） | 找窗口内实现与独立采用 |
| OntoAct（2610.21983） | 推理期条件验证；动作空间压到概念层 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2610-21983)：单机构/模拟） | 推理期约束方向待新源 |
| Agentic Power System（2611.03534） | 真实工业流程的“证据→授权→人决策”链 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2611-03534)：公司自证） | 找有独立采用的版本 |
| POLAR 引用链 | 看有没有 follow-up 报告误剪率 | 待扫描 | 雪球一层；只收过门者 |
| CASEL（2610.36570，CBASE 2026） | 后果 + 可逆性 + 歧义的运行时分配；模拟 12 万动作，有害轨迹 14.75%→7.02%；CASEL-NoRev 是 verify-only，15.53% 不能单归因给可逆性路由 | 已入档（probation） | 补 γ_m 实测；主表 τ̂=∞ |
| What Can Be Enforced?（2607.22868） | 可执行安全策略的理论边界；false-block/miss 前沿 | 已移出（[tombstone](../../meta/audits/2026-11-11-source-purge.md#src-2607-22868)：单作者无采用） | 理论边界方向待合格新源 |
| Safety monitors for agentic systems（2610.20960） | 运行时监控/安全监视器 | 待扫描 | 读摘要；先过五门再建卡 |
| OpenPort Protocol（2602.20196） | 工具访问的安全治理规范 | G1 不过（2026-02 首公开） | 除非窗口内新版本，不建卡 |
| trustgraph（开源） | 读路径 SHACL-AF 策略过滤；写路径 commit gate 仍无 | 已入档 | 验证 fail-open 与对象方向；判断读/写是否两个时刻 |
| ontology-rag-firewall（cloudbadal007） | OWL/SHACL 防火墙验合同条款、拦 agent 动作；read-path/checker 候选 | signal（G2 单作者、G3 无独立采用；11 star/2 fork） | 不建卡；read-path 第二实现候选，待独立采用再过门 |
| OPA（开源） | 通用策略引擎；补访问控制策略层；不解析本体/不消费 Glyph 标签 | 已入档（adjunct） | 接 label→policy、冲突/审计测试 |

## 入档判据

- 报告 **误剪/漏检** 或 **剪枝率/代价**，而不只是任务奖励。
- 有真实部署的失败复盘，或可复现的授权链。
- 会改变 E-04/E-13 的边界，或推翻“强模型上硬护栏必然更好”的单向判断。

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-07 | 本地 20 篇复筛 | POLAR 缺误剪率；Commit Boundary 缺实现 | 两篇进候选队列头 |
| 2026-11-07 | 首轮外部扫描（web） | 4 个候选；CASEL、Enforced 摘要已读 | CASEL 已落盘/建卡；Enforced 待落盘 |
| 2026-11-08 | 01 派子主题回写 | 修正 L4/L7/L9/L10/L11 与计数；解除 Commit Boundary 的 E-05 错挂 | 回写 `claims.md`/README；遗留见下 |
| 2026-11-09 | 开源侧（trustgraph） | 读路径授权有实现、写路径仍无；F5 入档 | 补 fail-open/对象方向验证 |

## 本轮计划

> 2026-11-12 对账后：POLAR/Commit Boundary/OntoAct/Enforced 均已移出，原「补数」计划作废；方向保留，证据按五门重找。

1. **false-veto/剪枝率**：找窗口内报告这两个数的过门新源（研究 + 工程复盘并重）；没有就不升 E。
2. **读路径第二实现**：trustgraph 之外找独立实现 + harness 调用点，再决定是否升第七时刻。
3. **策略层**：OPA 接 label→policy 的冲突/审计测试；领域策略来源仍缺（access-control G1/G2）。
4. 引用雪球只收过门者；候选先入本表，不预建卡。
