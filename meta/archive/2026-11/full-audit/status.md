> **历史快照（2026-11-08/09）**：已归档，不再维护。现行规则见 `meta/README.md`，当前状态见 `meta/state.md`。文中的计数与结论可能已被后续修复取代。

# 全审 checkpoint（2026-11-08）

> 目的：把当前工作收口，停止“越修越宽”的串行循环。后续按子领域推进，不再在一个上下文里同时拖 22 digest + 20 topic。

## 一、硬指标

| 项 | 状态 |
|---|---|
| digest E3+ | **22/22** |
| L3 E4 | **12/12** |
| topic A4 段落 | **20/20** |
| **G-X 吸收** | **20/20 pass** |
| 链接 | **1,605 / 0 broken** |
| 人类抽检 | 未做（静默模式，Phase 4 待） |
| Phase 3 价值链 | **8 个 V3 已设计，未跑** |
| Phase 4 双 critic | **digest 4/5 pass + CAI explained-residual；topic 5/5 pass；代办 5+5** |
| Phase 5 报告 | **条件式 report/no-go 已写** |

## 二、G-X 通过（20）

T-01…T-20 全部 pass（含 T-05 evidence、T-16 mechanism、T-17 failure-attribution、T-18 trace、T-19 metrics、T-20 feasibility）。

## 三、未通过 / 未做（0）

### （历史）T-05 evidence：已 pass

已修：span 无源、成本单位、12k/5k 预算、8k/262k 混用、E=∅ 语义、SPARQL/临床边界、name-linking 200。
残留（critic 仍 fail）：
1. `mechanism.md:66` 等级通胀条说“论文未测分布”，与 digest §4.3 的 entailed+supported 70.0%/53.2% 冲突；应改为“论文给了分布，但没测通胀/校准”。
2. `findings.md:50` 把 12k total 与 5k generated 说成“冲突”；应写“不同量：5k generated 是论文，12k total 是工程闸（推测）”，stop 保留两者。
3. Test 2 OQ 23.2% 与两个例外未写进 F1/README；`整体最优/优于文本 RAG` 过度概括。

**处理**：这 3 条是一次小修，不再开新循环；下次 T-05 子领域一次修完并复跑。

### （历史）T-16…T-20：已 pass

G-X 初始 fail，尚未逐条修。它们是 06 measure 子领域，应一起做，不要散在 20 个 topic 的上下文里。

## 四、为什么越修越慢

1. **G-X 是 22×20 的交叉核对**：每修一个 topic 就触发一次 5-agent 复核，复核又产生新 residue；上下文线性膨胀。
2. **三种工作混在一起**：digest 内容审计、topic 跨页一致性、G-X 吸收核对；它们的验收标准不同，却在一个 goal 里串行。
3. **修一个点会牵动跨页 claims/README/conclusions**：agent 被限制只改子目录，残留只能主控回改，形成“修 topic → 发现父页旧句 → 再修父页”的长尾。
4. **证据等级语义细**：同一句“已核/推测”在不同页有不同含义，critic 每次都能找到新的边界。

## 五、建议：按子领域推进（6 个 workstream）

| 子领域 | topics | 当前 | 下一步 |
|---|---|---|---|
| **A. 01 constraint** | action-gate、commit-gate、reasoning-gate | 3/3 G-X pass | 只做跨页 claims/conclusions 回写 |
| **B. 02 judgment** | checker、evidence、calibration | 2/3 pass；evidence 暂停 | **先收 evidence 3 条**，再复跑 B |
| **C. 03 knowledge** | compilation、projection | 2/2 pass | 只做父页 claims/README 回写 |
| **D. 04 state** | memory、identity、determinism | 3/3 pass | 只做父页 claims/README 回写 |
| **E. 05 produce** | generation、refinement、representation、lifecycle | 4/4 pass | 只做父页 claims/README 回写 |
| **F. 06 measure** | mechanism、failure-attribution、trace、metrics、feasibility | 1/5 pass | **整组 5 个一起修**，再复跑 F |
| **G. 跨页** | conclusions/THESIS/sources/value trace | 未做 | 各子领域 pass 后统一回写 |

