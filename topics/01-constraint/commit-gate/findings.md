# 持久化前 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `commit-gate/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 推理证据 ≠ 授权证据；`UNVERIFIED` 不能当 positive support | 已核（概念） |
| F2 | 提交条件应显式化：证据齐/冲突清/版本有效 | 已核（设计规范） |
| F3 | 同源检索不是独立确认；「没冲突」不是 positive support | 已核（概念） |
| F4 | 只有设计，没有实现；保证是条件性的 | 已核 |

## F1 · 推理 ≠ 授权

- **判断**：能支持假设，不等于有权推动持久化变更；`UNVERIFIED` 可进 Planner，但不能当授权证据。
- **条件**：Commit Boundary 概念架构；无实现。
- **边界**：不是实证效果；只是状态语义。
- **来源**：Commit Boundary §3–5；digest §3。

## F2 · 三条件

- **判断**：证据齐、冲突清、版本有效，三条全过才 commit；不满足时保留待定，不丢弃。
- **含义**：把「冲突已解决」「版本仍有效」写进提交条件，不留给模型自觉。
- **边界**：冲突清 vs 冲突已标注的降级条件未定。
- **来源**：§4–5；digest §3。

## F3 · 同源不确认

- **判断**：hypothesis 诱导的多个结果不能互相印证；同源 query/hypothesis/source 不算 corroboration；「没检测到冲突」也不是 positive support。
- **含义**：这是 agentic ER 的核心失败模式；dependency-aware lineage 仍是上游漏洞。
- **来源**：§5.3；digest §5。

## F4 · 只有设计

- **判断**：Commit Boundary 自述无实现、无实证；保证是条件性的——依赖域策略充分、promotion 可靠、强制执行。
- **含义**：只能作设计提案引用，不能作效果证据；false-defer 率未知。
- **来源**：摘要/§8；digest §5。
