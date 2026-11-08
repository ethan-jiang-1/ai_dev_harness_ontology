# 持久化前 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 位置

变更即将落盘或写入外部系统的那一刻。前面所有环节都是「推理」，这里是唯一「改变世界」的时刻。

## 核心区分

| | 推理证据 | 授权证据 |
|---|---|---|
| 要什么 | 能支持假设 | 证据齐、冲突清、版本有效 |
| 不足时 | 结论标为低等级 | 拒绝 commit |
| 谁定 | 本体定义的证据类型 | 本体定义的授权谓词 |

混成一个判据会得到两种失败：过度保守（推理阶段就要求授权级证据）或错误落盘（推理级证据直接放行）。

## 三段式放行

1. **证据齐**：本体要求的证据类型是否都在场。
2. **冲突清**：已识别的冲突是否被显式解决，而非被忽略。
3. **版本有效**：依据的版本是否仍是当前版本。

三条全过才允许持久化。任何一条不满足时，产出保留在「待定」状态，而不是被丢弃。

## 证据状态机（Commit Boundary）

| 状态 | 含义 |
|---|---|
| `QUARANTINE_EVIDENCE` | 有 admission conflict/indeterminate，暂不可见 |
| `UNVERIFIED` | 可进 Planner 推理；**不是** positive authorization support |
| `P_auth(q_m, ω)` | 对特定命题、观察域、policy version 有授权资格 |
| `PASS` / `BREACH` / `UNKNOWN_EVIDENCE` | 三态结论；`BREACH` > `UNKNOWN` > `PASS` |

## 四条 promotion 规则

- 评估**具体命题**，不是文档相关性/查询匹配。
- 不把 Planner 置信度、LLM `verified` 标签、多个 `UNVERIFIED` 重复当授权证据。
- **不因为 hypothesis 诱导了检索就把结果当独立确认**；同源 query/hypothesis 不算 corroboration。
- 不从「没检测到冲突」推断 positive support。

## 两阶段

Phase 1 授权 proposed mutation；Phase 2 验证 realized candidate；commit 时 scope/version/graph/evidence 必须在同一 snapshot。

## 失效模式

- **授权即全信。** 一次批准覆盖整个会话，后续变更继承该批准。
- **冲突被静默消解。** 系统倾向「选一个」，而不是「记录冲突并阻塞」。
- **版本失效未检测。** 依据在推理期间被更新，落盘时用的是过期证据。
- **待定状态不可见。** 被阻塞的变更没有队列，等于被静默丢弃。
- **把「没有冲突」当「支持」。** 没检测到冲突只是没检测到，不是 positive support。
- **依赖链未记录。** 架构不控制 hypothesis-conditioned retrieval；没有 dependency-aware lineage，promotion 仍可能被污染。
- **Policy/promotion 正确性外包。** 架构只保证「按 contract 执行」，不保证 contract 本身对。

## 与本体 / 回路的关系

本体在落盘前以 **authorization predicates / claim-specific promotion / scope/version** 出现；约束强度强（能阻止持久化），但覆盖率取决于 domain policy。被违反时能报出缺哪条证据/冲突/版本；不能保证 policy 本身正确。

## 关联

- [Commit Boundary digest](../../../src/papers/2610.37407-commit-boundary/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [memory](../../04-state/memory/README.md)
