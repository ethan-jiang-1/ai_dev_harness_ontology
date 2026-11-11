---
status: draft
updated: 2026-11-12
---

# 06 测量派 · 局部结论

> 本页是本派的局部判断账本。跨派/对外引用的结论升到 [conclusions](../conclusions.md) 的 E-xx；`06-Lx` 只在本派内使用。

| ID | 判断 | 等级 | 证据 | 备注 |
|---|---|---|---|---|
| 06-L1 | 答对≠内部有本体；本体预测机制上可干预，但无法与类别辅助信息干净分离 | withdrawn | E-10 / MIOE | 2026-11-11 源移出；待重写。两模型/两任务；MDAS 0.59 |
| 06-L2 | 失败多归工作流 | withdrawn | E-06 / Diagnose | 2026-11-12 源移出（E-06 撤回）；待重写。角色级归因 |
| 06-L3 | 只看输出的尺子会漏掉冗余/错误继承 | 已核 | E-07 / E-09 | 需看轨迹；SLB 85%/24% |
| 06-L4 | 度量错配是文献冲突主因 | 推测 | C-03 | 分析框架 |
| 06-L5 | agent 评测应把配置当变量；54% score variance 来自重复同一配置的 run-to-run 噪声 | 已核 | E-18 / Agents Are Systems | 8,640 runs；4 tasks；5 axes |
| 06-L6 | 本体接地失败可拆成 Input/Generator/Output/Validator/Repairer 五角色 + 七个诊断变量；语法通过不等于语义充分 | withdrawn | E-06 / Diagnose | 2026-11-11 源移出；待重写。框架，非量化；无分布比例 |
| 06-L7 | 七变量可做实验诊断表，但未验证能预测重设计效果 | withdrawn | Diagnose | 2026-11-11 源移出；待重写。需要前后对照 |
| 06-L8 | SLB 普遍且冗余：85% traces、24% token、77–89% 程序仍独立重算；placeholders 可减 97% 而不损准确率 | 已核 | E-09 | 2,000 generations；闭源未测 |
| 06-L9 | 形式语言是 SLB 最强解释变量：Python > Z3/PDDL（0.03–0.20 ratio） | 已核 | E-09 | FL 解释 0.123 方差 vs 数据集 0.057 |
| 06-L10 | MIOE：MDAS 最好 0.592/0.587（instance）、0.513/0.542（subclass）；多任务 Iso +0.081 / Cause −0.052；多层窗口 0.667 | withdrawn | E-10 | 2026-11-11 源移出；待重写。只 Qwen3；「部分分离」原因未定 |
| 06-L11 | 验证行为靠系统提供，不靠 prompt：prompt none→binding 只 19%→22%；oracle 翻三倍 | 已核 | E-18 | 只 verification 一个维度 |
| 06-L12 | Agent 很少拒绝弱 specialist：mmlu-astronomy 上 99.8% 仍用 AstroSage；给 oracle 也不显著改善 | 已核 | E-18 | authority bias/探索不足 |
| 06-L13 | 落地经济学：值不值得不是本体质量，是「位置 × 成本 × 使能条件」；没有单一答案 | 推测 | E-08/E-13/E-14/E-15 | 见 [feasibility](./feasibility/README.md) |
| 06-L14 | 没有一条适用于所有机制的能力曲线：约束类随能力下降，知识投影不随容量上升 | 推测 | E-13 / E-12 | Wave 1 综合 |
| 06-L15 | 覆盖率可按「七类失效 × 八位置」分类；位置是专门化的，不能排成一条强度线，也不能合成百分比 | 推测 | [coverage](./metrics/coverage.md) / C-03 | 设计分类，非测量；矩阵逐格可反驳 |
| 06-L16 | 同一机制换尺子可翻转结论方向：约束类在任务账混合/负、在风险账前沿更优；知识供给在准确率 neutral、在 token 上正收益 | 已核（逐格）/ 推测（翻转） | E-01/E-04/E-08/E-12/E-14/E-15；C-03 | 2×2 见 03 measurement；无同数据集两把尺子对照，翻转是跨来源综合 |
| 06-L17 | 跨段传播会换形态：同一 0 行可能来自缺 tag/错 join/超时/真答案为空；同一 allow 可能来自错 level/skip/版本；单段指标看不见 | 推测（综合） | metrics/propagation；E-06 | 无跨段注入实验；只有 query 段成本有数 |
