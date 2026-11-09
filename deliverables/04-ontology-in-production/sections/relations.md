---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 6. 关系与维护

> 本章回答：04 和 01/02/03、05 是什么关系。 ｜ 读完你应该能：知道什么问题该回哪一份。

## 6.1 与另外三份交付物的关系

| 交付物 | 回答 | 04 什么时候去 |
|---|---|---|
| [01 现状](../../01-capability-status/README.md) | 今天能做成什么、不能承诺什么 | 立项前判断“值不值得” |
| [02 工程](../../02-engineering-playbook/README.md) | 选哪个接缝/recipe、怎么验收 | 选 R0/R5/R8/R9 时 |
| [03 机制](../../03-mechanism-reference/README.md) | 为什么是这些位置、边界在哪 | 评审“凭什么”时 |
| **04（本份）** | 建 → 用 → 治的落地生命周期 | 从 CQ 到应用的全流程 |

**一句话**：01 判断值不值得，02 决定接在哪，03 说凭什么，04 把建/用/治串起来。

## 6.2 与 05 研究页的关系

- **05 生产派**：04 的“建”只抽工程可用部分；本轮没有 in-scope evaluation，A.2–A.5 保持 signal，不新增 E。
- **03 知识派**：`03/querying` 是 E-21 的出处；04 B.3 引 E-21，不重复 digest。
- **01 约束派**：`01/access-control` + commit-gate 是 E-22/E-20 的出处；04 C.1 引 E，不重复机制。

## 6.3 维护

- 04 不新增 E；E 先在 topics 定义（本轮 E-21/E-22），04 只引 E；未入库的进 `evidence/` 的 signal 表。
- 新外部来源先问：它改变“建/用/治”的哪一条？答不出就只进 evidence；改变判断才升 E。
- 旧于 2026-07 或 origin 不在 US/China/Germany/Singapore 的来源不再新入档。
- 01/02/03 的判断变化时，回改 04 的相关段；04 不调和冲突。
- 每次结构性修改后跑 `python3 meta/tools/check_repo.py`。
