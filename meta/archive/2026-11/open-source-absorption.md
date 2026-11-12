---
status: superseded
updated: 2026-11-09
---

# 开源证据吸收矩阵（code → topics）

> 目的：回答「代码发现有没有真的进 topics 的判断」，而不是 digest 与 topics 各自合格、互不相干。
> 规则见 [开源消化计划](./open-source-digestion-plan.md) §3（A 闸 + 融合契约）。每次改 topics 后更新本页。

## 状态

| 状态 | 含义 |
|---|---|
| `pending` | 已选定，digest/吸收未开始 |
| `absorbed` | 代码发现已进 sources/findings/claims，且能反查 digest 段落 |
| `partial` | 进了 findings，但还没进 claims（或反之） |
| `orphan` | digest 有发现，topics 没接（必须修） |
| `rejected` | 明确判定「不适用/不改变判断」，写明理由 |

## 矩阵

| # | 项目 | 机制 | 执行形态 | 调用点 | 对应论文 digest | 目标 L/F | 状态 | 动作 |
|---|---|---|---|---|---|---|---|---|
| OS-01 | trustgraph | SHACL-AF 读路径策略过滤 | executed（读路径） | `policy/triples/service.py → policy_filter.py` | Commit Boundary / POLAR | 01-L13 / commit-gate F5 | absorbed | L13 备注收窄；F5、G1 更新；fail-open 待验 |
| OS-02 | semantica | OWL 生成 + 派生 SHACL + pyshacl | mixed（offline/CLI） | `semantica/ontology/ontology_validator.py:148`；`engine.py: to_shacl/validate_graph` | OntoDoc / Ontology Catch | 05 generation F7；02 checker G6 | absorbed | F7 入档；checker 加 G6；未改 L |
| OS-03 | open-ontologies | SHACL 引擎（默认/verified）+ 变更影响 | executed（工具面；C2 阻塞） | `src/shacl.rs` / `shacl_verified.rs` / `closure_diff.rs` | What Does an Ontology Catch / Commit Boundary / SFE-O | 02 checker F7；05 lifecycle 判断 4 | absorbed（代码级；未跑） | 两条 sources 行；F7；生命周期边界；待重跑 C2 |
| OS-04 | ontop | OBDA 查询重写 | executed（供给） | `engine/.../QuestQueryProcessor.reformulateIntoNativeQuery` | CAI（边界对照） | 03 frontier（无 claim 改动） | partial | 已进 03 frontier；不改 claims；待做「有/无本体」消融 |

## 完成判据

- 无 `orphan`；`partial` 有明确下一步。
- 改动的 `L-xx` ≤3 条；`conclusions` 无直接代码来源的 `E-xx`。
- 每条 `absorbed` 都能反查到 digest 的具体段落与 `文件:符号`。

## 变更记录

- 2026-11-09：建表；4 个本轮项目全部 `pending`。
- 2026-11-09：OS-01 trustgraph → `absorbed`（01-L13 备注收窄；commit-gate F5；G1 读侧有答案）。
- 2026-11-09：OS-02 semantica → `absorbed`（05 generation F7；02 checker G6）。
- 2026-11-09：OS-04 ontop → `partial`（03 frontier 候选 + 03 sources 主记录；不改 claims）。
- 2026-11-09：OS-03 open-ontologies → `absorbed`（02 checker F7/F8；05 lifecycle 判断 4；C2 阻塞记录）。
