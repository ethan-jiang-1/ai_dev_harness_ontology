# 用错了尺子 · 发现（F）

> `F` 编号是子主题局部编号；跨页引用写 `metrics/Fx`。一句里混有事实与推断时，在句末分别标；未标处按 `推测` 处理。

## 索引

| ID | 判断（一行） | 等级 |
|---|---|---|
| F1 | reward 不是防伤害度量；用它判护栏会漏掉防伤害（后果为推断） | 已核 |
| F2 | catch/FA 与 precision 不能跨口径拼；混报会掩盖非对称代价 | 已核 |
| F3 | 输出正确会掩盖过程无效 | 已核 |
| F4 | 单次 score 不可靠；复合指标的定义域/档位决定可比性 | 已核 |

## F1 · reward 不是防伤害

- **案例**：POLAR 18 个模型-域格只有 8 个 reward 改善；作者声明 reward 是任务奖励，不是防伤害的直接度量——被 veto 的风险动作不体现在 reward 里。
- **含义**：用 reward 判护栏，「改善」只说明任务完成，不说明伤害没发生。把有效护栏判成失败是**推断**：POLAR 没有同批防伤害测量，不能从 8/18 推出「护栏无效」或「有效」（`推测`）。
- **来源**：[POLAR digest](../../../src/papers/2610.08082-polar/digest.md) §5、Table 3；E-04。

## F2 · catch/FA 非对称，precision 另口径

- **真实答案（UniProt，4,410 条 / 3,383 可检查）**：curated catch 18.9% / FA 16.8%；data-derived 8.2 / 3.5；masked LLM 5.0 / 1.8；空结果重试 2.5 / 0.1。
- **precision 是另一口径**：curated 57.1 / data-derived 72.3 / masked LLM 93.7 / 空结果 100，来自**人工故障 + 假设错答案占 25%**，不能与上面的真实答案 catch/FA 拼成一组。把 18.9/16.8 套同一公式约 27.3%，是反推，论文未直接给。
- **人工故障/control**：curated catch 60.1% / FA 15.0%；data-derived 75.6 / 9.7；空结果 79.2 / 0。16.8/3.5 与 15.0/9.7 都叫 FA，但分属真实答案与人工故障两表，**不能跨表拼**。
- **含义**：只看 accuracy 会把「多抓错、多杀对」混在一起；FA 触发重试，specific feedback 修好 28.3% 的 flagged wrong、也修坏 1.0% 的 flagged correct（generic 为 20.2 / 0.2）。
- **来源**：[Ontology Catch digest](../../../src/papers/2610.37809-what-does-an-ontology-catch/digest.md) Table 2/3, p.7；§4.1–4.3；E-02。

## F3 · 过程不可见

- **案例**：SLB 85% 轨迹、24% token；B1–B4 都能通过 program accuracy；163/1,791 程序继承轨迹答案。
- **验证行为同理**：prompt 从 none 到 binding，reference-based verification 只 19%→22%；给 oracle 才翻三倍；约 3/4 的 run 只做 format-only。把「要求自检」当验证证据，等于没测。`已核`（数字）/`推测`（指标后果）。
- **含义**：只看最终产物会放过冗余与错误继承。要看见它们，判据必须读 trace/program——这是工程要求（`推测`）；论文证明的是「输出评估看不见」，不是「trace 一定值得采」。
- **来源**：[SLB digest](../../../src/papers/2611.02395-solver-like-behavior/digest.md) §5；[Agents digest](../../../src/papers/2610.01618-agents-are-systems/digest.md) §4.3；E-07/E-09/E-18。

## F4 · 单次 score 不可靠，定义域/档位决定可比性

- **案例**：在**真实尝试**（过 hurdle）中，54% 的 score variance 来自同一配置的重复运行；不排除 hurdle 失败时配置只解释 39.4%，排除后 46.1%。`GAP_CLOSED=(S−B)/(R−B)` 只在 `R>B` 的任务上定义；hurdle 过滤「没真正尝试」的 run，不过 hurdle 的 run 不进这个方差口径。
- **五轴档位**：Information none/identity/interface/protocol；Reasoning act-only/think-act/ReAct；Verification none/asked/reported/binding；Budget 5/10/20 min；Model Qwen3.5-35B-A3B / 122B-A10B / 397B-A17B。只记轴名不记档位，两次跑分不可比（本页字段规则）。
- **效率≠结果**：Sonnet 工具调用少、错误少、校准好，但 pooled G 更低（单例，`已核`）；把效率当结果的替代指标是 `推测`。
- **含义**：单次跑分不能做配置比较；5 runs/config 起步，报 CI、completion、cost、calibration，并把分母（hurdle/completion）与 GAP_CLOSED 是否定义写在同一页。
- **来源**：[Agents digest](../../../src/papers/2610.01618-agents-are-systems/digest.md) §3.2/§3.3/§4.1/§4.2/§6.1；E-18。
