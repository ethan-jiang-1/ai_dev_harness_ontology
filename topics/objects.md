---
status: draft
updated: 2026-11-12
scope: evidence-objects
---

# 硬对象注册表（O-xx）

> **这是地址层，不是结论层。** 每个对象只回答「这条判断的数/公式/代码在哪、在什么域、什么会推翻它」；不新增判断，不与 `E-xx` 竞争。
>
> **引用规则（ADR 0009，方案 A）**：交付物可引 `O-xx` 作**地址**，主句仍必须落在 `E-xx`；O 必须挂 ≥1 条 E，冲突时以 E 为准，O 撤销。
>
> **ID**：`O-C01`（代码）/ `O-F01`（公式）/ `O-T01`（停线）/ `O-M01`（矩阵）/ `O-N01`（数值）/ `O-R01`（反例）/ `O-P01`（协议）。类型前缀是执行时加的（计划原稿写 `O-01`），检查规则相应写成 `O-[CFTMNRP]\d\d`。
>
> **schema**：`claim / value / address / domain / provenance / hardness / falsifier / feeds`；`status` 默认 `active`，变更见文末。硬度：**H2 可核对**（`§/表` 地址 + 域）；**H3 可复算/可执行**（公式例、`file:symbol`、行 ID）。H1（带数无地址）不进本表。

## 计数（2026-11-12 对账）

| 项 | 值 |
|---|---|
| 注册对象 | **94**（含 20 已撤回，编号保留供回链） |
| 现存对象 | **74**（H3 33 / H2 41） |
| 类型（注册） | C 15 / F 15 / T 13 / M 4 / N 29 / R 12 / P 6 |
| 已撤回 | 20：F08/F10/F15、N01–N03/N07–N09/N13–N15、R02/R05/R12、T05–T07、P02/P03 |
| E 覆盖 | 现存 10 条 E 有对象；E-02/03/04 行为撤回存档 |

**怎么用**：先按交付物页找 E，再从 E 索引找对象；`feeds` 列是该对象在交付物里的落点。引用时写 `E-xx（O-N02）`——E 是结论，O 是地址。

## C · 代码锚（15）

| ID | claim | value | address | domain | provenance | 硬度 | falsifier | feeds |
|---|---|---|---|---|---|---|---|---|
| O-C01 | 策略入口与策略来源 | SHACL-AF（NodeShape + SPARQLTarget + SPARQLRule + tg-pol:blocks）从 `urn:graph:policy` 加载；判定单位是节点 IRI | policy/policy_filter.py: PolicyFilter.load_policies（pin 184f622） | trustgraph @184f6228；只读代码 | E-20；digest §3/§6 | H3 | 找到第二个策略入口，或策略实际不来自该命名图 | 03 execution-forms；03 commit |
| O-C02 | 只删 subject 侧 | _triple_blocked 只检查 triple.s；以敏感节点为 object 的三元组不删 | policy/policy_filter.py: _triple_blocked（pin 184f622） | trustgraph @184f6228 | E-20；digest §3/§6 | H3 | 构造 object 侧敏感三元组，若被删除则行为不同 | 03 execution-forms；03 commit |
| O-C03 | fail-open | target/rule 抛异常 → 当作不命中/无判定；缺 sh:select/construct → 跳过策略；无策略 → 全量返回；只有「有策略但没传 user_context」是 fail-closed | policy/policy_filter.py: apply（pin 184f622） | trustgraph @184f6228 | E-20；digest §6 | H3 | 构造抛异常 target，若请求仍返回数据则 fail-open 确认 | 03 execution-forms；01 data/e7-e8 |
| O-C04 | 策略测试存在但未重跑 | test_policy_filter.py 31 条，覆盖判定/非阻断直通/回调/无策略直通/缓存/并发 | tests/unit/test_policy/test_policy_filter.py（pin 184f622） | trustgraph @184f6228 | E-20；digest §6 | H3 | 在 pin commit 上重跑失败，或缺异常路径用例 | 03 execution-forms；03 commit |
| O-C05 | 本体先编译成 SHACL | OntologyEngine.to_shacl() 从 ontology dict 生成 shapes | engine.py:200 to_shacl（pin 39cf721） | semantica @39cf7216；只读代码 | E-20；digest §3 | H3 | 发现 validate 路径绕过 to_shacl 直接吃 OWL | 03 execution-forms |
| O-C06 | 校验入口 | validate_graph() 调 pyshacl 校验 | engine.py:313 validate_graph（pin 39cf721） | semantica @39cf7216 | E-20；digest §3 | H3 | 存在不经过 validate_graph 的校验路径 | 03 execution-forms |
| O-C07 | 校验时不做 OWL 推理 | pyshacl.validate(inference="none")；validate_graph 不暴露推理参数 | ontology_validator.py:194 pyshacl.validate(inference="none")（pin 39cf721） | semantica @39cf7216 | E-20；digest §3/§6 | H3 | 把 inference 改为非 none 后行为变化，说明当前是显式关闭 | 03 execution-forms |
| O-C08 | 查询重写时执行 | QuestQueryProcessor 构造时 rewriter.setTBox(getSaturatedTBox())；reformulateIntoNativeQuery 做 TBox 饱和 + 重写 | QuestQueryProcessor.java:31 / :79（pin 964dbb7） | ontop @964dbb7943；只读代码 | E-20；digest §3/§6 | H3 | 重写不依赖 TBox（例如只做映射展开） | 03 execution-forms；02 offline-and-obda |
| O-C09 | 重写后原生执行 | QuestStatement 在 JDBC 上执行原生 SQL，结果转回 SPARQL 绑定 | QuestStatement.java:131（pin 964dbb7） | ontop @964dbb7943 | E-20；digest §3 | H3 | 执行路径绕过重写器，直接用原 SPARQL | 03 execution-forms |
| O-C10 | SHACL 编译成 SPARQL | 默认路径把 SHACL Core 约束编译为 SPARQL，交 Oxigraph 求值 | src/shacl.rs（pin 375fbc4） | open-ontologies @375fbc47；只读代码 | E-20；digest §3/§6 | H3 | 存在不经过编译的默认求值路径 | 03 execution-forms |
| O-C11 | verified 路径的覆盖与拒绝 | verified 包装 oo-shacl 的 SHACL Core；拒绝 sh:sparql 与自定义组件（120 条里 22 条）；exit 3 = undetermined | src/shacl_verified.rs（pin 375fbc4） | open-ontologies @375fbc47 | E-20；digest §3/§6 | H3 | verified 路径接受 sh:sparql 或漏报 22/120 | 03 execution-forms |
| O-C12 | 三态在退出码被折叠 | gate_exit_code 把 null 折叠成 2（与 violation 不可区分） | src/main.rs:1822 gate_exit_code（pin 375fbc4） | open-ontologies @375fbc47 | E-20；digest §6 | H3 | 构造 undetermined 与 violation，若退出码相同则折叠确认 | 03 execution-forms；02 offline-and-obda |
| O-C13 | 变更影响报告 | closure_diff 报告 entailments_lost / lost_by_warrant / monotonicity_violations，exit 2 为 stop-the-line；是否阻断由调用方决定 | src/closure_diff.rs（pin 375fbc4） | open-ontologies @375fbc47 | E-20；digest §3/§6 | H3 | 报告字段缺失，或 exit 2 被调用方忽略后仍视为通过 | 03 execution-forms；02 offline-and-obda |
| O-C14 | 不解析本体 | ast/ 是 Rego AST，compile/ 是 Rego 编译；没有 OWL/SHACL/RDF 的解析或推理 | ast/、compile/（pin 3dc83ae） | OPA @3dc83ae32；只读代码 | E-22；OPA digest §2/§10 | H3 | 找到 RDF/OWL 解析模块，或策略直接消费本体文件 | 03 commit；01 access-control |
| O-C15 | 只返回 decision，执行在调用方 | server/server.go 暴露 /v1/data/...，返回 allow/deny/结果；阻断不由 OPA 执行 | server/server.go（pin 3dc83ae） | OPA @3dc83ae32 | E-22；OPA digest §3/§5 | H3 | OPA 进程内直接执行副作用或阻断写操作 | 03 commit；01 access-control |

