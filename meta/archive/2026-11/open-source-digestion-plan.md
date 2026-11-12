---
status: superseded
updated: 2026-11-09
---

# 开源项目消化计划：从代码证据到 topics 判断

> 本计划只管一件事：把 `src/open-source/` 里**已建卡的项目**推进到「可被 topics 引用」，并把信息按现有 promote 路径送进 `topics/`。
> 它不改变 [AGENTS](../../../AGENTS.md) 的落点规则；与 AGENTS 冲突时，以 AGENTS 为准。

## 0. 一句话

**不平均用力，一个子领域一个子领域收。** 每个项目过五道 C 闸（定位 → 调用链 → 最小运行 → 自包含 digest → 与论文对照），再过四道 A 闸（sources → findings → claims → frontier/conclusions），最后用一张吸收矩阵查「代码发现有没有真的进判断」。

## 1. 门槛：先筛，再消化

### 1.1 本轮临时门槛（2026-11-09 起）

1. **stars ≥ 1,000**（临时规则，可随时撤销；star 是注意力，不是证据）。
2. **本体是代码里的对象**：能指到 `文件:符号`；纯图检索、纯 prompt、闭源 core 不进。
3. **能 pin commit**，且能写出至少一条候选调用链。

### 1.2 按门槛重排

| 项目 | stars | 本轮状态 | 理由 |
|---|---:|---|---|
| semantica-agi/semantica | 14,475 | **消化** | OWL 生成 + pyshacl；影响最大 |
| trustgraph-ai/trustgraph | 2,902 | **消化** | SHACL-AF 策略过滤 + 抽取 schema |
| fabio-rovai/open-ontologies | 2,848 | **消化** | 真 SHACL 引擎 + 变更/影响面 |
| ontop/ontop | 1,016 | **消化** | OBDA 查询重写，供给侧极端形态 |
| apache/jena | 1,501 | 对照（不写完整 digest） | 标准栈控制组；在 digest 里引用 |
| monarch-initiative/ontogpt | 1,089 | 对照（可选） | 生成侧接地；LinkML 不是执行判据 |
| deeplethe/utopia | 8,692 | 候选，不进 | 过星门槛，但 3 个月、AI 提交占 58%，本体形态待核 |
| HelixDB/helix-foundry | 2,082 | 候选，不进 | 过星门槛，但自建 Go schema、1 个月 |
| RDFLib/pySHACL | 371 | **已删除**（<1,000★） | 最便宜的运行基线；撤销门槛时重新建卡 |
| ontodev/robot | 329 | **已删除**（<1,000★） | OBO 生命周期对照 |
| sib-swiss/sparql-llm | 130† | **已删除**（<1,000★） | 最贴回路内，但样本太小 |

> 低于门槛的项目**已从磁盘删除**；只在 [`_scan-2026-11-09.md`](../../../src/open-source/_scan-2026-11-09.md) 保留元数据。撤销门槛时重新建卡，不默认恢复。

**代价要说清**：把 pyshacl / ROBOT / sparql-llm 拿掉后，本轮没有「十分钟能跑通」的基线；剩下四个的运行成本分别是 Rust（392MB）、Python 微服务、Java（Ontop）、Python（Semantica），**Wave 1 要先算环境预算**，不要默认都能当天跑。

## 2. 第一道漏斗：code → digest（C 闸）

每道闸有明确的「过了没」判据；不过就不进下一道。

| 闸 | 要产出 | 通过判据 | 不过怎么办 |
|---|---|---|---|
| **C0 卡** | `card.md` | commit 已 pin；本体位置、调用点、证据入口齐；待核项列清 | 补卡，不写 digest |
| **C1 调用链** | digest §3 | 一条端到端：输入 → 本体加载/编译 → 校验/推理/查询 → 输出/动作 → 失败处理；每步 `文件:符号` | 标「未定位」，降为 `推测`，不写「执行」结论 |
| **C2 最小运行** | digest §5 | 官方示例/测试跑过，命令、环境、结果、报错原文都留；失败也算过闸 | 环境跑不起来 → 写清阻塞点，digest 标「未跑」；**不许用 README 替运行** |
| **C3 自包含 digest** | `digest.md` | 10 段齐；每个判断带四档等级；「不能证明什么」至少 4 条；`quality` 有理由 | 退回 C1/C2 |
| **C4 论文对照** | digest §7 | 至少一篇论文 digest 的机制逐条对：对应 / 形态不同 / 没实现 / 没找到 | 只写「没找到」，不写「不存在」 |

**C 闸的硬规则**：

