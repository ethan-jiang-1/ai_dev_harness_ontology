---
status: draft
deliverable_status: draft
updated: 2026-11-11
target: 架构师 / 研究者
basis: E-01–E-20, C-03/C-04; topics/README 四轴
---

# 03 · 机制参考：六个位置、三根分类轴与证据边界

> **读者**：架构师 / 研究者 ｜ **回答**：为什么是这些位置/形态、证据边界在哪 ｜ **不回答**：具体怎么做（去 02）、今天能做成什么（去 01）。
>
> **第一次来**：先读 [START](../START.md)（10 分钟），再回本份。
>
> **2026-11-11 证据重置**：E-02/E-03/E-04/E-06/E-10/E-11/E-13/E-16/E-26 已撤回。03 的 checker/evidence/action/outside 位置卡保留机制描述，但**不再把它们当 admitted 结论**；每张卡顶部有单卡提示。
>
> **词源（只定词，不撑效果）**：本体/顶层本体 = `N: ISO/IEC 21838-1/-2`；约束/校验/三态 = `N: W3C SHACL`，规则/target = `N: W3C SHACL-AF`；推理/profile = `N: W3C OWL 2 Profiles`；策略表达/判定架构 = `N: W3C ODRL 2.2` / `N: OASIS XACML 3.0`。六位置、接缝、强度、覆盖率、执行形态 = `local`。逐词见 [术语 §0](./sections/glossary.md#term-sources)；标准边界见 [规范主干](../../topics/trunk.md)。

## 先走一条 claim

同事说：「读路径过滤能防止敏感数据泄漏。」03 不直接答「能/不能」，而是把它拆成三句：**机器在哪个时刻做了什么？只删哪一侧？异常时放行还是拒绝？**

现状：trustgraph 在正常路径、有 policy、只读检索、只删 subject 的条件下，能把被 block 的 subject 侧三元组删掉；但异常 fail-open、object 方向未测、只有 1 个实现、不拦写/落盘。所以这句话只能成立到「best-effort 可见性过滤」，**不能成立到「访问控制/授权」**（E-20/E-22；完整走查见 [claim 走查](./sections/claim-walkthrough.md)）。

同一套读法也适用于「编译成 SHACL 比塞进 prompt 更可靠」：判词是 M1（同一本体换位置/形态）**未开**，不能成立到「编译更好」；最接近的模板是 Grammar Prompting（同一文法放 prompt vs 约束解码；见 [gaps §3.1](./evidence/gaps.md#31-m1同本体跨位置)）。

**三条判断（读完能复述）：**

1. **强度不是好坏。** 强度问「违反时能不能改变走向」；覆盖率问「能碰到多少类失效」。强端管得硬，但管得少。
2. **尺子跟机制走。** 不改变走向的供给/契约位置，准确率/token 仍可用；能改变走向的判定/动作/落盘位置，用单一 accuracy/reward 会错配（C-03）。**注意：支撑这条的 E-04 已撤回；判断本身降为 `推测`，待新源。**
3. **六个位置问的问题不同；承重墙是 M1/M2。** 没有同本体跨位置对照，也没有覆盖率测量；这份参考能给出分类与边界，不能给出效应量。

> **只读 5 页（约 30 分钟）**：本页 §0 → [地图 §2.3 六位置表](./sections/map.md#23-六个位置一页表) → [Claim 走查](./sections/claim-walkthrough.md) → [边界前五条](./sections/boundaries.md) → [证据台账](./evidence/ledger.md)。
>
> **内码**：B1–B15 = 证据边界；N01–N12 = 常见主张的反例；M1–M5 = 承重假设/研究期待；O-xx = 对象地址。详见 [术语](./sections/glossary.md)。
>
> **证据等级**：`已核` 只表示原文/代码读对了，不表示命题被验证；`H` 是组织假设，`D` 是工作定义/设计提案（概念架构），`G` 是缺口。不要把 03 的分类当成效应量。

## 0. 一页结论

- **强度不是好坏。** 强度问「违反时能不能改变走向」；覆盖率问「能碰到多少类失效」。强端管得硬，但管得少。
- **强端不是更好，是更窄（组织假设，非 E；证据见附录 §3.2）。** 它不是一条可排序的强度线：六位置是专门化的，查 [coverage 矩阵](./across-positions/coverage.md)，不查直线。
- **尺子跟机制走。** 不改变走向的供给/契约位置，准确率/token 仍可用；能改变走向的判定/动作/落盘位置，用单一 accuracy/reward 会错配（C-03）。
- **六个位置问的问题不同。** context 看到什么、memory 记得什么、evidence 带什么依据、checker 对不对、action 能不能做、commit 够不够授权；不是「六个都该做」。
- **承重墙是 M1/M2。** 没有同本体跨位置对照，也没有覆盖率测量；这份参考能给出分类与边界，不能给出效应量。



## 导航

| 节 | 文件 | 内容 |
|---|---|---|
| 导读 | [GUIDE.md](./GUIDE.md) | 先读哪一页、按什么顺序 |
| 2 地图 | [sections/map.md](./sections/map.md) | 主张类型、四轴、六位置、强度矩阵 |
| 3 主体 | [positions/README.md](./positions/README.md) | 六张位置卡 + 三张横切页索引 |
| 4 边界 | [sections/boundaries.md](./sections/boundaries.md) | 15 条边界 + 12 条反例；全文在 [boundaries.md](./evidence/boundaries.md) |
| 5 验收 | [sections/acceptance.md](./sections/acceptance.md) | M1–M5、缺口 |
| 6 关系 | [sections/relations.md](./sections/relations.md) | 与 01/02 的关系、维护、目录 |
| 术语 | [sections/glossary.md](./sections/glossary.md) | E/C/H/D/G、O/B/R、seams、覆盖率符号 |
| 读者检查 | [sections/reader-checks.md](./sections/reader-checks.md) | 5 组：定位/证据/边界/形态/判不了 |
| Claim 走查 | [sections/claim-walkthrough.md](./sections/claim-walkthrough.md) | 读路径能不能防泄漏 |
| Placement | [sections/placement.md](./sections/placement.md) | 五步把 claim 放到正确位置 |
| 模板 | [sections/templates.md](./sections/templates.md) | claim 走查空表 |
| 证据台账 | [evidence/ledger.md](./evidence/ledger.md) | E-xx 支持/不支持哪个位置 |
| 缺口 | [evidence/gaps.md](./evidence/gaps.md) | M1–M5、负结果、下一步 |

## 关注什么 / 需要什么材料

| 项 | 内容 |
|---|---|
| 关心 | 为什么是这些位置、形态怎么分、每条判断的证据边界在哪 |
| 需要材料 | E-xx、`topics/` 的 mechanism/seams/execution-forms、`boundaries.md` |
| 不做什么 | 不写操作手册（去 02）、不做能力判断（去 01）；只做依据与边界 |