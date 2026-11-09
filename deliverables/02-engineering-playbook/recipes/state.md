---
status: draft
updated: 2026-11-09
parent: ../README.md
basis: E-05/E-17；identity & memory mechanism
---

# R7 · 跨轮身份/记忆：先 registry，再状态

> 记忆不是「把更多东西存下来」，而是**状态**：事实 + 有效性/scope/更新/冲突 + 当前请求怎么用。身份不是内容问题；没有 canonical ID，后面的冲突、失效、证据都挂不住。

## 目标

让同一实体跨期可对齐，让冲突/失效/来源可保留，让当前请求只取可用子集；避免「同一实体碎裂」与「错误合并长期污染」。

## 适用 / 不适用

| 适用 | 不适用 |
|---|---|
| 跨会话/跨期实体知识（客户、产品、项目） | 实体名稳定、单次会话、无跨期观察 |
| 需要保留冲突/失效/来源 | 只需一次性摘要/检索 |
| 下游判断依赖历史一致性 | 没有稳定 head ID/跨期数据 |
| 能接受写侧人工队列 | 要求全自动 merge/split、零人工 |

## 前提

- 能从 CRM/通讯录/主数据导出稳定 head + canonical name。
- 有跨期文档/对话，能按 period 回填，不跨期合并。
- 有 200–500 份文档/200–500 请求可评测。
- 有 audit/回滚预案；merge/split 写侧只进队列。

## 接缝 / 形态

跨轮 / `compiled`。本体以 **identity registry / 对齐条件 / 冲突表示 / concept–fact 图** 出现；约束中等，能对齐/保留冲突，不能保证语义真值。

## 最小数据契约

```text
registry: {canonical_id, type, normalized_name, aliases[],
           first_seen, last_seen, source_version}

edge: {head_id, target_id, relation, source_indicator(1/2/3),
       observations[], state(五态), score(σ), first/last_seen}

relational_state: {fact_id, validity, scope, supersedes[], conflicts[], concept_id}

reasoning_state: {request_id, used_facts[], roles[], priority[]}
                 # 每请求生成，不回写事实

match_log: {surface, layer_hit, score, anchor, alias_written, period}
```

**匹配顺序**：identifier → normalized name → learned alias → semantic fallback（同类型，score ≥0.8，取最高；否则新注册）。阈值按域重标；0.8 是在 investor T−1 上选的，有调参乐观偏差。

**五态**（N=3）：每 period 每条边至多一次强度/状态更新；连续 miss ≤3 仍是 Stable，第 4 次 miss 才进 Fading，Fading 后再匹配为 Reactivated。`σ_init=0.5`、匹配 +0.2、未匹配 ×0.8、<0.01 归零但边不删。

## 做法（2 周 shadow）

1. **定稳定 head**：从 CRM/通讯录导出 canonical ID + 规范名；冻结「speaker 变、head 不变」。
2. **registry v0**：identifier → normalized name → alias 三级匹配；alias 持久化；semantic fallback 先关、留开关；记录命中层级。
3. **事实/关系状态分存**：200–500 份文档过抽取；按 `head + typed target` 建边；落五态 + σ；`SUPERSEDES`/`CONFLICTS_WITH` 先用人工规则。
4. **评测三层**：
   - 抽取层：hallucination / normalization error / round-trip F1。
   - 身份层：`CMR = MMR × merge precision`；human-audit reattachment recall。
   - 状态层：Complete Retrieval；Acc@complete。
5. **写侧只进队列**：merge/split 不自动落盘；`UNVERIFIED` 只进推理，不授权；每次 match 落日志。
6. **预写 go/no-go + 回滚**：阈值先冻结；alias 回滚脚本/流程当场跑一次。

## 证据

- alias memory 让 final-period CMR **+7.8–12.1pp**（4 settings）；human-audit recall **+22.5–29.0pp**；semantic matching token **−40.3%**（E-05）。
- EvoMemState：Complete Retrieval 85.6%（与最好 baseline 相当），但 Acc@complete **70.8/68.5（+11.5/+31.2）**；去掉 Relational −8.9/−6.4，去掉 Reasoning −8.0/−15.0，去掉 RL −7.9/−16.4（E-17）。
- merge precision 85.6–97.5%（4 settings）；**部分设置已低于 90%**；false merge 污染幅度未测。
- 条件：FIRME 专有投资人数据/3 period/无年度周期；EvoMem 文本 only、需训练信号；不能直接外推。
- **CMR 是跨期匹配率，不是答案正确率**；单看 CMR 会把「合并更激进」误判成进步。

## 成本

| 项 | 量级 | 等级 |
|---|---|---|
| registry/alias store | 1–2 人周 | 推测 |
| 本体/概念图 | 1–2 人周 | 推测 |
| 人审 | 0.5–1 人日/200 条 | 推测 |
| 维护 | 0.5 人日/月 | 推测 |
| GRPO（第二阶段） | GPU/评分器；论文未报 GPU 小时 | 未知 |

## 验收 / 停

| 指标 | 通过线（工程建议） | 停 |
|---|---|---|
| merge precision | ≥90%（按域重标） | <90% → 停/回滚 alias |
| alias 增益 | ≥5pp | <5pp → 停/回滚 |
| Complete Retrieval | ≥80% | <80% → 先修检索 |
| Acc@complete | +10pp 或至少不降 | 无提升/下降 → 停，检查 state 噪声 |
| 冲突 | ≤20% | >20% → 先修冲突 |
| 抽取层 | round-trip/归一化达域内基线 | 未达 → 先修抽取 |
| 训练信号 | 有答案/评分器 | 没有 → 不训 GRPO |
| false merge | 下游错误在可接受线内 | 超线 → 停，先修 registry |

**没有稳定 head ID、无跨期观察、实体名稳定、单次会话 → 不做。**

## 失效模式

- **合并错误。** 两个相似实体被当成一个，历史被污染。
- **拆分错误。** 同一实体跨期碎裂，证据挂不上新版本。
- **别名漂移。** 规范名与持久别名失配。
- **来源/时间丢失。** 无法判断某条关系属于哪个版本。
- **registry 过时。** 本体升级后，旧身份无法对齐。
- **错误合并的传播。** 一个 false merge 会把后续同一 surface form 路由到错误 anchor；幅度未测，无自动回滚。
- **把「没观察到」当「不是同一实体」。** 未匹配只说明当前证据不足，不是否定。
- **把 CMR 当任务成功。** CMR 高不等于 agent 答对；要补任务级指标。
- **把 Reasoning State 当形式保证。** 它是自然语言/结构化规则，不可形式验证。

## 写侧边界

- merge/split 授权归 [R9](constraint.md#r9--落盘前授权现在只能设计不要声称已落地)。
- `UNVERIFIED` 可进 Planner，但不构成授权证据。
- 同源检索不算独立确认；「没检测到冲突」不是 positive support。
- 两阶段：Phase 1 授权 proposed；Phase 2 验证 realized；同 snapshot。

## 可抄锚点

- [identity 机制](../../../topics/04-state/identity/mechanism.md) 的 registry/edge/match 契约、冷启动、stop。
- [memory 机制](../../../topics/04-state/memory/mechanism.md) 的 relational/reasoning state、三层评测、五态。
- FIRME 的匹配顺序/alias 复用；EvoMem 的 state 分层；不要抄 0.8 阈值跨域。

**出处**：[identity 机制](../../../topics/04-state/identity/mechanism.md) · [memory 机制](../../../topics/04-state/memory/mechanism.md) · [E-05/E-17](../../../topics/conclusions.md)
