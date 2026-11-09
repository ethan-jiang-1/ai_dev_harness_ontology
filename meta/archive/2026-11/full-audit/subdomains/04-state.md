> **历史快照（2026-11-08/09）**：已归档，不再维护。现行规则见 `meta/README.md`，当前状态见 `meta/state.md`。文中的计数与结论可能已被后续修复取代。

# 04 state · status

- **G-X：3/3 pass**（memory、identity、determinism）。
- **A4：3/3**；E4：3/3。
- **关键判断**：
  - 状态不是事实集；检索 85.6 vs 86.4，而 Acc@complete 70.8 vs 68.5。
  - 身份先于内容；false merge 是风险，但“长期污染”未测。
  - 确定性是输入完备性 + 锚点问题；9% 继承是一手计数。
- **已修**：70.8/36.8 跨基准、alias 主增量、90% 阈值、10 个月度/3 reporting、9% 待核。
- **Residual**：
  - false merge 传播/回滚未测。
  - determinism 的跨运行重放没有一手证据，只有 E-06 类比。
- **下一步**：人类抽检 memory；先做单域 200–500 请求，不先训 GRPO。
