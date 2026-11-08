# 输出后判定 · 机制

> 只写「它怎么跑」。判断回 [findings](./findings.md)，边界/下一步回 [frontier](./frontier.md)。

## 问题

输出已形成、尚未被使用；需要判断「它是否忠于本体/数据」。格式检查只能看语法，测试只能看行为；本体是唯一既外部、又能覆盖语义的判据——但 checker 自己也会错。

## 三种来源

| 来源 | 怎么来 | 能查什么 | 系统性偏向 |
|---|---|---|---|
| curated | 图作者发布，按原样用 | domain/range/disjointness、类/属性声明 | 缺声明/与数据矛盾 → 误报高 |
| data-derived | 从数据总结类/属性/常见模式；模式≥5 次才允许 | 类型、属性使用、join 模式 | 把「常见」当「应然」；抓不到语义错 |
| LLM-generated | 从同一 summary + 实例样本写；可加 disjointness | 同上 + 可能补声明 | 不稳定；同 recipe 不同 draw 差异大 |

## 判定回路

`Question → LLM agent → SPARQL → KG → answers → check → pass/flag → answer kept`。

- flag 触发**一次重试**；消息 specific（指出失败约束/查询片段）或 generic。
- 每个 verdict 对正确答案打分：caught / missed / false alarm / correct pass。
- 重试后：fixed（错→对）、corrupted（对→错）。
- 不支持的 fragment（UNION、subquery）返回 **unknown**，不是 pass/flag。

## 检查类型

- **Query checks**：解析 SPARQL，推断变量类型；检查 term 存在、class membership、domain/range、disjointness、datatype range。
- **Binding checks**：对结果绑定重新求值；检查类/属性/数据类型。
- **data-derived pattern checks**：属性与数据从未共现的类、没有类支持≥5 次的 join。
- **空结果重试**：查询返回空就重试；不需要本体，是强基线。

## 三种用法

- **as context**：把本体渲染进 prompt，让 agent 自己参考。
- **as check**：编译成 checker，对查询/答案做结构检查。
- **both**：两者都用；本文发现同源 context+checker 的 catch 反而下降（探索性）。

## 成本

| Check | 每答案 token（median） | 时间（median） | 备注 |
|---|---|---|---|
| curated | 65,976 | 46.0 s | false alarm 多 → 重试多 |
| data-derived | 28,076 | 17 s | FA 少；生成 <$1 |
| 空结果重试 | 低 | 低 | FA≈0；真实答案 catch 仅 2.5% |

## 失效模式

- **误报导致「修坏」。** 正确答案被 flag，agent 去修，把对的改成错的；specific feedback corrupt 1.0%。
- **漏检结构化错误。** 类型都对、关系方向反了/边界划错，检查抓不到。
- **判定器不可解释。** 只说错、不说哪条约束，模型只能换姿势重试。
- **串联放大误报。** 前一级误报引发下游大量无效工作。
- **把 curated 当权威。** 发布状态的本体可能缺声明/与数据矛盾；不审计就上线，FA 系统性偏高。
- **用 accuracy 评估 checker。** catch 与 FA 混在一起，会得出反向结论。
- **同源 context + checker。** 确认偏差会降低 catch；不要让同一份 artifact 既喂又判。

## 与本体 / 回路的关系

本体在输出后以 **schema/约束** 出现；约束强度中（能 flag，不保证语义真值），覆盖率取决于错误类型。被违反时 checker 能报出约束/查询片段；不能报「意义不对」。

## 关联

- [Ontology Catch digest](../../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md)
- [findings](./findings.md) · [frontier](./frontier.md)
- [00-harness/verification](../../00-harness/verification.md)