## F · 公式（15）

| ID | claim | value | address | domain | provenance | 硬度 | falsifier | feeds |
|---|---|---|---|---|---|---|---|---|
| O-F01 | 编译回本门槛 | `p_min = 2.0% + c/(0.929Q)`；Q=1,000、c=10 → 公式 3.08%，digest 写 3.12%（差 0.04pp，c/Q 疑为 rounded） | src/papers/2610.41172-context-as-infrastructure/digest.md#43-成本模型 | 冻结语料；c 只含首次编译，不含变更重抽/重聚类 | E-14；CAI §4.3 | H3 | 按公式复算与表值不一致且无法用 rounded 解释 | 02 §5.1 T04；01 data/e3 |
| O-F02 | 判门阈值随 miss 移动 | miss ±1.5pp → p_h* 0.4–3.6%（名义 2.0%）；2.0–3.6% 只适用论文门 | src/papers/2610.41172-context-as-infrastructure/digest.md#43-成本模型 | 论文门；FRAMES 类语料 | E-14；CAI §4.3 | H3 | 换语料/门后实测 p_h* 落在 band 外 | 01 data/e3；02 §5.3 |
| O-F03 | 多模式分配的代价 | `J(m) = γ_m·p̂ĉ + λk(m) + μq(m)`；γ 仅假设值（1.00/0.42/0.15/0.04） | src/papers/2610.36570-casel/digest.md#33-六种模式与代价 | 模拟；审批疲劳未建模 | E-15；CASEL §3.3/§6.5 | H2 | γ CI 宽到分不开 direct/verify，或审批疲劳使 J 排序翻转 | 02 recipes/constraint.md；06 feasibility |
| O-F04 | 护栏 NPV 口径 | `NPV_build = Σ(伤害节省 − 审批成本 + task success 收益)/(1+r)^t − TCO`；`NPV_do_nothing = 0`；单价全空 | src/papers/2610.36570-casel/digest.md#e4-成本收益模型公式不编价 | 建模约定；不是论文结果 | E-15 + derived | H2 | 代入单价后排序与 harm–approval 前沿矛盾 | 06 feasibility F5；02 operations/cost |
| O-F05 | 审批成本/千次 | `approval_rate × 1000 × minutes_per_approval/60 × hourly_rate`；单价空 → 只能给公式与敏感性 | src/papers/2610.36570-casel/digest.md#e4-成本收益模型公式不编价 | 同上；审批疲劳未建模 | derived；CASEL §6.5 | H2 | 实测每分钟审批成本与假设差一个量级 | 02 operations/cost |
| O-F06 | 判门样本量 | 100–200 只够 smoke；2.0 vs 3.6 需 1,600–2,000 shadow 查询；真实 4%→约 1,900、3.5%→约 9,000（digest 推算） | src/papers/2610.41172-context-as-infrastructure/digest.md#6-工程上怎么用 | 95% CI 下界判门；预登记样本量 | E-14 + derived | H2 | 预注册序贯设计使所需样本显著下降 | 02 operations/evaluation；01 §5.2 |
| O-F07 | 平均收益是 hit/miss 混合 | `savings = p_h·s_hit + (1−p_h)·s_miss`；0.43×(−91%) + 0.57×(+1.9%) = −38.0% | src/papers/2610.41172-context-as-infrastructure/digest.md#42-token-收益是条件性的 | FRAMES；p_h=0.43 是反推；两端为条件值 | E-08/E-14 + derived | H3 | 同语料实测 p_h 与 43% 差 >10pp 且平均收益翻转 | 01 data/e3；02 §5.1 |
| O-F08 | （已撤回）prevalence 修正后的 precision 可复算 | `PPV = π·Se / (π·Se + (1−π)·FA)`；π=0.25；curated Se=60.1%、FA=15.0% → 57.2%（原文 57.1）；data-derived 75.6/9.7 → 72.2%（原文 72.3） | meta/audits/2026-11-11-source-purge.md | 人工故障；25% 错答案假设；单 benchmark；输入四舍五入 | E-02；Catch §4.2 + derived | H3 | 真实错答案比例偏离 25% 使排序翻转 | 02 recipes/judgment；01 data/e4 |
| O-F09 | 「neutral」的分辨率 | `half-width = 1.96·sqrt(p(1−p)/n)`；p=0.91、n=200 → ±3.97pp（单臂）；两臂独立差 ×√2 → ±5.61pp | src/papers/2610.41172-context-as-infrastructure/digest.md#41-被测量的结构化工件没有准确率增益 | 单次运行、无 CI；FRAMES N=200；配对数据未给 | E-01；CAI §4.1 + derived | H3 | 配对分析或更大 N 使区间明显更窄 | 01 boundaries；03 context |
| O-F10 | （已撤回）序列分数取最弱一步 | `φ(π) = min φ(u)`；T1 w、T2 w·1[Bound]、T3 w·(1−w_loss)、T4/T5 0；示例（权重为假设）：T1 w=0.9 → 0.90 APPROVE；T3 w=0.9、w_loss=0.2 → 0.72 Veto | meta/audits/2026-11-11-source-purge.md | POLAR 五档；τ=0.80；示例权重 illustrative，不是论文数 | E-04；POLAR §3.4 + derived example | H3 | 论文实际用加权和/平均而非 min，或 τ 不是 0.80 | 02 recipes/constraint；03 action |
| O-F11 | alias/registry 的相对提升 | `lift = (Full − baseline)/baseline`；(30.4−22.2)/22.2=+36.9%；(30.4−8.2)/8.2=2.71 → 3.71× | src/papers/2610.40482-firme/digest.md#41-memory-usability | investor+Opus 单设置；CMR 口径；其他设置 2.3–3.7× | E-05；FIRME Table 3 + derived | H3 | 另一设置显示相对提升 <10% | 01 data/e6；04 identity |
| O-F12 | 审批相对降幅 | `reduction = (12.6−8.7)/12.6 = 31.0%`；HSR 7.02 vs 5.82（CASEL 更高） | src/papers/2610.36570-casel/digest.md#43-为什么-casel-不是最低-hsr | 模拟；τ=∞ 主表；审批疲劳未建模 | E-15；CASEL §4.3 + derived | H3 | 审批疲劳建模后相对优势消失 | 01 data/e5；06 feasibility |
| O-F13 | 消融差可直接复算 | `Δ = score(full) − score(ablation)`；57.6−48.7=8.9；57.6−49.6=8.0；57.6−49.7=7.9 | src/papers/2611.03743-evomemstate/digest.md#4-结果数字与条件 | MemSyco；Qwen3-8B；单模型族 | E-17；EvoMem §4 + derived | H3 | 重跑方差大于 1pp，使差值不可区分 | 01 data/e6；04 memory |
| O-F14 | 薄层与深层的边际贡献可加 | `Δ_total = Δ_K1 + Δ_K2`；54.6 + 19.8 = 74.4pp；薄层占 54.6/74.4 = 73.4% | src/papers/2610.11768-narrow-and-deep/digest.md#41-投影文本 | 单工厂/9 任务；同一 rubric 端点差；加法未做交互检验 | E-12；N&D §4.1 + derived | H3 | 端点差不是同一 rubric，或交互项使可加性不成立 | 01 map；02 knowledge |
| O-F15 | （已撤回）同预算的 token 效率（派生） | `eff = accuracy/(tokens/1000)`；84.9/9.7=8.75 vs 66.7/96.7=0.69 → 12.7×（论文未报此指标） | meta/audits/2026-11-11-source-purge.md | Test 3、Qwen、8k 预算；派生指标不是论文数 | E-03；OA-RAG §4.2 + derived | H3 | 换预算/任务复算后比值 ≤1，或论文自己报的 efficiency 不同 | 02 judgment；01 map |

