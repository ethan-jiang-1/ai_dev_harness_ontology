---
status: draft
updated: 2026-11-09
parent: ../README.md
basis: E-02/E-04/E-08/E-14/E-18；06/metrics；06/trace
---

# 评测设计：先量噪声，再量效应

> 大多数「机制有效/无效」的争论，不是效应不存在，而是**没有先量噪声、没有预注册、没有分母**。E-18：54% 的 score variance 来自同一配置的重复运行（真实尝试、过 hurdle；排除 hurdle 后 46.1%）。

## 1. 五条硬规则

1. **先量噪声地板。** 同题同配置重复 5 次；效应量小于 CI 宽度 → 写「不可判」，不写「无差异」。
2. **主指标预注册。** 开跑前写死主指标、stop line、反事实、成本单位、样本量；跑完不改。
3. **非对称代价分开报。** catch/FA、拦截/误拦、false-veto/审批，不合成 accuracy。
4. **基线必须是可重跑的。** 空结果重试、未编译 harness、不做 registry、不上护栏；不能写「业界通常」。
5. **报告 completion/cost/calibration。** 缺一项，判分作废（06/metrics 的验收规则）。

## 2. 噪声地板（2 天）

| 步 | 动作 | 产出 |
|---|---|---|
| 1 | 固定 `config_fingerprint` 五轴档位 | 配置卡 |
| 2 | 同题同配置重复 5 次 | 5 个 run |
| 3 | 算 run-to-run 方差占比、CI 宽度 | 噪声报告 |
| 4 | 判断待检效应是否大于噪声带 | go/no-go 前提 |

**没有噪声报告，不跑第二臂。** 5 runs/config 是论文设计（E-18）；预算不够就减题量，不要减 runs。

## 3. 样本量（工程起点，`推测`）

| 机制 | 样本 | 为什么 |
|---|---:|---|
| K1/投影 | 3 任务 × 2 臂；9 任务扩展 | N&D 的任务构造 |
| 编译 | 100–200 问；100–400 条 φ 审计 | `p_h`/miss 分布；φ 区间 |
| 证据契约 | 200 题 | OA-RAG 口径 |
| checker | 200 题 + 50 条人工抽检 | catch/FA 初值 |
| 动作闸 | 200–500 shadow 决策 + 100 条 blocked 标注 | false-veto |
| 记忆 | 200–500 文档 + 200 units + 200 请求 | 三层评测 |
| commit gate | 20–50 条 false-defer 样本 | 契约最小验证 |

**样本量不是保证。** 稀疏事件（false-veto、false merge）需要按预期率算功效；2 周 log-only 不够判 HSR。

## 4. 预注册模板

```text
mechanism: R?
failure_form: 做错|没做|慢|不准|内部没有|输出对了
primary_metric: ?
process_metric: ?
asymmetry_pair: 漏/误
counterfactual: ?
stop_line: ?
sample: n / runs / seeds
cost_unit: per_checked|per_flagged
analysis: paired? CI method? subgroup?
```

**预注册的 stop line 不能跑完再改。** 改了就标 `exploratory`，不能当 go/no-go。

## 5. Shadow vs A/B

| 方式 | 用途 | 限制 |
|---|---|---|
| Shadow | 护栏/写路径；不接线上写权限 | 只能估分布，不能证明任务收益 |
| 回放 | 有历史轨迹；同轨迹配对 | 轨迹选择偏差 |
| A/B | 读路径/供给；按 collection hash 分桶 | 需要流量；不能跨桶污染 |
| 离线标注 | checker/记忆 | 标注偏差；无 ground truth 时只能抽检 |

**动作闸/commit gate 先 shadow**；没有真实状态/授权标签，不做硬 veto。

## 6. 报告模板

```text
n_runs/config, CI, completion, cost, calibration
primary: point + CI
process: ...
asymmetry: catch/FA or block/false-veto, separately
subgroups: model/domain/tool
decision: go|no-go|not enough data
```

**禁止**：

- 用均值代替分布（−38% 是 −91%/+1.9% 的混合）。
- 用 retention 代 false-veto。
- 用 accuracy 代 catch/FA。
- 用单次 run 比较配置。
- 把 `unknown` 并进 pass。

## 7. 出口

| 结论 | 条件 |
|---|---|
| **go** | 效应量 > 噪声带；FA/误拦在预算内；成本可接受 |
| **no-go** | 效应量落在噪声带；或主/过程指标相反且无决策规则 |
| **不出结论** | 成本口径缺项、抽检不足、只有单次 run、`unknown` 太多 |

**不出结论不是失败**；它防止把噪声写成结论。

## 8. 两周 sprint

1. 第 1–2 天：锁口径、配置指纹、成本单位。
2. 第 3–5 天：量噪声地板（5 runs/config）。
3. 第 6–7 天：跑两臂（200 题 × 2 臂 × 5 runs 或 shadow 200–500）。
4. 第 8–9 天：出报表（CI、非对称、成本、completion）。
5. 第 10 天：复算 + go/no-go memo。

## 9. 反模式

1. **先跑再定指标。** 事后挑一个显著的结果。
2. **不量噪声就 A/B。** 效应可能小于 run-to-run。
3. **只报均值。** 掩盖两端与子群。
4. **把 `p_h` 当 φ。** 放行率不是正确率。
5. **把 5 runs 当万能。** 稀疏事件仍需更大样本/更长窗口。
6. **机制 owner 兼评测 owner。** 口径会漂；至少独立复核。

**出处**：[06/metrics](../../../topics/06-measure/metrics/mechanism.md) · [06/feasibility](../../../topics/06-measure/feasibility/mechanism.md) · [E-18](../../../topics/conclusions.md)
