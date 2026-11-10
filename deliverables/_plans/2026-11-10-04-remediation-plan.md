---
status: draft
type: work-plan
updated: 2026-11-10
target: deliverables/04-ontology-in-production
scope: content-remediation
---

# 04 内容整改计划：只做阅读、消化、校对、补内容

> **不做实现。** 不写 engine / harness / reference filter / EXP；不把 04 变成起始包。
> 04 是文档交付物；示例是阅读与对照用的 fixture，不是要交付的系统。
> 现有 3 个可选片段保留，标「作者已跑过；读者可选」；不新增可执行代码。
> 本计划是工作底稿，不是交付正文；不新增 E，不把计划里的判断写成仓库结论。

## 0. 定位

- **读者**：要落地小型本体查询应用的团队、评审/负责人、想快速读懂的新人。不是从零建系统的开发者。
- **04 是什么**：一份可读、可对照、可验收的落地材料；示例用来把数字/字段/失败模式讲清楚，不用来承诺「照抄就能跑」。
- **整改是什么**：读 `topics/` / `src/` 里的素材，把 04 的判断、数字、条件写对；补读者需要的解释内容；修内部矛盾。
- **整改不是什么**：不是写代码、不是补 evaluator、不是让 12 条 leak cases 变成可执行套件、不是加 `build_report.json` / `versions.json` / `query_log.json`。

## 1. 原则

1. **先读源，再改文。** 04 的每个数字/判断先回到 `topics/` 或 `src/` 找条件；找不到就标 `推测` 或 `gap`，不编。
2. **一个数只写一次。** canonical 值放正文一张表；其他页面引用，不复制。复制是矛盾的来源。
3. **数字带三件事**：principal、时点（raw / post-policy）、证据等级。缺一项就不算可读。
4. **主路径自包含。** 读者不打开 `topics/` 也能读懂 04；细节链接标「可选/出处」。
5. **先落 `topics/`，再落 04。** 如果整改改变了「策略可判定」「skip 会不会泄漏」「CQ3 能不能返回」这类判断，先改派内 `claims.md` / 机制页，再改 04；不改跨派 E。
6. **只改内容，不改形态。** 9 件产物不变；示例 JSON 只做与正文一致的最小修改；不扩成可执行套件。

## 2. 内容问题分诊

> `级`：P0 会卡住理解/验收；P1 会卡住新人读懂或复现；P2 文档硬伤。
> 这些是**阅读/写作问题**，不是工程问题。

### 2.1 语义（P0）

| ID | 问题 | 修法（文字/表格） |
|---|---|---|
| S1 | B.6 的 CQ1 2 / CQ2 7 列 4 表 / CQ3 4，没写 principal，也没写 raw 还是 post-policy；dec-0001 的 CQ2 是 0/7 | B.6/A.5 只写 raw；C.4 写 governed；每条期望加 principal 列；新增 journey 页把两者串起来 |
| S2 | `body/README` 说 C 用 CQ1–CQ3，但 C 章没有 CQ1/CQ3 的审计 | C.4 加 query log 表（CQ1/CQ2/CQ3/LEAK-T1 各一行）；审计样例只作样例，不是全集 |
| S3 | `policy.json` 没有优先级/默认；T1 同时匹配 R1/R7、T7 匹配 R6/R7、T9 匹配 R4/R6 | C.2 写「判定顺序」小节：specific rules → priority → 同优先级冲突=undetermined → 无命中=default；T9 保持 undetermined |
| S4 | `skip` 到底返回不返回行：T7/T8 期望 skip，LEAK-T1/L2 期望 0 行；dec-0002 的 skip 返回了行 | C.3 写清：skip=未判定，不是安全声明；执行层可以返回、也可以 withhold；leak 的期望是「敏感 object 不出现」，不是「0 行」 |
| S5 | 执行单位不明：CQ2 输出 column，CQ3 输出 dataset，L5 输出 count | C.3 加一句：判定单位是「输出行的 subject」；无 subject 的聚合查询不在列策略覆盖内，标 gap |
| S6 | 审计粒度不清：dec-0001 的 subject 是 `col_ssn`，outcome 是 query 级「CQ2 0/7」 | C.4 写清 per-subject record + query-level summary 表；dec-0001 outcome 改 per-subject |

