# 访问控制 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，缺口回 [frontier](./frontier.md)。
> **本页不把 Glyph 写成 SHACL-AF**：Glyph 的本体没有被求值，只当封闭标签空间、候选来源与 tier 权重。

## 总链

```
source / column
  → classification / label   (Glyph；停在这里)
  → policy                   (本派无来源)
  → post-filter              (trustgraph；读路径)
  → verdict / audit          (只有片段)
```

| 阶段 | 谁做 | 输入 | 输出 | 证据停在哪 |
|---|---|---|---|---|
| source / column | 企业数据目录 | metadata key、可选描述、生产该列的代码 | 列 | — |
| classification / label | Glyph | metadata key + 代码 | 多标签子集 `Y ⊆ O` + confidence + justification | **停在这里**：没有策略判定 |
| policy | **无来源** | — | — | 空白：无策略语言/冲突/默认/版本 |
| post-filter | trustgraph | 策略图 + `user_context` + 查询结果三元组 | 过滤后的三元组 | 独立策略图；不消费 Glyph 标签 |
| verdict / audit | trustgraph（事件）/ Glyph（标签 provenance） | 判定结果 | 策略事件、标签来源 | 无 join；无判定级审计 |

## 1. source / column

Glyph 的输入只有元数据：`catalog.database.table.column`（长类型截断到 200 字符）、可选的人工描述，以及生产该列的代码。**不读 cell value**——最敏感的表在分类完成前本来就不许读值，这是它的问题设定，不是实现偷懒。

列进入两个 agent：Descriptor 先造描述，Tagger 再打标签；两者可独立跑，但描述 tagger 依赖描述。

## 2. classification / label（Glyph）

### 2.1 Descriptor（描述）

- 企业 GitHub 代码搜索上的 active RAG：模型自己决定查什么，把描述落在**产出该列的应用代码**上。
- 按表批量，≤50 列/次；每列默认 3 次工具调用预算，批级封顶后强制收尾。
- LLM-as-Judge 按 plausibility / specificity / completeness / PII awareness 打分，低于阈值回炉，默认 ≤2 轮；judge 用与生成器不同的模型家族。
- 失败模式：代码搜不到时退化为「按列名猜」；论文没报 RAG 失败率。

### 2.2 Tagger（三路）

| 策略 | 输入 | 怎么出标签 | 停在哪 |
|---|---|---|---|
| description tagger | `"{name}: {description}"` | stock MiniLM 检索本体 annotation 定义，LLM 从候选里选并排序 | 只覆盖**有描述**的列 |
| LOB regex tagger | 列名 | 专家按业务线手写规则，命中即固定标签 | 规则外几乎不发火；只覆盖手写模式 |
| metadata tagger | metadata key | 微调 6 层 MiniLM → flat 内积索引 → 相似历史指派作候选 → LLM 重排 | 依赖「已验证的历史指派」；新标签冷启动没有邻居 |

三路的设计意图是失败模式不相关。实际端到端单跑：metadata **0.880**（F2，最强）、description **0.238**、regex **0.050**；所以后两路更像融合输入，不是可单独部署的标注器。

### 2.3 融合与 tier 重排

```
rrf(t) = Σ_{i ∈ 含 t 的活跃列表} 1 / (k + r_i)      k = 60，r_i 从 1 起
归一化分母 = n_active / (k + 1)                     # 全部来源都排 #1 时的理论最大值
```

- 三路分数不可比（ANN cosine、LLM 置信度、二值规则），所以只融合名次，不校准分数。
- 同一标签被多路提名时，按固定优先级继承其中一路的 provenance（reasoning / ontology / grades），置信度用跨源 RRF 分；去重按 annotation 名，排序用 annotation 名做确定性 tie-break。
- 最后按 sensitivity tier 重排：`α·c + (1−α)·w`，`c` 是 RRF 置信度，`w` 是本体 tier 权重——untiered 与更高敏感 = 1.0，更低敏感的第 2/3/4 级 = 0.75 / 0.5 / 0.25；低于最低归一化分的标签直接丢弃。`α` 未报告。
- 输出：每列一个本体子集 `Y ⊆ O`，每个标签带 confidence 与 justification（per-tag provenance）。

### 2.4 停在哪

