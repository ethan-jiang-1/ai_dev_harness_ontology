---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 6. 关系与维护

### 6.1 与另外两份交付物的关系

| 交付物 | 回答 | 读者 | 形态 |
|---|---|---|---|
| [01 现状](../README.md) | 今天能做成什么、不能承诺什么 | 决策者/工程负责人 | 判断 + 矩阵 |
| [02 工程实施](../../02-engineering-playbook/README.md) | 拿本体做某件事，具体怎么做 | 工程负责人/架构师 | 步骤 + 接口 + 验收 |
| [03 机制参考](../../03-mechanism-reference/README.md) | 为什么是这些位置/形态，证据边界在哪 | 架构师/研究者 | 参考 + 边界 |

**一句话**：01 告诉你「值不值得做」，02 告诉你「怎么做」，03 告诉你「凭什么这么说、说到哪为止」。


### 6.2 维护

- 本页是 01 的稳定判断；新证据先回 `topics/` 的 claims/E，再改本页。
- 能力分级（A/B/C/D）是交付层排序，不是 E；改分级要回 `topics/` 改证据。
- 数据表与工作底稿在 `data/` 与 [../_plans/01-capability-status.md](../../_plans/01-capability-status.md)；它们不构成稳定判断。
- 每次结构性修改后跑 `python3 meta/tools/check_repo.py`。
