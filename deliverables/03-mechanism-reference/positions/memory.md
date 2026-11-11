---
status: draft
deliverable_status: draft
updated: 2026-11-11
position: memory
evidence: [E-05, E-17]
---

# memory：下一轮记得什么

> **一句话**：记忆是**状态**，不是事实集合。本体在这里只做对齐、槽位与印证条件；它不承担自由推理，也不能保证跨运行一致。
>
> **词源**：「agent 记忆 / 跨轮状态 / registry / CMR」是 `local` 工作词，没有标准锚（[规范主干 §4](../../../topics/trunk.md) 已列为缺口）；「本体 / 类 / 属性」有 `N: ISO/IEC 21838-1` 与 `N: W3C OWL 2 Profiles`，但标准不定义记忆机制。

**为什么不是相邻位置**：不是 context（context 只给一次，不保留跨轮状态）；不是 determinism（跨运行，不是跨轮）。

## 1. 机制

两种克制的做法，本体参与程度不同：

| 做法 | 本体做什么 | 机器做什么 | 代表 |
|---|---|---|---|
| 本体只做对齐与印证 | 定义实体、槽位、关系赋值条件；跨期身份由 registry 锚定 | 分层匹配（ID → 规范名 → alias → 语义兜底）；重复观察定向到同一历史 | FIRME（E-05） |
| 本体引导增量归纳 | concept/fact 图增量构建；`CREATE/MERGE/SPLIT` 修订层级 | 事实挂到最具体 concept；`SUPERSEDES`/`CONFLICTS_WITH` 表示更新与冲突 | EvoMemState（E-17） |

关键区分：**关系状态**（事实的有效性/scope/更新/冲突）持久；**推理状态**（当前请求用哪些事实、什么角色）按请求生成，不回写事实。混在一起，结构会随请求漂移，事后答不出「这条为什么被用」。

## 2. 触发、输入、输出

| 项 | 内容 |
|---|---|
| 触发 | 回合结束/新观察进入；跨期文档/对话 |
| 输入 | 对话/文档、CRM/通讯录 head、本体槽位；EvoMem 另需评分器/训练信号 |
| 输出 | registry（canonical_id/aliases）、边（五态/σ）、relational state、reasoning state |
| 下一步 | 下一轮检索/判断按这些状态取事实；写侧 merge/split 另进 commit 门 |

## 3. 能改变什么

- **身份对齐：alias 复用在 registry + 语义兜底之上带来增量。** final-period CMR +7.8–12.1pp（4 settings），human-audit reattachment recall +22.5–29.0pp，semantic matching token −40.3%。`已核`（E-05；专有数据、3 period、无年度周期；token 仅 investor/Opus/final period，不含 registry 构建）
- **状态结构：增益在「会不会用」，不在「检索更多」。** Complete Retrieval 85.6%（与最好 baseline 相当），Acc@complete 70.8/68.5（+11.5/+31.2）；去掉 Relational −8.9/−6.4，去掉 Reasoning −8.0/−15.0，去掉 RL −7.9/−16.4。`已核`（E-17；文本 only、需训练信号；两个 Acc 分属不同基准，不可相减）
- **推理状态可跨系统迁移。** 跨 6 系统 +0.2–4.9pp。`已核`（E-17）

## 4. 拦不住什么 / 失效模式

| 失效 | 说明 | 证据/等级 |
|---|---|---|
| false merge 长期污染 | 一个错 alias 会把后续同名观察路由到错误 anchor；传播幅度未测、无自动回滚 | `推测`（机制推断；E-05 的 merge precision 85.6–97.5%） |
| 过期事实不失效 | 新值覆盖旧值但无版本，历史结论的依据消失 | `推测`（机制推断） |
| 冲突被静默消解 | 把冲突压成单一分数/标签，绕过 unresolved | `推测`（E-17 要求保留冲突） |
| 跨运行不确定 | 跨轮一致 ≠ 同一输入两次运行一致；后者是 determinism，不在这一格 | `已核`（E-17 未测跨运行） |
| 跨模态未测 | 两篇都是文本记忆；文档/图片/artifact 未测 | `已核`（E-05/E-17 的限定） |
| 无训练信号时 reasoning state 不成立 | GRPO 需答案/评分器；固定 self-reflection 可能帮倒忙（50.5→48.9） | `已核`（E-17 的边界） |

## 5. 使能条件

- 多会话、跨期实体知识，身份会变、别名会漂；
- 有稳定 head + canonical 名，能从 CRM/通讯录导出；
- 能接受文本 only；EvoMem 的 reasoning state 另需训练信号；
- 写侧 merge/split 有 commit 门或至少人工队列；没有就不要自动落盘。

## 6. 证据与边界

| 证据 | 等级 | 支持什么 | 不能证明什么 |
|---|---|---|---|
| E-05 | 已核 | registry/alias 的 CMR 增量；本体做对齐与印证 | 通用域；长期污染；跨运行；registry 净效应（无「完全不做对齐」对照） |
| E-17 | 已核 | 两层状态；Acc@complete 提升；去掉状态层掉点 | 跨模态；无训练信号；形式保证（reasoning state 不可形式验证） |

> 不要把 «本体克制» 读成 «本体稳定»：FIRME 的本体是给定的小本体，EvoMem 的本体是持续维护的对象；后者层级错误会传进 relational state，幅度未测。

## 7. 可证伪条件

- 无训练信号的 reasoning state 在同类基准上仍带来 Acc@complete 提升 → 放宽「需训练信号」；
- registry 的净效应被单独识别且为零，alias 增量可归因于语义匹配器 → 收窄 E-05 的机制解释；
- false merge 的长期传播被测量且很小 → 放宽「污染」警告；
- 跨模态记忆复现 CMR/Acc@complete 增益 → 扩大 E-05/E-17 的适用范围。

## 8. 上游指针

- 机制：[memory/mechanism](../../../topics/04-state/memory/mechanism.md) · [identity/mechanism](../../../topics/04-state/identity/mechanism.md)
- 判断：[04-state/README](../../../topics/04-state/README.md) · [conclusions](../../../topics/conclusions.md) E-05/E-17
- 施工：[02 R7（recipes）](../../02-engineering-playbook/recipes/README.md) · [01 能力 7](../../01-capability-status/sections/map.md#22-一张表)
- 长版论证：[附录 §3.4.2](../appendix-constraint-spectrum.md#342-memory状态不是事实集合)
