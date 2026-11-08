---
status: draft
updated: 2026-11-08
quality: A
based_on: card.md
claims: [E-10]
---

# MIOE：模型答对本体题，不等于内部有一个干净、模块化的本体

> 这篇消化不假设你读过论文。先给结论，再把术语、做法、数字、边界讲清楚；读完这一页，应该能自己判断它值不值得信、能不能用。

## 0. 三句话

1. **它问什么**：模型在做本体工程任务（判断实体属于哪个类、类之间的上下位）时，答对是因为内部真的在算「本体关系」，还是因为别的线索？行为正确率回答不了这个问题。
2. **它怎么做**：用**因果干预**（interchange intervention）换掉模型内部的一小段表示，看目标答案有没有按预期改变，同时看一个无关的「类别属性」有没有被一起带过去。
3. **它发现什么**：本体预测在内部是**可干预**的——换表示能改变答案；但单层最好的方法也只能**部分分离**目标关系与类别属性（Disentangle 约 0.59；多层最高 0.667，DAS 512×4），而且不同类差异很大。**「答对」不等于「内部有一个干净、模块化的本体」。**

## 1. 它解决什么问题

本体工程任务里，模型经常能给出看起来正确的答案（下面 `Airport/Infrastructure` 是示意，不是 MIOE 的类表；类表见 Table 12/13）。但**行为正确**可能来自：

- 真的在内部表示了「Airport ⊑ Infrastructure」这条本体关系；
- 只是记住了「Airport 和 Infrastructure 经常一起出现」；
- 或者靠别的类别属性（Country 有 currency、Airport 有 country/located-in）做了联想。

如果只是后者，那么「模型懂本体」这个说法就站不住；外部约束（判定器、校验器）也不能因为「模型答对了」就被省掉。MIOE 要测的是**内部机制**，不是输出分数。

## 2. 术语：读数字前先看

| 术语 | 用大白话说 |
|---|---|
| **MIOE** | 本文的机制可解释性基准名；全称按论文标题可读作 Mechanistic Interpretability for Ontology Engineering。 |
| **Entity typing（实体类型）** | 给一个实体，问它属于哪个类。示意：`Airport` 是 `Infrastructure` 还是 `Country`？（实际类表见 Table 12/13） |
| **Subsumption（上下位）** | 给一个类，问它的父类。例：`Airport` 是不是 `Infrastructure` 的子类？ |
| **Auxiliary attribute（类别属性）** | 某个类特有的属性，用来测「有没有把无关信息一起改掉」。例：`Country` 有 `currency`，`Airport` 有 `country` / `located in`（论文附录 Table 12；不是 runway length）。 |
| **Interchange intervention（互换干预）** | 准备两个输入：base（要测的）和 source（提供目标答案的）。把 base 在某一层、某个 token 的内部表示替换成 source 的，再看输出。 |
| **Cause（因果性）** | 干预后，base 的目标答案有没有变成 source 的？变了 = Cause 高。 |
| **Iso（隔离性）** | 干预后，base 的类别属性有没有保持原样？保持 = Iso 高。 |
| **Disentangle（分离度）** | Cause 与 Iso 的平均。高 = 「目标换对了，又没把别的信息带过去」。 |
| **SAE** | 稀疏自编码器：把激活分解成稀疏特征。这里作为干预方法之一。 |
| **DBM / MDBM** | 学习二值掩码找干预维度；MDBM 是多任务版。 |
| **DAS / MDAS** | 学习一个低维子空间做干预；MDAS 是多任务版。单层 MDAS 最强；全表最高是四层 DAS 512×4（0.667）。 |
| **rank** | 子空间维度；`rank 256–512` 是每层保留的维数。 |
| **Layer / window** | 干预发生在第几层；多层时用连续 2–4 层的窗口，每层一个子空间。 |
| **Residual stream** | Transformer 每层传递的向量流；本文在 subject token 的这一位置替换表示。 |
| **Entity / Context** | 两种评估切分：Entity 用训练模板考未见 subject；Context 用未见模板考训练 subject。不是两种 prompt 写法。 |

## 3. 它怎么做

### 3.1 数据

- 从 Wikidata / WordNet / schema.org 采样，构造两个任务：
  - `instance of`：54 个类、1,099 个 subject、376 个类别属性、4,288 个 prompt 模板。
  - `subclass of`：39 个类、1,113 个 subject、160 个类别属性、2,095 个 prompt 模板。
- 每个样本带：base 的实体/类、目标本体答案、一个类别属性问题（用来算 Iso）。
- 两个评估切分：**Entity** 用训练模板考未见 subject；**Context** 用未见模板考训练 subject。用来测干预是否跨 subject/模板泛化，不是「两种 prompt 写法」。

### 3.2 模型与方法

- 模型：Qwen3-8B、Qwen3-4B；36 层 decoder-only Transformer。
- 方法：SAE、DBM、MDBM、DAS、MDAS。
- 单层实验：36 层都扫；干预位置是 prompt 里 subject token 的 residual stream。
- 多层实验：连续 2 层/4 层窗口，每层一个 rank-k 子空间；`k×w` 表示 rank×window。
- 评价：Cause（目标答案变成 source 的类）、Iso（类别属性保持 base）、Disentangle（两者平均）。**只对未干预模型本来就能答对的 retained prompt instance 做干预**；base accuracy 在附录。Cause/Iso 先按 prompt 模板分组、再 macro-average，不是原始样本平均。

