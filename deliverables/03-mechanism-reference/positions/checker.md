---
status: draft
deliverable_status: draft
updated: 2026-11-11
position: checker
evidence: [E-02, E-20]
---

# checker：产出对不对

> **2026-11-11 证据重置**：主锚 **E-02 已撤回**；本卡的旧 catch/FA/空结果重试数字只作回查，不再作为 admitted 结论。E-20 的 SHACL 代码级发现仍有效，但它只支撑「结构检查/三态」，不支撑 checker 的效应量。


> **一句话**：本体在这里是**外部判据**，不是模型自评。它能把「类型/声明/模式」错误变成可阻断的信号，但抓不住「意义变了」；而且判定器自己会误报，误报会把对的东西改坏。

**为什么结构错能拦、语义错抓不到**：checker 用 reasoner/SPARQL 检查类型/声明/domain-range；意义变化不在图里。**原锚 E-02 已撤回**：旧 curated FA 16.8%、precision 57.1%、空结果重试 79.2%/0% 等数字停用，不能拼成「准确率」。**条件**：有声明/闭世界；**反例**：语义错为主时越查越误；**决策**：先找新源，再谈 checker。

**为什么不是相邻位置**：不是 evidence（evidence 带依据，checker 判对错）；不是 action（checker 不改动作）。

## 1. 机制

| 来源 | 怎么来 | 能查什么 | 系统性偏向 |
|---|---|---|---|
| curated | 图作者发布，按原样用 | domain/range、声明、disjointness | FA 主源是缺声明/闭世界；不是「与数据矛盾」 |
| data-derived | 从数据总结模式（共现 ≥5 次） | 类型、属性使用、join 模式 | 只抓数据里没见过的组合；抓不到语义错 |
| LLM-generated | 从 summary + 实例样本写 | 同上，可能补声明 | 同 recipe 不同 draw 差异大 |

判定回路：`Question → agent → SPARQL → KG → answers → check → pass/flag → answer kept`。flag 触发一次重试；消息 specific（指出约束/片段）或 generic。每个 verdict 对正确答案打分：caught / missed / false alarm / correct pass；重试后 fixed / corrupted。不支持的 fragment 返回 **unknown**，不是 pass/flag。

**覆盖与保证**：同一 SHACL 引擎的两条路径——默认支持 `sh:sparql` 但会 skip；verified 覆盖 Core 但拒绝 `sh:sparql`（22/120）。`已核（代码）`（E-20）

## 2. 触发、输入、输出

| 项 | 内容 |
|---|---|
| 触发 | 产出已形成、尚未被使用；可挂在输出后，也可挂离线/CLI |
| 输入 | query、bindings、本体/schema、data summary |
| 输出 | `{verdict: pass / flag / unknown, constraint_id, query_fragment, message, evidence}` |
| 下一步 | 阻断/退回/仅标注是策略层；unknown 不阻断，也不能并进 pass |

## 3. 能改变什么

- **三来源各有偏向，无单一向优。** 真实答案 catch/FA：curated 18.9/16.8、data-derived 8.2/3.5、masked LLM 5.0/1.8；precision（人工故障 + 25% 错答案假设）57.1/72.3/93.7。`withdrawn`（原 E-02；单 checker 实验）
- **curated 的精确度仅略优于随机。** +1.6 点，CI 跨零；FA 主源是 declaration/domain-range（盲审 32 个 FA：undeclared term 17、closed-world 11、data clash 0）。`withdrawn`（原 E-02）
- **空结果重试是强基线。** 人工 fault 上 catch 79.2%、FA 0%；真实答案 catch 2.5%、FA 0.1%。`withdrawn`（原 E-02）
- **LLM judge 检错更多，但修坏多于修好。** 真实答案 catch 40.3%、FA 16.2%；40 修好 / 83 修坏。`withdrawn`（原 E-02；附录 C.2 比较器；成本/稳定性未测）
- **三态可以显式化。** 开源侧 `oo-shacl` 的 exit 3（undetermined）进入 wrapper 后变成 `conforms: null`，外层映射为 exit 2；JSON 保留第三态，shell 退出码不保留。`已核（代码）`（E-20）

## 4. 拦不住什么 / 失效模式

| 失效 | 说明 | 证据/等级 |
|---|---|---|
| 语义错抓不到 | 类型都对、关系方向反/边界划错（changes of meaning），结构检查 0% | `withdrawn`（原 E-02） |
| 误报引发「修坏」 | 正确答案被 flag，agent 去修；specific feedback corrupt 1.0% | `withdrawn`（原 E-02） |
| 把 curated 当权威 | curated precision 仅略优于随机；缺声明会对正确答案误报 | `withdrawn`（原 E-02） |
| 三态折叠 | unknown 并进 pass，污染 catch/FA 分母 | `已核（代码）`（E-20） |
| 覆盖与保证不可兼得 | 支持 `sh:sparql` 但 skip；verified 覆盖 Core 但拒绝 22/120 | `已核（代码）`（E-20） |
| 同源检查 | 同一 artifact 既做 context 又做 checker 时 catch 下降；机制未定 | `推测`（E-02 的探索性观察） |
| 没有 ground truth | 部署时只能抽样审计，无法直接算全量曲线 | `withdrawn`（原 E-02 的部署度量边界） |

## 5. 使能条件

- 错误是结构/声明/模式类，或至少能被外部约束表达；
- 有标注故障或可比基线（空结果重试）；没有标注就不知道曲线；
- 有策略层决定「flag 后阻断/退回/仅标注」；没有策略，checker 只是告警；
- 能接受「语义错另找 judge/人工」；judge 要先测净修复/成本/稳定性。

## 6. 证据与边界

| 证据 | 等级 | 支持什么 | 不能证明什么 |
|---|---|---|---|
| E-02 | **withdrawn** | 三来源 catch/FA；curated FA 归因；空结果基线；judge 净修复 | 部署 precision；false-veto；跨域；语义错 |
| E-20 | 已核（代码） | 三态接口；覆盖–保证边界；执行≠授权 | 效应量；所有实现；语义正确 |

> **旧口径停用**：precision 57.1% 等数字随 E-02 撤回，不再作为口径示例。

## 7. 可证伪条件

- 结构 checker 在 changes of meaning 上 catch >0 且 FA 可接受 → 推翻「语义错抓不到」；
- 净修复（fixed − corrupted）稳定 >0，且成本低于人工 → 支持 judge 分支；
- false-veto 被标注且很小 → 放宽「误报修坏」的警告；
- 第二个独立实现复现三态/覆盖边界 → 扩大 E-20 的适用范围。

## 8. 上游指针

- 机制：[checker/mechanism](../../../topics/02-judgment/checker/mechanism.md)
- 判断：[02-judgment/README](../../../topics/02-judgment/README.md) · [conclusions](../../../topics/conclusions.md) E-02/E-20
- 施工：[02 R5（recipes）](../../02-engineering-playbook/recipes/README.md) · [01 能力 5](../../01-capability-status/sections/map.md#22-一张表)
- 长版论证：[附录 §3.4.4](../appendix-constraint-spectrum.md#344-checker输出后的判定器)
