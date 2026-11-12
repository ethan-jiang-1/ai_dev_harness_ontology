---
status: draft
type: trunk-wiring-report
updated: 2026-11-11
scope: 核心计划第 7 步（01→02→03→04 定义段接规范主干）
---

# 接线报告：把规范主干接进交付物（2026-11-11）

> **这是核心计划第 7 步的产出，也是第 8 步术语 v1 的入口。** 只记录「定义句接到哪、怎么验、还剩什么」，不新增 E/L。
>
> 主干索引：[topics/trunk.md](../../topics/trunk.md)；逐词判定：[meta/status/term-baseline.md](../../meta/status/term-baseline.md)。

## 1. 接线口径

| 标记 | 含义 | 用在哪 |
|---|---|---|
| `（N: 标准名）` | 有规范性锚：标准/权威本体**只定「这个词什么意思、什么叫合格」** | 定义句、术语页、首现 |
| `（local）` | 本仓库工作词：没有标准锚，必须首现解释 | 机制词、排序词、指标 |
| `E-xx` | 资料性证据（I 层）：效应量、代码锚、失败模式 | 效应句 |

**三条硬规则**（与 [trunk §3](../../topics/trunk.md) 一致）：

1. 标准只定词，不撑效果；效应只能引 E-xx。
2. `local` 不得写成「行业标准/共识」；首现必须解释。
3. 论文条件编号（K0–K4）只作出处/回查，不进定义句主位。

## 2. 逐页接线

