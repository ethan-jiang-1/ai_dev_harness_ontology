---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# 参考表：正文用到的矩阵与目录

> 这些表已从研究底稿消化到 04，读正文时不需要跳出去。证据等级用「已核 / 推测 / 工程产物 / 未测」标，不在这里展开来源。
>
> **词源**：「leak oracle / principal / level 1–4 / skip」是 `local` 工程词；SHACL/shape/三态 = `N: W3C SHACL`；策略表达 = `N: W3C ODRL 2.2`，判定架构 = `N: OASIS XACML 3.0`；数据分级 = `N: GB/T 43697-2024`，个人信息 = `N: GB/T 35273-2020`。逐词见 [术语 §0](90-glossary.md#term-sources)。

## 0. 契约 ↔ `build_report` 覆盖表 / canonical 计数

> 这页补上 A.1 说的「覆盖表」；A.1 六项与 A.5 `build_report` 只部分对应。来源：`topics/05-produce/representation/consumability.md` §3。

| `build_report`（A.5） | consumer | principal | moment | answers | refuses | load |
|---|---|---|---|---|---|---|
| `load.parsed` | — | — | — | — | — | ✓（仅本地解析） |
| `load.violations` | — | — | — | — | —（shape 违反 ≠ 拒绝） | ✓（shape） |
| `load.missing_fields` | — | — | — | — | — | ✓（产物必填，非契约） |
| `classes`/`properties` | — | — | — | — | — | ✓ |
| `policy_version`/`tag_version` | — | 弱（产物版本，非主体） | — | — | 弱（非拒绝谓词） | — |
| `provenance.source` | — | —（`synthetic` 不是 principal） | — | — | — | — |

三个碰撞：`load` 在 A.1 是“怎么加载”、在 A.5 是“加载结果”；`violations` ≠ `refuses`；`missing_fields` ≠ 契约缺字段。`missing_fields=[]` 不能证明六格完整。

**canonical 计数**（其他页引用这里，不复制）：

| 项 | 值 |
|---|---|
| 产物 | 9 件；`build_report` 是 A.5 内联样例，不单独成文件 |
| 类 / 属性 / shapes | 11 / 5 / 2 |
| 表 / 列 / dataset | 5 / 13 / 5 |
| 坏样本 | 10；shape 声明样本 2；现抓 S7/S8 |
| policy | 8 条规则；11 条测试；T9 undetermined；T10 default deny；T11 governance dataset allow |
| leak | 12 例；部分需要额外 fixture（见 §5） |
| audit | 3 条样例；query 级 summary 在 C.4 表 |
| 版本 | policy 0.4.0；ontology/tag/contract 0.1.0；snapshot 是日期标签 |

## 1. 三档表示 × 四类消费

| 档 \ 消费 | load | validate | query | explain | 成本 |
|---|---|---|---|---|---|
| 词表 | supported | partial | supported | partial | 低 |
| 结构表 | supported | supported | supported | partial | 中 |
| 逻辑表 | supported | partial | partial | not | 高 |

**读法**：结构表是唯一三关都 `supported` 的档；词表 validate/explain 弱；逻辑表 explain 无可移植路径。这是能力矩阵，不是效应量。

## 2. 十个坏样本

| # | 坏样本 | 失败类型 | 现有闸门 |
|---|---|---|---|
| S1 | 缺 principal | 契约缺字段 | silent |
| S2 | 缺 moment | 契约缺字段 | silent |
| S3 | 缺 refuse | 契约缺字段 | 全放行 |
| S4 | 缺 load | 契约缺字段 / 假阳性 | `parsed=true` |
| S5 | 缺 version | 契约缺字段 | silent |
| S6 | shape 缺 target | 0 focus / 空转 | `conforms=true` |
| S7 | tag 是字面量 | shape 违反 | **抓住** |
| S8 | level 缺失 | shape 违反 | **抓住** |
| S9 | 无 dataset 边 | answer undercoverage | 不报 |
| S10 | 版本不一致 | version skew | silent |

**分母**：`2/2` 是 shape 声明样本（S7/S8）；10 个契约坏样本只抓 2 个（同一对 S7/S8）。不要把它当两个独立测试。

## 3. 四条查询路线

| 路线 | 先有什么 | 指标（单设置） | 成本 | 主要失败 | 可比性 |
|---|---|---|---|---|---|
| GGC | 已有 KG + 生成器 | 答案集匹配 90.23→98.33 | 单跑 ~30h / 选择性 ~33h / 全量 ~60h | 空结果无机制；单 KG/单骨干；无 2×2 | 与其余不可比 |
| NLKGQ | 完整 OWL + endpoint | 旧报告有 Match/Exact（源已移出，不引用） | 未报 | snapshot/窗口；wrapper 手工 | 与 GGC 不可比 |
| KGVoyager | 只有 endpoint | 旧报告有 F1 与成本（源已移出，不引用） | 未报 | 非 `rdf:type` 图；探索成本；benchmark 小 | 与前两者不可比 |
| OBDA | 关系库 + 映射 | 无 benchmark | 未报 | 重写正确≠查询正确；OWL 2 QL | 与三者不可比 |

**读法**：三条路线的旧分数不能排成一条线（其中两条来源已移出）；按资产条件选，不按总分排。

## 4. 十七类失败

| # | 类型 | 触发 | 检测 |
|---|---|---|---|
| 1 | Gate 分布外 | 换图/换生成器 | 目标分布 100 条重标，报 trigger/FPR |
| 2 | 无 2×2 | 只报总准确率 | 初始对/错 × 改后对/错 |
| 3 | 空结果不进 Gate | 0 行 | 单独采样，分因 |
| 4 | 本体超窗口 | 完整 OWL 太大 | 统计 ontology token；slice 对照 |
| 5 | snapshot 漂移 | endpoint 更新 | 记录并重放 snapshot |
| 6 | wrapper 手工 | 原生词不透明 | wrapper→native 映射单测 |
| 7 | 非 `rdf:type` 图 | Wikidata 类体系 | `ASK { ?s a ?c }` 抽样 |
| 8 | 探索成本膨胀 | 图/属性规模大 | iterations / tool calls / wall-clock |
| 9 | benchmark 小且同源 | 题量小、同源 | 换独立域；报 CI |
| 10 | 重写正确但结果错 | OBDA | 原生 SQL vs 重写 SQL 结果集 |
| 11 | OWL 2 QL 表达力 | 超 QL 公理 | `ontop validate`；列被拒公理 |
| 12 | 执行准确≠业务正确 | 只看 accuracy | 自域配对 + 人工抽检 |
| 13 | 实体未链接 | 只给自然语言名 | `ASK { ?e rdfs:label "…"@en }` |
| 14 | 聚合/去重错 | 非 DISTINCT / join 放大 | `COUNT(*)` vs `COUNT(DISTINCT ?x)` |
| 15 | `LIMIT` 无 `ORDER BY` | 998/1,000 带 LIMIT | 同 query 连跑 5 次比结果集 |
| 16 | 假空（超时/放弃） | 超时 / 不提交 / 失败记 0 | 查超时/放弃日志；gold query 复跑 |
| 17 | 参考本身错 | benchmark 缺陷 | 执行 gold query；`gold_invalid` 剔除 |

## 5. 读路径十条用例

> 上游有 4 条待核（E-23）：本表 10 条里 6 条已核、4 条待核；引用时按 [govern C.3](../03-body/03-govern.md) 的标注。

| # | 用例 | 安全期望 | trustgraph（`184f622`） |
|---|---|---|---|
| 1 | subject 命中 | 删 | 删 |
| 2 | object 命中 | 删 | **不删**（只查 `triple.s`；`?col` 全表探针返回 3 行，单 object 探针 1 行） |
| 3 | 两侧命中 | 两侧删 | 半（subject 删、object 留） |
| 4 | 都不命中 | 原样 | 原样 |
| 5 | target 异常 | fail-closed | **fail-open** |
| 6 | 缺 `user_context` | 拒 | 拒（唯一 fail-closed） |
| 7 | alias | 按同实体过滤 | 无处理 |
| 8 | 聚合 | 不返回可反推计数 | 入口是三元组流，不适用 |
| 9 | 无策略 | 默认 deny / 显式 open | open mode |
| 10 | 版本不匹配 | 拒/回退 | 60s 缓存，不含版本 |

**判定**：单实现、fail-open、只删 subject；没有合格第二实现。读过滤 ≠ 写授权。

**12 条 leak cases 与这 10 条的关系**：L1↔1、L2↔2、L3↔3、L10↔6、L4↔7、L5↔8、L11↔9、L9↔10；L6/L7/L8/L12 是额外泄漏面；用例 4/5 没有 L 对应。两套不是一套，编号不要混。

## 6. 输出校验六类

| # | 类 | 查什么 | 失败例 | 成本 |
|---|---|---|---|---|
| 1 | schema | 列名/类型/非空 | `?col` 为字面量 | 低 |
| 2 | cardinality | 行数/表数/列数 | CQ2 0 行；CQ3 少 dataset | 低 |
| 3 | provenance | `query_id/snapshot/version` | 结果无法回放 | 低 |
| 4 | freshness | snapshot 在 SLA 内 | 30 天前快照 | 低 |
| 5 | cross-field | level/tag/策略一致 | `col_ssn` level 2 | 中 |
| 6 | semantic plausibility | 分布/类型反常 | 所有列 level 4 | 高 |

**三态**：pass / violation / undetermined；`pass` 只在 `targeted>0` 且 `skipped=0` 时给。

## 7. 故障矩阵（10 类 × 3 段）

| # | 故障 | build | query | govern | 信号 |
|---|---|---|---|---|---|
| 1 | 坏 shape | `targeted=0` | 看似通过 | 无违反 | targeted/skipped |
| 2 | 缺 tag | violations 0 | 少行/多行 | level=null → deny/skip | CQ3 计数 |
| 3 | 错 level | shape 通过 | CQ2 多/少列 | allow/deny 反 | tag vs col level |
| 4 | 空结果 | — | 0 行 | 被当没有敏感列 | 分因表 |
| 5 | 错 join | — | 0 行/错集 | object 泄漏 | MINUS 双向、LEAK-T1 |
| 6 | policy skip | — | — | 表/数据集不判 | skip + reason |
| 7 | object 泄漏 | — | 结果含敏感列 | leak_check 失败 | 结果内容 |
| 8 | 快照过期 | — | 同题不同分 | 无法 replay | snapshot |
| 9 | 版本不匹配 | 缺版本 | 语义漂移 | 版本对不上 | 版本三元组 |
| 10 | 超时/放弃 | — | 0 行（假空） | 缺 decision | 超时/放弃日志 |

**读法**：同一「0 行」可能是 2/4/5/10；同一「allow」可能是 3/6/9。先定位到段，再改 prompt/策略。

> 细节/出处（可选）：原始研究底稿在 [`topics/`](../../../topics/README.md)；主路径不需要打开。

> 回 [04 目录](../README.md) ｜ 回 [验收](05-acceptance.md)
