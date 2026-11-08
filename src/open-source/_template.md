---
repo: {org}/{repo}
url: https://github.com/{org}/{repo}
commit: {SHA or tag}
license: {MIT/Apache-2.0/...}
stars_at_scan: {number, date}
last_push: {YYYY-MM-DD}
source_type: open-source
ontology_role: {core | adjunct | none | marketing}
harness_seam: {supply | judgment | authorization | memory | generation | measure | harness | multiple}
execution: {executed | context | mixed | none}
status: seed
updated: YYYY-MM-DD
---

# {org}/{repo}

## 一句话

它是什么，不超过两行；不要抄 README 营销句。

## 本体在哪

- 文件/目录：
- 格式：OWL / SHACL / RDF / property graph schema / JSON schema / prompt
- 谁维护：
- 是否版本化/可回滚：

## harness 接缝

- 供给 / 判定 / 授权 / 记忆 / 生成 / 度量：
- 调用点（文件/函数）：
- 输入/输出：
- 失败时降级：

## 执行还是装饰

- 真的执行（SHACL/OWL/policy/约束检查）：
- 还是只塞进 prompt/上下文：
- 证据（测试/benchmark/issue/案例）：
- 不能证明什么：

## 与 digest 对照

| digest | 机制 | 这个项目对应/缺失 |
|---|---|---|
| | | |

## 代码地图

| 文件/函数 | 作用 | 备注 |
|---|---|---|
| | | |

## 局限

- license/维护风险：
- 未实现/未测：
- 与论文条件的差异：

## 为什么值得继续读

一句话；如果只是“star 多”，不值得。

## 下一步

- [ ] 定位执行点
- [ ] 跑最小示例/测试
- [ ] 写 code-map
- [ ] 回链 topics/digest
