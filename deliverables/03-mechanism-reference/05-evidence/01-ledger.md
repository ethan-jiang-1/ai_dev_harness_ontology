---
status: draft
deliverable_status: draft
updated: 2026-11-11
section: evidence-ledger
evidence: [E-01, E-02, E-03, E-04, E-05, E-06, E-07, E-08, E-09, E-10, E-11, E-12, E-13, E-14, E-15, E-16, E-17, E-18, E-19, E-20, E-22, C-03, C-04]
---

# 证据台账：每条 E 支持哪个位置

> 03 的每个规范句都要能回到这里。**E 是证据，不是位置**；同一条 E 可以支持多个位置，也可以只作边界证据。
>
> **2026-11-11 证据重置**：E-02/E-03/E-04/E-06/E-10/E-11/E-13/E-16/E-26 已 `withdrawn`；本页保留行只作回查，不再作为结论。受影响位置：evidence/checker/action 转 gap；context 仍由 E-12/E-14 支撑。
>
> 等级只有「已核 / 已核（代码）/ 推测 / 存疑」；本仓库没有「已证」。C 是冲突/方法论条目，不是等级。

## 1. 按位置

| 位置 | 主证据 | 边界证据 | 不能用的证据 |
|---|---|---|---|
| context | E-12、E-14 | E-01、E-08 | E-04/E-02（均已撤回，只作历史） |
| memory | E-05、E-17 | E-18（噪声） | E-12（知识供给）、E-03（已撤回，只作历史） |
| evidence | **gap（E-03 撤回）** | — | E-01（工件无增益） |
| checker | E-20（代码级：三态/结构检查）；**E-02 撤回** | — | E-04（动作）、E-15（审批） |
| action | **gap（E-04/E-13/E-16 撤回）**；E-15 仅参照 | E-18（噪声） | E-02（checker）、E-12（供给） |
| commit | E-20（否定性） | commit-gate 概念架构（非 E；源已移出） | E-04/E-02（均已撤回） |
| read-path | E-20 / E-22 | 三态接口见 E-20（E-02 已撤回） | E-04（已撤回）、E-15（审批） |
| determinism | 无 E | E-17（跨轮，不是跨运行）、E-18（噪声） | E-05（跨期身份） |

## 2. 逐条

| 编号 | 等级 | 一句话 | 支持的 03 位置/命题 | 不能证明 |
|---|---|---|---|---|
| E-01 | 已核 | 强检索 harness 下，被测量的结构化工件在 FRAMES 上无准确率增益；PageIndex 大纲退化；ontology `not measured` | context 的边界；C-04 | 本体无增益；可外推到所有工件 |
| E-02 | 已核 · **withdrawn** | 三来源 catch/FA 各有偏向；curated precision 仅略优于随机；空结果重试是关键基线；judge 修坏多于修好 | checker；evidence 的口径边界；M4 | 部署 precision；false-veto；跨域；语义错 |
| E-03 | 已核 · **withdrawn** | 强制接地等级平均最优；Tests 1–2 +10–15pp；等级是模型自评；检索是主瓶颈 | evidence | 形式保证；等级校准；句级 span |
| E-04 | 已核 · **withdrawn** | 旧格数/改善数停用；retail/强模型回退；T1-only ≈ blanket veto；结构贡献未隔离；false-veto 未测 | action；C-03；M1/M3 的边界 | 结构判据有效；reward 低估；合法意图误拦 |
| E-05 | 已核 | 本体做对齐/印证；alias CMR +7.8–12.1pp；token −40.3% | memory/identity | 长期污染；跨运行；通用域；registry 净效应 |
| E-06 | 已核 · **withdrawn** | 本体接地类失败多来自工作流（输入/接地/模板/校验/修复）；语法通过≠语义充分 | 工作流背景；P2；failure attribution | 失败分布；跨域量化 |
| E-07 | 已核 | 形式化器存在 solver-like behavior：轨迹里算出答案，程序只复述 | 过程尺子；formalization 边界 | 本体增益；所有任务 |
| E-08 | 已核 | 导航树是唯一被测出正收益的工件：证据充分 −91%，不充分 +1.9%，平均 −38% | context 的编译；RQ5 | 准确率提升；无条件省 token；本体形态 |
| E-09 | 已核 | SLB 规模与干预：85% traces、24% token；placeholders 减 97% 而不损准确率 | 过程尺子；determinism 的“错误继承”边界 | 本体增益；所有形式语言 |
| E-10 | 已核 · **withdrawn** | 本体预测机制上可干预，但无法与类别辅助信息干净分离 | 06 mechanism；内部本体不干净 | harness 执行；位置效应 |
| E-11 | 推测 · **withdrawn** | 训练好的检索嵌入中，前缀维度与分类法粒度对齐 | representation 边界 | 任何执行/位置结论 |
| E-12 | 已核（分数）/存疑（排序） | 投影文本 pooled 最高但非普适；K0→K1 +54.6pp、K1→K2 +19.8pp；单工厂 9 任务 | context；P1b/P1c；M1 的形态半 | 跨域排序；深度本体；文本永远最好 |
| E-13 | 已核 · **withdrawn** | 约束收益可能随基线能力升高而缩小；六点拟合（数值停用） | action 的能力边界 | 预测曲线；零交叉阈值；部署规则 |
| E-14 | 已核 | 编译盈亏平衡是条件性的：`p_h > 2%`、`p_min = 2% + c/(0.929Q)`；平均 −38% 是混合；配对时延约 3× | context 的经济学；RQ5 | 普适 token 节省；本体增益 |
| E-15 | 已核 | CASEL 模拟 HSR 14.75→7.02%、审批 8.7%；最低 HSR 4.38%；无本体变量 | action 的审批/分配；M4 | 本体增益；审批疲劳；所有方法同 menu |
| E-16 | 已核 · **withdrawn** | 约束形式决定天花板/护栏；三值条件 + revision 提高成功率、减少无效干预 | action/reasoning | 安全保证；真实工厂；所有知识源 |
| E-17 | 已核 | 记忆是状态不是事实集合；Acc@complete +11.5/+31.2；去掉状态层掉点；需训练信号 | memory | 跨模态；无训练信号；跨运行；形式保证 |
| E-18 | 已核 | agent 评测应把配置当系统变量；54% 方差来自重复同一配置的 run-to-run 噪声；信息 > 模型/预算 | measurement 的噪声地板；M1/M5 | 本体增益；跨域常数；排除 memory/multi-agent |
| E-19 | 推测 | 机制是否值得落地取决于位置×成本×使能条件，不是本体质量 | 03 的横切判断；RQ5 | 任何单机制的效应量 |
| E-20 | 已核（代码） | `engine` 至少四种语义；执行≠健全；执行≠授权；三态在 shell 退出码被折叠 | execution-forms；commit 的否定证据；M3 | 效应量；形态改变行为；所有实现 |
| E-22 | 已核 | 访问控制至少分三层（标签/策略/执行），层间不能互推；Glyph 单企业标签层不产策略/不执行；策略层无领域本体来源；执行层只有 trustgraph 单实现读路径；读路径≠写授权 | read-path 的边界；N07；M3 | 端到端访问控制；跨企业；漏标率；生产效果 |
| C-03 | 冲突（非等级） | 用准确率/reward 量控制类机制会得出错误结论；按机制类型选尺 | measurement 的主轴 | 不是新证据；不能替代机制级测量 |
| C-04 | 冲突（非等级） | E-01（结构化工件无增益）vs E-12（投影文本有效）不矛盾：投影什么不同 | context 的边界；M1/M4 | 已裁决；普适排序 |