Glyph 停在 **label**：不产出 allow/deny，不签发 subject/resource attribute，不把 275 个叶节点映射成策略，也不执行访问控制。它没有 SHACL/OWL 求值、没有查询重写、没有一致性校验；本体只做三件事——封闭标签空间、候选来源、tier 权重。

## 3. policy（本派无来源）

这一层是空白，必须说清空在哪：

- **谁写策略**：本派没有来源。trustgraph 的策略图 `urn:graph:policy` 是外部写入的 SHACL-AF NodeShape，但谁授权、怎么评审、怎么发布，不在两个来源里。
- **冲突/优先级**：唯一可见的是 `sh:order` 升序、首命中即停（执行顺序），这不是冲突消解语义；Glyph 的 sensitivity tier 是标签重排权重，也不是策略优先级。
- **默认 allow/deny**：没有来源。
- **标签 → 策略属性**：没有接口。Glyph 的 275 个 annotation 与 tier 不会自动变成策略里的 subject/resource 属性；由谁签发、怎么版本化，未定义。
- **策略版本/回滚**：没有来源。

所以机制链在这里断开：标签层产出标签，执行层消费一份**独立编写**的策略图，中间没有「标签→策略」的翻译层。

## 4. post-filter（trustgraph）

它在查询结果返回前工作，属于**读路径**：

1. `TriplesQueryRequest` 可带 `user_context`；服务先看策略图里有没有 `sh:NodeShape`（service 级缓存 60s）。
2. 有策略 + 无 `user_context` → 返回 policy-enforcement-error；无策略 → 原样转发（open mode）。
3. 有策略 + 有 context → 后端流式返回三元组，逐批过滤：
   - 候选 IRI = 本批三元组的 subject ∪ object；
   - 按策略 SELECT 里「从 `?this` 可达」的谓词逐条 hydrate；
   - 每个候选节点按 `sh:order` 依次求值：`sh:SPARQLTarget`(SELECT) 命中 → `sh:SPARQLRule`(CONSTRUCT) → 解析 `sh:resultSeverity` / `sh:resultMessage` / `tg-pol:blocks`；
   - 第一个命中策略生效；blocked 节点从结果中剔除；
   - `PolicyEventPublisher` 发策略事件。
4. 过滤后的批次才回到 agent 上下文。

**执行点**：后端已经取回数据，过滤器在服务层做结果变换；它不是存储级 ACL，也不是动作前 gate。错误路径与方向性边界见 [commit-gate F5–F7](../commit-gate/findings.md)，本页不复述。

**不消费 Glyph 标签**：策略图独立存在，没有从 Glyph 的标签/本体自动生成策略的路径；两个来源之间没有 join key。

## 5. verdict / audit

- trustgraph：有 `sh:resultSeverity` / `sh:resultMessage` / policy event；没有判定日志 schema、保留策略、策略版本绑定，也没有「为什么允许」的记录（只记录被 block 的节点事件）。
- Glyph：per-tag provenance 记录「哪路来源、多少分、什么理由」；这是**标签级**审计，不是访问判定级审计。
- 缺口：没有一条记录能回答「列 C 在策略 P 的 vN 下、依据标签 L 的 vM，为什么对用户 U 可见」。这是 [frontier G2](./frontier.md)。

## 常见误读

- **「Glyph 用了本体，所以本体被执行」**：错。Glyph 的本体没有被求值；它只做标签空间、候选检索与 tier 权重。`engine` 形态见 [E-20](../../conclusions.md) 与 [execution-forms](../../execution-forms.md)。
- **「NDCG 0.92 = 打标准确率 92%」**：错。那是同一编码器微调前后的检索指标，列级留出、同分布上界、未控表内泄漏；Table 2 caption 明说不是 tagging metrics。
- **「trustgraph 过滤 = 写授权」**：错。它拦的是查询结果，不是落盘变更；写路径见 [commit-gate](../commit-gate/README.md)。
- **「有策略过滤 = 策略正确」**：错。策略冲突、默认 allow/deny、版本与标签映射都没有来源。

## 接缝

- [E-20](../../conclusions.md)：`engine` 包含 SHACL-AF 策略求值；本页只取 trustgraph 的**读路径**那一支，不把 `engine` 当强度刻度。
- [commit-gate F5–F7](../commit-gate/findings.md)：读路径实现与错误路径/方向性边界；本页只接「执行层存在」，不重复其失败模式。
- [action-gate](../action-gate/README.md)：动作前可逆性；与读路径不是同一时刻。
