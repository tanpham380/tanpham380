#!/usr/bin/env python3
"""Extract and validate every ```mermaid block in the given Markdown files.

Offline structural checks always run. Pass --remote to also ask mermaid.ink whether the
diagram actually parses (needs network).

Usage:
  python3 .agents/skills/mermaid-architecture/scripts/validate-mermaid.py experiment/README.md
  python3 .agents/skills/mermaid-architecture/scripts/validate-mermaid.py --remote README.md

Exit code 1 when any block fails.
"""
from __future__ import annotations

import base64
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BLOCK_RE = re.compile(r"```mermaid\n(.*?)```", re.S | re.M)
KNOWN_HEADS = (
    "graph ", "flowchart ", "sequencediagram", "classdiagram",
    "erdiagram", "statediagram", "journey", "gantt", "pie", "gitgraph",
)


def structural(body: str, label: str) -> list[str]:
    problems = []
    lines = [ln.strip() for ln in body.splitlines() if ln.strip() and not ln.strip().startswith("%%")]
    if not lines:
        return [f"{label}: empty block"]
    head = lines[0].lower()
    if not head.startswith(KNOWN_HEADS):
        problems.append(f"{label}: unknown diagram type -> {lines[0]}")
        return problems

    if head.startswith(("graph", "flowchart")):
        opens = sum(1 for ln in lines if ln.startswith("subgraph"))
        ends = sum(1 for ln in lines if ln == "end")
        if opens != ends:
            problems.append(f"{label}: {opens} 'subgraph' vs {ends} 'end'")
        for ln in lines[1:]:
            if re.search(r"\[\s*\]", ln):
                problems.append(f"{label}: empty node label -> {ln}")
            if "-->" in ln and "|" in ln:
                label_part = ln.split("|", 1)[1].split("|", 1)[0]
                if not label_part.strip():
                    problems.append(f"{label}: empty edge label -> {ln}")
    if head.startswith("sequencediagram"):
        for ln in lines[1:]:
            if ln.startswith("participant") and " as " not in ln and ":" in ln:
                problems.append(f"{label}: participant alias should use 'as' -> {ln}")
    return problems


def remote(body: str) -> tuple[bool, str]:
    b64 = base64.urlsafe_b64encode(body.encode("utf-8")).decode()
    url = "https://mermaid.ink/svg/" + urllib.parse.quote(b64)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "mermaid-validate"})
        with urllib.request.urlopen(req, timeout=40) as res:
            return res.status == 200 and b"<svg" in res.read(400), ""
    except Exception as exc:  # noqa: BLE001 - report whatever the network said
        return False, str(exc)[:160]


def main(argv: list[str]) -> int:
    args = [a for a in argv if a != "--remote"]
    use_remote = "--remote" in argv
    if not args:
        print(__doc__)
        return 2

    failures = 0
    checked = 0
    for rel in args:
        path = rel if os.path.isabs(rel) else os.path.join(ROOT, rel)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        for idx, body in enumerate(BLOCK_RE.findall(text), 1):
            checked += 1
            label = f"{rel}#{idx}"
            problems = structural(body, label)
            if use_remote and not problems:
                ok, err = remote(body)
                if not ok:
                    problems.append(f"{label}: remote render failed ({err})")
            if problems:
                failures += len(problems)
                for problem in problems:
                    print(f"FAIL: {problem}")
            else:
                print(f"ok:   {label}")

    print(f"\n{checked} block(s), {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
