---
name: repo-hygiene
description: 'Use before committing when files were added, moved, or deleted, when a binary or build artifact is involved, or when a GitHub Actions workflow changes. Audits large binaries, duplicate artifacts, broken Mermaid fences, and unpinned CI actions. Keywords: repo hygiene, cleanup, large file, binary, gitignore, workflow, actions, lint, dọn dẹp repo.'
---

# Repository hygiene

This repo mixes prose, diagrams, and heavy evidence (PDF reports, MP4 demos, PPTX). Without
discipline it bloats. It is currently **~91 MB of tracked binaries** — keep it from growing.

## Run the audit

```bash
python3 .agents/skills/repo-hygiene/scripts/repo-audit.py            # report only
python3 .agents/skills/repo-hygiene/scripts/repo-audit.py --strict   # treat warnings as failures
```

Output levels:

| Level | Meaning | Action |
| --- | --- | --- |
| `FAIL` | blocking: unpinned action, missing `mermaid` fence tag | fix before commit |
| `warn` | a tracked binary > 5 MB | justify or move it out |
| `note` | duplicate artifacts, big total payload, no `timeout-minutes` | judgement call |

## Policy

| Artifact | Destination | Hard limit |
| --- | --- | --- |
| Screenshot, exported diagram | `SDN/Image/` or `src/` | 500 KB — compress first |
| Report PDF (canonical only) | `SDN/Report/` | 8 MB, one version |
| Demo video | external host, link from `SDN/README.md` | do not add new ones to git |
| Slides | `SDN/Slide/` only if referenced | 10 MB |
| Generated output (CV PDF, snake SVG) | `cv/`, `output` branch | regenerated, never hand-edited |

## Procedure

1. `git status --short` — list what you touched.
2. Run the audit. Read `FAIL` first.
3. Fix in this order:
   - **Mermaid fence without `mermaid`** → add the language tag.
   - **Unpinned action** → `uses: owner/action@v4` (major tag) and keep `permissions` minimal.
   - **Binary > 5 MB** → prefer a link over a copy. If it must stay, say why in the commit body.
   - **Duplicate `_ver1..ver5`** → keep the highest version as the canonical name and delete the
     rest; git history retains them.
4. Confirm `.gitignore` covers build output:
   ```gitignore
   rendercv_output/
   .DS_Store
   node_modules/
   ```
5. Re-run the audit until only justified `note:` lines remain.
6. Report what changed and the remaining warnings verbatim.

## Do not

- Do not `git rm --cached` a needed artifact just to make the audit green.
- Do not rewrite history to shrink the repo unless the user explicitly asks — it breaks the
  `output` branch and every external link into `raw.githubusercontent.com`.
- Do not add a `.gitattributes` LFS rule without asking; GitHub Pages does not serve LFS files.
