---
id: EXP-006
status: draft
experiment_status: 设计中
updated: 2026-11-08
rq: [RQ4]
targets: [E-02, 02-L6]
artifact: pending（checker 实现与题库在仓库外）
---

# EXP-006 · Ontology Catch checker：先超过空结果重试

## 要回答什么

在 200 题本方 KG 上，**data-derived checker** 相对「空结果重试」基线，能否提供 **≥5pp 增量 catch**（有结果但答错），且 FA ≤10%、per-1k 成本 ≤人工审核的 1/3？

## 会推翻什么

| 若结果为 A | 则 |
|---|---|
| 增量 catch ≥5pp、FA ≤10%、成本 ≤1/3 | 可进第二阶段（扩题/在线 A/B）；E-02 的“data-derived 有独立价值”在本域成立 |
| 增量 catch <5pp | 不建 checker；结构检查在本域只值空结果重试 |
| FA >15% | 停；误报修坏超过拦下的错 |
| 语义错为主（changes of meaning） | 换 LLM judge/人工，不用结构 checker |
| 只看 curated 的 catch 高 | 不算数：curated FA 也高，必须同报 FA/成本 |

## 设计

- **变量**：checker = 空结果重试（baseline）vs 空结果重试 + data-derived check。
- **对照**：同一 200 题、同一 KG、同一答案生成器；只加 checker。
- **被控住的混淆项**：
  - 题库分层：真实错误/人工故障/正确题比例**预注册**；不能事后调。
  - 同一 SPARQL 执行环境；同一数据版本；同一 judge。
  - 人工复核 50 条，盲于 arm。
- **主指标**：增量 catch = checker 在「有结果但答错」子集上的额外拦截率（相对空结果重试）；**分母是错误子集，不是 200 题**。
- **次指标**：FA（正确题被 flag）、per-1k token/工时、告警处置时长。
- **非对称代价**：漏检（放过错）vs 误报（改坏对）；分开报，不合成 accuracy。
- **分母/口径**：按题；per-flagged 成本与 per-checked 成本分开；66k 是 per-flagged，不是每答案。

## 样本量与功效

- 先导测错误率；目标 ≥80 个错误。若 200 题只有 20% 错误（40 个），5pp = 2 个错误，CI 不可判；扩到 400–800 题或按错误数累计。
- 所以 5pp 只作**方向性 go/no-go**；要统计结论，需 ≥80 个错误，或按错误数而非题数算。
- 人工复核用于估 precision/FA：目标 100–200 条正确题；50 条只能做 smoke，不能判 FA 门。FA 的 CI 用 Wilson。
- 混合集比例（真实/人工故障）预注册；人工故障占错例 ≥1/3 时 data-derived 的 catch 会被抬高。

## 数据表单

| 字段 | 类型 | 谁填 | 何时填 |
|---|---|---|---|
| `question_id` | string | 平台 | 题库冻结时 |
| `stratum` | real_error/artificial/correct | 题库 owner | 同上 |
| `gold_answer` | text | 题库 owner | 同上 |
| `arm` | baseline/checker | 平台 | 每次运行 |
| `query` | text | 平台 | 每次运行 |
| `result_rows` | int | 平台 | 每次运行 |
| `checker_verdict` | pass/flag/unknown | 平台 | 每次运行 |
| `constraint_id` | string/blank | 平台 | 每次运行 |
| `error_subset` | 0/1 | 题库 owner | 冻结时 |
| `correct` | 0/1 | 双人盲评 | 评分时 |
| `flagged_correct` | 0/1 | 双人盲评 | 评分时 |
| `tokens_in/out` | int | 平台 | 每次运行 |
| `latency_s` | float | 平台 | 每次运行 |
| `review_minutes` | float | 业务 | 若处置 |
| `error_subset_n` | int | 平台 | 统计时 |

## go/no-go

- **go**：增量 catch ≥5pp（错误子集）；FA ≤10%；per-1k 成本 ≤人工审核 1/3；100–200 条复核完成、κ≥0.6。
- **no-go**：增量 <5pp；或 FA >15%；或 per-1k >人工 1/3。
- **FA 10–15%**：不出结论；扩正确题样本后重判，不能二选一。
- **不出结论**：题库 <200；或错误数 <80；或混合集比例未预注册；或 κ<0.6；或成本输入缺失（没有单价/人时价，不能判 per-1k 门）。
- **停止线**：语义错为主 → 换 LLM judge/人工；curated 与数据矛盾未审计 → 先修本体。

## 2 周排期

| 天 | 做什么 | 交付物 |
|---|---|---|
| D1–2 | 冻结 200 题与分层比例；先导测错误率；写 gold/判分 rubric | 题库 v1；错误数预估 |
| D3–4 | 跑空结果重试基线；记录 catch/FA/token/延迟 | baseline 报告 |
| D5–7 | 生成 data-derived summary + declaration/pattern check；同题跑 checker | checker 日志 |
| D8–9 | 人工抽 100–200 条盲评；算增量 catch/FA/Wilson CI | 标注表；指标表 |
| D10 | 出 go/no-go + build/buy/不做 memo | 1 页 memo |

## 会改变哪个决定

- **build / buy / 不做**：过门 → 进第二阶段；不过 → 不建 checker，只保留空结果重试。
- **阈值/流程**：把 FA 预算与 per-1k 成本写进验收；没有空结果基线不立项。

## 回链

- topics：[02/checker](../../topics/02-judgment/checker/mechanism.md) · [02/calibration](../../topics/02-judgment/calibration/mechanism.md)
- digest：[Ontology Catch](../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) §6.5/§6.6
- 结论：E-02；02-L6
