---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 可填模板：表/列、契约、TBox、shape、policy、audit、验收、成本

> **给谁**：已经读完 [transfer](./transfer.md)、要开始填自己那一份的团队。
> **怎么用**：复制到你的项目文档，逐格填；**填不出就写「不知道」或「未做」，不要编**。每一格都有「判据」；没有判据的格，说明你还没决定。
>
> 这些是**空表**，不是 04 的 fixture；不要照抄 11 类、8 条规则、3 条 CQ。模板只保证「字段齐」，不保证「内容对」。

## 0. 使用规则

1. **先填 T1 和 T0**：T1 是契约，T0 是你的表/列清单；T1 填不出，后面的 T2–T7 不用填；T0 填不出，T2 只能照抄 fixture。
2. **每个「通过」要有证据**：文件、命令输出、或一条可复跑的查询；「未测」不是「通过」。
3. **两个决策先拍板**：principal 模型、多标签规则（[transfer §6](./transfer.md#6-两个必须你定的选择)）。没拍板，T5 的 policy 表先空着。
4. **模板不是验收**：填完只说明字段齐；能不能上线看 [acceptance](./acceptance.md) 的 5 组门槛。

<a id="t0-表列清单"></a>
## TPL-0 表 / 列清单（起点）

| 表 | 列 | 类型 | 现在有标签？ | 等级 | 多标签列？ | 备注 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

**判据**：

- 一列一行；不知道标签/等级写 `?`，不要猜。标签从哪来、够不够：见 [label-source](./label-source.md)。
- 「多标签列？」写 Y/N；写 Y 的列就是 [transfer §6.2](./transfer.md#p-multitag) 的样本，先别急着建 shape。
- 这张表是 T2（TBox）和 T4（shape）的输入；没有它，TBox 只能照抄 fixture 的 11 类。

<a id="t1-契约"></a>
## TPL-1 契约

| consumer | principal | moment | answers（CQ id + 期望） | refuses（条件） | load（怎么加载） |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

**判据**：

- 每行 6 项有值；`refuses` 写 `—` 表示「明确不拒」，不算空。
- `answers` 至少 1 个 CQ id；`refuses` 写 `—` 时，要在 `answers` 里说清为什么不需要拒绝（fixture 的 UI/agent 就是这样）。
- `principal` 写「判谁」，不是「谁调用」；三层见 [transfer §6.1](./transfer.md#p-principal)。

**两个决策**（填在契约下面，不要只放在脑子里）：

| 决策 | 你的选择 | 写进哪里 | 谁签 |
|---|---|---|---|
| principal 模型 | A 服务身份 / B 用户角色 / C 两层 | 契约 + policy |  |
| 多标签规则 | A 单标签 / B 集合最严 / C 逐标签 | 契约 + shape + policy |  |

<a id="t2-tbox-清单"></a>
## TPL-2 TBox 清单

| 类 | 父类 | 为什么在 | 用在哪（CQ / shape / policy） | 删 / 留 |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |

**判据**：

- 「用在哪」写不出 → 删（fixture 删 `Address` 的判据）。
- 类数 5–10 个起步；超过 10 个，先删没有用到的。
- 结构类（dataset/table/column）与标签类分开列；标签类只建会被查询/判定的。
- 父类不是「为了好看」：`PII` 这种分组类如果没有 CQ 直接查，写不出用途就删。

<a id="t3-属性与边清单"></a>
## TPL-3 属性与边清单

| 属性 | domain | range | 反向边显式写？ | 用在哪 |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |

**判据**：

- 执行层不 entail：`owl:inverseOf` 只是文档；要 join 的反向边两侧都写。
- `sensitivityLevel` 挂 Tag 还是 Column，写清；挂错，policy 输入就错。
- 每个属性至少被一条 CQ/shape/policy 用；没有就删。

<a id="t4-shape-与负例"></a>
## TPL-4 shape 与负例

| 约束 | 形态（shape / ASK / CQ） | target | 已知违反 | 干净样本 | 现在抓住？ |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
|  |  |  |  |  |  |

**判据**：

- 每条 shape 有 target；`targeted=0` 不是 pass。
- 每条约束至少 1 个已知违反 + 1 个干净样本；没有负例 = 未验证。
- 写不成 shape 的（如 CQ3、dataset 边）就写 ASK/CQ，不要硬造。
- `violations=2` 只证明两个已声明样本被抓住；干净样本误报没测就写「未测」。

<a id="t5-policy-表与测试"></a>
## TPL-5 policy 表与测试

| id | principal | action | kind | condition | effect | priority | obligation | reason |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |

**判据**：

- 至少 1 条 default；如果有表/数据集读，至少 1 条 skip；至少 1 条平局，或写清为什么你的规则没有平局。
- 每条规则至少 1 个测试；没有测试的规则 = 未验证。
- principal 与 T1 对齐；对不齐就停。
- `clearance` 只有被规则消费才写进 condition；否则只记录。

**测试表**：

| 用例 | principal | action | kind | level | 期望 decision | 期望 reason | 命中规则 |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |

**判据**：有唯一期望的用例数写清（fixture 10/11）；平局写 `undetermined`；default 与 skip 各 1 条（如有）；`clearance` 只出现在输入、不影响 decision。

<a id="t6-audit-记录"></a>
## TPL-6 audit 记录

| 字段 | 填什么 | 必填？ |
|---|---|---|
| `decision_id` | 唯一 id | 是 |
| `query_id` | CQ1–CQ3 / LEAK-T1 | 是 |
| `executor` | 执行器 + 版本 | 是 |
| `snapshot` | 内容 hash 或日期标签（写清是哪种） | 是 |
| `who` | `role:user` | 是 |
| `action` | read / write / delete / export | 是 |
| `judged_subject` | 一个 subject | 是 |
| `subject_kind` | column / table / dataset / triple / graph | 是 |
| `judged_triple` | 三元组（可空） | 建议 |
| `resource_level` | 1–4 / null | 建议（列级） |
| `user_context` | role / clearance | 是 |
| `policy_version` / `tag_version` | 版本 | 是 |
| `decision` | allow / deny / skip / undetermined | 是 |
| `reason` | policy_allow / policy_deny / table_subject_not_judged / default_deny / priority_gap | 是 |
| `execution_effect` | returned / withheld / error | 是 |
| `obligation` | log / mask / approve / none | 是 |
| `evidence` | 命中的 tag / 规则 | 是 |
| `outcome` | 实际返回/扣留什么 | 是 |
| `leak_check` | passed / object_direction_failed / ... | 是 |

**判据**：

- 一条记录一个 `judged_subject`；query 级 0 列（7 列全拒）不进 subject 记录，放 query log。
- `execution_effect` 与 `decision` 分开：`skip` 可以 returned，也可以 withheld。
- 严格 replay 需要内容 hash + parser 版本；只有日期标签就写「同 fixture 对照」，不要写「可回放」。

<a id="t7-build_report"></a>
## TPL-7 build_report

| 字段 | 填什么 | 判据 |
|---|---|---|
| `load.parsed` | true / false | 3 个 TTL 是否解析 |
| `load.missing_fields` | 产物缺哪些字段 | 不是契约缺字段 |
| `validate.violations` | shape 违反数 | 与负例表对得上 |
| `validate.targeted` | 有 target 且被检查的 shape 数 | `targeted=0` 不是 pass |
| `validate.caught` / `declared_shape_samples` | 抓住数 / shape 声明样本数 | 分母 1 |
| `validate.contract_bad_samples` / `contract_caught` | 契约坏样本数 / 抓住数 | 分母 2，不要与 shape 混 |
| `validate.clean_fp` | 干净样本误报 | 没测就写「未测」 |
| `answer.CQ1–CQ3` | 期望 vs 实际 + principal + raw/governed | 每条有 `query_id` |
| `classes` / `properties` | 11 / 5（换成你的） | 与 T2/T3 对得上 |
| `policy_version` / `ontology_version` / `tag_version` / `contract_version` | 版本 | 版本来源写清 |
| `snapshot` | 内容 hash 或日期标签 | 日期标签不是 hash |
| `parser` | 执行器 + 版本 | 不记版本就不能跨版本重跑 |
| `provenance.source` | synthetic / 真数据 | `synthetic` 不是 principal |

**判据**：两个分母不要混；`violations=2` 不等于干净；`parsed=true` 不等于可用。

<a id="t8-验收记录"></a>
## TPL-8 验收记录

| 检查 | 结果 | 证据 | 未做 |
|---|---|---|---|
| A1–A5 |  |  |  |
| B1–B5 |  |  |  |
| C1–C5 |  |  |  |

**判据**：没做就写「未做」，不要写「通过」；结果只能是 `go / conditional / no-go / not enough data` 之一（见 [decision](./decision.md)）。完整模板见 [acceptance](./acceptance.md#记录模板)。

<a id="t9-成本工作纸"></a>
## TPL-9 成本工作纸

| 项 | 公式 / 输入 | 你的参数 | 你的值 | 来源 / 备注 |
|---|---|---|---|---|
| 打标 | `N_col × t_label × (1 + r_review)` |  |  | 50 列样本；见 [decision §2.5](./decision.md) |
| 执行层修复 | `spike + fix + test + rollout` |  |  | 3–5 天（`推测`）spike；object 探针 |
| 审计运营 | `QPS × 86400`；`records × bytes × retention`；`sample × minutes` |  |  | 1 周 shadow |
| 维护 | `changes/month × hours` |  |  | policy/tag/形状变更 |
| TCO | 建设 + 运行 + 人审 + 维护 + 失败 |  |  | 02 cost |

**判据**：

- 打标/执行层/审计至少各填 1 个实测数；否则写 `not enough data`，不要出 `go`。
- 人日价/审批分钟价/事故成本是业务输入，不是研究结论；缺项 >2 只出敏感性，不出点估计。
- 参数来源写清（样本/日志/报价）；没有来源的数字不算。
