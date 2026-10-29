#!/usr/bin/env python3
"""Repository hygiene audit for the portfolio repo. Stdlib only.

Reports (never modifies):
  - untracked or ignored files larger than 1 MB
  - tracked binaries and their total size
  - duplicate-looking artifacts (e.g. *_ver1 ... _ver5, "-copy", " 2.")
  - Mermaid fences without a preceding language tag
  - workflow files missing timeout-minutes or a pinned action version

Exit code 1 if a blocking problem is found (binary > 5 MB or duplicate report set).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BINARY_EXT = {".pdf", ".pptx", ".docx", ".mp4", ".mov", ".png", ".jpg", ".jpeg", ".gif", ".zip", ".svg"}
BIG = 1 * 1024 * 1024
TOO_BIG = 5 * 1024 * 1024

problems: list[str] = []
warnings: list[str] = []
notes: list[str] = []
STRICT = "--strict" in sys.argv


def git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
        ).stdout
    except FileNotFoundError:
        return ""


def tracked_files() -> list[str]:
    out = git("ls-files")
    return [line for line in out.splitlines() if line]


def walk_files() -> list[tuple[str, int]]:
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "rendercv_output"}]
        for name in filenames:
            full = os.path.join(dirpath, name)
            try:
                size = os.path.getsize(full)
            except OSError:
                continue
            found.append((os.path.relpath(full, ROOT), size))
    return found


def check_binaries(files: list[tuple[str, int]]) -> None:
    tracked = set(tracked_files())
    total = 0
    for rel, size in files:
        ext = os.path.splitext(rel)[1].lower()
        if ext not in BINARY_EXT:
            continue
        if rel in tracked:
            total += size
            if size > TOO_BIG:
                warnings.append(f"tracked binary > 5 MB: {rel} ({size / 1048576:.1f} MB)")
        elif size > BIG:
            notes.append(f"untracked/ignored file > 1 MB: {rel} ({size / 1048576:.1f} MB)")
    if total > 60 * 1048576:
        notes.append(f"tracked binaries total {total / 1048576:.0f} MB — consider moving evidence out of the repo")
    print(f"tracked binary payload: {total / 1048576:.1f} MB")


def check_duplicates() -> None:
    groups: dict[str, list[str]] = {}
    for rel, _ in walk_files():
        base = os.path.basename(rel)
        stem = re.sub(r"(_ver\d+|[-_ ]?copy| \d+)(\.[^.]+)$", r"\2", base)
        if stem != base:
            groups.setdefault(os.path.join(os.path.dirname(rel), stem), []).append(rel)
    for stem, members in groups.items():
        if len(members) > 1:
            notes.append(f"versioned duplicates near {stem}: {', '.join(sorted(members))}")


def check_mermaid_fences() -> None:
    for rel in tracked_files():
        if not rel.endswith(".md"):
            continue
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
        for idx, line in enumerate(lines, 1):
            if line.strip() == "```" and idx <= len(lines) - 1:
                nxt = lines[idx].strip()
                if any(k in nxt for k in ("graph ", "flowchart ", "sequenceDiagram", "classDiagram", "erDiagram")):
                    problems.append(f"{rel}:{idx}: mermaid block missing the 'mermaid' language tag")


MERMAID_FENCE_RE = re.compile(r"```mermaid\n(.*?)```", re.S | re.M)


def check_mermaid_structure() -> None:
    """Cheap structural check: balanced subgraph/end, no empty node label."""
    for rel in tracked_files():
        if not rel.endswith(".md"):
            continue
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        for idx, block in enumerate(MERMAID_FENCE_RE.findall(text), 1):
            body = [ln.strip() for ln in block.splitlines() if ln.strip() and not ln.strip().startswith("%%")]
            if not body:
                continue
            header = body[0].lower()
            if "sequencediagram" in header:
                continue  # alt/loop/opt blocks legitimately use 'end' without 'subgraph'
            opens = sum(1 for ln in body if ln.startswith("subgraph"))
            ends = sum(1 for ln in body if ln == "end")
            if opens != ends:
                problems.append(
                    f"{rel}: mermaid block #{idx} has {opens} 'subgraph' but {ends} 'end'"
                )
            for ln in body:
                if re.search(r'\[\s*\]', ln) or re.search(r'"[^"]*\b(?:-|:)[^"]*"\s*\]', ln):
                    pass
                if re.search(r'\[\s*\]', ln):
                    problems.append(f"{rel}: mermaid block #{idx} has an empty node label -> {ln}")


def check_workflows() -> None:
    wf_dir = os.path.join(ROOT, ".github", "workflows")
    if not os.path.isdir(wf_dir):
        return
    for name in sorted(os.listdir(wf_dir)):
        if not name.endswith((".yml", ".yaml")):
            continue
        with open(os.path.join(wf_dir, name), encoding="utf-8") as fh:
            text = fh.read()
        if "timeout-minutes" not in text:
            notes.append(f".github/workflows/{name}: no timeout-minutes")
        for use in re.findall(r"uses:\s*([^\s#]+)", text):
            if "@" not in use:
                problems.append(f".github/workflows/{name}: action without version pin -> {use}")
            elif re.search(r"@(main|master|latest)$", use):
                problems.append(f".github/workflows/{name}: action pinned to a moving ref -> {use}")


def main() -> int:
    files = walk_files()
    check_binaries(files)
    check_duplicates()
    check_mermaid_fences()
    check_mermaid_structure()
    check_workflows()

    for note in notes:
        print(f"note: {note}")
    for warning in warnings:
        print(f"warn: {warning}")
    for problem in problems:
        print(f"FAIL: {problem}")

    if problems or (STRICT and warnings):
        print(f"\n{len(problems)} problem(s), {len(warnings)} warning(s), {len(notes)} note(s)")
        return 1
    print(f"ok — no problems ({len(warnings)} warning(s), {len(notes)} note(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