- 「跑通官方示例」只证明代码能执行，**不证明机制有效**；证据等级仍是 `已核`，不是 `已证`。
- `executed / context / mixed / none` 四选一，必须附调用点；选 `executed` 还须回答「违反时改变什么走向」。
- 自研实现也算执行：trustgraph 的 SHACL-AF 不在 pyshacl 里，别用依赖清单判死刑。

## 3. 第二道漏斗：digest → topics（A 闸）

### 3.1 信息落点（一张表说完）

| 代码发现的性质 | 落到哪 | 格式 | 不许做什么 |
|---|---|---|---|
| 项目事实、调用链、证据入口 | 项目 `digest.md` | 10 段 + `文件:符号` | 不写成第二篇 README |
| 「这个项目支撑/削弱哪条判断」 | `topics/<派>/sources.md` | 一行：项目 → `reading` → 支撑的 `L/F` → digest 链接 | 不把 card 当内容 |
| 代码级新事实（接口、降级、失败模式） | `topics/<派>/<子主题>/findings.md` | `F-xx` + 证据 + 等级 | 不写「下一步计划」 |
| 某条 `L-xx` 要改 | `topics/<派>/claims.md` | 新号或改旧号 + 证据 + 原判断哪条作废 | 不直接写进 `conclusions` |
| 论文机制在代码里**没实现/形态不同** | `topics/<派>/frontier.md` | `G/N`：可验证的问题 | 不硬升成 claim |
| 跨派、且改变了对外结论 | `topics/conclusions.md` | `E-xx` / `C-xx` / `Q-xx` | 不跳过 `claims` |
| 子主题 dashboard 摘要 | `topics/<派>/<子主题>/README.md` | 只改被 claims/findings 改动的段 | 不复制 digest 全文 |

### 3.2 A 闸（每进一层都要过）

- **A1 sources**：每个消化过的项目在**至多两个** `sources.md` 出现（主效应归派）；写 `open-source` 类型与 `reading`。
- **A2 findings**：只写「代码里能指到」的事实；与论文数字并列时，标清哪边是代码、哪边是论文。
- **A3 claims**：只在**改变判断**时动；改动必须写「旧判断作废/收窄/加强」；没有改变的，不新增 L。
- **A4 frontier/conclusions**：`frontier` 放缺口；`conclusions` 只在跨派或对外时动，且至少两个来源（代码 + 论文）支撑。

### 3.3 融合契约：让代码证据「长进」旧句子

吸收不是加一节「开源证据」，而是决定旧判断**要不要改写、怎么改写**。动笔前先选模式：

| 模式 | 触发条件 | 写法 | 落点 |
|---|---|---|---|
| **补边界** | 代码证明机制只在某条件下成立 | 旧句 + 条件从句（`仅在…时；代码侧…`） | `claims.md` 改旧行 |
| **换形态** | 代码里机制存在，但不是论文描述的位置/形式 | 改机制标签（如 pre-action gate → 读路径策略过滤），并写清新位置 | `claims.md` + 子主题 README |
| **给反例** | 论文机制在代码里找不到，或代码里有相反行为 | 保留旧句 + 反例 + 标 `存疑`；不合并成「平均」 | `claims.md` + `frontier` 的 G/N |
| **只加实现细节** | 接口/成本/失败模式，不改变真值 | 不改 claim；写 `findings.md` 的 F-xx | `findings.md` |
| **无对应** | 现有子主题装不下 | 不建新派/新子主题；写 `frontier` 的 G/N | `frontier.md` |

四条硬规则：

1. **先认领，再动笔**：写 digest 前先在 `sources.md` 预定一行（项目 → 哪条 `L/F`）；写不出就不写 digest。
2. **一段一锚**：digest 每个关键段标它回应哪条 `L/E`；没有对应就标 `F-new`，并准备进 `findings.md`。
3. **改写，不追加**：topics 里改旧句 + 边界从句，不新增「开源证据」小节；证据指针写成 `项目@commit:文件:符号`。
4. **不新增派/子主题**：代码发现按机制归入现有子主题；装不下就进 `frontier`，不建目录。
5. **反向回改**：改 `claims` 后必须回改 `sources.md` 与子主题 README 的摘要句，否则父页旧句。

## 4. 吸收矩阵（G-X 的代码版）

新建 `meta/open-source-absorption.md`，一行一个「项目 × 机制」，状态四选一：