## T · 停线（13）

| ID | claim | value | address | domain | provenance | 硬度 | falsifier | feeds |
|---|---|---|---|---|---|---|---|---|
| O-T01 | R0 准入 | 任一项 unknown 当 pass → 停 | deliverables/02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺 | 四项检查：名字/单位、声明、覆盖、执行落点 | 工程建议 | H2 | 四项检查不能预测后续失败（无对照） | 02 recipes/readiness |
| O-T02 | K1 语义层 | 剩余 trap 与深知识无关 → 停 | deliverables/02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺 | 单工厂/9 任务 | 工程建议 + E-12 | H2 | 深知识成为主要剩余错误来源 | 02 recipes/knowledge |
| O-T03 | 投影 | <5pp、>60k 字符、>2 人周/月 → 停 | deliverables/02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺 | 单工厂；顺序敏感 | 工程建议 + E-12 | H2 | 跨域复现显示 +5pp 在 60k 内稳定 | 02 recipes/knowledge |
| O-T04 | 编译 | p_h 的 95% CI 下界 ≤ p_min → 停（不用点估计） | deliverables/02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺 | 冻结/变更语料分开 | E-14 / O-F01 | H3 | 预注册序贯设计能更早判且不增错误率 | 02 recipes/knowledge；01 data/e3 |
| O-T05 | （已撤回）证据契约 | 检索率 <50% → 停（先修检索）；阈值随源停用，协议设计可换锚复用 | meta/audits/2026-11-11-source-purge.md#src-2610-36335 | 医学 QA；gold evidence 场景 | 工程建议 + E-03（已撤回） | H2 | 检索率低但 grounding 仍能补足 | 02 recipes/judgment |
| O-T06 | （已撤回）checker | 增量 catch <5pp、FA >15% → 停（先超空结果重试）；阈值随源停用 | meta/audits/2026-11-11-source-purge.md#src-2610-37809 | UniProt 真实答案；人工故障 | 工程建议 + E-02（已撤回） | H2 | 第二域显示 5pp/15% 不适用 | 02 recipes/judgment；01 data/e4 |
| O-T07 | （已撤回）动作闸 | 在 miss 预算下 false-block 前沿不可接受 → 停；不要用单点 5%；阈值随源停用 | meta/audits/2026-11-11-source-purge.md#src-2610-08082 | τ²-bench；blocked log 无标签 | E-04 + 2607.22868（均已移出） | H2 | 有标签数据使单点阈值可判定 | 02 recipes/constraint；01 data/e5 |
| O-T08 | 记忆 | merge precision <90% → 停 | deliverables/02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺 | 专有数据；文本 only | 工程建议 + E-05 | H2 | 第二域显示 90% 过高/过低 | 02 recipes/state；01 data/e6 |
| O-T09 | 读路径 | fail-open 未修 或 object 方向未测 → 停 | deliverables/02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺 | 单实现；SHACL-AF | E-20 / O-C03 / O-C02 | H3 | 第二实现证明 object 方向受控且异常路径 fail-closed | 02 recipes/constraint；01 data/e7-e8 |
| O-T10 | 落盘授权 | false-defer >20%、unresolved >10%、审计不可追 → 停 | deliverables/02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺 | 无实现；只有概念契约 | 工程建议 / gap | H2 | 有实现且 false-defer 可测 | 02 recipes/constraint |
| O-T11 | 离线 SHACL | 三态折叠 或 覆盖不明 → 停（必须能报 checked/passed/undetermined） | deliverables/02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺 | CI/离线；派生 shapes 未测 | E-20 / O-C12 | H3 | 派生 shapes 覆盖可测且三态不折叠 | 02 recipes/offline-and-obda |
| O-T12 | OBDA | 需要 DL 推理 或 事务写入 → 停 | deliverables/02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺 | ontop；OWL 2 QL | E-20 / O-C08 / O-C09 | H3 | OWL 2 QL 之外的重写被实现且可验收 | 02 recipes/offline-and-obda |
| O-T13 | 受监管供给 | citation 精度 <0.95 或 strict-pass 违规 >0 → 停 | deliverables/02-engineering-playbook/02-sections/05-acceptance.md#51-验收与-stop按机制选尺 | Grid 类；真实运营商未测 | 工程建议 + Grid signal | H2 | 客户侧显示 0.95 与 0 不可达 | 02 recipes/regulated |

