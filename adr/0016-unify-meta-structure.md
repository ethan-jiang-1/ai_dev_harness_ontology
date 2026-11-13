---
status: draft
updated: 2026-11-13
---

# ADR 0016：统一 `meta/` 治理结构与工作底稿分家

## 背景

在跨仓库对照 `ai_dev_harness_ontology` 与 `ai_dev_harness_security` 的治理层后，发现双方虽然研究同一套“harness 研究档案流水线”（`src/` → `topics/` → `deliverables/`），但 `meta/` 目录已产生不必要的结构分裂：

1. 本仓库将字段表、写作标准、加载路径、交稿检查、研究协议全部混在 `meta/rules/`，[conventions.md](../meta/rules/conventions.md) 兼具机器字段定义与主观干货品味（217 行），且同时存在 `meta/AGENTS.md` 与 [meta/README.md](../meta/README.md) 两张相邻门牌。
2. 模板分散在 `src/_templates/`（6 个）与 `meta/templates/`（2 类）两处。
3. `deliverables/_plans/` 物理位置与命名名不副实（[ADR 0012](./0012-instruction-layer-single-home.md) §5 当时的妥协）：41 个文件里既包含 23 份执行计划，也包含 17 份冷读、质量评分、内容审计、缺口盘点等非计划底稿。
4. 缺乏独立的 `information-flow.md`、`staleness.md`、`extension-points.md` 与 `working-agreements.md` 单页规范，导致三层受众、复核周期与并发交接散落在 ADR 与旧计划里。

同时，本仓库沉淀的 `meta/tools/check_repo.py`、`meta/status/state.md`、`meta/deliverables/scope.md`、`meta/rules/excluded-sources.md` 与 `meta/audits/` 已被证明是高价值的工程治理武器，应作为标准组件保留。

## 决策

吸取两仓各自优势，将本仓治理层收敛为与 `security` 对齐的通用研究档案骨架：

1. **单入口 + 独立 Schema**：合并原 `meta/AGENTS.md` 到 [meta/README.md](../meta/README.md)；从 `conventions.md` 抽离全仓字段、枚举、证据阶梯、阅读深度、编号与校验规则到 [meta/schema.md](../meta/schema.md)，`conventions.md` 只管写作口径与干货门槛。
2. **`rules/` 与 `workflow/` 二分**：
   - `meta/rules/` 只放静态口径：`conventions.md`、[information-flow.md](../meta/rules/information-flow.md)、[source-types.md](../meta/rules/source-types.md)、[excluded-sources.md](../meta/rules/excluded-sources.md)、[staleness.md](../meta/rules/staleness.md)。
   - `meta/workflow/` 只放动态流程：[loading.md](../meta/workflow/loading.md)、[checklist.md](../meta/workflow/checklist.md)、[topic-research-protocol.md](../meta/workflow/topic-research-protocol.md)、[extension-points.md](../meta/workflow/extension-points.md)、[working-agreements.md](../meta/workflow/working-agreements.md)。
3. **模板全仓收敛**：原 `src/_templates/*` 迁入 `meta/templates/src/`，原 `meta/templates/` 主题模板归入 `meta/templates/topics/`，`src/` 不再自带模板目录。
4. **计划与工作底稿分家（替代 ADR 0012 §5）**：撤销 `deliverables/_plans/`；有推进状态机的计划归入 [meta/plans/](../meta/plans/README.md)（现行 `plan_status: active` ≤ 1，已完成的历史计划归入 `meta/archive/2026-11/plans/`）；无状态机的冷读、评分、审计、缺口盘点留在 [deliverables/_workpapers/](../deliverables/_workpapers/README.md)。
5. **保留本仓治理武器**：保留 `meta/tools/`（补 [README](../meta/tools/README.md) 并强化 `check_repo.py` 对 `plan_status` 的校验）、`meta/status/`、`meta/deliverables/` 与 `meta/audits/`（保留独立一级以避免改写 `CHARTER.md` §4.3 规范路径）。

## 后果

- 规则、流程、模板、状态、计划、底稿各归其位，两仓拥有一致的心智模型，新接手 Agent 无需重新适应结构。
- `deliverables/` 下只保留 `_workpapers/`，彻底消除“为什么交付物里有个 `_plans` 却装满评分报告”的认知冲突。
- 全仓相对链接按新路径重写，并由 `python3 meta/tools/check_repo.py` 保证零断链、零枚举越界。
