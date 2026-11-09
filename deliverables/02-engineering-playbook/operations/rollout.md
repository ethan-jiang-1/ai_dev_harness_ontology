---
status: draft
updated: 2026-11-09
parent: ../README.md
basis: action-gate/commit-gate/read-path 机制；06/feasibility
---

# 上线与运行：shadow → advisory → enforce

> 本页是工程流程，不是 E。所有门槛都是 `推测`；没有账本/标注时不要跳过阶段。

## 1. 三个阶段

| 阶段 | 系统做什么 | 人能做什么 | 不能做什么 |
|---|---|---|---|
| **Shadow** | 照常执行，旁路记录 gate 决策 | 看分布、标 blocked、算 false-veto | 不能阻断 |
| **Advisory** | 给建议/告警，不改变执行 | 审批/忽略；记录采纳率 | 不能自动拒 |
| **Enforce** | 按策略阻断/降级 | 处理升级/例外 | 不能无回滚 |

**入口**：

- Shadow：有账本 + 基线；不需要标注完。
- Advisory：shadow 的 false-veto/FA 在可接受线内；有人工队列。
- Enforce：advisory 的误拦/漏拦可接受；有回滚/审计；业务 owner 签核。

## 2. 每阶段的出口

| 阶段 | 出口（工程建议） | 不过怎么办 |
|---|---|---|
| Shadow | 能按机制出分布；100 条 blocked 已标；false-veto 有初值 | 补账本/标注 |
| Advisory | 采纳率/误拦/审批量可测；task success 不降 >2pp | 降回 shadow |
| Enforce | 回滚演练过；审计可追；owner 明确 | 不 enforce |

**不要**从 shadow 直接跳 enforce；至少一个完整周期（2–4 周）的 advisory。

## 3. 回滚

| 机制 | 回滚动作 | 前提 |
|---|---|---|
| R2 投影 | 回上一 `projection_version`；冻结生成器 | 版本/映射表 |
| R5 checker | 关 flag/降级为提示 | 开关 + 基线 |
| R6 动作闸 | 关 veto，降 advisory；清缓存 | 决策日志 + 审批队列 |
| R7 记忆 | 回滚 alias 集；停 merge/split 写 | alias 版本 + 审计 |
| R8 读路径 | 关策略/回上一 policy_version；清缓存 | 策略版本 + 缓存 |
| R9 commit gate | 停写路径；defer 队列保留 | 事务/审计 |
| R12 受监管 | 回上一法规/工具版本；停签核流程 | 版本/签核记录 |

**回滚要演练**，不是写在文档里。alias/策略/投影至少各跑一次。

## 4. 审批队列

| 项 | 建议 |
|---|---|
| owner | 具名团队，不是「平台」 |
| SLA | 按风险分级；高风险 1 小时内 |
| 批量 | 同类合并；保留单条理由 |
| 疲劳指标 | 队列长度、平均等待、跳过率、复议率 |
| 例外 | 白名单/临时授权；到期自动失效 |
| 审计 | 谁、何时、基于哪条证据/策略 |

**审批率 >15% 或队列持续积压 → 降级/停**（工程建议）。审批疲劳未建模；不要只看 HSR。

## 5. 版本契约

```text
artifact: {kind: ontology|projection|shapes|policy|prompt|model|registry,
           id, version, hash, generated_at, supersedes, valid_from}
```

- 每次变更递增版本；旧版本保留以支持审计/回滚。
- `snapshot_id` 绑定同一次决策用到的 ontology/policy/evidence/version。
- 生成物只读；手工修改视为故障。

## 6. 事故响应

| 事件 | 第一动作 | 后续 |
|---|---|---|
| false-veto 投诉 | 关/降 gate；保留日志 | 标 blocked；修 T1–T5/阈值 |
| 数据泄漏 | 关读路径/清缓存 | 查 object 方向/策略异常；补测试 |
| false merge | 停 merge/split；回滚 alias | 查 registry/阈值；补人工队列 |
| 过度阻断 | 降 advisory | 查 false-veto/审批率 |
| 版本错配 | 停写；回 snapshot | 修版本契约/重放 |

## 7. 角色（RACI 简版）

| 角色 | 负责 |
|---|---|
| 机制 owner | 失效形态、主指标、stop line |
| 平台/评测 owner | 账本、基线、噪声、复算 |
| 域 owner | 本体/投影/policy、curator 权重 |
| 审批 owner | 队列、SLA、例外 |
| 独立复核 | FA/false-veto 抽检，不能由机制 owner 兼 |

## 8. 反模式

1. **没有 shadow 就 enforce。** 误拦不可见。
2. **没有回滚就上线。** 出事只能关系统。
3. **审批队列无 owner。** 积压退化成橡皮图章。
4. **版本不绑定 snapshot。** 审计答不出「当时用的是哪版」。
5. **把 advisory 当 enforce。** 建议不被执行，不等于机制有效。

**出处**：[action-gate 机制](../../../topics/01-constraint/action-gate/mechanism.md) · [commit-gate 机制](../../../topics/01-constraint/commit-gate/mechanism.md) · [06/feasibility](../../../topics/06-measure/feasibility/mechanism.md)