## M · 矩阵（4）

| ID | claim | value | address | domain | provenance | 硬度 | falsifier | feeds |
|---|---|---|---|---|---|---|---|---|
| O-M01 | 覆盖率矩阵 | 七类失效 × 八位置；位置是专门化的，不能排成强度线，也不能合成百分比；行 ID `row-<失效类>` | deliverables/03-mechanism-reference/04-across-positions/01-coverage.md#3-矩阵 | H/D 分类设计；不是 E | 06-L15 + coverage | H3 | 同一失效在 >1 位置出现同等效应，专门化不成立 | 03 coverage；01 map |
| O-M02 | 执行形态矩阵 | 6 行（trustgraph/semantica/ontop/open-ontologies/OPA/Qlever）× 语义/失败模式；行 ID `row-<project>` | topics/execution-forms.md#代码级核对2026-11-09 | pin commits；只读代码 | E-20 | H3 | 两个项目在同一行为上语义相同，分类 collapse | 03 execution-forms；03 positions |
| O-M03 | 度量分派 | 八行：位置 → 主指标/过程指标/反事实/停；行 ID `row-<position>` | topics/06-measure/metrics/mechanism.md#按位置分派八行设计 | 设计，非测量 | 06-L13 + C-03 | H3 | 同一机制换尺子结论一致，错配不成立 | 02 §5.1；06 metrics |
| O-M04 | 机制类型 × 尺子 2×2 | 2 行（约束/知识供给）× 2 列（任务账/风险成本账）；逐格已核，方向翻转是跨来源综合；行 ID `row-<机制>` | deliverables/03-mechanism-reference/04-across-positions/03-measurement.md#25-机制类型与尺子分派 | 无同数据集两把尺子对照；C-03 的具体化 | 06-L16；C-03；E-01/E-08/E-12/E-14/E-15（E-04 已撤回，约束格现以 E-15 为锚） | H3 | 同数据集两把尺子结论一致，或某格证据被推翻 | 03 measurement；02 §5.1 |

## N · 数值（29）