### 2.2 数字/计数（P1）

| ID | 问题 | 修法 |
|---|---|---|
| N1 | 「11 类」与 TTL 只有 4 个 `a owl:Class` 不一致；`Address` 未用 | 删 `Address`，加 `:WorkEmail`（Email 子类），`tag_email_1` 改 `a :WorkEmail`；所有类补 `a owl:Class`；仍 11 类，CQ1 仍 2；数据表 tag 改 WorkEmail |
| N2 | `sensitivityLevel` 只要求 integer；policy 对 0 是 allow | A.4 shape 加 `minInclusive 1`/`maxInclusive 4`；A.4/boundaries 加一句「0/负数不在合法域；策略假定 1–4」；不新增坏样本，fixture 仍 2 violations |
| N3 | `policy.json` 7 条规则，但 CQ3 的 governance 没有数据集级规则 | 加 R8 `governance read dataset allow`；C.2 表加一行；policy tests 加 T11（governance dataset → allow）；「10 条」改「11 条」；「9 条唯一」改「10 条唯一」 |
| N4 | 12 条 leak cases 里 5 条在 fixture 没有数据/开关；L5 COUNT 的 `expected_rows:0` 语义不对 | reference §5 加 `illustrative/needs` 列；C.3 表改为「expected effect + sensitive object absent」；JSON 只加 `note`，不扩 harness；明确「这是测试设计，不是可执行套件」 |
| N5 | 只有 2 条 audit 记录；没有 allow 案例 | 加 dec-0003 CQ1 steward allow（同一 schema）；「2 条」改「3 条」；CQ3 的 governance 记录用 query log 表描述，不新增 JSON |
| N6 | `tag_version` / `contract_version` 没有来源；`snapshot` 是日期；`executor` 不记版本 | A.5 加「版本来源」表：policy←policy.json；ontology←ontology.ttl；tag/contract←`fixture 约定`（没有独立文件）；snapshot 标「日期标签，不是 hash」；真 replay 需要 hash+parser 版本，写进 boundaries |
| N7 | `build_report` 没有 consumer/principal/query_id；契约六项与 build_report 只有部分对应 | A.5 加覆盖表（从 `topics/05-produce/representation/consumability.md` §3 消化）；不新增 JSON 字段，只在正文表里标「缺」 |
| N8 | 9 件产物里没有 `build_report` 文件，但 A.5 有 JSON | README §2 注明「build_report 是 A.5 的内联样例，不单独成文件；9 件不变」 |

### 2.3 证据/来源（P1）

| ID | 问题 | 修法 |
|---|---|---|
| E1 | `build.md:38` 说「覆盖表见参考表 §2」，但 §2 是 10 个坏样本 | reference 加 §0「契约 ↔ build_report 覆盖表」；改链接 |
| E2 | `govern.md:104` 说「六类里只有前两类成本低」，reference §6 是四低一中一高 | 改为「前四类低，第五类中，第六类高；只测了前两类」 |
| E3 | `build.md:87` 的 PPV「见 evidence」但 evidence 没有 | evidence 加 O-F08 的公式/值，或删「见 evidence」 |
| E4 | `topics/01-constraint/policy/mechanism.md` 的 10 条测试 ID 与 04 `policy_tests.json` 已分叉 | 以 `policy_tests.json` 为 canonical（11 条），回改 topic 表；两边注明「对齐版本」 |
| E5 | read-path 说 object 命中「返回 1 行」，04 L2 说「保留 3 行」 | 统一 query 与计数；说明 1 行是单 object 探针，3 行是 `?col` 全表探针 |
| E6 | GGC 只写 92.34/98.33，reference 写 90.23→98.33 | B.3 补一句「Generator 单跑 90.23；全量 92.34；选择性 98.33」；不改变判断 |
| E7 | O-F14/O-N28/F1 没有链接 | evidence 加 O-F08/O-F14 链接；正文首次出现给一句人话 |

### 2.4 新人内容（P1）

