---
status: draft
updated: 2026-11-13
---

# Schema：全仓字段与枚举的唯一来源

> **本页是全仓字段、枚举、证据阶梯与编号前缀的唯一权威。** [conventions](./rules/conventions.md)、[checklist](./workflow/checklist.md)、[source-types](./rules/source-types.md) 与模板只解释用法，**不重复定义枚举**。新增字段或枚举值必须先过 [ADR](../adr/README.md)，再改本页与消费者（[ADR 0012](../adr/0012-instruction-layer-single-home.md)、[ADR 0016](../adr/0016-unify-meta-structure.md)）。

## 0. 两条硬规则

1. **机器字段只放规范值。** `status`、`source_type`、`reading`、`provenance`、`quality`、`admission`、`evidence_role`、`execution_form`、`seam`、`plan_status`、`deliverable_status` 等字段不得写复合斜杠、装饰性括号或自造词。
2. **不在正文里造新值。** 需要新字段或新枚举值 → 先写 ADR → 改本页与 `meta/tools/check_repo.py` → 同步消费者。

## 1. 文档与来源字段

| 字段 | 用在哪 | 取值 | 含义 |
|---|---|---|---|
| `status` | 所有文档（ADR 除外） | `seed` / `draft` / `stabilized` / `superseded` | 文档成熟度，不代表篇幅或完成度 |
| `updated` | 所有文档 | `YYYY-MM-DD` | 最后一次实质修订；搬家、改链接、批量重排不算 |
| `home` | 源卡 / digest | `topics/01-constraint` … `topics/06-measure` | 主归位派 |
| `subtopic` | 源卡 / digest | `<子主题目录名>` | 主归位子主题 |
| `also_supports` | 源卡 / digest | `[<子主题1>, ...]` | 一源喂多子主题时的其余支持目标 |
| `source_type` | `src/` 卡片 | `paper` / `preprint` / `blog` / `engineering` / `standard` / `talk` / `survey` / `open-source` | 素材类型；证据天花板见 [source-types](./rules/source-types.md) |
| `standing` | `src/` 标准卡 | `normative` / `informative` | 源位阶：规范性（可定词、定合格性）/ 资料性（只佐证）；`signal` 归 `admission` |
| `reading` | `src/` 卡片 | 论文/材料：`未读` / `综述级` / `摘要级` / `精读` / `已消化`；代码：`未读` / `已读代码` / `已跑通` | 读到什么程度；**不是证据等级** |
| `provenance` | `src/` 卡片 | 论文/材料：`原文正文` / `原文摘要` / `综述转述` / `未核`；代码：`一手代码` / `一手文档` / `未核` | 证据来自哪里 |
| `quality` | `digest.md` | `A` / `B` / `C` | 证据强度粗分：A 多基准/真实部署/消融（代码：有测试且有生产/基准）；B 单基准/单域/有限评估（代码：有测试但单路径）；C 概念/模拟/小样本/无量化（代码：只读代码/无测试） |
| `evidence_role` | 源卡 | `execution-test` / `mechanism-only` / `harness-evidence` / `boundary-ruler` / `unclear` | 对中心问题提供哪类证据 |
| `execution_form` | 源卡 | `engine` / `compiled` / `context` / `label` / `none` / `unknown` | 本体以什么形态被执行（第四轴） |
| `admission` | `src/` 卡 | `admitted` / `admitted (probation)` / `signal` / `excluded` | 五门准入判定；没有就是未判；见 [CHARTER §4](../CHARTER.md#4-素材准入material-gate) |
| `gate_checked` | `src/` 卡 | `YYYY-MM-DD` | 最后一次过门日期 |
| `impact_evidence` | `src/` 卡 | `I1: ...; I3: ...` | 逐条列独立信号（`I1`–`I5`）；`admitted` 必填 |
| `liveness` | `src/` 卡 | 文本 + 日期 | 最近一次活动及日期（G2 证据） |
| `provenance_type` | `src/` 卡 | `standard-body` / `academic` / `foundation` / `community` / `company` / `individual` | 来源结构，决定 G4 |
| `reliability` / `impact` | `src/` 论文卡 | `high` / `medium` / `low` | 可靠性/影响粗分，不替代 `impact_evidence` |
| `updates` | 源卡 / digest | 路径列表 | 修正旧判断时必须回改的主题页 |

### 1.1 `src/open-source/` 专用字段

| 字段 | 取值 | 含义 |
|---|---|---|
| `commit` / `release` / `license` | SHA 或 tag / tag / SPDX | 版本与许可；不 pin commit 不算入库 |
| `scan_date` / `stars_at_scan` / `last_push` | `YYYY-MM-DD` / 数字 / `YYYY-MM-DD` | 扫描快照；star 只作影响力参考，不算信号 |
| `ontology_role` | `core` / `adjunct` / `none` / `unclear` | 本体在项目里的地位 |
| `seam` | `action-gate` / `evidence` / `checker` / `commit-gate` / `memory` / `determinism` / `read-path` / `supply` / `reasoning` / `training` / `none` | 六时刻 + 轴外位置（初判，定级在 digest） |

## 2. 状态与阶段字段

| 字段 | 用在哪 | 取值 | 判据 |
|---|---|---|---|
| `status` | 通用文档 | `seed` / `draft` / `stabilized` / `superseded` | `seed` 结构在、内容开始、未交叉核对；`draft` 论证完整、至少一次交叉核对；`stabilized` 结论稳定且经独立复现或外部签核（当前无文档达到）；`superseded` 保留指针 |
| `deliverable_status` | `deliverables/` | `draft` / `stable` / `frozen` | 交付物阶段 |
| `plan_status` | `meta/plans/` | `active` / `completed` / `abandoned` | 计划专用；**不要用文档 `status`**；全仓同时 `active` ≤ 1 份 |
| `experiment_status` | 历史或仓外 `EXP` | `未开始` / `设计中` / `运行中` / `已完成` / `已放弃` | 实验阶段；仓内不建实验目录 |

> **文档状态与阅读进度是两件事。** 一张 `reading: 摘要级` 的卡，其 `status` 通常是 `draft`；不要写 `status: 摘要级`。

## 3. 判断与证据阶梯

### 3.1 证据等级（四档）

| 等级 | 含义 | 出处要求 |
|---|---|---|
| **已证** | 独立复现（本仓库不设实验目录） | 需仓库外复现记录 + `EXP-xxx` 指针 |
| **已核** | 读过一手原文（至少摘要）或一手代码 | 需卡片/digest/原文链接或 `commit` + `file:symbol` |
| **推测** | 有线索、未核原文，或来自二手转述 | 标注来源，写清为何未核 |
| **存疑** | 有反例，或证据互相矛盾 | 必须写出反例或冲突双方 |

- **默认是推测。** 没标等级的论断，一律按 `推测` 处理。
- **证据等级 vs 接地等级**：接地等级是已移出语料里的概念（entailed / supported / related / unrelated），描述输出与本体的关系；证据等级是本仓库对主张的置信度。见 [GLOSSARY](../GLOSSARY.md#证据)。
- 正文写法映射：`一手正文` / `一手摘要` / `一手代码` → `已核`；`转述` / `待核` → `推测`；`反例` / `冲突` → `存疑`。

### 3.2 阅读深度（L1/L2/L3）

| 档 | 读到哪 | digest 目标长度 | 用途 |
|---|---|---|---|
| `L1` | 摘要 + 结论 + 局限 | 100–240 行 | 一页判断；只作边界/候选证据 |
| `L2` | 正文主要节 + 关键表 | 160–260 行 | 标准消化；可进子主题 `findings` |
| `L3` | 正文 + 关键表/图 + 附录按需 | 250–360 行 | 深消化；可支撑 `E`/`L` 核心证据 |

> 长度是目标，不是门：**自包含优先**。`L1/L2/L3` 是阅读深度，不是证据等级，也不是 `status`。

## 4. 编号前缀

| 前缀 | 含义 | 唯一落点 |
|---|---|---|
| `E-xx` | 跨派结论 | [topics/conclusions.md](../topics/conclusions.md) |
| `01-L<n>` … `06-L<n>` | 派内局部判断 | `topics/<派>/claims.md` |
| `Q-xx` | 存疑条目 | [topics/conclusions.md](../topics/conclusions.md) |
| `C-xx` | 冲突条目 | [topics/conclusions.md](../topics/conclusions.md) |
| `O-<X>nn` | 证据硬对象（`C/F/T/M/N/R/P`） | [topics/objects.md](../topics/objects.md)（只作地址，不替代 E） |
| `F<n>` / `G<n>` / `N<n>` | 子主题内发现 / 缺口 / 下一步 | `topics/<派>/<子主题>/findings.md` · `frontier.md`（局部唯一） |
| `EXP-xxx` | 仓库外验证指针 | 仅引用指针，仓内不建实验目录 |

## 5. 机器校验规则（由 `check_repo.py` 强制）

- 所有枚举值（`status`、`source_type`、`reading`、`provenance`、`quality`、`experiment_status`、`deliverable_status`、`seam`、`execution_form`、`evidence_role`、`admission`、`standing`、`plan_status`）必须落在 §1–§2 合法集合内。
- 论文/开源/网页 `admitted` 卡必须具备 `admission`、`gate_checked`、`impact_evidence`、`liveness`、`provenance_type`；论文/开源日期须 ≥ `2026-06-01`（在役标准例外除外）。
- 现役 `E-xx` 行必须同时包含一句 `**做法` 与指向 `mechanism` / `read-path` / `execution-forms` 等程序页的链接；已撤回 `E-xx`/`L-xx`/`O-xx` 与黑名单 ID 不得无 caveat 出现在活跃正文。
- 每份 `deliverables/NN-*/` 必须同时存在 `SCOPE.md` 与 `README.md`。
- `meta/plans/` 下 `plan_status: active` 至多 1 份。
- `meta/status/state.md` 里的 md 文件数、论文/开源/材料卡计数、`execution_form` 分布、结论等级数、硬对象数须与文件树一致。