| ID | claim | value | address | domain | provenance | 硬度 | falsifier | feeds |
|---|---|---|---|---|---|---|---|---|
| O-N01 | （已撤回）动作闸只在部分格改善 | 18 格 8 格改善；airline 六模型四个 +0.11–0.18；retail/强模型回退 | meta/audits/2026-11-11-source-purge.md | τ²-bench 3 域 × 6 模型；主实验 18 格 | E-04；POLAR Table 3 | H2 | 同轨迹配对后改善面显著扩大 | 01 map；02 recipes/constraint |
| O-N02 | （已撤回）阈值保留率按域差异极大 | τ=0.80：airline 36.6%、retail 100%、telecom 98.7% | meta/audits/2026-11-11-source-purge.md | 固定轨迹上的 logged decisions；不是 false-veto 率 | E-04；POLAR Table 4 | H2 | 换域复测得同一保留率，或漏标率使 36.6% 不可比 | 02 recipes/constraint；03 action |
| O-N03 | （已撤回）tier 消融 | qwen3-8B airline 150 runs/arm：full 0.080、no T3 0.073、T1+T3 0.087、T1-only 0.087、no irreversible 0.060 | meta/audits/2026-11-11-source-purge.md | 单模型/单域；CI 未全报 | E-04；POLAR Table 5 | H2 | 配对检验显示 T1-only 与 full 差异显著 | 01 data/e5；02 recipes/constraint |
| O-N04 | K1/K2 增益 | K0→K1 +54.6pp；K1→K2 +19.8pp；避坑率 0.605→0.802（OR 5.45） | src/papers/2610.11768-narrow-and-deep/digest.md#41-投影文本 | 单工厂/9 任务；答案基本写在文本里 | E-12；N&D §4.1 | H2 | 跨域复现显示 +5pp 不成立 | 01 map；02 recipes/knowledge |
| O-N05 | 投影形态排序有模型级反转 | pooled 0.777 文本 > 0.717 JSON > 0.638 查询 > 0.597 检索；GLM JSON 0.900 > 文本 0.891；Qwen 工具 0.407 < 检索 0.538 | src/papers/2610.11768-narrow-and-deep/digest.md#42-形式与接口 | 4 模型；工具为事后比较 | E-12；N&D §4.2 | H2 | 更多模型上文本—JSON 排序不翻转 | 02 recipes/knowledge；03 context |
| O-N06 | 容量反向未支持 | 9B 带投影 0.737 > 750B 不带 0.672；H2 单向 p=0.85（未支持，非证明无效应）；K4 0.644 vs K4x 0.645 | src/papers/2610.11768-narrow-and-deep/digest.md#41-投影文本 | 单 plant；区间约 0.3 宽 | E-12；N&D §4.1/§5 | H2 | 更大模型带投影仍显著劣于小模型 | 01 data；03 context |
| O-N07 | （已撤回）三源 catch/FA 各有偏向 | 真实答案（4,410 条，3,383 可检查）：curated 18.9/16.8、data-derived 8.2/3.5、masked LLM 5.0/1.8、空结果 2.5/0.1 | meta/audits/2026-11-11-source-purge.md | UniProt；单 benchmark | E-02；Catch Table 2 | H2 | 第二域显示 curated 不再略优于随机 | 01 data/e4；02 recipes/judgment |
| O-N08 | （已撤回）precision 依赖 25% 错答案假设 | curated 57.1、data 72.3、LLM masked 93.7、空结果 100（人工故障 + 25% 假设） | meta/audits/2026-11-11-source-purge.md | 人工故障；假设未在真实分布验证 | E-02；Catch Table 2 | H2 | 真实错答案比例偏离 25% 使 precision 排序翻转 | 02 recipes/judgment |
| O-N09 | （已撤回）空结果重试是很强基线 | 人工故障 catch 79.2%、FA 0%；真实答案 2.5%/0.1% | meta/audits/2026-11-11-source-purge.md | 人工故障 + 真实答案；两种口径 | E-02；Catch §3.6 | H2 | 第二域上空结果重试失效（catch 大幅下降） | 02 §5.3；01 data/e4 |
| O-N10 | 检索相当、会用更高 | Complete Retrieval 85.6% vs MemoryBank 86.4% | src/papers/2611.03743-evomemstate/digest.md#4-结果数字与条件 | 四基准；文本 only | E-17；EvoMem Table | H2 | 检索增益解释全部 accuracy 差 | 01 data/e6；04 memory |
| O-N11 | Acc@complete 提升 | 70.8%（+11.5）/ 68.5%（+31.2） | src/papers/2611.03743-evomemstate/digest.md#4-结果数字与条件 | 需要训练信号 | E-17；EvoMem §4 | H2 | 无训练部署下增益消失 | 01 data/e6；04 memory |
| O-N12 | 状态消融均有贡献 | MemSyco：−8.9 / −8.0 / −7.9；MemTrap：−6.4 / −15.0 / −16.4；跨 6 系统 +0.2–4.9 | src/papers/2611.03743-evomemstate/digest.md#4-结果数字与条件 | 文本；单模型族 | E-17；EvoMem §4 | H2 | 单组件消融无显著差 | 01 data/e6；04 memory |
| O-N13 | （已撤回）接地等级整体最优 | 平均 50.5% / 68.1%；Tests 1–2 +10–15pp | meta/audits/2026-11-11-source-purge.md | 三个大本体、六个医学 QA、2 backbone | E-03；OA-RAG §4.2 | H2 | 等级为自评、未校准，去掉等级后增益不变 | 01 map；02 recipes/judgment |
| O-N14 | （已撤回）同预算下 token 更少 | Test 3：84.9% vs 66.7%；9.7k vs 96.7k tokens/问 | meta/audits/2026-11-11-source-purge.md | 8k 预算；单 benchmark | E-03；OA-RAG §4.2 | H2 | 预算改变后优势消失 | 02 recipes/judgment |
| O-N15 | （已撤回）检索是主瓶颈 | gold evidence 完整检索率 MCQ 61.7% vs OQ 23.6% | meta/audits/2026-11-11-source-purge.md | 医学 QA；gold evidence 设置 | E-03；OA-RAG §4.4 | H2 | 检索率提高后 grounding 增益不变 | 02 §5.3；01 data/e4 |
| O-N16 | alias 的增量 | Full vs no-alias CMR +7.8–12.1pp（4 settings）；Full vs LLM-Norm 2.3–3.7× | src/papers/2610.40482-firme/digest.md#41-memory-usability | 专有数据；3 period | E-05；FIRME Table 3 | H2 | 无身份对齐对照组显示同等增益 | 01 data/e6；04 identity |
| O-N17 | human audit 与 merge precision | CMR +9.0–16.5pp；reattachment recall +22.5–29.0pp；merge precision 85.6–97.5% | src/papers/2610.40482-firme/digest.md#41-memory-usability | 200 units/setting；独立标注 | E-05；FIRME Table A2 | H2 | 另一批标注显示 precision <90% | 02 recipes/state |
| O-N18 | token 与语义匹配 | Full 6.20M vs no-alias 6.68M（−7.2%）；semantic matching token −40.3% | src/papers/2610.40482-firme/digest.md#41-memory-usability | investor/Opus/final period；不含 registry 构建 | E-05；FIRME Table 4 | H2 | 全周期计入后 token 反转 | 02 operations/cost |
| O-N19 | p_min 名义带与示例 | 名义 2.0%；Q=1,000/c=10 写 3.12%（按公式 3.08%）；miss ±1.5pp 使 band 0.4–3.6% | src/papers/2610.41172-context-as-infrastructure/digest.md#43-成本模型 | 冻结语料；论文门 | E-14；CAI §4.3 | H3 | 复算差无法用 rounded 解释 | 02 §5.1；01 data/e3 |
| O-N20 | 平均 −38% 是混合 | 43% hit × −91% + 57% miss × +1.9% = −38.0% | src/papers/2610.41172-context-as-infrastructure/digest.md#42-token-收益是条件性的 | FRAMES；p_h=43% 是反推 | E-08/E-14；CAI §4.2 | H3 | 实测 p_h 与 43% 差 >10pp 且平均收益翻转 | 01 data/e3；02 §5.1 |
| O-N21 | 时延约 3× | 3× 时延只在 7 道配对题上测（未编译臂另有 1 题失败） | src/papers/2610.41172-context-as-infrastructure/digest.md#42-token-收益是条件性的 | 7 题配对；p95 未报 | E-14；CAI §4.2/§8.5 | H2 | 更大样本显示时延 <3× 或长尾更差 | 02 operations/cost |
| O-N22 | 被测量的工件无准确率增益 | 摘要树/PageIndex/wiki/entity graph 在 FRAMES 上无可检出准确率增益；PageIndex 式大纲退化 | src/papers/2610.41172-context-as-infrastructure/digest.md#41-被测量的结构化工件没有准确率增益 | 单 benchmark；单 compiler/answer model | E-01；CAI §4.1 | H2 | 换 benchmark 后出现可检出增益 | 01 map；03 context |
| O-N23 | 限定条件 | 单基准 FRAMES、单 compiler/answer model、无 CI；ontology/timeline/mind map/session memory 为 not measured | src/papers/2610.41172-context-as-infrastructure/digest.md#41-被测量的结构化工件没有准确率增益 | 同上；Table 1 | E-01；CAI §4.1 | H2 | 原文表格显示这些工件被测量且有效 | 01 map；03 boundaries |
| O-N24 | 部署 ledger 为空 | 作者把本体价值放在部署层，但部署 ledger 无一行达预登记目标——作者主张，不是观测 | src/papers/2610.41172-context-as-infrastructure/digest.md#5-这些数字不能说明什么 | CAI Table 2；部署层 | E-01；CAI §5 | H2 | 出现达到预登记目标的部署行 | 01 boundaries；03 context |
| O-N25 | HSR 与审批 | HSR 14.75%→7.02%；审批 8.7% | src/papers/2610.36570-casel/digest.md#42-主结果 | 20 seeds/120k actions；模拟 | E-15；CASEL Table 2 | H2 | 部署实测与模拟差一个量级 | 01 map；02 recipes/constraint |
| O-N26 | 没有单一最优 | Consequence-Menu 4.38%/13.8%；Risk-Menu 5.82%/12.6%；Uncertainty 14.75%/6.9% | src/papers/2610.36570-casel/digest.md#42-主结果 | 模拟；主表 τ=∞ | E-15；CASEL Table 2 | H2 | 同 menu/cost 下出现唯一支配点 | 01 data/e5；03 coverage |
| O-N27 | full ledger 是低审批端点 | harm–compute 面被支配，但低审批端 4.3% approvals / 11.82% HSR 是前沿点；54% 直接执行步骤 p_t c_t > r̄_t | src/papers/2610.36570-casel/digest.md#42-主结果 | 模拟；γ 假设 | E-15；CASEL §4.2 | H2 | 「只对不可逆动作记账」被验证且前沿消失 | 02 recipes/constraint；06 feasibility |
| O-N28 | Glyph 的规模与标签空间 | ~3.4M 列 / ~98,000 表 / 4 业务线 / 3 后端；275 个叶标签（受治理内部本体，非公开词表） | src/papers/2609.10430-glyph/digest.md#41-规模本体与标签空间 | 单一组织（Apple）生产目录；平均 ~35 列/表（推测） | E-22；Glyph §4.1 | H2 | 跨企业复测显示规模/标签空间不可迁移 | 01 access-control；04 govern |
| O-N29 | 检索指标与融合增量 | NDCG@10 0.5497→0.9225；MAP@100 0.1888→0.9009；端到端 F2 0.890 vs 最强单策略 0.880（融合 +0.010） | src/papers/2609.10430-glyph/digest.md#42-编码器检索table-2-p6 | 列级留出、同分布；不是打标准确率 | E-22；Glyph §4.2/§4.3 | H2 | 换分布后 NDCG/MAP 提升不能复现 | 01 access-control；04 govern |

