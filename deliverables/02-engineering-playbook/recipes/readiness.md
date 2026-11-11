---
status: draft
updated: 2026-11-09
parent: ../README.md
basis: E-02/E-03/E-12/E-20；SFE-O；checker F2
---

# R0 · 本体可执行性体检

> **这不是建本体，是准入检查。** 30–60 分钟（有现成任务/样本；没有则半天），回答一个问题：手上这份本体，今天能不能被某个消费者执行？
>
> 四项检查任何一项不过，先修，不要上 R1–R12。检查项是工程配方（`推测`）；背后的失效有 E-xx 或代码级证据。

## 0. 一句话

**先证明「有消费者、有执行落点、名字/单位对、声明够用」，再选接缝。** 否则后面的 R1–R12 都建在沙上：投影会抄错单位，checker 会对每条正确答案误报，action gate 会拿过期状态做硬 veto。

**为什么是这四项**：四项分别对应四类已核失败——命名/单位（E-12）、缺声明/闭世界（E-02）、覆盖/检索（E-03）、执行落点（E-20）；任何一项不过，后面的 R1–R12 都在沙上。

## 1. 适用 / 不适用

| 适用 | 不适用 |
|---|---|
| 已有 OWL/RDFS/SHACL、ERD、taxonomy、字段字典中的任意一种 | 还没有任何领域词汇表，也没有领域专家 |
| 有一个明确消费者：agent、checker、查询接口、CI、记忆 | 消费者只是「以后可能会用」 |
| 能拿到任务、样本或历史误判 | 没有任务、没有样本、没有负例 |
| 愿意先修数据/声明，再谈机制 | 要求「先上机制，数据以后补」 |

**没有消费者 → 停。** 这是 SFE-O 的 stop 1，也是 [05/representation 机制](../../../topics/05-produce/representation/mechanism.md) 的第一条：没有判定器、查询、授权或 agent 真的读这份表示，只做文档，不做「可执行本体」。

## 2. 四项检查

| # | 检查 | 问什么 | 通过线（工程建议，`推测`） | 不过怎么办 | 证据 |
|---|---|---|---|---|---|
| 1 | 名字 / 单位 / 别名 | 同一个量是否有唯一 tag、单位、别名？ | 3 个代表性任务里，primary trap 不再由命名/单位歧义造成 | 先做 R1；不要做投影/编译 | E-12：K0→K1 避坑率 +54.6pp（单工厂、9 任务） |
| 2 | 声明 / domain-range | 用到的类/属性是否都有声明？ | 抽样 50 条数据，未声明 term = 0；domain/range 缺口有清单 | 先补声明；补不了的进人工队列 | E-02：curated 的 FA 主源是 undeclared term / closed-world，不是「与数据矛盾」 |
| 3 | 覆盖 / 词汇 | 任务里的实体/关系，本体覆盖多少？ | 200 题抽样，unknown IRI < 20%；gold evidence 检索率 ≥ 50% | 先补本体或换 R5 data-derived；不要做 R4 等级 | E-03：检索是主瓶颈（MCQ 61.7% vs OQ 23.6%）；20%/50% 是工程门 |
| 4 | 执行落点 / 版本 | 每条要执行的约束，是否有 shape/代码检查 + 一个能触发它的负例？ | 每个约束都有落点 + 负例；版本/来源字段齐全 | 只交付文档，不称「可执行本体」 | SFE-O：OWL 2 表达力够，但约束未落成可执行 SHACL |

### 2.1 检查 1：名字 / 单位 / 别名

**做法**：

1. 从历史误判里选 3 个任务，标出 primary trap（最常掉进去的那个坑）。
2. 建 tag registry：`{label, unit, quality_flag, aliases[]}`；建 slot map：`{entity_type, slot, unit}`。
3. 统一命名、单位、别名；补单位换算；**不改结构**。
4. 用同一模型回放 K0/K1；报 primary-trap avoidance，不只看总分。

**为什么先做**：这是已测各层里最大的一层增益，而且不需要建整座本体塔（E-12）。**但它只在单工厂、9 任务、答案基本写在文本里的条件下测过**；换域要重测。

### 2.2 检查 2：声明 / domain-range

**做法**：

