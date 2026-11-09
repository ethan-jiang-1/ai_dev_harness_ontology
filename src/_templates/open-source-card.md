---
status: seed            # seed | draft | stabilized | superseded
source_type: open-source
reading: 未读           # 未读 | 已读代码 | 已跑通
provenance: 未核         # 一手代码 | 一手文档 | 未核
updated: YYYY-MM-DD
repo: {org}/{repo}
url: https://github.com/{org}/{repo}
commit:                 # SHA 或 release tag，必须 pin
release:
license:
scan_date: YYYY-MM-DD
stars_at_scan: 0        # 只作影响力参考，不是质量证明
last_push: YYYY-MM-DD
ontology_role: unclear  # core | adjunct | none | unclear（初判，定级在 digest）
seam: none              # 六时刻 | read-path | supply | reasoning | training | none
execution_form: unknown # engine | compiled | context | label | none | unknown（初判，定级在 digest）
evidence_role: mechanism-only  # execution-test | mechanism-only | harness-evidence | boundary-ruler
home:                   # 归位：topics/<派>
subtopic:
also_supports: []
updates: []             # 本卡修正后需要回改的 topics 文档
---

# {org}/{repo} · 来源卡

> **这是来源卡，不是消化正文。** 只记能定位到文件/链接的事实：它是什么、本体在哪、从哪调、证据入口在哪。
> 调用链、执行/装饰的定级、与论文机制的对照，都在同目录 `digest.md`；文件索引在 `code-map.md`。

## 一句话

它是什么（项目定位 + 谁在用），不超过两行；不复述 README 营销句。

## 本体在哪

| 项 | 内容 |
|---|---|
| 文件 / 目录 | |
| 格式 | OWL / SHACL / RDF / property graph schema / JSON schema / LinkML / prompt |
| 谁生成、谁加载 | |
| 是否版本化 / 可回滚 | |

## 调用点

- 入口（文件:符号）：
- 本体在哪一步被读入：
- 输入 / 输出：
- 失败时降级（拒绝 / 重试 / 忽略）：

> 只写「代码里发生了什么」；「算不算接缝、是执行还是装饰」的定级放 `digest.md`。

## 证据入口

- tests：
- benchmark：
- issue / 生产案例：
- 能否最小复现（命令 + 期望结果）：

## 与哪篇 digest 对照

| 论文 digest | 机制 | 这里对应 / 缺失 |
|---|---|---|
| | | |

## 局限

- license / 维护风险：
- 闭源 core / 未测部分：
- 与论文条件的差异：

## 待办

- [ ] pin commit（填进 frontmatter）
- [ ] 定位本体加载与调用点
- [ ] 跑官方最小示例（失败也记）
- [ ] 写 `code-map.md`
- [ ] 写 `digest.md`，回链 topics