## R · 反例（12）

| ID | claim | value | address | domain | provenance | 硬度 | falsifier | feeds |
|---|---|---|---|---|---|---|---|---|
| O-R01 | 结构化上下文/本体能提准确率 | 被测工件（claim 树/RAPTOR/PageIndex/实体图/wiki）在 FRAMES 上 acc. neutral；ontology 行 `not measured`；N=200、p=91% 时两臂分辨率约 ±5.6pp | src/papers/2610.41172-context-as-infrastructure/digest.md#41-被测量的结构化工件没有准确率增益 | 强检索 harness；FRAMES；单 compiler/answer model；无 CI | E-01 | H2 | 换 benchmark 出现可检出增益，或配对 A/B 超过 δ | 01 boundaries；03 context |
| O-R02 | （已撤回）护栏必然提升任务表现 | 18 格仅 8 格改善；airline 六模型四个 +0.11–0.18；retail/强模型回退；T1-only≈blanket veto | meta/audits/2026-11-11-source-purge.md | τ²-bench；单 gate；reward 不是 harm 度量 | E-04 / Q-03 | H2 | 同轨迹配对后改善面显著扩大，或 harm 标签显示 net benefit | 01 §4.3；02 constraint |
| O-R03 | 深结构比薄语义层更值 | K0→K1 +54.6pp；K1→K2 +19.8pp；薄层约贡献 73% | src/papers/2610.11768-narrow-and-deep/digest.md#41-投影文本 | 单工厂；9 任务；答案基本写在文本里 | E-12 | H2 | 跨域深结构增益超过薄层 | 01 map；02 knowledge |
| O-R04 | 投影排序普适（文本 > JSON > 查询） | GLM JSON 0.900 > 文本 0.891；Qwen 工具 0.407 < 检索 0.538；pooled 0.777 只是平均 | src/papers/2610.11768-narrow-and-deep/digest.md#42-形式与接口 | 4 模型；工具为事后比较 | E-12 | H2 | 更多模型上文本—JSON 排序不翻转 | 02 knowledge；03 context |
| O-R05 | （已撤回）curated 本体更可靠 | curated precision 仅比随机高 1.6 点（CI 跨零）；真实答案 FA 16.8%；data-derived FA 3.5% | meta/audits/2026-11-11-source-purge.md | UniProt 4,410 条；单 benchmark；25% 假设 | E-02 | H2 | 第二域 curated 显著优于随机 | 01 data/e4；02 judgment |
| O-R06 | 有引擎就能拦 | trustgraph fail-open、只删 subject；open-ontologies 只做 CI/报告；semantica 校验时 inference=none；ontop 重写不是 gate | topics/execution-forms.md#代码级核对2026-11-09 | 4 项目 pin commit；只读代码 | E-20 | H2 | 第二实现 fail-closed 且有写授权 | 03 execution-forms；02 constraint |
| O-R07 | 有标签就能做访问控制 | 标签层（Glyph）/策略层（OPA 无领域本体）/执行层（trustgraph 单实现）不能互推；读路径过滤 ≠ 写授权 | topics/01-constraint/access-control/README.md#当前判断 | 单企业/单实现；无端到端验证 | E-22 | H2 | 端到端策略+执行验证 | 04 govern；01 access-control |
| O-R08 | 平均 −38% 可上线 | −38% = 43%×−91% + 57%×+1.9%；p_h=43% 是反推；时延 3× 只在 7 题上测 | src/papers/2610.41172-context-as-infrastructure/digest.md#42-token-收益是条件性的 | FRAMES；单语料；门实现未统一 | E-08 / E-14 | H2 | 实测 p_h 与 43% 差 >10pp 且平均收益翻转 | 02 §5.3；01 data/e3 |
| O-R09 | 审批越多越安全 | CASEL 8.7% approvals/7.02% HSR；Uncertainty 6.9%/14.75%；Risk 12.6%/5.82%；Consequence 13.8%/4.38% | src/papers/2610.36570-casel/digest.md#42-主结果 | 模拟；τ=∞ 主表；审批疲劳未建模 | E-15 | H2 | 审批疲劳建模后排序翻转 | 01 data/e5；06 feasibility |
| O-R10 | 不做身份对齐也能记忆 | no-alias CMR −7.8–12.1pp；LLM-Norm 2.3–3.7× 差；human audit +9.0–16.5pp | src/papers/2610.40482-firme/digest.md#41-memory-usability | 专有数据；3 period；无「完全不做对齐」对照 | E-05 | H2 | 无身份对照显示同等 CMR | 01 data/e6；04 identity |
| O-R11 | SLB 可靠提示词消除 | cautionary prompts 只减约 1/4；placeholders 减 SLB token 97% 而准确率 +2.6；85% traces/24% tokens | src/papers/2611.02395-solver-like-behavior/digest.md#41-slb-有多普遍 | 3 模型/4 CSP/2 FL；单次生成；闭源无 trace | E-09 | H2 | prompt 使 SLB 降至 <5% 且不损准确率 | 06 trace；02 evidence |
| O-R12 | （已撤回）reward 可证明护栏安全 | 单 gate/6 模型下 reward 不升反降；作者声明 reward 不是 harm 度量；无 harm 标签 | meta/audits/2026-11-11-source-purge.md | τ²-bench；单 benchmark | Q-03 / E-04 | H2 | harm 标签使 reward 与 harm 一致 | 01 constraint；06 metrics |

