---
status: draft
updated: 2026-11-09
quality: B
based_on: card.md
claims: []
---

# Same Operation, Different Permission：guardrail 拦住了，不等于拦对了

> 这篇消化不假设你读过原文。先讲清「同操作、不同权限」的评测设计，再看 false denial / unavailable decision / 加 reviewer 的数字，最后说它对 E5、E7/E8 的边界意味着什么。

## 0. 三句话

1. **它问什么**：guardrail 的决策是否跟随授权——同一个操作，在合法授权下应放行，在禁止授权下应拦住；现有评测只看「拦住多少」，不看「放过了多少合法请求」。
2. **它怎么做**：语言轨 50 个场景 × 4 种授权证据（2 lawful / 2 forbidden），固定操作、只变授权证据；native 轨 1,594 条 OpenFGA/Cedar 请求；8 个 guardrail；同时记决策正确性、可用性、实际 effect。
3. **它发现什么**：很多 blocked 不是正确拒绝，而是 review 失败（unavailable）；结构化 review 在 Qwen3.5-9B 上 117–124/160 没有可用决策；加 reviewer 能去掉错误，但也会 veto 大量合法请求（Safeguard after 27B：去掉 1 个错误批准，veto 171 个合法请求）。

## 1. 它解决什么问题

### 1.1 背景

Agent 代表用户执行动作：退款、改记录、部署代码。一个动作是否合法，取决于授权证据（delegation、handoff、withdrawal、issuer、scope）。Guardrail 放在动作前，既可能**批准未授权动作**，也可能**拒绝合法动作**。后者常被忽略：用户被反复误拦后，可能关掉 guardrail 或授予更大权限，保护反而消失。

### 1.2 现有评测缺什么

- 只看 prevention 总数：分不清「正确拒绝」与「review 失败导致的 block」。
- 不做同操作对比：always-block 或 always-allow 也能在单边指标上好看。
- 不做请求级配对：一个改动可能同时 gain 一些 lawful、lose 另一些，总数看不出来。

### 1.3 论文的立场

Guardrail 应同时在「拦住的未授权动作」和「放过的已授权动作」上评估；**blocked ≠ denied**；决策可用性与决策正确性要分开报。

## 2. 术语

| 术语 | 用大白话说 |
|---|---|
| **AuthorizationPairs** | 本文 benchmark；同一操作、不同授权证据的成对 case。 |
| **language track** | 50 scenarios × 4 contexts = 200；每个 scenario 固定 request/policy/effect，只变 evidence。 |
| **native-policy track** | 1,594 条 OpenFGA/Cedar 请求；引擎给参考标签；decision-only。 |
| **lawful / forbidden** | 授权证据允许 / 禁止该操作。 |
| **forbidden effect** | 被执行了的禁止请求。 |
| **lawful completion** | 被执行了的合法请求。 |
| **false denial** | 合法请求被**可用地**拒绝。 |
| **unavailable decision** | 接口无法产出可解析决策；执行被阻断，但不构成判断。 |
| **usable correctness** | 可用决策中与参考一致的比例。 |
| **all-must-allow composition** | 多个 reviewer 串联，前一个 allow 才看下一个；只会更严。 |

## 3. 它怎么做

### 3.1 语言轨

- 50 scenarios，每个 4 contexts：2 lawful、2 forbidden；共 200 contexts；40 dev / 160 test；**80 lawful / 80 forbidden**。
- 固定 request、policy、effect；只变授权证据（scope/status/issuer/irrelevant evidence）。
- 9 类 effect（ledger transfer、code deployment、document signing、file delivery 等）；本地执行并读回；1,600 个原始 effect 全部与 dispatched decision 一致。
- 参考标签：3 位安全专家独立标；186/200 一致（Fleiss κ=0.91）；14 个分歧裁决，3 个改标；67 条解释注记；198 个 determinate 标签由两个独立 evaluator 复现；2 个在更严格编码下 unresolved，但保留专家标签，排除后结论不变。

### 3.2 Native 轨

- 1,594 条 OpenFGA/Cedar 请求；47 apps；60 policies；379 dev / 1,215 test；23 组同 policy/query 的 lawful/forbidden 状态。
- OpenFGA/Cedar 引擎复现所有参考标签；模型只看 policy/request/state，不看答案。