1. 导出数据里实际用到的类/属性；与本体声明求差。
2. 缺声明的，先自动补 domain/range；补不了的进人工队列。
3. 用 50 条真实数据跑一次 SHACL/声明检查，记录误报。

**为什么先做**：curated checker 的 precision 仅略优于随机（+1.6 点，CI 跨零），FA 主源是 undeclared term 与 closed-world；每个缺失声明会经 declaration check 对用到它的正确答案误报（E-02，checker F2）。不补声明就上 checker，会得到「抓得多、杀得也多」的假象。

### 2.3 检查 3：覆盖 / 词汇

**做法**：

1. 抽 200 个真实问题/任务；标出问题里的实体、关系、限定。
2. 统计 unknown IRI、未覆盖关系、只能 near-match 的词汇。
3. 先修检索/覆盖，再谈 grounding 等级；等级只反映覆盖缺口时，不要拿它当质量信号。

**为什么先做**：OA-RAG 的检索是主瓶颈（gold evidence 完整检索 MCQ 61.7% vs OQ 23.6%）；检索率 <50% 时，加等级/推理层没有意义（E-03）。20% unknown IRI 是 [evidence 机制](../../../topics/02-judgment/evidence/mechanism.md) 的工程门，不是论文阈值。

### 2.4 检查 4：执行落点 / 版本

**做法**：

1. 列出「要执行的约束」：单位必填、范围、source 必填、矛盾标记、连接完整性。
2. 每条约束配一个 shape/代码检查 + 一个已知能触发它的负例。
3. 记录 artifact 版本：本体、shapes、映射、投影、policy 各自版本 + 生成时间。
4. 生成物只读；改动回源，不手工修生成物。

**为什么先做**：SFE-O 的结论是「表达 ≠ 执行」：OWL 2 能表达类/关系/约束，但数值、约束执行、外部服务都在 OWL 外；论文明确说约束尚未成为可执行 SHACL，不能把「模型评审通过」当 DoD（[SFE-O digest](../../../src/papers/2610.37123-sfe-o/digest.md)）。没有负例的 shape 只是声明，不是判据。

## 3. 你手上是什么，就走哪条

| 你有的 | 能做的 | 不要做 |
|---|---|---|
| OWL 2 DL + reasoner/SPARQL endpoint | R4（证据契约）、R6（条件闸，若需要） | 不要假设 `engine` 就会拦；E-20 四种语义不同 |
| OWL 2 QL + 稳定关系库 + R2RML 映射 | R11（OBDA 查询重写） | 不要拿它做 DL 推理/事务写入/授权 |
| SHACL shapes / 可派生 shapes | R5（输出后 checker）、R10（离线/CI） | 不要把 CLI 校验当 in-loop 自动拒收 |
| 只有 taxonomy / ERD / 字段字典 | R1（K1）+ R5 data-derived（低 FA） | 不要承诺 R2 投影或 R9 落盘授权 |
| 只有 Excel / 术语表 | R1；先补 unit/source | 不要建整座塔；不要做 checker |
| 已有 commit/审计/事务系统，但没有本体 | R9 只能设计；先补 domain policy | 不要把审批流当 commit gate |

## 4. 最小数据契约

`readiness_report`（工程 schema，`推测`）：

```text
{
  system_id, ontology_version, checked_at, consumer,
  gates: {
    names_units: {status: pass|flag|unknown, tasks: [], primary_traps: [], fixes: []},
    declarations: {status, used_terms, undeclared[], domain_range_gaps[], sample_n},
    coverage: {status, questions_n, unknown_iri_rate, gold_retrieval_rate, missing_terms[]},
    executable: {status, constraints_n, shapes_n, negative_examples_n, artifact_versions{}}
  },
  verdict: go|fix_first|stop,
  blockers: []
}
```

**三态必须显式**：`pass` / `flag` / `unknown`。`unknown` 不是 pass；没有检查过的项不能算通过（E-20 的代码核对发现，第三态在 shell 退出码会被折叠；接口层要保留）。

## 5. 30–60 分钟流程（有现成样本）

