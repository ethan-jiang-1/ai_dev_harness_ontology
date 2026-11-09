---
status: draft
updated: 2026-11-09
parent: ../README.md
note: illustrative reconstruction; not a deployment
---

# 附录 C · 端到端示例（示意，不是部署）

> **这是用公开证据拼出的设计走查，不是客户案例。** 场景取自 N&D 的工业设备设定，数字只引用论文已报告值；没有报告的地方写 `[待测]`，不编。
>
> 目的：让读者看到「R0 → 选一条 → 账本 → 两周 shadow → go/no-go」长什么样。它不证明这套组合在真实工厂有效。

## 1. 场景

某工厂冷却水系统，已有：

- 约 42 个 tag、33 个 binding、34 条 assumption、16 个 derivation、24 条 knowledge node（N&D 规模）。
- 3 个高频任务：2 个读数解释（泵出口压力、换热器温差）+ 1 个事故诊断（流量低报警）。
- 一个 9B 级现场模型 + 一个 30B+ 对照；上下文预算约 64k token。
- 历史误判：单位混用（bar/MPa）、tag 别名不一致、把「设计值」当「当前值」。

**目标**：先判断「薄语义层」够不够；不够再做投影；checker 只查结构，不承诺语义。

## 2. Week 0：R0 准入（1 天）

| 检查 | 结果 | 决定 |
|---|---|---|
| 消费者 | 值班问答 agent，读上下文；无写权限 | 可做 R1/R2/R5；不做 R6/R9 |
| 名字/单位 | 3 个任务里 2 个 primary trap 来自单位/别名 | 先做 R1 |
| 声明 | 抽样 50 条，7 条用到未声明属性 | 先补声明，否则 checker 会误报 |
| 覆盖 | 200 题抽样 unknown IRI `[待测]`；估计 >20% | 先补术语，不先做 R4 等级 |
| 执行落点 | 只有 2 条约束有 SHACL；无负例 | R5 暂缓，先补 shape/负例 |

**R0 结论**：`fix_first`。先 R1 + 补声明；R2/R5 排后。

## 3. Week 1：R1（K1）

**数据契约**：

```text
tag: {label: "P-101 出口压力", unit: "bar", aliases: ["泵出口压力","P101-P"], source: "P&ID rev C"}
slot: {entity_type: "pump", slot: "outlet_pressure", unit: "bar"}
```

**做法**：

1. 3 个任务各标 primary trap（单位、设计值/当前值、别名）。
2. K0：地址级标签 + 原始单位；K1：统一 tag/单位/别名。
3. 同一 9B 模型回放 3 任务 × 2 臂；每臂 5 次（噪声地板）。
4. 报 primary-trap avoidance 与 element score，分开报。

**预注册**：

```text
primary: primary-trap avoidance (K1 − K0)
pass: ≥ +10pp（本域工程门；N&D 报告 +54.6pp，单工厂）
stop: < +5pp 或剩余 trap 与深知识无关
```

**结果**：`[待测]`。若 K1 已让 3 个 trap 基本消失 → 停，不建塔；否则进 R2。

## 4. Week 2：R2（可选）

**触发**：K1 后仍有 trap 来自「需要跨节点知识/运行教训」。

**做法**：

1. 从描述记录生成约 45k 字符投影；固定 7 节顺序；每条带 `[node_id]`。
2. 出 `statement_id → node_id` 映射；版本头 `projection_version`。
3. K1 vs K2 回放；加打乱句序对照（N&D：0.777→0.685）。
4. 记录生成/维护工时；投影 ≤60k；维护 ≤2 人周/月。

**预注册**：

```text
primary: primary-trap avoidance (K2 − K1)
pass: ≥ +5pp；投影 ≤60k；映射 100% 可回指
stop: < +5pp、>60k、维护 >2 人周/月
```

**结果**：`[待测]`。若通过，进 R5；若不过，只交付 K1。

## 5. Week 3：R5（checker）

**前置**：补声明；写 5–10 条 shapes + 负例（单位必填、范围、source 必填、矛盾标记、连接完整性）。

**基线**：

- 空结果重试：人工 fault 上 catch 79.2%/FA 0%（E-02）；先跑本域 200 题。
- data-derived check：先上低 FA；curated 先审计/补声明。

**预注册**：

```text
primary: 增量 catch（相对空结果重试）
pass: ≥ +5pp 且 FA ≤15%
cost: per-flagged token/time ≤ 人工审核 1/3
stop: 增量 <5pp 或 FA >15%
```

**结果**：`[待测]`。语义错（意思反了）不归结构 checker；先测 judge 净修复，不默认替换。

## 6. 账本（贯穿）

```text
query ledger: query_id, arm(K0/K1/K2), hit/miss, tokens, latency, rounds,
              gate=pass|flag|unknown, citations
decision ledger: 本例不接写路径；只记 checker flag/人工处置
```

**每周看**：

- primary-trap avoidance + element score（分开）。
- token/问、p95、轮次。
- checker 增量 catch/FA、per-flagged 成本。
- 运行/维护工时。

## 7. Go/No-Go memo（模板）

```text
Scope: 3 tasks, 1 system, 9B + 30B, 5 runs/arm
Baseline: K0 / K1 / K2 / 空结果重试
Primary: ...
Result: point + CI
Stop line: ...
Decision: go R2 | go R5 | stop at K1 | not enough data
Risks: 单系统、答案在文本、维护工时、语义错未覆盖
```

## 8. 这个示例证明什么 / 不证明什么

**证明（设计上）**：

- R0 能在 1 天内把「先做什么」排出来。
- R1 的契约很小，不需要先建整座塔。
- R2/R5 都有明确的 stop；不是「上了再说」。
- 账本能把「平均分」拆成 trap/token/FA/成本。

**不证明**：

- 这套组合在真实工厂有效；所有 `[待测]` 都未测。
- 45k 投影跨设备可迁移；N&D 是单 plant。
- checker 能抓语义错；结构检查对 changes of meaning 为 0%。
- 9B 一定够；N&D 的 9B 带投影 > 750B 不带，但区间约 0.3 宽。

**一句话**：示例只展示「怎么走」，不展示「走了有效」。

**出处**：[projection 机制](../../../topics/03-knowledge/projection/mechanism.md) · [checker 机制](../../../topics/02-judgment/checker/mechanism.md) · [E-02/E-12](../../../topics/conclusions.md)
