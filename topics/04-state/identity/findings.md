# 身份 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `identity/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | registry 分层匹配 + 持久别名能把跨期观察锚到同一段历史 | 已核 |
| F2 | alias memory 是主要增量，semantic fallback 不是唯一来源 | 已核 |
| F3 | false merge 会长期污染，merge precision 必须与 CMR 同看 | 已核 |
| F4 | 身份变更需要独立授权，不能由「可推理证据」直接放行 | 推测 |

## F1 · registry 锚定

- **判断**：固定 product–topic 本体 + 规范身份/持久别名；重复观察定向到同一段历史。
- **证据**：FIRME 4 settings；human-audit reattachment recall +22.5–29.0 pp。
- **边界**：专有金融数据；10 个月度 period；单一本体。
- **来源**：FIRME §4–5；Table 3。

## F2 · alias 是增量

- **判断**：alias memory 提升 final-period CMR +7.8–12.1 pp；semantic matching token −40.3%。
- **含义**：别名复用是省钱机制；只靠语义 fallback 又贵又慢。
- **边界**：alias 与 canonical registry/semantic fallback 的分别贡献未拆分。
- **来源**：Table 3/4, p.7–8。

## F3 · false merge 的长期污染

- **判断**：一个错误匹配会把后续同名观察路由到错误 anchor；merge precision 必须和 CMR 一起看。
- **数字**：merge precision 85.6–97.5%；但错误一旦进入，很难回滚。
- **边界**：无自动回滚机制。
- **来源**：FIRME §5；digest §7。

## F4 · 身份变更是 commit 问题

- **判断**：`UNVERIFIED` 可进推理，但不能授权 merge/split；需要 claim-specific promotion、冲突解决、scope/version 检查。
- **等级**：`推测`（Commit Boundary 是概念架构，无实现）。
- **边界**：没有 false-defer 率；没有工程集成。
- **来源**：Commit Boundary §3–5；digest §3。