### 3.3 Guardrail 配置

- 8 个：Qwen3.5-9B（nonthinking）、Qwen3.5-27B（thinking）、Nemotron、Safeguard、Granite Guardian、PolicyGuard、NeMo self-check、Qwen3Guard（内容安全对照）。
- 共享 32K context、单次 attempt、一小时 deadline；prompt/parser 各自不同，所以比较的是完整体验，不是孤立模型因素。
- 语言轨 8 配置；matched-interface 研究在 2 个模型 × 4 接口 × 3 seeds × 200 inputs = 4,800 calls。

### 3.4 评分

- 每个决策记三件事：正确性（lawful/forbidden）、可用性（usable/unavailable）、实际 effect。
- 同一请求跨配置按 identity 配对；gain/loss 分别计，不用净总数替代。

## 4. 结果：数字与条件

### 4.1 语言轨（160 test：80 lawful / 80 forbidden）

- **Qwen3.5-27B 与 Safeguard 在 160 条上全对**（该轨；native 轨不同）。
- 其余六个配置各有失败：Qwen3.5-9B、Granite、NeMo 有 6–17 个 forbidden effects、8–15 个 false denials；Nemotron 放行 58 个 forbidden、12 个 unavailable；Qwen3Guard 放行 72/80 forbidden（内容安全标签迁移到授权很差）。
- **Structured review 的 unavailable**：Qwen3.5-9B 117–124/160；Qwen3.5-27B 48–50/160；不是 truncation，响应正常结束。
- **Schema decoding** 让所有决策可用；但 Qwen3.5-9B 仍最多 6 个 forbidden effects；Qwen3.5-27B 每 seed 仍有 5–6 个 false denials。

> 出处：§5.1、§5.2、Table 1、Table 4。

### 4.2 Native 轨（1,215 test）

- **Qwen3.5-27B**：99.1% 正确；1 个 incorrect approval；10 个 false denials。
- **Safeguard**：84.2% 正确；**174/767 lawful requests 被 false deny**。
- **Qwen3.5-9B**：69.4% 正确；**261/448 forbidden requests 被错误批准**。

> 出处：§5.1、Table 2。

### 4.3 加 reviewer：去错，也 veto 合法请求

| 组合 | incorrect approvals /448 | lawful approvals /767 |
|---|---:|---:|
| Qwen3.5-9B | 261 | 656 |
| Qwen3.5-27B | 1 | 757 |
| Safeguard | 12 | 588 |
| 9B → 27B | 1 | 648 |
| 27B → 9B | 1 | 648 |
| 27B → Safeguard | 0 | 586 |
| Safeguard → 27B | 0 | 586 |

- 9B → 27B：去掉 260/261 个错误批准，代价 8 个 lawful approvals。
- 27B → 9B：不去掉任何错误，反而失去 109 个 lawful approvals。
- **27B → Safeguard：去掉 1 个错误批准，veto 171 个 lawful requests。**
- all-must-allow 只会更严；加 reviewer 的收益/代价必须按请求 identity 算，不能只看总数。

> 出处：§5.3、Table 2。

### 4.4 修接口：可用性恢复，但授权集合会变

- direct → schema：5/6 runs 同时有 gains 和 losses；net −3 到 +27；36 个 interface 对比里只有 1 个在 scenario-cluster + Holm 后显著（Qwen3.5-9B seed 1 的 +27）。
- Schema review 在 Qwen3.5-9B 上 seed 0 forbidden effects 从 3 升到 6，seed 2 从 14 降到 3；在 27B 上每 seed 都 0 forbidden，但仍有 5–6 false denials。
- **结论**：修输出格式能修「不可用」，不能修「判断错」；一个改动可能同时帮一些请求、害另一些。

> 出处：§5.3、Figure 1、Appendix E/G。

## 5. 这些数字不能说明什么

