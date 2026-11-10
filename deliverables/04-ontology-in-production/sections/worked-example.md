---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 第二个 worked domain：3 表 / 6 列（示意）

> **给谁**：已经读完 [transfer](./transfer.md)，想看「同一套推导换一个域」的人。
> **这一页是示意图，不是第二个 fixture**：没有 TTL/JSON，不要求跑；数字只说明这套推导自洽，不是测量。
> 为了演示多标签，这个域**故意**让 `ticket_body` 带两个 tag；主 fixture 是单标签。多标签规则选 B（最严），换 A/C 数字会变（见 §5）。

## 1. 域

客服工单 + 付款，2 个 dataset、3 张表、6 列。

| dataset | table | column | tag(s) | level | 备注 |
|---|---|---|---|---|---|
| ds_support | t_account | acct_email | Email | 3 | |
| ds_support | t_account | acct_phone | Phone | 3 | |
| ds_support | t_ticket | ticket_subject | — | — | 坏样本：`hasTag "subject"` 字面量 |
| ds_support | t_ticket | ticket_body | FreeText + PII | 2 + 3 | 多标签；规则 B 取 max=3 |
| ds_billing | t_payment | card_last4 | Financial | 4 | |
| ds_billing | t_payment | pay_status | — | — | 未打标 |

- 结构类：`Dataset` / `Table` / `Column`（3）。
- 标签类：`Tag` / `PII` / `Email` / `Phone` / `Financial` / `FreeText`（6）；`Email`/`Phone`/`Financial` 是 `PII` 子类，`FreeText` 直接挂 `Tag`。
- 合计 **9 类 / 5 属性**。属性：`columnOfTable`、`tableInDataset`、`hasTag`、`sensitivityLevel`、`hasColumn`。
- `owl:inverseOf` 只是文档；`hasColumn` 与 `columnOfTable` 两侧显式写。

## 2. TBox（9 类 / 5 属性）

| 类 | 父类 | 为什么在 | 用在哪 |
|---|---|---|---|
| `Dataset` / `Table` / `Column` | — | 查询主语/连接点 | CQ2、CQ3 |
| `Tag` | — | 等级挂载 + shape target | A.4 |
| `PII` | `Tag` | 个人信息分组，同时是 `ticket_body` 的 tag | CQ2、R2 |
| `Email` | `PII` | CQ1 要查 | CQ1 |
| `Phone` | `PII` | 等级 3 | CQ2、R2 |
| `Financial` | `PII` | 等级 4 | CQ2、R2 |
| `FreeText` | `Tag` | `ticket_body` 的正文标签；等级 2 | CQ2、R1 |

> 和主 fixture 的 `PII` 不同：这里 `PII` **被直接用作 tag**（`tag_pii_1`），不是只作分组。这样能演示「父类也能挂等级」。

## 3. 三条 CQ（raw）

| CQ | 契约行 | 问题 | 主语 → 输出 | 过滤 / 连接 | expected | 0 行先问 |
|---|---|---|---|---|---|---|
| CQ1 | 应用/analyst | 哪些列是 `Email`（含子类） | Column → col/table | `hasTag` + `subClassOf* Email` | 1 列 / 1 表 | TBox 同图？子类边？ |
| CQ2 | 应用/analyst | 哪些表至少有一列 level ≥ 3 | Column → table/col | `hasTag` + `level ≥ 3` | 4 列 / 3 表 | 多标签取了哪个 level？ |
| CQ3 | 治理/governance | 哪些 dataset 有「没有带 level 的 tag」的列 | Column → dataset/count | `NOT EXISTS` + `tableInDataset` | 2 dataset ×1 | 类型写了？dataset 边？ |

**CQ2 的手算**（规则 B，max）：

- `acct_email` 3 → t_account
- `acct_phone` 3 → t_account
- `ticket_body` max(2,3)=3 → t_ticket
- `card_last4` 4 → t_payment
- 去重后 **4 列 / 3 表**。

**CQ3 的手算**：`ticket_subject`（字面量 tag，无 level）+ `pay_status`（无 tag）→ `ds_support` 与 `ds_billing` 各 1，共 **2 dataset**。

> `ticket_subject` 的坏标注会被 CQ3 当「未打标」——和主 fixture 的 `col_legacy` 一样，这是「坏标注」和「没标注」在 CQ3 里不可分的已知问题；shape 能把它单独报出来。

## 4. 两条 shape（2 violations）

| 约束 | 形态 | target | 已知违反 | 干净样本 | 结果 |
|---|---|---|---|---|---|
| Tag 有 1–4 的整数 level | `TagHasLevel` | `:Tag` | `tag_unknown` 缺 level | `tag_email_1` | 1 violation |
| `hasTag` 非字面量 | `HasTagClass` | `hasTag` subjects | `ticket_subject` → `"subject"` | `acct_email` → Email | 1 violation |
| 未打标可发现（CQ3） | CQ（不是 shape） | — | `ticket_subject` / `pay_status` | `acct_email` | 不计数 |

`targeted=2`；`violations=2`；干净样本误报未测（写「未测」）。

## 5. 多标签：规则 B 的算法与 A/C 的差别

`ticket_body` 有两个 tag：FreeText(2) + PII(3)。三种规则下的 CQ2：

