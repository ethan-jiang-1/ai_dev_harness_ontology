# 机制尺子 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `mechanism/Fx`。
> 分数均为 Disentangle（Cause 与 Iso 的平均），不是准确率。机制与数字见 [MIOE digest](../../../meta/audits/2026-11-11-source-purge.md#src-2610-38326) §4（对应一手 Table 2/3）；Table/Fig. 页码指原文。

## 索引
> **2026-11-13 对账**：F1–F5 的唯一来源 MIOE（2610.38326，E-10）已移出（[tombstone](../../../meta/audits/2026-11-11-source-purge.md#src-2610-38326)），本索引与 README 已同步降为 `推测`（机制/历史示例，不作活证据）。

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | 本体预测机制上可干预 | 推测（源已移出，历史示例） |
| F2 | 无法与类别辅助信息干净分离；单层最好约 0.59 | 推测（源已移出，历史示例） |
| F3 | Distributed subspace > SAE/DBM；MDAS vs DAS 不宜排序 | 推测（源已移出，历史示例） |
| F4 | 多任务 Iso↑/Cause↓（配对差）；多层窗口更好，Δ 有独立基线 | 推测（源已移出，历史示例） |
| F5 | 类级差异大、按角色不对称；原文无可引用区间 | 推测（源已移出，历史示例） |

## F1 · 可干预

- **判断**：换掉内部表示能改变本体层答案；存在可定位的内部表征。
- **数字**：MDAS 0.592/0.587（instance-of）、0.513/0.542（subclass-of），Entity/Context；Qwen3-8B 单层。
- **边界**：可干预 ≠ 可精确控制；只 subject token 的 residual stream。
- **来源**：Table 2, p.6；digest §4.1。

## F2 · 部分分离

- **判断**：没有方法到 Cause=1、Iso=1；单层最好约 0.59。
- **含义**：0.59 是 Cause/Iso 的平均分，不是「59% 的样本同时做到」；正确输出不等于干净内在本体，外部判据的必要性增强。
- **边界**：可能是表示纠缠，也可能是方法不够强；原文不能区分。
- **来源**：Table 2/3；§5；digest §4.1、§5。

## F3 · 方法排序

- **数字**（instance-of，Entity/Context，Qwen3-8B 单层 Disentangle）：SAE 0.412/0.371；DBM 0.425/0.396；MDBM 0.443/0.408；DAS 0.584/0.547；MDAS 0.592/0.587。
- **含义**：稀疏特征不等于因果变量；distributed subspace 更强。
- **不宜排序**（instance-of，Entity）：MDAS 的 Iso 更高（0.658 vs 0.579）、DAS 的 Cause 更高（0.589 vs 0.527）；0.592 与 0.584 只差 0.008，单 seed、无 CI，不能当稳定排序。
- **口径**：各方法按 Entity Disentangle 选最佳层/维度，Context 复用同一配置（不是对称切分）；Dimension 定义不同（SAE latent width / DBM mask / DAS·MDAS rank），不是同容量对照。
- **来源**：Table 2 及 caption, p.6；Appendix Table 4；digest §4.1。

## F4 · 多任务/多层

- **多任务**（MDBM/MDAS）：**best-vs-best 配对差** Iso +0.081 / Cause −0.052（不是多任务整体平均）；Disentangle 仍升。
- **多层**：instance-of 上 DAS 512×4 0.667（+0.102，全表最高）、MDAS 256×4 0.666（+0.074）、MDAS 512×4 0.663（+0.070）；subclass-of 的 MDAS 512×4 0.565（+0.052）。
- **Δ 基线**：相对同方法、同总维的单层结果。DAS 512×4 的基线是单层 DAS rank 2048 ≈0.565（由 0.667−0.102 反推），**不是** [digest §4.1](../../../meta/audits/2026-11-11-source-purge.md#src-2610-38326) 的 DAS 0.584；subclass MDAS 的基线是 0.513。0.667/0.666/0.663 的差距可能在小样本噪声内。
- **小 rank 前提**：单层审计用 rank 1024/2048；256–512 的单层小 rank 下 Cause 会掉，0.40/0.55 阈值作废，只认随机子空间对照（digest §6.2 的工程线；论文未做该阈值对照，`推测`）。
- **含义**：权衡不是免费（多任务用 Cause 换 Iso）；多层把计算分布在短层段。
- **来源**：§4.2, p.5；Table 3 及 caption, p.7；digest §4.2。

## F5 · 类级差异

- **判断**：类级差异大；具体/规则类（airport/country/currency/university）分离较好；宽泛/异质类（body of water/geographical feature/food/biological process/material）较差。
- **没有区间**：原文的类级结果是 Fig. 3 散点与附录的类级均值/排名，没有可直接引用的类级区间；类级切点必须按本域散点重算。
- **角色不对称**：同一个类当 base 与当 source 的 Disentangle 不同（如 protein、video game 更适合当 source）。
- **含义**：聚合分数会掩盖域差异；做类级分析、报全部类。
- **来源**：Fig. 3, p.7；§4.3；Appendix Table 6–8；digest §4.3。
