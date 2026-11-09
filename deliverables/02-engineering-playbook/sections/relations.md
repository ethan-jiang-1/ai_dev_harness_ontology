---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 6. 关系与维护

> 本章回答：02 与 01/03 的关系、附录与维护。 ｜ 读完你应该能：知道细节去哪查。

### 6.1 与另外两份交付物的关系

| 交付物 | 回答 | 读者 | 形态 |
|---|---|---|---|
| [01 现状](../../01-capability-status/README.md) | 今天能做成什么、不能承诺什么 | 决策者/工程负责人 | 判断 + 矩阵 |
| [02 工程实施](../README.md) | 拿本体做某件事，具体怎么做 | 工程负责人/架构师 | 步骤 + 接口 + 验收 |
| [03 机制参考](../../03-mechanism-reference/README.md) | 为什么是这些位置/形态，证据边界在哪 | 架构师/研究者 | 参考 + 边界 |

**一句话**：01 告诉你「值不值得做」，02 告诉你「怎么做」，03 告诉你「凭什么这么说、说到哪为止」。


### 6.2 附录

- [A · 接口总表](../appendices/interfaces.md)：R0–R12 的字段、三态、版本。
- [B · 追溯表](../appendices/traceability.md)：R → E → mechanism → 边界；与 01/03 的 crosswalk。
- [C · 端到端示例](../appendices/case.md)：示意走查，不是部署。
- [recipes/](../recipes/README.md)：13 条完整配方。
- [operations/](../operations/ledger.md)：账本、评测、成本、上线、领域。

### 6.3 维护

- 本页是 02 的门厅；新增/修改 recipe 先改 `recipes/`，再回本页索引。
- 任何新判断先回 `topics/` 的 claims/E；02 不新增 E。
- 每次改动后跑 `python3 meta/tools/check_repo.py`；坏链不提交。
