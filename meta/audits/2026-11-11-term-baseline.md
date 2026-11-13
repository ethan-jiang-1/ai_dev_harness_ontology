---
status: draft
type: term-baseline-audit
updated: 2026-11-11
scope: 06-measure 试点 + v1 词表冲突
---

# 术语基线审计：06-measure 试点（2026-11-11）

> 依据 [ADR 0011](../../adr/0011-source-standing-and-term-baseline.md) 与 [核心计划第 8 步](../archive/2026-11/plans/2026-11-11-core-plan.md)。**只记录术语用法与处置，不新增判断。**
>
> 词表本体在 [meta/status/term-baseline.md](../status/term-baseline.md)（v0 10 词 + v1 29 词）；N/I/S 与标准边界见 [topics/trunk.md](../../topics/trunk.md)。

## 1. 试点范围

| 文件 | 查什么 | 结果 |
|---|---|---|
| [06-measure README](../../topics/06-measure/README.md) | 三句主张与四把尺子里的裸词 | 0 冲突；「判定器」用法与 v1 `narrower` 一致 |
| [06-measure claims](../../topics/06-measure/claims.md) | 17 条 L 的定义词 | 0 冒充行业标准；2 条 L 用到「接地」（`local`，已解释） |
| [metrics/coverage](../../topics/06-measure/metrics/coverage.md) | 「覆盖率」是否被写成百分比/召回率 | 0 冲突；明确「不合成百分比」 |
| [conclusions](../../topics/conclusions.md) 的 06 相关行 | 是否把 `local` 词写成行业术语 | 0 冲突 |

## 2. 逐条判定（只列有术语含义的行）

| 行 | 原词 | 判定 | 处置 | 是否冲突 |
|---|---|---|---|---|
| 06-L1 | 「本体预测」 | 描述句，非术语 | 保留；L1 已 `withdrawn` | 否 |
| 06-L6 / 06-L7 | 「本体接地失败」「五角色 + 七变量」 | 「接地」`local`；框架 `local` | 保留机制描述；两条 L 已 `withdrawn`，不得当预测器 | 否 |
| 06-L13 | 「落地经济学」 | `local` 综合词 | 只在本仓库语境用 | 否 |
| 06-L15 | 「覆盖率」 | 与 GLOSSARY `local` 定义一致 | 保留；对外链 coverage 页 | 否 |
| 06-L16 / 03 measurement | 「任务账 / 风险账」 | **裸词**（GLOSSARY 无条） | v1 补判 `local`；首现解释；GLOSSARY 词条待下一版补 | **是（已补判）** |
| 06 README | 「判定器」 | SHACL 只定图校验 → `narrower` | 保留；不写成「SHACL 判定器」 | 否 |

## 3. 处理与后续

1. **无术语冲突需要撤回判断**：06-measure 没有把 `local` 词写成行业标准；没有 `divergent` 级冲突。
2. **补一条裸词**：「任务账 / 风险账」进 [term-baseline](../status/term-baseline.md) §5/§6，判 `local`；GLOSSARY 词条待 v1.1 补。
3. **复跑方法**（下一轮按派抽样）：

```bash
# 交付物里的裸词：定义行既无 N 也无 local
grep -rn "（N:\|（local" deliverables --include=*.md | wc -l
# 借权威：把 local 词写成行业标准
grep -rn "行业标准\|行业共识\|成熟度标准" deliverables topics --include=*.md \
  | grep -v "不是\|不得\|不要\|禁止\|非标准\|撤回\|历史"
```

4. **判定**：试点通过——06-measure 的术语用法可作为 v1 之后其他派的样板；本条审计不设整改 deadline（没有外部资产依赖）。

> 本页是审计记录，不是新 E/L；结论只关于「词怎么用」，不关于「判断对不对」。
