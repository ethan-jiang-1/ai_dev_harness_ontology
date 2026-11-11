---
status: draft
updated: 2026-11-09
parent: ../README.md
basis: 06/feasibility、06/metrics、06/trace；E-02/E-04/E-08/E-14/E-18
---

# 账本：先记原始记录，再谈指标

> **2026-11-11 证据重置**：本页 basis 中的 E-02/E-03/E-04/E-13 已撤回；相关数字只作历史，不再作为“已测”依据。


> 没有账本，`p_h`、false-veto、审批成本、catch/FA 都算不出来；所有 go/no-go 都退化成「感觉」。
>
> 账本不是「日志」：日志是非结构化流水，账本是**按查询/决策一行、字段稳定、可复算**的数据表。见 [GLOSSARY](../../../GLOSSARY.md)。

## 1. 两本账，不要合成一本

| 账本 | 一行是什么 | 用来算 | 主要 owner |
|---|---|---|---|
| **Query ledger** | 一次查询/回答 | `p_h`、miss penalty、token/问、p95、轮次、err_rate | 检索/上下文平台 |
| **Decision ledger** | 一次动作/审批/回滚 | HSR、false-veto、审批率、task success、`J(m)` | 工具/平台/风控 |

**不要用 query ledger 算 false-veto**：它没有 blocked decision 的合法/伤害标签。**不要用 decision ledger 算 `p_h`**：它没有证据充分率。

## 2. 共用字段（两本都有）

```text
event_id, timestamp, run_id, arm, config_fingerprint, repeat_idx,
cost_unit(per_checked|per_flagged), trace_ref,
model, prompt_version, tool_version, policy_version, ontology_version
```

- `config_fingerprint`：至少含 Information/Reasoning/Verification/Budget/Model 五轴的**档位**，不是轴名；没有它，两次跑分不可比。
- `repeat_idx`：缺了算不出 run-to-run 方差（E-18：54% variance 来自同配置重复）。
- `cost_unit`：缺了会把「per flagged」当「per answer」。
- `trace_ref`：指向 trace/程序/工具调用；没有它，只能看输出。

## 3. Query ledger

```text
query_id, user/session_hash, query_text_ref,
retrieval: {tool, top_k, hit|miss, claim_ids[], chunk_ids[], span_coverage},
tokens: {in, out, total}, latency_ms, rounds,
gate: {verdict: pass|flag|unknown, constraint_id?, err_rate?},
citations: [{doc_id, version, page, span}],
answer_ref, error_type?
```

**必填口径**：

- token 按**每问总量**，不是单次模型调用。
- `hit/miss` 是证据充分性门（`p_h` 的分子/分母），不是「检索到没有」。
- `err_rate` 只对 accepted query 抽样审计；没有审计就写 `unknown`。
- p95 按时延分布算，不用均值代替。

**最小示例**：

```text
q-001, arm=compiled, hit=true, tokens=8.9k, latency=4.2s, rounds=2,
gate=pass, citations=3, span_coverage=0.92
```

## 4. Decision ledger

```text
trajectory_id, step_idx, tool, entity, args_hash,
tier(T1–T5), phi, tau, c_base, p_hat, c_hat, rho, g, d,
J_m?, mode(direct|verify|sandbox|clarify|approve|abstain),
decision(allow|veto|escalate), reason,
approval: {required, approver_hash, minutes, queue_wait},
rollback: {attempted, succeeded, reason},
task_success, harm(0/1/unknown), legal_intent(yes|no|unsure),
false_veto(yes|no|unknown), unavailable(0/1), lawful_completion(0/1),
harm_label_source
```

**必填口径**：

- HSR/harm 按**轨迹**，不是按 step。
- `false-veto` 需要 `blocked=true` + `legal_intent=yes` + `harm=none/low` 三个标签；缺一个就是 `unknown`。
- 审批按**分钟/次**；没有 minutes 就算不出审批成本。
- `p_hat` 必须校准（isotonic/temperature scaling）；不校准，阈值和 `J(m)` 没有意义。
- `gamma_m` 是假设值，不是测量；没有 `gamma` 数据不要算 `J(m)` 点估计，只给敏感性。

**最小示例**：

```text
t-017, step=4, tool=transfer, tier=T4, phi=0, tau=0.8,
decision=veto, reason=no_inverse, approval=0, task_success=0,
harm=unknown, false_veto=unknown
```

