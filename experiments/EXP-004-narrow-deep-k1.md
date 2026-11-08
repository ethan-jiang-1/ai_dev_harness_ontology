---
id: EXP-004
status: draft
experiment_status: 设计中
updated: 2026-11-08
rq: [RQ5]
targets: [E-12, 03-L1]
artifact: pending（实现产物在仓库外；本文件只放协议）
---

# EXP-004 · N&D K0/K1/K2：命名+单位够不够，塔值不值

## 要回答什么

在本厂一台设备上，**K2（塔+投影）相对 K1（命名+单位）的 primary-trap avoidance 是否 ≥15pp**；同时 **K1 相对 K0 是否已拿到大部分收益**？

## 会推翻什么

| 若结果为 A | 则 |
|---|---|
| K2−K1 ≥ +15pp，且 ≥2/3 任务同向 | **进全塔建设**；E-12 的“塔再 +19.8pp”在本厂成立（K2 臂是 1/10 试点塔） |
| K2−K1 < +5pp | **不建塔**；只做 K1 命名+单位，预算转治理 |
| K2−K1 在 5–15pp | 证据不足；扩任务到 6–9 个再判，不建塔 |
| K1−K0 < +5pp 且 K2−K1 也 <5pp | 命名与塔都不够；先修数据/任务，不立项 |
| K1−K0 很大但 K2−K1 很小 | K1 是主收益；塔的边际不值，支持“先做 K1” |
| 只有 1 个任务同向 | 任务是特例；不外推，回到任务选择 |

## D0 gate（D1 前签核）

- 1 台设备 + 3 个任务卡（ground truth/trap/rubric）。
- 3 人：1 curator（K2 1/10 塔）、1 后端（投影/日志）、1 领域工程师（任务/评分）。
- K1 命名/单位审计清单；K2 1/10 塔范围（162 节点）与 45k 投影生成器。
- 盲评人 2 名 + 仲裁 1 名；judge 版本/温度/prompt 冻结。
- 任一不过 → 本 2 周只交付任务卡/塔/投影，不跑 54 trials。

## 设计

- **变量**：上下文 = K0（原始描述/日志）vs K1（tag 名、单位、binding 校正）vs K2（K1 + 塔/投影，45k 字符）。
- **对照**：同设备、同任务、同 prompt、同 judge、同 rubric；只换上下文。
- **被控住的混淆项**：
  - 模型：9B 与 30B+ 各一，固定版本/温度（温度写进预注册；不要用 0 当“稳”）。
  - 任务：3 个“答案在文本里”的任务（2 读数解释 + 1 事故诊断）；任务卡先冻结。
  - 顺序：K0/K1/K2 轮转，避免疲劳/顺序效应。
  - judge：同一模型 + 双人盲评 30 条；judge 不知道 arm。
- **主指标**：K2−K1 的 primary-trap avoidance（绝对 pp）。
- **次指标**：K1−K0（命名/单位的独立贡献）；element score；token/问、轮次、时延。
- **非对称代价**：把“陷阱已避开”误判为“没避开”（保守）vs 把“没避开”误判为“避开”（危险）；评分表分开记。
- **分母/口径**：按任务×模型×seed；pooled 只作方向，逐任务/逐模型必报。

## 样本量与功效

- 有效样本单位是**任务数 3**，不是 trial；模型也只有 2 个，不能推断模型总体。
- 每 arm：3 任务 × 2 模型 × 3 seeds = 18 trials；三 arm 共 54 trials。
- 3 任务等权时，一个任务从全错到全对可把 pooled 拉约 33pp；15pp 线挡不住单任务驱动。
- 所以 15/5 只作**方向性 go/no-go**；要统计结论，需扩到 6–9 任务，或把任务当随机效应。
- 若 3 seeds 的 task-level 方差 > 10pp，先扩任务，不扩 seed；温度/采样参数写进预注册。

## 数据表单

