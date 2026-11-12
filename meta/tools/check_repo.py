#!/usr/bin/env python3
"""Repository self-check for ai_dev_harness_ontology.

Read-only. Run from the repo root:

    python3 meta/tools/check_repo.py

Exit code 0 = pass, 1 = errors. Warnings do not fail.

It checks the things a human checklist kept missing:
  * relative links resolve, including the #anchor part
  * frontmatter enums are legal
  * E/Q/C/L ids are defined before use
  * paper directories, manifest rows and card fields agree
  * meta/status/state.md's file count agrees with the filesystem

It deliberately does not judge prose or evidence quality.
"""

from __future__ import annotations

import os
import glob as glob_mod
import re
import sys
from collections import Counter
from urllib.parse import unquote

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
ADMISSION = {"admitted", "admitted (probation)", "signal", "excluded"}
FRESHNESS_CUTOFF = "2026-06-01"

RAW_PAPER = re.compile(r"^src/papers/[^/]+/(paper|references|appendix)\.md$")
SKIP_FRONTMATTER = {"README.md", "AGENTS.md", "GLOSSARY.md", "THESIS.md"}


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT)


def md_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", ".tmp-venv", ".pi"}]
        for name in filenames:
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def strip_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def heading_slug(heading: str) -> str:
    """Approximate GitHub's heading anchor slug (CJK kept, punctuation dropped)."""
    h = re.sub(r"`", "", heading)
    h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h)
    h = re.sub(r"<[^>]+>", "", h).strip().lower()
    h = re.sub(r"[^\w\u4e00-\u9fff\- ]", "", h)
    return h.replace(" ", "-")