| 规则 | 怎么取 level | CQ2 结果 | 必须写清 |
|---|---|---|---|
| **A 单标签归一** | 先合并成一个主标签 | 主标签 FreeText(2) → **3 列 / 2 表**；主标签 PII(3) → **4 列 / 3 表** | 合并规则/谁裁决 |
| **B 集合最严** | 任一 tag deny 即 deny；level 取 max | **4 列 / 3 表**（本页采用） | C.2 规则要按 sets 重写 |
| **C 逐标签判定** | 每 tag 一条 decision；query 级取最严 | CQ2 列数同 B（4/3）；audit 每条 tag 一条 | query 级聚合规则 |

> 这张表就是 [transfer §6.2](./transfer.md#p-multitag) 的实例：**多标签不是「加一个 tag」，它会改 CQ 的数字、policy 的输入和 audit 的粒度**。选 A 时必须写「哪个是主标签」，否则结果不可复算。

## 6. policy（5 条规则 + 5 条测试）

principal 模型选 **B：终端用户角色**（`analyst` / `governance`）；`user_context.role` 透传。

| id | principal | action | kind | condition | effect | priority |
|---|---|---|---|---|---|---|
| R1 | analyst | read | column | level 1–2 | allow | 10 |
| R2 | analyst | read | column | level 3–4 | deny | 10 |
| R3 | analyst | read | table / dataset | — | skip | 20 |
| R4 | governance | read | dataset | — | allow | 10 |
| R5 | any | any | any | 无命中 | deny（default） | 99 |

| 用例 | principal | action | kind | level | 期望 | reason | 命中 |
|---|---|---|---|---|---|---|---|
| T1 | analyst | read | column | 2 | allow | policy_allow | R1 |
| T2 | analyst | read | column | 3 | deny | policy_deny | R2 |
| T3 | analyst | read | table | null | skip | table_subject_not_judged | R3 |
| T4 | analyst | delete | column | 1 | deny | default_deny | R5 |
| T5 | governance | read | dataset | null | allow | policy_allow | R4 |

> T5 只命中 R4；R3 的 principal 是 analyst，不匹配 governance。T3 只命中 R3 → skip。T4 没有命中 → default deny。

## 7. raw → governed → audit

| query | principal | raw | decision | governed |
|---|---|---|---|---|
| CQ1 | analyst | 1 列 / 1 表 | deny（R2, level 3） | 0 列 |
| CQ2 | analyst | 4 列 / 3 表 | deny（逐列） | 0 列 |
| CQ3 | governance | 2 dataset | allow（R4） | 2 dataset |
| MINI-LEAK-1（表页探针） | analyst | 2 列 | skip（R3） | returned acct_email/acct_phone（leak） |

表页探针：`SELECT ?col WHERE { :t_account :hasColumn ?col }` → `acct_email`、`acct_phone`；analyst 本不该看，但 R3 对 table 只是 skip，执行层返回 → `object_direction_failed`。

审计最小样例：

```json
{"decision_id":"mini-0001","query_id":"CQ1","who":"analyst:alice","judged_subject":":acct_email","subject_kind":"column","resource_level":3,"decision":"deny","reason":"policy_deny","execution_effect":"withheld","leak_check":"passed"}
```

```json
{"decision_id":"mini-0002","query_id":"MINI-LEAK-1","who":"analyst:alice","judged_subject":":t_account","subject_kind":"table","resource_level":null,"decision":"skip","reason":"table_subject_not_judged","execution_effect":"returned","leaked_object":":acct_email","leaked_object_level":3,"leak_check":"object_direction_failed"}
```

> 只展示判定相关字段；完整必填字段（executor/snapshot/policy_version/tag_version/obligation/evidence/outcome/user_context）见 [audit.schema](../example/audit.schema.json) / [C.4](../body/govern.md)。

## 8. build_report（示意）

| 字段 | 值 |
|---|---|
| `classes` / `properties` | 9 / 5 |
| `shapes` / `targeted` / `violations` | 2 / 2 / 2 |
| `answer.CQ1` | 1 列 / 1 表（analyst, raw） |
| `answer.CQ2` | 4 列 / 3 表（analyst, raw） |
| `answer.CQ3` | 2 dataset（governance, raw） |
| `policy_version` / `ontology_version` | 0.1.0 / 0.1.0 |
| `snapshot` / `parser` | 示意，无 hash；未跑 |

> 这是「按规则手算」的表，不是运行记录；`snapshot`/`parser` 没有，所以不能 replay。

## 9. 和主 fixture 的差别

| 项 | 主 fixture | 这个域 |
|---|---|---|
| 规模 | 5 表 / 13 列 / 5 dataset | 3 表 / 6 列 / 2 dataset |
| 类 / 属性 | 11 / 5 | 9 / 5 |
| 标签 | 单标签 | `ticket_body` 多标签 |
| policy / 测试 | 8 / 11 | 5 / 5 |
| principal | 契约未写死（steward vs analyst） | 明确选 B（用户角色） |
| object 方向 | trustgraph fail-open | 同样会泄漏（MINI-LEAK-1） |

**这页说明**：同一套 5 问/4 步/3 步/5 步可以换域走一遍；多标签会改数字；object 方向不是 policy 能修的。
**这页不说明**：你的域可迁移；规模可扩展；标签源可用；效果/成本。

## 10. 相关页

- 推导方法：[transfer](./transfer.md)；填表：[templates](./templates.md)。
- 标签来源/准入：[label-source](./label-source.md)。
- 主 fixture：[example/README](../example/README.md)。
- 拍板：[decision](./decision.md)。
