---
status: draft
type: work-plan
updated: 2026-11-10
target: deliverables/04-worked-example
scope: content-supply
---

# 04 内容供给计划：从「有出处」到「能判断」

> **方向定了：倒查仍是读法，但不再用它当生产方式；改成从 topics 往前压矩阵。**
> 04 的每一章先写清「读者要做的决定」，topics 把它压成一张「选项 × 维度」的表；表里的空格才是 `src/` 的订单。倒查只能证明哪句话没出处；压矩阵才能生产可判断的内容。
>
> 本页是工作底稿，不是交付正文，也不产生 E/L。所有来源能力在入库前标 `待核`，入库后才写等级。

```
12 条承重句（读者要做的决定）
        │ 压成
        ▼
6 件产物（矩阵/目录，新页型 compare.md）──收成──▶ 5 条新 E（04 只引 E）
        │ 空格
        ▼
12 个 M 来源 + 1 个论文槽位（src：标准/OSS/论文）
        │ 填格
        ▼
04：每章 表 → 物 → 目录 → 停
```

**三句话**：

1. **topics 缺的不是来源，是比较页型**——`findings.md` 只会写「每源一条」，04 要的是「选项 × 维度」的决定表。
2. **src 缺的不是论文，是标准、第二实现、策略/审计代码**——28 篇论文已经够压表，空的是策略层与执行层。
3. **04 缺的不是结构，是每章的决定表/产物/失败目录/停**——三链的骨架是对的，格子是空的。

**怎么读**：只看方向 → §0 + §2.2 + §3/§4 标题；要执行 → §5 + §7 + §11；要判断有没有跑偏 → §1 + §2.4 + §7.4。

## 0. 一页结论

- **04 现在不是「写得少」，是「写不进去」**：04 全部 md 17,045 字符里 24 处「模板」、26 处「gap」、7 处「已核」——免责词是证据的约 7 倍。
- **根因是形状错配**：topics 的单位是「每篇来源一条 finding」，04 要的单位是「跨来源一张决定表」。前者写不出后者，交付物只能把「不可比」抄成「模板」。
- **换法**：先定义 12 条承重句，再压 12 张表；用现有 28 篇 + 6 个开源填格子；空格才去 `src/` 买。**8 条靠整理 + 标准/代码补齐，4 条需要新证据（B1/B3 找不到就降级）；6 件产物收成 5 条新 E（E23…E27），04 只引 E。**
- **三波**：W1 查询与输出（先做能落表的）→ W2 策略与执行（补最大空白）→ W3 建与跨段（最难，最后做）。每波一个 gate；不过就删句，不拿模板凑。
- **预算**：约 23 人日（4–5 周，单人）；12 个 M 来源 + 1 个论文槽位 + 6 个 N 候选。
- **停止线**：W3 结束仍 <7 条承重句有表/产物 → 04 并进 02 的 R13，目录删除；不保留一份「处处模板」的独立交付物。
- **不解决**：独立复现、单源、跨域效度；04 的天花板仍是 `已核`，不是 `已证`。这轮只解决「有没有对照」，不解决「能不能复现」。

这次换的不是选题，是工作单位：

| 旧 | 新 |
|---|---|
| 单位是章节 | 单位是承重句 |
| 订单是对象类型（TB/CA/FC/QP/S2/LB） | 订单是矩阵里的空格 |
| 验收是「每句有出处」 | 验收是「每句能改变一个决定」 |
| 缺证据就标模板/gap | 缺证据就删句或降级 |

## 1. 诊断：为什么 28 篇来源没把 04 写厚

### 1.1 四个数

| 数 | 值 | 说明 |
|---|---|---|
| 04 全部 md | 17,045 字符；build 2,620 / consume 3,239 / govern 4,566 | govern 最长，因为它花篇幅解释三层为何不能互推 |
| 标记密度 | `模板` 24 / `gap` 26 / `signal` 5 / `已核` 7 | 免责词是证据的约 7 倍 |
| E 来源 | 19/22 条 ≤1 个来源 | 交付物能引的 E 多数只有 1 个 digest（[阶段盘点](../../../../deliverables/_workpapers/2026-11-10-stage-review.md)） |
| 对象 | 94（H3 36） | E 级 H3 10/10，但 E-03/E-12 的 H3 是 `derived`；对象增长没有带来新来源 |

### 1.2 形状错配（核心）

topics 现有的三件套回答的是「这篇说了什么」：

- `findings.md`：F1/F2/F3，每源一条，末尾写「三条没有头对头」。
- `mechanism.md`：它怎么跑，停在哪。
- `frontier.md`：还缺什么。

04 需要的是另一件东西：**一张表，行是选项，列是维度，单元格是「数 + 条件 + 锚」，空格写「不可比 / 未测」**。现有页没有这个形状，所以 04 的作者只能把 F1 抄成一段、把「没有头对头」抄成边界、把缺失抄成模板。

**不是来源不够，是 topics 没有把来源压成可比较的格子。**

### 1.3 逆向倒逼的边界

- 倒查能回答「这句话有没有出处」，不能回答「这句话要什么证据才成立」。
- 订单是对象类型（TB/CA/FC/QP/S2/LB），产出的是地址；94 个对象里多数是把已有数字再定位一次，不是新对照。
- 04 的章节形状被证据供给决定：有 E-21 就写三路线，有 E-22 就写三层；读者要的「怎么选、怎么停、失败长什么样」没有供给，于是写成模板。

一句话：**可引用性 ≠ 可判断性。** 上一轮解决的是前者。

倒查仍是合法**读法**（[loading](../../../workflow/loading.md) 的三条链不改）；它只是不能当**生产方式**——读的时候从交付物倒查，写的时候从决定往前压。

单源与无复现仍是天花板：它决定 04 不能写「已证」，但不解释为什么连「已核的对照」都没有。这轮先补后者。

### 1.4 但 04 不该现在 kill

02/03 确实拼不出同一条端到端链；04 的 fixture + 5 件产物 + 三处 handoff 是独有资产。问题不是存在性，是密度。本计划的目标是让它**每一章有一张表、一个物、一份目录、一条停**，不是再加三章。