| 页 | 改了什么 | N 锚 / local |
|---|---|---|
| [START](../../deliverables/START.md) §2 | 三词表加「词源」列与读法说明 | 本体 `N: ISO/IEC 21838-1`（broader）；harness / 接缝 `local` |
| [01 README](../../deliverables/01-capability-status/README.md) | 术语基线段改成「术语来源（读法）」；三条判断后加「词源速查」 | 本体/TLO、约束/校验、ODRL/XACML 有 N；领域本体、知识图谱、语义层、接地、动作闸、落盘授权、A/B/C/D、gap 为 `local` |
| [01 术语 §0](../01-capability-status/02-sections/90-glossary.md#term-sources) | 新增 18 行来源表（v0/v1 的词在 01 的首现） | 10 张标准卡全部落到词；其余 `local` |
| [01 map](../01-capability-status/02-sections/02-map.md) | 判定口径表后加来源注；§2.2 计数后加词源注；执行形态标 `local` | SHACL/OWL 2 Profiles 有 N；A/B/C/D、读路径、动作闸、落盘授权 `local` |
| [01 capabilities](../01-capability-status/03-capabilities/README.md) | 顶部词源；§3.4/§3.6/§3.8/§3.9 加词源句 | SHACL/SHACL-AF/OWL 2 Profiles 有 N；接地、动作闸、读路径、commit gate `local` |
| [01 K 页](../01-capability-status/02-sections/92-k-ladder.md) | K 的 `local` 判定改成标记形式；§2 表加「本表读法」 | K0–K4 `local`（论文条件，非术语） |
| [01 decision-record](../01-capability-status/02-sections/09-decision-record.md) | 顶部加词源句 | 同 README；判定仍走证据 |
| [02 README](../../deliverables/02-engineering-playbook/README.md) | 证据等级段后加词源 | 本体/TLO、SHACL、ODRL/XACML、ODCS 有 N；接缝/形态/动作闸/读路径/落盘/接地 `local` |
| [02 术语 §0](../02-engineering-playbook/02-sections/90-glossary.md#term-sources) | 新增 14 行来源表 | 含 OMG Commons、ODCS、GB/T 两标 |
| [02 R4/R5](../02-engineering-playbook/03-recipes/04-judgment.md) | 顶部加词源 | SHACL/SHACL-AF 有 N；接地、catch/FA `local` |
| [02 R6/R8/R9](../02-engineering-playbook/03-recipes/06-constraint.md) | 顶部加词源 | ODRL/XACML 只到表达/架构；可逆性、动作闸、读路径、落盘 `local` |
| [02 R10/R11](../02-engineering-playbook/03-recipes/10-offline-and-obda.md) | 顶部加词源 | SHACL/SHACL-AF、OWL 2 Profiles 有 N；效应回 E-20 |
| [02 接口附录](../02-engineering-playbook/05-appendices/01-interfaces.md) | 加数据契约词源 | 数据契约 `N: ODCS v3.1.0`；字段名是 `local` 工程配方 |
| [03 README](../../deliverables/03-mechanism-reference/README.md) | 顶部加词源 | 六位置/接缝/强度/覆盖率/形态 `local` |
| [03 术语 §0](../03-mechanism-reference/02-sections/90-glossary.md#term-sources) | 新增 13 行来源表 | 含 OMG Commons、XACML、SHACL-AF |
| [03 checker](../03-mechanism-reference/03-positions/04-checker.md) | 顶部加词源 | SHACL/SHACL-AF 有 N；checker/catch/FA/接地 `local`；E-02 仍 withdrawn |
| [03 action](../03-mechanism-reference/03-positions/05-action.md) | 顶部加词源 | ODRL/XACML 只到表达/架构；可逆性、min φ、τ `local`；E-04/13/16 仍 withdrawn |
| [03 commit](../03-mechanism-reference/03-positions/06-commit.md) | 顶部加词源 | XACML/ODRL 只到判定架构；commit gate/三段式 `local`（概念架构） |
| [03 memory / evidence](../03-mechanism-reference/03-positions/02-memory.md) | 顶部加词源 | 记忆/接地 `local`；标准不定义机制 |
| 04 README | 内码后加词源 | 本体/SHACL/ODRL/XACML/GB-T/ODCS 有 N；TBox/ABox、principal、level、skip、leak oracle `local` |
| 04 术语 §0 | 新增 12 行来源表 | 数据分级/个人信息/数据契约/OWL 有 N |
| 04 build A.3 | TBox/ABox 段加词源 | TBox/ABox `local`；类/属性语义 `N: OWL 2 Profiles` |
| 04 govern C.1/C.2 | C.1 后加词源；C.2 `skip` 规则加标记 | 分级/个人信息有 N；level 1–4、skip、principal `local` |

## 3. 验收（可复跑）

```bash
cd /Users/bowhead/ai_dev_harness_ontology

# 1) 四个术语页都有 §0 与 term-sources 锚
grep -l "term-sources" deliverables/*/sections/glossary.md

# 2) 主路径定义页都有「词源」
grep -l "词源" deliverables/START.md deliverables/0*/README.md \
  deliverables/01-capability-status/capabilities/README.md \
  deliverables/02-engineering-playbook/recipes/*.md \
  deliverables/03-mechanism-reference/positions/*.md \
  deliverables/04-worked-example/body/*.md

# 3) 没有「标准证明效果」的句子（命中都应是否定句/规则说明）
grep -rn "ISO.*证明\|SHACL.*证明\|ODRL.*证明\|XACML.*证明\|GB/T.*证明" \
  deliverables --include=*.md | grep -v "不\|不得\|不能\|不要\|非"

# 4) 自检
python3 meta/tools/check_repo.py
```

**结果**：见 §4。`check_repo` 每批通过（当前 440 md）。

## 4. 审计结果

### 4.1 机械审计（2026-11-11，仓库内 grep + check_repo）

| 检查 | 命令 | 结果 |
|---|---|---|
| 四个术语页都有 §0 与锚点 | `grep -c term-sources deliverables/0*/sections/glossary.md` | 4/4 = 1 |
| 主路径定义页都有「词源」 | 对 START/四个 README/capabilities/4 条 recipe/接口附录/5 张位置卡/04 build+govern 逐个 grep | 22/22 页 ≥1 |
| 标准当效果证据 | `grep -rn "ISO.*证明\|SHACL.*证明\|ODRL.*证明\|XACML.*证明\|GB/T.*证明\|ODCS.*证明" deliverables` | 0 处（命中都是规则说明/本报告） |
| 借权威 | `grep -rn "行业标准\|成熟度标准\|行业共识" deliverables \| grep -v "不是\|不得\|不要\|禁止\|非标准\|撤回\|历史"` | 0 处真实（k-ladder 否定表、_plans 历史稿） |
| 撤回 E 当结论 | scan-report §2 命令 | 0 处 |
| 坏链/坏锚/未定义 ID | `check_repo` | 0 |
| 定义段落的页都有来源注 | `grep -rl "定义为\|是指\|指的是\|所谓" deliverables/0* \| xargs grep -L "词源\|term-sources"` | 0 个无来源页 |
| 文件数 | `check_repo` | 442 md（10 论文 / 8 开源 / 11 材料卡） |

### 4.2 代理冷读（第 9 步，非真人）

- 第一轮 68/100，抓到 **2 处口径冲突**（START「只记一句」vs 01「不能承诺」；map §2.2 等级列混装 `gap`/`设计`，读成「gap=C」）。
- 修复后第二轮复核 **86/100**，再补 3 处：`gap` 收窄为「曾有 E、被撤回」、#14「从未有 E 的设计提案走 C」写明、START 两个裸词就地解释。
- 详细记录：[cold-read](./2026-11-11-cold-read.md)。

### 4.3 验收判定

| 核心计划验收 | 结果 |
|---|---|
| 每个定义后有 `N:标准名` 或 `local` | **过**（四个术语页 §0 全覆盖；正文定义页 22/22 有词源注；冷读未再报漏标） |
| 没有「标准证明效果」 | **过**（机械扫描 0，冷读未发现） |
| `S` 不出现 | **过**（交付物无 `signal` 当证据；frontier 之外的 S 未进正文） |
| `trunk §5.1` 与实际页面一致 | **过**（抽查 SHACL/ODRL/GB/T 43697 三行；冷读未报不一致） |
| `check_repo` 通过 | **过**（442 md） |

## 5. 已知限制

1. **只接定义/首现，不重写章节**：正文的机制描述、步骤、验收未动；这是有意的（核心计划「不为接线重写章节」）。
2. **`N` 只到摘要级**：ISO/IEC 21838 的条款号仍是 `待核`；GB/T 两标与 ODCS 的字段级条款未逐条核。
3. **`local` 仍是多数**：40 词里只有 2 个 `standard` 锚 + 2 个 `narrower` 标准义；这不影响使用，但对外文档必须首现解释。
4. **中文输出口径**：`（N: …）` / `（local）` 是给人看的标记，不参与 `check_repo` 的枚举校验；漏标靠本报告的 grep 与人工审计兜底。

> 本页是工作记录，不是交付正文；不构成 E/L。
