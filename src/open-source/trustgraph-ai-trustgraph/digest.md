---
status: draft
updated: 2026-11-09
quality: B
based_on: card.md
commit: 184f6228e9ebfa0e54f87e0e66f190549dfbd162
claims: [01-L13]
---

# trustgraph：本体在真实 agent 平台里以「读路径策略过滤 + 抽取 schema」被执行

> **自包含**：不假设读者读过 README、card 或论文。代码位置写到 `文件:符号`，不贴大段代码。
> **证据等级**（四档）：
> - `已核`：读过代码，能指到文件/函数；或读过一手文档原文。
> - `已证`：不仅跑通，且能用 `EXP-xxx` 在本仓库外复现；**跑通单测不等于机制有效**。
> - `推测`：只读 README/文档/issue，没有代码定位。
> - `存疑`：README 与代码/issue 冲突，或核心闭源。
> `reading: 已读代码` 指读到哪；与证据等级是两件事。

## 0. 三句话

1. **它是什么**：TrustGraph 是一个面向 agent 的数据/治理平台，仓库是多个 flow 服务组成的 monorepo；本体在这个系统里有两种形态——抽取用的类/属性 schema，和策略图（`urn:graph:policy`）里的 SHACL-AF NodeShape。
2. **本体怎么被用**：**执行**。查询结果返回前，`PolicyFilter` 会按用户上下文逐个节点求值 SHACL-AF 策略，命中 `tg-pol:blocks=true` 的节点，其三元组被剔除；这是读路径的授权过滤，不是动作前 gate。
3. **证据到哪**：代码调用链已通读、`tests/unit/test_policy` 31 条单测独立跑过（`已核`）；没有生产泄漏/性能数据，错误路径没有测试（`推测`/`存疑` 见 §6）。

## 1. 项目与维护状态

- 仓库：`trustgraph-ai/trustgraph`，Apache-2.0，本次 pin `184f6228e9eb`。
- 规模：30 贡献者、1,603 commits、28 个月（2024-07 起）；2026-11-08 仍在推送。
- 结构：`trustgraph-flow/` 是 flow 服务集合（抽取、查询、策略、agent 等），`trustgraph-base/` 是 schema 与运行时基座，`containers/` 是部署。
- 与本研究的关系：它不是「论文的实现」，而是一个**产品化的 agent 数据平面**；价值在于看「本体/策略在真实系统里落在哪一步」。

## 2. 本体在哪

两处，别混：

| 形态 | 位置 | 格式 | 谁加载 | 用途 |
|---|---|---|---|---|
| **抽取 schema** | 规格 `specs/ontology/trustgraph.ttl`；运行时由配置服务下发 | OWL/Turtle（规格）；`OntologyClass`/`OntologyProperty` 结构（运行时） | `extract/kg/ontology/ontology_loader.py: OntologyLoader` | 给抽取选类（`ontology_selector.py`）、归一化、转三元组 |
| **策略** | 命名图 `urn:graph:policy` | SHACL-AF：`sh:NodeShape` + `sh:SPARQLTarget`(SELECT) + `sh:SPARQLRule`(CONSTRUCT) + `sh:order` + `tg-pol:blocks` | `policy/policy_filter.py: PolicyFilter.load_policies` | 查询结果返回前，按用户上下文判定节点是否可见 |

**关键区分**：仓库里的 `trustgraph.ttl` 是**词表规格**，不是运行时直接解析的文件；运行时本体来自配置服务。策略不是 OWL 推理，是 SHACL-AF 的 SPARQL 求值。

## 3. 调用链

```
TriplesQueryRequest（可带 user_context）
 → policy/triples/service.py: Processor.on_message
   → _needs_policy：数 urn:graph:policy 里的 sh:NodeShape（service 级缓存 60s）
       ├ 有策略 + 无 user_context → 返回 policy-enforcement-error（服务级 fail-closed）
       ├ 无策略 → _passthrough（原样转发，open mode）
       └ 有策略 + 有 context → _filtered_query
            → 后端 triples 流式返回，逐批 PolicyFilter.apply(triples, collection, user_context)
                → 候选 IRIs = 本批三元组的 subject ∪ object
                → _hydrate_node：按策略 SELECT 里「从 ?this 可达」的谓词逐条取数（并发）
                → _build_context_graph：UserContext → rdflib triples
                → 每个候选节点按 sh:order 依次：
                     _run_sparql_target（SELECT ?this，命中即该策略适用）
                     → _run_sparql_rule（CONSTRUCT ValidationResult）
                     → 解析 sh:resultSeverity / sh:resultMessage / tg-pol:blocks
                     → 第一个命中策略生效（break）
                → blocked 节点：剔除其作为 **subject** 的三元组
            → 过滤后的批次回送；PolicyEventPublisher 发策略事件
```

