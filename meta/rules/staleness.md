---
status: draft
updated: 2026-11-13
---

# 过期与复核（Staleness）

> 依据 [CHARTER §4](../../CHARTER.md#4-素材准入material-gate) 与 [ADR 0013](../../adr/0013-source-whitelist-blacklist.md)。时效判定以宪章为准，本页规定仓内的周期性复核与退场执行口径。

## 1. 两条硬时间线

| 规则 | 适用对象 | 判据 | 超期处置 |
|---|---|---|---|
| **窗口与活跃度**（G1/G2） | 所有 `src/` 材料 | 首次公开 ≥ `2026-06-01`（在役标准走 §4.4 例外）；代码 180 天内有提交、社区 90 天内有讨论 | 不满足 → 降为 `excluded` 移出 `src/`，进 [excluded-sources](./excluded-sources.md) 与 [audits/](../audits/2026-11-11-material-gate.md) |
| **观察期转正**（probation） | `admitted (probation)` 材料（如 P0 四篇：GGC / Agents / N&D / CASEL） | 首次准入后 **6 个月内**必须补到第二个独立信号（I1–I5）；**不得连续续期** | 到期（2027-05-11）仍只有一个信号 → 降为 `signal` 并移出 `src/`，依赖它的 `E/L` 同步降级或撤回 |
| **全仓半年复核** | 所有 `admitted` 卡片与引用它的判断 | 每 **6 个月**重审一次 `liveness` 与 `impact_evidence` | 更新卡上 `gate_checked`；不合格的按 [CHARTER §4.3](../../CHARTER.md#43-回溯与退出无-grandfathering) 退出 |

## 2. 动作与记录

1. **不保留历史语料豁免**：已入库/已消化/已引用均不构成豁免；过期或失效源先删，再回改下游 `claims.md` / `conclusions.md` / `deliverables/`。
2. **删后防复入**：所有移出源必须同步写入 [excluded-sources](./excluded-sources.md)（命中即禁读禁引），并在 `meta/audits/YYYY-MM-DD-material-gate.md` 留痕；`check_repo.py` 会自动拦截黑名单 arXiv ID 重新入库。
3. **`updated` 纪律**：仅在实质修订内容或重审时更新 frontmatter 的 `updated`；搬家、改路径、批量重写链接不刷 `updated`。
4. **当前待复核重点**：见 [state.md 的 A 轨目标](../status/state.md#当前目标下一步做什么)（P0 四篇 probation 补第二信号，截止 2027-05-11）。