| ID | 问题 | 修法（文字/表格） |
|---|---|---|
| R1 | 第一页就出现 TBox/ABox/CQ/SHACL/SPARQL/Turtle，没有定义；也没有「为什么用本体」 | 新增 `sections/glossary.md`（概念 15 条）；README 开头加「这是什么/不是什么」；「为什么」一段 + 链 01 |
| R2 | 没有一条查询的旅程 | 新增 `sections/journey.md`：CQ1 steward allow、CQ1 analyst deny、CQ2 7/4 vs 0/7、CQ3 governance、LEAK-T1 skip/leak |
| R3 | GUIDE 说「2 小时……几个人、几天」，04 没有人日；30 分钟路径对新人不可能 | GUIDE 加 effort 表（2–4 人周建模 + 3–5 人日 shapes，`推测`）；「30 分钟」改「30 分钟读 + 手算核对」；加「learning mode（用 fixture 契约）」 |
| R4 | 门槛数有 6/5/4/3 四种 | acceptance 放唯一 5 组门槛表；README/GUIDE 只链接，不复制数字 |
| R5 | 内码太多且未解释：E/T/S/O/F/L、K0/K1、GGC/NLKGQ/KGVoyager、Glyph/trustgraph/SFE-O | glossary 加「内码速查」；正文首次出现给一句人话；O-F08/O-F14 给链接 |
| R6 | 「5 分钟跑通」容易读成整条链跑通 | 改标题「5 分钟跑通查询子集（可选）」；首句说明只覆盖 parse/shapes/CQ1 |

### 2.5 文档硬伤（P1/P2）

| ID | 问题 | 修法 |
|---|---|---|
| H1 | `govern.md:40` 说「obligation 不在 policy.json；表比文件多一列」，但 C.2 表没有 obligation | C.2 表加 obligation 列（全 log），或删这句；与 topics/policy 的 7 列 schema 对齐 |
| H2 | `consume.md:148` 的「85%」没有出处 | 删掉或改成「任一分数」；若保留，补来源 |
| H3 | `fault_matrix.json` F5 写「T1 探针」，C.3 明确是 LEAK-T1 | 改 LEAK-T1；与 reference §7 对齐 |
| H4 | `policy_tests.json` T3 note 说「与 R7 同效，reason 不可区分」，但测试期望 policy_deny | 改为「效果同，reason 不同；R3 命中记 policy_deny」 |
| H5 | README §4 说「当前 fixture 预期返回行」，实际是 trustgraph 执行层返回行 | 改成「当前执行层（trustgraph）预期返回行」 |
| H6 | acceptance 模板 `checked` 含 C4，`not_run` 又含「C4 replay」 | 拆 C4 schema / C4 replay；模板只写实际读过的 |
| H7 | `ontology.ttl` 重复 `@prefix owl:`；`owl:inverseOf` 声明了但执行层不 entail | 删重复行；A.3 明说「inverseOf 只是文档，ABox 两侧显式写」 |
| H8 | `leak_cases.json` 的 query 没有 PREFIX | 加全局 `prefixes` 字段或每条 PREFIX（只改内容） |
| H9 | `reference §2` 标题是「十个坏样本」，被当成「覆盖表」 | 同 E1；加 §0 |
| H10 | README §4 的 6 条 vs acceptance 的 15 条/5 组 | README §4 只放 5 组门槛摘要；详细 15 项在 acceptance |

## 3. 目标形态

**04 读起来应该像一份“能读懂、能对照、能验收”的材料：**

```
README（这是什么/不是什么 + 读法 + 5 组门槛摘要）
  → GUIDE（10 分钟 / 2 小时 / 1 天；读什么）
  → A 建（契约 → 表示档位 → 本体 → shapes → 三关）
  → B 用（资产 → 路线 → 3 CQ raw → 空结果 → 纠错/OBDA）
  → C 治（三层 → 策略表/判定顺序 → skip/leak → 审计/query log）
  → sections（journey / glossary / reference / acceptance / map / boundaries）
  → evidence（出处，可选）
```

**内容形态**

