# 访问控制 · 发现（F）

> 只放已经能站住的判断。`F` 编号是子主题局部编号；跨页引用写 `access-control/Fx`。
> 本页只写标签/策略/执行三层。错误路径与对象方向的细节在 [commit-gate F5–F7](../commit-gate/findings.md)，不在此复述。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 标签/分类层是权限的输入，不是执行：Glyph 能大规模产标签，但不产策略判定、不执行访问控制 | `已核`（一手正文；生产部署为作者报告）/ `推测`（跨企业） |
| F2 | 执行层另有其物：trustgraph 的 SHACL-AF post-filter 只做读路径过滤，单实现 | `已核`（代码） |
| F3 | 标签 ≠ 策略 ≠ 执行：策略层在本派没有来源 | `推测`（综合） |

## 怎么读

- 想看机制：去 [mechanism.md](./mechanism.md)。
- 想看还缺什么/下一步：去 [frontier.md](./frontier.md)。
- 想看错误路径/方向性的代码细节：去 [commit-gate F5–F7](../commit-gate/findings.md)。
- 想看原始材料：去 [Glyph digest](../../../src/papers/2609.10430-glyph/digest.md) 与 [trustgraph digest](../../../src/open-source/trustgraph-ai-trustgraph/digest.md)。

## F1 · 标签/分类层是权限的输入，不是执行

- **判断**：Glyph 做的是列级敏感性标签/分类，不是访问控制。它不产出 allow/deny，不执行过滤，也不把标签签发成策略属性；「有标签」到「有权」之间缺一段接口。
- **数字与条件**：
  - 规模与本体：单一组织（Apple）生产目录，~3.4M 列 / ~98,000 表 / 4 条业务线 / 3 种后端（Iceberg、RDBMS、Cassandra）；标签空间是内部 **275-leaf** Data Classification Ontology；~72% 列是 `NON_SENSITIVE`。输入只用 metadata key `catalog.database.table.column`（+ 可选描述）与生产该列的代码，**不读 cell value**（§1、§4.1）。
  - 机制：description / LOB regex / metadata 三路并行；metadata 路由 6 层 all-MiniLM-L6-v2 在「已验证的历史指派」上微调（70,948 对，每标签 ≤3,000），flat 内积索引 + LLM 重排；三路用 **RRF(k=60)** 融合，再按 sensitivity tier 做 `α·c+(1−α)·w` 重排；每标签带 source/score/reasoning（§3–§4.3）。
  - 检索数字（Table 2）：NDCG@10 **0.5497→0.9225**、MAP@100 **0.1888→0.9009**、MRR@10 0.7875→0.9469、Acc@1 0.7138→0.9229。条件是**同一个 stock all-MiniLM-L6-v2 的微调前后**、9,242 条 query / 83,229 条 corpus、每标签 10% 列级留出；作者自认**同分布上界、未控表内泄漏**；Table 2 caption 明说这是 retrieval, not tagging metrics。**不是打标准确率，也不是对公开基线的提升**。
  - 端到端（Table 3）：curated 集 micro-F2 **0.890**（G1 0.878 / G2 0.961 / G3 0.938），最强单策略 metadata-only **0.880**；fusion F1 0.897 vs metadata-only 0.912。RRF 的端到端增益只有 **+0.010 F2 / −0.015 F1**。条件：1,905 张评估表与 15,205 张表的向量索引表级不相交；Claude Sonnet 4.5；无 P/R、无每组样本量、无 CI、单次运行。
  - 生产接受率（Fig. 2）：6 周、~24,000 条 steward 判定，**63.3%→99.8%**。作者自称 association 不是因果；这是 **precision-like、对 FN 盲**的接受率，不是漏标率、未标注率或授权正确性。
- **边界**：
  - 没有策略引擎、ACL/ABAC、执行点、拒绝率；「needed for access control」只是动机句。
  - 单企业、内部本体与代码不公开；无公开基准、无 OOD；跨企业/跨目录一律 `推测`。
  - 未标注/未覆盖列的下游处置未报告；不能把「标签可大规模产出」读成「敏感列都被覆盖」。
- **来源**：[Glyph digest](../../../src/papers/2609.10430-glyph/digest.md) §1–§5、§8；arXiv:2609.10430v1；[card](../../../src/papers/2609.10430-glyph/card.md) 只作 provenance。
- **等级**：`已核`（机制与数字，一手正文；生产部署为作者报告）/ `推测`（跨企业、标签→策略映射）。

## F2 · 执行层另有其物

