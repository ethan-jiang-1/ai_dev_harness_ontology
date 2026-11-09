---
status: draft
updated: 2026-11-09
rq: [RQ1, RQ2, RQ5]
---

# 执行形态：本体以什么方式被机器使用

> 第四根横切轴。派轴问「凭什么起作用」，时刻轴问「在哪一格」，形态轴问「机器拿它做了什么」。三根轴不能互相替代。

## 为什么要这根轴

中心问题的后半句是「以什么形式被执行」，但六派回答的是机制类型，`seams` 回答的是介入时刻。两者都装不下一个更基本的事实：同一份本体，可以只被塞进 prompt，也可以被编译成 SHACL 再求值；前者是「上下文」，后者是「执行」。**不区分形态，就会把「本体没被测量」和「本体被执行后无效」混成一句话。**

这根轴也是论文与开源项目的接点：论文常停在「提出机制」，代码能回答「机器到底跑没跑」。开源卡的 `execution_form` 是第一次把这个区分落到字段上；本页把它扩展到全部来源。

**一个换词检查（2026-11-09，按 digest §3/§4/§8 分类，不是元分析）**：26 个来源里 15 个的结论把「本体」换成「任意结构化上下文」仍然成立（`推测`，分类判断）；只有 3 个（MIOE、Ontology Catch、OA-RAG）的结论依赖 OWL/DL 语义。这个配比说明：仓库过去测的更多是「结构化上下文 + harness 位置」，不是「本体形态」。形态轴就是把这部分说清楚。

## 五档

| 值 | 机器拿它做了什么 | 判据 |
|---|---|---|
| `engine` | 推理器/引擎直接求值：DL reasoner、SHACL、查询重写 | 有求解/求值调用；输出随本体变化 |
| `compiled` | 本体先被编译成约束/规则/状态结构，再由代码执行 | 有「本体 → 约束/规则」的转换步骤；转换物被求值 |
| `context` | 作为文本/结构化上下文注入，模型自行使用 | 进入 prompt/上下文；没有外部求值 |
| `label` | 只当标签表/schema/分类，不参与判定 | 本体只提供类型名/关系名 |
| `none` | 没有执行，或本体不是被测变量 | 概念/生成/评测/边界证据 |
| `unknown` | 读了但定不了级 | 只在证据不足时用，digest 要写为什么 |

**注意**：`compiled` 与 `engine` 的区别是「有没有一个显式的编译步骤」；`context` 不是「弱执行」，是「不执行，只供给」。不要把 `context` 当成 `engine` 的低配版——它们回答的是不同问题。

`engine` 是统称：代码核对发现它至少覆盖 OWL 2 QL 查询重写（ontop）、SHACL-AF 策略求值（trustgraph）、SHACL 校验（semantica）、SHACL→SPARQL/verified Core（open-ontologies）四种语义。计数时不要把四种合成一个「强执行」。

## 26 个来源的初判

计数：`engine` 4 / `compiled` 7 / `context` 2 / `label` 1 / `none` 12。

| 来源 | 形态 | 依据（digest） | 备注 |
|---|---|---|---|
| OA-RAG | `engine` | OWL/DL reasoner + SPARQL `DESCRIBE/ASK/SELECT` | 本体同时当推理器与注释源 |
| trustgraph | `engine` | `policy/policy_filter.py` 自研 SHACL-AF 求值 | 读路径授权；轴外位置 `read-path` |
| ontop | `engine` | TBox 饱和 + 查询重写成 SQL | 供给/查询编译；轴外位置 `supply` |
| open-ontologies | `engine` | `shacl.rs` / `shacl_verified.rs` 两条求值路径 | 工具面；执行未跑起来（C2） |
| POLAR | `compiled` | Datalog 动作本体 + 状态投影，代码算逆序列 | 动作前剪枝 |
| OntoAct | `compiled` | 三值条件 ⊤/⊥/? + 假设 revision，代码验证 | 推理期 |
| Ontology Catch | `compiled` | 本体编译成 checker（pass/flag/unknown） | 输出后判定 |
| 多 agent 诊断 | `compiled` | 代码在 SYMP/DOID/HPO 上算确定性评分 | LLM 只做语言 |
| FIRME | `compiled` | product–topic 本体 + registry/规则融合 | 记忆对齐 |
| EvoMemState | `compiled` | 本体引导 relational state + 策略 | 记忆状态 |
| semantica | `compiled` | 本体 `to_shacl` → pyshacl | 离线/CLI；checker 组件 |
| N&D | `context` | 本体塔投影成约 45k 字符文本进 prompt | 供给 |
| Grid Agents | `context` | 作者明说「知识系统，不是形式 OWL」 | 受监管供给 |
| ReX-GG | `label` | 本体只当标签表（四种关系） | 不参与判定 |
| CAI | `none` | Table 1 ontology 是 `not measured` | 边界证据 |
| CASEL | `none` | 无本体变量；审批/风险分配 | harness 证据 |
| SLB | `none` | 「本体」是标注体系，不是域本体 | harness 证据 |
| Agents are Systems | `none` | 全文无本体变量 | harness 证据 |
| CASTON | `none` | 本体精化，未测下游执行 | 生产 |
| Diagnose | `none` | 本体接地 DSL 的任务诊断 | 边界证据 |
| Commit Boundary | `none` | 概念协议，无实现 | 生产/治理 |
| OntoDoc | `none` | 本体生成，未测下游 | 生产 |
| Peeling | `none` | 从嵌入抽分类法，未测下游 | 生产/表示 |
| Evontree | `none` | 训练侧规则筛数据 | 训练 |
| MIOE | `none` | 测模型内部表示，不是 harness 执行 | 尺子 |
| SFE-O | `none` | OWL 表达力够，但约束未落成可执行 SHACL | 表示边界 |

