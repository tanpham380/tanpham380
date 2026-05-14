# MPLS Network Technical Guide

## 1. Purpose

This document defines technical standards and implementation guidance for MPLS-based branch connectivity in enterprise environments.

## 2. Scope

- WAN/MPLS connectivity between HQ and branch offices
- L2/L3 segmentation model and VLAN planning
- Routing policy and failover behavior
- Security controls at edge and core layers
- Operations runbook and troubleshooting workflow

## 3. Reference Architecture

## 3.1 Logical Topology

- HQ core network connected to MPLS provider edge (PE)
- Branch CE routers connected to MPLS cloud
- Segmented VLANs for server, user, management, and voice zones
- Firewall inspection at branch and/or HQ egress

## 3.2 Typical Traffic Flows

- Branch user VLAN to HQ application VLAN
- Branch services to centralized identity/DNS/NTP
- Internet-bound traffic policy (local breakout or HQ breakout)

## 4. Technical Baseline

## 4.1 IP and VLAN Plan

- Define per-site subnet blocks
- Define VLAN IDs and naming convention
- Reserve management and transit subnets

## 4.2 Routing Standards

- Dynamic routing protocol policy (OSPF/BGP as applicable)
- Route summarization boundaries
- Prefix filtering and route control policy
- Default route strategy (single-homed/dual-homed)

## 4.3 High Availability and Redundancy

- Dual CE uplinks where possible
- Redundant firewall paths and state sync policy
- Link monitoring and failover timers

## 4.4 Security Standards

- Access control by zone and least privilege model
- Management plane hardening (SSH, AAA, logging)
- Segmentation for sensitive systems
- Change approval for ACL/routing policy updates

## 5. Implementation Guide

## 5.1 Pre-checklist

- Approved HLD/LLD and IP plan
- Device inventory and firmware baseline
- Circuit handoff details from MPLS provider
- Backout plan and maintenance window

## 5.2 Build Steps

1. Configure CE interfaces and transit links.
2. Configure VLAN interfaces and gateway policies.
3. Apply routing protocol and route filters.
4. Apply ACL/firewall policy and test segmentation.
5. Validate site-to-site reachability and application paths.

## 5.3 Validation Steps

- Ping and traceroute between critical segments
- Route table and neighbor status validation
- Failover test for link/device redundancy
- Application smoke tests from branch to HQ

## 6. Operations Runbook

## 6.1 Daily Checks

- Link health and packet loss trends
- Routing adjacency status
- Firewall policy hit anomalies
- Device resource utilization (CPU/memory/interface)

## 6.2 Incident Handling Workflow

1. Detect and classify incident impact.
2. Isolate layer (physical, routing, security, application).
3. Execute rollback or mitigation.
4. Confirm service restoration.
5. Publish RCA and preventive action.

## 7. Troubleshooting Matrix

| Symptom | Likely Cause | Validation | Action |
| --- | --- | --- | --- |
| Branch cannot reach HQ app | Route missing/filter issue | Check route table/adjacency | Update route policy or summary |
| Intermittent latency | Provider path issue or duplex mismatch | Interface errors and path trace | Escalate provider and fix interface settings |
| VLAN access denied | ACL/firewall mismatch | Policy hit logs | Correct ACL rule order and object |
| Failover not triggering | Monitoring timer/policy mismatch | HA state and health probes | Tune timers and verify probe path |

## 8. Change Management

- Record change request ID, risk level, and rollback plan
- Apply changes in maintenance windows
- Capture pre/post validation evidence
- Update network diagrams and inventory after each change

## 9. Documentation Artifacts

- High-level diagram and low-level diagram
- Device config backups
- Validation report and test logs
- Final as-built document

## 10. Revision History

| Version | Date | Author | Notes |
| --- | --- | --- | --- |
| 0.1 | 2026-05-14 | Pham Thanh Tan | Initial technical guide template |