### 3.3 一个具体例子

base：subject `France`，目标类 `Country`，类别属性问「currency = Euro」。
source：subject `Paris`，目标类 `City`，类别属性是「population = …」。

- 如果干预后模型把 `France` 的目标类从 `Country` 答成 `City`，但 currency 没变：Cause 高、Iso 高 → 分离好。
- 如果目标类变成 `City`，同时把 currency 换成了 population：Cause 高、Iso 低 → 目标变了，但把无关信息也带过去了。
- 如果目标没变：Cause 低。

**这就是为什么只看「答对」不够**：目标答案可以变，也可以「连带」改变别的属性；后者说明内部表示没有干净地分离本体关系。

## 4. 结果：数字与条件

### 4.1 单层最好结果（Qwen3-8B）

| 方法 | instance of（Entity / Context） | subclass of（Entity / Context） |
|---|---|---|
| SAE | 0.412 / 0.371 | 0.397 / 0.429 |
| DBM | 0.425 / 0.396 | 0.431 / 0.443 |
| MDBM | 0.443 / 0.408 | 0.440 / 0.450 |
| DAS | 0.584 / 0.547 | 0.496 / 0.535 |
| **MDAS** | **0.592 / 0.587** | **0.513 / 0.542** |

> 出处：Table 2, p.6。各方法按 **Entity Disentangle** 选最佳层/维度，Context 用同一配置（不是对称切分）；SAE 8192/L13、DBM 4096/L10、DAS 1024/L17、MDAS 2048/L17（subclass 侧不同）。Dimension 定义不同（SAE latent width、DBM mask、DAS/MDAS rank），不是同容量对照。原文只报 seed 42、无 CI/方差；0.592 vs 0.584 不宜当稳定排序。

- 分数是 **Disentangle**，范围 0–1；不是准确率，也不是「本体理解百分比」。
- **没有方法到 1.0**；单层最好 MDAS 约 0.59，多层最高 0.667。0.59 是 Cause/Iso 的平均分，不等于「59% 的样本同时做到」。
- DAS/MDAS（分布式子空间）明显优于 SAE/DBM；SAE 在 **instance-of** 上的 Iso 只有 **0.352/0.344**（subclass-of 为 0.210/0.233；Table 2, p.6），说明稀疏特征不等于因果变量。

### 4.2 多任务与多层

- **多任务**（MDBM/MDAS）加辅助保持监督：**best reported multi-task configurations** 的 Iso 平均 **+0.081**、Cause 平均 **−0.052**（best-vs-best 配对差，不是多任务整体平均效应）；Disentangle 仍提升（Results, p.5）。
- **多层窗口**（Qwen3-8B，instance of）：
  - DAS 512×4：**0.667（+0.102）**，全表最高；MDAS 512×4 是 0.663，MDAS 256×4 是 0.666，差距可能在小样本噪声内，别把 0.667 vs 0.666 当稳定排序。
  - subclass of 的 MDAS 512×4：0.565（+0.052）
- 层剖面：Cause 在早期层弱，在中层/中后层最强；更后的层 Iso 高，但 Cause 可能掉到接近 0——**干预已经改不动输出**。

### 4.3 类级差异

- 具体、规则的类（airport、country、currency、university）分离较好；宽泛、异质的类（body of water、geographical feature、food、biological process、material）较差。
- 类级 Disentangle 的差异很大（Fig. 3, p.7 的散点）；原文没有给可直接引用的「0.03–0.65」区间，不要把它当量化结论。聚合分数会掩盖这种差异。
- 同一个类在不同角色（base vs source）下表现也不同：有的类更适合当 base，有的更适合当 source。

> 多层结果出处：Table 3, p.7；层剖面 Fig. 1, p.6；类级 Fig. 3, p.7。**Δ 是相对「同方法、同总维度」的单层结果**：DAS 512×4 的基线是单层 DAS rank 2048（≈0.565），不是 §4.1 的 DAS 0.584；MDAS 的 +0.052 基线是单层 MDAS 2048=0.513。**DAS 512×4 0.667 是全表最高；MDAS 0.666/0.663 紧随，差距不宜过度解读。**

### 4.4 这些数字之间的逻辑

- **为什么 DAS/MDAS 比 SAE/DBM 好？** SAE 找的是稀疏特征，不保证对应「目标关系」这个因果变量；DAS 直接学一个低维子空间，目标是把 cause 与 iso 分开。前者解释性好，后者因果干预更直接。
- **为什么多任务提升 Iso 却降 Cause？** 加辅助保持监督后，模型更倾向「别动无关属性」；代价是有时连目标也不动。Disentangle 仍升，因为保住无关信息的好处大于目标改变的小损失。
- **为什么多层比单层好？** 本体计算不像一个点，更像一段层间的分布式计算；在单层替换只能截到一部分，多层窗口能覆盖整段。
- **为什么类级差异大？** 具体类（airport/country）属性少而稳定；宽泛类（body of water/geographical feature）边界模糊、属性异质，目标关系与辅助属性更容易纠缠。

