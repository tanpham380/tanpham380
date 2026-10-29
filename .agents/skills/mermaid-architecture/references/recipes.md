# Diagram recipes used in this repo

Each recipe is a validated starting point. Replace content, keep structure.

## 1. Dual-WAN branch to head office (used in `experiment/` §1.1)

```mermaid
graph TD
    classDef edge fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    classDef firewall fill:#ffebee,stroke:#c62828,stroke-width:2px
    classDef compute fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    classDef wan fill:#fff9c4,stroke:#fbc02d,stroke-width:1px
    classDef branch fill:#efebe9,stroke:#4e342e,stroke-width:1px

    subgraph HO["Head Office"]
        FW["Firewall"]:::firewall
        SW["Core Switch"]:::edge
        VC["vCenter / ESXi cluster"]:::compute
        FW --> SW --> VC
    end

    subgraph PA["Provider A - L2"]
        A["MPLS L2VPN"]:::wan
    end

    subgraph PB["Provider B - hybrid"]
        B1["L3 gateway 10.90.97.249"]:::wan
        B2["MPLS next-hop 192.168.1.10"]:::wan
    end

    SW -->|"management frames"| A
    SW -->|"data subnets, RIP v2"| B1
    SW -->|"untagged mgmt"| B2
```

## 2. Kubernetes HA control plane

```mermaid
graph TD
    classDef lb fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    classDef cp fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px
    classDef worker fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px

    VIP["VIP 10.0.0.100<br/>Keepalived VRRP"]:::lb
    HAP["HAProxy :6443"]:::lb
    VIP --> HAP
    HAP -->|"health check"| CP1["control-plane 1"]:::cp
    HAP -->|"health check"| CP2["control-plane 2"]:::cp
    CP1 <-->|"etcd 2379"| CP2
    W1["worker 1"]:::worker --> VIP
    W2["worker 2"]:::worker --> VIP
```

## 3. NetworkPolicy decision flow

```mermaid
flowchart TD
    classDef deny fill:#ffebee,stroke:#c62828
    classDef allow fill:#e8f5e9,stroke:#2e7d32
    classDef q fill:#e1f5fe,stroke:#0288d1

    A["Pod ingress packet"]:::q --> B{"Namespace selected by policy?"}:::q
    B -->|no| B1["Allow all - no isolation"]:::allow
    B -->|yes| C{"Pod matches podSelector?"}:::q
    C -->|no| C1["Implicit deny"]:::deny
    C -->|yes| D{"Peer in from/ports?"}:::q
    D -->|yes| D1["Allow"]:::allow
    D -->|no| D2["Implicit deny"]:::deny
```

## 4. Sequence — storage outage during backup window

```mermaid
sequenceDiagram
    autonumber
    participant B as Backup job
    participant N as NAS
    participant H as ESXi host
    participant VM as App VM
    B->>N: mount CIFS
    N-->>B: slow (IOPS saturated)
    B->>H: snapshot
    H-->>B: queued
    Note over N,H: queue depth exceeds threshold
    VM-->>B: write latency spike
    B->>N: retry with backoff
    N-->>B: complete
```

## Rendering check helper

Structural check without Node:

```bash
python3 .agents/skills/repo-hygiene/scripts/repo-audit.py
```

Visual check: paste the block into <https://mermaid.live>. With Node installed, a full render is:

```bash
# .mmd file → svg, prints nothing on success
npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o /tmp/out.svg >/dev/null && echo "OK"
```
