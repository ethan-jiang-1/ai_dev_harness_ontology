---
status: draft
source_type: preprint
reading: 摘要级
provenance: 原文摘要
updated: 2026-11-07
arxiv: 2611.03743
title: EvoMemState: Evolving Memory State for Personal Agents
authors: Zhishang Xiang, Yunbo Tang, Zhongqiao Liu, et al.（厦门大学等）
pdf: 2611.03743-evomemstate.pdf
direction: 4
home: topics/04-state
subtopic: memory
updates: []
---

# EvoMemState

## 做了什么

把长期记忆从「独立事实集合」改为「**状态**」，拆成两层：

| 层 | 内容 | 由谁维护 |
|---|---|---|
| Relation State | 事实如何相互约束、失效、冲突 | 本体引导归纳 |
| Reasoning State | 当前请求该用哪些事实 | 从持续使用中学习（RL） |

初步研究指出两个失败：单独检索相关事实会漏掉更新与约束；证据完整时也可能用错，因为适用性、角色、优先级没定。

## 结果

跨记忆使用与对话回忆基准一致提升，尤其在**偏好更新**与**证据冲突**场景。

## 没测什么

**作者自述**：未在摘要列出。
**读者补充**：Reasoning State 依赖训练（RL），意味着冷启动与迁移成本未评估；本体在归纳中的具体角色未量化。

## 对本仓库的意义

| 关联 | 关系 |
|---|---|
| 04 状态派 | 核心文献：状态两层拆分 |
| [memory](../../../topics/04-state/memory/README.md) | 「事实集合 vs 状态」的直接对照 |

**最值得抄的**：把「哪些事实该用」从模型隐式判断里拿出来，变成一个显式的中间产物（Reasoning State）。这让「它为什么用了这条」可被检查。

## 待核

- [ ] 本体引导归纳的具体算法
- [ ] RL 训练数据的来源与规模
- [ ] 与 FIRME 的「本体只做槽位」路线相比，谁更可维护
