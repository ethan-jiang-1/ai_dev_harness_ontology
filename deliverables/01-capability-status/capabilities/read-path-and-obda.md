---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# 读路径与查询重写

> **一句话**：read-path/查询重写有代码，但别扩大解释。 ｜ **适用**：读侧可见性、OBDA。 ｜ **证据**：E-20（代码级）。 ｜ **边界**：fail-open/只删 subject；无 agent 集成。

## 3.8 读路径过滤/查询重写：有代码，但别扩大解释

trustgraph 在查询结果返回前跑 SHACL-AF 策略，命中 `tg-pol:blocks` 的节点，其 subject 侧三元组被删除；它是读路径 best-effort gate，不是动作前闸门：target/rule 异常时 fail-open，且只删 subject 侧（E-20）。ontop 在查询编译时做 TBox 饱和 + 查询重写，把 SPARQL 变成 SQL；它是供给层执行器，不是判定器（E-20）。

**机制（read-path）**：trustgraph 的 `PolicyFilter` 是查询结果后的 SHACL-AF 求值器；`_triple_blocked` 只查 `triple.s`，所以只删 subject 侧；target/rule 异常 → 不命中 → 放行；无策略 → passthrough。它被设计成**可用性优先的可见性过滤**，不是授权闸（trustgraph digest §3/§6）。**所以**：object 方向泄漏和 fail-open 是设计范围，不是可修的 bug；要用它做安全，必须补第二实现/两侧约束/异常注入。**反例**：`?s ex:worksFor ?o` 中 `?o` 被 block、`?s` 可见时，`_triple_blocked` 只查 `?s`，这条三元组仍返回。

**机制（OBDA）**：ontop 在查询编译时做 TBox 饱和 + 重写（rewrite → unfold → SQL）；本体不是「在运行时拦」，而是「把查询改写成 SQL」。边界可判：只支持 OWL 2 QL；需要 DL 推理/事务写入就不适合（E-20）。**所以**：OBDA 是 A（可先落地），因为边界能写成验收；它不是闸，不要拿它做授权。

**能做什么**：读侧可见性/信息屏障；OBDA（本体驱动的数据访问）式「本体+映射→SQL」的查询回答。

**不能做什么**：不能当写授权，不能当动作闸，不能证明对象方向也受控；ontop 只支持 OWL 2 QL，不做 DL 推理。

**距离**：read-path 只有 1 个独立实现；需要第二个实现才决定是否升第七时刻。

> 回到 [能力索引](./README.md)。
