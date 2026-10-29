# Project Guidelines

This repository is a **personal engineering portfolio / blog**: a GitHub profile README, a capstone
case study, an experiment lab, a static pixel-art page, and the published CV.

Primary audience: recruiters and hiring managers for **DevOps / Virtualization / Platform** roles.
Everything written here must be accurate, reproducible, and traceable to real work.

## Repository map

| Path | What it is | Rule |
| --- | --- | --- |
| `README.md` | GitHub profile README (public face) | Keep structure: header → About → Skills Matrix → Featured Projects → Analytics → Connect |
| `SDN/` | Capstone: SDN on Kubernetes (EVE-NG, HAProxy, Keepalived, NetworkPolicy) | Evidence lives here; `SDN/README.md` is the index |
| `experiment/` | Long-form real-world case studies | One `###` section per case, see `case-study` skill |
| `pixel-html/` | Self-contained static page, served by GitHub Pages from `main` | Single file, no build step, no external JS deps |
| `cv/` | RenderCV YAML sources, the `projects.yaml` manifest, generated PDFs | **Never hand-edit the PDFs**; the `Projects:` block is generated, everything else is manual |
| `src/` | Images/badges used by the README | Reference via `raw.githubusercontent.com` |
| `.agents/` | Agent rules + skills (VS Code + Antigravity) | See `.agents/README.md` |

## Commands

```bash
# CV (requires uv, auto-provisions Python 3.12 + rendercv)
.agents/skills/cv-builder/scripts/build-cv.sh          # build both PDFs into cv/

# CV projects: curated manifest -> both YAMLs (report first, then apply)
python3 .agents/skills/cv-builder/scripts/sync-projects.py         # drift report, exit 2 if out of sync
python3 .agents/skills/cv-builder/scripts/sync-projects.py --apply # rewrite Projects in EN + VI

# Repo hygiene / link + consistency checks (stdlib only)
python3 .agents/skills/repo-hygiene/scripts/repo-audit.py
python3 .agents/skills/profile-sync/scripts/check-profile-sync.py

# Mermaid sanity (no install): paste into https://mermaid.live; CI checks fences only
```

## Conventions

- **Language**: README and CV exist in EN + VI. Blog posts default to Vietnamese; case studies and
  diagrams use English technical terms. Do not translate technology names or CLI output.
- **Diagrams**: Mermaid only, `graph TD` / `sequenceDiagram`, with `classDef` colors and numbered
  edge labels (`-->|1. SIP Invite|`). No screenshots where a diagram is possible.
- **Claims**: every metric or achievement must be verifiable from this repo or an external link.
- **Static vs generated**: the CV keeps hand-written facts; only `Projects:` is generated from
  `cv/projects.yaml`. Public repos and `experiment/` case studies *suggest* CV updates — they never
  add themselves. Never invent a project, a bullet, or a number to fill a gap.
  Never invent numbers, employers, dates, or certifications.
- **Versioning artifacts**: large binary evidence (reports, videos, slides) is referenced, not
  bloated. Before adding a new binary over 2 MB, ask whether it belongs in this repo.
- **Commit style**: Conventional Commits (`docs:`, `fix:`, `chore:`, `feat:`), subject ≤ 72 chars.

## Skills available in `.agents/skills/`

`blog-post`, `case-study`, `cv-builder`, `mermaid-architecture`, `profile-sync`, `repo-hygiene`.

When a task matches a skill description, load and follow that skill instead of improvising.
