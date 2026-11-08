# 机制尺子 · 机制

> 只写「它怎么测」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

行为正确率不能证明模型内部在算本体关系；正确输出可能来自表面模式。MIOE 用因果抽象/互换干预测这一步。

## 因果抽象

- 高维变量：subject 的 target taxonomic value + class-specific auxiliary attributes。
- 干预：`II(M,F,x_base,x_source)`：把 base 在低层特征 F 的值替换成 source 诱导的值。
- **Cause**：目标答案是否变成 source 的类。
- **Iso**：辅助属性是否保持 base。
- **Disentangle**：两者平均。

## 数据与模型

- `instance of`：54 classes / 1,099 subjects / 376 attrs / 4,288 prompts。
- `subclass of`：39 / 1,113 / 160 / 2,095。
- Qwen3-8B、Qwen3-4B；36 层；subject-token residual stream。
- 方法：SAE、DBM、MDBM、DAS、MDAS；单层 36 层全扫；多层 2/4 层窗口。

## 结果

| 方法 | instance（Entity/Context） | subclass（Entity/Context） |
|---|---|---|
| SAE | 0.412 / 0.371 | 0.397 / 0.429 |
| DBM | 0.425 / 0.396 | 0.431 / 0.443 |
| MDBM | 0.443 / 0.408 | 0.440 / 0.450 |
| DAS | 0.584 / 0.547 | 0.496 / 0.535 |
| **MDAS** | **0.592 / 0.587** | **0.513 / 0.542** |

- 多任务：Iso +0.081、Cause −0.052。
- 四层窗口：DAS 512×4 0.667（+0.102）；MDAS 256×4 0.666；subclass MDAS 512×4 0.565。
- 层剖面：Cause 中层/中后层最强；后层 Iso 高但 Cause 可能崩。
- 类级：0.03–0.65；具体/规则类好，宽泛/异质类差。

## 失效模式

- **部分分离**：0.59 不是「懂本体 59%」；没有方法到 1.0。
- **表示 vs 方法**：可能是表示纠缠，也可能是干预不够强；本文不能区分。
- **单模型族**：只 Qwen3；跨模型未测。
- **单任务类型**：只 entity typing/subsumption；更丰富公理未测。
- **单干预位置**：subject token；其他位置未测。
- **聚合掩盖类级**：平均值可能由少数好类拉高。

## 与本体 / 回路的关系

本体在机制尺子里是 **被测试的对象**；它不进入运行时回路。测的是「内部有没有可干预的本体表征」，不是「输出对不对」。

## 关联

- [MIOE digest](../../../src/papers/2610.38326-mioe/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [metrics](../metrics/README.md)