| 分钟 | 动作 | 产出 |
|---:|---|---|
| 0–10 | 写消费者契约：谁在什么时刻读、要拒绝/回答什么 | 一页 consumer contract |
| 10–25 | 抽 3 个任务 + 50 条数据 + 200 个问题（可复用已有样本） | 检查样本 |
| 25–40 | 跑四项检查；每项给 pass/flag/unknown | `readiness_report` 草表 |
| 40–50 | 给 blocker 排优先级：先修哪个，能修到什么程度 | 修复清单 |
| 50–60 | 决定：go / fix_first / stop；写下一 sprint 的入口 | 一页 memo |

## 6. 验收 / 停

| 门 | 通过 | 停 |
|---|---|---|
| 消费者 | 有具名消费者与调用点 | 只有「以后会用」→ 停 |
| 名字/单位 | 3 任务 primary trap 不再由命名/单位造成 | 仍由命名/单位造成 → 先 R1 |
| 声明 | 50 条抽样 undeclared = 0 | 补不齐 → 先修数据，不上 checker |
| 覆盖 | unknown IRI < 20%，gold 检索 ≥ 50% | 低于线 → 先修检索/覆盖 |
| 执行落点 | 每个约束有 shape/代码 + 负例 | 没有负例 → 只交付文档 |
| 版本 | 本体/shapes/映射/投影都有版本 | 版本不可追 → 不上写路径 |

**任何一项 `unknown` 都不能当 pass。** 先补检查，再谈机制。

## 7. 反模式

1. **把 OWL 文件当可执行。** 表达力够 ≠ 有执行落点；SFE-O 的约束仍在文档里（[digest](../../../src/papers/2610.37123-sfe-o/digest.md)）。
2. **把 SHACL 通过当语义正确。** shapes 派生可能过度/不足；`inference="none"` 不展开子类（E-20）。
3. **没有消费者先建塔。** 投影/编译/checker 都没有调用点，最后只剩文档。
4. **把 curated 当权威。** precision 仅略优于随机；先审计/补声明（E-02）。
5. **没有 unit/source 就上投影。** 投影会把错误单位抄进上下文，而且看起来更权威。
6. **用「本体很完整」当准入。** 落地取决于「位置 × 成本 × 使能条件」，不是本体多完整（E-19，`推测`）。

## 8. 证据与边界

| 判断 | 等级 | 条件 / 不能说明 |
|---|---|---|
| K0→K1 避坑率 +54.6pp | 已核 | 单工厂、9 任务、答案基本写在文本里；不能外推跨域 |
| curated checker precision 仅略优于随机（+1.6 点，CI 跨零） | 已核 | UniProt；人工故障 + 25% 错答案假设；不是所有 curated |
| curated FA 主源是 undeclared term / closed-world | 已核 | 32 条盲审 + 消融；不是全量分解 |
| 检索是主瓶颈（MCQ 61.7% vs OQ 23.6%） | 已核 | 医学 QA、三个本体、2 backbone |
| 表达 ≠ 执行 | 已核（限 SFE-O） | 单域、无 agent 评测、`quality: C`；不能推出「第二档够用」 |
| 四项检查是必要准入 | 推测 | 工程配方；没有对照实验证明「不过就必失败」 |

**一句话**：R0 不证明本体会有效，只证明它**值得进入下一轮**；不通过 R0 的项目，不应该用 R1–R12 的效果数字立项。

## 9. 交接

- 名字/单位问题 → [R1](knowledge.md#r1--k1-语义层先把名字和单位对齐)
- 声明/覆盖问题 → [R5](judgment.md#r5--输出后-checker先超过空结果重试) 或 [R10 ](offline-and-obda.md#r10--离线ci-shacl把没检查完做成第三态)
- 查询/映射问题 → [R11 ](offline-and-obda.md#r11--obda-查询重写本体在查询编译时被执行)
- 消费者是投影 → [R2](knowledge.md#r2--知识投影把领域知识写成固定分节的文本)
- 消费者是动作闸 → [R6](constraint.md#r6--动作前可逆性闸只在不可逆高代价弱模型时试)

**出处**：[SFE-O digest](../../../src/papers/2610.37123-sfe-o/digest.md) · [05/representation 机制](../../../topics/05-produce/representation/mechanism.md) · [checker F2](../../../topics/02-judgment/checker/findings.md) · [E-02/E-03/E-12/E-20](../../../topics/conclusions.md)
