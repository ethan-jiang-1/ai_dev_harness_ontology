---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 验收清单

> 逐项勾。**没做就写「未做」，不要写「通过」**。门槛按组：A1–A4、A5+B1–B3、C1–C5；文末「加强项」不阻塞最小链。
> `A1–C5` 是检查项编号；正文小节写作 `A.1`、`B.2`、`C.3`（带点的是小节，不带点的是检查）。

## A 建

| # | 检查 | 怎么查 | 通过 | 未通过 |
|---|---|---|---|---|
| A1 | 契约 6 项无空 | 看 [A.1](../body/build.md) 表；每行有 consumer/principal/moment/answers/refuses/load | 6 项有值（`—`=明确不拒）；每行有 1 个 CQ 或拒绝条件 | 回 A.1，不要先建本体 |
| A2 | 3 个 TTL 可解析 | `rdflib` 解析 `ontology.ttl`/`shapes.ttl`/`catalog.ttl` | 3/3 parsed | 查语法/前缀 |
| A3 | shapes 有 target | 每个 shape 有 `sh:targetClass`/`targetNode`；`targeted>0` | 2/2 有目标 | 补 target；否则 `conforms=true` 是空转 |
| A4 | 已知 shape 坏样本被抓住 | `pyshacl` 跑 shapes；对照 [参考表 §2](./reference.md) | 2/2 shape 声明样本（字面量 tag、缺 level）；10 个契约坏样本只抓 2 个，见 [A.5](../body/build.md) | 查 shape 是否覆盖 |
| A5 | 三条 CQ 期望对 | 跑 [B.2](../body/consume.md) 的 CQ1/CQ2/CQ3 | CQ1 2 / CQ2 7 列 4 表 / CQ3 4 | 0 行先分因，不要改 prompt |

## B 用

| # | 检查 | 怎么查 | 通过 | 未通过 |
|---|---|---|---|---|
| B1 | 资产→路线有记录 | 填 [B.0](../body/consume.md) 第一列 | 5 行里能选 1 行 | 回 B.0，不要凭框架选 |
| B2 | 3 条 CQ 有 `query_id`/snapshot | 看 query log 或 [B.2](../body/consume.md) | 每条有 id/snapshot/version | 补记录 |
| B3 | 0 行分因 | 用 [B.2](../body/consume.md) 的 ASK 表 | 每条 0 行有原因 | 不要重试同一条 |
| B4 | 纠错有 2×2 或标「未测」 | 看 [B.3](../body/consume.md) | 有四格；或明确「未测」 | 没有就删「净收益」句 |
| B5 | OBDA 有去公理消融或标「未做」 | 看 [B.4](../body/consume.md) | 有/无公理结果集；或「未做」 | 不要写「本体有贡献」 |

## C 治

| # | 检查 | 怎么查 | 通过 | 未通过 |
|---|---|---|---|---|
| C1 | 三层来源写清 | 看 [C.1](../body/govern.md) | 标签/策略/执行各有来源或「无」 | 不要把标签当策略 |
| C2 | 10 条策略测试有 decision | 看 [policy_tests.json](../example/policy_tests.json) | 9 条有唯一期望；T9 显式 undetermined | 补优先级声明 |
| C3 | object 方向探针 | 跑 [C.3](../body/govern.md) 的 LEAK-T1 | 0 行；若返回行 → 泄漏 | 修执行层或降级 |
| C4 | audit 字段齐 | 对照 [audit.schema.json](../example/audit.schema.json) + [audit_records.json](../example/audit_records.json) | 2 条记录必填字段齐；`decision_id` 可 replay | 补版本/快照 |
| C5 | 12 条泄漏用例有期望 | 看 [leak_cases.json](../example/leak_cases.json) | 12 条有 expected | 补用例 |

## 最小上线门槛（5 组）

五组全满足才叫 **可上线候选**；缺一条就是「演示」或「conditional」。

1. A1–A4 过：契约、TTL 解析、target、坏样本。
2. A5 + B1–B3 过：3 条 CQ、路线、记录、空结果分因。
3. C1–C3 过：三层、策略测试、object 探针。
4. C4–C5 过：audit schema + 2 条记录 + 1 条 replay；12 条泄漏用例有期望。
5. 没有未修漏洞：object 泄漏、T9 优先级、`targeted=0`、写授权。

**当前 fixture 的默认结论是 `conditional`，不是 `可上线`**：C3 用的 trustgraph 已知 fail-open、只删 subject，object 探针会返回行；修法（第二实现/两侧约束/粗粒度 deny）不在 04 内。要过 C3，换或修执行层；否则只能交「conditional + 未修清单」。

## 加强项（不阻塞最小链）

- 3 条 CQ 全跑 + 2×2 纠错配对。
- OBDA 去公理消融。
- 10 类故障注入 + 跨段 replay。
- 200 表/5k 列规模测试。

## 记录模板

```json
{
  "fixture": "example/ 2026-11-10",
  "checked": ["A1","A2","A3","A4","A5","B1","B2","B3","C1","C2","C3","C4"],
  "failed": ["C3"],
  "not_run": ["B4","B5","C5","C4 replay"],
  "result": "conditional",
  "notes": "T9 未定；LEAK-T1 返回行；replay 未跑"
}
```
