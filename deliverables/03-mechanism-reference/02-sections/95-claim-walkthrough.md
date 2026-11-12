---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# Claim 走查：读路径过滤能防止敏感数据泄漏吗？

> **这是什么**：把一条常见主张拆成可判句，走一遍「位置 → 证据 → 成立到哪 → 什么条件下不成立」。
>
> **不是什么**：不是新 E，不是新测量。每个判断都落回 [E-20](../../../topics/conclusions.md)、[E-22](../../../topics/conclusions.md)、[N07](../05-evidence/02-boundaries.md) 与 [outside §3.2](../03-positions/07-outside.md#32-read-path检索返回前)。
>
> **工作定义（`D`，不是 E）**：本文的「泄漏」= 不该被该 principal 看到的 subject 侧或 object 侧三元组，出现在查询/检索返回的结果里。03 没有独立的「敏感数据」分类；这是为这条走查设的工作定义。

## 0. 一页结论

**位置**：`read-path`（轴外，不在六位置强度谱）。

**成立到**：在**正常路径**、**有 policy**、**只读检索**、**只删 subject 侧**的条件下，它能把被 `tg-pol:blocks` 命中的 subject 侧三元组从结果里删掉。`已核（代码）`（E-20）

**不成立到**：不能据此说「防止敏感数据泄漏」，更不能说「访问控制/授权」。四条硬边界：**异常 fail-open、object 方向未测、只有 1 个实现、不拦写/落盘**。`已核（代码）`（E-20）/ `已核`（E-22）

> 一句话：**它是 best-effort 可见性过滤，不是闸，不是授权。**

## 1. 把 claim 拆成三句

| # | 可判句 | 判定 | 依据 |
|---|---|---|---|
| 1 | 机器在检索返回前，按 policy 删除了被 block 的 subject 侧三元组 | **成立** | E-20：trustgraph 加载 SHACL-AF NodeShape，跑 `sh:SPARQLTarget` + `sh:SPARQLRule`，命中 `tg-pol:blocks` 的 subject 侧三元组从结果删除 |
| 2 | 删除后，敏感数据不会出现在结果里 | **只在窄条件成立**：正常路径 + 有 policy + subject 侧；object 方向/Fail-open 不成立 | E-20 的边界；本文 §3 |
| 3 | 因此它能当访问控制（授权） | **不成立** | E-22/N07：读路径 ≠ 写授权；有标签 ≠ 有策略 ≠ 执行正确 |

> **「防止」是第 2 句的强读法。** 第 1 句成立不代表第 2 句成立；第 2 句成立也不代表第 3 句成立。

## 2. 为什么是 read-path

| 候选位置 | 为什么不是 |
|---|---|
| **context** | context 是「给什么」；read-path 是「检索返回前删什么」。它改变的是结果集，不是上下文组织 |
| **action** | action 在副作用发生前拦动作；read-path 只影响读，不拦写/落盘 |
| **commit** | commit 管授权与落盘；read-path 不是授权 |
| **checker** | checker 验输出；read-path 在输出前改输入 |

> 它不在六位置，是因为只有 1 个实现、fail-open、单侧过滤，不满足「≥2 个独立实现」的扩轴规则（[outside §3.2](../03-positions/07-outside.md#32-read-path检索返回前)）。

> **read-path 不是一种机制。** 至少三个执行点：post-filter（trustgraph，node/subject，fail-open；**唯一已入库实现**）、rewrite（sparql-guard，node+graph，fail-closed，仓库外复跑 76/76；**候选未入库**）、scan（holosdb，predicate+graph，默认 deny；**候选未入库**）。**本文描述以 post-filter 为准**；三个执行点不能互替，「admitted 第二实现」仍为**无**。见 [read-path §3/§7](../../../topics/01-constraint/commit-gate/read-path.md)。

## 3. 成立到什么程度

| 条件 | 成立吗 | 说明 |
|---|---|---|
| 只读检索、结果集返回前 | 是 | 机制的触发点 |
| 有 `urn:graph:policy` 且 shape 命中 | 是 | 没 policy 就无从删 |
| 只删 subject 侧 | 是 | 这是它的设计，不是缺陷；但意味着 object 方向不管 |
| object 方向也不泄漏 | **未测** | 没有 object 用例；不能假设 |
| 异常时 fail-closed | **否** | 异常 fail-open（E-20）；出错时可能放行 |
| 有第二个独立实现 | **否** | 只有 trustgraph；单实现 |
| 能当写授权/落盘授权 | **否** | 读路径 ≠ 写授权（E-22） |
| 覆盖向量/文档检索 | **未测（推断）** | E-20 的 trustgraph 是图查询结果过滤；03 没有说它覆盖向量/文档检索 |

**结论**：它成立的范围是「正常路径的 subject 侧可见性过滤」；超出这个范围，每一格都要单独证。

## 4. 四条不成立条件（缺一条就不能当闸）

1. **异常 fail-open**：解析/执行出错时放行，而不是拒绝。Kirrane 2020 的形式化对照指出 FILTER 式重写在否定/子查询/聚合下不正确；结果过滤与「像不存在」不是同一语义（[卡](../../../meta/audits/2026-11-11-source-purge.md#src-web-kirrane-2020-qbac)）。SHACL-AF 对不支持的 custom target 只写「behavior undefined」+ SHOULD warn，不要求拒绝；fail-open 是实现选择，不是标准要求（[SHACL-AF 卡](../../../src/web/w3c-shacl-af/w3c-shacl-af.card.md)）。
2. **只删 subject 侧**：object 方向可能泄漏；没有 object 用例。
3. **不拦写/落盘**：它不改变写路径；不能替代 commit gate。
4. **单实现**：只有 trustgraph 一个 pin commit；没有第二实现/阻断测试。

> 这四条不是「永远不行」，是「在这四条修好之前，不能把 B 读成 A」。**§4 是「未修」；§5 是「未定义/未测」，两类要分开写。**

## 5. 缺什么（回 frontier，不在本文补）

| 缺口 | 补它需要什么 | 在哪 |
|---|---|---|
| 第二实现 | 另一个 pin commit 的 read-path 实现 + 调用点 | [gaps §2](../05-evidence/03-gaps.md) |
| object 方向 | object 用例 + 期望（敏感 object 不出现） | [gaps §2](../05-evidence/03-gaps.md) |
| fail-closed | 异常路径的阻断测试 | [gaps §2](../05-evidence/03-gaps.md) |
| 泄漏率/误拦率 | 实测（当前 0 个） | [measurement §2](../04-across-positions/03-measurement.md) |
| 「敏感数据」分类 | 领域标签/策略来源（E-22：策略层无领域本体来源） | [E-22](../../../topics/conclusions.md) |
| 共同 10 用例协议 | sparql-guard 已跑 10 用例（7 pass、1 alias leak、0 false-block）；trustgraph/holosdb 是复刻；还没有率 | [read-path §8](../../../topics/01-constraint/commit-gate/read-path.md) |
| alias/实体解析 | 未类型化 alias 会漏（EXP-002）；前置能修 node-level、不修 predicate-level（EXP-003）；规范只强制「已断言 sameAs 则展开」，不强制「先于过滤」（read-path §9–§10） | [read-path §8–§10](../../../topics/01-constraint/commit-gate/read-path.md) |
| coverage 的失效类 | 七类（A–G）里没有「泄漏」类；不要用覆盖率矩阵替这条 claim 的证据 | [coverage §2](../04-across-positions/01-coverage.md) |

## 6. 怎么用（读者动作）

- **当可见性过滤用**：可以；但要标「best-effort、fail-open、单实现」。
- **当授权用**：不行；要么补 commit gate，要么用真正的策略执行点。
- **量什么**：泄漏率（subject/object 分开）+ 误拦率 + 异常路径行为；三个都量不出，就写 `unknown`，不要写「已防止」。
- **写进方案时**：把 §4 四条写成「未修清单」，不要写成「已知风险，可接受」。

## 7. 与 01/04 的分工

- 值不值得做 → [01](../../01-capability-status/README.md)：读路径在 01 是 B（可试点），不是 A。
- 建/用/治一条访问控制链 → [04](../../04-worked-example/README.md)：04 的 C.3 有 LEAK-T1 探针，明确「skip ≠ allow」。
- 本文只回答：**这条 claim 成立到哪、什么条件下不成立。**
