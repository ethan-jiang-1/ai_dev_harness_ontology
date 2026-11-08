# 用错了尺子 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `metrics/Fx`。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | reward 不是防伤害度量；护栏评估会反向 | 已核 |
| F2 | catch 与 FA 不能合成 accuracy | 已核 |
| F3 | 输出正确会掩盖过程无效 | 已核 |
| F4 | 单次 score 不可靠；要报方差/完成率/成本 | 已核 |

## F1 · reward 不是防伤害

- **案例**：POLAR 18 组仅 8 组改善；reward 只度量「发生了且做对了」，不度量「没发生」。
- **含义**：用 reward 量护栏会把有效护栏判成失败。
- **来源**：POLAR §5；E-04/E-13。

## F2 · catch/FA 非对称

- **案例**：Ontology Catch curated 18.9/16.8/57.1；空结果 2.5/0.1/100。
- **含义**：只看 accuracy 会把「多抓错、多杀对」混在一起；FA 会驱动 agent 修坏正确答案。
- **来源**：Table 2, p.7；E-02。

## F3 · 过程不可见

- **案例**：SLB 85% 轨迹、24% token；B1–B4 都能通过 program accuracy。
- **含义**：只看最终产物会放过冗余与错误继承；必须读 trace/program。
- **来源**：SLB §5；E-07/E-09。

## F4 · 单次 score 不可靠

- **案例**：54% 方差来自重复同一配置；配置只解释 39.4–46.1%；Information > Model > Reasoning > Budget > Verification。
- **含义**：单次跑分不能做配置比较；至少 5 runs/config，报 CI/completion/cost/calibration。
- **来源**：Agents are Systems §4；E-18。
