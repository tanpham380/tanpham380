---
name: profile-sync
description: 'Use when the README, the CV, or the case studies might disagree — after adding a project, a certification, a skill, or a new job. Runs a consistency check across README.md, cv/*.yaml, SDN/ and experiment/. Keywords: sync, consistency, update profile, update readme, update cv, skills matrix, keep in sync, đồng bộ hồ sơ.'
---

# Keep README ↔ CV ↔ case studies in sync

A portfolio loses credibility the moment the CV says one thing and the README says another.
This skill finds and fixes the drift.

## Run the checker

```bash
python3 .agents/skills/profile-sync/scripts/check-profile-sync.py
```

It reports, as `FAIL:` (exit 1) or `note:`:

| Check | Meaning |
| --- | --- |
| matrix vs CV | a technology in the README Skills Matrix that no CV edition mentions |
| case-study numbering | `### <n>.` headings in `experiment/README.md` are not contiguous |
| relative links | a relative markdown link in any tracked `.md` file does not resolve |
| CV parity | section counts differ, or a fixed fact (`8.4/10`, `7.38/10`, a date) is missing from one edition |
| projects manifest | a project title declared in `cv/projects.yaml` is absent from one CV edition |

`note:` items are judgement calls: a hobby stack (Flutter, Django) may legitimately live in the
README matrix without being on the CV.

## The three sources of truth

| Fact | Canonical location | Mirrors |
| --- | --- | --- |
| Job title, employer, dates | `cv/*.yaml` `Work Experience` | `README.md` About, CV link badges |
| Skills matrix | `README.md` `## Skills Matrix` | CV `Core Competencies` |
| Capstone (6-node HA k8s, 8.4/10, HAProxy + Keepalived) | `SDN/README.md` | CV `Projects`, `README.md` Featured Projects |
| Project bullets on the CV | `cv/projects.yaml` (generated into `Projects:`) | `README.md` Featured Projects |
| Deep case studies | `experiment/README.md` | not mirrored — linked only |
| Certifications | `cv/*.yaml` `Certifications` | not listed in README by design |

## Curated vs discovered content

Two different questions, two different tools:

| Question | Tool | Behaviour |
| --- | --- | --- |
| "Do the README, the CV and the case studies agree?" | `check-profile-sync.py` | fails the build on a hard mismatch |
| "Has the outside world moved on?" | `sync-projects.py` | report only, never writes the CV |

`sync-projects.py` compares `cv/projects.yaml` against the public GitHub API and
`experiment/README.md` and reports:

- a manifest project whose repo is gone, archived, or a fork,
- a manifest project whose repo has no README (the CV links a repo with nothing to read),
- a **public repo that is not in the manifest** — a suggestion, never an automatic addition,
- an `experiment/` case study that no CV project cites (advisory: background reading),
- a project citing an `experiment/` heading that no longer exists (FAIL).

Repos under `exclude_repos` are filtered out, so forks and scratch mirrors never nag.

## Procedure

1. Run the checker. Note every `FAIL`.
2. For each failure pick the direction to fix:
   - **New project** → add it to `cv/projects.yaml` (EN + VI in the same entry), run
     `sync-projects.py --apply`, add it to `README.md` Featured Projects, and append a case study in
     `experiment/`. Never hand-edit the `Projects:` block in the YAMLs.
   - **New certification** → CV only, both languages.
   - **New skill** → `README.md` matrix; add to CV `Core Competencies` only if it is real work
     experience, not a curiosity.
   - **New job** → CV `Work Experience` (both), `README.md` About bullets, then re-render.
3. Re-run the checker until exit code is 0.
4. Rebuild the CVs (`.agents/skills/cv-builder/scripts/build-cv.sh`) if any YAML changed.
5. Optionally run `sync-projects.py` (no flag) to see whether GitHub or `experiment/` has drifted
   ahead of the curated manifest.
6. Report a short table: what changed, in which files, and the checker output.

## Never

- Never copy CV prose into the README. The README links the PDF badges; the prose stays in YAML.
- Never let one CV language carry a bullet the other lacks — mirror in the same commit.
- Never "fix" a checker `note:` by deleting a skill from the README if the user actually has it.
