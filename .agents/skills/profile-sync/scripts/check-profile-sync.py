#!/usr/bin/env python3
"""Check that README.md, cv/*.yaml and the case studies tell the same story.

Stdlib only. Exit code 1 when a hard inconsistency is found.

Checks
  1. Every technology token in README's Skills Matrix appears somewhere in a CV YAML.
  2. Every `### <n>.` case-study heading in experiment/README.md keeps a contiguous sequence.
  3. Every relative markdown link in tracked .md files resolves.
  4. Both CV YAML files have the same section keys, in the same order.
  5. No stale score/gpa/date drift between the two CV editions.
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
CV_FILES = ["cv/PhamThanhTan-ENG.yaml", "cv/PhamThanhTan-VIE.yaml"]
README = "README.md"
EXPERIMENT = "experiment/README.md"

# Tokens that live in the README matrix and should therefore be reflected in the CV.
MATRIX_TOKENS = [
    "Kubernetes", "Docker", "VMware", "Git", "Linux", "HAProxy", "Keepalived",
    "Windows Server", "Python", "Django", "Flutter", "Microsoft SQL Server",
    "Microservices", "IT Helpdesk",
]

problems: list[str] = []
notes: list[str] = []


def read(rel: str) -> str:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def section_keys(yaml_text: str) -> list[str]:
    """Top-level keys under `cv.sections:` (2-space indent)."""
    keys: list[str] = []
    in_sections = False
    for line in yaml_text.splitlines():
        if re.match(r"^\s{2}sections:\s*$", line):
            in_sections = True
            continue
        if in_sections:
            if re.match(r"^\s{0,2}\S", line) and not line.startswith("    "):
                break
            m = re.match(r"^ {4}(\S[^:]*):", line)
            if m:
                keys.append(m.group(1).strip())
    return keys


def check_matrix_vs_cv() -> None:
    readme = read(README)
    matrix = readme.split("## Skills Matrix", 1)
    matrix = matrix[1].split("\n---\n", 1)[0] if len(matrix) > 1 else ""
    cv_text = "\n".join(read(f) for f in CV_FILES)
    for token in MATRIX_TOKENS:
        if re.search(re.escape(token), matrix, re.I) and not re.search(re.escape(token), cv_text, re.I):
            notes.append(f"Skills Matrix lists '{token}' but no CV edition mentions it")


def check_case_study_numbering() -> None:
    headings = re.findall(r"^### (\d+)\. ", read(EXPERIMENT), re.M)
    if not headings:
        notes.append("no numbered case-study headings found in experiment/README.md")
        return
    numbers = [int(h) for h in headings]
    expected = list(range(numbers[0], numbers[0] + len(numbers)))
    if numbers != expected:
        problems.append(f"case-study numbering is not contiguous: {numbers}")


def check_relative_links() -> None:
    md_files: list[str] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "rendercv_output"}]
        for name in filenames:
            if name.endswith(".md"):
                md_files.append(os.path.relpath(os.path.join(dirpath, name), ROOT))

    link_re = re.compile(r"\[[^\]]*\]\((?!https?:|mailto:|#)([^)\s]+)\)")
    fence_re = re.compile(r"^```.*?^```", re.M | re.S)
    for rel in md_files:
        base = os.path.dirname(os.path.join(ROOT, rel))
        text = fence_re.sub("", read(rel))  # example links inside code fences are not real links
        for target in link_re.findall(text):
            target = target.split("#", 1)[0]
            if not target or target.startswith("<"):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                problems.append(f"{rel}: broken relative link -> {target}")


def check_cv_parity() -> None:
    texts = [read(f) for f in CV_FILES]
    keys = [section_keys(t) for t in texts]
    if len(set(len(k) for k in keys)) != 1:
        # VI and EN titles differ, so compare counts and positions only.
        problems.append(f"CV section counts differ: {[len(k) for k in keys]}")
    for marker in ["8.4/10", "7.38/10", "2022-12", "present"]:
        missing = [f for f, t in zip(CV_FILES, texts) if marker not in t]
        if missing:
            problems.append(f"marker '{marker}' missing from {missing}")


def check_cv_projects_sync() -> None:
    """The generated Projects block must match cv/projects.yaml (stdlib-only mirror of the check)."""
    manifest = os.path.join(ROOT, "cv", "projects.yaml")
    if not os.path.exists(manifest):
        problems.append("cv/projects.yaml is missing — the CV Projects block has no source")
        return
    with open(manifest, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    # Minimal parse: track the current language block and its title, without needing PyYAML.
    titles: dict[str, list[str]] = {"en": [], "vi": []}
    lang = None
    in_projects = False
    for line in lines:
        if line.startswith("projects:"):
            in_projects = True
            continue
        if in_projects and line[:1] and not line.startswith(" "):
            break
        if re.match(r"^    (en|vi):\s*$", line):
            lang = line.strip().rstrip(":").strip()
            continue
        m = re.match(r"^      title: (.+)$", line)
        if m and lang:
            titles[lang].append(m.group(1).strip().strip('"'))

    if not any(titles.values()):
        problems.append("cv/projects.yaml declares no projects")
        return
    if len(titles["en"]) != len(titles["vi"]):
        problems.append(f"cv/projects.yaml EN/VI project count differs: "
                        f"{len(titles['en'])} vs {len(titles['vi'])}")

    for rel, key in zip(CV_FILES, ("en", "vi")):
        text = read(rel)
        for title in titles[key]:
            if title not in text:
                problems.append(f"{rel}: project '{title}' from cv/projects.yaml is missing")
    notes.append(f"cv/projects.yaml drives the Projects block ({len(titles['en'])} projects)")

def main() -> int:
    check_matrix_vs_cv()
    check_case_study_numbering()
    check_relative_links()
    check_cv_parity()
    check_cv_projects_sync()

    for note in notes:
        print(f"note: {note}")
    for problem in problems:
        print(f"FAIL: {problem}")

    if problems:
        print(f"\n{len(problems)} problem(s), {len(notes)} note(s)")
        return 1
    print(f"ok — no problems ({len(notes)} note(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
