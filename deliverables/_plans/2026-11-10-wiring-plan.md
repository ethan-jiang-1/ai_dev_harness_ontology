---
status: draft
type: work-plan
updated: 2026-11-10
target: 交付物接线（M/R/X）
scope: wiring
---

# 接线计划：把 O-xx 接进三处交付物

> 对象层已完成（[91 个](../../topics/objects.md)）；本计划只做一件事：**让对象出现在交付物里**。一步一步，不扩对象。

## 0. 目标与顺序

一句话：**ADR → M（门槛表）→ R（反例集）→ X（执行矩阵）→ 冷读**；每步一个验收，不过就停。

| 步 | 做什么 | 落点 | 验收 |
|---|---|---|---|
| 0 | ADR 0009 定案：方案 A（O 只作地址，主句仍落 E） | [ADR 0009](../../adr/0009-object-layer.md)、[checklist](../../meta/rules/checklist.md) §3、[loading](../../meta/rules/loading.md) | 三处规则一致；O 必须挂 E |
| 1 | 02 §5.1 的 13 行停线加 `出处` + `量不出时` 两列 | [02 §5.1](../02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺) | 13/13 有出处；≥4 行挂 E/公式；≥2 行标 gap/工程建议 |
| 2 | 03 boundaries 加 12 条反例表（带数 + 条件 + O-R） | [03 boundaries](../03-mechanism-reference/05-evidence/02-boundaries.md) | 12 条带数；每条有「条件下不成立」 |
| 3 | 03 execution-forms 的代码核对表加 `O` 列；补 OPA 行；Qlever 标「无代码锚」 | [03 execution-forms](../03-mechanism-reference/04-across-positions/02-execution-forms.md) | 5 行有 O-C；「不保证什么」可点开 |
| 4 | 冷读：10 分钟内从 01/02 找到「先做/量什么/何时停」 | 01/02/03 | 卡点 ≤2；否则回修接线 |

## 1. 约束

- 只改交付物与规则；不改 E/L、不新增对象、不改结论。
- 每个 O 引用必须能打开（`check_repo` 的 O 检查覆盖）；打不开就回注册表修。
- 主句仍落 `E-xx`；O 只回答「这条 E 的数/代码在哪」。
- 不新增索引页；不借机扩写正文。

## 2. 验收

- [x] ADR 0009 状态 = 接受；checklist §3 与 loading 规则允许 O 作地址。
- [x] 02 §5.1：13 行 × 7 列；`出处` 非空；≥4 行挂 E/公式；≥2 行标 `工程建议 / gap`（R0、commit）。
- [x] 03 boundaries：12 条反例；每条有数、条件、O-R。
- [x] 03 execution-forms：5 行有 O-C；OPA 行入库；Qlever 标「无代码锚」。
- [x] 冷读通过；`check_repo` 通过；`meta/state` 更新。

## 3. 不做什么

- 不做 E-03/E-12 的 H3（研究，不是接线）。
- 不先做 Deck/一页图；接线没验收前不包装。
- 不借接线改判断；发现判断问题回 topics，不在交付物里补。
- 不把 O 写成第二套结论；O 与 E 冲突以 E 为准。

## 4. 执行记录（2026-11-10）

- **0 ADR**：0009 状态改为**接受（方案 A）**；[checklist](../../meta/rules/checklist.md) §3、[loading](../../meta/rules/loading.md) 规则 1、[objects.md](../../topics/objects.md) 头部三处同步。
- **1 M**：[02 §5.1](../02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺) 13 行 × 7 列；13/13 有出处；11 行挂 E/公式（5 纯 + 6 混合）；2 行 `工程建议 / gap`（R0、commit）。
- **2 R**：[boundaries.md §0](../03-mechanism-reference/05-evidence/02-boundaries.md#0-反例集r-table) 12 条；每条带数、条件、`O-Rxx`；B1–B15 原表保留，B/R 分工写在页首。
- **3 X**：[execution-forms §3](../03-mechanism-reference/04-across-positions/02-execution-forms.md#3-五个项目的代码级核对) 5 行 × 6 列（加 `O` 列）；补 OPA；Qlever 标「无代码锚」。
- **4 冷读**（自审，非外部读者）：
  - 路径 A：02「编译」→ `O-T04` → `O-F01` → CAI digest `#43-成本模型`，3 跳，数可复算（3.08 vs 3.12 已在对象里标）。
  - 路径 B：02「checker」→ `O-T06` → `O-P02` → 02 §5.3，2 跳，样本 200 与 5pp/15% 可查。
  - 路径 C：02「read-path」→ `O-T09` → `O-C03` → trustgraph digest §6，3 跳，fail-open 可核。
  - 卡点 0 断链；1 个误读风险——O 编号是地址、不是结论，已在 M-table 脚注写明；交付物无 `L-xx` 引用。

**验收**：见 §2，全部勾选由 [state](../../meta/status/state.md) 与 `check_repo` 输出背书。
