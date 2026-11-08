# 动作前拦截 · 发现（F）

> 只放**已经能站住**的判断。每条带等级、条件、反例/边界、来源。
> `F` 编号是子主题局部编号；跨页引用写 `action-gate/Fx`。

## 索引

| ID | 判断（一行） | 等级 | 详细 |
|---|---|---|---|
| F1 | 可逆性可以做成类型化判据（T1–T5 + 反向搜索），比 LLM judge 可审计 | 已核 | [F1](./findings/reversibility.md#f1) |
| F2 | 约束收益随基线能力上升而下降；强模型/retail 常回退 | 已核 | [F2](./findings/reversibility.md#f2) |
| F3 | T1-only ≈ blanket veto；结构反向组合的贡献未隔离 | 已核 | [F3](./findings/reversibility.md#f3) |
| F4 | 可逆性 ≠ 安全性 ≠ 授权；合法用户意图可能被误拦（误拦率未测） | 推测 | [F4](./findings/authorization.md) |
| F5 | 多模式分配是 harm–approval 前沿上的取舍：HSR 降、审批升、task success 降；不是单轴支配（模拟） | 已核 | [F5](./findings/multi-mode.md#f5) |
| F6 | 评估应报 harm–approval–cost 前沿；full ledger 在低审批端仍是前沿点；NoRev 不能当单变量 | 已核 | [F6](./findings/multi-mode.md#f6) |

## 怎么读

- 想看**机制**：去 [mechanism.md](./mechanism.md)。
- 想看**接口/参数/标注协议/成本公式/替代方案/stop 的工程口径**：去 [mechanism 的「工程发现 1–4」](./mechanism.md)。
- 想看**缺什么/下一步**：去 [frontier.md](./frontier.md)。
- 想看**原始论文**：去 `src/papers/2610.08082-polar/` 与 `src/papers/2610.36570-casel/`。