- **判断**：访问控制的执行不在 Glyph 里。trustgraph 在查询结果返回前，用 SHACL-AF 策略按 `user_context` 对节点求值，命中 `tg-pol:blocks=true` 的节点从结果中剔除；这是**读路径结果过滤**，不是动作前 gate，也不是写路径 commit gate。
- **实现与条件**：
  - 开源项目 `trustgraph-ai/trustgraph`，Apache-2.0，pin `184f6228e9eb`；策略图 `urn:graph:policy`，`sh:NodeShape` + `sh:SPARQLTarget`(SELECT) + `sh:SPARQLRule`(CONSTRUCT) + `sh:order` + `tg-pol:blocks`；服务入口 `policy/triples/service.py`，过滤器 `policy/policy_filter.py`。
  - 部署契约：有策略时才要求请求带 `user_context`；策略 flow 是可选组件，digest 未证明默认配置会启用它。
  - 证据：digest §5 记录 31 条单测；本次只读代码核对，未重跑。没有生产泄漏率、误拦率、延迟/吞吐数据。
- **边界**：
  - `read-path` 目前目前有 3 个执行点、但没有合格第二实现（粒度不同/无 harness 集成/无独立泄漏率）（[E-20](../../conclusions.md)）；不能外推为「访问控制可执行」的一般结论。
  - 错误路径与方向性边界已由 [commit-gate F5–F7](../commit-gate/findings.md) 记录，本页不复述；本页只把它当「执行层存在」的证据。
  - 它不消费 Glyph 的标签：策略图独立编写，两者没有 label→policy 接口。不能拿 trustgraph 证明 Glyph 标签被正确执行，也不能拿 Glyph 证明 trustgraph 策略正确。
  - 不证明写授权：拦截的是「看到什么」，不是「写什么」。
- **来源**：[trustgraph digest](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) §2–§6；代码 `policy/policy_filter.py`、`policy/triples/service.py`；[card](../../../src/open-source/trustgraph-ai-trustgraph/card.md) 只作 provenance。
- **等级**：`已核`（代码；31 条单测见 digest §5，未重跑）。

## F3 · 标签 ≠ 策略 ≠ 执行

- **判断**：三层必须分开：标签/分类回答「这列是什么、算哪类敏感」；策略回答「谁在什么条件下 allow/deny」；执行回答「在哪拦、拦不住怎么办」。本派只有第一层与第三层的来源；**第二层没有 ontology/KG 领域来源**，只有通用策略引擎 OPA（adjunct）候选。
- **三层对照**：

| 层 | 本派来源 | 它证明了什么 | 它不能证明什么 |
|---|---|---|---|
| 标签/分类 | Glyph | 大规模列级标签可工程化；per-tag provenance | 漏标率、跨企业、标签→策略映射 |
| 策略 | **无领域来源**；OPA（adjunct）候选 | — | 策略语言、冲突/优先级、默认 allow/deny、版本/审计 |
| 执行 | trustgraph | 读路径可按 SHACL-AF 策略删结果 | 健全性、写授权、生产效果、对象方向 |

- **为什么是 `推测`**：这是两个来源的分层对照，不是新实验；「策略层没有领域来源」是本仓库 01 的来源缺口，不是「世界上没有实现」；OPA 只是通用策略引擎候选，不解析 OWL/SHACL、不消费 Glyph 标签。
- **可证伪**：找到任一来源，能把标签映射成 subject/resource 属性、给出冲突消解与默认策略、并记录判定依据与策略版本，F3 就后退。
- **边界**：Glyph 的 NDCG/F2 是标签/检索质量，不是策略正确性；trustgraph 的过滤是 best-effort 执行（错误路径与方向性见 commit-gate F5–F7），不是策略正确性证明。把两者相加仍不等于端到端访问控制。
- **来源**：[Glyph digest](../../../src/papers/2609.10430-glyph/digest.md) §8；[trustgraph digest](../../../src/open-source/trustgraph-ai-trustgraph/digest.md) §4/§6；[E-20](../../conclusions.md)；[commit-gate F5–F7](../commit-gate/findings.md)。
- **等级**：`推测`（综合；分层对照，非新实验）。

## 候选跨派结论（仅提议，未写入 conclusions）

> **候选 E（编号待父 agent 在 `topics/conclusions.md` 定稿）**：访问控制至少分三层——标签/分类有生产级来源（Glyph，`已核` 一手）、策略层没有来源、执行层只有单实现读路径过滤（trustgraph，`已核` 代码）；因此「有敏感标签」不能推出「有策略」或「执行正确」。限定：Glyph 单企业/标签层，trustgraph 单实现/只读代码；无跨企业、无漏标率、无策略语言来源、无生产效果。等级：`推测`（综合）。
>
> 编号待父 agent 在 [`topics/conclusions.md`](../../conclusions.md) 定稿；本页只提议，不把它当已定义结论引用。
