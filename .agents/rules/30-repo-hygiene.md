---
trigger: model_decision
description: "Apply when adding, moving, or deleting files — especially binaries under SDN/, cv/, src/, or any GitHub Actions workflow change."
---

# Repository hygiene

## Where files go

| Kind | Location | Limit |
| --- | --- | --- |
| Screenshot / diagram export | `SDN/Image/`, `src/` | ≤ 500 KB each |
| Long-lived binary evidence (report, slide, video) | `SDN/Report/`, `SDN/Slide/`, `SDN/video/` | **ask first** if > 5 MB |
| New case study prose | `experiment/README.md` (append a `###` section) | — |
| New demo code | `SDN/DevCode/<topic>/` | runnable, with a short README |
| Generated output (CV PDF, snake SVG) | `cv/`, `output` branch | never hand-edited |

## Never commit

- `tapviet-studio/` (already ignored), `.DS_Store`, `node_modules/`, `rendercv_output/`,
  `*.aux`, `*.log`, credentials, `.env`, real internal hostnames/IPs of employers.
- A second copy of the same PDF (`*_ver1..ver5` style). Keep one canonical artifact per topic and
  let git history hold the old ones.

## Workflows

- Existing: `.github/workflows/main.yml` generates the contribution snake into the `output` branch.
  It needs `permissions: contents: write` — keep that scoped to the job.
- Any new workflow must: pin action versions by major tag, set `timeout-minutes`, and avoid
  `pull_request_target` with secrets. Run `repo-hygiene` skill's audit script afterwards.

## Before finishing any change

```bash
python3 .agents/skills/repo-hygiene/scripts/repo-audit.py
```

It reports untracked large files, tracked binaries, broken relative links, and Mermaid fences
without a language tag.
