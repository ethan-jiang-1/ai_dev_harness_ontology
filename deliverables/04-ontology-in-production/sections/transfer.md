---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 从你的表到这条链：4 个推导 + 2 个决策

> **给谁**：已经决定要试这条链、手上有一份自己的表/列清单的团队。
> **回答**：怎么从「你的 5 张表 + 3 个消费者问题」推到 04 的 9 件产物；哪两件事必须你先拍板。
> **不回答**：值不值得做（去 [01](../../01-capability-status/README.md)）、接哪个缝（去 [02](../../02-engineering-playbook/README.md)）、为什么是这些位置（去 [03](../../03-mechanism-reference/README.md)）。
>
> 这一页是**推导单**，不是第二份 fixture，也不是实施任务。它只把 [A](../body/build.md)/[B](../body/consume.md)/[C](../body/govern.md) 里已经成立的产物，倒着拆成「输入 → 判断 → 产物」。
> 每一步的产物都能回 04 的九件产物；涉及证据的地方标 `已核 / 推测 / 未测`。填表用 [templates](./templates.md)；想看换一个域怎么走，读 [worked-example](./worked-example.md)。

## 0. 先记住三条

1. **只建被用到的**：一个类/属性/规则，写不出「被哪条 CQ、shape 或 policy 用」就不建。fixture 删 `Address` 就是这个判据。
2. **每条推导要有停**：填不出契约、写不出 CQ、`targeted=0`、object 探针返回敏感列——四个位置任一出现，停在前一步，不要往下堆。
3. **04 不替你做的两个决定**：`principal` 判谁、多标签列怎么取 level。见 §6。这两件事不拍板，后面的 policy 与 audit 都是假的。

## 1. 一张表：从输入到九件产物