| 字段 | 类型 | 谁填 | 何时填 |
|---|---|---|---|
| `task_id` | string | 领域工程师 | 任务卡冻结时 |
| `task_type` | reading/diagnosis | 领域工程师 | 同上 |
| `ground_truth_elements` | list | 领域工程师 | 同上 |
| `primary_trap` | string | 领域工程师 | 同上 |
| `rubric_version` | string | 领域工程师 | 同上 |
| `prompt_version` | string | 平台 | 预注册时 |
| `model` | string/version | 平台 | 每次运行 |
| `temperature` | float | 平台 | 预注册时 |
| `arm` | K0/K1/K2 | 平台 | 每次运行 |
| `seed` | int | 平台 | 每次运行 |
| `context_hash` | string | 平台 | 每次运行 |
| `answer` | text | 模型 | 每次运行 |
| `rater1_trap` | 0/1 | 评审 A | 评分时 |
| `rater2_trap` | 0/1 | 评审 B | 评分时 |
| `adjudicated_trap` | 0/1 | 仲裁 | 分歧时 |
| `judge_trap` | 0/1 | judge | 评分时 |
| `element_score` | 0–1 | 双人盲评 | 评分时 |
| `tokens_in/out` | int | 平台 | 每次运行 |
| `latency_s` | float | 平台 | 每次运行 |
| `disagreement` | 0/1 | 复核人 | 评分后 |

## go/no-go

- **go（建塔）**：K2−K1 的 pooled primary-trap avoidance ≥ +15pp；≥2/3 任务同向；3 seeds 同向；双人评分 κ≥0.6。
- **no-go（不建塔）**：K2−K1 < +5pp；或 3 seeds 方向不一致。此时只做 K1。
- **命名不够（单独分支）**：K1−K0 < +5pp，且 K2−K1 < +5pp → 先修数据/任务，不立项。
- **不出结论**：K2−K1 在 5–15pp；或任务数 <3；或 κ<0.6；或温度/采样未预注册。
- **停止线**：K1 的命名/单位审计无法独立完成（混杂别的变更）；或 K2 投影无法由同一描述记录重建 → 停。

## 2 周排期

| 天 | 做什么 | 交付物 |
|---|---|---|
| D1–2 | 选 3 任务；写 ground truth/trap/rubric；单位/命名审计；定 K2 1/10 塔范围 | 任务卡 3 份；K1 变更清单；K2 范围 |
| D3–4 | 固化 K0/K1/K2 上下文；冻结 prompt/model/judge/温度；10 条预跑 | 上下文 hash；预注册表 |
| D5–7 | 跑 54 trials（3 arm × 2 模型 × 3 seeds × 3 任务） | trial log |
| D8–9 | 双人盲评 + 30 条 judge 校准；算逐任务/逐模型 + κ | 评分表；κ |
| D10 | 出 go/no-go；写“全塔/只 K1/修数据”memo | 1 页 memo |

## 会改变哪个决定

- **build / buy / 不做**：K2−K1 过线 → 建塔；否则只做 K1；命名不够 → 先修数据。
- **阈值/流程**：把“先做 K1、再测 K2 边际”写进本体建设流程；无 K1 审计不立项建塔。

## 预注册（v0，D0 后冻结）

- `protocol_version`: v0；`frozen_at`: pending D0；`frozen_by`: 待签。
- **H1**：K2−K1 的 pooled primary-trap avoidance ≥ +15pp。
- **H0**：K2−K1 < +5pp（塔的边际不值）。
- **主分析**：K2−K1 的 pooled 差值 + 逐任务/逐模型差值；3 seeds 同向；双人评分 κ。
- **不做的分析**：不把 K1−K0 当塔的门；不做 optional stopping；不因一个任务翻转改 pooled 口径。
- **偏离记录**：任务替换、模型版本、温度、prompt、rubric 任一变更 → 记 `deviations.md`，不静默改。
- **冻结件**：本文件 + 任务卡 + 预注册表（D3–4 产出）+ 代码/配置 hash。

## 回链

- topics：[03/projection](../topics/03-knowledge/projection/README.md) · [06/feasibility](../topics/06-measure/feasibility/README.md)
- digest：[N&D](../src/papers/2610.11768-narrow-and-deep/digest.md) §6.5/§6.6
- 结论：E-12；03-L1；03-L7
