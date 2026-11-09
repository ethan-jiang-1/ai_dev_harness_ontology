---
status: draft
updated: 2026-11-08
rq: [RQ2, RQ4]
---

# 01 约束派 · 前沿与挖掘

> 活页。稳定判断见 [README](./README.md)；证据见 [src](../../src/)；时刻位置见 [seams](../seams.md#六个时刻)。

## 这一派现在的前沿问题

1. **护栏收益与模型能力反向**（E-04/E-13；E-13 是六点描述性拟合）能否写成可预测的曲线，给出零交叉的部署阈值？
2. **误剪率 / 剪枝率**：POLAR 没有报告；不补这两个数，就算不出护栏的真实代价。
3. **复合动作的可逆性**：单步都可逆，组合可能不可逆；有没有可计算的判定？
4. **提交边界**（`01-L13/L14` 之外的授权判据）：Commit Boundary 自述是概念架构，缺实现与实证；**写路径**是否真的落地？**读路径**已有开源实现（trustgraph），已在 [seams](../seams.md#轴外位置可记录但不是六时刻) 登记为轴外位置 `read-path`；等第二个独立实现再决定是否升第七时刻。
5. **推理期约束**（OntoAct、多 agent 诊断）与动作期约束是否应合为一派？判据来源相同，但介入位置不同。

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

## 候选队列

| 候选 | 为什么重要 | 状态 | 下一步 |
|---|---|---|---|
| POLAR（2610.08082） | 本派最强证据；论文未报 false-veto/剪枝率；阈值敏感性见 digest | 已入档 | 标注 blocked log；补 false-veto |
| Commit Boundary（2610.37407） | 最值得研究的治理命题；但只是设计提案 | 已入档 | 找后续实现/引用 |
| OntoAct（2610.21983） | 推理期条件验证；动作空间压到概念层 | 已入档 | 补覆盖率/审计格式（G1/G4） |
| Agentic Power System（2611.03534） | 真实工业流程的“证据→授权→人决策”链 | 已入档 | 拆治理细节 |
| POLAR 引用链 | 看有没有 follow-up 报告误剪率 | 待扫描 | 雪球一层 |
| CASEL（2610.36570，CBASE 2026） | 后果 + 可逆性 + 歧义的运行时分配；模拟 12 万动作，有害轨迹 14.75%→7.02%；CASEL-NoRev 是 verify-only，15.53% 不能单归因给可逆性路由 | 已入档 | 补 γ_m 实测；主表 τ̂=∞ |
| What Can Be Enforced?（2607.22868） | 可执行安全策略的理论边界；false-block/miss 前沿；静态分不识别闭环效应 | 摘要已读 | 落盘 + 建卡；与 POLAR 对读 |
| Safety monitors for agentic systems（2610.20960） | 运行时监控/安全监视器 | 待扫描 | 读摘要 |
| OpenPort Protocol（2602.20196） | 工具访问的安全治理规范；偏工程 | 待扫描 | 只作 T2 线索 |
| trustgraph（开源） | 读路径 SHACL-AF 策略过滤；写路径 commit gate 仍无 | 已入档 | 验证 fail-open 与对象方向；判断读/写是否两个时刻 |

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

> 2026-11-08 子主题已回写；下一步补 false-veto/剪枝率、T1-only 配对与 Commit Boundary 实现。

1. POLAR 的 false-veto/剪枝率：1,745 条 blocked decisions 缺 harm/授权标签；论文没给，别把 retail 回退当误拦。
2. T1-only vs full 的同轨迹配对（action-gate G3）。
3. 从 POLAR、Commit Boundary 做引用雪球，找后续实现；没有实现就不升 E。
4. 继续评估 What Can Be Enforced?，候选先入本表，不急着建卡。
