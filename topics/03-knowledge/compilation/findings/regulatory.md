# 另一种编译：受监管知识系统

## F5

- **判断**：受监管知识供给的三原则是证据引用、数字由 solver 算、人做决策；并且**工具必须到达研究**，否则只是放在环境里。
- **等级**：`已核`（Grid Agents 一手技术报告；工业系统）。
- **条件/数字**：519 tasks / 8 families；Grid Studio 99.9%、13.9 s；base model 40.8%；法规证据 recall 0.967 vs 0.856；LegalBench-RAG F1 0.980；>2,000 bus 108/109；optimizer −33–67%；PowerMCP 仅 46/519 被调用。
- **反例/边界**：benchmark 单研究；最大 9,241 buses；GB corpus 特定；无形式安全；长期维护未量化。
- **来源**：[Grid 卡](../../../../src/papers/2611.03534-power-system-agentic/card.md) · [digest](../../../../src/papers/2611.03534-power-system-agentic/digest.md) · [03-L9](../../claims.md)

**和 CAI 的区别**：CAI 编译「主张-证据叶子」省 token；Grid 编译「法规知识系统」做合规审查与 solver 调度。共同点是证据可追溯、数字不靠模型。