- **数字**：每张期望表都有 `principal` 和 `raw / post-policy` 列；没有“裸数字”。
- **语义**：policy 的判定顺序、skip 的含义、审计粒度、版本来源，各有一小节文字，不靠读者猜。
- **示例**：fixture 仍是 5 表/13 列/11 类；示例 JSON 只做一致性修改；不承诺“跑”。
- **新人**：概念页 + journey + 术语/内码表；30 分钟是“读 + 手算核对”，不是“建完”。
- **形态**：9 件产物不变；不新增 `build_report.json`/`versions.json`/`query_log.json`；query log 用 C.4 的表。

## 4. 工作包

### C0 · 内容口径冻结（1 天）

- 定 §5 的 D1–D9；写进本计划和 `GLOSSARY.md` 草稿。
- 建一张 canonical 表（放 reference 或 A.5）：CQ1 2、CQ2 7/4、CQ3 4、classes 11、props 5、shapes 2、tables 5、columns 13、datasets 5、policy tests 11、leak cases 12、audit samples 3。
- 不做任何正文修改。

### C1 · 读源 + 证据对齐（2–3 天）

- 读：`topics/01-constraint/policy/mechanism.md`、`README.md`、`topics/01-constraint/commit-gate/read-path.md`、`topics/05-produce/representation/consumability.md`、`topics/objects.md`、`topics/03-knowledge/querying/compare.md`、`src/open-source/trustgraph-ai-trustgraph/digest.md`、`src/papers/2607.28082-ggc/digest.md`、`src/papers/2610.37809-what-does-an-ontology-catch/digest.md`。
- 建「承重句 → E/T/S/O → 条件」矩阵；04 每条主句一行。
- 找 6 个 P0 的源条件：raw/governed、CQ3 principal、skip、执行单位、审计粒度、policy 顺序。源里没有的，标 `gap`，不编。
- 只补 `topics/`/`src/` 缺的条件；不重写 digest，不新增 E。

### C2 · 语义内容（2–3 天）

- `body/build.md`：A.1 契约定义；A.2 K0/K1/pp；A.3 11 类/WorkEmail/minimality；A.4 shape 范围；A.5 三关 + 版本来源 + 覆盖表；A.6 边界。
- `body/consume.md`：CQ1/2/3 每条加 principal + raw；0 行分因；2×2；OBDA；删 85%。
- `body/govern.md`：C.1 三层；C.2 策略表 + 判定顺序 + 11 条测试；C.3 skip/leak/执行单位；C.4 per-subject + query log 表 + 3 条 audit 样例；C.5 成本表；C.6 边界。
- `example/`：最小一致性修改（WorkEmail、R8、T11、dec-0003、leak note、PREFIX、删重复 prefix、shape 范围）；不扩 harness。

### C3 · 新人内容（2–3 天）

- 新增 `sections/glossary.md`（概念 15 条 + 内码 10 条 + 版本词）。
- 新增 `sections/journey.md`（一条 query 的旅程；raw → policy → audit → replay 的读法）。
- `README`/`GUIDE`：这是什么/不是什么；30 分钟读路径；effort 表；learning vs applying；5 组门槛。
- `sections/map.md`：加「principal 对不上」「policy 冲突」「replay 版本对不上」三个症状。
- `sections/boundaries.md`：加「CQ3 聚合」「skip vs leak」「policy 语义未定」「level 范围」「版本不可 replay」五条边界。

### C4 · 文档一致性（1–2 天）

- 修 §2.3/§2.5 的 15 个硬伤。
- 统一所有计数（11 类、11 tests、3 audit、12 cases、9 artifacts）。
- 统一 gate 数（5 组）；README/GUIDE/acceptance 一致。
- `evidence/README.md` 加 O-F08/O-F14/PPV；每章证据行更新。
- `meta/state.md`、`deliverables/README.md`、`_plans/README.md` 同步。

### C5 · 冷读（1–2 天）

- 以「完全不懂」的姿势读一遍：只允许用 04 的文字；记录卡点。
- 10 问验收（见 §6）；P0 卡点修完再读一轮。
- 只改文字/表格/链接；不写代码。

## 5. 已定内容口径（不再问）

