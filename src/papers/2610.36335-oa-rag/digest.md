---
status: draft
updated: 2026-11-07
quality: A
based_on: card.md
claims: [E-03]
---

# OA-RAG · 消化

> 事实、数字、页码回 [card.md](./card.md)。这里只写**我们怎么用**、值不值得、哪里会坏。

## 工程思路

**要让 agent「用本体回答并交代证据」，按这个顺序：**

1. **先做 concept card。** 把每个类转成固定字段的文本卡（name / definition / parents / children / stated relations / annotations）。**agent 实际读的是卡，不是 OWL**；卡的质量决定检索与 grounding。
2. **三阶段分开：先想、再查、最后只依据证据回答。** Pre-tool reasoning 让模型暴露参数知识；ReAct loop 用 SPARQL 补证据；answering 阶段过滤失败观察，只从 evidence digest 作答。
3. **给 agent 三种查询原语。** `DESCRIBE` 看概念卡；`ASK` 问 reasoner 是否 entailed；`SELECT` 找候选。**Not Entailed ≠ false**，prompt 必须写明开放世界。
4. **空结果要 fallback。** 精确 SELECT 空结果时，BM25 取 top-k concept cards；否则 open-world 下会误判「不存在」。
5. **名字链接要能修。** 精确匹配失败 → 5 个候选 → agent 改 query；不要让一个拼写错误变成空结果。
6. **答案必须带证据 + grounding level。** 四个 level 是「证据支持强度」的粗分；不要把它当形式保证。
7. **单独量检索。** 把 gold evidence 是否被检索到、是否被引用分开；否则会把「检索不到」误判成「推理不行」。
8. **按 context 预算比较。** 与长上下文 RAG 比，要在同一 8k/32k/262k 预算下比；否则 token 效率的优势会被掩盖。
9. **保留 answering step。** 它不是装饰：去掉后平均掉 2.9–5.8 点。

## 实用意义

它解决的操作问题：

- **「医学 QA 的答案看起来对，但不知道依据哪条本体。」** → 每个答案报告观察 + grounding level。
- **「RAG 检索到一堆文本，模型自由发挥。」** → 本体 concept cards + reasoner + 证据 digest。
- **「长上下文 RAG 很贵。」** → Test 3 上 OA-RAG 9.7k tokens/问 vs i-MedRAG 96.7k；同等 8k 预算下 84.9% vs 66.7%。
- **「本体只当检索源，形式推理没用上。」** → ASK 让 reasoner 判定 entailment；DESCRIBE/SELECT 取注释与关系。
- **「不知道是检索错还是推理错。」** → 分开量 gold evidence 检索率与引用率；本文发现检索是主瓶颈。
- **「答案的 grounding level 能不能当可靠性信号？」** → 可以作弱信号；entailed/supported 正确率更高，但未校准。

**何时用**：有大规模 OWL 本体；问题需要概念定义/分类/关系；需要证据可追溯；context 预算有限。

**何时别用**：问题超出本体覆盖；没有 reasoner/SPARQL endpoint；需要形式正确性保证；多本体协调复杂；答案主要是文本阅读/计算。

## 质量评估

- **证据类型**：实证·基准（`已核`，一手正文）。
- **样本与对照**：3 个本体；Test 1 1,500 题、Test 2 1,477 题、Test 3 6,781 题；2 backbone；OntoTune/TaxoLLaMA + 5 类 RAG/agent 基线；ablation；8k context 统一。
- **优点**：三类推理模式覆盖广；本体形式+注释都用了；证据/grounding 报告；token 效率；ablation 清楚。
- **主要威胁**：grounding level 是模型自评，未校准；Test 3 与长上下文基线比较受预算影响；Test 2 OQ 仍差；三个本体都是生物医学；没有真实临床部署。
- **`quality: A` 理由**：多本体、多任务、多基线、ablation、token 账都齐；是当前 02 派最完整的一手证据。grounding 未校准是主要扣分项。

## 洞察