> 初判来自各 digest 的 §3/§4/§8；与卡片 `execution_form` 保持一致。改一档要同时改卡、本页与 digest 的判定段。4 个开源项目已在 pin commit 上做代码级核对，见下节。

## 代码级核对（2026-11-09）

在 card 所 pin 的 commit 上，把 4 个开源项目的执行路径读了一遍（只读代码，未跑测试）。四者都算「执行」，但语义不同：

| 项目（commit） | 位置 | 形态 | 代码实际做什么 | 不做什么 |
|---|---|---|---|---|
| trustgraph `184f622` | `read-path` | `engine` | `policy_filter.py` 从 `urn:graph:policy` 加载 SHACL-AF NodeShape；对候选节点跑 `sh:SPARQLTarget` + `sh:SPARQLRule`；`tg-pol:blocks` 默认 true；被 block 的 **subject 侧**三元组从查询结果删除；接在 `policy/triples/service.py` 返回前 | 不是动作前 gate；不做 OWL 推理；异常 fail-open；只删 subject 侧 |
| semantica `39cf721` | `checker` | `compiled` | `OntologyEngine.to_shacl` 从 ontology dict 派生 SHACL；`validate_graph`/`run_shacl_validation` 调 pyshacl，`inference="none"`；CLI `validate shacl` | 不在 agent loop 内自动调用；不做 OWL 推理；没有 catch/FA 测量 |
| ontop `964dbb7` | `supply` | `engine` | `QuestQueryProcessor` 构造时 `rewriter.setTBox(saturatedTBox)`；`reformulateIntoNativeQuery` 做 rewrite → unfold → SQL；`QuestStatement` 执行 | 不是 gate；不校验输出；不是 LLM agent |
| open-ontologies `375fbc4` | `none`（工具面；CI 规则门，不是回路授权） | `engine` | 默认 `ShaclValidator` 把 SHACL 约束编译成 SPARQL 交 Oxigraph；`--verified` 走 `oo-shacl`（0/2/3，3=undetermined，`Certified`）；`closure_diff` 报蕴含损失 | 不授权单次写/落盘；`enforce` 是 CI 规则门；外层 CLI 把 `conforms:null` 映射为 exit 2；未跑 |

**四条代码级判断**（`已核（代码）`；只读代码，不等于跑通）：

1. **`engine` 不是一种语义。** ontop 是 OWL 2 QL 的 TBox 饱和 + 查询重写；semantica 是 SHACL 校验且 `inference="none"`；trustgraph 是 SHACL-AF 策略求值；open-ontologies 是 SHACL→SPARQL 或 verified Core。四者都叫「执行」，只有 ontop 动 TBox 蕴含。
2. **执行 ≠ 健全。** trustgraph 在 target/rule 异常时返回 False/None，无策略直接放行；且 `_triple_blocked` 只查 `triple.s`。read-path 是 best-effort gate，不是强闸门。
3. **执行 ≠ 授权。** open-ontologies 有真求值器、影响报告与 `enforce` CI 规则门，但没有单次写授权/commit gate；semantica 是 CLI 校验，不在回路内。唯一 read-path gate 仍是 trustgraph，不够第二个独立实现，`read-path` 保持轴外。
4. **三态在接口上会被折叠。** `oo-shacl` 的 exit 3（undetermined）进入 wrapper 后变成 `conforms: null`；外层 `gate_exit_code` 把 null 映射为 exit 2，与解析失败同码。JSON 保留第三态，shell 退出码不保留——这是「执行形态」之外的一个接口层发现。

> 以上 4 条已收进 [E-20](./conclusions.md)（`已核（代码）`）；不升 `已证`，因为没有跑测试和对照实验。

## 它改变了什么

1. **把「本体有没有用」拆成「哪种形态、在哪一格」**。`engine`/`compiled` 才谈得上执行；`context` 谈的是供给；`label` 只是命名。但 `engine` 内部至少四种语义（见代码核对），不能把「有引擎」当成一个强度刻度。
2. **解释了 E 层的配比**。E 层里有多条来自 `none` 形态的来源（E-01/E-07/E-08/E-09/E-14/E-15/E-18），它们支撑的是 harness/度量命题，不是「本体执行」命题。
3. **给实验一个缺口**。现有实验多在换位置（EXP-003），缺「同一接缝、同一内容、只换形态」的消融；见 [EXP-007](../experiments/EXP-007-form-ablation.md)（提案）。

## 开放问题

- `engine` 与 `compiled` 的边界在工程上是否稳定？有的系统把编译藏在启动阶段。
- 形态差异能否解释效应量差异？目前只有跨来源的弱对照。
- 同一形态在不同接缝上是否可迁移？这是 RQ2 的下一刀。
- 「执行」是否必须可阻断？SHACL 报告不阻断，算不算执行？本页按「机器求值」算 `engine`，但是否改变走向另由 `seam` 判断。
