# 持久化前 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `commit-gate/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 推理证据 ≠ 授权证据；`UNVERIFIED` 不能当 positive support | 已核（概念） |
| F2 | 提交条件应显式化：证据齐/冲突清/版本有效；批准不跨 mutation 继承 | 已核（设计规范） |
| F3 | 同源检索不是独立确认；「没冲突」不是 positive support | 已核（概念） |
| F4 | 只有设计，没有实现；保证是条件性的 | 已核（概念） |

> `F` 只放判断；接口/字段/成本/stop/替代方案的工程口径放在 [mechanism](./mechanism.md) 的「工程发现 1–4」，不新增 `F` 编号。

## 怎么读

- 想看机制：去 [mechanism.md](./mechanism.md)。
- 想看接口/字段/成本/stop/替代方案的工程口径：去 [mechanism](./mechanism.md) 的「工程发现 1–4」。
- 想看缺什么/下一步：去 [frontier.md](./frontier.md)。

## F1 · 推理 ≠ 授权

- **判断**：能支持假设，不等于有权推动持久化变更；`UNVERIFIED` 可进 Planner，但不能当授权证据。
- **条件**：Commit Boundary 概念架构；无实现。
- **边界**：不是实证效果；只是状态语义。
- **来源**：Commit Boundary §3–5；digest §3。

## F2 · 三条件

- **判断**：证据齐、冲突清、版本有效，三条全过才 commit（实现上前两条聚合成 `PASS`，再验 scope/version）；不满足时 defer，不丢弃证据。
- **含义**：把「冲突已解决」「版本仍有效」写进提交条件，不留给模型自觉；`P_auth` 只对声明的命题/角色/观察域/policy version 有效，不跨 mutation 继承。
- **边界**：冲突清 vs 冲突已标注的降级条件未定。
- **来源**：§4–5；digest §3.1/§3.3/§6.5。

## F3 · 同源不确认

- **判断**：hypothesis 诱导的多个结果不能互相印证；同源 query/hypothesis/source 不算 corroboration；「没检测到冲突」也不是 positive support。
- **含义**：这是 agentic ER 的一类失败模式；dependency-aware lineage 仍是上游漏洞。
- **来源**：§5.3；digest §5。

## F4 · 只有设计

- **判断**：Commit Boundary 自述无实现、无实证；保证是条件性的——依赖域策略充分、promotion 可靠、强制执行等 7 条假设。
- **含义**：只能作设计提案引用，不能作效果证据；false-defer 率未知。
- **来源**：摘要/§8；digest §5。
