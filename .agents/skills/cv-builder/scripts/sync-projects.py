#!/usr/bin/env python3
"""Render `Projects:` in both CV editions from the curated manifest `cv/projects.yaml`,
and report drift against GitHub + `experiment/README.md`.

STATIC vs DYNAMIC
  Static (hand-written, never touched by this script):
      cv/PhamThanhTan-{ENG,VIE}.yaml everything OUTSIDE the `Projects:` block
  Dynamic (generated, do not hand-edit):
      the `Projects:` block in both files, sourced from cv/projects.yaml

The manifest is curated by a human. GitHub and experiment/ are only used to tell you
what is MISSING from it — nothing is ever added to the CV without a manifest entry.

Usage
  python3 .agents/skills/cv-builder/scripts/sync-projects.py            # report drift only
  python3 .agents/skills/cv-builder/scripts/sync-projects.py --apply    # rewrite Projects in both YAMLs
  python3 .agents/skills/cv-builder/scripts/sync-projects.py --scaffold tts-kokoro   # append a stub entry
  python3 .agents/skills/cv-builder/scripts/sync-projects.py --offline  # skip network checks

Exit codes
  0  in sync (or rewritten successfully)
  1  hard error (manifest/YAML unreadable, structural mismatch, --apply failed)
  2  drift found in report mode
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
MANIFEST = os.path.join(ROOT, "cv", "projects.yaml")
CV_FILES = [os.path.join(ROOT, "cv", "PhamThanhTan-ENG.yaml"), os.path.join(ROOT, "cv", "PhamThanhTan-VIE.yaml")]
EXPERIMENT = os.path.join(ROOT, "experiment", "README.md")
GITHUB_USER = "tanpham380"
REPO_ROOT_URL = "https://github.com/tanpham380"

# RenderCV entry field order, as rendered into the YAML.
FIELD_ORDER = ["name", "position", "date", "start_date", "end_date", "location", "summary", "highlights"]

UNSAFE_START = set("-?:,[]{}#&*!|>'\"%@` ")


# --------------------------------------------------------------------------- yaml

def require_yaml():
    """Import PyYAML, re-exec through uv if the system interpreter lacks it."""
    try:
        import yaml  # noqa: F401
    except ImportError:
        if os.environ.get("_SYNC_PROJECTS_REEXEC") == "1":
            sys.exit("error: PyYAML unavailable and uv re-exec already failed")
        uv = shutil_which("uv")
        if not uv:
            sys.exit("error: need PyYAML or `uv` on PATH (pip install pyyaml)")
        env = dict(os.environ, _SYNC_PROJECTS_REEXEC="1")
        os.execvpe(uv, [uv, "run", "--quiet", "--with", "pyyaml", "python", os.path.abspath(__file__), *sys.argv[1:]], env)
    import yaml
    return yaml


def shutil_which(name):
    for d in os.environ.get("PATH", "").split(os.pathsep):
        p = os.path.join(d, name)
        if os.access(p, os.X_OK):
            return p
    return None


def scalar(value: str) -> str:
    """Emit a YAML scalar, quoting only when the plain form would be ambiguous."""
    s = str(value)
    if not s:
        return '""'
    needs = (
        s[0] in UNSAFE_START
        or ": " in s
        or s.endswith(":")
        or " #" in s
        or any(c in s for c in "[]{}")
        or s.lower() in {"true", "false", "null", "yes", "no", "on", "off", "~"}
    )
    if needs:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


# ----------------------------------------------------------------------- manifest

def load_manifest(yaml):
    if not os.path.exists(MANIFEST):
        sys.exit(f"error: manifest not found: {MANIFEST}")
    with open(MANIFEST, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    projects = data.get("projects") or []
    if not projects:
        sys.exit("error: cv/projects.yaml has no `projects:` list")
    seen = set()
    for p in projects:
        pid = p.get("id")
        if not pid:
            sys.exit("error: every project needs an `id`")
        if pid in seen:
            sys.exit(f"error: duplicate project id `{pid}`")
        seen.add(pid)
        for lang in ("en", "vi"):
            block = p.get(lang) or {}
            if not block.get("title"):
                sys.exit(f"error: `{pid}` is missing {lang}.title")
            if not block.get("bullets"):
                sys.exit(f"error: `{pid}` is missing {lang}.bullets")
    return data


def project_url(p):
    if p.get("url"):
        return p["url"]
    if p.get("homepage"):
        return p["homepage"]
    if p.get("repo"):
        return f"{REPO_ROOT_URL}/{p['repo']}"
    return None


def entry_name(p, lang):
    title = p[lang]["title"]
    url = project_url(p)
    return f"[{title}]({url})" if url else title


def render_projects_block(projects, lang, indent="    "):
    """Return the `Projects:` block as YAML text, using the localized section key."""
    key = "Projects" if lang == "en" else "Dự án"
    out = [f"{indent}{key}:"]
    for p in projects:
        entry = {"name": entry_name(p, lang), "highlights": p[lang]["bullets"]}
        for field in ("position", "location", "date", "start_date", "end_date", "summary"):
            # A per-language value wins so localized job titles/locations stay natural.
            value = p[lang].get(field, p.get(field))
            if value is not None:
                entry[field] = value
        first = True
        for field in FIELD_ORDER:
            if field not in entry:
                continue
            lead = f"{indent}  - " if first else f"{indent}    "
            first = False
            if field == "highlights":
                out.append(f"{indent}    highlights:")
                for b in entry[field]:
                    out.append(f"{indent}      - {scalar(b)}")
            else:
                out.append(f"{lead}{field}: {scalar(entry[field])}")
    return "\n".join(out) + "\n"


def replace_projects_block(text, block, lang):
    """Surgically swap the Projects section, leaving every other line untouched."""
    keys = ["Projects"] if lang == "en" else ["Dự án", "Projects"]
    lines = text.splitlines(keepends=True)
    start = None
    for i, line in enumerate(lines):
        if any(line.rstrip("\n") == f"    {k}:" for k in keys):
            start = i
            break
    if start is None:
        sys.exit(f"error: no `    Projects:` section found in the {lang} YAML")
    end = len(lines)
    for j in range(start + 1, len(lines)):
        stripped = lines[j].rstrip("\n")
        if re.match(r"^    \S.*:\s*$", stripped) or re.match(r"^  \S", stripped) or re.match(r"^\S", stripped):
            end = j
            break
    return "".join(lines[:start]) + block + "".join(lines[end:])


# ------------------------------------------------------------------------- github

def gh_json(path):
    """GET an api.github.com path via `gh` (authenticated) with a curl fallback."""
    gh = shutil_which("gh")
    if gh:
        try:
            res = subprocess.run([gh, "api", path], capture_output=True, text=True, timeout=30)
            if res.returncode == 0:
                return json.loads(res.stdout)
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
            pass
    curl = shutil_which("curl")
    if not curl:
        return None
    try:
        headers = ["-H", "Accept: application/vnd.github+json",
                   "-H", f"User-Agent: {GITHUB_USER}-cv-sync"]
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if token:
            headers += ["-H", f"Authorization: Bearer {token}"]
        res = subprocess.run(
            [curl, "-fsSL", *headers, f"https://api.github.com/{path}"],
            capture_output=True, text=True, timeout=30,
        )
        if res.returncode == 0:
            return json.loads(res.stdout)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        pass
    return None


def check_github(manifest, offline):
    """Return (findings, new_repos, unreachable). Findings are (level, message) tuples."""
    findings, unreachable = [], False
    if offline:
        return [("skip", "network checks disabled (--offline)")], [], True

    repos = gh_json(f"users/{GITHUB_USER}/repos?per_page=100&sort=pushed")
    if repos is None:
        return [("skip", "GitHub API unreachable — repo checks skipped")], [], True

    by_name = {r["name"]: r for r in repos}
    managed = set()
    excluded = set(manifest.get("exclude_repos") or [])

    for p in manifest["projects"]:
        repo = p.get("repo")
        if not repo:
            continue
        managed.add(repo)
        info = by_name.get(repo)
        if info is None:
            findings.append(("fail", f"`{p['id']}` points at repo `{repo}`, which is not public on GitHub"))
            continue
        if info.get("archived"):
            findings.append(("warn", f"`{repo}` is archived — CV still claims it as a project"))
        if info.get("fork"):
            findings.append(("warn", f"`{repo}` is a fork — make sure the CV copy says what YOU built"))
        if not info.get("description"):
            findings.append(("note", f"`{repo}` has no GitHub description"))
        if not info.get("homepage") and p.get("homepage"):
            findings.append(("note", f"`{repo}` sets no GitHub homepage (CV links {p['homepage']})"))
        readme = gh_json(f"repos/{GITHUB_USER}/{repo}/readme")
        if readme is None:
            findings.append(("warn", f"`{repo}` has no README — the CV links a repo with nothing to read"))

    new_repos = [r for r in repos if r["name"] not in managed and r["name"] not in excluded]
    for r in new_repos:
        findings.append(("note", f"public repo `{r['name']}` is not in the manifest (not on the CV) — "
                                 f"add it with --scaffold {r['name']} if it deserves a line"))
    for name in sorted(excluded):
        if name not in by_name:
            findings.append(("warn", f"`exclude_repos` lists `{name}`, which is not a public repo any more"))
    return findings, new_repos, unreachable


# --------------------------------------------------------------------- experiment

def check_experiment(manifest):
    """Case-study sections in experiment/ that no CV project points at."""
    if not os.path.exists(EXPERIMENT):
        return [("skip", "experiment/README.md not found")], 0
    with open(EXPERIMENT, encoding="utf-8") as f:
        text = f.read()
    headings = re.findall(r"^#### (\d+\.\d+\..*)$", text, re.M)
    referenced = {p["experiment"] for p in manifest["projects"] if p.get("experiment")}
    findings = []
    for h in headings:
        num, _, title = h.partition(". ")
        if not any(h.startswith(prefix) or prefix in h for prefix in referenced):
            findings.append(("note", f"experiment `{num}. {title}` is not cited by any CV project "
                                     f"(advisory: background reading, not a showcase)"))
    for prefix in sorted(referenced):
        if not any(h.startswith(prefix) or prefix in h for h in headings):
            findings.append(("fail", f"a project claims experiment section `{prefix}`, but no such heading exists"))
    return findings, len(headings)


# ----------------------------------------------------------------------- scaffold

def scaffold(repo, yaml):
    url = f"{REPO_ROOT_URL}/{repo}"
    info = gh_json(f"repos/{GITHUB_USER}/{repo}") or {}
    desc = (info.get("description") or "").strip()
    langs = gh_json(f"repos/{GITHUB_USER}/{repo}/languages") or {}
    top = ", ".join(k for k, _ in sorted(langs.items(), key=lambda kv: -kv[1])[:2]) or "TODO"
    year = (info.get("pushed_at") or "")[:4] or "TODO"
    block = f"""
  - id: {repo.lower()}
    repo: {repo}
    date: {year}
    experiment: null
    en:
      title: TODO short title
      bullets:
        - "TODO what it does, the constraint that made it hard ({top})."
        - "TODO measurable outcome or notable technical decision."
    vi:
      title: TODO tiêu đề ngắn
      bullets:
        - "TODO nó làm gì, ràng buộc nào khiến nó khó ({top})."
        - "TODO kết quả đo được hoặc quyết định kỹ thuật đáng chú ý."
