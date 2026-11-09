---
status: draft
deliverable_status: draft
updated: 2026-11-09
section: execution-forms
evidence: [E-20]
---

# 形态：机器拿本体做了什么

> 同一份本体放在同一个位置，机器拿它做的事也可能不同。**「有引擎」不等于「会拦」，更不等于「有授权」。**
>
> 本页的上游是 [topics/execution-forms.md](../../../topics/execution-forms.md)；代码核对是 E-20，不是效应量。

## 1. 五档

| 形态 | 机器做什么 | 判据 | 不代表 |
|---|---|---|---|
| `engine` | 推理器/引擎直接求值：DL、SHACL、查询重写 | 有求解/求值调用；输出随本体变化 | 会拦、有授权 |
| `compiled` | 本体先编译成约束/规则/状态结构，再由代码执行 | 有「本体 → 约束/规则」的转换步骤，转换物被求值 | 编译正确 |
| `context` | 作为文本/结构化上下文注入，模型自行使用 | 进入 prompt/上下文；没有外部求值 | 弱执行（它是不执行） |
| `label` | 只当标签表/schema/分类 | 只提供类型名/关系名 | 参与判定 |
| `none` | 没有执行，或本体不是被测变量 | 概念/生成/评测/边界证据 | 「执行了但无效」 |

> `compiled` 与 `engine` 的差别是「有没有显式的编译步骤」；`context` 不是「弱执行」，是「不执行，只供给」。三根分类轴（派/时刻/形态）不能互相替代。

## 2. 执行链：求值 → 决策 → 执行 → 授权 → 审计

| 层 | 问什么 | E-20 里的例子 | 这一层的失败 |
|---|---|---|---|
| 求值 evaluate | 本体算出了什么？ | ontop 的查询重写；semantica 的 SHACL；trustgraph 的 SHACL-AF；open-ontologies 的 SHACL→SPARQL | 求值错、`inference="none"` 不展开、skip、fail-open |
| 决策 decide | 通过/违反/未检查完？放行/拒绝/升级？ | trustgraph 的 `tg-pol:blocks`；open-ontologies 的 verified 三态 | 第三态被折叠、策略缺失、unknown 并进 pass |
| 执行 enforce | 真的改变走向了吗？ | trustgraph 删除 subject 侧三元组；open-ontologies 的 `enforce` CI 门 | 只删 subject、fail-open、只做报告 |
| 授权 authorize | 谁有权推动写？证据够不够？ | 无（commit-gate 是概念架构） | 无实现、false-defer、批准越界复用 |
| 审计 audit | 为什么允许/拒绝？能重放吗？ | `closure_diff`；JSON 保留第三态 | 日志不可追、shell 退出码丢第三态 |

三条读法（`推测`，框架不是 E）：

1. **求值 ≠ 执行。** 一个 engine 可以只算不拦（ontop/semantica），也可以算了才拦（trustgraph）。
2. **执行 ≠ 授权。** CI 规则门、读路径过滤都不是单次写授权；`enforce` 不等于 `authorize`。
3. **授权 ≠ 正确。** commit gate 只保证按 contract 执行，不保证 policy 本身对。

## 3. 四个项目的代码级核对

| 项目（commit） | 位置 | 形态 | 机器实际做什么 | 不做什么 |
|---|---|---|---|---|
| trustgraph `184f622` | `read-path` | `engine` | 从 `urn:graph:policy` 加载 SHACL-AF NodeShape；跑 `sh:SPARQLTarget` + `sh:SPARQLRule`；被 block 的 subject 侧三元组从查询结果删除 | 不是动作前 gate；不做 OWL 推理；异常 fail-open；只删 subject 侧 |
| semantica `39cf721` | `checker` | `compiled` | `OntologyEngine.to_shacl` 派生 SHACL；`validate_graph` 调 pyshacl，`inference="none"`；CLI `validate shacl` | 不在 agent loop 内自动调用；不做 OWL 推理；无 catch/FA 测量 |
| ontop `964dbb7` | `supply` | `engine` | TBox 饱和 + 查询重写（rewrite → unfold → SQL）；`QuestStatement` 执行 | 不是 gate；不校验输出；不是 LLM agent |
| open-ontologies `375fbc4` | `none`（工具面；CI 规则门） | `engine` | 默认 SHACL→SPARQL 交 Oxigraph；`--verified` 走 `oo-shacl`（0/2/3，3=undetermined）；`closure_diff` 报蕴含损失 | 不授权单次写/落盘；`enforce` 是 CI 规则门；外层把 `conforms:null` 映射为 exit 2 |

> E-20 的限定：4 个项目、pin commit、只读代码、未跑测试；不是效应量，不能外推为所有实现。

## 4. 位置 × 形态

| 位置 | 常见形态 | 代码/证据 | 关键边界 |
|---|---|---|---|
| context | `context` / `compiled` | E-12/E-14；N&D/CAI | 不执行，只供给 |
| memory | `compiled` | E-05/E-17；FIRME/EvoMem | 状态结构，不是推理器 |
| evidence | `compiled` / `context` | E-03；OA-RAG | 输出契约，不阻断 |
| checker | `compiled` / `engine` | E-02/E-20；Catch/semantica | 判定≠策略；三态要显式 |
| action | `compiled` | E-04/E-16；POLAR/OntoAct | 机制多种，收益窄 |
| commit | 无实现（设计） | commit-gate 概念 | 不能声称已落地 |
| read-path | `engine` | trustgraph | best-effort；单实现 |
| supply | `engine` | ontop | 查询重写，不是闸 |

**一个反直觉的结论**：`engine` 内部至少四种语义（E-20）。选型时先问「机器到底做了什么」，再问「它能不能改变走向」。

## 5. 这张表不能证明什么

1. **不能证明「形态改变行为」。** 只有跨来源的弱对照；没有同一本体换形态的消融。
2. **不能证明「engine 更强」。** 四种 engine 语义不同；有的只算不拦。
3. **不能证明「compiled 正确」。** 编译可能过度/不足；`inference="none"` 不展开子类。
4. **不能证明「有 enforce 就有授权」。** CI 门与读路径过滤都不是写授权。
5. **不能把 `none` 读成「无效」。** 它只表示「没有执行，或本体不是被测变量」。

## 6. 什么会改变它

- 同一本体、同一任务，只换形态（context vs compiled vs engine）并测行为 → 形态的效应量；
- 出现一个既有求值又有单次写授权的实现 → 拆开「执行/授权」两层；
- 出现第二个独立 read-path 实现 → 讨论是否升第七时刻；
- 编译产物被证明覆盖/保证兼得 → 推翻「覆盖与保证不可兼得」。

## 7. 上游

- [topics/execution-forms.md](../../../topics/execution-forms.md)（五档、26 源初判、代码核对、执行链）
- [topics/seams.md](../../../topics/seams.md)（六时刻 + 轴外位置）
- [conclusions](../../../topics/conclusions.md) 的 E-20
- [02 §3/§5](../../02-engineering-playbook/sections/map.md#24-选形态五种别把-context-当低配-engine)（选型与开源参考）