## P · 协议（6）

| ID | claim | value | address | domain | provenance | 硬度 | falsifier | feeds |
|---|---|---|---|---|---|---|---|---|
| O-P01 | p_h 标定（shadow） | 样本 1,600–2,000；臂 gate-on/off；指标 p_h CI/整臂准确率/p95/成本；判定 CI 下界 > p_min 且整臂非劣 δ；停 CI 下界 ≤ p_min | src/papers/2610.41172-context-as-infrastructure/digest.md#6-工程上怎么用 | FRAMES 类语料；预登记固定样本量 | E-14 / O-F01 / O-F06 | H2 | 预注册序贯设计或更大样本改变结论 | 02 evaluation；01 §5.2 |
| O-P02 | （已撤回）checker 评估 | 样本 200 题 + 空结果基线；指标增量 catch/FA/净修复/per-1k；判定 catch ≥5pp、FA ≤15%、净修复 >0；停基线胜出；阈值随源停用，协议设计可换锚复用 | meta/audits/2026-11-11-source-purge.md#src-2610-37809 | 单域；故障分布未定 | E-02 / O-T06（已撤回） | H2 | 第二域显示阈值不适用 | 02 §5.3；01 data/e4 |
| O-P03 | （已撤回）false-veto 标注 | 样本 100 条 blocked + 授权标签（AuthorizationPairs 80/80 映射）；指标 false-block/miss 前沿；判定按 miss 预算选点；停无标签；标注协议可换锚复用 | meta/audits/2026-11-11-source-purge.md#src-2610-08082 | POLAR blocked log；单 gate | E-04 / 2607.22868（均已移出） | H2 | 标签定义不可复现 | 01 data/e5；02 constraint |
| O-P04 | 记忆三层评估 | 样本 200 units/setting；指标 CMR/human audit/round-trip；判定 +10pp、merge precision ≥90%；停 precision <90% | src/papers/2610.40482-firme/digest.md#41-memory-usability | 专有数据；文本 only | E-05 / E-17 | H2 | 三层不可互替被打破 | 01 data/e6；04 memory |
| O-P05 | read-path 泄漏率 | 样本 第二实现 + object 方向用例；指标泄漏率/误拦/时延；判定泄漏 0 且 object 方向受控；停 fail-open 未修 | deliverables/01-capability-status/09-data/e7-e8-code.md#3-还缺什么 | 单实现现状；SHACL-AF | E-20 | H2 | 第二实现 fail-closed 且 object 受控 | 02 §5.3；01 data/e7-e8 |
| O-P06 | 受监管 citation/strict-pass | 样本 20–50 单；指标 citation 精度/strict-pass 违规/签核；判定 ≥0.95 且违规 0；停不可达 | deliverables/02-engineering-playbook/03-recipes/12-regulated.md#验收--停 | Grid 类；真实运营商未测 | 工程建议 + Grid signal | H2 | 客户侧显示 0.95/0 不可达 | 02 regulated；04 govern |

## 索引 · 按 E

> E-02/03/04 已撤回（源未过准入）；其下行是存档，对象除 O-M04（已换锚 E-15 等）外全部 withdrawn，不得引用。

