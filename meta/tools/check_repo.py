#!/usr/bin/env python3
"""Repository self-check for ai_dev_harness_ontology.

Read-only. Run from the repo root:

    python3 meta/tools/check_repo.py

Exit code 0 = pass, 1 = errors. Warnings do not fail.

It checks the things a human checklist kept missing:
  * relative links resolve
  * frontmatter enums are legal
  * E/Q/C/L ids are defined before use
  * paper directories, manifest rows and card fields agree
  * known counts in the ledgers agree with the filesystem

It deliberately does not judge prose or evidence quality.
"""

from __future__ import annotations

import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STATUS = {"seed", "draft", "stabilized", "superseded"}
SOURCE_TYPE = {"paper", "preprint", "blog", "engineering", "standard", "talk", "survey", "open-source"}
READING = {"未读", "综述级", "摘要级", "精读", "已消化", "已读代码", "已跑通"}
PROVENANCE = {"原文正文", "原文摘要", "综述转述", "未核", "一手代码", "一手文档"}
QUALITY = {"A", "B", "C"}
EXPERIMENT_STATUS = {"未开始", "设计中", "运行中", "已完成", "已放弃"}
DELIVERABLE_STATUS = {"draft", "stable", "frozen"}
SEAM = {"action-gate", "evidence", "checker", "commit-gate", "memory", "determinism", "read-path", "supply", "reasoning", "training", "none"}
EXECUTION_FORM = {"engine", "compiled", "context", "label", "none", "unknown"}
EVIDENCE_ROLE = {"execution-test", "mechanism-only", "harness-evidence", "boundary-ruler", "unclear"}

RAW_PAPER = re.compile(r"^src/papers/[^/]+/(paper|references|appendix)\.md$")
SKIP_FRONTMATTER = {"README.md", "AGENTS.md", "GLOSSARY.md", "THESIS.md"}


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT)


def md_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def strip_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "-")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields, text[m.end():]


def scalar(fields, key):
    value = fields.get(key, "").strip()
    if not value or value.startswith("["):
        return None
    return value.split("#")[0].strip()


