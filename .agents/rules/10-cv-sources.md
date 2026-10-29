---
trigger: glob
globs: "cv/**/*.yaml, cv/**/*.yml, **/PhamThanhTan*.yaml"
description: "Rules for the RenderCV CV sources and their generated PDFs."
---

# CV rules

- **Single source of truth**: `cv/*.yaml` (RenderCV schema v2.x). PDFs in `cv/` are build output.
- **`Projects:` is generated**, everything else is hand-written. The block is rendered from
  `cv/projects.yaml` by `sync-projects.py`; editing it directly in the YAML will be overwritten.
- **Nothing is auto-added to the CV.** A new public repo or a new `experiment/` case study only
  produces a *suggestion* in the drift report. The author decides, edits `cv/projects.yaml`, and
  re-syncs. Never append a project the author did not curate.
- Never hand-edit `cv/*.pdf`. Never paste CV text into the README by hand — link the PDF.
- Content must stay consistent with `README.md` Skills Matrix, `SDN/README.md`, and
  `experiment/` case studies. When a new project ships, add it to both.
- Keep the EN and VI YAML files structurally identical (same sections, same order, same dates).
  Only prose and labels differ.
- Facts are fixed unless the user corrects them: current title *DevOps & Virtualization Engineer*,
  employer *Huong Nghiep A Au*, capstone score *8.4/10*, GPA *7.38/10*, FPT University.
- Dates use `YYYY-MM` and `present` (never `now`, never `HIỆN TẠI` inside a `date` field).
- **Photo**: `cv/photo.jpg` must be a real photograph of the author, supplied by the author.
  Never pull `avatar_url` from the GitHub API, never generate one, never use a placeholder portrait —
  a CV photo is an identity claim. If no real photo exists, leave `photo:` empty (the current state).
- Build with the skill script, which pins Python 3.12 + rendercv 2.8+ via `uv`:
  `.agents/skills/cv-builder/scripts/build-cv.sh`
- A CV change is not done until both PDFs regenerate **and** the page count has been checked
  (target: each edition ≤ 2 pages).
