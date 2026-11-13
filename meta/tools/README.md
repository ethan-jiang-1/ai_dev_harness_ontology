---
status: draft
updated: 2026-11-13
---

# 自检工具（Tools）

> **边界声明（[ADR 0005](../../adr/0005-repo-self-check.md)、[CHARTER §5](../../CHARTER.md#5-唯一例外)）**：`meta/tools/` 是全仓唯一允许存在代码的目录，只放**只读一致性检查工具**，不承载研究逻辑、不联网、不引入运行时依赖、不生成研究结论。

## 怎么跑

在仓库根目录执行：

```bash
python3 meta/tools/check_repo.py
```

退出码 `0` = 通过（0 errors）；非零即存在硬错误，修复前禁止提交。

## [`check_repo.py`](./check_repo.py) 查什么

| 检查项 | 查什么 | 失败怎么修 |
|---|---|---|
| 1. 相对链接与锚点 | 所有 `.md` 内部相对链接存在，且 `#fragment` 命中目标标题 slug 或 `<a id>`；禁止 `]( [` 嵌套坏链 | 修复路径或目标锚点 |
| 2. frontmatter 枚举 | `status`、`source_type`、`reading`、`provenance`、`quality`、`experiment_status`、`deliverable_status`、`seam`、`execution_form`、`evidence_role`、`admission`、`standing`、`plan_status` 是否合法 | 按 [schema](../schema.md) 修正值 |
| 3. 编号定义 | `E-xx` / `Q-xx` / `C-xx` / `0x-L<n>` 在 `conclusions.md` 或对应派 `claims.md` 有定义 | 补定义或改引用 |
| 4. 论文与开源清单 | 目录结构、PDF/`paper.md`/`card.md`/`digest.md`、`manifest` 行数、commit pin、`last_push` / `published` ≥ `2026-06-01`、`evidence_role`/`execution_form` | 补齐缺失文件或字段 |
| 5. 路线 B 与交付契约 | 现役 `E-xx` 含 `**做法` 与程序页链接；每份 `deliverables/NN-*/` 含 `SCOPE.md` + `README.md` | 补做法链接或 `SCOPE.md` |
| 6. 准入与防复入卫生 | `src/web`、`papers`、`open-source` 准入五字段齐全；[黑名单](../rules/excluded-sources.md) ID 未重新入库；无死 `src/` 反引号路径；无未加 caveat 的撤回 E/L/O | 清理撤回引用、补 caveat 或移出违禁源 |
| 7. 计数与计划卫生 | [state.md](../status/state.md) 的 md/论文/开源/材料卡/`execution_form`/结论/硬对象计数与文件树一致；`meta/plans/` 中 `plan_status: active` ≤ 1 | 先修源头或刷新 `state.md` |

## 它不查什么

- **不判证据质量与文体**：干货五问、证据等级是否过度外推、交付物是否符合 `SCOPE.md` 初心，靠 [checklist](../workflow/checklist.md) 与 [quality](../deliverables/quality.md) 人工审查。
- **不验外部 URL**：只读、不联网。
- **不替人改文件**：发现错误只报错退出。