1. **本体的「接口」是 concept card，不是 OWL。** agent 读的是固定字段的文本卡；卡的字段顺序/定义质量直接决定 grounding。**本体工程的一半是卡片工程。** `已核`（机制）
2. **grounding level 是弱信号，不是保证。** 作者自己写明「不提供形式正确性保证」；entailed 94.9% / supported 82.1% 是 Test 3 Qwen 的切片，不是全校准曲线。`已核`
3. **检索是主瓶颈，不是推理。** gold evidence 完全检索：MCQ 61.7% vs OQ 23.6%；一旦检索到，MCQ 95.1–98.4% 会被引用。**先修检索，再修推理。** `已核`
4. **本体作为检索源可以打赢教科书。** RAGont > RAGdoc（Test 3），且 token 更少；本体提供的是**紧凑、结构化、可追溯**的知识。`已核`
5. **query fallback 是双刃剑。** 平均 +0.4–1.8 点，但在结构化本体已足够时（Test 1 MCQ）可能引入不精确检索。`已核`
6. **answering step 不是装饰。** 去掉后平均掉 2.9–5.8 点；把「推理轨迹」整理成「证据 digest」再回答，是独立贡献。`已核`
7. **context 预算会改变结论。** i-MedRAG 在 262k 下有竞争力；同一 8k 下 OA-RAG 84.9% vs 66.7%。**比较 RAG 必须固定预算。** `已核`

## 成本与使能条件

| 成本 | 一次性 / 每次 | 说明 |
|---|---|---|
| Concept card 生成 | 每本体一次性 | 从 OWL 抽取字段；可自动，但质量需检查 |
| Reasoner / SPARQL | 集成一次性 | ELK/HermiT 等；materialize  inferred edges |
| ReAct 调用 | 每次 | 5.8 calls/问（Qwen Test 3）；9.7k tokens |
| Name linking / fallback | 每次查询 | BM25 + 字符串相似度；轻量 |
| Grounding 标注 | 每次 | 模型自评；未校准 |
| 评估 | 每本体 | 需要 gold evidence/答案；成本不低 |

**使能条件**：OWL 本体 + reasoner；SPARQL endpoint；concept card 可生成；LLM 会写 SPARQL（本文用 ReAct + 错误反馈）。

**2022 年做会卡在哪**：LLM 写 SPARQL 不稳；agent 工具调用不成熟；没有 OntoTune/MedRAG 这类对照；context 预算更小。

**反向条件**：本体覆盖不足；没有 reasoner；问题主要是文本阅读；需要形式保证；多本体协调。

## 与现有判断的关系

| 关联 | 关系 |
|---|---|
| **E-03** | **一手依据**：强制报告本体观察 + 接地等级，在三个本体、六个医学 QA 任务上整体最优；grounding 与正确率正相关。补充限定：level 是自评、未校准。 |
| **P1** | 支撑「本体价值在约束/证据」：答案必须报告观察，不是自由生成；但 grounding 仍是弱约束。 |
| **P2** | 支撑「harness 不可分离」：同一本体，换成 concept card + ReAct + answering，效果不同。 |
| **02-L2** | 支撑「接地等级显式化整体最优」；新增「等级是自评，需要校准」。 |
| [evidence](../../../topics/02-judgment/evidence/README.md) | 核心文献；机制细节回 card。 |
| [03 知识](../../../topics/03-knowledge/README.md) | concept card 是投影的一种：把 OWL 投影成 agent 可读文本。 |

## 不可迁移

- 三个本体都是生物医学（GO/FoodOn/SNOMED）；跨域未测。
- 两个 backbone（Llama-3-8B、Qwen3.5-9B）；其他模型/版本未测。
- Test 3 是医学 MCQ/开放题；真实临床对话/长病历不适用。
- grounding level 是模型自评；不能当形式正确性保证。
- Test 3 的 token 优势依赖 8k 统一预算；长上下文基线在 262k 下有竞争力。

## 开放问题

- grounding level 能否校准？需要独立标注/审计，给出每个 level 的 precision/recall。
- 检索瓶颈怎么修？concept card 的字段/长度、BM25 vs dense、query fallback 的策略。
- 多本体协调（作者 future work）会不会破坏 grounding 的可判定性？
- concept card 能否自动生成并保持与 OWL 同步？这是 05 生产的子问题。
- 在非医学域（工业/金融/法规）是否同样有效？尤其是本体覆盖不足时。
