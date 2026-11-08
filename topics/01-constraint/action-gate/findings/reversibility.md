# 可逆性门：结构、能力、caveat

## F1

- **判断**：可逆性可以做成类型化判据——T1–T5 关系 + 反向搜索 + 最弱一步分数，比 LLM judge 的 allow/block 更可审计。
- **等级**：`已核`（POLAR 一手正文）。
- **条件**：τ²-bench；6 模型 × 3 域；VetoPolicy；Layer B 从真实 DB/工具记录重建。
- **反例/边界**：不模拟完整 s′；不验证逆执行；T1-only 接近 blanket veto。
- **来源**：[POLAR 卡](../../../../src/papers/2610.08082-polar/card.md) · [digest](../../../../src/papers/2610.08082-polar/digest.md)

## F2

- **判断**：约束收益随基线能力上升而下降；强模型与 retail 常回退。
- **等级**：`已核`（POLAR 一手正文）。
- **条件**：18 个 model–domain 格仅 8 个改善；airline 四个模型 +0.11–0.18；slope −0.76/−0.67/−0.31（R² 0.92/0.98/0.65，六点描述性拟合）。
- **反例/边界**：不是部署阈值；retail 的失败可能是任务形态，不是机制失败；gpt-oss-120B retail −0.242。
- **来源**：[POLAR 卡](../../../../src/papers/2610.08082-polar/card.md) · [E-04 / E-13](../../../conclusions.md)

## F3

- **判断**：T1-only 接近 blanket veto，增益却不比 full 小；结构反向组合的贡献未被隔离。
- **等级**：`已核`（作者 tier ablation）。
- **条件**：qwen3-8B airline；full 0.080 [0.013,0.147]；T1-only 0.087 [0.020,0.153]；no-irreversible 0.060 [−0.007,0.127]。
- **反例/边界**：需要同一 baseline、同一轨迹的配对实验才能分开；1,745 条 blocked decisions 无 harm 标签，false-veto 未知。
- **来源**：[POLAR 卡](../../../../src/papers/2610.08082-polar/card.md) · [digest](../../../../src/papers/2610.08082-polar/digest.md)