### 推进顺序

1. **收 B**：evidence 3 条 residual（半小时级），复跑 T-05；B 全 pass。
2. **收 F**：5 个 topic 一起修，一次复跑；不要逐个开循环。
3. **跨页回写**：A–F 各自把 claims/README/conclusions 的旧句改掉；每派一次，不跨派。
4. **价值链**：只对 8 个 A4 做 V2/V3，不再 20 个全做。
5. **Phase 4**：5+5 人类抽检 + 双 critic；Phase 5 报告。

### 工作方式（降低上下文）

- **一个子领域一个 goal/round**；主控只读该子领域的 3–5 个 topic + 对应 digest。
- **每个子领域一个 status 文件**（`meta/full-audit/subdomains/<id>.md`），主上下文不再堆 20 个 agent 的长输出。
- **修-复跑最多 2 轮**；第 2 轮仍有 residual，标 `explained-residual` 并写“为什么不适用/谁负责”，不再无限追。
- **digest 冻结**：除非 G-X 发现事实冲突，不再改 digest；否则 scope 会再次膨胀。
- **父页回写集中做**：agent 只改子目录，主控按子领域一次性改 claims/README/conclusions。

## 五之二、跨页回写（2026-11-08）

- 01/03/04/05 四派已回写 claims/README/sources/frontier：
  - 01：F5/F6 旧归因、L9 NoRev、L8 menu/τ、L10 ledger、L11 三规模；commit-gate E-05 错挂已解。
  - 03：E-12 旧口径在派内已降级；projection/compilation 计数与 F1–F11 对齐；03-L1/L8/L9 收窄。
  - 04：04-L1/L3/L4/L5/L7 拆等级；3 period 与 10 月度拆分；merge precision 90% 降为建议。
  - 05：medium 非全 mixed、generation E-05 错挂修正、L8/L9 新增、representation 消费位置降推测。
- 仍待统一：conclusions 的 E-07/E-12/E-16/E-18、根 README/topics README 的派摘要、digest 的旧回链；下一轮集中改 conclusions，不动派内。

## 五之三、人类抽检包（2026-11-08）

- [human-review.md](./human-review.md)：5 digest + 5 topic，60–90 分钟，只判断“值不值得实施”。
- 重点：CAI、N&D、Evontree；action-gate、feasibility。
- 人类完成前，report 保持 no-go。

## 六、当前可以签什么

- 可以签：digest E3/E4、topic A4 段落、G-X 20/20、研究档案内部使用。
- **不能签**：对外交付/客户收益承诺；CAI 仍 explained-residual，人类 5+5 未做。
- 下一步只修 R-1/R-2/R-3（CAI/N&D/Evontree）+ 人类 5+5；其余不回头。

## 七、文件

- 本 checkpoint：[status.md](./status.md)
- G-X 问题：[gx-issues.md](./gx-issues.md)
- 吸收矩阵：[absorption-matrix.md](./absorption-matrix.md)
- 计划：[plan.md](./plan.md)
- 索引：[README.md](./README.md)

## 八、Blocked（2026-11-08）

- **阻塞条件**：人类 5+5 抽检未执行；AI 不能冒充人类 reviewer。
- 机器可核项已完成：22/22 E3、12/12 E4、20/20 A4、G-X 20/20、8 V3 设计、E/L 0 悬空、链接 1,628/0。
- CAI 的 residual 需要真实 `$/文档、人日费率、sprint 工时`，属组织数据，不是文本能补。
- 解除条件：用户或指定 reviewer 完成 [human-review.md](./human-review.md)，回填 pass/fail/不确定与 go/no-go。
- 解除后：按结果把 report 改成条件 go，或把 fail 项写进对应 frontier；不再重开全审。
