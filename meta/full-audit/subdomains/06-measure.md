# 06 measure · status

- **G-X：5/5 pass**（mechanism、failure-attribution、trace、metrics、feasibility）。
- **A4：4/5**（mechanism、trace、metrics、feasibility；failure-attribution 为 A3+）。
- **E4：5/5**。
- **关键判断**：
  - 机制可干预但只部分分离；单 seed/无 CI。
  - 失败归因是工作流问题，不是单一模型问题。
  - trace：输出正确会掩盖过程；SLB 与准确率无关联。
  - metrics：配置是系统变量；54% 方差限定“真实尝试/过 hurdle”。
  - feasibility：位置×成本×使能；12 机制仅 3 个能算盈亏平衡。
- **已修**：0.03–0.65、多任务 best-vs-best、trace VALUES/ratio、metrics 57.1、feasibility τ=∞。
- **Residual**：
  - CAI explained-residual：$/文档、人日费率、sprint 工时缺。
  - false-veto 无测量；账本 TCO 不可算。
- **下一步**：人类抽检 feasibility；先做 3 个可算机制的 NPV，不做全组合。
