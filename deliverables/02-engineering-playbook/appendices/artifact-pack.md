---
status: draft
updated: 2026-11-11
parent: ../README.md
note: filled sample for reading, not a run record
---

# 附录 D · 一份填好的产物包（R4 证据契约；历史模板）

> **2026-11-11 证据重置**：R4 的原锚 E-03 已撤回；本包只作“字段怎么填”的历史模板，不再表示 R4 可执行/可验收。表中 `已核` 只表示该值在旧 R4 示例里出现过，**不是当前 admitted 证据**。
>
> **这是什么**：把 [R4](../recipes/judgment.md#r4--输出证据契约让答案带依据和接地等级) 的十个字段，用 [case](./case.md) 的冷却水场景填一遍，让你看到「字段长什么样」。
>
> **不是什么**：不是运行记录，不是客户案例，不是效果证明。每个值都标了 `已核` / `推测` / `untested`；标 `untested` 的格子就是你要在自己的域里补的。
>
> **怎么用**：先读 §0 的交接表，再照 §2–§7 填你自己的一行；填不出的格，写「不知道」并链到 [acceptance §5.2](../sections/acceptance.md#53-期待与数据需求验收规格)。

## 0. 一页交接

| # | 产物 | 谁产 | 何时 | 怎么验 | 本包在哪 |
|---|---|---|---|---|---|
| 1 | R0 体检表 | 工程 + 数据 | 动手前 | 四项有 pass/flag/unknown | §1 |
| 2 | 接口契约（R4） | 应用 + 数据 | 选 recipe 后 | 三原语 + 观察类型 + 预算齐 | §2 |
| 3 | concept card 样例 | 数据/本体 | 建卡 | 8 字段齐，1–2k 字符 | §3 |
| 4 | 查询与观察样例 | 应用 | 回放前 | 每条观察能指到卡/ASK/SELECT | §4 |
| 5 | 账本行 | 应用 | 每次查询 | 字段齐，`hit/miss` 可算 | §5 |
| 6 | 停线记录 | 工程 | 每周/每阶段 | 主指标 + 停线 + 量不出时 | §6 |
| 7 | 未测清单 | 工程 | 交稿前 | 每条能说「缺什么数据」 | §7 |

> **和 04 的区别**：04 的产物包是访问控制链（契约→TTL→policy→audit）；02 的产物包是**一条 recipe 的接口、观察、账本、停线**。两者不互相替代。

## 1. R0 体检表（`已核` 来自 case §2）

| 检查 | 结果 | 判据 | 决定 |
|---|---|---|---|
| 消费者 | 值班问答 agent；只读上下文，无写权限 | 有 owner、有时刻、有拒绝条件 | 可做 R1/R2/R4/R5；不做 R6/R9 |
| 名字/单位 | 3 个任务里 2 个 primary trap 来自单位/别名（`已核`，case §2） | 抽样 ≥20 条，能说出 trap 类型 | 先做 R1 |
| 声明 | 抽 50 条，7 条用到未声明属性（`推测`，case §2） | 未声明属性会导致 checker 误报 | 先补声明 |
| 覆盖 | 200 题抽样 unknown IRI 估计 >20%（`untested`） | 未知 IRI 率可量 | 先补术语，不先做 R4 等级 |
| 执行落点 | 只有 2 条约束有 SHACL，无负例（`已核`，case §2） | 有 target、有负例 | R5 暂缓，先补 shape |

**R0 结论**：`fix_first`。先 R1 + 补声明；R2/R4 排后；R5 暂缓。

## 2. 接口契约（R4）

```text
output: {
  answer: string,
  observations: [
    { kind: "concept_card" | "ask" | "select",
      ref: string,            // iri / query id
      value: string,          // 卡摘要 / entailed|not-entailed|unknown / bindings hash
      source: string }        // 本体版本 + 工具名
  ],
  grounding: "entailed" | "supported" | "related" | "unrelated" | null
}
```

| 字段 | 本场景填什么 | 等级 | 判据 |
|---|---|---|---|
| `answer` | 「P-101 出口压力当前 0.42 MPa」 | `untested` | 答案必须由 observations 支撑 |
| `observations[].kind` | `concept_card` / `ask` / `select` 三选一 | `已核` | 与 R4 的三原语对齐 |
| `observations[].ref` | `pump:P-101` / `q-ask-001` / `q-sel-001` | `untested` | 能指到卡或查询 |
| `grounding` | `supported`（示例） | `untested` | 未校准前只做提示，不自动放行 |
| 预算 | ≤10 actions、≤5,000 **generated** tokens | `已核` | R4 的预算闸 |
| 空观察 | `grounding = null`，不编等级 | `已核` | R4 的 `E=∅` 规则 |

**契约的边界**：它约束格式与声明，不保证语义真值；`grounding` 是模型自评，未校准。

## 3. concept card 样例

```text
iri: pump:P-101
label: P-101 出口压力
definition: 冷却水泵 P-101 的出口压力测点
parents: [pump, pressure_measurement]
children: []
relations: [hasUnit bar, locatedIn pump_house, derivedFrom sensor:PT-101]
comments: 设计值 0.45 MPa；当前值以 DCS 为准
source: P&ID rev C + tag 表 2026-10
```

- 8 字段齐；单卡约 600 字符（≤2k）。
- `definition` 与 `comments` 的区别：前者是本体定义，后者是工程注记；不要把注记写进定义。
- 同名不同物（P-101 vs P101-P）走别名，不合并 IRI。

## 4. 查询与观察样例（文本，不是可执行套件）

| 观察 | 查询/动作 | 期望 | 等级 |
|---|---|---|---|
| 单位 | `ASK { pump:P-101 :hasUnit ?u }` | `bar` | `untested`（未跑） |
| 当前值 | `SELECT ?v WHERE { pump:P-101 :currentValue ?v }` | `0.42` | `untested` |
| 卡 | `DESCRIBE pump:P-101` | 8 字段卡 | `已核`（R4 的三原语） |
| 空结果 | 精确查询 0 行 → BM25 取 5–10 张候选卡 | 候选卡 + 「未命中」标记 | `已核`（R4 fallback 规则） |

**不要**把「查询文本」当「已跑通」；`untested` 就是没跑。

## 5. 账本行

```text
q-001, arm=context, hit=true, tokens=<实测>, latency=untested, rounds=2,
gate=pass, citations=3, span_coverage=0.92, grounding=supported,
snapshot=2026-11-11, notes="R4 样例；latency 未测"
```

| 字段 | 本场景 | 等级 |
|---|---|---|
| `hit/miss` | `hit`（有观察） | `untested` |
| `tokens` | **总** tokens 口径（generated 未单列）；旧均值随 E-03 撤回停用 | `历史` |
| `latency` | `untested` | `untested` |
| `citations` | 3 | `untested` |
| `span_coverage` | 0.92 | `untested` |
| `grounding` | `supported` | `untested`（未校准） |

> 账本行不是「跑分」；它的用途是让 `p_h`、false-veto、单位成本有分母。

## 6. 停线记录

| 指标 | 本场景值 | 停线 | 出处 | 量不出时 |
|---|---|---|---|---|
| 检索率 | `untested` | <50% | 工程建议（O-T05） | 先修检索，不上 R4 |
| 引用率 | `untested` | <85% | 工程建议 | 只做提示，不自动放行 |
| 净修复 | 不适用（R4 不做修复） | — | — | — |
| grounding 校准 | 未做 | 未校准 → 不自动路由 | R4 校准协议 | 只做排序/人工分流 |
| 预算 | 5.8 calls / 9.7k **总** tokens（**历史**，E-03 撤回） | >5,000 **generated** tokens / >10 actions | R4 历史 | 口径不同；新源前不设门槛 |

**结论**：本场景的 R4 只能到 `shadow + 人工分流`；`citation correctness` 没有 recipe，见 [R5 的 judge 分支](../recipes/judgment.md#r5--输出后-checker先超过空结果重试)（40 修好/83 修坏，净修复为负）。

## 7. 未测清单（交稿必填）

| # | 未测 | 为什么重要 | 补它需要什么 |
|---|---|---|---|
| 1 | 引用正确性（引用是否支持结论） | R4 只测「有没有引用」，不测「引用对不对」 | 独立标注 + 判定规则；当前无 recipe |
| 1b | 引用率的分子/分母 | 85% 这个阈值没有口径，无法预注册 | 定义「带 observations 的答案 / 全部答案」并抽检 |
| 2 | grounding 四级校准 | 未校准的等级不能自动路由 | 100–200 条/等级独立标注 |
| 3 | 真实 latency / p95 | 预算闸需要时延 | 一次回放 + 时延分布 |
| 4 | 跨域/多设备 | 单工厂不外推 | 第二域回放 |
| 5 | 本体归属性 | 15/26 来源换词仍成立 | 同任务换「任意结构化上下文」对照 |

> **这张表是产物包的一部分**：填不出未测清单，说明你还不知道自己的证据边界。

## 8. 与 01/03/04 的分工

- 值不值得做 → [01](../../01-capability-status/README.md)。
- 为什么是这些位置 → [03](../../03-mechanism-reference/README.md)。
- 建/用/治一条访问控制链 → [04](../../04-ontology-in-production/README.md)。
- 本页只回答：**一条 recipe 做完，手上应该有什么。**

## 9. 第二个例子：R1 K1（短）

> 目的：证明产物包不是「只有 R4 一份」。R1 的产物比 R4 少，但同样有「填好的长什么样」。

### 9.1 交接

| # | 产物 | 本包在哪 |
|---|---|---|
| 1 | R0 体检表（复用 §1） | 同上 |
| 2 | tag/单位/别名表 | §9.2 |
| 3 | 槽位映射 | §9.3 |
| 4 | K1 回放记录 | §9.4 |
| 5 | 停线记录 | §9.5 |
| 6 | 未测清单 | §9.6 |

### 9.2 tag / 单位 / 别名（3 行样例）

| tag | 单位 | 别名 | 槽位 | 等级 |
|---|---|---|---|---|
| `P-101` 出口压力 | bar | 泵出口压力 / P101-P | `pump.outlet_pressure` | `已核`（case） |
| `T-101` 出口温度 | °C | 泵出口温度 | `pump.outlet_temp` | `已核`（case） |
| `F-101` 流量 | m3/h | 冷却水流量 | `pump.flow` | `已核`（case） |

**判据**：一行一个 tag；别名不合并 IRI，只做查询展开；单位必须与 DCS 一致。

### 9.3 槽位映射

```text
pump:P-101  :outlet_pressure  "0.42"^^xsd:decimal  # bar
pump:T-101  :outlet_temp      "32.1"^^xsd:decimal  # °C
pump:F-101  :flow             "18.5"^^xsd:decimal  # m3/h
```

**判据**：槽位名是本体属性；单位是注释/元数据，不写进字面量。

### 9.4 K1 回放记录

```text
k1-001, arm=context, tasks=3, traps=3, hit=2, miss=1,
delta=+?pp, tokens=?, gate=untested, notes="fixture 3 行；未跑"
```

**判据**：`delta` 未测就写 `?`；不要用 +54.6pp 冒充本域结果。

### 9.5 停线

| 指标 | 本场景 | 停线 | 出处 |
|---|---|---|---|
| K1−K0 primary-trap avoidance | 未测 | < +5pp → 停；≥ +10pp → 过 | [canonical §2](../sections/canonical.md) |
| 别名覆盖率 | 未测 | < 80% → 先补别名 | 工程建议 |
| 单位冲突 | 0（fixture） | > 0 → 先修数据 | 工程建议 |

### 9.6 未测清单

| # | 未测 | 补它需要什么 |
|---|---|---|
| 1 | 本域 K1−K0 增益 | 3 个任务回放 + trap 标注 |
| 2 | 别名覆盖率 | tag 表全量 + 人工抽检 |
| 3 | 跨域 | 第二个域 |

> 第二份包比第一份短，这是正常的：**R1 的产物本来就少**；不要为了对称硬凑。
