---
trigger: glob
globs: "**/*.md, **/*.mmd, .github/workflows/*.yml"
description: "Markdown and Mermaid authoring conventions for README, blog, and case studies."
---

# Markdown / Mermaid conventions

## Markdown

- One H1 per file. Case-study sections inside `experiment/README.md` use `###`.
- Code fences always carry a language (`bash`, `yaml`, `python`, `mermaid`, `text`).
- Links to repo files are relative (`./SDN/README.md`); links to images in `src/` use
  `https://raw.githubusercontent.com/tanpham380/tanpham380/main/src/<file>` so they render on npm,
  PyPI, and GitHub alike.
- Tables over bullet lists when comparing ≥ 3 items with ≥ 2 attributes.
- No trailing double-space line breaks inside `<p align="center">` blocks.

## Mermaid

- Flow direction: `graph TD` for topology/architecture, `sequenceDiagram` for protocols.
- Always define `classDef` and apply with `:::name`; group with `subgraph`.
- Label every directional edge that carries a protocol, port, or step: `-->|1. SIP Invite|`.
- Quote node labels containing `/`, `:`, `(`, `)`, or `-` → `Node["Core Switch - VLAN 10"]`.
- Never use HTML tags inside node labels; use `<br/>` only if unavoidable.
- Keep under ~40 nodes per diagram; split into layers (physical / logical / flow) instead.
- Validate locally before committing: `npx -y @mermaid-js/mermaid-cli -i <file>.mmd -o /tmp/out.svg`
  or paste into <https://mermaid.live>.
- Do **not** add ER/class diagrams to the profile README — they belong in blog posts.

Diagram recipes and a working skeleton: [mermaid-architecture skill](../skills/mermaid-architecture/SKILL.md).
