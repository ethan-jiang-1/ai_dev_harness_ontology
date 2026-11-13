---
status: draft
updated: 2026-11-13
---

# 扩展点：往哪里加东西，不用改结构

> **本页只回答**：加什么、落哪、必须同步什么、什么时候该停下来写 ADR。结构决策索引见 [adr/README](../../adr/README.md)。

本仓库的骨架（三层流水线 + 六派 + 四轴 + 七部件）已稳定。新增研究内容时，优先落进现有最便宜的位置，**不要因为新材料/新现象轻易重排根目录或新建目录轴**。

## 1. 四条原则

1. **先走准入再建目录**：采/引前先查 [来源黑名单](../rules/excluded-sources.md)，再过 [CHARTER §4](../../CHARTER.md#4-素材准入material-gate) 五门；未过 G2/G3 的 `signal` 只进 `frontier.md` 候选队列，不建 `src/` 目录。
2. **能跨派/横切解决的不建目录**：新维度优先做横切页（如 `seams.md`、`execution-forms.md`、`domains.md`）；不要把“形态/来源类型”建成新的一级目录。
3. **能派内解决的不开新派/新交付物**：新机制先放现有派 `claims.md`（`L-xx`）；确实跨派且有独立判据再进 `topics/conclusions.md`；绝不为了“看起来完整”建空目录或占位文件。
4. **改契约先过 ADR**：新增字段、枚举值、目录层、源类型或交付物定性变更，先写 ADR 再改 [schema](../schema.md) 与消费者。

## 2. 扩展点总表

| 你要加什么 | 落点 | 必须同步 | 不要做 |
|---|---|---|---|
| 一篇论文 | `src/papers/{arxiv_id}-{slug}/`（模板在 [templates/src/](../templates/src/paper-card.md)） | `src/papers/manifest.md`、对应派 `sources.md`、[state](../status/state.md) | 跳过 `digest.md`；把 `signal` 建目录；只写 `card.md` |
| 一个开源项目 | `src/open-source/{org}-{repo}/`（pin `commit`） | `src/open-source/README.md`、对应派 `sources.md`、[state](../status/state.md) | vendor 代码；不写 `digest.md`；只凭 README/star 升 `已核` |
| 一个网页/标准/生产报告 | `src/web/{来源}/<slug>.card.md` | `src/web/README.md`、对应派 `sources.md`、[state](../status/state.md) | 用厂商营销文当跨组织 E；在役标准不附 `liveness` 活动证据 |
| 一个子主题 | `topics/<派>/<子主题>/`（模板在 [templates/topics/](../templates/topics/note-template.md)） | 该派 `README.md` 与 `sources.md` | 按来源类型建子主题；预建空目录 |
| 一条局部判断 | `topics/<派>/claims.md`（`0x-L<n>`） | 对应卡片 `updates:`；派 `README.md`（若改顶层结论） | 直接跳过 `claims.md` 改 `conclusions.md` |
| 一条跨派结论 | `topics/conclusions.md`（`E-xx`）+ 一句 `**做法` + `mechanism` 链接 | 引用页、[state](../status/state.md) 结论计数 | 无 `mechanism` 链接塞 12 步流程；引 withdrawn 源供等级 |
| 一个硬对象地址 | `topics/objects.md`（`O-<X>nn`） | `state.md` 硬对象计数 | 在交付物用 `O-xx` 替代 `E-xx` 作主句 |
| 一份研究/执行计划 | `meta/plans/YYYY-MM-DD-<slug>.md`（带 `plan_status`） | `meta/plans/README.md`（确认 `active` ≤ 1） | 放进 `deliverables/_workpapers/`；同时保留两份 `active` |
| 一份交付物评估/底稿 | `deliverables/_workpapers/YYYY-MM-DD-<slug>.md` | `deliverables/_workpapers/README.md` | 给底稿加 `plan_status`；把底稿当成交付正文 |
| 一个字段或枚举值 | [meta/schema.md](../schema.md) + 新 ADR | `meta/tools/check_repo.py`、受影响模板与 `checklist.md` | 在正文自造字段值；在 `conventions.md` 另抄枚举 |
| 淘汰/撤回一条源 | 移出 `src/` + 写入 [excluded-sources](../rules/excluded-sources.md) + `meta/audits/` | 受影响 `L-xx`/`E-xx`/`O-xx` 标撤回/降级、交付物同步清理 | 静默删源；保留历史源当作背景证据 |
| 一份新交付物 | `deliverables/NN-<name>/`（必含 `SCOPE.md` + `README.md`） | [scope.md](../deliverables/scope.md)、[loading.md](./loading.md)、`deliverables/README.md`、[state](../status/state.md)、新 ADR | 没写 `SCOPE.md` 就开写；新交付物与已有定性混用 |

## 3. 什么时候该升级 / 不要急着升级

- **不要急着开子主题**：只有 1 篇源、没有独立判据时，先留在派 `claims.md` / `frontier.md`，不要硬建目录。
- **不要急着升 `E-xx`**：仅在单派内部成立的判断留在 `claims.md`；跨派复用或进入 `deliverables/` 时再升 `E-xx`。
- **应该开新子主题**：同一子机制已有 ≥ 2 个独立来源、形成独立 `findings`/`mechanism`/`frontier` 需要承载时。