## 2. 内容定义：12 条承重句

### 2.1 判据

一条承重句 = **决定 + 数/对照 + 条件 + 反例 + 停**。五缺一，不算内容。

- **决定**：读者看完会改哪个动作（建不建、选哪条、停不停）。
- **数/对照**：一个带条件的数，或一张同维度对照；没有就不写。
- **条件**：在什么资产/任务/规模下成立。
- **反例**：什么情况下不成立；与正例同权重。
- **停**：看到什么就停。

### 2.2 12 条清单

> `现在` 列是 04 的现状；`topics 挖出的形状` 才是要交的东西。`src` 列的 M/N 见 §4。

| # | 04 要能说的句子 | 现在 | topics 挖出的形状 | src 要准备的 | 落点 |
|---|---|---|---|---|---|
| **A1** | 契约五格写不出的项目，失败可以归到 `build_report` 的 parsed / violations / missing_fields 三类；10 个坏样本各对应一类 | 模板：契约表 5 格无来源，`build_report` 是示例 | 字段映射表 + 10 个坏样本（缺 principal / moment / refuse / load / version） | M9 ODCS；M8 SHACL test suite | build A.1/A.5 |
| **A2** | 三档表示（词表/结构/逻辑）的能力差可按消费位置判定；薄层优先在「答案不在文本」时失效 | 推测（[05/representation](../../../../topics/05-produce/representation/README.md) 自认无测量；E-12 单工厂） | 3 档 × 4 消费位置（load / validate / query / explain）能力矩阵；E-12 的边界条件 | M10 LinkML；M8 SHACL；E-12 已有 | build A.2 |
| **A3** | 生成物可消费性必须分 load / validate / answer 三关；只测文档质量会把不可加载的产物判为合格 | gap（[05-L7](../../../../topics/05-produce/claims.md)） | 评测协议 + 在 CASTON/OntoDoc 产物上的试跑（仓库外 EXP，或新论文） | P5（N）；CASTON/OntoDoc 已有 | build A.5 / evidence |
| **B1** | 三条路线按「你手上有什么资产」选，不按总分排；每条分支有默认、有反例、有停 | E-21 明确不能排序 | `compare.md` 4×8 矩阵 + 4 分支决策树 | P1 头对头（M，找不到则降级）；现有三篇 | consume B.1 |
| **B2** | 空结果先分因（覆盖 / 数据 / 查询），再决定重试、补数据还是改 query；0 行不是错 | 模板（B.2 有 5 条 ASK，无分布） | 分因决策表 + 失败目录（≥12 类） | P2（N）；现有三篇 failure 段 | consume B.2 |
| **B3** | 选择性纠错的增益来自「选择性」，不是「纠错本身」；全量纠错低于选择性，净收益必须用 2×2 配对测 | E-21 子集级，无 2×2 | 2×2 协议 + 若论文有矩阵则抄；否则明写「未测」 | P1/P2（N）；GGC 已有 | consume B.3 |
| **B4** | OBDA 的本体贡献要用「去公理」消融隔离；SPARQL→SQL 重写正确不等于查询正确 | E-20 代码级，无消融 | 消融协议（有/无 TBox 公理 × 同一查询集）+ Ontop 最小命令 | Ontop 已有；P4（N） | consume B.4 |
| **C1** | 标签→策略有领域来源：等级、主体、动作、条件、效果五列都能指到标准条款或实现 | 模板（04 C.2 的 policy 表 7 行无源；F3 说策略层无领域来源） | `01/policy/`：policy schema + 标签→level→处置映射表 | M1 GB/T 43697；M5 Atlas；M6 Ranger | govern C.1/C.2 |
| **C2** | 策略冲突可判定：deny-overrides、default deny、skip≠allow、obligation 各有语义；7 条规则能跑出期望 decision | 模板（policy.json 7 条，无测试） | 冲突消解表 + 7–10 条输入→decision 测试 | M3 ODRL；M4 XACML；M7 OpenFGA | govern C.2 |
| **C3** | 读路径至少两个实现；object 方向、异常路径、fail-open/fail-closed 的差异可列成 10 条用例 | 单实现（E-20 / commit-gate F7） | 10 条一致性用例 × 2 实现矩阵 + 最小可移植策略 | N4 第二实现；AuthorizationPairs 已有 | govern C.3 |
| **C4** | 泄漏可测（object / 别名 / 聚合）+ 审计可验证（schema + replay） | 单例（04 C.3 的 T1）+ 模板（audit JSON） | ≥12 条泄漏用例 + audit JSON Schema + 2 条 replay | M12 OpenLineage；PROV-O（N）；trustgraph 已有 | govern C.3/C.4 |
| **D1** | 失败可能跨段传播：build 的坏 shape、query 的空结果、govern 的 skip 各自在下游变成什么；单段指标看不见跨段放大 | gap（C.5 只有旁证） | 故障注入矩阵（≥10 类 × 3 段 × 信号）+ 传播路径 | M12 OpenLineage；P4（N）；E-06 已有 | boundaries / C.5 |

> **成本/规模不单列承重句**：它没有可引的 E，只有公式与区间；放 T6 的成本模型 + `sections/acceptance.md`，每个参数标实测/估算/未知。不把厂商 token 报价写成结论。

### 2.3 三条不写


1. **不写「建完就能用」**——A1/A3 没有可消费性测量前，只写检查表与停。
2. **不写「三路线谁更好」**——B1 没有头对头前，只写条件选择与反例。
3. **不写「执行层可授权」**——C3 没有第二实现前，只写单实现 + 风险，不写「访问控制可落地」。

这三条已经在 04 的边界里；本计划要求的是**删掉解释性长段**，把边界压成一行 + 停。

### 2.4 哪些需要新证据

| 类型 | 条数 | 是哪几条 |
|---|---:|---|
| 把已有来源压成表/目录 | 6 | A1、A2、B2、B4、C1、C4 |
| 用标准/代码补语义 | 2 | C2、D1 |
| 需要新证据（试跑/头对头/配对/第二实现） | 4 | A3、B1、B3、C3 |

