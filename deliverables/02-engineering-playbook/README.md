---
status: draft
deliverable_status: draft
updated: 2026-11-12
target: 工程负责人 / 架构师
basis: E-01–E-20, C-03; recipes R0–R12
---

# 02 · 工程实施：把本体接进 harness 的做法

> **读者**：工程负责人 / 架构师 ｜ **回答**：拿本体做某件事，具体怎么做 ｜ **不回答**：值不值得做（去 01）、为什么是这些位置（去 03）。
>
> **状态**：`draft` ｜ **计数**：A=3（R1/R10/R11）/ B=4（R2/R3/R7/R8）/ C=1（R9）/ gap=4（R4/R5/R6/R12，不含 R0） ｜ **证据重置**：R4/R5/R6/R12 原锚撤回，W 表见 [91-canonical](02-sections/91-canonical.md#w-table)。
>
> **本页只做索引**。正文从 [00-overview](02-sections/00-overview.md) 开始；配方从 [03-recipes](03-recipes/README.md) 选。

## 30 秒结论

1. **先定错、再选配方**：错可逆吗、会扩散吗、判定事实拿得到吗；先过 R0 准入，再选一条。详见 [overview §0.2](02-sections/00-overview.md#02-主线)。
2. **点位语义是最大单层增益**：+54.6pp；投影只再 +19.8pp（E-12；单工厂/9 任务）。先做点位语义，不要先建塔。详见 [overview §0.3](02-sections/00-overview.md#sec-0-3)。
3. **约束/判定配方今天不能承诺**：R4/R5/R6/R12 转 gap；R9 只有设计。详见 [overview §0.4](02-sections/00-overview.md#04-一页结论)。

> 如果只做一件事：R0 准入 + 账本 + 名字/单位（K1）；见 [overview §0.5](02-sections/00-overview.md#sec-0-5)。

## 目录

> 编号规则：目录号（`02-sections`）= 书里的第几块；文件号（`02-map`）= 第几章/第几页；同号不同层正常。若预览器不解析相对链接，按「路径」列在文件树里打开（目录行给出目录）。

| 用途 | 读 | 路径 |
|---|---|---|
| 工程摘要、案例、主线、三条判断 | [00-overview](02-sections/00-overview.md) | `deliverables/02-engineering-playbook/02-sections/00-overview.md` |
| 怎么读、按什么顺序 | [01-GUIDE](02-sections/01-GUIDE.md) | `deliverables/02-engineering-playbook/02-sections/01-GUIDE.md` |
| 五步法、定错、选位置/形态 | [02-map](02-sections/02-map.md) | `deliverables/02-engineering-playbook/02-sections/02-map.md` |
| R0–R12 索引、开源、架构、路线 | [03-approach](02-sections/03-approach.md) | `deliverables/02-engineering-playbook/02-sections/03-approach.md` |
| 13 条 recipe | [03-recipes](03-recipes/README.md) | `deliverables/02-engineering-playbook/03-recipes/README.md` |
| 边界、反模式、不能证明什么 | [04-boundaries](02-sections/04-boundaries.md) | `deliverables/02-engineering-playbook/02-sections/04-boundaries.md` |
| 验收、stop、缺口、期待 | [05-acceptance](02-sections/05-acceptance.md) | `deliverables/02-engineering-playbook/02-sections/05-acceptance.md` |
| 账本/评测/成本/上线/领域 | [04-operations](04-operations/) | `deliverables/02-engineering-playbook/04-operations/` |
| 接口/追溯/案例/产物包 | [05-appendices](05-appendices/) | `deliverables/02-engineering-playbook/05-appendices/` |
| 术语与内码 | [90-glossary](02-sections/90-glossary.md) | `deliverables/02-engineering-playbook/02-sections/90-glossary.md` |
| 阈值、计数、W 表 | [91-canonical](02-sections/91-canonical.md) | `deliverables/02-engineering-playbook/02-sections/91-canonical.md` |

## 阅读顺序

| 时间 | 读什么 |
|---|---|
| 10 分钟 | 本页 → [overview §0.2–§0.5](02-sections/00-overview.md) → [R0 四项检查](03-recipes/00-readiness.md) |
| 40 分钟 | [01-GUIDE](02-sections/01-GUIDE.md) 的路径：overview → map §2.1 五步法 + §2.2 分诊 → R0 体检 → 一条 recipe → 产物包 |
| 评审/深读 | 04-boundaries → 05-acceptance → 91-canonical → 90-glossary |

## 维护

- **计数与阈值以 [91-canonical](02-sections/91-canonical.md) 为准**；本页不重复细节。
- 改配方：先改 [03-recipes](03-recipes/README.md)，再回 03-approach 与 91-canonical。
- 术语来源：`N:` / `local` 读法见 [90-glossary §0](02-sections/90-glossary.md#term-sources)。
- 本页只做索引；不新增判断，不复制正文。