| # | 决定 | 理由 |
|---|---|---|
| D1 | **raw 与 governed 分离**：B.6/A.5 写 raw；C.4 写 governed；每条期望标 principal | 否则 CQ2 的 7/4 与 0/7 无法共存 |
| D2 | **CQ3 归 `governance` 角色**；policy 加 R8 `governance read dataset allow`；T11 验证 | CQ3 是 dataset 级治理查询，不能用 analyst；否则 T3 的 null-deny 与 4 个 dataset 冲突 |
| D3 | **skip=未判定，不是安全声明**；leak 的期望是「敏感 object 不出现」，不是「0 行」 | 保留 `skip ≠ allow`；同时让 T7/T8 与 LEAK-T1 不再打架 |
| D4 | **per-subject 审计 + query log 表**；加 dec-0003 allow；CQ3 用 query log 表描述 | 一条 query 7 列，一个 subject 不能代表 0/7；query 级 summary 放正文表，不放新文件 |
| D5 | **policy 判定顺序写在 C.2**：specific → priority → 同优先级冲突=undetermined → 无命中=default deny；T9 保持 undetermined | 不把研究里的“优先级空洞”偷偷修掉；读者能按表复算 |
| D6 | **9 件产物不变**；不加 `build_report.json`/`versions.json`/`query_log.json` | 04 是读本；文件不是内容；版本来源用表格写 |
| D7 | **删 `Address`、加 `WorkEmail`、`tag_email_1` 改 `a :WorkEmail`**；所有类补 `a owl:Class`；仍 11 类，CQ1 仍 2 | 同时解决“未用类”和“子类路径装饰”，不改变 CQ 计数 |
| D8 | **level 强制 1–4**（shape 加 min/max）；不新增坏样本；A.4/boundaries 写「0/负数不在合法域」 | 堵 fail-open；不把 2 violations 的计数打乱 |
| D9 | **effort 表用区间 + `推测`**：2–4 人周建模 + 3–5 人日 shapes + 5–10 人日实现；GUIDE 不再承诺“2 小时估工期” | 诚实；不把别人的单厂数据当报价 |
| D10 | **不做实现**：不写 engine/harness/reference filter/EXP；现有 3 个可选片段保留并标「可选」 | 用户明确：只要读本/素材，不要实施 |

## 6. 验收 / DoD

- [ ] 每个期望数字都有 principal + raw/post-policy + 证据等级；没有裸数字。
- [ ] 每个主句能指回 `E/T/S/O` 或标 `工程产物/未测`；没有来源的降级或删。
- [ ] policy 判定顺序、skip 含义、审计粒度、版本来源各有一小节；读者能按文字复算 T1–T11。
- [ ] 11 类可用 `?c a owl:Class` 复现；`Address` 不再出现；`WorkEmail` 被 CQ1 命中；CQ1/CQ2/CQ3 计数不变。
- [ ] 10 个坏样本仍是 10 个；2 violations 不变；level 1–4 已写进 shape/边界。
- [ ] 9 件产物不变；没有新增 `build_report.json`/`versions.json`/`query_log.json`；query log 是 C.4 的表。
- [ ] 主路径无未定义术语/内码；glossary 覆盖 04 正文出现的 E/T/S/O/F/K 码。
- [ ] README/GUIDE/acceptance 门槛组数一致（5 组）；验收模板 `checked`/`not_run` 不重叠。
- [ ] `check_repo.py` 通过；`topics/`/`src/` 与 04 的测试 ID、object 计数、class 计数一致。
- [ ] 冷读 10 问能答；0 个 P0 卡点；P1 有登记。
- [ ] 没有新代码、没有新 E、没有生产效果承诺；04 状态保持 `draft`。

**冷读 10 问**

1. 这是什么？不是什么？
2. 9 件产物各是什么？哪件是文档、哪件是 JSON 样例？
3. CQ1/CQ2/CQ3 各是谁、raw 多少、policy 后多少？
4. policy 的默认/冲突/优先级怎么判？T9 为什么 undetermined？
5. skip 与 deny、allow 的区别？LEAK-T1 为什么不是「0 行」？
6. 12 条 leak cases 里哪些是测试设计、哪些需要额外 fixture？
7. 审计是 per-subject 还是 per-query？replay 需要哪些字段？fixture 的 snapshot 为什么不是 hash？
8. 11 类怎么数？level 0/负数为什么不在合法域？
9. 这条链要几个人、几天？哪些是推测？
10. 哪些话不能信？建/用/治各自的边界是什么？