## 5. 这些数字不能说明什么

1. **0.59 不是「59% 懂本体」。** 它是一个归一化的分离分数，取决于 Cause/Iso 的定义、干预方法和数据集；不能跨论文比较。
2. **「部分分离」有两种解释。** 可能是模型内部的表示本来就纠缠，也可能是当前干预方法不够精确；本文**不能区分**。这是最重要的未解问题。
3. **只测了 Qwen3-4B/8B。** 不能外推到 Llama/GPT/Claude；不同模型族的内部结构可能完全不同。
4. **只测了两个任务。** entity typing / subsumption 是最基础的本体关系；disjointness、domain/range、存在限制等更复杂的公理没测。
5. **干预位置只有 subject token 的 residual stream。** 换位置（其他 token、attention head、MLP）可能改变结论。
6. **聚合分数掩盖类级差异。** 0.59 的平均值可能由少数好类拉高；具体类要看类级表。
7. **没有下游任务/部署评估。** 它不告诉你「用这个机制指标能不能筛出可信的本体判断」。

## 6. 工程上怎么用

- **别用行为准确率证明「模型懂本体」。** 如果这个判断会影响架构（比如要不要外部判定器），至少要做一次因果干预；否则「答对」只是相关性。
- **同时看目标与辅助信息。** 只报 Cause 会高估：模型可能把目标换对了，但也把无关属性一起改了。Iso 是必要的对照。
- **优先 distributed subspace 方法。** 如果要做类似分析，DAS/MDAS 比 SAE/DBM 更可能给出可解释的因果变量；但计算成本更高。
- **多任务/多层通常更好，但有代价。** 多任务提升 Iso、降 Cause；多层窗口提升整体分离度，但扫描成本高。
- **做类级分析。** 不要只报平均值；具体类/宽泛类的差异可能决定你的域能不能用。
- **这不是生产工具。** 它是研究「内部有没有本体」的尺子；不要把它当在线判定器。

### 6.2 一次最小审计怎么跑

如果你只想回答「我们的模型是不是真的在用本体」，不需要复现整篇论文：

1. 选 20–30 个具体类 + 每个类 1 个辅助属性；类要具体、别用宽泛类。
2. 造 base/source 成对 prompt：base 问目标类，source 提供另一个类；辅助属性问题不变。
3. 选 2–3 个中间层（比如 12/18/24 层），用 DAS/MDAS 学 rank 256–512 的子空间。
4. 做互换干预：记录 Cause（目标是否换成 source）与 Iso（辅助属性是否保持 base）；报 Disentangle 与类级分布。
5. 加一个对照：用随机子空间/随机特征替代学到的 F 做干预；若 Cause 不升高，说明不是 F 在起作用。换辅助属性只影响 Iso，测不出干预是否生效；且只在 base-correct 的 retained 例上评估。
6. 结论只写「在哪些类/层上可干预、分离到什么程度」，不要写「模型懂/不懂本体」。

## 7. 质量与边界

- **证据类型**：机制研究（因果干预）；`quality: A`，因为多方法、多层、多类、开源，且结论克制。
- **强项**：把「答对 ≠ 有本体」从哲学争论变成可测的因果问题；同时测 Cause 与 Iso；给出层/类/方法的差异。
- **主要威胁**：只 Qwen3、只两个任务、单干预位置、聚合掩盖类级、无法区分「表示纠缠」与「方法不够强」。
- **引用时的限定**：说「MIOE 发现本体预测可干预但只部分分离」，不要说「MIOE 证明模型没有本体」；后者是过度解读。

## 8. 与仓库判断的关系

- **E-10（已核）**：本体预测在机制上可干预，但无法与类别辅助信息干净分离；答对不等于内部有一个干净、模块化的本体机制。
- **P1（价值在约束/控制）**：如果内部本体既不干净又不可靠，外部判据（判定器/闸门）的必要性反而增强；不能因为「模型答对了」就省掉外部约束。
- **P3（判定是权衡）**：Cause 与 Iso 是反向的；没有单一向优的方法，也没有单一「本体理解」分数。
- **06 测量派**：这是「机制尺子」的核心一手证据；它测的是内部过程，不是输出。

## 9. 还没解决 / 下一步

- **跨模型族**：Llama/GPT/Claude 是否同样部分分离？
- **更丰富的公理**：disjointness、domain/range、存在限制能否用同样方法测？
- **干预位置**：subject token 之外（attention/MLP/其他 token）是否改变结论？
- **表示 vs 方法**：「部分分离」到底是表示纠缠，还是方法不够强？需要更强干预/方法对照。
- **类级预测**：类级差异能否预测下游本体工程任务的表现？
- **下游效用**：机制指标能否用来筛选「可信的本体判断」？

## 10. 原文

- arXiv:2610.38326；PDF 在 `src/papers/2610.38326-mioe/`。
- 代码：https://github.com/King-s-Knowledge-Graph-Lab/MIOE
