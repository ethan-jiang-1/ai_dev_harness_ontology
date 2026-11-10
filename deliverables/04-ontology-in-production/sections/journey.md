---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 一条查询的旅程：raw → policy → governed → audit

> 本页是**读法**，不是可执行规格。只读文字和表，不运行代码；示例数字来自 fixture（5 表/13 列）。
> 读完你应该能说出：同一张 fixture，为什么 CQ1 在 steward 下是 2 列 / 2 表、在 analyst 下是 0 列；为什么 CQ2 是 7 列 / 4 表、analyst 下 0 列；为什么 LEAK-T1 不是“必须 0 行”。

## 0. 一张表看完

| query | principal | raw | policy | governed | audit |
|---|---|---|---|---|---|
| CQ1 | steward | 2 列 / 2 表 | allow（R4） | 2 列 / 2 表 | dec-0003 |
| CQ1 | analyst | 2 列 / 2 表 | deny（R2，level 3） | 0 列 | 样例未列 |
| CQ2 | steward | 7 列 / 4 表 | allow（R4） | 7 列 / 4 表 | query log |
| CQ2 | analyst | 7 列 / 4 表 | deny（R2，level≥3） | 0 列（7 列全拒） | dec-0001（col_ssn） |
| CQ3 | governance | 4 dataset | allow（R8） | 4 dataset | query log |
| LEAK-T1 | analyst | 3 列 | skip（R5） | returned t_hr/col_ssn（leak） | dec-0002 |

## 1. raw：查询本身返回什么

- CQ1 找 `:Email` 及子类；`tag_email_1` 是 `:WorkEmail`（`Email` 子类），加上 `col_customer_email`，所以 2 列 / 2 表。
- CQ2 找 level≥3；7 列 / 4 表。
- CQ3 找“没有带 level 的 tag”的列，按 dataset 分组；4 个 dataset 各 1。
- 这些数字在 [B.2](../body/consume.md)；它们**不经过 policy**，所以不要拿它们当“最终可见结果”。

## 2. policy：谁能不能看

- CQ1 的列 level=3：steward 命中 R4（allow）；analyst 命中 R2（level 3–4，deny）。同一 query，两个 principal，两个结果。
- CQ2 的 7 列都是 level≥3：steward allow；analyst 全 deny，所以 0 列（7 列全拒）。
- CQ3 是 dataset 级：governance 命中 R8（allow）；analyst 不适用（它没有 dataset 级规则，R5 是 skip）。没有 subject 的聚合查询不在列策略覆盖内。
- LEAK-T1 的 subject 是 table：R5 给 **skip**。skip 是“未判定”，不是 allow，也不是 deny；执行层可以返回，也可以 withhold。

判定顺序和 11 条测试见 [C.2](../body/govern.md)。T9 是故意留的 `undetermined`：steward 读 table 同时命中 R4 allow 和 R5 skip，两者同优先级。

## 3. governed：执行层实际返回什么

| 场景 | decision | execution_effect | 结果 |
|---|---|---|---|
| CQ1 steward | allow | returned | 2 列 / 2 表 |
| CQ1 analyst | deny | withheld | 0 列 |
| CQ2 analyst | deny | withheld | 0 列（7 列全拒） |
| CQ3 governance | allow | returned | 4 dataset |
| LEAK-T1 trustgraph | skip | returned | t_hr/col_ssn（leak） |
| LEAK-T1 安全过滤器 | skip | withheld | 无 col_ssn |

**LEAK-T1 的通过条件不是“0 行”**，而是“敏感 object `col_ssn` 不出现”。如果过滤器只按 level 去掉 `col_ssn`、留下 `col_dept`，`col_dept` 仍会被 R3 deny（level null），所以本 fixture 的 governed 结果是 0 列（结果为空）；关键是 `col_ssn` 不出现，0 列是 policy 的结果，不是 leak 的定义。

## 4. audit：留什么

- **per-subject**：dec-0001 只记 `col_ssn`，outcome 是“col_ssn withheld”；不是“CQ2 的 0 列（7 列全拒）”。
- **query 级 summary**：CQ2 的 0 列（7 列全拒）在 [C.4](../body/govern.md) 的 query log 表，不塞进一条 subject 记录。
- **3 条样例**：[audit_records.json](../example/audit_records.json) 有 deny / skip+leak / allow 三种；CQ2 的其余 6 列、CQ3 的 governance 记录只出现在 query log，不是 JSON 全集。
- **replay**：同 fixture 对照可以；严格 replay 需要内容 hash + parser 版本，当前 snapshot 是日期标签，见 [A.5](../body/build.md) 的版本来源表。

## 5. 这页不证明什么

- 不证明执行层安全：trustgraph 仍然 fail-open、只删 subject；参考过滤器只是文字对照，不是交付实现。
- 不证明生产：没有真实误报率、延迟、规模、权限。
- 不证明 policy 完整：T9 未定、clearance 未消费、聚合查询没有 subject。