| E | 对象数 | H3 | H2 | 对象 |
|---|---|---|---|---|
| E-01 | 6 | 2 | 4 | O-F09 O-M04 O-N22 O-N23 O-N24 O-R01 |
| E-02（withdrawn） | 7 | 1 | 6 | O-F08 O-T06 O-N07 O-N08 O-N09 O-R05 O-P02 |
| E-03（withdrawn） | 5 | 1 | 4 | O-F15 O-T05 O-N13 O-N14 O-N15 |
| E-04（withdrawn） | 9 | 2 | 7 | O-F10 O-T07 O-M04 O-N01 O-N02 O-N03 O-R02 O-R12 O-P03 |
| E-05 | 7 | 1 | 6 | O-F11 O-T08 O-N16 O-N17 O-N18 O-R10 O-P04 |
| E-08 | 4 | 3 | 1 | O-F07 O-M04 O-N20 O-R08 |
| E-09 | 1 | 0 | 1 | O-R11 |
| E-12 | 9 | 2 | 7 | O-F14 O-T02 O-T03 O-M04 O-N04 O-N05 O-N06 O-R03 O-R04 |
| E-14 | 11 | 7 | 4 | O-F01 O-F02 O-F06 O-F07 O-T04 O-M04 O-N19 O-N20 O-N21 O-R08 O-P01 |
| E-15 | 8 | 2 | 6 | O-F03 O-F04 O-F12 O-M04 O-N25 O-N26 O-N27 O-R09 |
| E-17 | 5 | 1 | 4 | O-F13 O-N10 O-N11 O-N12 O-P04 |
| E-20 | 19 | 17 | 2 | O-C01 O-C02 O-C03 O-C04 O-C05 O-C06 O-C07 O-C08 O-C09 O-C10 O-C11 O-C12 O-C13 O-T09 O-T11 O-T12 O-M02 O-R06 O-P05 |
| E-22 | 5 | 2 | 3 | O-C14 O-C15 O-N28 O-N29 O-R07 |

## 索引 · 按交付物

| 交付物 | 对象数 | H3 | 对象 |
|---|---|---|---|
| 01 现状 | 55 | 18 | O-C03 O-C14 O-C15 O-F01 O-F02 O-F06 O-F07 O-F08 O-F09 O-F11 O-F12 O-F13 O-F14 O-F15 O-T04 O-T06 O-T07 O-T08 O-T09 O-M01 O-N01 O-N03 O-N04 O-N06 O-N07 O-N09 O-N10 O-N11 O-N12 O-N13 O-N15 O-N16 O-N19 O-N20 O-N22 O-N23 O-N24 O-N25 O-N26 O-N28 O-N29 O-R01 O-R02 O-R03 O-R05 O-R07 O-R08 O-R09 O-R10 O-R12 O-P01 O-P02 O-P03 O-P04 O-P05 |
| 02 工程 | 59 | 18 | O-C08 O-C12 O-C13 O-F01 O-F02 O-F03 O-F04 O-F05 O-F06 O-F07 O-F08 O-F10 O-F14 O-F15 O-T01 O-T02 O-T03 O-T04 O-T05 O-T06 O-T07 O-T08 O-T09 O-T10 O-T11 O-T12 O-T13 O-M03 O-M04 O-N01 O-N02 O-N03 O-N04 O-N05 O-N07 O-N08 O-N09 O-N13 O-N14 O-N15 O-N17 O-N18 O-N19 O-N20 O-N21 O-N25 O-N27 O-R02 O-R03 O-R04 O-R05 O-R06 O-R08 O-R11 O-P01 O-P02 O-P03 O-P05 O-P06 |
| 03 机制 | 30 | 20 | O-C01 O-C02 O-C03 O-C04 O-C05 O-C06 O-C07 O-C08 O-C09 O-C10 O-C11 O-C12 O-C13 O-C14 O-C15 O-F09 O-F10 O-M01 O-M02 O-M04 O-N02 O-N05 O-N06 O-N22 O-N23 O-N24 O-N26 O-R01 O-R04 O-R06 |
| 04 落地 | 12 | 2 | O-F11 O-F13 O-N10 O-N11 O-N12 O-N16 O-N28 O-N29 O-R07 O-R10 O-P04 O-P06 |

## 索引 · 按类型

| 类型 | 数量 | H3 | 用途 |
|---|---|---|---|
| C | 15 | 15 | 代码锚（`file:symbol` + 行为 + 不保证什么） |
| F | 15 | 11 | 公式（inputs / 例 / 假设） |
| T | 13 | 4 | 停线（阈值 + 出处 + 量不出时） |
| M | 4 | 4 | 矩阵（行 ID + 每行出处） |
| N | 29 | 2 | 数值（数 + 域 + 表/节地址） |
| R | 12 | 0 | 反例（常见主张 + 已测反例 + 条件） |
| P | 6 | 0 | 协议（样本 / 臂 / 指标 / 判定 / 停） |

## 变更记录

- 2026-11-12 purge 对账：O-T05/T06/T07/P02/P03 五个停线/协议补标「已撤回」（唯一锚 E-02/E-03/E-04 已撤回，按本页「E 撤销则 O 撤销」规则）；累计 20 撤回、现存 74（H3 33 / H2 41）。O-M04 的锚去掉 E-04，约束格改以 E-15 为锚。阈值/协议设计本身可在换锚过门新源后复用；撤回对象不得被交付物引用。
- 2026-11-09 首轮：67 个对象入库（C15/F7/T13/M3/N29）；H3 27、H2 40。
- 2026-11-09 补完轮（R5）：加 F6（可复算）+ R12 + P6；累计 91 个对象（C15/F13/T13/M3/N29/R12/P6）；H3 33、H2 58。
- 2026-11-10 R6：加 F14/F15（E-12/E-03 的可复算量）+ M04（机制×尺子 2×2）；累计 94 个对象；H3 36、H2 58；E 级 H3 10/10。
- 2026-11-09：`O-F01` 复算暴露 digest §4.3 的例子「Q=1,000、c=10 → 3.12%」按公式是 3.08%（差 0.04pp）；`c`/`Q` 可能是 rounded。已写进对象与 [hard-objects-plan](../deliverables/_plans/2026-11-09-hard-objects-plan.md)。
- 2026-11-09：F03–F06 保持 H2（缺单价/γ 实测），不硬升；F08–F13 是可复算对象（E-01/E-02/E-04/E-05/E-15/E-17），全部标 `derived`。
- 2026-11-10：R6 后承重 E 的 H3 覆盖 10/10（F14 补 E-12、F15 补 E-03；均为 derived 算术/派生，不是新证据）。