| 你手上有什么 | 推导 | 产物 | 验收 | 模板 |
|---|---|---|---|---|
| 消费者、时刻、拒绝条件 | 契约 6 项 + 2 个决策（§6） | ① 消费者契约 | A1 | [T1](./templates.md#t1-契约) |
| 表 / 列 / 标签清单 | 5 问 → 类 + 属性（§2） | ② TBox / ABox | A2–A3 | [T0](./templates.md#t0-表列清单) / [T2](./templates.md#t2-tbox-清单) / [T3](./templates.md#t3-属性与边清单) |
| 「哪种数据错会让 CQ 静默错」 | 3 步 → shape + 负例（§4） | ③ shapes | A3–A4 | [T4](./templates.md#t4-shape-与负例) |
| 契约的 `answers` | 4 步 → CQ（§3） | ④ 3 条 SPARQL | A5 / B1–B3 | [T1](./templates.md#t1-契约) |
| 标签 + 等级 + 角色 | 5 步 → policy（§5） | ⑤ policy 表 | C1–C2 | [T5](./templates.md#t5-policy-表与测试) |
| 每条规则 + 冲突/默认/skip | 用例表 | ⑥ 策略测试 | C2 | [T5](./templates.md#t5-policy-表与测试) |
| 查询面 / 表页面 / 聚合 / 版本 | 12 面 | ⑦ 泄漏用例 | C3 / C5 | [reference §5](./reference.md#5-读路径十条用例) |
| 每个 decision | 最小单元 | ⑧ audit schema + 记录 | C4 | [T6](./templates.md#t6-audit-记录) |
| 三段故障 | 10 类 × 3 段 | ⑨ 故障矩阵 | 骨架；未做注入实验 | [reference §7](./reference.md#7-故障矩阵10-类--3-段) |

> `build_report` 是 A.5 的内联样例，不单独成文件；所以是「九件产物」，不是十件。

## 2. 推导 1：表 / 列 → TBox（5 问）

不要从「本体应该长什么样」开始，从「哪条 CQ / shape / policy 要用它」开始。

| # | 问 | 提示 / 答不出时 | 产物 |
|---|---|---|---|
| Q1 | 哪些对象会被查询或判定？通常只有三类：数据集、表、列 | 先写 3 条 CQ 的主语；主语只有列/表/数据集 | `:Dataset` / `:Table` / `:Column` 三个结构类 |
| Q2 | 哪些「标签」要参与查询或策略？ | 只建 CQ1–CQ3 和 policy 真正用到的；不要照搬 Glyph 275 叶 | `Tag` 层级（fixture 8 个，含 Tag） |
| Q3 | 等级挂在哪？ | fixture 挂 `Tag`（等级是标签的属性）；挂 `Column` 也可以，但 policy 输入要跟着改 | `:sensitivityLevel` |
| Q4 | 哪些关系要被 join？ | 列→表、表→数据集、列→标签；反向边要不要显式写 | `columnOfTable` / `tableInDataset` / `hasTag` |
| Q5 | 哪些只是文档、哪些要执行？ | `owl:inverseOf` 只是文档；`rdfs:subClassOf*` 要执行就必须 TBox 与 ABox 同图 | 物化边 / 同图加载 |

**fixture 的 11 类是怎么来的**（把这张表换成你的）：

| 类 | 为什么在 | 被谁用 | 你的判断 |
|---|---|---|---|
| `Dataset` / `Table` / `Column` | 结构类，查询的主语/连接点 | CQ2、CQ3、R8 | 你的表/数据集要不要分开建 |
| `Tag` | 等级挂载点 + shape 的 target | A.4（shape target）；C.2 的 level 来源 | 等级挂 tag 还是挂 column |
| `PII` | 标签层级的父类 | **没有 CQ/shape/policy 直接用它**；fixture 保留作分组 | 你需要「所有 PII」查询吗？不需要就删 |
| `Email` / `WorkEmail` | CQ1 要测子类 | CQ1（`subClassOf*`） | 你的标签有子类吗？没有就扁平 |
| `Phone` / `Name` / `Financial` / `SSN` | 不同标签 + 等级 | CQ2（level 来自 tag）；标签层级 | 只建会被查询/判定的标签族 |
| `Address` | 已删 | — | 没有任何 CQ/shape/policy 用 → 删 |

**标签从哪来**：这一节只决定「建哪些类」；标签源是否可信、覆盖多少列、漏标多少，见 [label-source](./label-source.md)。

**读法**：`PII` 是 fixture 里最容易被问「用在哪」的类——它只作分组，不被任何 CQ 直接查。你的 TBox 清单如果写不出「用在哪」，就按 `Address` 的判据删掉，而不是为了「层级完整」保留。保留/删除是工程选择（`推测`），但必须写理由。

**你的 TBox 最小检查**（经验值，`推测`）：

- 类数 5–10 个起步；超过 10 个先问「哪个类没有 CQ/shape/policy 用」。
- 结构类 3 个（dataset/table/column）+ 标签类 N 个 + 可选的父类。
- 属性 5 个左右：`columnOfTable`、`tableInDataset`、`hasTag`、`sensitivityLevel`，加一个业务关系也够。
- 要 join 的反向边（`hasColumn`）两侧显式写；`owl:inverseOf` 不 entail。
- 同一列多个标签怎么办？见 §6.2；不决定就不要写 shape。

## 3. 推导 2：消费者问题 → CQ（4 步）

CQ 不是「写一条 SPARQL」，是「把契约里的一行变成可核对的问题」。四步：

1. **点名**：从契约的 `answers` 里挑一个名词短语，写成「谁、在什么时刻、要哪些对象的哪些属性」。
2. **定主语/输出**：主语是列、表还是数据集？输出是列清单、表清单，还是计数？
3. **定过滤/连接**：标签/子类/等级/未打标；join 走 `columnOfTable` / `tableInDataset`。
4. **定 expected**：行数/列数/表数/数据集数；principal；raw 还是 governed；0 行先问什么。

fixture 的三条：

| CQ | 契约行 | 问题 | 主语 → 输出 | 过滤 / 连接 | expected | 0 行先问 |
|---|---|---|---|---|---|---|
| CQ1 | UI | 哪些列是 `Email`（含子类） | Column → col/table | `hasTag` + `subClassOf* Email` | 2 列 / 2 表 | TBox 同图？子类边？ |
| CQ2 | agent | 哪些表至少有一列 level ≥ 3 | Column → table/col | `hasTag` + `level ≥ 3` | 7 列 / 4 表 | level 缺失？tag 缺失？ |
| CQ3 | governance | 哪些 dataset 有「没有带 level 的 tag」的列 | Column → dataset/count | `NOT EXISTS` + `tableInDataset` | 4 dataset ×1 | 类型写了？dataset 边？ |

**写不出的三个信号**：

- 只能写成一句自然语言，写不出主语/输出 → 它不是 CQ，是需求；回 A.1 改契约。
- 写出来了，但 expected 说不出 → 它还不能验收；先补「期望几行/几列」。
- 写出来了，0 行不能分因 → 先补 [B.2 的 ASK 表](../body/consume.md#b2-三条查询--空结果分因)，不要先调 prompt。

**一个反例**：A.1 说「CQ 只是模板词，须在契约行可执行」。如果某一行写不出 1 个 CQ 或 1 个拒绝条件，删这行；不要为了填满 3 行编一个消费者。

**CQ1 的隐藏前置**：`?t a/rdfs:subClassOf* :Email` 需要 `ontology.ttl` 与 `catalog.ttl` **同图**。只加载 ABox 会得到 1 行（`tag_email_1` 的 `WorkEmail` 子类边不在图里）。这是 fixture 的坑，也是你落地时的第一条检查。

## 4. 推导 3：CQ → shape / 检查（3 步）

shape 不是「给本体加约束」，是「哪种数据错会让这条 CQ 静默错」。三步：

1. **找静默错**：缺 level → CQ2 少列；tag 是字面量 → CQ1 少行/0 行；无 dataset 边 → CQ3 少 dataset。
2. **选形态**：能写成 target + property + 条件 → shape；只能写成查询 → CQ/ASK（如 CQ3）；两者都不行 → 记 gap，不要硬造。
3. **配负例**：每条约束至少 1 个已知违反 + 1 个干净样本；没有负例 = 未验证。

| 约束 | 形态 | target | 已知违反 | 干净样本 | 现在抓住？ |
|---|---|---|---|---|---|
| Tag 有 1–4 的整数 level | `TagHasLevel` | `:Tag` | `tag_unknown` 缺 level | `tag_email_1` | 是 |
| `hasTag` 非字面量 | `HasTagClass` | `hasTag` 的 subjects | `col_legacy` → `"email"` | `col_email` → WorkEmail | 是 |
| 未打标可发现 | CQ3（不是 shape） | Column/dataset | `col_order_id` 等 4 列 | `col_email` | 不是 shape，是查询 |
| shape 缺 target | 检查项 | — | S6 | — | 否：0 focus → `conforms=true` |
| 无 dataset 边 | ASK / 检查项 | — | S9 | — | 否：不报 |

**停**：`targeted=0` 不是 pass；`violations=2` 只证明两个已声明样本被抓住，不证明干净数据无误报。没有 `clean_fp` 就写「未测」。

**不要为了完整硬造 shape**：CQ3 是查询，不是约束；dataset 边是 gap。把它们写成 shape 会让「targeted」虚高，反而掩盖空转。

## 5. 推导 4：标签 / 等级 → policy（5 步）

1. **列取值域**：principal / action / kind 各有哪些值。principal 不是 consumer 的名字，见 §6.1。
2. **标签 → level**：这是工程映射，不是标准。GB/T 43697 只分核心/重要/一般三级；GB/T 35273 只定义个人信息/敏感个人信息；「level 4 → 谁能读」是你的默认（`已核` 标准 / `推测` 映射）。标签源准入见 [label-source](./label-source.md)。
3. **写规则**：id / principal / action / kind / condition / effect / priority / obligation；default 与 skip 的 reason 单独写。
4. **冲突消解**：priority 数字最小；同优先级不同 effect = `undetermined`；不要偷偷把 T9 修成 allow/deny。
5. **写测试**：每条规则至少 1 个 allow/deny/skip 用例；default / skip / 平局各 1 条；`clearance` 只有被规则消费才算输入。

**三条硬规则**（抄自 [C.2](../body/govern.md)）：

- 先 `kind` 后 `level`：表/数据集不按列判。
- `skip` ≠ `allow`：它是第 4 种效果，必须带 reason。
- 不要用 `clearance` 做条件，除非你新写一条消费它的规则。

**一个反例**：policy 里写 `analyst`，但契约里只有 `steward` / `governance`。先补契约或说明 analyst 是 UI 的终端用户；不要直接跑测试，否则 11 条全绿也只证明「测试和契约不是一套」。

**你的 policy 最小检查**：

- 规则数按 `principal × action × kind` 的必要组合来；fixture 的 8 条是 4 个 principal（analyst/steward/service/governance）+ 列/表/dataset 的最小覆盖，不是标准。
- 至少 1 条 default；如果有表/数据集读，至少 1 条 skip；至少 1 条平局，或写清为什么你的规则没有平局。
- 每条规则至少 1 个测试；没有测试的规则 = 未验证。
- 规则里的 principal 与契约的 principal 对齐；对不齐就停，不要用测试数量掩盖。

## 6. 两个必须你定的选择

<a id="p-principal"></a>
### 6.1 `principal` 是服务身份还是用户角色？

04 里三个名字容易混：

| 名字 | 是什么 | 04 里在哪 | 你的契约要写 |
|---|---|---|---|
| `consumer` | 调用方：UI / agent / governance job | A.1 的 consumer 列 | 谁调用 |
| `principal` | policy 判定用的身份：用户 / 角色 / 服务账号 | C.2 的 policy 输入 | 判谁 |
| `user_context` | 请求携带的 `role` / `clearance` | C.4 的 audit 记录 | 怎么带、谁透传 |

**fixture 没有把这层写死**：A.1 把 `UI` 和 `steward` 放在同一行；C.4 的 query log 又列出 CQ1 在 `analyst` 下是 0 列（audit 样例未列）。两种读法都说得通——「UI 以 steward 服务身份读」或「UI 代终端用户 analyst 读」。但两者后果完全不同：

| 你的选择 | policy 判谁 | 结果 | 必须补 |
|---|---|---|---|
| **A 服务身份** | consumer 的服务账号（如 `steward`） | 应用能读全部列；列级拦截只能靠执行层 post-filter | 可信执行层 + object 方向测试；否则 UI 用户能看到 analyst 不该看的列 |
| **B 终端用户角色** | 登录用户的 role（`analyst` / `steward`） | 列级策略能按用户拦 | 认证 + `user_context` 透传；audit 的 `who` = 用户 |
| **C 两层都判** | 先 service 再 user，取交集 | 更安全，但复杂 | 委托模型 / 两层策略 / 审计两段 |

> 这是**工程选择**（`推测`），04 不替你选。fixture 的 CQ1 在 steward 下是 2 列 / 2 表、analyst 下是 0 列：如果这个 0 要由 policy 判出来，选 B（或 C 的 user 层）；如果由执行层过滤出来，选 A 也能得到 0，但就把安全押在执行层上了。把选择写进契约，再写 policy。

**落地检查**：拿一条真实请求，画出 `consumer → user_context → principal → decision → executor` 五步；哪一步断了，就在哪一步停，不要用「策略表看起来对」补。

<a id="p-multitag"></a>
### 6.2 一列多个 tag，level 取哪个？

04 的 fixture 是**一列一个 tag**；Glyph 是**列级多标签**（每列输出本体子集 `Y ⊆ O`；`已核`，Glyph digest；单企业，E-22）。fixture 的 shape 没有 `sh:maxCount 1`，policy 的 `resource_level` 是标量——所以真实多标签数据会在两个地方漏：

- CQ2 的 `DISTINCT` 把多 tag 的行折叠，看起来没问题，但 `level` 取了哪一条不清楚。
- policy 的 `resource_level` 只有一个值；如果两 tag 是 Email(3) + SSN(4)，判 3 还是 4 没有定义。

三个可选规则（选一个，写进契约 + shape）：

| 规则 | 怎么做 | policy 输入 | 代价 | 适合 |
|---|---|---|---|---|
| **A 单标签归一** | 加 `sh:maxCount 1`；多标签先合并/人工裁决成一个主标签 | 不变（标量 level） | 丢信息；合并规则要人审 | 标签少、可人工裁决 |
| **B 集合判定（最严）** | 保留多 tag；policy 输入改成 `levels`；任一 tag deny 即 deny | 改 schema / 改 condition | C.2 的 8 条规则要重写；CQ2 要 `COUNT(DISTINCT)` | 安全优先 |
| **C 逐标签判定** | 每 tag 一条 decision；query 级取交集/最严 | 不变，但记录多条 | audit 膨胀；query 级聚合要定 | 审计优先 |

> 这是工程选择（`推测`）；04 不替你选。选 A 就在 shape 里写死；选 B 就把 C.2 的规则表当模板重写；选 C 就在 audit 里加 `decision_group`。不选 = 多标签列的结果不可复算。

## 7. 最小路径：五个检查点

> 按产物分，不按日历；时间是量级（`推测`），不是报价。每一步的「停」比「过」重要。

| 检查点 | 入口 | 产物 | 通过 | 停 | 量级（`推测`） |
|---|---|---|---|---|---|
| **0 契约** | 3 个 owner（UI/数据/治理） | 契约 6 项 + §6 两个决策 + 3 条 CQ 草稿 | 3 条 CQ 写得出；每行有 1 个拒绝条件或明确 `—` | 填不出 → 不建 | 3–5 天 |
| **1 最小 TBox** | 检查点 0 | 5–10 类 + 5 属性 + 3 条 CQ raw | CQ 跑通；0 行能分因 | CQ 写不出 / 0 行无因 → 停 | 2–4 周 |
| **2 闸门** | 检查点 1 | 2 条 shape + 负例 + `build_report` | `targeted>0`；坏样本被抓住；干净样本 | `targeted=0` 当 pass → 停 | 3–5 天 |
| **3 策略 / 审计** | 检查点 2 | policy 表 + 测试（fixture 8/11）+ audit schema + 3 条记录 | 10/11 有唯一期望；T9 显式；object 探针 | object 泄漏未修 → conditional | 1 周 |
| **4 验收** | 检查点 3 | 5 组门槛 + 验收记录 | 5 组全过，或明确 conditional | 缺一条 → 演示/conditional | 0.5–1 天 |

> 成本工作纸见 [templates T9](./templates.md#t9-成本工作纸)；公式与敏感性见 [decision §2.5](./decision.md)。

**如果只有半天**：只做检查点 0 的契约草稿 + [T0](./templates.md#t0-表列清单) 清单，不要建 TBox。
**如果只有两天**：加 3 条 CQ 草稿与 raw 验证；TBox 从 5 个类开始，不要照抄 11 类。
**如果已经有一个能用的执行层**：从检查点 3 开始；但契约与 TBox 仍要补，否则 policy 没有主语。

## 8. 证据与边界

> 方法来自 A/B/C 与 `topics`；这一页不新增 E，也不把工程方法写成效果判断。

- **推导规则**：A.1（契约）、A.3（TBox）、A.4（shape/负例）、A.5（三关）、B.2（CQ/0 行）、C.2（policy/冲突）、C.4（audit）——这是工程方法，不是测量。
- **principal 模型**：A.1 / C.2 / C.4 的字段能看出三层，但 fixture 没有写死；三种选择是工程选择（`推测`），没有实测。
- **多标签**：Glyph 是列级多标签（`已核`，Glyph digest；单企业，E-22）；04 fixture 是单标签；三种规则是工程选择（`推测`），没有实测。
- **成本/工期**：2–4 人周建模、3–5 人日 shapes 是 SFE-O digest 自标 `推测` 的估算，未绑定流程条数/团队规模；不能当验收线，更不能当报价。
- **不证明**：这套推导在你的域有效；principal/多标签选择正确；规模可扩展；生产误报率/延迟。
- **换域**：第二个 worked domain 见 [worked-example](./worked-example.md)；它只演示方法，不是效果。
- **停**：契约填不出、CQ 写不出、`targeted=0`、object 泄漏未修、没有 principal/多标签决策——任一出现，停在原地。

## 9. 读完自测（6 题）

1. 你能说出 CQ1 在 steward 与 analyst 下为什么不同，以及这个不同是 policy 判的还是执行层过滤的吗？
2. `targeted=0` 为什么不是 pass？`violations=2` 为什么不能证明干净？
3. LEAK-T1 为什么「0 行」不是 leak 的定义？通过条件是什么？
4. 你的契约里 `principal` 是服务身份还是用户角色？policy 判哪个？写进契约了吗？
5. 你的多标签列，level 取哪个？shape 里写死了吗？policy 的输入还是标量吗？
6. 你的标签源过得了 [label-source](./label-source.md) 的 3/4/5 硬门吗？没有漏标/覆盖率，你敢接 deny 吗？

> 五题里有一题答不出，回到对应小节；不要用「先建起来再说」跳过。