关键实现细节（都能指到代码）：

- **判定单位是节点**（IRI），不是三元组。一个节点被 block，只删它以 subject 出现的三元组；**以它为 object 的三元组不删**（`_triple_blocked` 只检查 `triple.s`）。这是一个可验证的边界行为。
- **首个命中策略生效**：策略按 `sh:order` 升序，`_evaluate_node` 命中 target + rule 后 `break`；后面的策略不再看。
- **三处缓存**：查询结果 30s（`QueryCache`）、编译后的 SPARQL 64 条（`SparqlCache`）、节点判定 60s（`NodeDeterminationCache`，key 含 user context 哈希）。
- **hydrate 的规模**：每个候选节点 × 每个「从 ?this 可达的谓词」一次查询；谓词由 SPARQL 代数遍历得到（支持多跳、OPTIONAL/UNION）。
- **失败路径**：见 §6——target 抛异常 → 当作不命中；rule 抛异常 → 无判定；缺 `sh:select`/`sh:construct` → 跳过该策略；无策略 → 全量返回。**整体是 fail-open**；只有「有策略但没传 user_context」是 fail-closed。
- **2026-11-09 代码核对（pin `184f622`）**：`policy_filter.py` 的 `apply`、`_triple_blocked`（只查 `triple.s`）与异常返回 False/None 与上文一致；`tests/unit/test_policy/test_policy_filter.py` 有 31 条测试（存在，未重跑）。

## 4. 接缝判定

按 [seams](../../../topics/seams.md) 的三条件：

| 条件 | 是否成立 | 证据 |
|---|---|---|
| 有外部判据（来自本体，不是模型自评） | **成立** | SHACL-AF NodeShape + user_context；判定由 SPARQL 求值，不看模型说法 |
| 有阻断能力（违反可改变走向） | **部分成立** | 命中 `tg-pol:blocks=true` 的节点，其 subject 三元组不返回；object 方向不删 |
| 位置明确（能指到回路某一时刻） | **成立，但不在六时刻里** | 位置是「查询结果返回前」，介于图存储与 agent 上下文之间 |

**结论**：它算一个**读路径授权闸门**，但**不是**六时刻中的 action-gate / evidence / checker / commit-gate / memory / determinism。硬要类比，最接近 checker（输出后判定），但对象是检索结果而不是模型产出。这暴露了时刻轴的一个缺口：**检索返回前**没有独立时刻（见 §10 的 G）。

## 5. 证据与最小复现

- 单测：`tests/unit/test_policy/test_policy_filter.py`，31 条，覆盖判定/非阻断直通/回调/无策略直通/缓存/并发。
- 运行记录（C2）：仓库自带 pytest 会加载 `tests/conftest.py`，它 patch `trustgraph.base`（需要 pulsar-client 等重依赖），因此在 `/tmp` 合并 `trustgraph-base` 与 `trustgraph-flow` 的 `trustgraph/` 目录树后，把测试模块拷出单独跑：`31 passed in 0.13s`（rdflib 7.6.0，Python 3.13）。
- 策略样例：`docs/tech-specs/policy-test-data/aerosentinel-policies.ttl` 是完整可读的策略（信息屏障 + 范围过滤 + 角色过滤），可作为「真实策略长什么样」的样本。
- 设计文档：`docs/tech-specs/policy-filtering.md` 说明 enforcement mode（有策略才要求 user_context）与 SHACL-AF 的选型理由。
- **quality: B 的理由**：有 31 条单测 + 一份完整策略样例 + 代码级调用链；但没有生产/基准数据，错误路径无测试。按「B = 有测试但单路径」定级。

## 6. 不能证明什么

