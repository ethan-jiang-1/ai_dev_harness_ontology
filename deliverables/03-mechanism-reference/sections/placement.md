---
status: draft
updated: 2026-11-11
parent: ../README.md
---

# Placement：把一条 claim 放到正确的位置

> 这一步回答「它属于哪个位置」；不是「它有没有用」。五步，判不了就写 `undetermined`。

## 0. 五步

| 步 | 问什么 | 判据 | 判不了 |
|---|---|---|---|
| 1 | 机器有没有拿本体**做事**？ | 有执行（查询/校验/过滤/编译）→ 继续；只是「写进 prompt」→ `context`；没有执行 → `outside` / `none` | 读代码/文档，找不到执行点 → `none` |
| 2 | 在哪个**时刻**？ | 检索返回前 → `read-path`；进上下文前 → `supply`/`context`；输出时 → `evidence`；输出后 → `checker`；动作前 → `action`；落盘前 → `commit`；跨轮 → `memory`；跨运行 → `determinism` | 两个时刻都像 → 步 5 |
| 3 | **粒度**是什么？ | 单个节点 → node；谓词/列 → predicate；图 → graph；三元组 → triple | 实现只给两种粒度 → 写清两种 |
| 4 | 是 **gate** 还是 **filter**？ | 能阻断/拒绝 → gate；只删/改结果 → filter；异常放行 → fail-open；异常拒绝 → fail-closed | 文档没说异常路径 → `?` |
| 5 | 两格都像怎么办？ | 写 `undetermined` + 「做哪个测试能分开」 | 不要硬选 |

## 1. 三个常混的案例

### 1.1 read-path vs context

- **read-path**：在结果返回前**删/改行**（按 policy 删三元组、删节点）。它改变「能看见什么」。
- **context**：把知识**组织/格式化**进上下文（投影、分节、摘要）。它改变「怎么给」，不删行。
- **判据**：如果实现里有「删除/拒绝」的动作，是 read-path；如果只是「选择/格式化」，是 context。
- **反例**：把「检索前过滤」叫 context，会把「越权可见」误判成「供给问题」。

### 1.2 determinism vs memory

- **memory**：跨**轮/会话**保留状态（身份、事实、冲突）。
- **determinism**：跨**运行**同一输入是否收敛/可复现。
- **判据**：对象是「对话状态」还是「运行产物」；前者 memory，后者 determinism。
- **反例**：memory 卡 §4 把「跨运行不确定」列为失效模式——那是**效果/原因**，不是位置；位置仍是 determinism，memory 只是可能的来源。

### 1.3 `none` 不是位置

- `execution-forms` 里的 `none` 是**形态**（机器没执行本体），不是位置。
- 一个项目可以是 `position = outside` + `form = none`；不要写「位置 = none」。
- **判据**：先填位置（六时刻/轴外），再填形态（engine/compiled/context/label/none）。

## 2. 记录模板

```text
claim: <一句话>
位置: <context/memory/evidence/checker/action/commit/read-path/determinism/supply/outside>
时刻: <检索前/输出时/.../跨运行>
粒度: <node/predicate/graph/triple>
形态: <engine/compiled/context/label/none>
异常: <fail-open/fail-closed/?>
判不了: <缺哪个测试>
```

## 3. 边界

- **位置 ≠ 效应量**：放对位置不证明有用；效应量回 E-xx。
- **位置 ≠ 成熟度**：同一位置可以有实现/模拟/设计；看 [map §2.1](./map.md)。
- **`undetermined` 是合法出口**：判不了比硬塞好；写清缺什么测试。