| 状态 | 含义 |
|---|---|
| `pending` | 已选定，digest/吸收未开始 |
| `absorbed` | 代码发现已进 sources/findings/claims，且能反查 digest 段落 |
| `partial` | 进了 findings，但还没进 claims（或反之） |
| `orphan` | digest 有发现，topics 没接（必须修） |
| `rejected` | 明确判定「不适用/不改变判断」，写明理由 |

列：`项目 | 机制 | 执行形态 | 调用点 | 对应论文 digest | 影响的 L/F | 状态 | 动作`。
**完成标准**：没有 `orphan`；`partial` 有明确下一步负责人/会话。

## 5. 波次：一次只收一个子领域

> 教训来自论文全审：20 个主题一起拖，父页旧句会把你拖死。开源侧同理，**一次只动 1–2 个派**。

### Wave 1：判定与读路径（01 / 02）

1. **trustgraph**：追 `policy/triples/service.py → policy_filter.py` 的读路径策略链；跑 `tests/unit/test_policy`；写 digest。
   - 进 `01-constraint`：读路径授权 vs 动作前 gate 的差别（这是本轮最可能改判断的一条）。
   - 进 `02-judgment/checker`：策略求值算不算 checker。
2. **收口**：只改 01/02；更新矩阵；不碰 03/04/05/06。

### Wave 2：供给（03）

3. **semantica**：跑 `run_shacl_validation` 最小示例；确认 pyshacl 缺依赖时的降级。
   - 进 `03-knowledge`（供给）+ `02/checker`（校验，只补一段，不扩写）。
4. **ontop**：Docker 最小示例；追 `QuestQueryProcessor` 的 SPARQL→SQL 重写。
   - 进 `03-knowledge`：OBDA 作为 LLM 工具的边界（OWL 2 QL 限制）。
5. **收口**：矩阵 v2；03 的改动回写一次，避免两份口径。

### Wave 3：变更与生命周期（05 / 01）

6. **open-ontologies**：跑 W3C SHACL 一条用例；追 `closure_diff.rs` / `conservativity.rs` 的变更影响面。
   - 进 `05-produce/lifecycle` + `01-constraint/commit-gate`：它到底「阻断」还是「报告」。
7. **收口**：矩阵 v3；01 的第二处改动要回看 Wave 1 的结论是否被推翻。

### Wave 4：对照与结论（00 / conclusions）

8. **jena / ontogpt**：不写完整 digest，只在相关 digest 里做一段对照（标准栈为什么难进 agent；LinkML 约束的是抽取不是执行）。
9. **跨派检查**：只在出现「两个以上来源同向」时动 `conclusions`；否则写 `frontier` 的 G/N。
10. **全仓自检**：链接、frontmatter、`sources` 映射、矩阵无 orphan。

## 6. 完成定义（DoD）

一轮「开源消化完」= 同时满足：

- [x] 4 个核心项目都有 C3 的 `digest.md`，各有一条调用链 + 一次运行记录（成功或阻塞原因）：3 跑通，open-ontologies 因网络/工具链阻塞并留档。
- [x] 每个项目在 `sources.md` 至多两处、其中一处主记录（open-ontologies 跨 02/05 两处，主效应在 05 lifecycle；ontop 记在 03 frontier）；`reading`/`provenance` 与实际相符。
- [x] 6 条 `F-xx` 进 findings（commit-gate F5–F7、generation F7、checker F7–F8）；**1 条** `L-xx` 收窄（01-L13）；`conclusions` 未改。
- [x] `meta/open-source-absorption.md` 无 `orphan`（absorbed×3 + partial×1，partial 有下一步）。
- [x] README 状态表与磁盘一致：4 个目录、4 张卡、4 份 digest。
- [x] 低于门槛的项目已删除；扫描快照保留。

## 7. 不要做

- 不把 star 当证据；不把 README 当实现；不把「跑通示例」当「机制有效」。
- 不用 card 当 digest；不把 card 里的初判写成 topics 结论。
- 不因为「论文说应该有」就假设代码里有；找不到就写「没找到」，并进 `frontier`。
- 不在同一波里跨 3 个以上派；不在没有 digest 段落时新增 claim。
- 不为了凑数把 <1,000★ 的项目拉回来；要恢复先改门槛并说明理由。

## 8. 当前状态（2026-11-09）

- 已建卡：4 个（本轮）；已删除：3 个 <1,000★（元数据在扫描快照）。
- 已写 digest：4 个（trustgraph / semantica / ontop / open-ontologies）。
- 吸收矩阵：`absorbed`×3 + `partial`×1（ontop 只进 03 frontier），无 orphan。
- 下一动作：W4 对照（jena/ontogpt）可选；open-ontologies 换环境重跑 C2。
