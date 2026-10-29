# `.agents/` — Portable agent setup

One folder that both **GitHub Copilot in VS Code** and **Google Antigravity** (App / CLI / IDE
extension) read, plus any tool that follows the open `AGENTS.md` + `SKILL.md` standards
(Codex, Claude Code via `AGENTS.md`, Gemini CLI, Cursor, …).

```
.
├── AGENTS.md                  # root: always-on project instructions (also read by Antigravity)
└── .agents/
    ├── README.md              # this file
    ├── rules/                 # Antigravity modular rules (frontmatter + trigger)
    ├── skills/                # SKILL.md bundles — read by BOTH tools
    │   ├── blog-post/
    │   ├── case-study/
    │   ├── cv-builder/
    │   ├── mermaid-architecture/
    │   ├── profile-sync/
    │   └── repo-hygiene/
    └── skills/*/scripts/      # runnable helpers (kept dependency-free)
```

## What each surface reads

| Surface | Instructions | Skills | Notes |
| --- | --- | --- | --- |
| Copilot in VS Code | root `AGENTS.md` | `.agents/skills/<name>/SKILL.md` | Do **not** also add `.github/copilot-instructions.md` — duplicated guidance drifts |
| Antigravity (App/CLI/IDE) | root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/rules/*.md` | `.agents/skills/<name>/SKILL.md` | `.agents/rules/*.md` requires `trigger:` frontmatter |
| Codex / other `AGENTS.md` agents | root `AGENTS.md` | — | Skills are opt-in per tool |

Antigravity global (all projects) counterpart: `~/.gemini/config/skills/` and
`~/.gemini/config/rules/`. The workspace copies here are the source of truth; symlink them if you
want them global:

```bash
ln -s "$PWD/.agents/skills" ~/.gemini/config/skills    # only if you want them in every project
```

## Rules vs skills — how to choose

- **Rule** (`.agents/rules/`): a short, non-negotiable constraint ("never hand-edit CV PDFs").
  Antigravity-only, loaded automatically via `trigger`. Keep each file well under 24 KB.
- **Skill** (`.agents/skills/`): a repeatable *workflow* with steps, checklists and scripts, loaded
  on demand by both tools.

Trigger values used here:

| `trigger` | When it loads | Used for |
| --- | --- | --- |
| `model_decision` | agent sees only the `description`, reads the body when relevant | most rules |
| `glob` | file pattern matches | `*.yaml`/`cv/**` rules |
| `always_on` | every turn | avoid — eats the 20 000-token rules budget |
| `manual` | only when `@`-mentioned | release checklists |

## Static vs generated CV content

The CV keeps its hand-written facts (work experience, education, certifications) in
`cv/PhamThanhTan-{ENG,VIE}.yaml`. Only the `Projects:` block is generated, from the curated
manifest `cv/projects.yaml`, so one edit updates both editions:

```bash
python3 .agents/skills/cv-builder/scripts/sync-projects.py          # drift report
python3 .agents/skills/cv-builder/scripts/sync-projects.py --apply  # write both YAMLs
```

`experiment/` and the public GitHub repos are **evidence, not input**: the drift report suggests a
project the manifest is missing, and the author decides. Nothing lands on the CV uncurated — a CV is
an argument, not a dashboard.

## Verified awesome skill sources

Install a skill by copying its folder — keep the folder name equal to the `name:` field.

| Source | What to take from it | Why it matters here |
| --- | --- | --- |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) (`skills/`, `agents/`) | `make-blog-post`, `create-readme`, `draw-io-diagram-generator`, `documentation-writer`, `markdown-to-word-mermaid`, `convert-pdf-to-md`, `security-review`, `github-actions-hardening` | Directly reusable for blog writing, diagram export, PDF/DOCX conversion, CI hardening |
| [anthropics/skills](https://github.com/anthropics/skills) | `doc-coauthoring`, `docx`, `pdf`, `pptx`, `skill-creator`, `frontend-design`, `webapp-testing` | `pdf`/`docx` for CV export, `skill-creator` for authoring new skills |
| [skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills) | index of cross-tool skills | Discovery only |
| [JackyST0/awesome-agent-skills](https://github.com/JackyST0/awesome-agent-skills) | curated list incl. Copilot/Cursor/Claude | Discovery only |
| [rendercv/rendercv](https://github.com/rendercv/rendercv) | CV YAML schema + 9 themes | Powers `cv-builder` |
| [agents.md](https://agents.md/) | `AGENTS.md` spec + sample | Keeps root instructions portable |
| [agentskills.io](https://agentskills.io/home) | `SKILL.md` open standard | Keeps skills portable |

Copy-in command (review the skill before trusting it — skills execute instructions and scripts):

```bash
git clone --depth 1 https://github.com/github/awesome-copilot /tmp/awesome-copilot
cp -R /tmp/awesome-copilot/skills/make-blog-post .agents/skills/   # rename if a local skill exists
```

## Adding your own skill

```bash
mkdir -p .agents/skills/my-skill/{scripts,references,assets}
```

`.agents/skills/my-skill/SKILL.md`:

```markdown
---
name: my-skill
description: 'Use when <trigger phrase>, to <outcome>. Keywords: <words the agent sees>.'
---

# My Skill

## When to use
- …

## Procedure
1. …
2. Run [script](./scripts/do-thing.sh) and paste the output.
```

Rules: name matches folder, description is keyword-rich (it is the only discovery surface), keep
`SKILL.md` under ~500 lines, put detail in `references/`.

## Guardrails

- Skills and rules never get commit rights, secrets, or network calls to unknown hosts.
- Anything in `.agents/skills/*/scripts/` must be readable in one screen and safe to re-run.
- Regenerate, don't hand-patch, generated artifacts (CV PDFs, snake SVG).
