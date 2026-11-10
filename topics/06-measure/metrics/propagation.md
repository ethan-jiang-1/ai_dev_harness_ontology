---
status: draft
updated: 2026-11-10
rq: [RQ2, RQ4]
evidence: [E-06]
---

# 跨段传播：单段指标看不见的放大

> 回答：build → query → govern 三段里，哪些故障会跨段、在哪看得见、检测点放哪、成本量级多少。
> 不回答：单段内部的失败归因（[failure-attribution](../failure-attribution/README.md)）、单条机制的效应量（各派 findings）。

## 0. 三句话

- **单段指标会互相掩盖**：build 的 `violations=2` 看起来干净，query 的空结果可能来自缺 tag；govern 的 `skip` 看起来是「不适用」，实际是 object 泄漏。
- **传播不是「错误变多」，是「错误换形态」**：shape 违反 → 查询少行；缺 level → 策略 allow；空结果 → 被当成「没有数据」；`skip` → 审计里写成「未判定」。
- **本页是矩阵 + 协议，不是实测**：没有跨段注入实验；每条路径的证据只到单段/旁证，标 `推测（综合）`。

## 1. 故障矩阵（10 类 × 3 段）

| # | 故障 | build | query | govern | 观测信号 |
|---|---|---|---|---|---|
| 1 | 坏 shape（缺 target） | `conforms=true` 假通过 | 结果看似正常 | 审计无违反 | `targeted=0`；`skipped>0` |
| 2 | 缺 tag | `violations` 可能为 0 | CQ1/CQ3 少行/多行 | level=null → deny（或 skip） | CQ3 计数、空结果分因 |
| 3 | 错 level | shape 通过（类型对） | CQ2 多/少列 | 策略 allow/deny 反 | CQ2 结果、policy decision |
| 4 | 空结果 | — | 0 行 | 被当「没有敏感列」 | 分因表；`ASK` 检测 |
| 5 | 错 join/方向 | — | 0 行或错集 | object 方向泄漏 | `MINUS` 双向、T1 探针 |
| 6 | policy skip | — | — | 表/数据集不判 → 泄漏 | `skip` 与 `reason` |
| 7 | object 泄漏 | — | `SELECT ?col` 含敏感列 | audit `leak_check=failed` | 结果内容，不是行数 |
| 8 | 快照过期 | — | 同题不同分 | 审计无法 replay | `snapshot` 时间戳 |
| 9 | 版本不匹配 | `ontology_version` 缺 | CQ 语义漂移 | `policy_version` 对不上 | 版本三元组 |
| 10 | 超时/放弃 | — | 0 行（假空） | 审计缺 decision | 超时率、gave-up 计数 |

**读法**：同一「0 行」可能是 2/4/5/10 四种原因；同一「allow」可能是 3/6/9 三种原因。**不先把故障定位到段，就不要改 prompt/策略。**

## 2. 四条传播链

```
① 坏 shape ──▶ 0 focus ──▶ query 看似通过 ──▶ govern 无违反记录
② 缺 tag   ──▶ CQ1 少行 ──▶ 被当「没有 PII」──▶ 策略不触发
③ 错 level ──▶ CQ2 多列 ──▶ 策略 allow ──▶ 审计 reason=policy_allow
④ object 泄漏 ──▶ 结果含敏感列 ──▶ 审计 skip ──▶ leak_check=failed
```

**每条链的检测点**：

| 链 | 最早可检测点 | 检测 |
|---|---|---|
| ① | build | 每个 shape 必须有 target；`targeted>0` 才算跑过 |
| ② | build/query | `ASK { ?t a :Email }`；CQ3 计数与 dataset 边 |
| ③ | govern | `tagLevel` vs `colLevel`；policy decision 与 level 对账 |
| ④ | query/govern | T1 探针 + 结果内容检查；不能只看行数 |

## 3. 成本模型（量级，不是报价）

| 段 | 成本项 | 公式/口径 | 参数 | 状态 |
|---|---|---|---|---|
| build | 建模 + shapes + 负例 | `N_table × 建模人日 + N_shape × shape 人日 + 负例` | 2–4 人周建模；3–5 人日 shapes（SFE-O digest E3，`推测`） | 估算 |
| query | 生成 + 执行 + 纠错 | `Q × (生成 + 执行 + trigger × 纠错)` | GGC：单跑 ~30h、选择性 ~33h、全量 ~60h（单卡 3090）；KGVoyager：$2.43/85.6s per run | 有数（单设置） |
| govern | 策略求值 + 审计存储 | `D × (policy eval + audit write)` | 策略求值未测；审计存储按 decision 数 | 未知 |
| 跨段 | 检测 + 返工 | `故障数 × 定位人日 + 返工人日` | 无实测；按故障类型估 | 未知 |

**结论**：唯一有数的是 query 段（且单设置）；build 是估算；govern/跨段是未知。**不要把 GGC 的 30/33/60h 当你的 build 成本，也不要把 KGVoyager 的 $2.43 当生产单价。**

## 4. 检测点与仪表

| 段 | 仪表 | 记录 |
|---|---|---|
| build | `build_report` | `load.parsed`、`violations`、`missing_fields`、`targeted`、`skipped` |
| query | query log | `query_id`、snapshot、executor、0 行原因、2×2 配对 |
| govern | audit record | `decision_id`、`policy_version`、`tag_version`、`reason`、`leak_check` |
| 跨段 | [OpenLineage](../../../src/open-source/openlineage-openlineage/digest.md) | `run_id`、parent run、dataset/version、fault injection flag；`TestRunFacet.status` 是 pass/fail/skip |

**最小要求**：三段都有 `run_id`/`snapshot`/`version`，否则跨段不可 replay；没有 replay，矩阵只是故事。OpenLineage 的 `skip` = not executed，不等于 04 的 `undetermined`；映射时要把 `skip` 放进 `reason`，不能直接当第三态。

## 5. 边界

- **没有跨段注入实验**：矩阵是设计，不是实测；每条路径的证据只到单段/旁证。
- **E-06 是 position paper**：五角色/七变量是诊断词汇，不是量化分布；不能当「传播率」。
- **E-05/identity 的 alias 传播**是旁证：alias 错配沿后续观察传播，无自动回滚，幅度未测（`推测`）。
- **成本只有 query 段有数**：build 是估算；govern/跨段未知。
- **不要写「端到端可观测」**：本页只给检测点；没有生产仪表。

## 6. 下一步

1. **仓库外 EXP**：在 fixture 上注入 10 类故障，跑 build→query→govern，记录哪一段首次可见、传播到哪、能否 replay。`待核`
2. **仪表最小集**：`run_id/snapshot/policy_version/tag_version` 四件；没有就不做跨段比较。
3. **成本**：先量 build 的建模/shape 人日与 govern 的 decision 数；不要用厂商报价。

依据：E-06；[E-05](../../conclusions.md)；[output-validation](../../02-judgment/checker/output-validation.md)、[read-path](../../01-constraint/commit-gate/read-path.md)、[policy](../../01-constraint/policy/mechanism.md)；gap：端到端注入。
