---
status: draft
updated: 2026-11-12
parent: ../README.md
---

<a id="0-一页结论"></a>
# 0. 机制摘要：能确认什么、怎么读一条 claim

> 本页是 03 的正文第 0 章。索引与阅读顺序见 [README](../README.md)；位置卡从 [03-positions](../03-positions/README.md) 开始。

## 0.1 一条 claim 的读法

一条常见主张：「读路径过滤能防止敏感数据泄漏。」03 不直接答「能/不能」，而是把它拆成三句：**机器在哪个时刻做了什么？只删哪一侧？异常时放行还是拒绝？**

现状：trustgraph 在正常路径、有 policy、只读检索、只删 subject 的条件下，能把被 block 的 subject 侧三元组删掉；但异常 fail-open、object 方向未测、只有 1 个实现、不拦写/落盘。所以这句话只能成立到「best-effort 可见性过滤」，**不能成立到「访问控制/授权」**（E-20/E-22；完整走查见 [95-claim-walkthrough](./95-claim-walkthrough.md)）。

同一套读法也适用于「编译成 SHACL 比塞进 prompt 更可靠」：判词是 M1（同一本体换位置/形态）**未开**，不能成立到「编译更好」；最接近的模板是 Grammar Prompting（同一文法放 prompt vs 约束解码；见 [05-evidence/03-gaps §3.1](../05-evidence/03-gaps.md#31-m1同本体跨位置)）。

## 0.2 今天能确认什么（机制行为；不是效应验证）

| 能验证 | 证据 | 你能做 | 不能承诺 |
|---|---|---|---|
| 读侧可见性过滤 | E-20 代码级 + E-22 | 单侧 subject 过滤；fail-open 必须标出 | 授权；object 方向；第二实现 |
| 离线/CI 图校验 | E-20（SHACL/三态） | CI 门；三态上报；影响报告 | in-loop 自动拒收；语义正确 |
| 跨轮身份/记忆 | E-05/E-17 | registry + 状态结构；CMR/precision 同看 | 跨运行复现；false merge 传播 |
| 查询编译（OBDA） | E-20 | OWL 2 QL 查询重写 | DL 推理；写授权 |

> **矩阵里 `●` 少，不等于框架失效**：动作闸/checker 的效应量撤回后，03 能给的确定性集中在「看见」和「离线判定」；阻断要等新源（W 表见 [05-evidence/01-ledger §2.5](../05-evidence/01-ledger.md#w-table)）。
>
> **`已核（代码）` = 读代码确认执行语义，不是已验证有用**；本表四行里三行由 E-20 单源支撑。复跑入口见 [read-path §3/§8](../../../topics/01-constraint/commit-gate/read-path.md)（EXP-001/EXP-002）。

<a id="sec-0-3"></a>
## 0.3 三条判断

1. **强度不是好坏。** 强度问「违反时能不能改变走向」；覆盖率问「能碰到多少类失效」。强端管得硬，但管得少。
2. **尺子跟机制走。** 不改变走向的供给/契约位置，准确率/token 仍可用；能改变走向的判定/动作/落盘位置，用单一 accuracy/reward 会错配（C-03）。
3. **六个位置问的问题不同；承重墙是 M1/M2。** context 看到什么、memory 记得什么、evidence 带什么依据、checker 对不对、action 能不能做、commit 够不够授权；不是「六个都该做」。多数团队先做 context（点位语义/投影），再做 offline/CI 校验；action/commit 等新源。

> **承重墙是 M1/M2**：没有同本体跨位置对照，也没有覆盖率测量；这份参考能给出分类与边界，不能给出效应量。下一步见 [gaps §3 M1/M2 最小协议](../05-evidence/03-gaps.md#3-m1m2-最小协议未开)。

<a id="sec-0-4"></a>
## 0.4 第一个动作

- 拿一条 claim，先走 [91-placement](./91-placement.md) 五步：位置 / 时刻 / 粒度 / gate-or-filter / 判不了。
- 再查 [04-across-positions/01-coverage](../04-across-positions/01-coverage.md) 的矩阵，不查直线。
- 最后回 [05-evidence/01-ledger](../05-evidence/01-ledger.md) 看「不能证明」列；指不到边界的 claim，不算读懂。