def main() -> int:
    errors = []
    warnings = []

    files = list(md_files())
    texts = {}
    for path in files:
        try:
            texts[path] = open(path, encoding="utf-8").read()
        except UnicodeDecodeError:
            warnings.append(f"non-utf8: {rel(path)}")

    # 1. relative links
    for path, text in texts.items():
        body = strip_code(text)
        for m in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)\)", body):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#")[0]
            if not target:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                errors.append(f"broken link: {rel(path)} -> {target}")

    # 2. frontmatter enums
    for path, text in texts.items():
        fields, _ = parse_frontmatter(text)
        if fields is None:
            continue
        name = rel(path)
        status = scalar(fields, "status")
        if status and status not in STATUS:
            errors.append(f"bad status {status!r}: {name}")
        for key, allowed in (
            ("source_type", SOURCE_TYPE),
            ("reading", READING),
            ("provenance", PROVENANCE),
            ("quality", QUALITY),
            ("experiment_status", EXPERIMENT_STATUS),
            ("deliverable_status", DELIVERABLE_STATUS),
            ("seam", SEAM),
            ("execution_form", EXECUTION_FORM),
            ("evidence_role", EVIDENCE_ROLE),
        ):
            value = scalar(fields, key)
            if value and value not in allowed:
                errors.append(f"bad {key} {value!r}: {name}")
        if (
            "updated" not in fields
            and name not in SKIP_FRONTMATTER
            and not name.startswith("src/_templates/")
            and not RAW_PAPER.match(name)
            and not name.startswith("meta/tools/")
        ):
            warnings.append(f"no updated: {name}")

    # 3. id definitions
    conclusions = texts.get(os.path.join(ROOT, "topics/conclusions.md"), "")
    defined_e = set(re.findall(r"\|\s*(E-\d+)\s*\|", conclusions))
    defined_q = set(re.findall(r"\|\s*(Q-\d+)\s*\|", conclusions))
    defined_c = set(re.findall(r"\|\s*(C-\d+)\s*\|", conclusions))
    if not defined_e:
        errors.append("no E ids parsed from topics/conclusions.md")

    defined_l = set()
    for path, text in texts.items():
        if "/claims.md" in path:
            defined_l.update(re.findall(r"\|\s*(\d{2}-L\d+)\s*\|", text))

    for path, text in texts.items():
        name = rel(path)
        if RAW_PAPER.match(name) or name.startswith("src/web/") or name.startswith("meta/tools/"):
            continue
        for eid in set(re.findall(r"\bE-\d{2}\b", text)):
            if eid not in defined_e:
                errors.append(f"undefined {eid}: {name}")
        for qid in set(re.findall(r"\bQ-\d{2}\b", text)):
            if qid not in defined_q:
                errors.append(f"undefined {qid}: {name}")
        for cid in set(re.findall(r"\bC-\d{2}\b", text)):
            if cid not in defined_c:
                errors.append(f"undefined {cid}: {name}")
        for lid in set(re.findall(r"\b(\d{2}-L\d+)\b", text)):
            if lid not in defined_l:
                errors.append(f"undefined {lid}: {name}")

    # 4. paper inventory
    papers_dir = os.path.join(ROOT, "src/papers")
    paper_dirs = sorted(
        d for d in os.listdir(papers_dir)
        if os.path.isdir(os.path.join(papers_dir, d)) and not d.startswith("_")
    )
    if len(paper_dirs) != 22:
        errors.append(f"paper directories: expected 22, found {len(paper_dirs)}")
    for d in paper_dirs:
        base = os.path.join(papers_dir, d)
        required = ["card.md", "digest.md", "paper.md", "references.md", "appendix.md"]
        for name in required:
            if not os.path.exists(os.path.join(base, name)):
                errors.append(f"missing {name}: src/papers/{d}")
        if not any(f.endswith(".pdf") for f in os.listdir(base)):
            errors.append(f"missing pdf: src/papers/{d}")
        card, _ = parse_frontmatter(open(os.path.join(base, "card.md"), encoding="utf-8").read())
        if card:
            if scalar(card, "home") and scalar(card, "home") not in {
                "topics/01-constraint", "topics/02-judgment", "topics/03-knowledge",
                "topics/04-state", "topics/05-produce", "topics/06-measure",
            }:
                errors.append(f"bad home {scalar(card, 'home')!r}: src/papers/{d}/card.md")
            home = scalar(card, "home")
            # also_supports is a simple inline list; strip the bracketed prefix
            raw = card.get("also_supports", "").strip("[] ")
            subs = [x.strip("'\" ") for x in raw.split(",") if x.strip("'\" ")]
            for sub in ([scalar(card, "subtopic")] if scalar(card, "subtopic") else []) + subs:
                if home and sub and not os.path.exists(os.path.join(ROOT, home, sub, "README.md")):
                    errors.append(f"unknown subtopic {sub!r}: src/papers/{d}/card.md")
            if not scalar(card, "subtopic"):
                warnings.append(f"no subtopic: src/papers/{d}/card.md")

    # 4b. evidence role / execution form coverage
    role_counts = Counter()
    form_counts = Counter()
    for d in paper_dirs:
        card, _ = parse_frontmatter(open(os.path.join(papers_dir, d, "card.md"), encoding="utf-8").read())
        if not card:
            errors.append(f"no frontmatter: src/papers/{d}/card.md")
            continue
        for key in ("evidence_role", "execution_form"):
            value = scalar(card, key)
            if not value:
                errors.append(f"missing {key}: src/papers/{d}/card.md")
        if scalar(card, "evidence_role") in EVIDENCE_ROLE:
            role_counts[scalar(card, "evidence_role")] += 1
        if scalar(card, "execution_form") in EXECUTION_FORM:
            form_counts[scalar(card, "execution_form")] += 1

    # 5. manifest coverage
    manifest = os.path.join(papers_dir, "manifest.md")
    if os.path.exists(manifest):
        rows = re.findall(r"^\|\s*\d+\s*\|\s*(?:基础|扫描)\s*\|\s*(\d{4}\.\d{4,5})\s*\|", open(manifest, encoding="utf-8").read(), re.M)
        if len(rows) != len(paper_dirs):
            errors.append(f"manifest rows: expected {len(paper_dirs)}, found {len(rows)}")
        batch = "批次" in open(manifest, encoding="utf-8").read()
        if not batch:
            errors.append("manifest has no batch column")

    # 6. open-source inventory
    oss_dir = os.path.join(ROOT, "src/open-source")
    oss_projects = sorted(
        d for d in os.listdir(oss_dir)
        if os.path.isdir(os.path.join(oss_dir, d)) and not d.startswith("_")
    )
    for d in oss_projects:
        base = os.path.join(oss_dir, d)
        for name in ("card.md", "digest.md"):
            if not os.path.exists(os.path.join(base, name)):
                errors.append(f"missing {name}: src/open-source/{d}")
        card, _ = parse_frontmatter(open(os.path.join(base, "card.md"), encoding="utf-8").read())
        if card and not scalar(card, "commit"):
            errors.append(f"no commit pin: src/open-source/{d}/card.md")
        if card:
            for key in ("evidence_role", "execution_form", "seam"):
                if not scalar(card, key):
                    errors.append(f"missing {key}: src/open-source/{d}/card.md")
            if scalar(card, "evidence_role") in EVIDENCE_ROLE:
                role_counts[scalar(card, "evidence_role")] += 1
            if scalar(card, "execution_form") in EXECUTION_FORM:
                form_counts[scalar(card, "execution_form")] += 1

    # 6b. open-source README table agrees with card seam
    oss_readme = os.path.join(oss_dir, "README.md")
    if os.path.exists(oss_readme):
        readme = open(oss_readme, encoding="utf-8").read()
        for d in oss_projects:
            card, _ = parse_frontmatter(open(os.path.join(oss_dir, d, "card.md"), encoding="utf-8").read())
            if not card:
                continue
            repo = scalar(card, "repo")
            seam = scalar(card, "seam")
            if not repo or not seam:
                continue
            for line in readme.splitlines():
                if f"github.com/{repo}" in line and line.startswith("|"):
                    cells = [c.strip() for c in line.split("|")]
                    if len(cells) > 4 and seam not in cells[4]:
                        errors.append(f"README seam mismatch: {repo} card={seam} table={cells[4]!r}")

    # 7. conclusion level counts (section based; rows do not repeat the level)
    counts = Counter()
    section = None
    for line in conclusions.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        m = re.match(r"\|\s*(E-\d+)\s*\|", line)
        if m and section in {"已核（一手原文摘要）", "已核（代码）", "推测（未核原文）", "存疑", "冲突"}:
            key = {"已核（一手原文摘要）": "已核", "已核（代码）": "已核", "推测（未核原文）": "推测"}.get(section, section)
            counts[key] += 1
    if counts["已核"] != 18 or counts["推测"] != 2:
        warnings.append(f"conclusion levels changed: {dict(counts)} (meta/state may need update)")
    expected_roles = {"execution-test": 9, "mechanism-only": 8, "harness-evidence": 6, "boundary-ruler": 3}
    if dict(role_counts) != expected_roles:
        errors.append(f"evidence_role counts: expected {expected_roles}, found {dict(role_counts)}")
    expected_forms = {"engine": 4, "compiled": 7, "context": 2, "label": 1, "none": 12}
    if dict(form_counts) != expected_forms:
        errors.append(f"execution_form counts: expected {expected_forms}, found {dict(form_counts)}")

    # 8. summary
    print(f"files: {len(files)}  papers: {len(paper_dirs)}  open-source: {len(oss_projects)}")
    print(f"defined: E={len(defined_e)} Q={len(defined_q)} C={len(defined_c)} L={len(defined_l)}")
    print(f"conclusion levels: {dict(counts)}")
    print(f"evidence_role: {dict(role_counts)}")
    print(f"execution_form: {dict(form_counts)}")
    if warnings:
        print(f"\nWARNINGS ({len(warnings)})")
        for w in warnings:
            print("  -", w)
    if errors:
        print(f"\nERRORS ({len(errors)})")
        for e in errors:
            print("  -", e)
        return 1
    print("\nOK: links, frontmatter, ids, inventory, counts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
