---
status: draft
updated: 2026-11-09
parent: ../README.md
---

# 轴外：读路径过滤 / 查询重写

> **一句话**：read-path/查询重写有代码，但别扩大解释。 ｜ **适用**：读侧可见性、OBDA。 ｜ **证据**：E-20（代码级）。 ｜ **边界**：fail-open/只删 subject；无 agent 集成。

## 3.8 读路径过滤/查询重写：有代码，但别扩大解释

trustgraph 在查询结果返回前跑 SHACL-AF 策略，命中 `tg-pol:blocks` 的节点，其 subject 侧三元组被删除；它是读路径 best-effort gate，不是动作前闸门：target/rule 异常时 fail-open，且只删 subject 侧（E-20）。ontop 在查询编译时做 TBox 饱和 + 查询重写，把 SPARQL 变成 SQL；它是供给层执行器，不是判定器（E-20）。

**能做什么**：读侧可见性/信息屏障；OBDA（本体驱动的数据访问）式「本体+映射→SQL」的查询回答。

**不能做什么**：不能当写授权，不能当动作闸，不能证明对象方向也受控；ontop 只支持 OWL 2 QL，不做 DL 推理。

**距离**：read-path 只有 1 个独立实现；需要第二个实现才决定是否升第七时刻。
