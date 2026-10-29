---
name: blog-post
description: 'Use when turning raw notes, a lab, or a debugging session into a blog post or article for this portfolio. Drafts in the author voice (Vietnamese for the body, English for technical terms), with a Mermaid diagram, a config/code block, and a takeaway. Keywords: blog, article, write post, draft, viết bài, chia sẻ kinh nghiệm, tutorial.'
---

# Blog post from raw experience

Turns a scrap of real experience into a publishable post that matches this repo's voice.
The author is a **DevOps & Virtualization Engineer** — posts read as field notes, not marketing.

## Voice contract

- **Body language**: Vietnamese by default. Technical nouns stay English (`Keepalived`,
  `NetworkPolicy`, `control plane`). CLI output is never translated.
- **Person**: first person singular for decisions ("tôi chọn HAProxy vì…"), "chúng tôi" only when
  the work was genuinely a team effort (e.g. the 5-person capstone).
- **Shape**: problem → what I tried → what broke → what I shipped → what it cost → takeaway.
- **No** "in today's fast-paced world", "delve", "leverage", "game-changer". No emoji headings.
- Every claim: a tool, a number, or a link. If a number is missing, ask for it — do not estimate.

## Interview first (only what's missing)

Ask at most 4 of these, then start writing:

1. What was the trigger — an incident, a ticket, a design review?
2. What was the failure mode or constraint (mtu, iptables, DNS, storage IOPS, budget)?
3. What did you measure before/after (latency, downtime, MTTR, node count, cost)?
4. Any code/config you can share as the concrete example?

## Procedure

1. Read `AGENTS.md` and skim 2 existing sections of `experiment/README.md` for tone.
2. Pick the format:
   - **Incident note** — timeline, symptom, root cause, fix, prevention.
   - **Build log** — goal, constraints, architecture, step-by-step, result.
   - **Comparison** — 2–3 tools, a decision table, a "when to pick which" rule.
3. Draft with this skeleton:

```markdown
# <Outcome-oriented title, ≤ 60 chars>

> TL;DR: <one sentence a busy reader can act on>

## Bối cảnh
<system, scale, constraint — 3–5 lines>

## Vấn đề
<symptom + evidence: log line, error, metric>

## Cách tôi xử lý
1. <step with command>
2. <step>

```bash
# the one command that matters
```

## Kiến trúc sau khi sửa
<mermaid — see mermaid-architecture skill>

## Kết quả
| Metric | Trước | Sau |
| --- | --- | --- |
| ... | ... | ... |

## Bài học
- <3 bullets max, each actionable>

## Tham khảo
- [<title>](<url>)
```

4. Verify with the `mermaid-architecture` skill before saving; broken diagrams are the #1 defect.
5. Save to `experiment/README.md` (append) unless the user names another path. Do not create new
   top-level folders.
6. Report: title, word count, path, and the Mermaid blocks used.

## Anti-patterns

- Rewriting a paragraph to sound "senior" while dropping the numbers.
- Copying upstream docs. Reference the doc, then show what *your* environment did differently.
- Posting a runbook with employer-internal IPs, hostnames, or customer names — redact to RFC1918
  placeholders and say so in a footnote.