> E-21 是查询路线选择，不在 03 的证据基；未列。

## 2.5 撤回与历史（W 表）

> 03 的机制描述保留，但**效应量不再引用**。正文只写 `W-xx`（编号与 01/02 的 W 表一致；本份不用 W-05/W-07/W-08）；「重启前先量」是测量设计（`工程建议`）。

<a id="w-table"></a>
| 编号 | 原依据 | 状态 | 不能再用 | 重启前先量 | 在哪 |
|---|---|---|---|---|---|
| **W-01** | E-02 Ontology Catch | withdrawn | catch/FA、空结果重试、precision、净修复 | 200 题（三类各 ≥50，余下补足）；catch/FA/净修复分开；per-flagged（token 或人时） | [checker](../03-positions/04-checker.md) |
| **W-02** | E-03 OA-RAG | withdrawn | 检索率、引用率、等级校准、调用/token | 400–800 条答案（每级 100–200 条独立标注）；检索率 ≥50%、引用率 ≥85% | [evidence](../03-positions/03-evidence.md) |
| **W-03** | E-04/E-13 POLAR | withdrawn | 18 格、T1-only、false-veto、能力梯度 | shadow 200–500 决策；100 条 blocked 标注；同轨迹配对；报前沿不设单点 | [action](../03-positions/05-action.md) |
| **W-04** | E-16 OntoAct | withdrawn | 三值条件效应、无效干预率 | ≥100 条带前提的决策；先测三值覆盖率（⊤/⊥/?） | [outside](../03-positions/07-outside.md) |
| **W-06** | Commit Boundary | 移出 | promotion 七条、三段式「已核」 | 1 个 mutation class；20–50 条 false-defer；审计字段齐 | [commit](../03-positions/06-commit.md) |

> 表中每条都对应一张位置卡；卡里的「自测」一行与这里一致。
>
> **数量对账**：W-01 的 200 题 = 三类各 ≥50 + 余下按故障分布补足；W-02 的 400–800 条答案 = 四级各 100–200（题量按答案数算）。
>
> **强端提示**：W-03/W-04/W-06 的 shadow 需要**先自建最小影子实现**；没有实现时只能做设计评审，不能算「自测」——这与覆盖率矩阵判 `?D` 不矛盾。

## 3. 读表三条

1. **先看「不能证明」列。** E 的限定比结论更重要；03 的边界大部分直接来自这一列。
2. **不要把 harness 证据读成本体证据。** E-01/E-07/E-08/E-09/E-14/E-15/E-18 不是本体专属；E-20 是形态分类。
3. **C 不是等级。** C-03/C-04 是冲突/方法论条目；引用时写「冲突」或「方法论」，不要写「已核」。

## 4. 维护规则

- E-xx 变化时，先改 [conclusions](../../../topics/conclusions.md)，再回改位置卡。
- 新增 E 必须先在 topics 升，不在 03 里造。
- 每条 E 的 `status`（active/contested）以 conclusions 为准；不复制生命周期状态。
- 不列 L-xx；L 只在 topics 内部使用。

> 回 [03 目录](../README.md) ｜ 回 [证据边界](02-boundaries.md)