"""
    with open(MANIFEST, encoding="utf-8") as f:
        text = f.read()
    marker = "\n# Repos that exist publicly"
    if marker in text:
        text = text.replace(marker, block + marker, 1)
    else:
        text = text.rstrip("\n") + "\n" + block
    with open(MANIFEST, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"scaffolded `{repo}` into cv/projects.yaml — fill in the TODO lines, then run --apply")
    if desc:
        print(f"  GitHub description: {desc}")


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Sync the CV Projects block from cv/projects.yaml")
    ap.add_argument("--apply", action="store_true", help="rewrite the Projects block in both CV YAMLs")
    ap.add_argument("--scaffold", metavar="REPO", help="append a stub manifest entry for a GitHub repo")
    ap.add_argument("--offline", action="store_true", help="skip GitHub API checks")
    args = ap.parse_args()

    yaml = require_yaml()

    if args.scaffold:
        scaffold(args.scaffold, yaml)
        return 0

    manifest = load_manifest(yaml)
    projects = manifest["projects"]

    # 1. Render + write.
    changed = []
    for path in CV_FILES:
        lang = "vi" if path.endswith("-VIE.yaml") else "en"
        with open(path, encoding="utf-8") as f:
            before = f.read()
        block = render_projects_block(projects, lang)
        after = replace_projects_block(before, block, lang)
        if after != before:
            changed.append((path, lang, after))

    if args.apply:
        for path, _lang, after in changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(after)
            print(f"wrote {os.path.relpath(path, ROOT)}")
        if not changed:
            print("both CV YAMLs already match cv/projects.yaml")
        return 0

    # 2. Report.
    hard = 0
    if changed:
        print("drift: the CV Projects block does not match cv/projects.yaml")
        for path, lang, _ in changed:
            print(f"  - {os.path.relpath(path, ROOT)} ({lang}) needs regenerating  →  run with --apply")
    else:
        print(f"ok: {len(projects)} projects in sync across both CV editions")

    findings, _new, _unreachable = check_github(manifest, args.offline)
    exp_findings, n_sections = check_experiment(manifest)

    hard += sum(1 for level, _ in findings + exp_findings if level == "fail")
    for level, msg in findings + exp_findings:
        print(f"{level.upper():5} {msg}")
    if not args.offline and n_sections:
        print(f"NOTE  {n_sections} case studies scanned in experiment/README.md")

    return 1 if hard else (2 if changed else 0)


if __name__ == "__main__":
    sys.exit(main())