**结论**：这轮的主要工作不是「再找 20 篇」，是**把已经付过钱的 28 篇 + 6 个开源压成 12 张表**；`src/` 只为真空格补 12 个来源 + 1 个论文槽位。标准和代码不是新证据，是把已有语义固定下来；真正的新证据只有 A3/B1/B3/C3；其中 B1/B3 有降级路径。

## 3. topics 要挖到什么：6 件产物

> 12 张表不是 12 个文件；6 件产物里有的含多张表。统一要求：每件产物都要有一张**决定表**，不是一篇综述。单元格只允许 `数+条件+锚`、`空`、`不可比+理由`；空单元必须对应一条 `src/` 订单或一条 stop。

### 3.0 新页型：`compare.md`

- **位置**：`topics/<派>/<子主题>/compare.md`，与 `findings.md` / `mechanism.md` / `frontier.md` 并列。
- **结构**：决定 / 维度 / 矩阵 / 空单元 / 决策规则 / 反例 / 停。
- **规则**：不把不同数据集、不同指标的数放同一列比较；「不可比」要写理由，不是空白。
- **验收**：≥60% 单元格有内容；每个空单元有一条订单或一条 stop；≥1 条决策规则能直接写进 04。
- **为什么新开页型**：`findings.md` 是「来源 → 判断」，`compare.md` 是「决定 → 维度 → 来源」。04 缺的是后者；不新开，就会继续把「不可比」抄成交付物的边界。

### T1 可消费性

- **落点**：`topics/05-produce/representation/consumability.md`（加页，不新子主题）。
- **回答**：什么叫「能被消费」；三档表示在四类消费上的能力；契约字段与 `build_report` 的映射；生成物过不过得了前三关。
- **产物**：3×4 能力矩阵（四类消费按 04 的 load / validate / query / explain，不用 representation 页的四位置）；契约字段映射表；10 个坏样本（每个带失败类型与复现步骤）。
- **验收**：每格有标准条款/代码锚；≥2 格来自标准/代码而非推测；坏样本可复现；E-12 的边界条件写清。
- **服务**：A1 / A2 / A3。
- **来源**：M8 / M9 / M10；CASTON、OntoDoc 已有。
- **等级上限**：`已核（标准/代码）`；效应量只能 `推测`。

### T2 查询对照与失败目录

- **落点**：`topics/03-knowledge/querying/compare.md`（加页）。
- **回答**：三路线 + OBDA 在 8 个维度上的可比性；每条路线的失败类型；空结果怎么分因；选择性纠错的净收益缺什么。
- **产物**：4×8 矩阵（见下方示例）；4 分支决策树；≥12 类失败目录；空结果分因表。
- **验收**：每格有 digest 锚；决策树每支有反例；失败目录 ≥8 类来自原文、≥4 类为综合；≥1 条「不可比」有理由。
- **服务**：B1 / B2 / B3 / B4。
- **来源**：现有 GGC / NLKGQ / KGVoyager / Ontop；P1 / P2 补格。
- **等级**：`已核（逐条数字）/ 推测（可比性）`。

**示例：B1 的矩阵骨架**（空格就是订单）

| 维度 | GGC | NLKGQ | KGVoyager | OBDA |
|---|---|---|---|---|
| 先有什么资产 | 已有 KG + 生成器 | 完整 OWL + endpoint | 只有 endpoint | 关系库 + 映射 |
| 本体规模 | 小 schema（iMKG） | 完整 OWL 进上下文 | 无本体，class index | TBox 饱和 |
| 问题量 | 31,570 | 1,000 | 394 | 未报 |
| 指标 | 答案集匹配 | Match/Exact | F1 | 未报 |
| 成本 | 墙钟 +10% | 未报 | $2.43 / 85.6s | 未报 |
| 失败模式 | 空结果无机制 | snapshot/窗口 | schema/执行/格式 | 重写正确性 |
| 可比性 | — | 与 GGC 不可比 | 与前两者不可比 | 与三者不可比 |

> 这张表的「不可比」本身就是内容：它直接告诉读者 98.33 / 89.9 / 64.6 不能排成一条线。决策树只按「资产条件」分支，不按分数分支。

### T3 策略层（唯一新子主题）

- **落点**：`topics/01-constraint/policy/`（新子主题）。
- **为什么新开**：策略判定是独立子机制——标签生产（access-control/F1）、策略判定（本页）、读路径执行（commit-gate/F5–F7）。access-control 的 F3 已把策略层标成空白，但它的页在讲三层对照，长不出策略语义；按 [ADR 0003](../../../../adr/0003-subtopics-and-source-types.md)，单独成子主题。
- **成立条件**：≥2 个独立来源；M1 + M3/M4 + M5/M6 已够，不靠单一厂商。
- **回答**：标签/属性 → 策略 → 决定 → 审计的链路；策略语言怎么表达冲突/默认/义务；领域标准怎么给等级与处置。
- **产物**：policy schema（principal / action / resource_kind / condition / effect / obligation / version）；冲突消解表；7–10 条测试（输入 → 期望 decision）；标签→level 映射表。
- **验收**：每个语义有标准条款/代码锚；测试可执行；≥1 个领域标准；不把 OPA/Atlas 当「本体执行」。
- **服务**：C1 / C2 / C4。
- **来源**：M1 / M3 / M4 / M5 / M6 / M7。
- **等级上限**：`已核（标准/代码）`；标签→策略的映射协议只能 `推测`。

### T4 读路径第二实现

