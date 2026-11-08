# 跨轮记忆 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `memory/Fx`。
>
> 工程参数（五态边界/N=3、$100K 与 Rule 3/4、GRPO 配方/60K/seeds）在 [mechanism](./mechanism.md) 的「五态、融合阈值与训练配方」。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 本体在 FIRME 里只负责对齐/印证；「改动只影响槽位」是推断；EvoMem 增量建图并修订层级 | 已核 / 推测 |
| F2 | 在 registry + 语义兜底之上，alias memory 提升 CMR；false merge 是主要风险（污染未测量） | 已核（增量）/ 推测（污染） |
| F3 | 两层状态（关系 + 推理）分开；消融各有贡献，可审计性未验证 | 已核（消融）/ 推测（可审计性） |
| F4 | 增益在「会用」，不在「检索更多」 | 已核 |
| F5 | 评估分三层，抽取保真不能省 | 已核（分层/数字）/ 推测（不可互替） |

## F1 · 本体是克制的；固定性仅限 FIRME

- **判断**：FIRME 用固定 product–topic 本体做短期印证、用 registry 做跨期身份；本体只定义实体/关系/冲突与印证条件，不承担自由推理。EvoMem 的本体不是固定的：它增量建 concept/fact 图，并用 `CREATE/MERGE/SPLIT` 修订层级（digest §3.1）；层级错误会传进 relational state（§5.6）。
- **证据**：FIRME §3.2 的 Rule 4 只借本体把 topic 讨论关联到 product；融合只加引用，topic 与 product 身份不合并。本体最小形态是 product/topic 两类 + `CONTAINS`/`PARENT_OF`（§6.5），且按 use-case 定制（§5.4）。「本体改动只影响槽位/条件、不扩散成推理路径」没有改动对照；维护者与变更流程未定——这是本页架构推断 `推测`。
- **边界**：单一金融域（FIRME）；EvoMem 是个人助手基准；两篇都没有 ontology-change ablation，也没有测 CREATE/MERGE/SPLIT 的错误率与传播幅度。
- **来源**：FIRME §3.2、§5.4、§6.5；EvoMemState §3.1、§5.6、§9；digest §3、§5、§8。

## F2 · 身份先于内容

- **判断**：registry 分层匹配 + learned alias；错误匹配会把后续观察路由到错误历史。
- **数字**：alias memory final-period CMR +7.8–12.1 pp（4 settings）；human audit reattachment recall +22.5–29.0 pp；semantic matching token −40.3%；merge precision 85.6–97.5%。
- **边界**：专有数据；period 口径按数据集分开——investor calls 10 个月度 period，S&P 500 3 个 reporting period；false merge 的检测/回滚未验证（G5 未关），「长期污染」是机制推断、论文未测量（`推测`）。
- **来源**：Table 3/4, p.7–8；§4–5。false merge 的长期污染见 §9 未解决项。

## F3 · 两层状态

- **判断**：关系状态（有效性/scope/更新/冲突）与推理状态（当前请求怎么用）分开；前者本体引导，后者策略生成。消融显示两层各自有贡献；但「更可审计」是结构推断——Reasoning State 是自然语言/结构化规则，不是可形式验证的状态（digest §5.4）。
- **数字**：去掉 Relational State：MemSyco −8.9、MemTrap −6.4；去掉 Reasoning State：−8.0/−15.0；去掉 RL：−7.9/−16.4。
- **边界**：文本 only；GRPO 需要答案/评分器；需要形式可验证状态的域别用（§6.3），形式检查/审计是开放问题（§9）。「可审计」只指字段与状态转移可回放，不是语义真值或形式证明 `推测`；关系状态可检查的是 validity/scope/update/conflict 字段，不是事实真值。
- **来源**：EvoMemState §4–5；Table 2/3；digest §5.4、§9。

## F4 · 会用 > 检索更多

- **判断**：Complete Retrieval Rate 85.6%（MemoryBank 86.4，相当），但 Acc@complete 只有 70.8%（LoCoMo-Refined，较最强 baseline +11.5）/ 68.5%（MemSyco，+31.2）；增益在「会用」。
- **数字**：跨 6 个 memory backend 加 reasoning state +0.2–4.9；两个基准各自的 Acc@complete 与同基准最强 baseline 相比为 +11.5 / +31.2。
- **边界**：四个记忆基准；Acc@complete 是「完整检索」子集上的条件准确率，不是全样本准确率；开放域长期部署未测。旧写法把 LoCoMo-Refined 的 70.8 与另一基准的 baseline 行并列相减，属跨基准拼接，已删；不同基准的 Acc@complete 不能相减。
- **来源**：EvoMemState §5 / Figure 5（Qwen3-8B）；+11.5/+31.2 为与同基准最强 baseline 的差。

## F5 · 评估分三层，抽取保真不能省

- **判断**：FIRME 的评估分三层——CMR、human audit（reattachment recall / merge precision）、extraction faithfulness（round-trip F1）；三层测的不是同一件事，不能互相替代（digest §6.1 第 7 条）。
- **数字**：round-trip F1：investor calls 0.923–0.931；S&P 500 Opus 4.6 0.862–0.865、GPT-5.4-mini 0.786–0.805（每语料 1,000 个参考图，文档由固定 Opus 4.6 生成并共享）。抽取误差：幻觉 3.3–7.4%；归一化误差 investor calls Opus 3.2% / GPT 7.74%，S&P 500 Opus 2.8% / GPT 22.16%——没有 backend 全面占优（GPT 幻觉更低，但 S&P 归一化误差约 8 倍）。
- **边界**：round-trip 测「图→文本→图」重建，不测 registry 匹配，也不测下游答案正确率；S&P 无结构化现金流；参考图是抽样、文档生成器固定。293/300 是 final-period investor/Opus fusion 输出的 evidence-path 审计，不是抽取指标。
- **含义**：CMR 高不能推出答案对（F4 同理）；抽取层坏掉时，上层 CMR/Acc@complete 都建在错图上。部署时三层分开报，先看 round-trip 与归一化误差，再谈身份与状态。
- **来源**：FIRME §4.2、Table 6 / §4.3–4.4、§4.5、§6.1；digest §4.2、§6.1 第 7 条。