def anchors_for(path: str) -> set[str]:
    """Heading slugs plus explicit <a id="..."> anchors in one markdown file."""
    text = strip_code(open(path, encoding="utf-8").read())
    anchors = set(re.findall(r"""<[^>]*\bid=["']([^"']+)["']""", text))
    seen = Counter()
    for line in text.splitlines():
        if not line.startswith("#"):
            continue
        base = heading_slug(re.sub(r"^#+\s+", "", line))
        n = seen[base]
        anchors.add(base if n == 0 else f"{base}-{n}")
        seen[base] += 1
    return anchors


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

    # 1. relative links (file target + anchor)
    anchor_cache = {}
    for path, text in texts.items():
        body = strip_code(text)
        for m in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)\)", body):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            file_part, _, anchor = target.partition("#")
            anchor = unquote(anchor).strip()
            if file_part:
                resolved = os.path.normpath(os.path.join(os.path.dirname(path), file_part))
                if not os.path.exists(resolved):
                    errors.append(f"broken link: {rel(path)} -> {file_part}")
                    continue
            else:
                resolved = path
            if not anchor or not resolved.endswith(".md") or not os.path.isfile(resolved):
                continue
            if resolved not in anchor_cache:
                anchor_cache[resolved] = anchors_for(resolved)
            if anchor not in anchor_cache[resolved]:
                errors.append(f"broken anchor: {rel(path)} -> {rel(resolved)}#{anchor}")

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
            ("admission", ADMISSION),
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
    for d in paper_dirs:
        base = os.path.join(papers_dir, d)
        required = ["card.md", "digest.md", "paper.md", "references.md", "appendix.md"]
        for name in required:
            if not os.path.exists(os.path.join(base, name)):
                errors.append(f"missing {name}: src/papers/{d}")
        if not any(f.endswith(".pdf") for f in os.listdir(base)):
            errors.append(f"missing pdf: src/papers/{d}")
        card_path = os.path.join(base, "card.md")
        if not os.path.exists(card_path):
            continue
        card, _ = parse_frontmatter(open(card_path, encoding="utf-8").read())
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
            if scalar(card, "admission") and scalar(card, "admission").startswith("admitted"):
                published = scalar(card, "published")
                if not published or published < FRESHNESS_CUTOFF:
                    errors.append(f"stale admitted source (published {published!r}): src/papers/{d}/card.md")
                if not scalar(card, "impact_evidence"):
                    errors.append(f"admitted without impact_evidence: src/papers/{d}/card.md")

    # 4b. evidence role / execution form coverage
    role_counts = Counter()
    form_counts = Counter()
    for d in paper_dirs:
        card_path = os.path.join(papers_dir, d, "card.md")
        if not os.path.exists(card_path):
            continue
        card, _ = parse_frontmatter(open(card_path, encoding="utf-8").read())
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

    # 4b-2. active conclusion rows must carry a 做法 sentence + a practice link (route B)
    sec = None
    for line in conclusions.splitlines():
        if line.startswith("## "):
            sec = line[3:].strip()
            continue
        m = re.match(r"\|\s*(E-\d+)\s*\|", line)
        if not m or sec == "已撤回（源未过准入）" or "| withdrawn |" in line:
            continue
        eid = m.group(1)
        if "做法" not in line:
            warnings.append(f"{eid} has no 做法 sentence (route B: E is an index, practice must be one line)")
        if not re.search(r"mechanism|read-path|execution-forms|output-validation|consumability|policy/", line):
            warnings.append(f"{eid} has no practice link (route B: point at mechanism where steps/params/stop live)")

    # 4c. every deliverable has a SCOPE.md positioning contract (ADR 0014)
    deliv_dir = os.path.join(ROOT, "deliverables")
    for d in sorted(os.listdir(deliv_dir)):
        base = os.path.join(deliv_dir, d)
        if os.path.isdir(base) and re.match(r"^0\d-", d):
            if not os.path.exists(os.path.join(base, "SCOPE.md")):
                errors.append(f"missing SCOPE.md: deliverables/{d}")
            if not os.path.exists(os.path.join(base, "README.md")):
                errors.append(f"missing README.md: deliverables/{d}")

    # 4d. thin pages declared by school README must self-mark
    for school in sorted(glob_mod.glob(os.path.join(ROOT, "topics", "0*", "README.md"))):
        text = open(school, encoding="utf-8").read()
        m = re.search(r"\*\*薄页（<2 篇独立来源）\*\*：(.+)", text)
        if not m:
            continue
        for name in re.findall(r"([a-z][a-z0-9-]+)（", m.group(1)):
            page = os.path.join(os.path.dirname(school), name, "README.md")
            if not os.path.exists(page):
                warnings.append(f"thin-page list names missing dir: {name} ({os.path.relpath(school, ROOT)})")
                continue
            if "薄页（<2 篇独立来源）" not in open(page, encoding="utf-8").read():
                warnings.append(f"thin page not self-marked: topics/{os.path.basename(os.path.dirname(school))}/{name}/README.md")

    # 5. manifest coverage
    manifest = os.path.join(papers_dir, "manifest.md")
    if os.path.exists(manifest):
        rows = re.findall(r"^\|\s*\d+\s*\|\s*admitted[^|]*\|\s*(\d{4}\.\d{4,5})\s*\|", open(manifest, encoding="utf-8").read(), re.M)
        if len(rows) != len(paper_dirs):
            errors.append(f"manifest rows: expected {len(paper_dirs)}, found {len(rows)}")
        admission_col = "准入" in open(manifest, encoding="utf-8").read()
        if not admission_col:
            errors.append("manifest has no 准入 column")

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
            last_push = scalar(card, "last_push")
            if not last_push or last_push < FRESHNESS_CUTOFF:
                errors.append(f"stale open-source (last_push {last_push!r}): src/open-source/{d}/card.md")
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
        if m and "| withdrawn |" in line:
            continue
        if m and section in {"已核（一手原文摘要）", "已核（代码）", "推测（未核原文）", "存疑", "冲突"}:
            key = {"已核（一手原文摘要）": "已核", "已核（代码）": "已核", "推测（未核原文）": "推测"}.get(section, section)
            counts[key] += 1
    if counts["已核"] != 15 or counts["推测"] != 3:
        warnings.append(f"conclusion levels changed: {dict(counts)} (meta/state may need update)")

    # 7a. withdrawn conclusions must not carry weight for live rows (grades follow evidence)
    withdrawn = set()
    for line in conclusions.splitlines():
        m = re.match(r"\|\s*(E-\d+)\s*\|", line)
        if m and "| withdrawn |" in line:
            withdrawn.add(m.group(1))
    section = None
    for line in conclusions.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if section == "已撤回（源未过准入）" or not line.startswith("|"):
            continue
        m = re.match(r"\|\s*([EQLC]-\d+)\s*\|", line)
        if not m:
            continue
        hit = [w for w in withdrawn if w in line]
        if hit and not re.search(r"已撤回|撤回|作历史|withdrawn|待新源", line):
            warnings.append(f"{m.group(1)} cites withdrawn {sorted(hit)} as support (topics/conclusions.md)")

    # 7b. state.md is the single authoritative count; keep it equal to the tree
    state_path = os.path.join(ROOT, "meta/status/state.md")
    state_text = texts.get(state_path, "")
    if os.path.exists(state_path):
        state_match = re.search(r"\|\s*最后自检\s*\|[^\n]*?(\d+)\s*个\s*md", state_text)
        if not state_match:
            warnings.append("meta/status/state.md has no '最后自检 ... <N> 个 md' row")
        elif int(state_match.group(1)) != len(files):
            errors.append(f"meta/state md count {state_match.group(1)} != actual {len(files)}")

        web_cards = sum(
            1 for _, _, fs in os.walk(os.path.join(ROOT, "src/web"))
            for f in fs if f.endswith(".card.md")
        )
        for label, pattern, actual in (
            ("papers", r"\|\s*论文\s*\|\s*(\d+)\s*个目录", len(paper_dirs)),
            ("open-source", r"\|\s*开源\s*\|\s*(\d+)\s*个项目", len(oss_projects)),
            ("material cards", r"\|\s*材料卡\s*\|\s*(\d+)\s*张", web_cards),
        ):
            m = re.search(pattern, state_text)
            if not m:
                warnings.append(f"meta/status/state.md has no {label} count row")
            elif int(m.group(1)) != actual:
                errors.append(f"meta/state {label} count {m.group(1)} != actual {actual}")

        forms = re.search(
            r"\|\s*执行形态[^|]*\|\s*engine (\d+) / compiled (\d+) / context (\d+) / label (\d+) / none (\d+)",
            state_text,
        )
        if not forms:
            warnings.append("meta/status/state.md has no execution_form distribution row")
        else:
            got = dict(zip(("engine", "compiled", "context", "label", "none"), map(int, forms.groups())))
            for key, value in got.items():
                if form_counts.get(key, 0) != value:
                    errors.append(f"meta/state execution_form {key}={value} != actual {form_counts.get(key, 0)}")
            if sum(got.values()) != sum(form_counts.values()):
                errors.append(f"meta/state execution_form total {sum(got.values())} != actual {sum(form_counts.values())}")

    # 9. object registry (topics/objects.md): warn-only
    objects_path = os.path.join(ROOT, "topics/objects.md")
    object_ids = set()
    object_counts = Counter()
    if os.path.exists(objects_path):
        heading_cache = {}

        def heading_slugs(path):
            if path not in heading_cache:
                try:
                    text = open(path, encoding="utf-8").read()
                except OSError:
                    heading_cache[path] = set()
                else:
                    text = strip_code(text)
                    slugs = set(re.findall(r"""<[^>]*\bid=["']([^"']+)["']""", text))
                    for line in text.splitlines():
                        if line.startswith("#"):
                            h = re.sub(r"^#+\s+", "", line).strip().lower()
                            h = re.sub(r"[^\w\u4e00-\u9fff \-]", "", h)
                            slugs.add(h.replace(" ", "-"))
                    heading_cache[path] = slugs
            return heading_cache[path]

        for line in open(objects_path, encoding="utf-8"):
            m = re.match(r"\|\s*(O-[CFTMNRP]\d\d)\s*\|", line)
            if not m:
                continue
            oid = m.group(1)
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 9:
                warnings.append(f"object row too short: {oid}")
                continue
            if oid in object_ids:
                warnings.append(f"duplicate object id: {oid}")
            object_ids.add(oid)
            _, claim, value, address, domain, prov, hardness, falsifier, feeds = cells[:9]
            for name, val in (("claim", claim), ("value", value), ("address", address),
                              ("domain", domain), ("provenance", prov), ("falsifier", falsifier),
                              ("feeds", feeds)):
                if not val:
                    warnings.append(f"object {oid}: empty {name}")
            if hardness not in {"H1", "H2", "H3"}:
                warnings.append(f"object {oid}: bad hardness {hardness!r}")
            object_counts[hardness] += 1
            am = re.search(r"([^\s（]+?\.md)#([^\s（）]+)", address)
            if am:
                path, anchor = am.group(1), am.group(2)
                target = os.path.normpath(os.path.join(ROOT, path))
                if not os.path.exists(target):
                    warnings.append(f"object {oid}: missing address file {path}")
                elif anchor not in heading_slugs(target):
                    warnings.append(f"object {oid}: missing anchor #{anchor} in {path}")

        # references anywhere in markdown
        for path, text in texts.items():
            name = rel(path)
            if name == os.path.join("topics", "objects.md"):
                continue
            for oid in set(re.findall(r"\b(O-[CFTMNRP]\d\d)\b", text)):
                if oid not in object_ids:
                    warnings.append(f"undefined {oid}: {name}")

        state_objects = re.search(r"\|\s*硬对象\s*\|\s*(\d+)", state_text)
        if not state_objects:
            warnings.append("meta/status/state.md has no 硬对象 count row")
        elif int(state_objects.group(1)) != len(object_ids):
            errors.append(f"meta/state object count {state_objects.group(1)} != actual {len(object_ids)}")

    # 8. summary
    print(f"md files: {len(files)}  papers: {len(paper_dirs)}  open-source: {len(oss_projects)}")
    print(f"defined: E={len(defined_e)} Q={len(defined_q)} C={len(defined_c)} L={len(defined_l)}")
    print(f"conclusion levels: {dict(counts)}")
    print(f"evidence_role: {dict(role_counts)}")
    if object_ids:
        print(f"objects: {len(object_ids)} (H3 {object_counts.get('H3', 0)} / H2 {object_counts.get('H2', 0)} / H1 {object_counts.get('H1', 0)})")
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
    print("\nOK: links, anchors, frontmatter, ids, inventory, counts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
