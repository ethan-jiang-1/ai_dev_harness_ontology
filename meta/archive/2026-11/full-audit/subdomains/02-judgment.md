> **历史快照（2026-11-08/09）**：已归档，不再维护。现行规则见 `meta/README.md`，当前状态见 `meta/state.md`。文中的计数与结论可能已被后续修复取代。

# 02 judgment · status

- **G-X：3/3 pass**（checker、evidence、calibration）。
- **A4：3/3**；E4：3/3。
- **关键判断**：
  - checker 先超过空结果重试/随机 flag；catch/FA 分开报。
  - curated 真实答案 precision 只略优于随机；data-derived catch 低但 precision 高。
  - evidence 的 grounding 是自评，只能路由不能自动放行。
  - calibration 的 ECE/isotonic 两篇 digest 未测，标 explained-not-applicable。
- **已修**：57.1 precision 跨表、同源/generic 强表述、curated FA 归因、span 无源、12k/5k、Test2 OQ 23.2%。
- **Residual**：
  - 真实部署 precision、每级 recall、域移阈值未测。
  - checker 采纳门 vs V3 两把尺，需在试点统一。
- **下一步**：人类抽检 checker；先跑 200 题空结果基线 + data-derived check。