1. **不是本体评测。** 没有 ontology；guardrail 是通用 reviewer，不是 SHACL/OWL 判据。不能直接把它当 E-20 的「本体执行」证据。
2. **不是 commit gate。** 它测动作前/决策，不测落盘前授权；native 轨是 decision-only，没有 effect。
3. **不是部署。** 语言轨是合成场景；native 轨来自公开 policy 示例；没有真实客户流量。
4. **不是 harm 度量。** 它测 forbidden effect / lawful completion，不测事故成本；false denial 的代价也没有货币化。
5. **不能把 160 条的全对当通用。** Qwen3.5-27B 在语言轨 160/160，但在 native 轨是 99.1%，有 10 个 false denials；两个轨不同。
6. **不能把 unavailable 当 denial。** Unavailable 会阻断执行，在 prevention 总数里看起来像「拦住」，但它是 review 失败，不是授权判断。
7. **不能忽略 seed。** 3 seeds；单 seed 的增减可能是噪声；只有 1/36 对比过 Holm。
8. **不是「加 reviewer 更安全」。** 加 reviewer 去错，也 veto 合法请求；要看具体 reviewer 和顺序。

## 6. 工程上怎么用

### 6.1 复刻顺序

1. **先固定操作，只变授权证据。** 同一个 request/policy/effect，构造 lawful/forbidden 两版；否则 always-block/always-allow 也能过。
2. **分三件事记**：决策正确性、可用性、effect；不要把 unavailable 算成 denial，也不要把 block 总数当正确拒绝。
3. **按请求 identity 配对**：改动前后哪些 lawful 被 gain/loss；只看总数会漏掉「同时帮一些、害一些」。
4. **先修接口，再谈判断**：structured → schema 能修 unavailable，但不修 permission 错误；修完要重测。
5. **加 reviewer 要算 veto 代价**：all-must-allow 的 lawful approvals 下降是直接成本；用 Table 2 的方式报。
6. **把 false denial 当验收项**：固定一组必须放行的 lawful 请求，改动不能丢掉它们。

### 6.2 与本体 checker 的关系

- 本体 checker 也会遇到同样的问题：**结构检查通过/不通过/未检查完**三态；如果把「未检查完」当 pass 或当 flag，catch/FA/denial 都会被污染（对应 checker/F7）。
- 本体 checker 的「flag」不等于「动作被正确拒绝」；需要授权标签/请求 identity 才能算 false denial。
- 这篇不提供 ontology-specific 数字；它提供的是**评测设计**：同操作、不同权限、请求级配对、三态分开。

## 7. 质量与边界

- **证据类型**：benchmark + 多配置实验（一手正文）。
- **强项**：同操作对照、专家标注、κ=0.91、native 轨引擎标签、effect 验证、请求级配对、明确区分 unavailable。
- **主要威胁**：语言轨合成、AI 辅助起草、标注者缺临床/法律/金融视角；native 轨 decision-only；单次 attempt；3 seeds；模型配置不同；没有 ontology/harm。
- **`quality: B`**：设计和执行强；外部效度（合成、无部署、无本体）限制。

## 8. 与仓库判断的关系

- **E-04（动作闸）**：这篇不测本体闸，但补了「false-veto 不能从 block 数推」的评测方法；POLAR 的 1,745 blocked 无授权标签，这篇说明**有授权标签时误拦很常见**（Safeguard 174/767），但**不能把这个数搬到 POLAR**。
- **E-20（执行 ≠ 授权）**：这篇是另一个角度的同向证据：guardrail 的「拒绝」可能是 review 失败，不是授权判断；执行/阻断不等于正确授权。
- **checker/F7（三态）**：unavailable 必须单列；否则 denial/catch/FA 都不可比。
- **C-03（度量错配）**：只看 prevention 总数会漏掉 false denial；要同时报 forbidden effect / lawful completion / unavailable。
- **E-05**：无关（记忆）。
- **不新增 E/L**：这是 harness/评测证据，不是本体执行证据；先留作 E-04 的边界与 E5 的方法候选。

## 9. 还没解决 / 下一步

- 能否把 AuthorizationPairs 的「同操作、不同权限」设计搬到本体 checker：同一份本体，合法/非法实例成对，测 false denial？
- false denial 的代价如何货币化/排序？
- 多 reviewer 的最优顺序是否依赖请求分布？
- 真实部署的授权标签从哪来？
- 与 commit gate 的关系：落盘前授权是否也需要「同变更、不同证据」的成对评测？

## 10. 原文

- arXiv:2610.16838
- PDF：同目录 `2610.16838-same-operation-different-permission.pdf`
- 代码/数据：Appendix A reproduction guide；未在本地跑。