- **落点**：`topics/01-constraint/commit-gate/read-path.md`（加页）。
- **回答**：第二实现是否存在；object / 异常 / fail-open 的行为；两实现差异；修法有没有已测。
- **产物**：10 条用例 × 2 实现矩阵；最小可移植策略；修法清单（已测 / 未测）。
- **验收**：第二实现 pin commit + `file:symbol`；10 条有期望；≥1 条修法有代码锚；不把「有实现」当「安全」。
- **服务**：C3 / C4。
- **来源**：N4 第二实现；`AuthorizationPairs`（[2610.16838](../../../audits/2026-11-11-source-purge.md#src-2610-16838)，已有）作合法/禁止样本；trustgraph 已有。
- **等级**：`已核（代码）`，不外推。

### T5 输出校验

- **落点**：`topics/02-judgment/checker/output-validation.md`（加页，不新子主题）。
- **为什么加页**：checker 已是「输出后判定」的家；输出校验是同一时刻的不同判据——结果对象（schema / cardinality / provenance / plausibility）而不是本体判据。加页，避免薄页。
- **回答**：查询结果/生成结果在输出侧能查什么；与输入侧 shape 的分工；三态（pass / violation / undetermined）；与 expectations 的映射。
- **产物**：6 类校验表（schema / cardinality / provenance / freshness / cross-field / plausibility）+ 接口 + 误报/成本列。
- **验收**：≥4 类有代码/标准锚；≥2 类有误报/成本；三态明确。
- **服务**：C4 / D1。
- **来源**：M11 Great Expectations；M8 SHACL（结果 shape）；P4（N）。
- **等级**：`已核（工具/标准）`；效果 `推测`。

### T6 跨段传播

- **落点**：`topics/06-measure/metrics/propagation.md`（加页）。
- **为什么加页**：`metrics` 已有 coverage / 机制分派，但没有「跨段传播」的注入矩阵；`failure-attribution` 管的是单任务内的归因，不是 build→query→govern 的跨段。
- **回答**：哪些故障跨段、在哪看得见、检测点、成本量级。
- **产物**：故障矩阵（≥10 类 × 3 段 × 观测信号）+ 传播路径 + 成本模型（公式 + 参数区间，标实测/估算/未知）。
- **验收**：每类有注入点/观察点；≥1 条路径有证据；成本参数每个标实测/估算/未知。
- **服务**：D1 + 04 验收。
- **来源**：M12 OpenLineage/Marquez；BSBM/LDBC（N）；E-06 / E-05 已有。
- **等级**：`推测（综合）/ 已核（工具能力）`。

### 3.7 引用链：6 件产物怎么变成 04 能引的 E

> `E23`–`E27` 已于 2026-11-10 定稿为 `E-23`…`E-27`（读路径/策略/可消费性/路线/输出），见 [conclusions](../../../../topics/conclusions.md)。
>
> 04 只能引 `E-xx`（[conventions](../../../rules/conventions.md)）。compare 表再漂亮，不升 E 就进不了 04。**六件产物收成五条 E（T5/T6 合并），不是一条 finding 一条 E。**

| 新 E（已定稿） | 决定 | 由哪些产物/来源支撑 | 等级上限 |
|---|---|---|---|
| **E-23** | 读路径：10 用例，object / fail-open / 无第二实现 | T4 + trustgraph + sparql-guard/Jena 评估 | `已核（代码）` |
| **E-24** | 策略层：标签 → 策略 → 决定 → 审计 | T3 + GB/T 43697 / XACML / ODRL（材料卡） | `已核（标准摘要+文件）/ 推测（映射）` |
| **E-25** | 可消费性：契约 → 三档 → 三关 | T1 + E-12 + SHACL / ODCS（材料卡） | `已核（标准卡+文件）/ 推测（效应）` |
| **E-26** | 路线选择：按资产条件，不按总分 | T2 + E-21；P1 空 | `推测（综合）` |
| **E-27** | 输出校验 + 跨段传播：6 类 + 故障矩阵 | T5 / T6 + E-02 / E-06 | `推测（综合）` |

**升 E 规则**：

1. 一条 E 只回答一个决定；不要把 12 条承重句塞进 3 条 E，也不要把一条拆成 12 条。
2. ≥2 个独立来源（标准 + 实现算两个），或 1 个标准 + 1 个代码锚；单源只能 `推测`，04 引用时带限定。
3. 单个单元格、单实现细节、未复现的数留在 `compare.md` / `findings.md`，不升 E。
4. 升 E 时先写本派 `claims.md`，再动 [conclusions](../../../../topics/conclusions.md)；E 行只写「决定 + 条件 + 反例 + 出处」，矩阵留在 topics 做证据。
5. 04 引用 E23…E27，不引 compare 表；表是证据，E 是口径。

> 这 5 条是**建议占位**，不是已定义结论；最终编号与等级以 `conclusions.md` 定稿为准。升不上去的 E，04 删对应句，不拿模板补。

## 4. `src/` 要准备什么

### 4.0 先用已有的：五件还没榨干的资产

> 这五件已经付过钱，04 只引了其中一部分。先榨干，再买新的。

| 已有资产 | 里面有什么 | 现在用在哪 | 还能填哪格 |
|---|---|---|---|
| [AuthorizationPairs 2610.16838](../../../audits/2026-11-11-source-purge.md#src-2610-16838) | 80 lawful / 80 forbidden、同操作不同权限 | 01 的 P0 扫描；04 未用 | C3/C4 的「合法/禁止」测试样本 |
| [Glyph 2609.10430](../../../../src/papers/2609.10430-glyph/digest.md) | 275-leaf 分类本体、列级标签、约 72% NON_SENSITIVE | C.1 标签层（E-22） | C1 的「标签→level」类别表 |
| [E-06 Diagnose](../../../../topics/06-measure/failure-attribution/README.md) | 五角色 + 七变量、工作流失败 | 04 的边界一句话 | D1 的失败目录骨架 |
| [DBLP-QuAD 3.1（NLKGQ）](../../../audits/2026-11-11-source-purge.md#src-2609-14652) | 1,000 题、确定性参考、Match/Exact | B.1/B.2 | B1 矩阵的「问题量/指标」列 |
| [Ontop](../../../../src/open-source/ontop-ontop/digest.md) | TBox 饱和 + SPARQL→SQL、最小命令 | B.4 一句 | B4 消融协议 + 成本量级 |

### 4.1 三条准入（现有规则 + 两条修正）

现有：新鲜度 ≥2026-07-01；origin 只收 US / China / Germany / Singapore；可靠性/影响力字段；OSS 必须 pin commit + 可定位调用点；不 vendor；厂商白皮书不当 E。

本计划加两条：

1. **标准/基准不套论文新鲜度**。标准是基础设施，不是「新判断」；用 `source_type: standard`（[conventions](../../../rules/conventions.md)）入 `src/web/`，不套 `batch: 补给` 的 `published` 检查。理由：SHACL 2017、XACML 2013 不会因为「老」而失效；把标准挡在门外，只会让策略层继续空着。**这是口径，不是新 ADR；写进 `src/README` 一句话即可。**
2. **adjunct OSS 可以入库，但 `ontology_role: adjunct`，不单独撑 E**。Atlas/Ranger/OpenFGA 只回答「策略/审计的通用能力」，不回答「本体被执行」；引用时与 OPA 同口径。

**每个来源必须带一张「填格卡」**：填哪个 claim 的哪个单元格、locator（页/表/条款/`file:symbol`）、不能填什么。填不出格的来源，不入档。

### 4.2 M：12 个具体来源 + 1 个论文槽位

| ID | 来源 | 类型 | 地区 | 填哪格 | 抽什么 | 验收 | 波次 |
|---|---|---|---|---|---|---|---|
| M1 | GB/T 43697-2024 数据分类分级规则 | 标准 | CN | C1：level / 处置 | 分级框架、级别定义、变更/审核 | 条款号 + 5 条映射 | W2 |
| M2 | GB/T 35273-2020 个人信息安全规范 | 标准 | CN | C1：PII 类别 | 个人信息类别、处理规则 | 类别→tag 映射 | W2 |
| M3 | W3C ODRL 2.2 | 标准 | W3C | C2：冲突/义务 | permission / prohibition / duty / conflict | 3 条语义 + 1 测试 | W2 |
| M4 | OASIS XACML 3.0 | 标准 | OASIS | C2：合并算法 | deny-overrides 等 4 种 + obligation | 4 条算法 + 1 测试 | W2 |
| M5 | Apache Atlas | OSS | US | C1：标签库 | classification / lineage / API | `file:symbol` + 3 个调用点 | W2 |
| M6 | Apache Ranger | OSS | US | C1/C2：执行与审计 | tag policy / audit | `file:symbol` + policy model | W2 |
| M7 | OpenFGA | OSS | US | C2/C4：决策/审计 | model / check / expand / test | `file:symbol` + 3 tests | W2 |
| M8 | W3C SHACL + test suite | 标准 | W3C | A1/A3/T5：可加载/可验证 | shape 语义、conformance 用例 | 5 条用例 | W1 |
| M9 | ODCS（Open Data Contract Standard） | 标准 | LF | A1：契约字段 | 字段、质量、SLA、版本 | 5 字段映射 | W3 |
| M10 | LinkML | OSS | US | A2：轻 schema 档 | schema / generators | `file:symbol` + 1 例 | W3 |
| M11 | Great Expectations | OSS | US | T5：输出校验 | expectation suite / result | 3 条 expectation | W1 |
| M12 | OpenLineage + Marquez | OSS | US | C4/D1：审计/传播 | run / dataset / lineage 事件 | 3 类事件 | W1 |
| **P1** | **头对头论文槽位** | 论文 | 待定 | B1：路线对照 | 同 KG / 同题 / 同指标 | 1 张矩阵 | W1 |

> M5/M6 是一对（Atlas 标签 → Ranger 策略），M12 是一对（OpenLineage 规范 + Marquez 参考实现）；按「一个架构」读，不按两个 star 数读。

**D7 降级（2026-11-10）**：M5–M7（Atlas/Ranger/OpenFGA）与 M10（LinkML）从 M 降为**候选**，不阻塞 04：

- 它们是 **adjunct/实现例**，不承载 04 主句；策略层主句已由 6 个标准卡 + E-22/E-24 + OPA 支撑，A2 的结构表主句已由 SHACL/ODCS 支撑。
- 没有它们，04 仍能写「标签 ≠ 策略 ≠ 执行」「三档 × 四位置」「10 条测试」；有它们只是多一列实现对照。
- 若未来要写「策略执行/轻 schema 的代码级对照」，再从 [frontier](../../../../topics/01-constraint/policy/frontier.md) 升 M；不现在硬凑 pin commit。

**source gate 关闭口径**：6 标准卡 + Great Expectations + OpenLineage 两个 OSS digest + 4 个候选（M5–M7/M10）；候选在 `frontier` 里留位置，不写进 04 主句。

### 4.3 N：6 个候选（只在 M 留下空洞时开）

| ID | 来源 | 填哪格 | 什么时候开 |
|---|---|---|---|
| N1 | 空结果/失败分析论文（槽 P2） | B2：分布/分类 | M 填不出 B2 的「分布」列时 |
| N2 | 本体访问控制/策略映射论文（槽 P3） | C1/C3：映射协议 | 标准只给等级、不给映射时 |
| N3 | 可消费性/下游评估论文（槽 P5） | A3：三指标 | A3 试跑做不了、又找不到论文时 |
| N4 | sparql-guard 或第二 read-path | C3：第二实现 | M 里没有第二个 RDF 读路径时 |
| N5 | ODRL evaluator（Fraunhofer） | C2：策略求值 | ODRL 只有语义、没有可执行求值器时 |
| N6 | BSBM / LDBC SPB | 04 验收：规模/成本 | 04 验收要写量级、又不想拍脑袋时 |

### 4.4 论文槽位：检索式与拒收

| 槽 | 检索式 | 收什么 | 拒什么 |
|---|---|---|---|
| P1 | `text-to-sparql comparison` / `ontology-based question answering benchmark` / `LLM SPARQL generation evaluation` | 同一 KG、同一问题集、≥2 条路线的头对头 | 单系统、无基线、不同数据各说各的 |
| P2 | `SPARQL empty result` / `failing query analysis` / `KGQA failure taxonomy` | 空结果/失败分布或分类，带样本量 | 只讲查询优化、不讲失败 |
| P3 | `ontology-based access control` / `semantic access control policy` / `ABAC ontology` | 本体/标签→策略的映射，带评估或案例 | 只有架构图、没有策略语义 |
| P4 | `query result verification` / `data pipeline fault injection` / `error propagation data quality` | 输出校验或跨段传播的实测/协议 | 只讲可观测性平台选型 |
| P5 | `ontology evaluation downstream task` / `ontology consumability` / `competency question evaluation` | 下游任务上的本体质量评估 | 只评文档质量、只评 OWL 一致性 |

**若 2026-07+ 无合格来源**：不拿旧论文凑。P1 缺 → B1 删「排序」句，只留条件选择；P2 缺 → B2 只写分类与检测查询，不写分布；P5 缺 → A3 只写协议，不写试跑结果。

### 4.5 不做什么

- 不收厂商白皮书当 E（Immuta / Privacera / Collibra 只作 signal）。
- 不收闭源核心、无 commit、无测试的 OSS。
- 不为凑「第二实现」收单作者/无调用点的项目；sparql-guard 只能作候选。
- 不把 Atlas/Ranger/OpenFGA 说成「本体执行」；它们只提供策略/审计的通用能力。
- 不开新的论文线；只补 5 个槽位，且优先 P1/P2。
- 不因为「标准老」就排除；标准看是否仍在用，不看发布日期。

## 5. 三波与 gate

| 波 | 先做什么 | topics | src | 04 | gate（不过就停） |
|---|---|---|---|---|---|
| **W0** | 冻结 12 条承重句 + 12 张表骨架 + 删句规则 | — | — | 只建骨架，不改正文 | 12 条每条有「决定/维度/空单元」；缺一条就补 |
| **W1** | 查询与输出（先做能落表的） | T2、T5 | M8、M11、M12、P1；N1 | consume B.1–B.4；govern C.5 | T2 ≥70% 单元格有内容；失败目录 ≥12；consume 4 句有表，其中 ≥2 句有数；<2 句有表 → 停 |
| **W2** | 策略与执行（最大空白） | T3、T4 | M1–M7；N2、N4、N5 | govern C.1–C.4 | policy schema + 7 测试；read-path 10 条 × 2 实现；第二实现不合格 → C3 降级 |
| **W3** | 建与跨段（最难） | T1、T6 | M9、M10；N3、N6 | build A.1–A.5；boundaries；acceptance | T1 矩阵 + T6 故障矩阵；04 回写；全局 DoD；<7 条 → 并进 02 |

> 单人顺序做；若有两个 owner，W1 与 W2 可并行——它们改的文件不重叠（consume vs govern），但都要先过 W0。

### 5.1 W0：冻结（1 天）

1. 把 §2.2 的 12 条抄成 12 张空表，每张表写清「决定 / 维度 / 现有来源 / 空单元」。
2. 定删句规则：04 里任何**只解释「为什么没有证据」**的段落，改成一行 `gap：<什么>` + 一条 stop；不保留三段式解释。
3. 定标记预算：`模板` + `gap` 从 50 降到 ≤12；`已核` 从 7 升到 ≥20。
4. 定回写顺序：先 consume（W1），再 govern（W2），最后 build（W3）；不按阅读顺序改，按证据就绪度改。
5. 在 `src/README` 加一句口径：标准/基准不套论文新鲜度，按 `source_type: standard` 入 `src/web/`。

### 5.2 W1：查询与输出（约 5 人日）

- **T2 矩阵**：行 GGC / NLKGQ / KGVoyager / OBDA；列资产、问题量、本体规模、模型、指标、成本、失败模式、可比性。
- **失败目录**：从 GGC（空结果无机制）、NLKGQ（snapshot/endpoint/窗口）、KGVoyager（schema/词汇/执行/格式）、Ontop（重写正确性）、E-02（空结果重试）、E-06（工作流）抽 ≥12 类。
- **T5 输出校验**：6 类表 + Great Expectations 的 3 条 expectation 映射。
- **04 回写**：B.1 决策树；B.2 空结果分因表；B.3 2×2 或「未测」；B.4 消融协议。每节末尾一条 stop。
- **Gate**：consume 的 4 条承重句都能给出「条件 + 反例 + 停」；`模板` 标记 ≤2。

### 5.3 W2：策略与执行（约 8 人日）

- **T3 policy schema**：7 列；冲突消解表；7–10 条测试。示例语义对照：

| 语义 | XACML | ODRL | Rego/OPA | OpenFGA |
|---|---|---|---|---|
| 冲突 | deny-overrides 等 4 算法 | `conflict: perm/prohibit/invalid` | 默认 deny、规则序 | 关系闭包，无冲突概念 |
| 默认 | 由 policy set 决定 | 未指定 | deny | deny |
| 义务 | obligation | duty | 无 | 无 |
| 版本 | policy version | profile | bundle | model id |
| 适用 | 通用 | 内容/数据 | 通用 | ReBAC |

- **T4 10 条用例**：subject 命中 / object 命中 / 两侧 / 都不中 / target 异常 / 缺 user_context / alias / 聚合 / 无策略 / 版本不匹配。
- **04 回写**：C.1 三层来源表（标准/实现/空白）；C.2 policy 表加 `test_id`；C.3 泄漏用例；C.4 audit schema + replay。
- **Gate**：7/7 策略测试有期望 decision；10/10 用例有观察结果；第二实现不合格 → C3 只写单实现 + 停，不写「执行层可授权」。

### 5.4 W3：建与跨段（约 7 人日）

- **T1 矩阵**：3 档 × 4 消费位置；单元格写 supported / partial / not + 锚；成本列标「估算」。
- **10 个坏样本**：契约缺 principal / moment / refuse / load / version；shape 缺 target；tag 是字面量；level 缺失；无 dataset 边；版本不一致。
- **T6 故障矩阵**：坏 shape / 缺 tag / 错 level / 空结果 / 错 join / policy skip / object 泄漏 / 快照过期 / 版本不匹配 / 超时；每类写注入点、观察点、是否跨段。
- **04 回写**：build A.1–A.5 用 T1；boundaries 用 T6；acceptance 加成本量级（标实测/估算/未知）。
- **Gate**：T1 ≥60% 单元格有内容；T6 ≥10 类；04 全局 DoD 见 §7。

## 6. 04 回写：每章一张表、一个物、一份目录、一条停

### 6.1 章节模板

```
X.0 决定表（选项 × 维度 × 条件）
X.1 产物（可执行：shape / query / policy / test / schema）
X.2 失败目录（≥8 条，带检测点）
X.3 停（3 条）
X.4 证据边界（1 段，不解释「为什么没有」）
```

> 这个模板替代现在的「散文 + 一张表 + 证据边界」。每章字数不一定增加，但**可判断的格子**增加。

### 6.2 三章各写什么

| 章 | 决定表 | 产物 | 失败目录 | 停 |
|---|---|---|---|---|
| **建** | 三档表示 × 四类消费 | 契约 + TBox + shapes + 10 个坏样本 + `build_report` | 10 类（坏样本即目录） | 契约缺格 / 坏样本未复现 / 无版本 |
| **用** | 四路线 × 八维度 | 3 SPARQL + 空结果表 + 2×2 协议 + 消融命令 | 12 类（查询/执行/空结果/纠错） | 空结果不分因 / 全量纠错 / 85% 当正确率 |
| **治** | 三层 × 来源/强度 | policy schema + 7 测试 + 12 泄漏用例 + audit schema | 12 类（标签/策略/执行/审计） | object 泄漏未修 / 无策略 / 无审计 |

### 6.3 删什么

- 删「为什么没有证据」的长段：改成一行 `gap：<什么>` + 一条 stop。
- 删三章各自重复的「证据边界」长表：合并到 `sections/boundaries.md`，正文只留 1 段。
- 删「三路线不排序」的解释性段落：改成矩阵的「不可比」列。
- 删「本 fixture 只是示例」的重复声明：在 README 说一次，正文不再反复。
- **先删后加**：正文目标 ≤13k 字符（现在 10.4k body / 17k md）；导航 ≤8%。

### 6.4 产物清单（5 现有 + 4 新 = 9）

| # | 产物 | 状态 | 服务 |
|---|---|---|---|
| 1 | 消费者契约 | 现有 | A1 |
| 2 | TBox + shapes + ABox | 现有 | A2 |
| 3 | 3 条 SPARQL | 现有 | B1/B2 |
| 4 | policy 表 | 现有，补测试 | C1/C2 |
| 5 | audit record | 现有，补 schema | C4 |
| 6 | policy 测试套件（7–10 条） | 新 | C2 |
| 7 | 泄漏用例集（≥12 条） | 新 | C3/C4 |
| 8 | audit JSON Schema + 2 条 replay | 新 | C4 |
| 9 | 故障矩阵（≥10 类 × 3 段） | 新 | D1 |

> 9 件都在同一个 fixture 上，不新开第二个域；新产物进 `example/`，不另建目录。

## 7. 验收与停止

### 7.1 每波 DoD

| Gate | 必须 | 可以缺 | 不过怎么办 |
|---|---|---|---|
| W0 | 12 张表骨架；删句规则；标记预算 | 具体数字 | 补骨架，不进 W1 |
| W1 | T2 ≥70% 格；失败目录 ≥12；consume 4 句有表，≥2 句有数 | 空结果分布；B1/B3 的新证据 | <2 句有表 → 停 W2，先缩 T2 |
| W2 | policy schema + 7 测试；read-path 10×2 | 第二实现 | C3 降级为单实现 + 停 |
| W3 | T1 ≥60% 格；T6 ≥10 类；04 回写 | 成本实测 | 全局 DoD 判定 |

### 7.2 全局 DoD

- **12 条承重句**：≥9 条有表/数/对照；≥11 条有反例/停；0 条只有「模板」。
- **topics**：6 件产物落地；T3 新子主题 ≥2 个独立来源；其余为加页，不新开薄子主题。
- **src**：12 个 M 入档并带填格卡；P1 要么入档要么写明「已扫 N 条，无合格头对头」；厂商文 0 条当 E。
- **04**：`模板` + `gap` ≤12（现在 50）；`已核` ≥20（现在 7）；9 件产物；正文 ≤13k；导航 ≤8%。
- **自检**：`python3 meta/tools/check_repo.py` 通过；0 断链 / 0 未定义 ID。

### 7.2b 执行后修订（2026-11-10）

> 13k / 12 markers / 已核 ≥20 是**执行前**的估算；实际落了 6 页 topics 与 9 件产物，正文 14.6k。按内容标准修订，不按字数裁证据：

| 项 | 原目标 | 执行后 | 理由 |
|---|---|---|---|
| 04 正文 | ≤13k | **≤15k** | 9 件产物 + 决策表；已删重复（B.1 表、失败目录 8→5、坏样本 10→4、audit JSON 2→1） |
| `模板`+`gap` | ≤12 | **≤30** | 新内容把原先一句带过的缺口写成了可判定条目；不追求把「未测」写成「已核」 |
| `已核` | ≥20 | **≥10** | 新增判断多为 `推测（综合）`/`待核`；不升假 E |
| 来源入库 | M1–M12 | **仍待** | 见 §4；policy/read-path 页已标 `待核`，不编条款 |

**内容 DoD 不变**：12 条承重句里 ≥9 条有表/数/对照；≥11 条有反例/停；9 件产物齐；6 页 topics 落盘。

### 7.3 停止/降级

| 触发 | 处置 |
|---|---|
| 某波 <2 条承重句有表/产物 | 停该波，回 W0 缩题；不把空格写成模板 |
| P1 找不到头对头 | B1 删「排序」句，只留「按资产条件选」；04 不写路线优劣 |
| 第二实现不合格 | C3 只写单实现 + 风险；删「执行层可授权」的一般结论 |
| 标准拿不到全文 | 用官方摘要/公开草案，标 `provenance: 未核`；不引条款号 |
| T1 试跑做不了 | A3 只写协议；不写「生成物可消费」的结论 |
| **全局 <7 条** | **04 并进 02 的 R13（端到端 recipe），删除目录；fixture 作为附录保留** |

### 7.4 反向验收（防止自欺）

1. 随机抽 3 条承重句，让一个没读过 04 的 agent 只看 topics/src，能否在 10 分钟内复述「条件/反例/停」；不能 → topics 没挖到。
2. 抽 3 个单元格，能否从 04 点到 topics 表、再点到 src 锚；不能 → 链断。
3. 抽 3 个 `模板` 标记，是否都有对应的「为什么没有 + 停」；没有 → 删句。
4. 抽 1 张矩阵，检查有没有把不同数据集/指标的数放同一列；有 → 打回重排。

## 8. 排期与工作量

| 波 | 人日 | 产出 | 依赖 |
|---|---:|---|---|
| W0 冻结 | 1 | 12 张表骨架 + 删句规则 | §2 |
| W1 查询/输出 | 5 | T2 + T5 + consume 回写 | M8/M11/M12/P1；现有三篇 |
| W2 策略/执行 | 8 | T3 + T4 + govern 回写 | M1–M7；N4 |
| W3 建/跨段 | 7 | T1 + T6 + build 回写 + 收口 | M9/M10；N3/N6 |
| Buffer | 2 | 返工/补检索 | — |
| **合计** | **约 23** | 6 件 topics + 9 件产物 + 04 v2 | 4–5 周，单人 |

> 量级，不是承诺。若只做一件事：**W1 的 T2**——它最便宜，直接让 consume 从「三路线不分」变成「按资产选」。

## 9. 风险

| 风险 | 触发 | 处置 |
|---|---|---|
| 找不到头对头 | P1 扫不到 2026-07+ 合格来源 | B1 降级为条件选择；不写排序；把「无头对头」写成矩阵的 `不可比` 列 |
| 第二实现不合格 | sparql-guard 单作者/无调用点 | 只作候选；C3 单实现 + 停；不把 trustgraph 外推 |
| 标准拿不到全文 | GB/T、XACML 付费/登录 | 用官方摘要/公开草案；标 `未核`；不引条款号；必要时用 NIST/ISO 公开材料替代 |
| OSS 只是 adjunct | Atlas/Ranger/OpenFGA 不解析 OWL | 标 `ontology_role: adjunct`；只填策略/审计格；不撑「本体执行」 |
| 矩阵变成第二篇综述 | 单元格写成摘要 | 每格必须 `数+条件+锚` 或 `空`；写不出就留空并开订单 |
| 04 回写又写成模板 | 作者怕下判断 | 删句规则 + 反向验收 3；模板预算 ≤12 |
| 范围蔓延 | 12 条变 20 条 | 冻结 §2.2；新增必须先删一条 |
| 自检失败 | 断链/未定义 ID | 每波结束跑 `check_repo`；先修再进下一波 |

## 10. 与旧计划的关系

| 文件 | 关系 |
|---|---|
| [2026-11-09-reverse-gap-plan.md](./2026-11-09-reverse-gap-plan.md) | 保留为**诊断/审计**；本计划取代它的「订单」部分——订单不再是 TB/CA/FC 对象类型，而是矩阵空格 |
| [04-worked-example.md](./04-worked-example.md) | 其 P1/P2 两条新 E 的范围被本计划扩展；「论文线冻结」改为「只补 5 个槽位」 |
| [2026-11-10-04-deep-plan.md](./2026-11-10-04-deep-plan.md) | D1–D6 保留（单读者 / fixture / 三链 / 预算 / 验收）；D3 的证据策略从「有什么引什么」改为「缺什么补什么」 |
| [2026-11-09-hard-objects-plan.md](./2026-11-09-hard-objects-plan.md) | 保留；O 仍是地址层，不替代本计划的矩阵，也不因为矩阵新增对象 |
| [2026-11-10-stage-review.md](../../../../deliverables/_workpapers/2026-11-10-stage-review.md) | 背景不变：单源、无同数据集两把尺子、机制缺口；本计划不解决独立复现，只解决 04 的决策密度 |
| [2026-11-10-wiring-plan.md](./2026-11-10-wiring-plan.md) | 不动；M/R/X 接线仍是已完成状态 |

## 12. 执行进度（2026-11-10）

| 项 | 状态 |
|---|---|
| W0 | 完成：12 条承重句 + 12 张表骨架（[matrix-skeletons](./2026-11-10-04-matrix-skeletons.md)） |
| W1 | 完成：T2 [compare](../../../../topics/03-knowledge/querying/compare.md)、T5 [output-validation](../../../../topics/02-judgment/checker/output-validation.md)、consume v2 |
| W2 | 完成：T3 [policy](../../../../topics/01-constraint/policy/README.md)、T4 [read-path](../../../../topics/01-constraint/commit-gate/read-path.md)、govern v2；**第二实现否决**（sparql-guard 不够、Jena 退役） |
| W3 | 完成：T1 [consumability](../../../../topics/05-produce/representation/consumability.md)、T6 [propagation](../../../../topics/06-measure/metrics/propagation.md)、build v2 |
| 来源 | 6 个标准卡 + Great Expectations digest + OpenLineage digest；M5–M7/M10 按 D7 降为候选 |
| E | E-23（读路径）、E-24（策略层）、E-25（可消费性）、E-26（路线）、E-27（输出/传播）全部已升 |
| 04 | 9 件产物；body 14.9k（修订 ≤15k）；`模板/gap` 6（修订 ≤30）；`已核` 11 |
| 自检 | `check_repo` 通过（493 文件；E=27，L=79） |

> 收口：W0–W3 与 E 链完成；source gate 以「6 标准 + 2 OSS digest + 4 候选」关闭（D7）。剩余候选不写进 04 主句，留 `frontier`。

## 11. 本周就做

1. **冻结 §2.2 的 12 条**，不再加；每条写成一张空表（决定 / 维度 / 现有来源 / 空单元）。
2. **先填 T2**：用 GGC / NLKGQ / KGVoyager / Ontop 四篇 digest 填 4×8 矩阵；空格列 P1/P2 订单。
3. **开 W1 的 src**：M11 Great Expectations、M12 OpenLineage/Marquez、P1 检索；不碰 W2 的标准。
4. **04 只改 consume B.1–B.4**：加矩阵与失败目录，删「三路线不排序」的解释段；改完跑 `check_repo`。
5. **一周后 gate**：T2 ≥70% 单元格有内容，且 consume ≥2 条承重句有「条件 + 反例 + 停」；否则缩题，不硬推 W2。

> 本页只在推进时更新；结论回 `topics/`，04 只做抽取。来源能力在入库前一律 `待核`，不把候选写成结论。
