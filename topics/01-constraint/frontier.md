---
status: draft
updated: 2026-11-07
rq: [RQ2, RQ4]
---

# 01 约束派 · 前沿与挖掘

> 活页。稳定判断见 [README](./README.md)；证据见 [notes](../../notes/)；时刻位置见 [seams](../seams.md#六个时刻)。

## 这一派现在的前沿问题

1. **护栏收益与模型能力反向**（E-04/E-13）能否写成可预测的曲线，给出零交叉的部署阈值？
2. **误剪率 / 剪枝率**：POLAR 没有报告；不补这两个数，就算不出护栏的真实代价。
3. **复合动作的可逆性**：单步都可逆，组合可能不可逆；有没有可计算的判定？
4. **提交边界**（E-05 之外的授权判据）：Commit Boundary 自述是概念架构，缺实现与实证；有没有后续系统真的落地？
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
| POLAR（2610.08082） | 本派最强证据；缺误剪率/剪枝率/阈值敏感性 | 已入档 | 回正文补这三个数 |
| Commit Boundary（2610.37407） | 最值得研究的治理命题；但只是设计提案 | 已入档 | 找后续实现/引用 |
| OntoAct（2610.21983） | 推理期约束；动作空间压到概念层 | 已入档 | 补实验数字与失败模式 |
| Agentic Power System（2611.03534） | 真实工业流程的“证据→授权→人决策”链 | 已入档 | 拆治理细节 |
| POLAR 引用链 | 看有没有 follow-up 报告误剪率 | 待扫描 | 雪球一层 |
| CASEL（2610.36570，CBASE 2026） | 后果 + 可逆性 + 歧义的运行时分配；模拟 12 万动作，有害轨迹 14.75%→7.02%；移除可逆性路由回升到 15.53% | 已入档 | 正文补 simulator 假设与成本模型 |
| What Can Be Enforced?（2607.22868） | 可执行安全策略的理论边界；false-block/miss 前沿；静态分不识别闭环效应 | 摘要已读 | 落盘 + 建卡；与 POLAR 对读 |
| Safety monitors for agentic systems（2610.20960） | 运行时监控/安全监视器 | 待扫描 | 读摘要 |
| OpenPort Protocol（2602.20196） | 工具访问的安全治理规范；偏工程 | 待扫描 | 只作 T2 线索 |

## 入档判据

- 报告 **误剪/漏检** 或 **剪枝率/代价**，而不只是任务奖励。
- 有真实部署的失败复盘，或可复现的授权链。
- 会改变 E-04/E-13 的边界，或推翻“强模型上硬护栏只剩代价”。

## 最近扫描

| 日期 | 范围 | 结果 | 决定 |
|---|---|---|---|
| 2026-11-07 | 本地 20 篇复筛 | POLAR 缺误剪率；Commit Boundary 缺实现 | 两篇进候选队列头 |
| 2026-11-07 | 首轮外部扫描（web） | 4 个候选；CASEL、Enforced 摘要已读 | CASEL 已落盘/建卡；Enforced 待落盘 |

## 本轮计划

> 2026-11-07 首轮扫描已落盘 CASEL；下一步补正文，并评估 What Can Be Enforced?。

1. 读 POLAR 正文，补 `剪枝率 / 误剪率 / 阈值敏感性`，写进卡片与 E-04。
2. 从 POLAR、Commit Boundary 做引用雪球，找 2026 年的 follow-up。
3. 用检索式 1-3 扫一遍，候选先入本表，不急着建卡。
