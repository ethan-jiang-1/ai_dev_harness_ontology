# 跨轮记忆 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `memory/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 本体在记忆里负责对齐/印证条件，不是自由推理 | 已核 |
| F2 | 身份先于内容；alias memory 提升 CMR，false merge 长期污染 | 已核 |
| F3 | 两层状态（关系 + 推理）比单一事实集更可审计 | 已核 |
| F4 | 增益在「会用」，不在「检索更多」 | 已核 |

## F1 · 本体是克制的

- **判断**：FIRME 用固定 product-topic 本体 + registry 做跨期身份；本体只定义实体/关系/冲突/印证条件，不承担自由推理。
- **证据**：本体改动只影响槽位与条件；不是任意隐含结论。
- **边界**：单一金融域；其他域未测。
- **来源**：FIRME §3–4；digest §3。

## F2 · 身份先于内容

- **判断**：registry 分层匹配 + learned alias；错误匹配会把后续观察路由到错误历史。
- **数字**：alias memory final-period CMR +7.8–12.1 pp（4 settings）；human audit reattachment recall +22.5–29.0 pp；semantic matching token −40.3%；merge precision 85.6–97.5%。
- **边界**：专有数据；10 个月度 period；false merge 难回滚。
- **来源**：Table 3/4, p.7–8；§4–5。

## F3 · 两层状态

- **判断**：关系状态（有效性/scope/更新/冲突）与推理状态（当前请求怎么用）分开；前者本体引导，后者策略生成。
- **数字**：去掉 Relational State：MemSyco −8.9、MemTrap −6.4；去掉 Reasoning State：−8.0/−15.0；去掉 RL：−7.9/−16.4。
- **边界**：文本 only；GRPO 需要答案/评分器。
- **来源**：EvoMemState §4–5；Table 2/3。

## F4 · 会用 > 检索更多

- **判断**：Complete Retrieval Rate 85.6%（MemoryBank 86.4，相当），但 Acc@complete 70.8 vs 36.8；增益在「会用」。
- **数字**：MemSyco Acc@complete 68.5，比最强 baseline +31.2；跨 6 个 memory backend 加 reasoning state +0.2–4.9。
- **边界**：四个记忆基准；开放域长期部署未测。
- **来源**：EvoMemState §5；Table 4。
