---
status: draft
updated: 2026-11-10
parent: ../README.md
---

# 04 证据

> 已入库走 E；未入库只标 signal，不作依据；旧源已删。

## 1. 已入库 E

| E | 用在哪 | 等级 |
|---|---|---|
| E-02 | 建：负例/验收 | 已核 |
| E-04 | 边界：输入 gate≠输出校验 | 已核 |
| E-06 | 边界：失败在 workflow | 已核 |
| E-12 | 建：薄层优先 | 已核 |
| E-19 | 全篇：位置×成本 | 推测（综合） |
| E-20 | 用/治：执行形态 | 已核（代码） |
| E-21 | 用：三路线 | 已核（原文） |
| E-22 | 治：三层访问 | 已核（原文+代码） |

依据：[conclusions](../../../topics/conclusions.md)；不新增 E。

## 2. 外部信号（未入库，只作旁证）

| 来源（signal） | 用在哪 |
|---|---|
| Industrial KG 2609.31663 | 建：schema 抽取 |
| SAGA 2607.14494 | 建：grounding |
| Legal KG 2607.24551 | 用：法规本体 |
| Build2SPARQL 2610.00224 | 用：building KGQA |
| Researcher Agents 2608.07700 | 用：predicate |
| Graph-Agentic 2609.06391 | 治：失败传播 |
| AWS 语义层指南 | 用：语义层/MCP |
| HN: Netflix ontology | 治：observability |
