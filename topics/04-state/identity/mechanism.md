# 身份 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

同一实体在不同来源、不同时期以不同名字出现，被当成多个实体；或者两个相似实体被合并。身份不稳，后面的状态、冲突、失效都挂不住。

## 两种做法

| 做法 | 机制 | 代表 |
|---|---|---|
| registry 锚定 | 固定 product–topic 本体 + 规范身份/持久别名；重复观察定向到同一段历史 | FIRME |
| 时序属性图 | 领域无关本体把对话组织成带时间的事件；append-only 保留演化；检索时消解冲突 | APEX-MEM（摘要级，`待核`） |

## FIRME 的 registry

1. **分层匹配**：identifier → normalized name → learned alias → LLM semantic matching（同类型候选，score ≥0.8，取最高；否则新注册）。
2. **alias 复用**：匹配后的 surface form 加入 anchor 的 alias set；下次直接匹配，减少语义调用。
3. **错误匹配的后果**：后续同名观察会被路由到错误历史；一个 false merge 很难回滚。
4. **本体克制**：本体主要做对齐与印证条件，不承担自由推理。

## 身份变更是 commit 问题

Commit Boundary（概念架构）把「可推理的证据」与「可授权身份变更的证据」分开：

- `UNVERIFIED` 可以进 Planner 推理，但不能授权 merge/split。
- 需要 claim-specific promotion：命题级证据、provenance、角色、scope/version。
- 同源检索不算独立确认；「没检测到冲突」不是 positive support。
- 两阶段 supervisor + 原子 commit：Phase 1 授权 proposed mutation；Phase 2 验证 realized candidate。

## 失效模式

- **合并错误。** 两个相似实体被当成一个，历史被污染。
- **拆分错误。** 同一实体跨期碎裂，证据挂不上新版本。
- **别名漂移。** 规范名与持久别名失配。
- **来源/时间丢失。** 无法判断某条关系属于哪个版本。
- **registry 过时。** 本体升级后，旧身份无法对齐。
- **错误合并的长期污染。** 一个 false merge 会把后续同名观察路由到错误 anchor；merge precision 必须和 CMR 一起看。
- **把「没观察到」当「不是同一实体」。** 未匹配只说明当前证据不足，不是否定。

## 与本体 / 回路的关系

本体在身份层以 **规范 ID / 别名 / 对齐条件 / 类型约束** 出现；约束强度中（能对齐、能约束合并类型，不能保证语义同一）。被违反时通常没有即时信号，错误跨轮累积。

## 关联

- [FIRME digest](../../../src/papers/2610.40482-firme/digest.md)
- [Commit Boundary digest](../../../src/papers/2610.37407-commit-boundary/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
