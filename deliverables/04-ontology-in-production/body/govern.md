---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# C · 治：权限、来源、审计、输出校验

> 本章回答：怎么让“能答”变成“敢用”。 ｜ 读完你应该能：写出治理接口，而不是在上线前补一条审批。

## C.1 权限：先分“看得见”和“写得了”

| 层 | 问题 | 机制 | 不能当什么 |
|---|---|---|---|
| 标签/分类 | 这列/节点是什么、算哪类敏感 | sensitivity ontology + tagging（Glyph） | 策略判定或执行 |
| 节点级 | 这个实体/关系能不能返回 | 策略图/SHACL-AF post-filter（trustgraph） | 写授权 |
| 写路径 | 这个变更能不能落盘 | commit gate/promotion | 读过滤 |

**E-22（引）+ E-20**：Glyph 只做标签层（Apple 单企业；不产策略、不执行）；trustgraph 是单实现读路径过滤（fail-open/只删 subject）；策略层没有领域来源。**工程候选**：OPA（通用策略引擎；不解析本体/不消费标签；未入 E）。

**做法**：

1. 请求必须带 `user_context`；缺了就 fail-closed（有策略时）。
2. 先做读侧可见性，再做写侧授权；不要把 R8 当 R9。
3. 对 object 方向单独测：敏感节点作为 object 仍可能泄漏。
4. 审计日志记 `policy_version/decision/reason`。
5. 策略层单独补：谁写策略、冲突/默认 allow-deny、策略版本；Glyph 的标签与 trustgraph 的策略图没有接口。

## C.2 来源与时效：每条结论能回指

```text
evidence: {source_id, version, span/page, retrieved_at, valid_from/valid_to}
```

- 没有 `source/version` 的结论，不能进授权证据。
- 时效过期的证据不能当 positive support；要显式标 `stale`。
- 同源检索不算独立确认；`hypothesis_id/source_id` 要进 lineage。

## C.3 输出校验：不要只拦输入

**本轮没有 in-scope 的输出校验来源**；2026-04 的旧预印本已过期，不再引数字。以下只写工程做法。

**做法**：

1. 输出按 schema 校验：类型、必填、引用；
2. 关键结论做 evidence 检查：有没有 citation、citation 是否支持；
3. 高风险输出走 `pass/flag/unknown`，unknown 不自动放行；
4. 输出校验失败要能回退/重试/升级，不是只记日志。

## C.4 失败传播：按接口契约切

外部信号（未入库）：[Graph-Agentic RAG assurance](https://arxiv.org/abs/2609.06391) 把失败链拆成 evidence → retrieval → reasoning → capability/delegation → outcome 五个接口契约，要求 provenance、temporal validity、authorization、uncertainty、recoverability 显式化。

| 契约 | 要显式什么 | 失败时 |
|---|---|---|
| evidence | 来源、版本、时效 | 拒答/降级 |
| retrieval | 查了什么、为什么 | 记录空结果原因 |
| reasoning | 用了哪些事实、什么角色 | 可回放 |
| capability/delegation | 谁授权、能做什么 | fail-closed |
| outcome | 实际发生了什么、能否恢复 | 回滚/审计 |

## C.5 审计与人审

- **审计存储**：谁、何时、基于哪条 claim/policy/version；没有它，事后无法解释。
- **人审**：高风险写路径、低置信合并、异常策略；人审记录要能被查询。
- **回滚**：alias/policy/projection 至少各演练一次；没有回滚不做 enforce。

**行业信号（非 E）**：Netflix ontology-driven observability 的 HN 讨论（131 pts/32 comments，2026-10）同时出现“ontology 是必要形式化”与“企业投入数百万、关系库仍主导”两种经验；单公司/评论，不作 E。

## C.6 治理接口

```text
policy: {policy_id, version, subject, resource, action, effect}
request: {user_context, query/action, snapshot_id}
verdict: {allow|deny|escalate, reason, policy_id, obligations[]}
audit: {who, when, what, evidence[], policy_version, outcome}
```

## C.7 验收 / 停

| 指标 | 工程建议（`推测`） | 停 |
|---|---|---|
| 权限覆盖 | 应受控资源 100% 有策略 | 有资源无策略 → 不上线 |
| 泄漏率 | 0（含 object 方向） | 有泄漏 → 停 |
| provenance | 关键结论 100% 可回指 | 不可回指 → 停 |
| 审计可追 | 谁/何时/依据可查 | 不可查 → 停 |
| 输出校验 | 高风险输出有 verdict | 只记日志 → 不算治理 |
| 回滚 | 演练过 | 没演练 → 不 enforce |

## C.8 不能证明

- 读路径过滤 = 写授权；
- 有策略 = 策略正确；
- 有审计 = 语义正确；
- 单论文/单厂商 = 部署有效；
- 输出校验 = 形式保证。