## 7. 不做什么

- 不写代码、不建 engine/harness/reference filter、不建 `EXP-xxx`、不新增可执行文件。
- 不新增 `build_report.json`/`versions.json`/`query_log.json`；query log 用表。
- 不新增 E；不改 `topics/conclusions.md`；局部判断变化先落派内 `claims.md`。
- 不修 trustgraph、不声称生产可用、不声称泄漏率/延迟。
- 不把 04 改成从零教程；新人入口只到“能读懂 + 能对照”，不到“能独立建”。
- 不设外部资产 gate。
- 不为“看起来完整”加空文件/空小节。

## 8. 工期（1 人估算）

| 工作包 | 工期 | 前置 |
|---|---:|---|
| C0 口径冻结 | 1 天 | 本计划批准 |
| C1 读源/证据对齐 | 2–3 天 | C0 |
| C2 语义内容 | 2–3 天 | C1 |
| C3 新人内容 | 2–3 天 | C1（可与 C2 并行） |
| C4 一致性/硬伤 | 1–2 天 | C2/C3 |
| C5 冷读 | 1–2 天 | C2/C3/C4 |

**约 9–14 个工作日**；内容优先，不按文件数量排。

## 9. 文件清单

**04 文档**

- `README.md`、`GUIDE.md`
- `body/build.md`、`body/consume.md`、`body/govern.md`、`body/README.md`
- `sections/reference.md`、`sections/acceptance.md`、`sections/map.md`、`sections/boundaries.md`、`sections/relations.md`、`sections/README.md`
- 新增 `sections/journey.md`、`sections/glossary.md`
- `evidence/README.md`
- `example/README.md`；`example/ontology.ttl`、`catalog.ttl`、`shapes.ttl`、`policy.json`、`policy_tests.json`、`leak_cases.json`、`audit.schema.json`、`audit_records.json`（只做最小一致性修改）

**topics**

- `topics/01-constraint/policy/mechanism.md`、`README.md`、`findings.md`（只在判断变化时）
- `topics/01-constraint/commit-gate/read-path.md`
- `topics/05-produce/representation/consumability.md`
- `topics/objects.md`（O-F08/O-F14 入口）
- `topics/01-constraint/claims.md`、`topics/05-produce/claims.md`（如判断变化）

**src**

- `src/open-source/trustgraph-ai-trustgraph/digest.md`（删除单位/object 计数/版本缓存）
- `src/papers/2607.28082-ggc/digest.md`（三数口径，如缺）
- `src/papers/2610.37809-what-does-an-ontology-catch/digest.md`（PPV/O-F08，如缺）
- `src/web/w3c-shacl/w3c-shacl.card.md`（targetClass 子类闭包，如缺）
- `src/web/gbt-43697/gbt-43697.card.md`（三级名称，如缺）

**meta**

- `GLOSSARY.md`
- `meta/state.md`、`meta/checklist.md`（加一条「交付物语义一致」）
- `deliverables/_plans/README.md`、本计划
- `deliverables/README.md`

## 10. 第一步（C1）

先读这四份，不写正文：

1. `topics/01-constraint/policy/mechanism.md`：10 条测试、冲突消解、审计最小单元。
2. `topics/01-constraint/commit-gate/read-path.md`：object 方向、fail-open、1 行 vs 3 行。
3. `topics/05-produce/representation/consumability.md`：三关、10 坏样本、契约↔build_report。
4. `src/open-source/trustgraph-ai-trustgraph/digest.md`：`_triple_blocked`、缓存、版本。

产出「6 个 P0 的源条件表」：raw/governed、CQ3 principal、skip、执行单位、审计粒度、policy 顺序。源里没有的标 `gap`。这张表是 C2 的输入，不直接进 04。
