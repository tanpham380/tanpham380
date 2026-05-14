# Experiment Lab

This folder stores real-world use cases, practical PoCs, and architecture experiments.

## Suggested Structure

- network/: L2/L3, VLAN, routing, loop prevention, policy tests
- kubernetes/: NetworkPolicy, HA setup, service exposure, failure simulation
- automation/: Python scripts, tooling helpers, generated manifests
- security/: firewall rules, segmentation patterns, validation outputs

## Use Case Template

Create one folder per use case with this structure:

- use-case-name/
  - README.md
  - diagrams/
  - manifests/
  - scripts/
  - results/

## Recommended README.md for each use case

```markdown
# Use Case: <name>

## Goal
What problem this case solves.

## Context
Environment, constraints, assumptions.

## Architecture
Diagram(s), flow, components.

## Implementation
Steps, manifests, scripts, commands.

## Validation
How to test, expected result, actual output.

## Lessons Learned
What worked, what failed, and next improvement.
```

## Current Content

- network/vlan-leaking-loop-layer2.mmd
