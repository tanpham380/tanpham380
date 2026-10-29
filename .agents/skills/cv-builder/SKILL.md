---
name: cv-builder
description: 'Use when building, editing, or reviewing the CV in cv/. Converts RenderCV YAML sources into the EN and VI PDFs, checks page count, and keeps CV content consistent with the README. Keywords: CV, resume, curriculum vitae, rendercv, build cv, update cv, export pdf, sơ yếu lý lịch, hồ sơ.'
---

# CV builder (RenderCV)

The CV is generated, not typed. `cv/PhamThanhTan-ENG.yaml` and `cv/PhamThanhTan-VIE.yaml` are the
sources; `cv/PhamThanhTan-*.pdf` are build artifacts that the README links to.

## Static vs generated (read this before editing)

| Part of the CV | Owner | How it changes |
|---|---|---|
| Everything outside `Projects:` | **hand-written** in both YAMLs | edit directly |
| The `Projects:` / `Dự án:` block | **generated** from `cv/projects.yaml` | edit the manifest, then re-sync |

Adding a project therefore happens **once**, in the manifest, for both languages at the same time:

```bash
python3 .agents/skills/cv-builder/scripts/sync-projects.py                 # report drift (exit 2 if out of sync)
python3 .agents/skills/cv-builder/scripts/sync-projects.py --apply         # rewrite Projects in both YAMLs
python3 .agents/skills/cv-builder/scripts/sync-projects.py --scaffold tts-kokoro  # stub entry to fill in
```

The manifest is **curated by a human**. GitHub and `experiment/` are only used to *report* what is
missing — no repo is ever added to the CV automatically, and no bullet is ever generated. A public
repo that is not in the manifest is a suggestion, not an instruction. Repos listed under
`exclude_repos` (forks, scratch, mirrors) are never surfaced.

Manifest fields: `id`, `repo` (or `null`), `url`/`homepage`, `date` or `start_date`+`end_date`,
`position`, `location`, `experiment` (a `####` heading prefix in `experiment/README.md`), and the
required `en`/`vi` blocks with `title` + `bullets[]` (+ optional `summary`). A per-language
`location`/`position`/`summary` overrides the top-level value, so EN can say *FPT University* while
VI says *Đại học FPT*.

Never hand-edit the `Projects:` block: the next `--apply` will overwrite it.

## Facts you may rely on (do not invent others)

- Name: Pham Thanh Tan / Phạm Thanh Tân · born 26/06/2001 · Thu Duc, HCMC
- Title: DevOps & Virtualization Engineer
- Employer: Huong Nghiep A Au — System Engineer, 12/2022–present; Network Engineer intern 08/2022–12/2022
- FPT University, Information Assurance, 2019–2023, GPA 7.38/10
- FPT IT Helpdesk 03/2020–07/2022
- Capstone: SDN on Kubernetes, Technical Leader of 5, score 8.4/10
- Certifications: DevOpsEdu (03/2023), CCNA 200-301 via VN Pro (03/2022), CertNexus CEET (03/2022),
  CyberOps Associate (11/2021), CCNAv7 ITN (07/2021)

## Procedure

1. **Read before writing.** Open both YAML files and `README.md` Skills Matrix. Keep the three in
   sync — a technology listed in the README must appear in the CV if it belongs to real experience.
2. **Edit content only in `cv`:** `name`, `headline`, `location`, `email`, `phone`, `website`,
   `social_networks`, and `sections`. Each section is a list of typed entries:
   - percentage/single-line entries: `- text`
   - labeled entries: `- label: … \n details: …`
   - experience entries: `company, position, start_date, end_date, location, highlights[]`
   - education: `institution, area, degree, start_date, end_date, location, highlights[]`
3. **Dates**: `YYYY-MM`, `YYYY`, or `present`. Never prose.
4. **Numbers over adjectives.** Each bullet should say what changed (count, %, time saved, score).
   If the user did not supply a number, leave the bullet factual instead of guessing.
5. **Mirror the two languages.** Add a bullet to ENG → add the equivalent to VIE in the same commit.
6. **Render**:
   ```bash
   .agents/skills/cv-builder/scripts/build-cv.sh        # both
   .agents/skills/cv-builder/scripts/build-cv.sh ENG    # one
   ```
7. **Verify**: the script prints page count. Target ≤ 2 pages each. Above that, cut the oldest
   bullets (Activities/Interests first), not the metrics.
8. **Report** the diff summary, page counts, and any bullet you had to shorten to fit.

## Photo

The CV is photo-ready but ships **without** a photo, because a portrait is an identity claim.

- To enable, the author must provide a real photograph at `cv/photo.jpg`:
  - head-and-shoulders, plain background, square-ish crop (≥ 400×400 px, ~2:2),
  - compressed JPEG under 300 KB.
- Then, in both YAML files, set `cv.photo: photo.jpg` and switch the header to
  `alignment: left` with `photo_width: 2.8cm`, `photo_position: left`.
- After enabling, rebuild and confirm the CV is still ≤ 2 pages (a photo pushes content down).
- **Never** substitute the GitHub avatar, an AI-generated portrait, a stock photo, or an emoji.
  If the user has no real photo, keep `photo:` empty — ATS-oriented CVs are fine without one.

## Theme and layout

- `theme: engineeringresumes` — ATS-friendly, single column, no photo. Keep it.
- Margins 0.6in, body 9.5pt. Adjust margins before shrinking the font below 9pt.
- Other valid themes if the user asks: `classic`, `sb2nov`, `harvard`, `moderncv`, `opal`, `ink`,
  `ember`. Changing the theme is a visual decision — show the result before committing.

## Do not

- Do not edit the PDFs, do not commit `rendercv_output/` (the script removes it).
- Do not add a stock/AI/pulled avatar photo (see Photo above), a "references available on request"
  line, or a skill rating bar (e.g. "80%").
- Do not add a certification you cannot link or date.
- Do not translate technology names into Vietnamese.