1. **不能证明生产上减少了泄漏**：没有泄漏率、误拦率、审批成本任何测量；单测只证明代码按预期跑。
2. **不能证明错误路径安全**：target/rule 异常一律 fail-open；没有针对异常的测试。对手方可以构造坏策略/坏 SPARQL 让过滤静默失效。
3. **不能证明对象方向也受控**：只删 subject 侧三元组；如果敏感信息以 object 出现（如「某人 → 属于 → 敏感部门」），它仍可能返回。
4. **不能证明它拦的是 agent 的动作**：它拦的是「检索结果」，不是工具调用/落盘；与 commit gate、action-gate 不是同一时刻。
5. **不能证明策略是默认开启**：grep 不到默认容器/flow 配置引用 `triples-policy`；它是可选 flow，需要部署方显式切换。
6. **不能证明 SHACL-AF 完整**：只实现 `sh:target`(SELECT) + `sh:rule`(CONSTRUCT) + `sh:order` + 结果三字段，不是完整 SHACL 校验器（没有 shapes 组合、没有 `sh:message` 之外的结果结构）。
7. **不能证明性能**：没有延迟/吞吐数据；hydrate 的查询数随候选节点 × 谓词数增长，只有缓存兜底。
8. **不能把 README 的「AI governance」当效果**：这是产品定位，不是测量结论。

## 7. 与论文 digest 对照

| digest | 论文机制 | 代码里对应 | 缺什么 / 差异 |
|---|---|---|---|
| [Commit Boundary](../../../meta/audits/2026-11-11-source-purge.md#src-2610-37407) | 可推理 ≠ 可授权；授权判据应显式、绑定 scope/version，落盘前校验 | **有真实实现，但在读路径**：独立的策略层 + user_context + SHACL-AF 判定，不把模型推断当授权 | 写路径的 commit gate 仍无实现（Commit Boundary 的 F4 不变）；没有 `P_auth` 的 promotion/scope 语义，也没有 false-defer 测量 |
| [POLAR](../../../meta/audits/2026-11-11-source-purge.md#src-2610-08082) | 动作执行前按可逆性剪枝 | 形态不同：先让数据返回，再按策略删节点；不剪动作 | 位置不同（读路径 vs 动作前）；没有可逆性、没有 harm 度量 |
| [CASEL](../../../src/papers/2610.36570-casel/digest.md) | 护栏要报 harm–approval–cost 前沿 | 没有审批环节；只有可见/不可见 | 没有审批成本、没有 harm 度量，不能与 CASEL 的数字直接比 |

**一句话**：它支持「授权判据可以与推理分离」这个原则（Commit Boundary 的 L13），但把实现位置放在读路径；因此不能用来证明 commit gate 可落地。

## 8. 工程含义

要借鉴的话：

- **接口**：查询请求里带 `user_context`；有策略时缺它直接报错。这是「策略存在即强制」的部署契约。
- **数据**：策略是 RDF（SHACL-AF）；用户上下文是结构化 dataclass（roles/assignments/entitlements/override/delegation），可映射到大多数 IAM。
- **成本**：每批结果 × 每节点 × 每可达谓词一次图查询；缓存 TTL 30–60s。候选节点多、谓词多时，成本不可忽略。
- **失败模式**：fail-open（SPARQL 异常/缺字段）、只删 subject、首命中即停、策略热更新有 60s 窗口。
- **什么时候别用**：需要写路径授权、需要对象方向也受控、需要审计级「为什么允许」时，这个实现不够；它适合「读侧可见性」这一层。

## 9. 代码地图

见同目录 [`code-map.md`](./code-map.md)：入口、本体相关文件、调用链、运行记录、未定位项。

## 10. 下一步

- **G（frontier）**：六时刻是否漏了「检索返回前」这一格？需要第二个实现（如 Semantica / Open Ontologies）对照，再决定是否改 `topics/seams.md`。
- **验证 fail-open**：构造一个抛异常的 policy target，确认请求仍返回数据；这会把「错误路径安全」从 `推测` 变 `已核`（负结果）。
- **对象方向**：构造一个 blocked 节点作为 object 的三元组，确认是否泄漏。
- **回 topics**：`01/commit-gate` 加 F5（读路径授权有实现、写路径无）；`01-L13` 的备注收窄；`01/frontier` 的 G1 加证据。