## 5. 指标定义（先写分母）

| 指标 | 定义 | 分母 | 常见错误 |
|---|---|---|---|
| `p_h` | 证据充分、可替换的查询比例 | 全部查询 | 把「检索到」当 hit |
| `p_min` | `2% + c/(0.929Q)` | 自有 `c`、`Q` | 用论文 `c=10` |
| `err_rate` | accepted query 中答错的比例 | accepted query 抽样 | 用 `p_h` 代 err_rate |
| catch | 被 checker flag 且确实错的比例 | 人工标注错误 | 与 FA 混成 accuracy |
| FA | 被 flag 但答案正确的比例 | 被 flag 的正确答案 | 用 precision 代替 |
| false-veto | blocked 中「本可合法执行且低 harm」的比例 | blocked decisions | 用 retention/block count 代算 |
| false-block / miss | 合法动作被 block / 违规动作被 allow 的比例 | 合法 / 违规动作 | 只报拦截率；合成 accuracy |
| unavailable | 无法产出可解析决策的比例 | 决策请求 | 把「没判」算成 deny 或 pass |
| HSR | 有害轨迹比例 | 全部轨迹 | 按 step 算 |
| CMR | 跨期匹配率 = MMR × merge precision | incoming edges | 单看 CMR 奖励激进合并 |
| Acc@complete | 完整答案准确率 | 请求 | 与 retrieval recall 混 |
| leak rate | 过滤后仍出现的敏感节点比例 | 应被 block 的节点 | 只测 subject 方向 |

**报告规则**：

- 主指标 + 过程指标并报；非对称代价（漏/误）分开。
- 成本标 `per_checked` 还是 `per_flagged`；换口径即不可比。
- 没有 CI 的比率不要写「显著」；没有重复运行不要写「更好」。
- 任何「门通过率」进 memo，必须同页给 err_rate 或标 `unknown`。

## 6. 保留与安全

| 项 | 建议 | 理由 |
|---|---|---|
| 原始 query/answer | 存 hash + 脱敏文本；原文按 ACL | 含 PII/客户数据 |
| 工具参数 | 存 hash/结构化字段；敏感值脱敏 | 审计 vs 泄漏 |
| 审批人 | 存 `approver_hash`，不存姓名 | 最小化 |
| 保留期 | 90–180 天；审计样本可更长 | 复算/审计 vs 合规 |
| 访问 | 账本只读副本给评测；写权限归平台 | 防止自评篡改 |
| 版本 | schema 版本 + 采集器版本 | 跨季度可比 |

## 7. 最小落地（3–5 天）

1. **锁口径**：token/伤害/审批/成本单位四个口径先写死。
2. **建表**：按上面字段建两本账；先落 7 天历史流量或 200–500 条决策。
3. **回放**：能按 arm/机制出分布；算 baseline 的 token/p95/审批率。
4. **抽检**：100 条 accepted query 估 err_rate；100 条 blocked 标 false-veto。
5. **复算**：换人按同一账本重算，结论一致才算数。

## 8. 反模式

1. **只有日志，没有账本。** 字段不稳定，算不出分母。
2. **两本账合一。** query 与 decision 的分母不同；合了就算错。
3. **用均值代替分布。** 平均 −38% 会掩盖 −91%/+1.9%。
4. **用 retention 代 false-veto。** 保留率不是「拦对了多少」。
5. **缺 `repeat_idx`。** 无法区分效应与 run-to-run 噪声。
6. **缺 `cost_unit`。** 66k per flagged 被当每答案成本。
7. **自评账本。** 机制 owner 兼评测 owner，口径会漂。

## 9. 交接

- 评测设计 → [evaluation](evaluation.md)
- 成本 → [cost](cost.md)
- 上线/回滚 → [rollout](rollout.md)
- 指标分派/噪声 → [06/metrics 机制](../../../topics/06-measure/metrics/mechanism.md)
- 决策账本字段 → [06/feasibility 机制](../../../topics/06-measure/feasibility/mechanism.md)

**出处**：[feasibility](../../../topics/06-measure/feasibility/mechanism.md) · [metrics](../../../topics/06-measure/metrics/mechanism.md) · [trace](../../../topics/06-measure/trace/mechanism.md) · [E-18](../../../topics/conclusions.md)
